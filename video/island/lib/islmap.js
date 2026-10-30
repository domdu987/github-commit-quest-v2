// "ติดเกาะ" — the two islands on a 3D relief map with the squall building in the west, and the body cut-away that explains why
// seawater dries you out. Load after maps.js / mapsdata.js, tidemap.js and quakemap.js (it only borrows window.Maps at load time).
// Both scenes are redrawn every frame from one proxy tween, so seeking to any time gives the right picture. Gradients only, no filters,
// seeded RNG only. Frame both shots with a fixed identity camera: cam: { keys: [{ t: 0, ...fr(540, 960, 1, 540, 960, { drift: { s: 0 } }) }] }
//
//   Maps.VEH.boat                  a small longtail (side view, ~90 units, waterline on y 0) so Sets.mapTH can take vehicle: "boat"
//   IslMap.leg(L, id, sfx, o)      a second route on the same mapTH (o.x/o.y/o.s = the map's placement, o.route [[lon, lat]…],
//                                  o.vehicle "boat", o.to / o.toIcon / o.labDx / o.labDy / o.carS): draws the layer with ids
//                                  `${id}-${sfx}-*` (no start pin: the leg begins where the first one ended) so that
//                                  Maps.route(tl, `${id}-${sfx}`, t0, { go }) animates it after the first leg
//                                  · IslMap.TRIP = { bkk, pier, home } the lon/lat used by EP.1 (ท่าเรือฝั่งสุราษฎร์ฯ–ชุมพร, เกาะหลังเต่า สมมติ)
//   Sets.islMap3d(L, { id })       the map in L.set (#<id>-m3): the Gulf's west coast as a shelf of turquoise bands, เกาะหลังเต่า
//                                  (a hill, the village, its pier, palms) in the south-west and เกาะผี (a bare rocky hill with a strip
//                                  of beach, four palms) 4 km to the north-east, the intended course (dashed) between them, glints,
//                                  the cumulonimbus (#<id>-storm) far west, haze; draws the first frame
//   IslMap.play(tl, L, id, t0, o)  the shot: o.dur (default 9) · o.boatGo [a, b] seconds the boat runs out from the pier along the
//                                  course, reaching fraction o.boatTo (0.55) at b and holding there · o.storm { from: [u, v], to: [u, v],
//                                  r: [r0, r1], at, len } the cell's drift and growth (defaults: builds in the west from t 0 and sits over
//                                  the course by o.dur) · o.flash true lightning · o.driftAt (s) the red "blown off course" path starts
//                                  drawing from the boat toward the rocks of เกาะผี (the boat follows it) · o.labels { home, ghost,
//                                  storm, course } · o.chip (top chip text, none by default) · o.cam [{ t, u, v, tilt, yaw, S, cy }]
//                                  overrides the flight (world units: 1 = 10 m, u east, v south; the pier is at (-82, 70), เกาะผี's
//                                  beach at (196, -34)) · o.out (chip leaves)
//                                  Anchors stay above the caption band (labels clamp to y < 1400)
//   Sets.islXray(L, { id })        the X-ray of ฟ้า (hand-drawn in the channel's ink line, no rig): the hot afternoon beach behind her
//                                  (L.sky / L.far, bleached), the sand she stands on and the figure itself redrawn in L.set (#<id>-dyn),
//                                  the slab labels in L.light (#<id>-ui)
//   IslMap.xray(tl, id, t0, dur, o)  the mechanism over dur (k 0..1; o.k0 / o.k1 play part of it, o.ease; o.mix true = the last drops
//                                  of a fresh-water bottle fall into the cup first, k 0–.08): she lifts the plastic cup of seawater and
//                                  drinks (k .0–.2, label "ดื่ม 1 แก้ว" at .15) · her body turns to glass, a film X-ray: ribs, the
//                                  gullet, the two kidneys, the water inside her shown as a sea with a glinting horizon (k .1–.3) ·
//                                  the seawater runs down the gullet as a sparkling stream of salt crystals that gather at the
//                                  kidneys, which glow (k .2–.45, sentence "ไตคนทำปัสสาวะได้ แค่จืดกว่าน้ำทะเล" at .45) · the sea inside her
//                                  draws back like a falling tide while the lost water seeps down her legs into the sand, the wet ring
//                                  under her feet growing wider than a cup's worth (k .4–.75, label "เสียน้ำ มากกว่า 1 แก้ว" at .6) ·
//                                  the glass fades back to skin, the scene camera pushes in on her face: cracked lips, sweat, dull eyes
//                                  (k .8–1, "ยิ่งดื่ม ยิ่งกระหาย" at .85). No stamp. Texts from ARC S1 (NOAA). o.labels { cup, lost,
//                                  kidney, thirst } override. Suggested: know1 = k 0–.6, know2 = k .6–1
//   (Sets.islBody / IslMap.kidney, the older jar diorama, are kept only so old test shots still build; do not use them)
(function () {
  const f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const mk = (seed) => () => { seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const PI = Math.PI, RAD = PI / 180, INK = "#2e2a26";
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const smooth = (k) => { k = clamp(k); return k * k * (3 - 2 * k); };
  const ease3 = (k) => { k = clamp(k); return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
  const backOut = (k, s = 2.2) => { k = clamp(k) - 1; return 1 + (s + 1) * k * k * k + s * k * k; };
  const bounceOut = (k) => { k = clamp(k); const n = 7.5625, d = 2.75; if (k < 1 / d) return n * k * k; if (k < 2 / d) return n * (k -= 1.5 / d) * k + 0.75; if (k < 2.5 / d) return n * (k -= 2.25 / d) * k + 0.9375; return n * (k -= 2.625 / d) * k + 0.984375; };
  const lerp = (a, b, k) => a + (b - a) * k;
  const hx = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, b, k) => { const A = hx(a), B = hx(b); k = clamp(k); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, "0")).join(""); };
  const hash = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  const IslMap = (window.IslMap = window.IslMap || {});

  Sets.DEFS += `
    <linearGradient id="isMapSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8d4ea"/><stop offset=".5" stop-color="#d7ecf2"/><stop offset="1" stop-color="#eef6f2"/></linearGradient>
    <linearGradient id="isHaze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dcedf2" stop-opacity=".97"/><stop offset=".5" stop-color="#dcedf2" stop-opacity=".55"/><stop offset="1" stop-color="#dcedf2" stop-opacity="0"/></linearGradient>
    <radialGradient id="isCloudW"><stop offset="0" stop-color="#ffffff" stop-opacity=".98"/><stop offset=".6" stop-color="#f6fafc" stop-opacity=".9"/><stop offset="1" stop-color="#e8f0f4" stop-opacity="0"/></radialGradient>
    <radialGradient id="isCloudG"><stop offset="0" stop-color="#8e9ead" stop-opacity=".97"/><stop offset=".65" stop-color="#6c7c8c" stop-opacity=".9"/><stop offset="1" stop-color="#55636f" stop-opacity="0"/></radialGradient>
    <radialGradient id="isCloudD"><stop offset="0" stop-color="#44525e" stop-opacity=".95"/><stop offset=".7" stop-color="#3a4854" stop-opacity=".8"/><stop offset="1" stop-color="#2e3a44" stop-opacity="0"/></radialGradient>
    <radialGradient id="isStormShade"><stop offset="0" stop-color="#0a1e30" stop-opacity=".45"/><stop offset=".7" stop-color="#0a1e30" stop-opacity=".2"/><stop offset="1" stop-color="#0a1e30" stop-opacity="0"/></radialGradient>
    <radialGradient id="isBolt"><stop offset="0" stop-color="#fffce0" stop-opacity=".95"/><stop offset=".4" stop-color="#ffe08a" stop-opacity=".45"/><stop offset="1" stop-color="#ffe08a" stop-opacity="0"/></radialGradient>
    <radialGradient id="isSoft"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <linearGradient id="isPillD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#20384a"/><stop offset="1" stop-color="#0a1620"/></linearGradient>
    <linearGradient id="isPillC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf6"/><stop offset="1" stop-color="#eadcbc"/></linearGradient>
    <linearGradient id="isPillR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8a6a"/><stop offset="1" stop-color="#c0281e"/></linearGradient>
    <linearGradient id="isBodySky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fcbe6"/><stop offset=".5" stop-color="#cfe9f0"/><stop offset="1" stop-color="#f6efdc"/></linearGradient>
    <linearGradient id="isBodyFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eadfc4" stop-opacity="0"/><stop offset=".3" stop-color="#e2d2ae"/><stop offset="1" stop-color="#cdb98f"/></linearGradient>
    <linearGradient id="isSkin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f3cfae"/><stop offset="1" stop-color="#dba985"/></linearGradient>
    <linearGradient id="isGlass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset=".5" stop-color="#ffffff" stop-opacity=".12"/><stop offset="1" stop-color="#ffffff" stop-opacity=".4"/></linearGradient>
    <linearGradient id="isSea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fe0e8"/><stop offset="1" stop-color="#2a9ac4"/></linearGradient>
    <linearGradient id="isUrine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe98a"/><stop offset="1" stop-color="#e8b83a"/></linearGradient>
    <linearGradient id="isBodyWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fe4ff" stop-opacity=".85"/><stop offset="1" stop-color="#3aa0d8" stop-opacity=".9"/></linearGradient>
    <linearGradient id="isKidney" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8745a"/><stop offset="1" stop-color="#9a3a2e"/></linearGradient>
    <linearGradient id="isStomach" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0a890"/><stop offset="1" stop-color="#c96a56"/></linearGradient>
    <radialGradient id="isSaltG"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#dfe8f0"/></radialGradient>
    <linearGradient id="isXSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb6e4"/><stop offset=".45" stop-color="#cfe7f0"/><stop offset=".7" stop-color="#f6f3e6"/><stop offset="1" stop-color="#fff8ea"/></linearGradient>
    <linearGradient id="isXSand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf3dc"/><stop offset="1" stop-color="#e9d7b0"/></linearGradient>
    <radialGradient id="isXHeat" cx=".5" cy=".3" r=".7"><stop offset="0" stop-color="#ffffff" stop-opacity=".75"/><stop offset=".6" stop-color="#ffffff" stop-opacity=".2"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
    <linearGradient id="isXGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e6f7ff" stop-opacity=".82"/><stop offset=".5" stop-color="#b4e2f6" stop-opacity=".7"/><stop offset="1" stop-color="#7fc4e6" stop-opacity=".85"/></linearGradient>
    <linearGradient id="isXWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fe3ff" stop-opacity=".92"/><stop offset=".5" stop-color="#3fb4e0"/><stop offset="1" stop-color="#1c6fa8"/></linearGradient>
    <linearGradient id="isXKid" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e38a74"/><stop offset="1" stop-color="#a84434"/></linearGradient>
    <radialGradient id="isXKidGlow"><stop offset="0" stop-color="#ff6a4a" stop-opacity=".8"/><stop offset="1" stop-color="#ff6a4a" stop-opacity="0"/></radialGradient>
    <radialGradient id="isXWet"><stop offset="0" stop-color="#9a7a4e" stop-opacity=".9"/><stop offset=".75" stop-color="#b8976a" stop-opacity=".75"/><stop offset="1" stop-color="#c8ab80" stop-opacity="0"/></radialGradient>
    <linearGradient id="isXWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4e2bf"/><stop offset="1" stop-color="#d9bd8a"/></linearGradient>
    <linearGradient id="isXTee" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b6ecd8"/><stop offset="1" stop-color="#7fcdb4"/></linearGradient>
    <linearGradient id="isXHair" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7a4f33"/><stop offset="1" stop-color="#4b2e1b"/></linearGradient>`;

  // ======================================================================================================================
  // ---------------- 1. the travel map: a boat for Sets.mapTH, and a second leg on the same map ----------------
  const boatSide = () => `<path d="M-46,-6C-36,6 -4,12 30,8L48,-2L42,-14L30,-10C0,-6 -26,-6 -38,-16Z" fill="#f2c030" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M-40,-14C-20,-6 10,-6 40,-12" stroke="#2a5ab8" stroke-width="5" fill="none"/><path d="M-10,-6h34" stroke="#2a5ab8" stroke-width="3" opacity=".7"/>
    <path d="M-14,-10v-14h12v14" fill="#3a6aa8" stroke="${INK}" stroke-width="2.5"/><path d="M30,-10l16,-14" stroke="${INK}" stroke-width="4" stroke-linecap="round"/><path d="M46,-24l10,-3l-4,8l8,2l-12,4" fill="#e2382e" stroke="${INK}" stroke-width="2"/>
    <path d="M-46,-6q-14,4 -22,2" stroke="#8a9296" stroke-width="4" stroke-linecap="round"/><ellipse cx="2" cy="6" rx="52" ry="5" fill="#2a9ac4" opacity=".35"/>`;
  if (window.Maps && Maps.VEH) Maps.VEH.boat = boatSide;
  IslMap.TRIP = { bkk: [100.52, 13.75], pier: [99.32, 9.86], home: [100.02, 9.78] };
  const pinSVG = (fill, inner) => `<path d="M0,0C-6,-16 -30,-34 -30,-58A30,30 0 1 1 30,-58C30,-34 6,-16 0,0Z" fill="url(#${fill})" stroke="${INK}" stroke-width="3"/><circle cx="0" cy="-58" r="18" fill="#fffaf0"/><g transform="translate(0,-58)">${inner}</g><path d="M-18,-74Q-12,-84 -2,-86" stroke="#fff" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/>`;
  const labelSVG = (text) => { const w = Math.round(text.length * 32 * 0.56 + 44); return `<rect x="${-w / 2}" y="-30" width="${w}" height="56" rx="28" fill="#fffaf0" stroke="${INK}" stroke-width="3"/><text x="0" y="10" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="32" fill="${INK}">${text}</text>`; };
  function leg(L, id, sfx, o = {}) {
    const lid = `${id}-${sfx}`, X = o.x ?? 90, Y = o.y ?? 300, S = o.s ?? 1, pts = (o.route || []).map(([lo, la]) => Maps.P(lo, la));
    const rd = Maps.smooth(pts), [a, b] = [pts[0], pts[pts.length - 1]];
    let m = `<defs><mask id="${lid}-rm" maskUnits="userSpaceOnUse" x="-500" y="-500" width="2000" height="2400"><path id="${lid}-reveal" d="${rd}" stroke="#fff" stroke-width="40" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></mask></defs>
      <g mask="url(#${lid}-rm)"><path d="${rd}" stroke="#fffaf0" stroke-width="16" fill="none" stroke-linecap="round" opacity=".9"/><path d="${rd}" stroke="#2a6ad0" stroke-width="8" fill="none" stroke-linecap="round" stroke-dasharray="18 14"/></g>
      <path id="${lid}-path" d="${rd}" fill="none" stroke="none"/>`;
    // no start pin and no start label: the leg begins where the first one ended (empty groups keep Maps.route happy)
    m += `<g transform="translate(${f1(a[0])},${f1(a[1])})"><g id="${lid}-sh0"></g></g><g transform="translate(${f1(a[0])},${f1(a[1])})"><g id="${lid}-pin0"></g></g><g id="${lid}-lab0"></g>`;
    m += `<g transform="translate(${f1(b[0])},${f1(b[1])})"><g id="${lid}-sh1"><ellipse cx="0" cy="0" rx="16" ry="6" fill="#3a2a10" opacity=".35"/></g></g>`;
    m += `<g transform="translate(${f1(b[0])},${f1(b[1])})"><g id="${lid}-pin1">${pinSVG("mpPin", o.toIcon || `<circle r="7" fill="#c8241e"/>`)}</g></g>`;
    if (o.to) m += `<g transform="translate(${f1(b[0] + (o.labDx ?? 0))},${f1(b[1] - 128 + (o.labDy ?? 0))})"><g id="${lid}-lab1">${labelSVG(o.to)}</g></g>`;
    m += `<g transform="translate(${f1(b[0])},${f1(b[1])})"><g id="${lid}-rip" opacity="0"><circle r="34" fill="none" stroke="#2a6ad0" stroke-width="5"/></g></g>`;
    m += `<g id="${lid}-car" transform="translate(${f1(a[0])},${f1(a[1])})"><g transform="scale(${o.carS ?? 1})"><g id="${lid}-bob">${(Maps.VEH[o.vehicle] || Maps.VEH.boat)()}</g></g></g>`;
    put(L.set, `<g transform="translate(${X},${Y}) scale(${S})">${m}</g>`);
  }
  IslMap.leg = leg;

  // ======================================================================================================================
  // ---------------- 2. the two islands on a 3D relief map, the squall building in the west ----------------
  const F = 2500, LN = (() => { const v = [-0.55, -0.62, 0.62], l = Math.hypot(...v); return v.map((x) => x / l); })();
  // world: 1 unit = 10 m, u east, v south · เกาะหลังเต่า round (-250, 70), เกาะผี round (200, -70): 4.6 km apart
  const HOME = { c: [-250, 70], rx: 132, ry: 86, seed: 11, z: 7 }, GHOST = { c: [200, -70], rx: 44, ry: 31, seed: 23, z: 6 };
  const PIER = [[-124, 64], [-80, 66], [-80, 75], [-124, 76]], PIER_END = [-82, 70], BEACH = [196, -34], ROCKS = [180, -96];
  const COURSE = [[-82, 70], [-30, 52], [50, 22], [130, -8], [196, -34]];
  const DRIFT = [[50, 22], [96, -8], [138, -52], [166, -80], [180, -96]];
  const blobRing = (B) => { const g = mk(B.seed), n = 26; const pts = []; for (let i = 0; i < n; i++) { const a = (i / n) * PI * 2, w = 1 + 0.16 * Math.sin(a * 3 + g() * 2) + 0.1 * Math.sin(a * 5 + g() * 3); pts.push([B.c[0] + Math.cos(a) * B.rx * w, B.c[1] + Math.sin(a) * B.ry * w]); } return chaikin(pts, 2); };
  const chaikin = (pts, it) => { for (let k = 0; k < it; k++) { const out = []; for (let i = 0; i < pts.length; i++) { const a = pts[i], b = pts[(i + 1) % pts.length]; out.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25], [a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); } pts = out; } return pts; };
  const area = (r) => { let A = 0; for (let i = 0; i < r.length; i++) { const a = r[i], b = r[(i + 1) % r.length]; A += a[0] * b[1] - b[0] * a[1]; } return A / 2; };
  const normals = (pts) => { const s = area(pts) > 0 ? 1 : -1; return pts.map((a, i) => { const b = pts[(i + 1) % pts.length], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1; return [(s * dy) / l, (-s * dx) / l]; }); };
  const offset = (pts, d) => { const n = normals(pts); return chaikin(pts.map((p, i) => { const m = n[(i - 1 + pts.length) % pts.length], q = n[i], vx = (m[0] + q[0]) / 2, vy = (m[1] + q[1]) / 2; return [p[0] + vx * d, p[1] + vy * d]; }), 1); };
  const catmull = (pts, n = 12) => { const out = []; for (let i = 0; i < pts.length - 1; i++) { const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2; for (let q = 0; q < n; q++) { const t = q / n, t2 = t * t, t3 = t2 * t; out.push([0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3), 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)]); } } out.push(pts[pts.length - 1]); return out; };
  const along = (poly, k) => { let tot = 0; const L = [0]; for (let i = 1; i < poly.length; i++) { tot += Math.hypot(poly[i][0] - poly[i - 1][0], poly[i][1] - poly[i - 1][1]); L.push(tot); } const d = clamp(k) * tot; for (let i = 1; i < poly.length; i++) if (L[i] >= d) { const q = (d - L[i - 1]) / Math.max(1e-6, L[i] - L[i - 1]); return [lerp(poly[i - 1][0], poly[i][0], q), lerp(poly[i - 1][1], poly[i][1], q), Math.atan2(poly[i][1] - poly[i - 1][1], poly[i][0] - poly[i - 1][0])]; } return [...poly[poly.length - 1], 0]; };
  // camera (same model as tidemap.js, in world units)
  function camAt(keys, t) {
    let i = 0; while (i + 1 < keys.length && keys[i + 1].t <= t) i++;
    const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
    if (a === b || t <= a.t) return { ...a };
    const k = clamp((t - a.t) / (b.t - a.t)), e = i === 0 ? smooth(k) : ease3(k), S = a.S * Math.pow(b.S / a.S, e), w = 1 - (1 - e) * (a.S / S);
    return { u: a.u + (b.u - a.u) * w, v: a.v + (b.v - a.v) * w, tilt: lerp(a.tilt, b.tilt, e), yaw: lerp(a.yaw, b.yaw, e), S, cy: lerp(a.cy, b.cy, e) };
  }
  function camera(c) {
    const t = c.tilt * RAD, y = c.yaw * RAD, dist = F / c.S, C = { u: c.u, v: c.v, st: Math.sin(t), ct: Math.cos(t), sy: Math.sin(y), cyw: Math.cos(y), dist, S: c.S, cx: 540, cy: c.cy, tilt: c.tilt };
    C.gu = c.u - dist * C.st * C.sy; C.gv = c.v + dist * C.st * C.cyw; C.gz = dist * C.ct; C.near = dist * 0.16;
    return C;
  }
  const proj = (C, u, v, z) => { const dx = u - C.u, dy = v - C.v, x = dx * C.cyw + dy * C.sy, y = -dx * C.sy + dy * C.cyw, dep = C.dist - y * C.st - z * C.ct; return [C.cx + (F * x) / dep, C.cy + (F * (y * C.ct - z * C.st)) / dep, dep]; };
  const nearFn = (C, z) => { const lim = (C.dist - C.near - z * C.ct) / C.st; return (p) => lim - (-(p[0] - C.u) * C.sy + (p[1] - C.v) * C.cyw); };
  function clipEdge(pts, fn) { const out = [], n = pts.length; for (let i = 0; i < n; i++) { const a = pts[i], b = pts[(i + 1) % n], fa = fn(a), fb = fn(b); if (fa >= 0) out.push(a); if ((fa >= 0) !== (fb >= 0)) { const k = fa / (fa - fb); out.push([a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]); } } return out; }
  function clipRingE(pts, fn) { const n = pts.length, f = pts.map(fn); if (f.every((x) => x >= 0)) return pts.map((p, i) => [p[0], p[1], i]); const out = []; for (let i = 0; i < n; i++) { const j = (i + 1) % n, a = pts[i], b = pts[j]; if (f[i] >= 0) out.push([a[0], a[1], i]); if ((f[i] >= 0) !== (f[j] >= 0)) { const k = f[i] / (f[i] - f[j]); out.push([a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, f[i] >= 0 ? -1 : i]); } } return out; }
  const pathOf = (pp) => { let s = ""; for (let i = 0; i < pp.length; i++) s += (i ? "L" : "M") + f1(pp[i][0]) + "," + f1(pp[i][1]); return s; };
  const ringPath = (C, pts, z, fn) => { const c = clipEdge(pts, fn); return c.length >= 3 ? pathOf(c.map((p) => proj(C, p[0], p[1], z))) + "Z" : ""; };
  const segClip = (a, b, fn) => { const fa = fn(a), fb = fn(b); if (fa < 0 && fb < 0) return null; if (fa >= 0 && fb >= 0) return [a, b]; const k = fa / (fa - fb), m = [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]; return fa >= 0 ? [a, m] : [m, b]; };
  const lineOf = (C, pts, z, fn) => { let s = "", pen = false; for (let i = 0; i + 1 < pts.length; i++) { const sg = segClip(pts[i], pts[i + 1], fn); if (!sg) { pen = false; continue; } const p = proj(C, sg[0][0], sg[0][1], z), q = proj(C, sg[1][0], sg[1][1], z); if (!pen || sg[0] !== pts[i]) s += `M${f1(p[0])},${f1(p[1])}`; s += `L${f1(q[0])},${f1(q[1])}`; pen = sg[1] === pts[i + 1]; } return s; };
  const circ = (u, v, r, n = 36, ry = r) => Array.from({ length: n }, (_, i) => [u + Math.cos((i / n) * PI * 2) * r, v + Math.sin((i / n) * PI * 2) * ry]);
  const inside = (ring, x, y) => { let c = false; for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) { const [xi, yi] = ring[i], [xj, yj] = ring[j]; if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c; } return c; };

  let MD = null;
  function mapData() {
    if (MD) return MD;
    const isl = [HOME, GHOST].map((B) => { const pts = blobRing(B); return { B, pts, n: normals(pts), z: B.z, inner: offset(pts, -9), bands: [26, 64, 130].map((d) => offset(pts, d)) }; });
    const r = mk(5);
    const palms = [];
    isl.forEach((I, k) => { const n = k ? 5 : 16; for (let i = 0; i < n; i++) { const a = (i / n) * PI * 2 + r() * 0.3, w = 0.78 + r() * 0.12; palms.push([I.B.c[0] + Math.cos(a) * I.B.rx * w, I.B.c[1] + Math.sin(a) * I.B.ry * w, I.z, 0.9 + r() * 0.4, (r() - 0.5) * 0.5]); } });
    const huts = []; const rh = mk(9);
    for (let i = 0; i < 9; i++) huts.push([-170 + rh() * 44, 46 + rh() * 44, HOME.z, 0.8 + rh() * 0.4, ["#d8503a", "#3a8ac8", "#e8c040", "#b8b0a0"][i % 4]]);
    const hills = [{ u: -292, v: 64, z: HOME.z, h: 30, r: 44, karst: false, base: Array.from({ length: 7 }, (_, i) => { const a = (i / 7) * PI * 2; return [Math.cos(a) * 44 * (0.8 + hash(i + 3) * 0.3), Math.sin(a) * 36 * (0.8 + hash(i + 7) * 0.3)]; }), au: -6, av: 4 },
      { u: -236, v: 90, z: HOME.z, h: 14, r: 26, karst: false, base: Array.from({ length: 6 }, (_, i) => { const a = (i / 6) * PI * 2; return [Math.cos(a) * 26 * (0.8 + hash(i + 13) * 0.3), Math.sin(a) * 22 * (0.8 + hash(i + 17) * 0.3)]; }), au: 3, av: -2 },
      { u: 199, v: -76, z: GHOST.z, h: 24, r: 20, karst: true, base: Array.from({ length: 7 }, (_, i) => { const a = (i / 7) * PI * 2; return [Math.cos(a) * 21 * (0.8 + hash(i + 23) * 0.3), Math.sin(a) * 16 * (0.8 + hash(i + 29) * 0.3)]; }), au: 2, av: -2 }];
    const rg = mk(211), glints = [];
    for (let k = 0; glints.length < 220 && k < 4000; k++) { const u = -900 + rg() * 1800, v = -700 + rg() * 1300; if (isl.some((I) => inside(I.bands[0], u, v))) continue; glints.push([u, v, 2 + rg() * 5, rg() * 6, 0.6 + rg() * 0.8]); }
    const rr = mk(61), rain = Array.from({ length: 110 }, () => { const a = rr() * PI * 2, d = Math.sqrt(rr()); return [Math.cos(a) * d, Math.sin(a) * d * 0.72, rr(), 0.35 + rr() * 0.5]; });
    const caps = Array.from({ length: 70 }, () => { const a = rr() * PI * 2, d = Math.sqrt(rr()); return [Math.cos(a) * d, Math.sin(a) * d * 0.72, rr() * 6, 8 + rr() * 16]; });
    const rc = mk(33), puffs = Array.from({ length: 12 }, (_, i) => [(i / 12) * PI * 2 + rc() * 0.4, 0.55 + rc() * 0.4, 0.4 + rc() * 0.4, rc()]);
    MD = { isl, palms, huts, hills, glints, rain, caps, puffs, course: catmull(COURSE, 14), drift: catmull(DRIFT, 12) };
    return MD;
  }
  // 2.5D pills in screen space (constant size), same look as the channel's maps
  const pill = (w, h, o = {}) => { const r = o.r ?? h / 2, face = o.face || "url(#isPillD)", slab = o.slab || "#02060a", st = o.stroke || "#140e0a"; return `<ellipse cx="0" cy="${f1(h / 2 + 18)}" rx="${f1(w * 0.46)}" ry="14" fill="url(#isSoft)"/><rect x="${f1(-w / 2)}" y="${f1(-h / 2 + 9)}" width="${w}" height="${h}" rx="${r}" fill="${slab}" stroke="#140e0a" stroke-width="4"/><rect x="${f1(-w / 2)}" y="${f1(-h / 2)}" width="${w}" height="${h}" rx="${r}" fill="${face}" stroke="${st}" stroke-width="${o.sw ?? 4.5}"/><path d="M${f1(-w / 2 + r * 0.9)},${f1(-h / 2 + 7)}H${f1(w / 2 - r * 0.9)}" stroke="#fff" stroke-width="3.5" opacity="${o.hi ?? 0.28}" stroke-linecap="round"/>`; };
  const vis = (t) => t.replace(/[ัิ-ฺ็-๎]/g, "").length;
  const tagAt = (x, y, txt, o = {}) => { const fs = o.fs || 30, w = vis(txt) * fs * 0.56 + 56, h = fs + 26; return `<g transform="translate(${f1(x)},${f1(y)})" opacity="${f1(o.op ?? 1)}">${pill(w, h, o)}<text y="${f1(fs * 0.36)}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="${fs}" fill="${o.fill || "#fff6e8"}">${txt}</text></g>`; };
  // the storm's position, radius and build at time t
  function stormAt(o, t) {
    const s = o.storm || {}, from = s.from || [-600, -150], to = s.to || [-40, -40], r = s.r || [60, 175], at = s.at ?? 0, len = s.len ?? o.dur ?? 9;
    const k = smooth((t - at) / len), q = clamp((t - at) / len);
    return { u: lerp(from[0], to[0], k), v: lerp(from[1], to[1], k), r: lerp(r[0], r[1], smooth(q * 1.15)), grow: smooth(q * 1.3) };
  }
  const flashAt = (t) => { const c = Math.floor(t / 1.15), p = t - c * 1.15; if (hash(c + 5) < 0.4) return 0; const a = p < 0.11 ? 1 - p / 0.11 : p > 0.17 && p < 0.26 ? 0.6 * (1 - (p - 0.17) / 0.09) : 0; return a; };
  const palmIcon = (s, lean) => `<g transform="scale(${f1(s)})"><path d="M0,0C${f1(lean * 10)},-14 ${f1(lean * 16)},-26 ${f1(lean * 20)},-38" stroke="#7a5a36" stroke-width="3.2" fill="none" stroke-linecap="round"/>${[-150, -100, -50, 0, 50, 100, 150].map((a) => `<path d="M${f1(lean * 20)},-38q${f1(9 * Math.cos(((a - 90) * PI) / 180))},${f1(-5 + 7 * Math.sin(((a - 90) * PI) / 180))} ${f1(17 * Math.cos(((a - 90) * PI) / 180))},${f1(5 + 10 * Math.sin(((a - 90) * PI) / 180))}" stroke="${a % 100 ? "#2f8a3e" : "#4aa84e"}" stroke-width="3" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
  const hutIcon = (s, c) => `<g transform="scale(${f1(s)})"><path d="M-9,0v-8h18v8Z" fill="#d8aa70" stroke="${INK}" stroke-width="1.6"/><path d="M-12,-8l12,-9l12,9Z" fill="${c}" stroke="${INK}" stroke-width="1.6" stroke-linejoin="round"/><rect x="-2" y="-6" width="4" height="6" fill="#4a3a2a"/></g>`;
  const boatTop = (s, a) => `<g transform="rotate(${f1(a)}) scale(${f1(s)})"><path d="M-34,0C-30,-9 -6,-12 22,-9L40,0L22,9C-6,12 -30,9 -34,0Z" fill="#f2c030" stroke="${INK}" stroke-width="2.6" stroke-linejoin="round"/><path d="M-26,0h50" stroke="#2a5ab8" stroke-width="4" opacity=".85"/><rect x="-10" y="-5" width="12" height="10" rx="2" fill="#3a6aa8" stroke="${INK}" stroke-width="1.6"/><circle cx="12" cy="0" r="3.2" fill="#d8302a"/><path d="M-34,0l-12,0" stroke="#8a9296" stroke-width="3.5" stroke-linecap="round"/></g>`;

  function frame3d(inst, t) {
    const Dd = mapData(), o = inst.o, C = camera(camAt(inst.keys, t)), z0f = nearFn(C, 0), S = C.S, out = [];
    const st = stormAt(o, t), fl = o.flash === false ? 0 : flashAt(t);
    // the sea: a dark plane, the shelf bands round the islands, glints
    out.push(`<path d="${ringPath(C, [[-2600, -2200], [2600, -2200], [2600, 2200], [-2600, 2200]], 0, z0f)}" fill="#1b6a98"/>`);
    out.push(`<path d="${ringPath(C, [[-2600, -2200], [2600, -2200], [2600, -520], [-2600, -520]], 0, z0f)}" fill="#174f7e" opacity=".9"/>`);
    [["#2b95ba", 2], ["#46b9c8", 1], ["#8fe0d8", 0]].forEach(([col, bi]) => { let d = ""; Dd.isl.forEach((I) => (d += ringPath(C, I.bands[bi], 0, z0f))); if (d) out.push(`<path d="${d}" fill="${col}" stroke="${mix(col, "#ffffff", 0.3)}" stroke-width="${f1(clamp(0.5 * S, 1, 2.4))}" stroke-opacity=".5" stroke-linejoin="round"/>`); });
    let gl = "";
    Dd.glints.forEach(([u, v, l, ph, sp]) => { const op = 0.5 + 0.5 * Math.sin(t * 2.2 * sp + ph); if (op < 0.3) return; const uu = u + ((t * 2.4 * sp + ph * 9) % 18) - 9, sg = segClip([uu - l, v], [uu + l, v], z0f); if (!sg) return; const a = proj(C, sg[0][0], sg[0][1], 0), b = proj(C, sg[1][0], sg[1][1], 0); gl += `M${f1(a[0])},${f1(a[1])}L${f1(b[0])},${f1(b[1])}`; });
    out.push(`<path d="${gl}" stroke="#f2fcff" stroke-width="${f1(clamp(0.5 * S, 1.2, 3))}" stroke-linecap="round" opacity=".45"/>`);
    // the storm's shadow and the whitecaps under it
    const shd = ringPath(C, circ(st.u + st.r * 0.2, st.v + st.r * 0.25, st.r * 1.2, 36, st.r * 0.9), 0, z0f);
    if (shd) out.push(`<path d="${shd}" fill="url(#isStormShade)" opacity="${f1(0.4 + 0.6 * st.grow)}"/>`);
    let wc = "";
    Dd.caps.forEach(([cx, cy, ph, ln], k) => { const q = (ph + t * 1.6) % 6, u = st.u + cx * st.r * 1.05 + q * 4, v = st.v + cy * st.r * 1.05, sg = segClip([u - ln * 0.5, v], [u + ln * 0.5, v], z0f); if (!sg) return; const a = proj(C, sg[0][0], sg[0][1], 0.3), b = proj(C, sg[1][0], sg[1][1], 0.3); wc += `M${f1(a[0])},${f1(a[1])}L${f1(b[0])},${f1(b[1])}`; });
    out.push(`<path d="${wc}" stroke="#ffffff" stroke-width="${f1(clamp(0.9 * S, 1.4, 4))}" stroke-linecap="round" opacity="${f1(0.35 + 0.5 * st.grow)}"/>`);
    // the course (dashed) and the drift (red) the boat gets blown onto
    const bg = o.boatGo || [0.6, o.dur ?? 9], bk = clamp((t - bg[0]) / Math.max(0.1, bg[1] - bg[0]));
    out.push(`<path d="${lineOf(C, Dd.course, 0.4, z0f)}" stroke="#fffaf0" stroke-width="${f1(clamp(2.2 * S, 3, 9))}" fill="none" stroke-linecap="round" opacity=".55" stroke-dasharray="${f1(clamp(7 * S, 9, 26))} ${f1(clamp(5 * S, 7, 18))}"/>`);
    let dk = 0;
    if (o.driftAt !== undefined && t > o.driftAt) { dk = smooth((t - o.driftAt) / (o.driftLen ?? 2.2)); const n = Math.max(2, Math.round(Dd.drift.length * dk)); out.push(`<path d="${lineOf(C, Dd.drift.slice(0, n), 0.5, z0f)}" stroke="#2a0a06" stroke-width="${f1(clamp(3.4 * S, 5, 13))}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/><path d="${lineOf(C, Dd.drift.slice(0, n), 0.5, z0f)}" stroke="#ff4a3a" stroke-width="${f1(clamp(1.6 * S, 2.5, 7))}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`); }
    // the islands: walls shaded by the light, tops (sand with a green heart), the pier, then the things that stand up (far to near)
    const objs = [];
    Dd.isl.forEach((I) => {
      const c = clipRingE(I.pts, nearFn(C, I.z)), q = ["", "", "", "", "", ""];
      let foam = "";
      for (let i = 0; i < c.length; i++) { const a = c[i], b = c[(i + 1) % c.length], e = a[2]; if (e < 0) continue; const n = I.n[e], mu = (a[0] + b[0]) / 2, mv = (a[1] + b[1]) / 2; if ((C.gu - mu) * n[0] + (C.gv - mv) * n[1] <= 0) continue; const lit = clamp(0.5 + 0.62 * (n[0] * LN[0] + n[1] * LN[1])); const A0 = proj(C, a[0], a[1], 0), B0 = proj(C, b[0], b[1], 0), B1 = proj(C, b[0], b[1], I.z), A1 = proj(C, a[0], a[1], I.z); q[Math.round(lit * 5)] += `M${f1(A0[0])},${f1(A0[1])}L${f1(B0[0])},${f1(B0[1])}L${f1(B1[0])},${f1(B1[1])}L${f1(A1[0])},${f1(A1[1])}Z`; foam += `M${f1(A0[0])},${f1(A0[1])}L${f1(B0[0])},${f1(B0[1])}`; }
      q.forEach((d, k) => { if (d) out.push(`<path d="${d}" fill="${mix("#7a5a3a", "#e6cc9a", k / 5)}" stroke="${mix("#7a5a3a", "#e6cc9a", k / 5)}" stroke-width=".8" stroke-linejoin="round"/>`); });
      if (foam) out.push(`<path d="${foam}" stroke="#f2fdff" stroke-width="${f1(clamp(1.2 * S, 2, 6))}" opacity=".85" fill="none" stroke-linecap="round"/>`);
      const top = ringPath(C, I.pts, I.z, nearFn(C, I.z)), heart = ringPath(C, I.inner, I.z + 0.2, nearFn(C, I.z));
      out.push(`<path d="${top}" fill="#f4e7c4" stroke="#b58e5c" stroke-width="1.8" stroke-linejoin="round"/>`);
      if (heart) out.push(`<path d="${heart}" fill="${I.B === GHOST ? "#8aa06a" : "#6fae58"}" opacity=".92"/>`);
    });
    // the pier: a slab on posts, a hut at its end
    { const pz = HOME.z - 2.5, pr = ringPath(C, PIER, pz, nearFn(C, pz)); if (pr) { const sh = ringPath(C, PIER.map((p) => [p[0] + 2, p[1] + 3]), 0.2, z0f); out.push(`<path d="${sh}" fill="#04243c" opacity=".25"/><path d="${pr}" fill="#c9a06a" stroke="#6a4a2a" stroke-width="1.4"/>`); } }
    const cam3 = [C.gu, C.gv, C.gz];
    const face = (pts3, base) => { const [a, b, c] = pts3, ux = b[0] - a[0], uy = b[1] - a[1], uz = b[2] - a[2], vx = c[0] - a[0], vy = c[1] - a[1], vz = c[2] - a[2]; let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx; const l = Math.hypot(nx, ny, nz) || 1; nx /= l; ny /= l; nz /= l; const cx = pts3.reduce((s, p) => s + p[0], 0) / 3, cy = pts3.reduce((s, p) => s + p[1], 0) / 3, cz = pts3.reduce((s, p) => s + p[2], 0) / 3; if (nx * (cx - base[0]) + ny * (cy - base[1]) + nz * (cz - base[2]) < 0) { nx = -nx; ny = -ny; nz = -nz; } if (nx * (cam3[0] - cx) + ny * (cam3[1] - cy) + nz * (cam3[2] - cz) <= 0) return null; return { lit: clamp(0.3 + 0.75 * Math.max(0, nx * LN[0] + ny * LN[1] + nz * LN[2])), pp: pts3.map((p) => proj(C, p[0], p[1], p[2])) }; };
    Dd.hills.forEach((pk) => {
      const pc = proj(C, pk.u, pk.v, pk.z); if (pc[2] < C.near * 1.2) return;
      const ap = [pk.u + pk.au, pk.v + pk.av, pk.z + pk.h], ctr = [pk.u, pk.v, pk.z], nb = pk.base.length; let s = "";
      const lit0 = pk.karst ? "#5a6a60" : "#4f6a3a", lit1 = pk.karst ? "#cfd4c2" : "#cfd08e";
      for (let i = 0; i < nb; i++) { const b0 = pk.base[i], b1 = pk.base[(i + 1) % nb], f = face([[pk.u + b0[0], pk.v + b0[1], pk.z], [pk.u + b1[0], pk.v + b1[1], pk.z], ap], ctr); if (!f) continue; const col = mix(lit0, lit1, Math.pow(f.lit, 1.25)); s += `<path d="${pathOf(f.pp)}Z" fill="${col}" stroke="${mix(col, "#2a3018", 0.45)}" stroke-width="1" stroke-linejoin="round"/>`; }
      if (pk.karst) { const tp = proj(C, ...ap); s += `<circle cx="${f1(tp[0])}" cy="${f1(tp[1])}" r="${f1(clamp(3 * S, 2, 9))}" fill="#4f8a46" stroke="#24401f" stroke-width="1"/>`; }
      objs.push([pc[2], s]);
    });
    Dd.huts.forEach(([u, v, z, s0, c]) => { const p = proj(C, u, v, z); if (p[2] < C.near * 1.2) return; objs.push([p[2], `<g transform="translate(${f1(p[0])},${f1(p[1])})">${hutIcon(clamp((s0 * F * 0.75) / p[2], 0.5, 3.2), c)}</g>`]); });
    { const p = proj(C, PIER_END[0] - 6, PIER_END[1], HOME.z - 2.5); if (p[2] > C.near * 1.2) objs.push([p[2], `<g transform="translate(${f1(p[0])},${f1(p[1])})">${hutIcon(clamp((0.8 * F * 0.75) / p[2], 0.5, 3), "#a89a7a")}</g>`]); }
    Dd.palms.forEach(([u, v, z, s0, lean]) => { const p = proj(C, u, v, z); if (p[2] < C.near * 1.2) return; objs.push([p[2], `<g transform="translate(${f1(p[0])},${f1(p[1])})">${palmIcon(clamp((s0 * F * 0.55) / p[2], 0.4, 2.6), lean)}</g>`]); });
    // the boat: out along the course, then (o.driftAt) blown onto the drift path; a V of wake behind it
    let bp;
    if (dk > 0) { const [u, v, a] = along(Dd.drift, dk); bp = [u, v, a]; } else { const [u, v, a] = along(Dd.course, bk * (o.boatTo ?? 0.55)); bp = [u, v, a]; }
    if (t >= bg[0] - 0.3) {
      const p = proj(C, bp[0], bp[1], 0.6), p2 = proj(C, bp[0] + Math.cos(bp[2]) * 10, bp[1] + Math.sin(bp[2]) * 10, 0.6), ang = (Math.atan2(p2[1] - p[1], p2[0] - p[0]) * 180) / PI;
      const moving = (dk > 0 && dk < 0.999) || (bk > 0 && bk < 1), wl = moving ? 34 : 10;
      const wk = [[bp[0] - Math.cos(bp[2]) * wl + Math.sin(bp[2]) * 7, bp[1] - Math.sin(bp[2]) * wl - Math.cos(bp[2]) * 7], [bp[0], bp[1]], [bp[0] - Math.cos(bp[2]) * wl - Math.sin(bp[2]) * 7, bp[1] - Math.sin(bp[2]) * wl + Math.cos(bp[2]) * 7]];
      objs.push([p[2], `<path d="${lineOf(C, wk, 0.3, z0f)}" stroke="#ffffff" stroke-width="${f1(clamp(1.2 * S, 2, 6))}" fill="none" stroke-linecap="round" opacity=".7"/><ellipse cx="${f1(p[0] + 3)}" cy="${f1(p[1] + 5)}" rx="${f1(clamp(26 * S / 1.6, 18, 60))}" ry="${f1(clamp(8 * S / 1.6, 5, 18))}" fill="#04243c" opacity=".25"/><g transform="translate(${f1(p[0])},${f1(p[1])})">${boatTop(clamp(S * 0.55, 0.45, 1.5), ang)}</g>`]);
      inst.boatScreen = [p[0], p[1]];
    }
    objs.sort((a, b) => b[0] - a[0]);
    out.push(objs.map((x) => x[1]).join(""));
    // the rain curtain under the cloud, the cumulonimbus itself (billboard blobs), the bolt
    const base = 42 * (0.5 + 0.5 * st.grow), topZ = base + 110 * (0.4 + 0.6 * st.grow), sc = proj(C, st.u, st.v, base);
    if (sc[2] > C.near * 1.4) {
      const prB = (st.r * F) / sc[2];
      let rn = "";
      Dd.rain.forEach(([cx, cy, ph, op]) => { const u = st.u + cx * st.r * 0.95, v = st.v + cy * st.r * 0.95, fall = (ph + t * 0.9) % 1, a = proj(C, u, v, base * (1 - fall * 0.55)), b = proj(C, u, v, base * Math.max(0, 1 - fall * 0.55 - 0.3)); rn += `M${f1(a[0])},${f1(a[1])}L${f1(b[0])},${f1(b[1])}`; });
      const curt = (() => { const up = circ(st.u, st.v, st.r * 0.98, 30, st.r * 0.7).map((p) => proj(C, p[0], p[1], base)), dn = circ(st.u, st.v, st.r * 0.98, 30, st.r * 0.7).map((p) => proj(C, p[0], p[1], 0)); return pathOf(up.slice(0, 16)) + "L" + dn.slice(0, 16).reverse().map((p) => `${f1(p[0])},${f1(p[1])}`).join("L") + "Z"; })();
      out.push(`<g opacity="${f1(0.35 + 0.6 * st.grow)}"><path d="${curt}" fill="#3e5468" opacity=".45"/><path d="${rn}" stroke="#d8e8f0" stroke-width="${f1(clamp(0.9 * S, 1.4, 3.4))}" opacity=".8" stroke-linecap="round"/></g>`);
      if (fl > 0.05) { const g0 = proj(C, st.u - st.r * 0.1, st.v + st.r * 0.1, 0.5); const bolt = []; let x = sc[0] + prB * 0.1, y = sc[1]; const n = 7; for (let i = 0; i <= n; i++) { bolt.push([x, y]); x += (hash(i * 3 + Math.floor(t * 9)) - 0.5) * prB * 0.26; y += (g0[1] - sc[1]) / n; } out.push(`<circle cx="${f1(g0[0])}" cy="${f1(g0[1])}" r="${f1(prB * 0.7)}" fill="url(#isBolt)" opacity="${f1(fl)}"/><path d="${pathOf(bolt)}" stroke="#fff7c0" stroke-width="${f1(clamp(2.6 * S, 4, 10))}" fill="none" stroke-linejoin="round" stroke-linecap="round" opacity="${f1(fl)}"/><path d="${pathOf(bolt)}" stroke="#ffffff" stroke-width="${f1(clamp(1 * S, 1.5, 4))}" fill="none" stroke-linejoin="round" opacity="${f1(fl)}"/>`); }
      // the cloud: a dark flat base, grey body puffs, a bright cauliflower top, the anvil spreading east
      const tp = proj(C, st.u, st.v, topZ), pr = prB, h = sc[1] - tp[1];
      let cl = `<ellipse cx="${f1(sc[0])}" cy="${f1(sc[1])}" rx="${f1(pr * 1.05)}" ry="${f1(pr * 0.36)}" fill="url(#isCloudD)"/>`;
      Dd.puffs.forEach(([a, rr, bz, ph]) => { const cx = sc[0] + Math.cos(a) * pr * 0.62 * rr, cy = sc[1] - h * (0.12 + 0.55 * bz) + Math.sin(a) * pr * 0.14, br = pr * (0.28 + 0.22 * rr) * (1 + 0.04 * Math.sin(t * 1.3 + ph * 6)); const dark = bz < 0.62; cl += `<ellipse cx="${f1(cx)}" cy="${f1(cy)}" rx="${f1(br)}" ry="${f1(br * 0.78)}" fill="url(#${dark ? "isCloudG" : "isCloudW"})"/>`; });
      cl += `<ellipse cx="${f1(sc[0] + pr * 0.25)}" cy="${f1(tp[1] + pr * 0.06)}" rx="${f1(pr * (0.8 + 0.5 * st.grow))}" ry="${f1(pr * 0.17)}" fill="url(#isCloudW)" opacity=".9"/><ellipse cx="${f1(sc[0] - pr * 0.1)}" cy="${f1(tp[1] + pr * 0.02)}" rx="${f1(pr * 0.5)}" ry="${f1(pr * 0.3)}" fill="url(#isCloudW)"/>`;
      cl += `<ellipse cx="${f1(sc[0])}" cy="${f1(sc[1] + pr * 0.02)}" rx="${f1(pr * 1.0)}" ry="${f1(pr * 0.2)}" fill="url(#isCloudD)" opacity=".85"/>`;
      if (fl > 0.05) cl += `<ellipse cx="${f1(sc[0])}" cy="${f1(sc[1] - h * 0.35)}" rx="${f1(pr * 0.9)}" ry="${f1(h * 0.45)}" fill="#fff6c8" opacity="${f1(0.45 * fl)}"/>`;
      out.push(cl);
      inst.stormScreen = [sc[0], tp[1] - pr * 0.3];
    } else inst.stormScreen = null;
    // horizon haze
    const hz = 240 + 520 * clamp((C.tilt - 25) / 35);
    out.push(`<rect x="-60" y="-60" width="1200" height="${f1(hz + 60)}" fill="url(#isHaze)"/>`);
    // labels: billboards over the islands and the storm, clamped above the caption band
    const lab = { home: "เกาะหลังเต่า", ghost: "เกาะผี", storm: "พายุฝนฟ้าคะนอง", ...(o.labels || {}) };
    const tag = (u, v, z, txt, extra) => { const p = proj(C, u, v, z); if (p[2] < C.near * 1.4 || p[0] < -200 || p[0] > 1300 || p[1] > 1500) return ""; const x = clamp(p[0], 150, 930), y = clamp(p[1] - 150, 150, 1400), foot = proj(C, u, v, z); return `<path d="M${f1(foot[0])},${f1(foot[1])}L${f1(x)},${f1(y + 20)}" stroke="#140e0a" stroke-width="3" opacity=".5" stroke-dasharray="6 6"/>${tagAt(x, y, txt, extra)}`; };
    if (lab.home) out.push(tag(HOME.c[0] + 20, HOME.c[1] - 10, HOME.z + 2, lab.home, { face: "url(#isPillC)", slab: "#a8936a", fill: "#140e0a", hi: 0.7 }));
    if (lab.ghost) out.push(tag(GHOST.c[0], GHOST.c[1] - 4, GHOST.z + 2, lab.ghost, { face: "url(#isPillC)", slab: "#a8936a", fill: "#140e0a", hi: 0.7 }));
    if (lab.storm && inst.stormScreen && st.grow > 0.12) { const [x0, y0] = inst.stormScreen; out.push(tagAt(clamp(x0, 190, 890), clamp(y0 - 40, 150, 1400), lab.storm, { stroke: "#ffd23a", fill: "#ffd23a", op: clamp((st.grow - 0.12) / 0.25) })); }
    inst.g.innerHTML = out.join("");
  }
  const flight3d = (o) => { const D = o.dur ?? 9; return [
    { t: 0, u: -60, v: 0, tilt: 34, yaw: -8, S: 0.92, cy: 980 },
    { t: D * 0.42, u: -110, v: 12, tilt: 38, yaw: -4, S: 1.18, cy: 1000 },
    { t: D * 0.78, u: -30, v: 12, tilt: 46, yaw: 4, S: 2.1, cy: 1080 },
    { t: D, u: 20, v: 14, tilt: 50, yaw: 8, S: 2.6, cy: 1120 }]; };
  function islMap3d(L, o = {}) {
    const id = o.id || "im";
    put(L.sky, `<rect x="-600" y="-600" width="2400" height="3200" fill="url(#isMapSky)"/>`);
    put(L.set, `<g id="${id}-m3"></g>`);
    const inst = { id, o: { ...o }, keys: o.cam || flight3d(o), g: document.getElementById(`${id}-m3`) };
    L.ism3d = inst;
    frame3d(inst, 0);
  }
  const popIn = (tl, sel, at) => { tl.fromTo(sel, { scaleX: 0.1, scaleY: 0.1, opacity: 0, svgOrigin: "0 0" }, { scaleX: 0.82, scaleY: 1.24, opacity: 1, svgOrigin: "0 0", duration: 0.14, ease: "power2.out", immediateRender: false }, at); tl.to(sel, { scaleX: 1.16, scaleY: 0.86, svgOrigin: "0 0", duration: 0.1, ease: "sine.inOut" }, at + 0.14); tl.to(sel, { scaleX: 1, scaleY: 1, svgOrigin: "0 0", duration: 0.42, ease: "elastic.out(1, 0.42)" }, at + 0.24); };
  function play(tl, L, sid, t0, o = {}) {
    const inst = L.ism3d, id = `${sid}-im`, dur = o.dur ?? 9;
    Object.assign(inst.o, o); inst.o.dur = dur;
    inst.keys = o.cam || flight3d(inst.o);
    if (o.chip) {
      put(L.light, `<g id="${id}-chip" transform="translate(540,200)"><g id="${id}-chipB"><g id="${id}-chipP" opacity="0">${pill(Math.max(300, vis(o.chip) * 27 + 120), 100, { stroke: "#ffd23a", sw: 5 })}<text y="16" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="46" fill="#fff6e8">${o.chip}</text></g></g></g>`);
      popIn(tl, `#${id}-chipP`, t0 + (o.chipAt ?? 0.3));
      tl.fromTo(`#${id}-chipB`, { y: -3 }, { y: 3, duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.4);
      if (o.out !== undefined) tl.to(`#${id}-chipP`, { opacity: 0, duration: 0.2 }, t0 + o.out);
    }
    const px = { t: 0 };
    tl.fromTo(px, { t: 0 }, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => frame3d(inst, px.t) }, t0);
    frame3d(inst, 0);
  }

  // ======================================================================================================================
  // ---------------- 3. the body cut-away: a glass of seawater in, more water out, the body's level falls ----------------
  const BODY = {};
  const DEFB = { glass: "น้ำทะเล 1 แก้ว", kidney: "ไตคนทำปัสสาวะได้|แค่จืดกว่าน้ำทะเล", out: "ต้องฉี่น้ำออก|มากกว่าที่ดื่ม", thirst: "ยิ่งดื่ม ยิ่งกระหาย", stamp: "ห้ามดื่มน้ำทะเล", mix: "น้ำจืดหยดสุดท้าย…|ถูกใช้ละลายเกลือ" };
  const labW = (txt, fs = 32) => Math.max(...txt.split("|").map(vis)) * fs * 0.56 + 70;
  const labelB = (txt, o = {}) => { const fs = o.fs || 32, lines = txt.split("|"), w = labW(txt, fs), h = 26 + (fs + 8) * lines.length; return `${pill(w, h, { face: o.face || "url(#isPillD)", slab: o.slab || "#02060a", stroke: o.stroke || "#140e0a", r: 30, hi: o.hi })}${lines.map((l, i) => `<text y="${f1(fs * 0.36 + (i - (lines.length - 1) / 2) * (fs + 8))}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="${fs}" fill="${i ? (o.fill2 || "#ffd23a") : (o.fill || "#fff6e8")}">${l}</text>`).join("")}`; };
  // the figure: head at (540, 520), shoulders y 700, the torso down to y 1250 (its outline is also the clip for the water level)
  const TORSO = "M540,300C470,300 420,350 420,430C420,480 440,520 468,545C462,590 440,640 400,690C330,740 300,820 300,930V1180C300,1230 340,1260 390,1260H690C740,1260 780,1230 780,1180V930C780,820 750,740 680,690C640,640 618,590 612,545C640,520 660,480 660,430C660,350 610,300 540,300Z";
  function islBody(L, o = {}) {
    const id = o.id || "ib";
    put(L.sky, `<rect x="-600" y="-600" width="2400" height="3200" fill="url(#isBodySky)"/><circle cx="860" cy="330" r="230" fill="url(#tmSun)" opacity=".8"/><rect x="-600" y="1260" width="2400" height="1200" fill="url(#isBodyFloor)"/>`);
    put(L.far, `<g opacity=".5">${[[120, 0.9], [330, 0.7], [820, 1.0], [1000, 0.6]].map(([x, s]) => `<path d="M${x - 90 * s},700 C${x - 70 * s},560 ${x - 30 * s},500 ${x},490 C${x + 40 * s},500 ${x + 70 * s},560 ${x + 90 * s},700Z" fill="#8fb8b0"/>`).join("")}</g>`);
    put(L.set, `<g id="${id}-sec"><defs><clipPath id="${id}-bc"><path d="${TORSO}"/></clipPath><clipPath id="${id}-gc"><path id="${id}-gcP" d="M0,0"/></clipPath><clipPath id="${id}-jc"><path id="${id}-jcP" d="M0,0"/></clipPath></defs><g id="${id}-dyn"></g></g>`);
    put(L.light, `<g id="${id}-ui"></g>`);
    BODY[id] = { id, g: document.getElementById(`${id}-dyn`), ui: document.getElementById(`${id}-ui`), labels: {}, mix: !!o.mix };
    bodyFrame(BODY[id], 0);
  }
  const sx = (a) => clamp(a);
  function bodyFrame(inst, k) {
    const id = inst.id, lab = { ...DEFB, ...inst.labels }, out = [], ui = [], mixOn = inst.mix;
    const rr = mk(Math.floor(k * 300) + 1);
    // stages
    const kMix = mixOn ? sx(k / 0.06) : 1, kPour = sx((k - 0.04) / 0.16), kSalt = sx((k - 0.2) / 0.18), kWork = sx((k - 0.32) / 0.38), kOut = sx((k - 0.4) / 0.35), kThirst = sx((k - 0.7) / 0.2), kStamp = sx((k - 0.9) / 0.06);
    const level = lerp(0.62, 0.34, smooth(kWork)), pulse = kWork > 0 && kWork < 1 ? 1 + 0.06 * Math.sin(k * 160) : 1;
    // soft shadow on the floor, the figure's glass body
    out.push(`<ellipse cx="560" cy="1290" rx="330" ry="40" fill="url(#isSoft)" opacity=".55"/>`);
    out.push(`<path d="${TORSO}" fill="url(#isSkin)" stroke="#140e0a" stroke-width="5" stroke-linejoin="round"/>`);
    // the body's water: a level inside the outline (clipped), with a wobbling surface
    const wy = 1260 - 960 * level, wob = 4 * Math.sin(k * 60);
    let surf = `M300,${f1(wy + wob)}`; for (let x = 300; x <= 780; x += 40) surf += `L${x},${f1(wy + 5 * Math.sin(x * 0.03 + k * 70) + wob)}`;
    out.push(`<g clip-path="url(#${id}-bc)"><path d="${surf}V1270H300Z" fill="url(#isBodyWater)"/><path d="${surf}" stroke="#eafcff" stroke-width="5" fill="none" opacity=".9"/>${kWork > 0 && kWork < 1 ? Array.from({ length: 8 }, (_, i) => { const q = (i / 8 + k * 2.2) % 1, x = 330 + ((i * 97) % 440), y = wy + 60 + q * 320; return `<circle cx="${x}" cy="${f1(y)}" r="${f1(4 + (i % 3) * 2)}" fill="#ffffff" opacity="${f1(0.35 * (1 - q))}"/>`; }).join("") : ""}</g>`);
    // inner glow of the glass body and the organs: oesophagus, stomach, the two kidneys with ureters, the bladder
    out.push(`<path d="${TORSO}" fill="none" stroke="#ffffff" stroke-width="7" opacity=".35" transform="translate(-4,-4)"/>`);
    out.push(`<path d="M540,548C536,620 530,700 520,760" stroke="#c96a56" stroke-width="12" fill="none" stroke-linecap="round" opacity=".9"/>`);
    const sq = 1 + 0.08 * kPour * (1 - kPour) * 4;
    out.push(`<g transform="translate(500,840) scale(${f1(sq)},${f1(2 - sq)})"><path d="M-60,-70C-10,-110 70,-90 80,-30C88,20 50,70 0,76C-56,82 -92,40 -86,-10C-82,-40 -76,-56 -60,-70Z" fill="url(#isStomach)" stroke="#140e0a" stroke-width="4"/><path d="M-40,-50C-10,-72 30,-66 50,-40" stroke="#fff" stroke-width="6" opacity=".4" fill="none" stroke-linecap="round"/></g>`);
    // kidneys
    [[432, 960, 1], [648, 960, -1]].forEach(([kx, ky, dir]) => {
      out.push(`<g transform="translate(${kx},${ky}) scale(${f1(dir * pulse)},${f1(pulse)})"><path d="M-30,-60C10,-70 46,-40 46,0C46,42 14,72 -22,64C-40,60 -34,40 -30,30C-20,8 -22,-10 -32,-24C-40,-36 -46,-58 -30,-60Z" fill="url(#isKidney)" stroke="#140e0a" stroke-width="4"/><path d="M-14,-44C6,-50 26,-32 30,-8" stroke="#fff" stroke-width="5" opacity=".35" fill="none" stroke-linecap="round"/></g>`);
      out.push(`<path d="M${kx - dir * 26},${ky + 40}C${kx - dir * 30},${ky + 120} ${540 - dir * 30},${ky + 170} ${540 - dir * 18},${ky + 200}" stroke="#e8b83a" stroke-width="7" fill="none" stroke-linecap="round" opacity="${f1(0.5 + 0.5 * kOut)}"/>`);
    });
    // the bladder
    const bl = 0.2 + 0.8 * Math.max(0, Math.sin(PI * sx(kOut)));
    out.push(`<g transform="translate(540,1180)"><path d="M-50,0C-50,-40 -30,-60 0,-60C30,-60 50,-40 50,0C50,30 30,46 0,46C-30,46 -50,30 -50,0Z" fill="#fbe9b0" stroke="#140e0a" stroke-width="4"/><g clip-path="url(#${id}-bc)"></g><path d="M-${f1(46 * bl)},${f1(30 - 60 * bl + 10)}C-${f1(46 * bl)},${f1(40 - 60 * bl)} ${f1(46 * bl)},${f1(40 - 60 * bl)} ${f1(46 * bl)},${f1(30 - 60 * bl + 10)}V44H-${f1(46 * bl)}Z" fill="url(#isUrine)" opacity=".9"/><path d="M-34,30L34,30" stroke="#fff" stroke-width="3" opacity=".4"/></g>`);
    // salt crystals: ride the pour into the stomach, then drift to the kidneys and collect there
    let salt = "";
    for (let i = 0; i < 14; i++) {
      const ph = hash(i + 40), s = 5 + 4 * hash(i + 60);
      let x, y, op = 1;
      if (kSalt <= 0) { if (kPour <= 0.1) continue; const q = sx((kPour - ph * 0.3) / 0.7); if (q <= 0) continue; x = 520 - 40 * (1 - q) + 30 * Math.sin(ph * 9); y = 560 + 270 * q + 20 * Math.sin(i); }
      else { const side = i % 2 ? 1 : -1, q = smooth(sx((kSalt - ph * 0.4) / 0.6)); x = lerp(500 + 30 * Math.sin(ph * 9), 540 + side * 108, q); y = lerp(840 + 20 * Math.sin(i), 960 + (hash(i + 7) - 0.5) * 70, q); op = 1 - 0.35 * kOut; }
      salt += `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(ph * 90)})" opacity="${f1(op)}"><rect x="${-s / 2}" y="${-s / 2}" width="${s}" height="${s}" fill="url(#isSaltG)" stroke="#8aa0b0" stroke-width="1.6"/></g>`;
    }
    out.push(salt);
    // the glass of seawater on the left, tipping into the mouth
    const tip = -62 * smooth(kPour) * (1 - 0.15 * sx((kPour - 0.9) / 0.1)), gx = lerp(190, 390, smooth(sx(kPour * 1.6))), gy = lerp(1000, 560, smooth(sx(kPour * 1.6)));
    const fill = 1 - 0.95 * smooth(kPour), fresh = mixOn ? smooth(kMix) : 0;
    out.push(`<g transform="translate(${f1(gx)},${f1(gy)}) rotate(${f1(tip)})"><ellipse cx="0" cy="92" rx="70" ry="10" fill="url(#isSoft)" opacity=".5"/><path d="M-58,-80L-50,80Q0,94 50,80L58,-80Z" fill="#cfefff" opacity=".35" stroke="#140e0a" stroke-width="4"/>
      <path d="M${f1(-56 + 8 * (1 - fill))},${f1(80 - 156 * fill)}Q0,${f1(76 - 156 * fill + 8)} ${f1(56 - 8 * (1 - fill))},${f1(80 - 156 * fill)}L50,80Q0,94 -50,80Z" fill="url(#isSea)" opacity=".92"/>
      ${Array.from({ length: 6 }, (_, i) => `<rect x="${f1(-30 + i * 11)}" y="${f1(60 - 120 * fill + (i % 3) * 18)}" width="5" height="5" fill="#fff" opacity="${f1(0.8 * fill)}" transform="rotate(${i * 30} ${f1(-30 + i * 11)} ${f1(60 - 120 * fill + (i % 3) * 18)})"/>`).join("")}
      <path d="M-58,-80L-50,80Q0,94 50,80L58,-80Z" fill="url(#isGlass)" stroke="none"/><path d="M-44,-70L-38,60" stroke="#fff" stroke-width="5" opacity=".6" stroke-linecap="round"/></g>`);
    if (mixOn && k < 0.1) { // the fresh-water bottle tipped over the glass: its last drops
      const bk = smooth(kMix), bx = 150, by = 760;
      out.push(`<g transform="translate(${bx},${by}) rotate(${f1(-120 * bk)})"><path d="M-18,0h36v40l-6,16v110h-24v-110l-6,-16Z" fill="#dff4ff" stroke="#140e0a" stroke-width="3.5"/><rect x="-14" y="-16" width="28" height="18" rx="4" fill="#3aa0d8" stroke="#140e0a" stroke-width="3"/><path d="M-8,120h16" stroke="#3aa0d8" stroke-width="6" opacity=".7"/></g>`);
      for (let i = 0; i < 3; i++) { const q = (bk * 2 + i * 0.33) % 1; if (bk < 0.3) continue; out.push(`<ellipse cx="${f1(bx + 60 + 10 * i)}" cy="${f1(by + 60 + q * 260)}" rx="5" ry="8" fill="#9fe4ff" opacity="${f1(1 - q)}"/>`); }
    }
    // the pour: an arc of seawater from the rim into the mouth, drops, the throat swallowing
    if (kPour > 0.15 && kPour < 1) {
      const a = sx((kPour - 0.15) / 0.2) * (1 - sx((kPour - 0.85) / 0.15)), mx = 540, my = 530;
      out.push(`<path d="M${f1(gx + 40)},${f1(gy - 40)}Q${f1((gx + mx) / 2 + 20)},${f1(gy - 120)} ${mx},${my}" stroke="#5ccbe8" stroke-width="${f1(14 * a)}" fill="none" stroke-linecap="round" opacity=".9"/><path d="M${f1(gx + 40)},${f1(gy - 40)}Q${f1((gx + mx) / 2 + 20)},${f1(gy - 120)} ${mx},${my}" stroke="#ffffff" stroke-width="${f1(4 * a)}" fill="none" stroke-linecap="round" opacity=".8"/>`);
      out.push(`<ellipse cx="540" cy="${f1(620 + 100 * ((k * 9) % 1))}" rx="9" ry="${f1(14 * a)}" fill="#5ccbe8" opacity=".8"/>`);
    }
    // the face: eyes, the mouth (open while drinking, then slack and dry), sweat drops as thirst grows
    const open = Math.max(kPour > 0.15 && kPour < 0.95 ? 1 : 0, kThirst * 0.8);
    out.push(`<g transform="translate(540,430)"><ellipse cx="-36" cy="-10" rx="9" ry="${f1(10 - 6 * kThirst)}" fill="#140e0a"/><ellipse cx="36" cy="-10" rx="9" ry="${f1(10 - 6 * kThirst)}" fill="#140e0a"/><path d="M-50,-34q14,-10 28,-2M50,-34q-14,-10 -28,-2" stroke="#140e0a" stroke-width="5" fill="none" stroke-linecap="round"/>
      <path d="M-28,${f1(50 + 8 * kThirst)}Q0,${f1(50 + 8 * kThirst + 34 * open)} 28,${f1(50 + 8 * kThirst)}Q0,${f1(50 + 8 * kThirst + 6)} -28,${f1(50 + 8 * kThirst)}Z" fill="#7a2a2a" stroke="#140e0a" stroke-width="4"/>
      ${kThirst > 0 ? `<path d="M-24,${f1(50 + 8 * kThirst)}l4,-7M-8,${f1(50 + 8 * kThirst)}l3,-8M10,${f1(50 + 8 * kThirst)}l-3,-7M24,${f1(50 + 8 * kThirst)}l-4,-7" stroke="#d8402e" stroke-width="3" opacity="${f1(kThirst)}" stroke-linecap="round"/>` : ""}
      ${kThirst > 0.2 ? [[-80, -40, 0], [84, -20, 0.4], [-70, 30, 0.7]].map(([x, y, ph]) => { const q = (kThirst * 2 + ph) % 1; return `<path d="M${x},${f1(y + q * 60)}c-8,-12 -8,-22 0,-30c8,8 8,18 0,30Z" fill="#9fe4ff" stroke="#3aa0d8" stroke-width="2" opacity="${f1(1 - q)}"/>`; }).join("") : ""}</g>`);
    // the measuring jug on the right: the "1 แก้ว" mark, the urine rising past it
    const jx = 930, jy = 1250, jh = 360, jw = 150, jl = 1.42 * smooth(kOut);
    out.push(`<g transform="translate(${jx},${jy})"><ellipse cx="0" cy="14" rx="100" ry="14" fill="url(#isSoft)" opacity=".5"/><path d="M${-jw / 2},${-jh}L${-jw / 2 + 10},0H${jw / 2 - 10}L${jw / 2},${-jh}Z" fill="#cfefff" opacity=".35" stroke="#140e0a" stroke-width="4"/>
      <path d="M${-jw / 2 + 8},${f1(-jh * 0.6 * jl)}Q0,${f1(-jh * 0.6 * jl + 8)} ${jw / 2 - 8},${f1(-jh * 0.6 * jl)}L${jw / 2 - 10},0H${-jw / 2 + 10}Z" fill="url(#isUrine)" opacity=".9"/>
      ${[0.2, 0.4, 0.6, 0.8, 1.0].map((m) => `<path d="M${jw / 2 - 30},${f1(-jh * 0.6 * m)}h22" stroke="#140e0a" stroke-width="${m === 0.6 ? 4 : 2.4}" opacity="${m === 0.6 ? 0.9 : 0.5}"/>`).join("")}
      <path d="M${-jw / 2 - 6},${f1(-jh * 0.6)}H${jw / 2 + 6}" stroke="#c0281e" stroke-width="4" stroke-dasharray="10 6"/><text x="${-jw / 2 - 14}" y="${f1(-jh * 0.6 + 10)}" text-anchor="end" font-family="Kanit" font-weight="800" font-size="28" fill="#c0281e">1 แก้ว</text>
      <path d="M${-jw / 2},${-jh}L${-jw / 2 + 10},0H${jw / 2 - 10}L${jw / 2},${-jh}Z" fill="url(#isGlass)"/><path d="M${jw / 2},${-jh + 20}q40,20 44,80q0,40 -40,60" stroke="#140e0a" stroke-width="7" fill="none" stroke-linecap="round"/></g>`);
    // the stream from the bladder to the jug while it fills
    if (kOut > 0.02 && kOut < 0.98) { const a = Math.sin(PI * kOut); out.push(`<path d="M560,1215C700,1230 820,1180 ${jx - 30},${f1(jy - jh * 0.6 * jl - 10)}" stroke="#f2c43a" stroke-width="${f1(10 * a)}" fill="none" stroke-linecap="round" opacity=".9"/><path d="M560,1215C700,1230 820,1180 ${jx - 30},${f1(jy - jh * 0.6 * jl - 10)}" stroke="#fff6c0" stroke-width="${f1(3 * a)}" fill="none" stroke-linecap="round"/>`); }
    // blue drops leaving the body's water for the kidneys while they work
    if (kWork > 0 && kWork < 1) for (let i = 0; i < 10; i++) { const q = (hash(i + 90) + k * 3) % 1, side = i % 2 ? 1 : -1, x = lerp(540, 540 + side * 100, q), y = lerp(wy + 40 + 60 * hash(i + 3), 960, q); out.push(`<path d="M${f1(x)},${f1(y)}c-7,-10 -7,-18 0,-26c7,8 7,16 0,26Z" fill="#9fe4ff" stroke="#3aa0d8" stroke-width="2" opacity="${f1(0.9 * Math.sin(PI * q))}"/>`); }
    // the water gauge readout on the chest
    out.push(`<g transform="translate(540,1050)"><rect x="-70" y="-26" width="140" height="52" rx="26" fill="#02060a" opacity=".55"/><text y="12" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="${level < 0.45 ? "#ff8a6a" : "#9fe4ff"}">${Math.round(level * 100)}%</text><text y="-34" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#140e0a" opacity=".8">น้ำในตัว</text></g>`);
    inst.g.innerHTML = out.join("");
    // ---- pills, the cracked-lip tag and the stamp (screen space, constant size) ----
    const pop = (q) => backOut(sx(q), 2.6);
    if (mixOn && k > 0.0 && k < 0.2) ui.push(`<g transform="translate(300,620) scale(${f1(pop(k / 0.04) * (1 - sx((k - 0.16) / 0.04)))})">${labelB(lab.mix, { fs: 30 })}</g>`);
    if (kPour > 0.02 && k < 0.34) ui.push(`<g transform="translate(200,1200) scale(${f1(pop(kPour / 0.15) * (1 - sx((k - 0.3) / 0.04)))})">${labelB(lab.glass, { fs: 30, face: "url(#isPillC)", slab: "#a8936a", fill: "#140e0a", fill2: "#c0281e", hi: 0.7 })}</g>`);
    if (kSalt > 0.3 && k < 0.66) ui.push(`<g transform="translate(540,1380) scale(${f1(pop((kSalt - 0.3) / 0.2) * (1 - sx((k - 0.62) / 0.04)))})">${labelB(lab.kidney, { fs: 34 })}</g>`);
    if (kOut > 0.35 && k < 0.92) ui.push(`<g transform="translate(${jx - 60},${jy - jh - 150}) scale(${f1(pop((kOut - 0.35) / 0.15) * (1 - sx((k - 0.88) / 0.04)))})">${labelB(lab.out, { fs: 32, fill2: "#ff8a6a" })}</g>`);
    if (kThirst > 0.15) { const q = pop((kThirst - 0.15) / 0.2); ui.push(`<g transform="translate(540,250) scale(${f1(q)})">${labelB(lab.thirst, { fs: 40, stroke: "#ff8a6a", fill: "#ffd23a" })}</g>`); }
    if (kStamp > 0) { const q = kStamp, s = lerp(2.4, 1, 1 - Math.pow(1 - q, 3)), shake = q > 0.9 ? 0 : 4 * Math.sin(q * 40) * (1 - q); ui.push(`<g transform="translate(${f1(540 + shake)},${f1(1400 + shake * 0.5)}) rotate(-7) scale(${f1(s)})" opacity="${f1(sx(q * 3))}"><rect x="-270" y="-56" width="540" height="112" rx="16" fill="#fff" fill-opacity=".85" stroke="#c0281e" stroke-width="8"/><rect x="-256" y="-42" width="512" height="84" rx="10" fill="none" stroke="#c0281e" stroke-width="3"/><text y="20" text-anchor="middle" font-family="Mali" font-weight="700" font-size="56" fill="#c0281e">${lab.stamp}</text></g>`); }
    inst.ui.innerHTML = ui.join("");
  }
  function kidney(tl, id, t0, dur, o = {}) {
    const inst = BODY[id]; if (!inst) return;
    inst.labels = o.labels || {}; if (o.mix !== undefined) inst.mix = !!o.mix;
    const k0 = o.k0 ?? 0, k1 = o.k1 ?? 1, px = { k: k0 };
    tl.fromTo(px, { k: k0 }, { k: k1, duration: dur, ease: o.ease || "none", immediateRender: false, onUpdate: () => bodyFrame(inst, px.k) }, t0);
    bodyFrame(inst, k0);
  }

  // ======================================================================================================================
  // ---------------- 4. the X-ray of ฟ้า: a cup of seawater in, the sea inside her draws back, the sand under her feet soaks ----------------
  const XR = {};
  const DEFX = { cup: "ดื่ม 1 แก้ว", lost: "เสียน้ำ|มากกว่า 1 แก้ว", kidney: "ไตคนทำปัสสาวะได้|แค่จืดกว่าน้ำทะเล", thirst: "ยิ่งดื่ม ยิ่งกระหาย", mix: "น้ำจืดหยดสุดท้าย…" };
  // a slab of driftwood / coconut shell with the text on it (the island's own materials, not a dark app pill)
  const woodLabel = (txt, o = {}) => { const fs = o.fs || 32, lines = txt.split("|"), w = labW(txt, fs) + 10, h = 30 + (fs + 8) * lines.length;
    return `<ellipse cx="0" cy="${f1(h / 2 + 16)}" rx="${f1(w * 0.46)}" ry="12" fill="url(#isSoft)"/><rect x="${f1(-w / 2)}" y="${f1(-h / 2 + 10)}" width="${w}" height="${h}" rx="18" fill="#6a4a2a" stroke="#2e2a26" stroke-width="4"/><rect x="${f1(-w / 2)}" y="${f1(-h / 2)}" width="${w}" height="${h}" rx="18" fill="url(#isXWood)" stroke="#2e2a26" stroke-width="4"/>
      <path d="M${f1(-w / 2 + 22)},${f1(-h / 2 + 14)}q${f1(w * 0.3)},8 ${f1(w - 44)},-2" stroke="#b08a56" stroke-width="2" fill="none" opacity=".5"/><path d="M${f1(-w / 2 + 30)},${f1(h / 2 - 12)}q${f1(w * 0.25)},-6 ${f1(w - 60)},2" stroke="#b08a56" stroke-width="2" fill="none" opacity=".45"/>
      ${lines.map((l, i) => `<text y="${f1(fs * 0.36 + (i - (lines.length - 1) / 2) * (fs + 8))}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="${fs}" fill="${i ? (o.fill2 || "#c0281e") : (o.fill || "#2e2a26")}">${l}</text>`).join("")}`; };
  // the figure: the torso (neck to the thighs, cut at y 1330) is the X-ray part and the clip for the water; head, hair, arms stay drawn over it
  const XBODY = "M504,676H576L582,742C650,750 700,776 736,830C740,900 730,990 722,1080C718,1120 720,1150 726,1182H354C360,1150 362,1120 358,1080C350,990 340,900 344,830C380,776 430,750 498,742Z";
  const XTEE = "M498,742C430,750 380,776 344,830C340,900 350,990 358,1080C360,1110 360,1140 358,1170H722C720,1140 720,1110 722,1080C730,990 740,900 736,830C700,776 650,750 582,742L576,700H504Z";
  const XFACE = "M422,566C422,470 470,436 540,436C610,436 658,470 658,566C658,646 612,694 540,696C468,694 422,646 422,566Z";
  function islXray(L, o = {}) {
    const id = o.id || "ix";
    put(L.sky, `<rect x="-600" y="-600" width="2400" height="3200" fill="url(#isXSky)"/><circle cx="820" cy="250" r="300" fill="url(#tmSun)" opacity=".9"/><circle cx="820" cy="250" r="60" fill="#fffdf0"/>`);
    // the far shore: bleached palms and the sea's glitter, soft (the heat washes them out)
    let far = `<rect x="-600" y="1080" width="2400" height="240" fill="#79c9d8" opacity=".55"/><path d="M-600,1082Q540,1060 1680,1086V1110Q540,1090 -600,1112Z" fill="#ffffff" opacity=".5"/>`;
    [[60, 0.9], [230, 0.7], [900, 1.0], [1060, 0.8]].forEach(([x, s]) => { far += `<g transform="translate(${x},1080) scale(${s})" opacity=".42"><path d="M0,0C-6,-120 -2,-240 10,-360" stroke="#8aa58e" stroke-width="14" fill="none" stroke-linecap="round"/>${[-150, -100, -40, 30, 90, 150].map((a) => `<path d="M10,-360q${f1(Math.cos(a * RAD) * 90)},${f1(Math.sin(a * RAD) * 60 - 20)} ${f1(Math.cos(a * RAD) * 170)},${f1(Math.sin(a * RAD) * 110)}" stroke="#7fae86" stroke-width="18" fill="none" stroke-linecap="round"/>`).join("")}</g>`; });
    far += `<rect x="-600" y="-600" width="2400" height="3200" fill="url(#isXHeat)"/>`;
    put(L.far, far);
    put(L.set, `<rect x="-600" y="1110" width="2400" height="1400" fill="url(#isXSand)"/><defs><clipPath id="${id}-bc"><path d="${XBODY}"/></clipPath><clipPath id="${id}-tc"><path d="${XTEE}"/></clipPath></defs><g id="${id}-dyn"></g>`);
    put(L.light, `<g id="${id}-ui"></g>`);
    XR[id] = { id, g: document.getElementById(`${id}-dyn`), ui: document.getElementById(`${id}-ui`), labels: {}, mix: !!o.mix };
    xrayFrame(XR[id], 0);
  }
  // an arm: shoulder → elbow → hand as ink-outlined skin strokes, the sleeve over the upper arm, a round hand with the pink wristband
  const armSVG = (sx0, sy0, ex, ey, hx, hy, op = 1) => `<g opacity="${f1(op)}"><path d="M${sx0},${sy0}L${f1(ex)},${f1(ey)}L${f1(hx)},${f1(hy)}" stroke="${INK}" stroke-width="54" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M${sx0},${sy0}L${f1(ex)},${f1(ey)}L${f1(hx)},${f1(hy)}" stroke="#ebc19c" stroke-width="44" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M${sx0},${sy0}L${f1(sx0 + (ex - sx0) * 0.42)},${f1(sy0 + (ey - sy0) * 0.42)}" stroke="${INK}" stroke-width="56" fill="none" stroke-linecap="round"/><path d="M${sx0},${sy0}L${f1(sx0 + (ex - sx0) * 0.42)},${f1(sy0 + (ey - sy0) * 0.42)}" stroke="#8fd6bc" stroke-width="46" fill="none" stroke-linecap="round"/>
    <circle cx="${f1(hx)}" cy="${f1(hy)}" r="31" fill="#ebc19c" stroke="${INK}" stroke-width="4"/><path d="M${f1(hx - 22)},${f1(hy + 8)}q22,10 44,0" stroke="#c89a74" stroke-width="3" fill="none"/>
    <path d="M${f1(hx - 24)},${f1(hy - 28)}q24,-10 48,0" stroke="#ff7eb0" stroke-width="7" fill="none" stroke-linecap="round" transform="rotate(${f1(Math.atan2(hy - ey, hx - ex) / RAD + 90)} ${f1(hx)} ${f1(hy)})"/></g>`;
  function xrayFrame(inst, k) {
    const id = inst.id, lab = { ...DEFX, ...inst.labels }, mixOn = inst.mix, out = [], ui = [];
    const kMix = mixOn ? sx(k / 0.08) : 1, kPour = mixOn ? sx((k - 0.06) / 0.16) : sx((k - 0.02) / 0.18), kX = smooth(sx((k - 0.12) / 0.2)) * (1 - smooth(sx((k - 0.8) / 0.12)));
    const kSalt = sx((k - 0.2) / 0.25), kDrain = smooth(sx((k - 0.4) / 0.35)), kEnd = smooth(sx((k - 0.82) / 0.18)), kThirst = sx((k - 0.6) / 0.4);
    const glow = sx((kSalt - 0.6) / 0.4) * (1 - 0.5 * kEnd);
    // scene camera: push in on her face at the end
    const S = lerp(1, 1.7, kEnd), cx = 540, cy = lerp(900, 600, kEnd);
    const wrap = `translate(${f1(540 - cx * S)},${f1(960 - cy * S)}) scale(${f1(S)})`;
    // the wet ring under her feet: grows with the drain, wider than a cup's worth
    const ring = 70 + 320 * kDrain;
    out.push(`<ellipse cx="540" cy="1320" rx="${f1(ring)}" ry="${f1(ring * 0.26)}" fill="url(#isXWet)" opacity="${f1(sx(kDrain * 4))}"/>`);
    out.push(`<ellipse cx="540" cy="1326" rx="240" ry="34" fill="url(#isSoft)" opacity=".45"/>`);
    // hair, back layer (the bob behind the head, down to the jaw)
    out.push(`<path d="M414,560C396,640 404,720 436,768L470,742L540,756L610,742L644,768C676,720 684,640 666,560C656,468 424,468 414,560Z" fill="url(#isXHair)" stroke="${INK}" stroke-width="4"/>`);
    // the legs under the shorts (two columns with a gap), then the torso: skin + tee + shorts, fading as the X-ray takes over
    const skinOp = 1 - 0.92 * kX;
    out.push(`<path d="M356,1180H524Q528,1260 520,1330H362Q354,1260 356,1180Z" fill="url(#isSkin)" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><path d="M556,1180H724Q726,1260 718,1330H560Q552,1260 556,1180Z" fill="url(#isSkin)" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><path d="M360,1190q80,16 160,0M560,1190q80,16 160,0" stroke="#c89a74" stroke-width="3" fill="none" opacity=".5"/>`);
    out.push(`<g opacity="${f1(skinOp)}">
      <path d="${XBODY}" fill="url(#isSkin)" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
      <path d="${XTEE}" fill="url(#isXTee)" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
      <path d="M356,1170H724L720,1262Q540,1280 360,1262Z" fill="#c8b48a" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><path d="M540,1172V1270" stroke="#9c8862" stroke-width="4" opacity=".6"/><path d="M350,1192q190,22 380,0" stroke="#9c8862" stroke-width="3" fill="none" opacity=".5"/>
      <g clip-path="url(#${id}-tc)"><path d="M478,930C508,888 572,888 612,930C592,900 528,900 508,930L488,1010C530,1032 580,1032 628,1010L608,930C656,952 646,994 608,1012C568,1032 506,1032 478,1012Z" fill="#2a6ab8" opacity=".85"/><path d="M484,990q35,-30 70,0t70,0" stroke="#fff" stroke-width="6" fill="none" opacity=".7" stroke-linecap="round"/><path d="M622,1012l34,-26v40z" fill="#2a6ab8" opacity=".85"/></g>
      <g clip-path="url(#${id}-tc)"><path d="M300,700H470Q430,960 450,1200H300Z" fill="#2e2a26" opacity=".08"/><path d="M690,760Q740,980 726,1182H780V700Z" fill="#ffffff" opacity=".18"/></g><path d="M504,676Q540,720 576,676" fill="#2e2a26" opacity=".14"/></g>`);
    // the X-ray torso: the same outline as glass, ribs, the gullet, the two kidneys, the sea inside her with a glinting horizon
    const level = lerp(0.72, 0.36, kDrain), wy = 1182 - 440 * level, wob = 3 * Math.sin(k * 90);
    let surf = `M300,${f1(wy + wob)}`; for (let x = 300; x <= 780; x += 30) surf += `L${x},${f1(wy + 4 * Math.sin(x * 0.04 + k * 80) + wob)}`;
    out.push(`<g opacity="${f1(kX)}"><path d="${XBODY}" fill="url(#isXGlass)" stroke="#dff6ff" stroke-width="6" stroke-linejoin="round"/>
      <g clip-path="url(#${id}-bc)"><path d="${surf}V1200H300Z" fill="url(#isXWater)"/><path d="${surf}" stroke="#ffffff" stroke-width="5" fill="none" opacity=".9"/>
      ${Array.from({ length: 9 }, (_, i) => `<path d="M${f1(340 + i * 46)},${f1(wy - 4 + 2 * Math.sin(i + k * 50))}h${f1(10 + 8 * hash(i))}" stroke="#ffffff" stroke-width="3" opacity="${f1(0.4 + 0.5 * Math.abs(Math.sin(k * 40 + i)))}" stroke-linecap="round"/>`).join("")}
      ${kDrain > 0 && kDrain < 1 ? Array.from({ length: 10 }, (_, i) => { const q = (hash(i + 20) + k * 2.5) % 1, x = 370 + ((i * 83) % 340); return `<circle cx="${x}" cy="${f1(wy + 40 + q * (1182 - wy - 60))}" r="${f1(3 + (i % 3) * 2)}" fill="#ffffff" opacity="${f1(0.4 * (1 - q))}"/>`; }).join("") : ""}
      ${[0, 1, 2, 3, 4].map((i) => `<path d="M${f1(424 + i * 6)},${f1(830 + i * 46)}Q540,${f1(862 + i * 46)} ${f1(656 - i * 6)},${f1(830 + i * 46)}" stroke="#ffffff" stroke-width="7" fill="none" opacity=".45" stroke-linecap="round"/>`).join("")}
      <path d="M540,690V800" stroke="#ffffff" stroke-width="8" opacity=".5" stroke-linecap="round"/><path d="M540,690C542,790 536,870 528,940" stroke="#ffd0b8" stroke-width="10" fill="none" stroke-linecap="round" opacity=".75"/></g>
      ${[[470, 1010, 1], [610, 1010, -1]].map(([kx, ky, d]) => `<circle cx="${kx}" cy="${ky}" r="${f1(70 + 20 * Math.sin(k * 120))}" fill="url(#isXKidGlow)" opacity="${f1(glow)}"/><g transform="translate(${kx},${ky}) scale(${d},1)"><path d="M-26,-54C14,-62 44,-34 44,0C44,38 16,64 -20,58C-38,54 -32,36 -28,26C-18,8 -20,-8 -30,-22C-38,-34 -42,-52 -26,-54Z" fill="url(#isXKid)" stroke="#2e2a26" stroke-width="3.5"/><path d="M-10,-40C8,-44 26,-30 30,-8" stroke="#fff" stroke-width="4" opacity=".4" fill="none" stroke-linecap="round"/></g>`).join("")}</g>`);
    // the salt: a sparkling stream down the gullet while she drinks, then crystals gathering at the kidneys
    let salt = "";
    for (let i = 0; i < 16; i++) {
      const ph = hash(i + 40), s = 4 + 4 * hash(i + 60); let x, y, op;
      if (kSalt <= 0.02) { if (kPour <= 0.2) continue; const q = sx((kPour - 0.2 - ph * 0.3) / 0.6); if (q <= 0) continue; x = 540 - 12 * q + 10 * Math.sin(ph * 9 + q * 6); y = 700 + 240 * q; op = kX * 0.9 + 0.1; }
      else { const side = i % 2 ? 1 : -1, q = smooth(sx((kSalt - ph * 0.4) / 0.6)); x = lerp(528 + 10 * Math.sin(ph * 9), 540 + side * 70, q); y = lerp(940, 1010 + (hash(i + 7) - 0.5) * 60, q); op = kX * (1 - 0.5 * kDrain); }
      salt += `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(ph * 90 + k * 200)})" opacity="${f1(op)}"><rect x="${-s / 2}" y="${-s / 2}" width="${s}" height="${s}" fill="url(#isSaltG)" stroke="#9ab8c8" stroke-width="1.4"/><path d="M${-s},0H${s}M0,${-s}V${s}" stroke="#ffffff" stroke-width="1.2" opacity=".8"/></g>`;
    }
    out.push(salt);
    // the water she loses: drops running down the outside of her legs into the sand while the sea inside draws back
    if (kDrain > 0.03 && kDrain < 1) for (let i = 0; i < 8; i++) { const q = (hash(i + 90) + k * 2.2) % 1, side = i % 2 ? 1 : -1, x = 540 + side * (196 + 10 * hash(i)) + side * 4 * Math.sin(q * 9), y = lerp(1180, 1318, q); out.push(`<path d="M${f1(x)},${f1(y)}c-6,-9 -6,-16 0,-24c6,8 6,15 0,24Z" fill="#8fe3ff" stroke="#3fb4e0" stroke-width="2" opacity="${f1(0.9 * Math.sin(PI * q))}"/>`); }
    // her left arm hangs at her side (screen right); her right arm (screen left) lifts the cup to her mouth, then lowers once it is empty
    const armOp = 1 - 0.3 * kX;
    const bk = mixOn ? smooth(kMix) : 0, mixUp = mixOn ? sx((0.14 - k) / 0.04) : 0;
    if (mixUp > 0) out.push(armSVG(718, 826, lerp(752, 700, mixUp), lerp(1010, 1000, mixUp), lerp(742, 470, mixUp), lerp(1190, 1040, mixUp), armOp)); else out.push(armSVG(718, 826, 752, 1010, 742, 1190, armOp));
    const lift = smooth(sx(kPour / 0.25)) * (1 - smooth(sx((kPour - 0.85) / 0.15))), ex = lerp(300, 318, lift), ey = lerp(1010, 880, lift), hx2 = lerp(330, 466, lift), hy = lerp(1190, 660, lift);
    const tip = -74 * smooth(sx((kPour - 0.25) / 0.5)) * (1 - 0.3 * sx((kPour - 0.85) / 0.15)), fillC = (1 - 0.95 * smooth(sx((kPour - 0.25) / 0.6))) * (mixOn ? 0.82 + 0.18 * smooth(kMix) : 1);
    out.push(armSVG(362, 826, ex, ey, hx2, hy, armOp));
    // the face (always skin, drawn over everything): the jaw, the ear, bangs and side locks, the star clip, brows, eyes, nose, mouth
    const open = sx((kPour - 0.3) / 0.15) * (1 - sx((kPour - 0.85) / 0.15)), dull = kThirst, lidH = 11 - 7 * dull, my = 648 + 6 * dull;
    out.push(`<path d="${XFACE}" fill="url(#isSkin)" stroke="${INK}" stroke-width="5"/><path d="M656,560q22,-6 24,22q-2,26 -24,30" fill="#e9b894" stroke="${INK}" stroke-width="4"/>
      <path d="M420,586C410,500 440,428 540,424C640,428 670,500 660,586Q650,548 618,540C600,520 572,548 552,538Q540,520 528,538Q500,548 480,540Q450,548 420,586Z" fill="url(#isXHair)" stroke="${INK}" stroke-width="4"/><path d="M470,470q50,-26 110,-10M450,520q30,-20 60,-16" stroke="#9a6a44" stroke-width="3" fill="none" opacity=".45" stroke-linecap="round"/>
      <path d="M422,586C414,640 420,700 440,740L458,716L448,620Z" fill="url(#isXHair)" stroke="${INK}" stroke-width="4"/><path d="M658,586C666,640 660,700 640,740L622,716L632,620Z" fill="url(#isXHair)" stroke="${INK}" stroke-width="4"/>
      <path d="M452,560q40,-22 80,-10" stroke="#a8764a" stroke-width="4" fill="none" opacity=".5" stroke-linecap="round"/>
      <g transform="translate(612,496) rotate(-12)"><path d="M0,-18L6,-6L19,-5L9,4L12,18L0,11L-12,18L-9,4L-19,-5L-6,-6Z" fill="#f2c030" stroke="${INK}" stroke-width="2.5"/></g>
      <g transform="translate(0,${f1(8 * dull)})"><path d="M478,544q22,-12 44,-4" stroke="${INK}" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M602,544q-22,-12 -44,-4" stroke="${INK}" stroke-width="5" fill="none" stroke-linecap="round"/></g>
      <ellipse cx="500" cy="590" rx="11" ry="${f1(lidH)}" fill="#3a2016"/><ellipse cx="580" cy="590" rx="11" ry="${f1(lidH)}" fill="#3a2016"/><path d="M486,${f1(590 - lidH)}q14,-6 28,0M566,${f1(590 - lidH)}q14,-6 28,0" stroke="${INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/><ellipse cx="470" cy="628" rx="18" ry="9" fill="#e88a8a" opacity="${f1(0.35 * (1 - dull))}"/><ellipse cx="610" cy="628" rx="18" ry="9" fill="#e88a8a" opacity="${f1(0.35 * (1 - dull))}"/><circle cx="497" cy="585" r="3" fill="#fff" opacity="${f1(1 - dull)}"/><circle cx="577" cy="585" r="3" fill="#fff" opacity="${f1(1 - dull)}"/>
      ${dull > 0.3 ? `<path d="M486,${f1(584 - 2 * dull)}q14,-8 28,0M566,${f1(584 - 2 * dull)}q14,-8 28,0" stroke="#dba985" stroke-width="${f1(7 * dull)}" fill="none" stroke-linecap="round"/>` : ""}
      <path d="M536,610q8,12 0,20" stroke="${INK}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/>
      <path d="M512,${f1(my)}Q540,${f1(my + 28 * open)} 568,${f1(my)}Q540,${f1(my + 9)} 512,${f1(my)}Z" fill="${open > 0.2 ? "#7a2a2a" : mix("#d0606a", "#c9a090", dull)}" stroke="${INK}" stroke-width="4"/>
      ${dull > 0.3 ? `<path d="M530,${f1(my + 3)}l1,5M541,${f1(my + 4)}l0,5M552,${f1(my + 3)}l-1,5" stroke="#9a4a3a" stroke-width="1.8" opacity="${f1((dull - 0.3) * 1.4)}" stroke-linecap="round"/>` : ""}
      ${dull > 0.35 ? [[446, 540, 0], [648, 560, 0.4], [462, 620, 0.7]].map(([x, y, ph]) => { const q = (dull * 2 + ph) % 1; return `<path d="M${x},${f1(y + q * 50)}c-7,-10 -7,-18 0,-26c7,8 7,16 0,26Z" fill="#9fe4ff" stroke="#3aa0d8" stroke-width="2" opacity="${f1((1 - q) * sx((dull - 0.35) / 0.2))}"/>`; }).join("") : ""}`);
    // the cup (a clear plastic cup of seawater) in her hand
    out.push(`<g transform="translate(${f1(hx2 + 14)},${f1(hy - 36)}) rotate(${f1(tip)})"><path d="M-44,-66L-36,60Q0,70 36,60L44,-66Z" fill="#dff6ff" opacity=".35" stroke="${INK}" stroke-width="4"/>
      <path d="M${f1(-42 + 6 * (1 - fillC))},${f1(60 - 122 * fillC)}Q0,${f1(66 - 122 * fillC)} ${f1(42 - 6 * (1 - fillC))},${f1(60 - 122 * fillC)}L36,60Q0,70 -36,60Z" fill="url(#isSea)" opacity=".92"/>
      ${Array.from({ length: 5 }, (_, i) => `<rect x="${f1(-22 + i * 11)}" y="${f1(40 - 90 * fillC + (i % 2) * 14)}" width="4" height="4" fill="#fff" opacity="${f1(0.85 * fillC)}"/>`).join("")}
      <path d="M-44,-66L-36,60Q0,70 36,60L44,-66Z" fill="url(#isGlass)"/><path d="M-32,-56L-26,48" stroke="#fff" stroke-width="4" opacity=".6" stroke-linecap="round"/></g>`);
    if (mixOn && k < 0.14) { // the fresh-water bottle in her left hand, upended over the cup: its last drops fall in
      const bx = lerp(742, 470, mixUp), by = lerp(1190, 1040, mixUp);
      out.push(`<g transform="translate(${f1(bx)},${f1(by)}) rotate(${f1(-150 * bk)})"><path d="M-18,-60h36v40l-6,16v110h-24v-110l-6,-16Z" fill="#dff4ff" stroke="${INK}" stroke-width="3.5"/><rect x="-14" y="-76" width="28" height="18" rx="4" fill="#3aa0d8" stroke="${INK}" stroke-width="3"/><path d="M-8,20h16" stroke="#3aa0d8" stroke-width="5" opacity=".6"/></g>`);
      for (let i = 0; i < 3; i++) { const q = (bk * 2 + i * 0.33) % 1; if (bk < 0.35 || k > 0.1) continue; out.push(`<ellipse cx="${f1(hx2 + 14 + 4 * Math.sin(i))}" cy="${f1(hy - 110 + q * 60)}" rx="4" ry="7" fill="#9fe4ff" opacity="${f1(1 - q)}"/>`); }
    }
    // the stream from the cup's rim into her mouth while she drinks
    if (kPour > 0.3 && kPour < 0.9) { const a = Math.sin(PI * sx((kPour - 0.3) / 0.6)); out.push(`<path d="M${f1(hx2 + 44)},${f1(hy - 72)}Q${f1(hx2 + 66)},${f1(hy - 60)} 540,662" stroke="#5ccbe8" stroke-width="${f1(12 * a)}" fill="none" stroke-linecap="round" opacity=".9"/>`); }
    // heat shimmer lines over the sand at the end
    if (kEnd > 0.2) out.push(`<g opacity="${f1(0.4 * kEnd)}">${[0, 1, 2].map((i) => `<path d="M${f1(200 + i * 120)},${f1(1200 + i * 40)}q40,-6 80,0t80,0t80,0" stroke="#fff" stroke-width="3" fill="none"/>`).join("")}</g>`);
    inst.g.innerHTML = `<g transform="${wrap}">${out.join("")}</g>`;
    // ---- the slab labels (screen space, constant size) ----
    const pop = (q) => backOut(sx(q), 2.4);
    if (mixOn && k > 0.01 && k < 0.14) ui.push(`<g transform="translate(300,400) scale(${f1(pop(k / 0.04) * (1 - sx((k - 0.11) / 0.03)))})">${woodLabel(lab.mix, { fs: 28 })}</g>`);
    if (k > 0.13 && k < 0.36) ui.push(`<g transform="translate(230,430) scale(${f1(pop((k - 0.13) / 0.05) * (1 - sx((k - 0.33) / 0.03)))})">${woodLabel(lab.cup, { fs: 32 })}</g>`);
    if (k > 0.44 && k < 0.72) ui.push(`<g transform="translate(540,1400) scale(${f1(pop((k - 0.44) / 0.06) * (1 - sx((k - 0.69) / 0.03)))})">${woodLabel(lab.kidney, { fs: 34 })}</g>`);
    if (k > 0.58 && k < 0.84) ui.push(`<g transform="translate(830,1230) scale(${f1(pop((k - 0.58) / 0.06) * (1 - sx((k - 0.81) / 0.03)))})">${woodLabel(lab.lost, { fs: 32, fill2: "#c0281e" })}</g>`);
    if (k > 0.84) ui.push(`<g transform="translate(540,250) scale(${f1(pop((k - 0.84) / 0.06))})">${woodLabel(lab.thirst, { fs: 42, fill: "#c0281e" })}</g>`);
    inst.ui.innerHTML = ui.join("");
  }
  function xray(tl, id, t0, dur, o = {}) {
    const inst = XR[id]; if (!inst) return;
    inst.labels = o.labels || {}; if (o.mix !== undefined) inst.mix = !!o.mix;
    const k0 = o.k0 ?? 0, k1 = o.k1 ?? 1, px = { k: k0 };
    tl.fromTo(px, { k: k0 }, { k: k1, duration: dur, ease: o.ease || "none", immediateRender: false, onUpdate: () => xrayFrame(inst, px.k) }, t0);
    xrayFrame(inst, k0);
  }

  Object.assign(Sets, { islMap3d, islBody, islXray });
  Object.assign(IslMap, { play, kidney, xray, DEFX, frame3d, camAt, HOME, GHOST, COURSE, DRIFT, PIER_END, BEACH, ROCKS, DEFB });
})();
