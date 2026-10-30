// "ทะเลลด" sets — บ้านแหลมหอย, a fictional fishing village on Thailand's Andaman coast over the New Year holiday. Limestone karst islands
// on the horizon (Phang Nga), coconut palms and casuarinas, longtail boats with ผ้าสามสี and a garland on the bow, ยาย's wooden seafood
// shop and, right beside it, โรงแรมแหลมหอย — a 5-storey reinforced-concrete hotel with an outside stair and a flat roof (the vertical
// refuge: ปภ. "อาคารที่มั่นคงแข็งแรงและมีความสูงมากกว่า 4 ชั้นขึ้นไป"), a warning tower with loudspeakers, the blue evacuation sign, and
// the jungle hill whose steps climb well above the palms and the hotel's roof to the assembly point (จุดรวมพล).
// Same layer contract as pop2.js (sky / far / mid / set / act / fg; glow above the darkness; light = screen space). Seeded RNG only.
// Everything that moves is redrawn from the timeline clock by one proxy tween per call, so any seek gives the same frame.
// Gradients only, no SVG filters. Needs pop2.js and qkmat.js loaded first. Ink #2e2a26; the morning sun is on the right.
//
//   Sets.tideBeach(L, o)   the beach · o.view "sea" (default) | "land" · o.time "morning" | "eerie" | "storm" | "squall" · o.seed
//     view "sea"   looking out to sea from the beach; horizon at o.hz (640), camera o.hc metres up (3; 5 = from ยาย's deck), the water's
//                  edge at o.shore metres (14). A ground point d metres away is at y = hz + 2400·hc / d (Tide.yAt(id, d)).
//                  o.sea 0…1 the water level (1 = drawn back ~350 m to a thin band at the horizon) · o.boats 0…2 longtails at anchor
//                  (they ground and pitch when the water leaves them; none ever heads out) · o.fish (14) · o.people n small figures
//                  who walk out onto the seabed and stop short of the water, some stooping for fish · o.palms false · o.frame "eave"
//                  frames the shot from inside ยาย's shop (tin roof, blue awning, post, the deck rail and a drink in L.fg)
//                  ids (redrawn): #id-water #id-shal #id-film #id-foam #id-foam2, #id-boat0/1 (+ #id-boat0-w waterline band),
//                  #id-fish0…, #id-crab0…, #id-p0… (figures; children -a -b walk frames, -c stooping), #id-birds, #id-palm0/1
//                  (fronds, data-o = crown), #id-karsts
//     view "land"  from the shallows looking inland: #id-hotel (#id-f1 … #id-f5 the storeys, #id-roof, #id-stair, #id-hsign, the
//                  roof flag #id-flag), #id-shop (#id-clue = the old photo + the newspaper clipping on its back wall), #id-tower
//                  (#id-beacon), #id-sign (the evacuation sign), #id-boatL0, #id-swash (the water's edge at the bottom), #id-palm0…
//   Tide.sea(tl, id, t0, dur, o)       runs a "sea" view: swash, glitter, bobbing boats, flopping fish, scuttling crabs, walkers, birds;
//                                      o.to (target level), o.at / o.len (seconds into the call the water starts / takes to draw
//                                      back), o.ease, o.walkAt (when the walkers set off), o.birds "flee"
//   Tide.recede(tl, id, t0, dur, to)   = Tide.sea with the water drawing back to level `to` over the whole call
//   Tide.land(tl, id, t0, dur, o)      runs a "land" / hill view: swash, the flag, palms, the tower's beacon (o.siren true)
//   Sets.tideWave(L, o)    low on the upper beach (camera o.hc 1.2 m up, horizon o.hz 1290) looking out under a squall sky (o.time
//                          "squall"): a steep wall of muddy water (dark teal at the foot to sediment olive-brown up the face, flow lines
//                          and churn climbing it) with a torn white crest, fine spray thrown forward off it, a boiling foam skirt where it
//                          comes down on the sand and a sheet of water racing ahead. Debris rides half-sunk in its face (the green longtail
//                          พง 0418, planks, a beach umbrella, a cooler); palms, a massage hut and a coconut stall stand in its path and are
//                          swallowed as it reaches them; a runner flees ahead of it (o.runner false: none); the sand has footprints and
//                          things left behind. o.shore (45) the sea's usual edge, o.u the start progress.
//                          ids (redrawn): #id-wall (#id-wallG), #id-cr0…2 (the crest), #id-sk0…2 (the skirt), #id-sp0…2 (spray),
//                          #id-sheet, #id-deb0…4 (+ #id-lap0… their sunk part), #id-ov0…6 (palms and shacks; #id-ovg/ovw the foam
//                          climbing them), #id-rn (the runner, frames #id-rn0…3), #id-birds, #id-scud · Tide.waveIn(tl, id, t0, dur, o)
//                          brings it in: o.from 0 → o.to 1 (150 m out → 14 m from the camera; 9 m high inside ~90 m)
//   Sets.tideHill(L, o)    on the evacuation steps high on the hill, looking down at the village and the bay: concrete steps with a
//                          steel handrail, the blue sign "เส้นทางหนีคลื่นยักษ์" (#id-sign), the warning tower (#id-tower, #id-beacon),
//                          the hotel's roof beside ยาย's shop, roofs, palms, the karsts; o.sea the bay's level: 0 the sea at the beach
//                          … 1 drawn back (the first time) … 1.7 the second time, far out toward the karsts; o.line 0…1 the white line
//                          on the horizon · run it with Tide.land (the flag, o.siren the beacon) and, for the water, one of:
//     Tide.hillSea(tl, id, t0, dur, o)  the bay draws back (or in) from o.from (the set's level) to o.to between o.at and o.at + o.len
//                          seconds into the call (o.ease); the bare seabed (#id-bed, its edge #id-bedE) is redrawn, the two longtails
//                          out on the bay (#id-hb0/1, waterline #id-hb0-w) bob, then lie over on the mud; o.line [w0, w1] grows the
//                          white line (#id-wl) from o.lineAt seconds (0.6 of the call) to the end
//     Tide.surge(tl, id, t0, dur, o)    the first wave: the sea runs back in over the seabed (its edge churned white), pours over the
//                          beach and floods the village ground round the shop and the hotel's ground floor (~2–3 m; #id-flood under
//                          copies of the roofs and crowns #id-above, a band of water over the foot of the hotel, the shop, each palm
//                          and the tower #id-fb0…9), swirls past them carrying a plank, a cooler, a chair, an umbrella (#id-fd0…3),
//                          then drains back out to sea leaving the ground dark and wet with a line of litter (#id-fwet); o.to the
//                          height at its peak (1), o.rise / o.hold the fractions of the call where it peaks / starts to drain
//                          (0.34 / 0.6), o.after the bay's level once it has gone (0.35, already drawing back again)
//   Sets.tideSand(L, o)    the opener: straight down onto wet sand as the sea pulls back off it; the title pressed into the sand
//                          (o.title "ทะเลลด", o.sub "EP.1", o.fs size), fish beside it, a crab · Tide.sandTitle(tl, id, t0, dur, o)
//                          runs the water off (o.from 0 = sea over the frame … o.to 1 = gone off the top) · o.hand true adds ตังค์'s
//                          right arm in from the bottom right corner (#id-hand: the edge of his yellow tank top at the shoulder; its
//                          shadow #id-hshd) — Tide.reach(tl, id, t0, dur, o) reaches it across the sand to fish 0 at (230, 1380),
//                          slowing with a little hesitant tremble, the fingers curling at the end (o.to the wrist's end, o.aim)
//   Sets.tideShop(L, o)    ยาย's shop (ร้านยายพร) · o.view:
//     "room"   inside, one fixed perspective (Tide.SHOP: 1 m at depth Z is 1100/Z px, the eye 1.45 m up at (400, 860), the back wall
//              at Z 5.6 from X −1.7 to 2.1): the open front on the right looks out over the deck rail to the beach and the sea (drawn
//              in the set, so the horizon stays on the eye line in any framing); the tin roof with a net of fishing floats and a
//              ceiling fan; on the back wall the drinks fridge, the chalk menu, the shrine shelf, the old photo and the clipping
//              (#id-clue: #id-photo, #id-clip) right over ยาย's spot, the shell-framed clock (#id-clock), the calendar, the shelves;
//              the counter, the near table, the stools and the ice cooler in front of the cast (#id-front, moved after the actors in
//              L.act, so the counter hides ยาย below the waist), the far table by the open front (in the set). Tide.shopPos(X, Z) → { x, y, s } the feet and
//              the rig scale for an adult (ตังค์ × 0.76); Tide.SHOP.spots: ยาย behind the counter (−0.1, 5.0) → (378, 1179) s 0.57,
//              จูน at its end (1.1, 3.3) → (767, 1343) s 0.86, ตังค์ (0.55, 2.7) → (624, 1451). o.clock "07:40" the time shown ·
//              Tide.clockBack(tl, id, t0, dur, o) spins only the clock's hands back o.hours (2) — a twitch forward, the spin with a
//              sweep trail, a small overshoot — and settles them on o.to ("07:40"); then the second hand ticks on
//     "wall"   the insert: the photo (#id-photo) on its nail and string, its glass dusty, the clipping (#id-clip) taped beside it, the
//              calendar with the 26th ringed in red, a ledge with shells and an offering · Tide.wipe(tl, id, t0, dur) ยาย's hand
//              comes in from the right in her cream sleeve with a checked cloth, rubs the dust off the glass in loops, lifts away;
//              a glint crosses the clean glass
//     "table"  the insert: a glass of water on the red table by the open front, the condiment rack, a bowl of น้ำปลาพริก; the sea and
//              its glitter behind in L.sky / L.far (blur them) · Tide.cupShake(tl, id, t0, dur, o) faint rings run across the water,
//              the glass shivers a pixel, the caustic quivers (o.amp 0.3, o.grow true builds it)
//     "door"   from the beach after everyone has gone ("eerie" light, a low camera): the folding doors open on the dark shop, the
//              empty space on the back wall where the photo hung (the clipping still there), one of ยาย's brown slippers on the
//              middle step, the broom fallen down the steps, a stool tipped over, her prints — one sandal, one bare foot — going
//              off to the left toward the hotel · Tide.doorWind(tl, id, t0, dur, o) a loose door leaf swings, the menu sheet flaps,
//              the awning's hem and the shell chime stir (o.amp 1; o.siren true blinks the tower's beacon on the hill)
//   Props as SVG strings for other sets: Tide.longtail(o) · Tide.coco(x, G, s, lean, seed, o) (o.fl frond length, o.trunk false) ·
//   Tide.tower(x, G, s, id) · Tide.evacSign(x, y, s, o) (o.dir 1 | −1 | 0 up) · Tide.fig(id, pal) · Tide.HOTEL { W, FH, NF, floorY(n) }
(function () {
  const { mk, f1, put, cloud2, crown, smoothClosed, blob } = Pop2;
  const Qk = window.Qk, T = Qk.tone, CS = Qk.cs;
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const OUT2 = `stroke="${INK}" stroke-width="2" stroke-linejoin="round"`;
  const Tide = (window.Tide = window.Tide || {});
  const ST = (Tide._st = Tide._st || {});
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const sm = (a, b, x) => { const k = clamp((x - a) / (b - a), 0, 1); return k * k * (3 - 2 * k); };
  const lerp = (a, b, k) => a + (b - a) * k;
  const hx = (h) => { h = h.replace("#", ""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); };
  const mix = (a, b, k) => { const A = hx(a), B = hx(b); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, "0")).join(""); };
  const el = (id) => document.getElementById(id);
  const P2 = (p) => `${f1(p[0])},${f1(p[1])}`;

  Sets.DEFS += `
    <linearGradient id="tdCloudM" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".7" stop-color="#eef4f8"/><stop offset="1" stop-color="#c4d6e2"/></linearGradient>
    <linearGradient id="tdCloudE" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6f0de"/><stop offset=".7" stop-color="#ddd8c6"/><stop offset="1" stop-color="#a8a898"/></linearGradient>
    <linearGradient id="tdCloudS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a928e"/><stop offset=".6" stop-color="#5a6266"/><stop offset="1" stop-color="#2c3238"/></linearGradient>
    <linearGradient id="tdTrunk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6e6052"/><stop offset=".55" stop-color="#9c8c78"/><stop offset="1" stop-color="#c8b8a0"/></linearGradient>
    <linearGradient id="tdFish" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3e5a6e"/><stop offset=".45" stop-color="#9fb8c4"/><stop offset=".6" stop-color="#e8f2f4"/><stop offset="1" stop-color="#f8fbfb"/></linearGradient>
    <linearGradient id="tdSign" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a6cc0"/><stop offset="1" stop-color="#1a4e94"/></linearGradient>
    <linearGradient id="tdTin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c4ccce"/><stop offset=".6" stop-color="#9aa4a8"/><stop offset="1" stop-color="#7a8488"/></linearGradient>
    <linearGradient id="tdTile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2683c"/><stop offset="1" stop-color="#b24626"/></linearGradient>
    <linearGradient id="tdCream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6ead0"/><stop offset="1" stop-color="#e6d4b0"/></linearGradient>
    <linearGradient id="tdTeal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4f9e9a"/><stop offset=".5" stop-color="#69b8b2"/><stop offset="1" stop-color="#4a948e"/></linearGradient>
    <linearGradient id="tdPole" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8e969a"/><stop offset=".45" stop-color="#e2e6e6"/><stop offset="1" stop-color="#a4acb0"/></linearGradient>
    <linearGradient id="tdHorn" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f4f6f4"/><stop offset="1" stop-color="#b8c0c2"/></linearGradient>
    <linearGradient id="tdPanel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a5e9c"/><stop offset=".5" stop-color="#1e3462"/><stop offset="1" stop-color="#2c4a84"/></linearGradient>
    <linearGradient id="tdTarp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a86d0"/><stop offset="1" stop-color="#215e9e"/></linearGradient>
    <linearGradient id="tdWoodH" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b88250"/><stop offset="1" stop-color="#8a5a32"/></linearGradient>
    <linearGradient id="tdStep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2ddd2"/><stop offset="1" stop-color="#b8b0a2"/></linearGradient>
    <radialGradient id="tdFoam"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".6" stop-color="#f2f6f6" stop-opacity=".7"/><stop offset="1" stop-color="#dfe8ea" stop-opacity="0"/></radialGradient>
    <radialGradient id="tdSpray"><stop offset="0" stop-color="#f4f8f8" stop-opacity=".75"/><stop offset=".55" stop-color="#e2eaec" stop-opacity=".35"/><stop offset="1" stop-color="#d8e2e4" stop-opacity="0"/></radialGradient>
    <radialGradient id="tdBeacon"><stop offset="0" stop-color="#ffd0c8" stop-opacity="1"/><stop offset=".3" stop-color="#ff4a3a" stop-opacity=".7"/><stop offset="1" stop-color="#ff3a2a" stop-opacity="0"/></radialGradient>
    <radialGradient id="tdGlint"><stop offset="0" stop-color="#ffffff" stop-opacity=".9"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>`;

  // ---------------- palettes per time of day ----------------
  const PAL = {
    morning: { sky: ["#2b7fd2", "#5ea9e6", "#aed8f0", "#eef6ee"], cloud: "tdCloudM", cl: ["#ffffff", "#9fb8ca"], sun: 0.75,
      sea: ["#b8dce0", "#5aa8cc", "#2a7fb6", "#1f9cb4", "#45c6c2", "#90e4d4"], sand: ["#f8eed8", "#eedcb6", "#dfc79c"], wet: ["#c7ab80", "#d8c29c"],
      bed: ["#b59e76", "#9c8966", "#84775c"], haze: "#e4f0ee", rock: "#c6b8a8", green: ["#2c6a3a", "#4c904a", "#8cc268"], leaf: ["#2f6e3a", "#4f9a44", "#9ccc6a"], light: 1 },
    eerie: { sky: ["#6a8697", "#9cb0b4", "#cfd2c0", "#f0e2bc"], cloud: "tdCloudE", cl: ["#f4f0e2", "#9a9c94"], sun: 0.35,
      sea: ["#c4cfc4", "#88a6a6", "#4b7b8c", "#4e8a90", "#7cb2aa", "#a8d0c2"], sand: ["#f0e4ca", "#e0cea8", "#ceb890"], wet: ["#b9a482", "#c8b490"],
      bed: ["#a2916e", "#887b5e", "#6e664f"], haze: "#e9dfc2", rock: "#bab09f", green: ["#365c3a", "#557a4a", "#86a266"], leaf: ["#34583a", "#567c48", "#94b070"], light: 0.75 },
    storm: { sky: ["#1e262e", "#36424a", "#5e6866", "#8e9084"], cloud: "tdCloudS", cl: ["#8a928e", "#22282e"], sun: 0,
      sea: ["#8a968e", "#53666a", "#344f5a", "#3c5a60", "#5a7a76", "#7a968c"], sand: ["#cabea4", "#b8a886", "#a2906e"], wet: ["#8c7c60", "#9c8c6e"],
      bed: ["#867658", "#6e624a", "#5a523e"], haze: "#8e9284", rock: "#8a8074", green: ["#1e3426", "#304a32", "#4a6442"], leaf: ["#1e3624", "#2e4c30", "#52704a"], light: 0.45 },
    // the squall the wave comes in under: a low grey lid, darker than a normal day but paler than the water so the wall stands out
    squall: { sky: ["#3c4854", "#62707a", "#949ea2", "#b6bab2"], cloud: "tdCloudS", cl: ["#a8b0ae", "#3a444a"], sun: 0,
      sea: ["#8a968e", "#53666a", "#344f5a", "#3c5a60", "#5a7a76", "#7a968c"], sand: ["#d6caae", "#c4b696", "#ae9e7e"], wet: ["#8e8064", "#a09074"],
      bed: ["#867658", "#6e624a", "#5a523e"], haze: "#9aa09a", rock: "#8a8074", green: ["#22382a", "#344e34", "#4e6846"], leaf: ["#26402a", "#3a5c38", "#6a8a56"], light: 0.55 },
  };

  // ---------------- sky ----------------
  function sky(L, id, P, hz, o = {}) {
    const r = mk(o.seed || 31), storm = P === PAL.storm;
    let g = `<defs><linearGradient id="${id}-skyG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(hz - 1900)}" x2="0" y2="${f1(hz + 30)}"><stop offset="0" stop-color="${P.sky[0]}"/><stop offset=".5" stop-color="${P.sky[1]}"/><stop offset=".84" stop-color="${P.sky[2]}"/><stop offset="1" stop-color="${P.sky[3]}"/></linearGradient></defs>`;
    g += `<rect x="-3000" y="${f1(hz - 4200)}" width="8000" height="${f1(4200 + 2200)}" fill="url(#${id}-skyG)"/>`;
    if (P.sun) g += `<circle cx="${o.sunX ?? 1480}" cy="${f1(o.sunY ?? hz - 1350)}" r="820" fill="url(#qkSun)" opacity="${P.sun}"/>`;
    for (let k = 0; k < 9; k++) { const cx = -900 + r() * 3000, cy = hz - 1750 + r() * 900, w = 380 + r() * 620; g += `<path d="M${f1(cx)},${f1(cy)}q${f1(w * 0.5)},${f1(-14 - r() * 18)} ${f1(w)},${f1(-4 + r() * 10)}" stroke="${storm ? "#58626a" : "#ffffff"}" stroke-width="${f1(6 + r() * 9)}" opacity="${f1(0.12 + r() * 0.14)}" stroke-linecap="round" fill="none"/>`; }
    for (let k = 0; k < 6; k++) g += cloud2(-760 + k * 640 + r() * 220, hz - 820 - r() * 700, 300 + r() * 320, 96 + r() * 60, r, P.cloud, P.cl[0], P.cl[1]);
    if (storm) for (let k = 0; k < 7; k++) g += cloud2(-900 + k * 560 + r() * 200, hz - 1300 + r() * 900, 900 + r() * 500, 300 + r() * 160, r, P.cloud, "#6a7472", "#141a20");
    put(L.sky, g);
    // far: a bank of tropical cumulus standing over the horizon haze
    let fr = "";
    for (let k = 0; k < 7; k++) fr += cloud2(-1000 + k * 560 + r() * 220, hz - 170 - r() * 160, 480 + r() * 520, 220 + r() * 170, r, P.cloud, P.cl[0], P.cl[1]);
    put(L.far, fr);
  }

  // ---------------- a limestone tower island (Phang Nga) ----------------
  // sheer streaked cliffs, an undercut notch at the waterline, a cap of jungle and plants on the ledges; v 0 (near) … 1 (far) hazes it
  function karst(id, k, x, base, w, h, r, P, v, sh = 0) {
    const L0 = x - w / 2, R0 = x + w / 2, pts = [];
    pts.push([L0 + w * 0.07, base + 3], [L0 + w * (0.04 + r() * 0.03), base - h * 0.07], [L0 - w * 0.02, base - h * (0.26 + r() * 0.1)], [L0 + w * (0.01 + r() * 0.05), base - h * 0.55], [L0 - w * 0.03, base - h * 0.78]);
    const n = 7;
    for (let i = 0; i <= n; i++) { const u = i / n; pts.push([L0 + w * (0.05 + 0.9 * u), base - h * (0.72 + 0.28 * Math.pow(Math.sin(Math.PI * Math.pow(u, 0.8 + sh)), 0.55) + (r() - 0.5) * 0.06)]); }
    pts.push([R0 + w * 0.03, base - h * 0.72], [R0 - w * (0.01 + r() * 0.04), base - h * 0.42], [R0 + w * 0.02, base - h * 0.14], [R0 - w * 0.05, base + 3]);
    const d = smoothClosed(pts), cid = `${id}-kc${k}`, hz = P.haze, fv = v * 0.72;
    const rock = mix(P.rock, hz, fv), rockD = mix(T(P.rock, -0.34), hz, fv), rockL = mix(T(P.rock, 0.2), hz, fv);
    let g = `<defs><clipPath id="${cid}"><path d="${d}"/></clipPath><linearGradient id="${cid}g" gradientUnits="userSpaceOnUse" x1="${f1(L0)}" y1="0" x2="${f1(R0)}" y2="0"><stop offset="0" stop-color="${rockD}"/><stop offset=".42" stop-color="${rock}"/><stop offset=".86" stop-color="${rockL}"/><stop offset="1" stop-color="${rock}"/></linearGradient></defs>`;
    g += `<path d="${d}" fill="url(#${cid}g)"/>`;
    let c = "";
    // the streaks: rust, soot and chalk running down from the cap
    for (let i = 0; i < 16; i++) {
      const sx = L0 + w * (0.06 + r() * 0.88), col = [mix("#b97a46", hz, fv), mix("#4e463e", hz, fv), mix("#f2ece0", hz, fv)][i % 3], wv = w * (0.006 + r() * 0.02);
      let p = `M${f1(sx)},${f1(base - h * (0.8 + r() * 0.2))}`;
      for (let yy = 1; yy <= 6; yy++) p += `L${f1(sx + Math.sin(yy * 1.7 + i) * w * 0.012)},${f1(base - h * (0.82 - yy * 0.13))}`;
      c += `<path d="${p}" stroke="${col}" stroke-width="${f1(wv)}" fill="none" opacity="${f1(0.22 + r() * 0.3)}" stroke-linecap="round"/>`;
    }
    // the notch the sea has bitten out at the waterline, and its lit lip
    c += `<rect x="${f1(L0 - 40)}" y="${f1(base - h * 0.085)}" width="${f1(w + 80)}" height="${f1(h * 0.1)}" fill="${mix("#2c2620", hz, fv)}" opacity=".55"/>`;
    c += `<path d="M${f1(L0 - 40)},${f1(base - h * 0.09)}H${f1(R0 + 40)}" stroke="${rockL}" stroke-width="${f1(Math.max(1, h * 0.012))}" opacity=".6"/>`;
    // shade on the left flank
    c += `<rect x="${f1(L0 - 40)}" y="${f1(base - h * 1.1)}" width="${f1(w * 0.3)}" height="${f1(h * 1.2)}" fill="${mix("#1e2a2e", hz, fv)}" opacity=".18"/>`;
    g += `<g clip-path="url(#${cid})">${c}</g>`;
    // the jungle cap and plants on the ledges
    const G0 = mix(P.green[0], hz, fv), G1 = mix(P.green[1], hz, fv), G2 = mix(P.green[2], hz, fv);
    let cap = "";
    for (let i = 0; i < n + 6; i++) { const u = i / (n + 5), px = L0 + w * (0.03 + 0.94 * u), py = base - h * (0.72 + 0.28 * Math.pow(Math.sin(Math.PI * u), 0.55)) + h * 0.03, R = w * (0.05 + r() * 0.05); cap += `<path d="${blob(px, py, R, r, 8)}" fill="${G0}"/>`; }
    for (let i = 0; i < n + 4; i++) { const u = i / (n + 3), px = L0 + w * (0.06 + 0.88 * u), py = base - h * (0.73 + 0.28 * Math.pow(Math.sin(Math.PI * u), 0.55)), R = w * (0.035 + r() * 0.035); cap += `<path d="${blob(px - R * 0.2, py - R * 0.25, R, r, 7)}" fill="${G1}"/>`; }
    for (let i = 0; i < n; i++) { const u = (i + 0.5) / n, px = L0 + w * (0.25 + 0.7 * u), py = base - h * (0.76 + 0.28 * Math.pow(Math.sin(Math.PI * u), 0.55)), R = w * (0.022 + r() * 0.02); cap += `<path d="${blob(px - R * 0.3, py - R * 0.3, R, r, 6)}" fill="${G2}"/>`; }
    for (let i = 0; i < 7; i++) { const side = r() < 0.5, px = side ? L0 + w * (0.02 + r() * 0.12) : R0 - w * (0.02 + r() * 0.12), py = base - h * (0.25 + r() * 0.5), R = w * (0.02 + r() * 0.025); cap += `<path d="${blob(px, py, R, r, 6)}" fill="${G1}"/><path d="M${f1(px)},${f1(py)}q${f1(R * 0.3)},${f1(R * 2)} 0,${f1(R * 3.4)}" stroke="${G0}" stroke-width="${f1(Math.max(1, R * 0.25))}" fill="none"/>`; }
    g += cap;
    return { g, d };
  }

  // ---------------- a coconut palm: a curved ringed trunk, a crown of drooping pinnate fronds, a bunch of coconuts ----------------
  // origin (x, G) the foot; H 900·s tall; lean the crown's sideways offset as a fraction of the height; o.q detail 1 | 0.5; o.id → the
  // fronds group gets that id and data-o (the crown) so they can sway; o.pal [dark, mid, light] leaves; o.trunk false (fronds only)
  function coco(x, G, s, lean, seed, o = {}) {
    const r = mk(seed), H = 900, cx = lean * H, cy = -H, q = o.q ?? 1, pal = o.pal || ["#2f6e3a", "#4f9a44", "#9ccc6a"];
    const B = (u) => { const b = 2 * u * (1 - u), c = u * u; return [b * lean * H * 0.08 + c * cx, b * -H * 0.56 + c * cy]; };
    const Wd = (u) => lerp(30, 15, u);
    let g = "";
    if (o.trunk !== false) {
      g += CS(-60, 4, 120, 20, 0.8);
      const Lp = [], Rp = [];
      for (let i = 0; i <= 20; i++) { const u = i / 20, [px, py] = B(u), [qx, qy] = B(Math.min(1, u + 0.01)), dx = qx - px, dy = qy - py, len = Math.hypot(dx, dy) || 1, nx = -dy / len, ny = dx / len, w = Wd(u) + (i === 0 ? 10 : 0); Lp.push([px - nx * w, py - ny * w]); Rp.push([px + nx * w, py + ny * w]); }
      g += `<path d="M${Lp.map(P2).join("L")}L${Rp.reverse().map(P2).join("L")}Z" fill="url(#tdTrunk)" ${OUT3}/>`;
      let rings = "";
      for (let i = 1; i < 34; i++) { const u = i / 34, [px, py] = B(u), w = Wd(u); rings += `M${f1(px - w * 0.9)},${f1(py + 2)}q${f1(w * 0.9)},${f1(5 + w * 0.12)} ${f1(w * 1.8)},0`; }
      g += `<path d="${rings}" stroke="#5a4c40" stroke-width="2.4" fill="none" opacity=".55"/>`;
      g += `<path d="${Array.from({ length: 12 }, (_, i) => { const u = (i + 0.5) / 12, [px, py] = B(u), w = Wd(u); return `M${f1(px + w * 0.35)},${f1(py)}l${f1(w * 0.3)},${f1(-H / 30)}`; }).join("")}" stroke="#efe2c8" stroke-width="3" opacity=".45"/>`;
    }
    // fronds: each a drooping fringe of leaflets hanging from an arching rachis (light on top, a darker underside), back ones darker
    let fr = `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="30" fill="#4a3e2c"/>`;
    const N = Math.round(12 * (q < 1 ? 0.8 : 1)), FL = o.fl ?? 1;
    const fronds = [];
    for (let k = 0; k < N; k++) {
      const a = (-196 + (k / (N - 1)) * 212 + (r() - 0.5) * 14) * Math.PI / 180, len = (320 + r() * 100) * FL;
      const dx = Math.cos(a), up = Math.sin(a);
      fronds.push({ P0: [cx, cy], P1: [cx + dx * len * 0.5, cy + up * len * 0.42 - 60 * FL], P3: [cx + dx * len, cy + up * len * 0.3 + (100 + (1 - Math.abs(up)) * 130) * FL], len, back: up < -0.55 });
    }
    fronds.push({ P0: [cx, cy], P1: [cx + 40 * FL, cy + 140 * FL], P3: [cx + 30 * FL, cy + 330 * FL], len: 300 * FL, back: true, dead: true });
    fronds.sort((a, b) => (b.back ? 1 : 0) - (a.back ? 1 : 0));
    fronds.forEach((f) => {
      const pt = (u) => [(1 - u) * (1 - u) * f.P0[0] + 2 * u * (1 - u) * f.P1[0] + u * u * f.P3[0], (1 - u) * (1 - u) * f.P0[1] + 2 * u * (1 - u) * f.P1[1] + u * u * f.P3[1]];
      const M = Math.round(26 * q), top = [], bot = [], lines = [];
      for (let i = 0; i <= M; i++) {
        const u = 0.04 + (i / M) * 0.96, [px, py] = pt(u), [qx, qy] = pt(Math.min(1, u + 0.01)), tx = qx - px, ty = qy - py, tl = Math.hypot(tx, ty) || 1;
        let nx = -ty / tl, ny = tx / tl; if (ny < 0) { nx = -nx; ny = -ny; }
        const ll = f.len * 0.34 * Math.pow(Math.sin(Math.PI * Math.min(1, u * 1.12 + 0.04)), 0.75) * (i % 2 ? 0.74 : 1);
        const ex = px + (nx * 0.38 - tx / tl * 0.22) * ll, ey = py + (ny * 0.38 + 0.92) * ll;
        top.push([px, py]); bot.push([ex, ey]);
        if (i % 2 === 0) lines.push(`M${f1(px)},${f1(py)}L${f1(ex)},${f1(ey)}`);
      }
      const shape = `M${top.map(P2).join("L")}L${bot.slice().reverse().map(P2).join("L")}Z`;
      const c0 = f.dead ? "#7a6a3e" : f.back ? T(pal[0], -0.2) : pal[0], c1 = f.dead ? "#a89050" : f.back ? T(pal[1], -0.15) : pal[1], c2 = f.dead ? "#c8b070" : pal[2];
      fr += `<path d="${shape}" fill="${c0}" transform="translate(5,7)" opacity=".75"/><path d="${shape}" fill="${c1}"/>`;
      fr += `<path d="${lines.join("")}" stroke="${c0}" stroke-width="2.4" opacity=".75"/>`;
      fr += `<path d="M${P2(f.P0)}Q${P2(f.P1)} ${P2(f.P3)}" stroke="${c2}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".95"/>`;
    });
    // the coconuts under the crown
    const nuts = [[-22, 24], [6, 30], [30, 20], [-6, 44], [20, 42]].map(([nx, ny]) => `<circle cx="${f1(cx + nx)}" cy="${f1(cy + ny)}" r="17" fill="${r() < 0.5 ? "#7c8a3a" : "#8e6a34"}" ${OUT2}/><circle cx="${f1(cx + nx + 5)}" cy="${f1(cy + ny - 6)}" r="5" fill="#fff" opacity=".35"/>`).join("");
    fr += nuts;
    const fid = o.id ? ` id="${o.id}" data-o="${f1(cx)} ${f1(cy)}"` : "";
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}<g${fid}>${fr}</g></g>`;
  }
  Tide.coco = coco;

  // ---------------- a casuarina (สนทะเล): a thin dark trunk and tiers of drooping needle tufts ----------------
  function casu(x, G, s, seed, pal) {
    const r = mk(seed);
    let g = CS(-30, 4, 90, 14, 0.6) + `<path d="M-7,0Q-2,-300 3,-660L9,-660Q8,-300 9,0Z" fill="#4a3c30"/>`;
    for (let t = 0; t < 9; t++) {
      const yy = -700 + t * 64, wv = 26 + t * 20;
      for (let k = 0; k < 3 + Math.floor(t / 2); k++) {
        const tx = (r() - 0.5) * wv * 2, ty = yy + (r() - 0.5) * 30, w = 34 + r() * 30, h = 70 + r() * 50, c = [pal[0], T(pal[0], -0.15), pal[1]][k % 3];
        g += `<path d="M${f1(tx - w / 2)},${f1(ty)}Q${f1(tx)},${f1(ty - h * 0.5)} ${f1(tx + w / 2)},${f1(ty)}L${f1(tx + w * 0.4)},${f1(ty + h * 0.6)}Q${f1(tx)},${f1(ty + h)} ${f1(tx - w * 0.4)},${f1(ty + h * 0.6)}Z" fill="${c}"/>`;
        let st = ""; for (let j = 0; j < 6; j++) { const sx = tx - w * 0.35 + j * w * 0.14; st += `M${f1(sx)},${f1(ty + h * 0.55)}q${f1((r() - 0.5) * 6)},${f1(h * 0.2)} ${f1((r() - 0.5) * 8)},${f1(h * 0.45)}`; }
        g += `<path d="${st}" stroke="${c}" stroke-width="2.4" fill="none" stroke-linecap="round"/>`;
      }
    }
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  }

  // ---------------- a longtail boat (เรือหางยาว), side on ----------------
  // local: stern at x −500, the bow at +500, the waterline y 0, keel ~ +40, the prow's tip (548, −336); o.hull o.band o.stripe colours,
  // o.flip faces left, o.water the local sea colour for the waterline band (o.wid gives it an id), o.canopy, o.no registration text
  Tide.longtail = (o = {}) => {
    const c = o.hull || "#2f6fa0", band = o.band || "#d8423a", stripe = o.stripe || "#f4f2e8";
    const hull = "M-500,-120L-486,-34Q-472,18 -398,32L300,40Q420,36 470,-40Q500,-108 520,-210Q532,-290 548,-336Q553,-348 544,-344Q530,-300 512,-214Q496,-150 436,-140Q20,-104 -500,-120Z";
    const cid = `lt${Math.floor((o.seed || 1) * 7919) % 100000}${o.k || 0}`;
    let g = `<defs><clipPath id="${cid}"><path d="${hull}"/></clipPath></defs>`;
    // the inside of the boat seen from above the near rail: the far rail, thwarts, a fuel can, a coil of rope
    g += `<path d="M-492,-122Q20,-106 436,-142L452,-168Q20,-136 -480,-150Z" fill="#3a2a1e" ${OUT2}/>`;
    g += [-300, -80, 140, 330].map((tx) => `<path d="M${tx},-118l14,-24h46l-10,24z" fill="#a8743e" ${OUT2}/>`).join("");
    g += `<rect x="-200" y="-150" width="34" height="30" rx="5" fill="#d84a36" ${OUT2}/><ellipse cx="60" cy="-136" rx="30" ry="9" fill="none" stroke="#e8d8a8" stroke-width="5"/>`;
    if (o.canopy) g += `<path d="M-180,-118V-262M240,-142V-270" stroke="#7a6a5a" stroke-width="7"/><path d="M-220,-262Q30,-300 280,-270L270,-246Q30,-276 -210,-240Z" fill="url(#tdTarp)" ${OUT2}/>`;
    g += `<path d="${hull}" fill="${c}"/>`;
    // paint: the sheer strake in wood, a white stripe, a red band, dark bottom below the waterline
    g += `<g clip-path="url(#${cid})"><rect x="-520" y="-170" width="1100" height="70" fill="url(#tdWoodH)"/><path d="M-520,-100Q20,-78 520,-120L520,-104Q20,-62 -520,-84Z" fill="${stripe}"/>
      <path d="M-520,-84Q20,-62 520,-104L520,-90Q20,-48 -520,-70Z" fill="${band}"/><rect x="-520" y="4" width="1100" height="60" fill="${T(c, -0.45)}"/>
      <path d="M-520,-30Q20,-6 520,-60" stroke="#fff" stroke-width="5" opacity=".18" fill="none"/>
      ${[-140, -126, -112].map((y) => `<path d="M-520,${y}Q20,${y + 28} 440,${y - 20}" stroke="#6a4424" stroke-width="2" opacity=".5" fill="none"/>`).join("")}
      <path d="M440,-150Q505,-170 548,-336" stroke="#fff" stroke-width="10" opacity=".22" fill="none"/></g>`;
    g += `<path d="${hull}" fill="none" ${OUT3}/>`;
    g += `<path d="M-500,-122Q20,-106 436,-142Q500,-150 536,-300" stroke="#c89464" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M-500,-126Q20,-110 436,-146" stroke="#f4dcb0" stroke-width="3" fill="none" opacity=".8"/>`;
    if (o.no !== false) g += o.flip ? `<text x="-420" y="-58" transform="scale(-1,1)" font-family="Kanit" font-weight="700" font-size="26" fill="#fff" opacity=".9">${o.no || "พง 3127"}</text>` : `<text x="300" y="-58" font-family="Kanit" font-weight="700" font-size="26" fill="#fff" opacity=".9">${o.no || "พง 3127"}</text>`;
    // the engine on its pivot at the stern, the long shaft and the propeller, the tiller
    g += `<path d="M-470,-140L-520,-196" stroke="#5a5048" stroke-width="12"/><g transform="translate(-505,-226)"><rect x="-58" y="-40" width="116" height="72" rx="10" fill="#6a7074" ${OUT2}/>
      ${[-36, -18, 0, 18, 36].map((xx) => `<path d="M${xx},-36v62" stroke="#4a5054" stroke-width="5"/>`).join("")}<rect x="-58" y="-40" width="116" height="14" rx="6" fill="#9aa2a6"/><circle cx="34" cy="-48" r="12" fill="#d84a36" ${OUT2}/><rect x="-74" y="-6" width="18" height="30" fill="#3e4448" ${OUT2}/></g>`;
    g += `<path d="M-540,-196L-860,28" stroke="#7e868a" stroke-width="11" stroke-linecap="round"/><path d="M-540,-196L-860,28" stroke="#d8dcdc" stroke-width="3" opacity=".6"/>`;
    g += `<g transform="translate(-864,32) rotate(-35)"><ellipse rx="10" ry="34" fill="#c8a040" ${OUT2}/></g><path d="M-470,-226L-300,-262" stroke="#5a5048" stroke-width="8" stroke-linecap="round"/>`;
    // the prow: a garland of marigolds and jasmine, ribbons (ผ้าสามสี) knotted round the stem and streaming back
    const rib = ["#e8302a", "#f6c02a", "#2e9a4a", "#ffffff", "#e84a9a"];
    rib.forEach((cc, i) => { const sx = 538 - i * 3, sy = -312 + i * 6; g += `<path d="M${sx},${sy}C${sx - 40},${sy + 30 + i * 8} ${sx - 70},${sy + 10 + i * 10} ${sx - 110 - i * 8},${sy + 50 + i * 12}" stroke="${cc}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".95"/>`; });
    g += `<path d="M528,-300L552,-306M524,-286L550,-292" stroke="#f6c02a" stroke-width="7"/>`;
    for (let i = 0; i < 9; i++) { const u = i / 8, gx = 520 + Math.sin(u * Math.PI) * 26 - 12, gy = -268 + u * 70; g += `<circle cx="${f1(gx)}" cy="${f1(gy)}" r="8" fill="${i % 2 ? "#f4a020" : "#ffe7a0"}" stroke="#a86010" stroke-width="1.5"/>`; }
    g += `<path d="M514,-274Q492,-226 520,-196" stroke="#f8f6ee" stroke-width="6" stroke-dasharray="3 5" fill="none"/>`;
    // the waterline band (shown while afloat): the sea laps the hull
    if (o.water) g += `<g${o.wid ? ` id="${o.wid}"` : ""}><path d="M-560,-6Q20,4 560,-10V80H-560Z" fill="${o.water}"/><path d="M-560,-6Q-300,-12 -60,0T560,-10" stroke="#fff" stroke-width="5" fill="none" opacity=".75"/><path d="M-520,10Q-200,4 120,14T540,6" stroke="#fff" stroke-width="2.5" fill="none" opacity=".35"/></g>`;
    return o.flip ? `<g transform="scale(-1,1)">${g}</g>` : g;
  };

  // ---------------- ยาย's seafood shop: a wooden shack on stumps, tin roof, blue awning, hand-painted sign ----------------
  // origin = the sand under the front middle; ~600 wide, 470 tall at s = 1; the old photo + the clipping on the back wall (#id-clue)
  function shop(id, x, G, s, r) {
    let g = CS(0, 6, 360, 34, 0.9);
    // stumps and the shadow under the deck
    g += `<rect x="-300" y="-54" width="600" height="54" fill="#000" opacity=".28"/>`;
    [-280, -140, 0, 140, 270].forEach((px) => { g += `<rect x="${px - 10}" y="-50" width="20" height="50" fill="#bcb6aa" ${OUT2}/>`; });
    // the back wall in faded teal planks, the side wall
    g += `<rect x="-292" y="-372" width="584" height="318" fill="url(#tdTeal)" ${OUT3}/>`;
    for (let k = 0; k < 15; k++) g += `<path d="M${-292 + k * 39},-372V-54" stroke="#3e7e7a" stroke-width="2.5" opacity=".7"/><rect x="${-288 + k * 39}" y="${-360 + (k % 4) * 60}" width="${8 + (k % 3) * 6}" height="${30 + (k % 5) * 12}" fill="#d8e8e0" opacity=".25"/>`;
    // the window with its shutter propped up
    g += `<rect x="-250" y="-300" width="150" height="110" fill="#22343a" ${OUT2}/><path d="M-252,-300L-260,-352H-92L-100,-300Z" fill="#5a9a94" ${OUT2}/><path d="M-176,-300V-190M-250,-246H-100" stroke="#4a8a84" stroke-width="5"/>`;
    // the clue: an old framed photo (two men on a boat) and a yellowed newspaper clipping taped beside it
    g += `<g id="${id}-clue"><rect x="40" y="-312" width="78" height="62" fill="#5a3a22" ${OUT2}/><rect x="48" y="-304" width="62" height="46" fill="#cfc2a0"/>
      <path d="M50,-268Q78,-262 108,-270V-258H50Z" fill="#7a6a54"/><circle cx="68" cy="-286" r="6" fill="#6a5a46"/><circle cx="90" cy="-284" r="6" fill="#6a5a46"/><path d="M62,-280h12v14h-12zM84,-278h12v12h-12z" fill="#6a5a46"/>
      <g transform="rotate(4 160 -270)"><rect x="132" y="-318" width="62" height="80" fill="#efe0b2" ${OUT2}/><rect x="138" y="-312" width="50" height="9" fill="#5a5040"/><rect x="138" y="-298" width="22" height="18" fill="#9a8c70"/>
      ${[-298, -292, -286, -280, -272, -266, -260, -254, -248].map((yy, i) => `<path d="M${i < 4 ? 164 : 138},${yy}H188" stroke="#7a705c" stroke-width="2"/>`).join("")}<rect x="150" y="-324" width="26" height="10" fill="#f4f0e0" opacity=".8" transform="rotate(-8 163 -319)"/></g></g>`;
    // a calendar, a shell wind chime, a lantern under the eave
    g += `<rect x="220" y="-320" width="44" height="58" fill="#f4f2ea" ${OUT2}/><rect x="220" y="-320" width="44" height="16" fill="#d84a36"/><text x="242" y="-276" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="20" fill="#2e2a26">26</text>`;
    // the deck: planks seen from the front edge and a sliver of top
    g += `<rect x="-306" y="-70" width="612" height="20" fill="#a8743e" ${OUT2}/><rect x="-306" y="-82" width="612" height="12" fill="#c89464"/>${Array.from({ length: 12 }, (_, k) => `<path d="M${-300 + k * 52},-70v20" stroke="#6a4424" stroke-width="2"/>`).join("")}`;
    // posts holding the roof
    [-296, 296].forEach((px) => { g += `<rect x="${px - 9}" y="-430" width="18" height="360" fill="#9a6a3e" ${OUT2}/>`; });
    // tables and stools, the cooler, the grill with squid and smoke
    const table = (tx, c) => `<rect x="${tx - 60}" y="-150" width="120" height="12" rx="4" fill="${c}" ${OUT2}/><path d="M${tx - 50},-138L${tx - 56},-82M${tx + 50},-138L${tx + 56},-82" stroke="${T(c, -0.3)}" stroke-width="7"/>
      <rect x="${tx - 92}" y="-118" width="36" height="8" rx="3" fill="#2a6ab8" ${OUT2}/><path d="M${tx - 88},-110l-4,28M${tx - 60},-110l4,28" stroke="#1e4e8a" stroke-width="5"/><rect x="${tx + 56}" y="-118" width="36" height="8" rx="3" fill="#2a6ab8" ${OUT2}/><path d="M${tx + 60},-110l-4,28M${tx + 88},-110l4,28" stroke="#1e4e8a" stroke-width="5"/>`;
    g += table(-150, "#d8402e") + table(60, "#d8402e");
    g += `<rect x="168" y="-168" width="110" height="86" rx="8" fill="#f4f6f4" ${OUT2}/><rect x="168" y="-168" width="110" height="18" rx="6" fill="#dfe6e8"/><rect x="176" y="-140" width="30" height="8" fill="#2a8ad0"/><text x="223" y="-110" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="17" fill="#2a6ab8">น้ำแข็ง</text>`;
    // the shop's front edge and roof: tin with rust, a blue tarp awning with a scalloped hem
    g += `<path d="M-330,-432L330,-432L360,-396H-360Z" fill="url(#tdTin)" ${OUT3}/>${Array.from({ length: 24 }, (_, k) => `<path d="M${-330 + k * 28},-432L${-358 + k * 30},-396" stroke="#7a8488" stroke-width="2.5" opacity=".7"/>`).join("")}
      ${[-250, -60, 140, 270].map((rx) => `<path d="M${rx},-430q4,18 -2,34" stroke="#b0643a" stroke-width="7" opacity=".55"/>`).join("")}`;
    g += `<path d="M-360,-396H360V-364Q342,-348 324,-364Q306,-348 288,-364Q270,-348 252,-364Q234,-348 216,-364Q198,-348 180,-364Q162,-348 144,-364Q126,-348 108,-364Q90,-348 72,-364Q54,-348 36,-364Q18,-348 0,-364Q-18,-348 -36,-364Q-54,-348 -72,-364Q-90,-348 -108,-364Q-126,-348 -144,-364Q-162,-348 -180,-364Q-198,-348 -216,-364Q-234,-348 -252,-364Q-270,-348 -288,-364Q-306,-348 -324,-364Q-342,-348 -360,-364Z" fill="url(#tdTarp)" ${OUT2}/>
      <path d="M-360,-390H360" stroke="#7ab8f0" stroke-width="4" opacity=".6"/>`;
    // the sign on the roof: white board, blue frame, red letters, a fish and a crab painted at the ends
    g += `<rect x="-232" y="-520" width="464" height="92" rx="8" fill="#f8f4ea" stroke="#1e4e94" stroke-width="7"/><path d="M-200,-428V-400M200,-428V-400" stroke="#6a5a4a" stroke-width="8"/>
      <text x="0" y="-468" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="50" fill="#d8302a" stroke="#7a1410" stroke-width="1.5">ร้านยายพร</text>
      <text x="0" y="-438" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#1e4e94">อาหารทะเลสด · ปลาเผา หมึกย่าง</text>
      <g transform="translate(-196,-474)"><path d="M-22,0C-10,-14 12,-14 20,-4L32,-12L30,0L32,12L20,4C12,14 -10,14 -22,0Z" fill="#3a8ad0" ${OUT2}/><circle cx="-12" cy="-2" r="2.5" fill="${INK}"/></g>
      <g transform="translate(196,-474)"><ellipse rx="18" ry="12" fill="#e8582a" ${OUT2}/><path d="M-16,-8l-10,-12M16,-8l10,-12M-14,8l-10,8M14,8l10,8" stroke="#e8582a" stroke-width="4"/><circle cx="-6" cy="-10" r="3" fill="${INK}"/><circle cx="6" cy="-10" r="3" fill="${INK}"/></g>`;
    // the grill out front: a charcoal tray on legs with squid on skewers, a little smoke; a menu board; a Thai flag on the post
    g += `<g transform="translate(-250,-20)"><path d="M-46,0L-40,-60M46,0L40,-60" stroke="#3a3a3a" stroke-width="6"/><rect x="-56" y="-78" width="112" height="22" rx="4" fill="#4a4a4e" ${OUT2}/><rect x="-50" y="-80" width="100" height="6" fill="#ff8a3a"/>
      ${[-36, -12, 12, 36].map((sx) => `<path d="M${sx},-86l6,-40" stroke="#c8a870" stroke-width="3"/><ellipse cx="${sx + 4}" cy="-108" rx="9" ry="16" fill="#f0d8c0" ${OUT2}/>`).join("")}
      <path d="M-20,-130q-14,-40 6,-70q14,-30 -2,-60" stroke="#f2f2f2" stroke-width="16" fill="none" opacity=".25" stroke-linecap="round"/></g>`;
    g += `<g transform="translate(330,0) rotate(-6)"><path d="M-36,0L-24,-120M36,0L24,-120" stroke="#8a5a32" stroke-width="7"/><rect x="-44" y="-170" width="88" height="96" rx="6" fill="#2e3a34" stroke="#8a5a32" stroke-width="6"/>
      ${["ปลาเผา", "หมึกย่าง", "กุ้งเผา", "ข้าวผัด"].map((t, i) => `<text x="-34" y="${-146 + i * 21}" font-family="Mali" font-weight="700" font-size="15" fill="#f4f0e2">${t}</text>`).join("")}</g>`;
    g += `<path d="M-296,-430V-520" stroke="#9a9a9a" stroke-width="5"/><g transform="translate(-296,-520)">${["#e0282a", "#ffffff", "#2a3a8a", "#ffffff", "#e0282a"].map((c, i) => `<rect x="0" y="${i * 9}" width="64" height="${i === 2 ? 18 : 9}" fill="${c}" transform="translate(0,${i > 2 ? 9 : 0})"/>`).join("")}</g>`;
    // a hanging shell chime and a lantern at the eave
    g += `<path d="M-60,-364V-330M-50,-364V-322M-40,-364V-334" stroke="#8a7a6a" stroke-width="1.5"/><circle cx="-60" cy="-326" r="5" fill="#f4e8d8" ${OUT2}/><circle cx="-50" cy="-318" r="5" fill="#f8d8d0" ${OUT2}/><circle cx="-40" cy="-330" r="5" fill="#f4e8d8" ${OUT2}/>`;
    return `<g id="${id}-shop" transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  }

  // ---------------- the hotel (โรงแรมแหลมหอย): five storeys of reinforced concrete beside ยาย's shop — the vertical refuge ----------------
  // origin = the ground under the middle; W 560 wide, FH 104 a storey (storey n's band is y −n·FH … −(n−1)·FH), a flat roof at −5·FH
  // with a parapet and a steel railing; the outside stair tower on the right (stairwell windows with the flights behind them).
  // ids: #id-hotel, #id-f1 … #id-f5 (each storey's front, to wet or flood it), #id-roof (slab, railing, tank), #id-stair, #id-hsign
  const HOTEL = { W: 560, FH: 104, NF: 5, floorY: (n) => -n * 104 };
  Tide.HOTEL = HOTEL;
  function hotel(id, x, G, s) {
    const { W, FH, NF } = HOTEL, top = -NF * FH, SW = 112, X0 = -W / 2, X1 = W / 2 - SW;
    let g = CS(30, 8, 440, 36, 0.85);
    // the shaded side wall receding to the left
    g += `<path d="M${X0},${top - 30}L${X0 - 70},${top - 4}V-6L${X0},0Z" fill="#cbbfa8" ${OUT3}/>`;
    for (let n = 1; n < NF; n++) g += `<path d="M${X0},${-n * FH}L${X0 - 70},${-n * FH + 22}" stroke="#a89c86" stroke-width="5"/>`;
    for (let n = 1; n <= NF; n++) {
      const y0 = -n * FH, y1 = y0 + FH;
      let f = `<rect x="${X0}" y="${y0}" width="${X1 - X0}" height="${FH}" fill="#f4f0e6"/>`;
      if (n === 1) {
        // the lobby: a glass front, the entrance canopy, two potted palms
        f += `<rect x="${X0 + 20}" y="${y0 + 22}" width="${X1 - X0 - 40}" height="${FH - 22}" fill="#9ccbd8" ${OUT2}/>`;
        for (let k = 1; k < 6; k++) f += `<path d="M${X0 + 20 + k * (X1 - X0 - 40) / 6},${y0 + 22}V${y1}" stroke="#5a7a86" stroke-width="3"/>`;
        f += `<path d="M${X0 + 30},${y1}L${X0 + 110},${y0 + 22}H${X0 + 150}L${X0 + 70},${y1}Z" fill="#fff" opacity=".35"/><path d="M${X0 + 220},${y1}L${X0 + 290},${y0 + 22}H${X0 + 310}L${X0 + 240},${y1}Z" fill="#fff" opacity=".25"/>`;
        f += `<path d="M${X0 + 120},${y0 + 14}H${X0 + 330}L${X0 + 344},${y0 + 34}H${X0 + 106}Z" fill="#8a6a4a" ${OUT2}/>`;
      } else {
        // four rooms: a recessed balcony, a sliding glass door with a curtain, a glass railing with a steel top rail, an AC unit
        const bw = (X1 - X0) / 4;
        for (let k = 0; k < 4; k++) {
          const bx = X0 + k * bw;
          f += `<rect x="${bx + 8}" y="${y0 + 10}" width="${bw - 16}" height="${FH - 14}" fill="#c6c0b2"/>`;
          f += `<rect x="${bx + 18}" y="${y0 + 18}" width="${bw - 36}" height="${FH - 24}" fill="#7fb2c4" ${OUT2}/><path d="M${bx + bw / 2},${y0 + 18}V${y1 - 6}" stroke="#4a6a78" stroke-width="3"/>`;
          f += `<path d="M${bx + 22},${y0 + 20}H${bx + 44}V${y1 - 8}H${bx + 22}Z" fill="${["#f2e6c8", "#e8d0c0", "#d8e4e8", "#f0e0b8"][(k + n) % 4]}" opacity=".9"/>`;
          f += `<path d="M${bx + bw - 34},${y1 - 6}L${bx + bw - 22},${y0 + 18}H${bx + bw - 12}L${bx + bw - 24},${y1 - 6}Z" fill="#fff" opacity=".35"/>`;
          f += `<rect x="${bx + 6}" y="${y1 - 40}" width="${bw - 12}" height="38" fill="#bfe4ea" opacity=".45"/><path d="M${bx + 6},${y1 - 40}H${bx + bw - 6}" stroke="#d8dcdc" stroke-width="5"/>`;
          if ((k + n) % 3 === 0) f += `<rect x="${bx + bw - 60}" y="${y1 - 32}" width="36" height="26" fill="#d8dcdc" ${OUT2}/><circle cx="${bx + bw - 42}" cy="${y1 - 19}" r="8" fill="#9aa0a2"/>`;
          if ((k * 3 + n) % 5 === 1) f += `<path d="M${bx + 30},${y1 - 42}h28v24h-28z" fill="${["#e84a3a", "#2a8ad0", "#f2c030"][(k + n) % 3]}" ${OUT2}/>`;
        }
      }
      // the slab edge under the storey
      f += `<rect x="${X0 - 6}" y="${y1 - 7}" width="${X1 - X0 + 12}" height="10" fill="#e4dccc" ${OUT2}/>`;
      g += `<g id="${id}-f${n}">${f}</g>`;
    }
    // the outside stair tower: concrete with a column of stairwell windows, the flights zig-zagging behind the glass
    let st = `<rect x="${X1}" y="${top - 40}" width="${SW}" height="${-top + 40}" fill="#ebe4d6" ${OUT3}/>`;
    for (let n = 1; n <= NF; n++) {
      const y0 = -n * FH;
      st += `<rect x="${X1 + 22}" y="${y0 + 14}" width="${SW - 44}" height="${FH - 24}" fill="#4e6a74" ${OUT2}/>`;
      st += `<path d="M${X1 + 26},${y0 + FH - 14}L${X1 + SW - 26},${y0 + 22}" stroke="#d8d0c0" stroke-width="9"/><path d="M${X1 + 26},${y0 + FH - 34}L${X1 + SW - 26},${y0 + 4}" stroke="#f4f0e6" stroke-width="2.5"/>`;
      st += `<path d="M${X1 + 26},${y0 + 16}L${X1 + 40},${y0 + 16}L${X1 + 26},${y0 + 50}Z" fill="#fff" opacity=".22"/>`;
    }
    st += `<rect x="${X1 + 30}" y="${top - 30}" width="${SW - 60}" height="18" fill="#2e8a4a" ${OUT2}/><path d="M${X1 + 40},${top - 21}h12l-4,-4m4,4l-4,4" stroke="#fff" stroke-width="2" fill="none"/>`;
    g += `<g id="${id}-stair">${st}</g>`;
    // the flat roof: the slab edge, a parapet, a steel railing all round, a water tank and the sign
    let rf = `<rect x="${X0 - 8}" y="${top - 10}" width="${X1 - X0 + 16}" height="14" fill="#e4dccc" ${OUT2}/><rect x="${X0}" y="${top - 34}" width="${X1 - X0}" height="24" fill="#f2ede2" ${OUT2}/>`;
    rf += `<path d="M${X0},${top - 78}H${X1}" stroke="#c8ccce" stroke-width="7"/><path d="M${X0},${top - 80}H${X1}" stroke="#fff" stroke-width="2" opacity=".8"/>`;
    for (let k = 0; k <= 12; k++) rf += `<path d="M${X0 + k * (X1 - X0) / 12},${top - 34}V${top - 78}" stroke="#a8aeb0" stroke-width="4"/>`;
    rf += `<path d="M${X0},${top - 56}H${X1}" stroke="#b8bec0" stroke-width="3"/>`;
    rf += `<g transform="translate(${X0 + 90},${top - 34})"><rect x="-34" y="-82" width="68" height="70" rx="8" fill="#5a8ad0" ${OUT2}/><path d="M-34,-60h68M-34,-40h68" stroke="#3a6ab0" stroke-width="3"/><path d="M-26,-12V0M26,-12V0" stroke="#8a9296" stroke-width="6"/></g>`;
    rf += `<g id="${id}-hsign"><rect x="${X0 + 170}" y="${top - 112}" width="290" height="58" rx="6" fill="#1e3a5a" ${OUT2}/><text x="${X0 + 315}" y="${top - 74}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#f4e6b8">โรงแรมแหลมหอย</text><path d="M${X0 + 200},${top - 54}V${top - 34}M${X0 + 430},${top - 54}V${top - 34}" stroke="#5a6266" stroke-width="5"/></g>`;
    g += `<g id="${id}-roof">${rf}</g>`;
    return `<g id="${id}-hotel" transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  }
  // the Thai flag on a pole: the cloth is redrawn by Tide.land (#id-flag, #id-flagw, #id-flagb) from the pole top (px, py), scale s
  const flagPole = (id, px, py, h, s) => `<path d="M${f1(px)},${f1(py + h * s)}V${f1(py)}" stroke="#d8dcdc" stroke-width="${f1(6 * s)}"/><circle cx="${f1(px)}" cy="${f1(py - 4 * s)}" r="${f1(6 * s)}" fill="#e8c040"/><path id="${id}-flag" d="" fill="#e0282a"/><path id="${id}-flagw" d="" fill="#ffffff"/><path id="${id}-flagb" d="" fill="#2a3a8a"/>`;

  // ---------------- the warning tower: a steel pole, a ladder, a solar panel, two tiers of horn speakers, a red beacon ----------------
  Tide.tower = (x, G, s, id) => {
    const H = 700;
    let g = CS(0, 4, 90, 14, 0.7);
    g += `<rect x="-44" y="-70" width="88" height="70" fill="#a8b0b4" ${OUT2}/><rect x="-44" y="-70" width="88" height="10" fill="#c8d0d2"/><rect x="-30" y="-52" width="60" height="22" fill="#1e5aa8"/><text x="0" y="-36" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="13" fill="#fff">หอเตือนภัย</text>`;
    g += `<path d="M-70,0V-50M70,0V-50M-70,-50H70" stroke="#9aa0a2" stroke-width="3"/><path d="M-70,-48L70,0M-70,0L70,-48" stroke="#9aa0a2" stroke-width="1" opacity=".5"/>`;
    g += `<path d="M-14,-70L-8,${-H}H8L14,-70Z" fill="url(#tdPole)" ${OUT2}/>`;
    g += `<path d="M18,-80V${-H + 40}M34,-80V${-H + 40}" stroke="#9aa0a2" stroke-width="3"/><path d="${Array.from({ length: 22 }, (_, k) => `M18,${-90 - k * 26}H34`).join("")}" stroke="#9aa0a2" stroke-width="3"/>`;
    g += `<g transform="translate(-14,${-H * 0.52}) rotate(-20)"><rect x="-96" y="-34" width="96" height="64" fill="url(#tdPanel)" ${OUT2}/><path d="M-72,-34v64M-48,-34v64M-24,-34v64M-96,-2h96" stroke="#7a9ad0" stroke-width="1.5"/></g><path d="M-14,${-H * 0.52}h-30" stroke="#8a9296" stroke-width="5"/>`;
    // speakers: a ring platform, then horns facing left, front and right in two tiers
    g += `<rect x="-60" y="${-H + 10}" width="120" height="10" fill="#8a9296" ${OUT2}/>`;
    const horn = (hx, hy, dir, sc) => dir === 0 ? `<g transform="translate(${hx},${hy}) scale(${sc})"><ellipse rx="22" ry="22" fill="#2e3236" ${OUT2}/><ellipse rx="15" ry="15" fill="#5a6064"/><circle r="6" fill="#1e2226"/></g>`
      : `<g transform="translate(${hx},${hy}) scale(${dir * sc},${sc})"><path d="M0,-9L44,-26V26L0,9Z" fill="url(#tdHorn)" ${OUT2}/><ellipse cx="44" cy="0" rx="7" ry="26" fill="#2e3236" ${OUT2}/><rect x="-14" y="-10" width="16" height="20" fill="#8a9296" ${OUT2}/></g>`;
    g += horn(-20, -H - 6, -1, 1) + horn(20, -H - 6, 1, 1) + horn(0, -H - 8, 0, 0.9) + horn(-18, -H - 52, -1, 0.9) + horn(18, -H - 52, 1, 0.9) + horn(0, -H - 54, 0, 0.8);
    g += `<rect x="-8" y="${-H - 80}" width="16" height="78" fill="#9aa2a6" ${OUT2}/><path d="M0,${-H - 80}V${-H - 150}" stroke="#7a8286" stroke-width="4"/><circle cx="0" cy="${-H - 88}" r="9" fill="#c82a1e" ${OUT2}/>`;
    g += `<circle id="${id}-beacon" cx="0" cy="${-H - 88}" r="60" fill="url(#tdBeacon)" opacity="0"/>`;
    return `<g id="${id}-tower" transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  };

  // ---------------- the blue tsunami evacuation sign on its post; (x, y) = the foot of the post; o.dir 1 (arrow right) | -1 | 0 (up) ----------------
  Tide.evacSign = (x, y, s, o = {}) => {
    const dir = o.dir ?? 1, W = 300, H = 190, top = -270 - H;
    let g = CS(10, 4, 60, 10, 0.7) + `<rect x="-7" y="-280" width="14" height="280" fill="url(#tdPole)" ${OUT2}/>`;
    g += `<rect x="${-W / 2 + 6}" y="${top + 8}" width="${W}" height="${H}" rx="12" fill="#000" opacity=".25"/>`;
    g += `<rect x="${-W / 2}" y="${top}" width="${W}" height="${H}" rx="12" fill="url(#tdSign)" stroke="#f4f6f8" stroke-width="7"/><rect x="${-W / 2 + 10}" y="${top + 10}" width="${W - 20}" height="${H - 20}" rx="8" fill="none" stroke="#f4f6f8" stroke-width="2.5" opacity=".7"/>`;
    // the wave
    g += `<g transform="translate(${-W / 2 + 70},${top + 80})" fill="none" stroke="#fff" stroke-linecap="round"><path d="M-46,26Q-40,-30 6,-34Q36,-34 40,-10Q30,-22 14,-16Q2,-8 14,4" stroke-width="9"/><path d="M-50,40Q-10,24 46,36" stroke-width="7"/><path d="M-50,54Q0,40 50,52" stroke-width="5"/></g>`;
    // a figure running up a slope, the arrow
    g += `<g transform="translate(${W / 2 - 92},${top + 84})"><path d="M-46,52L46,-6" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="6" cy="-40" r="9" fill="#fff"/>
      <path d="M2,-28L-6,4M-2,-20L18,-12M-2,-20L-20,-6M-6,4L10,18L8,34M-6,4L-24,16L-34,10" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"/></g>`;
    const ax = dir === 0 ? 0 : dir * 30;
    g += dir === 0 ? `<path d="M${W / 2 - 34},${top + 64}l-16,22h10v30h12v-30h10z" fill="#fff"/>` : `<path d="M${-16 + ax},${top + 118}h${f1(dir * 36)}v-12l${f1(dir * 24)},20l${f1(-dir * 24)},20v-12h${f1(-dir * 36)}z" fill="#fff" transform="translate(${dir > 0 ? 40 : -40},0)"/>`;
    g += `<text x="0" y="${top + 158}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="25" fill="#fff">เส้นทางหนีคลื่นยักษ์</text><text x="0" y="${top + 178}" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="13" fill="#e8f0fa" letter-spacing="1">TSUNAMI EVACUATION ROUTE</text>`;
    g += `<path d="M${-W / 2 + 14},${top + 12}L${-W / 2 + 70},${top + 12}L${-W / 2 + 14},${top + 80}Z" fill="#fff" opacity=".12"/>`;
    return `<g${o.id ? ` id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})">${g}</g>`;
  };

  // ---------------- small far figures: 100 units = 1.65 m, feet at (0, 0); pal [shirt, shorts, skin, hat|null]; frames -a -b -c ----------------
  Tide.fig = (id, pal, extra = "") => {
    const [sh, pa, sk, hat] = pal;
    const head = (cx, cy) => `<circle cx="${cx}" cy="${cy}" r="9" fill="${sk}" ${OUT2}/><path d="M${cx - 9},${cy - 2}Q${cx},${cy - 14} ${cx + 9},${cy - 2}" fill="#2a2420"/>${hat ? `<ellipse cx="${cx}" cy="${cy - 7}" rx="15" ry="4" fill="${hat}" ${OUT2}/><path d="M${cx - 7},${cy - 8}Q${cx},${cy - 20} ${cx + 7},${cy - 8}Z" fill="${hat}" ${OUT2}/>` : ""}`;
    const body = (lean) => `<path d="M${-9 + lean},-74H${9 + lean}L${8 + lean * 0.5},-44H${-8 + lean * 0.5}Z" fill="${sh}" ${OUT2}/><rect x="${-8 + lean * 0.3}" y="-48" width="16" height="12" fill="${pa}" ${OUT2}/>`;
    const a = `<g id="${id}-a"><path d="M-4,-38L-12,0M4,-38L9,0" stroke="${sk}" stroke-width="6" stroke-linecap="round"/><path d="M-8,-70L-14,-48M8,-70L15,-50" stroke="${sk}" stroke-width="5" stroke-linecap="round"/>${body(0)}${head(0, -84)}</g>`;
    const b = `<g id="${id}-b" opacity="0"><path d="M-4,-38L5,0M4,-38L-7,0" stroke="${sk}" stroke-width="6" stroke-linecap="round"/><path d="M-8,-70L-3,-48M8,-70L4,-48" stroke="${sk}" stroke-width="5" stroke-linecap="round"/>${body(0)}${head(0, -84)}</g>`;
    const c = `<g id="${id}-c" opacity="0"><path d="M-6,-36L-10,0M6,-36L8,0" stroke="${sk}" stroke-width="6" stroke-linecap="round"/><path d="M-9,-46H9L22,-70H4Z" fill="${sh}" ${OUT2}/><path d="M16,-62L26,-30M10,-60L14,-28" stroke="${sk}" stroke-width="5" stroke-linecap="round"/>${head(24, -72)}</g>`;
    return `${a}${b}${c}${extra}`;
  };

  // ---------------- a fish lying on the sand (100 units long), a crab, rocks, pools ----------------
  const fishSVG = (c) => `<path d="M-50,0C-30,-22 18,-24 36,-7L56,-20L52,0L56,20L36,7C18,24 -30,22 -50,0Z" fill="${c || "url(#tdFish)"}" ${OUT3}/><circle cx="-34" cy="-4" r="4.5" fill="#fff" ${OUT2}/><circle cx="-34" cy="-4" r="2" fill="${INK}"/><path d="M-24,-10Q-20,0 -24,10" stroke="${INK}" stroke-width="2" fill="none" opacity=".6"/><path d="M-30,-12Q0,-20 30,-8" stroke="#fff" stroke-width="4" opacity=".6" fill="none" stroke-linecap="round"/><path d="M-4,-17l10,-12l8,10" fill="#5e7888" ${OUT2}/>`;
  const crabSVG = `<ellipse cx="0" cy="0" rx="22" ry="14" fill="#d8682e" ${OUT2}/><path d="M-18,6l-14,12M-12,10l-8,14M18,6l14,12M12,10l8,14" stroke="#b84a1e" stroke-width="4" stroke-linecap="round"/><path d="M-16,-6l-14,-14M16,-6l14,-14" stroke="#b84a1e" stroke-width="5"/><ellipse cx="-32" cy="-22" rx="9" ry="7" fill="#e87a3e" ${OUT2}/><ellipse cx="32" cy="-22" rx="9" ry="7" fill="#e87a3e" ${OUT2}/><path d="M-6,-12v-8M6,-12v-8" stroke="${INK}" stroke-width="3"/><circle cx="-6" cy="-21" r="3" fill="${INK}"/><circle cx="6" cy="-21" r="3" fill="${INK}"/><ellipse cx="-6" cy="-4" rx="10" ry="4" fill="#fff" opacity=".3"/>`;

  // ======================== the seabed and the beach, looking out to sea ========================
  const SEA = { FX: 2400, FY: 7200, SHORE: 14, DMAX: 350 };
  const dRand = (r, a, b) => a * Math.pow(b / a, r());
  // a tide pool that mirrors the sky; a rock with a lit cap, barnacles and a fringe of weed; a starfish; a stub of coral
  const pool = (r, P, px, py, rx, ry) => {
    const pts = Array.from({ length: 10 }, (_, k) => { const a = (k / 10) * Math.PI * 2, j = 0.75 + r() * 0.35; return [px + Math.cos(a) * rx * j, py + Math.sin(a) * ry * j]; });
    const d = smoothClosed(pts);
    return `<path d="${d}" fill="${T(P.bed[2], -0.35)}" opacity=".45" transform="translate(0,${f1(ry * 0.3)})"/><path d="${d}" fill="${mix(P.sky[1], P.bed[2], 0.3)}"/><path d="${d}" fill="${P.sky[2]}" opacity=".35" transform="translate(0,${f1(-ry * 0.3)}) scale(1,.6)" transform-origin="${f1(px)} ${f1(py)}"/><path d="${d}" fill="none" stroke="${T(P.bed[1], -0.3)}" stroke-width="${f1(Math.max(0.8, ry * 0.12))}" opacity=".6"/>
      <path d="M${f1(px - rx * 0.45)},${f1(py - ry * 0.15)}h${f1(rx * 0.42)}M${f1(px + rx * 0.05)},${f1(py + ry * 0.2)}h${f1(rx * 0.2)}" stroke="#fff" stroke-width="${f1(Math.max(1, ry * 0.14))}" opacity=".6" stroke-linecap="round"/><path d="M${f1(px - rx * 0.6)},${f1(py + ry * 0.35)}q${f1(rx * 0.3)},${f1(-ry * 0.15)} ${f1(rx * 0.6)},0t${f1(rx * 0.6)},0" stroke="${P.sky[0]}" stroke-width="${f1(Math.max(0.8, ry * 0.1))}" fill="none" opacity=".35"/>`;
  };
  const rockS = (r, P, px, py, w, h) => {
    const pts = [[px - w / 2, py + h * 0.06]];
    for (let k = 1; k < 8; k++) { const a = Math.PI + (k / 8) * Math.PI, j = 0.78 + r() * 0.32; pts.push([px + Math.cos(a) * w / 2 * j, py + Math.sin(a) * h * j]); }
    pts.push([px + w / 2, py + h * 0.06]);
    const d = smoothClosed(pts), sw = Math.max(0.8, w * 0.02);
    let g = CS(px - w * 0.15, py, w * 0.7, Math.max(2, h * 0.25), 0.9) + `<path d="${d}" fill="${mix("#5a5248", P.haze, 0.1)}" stroke="${INK}" stroke-width="${f1(sw)}"/>`;
    g += `<path d="${smoothClosed(pts.map(([x, y]) => [px + (x - px) * 0.62 + w * 0.1, py - h * 0.18 + (y - py) * 0.6]))}" fill="#8a8072" opacity=".8"/>`;
    for (let k = 0; k < 6; k++) g += `<circle cx="${f1(px + (r() - 0.5) * w * 0.7)}" cy="${f1(py - r() * h * 0.6)}" r="${f1(Math.max(0.6, w * 0.025))}" fill="#e2dccc" opacity=".85"/>`;
    g += `<path d="${Array.from({ length: 8 }, () => { const sx = px + (r() - 0.5) * w * 0.9; return `M${f1(sx)},${f1(py)}q${f1(w * 0.03)},${f1(-h * 0.2)} ${f1(w * 0.07)},${f1(-h * 0.08)}`; }).join("")}" stroke="#6f7a3a" stroke-width="${f1(Math.max(0.8, w * 0.03))}" fill="none"/>`;
    return g;
  };
  const star = (px, py, R, rot) => { let d = ""; for (let k = 0; k < 10; k++) { const a = rot + (k / 10) * Math.PI * 2, rr = k % 2 ? R * 0.42 : R; d += `${k ? "L" : "M"}${f1(px + Math.cos(a) * rr)},${f1(py + Math.sin(a) * rr * 0.5)}`; } return `<path d="${d}Z" fill="#e8743a" stroke="#8a3a1a" stroke-width="${f1(Math.max(0.6, R * 0.08))}"/><circle cx="${f1(px)}" cy="${f1(py)}" r="${f1(R * 0.18)}" fill="#ffb07a"/>`; };
  const coral = (r, px, py, s) => { const c = ["#c98a7a", "#b79a74", "#a8807a", "#d2a080"][Math.floor(r() * 4)]; let d = ""; for (let k = 0; k < 6; k++) { const a = -Math.PI / 2 + (r() - 0.5) * 1.8, L = s * (0.6 + r() * 0.6); d += `M${f1(px)},${f1(py)}q${f1(Math.cos(a) * L * 0.5)},${f1(Math.sin(a) * L * 0.6)} ${f1(Math.cos(a) * L)},${f1(Math.sin(a) * L)}`; } return `<path d="${d}" stroke="${c}" stroke-width="${f1(Math.max(1, s * 0.22))}" stroke-linecap="round" fill="none"/><path d="${d}" stroke="#fff" stroke-width="${f1(Math.max(0.5, s * 0.07))}" stroke-linecap="round" fill="none" opacity=".35"/>`; };

  // the corner of ยาย's shop seen from inside, framing the top left: the tin roof's underside with its rafters, the blue scalloped awning, the post, a shell chime
  function eave(P) {
    const A = [-300, 520], B = [900, -200], n = 22;
    let g = `<path d="M-300,-200H900L-300,520Z" fill="#2e2c2a"/>`;
    for (let k = 1; k < 8; k++) g += `<path d="M${f1(lerp(-300, 900, k / 8))},-200L${f1(lerp(-300, 900, k / 8) - 160)},${f1(lerp(-200, 520, 1 - k / 8) + 40)}" stroke="#5a4a3a" stroke-width="14"/>`;
    let hem = "";
    for (let k = n; k >= 1; k--) { const u = (k - 1) / n, x = lerp(A[0], B[0], u), y = lerp(A[1], B[1], u), um = (k - 0.5) / n, xm = lerp(A[0], B[0], um), ym = lerp(A[1], B[1], um); hem += `Q${f1(xm)},${f1(ym + 70)} ${f1(x)},${f1(y + 40)}`; }
    g += `<path d="M-300,520L900,-200V-160${hem}Z" fill="url(#tdTarp)" stroke="#14325a" stroke-width="3"/>`;
    g += `<path d="M-300,532L900,-188" stroke="#7ab8f0" stroke-width="5" opacity=".5"/>`;
    g += `<rect x="-10" y="380" width="56" height="1700" fill="url(#tdWoodH)" stroke="#2a1a10" stroke-width="4"/><path d="M8,400V2060" stroke="#d8a874" stroke-width="5" opacity=".5"/>`;
    g += `<rect x="-200" y="1690" width="1500" height="46" fill="url(#tdWoodH)" stroke="#2a1a10" stroke-width="4"/><path d="M-200,1698H1300" stroke="#e2b880" stroke-width="5" opacity=".6"/>${[120, 520, 920].map((x) => `<rect x="${x}" y="1736" width="40" height="300" fill="#8a5a32" stroke="#2a1a10" stroke-width="4"/>`).join("")}
      <g transform="translate(760,1690)"><path d="M-22,0L-18,-58H18L22,0Z" fill="#f4f6f8" opacity=".8" stroke="#6a7a84" stroke-width="2"/><rect x="-17" y="-44" width="34" height="40" fill="#e88a3a" opacity=".85"/><path d="M6,-58L16,-96" stroke="#e84a6a" stroke-width="4"/></g>`;
    g += `<path d="M300,420V520M318,410V548M336,400V506" stroke="#8a7a6a" stroke-width="2"/>${[[300, 526], [318, 554], [336, 512]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="10" fill="#f6e8d8" stroke="#6a5a4a" stroke-width="2.5"/>`).join("")}`;
    return g;
  }

  function seaView(L, o) {
    const id = o.id || "tb", P = PAL[o.time || "morning"], r = mk(o.seed || 7), HZ = o.hz ?? 640;
    const HC = o.hc ?? 3, FY = SEA.FX * HC, SH = o.shore ?? 14, yAt = (d) => HZ + FY / d, Y0 = yAt(SH), Yw = yAt(SH * 0.79);
    sky(L, id, P, HZ, { seed: (o.seed || 7) + 1 });
    // mid: seabirds over the water
    let bd = `<g id="${id}-birds">`;
    for (let k = 0; k < 11; k++) { const bx = 80 + r() * 900, by = HZ - 160 - r() * 300, bs = 0.5 + r() * 0.7; bd += `<path d="M${f1(bx - 15 * bs)},${f1(by)}q${f1(7 * bs)},${f1(-9 * bs)} ${f1(15 * bs)},0q${f1(7 * bs)},${f1(-9 * bs)} ${f1(15 * bs)},0" stroke="#3a4048" stroke-width="${f1(2.6 * bs)}" fill="none" stroke-linecap="round"/>`; }
    put(L.mid, bd + `</g>`);
    let s = "";
    // ---- the seabed (hidden under the water until it draws back) ----
    s += `<defs><linearGradient id="${id}-bedG" gradientUnits="userSpaceOnUse" x1="0" y1="${HZ}" x2="0" y2="${f1(Y0)}"><stop offset="0" stop-color="${mix(P.bed[2], P.haze, 0.5)}"/><stop offset=".22" stop-color="${P.bed[2]}"/><stop offset=".7" stop-color="${P.bed[1]}"/><stop offset="1" stop-color="${P.bed[0]}"/></linearGradient></defs>`;
    s += `<rect x="-3000" y="${HZ}" width="8000" height="${f1(Y0 - HZ + 80)}" fill="url(#${id}-bedG)"/>`;
    for (let d = SH * 1.04; d < SEA.DMAX; d *= 1.045) {
      const y = yAt(d), a = clamp(260 / d, 0.4, 10), w = clamp(80 / d, 0.6, 5.5), ph = r() * 6;
      let p = "";
      for (let x = -1300; x <= 2400; x += 50) p += `${p ? "L" : "M"}${x},${f1(y + Math.sin(x * 0.006 + ph) * a + Math.sin(x * 0.021 + ph * 2) * a * 0.4)}`;
      s += `<path d="${p}" stroke="${T(P.bed[2], -0.3)}" stroke-width="${f1(w)}" fill="none" opacity=".42"/><path d="${p}" stroke="${T(P.bed[0], 0.3)}" stroke-width="${f1(w * 0.7)}" fill="none" opacity=".45" transform="translate(0,${f1(w * 1.2)})"/>`;
    }
    for (let k = 0; k < 34; k++) { const d = dRand(r, SH + 2, 260), R = 0.6 + r() * 1.4, rx = SEA.FX * R / d, ry = clamp(FY * R / (d * d), 1, rx * 0.3); s += pool(r, P, -1000 + r() * 3100, yAt(d), rx, ry); }
    for (let k = 0; k < 40; k++) { const d = dRand(r, SH + 1.5, 160), w = SEA.FX * (0.5 + r() * 1.6) / d; s += rockS(r, P, -1100 + r() * 3300, yAt(d), w, w * (0.28 + r() * 0.2)); }
    for (let k = 0; k < 46; k++) { const d = dRand(r, SH + 1, 120), sz = SEA.FX * (0.18 + r() * 0.25) / d; s += coral(r, -1100 + r() * 3300, yAt(d), sz); }
    for (let k = 0; k < 14; k++) { const d = dRand(r, SH + 1, 60); s += star(-600 + r() * 2300, yAt(d), SEA.FX * 0.12 / d, r() * 6); }
    for (let k = 0; k < 30; k++) { const d = dRand(r, SH + 1, 90), sz = SEA.FX * 0.2 / d, x = -900 + r() * 2900, y = yAt(d); s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(sz)}" ry="${f1(sz * 0.32)}" fill="${r() < 0.5 ? "#3a3028" : "#f2ece0"}" opacity=".85"/>`; }
    for (let k = 0; k < 36; k++) { const d = dRand(r, SH + 1, 140), sz = SEA.FX * (0.3 + r() * 0.5) / d, x = -1000 + r() * 3100, y = yAt(d); s += `<path d="M${f1(x)},${f1(y)}c${f1(sz * 0.3)},${f1(-sz * 0.2)} ${f1(sz * 0.7)},${f1(sz * 0.1)} ${f1(sz)},${f1(-sz * 0.05)}M${f1(x + sz * 0.2)},${f1(y + 1)}c${f1(sz * 0.3)},${f1(-sz * 0.15)} ${f1(sz * 0.6)},${f1(sz * 0.12)} ${f1(sz * 0.9)},0" stroke="#5e6a32" stroke-width="${f1(Math.max(0.8, sz * 0.09))}" fill="none" opacity=".8"/>`; }
    // ---- the beach: a wet band that mirrors the sky, then dry sand toward the camera ----
    s += `<defs><linearGradient id="${id}-beachG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(Y0 - 30)}" x2="0" y2="2100"><stop offset="0" stop-color="${P.wet[0]}"/><stop offset=".13" stop-color="${P.wet[1]}"/><stop offset=".2" stop-color="${P.sand[2]}"/><stop offset=".55" stop-color="${P.sand[1]}"/><stop offset="1" stop-color="${P.sand[0]}"/></linearGradient></defs>`;
    s += `<rect x="-3000" y="${f1(Y0 - 34)}" width="8000" height="2200" fill="url(#${id}-beachG)"/>`;
    s += `<rect x="-3000" y="${f1(Y0 - 34)}" width="8000" height="${f1(Yw - Y0 + 34)}" fill="${P.sky[2]}" opacity=".24"/>`;
    for (let k = 0; k < 30; k++) { const y = Y0 + r() * (Yw - Y0), x = -900 + r() * 2900, w = 60 + r() * 240; s += `<path d="M${f1(x)},${f1(y)}h${f1(w)}" stroke="#fff" stroke-width="${f1(1.5 + r() * 2.5)}" opacity="${f1(0.18 + r() * 0.3)}" stroke-linecap="round"/>`; }
    // the high-tide line: dried weed, twigs, shells
    const Yt = yAt(SH * 0.6);
    for (let k = 0; k < 90; k++) { const x = -1200 + r() * 3500, y = Yt + (r() - 0.5) * 26 + Math.sin(x * 0.004) * 14, w = 8 + r() * 26; s += `<path d="M${f1(x)},${f1(y)}l${f1(w)},${f1((r() - 0.5) * 6)}" stroke="${["#6a5a3a", "#3a3428", "#8a7a52", "#f2ece0"][k % 4]}" stroke-width="${f1(2 + r() * 3)}" stroke-linecap="round" opacity=".8"/>`; }
    // wind ripples on the dry sand, footprints walking to the sea, crab holes with their sand balls, shells
    for (let k = 0; k < 26; k++) { const y = Yw + 20 + Math.pow(r(), 1.3) * (1920 - Yw), x = -900 + r() * 2900, w = 80 + r() * 260; s += `<path d="M${f1(x)},${f1(y)}q${f1(w / 2)},${f1(-6 - r() * 6)} ${f1(w)},0" stroke="#fff" stroke-width="3" fill="none" opacity=".35"/><path d="M${f1(x)},${f1(y + 4)}q${f1(w / 2)},${f1(-6)} ${f1(w)},0" stroke="${T(P.sand[2], -0.15)}" stroke-width="2" fill="none" opacity=".35"/>`; }
    for (let k = 0; k < 16; k++) { const u = k / 15, d = lerp(SH * 0.42, SH * 1.12, u), y = yAt(d), sz = SEA.FX * 0.13 / d, x = 520 + Math.sin(u * 5) * 60 + (k % 2 ? sz * 1.6 : -sz * 1.6); s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(sz * 0.55)}" ry="${f1(sz * 0.28)}" fill="${T(P.sand[2], -0.22)}" opacity=".55"/><ellipse cx="${f1(x - sz * 0.08)}" cy="${f1(y - sz * 0.05)}" rx="${f1(sz * 0.45)}" ry="${f1(sz * 0.2)}" fill="${T(P.sand[2], -0.1)}" opacity=".5"/>`; }
    for (let k = 0; k < 14; k++) { const d = SH * (0.45 + r() * 0.4), y = yAt(d), x = -300 + r() * 1700, sz = SEA.FX * 0.05 / d; s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(sz)}" ry="${f1(sz * 0.5)}" fill="#5a4a32"/>` + Array.from({ length: 7 }, () => { const a = r() * Math.PI * 2, rr = sz * (1.8 + r() * 2.4); return `<circle cx="${f1(x + Math.cos(a) * rr)}" cy="${f1(y + Math.sin(a) * rr * 0.5)}" r="${f1(sz * 0.32)}" fill="${T(P.sand[2], -0.08)}" stroke="${T(P.sand[2], -0.3)}" stroke-width=".8"/>`; }).join(""); }
    for (let k = 0; k < 26; k++) { const d = SH * (0.42 + r() * 0.48), y = yAt(d), x = -500 + r() * 2100, sz = SEA.FX * 0.035 / d; s += `<path d="M${f1(x - sz)},${f1(y)}a${f1(sz)},${f1(sz * 0.7)} 0 0 1 ${f1(sz * 2)},0z" fill="${["#f8f2ea", "#f4d8cc", "#e8dcc0"][k % 3]}" stroke="#9a8a72" stroke-width=".8"/>`; }
    put(L.set, s);
    // ---- the water (redrawn), the karsts and their reflections ----
    const isl = o.islands || [[-560, 300, 250, 0.78, 0.1], [60, 170, 170, 0.86, 0.3], [560, 340, 330, 0.5, 0], [1100, 190, 200, 0.82, 0.2], [1580, 320, 290, 0.66, 0.1], [2140, 220, 160, 0.88, 0.2]];
    const KS = isl.map(([x, w, h, v, sh], k) => ({ ...karst(id, k, x, HZ + 4, w, h, r, P, v, sh), x, w, h, v }));
    let refl = "";
    KS.forEach((k) => { refl += `<g transform="translate(0,${f1(2 * HZ + 8)}) scale(1,-1)" opacity="${f1(0.28 * (1 - k.v * 0.6))}"><path d="${k.d}" fill="${mix(T(P.rock, -0.4), P.sea[2], 0.35)}"/></g>`; });
    let spark = "";
    const SPK = o.time === "storm" ? 0.2 : o.time === "eerie" ? 0.45 : 1;
    for (let k = 0; k < 150; k++) { const d = dRand(r, 15, 330), y = yAt(d), x = -1200 + r() * 3500, len = SEA.FX * (0.4 + r() * 1.8) / d; spark += `<path d="M${f1(x)},${f1(y)}h${f1(len)}" stroke="#fff" stroke-width="${f1(clamp(40 / d, 0.6, 3.4))}" opacity="${f1((0.25 + r() * 0.5) * SPK)}" stroke-linecap="round"/>`; }
    for (let k = 0; k < 70; k++) { const d = dRand(r, 15, 200), y = yAt(d), x = -1200 + r() * 3500, len = SEA.FX * (0.8 + r() * 2.2) / d, hh = len * 0.12; spark += `<path d="M${f1(x)},${f1(y)}q${f1(len / 2)},${f1(-hh)} ${f1(len)},0" stroke="${T(P.sea[2], -0.2)}" stroke-width="${f1(clamp(50 / d, 0.6, 4))}" fill="none" opacity=".45"/><path d="M${f1(x + len * 0.2)},${f1(y - hh * 0.6)}q${f1(len * 0.3)},${f1(-hh * 0.4)} ${f1(len * 0.6)},0" stroke="#fff" stroke-width="${f1(clamp(30 / d, 0.5, 2.6))}" fill="none" opacity="${f1(0.55 * SPK)}"/>`; }
    let w = `<g id="${id}-sea"><defs><linearGradient id="${id}-seaG" gradientUnits="userSpaceOnUse" x1="0" y1="${HZ}" x2="0" y2="${f1(Y0)}"><stop offset="0" stop-color="${P.sea[0]}"/><stop offset=".05" stop-color="${P.sea[1]}"/><stop offset=".28" stop-color="${P.sea[2]}"/><stop offset=".62" stop-color="${P.sea[3]}"/><stop offset=".88" stop-color="${P.sea[4]}"/><stop offset="1" stop-color="${P.sea[5]}"/></linearGradient>
      <clipPath id="${id}-wclip"><path id="${id}-wclipP" d=""/></clipPath></defs>
      <path id="${id}-water" d="" fill="url(#${id}-seaG)"/><g clip-path="url(#${id}-wclip)">${refl}${spark}</g>
      <path id="${id}-shal" d="" fill="${P.sea[5]}" opacity=".5"/><path id="${id}-film" d="" fill="#ffffff" opacity="0"/>
      <path id="${id}-foam2" d="" stroke="#ffffff" fill="none" opacity=".45" stroke-linecap="round"/><path id="${id}-foam" d="" stroke="#ffffff" fill="none" opacity=".92" stroke-linecap="round"/></g>`;
    w += `<g id="${id}-karsts">${KS.map((k) => k.g).join("")}<rect x="-3000" y="${HZ - 26}" width="8000" height="34" fill="${P.haze}" opacity=".45"/></g>`;
    put(L.set, w);
    // ---- longtails at anchor ----
    const BT = [{ x: 140, d: 50, flip: false, hull: "#2f6fa0", band: "#d8423a", no: "พง 3127" }, { x: 900, d: 84, flip: true, hull: "#2e8a5a", band: "#f2c02a", no: "พง 0418" }].slice(0, o.boats ?? 2);
    let bt = "";
    BT.forEach((b, k) => { b.s = SEA.FX * 11 / b.d / 1000; b.ph = r() * 6; b.water = b.d < 60 ? P.sea[3] : P.sea[2]; bt += `<g id="${id}-boat${k}">${Tide.longtail({ hull: b.hull, band: b.band, no: b.no, flip: b.flip, water: b.water, wid: `${id}-boat${k}-w`, seed: k + 3, k })}</g>`; });
    // ---- the fish, the crabs and the walkers (redrawn) ----
    const FI = Array.from({ length: o.fish ?? 14 }, () => ({ x: -150 + r() * 1400, d: dRand(r, SH + 1.5, 95), ph: r() * 9, flip: r() < 0.5, c: r() < 0.25 ? "#c8a0a8" : null }));
    FI.forEach((f) => { f.s = SEA.FX * 0.55 / f.d / 100; });
    const CR = Array.from({ length: 6 }, () => ({ x: -100 + r() * 1300, d: dRand(r, SH + 1, 55), ph: r() * 9 }));
    CR.forEach((c) => { c.s = SEA.FX * 0.16 / c.d / 50; });
    const SHC = ["#e84a3a", "#2a8ad0", "#f2c030", "#ffffff", "#3aa86a", "#e87ab0", "#8a5ad0", "#f28a30"], PA = ["#2a3a5a", "#5a4a3a", "#1e2a3a", "#c8b890"], SK = ["#e3ad84", "#c88d63", "#b9805a", "#d89c74"], HT = [null, "#e8d8a0", null, "#d84a3a", null, "#f4f0e6"];
    const PE = Array.from({ length: o.people || 0 }, (_, k) => ({ x: -60 + ((k + 0.5) / Math.max(1, o.people)) * 1200 + (r() - 0.5) * 120, d0: SH + 3 + Math.pow(r(), 1.5) * 62, v: 0.9 + r() * 0.9, bend: r() < 0.4, delay: r() * 1.2, pal: [SHC[k % 8], PA[k % 4], SK[k % 4], HT[k % 6]] }));
    let dyn = bt;
    FI.forEach((f, k) => { dyn += `<g id="${id}-fish${k}" opacity="0">${fishSVG(f.c)}</g>`; });
    CR.forEach((c, k) => { dyn += `<g id="${id}-crab${k}" opacity="0">${crabSVG}</g>`; });
    PE.sort((a, b) => b.d0 - a.d0).forEach((p, k) => { p.k = k; dyn += `<g id="${id}-p${k}">${Tide.fig(`${id}-p${k}`, p.pal)}</g>`; });
    put(L.set, dyn);
    // ---- palms framing the top, a net drying on poles, buckets, a log ----
    let near = "";
    if (o.palms !== false && o.frame !== "eave") {
      near += coco(-230, 2040, 2.3, 0.07, (o.seed || 7) + 11, { id: `${id}-palm0`, pal: P.leaf, fl: 0.62 });
      near += coco(1330, 1960, 2.15, -0.1, (o.seed || 7) + 12, { id: `${id}-palm1`, pal: P.leaf, fl: 0.6 });
    }
    if (o.frame === "eave") near += coco(1290, 1980, 2.2, -0.08, (o.seed || 7) + 12, { id: `${id}-palm1`, pal: P.leaf, fl: 0.6 });
    near += `<g transform="translate(560,1760) rotate(-4)"><path d="M-240,0Q-60,-38 220,-14L230,8Q-60,-6 -236,26Z" fill="#9a8466" ${OUT3}/><path d="M-200,-2Q-60,-30 200,-10" stroke="#c8b08a" stroke-width="5" fill="none"/><ellipse cx="-236" cy="12" rx="14" ry="20" fill="#7a6448" ${OUT2}/></g>`;
    near += `<g transform="translate(250,1600)">${CS(0, 4, 50, 10)}<path d="M-34,-60L-28,0H28L34,-60Z" fill="#2a8ad0" ${OUT2}/><ellipse cx="0" cy="-60" rx="34" ry="9" fill="#1e5a90" ${OUT2}/><path d="M-30,-60Q0,-110 30,-60" stroke="#d8dcdc" stroke-width="4" fill="none"/></g>`;
    near += `<g transform="translate(860,1640) rotate(8)">${CS(0, 4, 44, 9)}<ellipse cx="0" cy="-22" rx="30" ry="24" fill="#8a6a3a" ${OUT2}/><path d="M-20,-30q10,-8 24,-4" stroke="#c8a870" stroke-width="4" fill="none"/></g>`;
    put(L.set, near);
    // ---- foreground: beach morning glory creeping in at the bottom corners ----
    let fg = "";
    const vine = (x0, y0, dir, seed) => { const rr = mk(seed); let v = `<path d="M${x0},${y0}q${dir * 160},-60 ${dir * 340},-30t${dir * 300},10" stroke="#4a7a3a" stroke-width="7" fill="none"/>`; for (let k = 0; k < 9; k++) { const u = k / 8, vx = x0 + dir * (40 + u * 600), vy = y0 - 40 + Math.sin(u * 4) * 20; v += `<path d="M${f1(vx)},${f1(vy)}c${f1(-26)},-28 ${f1(-26)},-58 0,-66c26,8 26,38 0,66z" fill="${rr() < 0.5 ? "#4f8a3e" : "#6aa84a"}" stroke="#2e5a2a" stroke-width="2"/>`; if (k % 3 === 1) v += `<g transform="translate(${f1(vx + dir * 20)},${f1(vy - 70)})"><path d="M0,0L-16,-34Q0,-44 16,-34Z" fill="#d86ab0" stroke="#8a2a6a" stroke-width="2"/><ellipse cx="0" cy="-36" rx="18" ry="6" fill="#f4a0d8" stroke="#8a2a6a" stroke-width="2"/></g>`; } return v; };
    fg += vine(-120, 1930, 1, 3) + vine(1220, 1950, -1, 4);
    if (o.frame === "eave") fg += eave(P);
    put(L.fg, fg);
    // ---- the state for the redraw ----
    ST[id] = { kind: "sea", P, HZ, yAt, FY, SH, lvl: o.sea || 0, BT, FI, CR, PE, walkAt: o.walkAt || 0 };
    seaDraw(id, 0, o.sea || 0, 0);
  }

  // redraw a "sea" view at timeline time t, water level u (0…1), tl the seconds since the figures may set off
  function seaDraw(id, t, u, tw) {
    const S = ST[id], { HZ, yAt, P } = S;
    const yE0 = yAt(S.SH), yE1 = yAt(SEA.DMAX), yE = lerp(yE0, yE1, u), swash = 1 - sm(0, 0.12, u);
    const dE = S.FY / (yE - HZ) + swash * 0.8 * (S.SH / 14) * Math.sin(t * 1.5);
    const edge = (x, dd) => yAt(dd + 0.32 * Math.sin(x * 0.0045 + t * 1.1) * (dd / 14) + 0.18 * Math.sin(x * 0.013 - t * 1.7) * (dd / 14));
    const line = (dd, rev) => { const pts = []; for (let x = -1300; x <= 2400; x += 40) pts.push(`${x},${f1(edge(x, dd))}`); if (rev) pts.reverse(); return pts; };
    const E = line(dE, true);
    const water = `M-1300,${HZ - 2}L2400,${HZ - 2}L${E.join("L")}Z`;
    el(`${id}-water`).setAttribute("d", water);
    el(`${id}-wclipP`).setAttribute("d", water);
    el(`${id}-shal`).setAttribute("d", `M${line(dE * 1.28, false).join("L")}L${E.join("L")}Z`);
    const fw = clamp(5200 * (S.FY / 7200) / (dE * dE), 1.1, 10);
    const foam = el(`${id}-foam`), foam2 = el(`${id}-foam2`);
    foam.setAttribute("d", `M${line(dE, false).join("L")}`); foam.setAttribute("stroke-width", f1(fw));
    foam2.setAttribute("d", `M${line(dE * 1.07, false).join("L")}`); foam2.setAttribute("stroke-width", f1(fw * 0.6));
    const film = el(`${id}-film`);
    film.setAttribute("d", `M${line(dE, false).join("L")}L${line(Math.max(S.SH, dE * 0.7), true).join("L")}Z`);
    film.setAttribute("opacity", f1(0.2 * sm(0.01, 0.12, u)));
    // boats ride the swell, then ground and pitch when the water leaves them
    S.BT.forEach((b, k) => {
      const g = sm(b.d - 2, b.d + 14, dE), bob = (1 - g) * 5 * b.s * Math.sin(t * 1.3 + b.ph), roll = (1 - g) * 1.4 * Math.sin(t * 0.9 + b.ph) + g * (k % 2 ? -9 : 11);
      el(`${id}-boat${k}`).setAttribute("transform", `translate(${f1(b.x)},${f1(yAt(b.d) + bob + g * 6 * b.s)}) rotate(${f1(roll)}) scale(${f1(b.s)})`);
      el(`${id}-boat${k}-w`).setAttribute("opacity", f1(1 - g));
    });
    // fish flop once the water has left them; crabs scuttle
    S.FI.forEach((f, k) => {
      const op = sm(f.d * 1.0, f.d * 1.08, dE), env = Math.max(0, Math.sin(t * 1.9 + f.ph * 3)), flop = Math.sin(t * 12 + f.ph) * env;
      const e = el(`${id}-fish${k}`);
      e.setAttribute("opacity", f1(op));
      e.setAttribute("transform", `translate(${f1(f.x)},${f1(yAt(f.d) - Math.abs(flop) * 30 * f.s)}) rotate(${f1(flop * 28 + (f.flip ? 170 : -8))}) scale(${f1(f.s)},${f1(f.s * (0.8 + 0.2 * Math.abs(flop)))})`);
    });
    S.CR.forEach((c, k) => {
      const op = sm(c.d, c.d * 1.08, dE), e = el(`${id}-crab${k}`);
      e.setAttribute("opacity", f1(op));
      e.setAttribute("transform", `translate(${f1(c.x + Math.sin(t * 0.8 + c.ph) * 60 * c.s)},${f1(yAt(c.d))}) scale(${f1(c.s)})`);
    });
    // walkers head out onto the seabed and stop short of the water; some stoop to pick up fish
    S.PE.forEach((p) => {
      const tau = Math.max(0, tw - p.delay), d = Math.min(p.d0 + p.v * tau, dE - 4), moving = d < dE - 4.05 && tw > p.delay, sc = 39.6 / d;
      const stoop = p.bend && Math.sin(tw * 0.9 + p.x) > 0.35;
      const frame = stoop ? "c" : moving ? (Math.floor(tw * 4.2 + p.x) % 2 ? "a" : "b") : "a";
      const g = el(`${id}-p${p.k}`);
      g.setAttribute("transform", `translate(${f1(p.x)},${f1(yAt(d))}) scale(${f1(sc)})`);
      g.setAttribute("opacity", d < S.SH + 0.5 ? "0" : "1");
      ["a", "b", "c"].forEach((n) => el(`${id}-p${p.k}-${n}`).setAttribute("opacity", n === frame ? "1" : "0"));
    });
  }

  // run a "sea" view: o.to the level it draws back to, o.at / o.len (seconds into the call), o.ease, o.walkAt, o.birds ("flee")
  Tide.sea = (tl, id, t0, dur, o = {}) => {
    const S = ST[id], u0 = S.lvl, u1 = o.to ?? u0, at = o.at ?? 0, len = o.len ?? Math.max(0.01, dur - at), E = gsap.parseEase(o.ease || "power1.inOut"), c = { t: 0 };
    const lv = (t) => (t <= at ? u0 : t >= at + len ? u1 : lerp(u0, u1, E((t - at) / len)));
    const birds = el(`${id}-birds`);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => {
      seaDraw(id, t0 + c.t, lv(c.t), c.t - (o.walkAt || 0));
      if (birds) birds.setAttribute("transform", o.birds === "flee" ? `translate(${f1(c.t * 260)},${f1(-c.t * 140)})` : `translate(${f1(c.t * 30)},0)`);
      [0, 1].forEach((k) => { const p = el(`${id}-palm${k}`); if (p) { const [px, py] = p.getAttribute("data-o").split(" "); p.setAttribute("transform", `rotate(${f1(1.6 * Math.sin((t0 + c.t) * 1.1 + k * 2))} ${px} ${py})`); } });
    } }, t0);
  };
  Tide.recede = (tl, id, t0, dur, to, o = {}) => Tide.sea(tl, id, t0, dur, { ...o, to, at: 0, len: dur });
  Tide.yAt = (id, d) => ST[id].yAt(d);

  // ======================== the village from the shallows, looking inland ========================
  // the jungle hill (a jungle-covered ridge whose path climbs well above the palms and the hotel's roof), the assembly point at the top
  function hill(id, P, r, o) {
    const top = o.top ?? 330, foot = o.foot ?? 1240;
    const ridge = o.ridge || [[-1500, foot + 120], [-1100, foot - 200], [-700, top + 420], [-300, top + 150], [120, top + 20], [420, top], [760, top + 70], [1150, top + 260], [1600, top + 520], [2100, foot - 160], [2600, foot + 60]];
    let g = `<defs><linearGradient id="${id}-hillG" gradientUnits="userSpaceOnUse" x1="0" y1="${top}" x2="0" y2="${foot + 200}"><stop offset="0" stop-color="${P.green[1]}"/><stop offset=".6" stop-color="${P.green[0]}"/><stop offset="1" stop-color="${T(P.green[0], -0.25)}"/></linearGradient></defs>`;
    g += `<path d="${smoothClosed(ridge.concat([[2600, foot + 600], [-1500, foot + 600]]))}" fill="url(#${id}-hillG)"/>`;
    // the jungle canopy: crowns in three depths, lit from the right
    const yr = (x) => { for (let i = 0; i < ridge.length - 1; i++) if (x >= ridge[i][0] && x <= ridge[i + 1][0]) { const k = (x - ridge[i][0]) / (ridge[i + 1][0] - ridge[i][0]); return lerp(ridge[i][1], ridge[i + 1][1], k); } return foot; };
    for (let k = 0; k < 230; k++) {
      const x = -1400 + r() * 3900, y0 = yr(x), y = y0 + 20 + Math.pow(r(), 0.8) * (foot + 140 - y0), R = 34 + r() * 46;
      g += crown(x, y, R, r, [T(P.green[0], -0.12), P.green[1], P.green[2], T(P.green[2], 0.2)], 7);
    }
    // emergent trees and palms along the ridge
    for (let k = 0; k < 16; k++) { const x = -1100 + k * 230 + r() * 80, y = yr(x) + 30; g += crown(x, y - 40, 60 + r() * 40, r, [P.green[0], P.green[1], P.green[2], T(P.green[2], 0.25)], 9); }
    g += `<defs><linearGradient id="${id}-sideH" gradientUnits="userSpaceOnUse" x1="-900" y1="0" x2="1900" y2="0"><stop offset="0" stop-color="#0e2a1a" stop-opacity=".35"/><stop offset=".45" stop-color="#0e2a1a" stop-opacity="0"/><stop offset=".8" stop-color="#fff4d0" stop-opacity=".12"/><stop offset="1" stop-color="#fff4d0" stop-opacity=".2"/></linearGradient></defs><rect x="-1500" y="${top - 60}" width="4100" height="${foot - top + 300}" fill="url(#${id}-sideH)"/>`;
    g += `<defs><linearGradient id="${id}-hazeH" gradientUnits="userSpaceOnUse" x1="0" y1="${top}" x2="0" y2="${foot}"><stop offset="0" stop-color="${P.haze}" stop-opacity=".42"/><stop offset=".7" stop-color="${P.haze}" stop-opacity=".1"/><stop offset="1" stop-color="${P.haze}" stop-opacity="0"/></linearGradient></defs><rect x="-1500" y="${top - 60}" width="4100" height="${foot - top + 300}" fill="url(#${id}-hazeH)"/>`;
    // the evacuation path: concrete steps zig-zagging up the slope with a handrail, lamp posts, to the assembly point
    const path = o.path || [[-40, foot - 10], [260, foot - 170], [60, foot - 330], [330, foot - 520], [190, foot - 680], [400, top + 120]];
    const pd = `M${path.map(P2).join("L")}`;
    g += `<path d="${pd}" stroke="#5a5448" stroke-width="30" fill="none" stroke-linejoin="round" opacity=".35" transform="translate(4,6)"/><path d="${pd}" stroke="#e2dccf" stroke-width="24" fill="none" stroke-linejoin="round"/>`;
    for (let i = 0; i < path.length - 1; i++) {
      const [x0, y0] = path[i], [x1, y1] = path[i + 1], n = Math.round(Math.hypot(x1 - x0, y1 - y0) / 14);
      let st = "";
      for (let j = 1; j < n; j++) { const u = j / n, px = lerp(x0, x1, u), py = lerp(y0, y1, u); st += `M${f1(px - 10)},${f1(py)}h20`; }
      g += `<path d="${st}" stroke="#a8a090" stroke-width="2.5"/>`;
      g += `<path d="M${f1(x0 + 14)},${f1(y0 - 14)}L${f1(x1 + 14)},${f1(y1 - 14)}" stroke="#c8ccce" stroke-width="3.5"/>`;
      g += `<path d="M${f1(lerp(x0, x1, 0.5) + 14)},${f1(lerp(y0, y1, 0.5) - 14)}v18" stroke="#9aa0a2" stroke-width="3"/>`;
    }
    // the assembly point at the top: a pavilion and a green sign
    const [ax, ay] = path[path.length - 1];
    g += `<g transform="translate(${f1(ax + 40)},${f1(ay + 10)})"><path d="M-60,0V-60M60,0V-60" stroke="#8a6a4a" stroke-width="7"/><path d="M-84,-56L0,-100L84,-56Z" fill="#c8542e" ${OUT2}/><rect x="-62" y="-10" width="124" height="12" fill="#d8d0c0"/>
      <g transform="translate(110,0)"><path d="M0,0V-70" stroke="#9aa0a2" stroke-width="5"/><rect x="-40" y="-118" width="80" height="54" rx="6" fill="#2a9a4a" stroke="#fff" stroke-width="4"/><text x="0" y="-84" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="17" fill="#fff">จุดรวมพล</text></g></g>`;
    return g;
  }
  // a house with a tin roof (for the village behind the beach), origin = the ground under the middle
  const hut = (x, G, s, r, c) => {
    const w = 170 + r() * 90, h = 110 + r() * 40, wall = c || ["#e8dcc4", "#d8e4e4", "#f0d8b8", "#c8d8c0"][Math.floor(r() * 4)];
    let g = CS(0, 4, w * 0.7, 12, 0.7) + `<rect x="${f1(-w / 2)}" y="${f1(-h)}" width="${f1(w)}" height="${f1(h)}" fill="${wall}" ${OUT2}/>`;
    g += `<rect x="${f1(-w * 0.3)}" y="${f1(-h * 0.7)}" width="${f1(w * 0.22)}" height="${f1(h * 0.42)}" fill="#3a4a54" ${OUT2}/><rect x="${f1(w * 0.08)}" y="${f1(-h * 0.8)}" width="${f1(w * 0.2)}" height="${f1(h * 0.8)}" fill="#7a5a3a" ${OUT2}/>`;
    g += `<path d="M${f1(-w / 2 - 20)},${f1(-h)}L${f1(-w * 0.1)},${f1(-h - 70)}H${f1(w * 0.1)}L${f1(w / 2 + 20)},${f1(-h)}Z" fill="url(#tdTin)" ${OUT2}/>`;
    g += `<path d="${Array.from({ length: 9 }, (_, k) => `M${f1(-w / 2 - 14 + k * (w + 28) / 8)},${f1(-h)}l${f1(w * 0.03)},${f1(-62)}`).join("")}" stroke="#7a8488" stroke-width="2" opacity=".6"/>`;
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${f1(s)})">${g}</g>`;
  };

  function landView(L, o) {
    const id = o.id || "tl", P = PAL[o.time || "morning"], r = mk(o.seed || 9);
    sky(L, id, P, 1200, { seed: (o.seed || 9) + 1, sunX: 1260, sunY: 180 });
    put(L.far, hill(id, P, r, { top: 300, foot: 1260, path: [[60, 1250], [-40, 1085], [170, 935], [20, 785], [230, 640], [110, 490], [330, 385]] }));
    // mid: the houses and trees of the village, the warning tower
    const Gm = 1330;
    let m = "";
    for (let k = 0; k < 9; k++) m += casu(-900 + k * 380 + r() * 120, Gm - 30, 0.55 + r() * 0.25, (o.seed || 9) + 40 + k, P.leaf);
    for (let k = 0; k < 10; k++) m += hut(-1000 + k * 360 + r() * 120, Gm, 0.75 + r() * 0.2, r);
    // (none behind the tower: its fronds would tangle with the loudspeakers)
    for (let k = 0; k < 6; k++) { const px = -800 + k * 520 + r() * 200, ps = 0.62 + r() * 0.18, pl = (r() - 0.5) * 0.4; if (Math.abs(px - 890) > 330) m += coco(px, Gm + 10, ps, pl, (o.seed || 9) + 60 + k, { q: 0.5, pal: P.leaf }); }
    m += Tide.tower(890, Gm + 20, 0.98, id);
    put(L.mid, m);
    // set: the sand, the hotel and ยาย's shop right beside it, a longtail pulled up, the sign by the road, a palm framing the right
    let s = `<defs><linearGradient id="${id}-sandG" gradientUnits="userSpaceOnUse" x1="0" y1="1300" x2="0" y2="1950"><stop offset="0" stop-color="${P.sand[1]}"/><stop offset=".6" stop-color="${P.sand[0]}"/><stop offset=".9" stop-color="${P.sand[2]}"/><stop offset="1" stop-color="${P.wet[0]}"/></linearGradient></defs>`;
    s += `<path d="M-3000,1330Q540,1290 4000,1340V2400H-3000Z" fill="url(#${id}-sandG)"/>`;
    for (let k = 0; k < 24; k++) { const y = 1380 + Math.pow(r(), 1.2) * 480, x = -900 + r() * 2900, w = 70 + r() * 220; s += `<path d="M${f1(x)},${f1(y)}q${f1(w / 2)},-7 ${f1(w)},0" stroke="#fff" stroke-width="3" fill="none" opacity=".4"/>`; }
    for (let k = 0; k < 18; k++) { const u = k / 17, x = 560 + Math.sin(u * 4) * 80 + (k % 2 ? 18 : -18), y = 1860 - u * 420, sz = 22 * (1.1 - u * 0.6); s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(sz * 0.5)}" ry="${f1(sz * 0.25)}" fill="${T(P.sand[2], -0.2)}" opacity=".5"/>`; }
    s += `<path d="M95,1490L560,1490L330,1660L-260,1660Z" fill="#2a2018" opacity=".16"/><path d="M590,1560L1075,1560L860,1700L380,1700Z" fill="#2a2018" opacity=".14"/>`;
    s += hotel(id, 330, 1490, 0.84);
    s += flagPole(id, 120, 896, 160, 0.84);
    s += shop(id, 830, 1560, 0.86, r);
    s += `<g id="${id}-boatL0" transform="translate(700,1790) rotate(-3) scale(0.48)">${CS(0, 46, 520, 40, 0.9)}${Tide.longtail({ hull: "#2f6fa0", band: "#d8423a", no: "พง 3127", flip: true, seed: 11 })}</g>`;
    s += Tide.evacSign(160, 1770, 0.72, { id: `${id}-sign`, dir: 0 });
    const rr = mk((o.seed || 9) + 5);
    for (let k = 0; k < 18; k++) { const x = -40 + rr() * 1160, y = 1640 + rr() * 200, sz = 8 + rr() * 10; s += `<path d="M${f1(x - sz)},${f1(y)}a${f1(sz)},${f1(sz * 0.7)} 0 0 1 ${f1(sz * 2)},0l${f1(-sz)},${f1(sz * 0.5)}z" fill="${["#f8f2ea", "#f4d8cc", "#e8dcc0"][k % 3]}" stroke="#9a8a72" stroke-width="1.2"/>`; }
    s += `<g transform="translate(980,1700)">${CS(0, 4, 40, 8)}<ellipse cx="0" cy="-20" rx="26" ry="22" fill="#8a6a3a" ${OUT2}/><path d="M-16,-28q8,-6 20,-3" stroke="#c8a870" stroke-width="3.5" fill="none"/></g><path d="M380,1700c40,-14 80,10 130,-4s70,12 110,0" stroke="#5a6a32" stroke-width="7" fill="none" opacity=".8"/>`;
    s += coco(1400, 2000, 2.3, -0.06, (o.seed || 9) + 71, { id: `${id}-palm0`, pal: P.leaf, fl: 0.6 });
    // the water's edge at the bottom (redrawn): shallows over the sand, the foam lace
    s += `<path id="${id}-swashW" d="" fill="${P.sea[4]}" opacity=".78"/><path id="${id}-swash" d="" stroke="#fff" stroke-width="13" fill="none" stroke-linecap="round" opacity=".95"/><path id="${id}-swash2" d="" stroke="#fff" stroke-width="5" fill="none" opacity=".55"/>`;
    put(L.set, s);
    put(L.fg, `<g transform="translate(-80,-60) rotate(22)">${coco(0, 0, 1.25, 0, 77, { trunk: false, pal: [T(P.leaf[0], -0.3), T(P.leaf[1], -0.25), P.leaf[1]] })}</g>`);
    ST[id] = { kind: "land", P, flag: { px: 120, py: 896, s: 0.84 }, swashY: 1846 };
    landDraw(id, 0);
  }

  // the Thai flag's cloth as five bands rippling from the pole top (px, py)
  function flagDraw(id, px, py, s, t) {
    const W = 110 * s, H = 72 * s, band = (y0, y1) => { let d = ""; for (let k = 0; k <= 10; k++) { const u = k / 10, x = px + u * W, w = Math.sin(u * 5 - t * 6) * 6 * s * u; d += `${k ? "L" : "M"}${f1(x)},${f1(py + y0 * H + w)}`; } for (let k = 10; k >= 0; k--) { const u = k / 10, x = px + u * W, w = Math.sin(u * 5 - t * 6) * 6 * s * u; d += `L${f1(x)},${f1(py + y1 * H + w)}`; } return d + "Z"; };
    const a = el(`${id}-flag`), b = el(`${id}-flagw`), c = el(`${id}-flagb`);
    if (!a) return;
    a.setAttribute("d", band(0, 1)); b.setAttribute("d", band(1 / 6, 5 / 6)); c.setAttribute("d", band(2 / 6, 4 / 6));
  }
  function landDraw(id, t) {
    const S = ST[id];
    if (S.flag) flagDraw(id, S.flag.px, S.flag.py, S.flag.s, t);
    const w = el(`${id}-swash`);
    if (w && S.swashY) {
      const yb = S.swashY + 34 * Math.sin(t * 1.4), pts = [];
      for (let x = -1300; x <= 2400; x += 40) pts.push(`${x},${f1(yb + 12 * Math.sin(x * 0.006 + t * 1.2) + 6 * Math.sin(x * 0.021 - t * 2))}`);
      w.setAttribute("d", `M${pts.join("L")}`);
      el(`${id}-swash2`).setAttribute("d", `M${pts.map((p) => { const [x, y] = p.split(","); return `${x},${f1(+y + 26)}`; }).join("L")}`);
      el(`${id}-swashW`).setAttribute("d", `M${pts.join("L")}L2400,2400L-1300,2400Z`);
    }
  }
  // run a "land" or hill view: the flag, the swash, the palms; o.siren true blinks the tower's beacon
  Tide.land = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, bc = el(`${id}-beacon`);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => {
      const t = t0 + c.t;
      landDraw(id, t);
      [0, 1].forEach((k) => { const p = el(`${id}-palm${k}`); if (p) { const [px, py] = p.getAttribute("data-o").split(" "); p.setAttribute("transform", `rotate(${f1(1.8 * Math.sin(t * 1.1 + k * 2))} ${px} ${py})`); } });
      if (bc) bc.setAttribute("opacity", o.siren ? f1(Math.max(0, Math.sin(t * 9))) : "0");
    } }, t0);
  };

  // ======================== the wave: low on the beach, a wall of muddy water rolling in over the sand ========================
  // The camera stands low (o.hc m) on the upper beach looking out to sea; the sea's usual edge is o.shore m out, the bare seabed beyond.
  // u 0 … 1 brings the wall in from 150 m to 14 m (9 m high once inside ~90 m). Palms and beach shacks standing at fixed distances are
  // swallowed as it passes them, debris rides half-sunk in its face, a runner flees ahead of it (still clear of it at u 1).
  const WAV = { FX: 2400, CX: 540, D0: 150, D1: 14 };
  const WCOL = [[0, "#84794e"], [0.12, "#6c6544"], [0.36, "#50553f"], [0.66, "#2e463f"], [1, "#183438"]];
  const wDist = (u) => lerp(WAV.D0, WAV.D1, u), wHeight = (u) => lerp(5, 9, sm(0, 0.45, u));
  const wCol = (f) => { let i = 0; while (i < WCOL.length - 2 && f > WCOL[i + 1][0]) i++; return mix(WCOL[i][1], WCOL[i + 1][1], clamp((f - WCOL[i][0]) / (WCOL[i + 1][0] - WCOL[i][0]), 0, 1)); };
  const pk = (v, p) => Math.pow(Math.abs(Math.sin(v)), p);
  // smooth value noise 0…1 and a few octaves of it, for torn edges that never repeat
  const hsh = (i) => { const v = Math.sin(i * 127.1 + 311.7) * 43758.5453; return v - Math.floor(v); };
  const vn = (x) => { const i = Math.floor(x), f = x - i; return lerp(hsh(i), hsh(i + 1), f * f * (3 - 2 * f)); };
  const fbm = (x) => 0.5 * vn(x) + 0.28 * vn(x * 2.13 + 17.3) + 0.14 * vn(x * 4.37 + 41.9) + 0.08 * vn(x * 8.71 + 73.1);
  // the sum of sharp torn points (each {X, h, w}, flickering) under a sample at X: the raw stuff of a ripped foam edge
  const tearAt = (list, X, t) => { let v = 0; for (const q of list) { const dx = Math.abs(X - q.X); if (dx < q.w) v += q.h * (0.55 + 0.45 * Math.sin(t * q.f + q.ph)) * Math.pow(1 - dx / q.w, 1.4); } return v; };
  // a torn, pointed fragment (a sheet of foam, a gout of mud): radii j round an ellipse w long and h thick, turned by a radians
  const shardD = (cx, cy, w, h, a, j) => {
    const n = j.length, ca = Math.cos(a), sa = Math.sin(a);
    let d = "";
    for (let i = 0; i < n; i++) { const th = (i / n) * Math.PI * 2, ex = Math.cos(th) * w * j[i], ey = Math.sin(th) * h * j[i]; d += `${i ? "L" : "M"}${f1(cx + ex * ca - ey * sa)},${f1(cy + ex * sa + ey * ca)}`; }
    return d + "Z";
  };
  const jag8 = (r) => Array.from({ length: 8 }, (_, i) => (i % 4 === 0 ? 1 : 0.3 + r() * 0.62));
  // a droplet: an ellipse rx × ry stretched along a radians
  const dropD = (cx, cy, rx, ry, a) => { const c = Math.cos(a) * rx, s = Math.sin(a) * rx, g = f1(a * 57.2958); return `M${f1(cx - c)},${f1(cy - s)}a${f1(rx)},${f1(ry)} ${g} 1,0 ${f1(2 * c)},${f1(2 * s)}a${f1(rx)},${f1(ry)} ${g} 1,0 ${f1(-2 * c)},${f1(-2 * s)}Z`; };

  // ---------- what the wall carries (local units 100 = 1 m, centred): svg, the silhouette the water may cover, size ----------
  const plankSVG = (L, W, c, broken) => `<path d="M${-L / 2},${-W / 2}H${L / 2}${broken ? `l-14,${f1(W * 0.3)}l10,${f1(W * 0.25)}l-12,${f1(W * 0.45)}` : `V${W / 2}`}H${-L / 2}Z" fill="${c}" ${OUT2}/><path d="M${-L / 2 + 12},${f1(-W * 0.12)}H${L / 2 - 30}M${-L / 2 + 40},${f1(W * 0.2)}H${L / 2 - 60}" stroke="${T(c, -0.35)}" stroke-width="2" opacity=".6"/><circle cx="${-L / 2 + 14}" cy="0" r="2.5" fill="#3a342e"/><circle cx="${L / 2 - 40}" cy="0" r="2.5" fill="#3a342e"/>`;
  const UMB = "M-100,0Q-92,-66 0,-80Q92,-66 100,0Q75,-12 50,0Q25,-12 0,0Q-25,-12 -50,0Q-75,-12 -100,0Z";
  const umbSVG = `<path d="M-3,-80V150" stroke="#c8ccce" stroke-width="7"/><path d="${UMB}" fill="#e8402e" ${OUT2}/><path d="M-50,0Q-40,-58 0,-80Q-16,-52 -25,-6ZM50,0Q40,-58 0,-80Q16,-52 25,-6Z" fill="#f6f2ea"/><path d="${UMB}" fill="none" ${OUT2}/><path d="M-3,-80v-10" stroke="#c8ccce" stroke-width="6"/>`;
  const coolerSVG = `<rect x="-31" y="-18" width="62" height="38" rx="5" fill="#2e78c8" ${OUT2}/><rect x="-34" y="-27" width="68" height="11" rx="4" fill="#f4f4f0" ${OUT2}/><path d="M-12,-31h24" stroke="#f4f4f0" stroke-width="5" stroke-linecap="round"/><path d="M-24,-6h48" stroke="#fff" stroke-width="3" opacity=".35"/>`;
  const LT_HULL = "M-500,-120L-486,-34Q-472,18 -398,32L300,40Q420,36 470,-40Q500,-108 520,-210Q532,-290 548,-336L544,-344Q530,-300 512,-214Q496,-150 436,-140Q20,-104 -500,-120Z";
  const DEBRIS = [
    // the green longtail that lay stranded on the seabed: thrown up the face bow first, stern and engine under
    { svg: () => Tide.longtail({ hull: "#2e8a5a", band: "#f2c02a", no: "พง 0418", seed: 5 }), sil: `<path d="${LT_HULL}"/><path d="M-580,-280H-440V-150H-580ZM-545,-205L-875,22L-858,44L-532,-186Z"/>`,
      k: 0.62, X: -3.0, h: 0.56, a: -22, va: 0, wob: 3, ca: -4, off: -0.8, R: 3.8, fw: 0.3 },
    { svg: () => plankSVG(330, 26, "#9a7046", false), sil: `<rect x="-170" y="-16" width="340" height="32"/>`, k: 1, X: 0.6, h: 0.5, a: 30, va: 52, wob: 0, ca: 8, off: 0.05, R: 1.9, fw: 0.22 },
    { svg: () => plankSVG(180, 22, "#b08a5a", true), sil: `<rect x="-95" y="-14" width="190" height="28"/>`, k: 1, X: 3.6, h: 0.42, a: -40, va: -80, wob: 0, ca: -6, off: 0, R: 1.1, fw: 0.18 },
    { svg: () => umbSVG, sil: `<path d="${UMB}"/><rect x="-8" y="-90" width="10" height="245"/>`, k: 1, X: 4.8, h: 0.24, a: 150, va: 0, wob: 22, ca: 4, off: 0.15, R: 1.45, fw: 0.22 },
    { svg: () => coolerSVG, sil: `<rect x="-36" y="-34" width="72" height="56"/>`, k: 1, X: 2.0, h: 0.2, a: 0, va: 0, wob: 16, ca: -4, off: 0.08, R: 0.55, fw: 0.14 },
  ];

  // ---------- what stands on the beach in its path: a massage hut, a coconut-drink stall (100 = 1 m, origin the sand) ----------
  const hutSVG = () => {
    let g = CS(0, 2, 240, 26, 0.45);
    g += [-172, -60, 60, 172].map((x) => `<rect x="${x - 6}" y="-50" width="12" height="50" fill="#5e4630"/>`).join("");
    g += `<rect x="-196" y="-64" width="392" height="16" fill="#9a7448" ${OUT2}/>`;
    g += `<rect x="-180" y="-78" width="166" height="14" rx="4" fill="#c8402e" ${OUT2}/><rect x="14" y="-78" width="166" height="14" rx="4" fill="#2e62a8" ${OUT2}/><path d="M-176,-78l22,-26l22,26zM20,-78l22,-26l22,26z" fill="#e8b830" ${OUT2}/>`;
    g += [-188, 188].map((x) => `<rect x="${x - 7}" y="-268" width="14" height="206" fill="#c8a868" ${OUT2}/><path d="M${x - 7},-210h14M${x - 7},-150h14M${x - 7},-100h14" stroke="#8a6a38" stroke-width="2.5"/>`).join("");
    g += `<path d="M-182,-258Q-150,-170 -178,-84L-152,-84Q-130,-170 -150,-258Z" fill="#f2eee4" ${OUT2}/><path d="M182,-258Q150,-170 178,-84L152,-84Q130,-170 150,-258Z" fill="#f2eee4" ${OUT2}/>`;
    let fr = ""; for (let i = 0; i <= 24; i++) fr += `L${f1(242 - i * 20.2)},${-252 + (i % 2 ? 12 : 0)}`;
    g += `<path d="M-128,-338L128,-338L242,-252${fr}Z" fill="#b89a5a" ${OUT2}/>`;
    g += `<path d="${Array.from({ length: 14 }, (_, i) => `M${-120 + i * 18.5},-336L${-226 + i * 34.8},-258`).join("")}" stroke="#8e7442" stroke-width="3" opacity=".7"/>`;
    g += `<rect x="-104" y="-322" width="208" height="46" rx="5" fill="#f4ead2" ${OUT2}/><text x="0" y="-288" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="#b8302a">นวดแผนไทย</text>`;
    return g;
  };
  const stallSVG = () => {
    let g = CS(0, 2, 190, 24, 0.45);
    g += `<path d="M-136,-122V-246M136,-122V-246" stroke="#7a5a3a" stroke-width="10"/>`;
    g += `<rect x="-140" y="-112" width="280" height="112" fill="#3a88c4" ${OUT2}/><rect x="-140" y="-86" width="280" height="12" fill="#f4f2ea"/><rect x="-152" y="-126" width="304" height="16" rx="3" fill="#a87a4a" ${OUT2}/>`;
    g += `<text x="0" y="-26" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="32" fill="#fff">น้ำมะพร้าว</text>`;
    g += [-110, -78, -46].map((x) => `<circle cx="${x}" cy="-142" r="16" fill="#6e9a3a" ${OUT2}/>`).join("") + [40, 62, 84].map((x) => `<rect x="${x - 6}" y="-170" width="12" height="44" rx="4" fill="${x === 62 ? "#e8a020" : "#d84a36"}" ${OUT2}/>`).join("");
    g += `<path d="M-180,-240Q0,-272 180,-240L176,-214${Array.from({ length: 10 }, (_, i) => `Q${158 - i * 36},-204 ${140 - i * 36},-214`).join("")}L-180,-214Z" fill="url(#tdTarp)" ${OUT2}/>`;
    return g;
  };
  // [screen x, distance m, kind, palm height m, lean]: back to front; each is swallowed when the wall reaches its distance
  const OVER = [[600, 41, "palm", 8, 0.04], [250, 36, "palm", 7, -0.08], [990, 31.5, "stall"], [760, 27.3, "palm", 6, 0.07], [330, 26.6, "hut"], [118, 25.8, "palm", 6.5, -0.05], [1065, 24.8, "palm", 5.5, 0.12]];

  // ---------- a figure sprinting left, looking back (100 units = 1.65 m, feet at 0,0): four frames of the stride #id-rn0 … rn3 ----------
  const RUN = [
    { nl: [[0, -46], [-14, -28], [-26, -6]], fl: [[0, -46], [9, -28], [26, -34]], na: [[-6, -74], [3, -61], [12, -69]], fa: [[-6, -74], [-17, -64], [-27, -74]] },
    { nl: [[0, -48], [-2, -26], [1, -3]], fl: [[0, -48], [-15, -36], [-8, -16]], na: [[-6, -76], [-10, -61], [-19, -65]], fa: [[-6, -76], [-2, -62], [5, -58]] },
    { nl: [[0, -46], [9, -28], [26, -34]], fl: [[0, -46], [-14, -28], [-26, -6]], na: [[-6, -74], [-17, -64], [-27, -74]], fa: [[-6, -74], [3, -61], [12, -69]] },
    { nl: [[0, -48], [-15, -36], [-8, -16]], fl: [[0, -48], [-2, -26], [1, -3]], na: [[-6, -76], [-2, -62], [5, -58]], fa: [[-6, -76], [-10, -61], [-19, -65]] },
  ];
  const runnerSVG = (id, [sh, pa, sk, hr]) => RUN.map((p, i) => {
    const dk = T(sk, -0.25), hy = p.nl[0][1];
    const limb = (pts, w, c) => { const d = `M${pts.map(P2).join("L")}`; return `<path d="${d}" stroke="${INK}" stroke-width="${w + 3.4}" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" stroke="${c}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`; };
    let g = limb(p.fa, 5, dk) + limb(p.fl, 7, dk);
    g += `<path d="M-10,${hy - 5}L9,${hy - 5}L11,${hy + 9}L-11,${hy + 8}Z" fill="${pa}" ${OUT2}/>` + limb(p.nl, 7, sk);
    g += `<path d="M-15,${hy - 29}Q-6,${hy - 34} 4,${hy - 30}L9,${hy - 3}L-10,${hy - 1}Z" fill="${sh}" ${OUT2}/>` + limb(p.na, 5, sk);
    g += `<circle cx="-9" cy="${hy - 41}" r="9" fill="${sk}" ${OUT2}/><path d="M-18,${hy - 43}A9.4,9.4 0 0 1 0,${hy - 40}Q-5,${hy - 47} -18,${hy - 43}Z" fill="${hr}"/><circle cx="-3" cy="${hy - 41}" r="1.4" fill="${INK}"/>`;
    return `<g id="${id}-rn${i}"${i ? ' opacity="0"' : ""}>${g}</g>`;
  }).join("");

  function tideWave(L, o) {
    const id = o.id || "tw", P = PAL[o.time || "squall"], r = mk(o.seed || 17), HZ = o.hz ?? 1290, hc = o.hc ?? 1.2, SH = o.shore ?? 45;
    const { FX, CX } = WAV, yAt = (d) => HZ + FX * hc / d;
    // the sky: a low lid of grey cloud, paler toward the sea; torn scud driven inland beneath it
    let k0 = `<defs><linearGradient id="${id}-skyG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(HZ - 1700)}" x2="0" y2="${HZ}"><stop offset="0" stop-color="${P.sky[0]}"/><stop offset=".45" stop-color="${P.sky[1]}"/><stop offset=".8" stop-color="${P.sky[2]}"/><stop offset="1" stop-color="${P.sky[3]}"/></linearGradient>
      <radialGradient id="${id}-skyL"><stop offset="0" stop-color="#eef0ec" stop-opacity=".4"/><stop offset="1" stop-color="#eef0ec" stop-opacity="0"/></radialGradient></defs>`;
    k0 += `<rect x="-3000" y="${f1(HZ - 4000)}" width="8000" height="5400" fill="url(#${id}-skyG)"/><ellipse cx="760" cy="${f1(HZ - 1180)}" rx="1000" ry="460" fill="url(#${id}-skyL)"/>`;
    for (let k = 0; k < 14; k++) {
      const cy = HZ - 1720 + k * 100 + r() * 50, cx = -500 + r() * 2100, w = 700 + r() * 1000, h = 30 + r() * 56, dk = r() < 0.6, top = [], bot = [];
      for (let i = 0; i <= 9; i++) { const q = i / 9, x = cx - w / 2 + q * w, env = Math.pow(Math.sin(Math.PI * q), 0.7) + 0.02; top.push([x, cy - h * env * (0.6 + r() * 0.6)]); bot.push([x, cy + h * 0.3 * env * (0.5 + r() * 0.7)]); }
      k0 += `<path d="${smoothClosed(top.concat(bot.reverse()))}" fill="${dk ? "#28323c" : "#aab2b4"}" opacity="${f1(dk ? 0.12 + r() * 0.16 : 0.1 + r() * 0.12)}"/>`;
    }
    put(L.sky, k0);
    let sc = "";
    for (let k = 0; k < 10; k++) {
      const cx = -600 + r() * 2300, cy = HZ - 660 - r() * 700, w = 220 + r() * 420, h = 16 + r() * 26, pts = [];
      for (let i = 0; i < 12; i++) { const a = (i / 12) * Math.PI * 2, j = i % 3 === 0 ? 1.15 : 0.55 + r() * 0.45; pts.push([cx + Math.cos(a) * w / 2 * j, cy + Math.sin(a) * h * j]); }
      sc += `<path d="${smoothClosed(pts)}" fill="#323c44" opacity="${f1(0.3 + r() * 0.3)}"/>`;
    }
    put(L.far, `<g id="${id}-scud">${sc}</g>`);
    // mid: birds fleeing inland, high over the wall
    put(L.mid, `<g id="${id}-birds">${Array.from({ length: 14 }, () => { const bx = -100 + r() * 1200, by = HZ - 760 - r() * 520, bs = 0.6 + r() * 0.8; return `<path d="M${f1(bx - 15 * bs)},${f1(by)}q${f1(7 * bs)},${f1(-10 * bs)} ${f1(15 * bs)},0q${f1(7 * bs)},${f1(-10 * bs)} ${f1(15 * bs)},0" stroke="#1e2428" stroke-width="${f1(2.8 * bs)}" fill="none" stroke-linecap="round"/>`; }).join("")}</g>`);
    // the ground: the bare seabed past the sea's usual edge (hidden once the wall is on the sand), then the beach up to the camera
    const Y0 = yAt(SH);
    let s = `<defs><linearGradient id="${id}-bedG" gradientUnits="userSpaceOnUse" x1="0" y1="${HZ}" x2="0" y2="${f1(Y0)}"><stop offset="0" stop-color="${mix(P.bed[2], P.haze, 0.4)}"/><stop offset="1" stop-color="${P.bed[0]}"/></linearGradient>
      <linearGradient id="${id}-beachG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(Y0)}" x2="0" y2="1940"><stop offset="0" stop-color="${P.wet[0]}"/><stop offset=".05" stop-color="${P.sand[2]}"/><stop offset=".45" stop-color="${P.sand[1]}"/><stop offset="1" stop-color="${P.sand[0]}"/></linearGradient></defs>`;
    s += `<rect x="-3000" y="${HZ - 2}" width="8000" height="${f1(Y0 - HZ + 4)}" fill="url(#${id}-bedG)"/>`;
    for (let k = 0; k < 12; k++) { const d = dRand(r, SH + 4, 300), R = 1.5 + r() * 4, px = FX / d; s += pool(r, P, -900 + r() * 2900, yAt(d), R * px, clamp(R * px * hc / d, 1, R * px * 0.3)); }
    s += `<rect x="-3000" y="${f1(Y0)}" width="8000" height="${f1(2000 - Y0)}" fill="url(#${id}-beachG)"/>`;
    // footprints running up the beach toward the camera: everyone who got the warning
    let fp = "";
    for (let k = 0; k < 8; k++) {
      let X = -6 + r() * 12, n = 0; const dir = (r() - 0.5) * 0.14;
      for (let d = 40; d > 3; d -= 0.72 + r() * 0.2, n++) { X += dir; const px = FX / d, x = CX + (X + (n % 2 ? 0.12 : -0.12)) * px; fp += `<ellipse cx="${f1(x)}" cy="${f1(yAt(d))}" rx="${f1(0.055 * px)}" ry="${f1(0.13 * px * hc / d + 0.5)}" fill="#6e5e46" opacity=".28"/>`; }
    }
    s += fp;
    // left behind on the sand: flip-flops, a child's bucket and spade, a towel, a straw hat
    const flat = (x, d, svg, rot = 0) => { const k = FX / d / 100; return `<g transform="translate(${f1(x)},${f1(yAt(d))}) scale(${k.toFixed(4)},${(k * Math.min(1, Math.max(0.32, 2.4 * hc / d))).toFixed(4)}) rotate(${rot})">${svg}</g>`; };
    const ff = (c) => `<path d="M-14,-1Q-15,-7 -9,-8L9,-9Q15,-9 15,-3Q15,3 9,4L-9,5Q-15,5 -14,-1Z" fill="${c}" ${OUT2}/><path d="M-12,-1Q-13,-5 -9,-6L8,-7Q12,-7 12,-3" stroke="#fff" stroke-width="1.6" fill="none" opacity=".45"/><path d="M5,-2L-3,-8M5,-2L-3,4" stroke="#2a62b0" stroke-width="2.6" stroke-linecap="round"/>`;
    s += flat(170, 12.5, `<rect x="-80" y="-40" width="160" height="80" rx="4" fill="#f2efe6" ${OUT2}/><path d="M-80,-24H80M-80,-8H80M-80,8H80M-80,24H80" stroke="#d8583a" stroke-width="7"/><rect x="-80" y="-40" width="160" height="80" rx="4" fill="none" ${OUT2}/>`, -10);
    s += flat(330, 6.6, ff("#f2c02a"), 22) + flat(372, 6.4, ff("#f2c02a"), -34);
    s += flat(905, 7.8, `<ellipse rx="22" ry="20" fill="#e2c27a" ${OUT2}/><ellipse cy="-2" rx="11" ry="10" fill="#d4b066" ${OUT2}/><path d="M-11,-1Q0,4 11,-1" stroke="#b8402e" stroke-width="3" fill="none"/>`, 10);
    { const k = FX / 9.4 / 100; s += `<g transform="translate(790,${f1(yAt(9.4))}) scale(${k.toFixed(4)})">${CS(0, 0, 26, 6, 0.5)}<g transform="rotate(-72)"><path d="M-11,-22L11,-22L8,0L-8,0Z" fill="#e84a2e" ${OUT2}/><ellipse cx="0" cy="-22" rx="11" ry="3.5" fill="#a82a1e" ${OUT2}/><path d="M-11,-20Q0,-38 11,-20" stroke="#f2c02a" stroke-width="2" fill="none"/></g><path d="M22,-2L42,-14" stroke="#f2c02a" stroke-width="3.5" stroke-linecap="round"/><path d="M16,0L24,-7L28,-2L20,5Z" fill="#2a8ad0" ${OUT2}/></g>`; }
    put(L.set, s);

    // the wall, redrawn every frame: its body, mud boiling and flow drawn up the face, debris riding half-sunk, the torn crest, a boiling skirt, spray
    const A = (n, f) => Array.from({ length: n }, f);
    const st = {
      bands: A(26, () => ({ X: -11 + r() * 22, lx: 2 + r() * 5, h0: r(), v: 0.05 + r() * 0.07, w: 0.03 + r() * 0.07, lt: r() < 0.5, ph: r() * 6 })),
      diag: A(30, () => ({ X: -11 + r() * 22, lx: 0.7 + r() * 2.2, h0: r(), v: 0.07 + r() * 0.08, dh: (0.04 + r() * 0.1) * (r() < 0.7 ? 1 : -1), w: 0.025 + r() * 0.05, lt: r() < 0.6 })),
      shard: A(90, () => ({ X: -11 + r() * 22, h0: r(), v: 0.04 + r() * 0.08, sz: 0.3 + r() * 1.1, asp: 0.1 + r() * 0.16, a: (r() - 0.5) * 0.5, va: (r() - 0.5) * 0.3, tone: r() < 0.45 ? 0 : r() < 0.84 ? 1 : 2, j: jag8(r) })),
      boil: A(10, () => ({ X: -10 + r() * 20, h0: r(), v: 0.03 + r() * 0.04, sz: 1.2 + r() * 1.6, asp: 0.45 + r() * 0.3, a: (r() - 0.5) * 0.6, j: A(10, () => 0.7 + r() * 0.3) })),
      // torn points along the crest's top, foam tongues hanging off its underside, torn points along the skirt
      tear: A(170, () => ({ X: -12 + r() * 24, h: 0.008 + Math.pow(r(), 2.4) * 0.065, w: 0.04 + r() * 0.15, f: 1.5 + r() * 3, ph: r() * 6.28 })),
      drip: A(120, () => ({ X: -12 + r() * 24, h: 0.015 + Math.pow(r(), 1.8) * 0.13, w: 0.05 + r() * 0.24, f: 0.6 + r() * 1.2, ph: r() * 6.28 })),
      stear: A(110, () => ({ X: -12 + r() * 24, h: 0.008 + Math.pow(r(), 2.2) * 0.034, w: 0.12 + r() * 0.28, f: 2 + r() * 3, ph: r() * 6.28 })),
      // lace: torn white streaks peeling off the crest and sliding down across the face
      lace: A(34, () => ({ X: -11 + r() * 22, ph: r(), v: 0.18 + r() * 0.2, len: 0.3 + r() * 0.7, asp: 0.13 + r() * 0.1, a: 0.15 + r() * 0.35, j: jag8(r) })),
      drop: A(260, () => ({ X: -11 + r() * 22, ph: r(), life: 0.45 + r() * 0.5, vf: 0.8 + r() * 2.7, vu: 0.5 + r() * 2.6, vx: (r() - 0.5) * 2, sz: 0.009 + r() * 0.022 })),
      mist: A(90, () => ({ X: -11 + r() * 22, ph: r(), life: 0.8 + r() * 0.7, vf: 0.3 + r() * 0.9, vu: 1 + r() * 1.6, vx: (r() - 0.5) * 1.4, sz: 0.005 + r() * 0.009 })),
      sheet: A(26, () => ({ X: -10 + r() * 20, ph: r(), life: 0.35 + r() * 0.3, vf: 3 + r() * 4, vu: 0.6 + r() * 1.8, vx: (r() - 0.5) * 2.4, h0: 0.3 + r() * 0.9, sz: 0.2 + r() * 0.4, j: jag8(r), lt: r() < 0.65 })),
    };
    let w = `<g id="${id}-wave"><defs>
      <linearGradient id="${id}-wallG" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1000">${WCOL.map(([q, c]) => `<stop offset="${q}" stop-color="${c}"/>`).join("")}</linearGradient>
      <linearGradient id="${id}-lipG" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1000"><stop offset="0" stop-color="#c2b07a" stop-opacity=".45"/><stop offset="1" stop-color="#c2b07a" stop-opacity="0"/></linearGradient>
      <clipPath id="${id}-bodyC"><path id="${id}-bodyCP" d=""/></clipPath>${DEBRIS.map((q, k) => `<clipPath id="${id}-dc${k}">${q.sil.replace(/<(path|rect) /g, '<$1 transform="scale(1.06)" ')}</clipPath><linearGradient id="${id}-lg${k}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1000">${WCOL.map(([o2, c]) => `<stop offset="${o2}" stop-color="${c}"/>`).join("")}</linearGradient>`).join("")}</defs>`;
    w += `<path id="${id}-wall" d="" fill="url(#${id}-wallG)"/><g clip-path="url(#${id}-bodyC)"><path id="${id}-boil" d="" fill="#857a4e" opacity=".2"/>`;
    w += st.bands.map((b, k) => `<path id="${id}-bd${k}" d="" stroke="${b.lt ? "#a89c72" : "#14221f"}" fill="none" stroke-linecap="round"/>`).join("");
    w += st.diag.map((b, k) => `<path id="${id}-dg${k}" d="" stroke="${b.lt ? "#b0a47a" : "#162420"}" fill="none" stroke-linecap="round"/>`).join("");
    w += `<path id="${id}-sh0" d="" fill="#13211f" opacity=".24"/><path id="${id}-sh1" d="" fill="#8e8358" opacity=".22"/><path id="${id}-sh2" d="" fill="#c8ccbe" opacity=".2"/><path id="${id}-lip" d="" fill="url(#${id}-lipG)"/><path id="${id}-lace" d="" fill="#eef1ec" opacity=".42"/>`;
    w += DEBRIS.map((q, k) => `<g id="${id}-deb${k}">${q.svg()}<path id="${id}-lap${k}" d="" clip-path="url(#${id}-dc${k})" fill="url(#${id}-lg${k})" opacity=".97"/></g><path id="${id}-lapf${k}" d="" fill="#e2e7e1"/>`).join("") + `</g>`;
    w += `<path id="${id}-veil" d="" fill="#e4e9e6" opacity=".16"/><path id="${id}-cr0" d="" fill="#aab4af"/><path id="${id}-cr1" d="" fill="#d6dcd6"/><path id="${id}-cr2" d="" fill="#f5f7f2"/>`;
    w += `<path id="${id}-sheet" d="" fill="#5c5a44" opacity=".92"/><path id="${id}-sheetF" d="" fill="#e8ebe4" opacity=".9"/>`;
    w += `<path id="${id}-sk0" d="" fill="#b4bdb8" opacity=".6"/><path id="${id}-sk1" d="" fill="#d2d8d2"/><path id="${id}-sk2" d="" fill="#f3f5f0"/><path id="${id}-ts0" d="" fill="#a6b0ac" opacity=".85"/><path id="${id}-ts1" d="" fill="#f0f2ec" opacity=".9"/>`;
    w += `<path id="${id}-sp0" d="" fill="#eef2ee" opacity=".22"/><path id="${id}-sp1" d="" fill="#eef2ee" opacity=".45"/><path id="${id}-sp2" d="" fill="#f4f6f2" opacity=".75"/></g>`;
    put(L.set, w);
    // in front of it: palms and shacks it is about to swallow, foam climbing them as it arrives; then the runner
    const leafW = ["#2c5232", "#467840", "#86a862"];
    const ov = OVER.map(([x, d, kind, m, lean], i) => {
      const px = FX / d, G = yAt(d), palm = kind === "palm";
      const body = palm ? coco(0, 0, +(px * m / 900).toFixed(4), lean, (o.seed || 17) + 40 + i, { id: `${id}-ovp${i}`, pal: leafW, fl: 0.72 }) : `<g transform="scale(${(px / 100).toFixed(4)})">${kind === "hut" ? hutSVG() : stallSVG()}</g>`;
      return { x, d, palm, G, h: palm ? 1.5 : kind === "hut" ? 2.1 : 1.7, w: palm ? 3.4 : kind === "hut" ? 5.6 : 4.2, fmax: 1, svg: `<g id="${id}-ov${i}"><g id="${id}-ovr${i}" transform="translate(${x},${f1(G)})">${body}</g></g><path id="${id}-ovg${i}" d="" fill="${mix(wCol(0.55), "#b8c0b6", 0.25)}"/><path id="${id}-ovm${i}" d="" fill="#c3cac3"/><path id="${id}-ovw${i}" d="" fill="#eef1ec"/><path id="${id}-ovs${i}" d="" fill="#f0f3ee" opacity=".85"/>` };
    });
    put(L.set, ov.map((q) => q.svg).join(""));
    if (o.runner !== false) put(L.set, `<g id="${id}-rn">${CS(0, 0, 26, 6, 0.4)}${runnerSVG(id, ["#d8402e", "#2a3a62", "#c4885c", "#1e1a18"])}</g>`);
    ST[id] = { kind: "wave", P, HZ, hc, ...st, ov, run: o.runner !== false };
    waveDraw(id, 0, o.u ?? 0.8);
  }

  // redraw the wall at time t and progress u (0 far out … 1 at 14 m and towering)
  function waveDraw(id, t, u) {
    const S = ST[id], { HZ, hc } = S, { FX, CX } = WAV, dW = wDist(u), Hm = wHeight(u), px = FX / dW, base = HZ + hc * px, Hp = Hm * px;
    const Xs = (x) => (x - CX) / px, xs = (X) => CX + X * px;
    const crest = (X) => 0.9 + 0.06 * Math.sin(X * 0.45 + 1.1) + 0.035 * Math.sin(X * 1.3 + t * 1.1) + 0.015 * Math.sin(X * 3.7 - t * 2.3);
    const spike = (X) => 0.05 * pk(X * 4.1 + t * 1.9, 8) + 0.035 * pk(X * 7.3 - t * 2.9 + 1, 10) + 0.022 * pk(X * 13.1 + t * 3.7 + 2, 12) + 0.006 * Math.sin(X * 23 + t * 5);
    const bandH = (X) => 0.065 + 0.025 * Math.sin(X * 0.9 + 2) + 0.015 * Math.sin(X * 2.7 - t * 1.2);
    const tongue = (X) => 0.09 * pk(X * 1.6 + 0.5 + t * 0.4, 6) + 0.06 * pk(X * 3.9 + 1.7 - t * 0.7, 9) + 0.03 * pk(X * 8.3 + t, 12);
    const hY = (X, h) => base - Hp * h * crest(X);
    const set = (k, a, v) => el(`${id}-${k}`).setAttribute(a, v);
    // the body: a steep face up to a ragged crest line
    const X0 = -80, X1 = 1160, cols = [];
    for (let x = X0; x <= X1; x += 4) { const X = Xs(x); cols.push({ x, X, top: base - Hp * crest(X) }); }
    const body = `M${X0},${f1(base + 6)}L${cols.map((c) => `${c.x},${f1(c.top)}`).join("L")}L${X1},${f1(base + 6)}Z`;
    set("wall", "d", body); set("bodyCP", "d", body);
    set("wallG", "y1", f1(base - Hp * 0.97)); set("wallG", "y2", f1(base));
    set("lipG", "y1", f1(base - Hp * 0.92)); set("lipG", "y2", f1(base - Hp * 0.6));
    set("lip", "d", `M${cols.map((c) => `${c.x},${f1(c.top + Hp * 0.03)}`).join("L")}L${X1},${f1(base - Hp * 0.58)}L${X0},${f1(base - Hp * 0.58)}Z`);
    // the face: mud boiling up, long flow lines drawn up the wall, shorter sheared streaks, churned fragments — all climbing
    let bo = "";
    S.boil.forEach((b) => { const p = (b.h0 + t * b.v) % 1, sz = b.sz * px * (0.6 + 0.5 * Math.sin(Math.PI * p)); bo += shardD(xs(b.X), hY(b.X, 0.05 + 0.6 * p), sz, sz * b.asp, b.a, b.j); });
    set("boil", "d", bo);
    S.bands.forEach((b, k) => {
      const p = (b.h0 + t * b.v) % 1, h = 0.05 + 0.8 * p; let d = "";
      for (let i = 0; i <= 10; i++) { const X = b.X - b.lx + (b.lx * i) / 5; d += `${i ? "L" : "M"}${f1(xs(X))},${f1(hY(X, h) + Hp * 0.008 * Math.sin(X * 2.1 + b.ph + t * 1.7))}`; }
      const e = el(`${id}-bd${k}`); e.setAttribute("d", d); e.setAttribute("stroke-width", f1(Math.max(0.6, b.w * px))); e.setAttribute("opacity", f1(Math.pow(Math.sin(Math.PI * p), 0.8) * (b.lt ? 0.24 : 0.32)));
    });
    S.diag.forEach((b, k) => {
      const p = (b.h0 + t * b.v) % 1, ha = 0.08 + 0.72 * p, hb = clamp(ha + b.dh, 0.04, 0.88), Xb = b.X + b.lx, mx = (b.X + Xb) / 2, mh = (ha + hb) / 2 + 0.015;
      const e = el(`${id}-dg${k}`); e.setAttribute("d", `M${f1(xs(b.X))},${f1(hY(b.X, ha))}Q${f1(xs(mx))},${f1(hY(mx, mh))} ${f1(xs(Xb))},${f1(hY(Xb, hb))}`);
      e.setAttribute("stroke-width", f1(Math.max(0.6, b.w * px))); e.setAttribute("opacity", f1(Math.sin(Math.PI * p) * (b.lt ? 0.24 : 0.1)));
    });
    const sh = ["", "", ""];
    S.shard.forEach((b) => { const p = (b.h0 + t * b.v) % 1, sz = b.sz * px * Math.sin(Math.PI * p); if (sz > 0.8) sh[b.tone] += shardD(xs(b.X + Math.sin(t * 0.7 + b.a * 9) * 0.2), hY(b.X, 0.03 + 0.78 * p), sz, sz * b.asp, b.a + b.va * t, b.j); });
    sh.forEach((d, k) => set(`sh${k}`, "d", d));
    // debris riding in the face: its lower part sunk behind a ragged waterline (painted over in the face's colour, clipped to its outline)
    DEBRIS.forEach((q, k) => {
      const X = q.X + 0.25 * Math.sin(t * 0.5 + k), x = xs(X), y = hY(X, q.h + 0.012 * Math.sin(t * 1.3 + k * 2)), sc = (px / 100) * q.k, a = q.a + q.va * t + q.wob * Math.sin(t * 1.1 + k), ar = a * Math.PI / 180;
      set(`deb${k}`, "transform", `translate(${f1(x)},${f1(y)}) rotate(${f1(a)}) scale(${sc.toFixed(4)})`);
      const ca = Math.cos(q.ca * Math.PI / 180), sa = Math.sin(q.ca * Math.PI / 180), nx = -sa, ny = ca, R = q.R * px, cx = x + nx * q.off * px, cy = y + ny * q.off * px, line = [];
      for (let i = 0; i <= 16; i++) { const s = (i / 16) * 2 - 1, j = (0.05 * Math.sin(s * 7 + t * 4 + k) + 0.06 * pk(s * 11 + t * 2.6 + k, 6)) * R; line.push([cx + s * R * ca - nx * j, cy + s * R * sa - ny * j]); }
      const far = 2.2 * R, poly = line.concat([[line[16][0] + nx * far, line[16][1] + ny * far], [line[0][0] + nx * far, line[0][1] + ny * far]]);
      const ic = Math.cos(-ar), is = Math.sin(-ar), loc = poly.map(([wx, wy]) => { const dx = (wx - x) / sc, dy = (wy - y) / sc; return [dx * ic - dy * is, dx * is + dy * ic]; });
      set(`lap${k}`, "d", `M${loc.map(P2).join("L")}Z`);
      const lg = el(`${id}-lg${k}`); lg.setAttribute("y1", f1(base - Hp * 0.97)); lg.setAttribute("y2", f1(base)); lg.setAttribute("gradientTransform", `scale(${(1 / sc).toFixed(5)}) rotate(${f1(-a)}) translate(${f1(-x)},${f1(-y)})`);
      const fw = q.fw * px, up = [], dn = [];
      line.forEach(([lx, ly], i) => { const s = i / 16, env = Math.sin(Math.PI * s), spk = fw * env * (0.45 + 0.9 * pk(s * 9 + t * 3.1 + k, 4)); up.push([lx - nx * spk, ly - ny * spk]); dn.push([lx + nx * fw * env * 0.55, ly + ny * fw * env * 0.55]); });
      set(`lapf${k}`, "d", `M${up.map(P2).join("L")}L${dn.reverse().map(P2).join("L")}Z`);
    });
    // the crest: a ragged white band — torn points thrown up off its top, foam tongues hanging off its underside and dragged sideways —
    // in three tones, each with its own tear so they never stack into a contour
    const tA = [], tB = [], dA = [], dB = [];
    cols.forEach((c) => { tA.push(tearAt(S.tear, c.X, t)); tB.push(tearAt(S.tear, c.X + 0.31, t)); dA.push(tearAt(S.drip, c.X, t)); dB.push(tearAt(S.drip, c.X - 0.53, t)); });
    const crestLayer = (m, b, g, tp, dp, o) => {
      const top = [], bot = [];
      cols.forEach((c, i) => { const dy = Hp * ((0.035 + 0.05 * fbm(c.X * 1.2 + t * 0.3 + o)) * b + dp[i] * g); top.push([c.x, c.top - Hp * (0.012 * fbm(c.X * 3.1 + t + o) + tp[i] * m)]); bot.push([c.x + dy * 0.35, c.top + dy]); });
      return `M${top.map(P2).join("L")}L${bot.reverse().map(P2).join("L")}Z`;
    };
    set("cr0", "d", crestLayer(0.55, 1, 1, tB, dA, 0)); set("cr1", "d", crestLayer(0.8, 0.7, 0.55, tA, dB, 5)); set("cr2", "d", crestLayer(1, 0.38, 0.22, tA, dA, 11));
    set("veil", "d", `M${cols.map((c, i) => `${c.x},${f1(c.top - Hp * (0.03 + 0.07 * fbm(c.X * 0.9 - t * 0.6 + 3) + tA[i] * 0.9))}`).join("L")}L${X1},${f1(cols[cols.length - 1].top + Hp * 0.02)}L${X0},${f1(cols[0].top + Hp * 0.02)}Z`);
    let la = "";
    S.lace.forEach((q) => { const p = (q.ph + t * q.v) % 1, X = q.X + p * 0.8, len = q.len * px * Math.sin(Math.PI * p); if (len > 1) la += shardD(xs(X), hY(X, 0.86 - 0.24 * p), len, len * q.asp, q.a, q.j); });
    set("lace", "d", la);
    // the sheet of water racing ahead over the sand, frothing at its edge
    const dS = Math.max(WAV.D1 - 2, dW - 3.2), yS = HZ + hc * FX / dS, run = [];
    cols.forEach((c, i) => { if (i % 3 === 0) run.push([c.x, yS + (yS - base) * (0.25 * Math.sin(c.X * 1.1 + t * 2.3) + 0.15 * Math.sin(c.X * 2.9 - t * 3.1))]); });
    set("sheet", "d", `M${X0},${f1(base)}L${run.map(P2).join("L")}L${X1},${f1(base)}Z`);
    const froth = run.map(([x, y]) => [x, y - 2 - (yS - base) * 0.4 * pk(x * 0.05 + t * 3, 4)]);
    set("sheetF", "d", `M${run.map(([x, y]) => `${x},${f1(y + 2)}`).join("L")}L${froth.reverse().map(P2).join("L")}Z`);
    // the skirt: where the wall comes down on the sand it boils up white, torn sheets standing up out of it
    const sT = cols.map((c) => tearAt(S.stear, c.X, t)), sT2 = cols.map((c) => tearAt(S.stear, c.X + 0.41, t));
    const skirt = (h0, amp, m, tp, o, drop) => {
      const top = [], bot = [];
      cols.forEach((c, i) => { top.push([c.x, base - Hp * (h0 + amp * fbm(c.X * 1.3 + t * 0.7 + o) + tp[i] * m)]); bot.push([c.x, base + hc * px * drop / dW * (0.5 + fbm(c.X * 2.1 + o - t))]); });
      return `M${top.map(P2).join("L")}L${bot.reverse().map(P2).join("L")}Z`;
    };
    set("sk0", "d", skirt(0.08, 0.07, 0.9, sT, 3, 2)); set("sk1", "d", skirt(0.045, 0.06, 0.8, sT2, 7, 1.4)); set("sk2", "d", skirt(0.02, 0.05, 0.5, sT, 11, 0.7));
    // spray and torn sheets of water flung forward (true 3-D flight, projected): off the crest, off the skirt
      const sp = ["", "", ""], ts = ["", ""];
    const emit = (q, small) => {
      const tau = ((q.ph + t / q.life) % 1) * q.life, X = q.X + q.vx * tau, h = (crest(q.X) + spike(q.X) * 0.6) * Hm + q.vu * tau - 4.9 * tau * tau, d = dW - q.vf * tau;
      if (d < 1) return;
      const pxd = FX / d, x = CX + X * pxd, y = HZ + (hc - h) * pxd, kk = tau / q.life, op = Math.pow(1 - kk, 0.8) * sm(0, 0.08, kk);
      const vx = q.vx * pxd + X * FX * q.vf / (d * d), vy = -(q.vu - 9.8 * tau) * pxd + (hc - h) * FX * q.vf / (d * d), rr = Math.max(0.5, q.sz * pxd);
      sp[op > 0.6 ? 2 : op > 0.3 ? 1 : 0] += dropD(x, y, rr * (small ? 1.2 : 1.6 + Math.min(2.4, Math.hypot(vx, vy) / 900)), rr, Math.atan2(vy, vx));
    };
    S.drop.forEach((q) => emit(q, false)); S.mist.forEach((q) => emit(q, true));
    sp.forEach((d, k) => set(`sp${k}`, "d", d));
    S.sheet.forEach((q) => {
      const tau = ((q.ph + t / q.life) % 1) * q.life, d = dW - q.vf * tau, h = q.h0 + q.vu * tau - 4.9 * tau * tau, X = q.X + q.vx * tau;
      if (h < -0.1 || d < 1) return;
      const pxd = FX / d, x = CX + X * pxd, y = HZ + (hc - h) * pxd, fade = 1 - tau / q.life;
      const vx = q.vx * pxd + X * FX * q.vf / (d * d), vy = -(q.vu - 9.8 * tau) * pxd + (hc - h) * FX * q.vf / (d * d), len = q.sz * pxd * (0.4 + 0.6 * fade);
      ts[q.lt ? 1 : 0] += shardD(x, y, len, len * 0.26, Math.atan2(vy, vx), q.j);
    });
    ts.forEach((d, k) => set(`ts${k}`, "d", d));
    // the palms and shacks in its path: foam climbs them as it arrives, they shudder, and are gone when it passes
    S.ov.forEach((q, i) => {
      const gap = dW - q.d, vis = sm(0, 0.5, gap), pxd = FX / q.d;
      el(`${id}-ov${i}`).setAttribute("opacity", f1(vis));
      ["ovg", "ovm", "ovw", "ovs"].forEach((k) => set(`${k}${i}`, "opacity", f1(vis * (k === "ovs" ? 0.85 : 1))));
      const f = sm(2.8, 0.1, gap) * q.fmax, blast = sm(9, 0.5, gap), shud = f * 3 * Math.sin(t * 13 + i);
      set(`ovr${i}`, "transform", `translate(${q.x},${f1(q.G)}) rotate(${f1(shud + (q.palm ? blast * 3 * Math.sin(t * 1.7 + i) : 0))})`);
      if (q.palm) { const p = el(`${id}-ovp${i}`), [ox, oy] = p.getAttribute("data-o").split(" "); p.setAttribute("transform", `rotate(${f1((2 + 9 * blast) * Math.sin(t * 2.6 + i * 1.3))} ${ox} ${oy})`); }
      if (vis <= 0 || f < 0.01) { ["ovg", "ovm", "ovw", "ovs"].forEach((k) => set(`${k}${i}`, "d", "")); return; }
      // the water surging round it (the face's colour) with a torn white froth riding on top, spray thrown up where it hits
      const hw = (q.w / 2) * pxd * (0.8 + 0.5 * f), Hc = f * q.h * pxd, wt = [], mt = [], mb = [], ft = [], fb = [];
      for (let j = 0; j <= 26; j++) {
        const s = j / 26, x = q.x - hw + 2 * hw * s, env = Math.pow(Math.sin(Math.PI * s), 0.35), X = s * 7 + i * 3.1, yw = q.G - Hc * env * (0.7 + 0.4 * fbm(X + t * 1.5)), tear = Math.pow(fbm(X * 2.3 - t * 2.2 + 9), 3);
        wt.push([x, yw]); mt.push([x, yw - Hc * env * (0.07 + 0.55 * tear)]); mb.push([x + Hc * 0.1 * env, yw + Hc * env * (0.32 + 0.25 * fbm(X * 1.3 + t * 0.8 + 2))]);
        ft.push([x, yw - Hc * env * (0.03 + 0.42 * tear)]); fb.push([x + Hc * 0.14 * env, yw + Hc * env * (0.1 + 0.2 * fbm(X * 1.7 + t + 4))]);
      }
      set(`ovg${i}`, "d", `M${wt.map(P2).join("L")}L${f1(q.x + hw)},${f1(q.G + 3)}L${f1(q.x - hw)},${f1(q.G + 3)}Z`);
      set(`ovm${i}`, "d", `M${mt.map(P2).join("L")}L${mb.reverse().map(P2).join("L")}Z`);
      set(`ovw${i}`, "d", `M${ft.map(P2).join("L")}L${fb.reverse().map(P2).join("L")}Z`);
      let spl = "";
      for (let j = 0; j < 5; j++) { const ph = (t * 1.7 + j * 0.37 + i * 0.21) % 1, side = (j / 4 - 0.5) * 0.6, L2 = Hc * 0.5 * Math.sin(Math.PI * ph) + 1; spl += shardD(q.x + side * hw * (0.5 + 0.6 * ph), q.G - Hc * (0.8 + 0.8 * ph), L2, L2 * 0.16, -Math.PI / 2 + side * 1.1, [1, 0.5, 0.7, 0.45, 1, 0.5, 0.7, 0.45]); }
      set(`ovs${i}`, "d", spl);
    });
    // the runner: well ahead of the wall, angling left up the beach
    if (S.run) {
      const dR = 0.72 * dW + 0.8, Xr = 4.52 - 30.3 * (u - 0.765), pxr = FX / dR, fr = Math.floor(((t * 7) % 4 + 4) % 4);
      set("rn", "transform", `translate(${f1(CX + Xr * pxr)},${f1(HZ + hc * pxr)}) scale(${(pxr * 1.65 / 100).toFixed(4)})`);
      for (let i = 0; i < 4; i++) set(`rn${i}`, "opacity", i === fr ? 1 : 0);
    }
  }
  Tide.waveIn = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, u0 = o.from ?? 0, u1 = o.to ?? 1, birds = el(`${id}-birds`), scud = el(`${id}-scud`);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => {
      const k = c.t / dur, t = t0 + c.t;
      waveDraw(id, t, lerp(u0, u1, k));
      if (birds) birds.setAttribute("transform", `translate(${f1(-c.t * 120)},${f1(-c.t * 90)})`);
      if (scud) scud.setAttribute("transform", `translate(${f1(-c.t * 70)},0)`);
    } }, t0);
  };

  // ======================== on the evacuation path up the hill, looking down at the village and the bay ========================
  // The bay's level u: 0 the sea at the beach … 1 drawn back the first time … HILL.LMAX (1.7) the second time, far out to the karsts.
  // The bare seabed, its marks and two longtails are redrawn (hillSeaDraw). The flood (Tide.surge) is redrawn in the mid layer over the
  // village ground, under copies of the roofs and tree crowns (#id-above), with a band of water over the foot of everything standing in it.
  const HILL = { BY: 1040, GV: 1240, LMAX: 1.7 };
  const hillEdge = (HZ, u) => lerp(HILL.BY - 6, HILL.BY - (HILL.BY - HZ) * 0.42, u);
  // y at x on a quadratic Bézier from (x0, y0) via (cx, cy) to (x1, y1) whose x only grows
  const qAt = (x, x0, y0, cx, cy, x1, y1) => {
    const A = x0 - 2 * cx + x1, B = 2 * (cx - x0), C = x0 - x;
    const t = clamp(Math.abs(A) < 1e-6 ? -C / B : (-B + Math.sqrt(Math.max(0, B * B - 4 * A * C))) / (2 * A), 0, 1);
    return (1 - t) * (1 - t) * y0 + 2 * t * (1 - t) * cy + t * t * y1;
  };
  function tideHill(L, o) {
    const id = o.id || "th", P = PAL[o.time || "morning"], r = mk(o.seed || 13), r2 = mk((o.seed || 13) + 501), HZ = o.hz ?? 520;
    sky(L, id, P, HZ, { seed: (o.seed || 13) + 1 });
    // far: the bay from above — the sea to the horizon, the karsts, the curve of the beach; the seabed and two longtails (redrawn)
    const { BY, GV } = HILL, sea = o.sea || 0, EMAX = hillEdge(HZ, HILL.LMAX), dep = (y) => clamp((y - HZ) / (BY - HZ), 0.05, 1);
    let f = `<defs><linearGradient id="${id}-seaG" gradientUnits="userSpaceOnUse" x1="0" y1="${HZ}" x2="0" y2="${BY}"><stop offset="0" stop-color="${P.sea[0]}"/><stop offset=".1" stop-color="${P.sea[1]}"/><stop offset=".45" stop-color="${P.sea[2]}"/><stop offset=".8" stop-color="${P.sea[3]}"/><stop offset="1" stop-color="${P.sea[4]}"/></linearGradient>
      <linearGradient id="${id}-bedG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(EMAX)}" x2="0" y2="${BY}"><stop offset="0" stop-color="${T(P.bed[2], -0.14)}"/><stop offset=".5" stop-color="${P.bed[1]}"/><stop offset="1" stop-color="${mix(P.bed[0], P.sand[1], 0.25)}"/></linearGradient>
      <clipPath id="${id}-bedC"><path id="${id}-bedCP" d=""/></clipPath></defs>`;
    f += `<rect x="-3000" y="${HZ}" width="8000" height="${BY - HZ + 400}" fill="url(#${id}-seaG)"/>`;
    for (let k = 0; k < 90; k++) { const y = HZ + Math.pow(r(), 1.6) * (BY - HZ), x = -1000 + r() * 3100, len = 20 + (y - HZ) * 0.3 * r(); f += `<path d="M${f1(x)},${f1(y)}h${f1(len)}" stroke="#fff" stroke-width="${f1(1 + (y - HZ) / 300)}" opacity="${f1(0.2 + r() * 0.35)}" stroke-linecap="round"/>`; }
    // the white line far out (Tide.hillSea o.line): a dark face under a thin bright crest, spreading along the horizon behind the karsts
    f += `<g id="${id}-wl" opacity="0"><path id="${id}-wlA" d="" fill="#ffffff" opacity=".28"/><path id="${id}-wlD" d="" fill="${T(P.sea[2], -0.42)}" opacity=".8"/><path id="${id}-wlB" d="" fill="#ffffff"/></g>`;
    [[-280, 210, 210, 0.8], [250, 270, 300, 0.6], [800, 190, 200, 0.82], [1280, 250, 240, 0.7]].forEach(([x, wv, hv, v], k) => { f += karst(id, k, x, HZ + 4, wv, hv, r, P, v).g; });
    f += `<rect x="-3000" y="${HZ - 20}" width="8000" height="30" fill="${P.haze}" opacity=".5"/>`;
    // the bay stirred up while the surge comes in (Tide.surge): muddy toward the shore, lines of white water running in
    const WC = Array.from({ length: 30 }, (_, k) => ({ x: -500 + ((k + r2()) / 30) * 2200, p: r2(), v: 0.18 + r2() * 0.14, w: 60 + r2() * 160 }));
    f += `<g id="${id}-bay" opacity="0"><defs><linearGradient id="${id}-bayG" gradientUnits="userSpaceOnUse" x1="0" y1="${HZ + 120}" x2="0" y2="${BY + 10}"><stop offset="0" stop-color="#6e7a62" stop-opacity="0"/><stop offset=".55" stop-color="#6e7a62" stop-opacity=".55"/><stop offset="1" stop-color="#7a7254" stop-opacity=".9"/></linearGradient></defs><rect x="-3000" y="${HZ + 120}" width="8000" height="${BY - HZ}" fill="url(#${id}-bayG)"/>${WC.map((_, k) => `<path id="${id}-wc${k}" d="" stroke="#ffffff" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
    // the seabed laid bare between the beach and the drawn-back water: fixed marks over the whole band it can reach, shown by the clip
    let bc = "";
    for (let k = 0; k < 40; k++) { const y = EMAX + r() * (BY - EMAX), x = -800 + r() * 2700, w = 30 + r() * 120; bc += `<path d="M${f1(x)},${f1(y)}h${f1(w * dep(y))}" stroke="${T(P.bed[2], -0.2)}" stroke-width="${f1(0.8 + 1.6 * dep(y))}" opacity=".5"/>`; }
    for (let k = 0; k < 14; k++) { const cx = -600 + r() * 2300, cy = EMAX + r() * (BY - EMAX), rx = 20 + r() * 60, ry = 4 + r() * 8; bc += `<ellipse cx="${f1(cx)}" cy="${f1(cy)}" rx="${f1(rx * (0.4 + 0.6 * dep(cy)))}" ry="${f1(ry * (0.4 + 0.6 * dep(cy)))}" fill="${P.sky[2]}" opacity=".8"/>`; }
    // (the marks below draw on their own seed, so the village keeps its layout) reef heads and rocks, more of them far out; pools that mirror the sky
    for (let k = 0; k < 34; k++) { const y = EMAX + Math.pow(r2(), 1.5) * (BY - EMAX - 20), x = -700 + r2() * 2500, w = (10 + r2() * 26) * (0.35 + dep(y)); bc += `<ellipse cx="${f1(x + w * 0.2)}" cy="${f1(y + w * 0.12)}" rx="${f1(w)}" ry="${f1(w * 0.3)}" fill="${T(P.bed[2], -0.45)}" opacity=".45"/><ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w)}" ry="${f1(w * 0.34)}" fill="${T(P.bed[2], -0.3)}"/><ellipse cx="${f1(x - w * 0.18)}" cy="${f1(y - w * 0.1)}" rx="${f1(w * 0.55)}" ry="${f1(w * 0.15)}" fill="${T(P.bed[1], 0.18)}" opacity=".7"/>`; }
    for (let k = 0; k < 12; k++) { const y = EMAX + 14 + r2() * (BY - EMAX - 60), x = -500 + r2() * 2100, w = (24 + r2() * 60) * (0.3 + dep(y)); bc += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w)}" ry="${f1(w * 0.13)}" fill="${P.sky[2]}" opacity=".75"/><path d="M${f1(x - w * 0.5)},${f1(y - w * 0.03)}h${f1(w * 0.45)}" stroke="#fff" stroke-width="${f1(0.8 + dep(y))}" opacity=".7" stroke-linecap="round"/>`; }
    for (let k = 0; k < 18; k++) { const y = EMAX + r2() * (BY - EMAX), x = -600 + r2() * 2300, w = (16 + r2() * 30) * dep(y); bc += `<path d="M${f1(x)},${f1(y)}q${f1(w * 0.5)},${f1(-w * 0.12)} ${f1(w)},0" stroke="#5e6a32" stroke-width="${f1(0.8 + dep(y))}" fill="none" opacity=".7"/>`; }
    let rb = "";
    // sand ripples left by the water: broken wavy bands in perspective, a dark trough and a lit crest
    for (let k = 0; k < 26; k++) {
      const e = lerp(EMAX + 6, BY - 4, Math.pow((k + 0.3 + 0.5 * r2()) / 26, 1.25)), d0 = dep(e), ph = r2() * 9, x0 = -900 + r2() * 600, len = 900 + r2() * 1600, amp = 1.5 + 4 * d0;
      let d = ""; for (let x = x0; x <= x0 + len; x += 40) d += `${d ? "L" : "M"}${x},${f1(e + qAt(x, -3000, 0, 540, -30, 4000, 10) + amp * Math.sin(x * 0.011 + ph) + amp * 0.6 * Math.sin(x * 0.031 + ph * 2))}`;
      rb += `<path d="${d}" stroke="${T(P.bed[2], -0.28)}" stroke-width="${f1(0.8 + 3 * d0)}" fill="none" opacity=".3"/><path d="${d}" stroke="${T(P.bed[0], 0.3)}" stroke-width="${f1(0.6 + 2 * d0)}" fill="none" opacity=".3" transform="translate(0,${f1(-1 - 2 * d0)})"/>`;
    }
    for (let k = 0; k < 36; k++) { const y = EMAX + 8 + Math.pow(r2(), 1.2) * (BY - EMAX - 30), x = -400 + r2() * 1900, w = (4 + r2() * 5) * (0.4 + dep(y)); rb += `<path d="M${f1(x)},${f1(y)}h${f1(w)}" stroke="${r2() < 0.5 ? "#e8f2f4" : "#b8c8d0"}" stroke-width="${f1(1 + dep(y))}" stroke-linecap="round"/>`; }
    f += `<path id="${id}-bed" d="" fill="url(#${id}-bedG)"/><g clip-path="url(#${id}-bedC)">${rb}${bc}<path id="${id}-bedW2" d="" fill="${P.sky[2]}" opacity=".16"/><path id="${id}-bedW" d="" fill="${P.sky[2]}" opacity=".34"/></g>`;
    f += `<path id="${id}-bedE" d="" stroke="#ffffff" stroke-width="4" fill="none" opacity=".8" stroke-linecap="round"/>`;
    // two longtails out on the bay: afloat they bob, left on the mud they lie over on their keels
    const HB = [{ x: 210, y: 936, s: 0.056, flip: false, hull: "#2f6fa0", band: "#d8423a", ph: 0.7 }, { x: 985, y: 864, s: 0.046, flip: true, hull: "#2e8a5a", band: "#f2c02a", ph: 2.6 }];
    HB.forEach((b, k) => { f += `<g id="${id}-hb${k}"><ellipse id="${id}-hb${k}-s" cx="0" cy="40" rx="560" ry="46" fill="#2a2418" opacity="0"/>${Tide.longtail({ hull: b.hull, band: b.band, no: false, flip: b.flip, water: P.sea[3], wid: `${id}-hb${k}-w`, seed: 41 + k, k: 7 + k })}</g>`; });
    // the beach: a pale curve of sand with the swash
    f += `<path d="M-3000,${BY}Q540,${BY - 40} 4000,${BY + 20}V${BY + 420}H-3000Z" fill="${P.sand[1]}"/><path id="${id}-fwb" d="M-3000,${BY}Q540,${BY - 40} 4000,${BY + 20}V${BY + 120}Q540,${BY + 60} -3000,${BY + 110}Z" fill="#5a4a32" opacity="0"/><path id="${id}-swh" d="M-3000,${BY}Q540,${BY - 40} 4000,${BY + 20}" stroke="#fff" stroke-width="5" fill="none" opacity="${sea > 0 ? 0.2 : 0.85}"/>`;
    put(L.far, f);
    // mid: the village from above — roofs, the hotel beside ยาย's shop, palms, the tower
    const gTop = (x) => qAt(x, -3000, BY + 70, 540, BY + 30, 4000, BY + 90);
    let m = `<path d="M-3000,${BY + 70}Q540,${BY + 30} 4000,${BY + 90}V${GV + 300}H-3000Z" fill="${mix(P.green[1], P.sand[1], 0.35)}"/>`;
    m += `<path d="M-3000,${GV - 70}Q540,${GV - 110} 4000,${GV - 60}" stroke="#b8b0a0" stroke-width="22" fill="none"/>`;
    const HU = [], CR = [];
    for (let k = 0; k < 18; k++) {
      const x = -900 + k * 200 + r() * 80, y = BY + 110 + r() * 120, w = 70 + r() * 70;
      const roof = `<path d="M${f1(-w / 2)},0L${f1(-w / 2 + 12)},-30H${f1(w / 2 - 12)}L${f1(w / 2)},0Z" fill="${r() < 0.5 ? "url(#tdTin)" : "url(#tdTile)"}" ${OUT2}/>`;
      m += `<g transform="translate(${f1(x)},${f1(y)})">${roof}<path d="M${f1(-w / 2)},0H${f1(w / 2)}V18H${f1(-w / 2)}Z" fill="#e8dcc4" ${OUT2}/></g>`;
      HU.push(`<g transform="translate(${f1(x)},${f1(y)})">${roof}</g>`);
    }
    for (let k = 0; k < 22; k++) { const c = crown(-900 + r() * 2900, BY + 90 + r() * 200, 22 + r() * 18, r, [P.green[0], P.green[1], P.green[2], P.green[2]], 6); m += c; CR.push(c); }
    // the flood (Tide.surge): the wet ground it leaves behind, the moving water, the roofs and crowns again on top of it
    const FM = (x) => 1306 + 34 * (fbm(x * 0.004 + 7.3) - 0.5);
    m += `<defs><linearGradient id="${id}-fG" gradientUnits="userSpaceOnUse" x1="0" y1="${BY - 44}" x2="0" y2="1330"><stop offset="0" stop-color="${mix(P.sea[4], "#5a6450", 0.6)}" stop-opacity="0"/><stop offset=".1" stop-color="${mix(P.sea[3], "#565c48", 0.65)}"/><stop offset=".34" stop-color="#5e5a40"/><stop offset=".7" stop-color="#6c6244"/><stop offset="1" stop-color="#7a6c48"/></linearGradient>
      <clipPath id="${id}-fC"><path id="${id}-fCP" d=""/></clipPath><clipPath id="${id}-fwC"><path id="${id}-fwCP" d=""/></clipPath></defs>`;
    let wet = `<rect x="-1400" y="${BY - 60}" width="4000" height="420" fill="#3e3424" opacity=".55"/>`;
    wet += `<path d="${Array.from({ length: 150 }, (_, i) => { const x = -1300 + i * 25; return `${i ? "L" : "M"}${x},${f1(FM(x) - 2)}`; }).join("")}" stroke="#3a3024" stroke-width="4" fill="none" stroke-dasharray="7 4 16 6 4 5" opacity=".75"/>`;
    for (let k = 0; k < 26; k++) { const x = -200 + r2() * 1500, y = FM(x) - 4 - r2() * 60, a = r2() * 180, c = ["#8a6a44", "#5a4632", "#e8e2d4", "#d84a36", "#2a8ad0"][k % 5]; wet += `<rect x="${f1(x - 6)}" y="${f1(y - 1.5)}" width="${f1(8 + r2() * 10)}" height="3" rx="1" fill="${c}" transform="rotate(${f1(a)} ${f1(x)} ${f1(y)})" opacity=".85"/>`; }
    for (let k = 0; k < 10; k++) { const x = -200 + r2() * 1500, y = BY + 90 + r2() * 180, w = 14 + r2() * 26; wet += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w)}" ry="${f1(w * 0.18)}" fill="${P.sky[2]}" opacity=".7"/><path d="M${f1(x - w * 0.6)},${f1(y - w * 0.04)}h${f1(w * 0.5)}" stroke="#fff" stroke-width="1.6" opacity=".7"/>`; }
    m += `<g id="${id}-fwet" opacity="0" clip-path="url(#${id}-fwC)">${wet}</g>`;
    let tx = `<path d="M-1300,${BY + 64}Q540,${BY + 40} 2400,${BY + 30}V${BY + 74}Q540,${BY + 86} -1300,${BY + 112}Z" fill="#dfe8e0" opacity=".16"/><path d="M-1300,${BY + 150}Q540,${BY + 128} 2400,${BY + 118}V${BY + 140}Q540,${BY + 152} -1300,${BY + 172}Z" fill="#dfe8e0" opacity=".1"/>`;
    for (let k = 0; k < 50; k++) { const x = -300 + r2() * 1700, y = BY + 20 + r2() * 280, w = (12 + r2() * 40) * (0.5 + 0.5 * dep(y)); tx += `<path d="M${f1(x)},${f1(y)}q${f1(w / 2)},${f1(-3 - r2() * 4)} ${f1(w)},0" stroke="#eef0e2" stroke-width="2" fill="none" opacity="${f1(0.14 + r2() * 0.2)}"/>`; }
    const FS = Array.from({ length: 44 }, (_, k) => ({ x: -200 + ((k + r2()) / 44) * 1500, p: r2(), v: 0.28 + r2() * 0.22, w: 30 + r2() * 70, sw: 2 + r2() * 3 }));
    tx += FS.map((q, k) => `<path id="${id}-fs${k}" d="" stroke="#f6f4ea" stroke-width="${f1(q.sw)}" fill="none" stroke-linecap="round" opacity="0"/>`).join("");
    const FP = Array.from({ length: 26 }, (_, k) => ({ x: -150 + ((k + r2()) / 26) * 1400, p: r2(), v: 0.2 + r2() * 0.16, R: 14 + r2() * 22, d: blob(0, 0, 10, r2, 7) }));
    tx += FP.map((q, k) => `<path id="${id}-fp${k}" d="${q.d}" fill="#f4f2e8" opacity="0"/>`).join("");
    let fl = `<path id="${id}-fS" d="" fill="url(#${id}-fG)"/><g clip-path="url(#${id}-fC)">${tx}</g>`;
    // white water churning over the crest of the beach, and bores (torn white bands) running in across the flood toward us
    fl += `<g id="${id}-pour" opacity="0"><path id="${id}-crB" d="" fill="#ffffff" opacity=".35"/><path id="${id}-crA" d="" fill="#ffffff" opacity=".85"/></g>`;
    fl += `<g clip-path="url(#${id}-fC)">${[0, 1, 2, 3].map((k) => `<path id="${id}-bo${k}" d="" fill="#f4f2e8" opacity="0"/>`).join("")}</g>`;
    fl += `<path id="${id}-fFd" d="" stroke="#3e3626" stroke-width="18" fill="none" opacity=".3"/><path id="${id}-fF2" d="" stroke="#ffffff" stroke-width="24" fill="none" opacity=".42" stroke-linecap="round"/><path id="${id}-fF1" d="" stroke="#ffffff" stroke-width="7" fill="none" opacity=".95" stroke-linecap="round" stroke-dasharray="46 7 20 6 64 9"/>`;
    const FC = Array.from({ length: 40 }, (_, k) => ({ x: -250 + ((k + r2()) / 40) * 1600, R: 5 + r2() * 9, ph: r2() * 6 }));
    fl += FC.map((_, k) => `<circle id="${id}-fc${k}" r="1" fill="#ffffff" opacity="0"/>`).join("");
    // things it carries: a plank, a cooler, a red plastic chair, a striped beach umbrella
    const DB = [{ x: 300, a: 0.62, ph: 0.4, r0: 20 }, { x: 600, a: 0.78, ph: 2.1, r0: -10 }, { x: 860, a: 0.55, ph: 3.7, r0: 35 }, { x: 1080, a: 0.7, ph: 5.2, r0: -25 }, { x: 160, a: 0.45, ph: 1.3, r0: 60 }, { x: 960, a: 0.36, ph: 4.4, r0: -40 }];
    const dbArt = [`<rect x="-15" y="-2.6" width="30" height="5.2" rx="1.2" fill="#a07a50" stroke="${INK}" stroke-width="1.2"/>`,
      `<rect x="-7" y="-4.6" width="14" height="9.2" rx="1.6" fill="#f4f6f4" stroke="${INK}" stroke-width="1.2"/><rect x="-7" y="-4.6" width="14" height="3" rx="1.2" fill="#2a8ad0"/>`,
      `<path d="M-6,4V-6H6V4M-6,-1H6" stroke="#d8402e" stroke-width="2.6" fill="none"/>`,
      `<path d="M-12,0A12,7 0 0 1 12,0Z" fill="#f2f0e8" stroke="${INK}" stroke-width="1.1"/><path d="M-12,0A12,7 0 0 1 -4,-6.4L0,0ZM4,-6.4A12,7 0 0 1 12,0L0,0Z" fill="#e84a3a"/>`,
      `<rect x="-6" y="-8" width="12" height="16" rx="3" fill="#2a6ab8" stroke="${INK}" stroke-width="1.2"/><path d="M-6,-3H6M-6,3H6" stroke="#1a4a8a" stroke-width="1.2"/>`,
      `<path d="M-18,2Q0,-6 18,0" stroke="#5a7a3a" stroke-width="3" fill="none"/><path d="M-14,0l-3,6M-8,-2l-2,7M-2,-3l-1,7M4,-3l1,7M10,-2l2,6" stroke="#6a8a44" stroke-width="2"/>`];
    fl += DB.map((b, k) => `<g id="${id}-fd${k}" opacity="0"><g transform="scale(1.7)">${dbArt[k]}</g></g>`).join("");
    m += `<g id="${id}-flood" opacity="0">${fl}</g><g id="${id}-above" opacity="0">${HU.join("")}${CR.join("")}</g>`;
    // the hotel seen from above: its roof with the railing, the five storeys foreshortened; the shop's blue awning beside it. Each thing that
    // stands in the flood gets a band of water over its foot (#id-fb0 …), drawn right after it so whatever stands in front still covers it.
    const SD = [], band = (k) => `<g id="${id}-fb${k}" opacity="0"><path id="${id}-fb${k}w" d="" fill="url(#${id}-fG)"/><path id="${id}-fb${k}k" d="" stroke="#ffffff" stroke-width="2.2" fill="none" opacity=".7" stroke-linecap="round" stroke-dasharray="9 5"/><path id="${id}-fb${k}f" d="" stroke="#ffffff" stroke-width="3.2" fill="none" opacity=".95" stroke-linecap="round"/><g id="${id}-fb${k}s" fill="#ffffff">${[0, 1, 2, 3, 4, 5].map((i) => `<circle id="${id}-fb${k}s${i}" r="1" opacity="0"/>`).join("")}</g></g>`;
    m += `<g transform="translate(560,${BY + 236}) scale(.36)"><path d="M-288,-554H168L196,-640H-262Z" fill="#e2dccf" ${OUT2}/><path d="M-262,-640H196" stroke="#a8aeb0" stroke-width="6"/>${hotel(id, 0, 0, 1)}</g>` + band(0);
    SD.push([432, 663, BY + 236, 30]);
    m += `<g transform="translate(760,${BY + 250}) scale(.34)">${shop(id + "s", 0, 0, 1, r)}</g>` + band(1);
    SD.push([652, 868, BY + 250, 32]);
    for (let k = 0; k < 7; k++) {
      const cx = -500 + k * 300 + r() * 120, cy = BY + 240 + r() * 40, cs = 0.42 + r() * 0.1, cl = (r() - 0.5) * 0.4;
      m += coco(cx, cy, cs, cl, (o.seed || 13) + 80 + k, { q: 0.5, pal: P.leaf }) + band(2 + k);
      SD.push([cx - 36 * cs, cx + 36 * cs, cy, 20]);
    }
    m += Tide.tower(330, GV + 30, 0.62, id) + band(9);
    SD.push([300, 360, GV + 30, 22]);
    m += flagPole(id, 488, BY + 0, 120, 0.36);
    put(L.mid, m);
    // set: the hillside jungle either side, the concrete steps coming down toward the village, the steel handrail, the sign
    let s = "";
    const steps = 26, near = 1990, farY = 1230;
    const yK = (k) => farY + (near - farY) * Math.pow(k / steps, 1.7), wK = (k) => lerp(120, 760, Math.pow(k / steps, 1.7)), cxK = (k) => lerp(560, 470, Math.pow(k / steps, 1.2));
    // jungle masses either side, lit from the right
    for (let k = 0; k < 70; k++) { const side = k % 2 ? 1 : -1, y = 1150 + r() * 950, x = side < 0 ? -200 + r() * (cxK(clamp(steps * (y - farY) / (near - farY), 0, steps)) - 250 + 200) : 760 + r() * 700, R = 70 + r() * 110 * ((y - 1100) / 900 + 0.4); s += crown(x, y, R, r, [T(P.green[0], -0.1), P.green[1], P.green[2], T(P.green[2], 0.2)], 9); }
    // the steps: a concrete flight narrowing away, each tread lit on top with a dark riser
    let tr = "";
    for (let k = steps; k >= 1; k--) {
      const y0 = yK(k - 1), y1 = yK(k), w0 = wK(k - 1), w1 = wK(k), c0 = cxK(k - 1), c1 = cxK(k), hR = (y1 - y0) * 0.38;
      tr += `<path d="M${f1(c0 - w0 / 2)},${f1(y0)}H${f1(c0 + w0 / 2)}L${f1(c1 + w1 / 2)},${f1(y1 - hR)}H${f1(c1 - w1 / 2)}Z" fill="url(#tdStep)"/>`;
      tr += `<path d="M${f1(c1 - w1 / 2)},${f1(y1 - hR)}H${f1(c1 + w1 / 2)}V${f1(y1)}H${f1(c1 - w1 / 2)}Z" fill="#8e877a"/><path d="M${f1(c1 - w1 / 2)},${f1(y1 - hR)}H${f1(c1 + w1 / 2)}" stroke="#f4f0e8" stroke-width="${f1(clamp(w1 * 0.006, 1, 4))}"/>`;
    }
    s += `<path d="M${f1(cxK(0) - wK(0) / 2 - 20)},${f1(yK(0))}L${f1(cxK(steps) - wK(steps) / 2 - 80)},${f1(near)}H${f1(cxK(steps) + wK(steps) / 2 + 80)}L${f1(cxK(0) + wK(0) / 2 + 20)},${f1(yK(0))}Z" fill="#6e6a5c"/>` + tr;
    // the steel handrail on the right: posts at every other step and a top rail
    let rail = "", top = [];
    for (let k = 0; k <= steps; k += 2) { const x = cxK(k) + wK(k) / 2 + wK(k) * 0.06, y = yK(k), h = wK(k) * 0.42; rail += `<path d="M${f1(x)},${f1(y)}V${f1(y - h)}" stroke="#a8b0b4" stroke-width="${f1(clamp(wK(k) * 0.016, 1.5, 12))}" stroke-linecap="round"/>`; top.push([x, y - h]); }
    s += rail + `<path d="M${top.map(P2).join("L")}" stroke="#d8dee0" stroke-width="${f1(10)}" fill="none" stroke-linecap="round"/><path d="M${top.map(P2).join("L")}" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/>`;
    s += Tide.evacSign(170, 1880, 1.0, { id: `${id}-sign`, dir: 0 });
    put(L.set, s);
    put(L.fg, `<g transform="translate(1180,-80) rotate(-30)">${coco(0, 0, 1.3, 0, 91, { trunk: false, pal: [T(P.leaf[0], -0.3), T(P.leaf[1], -0.2), P.leaf[1]] })}</g>`);
    ST[id] = { kind: "hill", P, HZ, flag: { px: 488, py: BY, s: 0.36 }, lvl: sea, line: o.line || 0, HB, SD, FS, FP, FC, DB, WC, FM, gTop, eOff: (x) => qAt(x, -3000, 0, 540, -30, 4000, 10) };
    landDraw(id, 0);
    hillSeaDraw(id, 0, sea, o.line || 0, 0);
    floodDraw(id, 0, 0, 0, 0, 1);
  }
  // redraw the bay: level u (0 … HILL.LMAX), the white line w (0 … 1), bore 0 … 1 (the sea running back in over the seabed, its edge churned white)
  function hillSeaDraw(id, t, u, w = 0, bore = 0, agi = 0) {
    const S = ST[id], { HZ } = S, BY = HILL.BY, e = hillEdge(HZ, u), shown = u > 0.004;
    const pts = [];
    for (let x = -1300; x <= 2400; x += 30) pts.push([x, e + S.eOff(x) + (2 + 8 * bore) * Math.sin(x * 0.011 + t * (1.3 + 5 * bore)) + (1.2 + 5 * bore) * Math.sin(x * 0.031 - t * 2.3)]);
    const top = `M${pts.map(P2).join("L")}`, bed = shown ? `${top}L2400,${BY + 60}L-1300,${BY + 60}Z` : "";
    el(`${id}-bed`).setAttribute("d", bed);
    el(`${id}-bedCP`).setAttribute("d", bed);
    el(`${id}-bedW`).setAttribute("d", shown ? `${top}L${pts.slice().reverse().map(([x, y]) => P2([x, y + 4 + 0.05 * (y - HZ)])).join("L")}Z` : "");
    el(`${id}-bedW2`).setAttribute("d", shown ? `${top}L${pts.slice().reverse().map(([x, y]) => P2([x, y + 10 + 0.16 * (y - HZ)])).join("L")}Z` : "");
    // the bay stirred up by the surge: whitecaps running in toward the beach, muddy water near the shore
    const bay = el(`${id}-bay`);
    bay.setAttribute("opacity", f1(clamp(agi, 0, 1)));
    if (agi > 0.01) S.WC.forEach((c, k) => {
      const q = (c.p + t * c.v) % 1, y = lerp(HZ + 60, BY - 8, Math.pow(q, 0.8)), d0 = clamp((y - HZ) / (BY - HZ), 0.05, 1), w2 = c.w * (0.3 + d0), x = c.x + 30 * Math.sin(q * 5 + k), e = el(`${id}-wc${k}`);
      e.setAttribute("d", `M${f1(x - w2 / 2)},${f1(y)}q${f1(w2 / 2)},${f1(-3 - 5 * d0)} ${f1(w2)},0`);
      e.setAttribute("stroke-width", f1(1.2 + 4 * d0));
      e.setAttribute("opacity", f1(0.85 * Math.sin(Math.PI * q)));
    });
    const E = el(`${id}-bedE`);
    E.setAttribute("d", shown ? top : "");
    E.setAttribute("stroke-width", f1(2.5 + 9 * bore));
    E.setAttribute("opacity", f1(0.7 + 0.25 * bore));
    el(`${id}-swh`).setAttribute("opacity", f1(lerp(0.85, 0.2, sm(0, 0.06, u))));
    // the longtails: afloat they bob; left on the mud they lie over on their keels
    S.HB.forEach((b, k) => {
      const ey = e + S.eOff(b.x), g = 1 - sm(b.y - 6, b.y + 10, ey);
      const bob = (1 - g) * 1.2 * Math.sin(t * 1.6 + b.ph), roll = (1 - g) * 2 * Math.sin(t * 1.1 + b.ph) + g * (k ? -10 : 12);
      el(`${id}-hb${k}`).setAttribute("transform", `translate(${f1(b.x)},${f1(b.y + bob + g * 1.5)}) rotate(${f1(roll)}) scale(${b.s})`);
      el(`${id}-hb${k}-w`).setAttribute("opacity", f1(1 - g));
      el(`${id}-hb${k}-s`).setAttribute("opacity", f1(0.35 * g));
    });
    // the white line: a crest spreading out from the middle of the bay, a dark face under it, a soft glow
    const wl = el(`${id}-wl`), q = clamp(w, 0, 1);
    wl.setAttribute("opacity", f1(sm(0, 0.12, q) * (0.88 + 0.12 * Math.sin(t * 7))));
    if (q > 0) {
      const half = 90 + 1300 * Math.pow(q, 1.2), cx = 560, y0 = HZ + 9;
      const band = (th, dy) => { const up = [], dn = []; for (let x = cx - half; x <= cx + half + 1; x += 20) { const v = (x - cx) / half, tw = th * Math.pow(Math.max(0, 1 - v * v), 0.6), yy = y0 + dy + 0.8 * Math.sin(x * 0.04 + t * 2.4); up.push([x, yy - tw / 2]); dn.push([x, yy + tw / 2]); } return `M${up.map(P2).join("L")}L${dn.reverse().map(P2).join("L")}Z`; };
      el(`${id}-wlA`).setAttribute("d", band(14 + 14 * q, -1));
      el(`${id}-wlD`).setAttribute("d", band(4 + 7 * q, 3 + 3 * q));
      el(`${id}-wlB`).setAttribute("d", band(2.6 + 3.6 * q, -0.8));
    }
  }
  // redraw the flood over the village: K 0 … 1 how far in it has run and how deep, Km the furthest it has reached (the ground stays wet
  // up to there), F the flow clock (seconds of flow, run backwards while it drains), dir +1 running inland … −1 back out to sea
  function floodDraw(id, t, K, Km, F, dir) {
    const S = ST[id], BY = HILL.BY, on = K > 0.002, xs = [];
    for (let x = -1300; x <= 2400; x += 25) xs.push(x);
    el(`${id}-flood`).setAttribute("opacity", f1(sm(0, 0.04, K)));
    el(`${id}-above`).setAttribute("opacity", on ? "1" : "0");
    el(`${id}-fwet`).setAttribute("opacity", Km > 0.002 ? "1" : "0");
    el(`${id}-fwb`).setAttribute("opacity", f1(0.42 * sm(0, 0.3, Km)));
    el(`${id}-fwCP`).setAttribute("d", Km > 0.002 ? `M-1300,${BY - 60}H2400L${xs.slice().reverse().map((x) => P2([x, lerp(BY + 34, S.FM(x) + 4, Km)])).join("L")}Z` : "");
    if (!on) { S.SD.forEach((_, k) => el(`${id}-fb${k}`).setAttribute("opacity", "0")); return; }
    const yF = (x) => lerp(BY + 34, S.FM(x), K) + 3 * Math.sin(x * 0.023 + t * 4.2) + 2 * Math.sin(x * 0.061 - t * 6.1);
    const front = xs.map((x) => [x, yF(x)]), d = `M-1300,${BY - 44}H2400L${front.slice().reverse().map(P2).join("L")}Z`, fl = `M${front.map(P2).join("L")}`;
    el(`${id}-fS`).setAttribute("d", d);
    const pr = sm(0.05, 0.4, K) * clamp(dir + 0.3, 0, 1);
    el(`${id}-pour`).setAttribute("opacity", f1(pr));
    const crY = (x) => qAt(x, -1300, BY + 36, 540, BY + 6, 2400, BY + 50), torn = (y0, th, ph) => {
      const up = [], dn = [];
      for (let x = -1300; x <= 2400; x += 20) { const c = y0(x); up.push([x, c - th * (0.4 + fbm(x * 0.021 + ph + t * 1.7))]); dn.push([x, c + th * (0.3 + fbm(x * 0.017 - ph - t * 1.3))]); }
      return `M${up.map(P2).join("L")}L${dn.reverse().map(P2).join("L")}Z`;
    };
    if (pr > 0.01) { el(`${id}-crA`).setAttribute("d", torn(crY, 9, 0)); el(`${id}-crB`).setAttribute("d", torn(crY, 22, 3)); }
    [0, 1, 2, 3].forEach((k) => {
      const q = (((k * 0.27 + F * 0.22) % 1) + 1) % 1, e = el(`${id}-bo${k}`), y0 = (x) => lerp(crY(x) + 14, yF(x) - 4, q);
      e.setAttribute("d", torn(y0, 3 + 7 * q, k * 2.1));
      e.setAttribute("opacity", f1(0.75 * Math.sin(Math.PI * q) * sm(0.2, 0.6, K) * clamp(dir + 0.4, 0, 1)));
    });
    el(`${id}-fCP`).setAttribute("d", d);
    el(`${id}-fF1`).setAttribute("d", fl);
    el(`${id}-fF1`).setAttribute("stroke-dashoffset", f1(-F * 34));
    el(`${id}-fF2`).setAttribute("d", fl);
    el(`${id}-fFd`).setAttribute("d", `M${front.map(([x, y]) => P2([x, y - 10])).join("L")}`);
    // the flow streaks ride from the beach to the front (and back again while it drains)
    S.FS.forEach((s, k) => {
      const q = (((s.p + s.v * F) % 1) + 1) % 1, x = s.x + 16 * Math.sin(q * 6 + k), y0 = BY + 16, y1 = yF(x) - 8, e = el(`${id}-fs${k}`);
      if (y1 < y0 + 12) { e.setAttribute("opacity", "0"); return; }
      const y = lerp(y0, y1, q), w = s.w * (0.55 + 0.45 * q);
      e.setAttribute("d", `M${f1(x - w / 2)},${f1(y)}q${f1(w / 2)},${f1(-2.5 - 3 * q)} ${f1(w)},0`);
      e.setAttribute("opacity", f1(0.8 * Math.sin(Math.PI * q)));
    });
    S.FP.forEach((s0, k) => {
      const q = (((s0.p + s0.v * F) % 1) + 1) % 1, x = s0.x + 20 * Math.sin(q * 4 + k), y = lerp(BY + 20, yF(x) - 10, q), e = el(`${id}-fp${k}`), R = s0.R * (0.6 + 0.6 * q);
      e.setAttribute("transform", `translate(${f1(x)},${f1(y)}) scale(${(R / 10).toFixed(2)},${(R * 0.036).toFixed(3)}) rotate(${f1(t * 20 + k * 40)})`);
      e.setAttribute("opacity", f1(0.55 * Math.sin(Math.PI * q) * sm(0.2, 0.6, K)));
    });
    S.FC.forEach((c, k) => {
      const x = c.x + 8 * Math.sin(t * 3 + c.ph), y = yF(x) - 4 - 6 * Math.abs(Math.sin(t * 5 + c.ph)), e = el(`${id}-fc${k}`);
      e.setAttribute("cx", f1(x)); e.setAttribute("cy", f1(y)); e.setAttribute("r", f1(c.R * (0.7 + 0.3 * Math.sin(t * 7 + c.ph))));
      e.setAttribute("opacity", f1(0.85 * sm(0.05, 0.3, K)));
    });
    S.DB.forEach((b, k) => {
      const x = b.x + 26 * Math.sin(t * 0.55 + b.ph) + 6 * F * Math.sin(b.ph), y = lerp(BY + 40, yF(b.x) - 16, b.a) + 2 * Math.sin(t * 2.1 + b.ph), e = el(`${id}-fd${k}`);
      e.setAttribute("transform", `translate(${f1(x)},${f1(y)}) rotate(${f1(b.r0 + 20 * Math.sin(t * 0.8 + b.ph))})`);
      e.setAttribute("opacity", f1(sm(0.12, 0.35, K)));
    });
    // the water round the foot of the hotel, the shop, the palms and the tower: a band up to the waterline, a foam line, a wake downstream
    S.SD.forEach(([x0, x1, yb, D], k) => {
      const dpt = D * K * sm(yb - 16, yb + 4, yF((x0 + x1) / 2)), g = el(`${id}-fb${k}`);
      g.setAttribute("opacity", dpt > 0.6 ? "1" : "0");
      if (dpt <= 0.6) return;
      const pts = [], n = Math.max(4, Math.round((x1 - x0) / 8));
      for (let i = 0; i <= n; i++) { const x = x0 - 4 + ((x1 - x0 + 8) * i) / n; pts.push([x, yb - dpt + 1.6 * Math.sin(x * 0.2 + t * 5 + k)]); }
      const tp = `M${pts.map(P2).join("L")}`;
      el(`${id}-fb${k}w`).setAttribute("d", `${tp}L${f1(x1 + 4)},${f1(yb + 5)}L${f1(x0 - 4)},${f1(yb + 5)}Z`);
      el(`${id}-fb${k}f`).setAttribute("d", tp);
      const wl = 8 + dpt * 1.1, wk = el(`${id}-fb${k}k`);
      wk.setAttribute("d", `M${f1(x0 - 2)},${f1(yb + 2)}q${f1(-wl * 0.3)},${f1(wl * 0.5)} ${f1(-wl * 0.8)},${f1(wl)}M${f1(x1 + 2)},${f1(yb + 2)}q${f1(wl * 0.3)},${f1(wl * 0.5)} ${f1(wl * 0.8)},${f1(wl)}`);
      wk.setAttribute("stroke-dashoffset", f1(-F * 40));
      wk.setAttribute("opacity", f1(0.75 * clamp(dir, 0, 1)));
      // spray thrown up round the corners of the big ones
      for (let i = 0; i < 6; i++) {
        const sp = el(`${id}-fb${k}s${i}`), big = D >= 30, side = i % 2 ? x1 + 3 : x0 - 3, ph = t * (3 + i) + i * 1.7, up = (0.5 + 0.5 * Math.sin(ph)) * dpt * 0.9;
        sp.setAttribute("cx", f1(side + (i % 2 ? 1 : -1) * (2 + i * 1.5))); sp.setAttribute("cy", f1(yb - dpt - up)); sp.setAttribute("r", f1(big ? 3 + dpt * 0.18 * (1 + (i % 3)) : 0));
        sp.setAttribute("opacity", f1(big ? 0.75 * (1 - 0.6 * Math.sin(ph)) * clamp(dpt / 20, 0, 1) : 0));
      }
    });
  }
  // the first wave, from the hill: the sea runs back in over the bare seabed (its edge churned white), pours over the beach and floods
  // the village ground round the shop and the hotel's ground floor (~2–3 m), swirls past them carrying planks and a cooler, then drains
  // back out to sea leaving the ground dark and wet with a line of litter. o.to the flood's height at its peak (1 = up the hotel's
  // ground floor), o.from the bay's level before it comes (the set's), o.rise / o.hold the fractions of the call where it peaks and where
  // it starts to drain (0.34 / 0.6), o.after the bay's level once it has gone (0.35: the sea already drawing back again)
  Tide.surge = (tl, id, t0, dur, o = {}) => {
    const S = ST[id], c = { t: 0 }, top = o.to ?? 1, u0 = o.from ?? S.lvl, u1 = o.after ?? 0.35, R = o.rise ?? 0.34, Hd = o.hold ?? 0.6;
    const Eo = gsap.parseEase("power2.out"), Ei = gsap.parseEase("power2.in"), Es = gsap.parseEase("sine.inOut");
    const Kat = (k) => (k < 0.1 ? 0 : k < R ? Eo((k - 0.1) / (R - 0.1)) : k < Hd ? 1 : k < 0.94 ? 1 - Es((k - Hd) / (0.94 - Hd)) : 0);
    const dir = (k) => Math.cos(Math.PI * sm(Hd - 0.02, Hd + 0.14, k));
    const flowAt = (k) => { let F = 0; const n = Math.max(1, Math.ceil(k * 80)); for (let i = 0; i < n; i++) F += (dir(((i + 0.5) / n) * k) * k * dur) / n; return F; };
    const draw = (tt) => {
      const k = clamp(tt / dur, 0, 1), K = Kat(k), ub = k < 0.16 ? lerp(u0, 0, Eo(k / 0.16)) : k < 0.8 ? 0 : lerp(0, u1, Ei((k - 0.8) / 0.2));
      hillSeaDraw(id, t0 + tt, ub, S.line, k < 0.16 ? 1 - sm(0.1, 0.16, k) : 0, sm(0, 0.08, k) * (1 - sm(Hd, 0.95, k)));
      floodDraw(id, t0 + tt, K * top, (k < R ? K : 1) * top, flowAt(k), dir(k));
    };
    draw(0);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => draw(c.t) }, t0);
  };
  // the bay drawing back (or in) from level o.from (the set's) to o.to between o.at and o.at + o.len seconds into the call (o.ease);
  // the white line on the horizon grows from o.line[0] to o.line[1] between o.lineAt (0.6 of the call) and the end; the boats bob, then lie over
  Tide.hillSea = (tl, id, t0, dur, o = {}) => {
    const S = ST[id], c = { t: 0 }, u0 = o.from ?? S.lvl, u1 = o.to ?? u0, at = o.at ?? 0, len = o.len ?? Math.max(0.01, dur - at), E = gsap.parseEase(o.ease || "power1.inOut");
    const [w0, w1] = o.line ?? [S.line, S.line], la = o.lineAt ?? dur * 0.6, Ew = gsap.parseEase("power1.in");
    const draw = (tt) => {
      const u = tt <= at ? u0 : tt >= at + len ? u1 : lerp(u0, u1, E((tt - at) / len));
      hillSeaDraw(id, t0 + tt, u, lerp(w0, w1, Ew(clamp((tt - la) / Math.max(0.01, dur - la), 0, 1))), 0);
    };
    draw(0);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => draw(c.t) }, t0);
  };

  // ======================== the opener: straight down onto wet sand as the sea pulls back off the title ========================
  function tideSand(L, o) {
    const id = o.id || "ts", r = mk(o.seed || 23), title = o.title || "ทะเลลด";
    put(L.sky, `<rect x="-600" y="-600" width="2300" height="3200" fill="#cbb084"/>`);
    let s = `<defs><radialGradient id="${id}-sandG" gradientUnits="userSpaceOnUse" cx="420" cy="760" r="1500"><stop offset="0" stop-color="#dcbd88"/><stop offset=".55" stop-color="#c49e68"/><stop offset="1" stop-color="#9a7a4c"/></radialGradient></defs>`;
    s += `<rect x="-600" y="-600" width="2300" height="3200" fill="url(#${id}-sandG)"/>`;
    // ripples running across, slightly diagonal, each a dark trough and a lit crest
    for (let k = 0; k < 44; k++) { const y0 = -300 + k * 56, ph = r() * 6; let p = ""; for (let x = -400; x <= 1500; x += 40) p += `${p ? "L" : "M"}${x},${f1(y0 + x * 0.12 + Math.sin(x * 0.009 + ph) * 16)}`; s += `<path d="${p}" stroke="#9a7e54" stroke-width="7" fill="none" opacity=".35"/><path d="${p}" stroke="#efe0c0" stroke-width="4" fill="none" opacity=".45" transform="translate(-3,-6)"/>`; }
    for (let k = 0; k < 260; k++) s += `<circle cx="${f1(-200 + r() * 1500)}" cy="${f1(-200 + r() * 2400)}" r="${f1(0.8 + r() * 1.8)}" fill="${r() < 0.5 ? "#fff8e8" : "#7a6444"}" opacity="${f1(0.3 + r() * 0.5)}"/>`;
    // the sheen of wet sand: soft bands of reflected sky and a scatter of glints
    for (let k = 0; k < 9; k++) { const y = -100 + k * 260 + r() * 80; s += `<path d="M-400,${f1(y)}Q540,${f1(y - 120)} 1500,${f1(y + 40)}V${f1(y + 110)}Q540,${f1(y - 20)} -400,${f1(y + 90)}Z" fill="#e8f2f4" opacity="${f1(0.05 + r() * 0.07)}"/>`; }
    for (let k = 0; k < 80; k++) s += `<circle cx="${f1(-100 + r() * 1300)}" cy="${f1(-100 + r() * 2200)}" r="${f1(1.2 + r() * 2.2)}" fill="#ffffff" opacity="${f1(0.4 + r() * 0.5)}"/>`;
    // shells and pebbles with their shadows (the sun is low on the upper left)
    const shell = (x, y, sz, rot, c) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(rot)})"><path d="M${f1(-sz + 5)},${f1(5)}a${f1(sz)},${f1(sz * 0.8)} 0 0 1 ${f1(sz * 2)},0l${f1(-sz)},${f1(sz * 0.5)}z" fill="#000" opacity=".2"/><path d="M${f1(-sz)},0a${f1(sz)},${f1(sz * 0.8)} 0 0 1 ${f1(sz * 2)},0l${f1(-sz)},${f1(sz * 0.5)}z" fill="${c}" ${OUT2}/>${Array.from({ length: 6 }, (_, i) => `<path d="M0,${f1(sz * 0.5)}L${f1(-sz + i * sz * 0.4)},${f1(-sz * 0.3 - Math.sin(i / 5 * Math.PI) * sz * 0.4)}" stroke="#8a6a5a" stroke-width="1.5" opacity=".6"/>`).join("")}</g>`;
    [[160, 380, 34, -20, "#f6e4d8"], [880, 300, 26, 30, "#f8d8c8"], [960, 1310, 30, -40, "#efe6d8"], [120, 1560, 24, 10, "#f2dcc8"], [720, 1690, 36, 64, "#f8eadc"], [420, 1840, 22, -10, "#f6d8d0"]].forEach((a) => { s += shell(...a); });
    for (let k = 0; k < 16; k++) { const x = -40 + r() * 1160, y = r() * 1920, R = 6 + r() * 12; s += `<ellipse cx="${f1(x + 4)}" cy="${f1(y + 5)}" rx="${f1(R)}" ry="${f1(R * 0.75)}" fill="#000" opacity=".2"/><ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(R)}" ry="${f1(R * 0.75)}" fill="${["#6a6058", "#8a7e70", "#d8d0c4", "#4a4038"][k % 4]}" ${OUT2}/><ellipse cx="${f1(x - R * 0.3)}" cy="${f1(y - R * 0.3)}" rx="${f1(R * 0.35)}" ry="${f1(R * 0.22)}" fill="#fff" opacity=".4"/>`; }
    // a ghost crab's hole with its sand balls
    s += `<ellipse cx="880" cy="1520" rx="16" ry="12" fill="#3a2c1c"/>` + Array.from({ length: 22 }, () => { const a = r() * Math.PI * 2, d = 24 + r() * 60; return `<circle cx="${f1(880 + Math.cos(a) * d)}" cy="${f1(1520 + Math.sin(a) * d)}" r="${f1(4 + r() * 3)}" fill="#cfb88c" stroke="#8a7050" stroke-width="1.2"/>`; }).join("");
    // a strand of weed and the foam's lacy leftovers
    s += `<path d="M-40,1180C120,1150 200,1240 340,1200S560,1150 640,1210" stroke="#4a5a2a" stroke-width="9" fill="none" opacity=".8"/><path d="M-30,1176C120,1146 200,1236 340,1196" stroke="#7a8a3a" stroke-width="3" fill="none"/>`;
    // the title pressed into the sand: a dark lip in shadow on the upper left, a lit lip on the lower right, the groove's floor
    const TX = 540, TY = 1020, FS = o.fs || 292, rot = -5;
    const tx = (fill, dx, dy, extra = "") => `<text x="${TX + dx}" y="${TY + dy}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${FS}" fill="${fill}" ${extra}>${title}</text>`;
    s += `<defs><clipPath id="${id}-tclip"><text x="${TX}" y="${TY}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${FS}">${title}</text></clipPath></defs>`;
    s += `<g transform="rotate(${rot} ${TX} ${TY})">${tx("#fbf0d6", 6, 7)}${tx("#f2dfb8", 3, 3)}<g clip-path="url(#${id}-tclip)">${tx("#46341e", 0, 0)}${tx("#86663e", 9, 11)}<path d="M${TX - 520},${TY - 40}L${TX + 520},${TY - 110}" stroke="#e8f2f4" stroke-width="10" opacity=".25"/></g>
      <g id="${id}-tw" opacity="0" clip-path="url(#${id}-tclip)">${tx("#bfe6ee", 7, 9)}<path d="M${TX - 420},${TY - 120}L${TX + 420},${TY - 40}" stroke="#fff" stroke-width="16" opacity=".55"/></g>
      ${o.sub ? `<text x="${TX}" y="${TY + 150}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="64" fill="#7a6244" opacity=".9">${o.sub}</text><text x="${TX + 3}" y="${TY + 153}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="64" fill="#f6ead0" opacity=".55">${o.sub}</text>` : ""}</g>`;
    // a driftwood stick that wrote it
    s += `<g transform="translate(860,1190) rotate(28)">${CS(8, 10, 120, 10, 0.8)}<path d="M-130,-6Q0,-16 130,-4L132,8Q0,0 -128,8Z" fill="#9a8466" ${OUT2}/><path d="M-110,-4Q0,-12 110,-2" stroke="#d8c8a8" stroke-width="3" fill="none"/></g>`;
    put(L.set, s);
    // fish and a crab (redrawn): revealed as the water leaves them, then flapping
    const FI = [[230, 1380, 1.55, -14, false], [840, 760, 1.25, 168, true], [650, 1500, 1.35, 20, false], [300, 620, 1.1, 200, true]].map(([x, y, sc, rot, fl]) => ({ x, y, sc, rot, fl, ph: r() * 9 }));
    put(L.set, FI.map((f, k) => `<g id="${id}-fish${k}">${fishSVG()}</g>`).join("") + `<g id="${id}-crab0">${crabSVG}</g>`);
    // the water (redrawn): a translucent sheet with caustics over the sand, the foam lace at its edge, bubbles, a wet sheen behind
    let w = `<defs><linearGradient id="${id}-wG" gradientUnits="userSpaceOnUse" x1="0" y1="-300" x2="0" y2="2200"><stop offset="0" stop-color="#2a8ab0" stop-opacity=".88"/><stop offset=".5" stop-color="#3ab0c0" stop-opacity=".66"/><stop offset="1" stop-color="#7ad8d4" stop-opacity=".5"/></linearGradient><clipPath id="${id}-wclip"><path id="${id}-wclipP" d=""/></clipPath></defs>`;
    w += `<path id="${id}-sheen" d="" fill="#ffffff" opacity=".18"/><path id="${id}-water" d="" fill="url(#${id}-wG)"/>`;
    let ca = "";
    for (let k = 0; k < 70; k++) { const x = -300 + r() * 1700, y = -300 + r() * 2500, rr = 30 + r() * 70; ca += `<path d="M${f1(x - rr)},${f1(y)}q${f1(rr * 0.5)},${f1(-rr * 0.4)} ${f1(rr)},0t${f1(rr)},0" stroke="#e8fbff" stroke-width="${f1(2 + r() * 3)}" fill="none" opacity="${f1(0.18 + r() * 0.25)}"/>`; }
    w += `<g clip-path="url(#${id}-wclip)"><g id="${id}-caus">${ca}</g><path d="M-400,300L1500,-100V100L-400,500Z" fill="#fff" opacity=".12"/></g>`;
    w += `<path id="${id}-foamB" d="" stroke="#ffffff" stroke-width="30" fill="none" opacity=".55" stroke-linecap="round"/><path id="${id}-foam" d="" stroke="#ffffff" stroke-width="12" fill="none" stroke-linecap="round"/>`;
    w += `<g id="${id}-bub">${Array.from({ length: 40 }, (_, k) => `<circle id="${id}-b${k}" r="4" fill="none" stroke="#fff" stroke-width="2.5" opacity=".8"/>`).join("")}</g>`;
    put(L.set, w);
    if (o.hand) put(L.set, handParts(id));
    put(L.glow, `<g id="${id}-glints">${Array.from({ length: 14 }, (_, k) => `<circle id="${id}-g${k}" r="18" fill="url(#tdGlint)" opacity="0"/>`).join("")}</g>`);
    ST[id] = { kind: "sand", FI, TY, ph: Array.from({ length: 40 }, () => [r(), r(), r()]), hand: o.hand ? { sh: o.handFrom || [800, 1890], from: [700, 1832], to: o.handTo || [392, 1500], aim: o.handAim || [262, 1372] } : null };
    sandDraw(id, 0, o.u ?? 0);
    if (o.hand) reachDraw(id, 0, 0);
  }
  // redraw the opener: u 0 (the sea covers the frame) … 1 (it has run off the top)
  function sandDraw(id, t, u) {
    const S = ST[id], yE = lerp(2080, -260, u);
    const edge = (x) => yE + 28 * Math.sin(x * 0.009 + t * 1.6) + 14 * Math.sin(x * 0.027 - t * 2.4);
    const E = []; for (let x = -400; x <= 1500; x += 30) E.push([x, edge(x)]);
    const wd = `M-400,-700H1500V${f1(edge(1500))}L${E.slice().reverse().map(P2).join("L")}Z`;
    el(`${id}-water`).setAttribute("d", wd); el(`${id}-wclipP`).setAttribute("d", wd);
    el(`${id}-foam`).setAttribute("d", `M${E.map(P2).join("L")}`);
    el(`${id}-foamB`).setAttribute("d", `M${E.map(([x, y]) => [x, y - 14]).map(P2).join("L")}`);
    el(`${id}-sheen`).setAttribute("d", `M${E.map(P2).join("L")}L1500,${f1(yE + 420)}L-400,${f1(yE + 420)}Z`);
    el(`${id}-caus`).setAttribute("transform", `translate(${f1(Math.sin(t * 0.8) * 20)},${f1(Math.cos(t * 0.6) * 16)})`);
    // the grooves still hold water just after the edge passes, then drain
    const pass = clamp((S.TY - 60 - yE) / 380, 0, 1);
    el(`${id}-tw`).setAttribute("opacity", f1(yE > S.TY + 80 ? 0 : 0.85 * (1 - sm(0.25, 1, pass))));
    for (let k = 0; k < 40; k++) {
      const [a, b, c] = S.ph[k], x = -350 + a * 1800, life = (b + t * (0.6 + c)) % 1, y = edge(x) + 10 + life * 60, e = el(`${id}-b${k}`);
      e.setAttribute("cx", f1(x)); e.setAttribute("cy", f1(y)); e.setAttribute("r", f1(3 + c * 7)); e.setAttribute("opacity", f1((1 - life) * 0.8));
    }
    S.FI.forEach((f, k) => {
      const shown = sm(f.y - 40, f.y - 160, yE), env = Math.max(0, Math.sin(t * 2.1 + f.ph * 3)), flop = Math.sin(t * 13 + f.ph) * env * shown;
      el(`${id}-fish${k}`).setAttribute("transform", `translate(${f1(f.x)},${f1(f.y - Math.abs(flop) * 18)}) rotate(${f1(f.rot + flop * 24)}) scale(${f1(f.fl ? -f.sc : f.sc)},${f1(f.sc * (0.85 + 0.15 * Math.abs(flop)))})`);
    });
    const cs = sm(1500, 1300, yE), cx = 880 - cs * 140 + Math.sin(t * 3) * 6;
    el(`${id}-crab0`).setAttribute("transform", `translate(${f1(cx)},${f1(1500 + cs * 30)}) scale(${f1(0.9 * cs + 0.001)})`);
    for (let k = 0; k < 14; k++) { const [a, b] = S.ph[k], g = el(`${id}-g${k}`), gx = -100 + a * 1300, gy = yE - 40 - b * 900; g.setAttribute("cx", f1(gx)); g.setAttribute("cy", f1(gy)); g.setAttribute("opacity", f1(Math.max(0, Math.sin(t * 5 + k * 1.7)) * 0.8)); }
  }
  Tide.sandTitle = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, E = gsap.parseEase(o.ease || "power2.inOut"), u0 = o.from ?? 0, u1 = o.to ?? 1;
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => sandDraw(id, t0 + c.t, lerp(u0, u1, E(c.t / dur))) }, t0);
  };

  // ======================== ยาย's shop (ร้านยายพร) from inside, and from the beach once everyone has gone: Sets.tideShop ========================
  Sets.DEFS += `
    <linearGradient id="tdWallIn" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4f948e"/><stop offset=".55" stop-color="#68b0a8"/><stop offset="1" stop-color="#7cc2b8"/></linearGradient>
    <linearGradient id="tdTarpLit" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3f88cc"/><stop offset=".6" stop-color="#5aa8ec"/><stop offset="1" stop-color="#7cc0f4"/></linearGradient>
    <linearGradient id="tdCtr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3e8680"/><stop offset=".6" stop-color="#58a29a"/><stop offset="1" stop-color="#6cb4aa"/></linearGradient>
    <linearGradient id="tdRedTop" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c8382a"/><stop offset=".7" stop-color="#e04a36"/><stop offset="1" stop-color="#ec6a50"/></linearGradient>
    <linearGradient id="tdStool" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1e559c"/><stop offset=".6" stop-color="#2a6ab8"/><stop offset="1" stop-color="#4a8ad4"/></linearGradient>
    <linearGradient id="tdFridge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4fbfc"/><stop offset="1" stop-color="#cfe6ec"/></linearGradient>
    <linearGradient id="tdSleeve" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d8c8a8"/><stop offset=".45" stop-color="#f4e6cc"/><stop offset="1" stop-color="#fbf2e0"/></linearGradient>
    <linearGradient id="tdTankTop" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe066"/><stop offset=".6" stop-color="#f6c832"/><stop offset="1" stop-color="#d8a01e"/></linearGradient>
    <radialGradient id="tdCaus"><stop offset="0" stop-color="#fffbe6" stop-opacity=".95"/><stop offset=".5" stop-color="#fff2c4" stop-opacity=".5"/><stop offset="1" stop-color="#fff2c4" stop-opacity="0"/></radialGradient>
    <radialGradient id="tdAO"><stop offset="0" stop-color="#1a1410" stop-opacity=".55"/><stop offset="1" stop-color="#1a1410" stop-opacity="0"/></radialGradient>
    <pattern id="tdPakama" patternUnits="userSpaceOnUse" width="34" height="34"><rect width="34" height="34" fill="#f2ece0"/><rect width="34" height="11" fill="#d8504a" opacity=".75"/><rect width="11" height="34" fill="#d8504a" opacity=".75"/><rect x="17" width="5" height="34" fill="#3a6ab0" opacity=".55"/><rect y="17" width="34" height="5" fill="#3a6ab0" opacity=".55"/></pattern>`;
  // SVG that must stand in front of the cast: appended to L.act and moved after the actors once the shot has been built (a microtask
  // runs after the engine's synchronous build), so it covers them and the shot's darkness and grade still fall on it
  const front = (L, id, svg) => {
    L.act.insertAdjacentHTML("beforeend", `<g id="${id}">${svg}</g>`);
    const g = document.getElementById(id);
    queueMicrotask(() => { if (g && g.parentNode) g.parentNode.appendChild(g); });
  };
  // a tapered capsule from A (width wa) to B (width wb): limbs, posts, handles
  const limb = (A, B, wa, wb) => {
    const dx = B[0] - A[0], dy = B[1] - A[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l;
    const a1 = [A[0] + (nx * wa) / 2, A[1] + (ny * wa) / 2], a2 = [A[0] - (nx * wa) / 2, A[1] - (ny * wa) / 2], b1 = [B[0] + (nx * wb) / 2, B[1] + (ny * wb) / 2], b2 = [B[0] - (nx * wb) / 2, B[1] - (ny * wb) / 2];
    return `M${P2(a1)}L${P2(b1)}A${f1(wb / 2)},${f1(wb / 2)} 0 0 0 ${P2(b2)}L${P2(a2)}A${f1(wa / 2)},${f1(wa / 2)} 0 0 0 ${P2(a1)}Z`;
  };
  // two-bone reach: the elbow for a shoulder S, a wrist W, bone lengths l1 l2, bent to the side `side` (+1 | −1)
  const elbowOf = (S, W, l1, l2, side) => {
    const dx = W[0] - S[0], dy = W[1] - S[1], d = clamp(Math.hypot(dx, dy), Math.abs(l1 - l2) + 1, l1 + l2 - 1), a = Math.atan2(dy, dx);
    const b = Math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1)) * side;
    return [S[0] + Math.cos(a + b) * l1, S[1] + Math.sin(a + b) * l1];
  };
  // ---------------- the "room" view: a fixed perspective, 1 m at depth Z = 1100/Z px, the eye 1.45 m up at (400, 860) ----------------
  // the back wall at Z 5.6 from X −1.7 to 2.1, the ceiling 2.9 m up; the open front along the right (X 2.1) looks out over the deck to the sea
  const SHOP = { F: 1100, EYE: 1.45, VX: 400, VY: 860, ZB: 5.6, XL: -1.7, XR: 2.1, H: 2.9 };
  const R3 = (X, Y, Z) => [SHOP.VX + (SHOP.F * X) / Z, SHOP.VY + (SHOP.F * (SHOP.EYE - Y)) / Z];
  const Q3 = (...p) => `M${p.map((q) => P2(R3(...q))).join("L")}Z`;
  const L3 = (...p) => `M${p.map((q) => P2(R3(...q))).join("L")}`;
  Tide.SHOP = SHOP;
  // where to stand someone in the room: X across (−1.7 … 2.1), Z in depth (1.5 … 5.6) → the screen spot of the feet and the rig scale (an adult)
  Tide.shopPos = (X, Z, h = 1.6) => { const [x, y] = R3(X, 0, Z); return { x: Math.round(x), y: Math.round(y), s: +((h * SHOP.F) / Z / 620).toFixed(3) }; };
  SHOP.spots = { yai: [-0.1, 5.0], june: [1.1, 3.3], tang: [0.55, 2.7] };
  // a wall clock in a frame of shells at (cx, cy), dial radius R: hands #id-hh #id-mh #id-sh, the sweep trail #id-ctr
  function clockSVG(id, cx, cy, R) {
    const k = R / 47, pt = (a, d) => [cx + Math.sin((a * Math.PI) / 180) * d, cy - Math.cos((a * Math.PI) / 180) * d];
    let g = `<g id="${id}-clock"><circle cx="${f1(cx + 3 * k)}" cy="${f1(cy + 6 * k)}" r="${f1(R * 1.44)}" fill="#14262a" opacity=".24"/>`;
    g += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(R * 1.16)}" fill="#c8a272" stroke="${INK}" stroke-width="${f1(2 * k)}"/><circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(R * 1.16)}" fill="none" stroke="#8a6a44" stroke-width="${f1(3 * k)}" stroke-dasharray="${f1(4 * k)} ${f1(3 * k)}"/>`;
    for (let i = 0; i < 16; i++) {
      const a = (i / 16) * 360, [sx, sy] = pt(a, R * 1.27), c = ["#f8e6d0", "#f4c8b4", "#fbf0e2", "#f0d6a8"][i % 4];
      g += `<g transform="translate(${f1(sx)},${f1(sy)}) rotate(${f1(a)}) scale(${f1(k)})"><path d="M0,10C-13,7 -17,-6 -12,-15Q0,-21 12,-15C17,-6 13,7 0,10Z" fill="${c}" stroke="${INK}" stroke-width="1.7"/>${[-8, -4, 0, 4, 8].map((x) => `<path d="M0,8L${x},-15" stroke="#b07a5a" stroke-width="1.1" opacity=".75"/>`).join("")}<path d="M-5,8h10v5h-10z" fill="${c}" stroke="${INK}" stroke-width="1.3"/></g>`;
    }
    for (let i = 0; i < 16; i++) { const a = ((i + 0.5) / 16) * 360, [sx, sy] = pt(a, R * 1.13); g += `<g transform="translate(${f1(sx)},${f1(sy)}) rotate(${f1(a + 90)}) scale(${f1(k)})"><ellipse rx="6.5" ry="4.4" fill="#f6eedc" stroke="${INK}" stroke-width="1.3"/><path d="M-4,0h8" stroke="#8a6a4a" stroke-width="1.2"/></g>`; }
    { const [x1, y1] = pt(-38, R * 1.28), [x2, y2] = pt(140, R * 1.3); let st = ""; for (let i = 0; i < 10; i++) { const a = (i / 10) * Math.PI * 2 - Math.PI / 2, rr = i % 2 ? 6 : 15; st += `${i ? "L" : "M"}${f1(Math.cos(a) * rr)},${f1(Math.sin(a) * rr)}`; }
      g += `<g transform="translate(${f1(x1)},${f1(y1)}) rotate(-20) scale(${f1(k)})"><path d="${st}Z" fill="#e8743a" stroke="${INK}" stroke-width="1.6"/><circle r="3" fill="#ffb07a"/></g><g transform="translate(${f1(x2)},${f1(y2)}) rotate(130) scale(${f1(k)})"><path d="M-14,4C-14,-8 -2,-14 8,-12L16,-16L13,-8C16,-2 12,6 2,6Z" fill="#f4d2b8" stroke="${INK}" stroke-width="1.6"/><path d="M-8,0Q-2,-8 8,-8" stroke="#c8906a" stroke-width="1.6" fill="none"/></g>`; }
    g += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(R)}" fill="#fbf6e8" stroke="${INK}" stroke-width="${f1(2.6 * k)}"/><circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(R * 0.9)}" fill="none" stroke="#3a7ab8" stroke-width="${f1(1.2 * k)}" opacity=".7"/>`;
    let tk = "";
    for (let i = 0; i < 60; i++) { const a = i * 6, big = i % 5 === 0, [x0, y0] = pt(a, R * (big ? 0.76 : 0.82)), [x1, y1] = pt(a, R * 0.88); tk += `M${f1(x0)},${f1(y0)}L${f1(x1)},${f1(y1)}`; }
    g += `<path d="${tk}" stroke="${INK}" stroke-width="${f1(1.1 * k)}"/>`;
    g += [[0, "12"], [90, "3"], [180, "6"], [270, "9"]].map(([a, t]) => { const [x, y] = pt(a, R * 0.6); return `<text x="${f1(x)}" y="${f1(y + R * 0.1)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${f1(R * 0.27)}" fill="${INK}">${t}</text>`; }).join("");
    g += `<text x="${f1(cx)}" y="${f1(cy - R * 0.28)}" text-anchor="middle" font-family="Kanit" font-weight="500" font-size="${f1(R * 0.12)}" fill="#3a7ab8">แหลมหอย</text>`;
    g += `<g transform="translate(${f1(cx)},${f1(cy + R * 0.36)}) scale(${f1(k * 0.5)})"><path d="M-30,2Q0,14 30,2L24,10Q0,18 -24,10Z" fill="#3a7ab8"/><path d="M-36,16Q-18,10 0,16T36,16" stroke="#3a7ab8" stroke-width="3" fill="none"/></g>`;
    g += `<path id="${id}-ctr" d="" fill="${INK}" opacity="0"/>`;
    g += `<g id="${id}-hh"><path d="M${f1(cx - R * 0.05)},${f1(cy + R * 0.12)}L${f1(cx - R * 0.065)},${f1(cy)}L${f1(cx - R * 0.03)},${f1(cy - R * 0.5)}L${f1(cx)},${f1(cy - R * 0.57)}L${f1(cx + R * 0.03)},${f1(cy - R * 0.5)}L${f1(cx + R * 0.065)},${f1(cy)}L${f1(cx + R * 0.05)},${f1(cy + R * 0.12)}Z" fill="${INK}"/></g>`;
    g += `<g id="${id}-mh"><path d="M${f1(cx - R * 0.04)},${f1(cy + R * 0.14)}L${f1(cx - R * 0.045)},${f1(cy)}L${f1(cx - R * 0.018)},${f1(cy - R * 0.76)}L${f1(cx)},${f1(cy - R * 0.83)}L${f1(cx + R * 0.018)},${f1(cy - R * 0.76)}L${f1(cx + R * 0.045)},${f1(cy)}L${f1(cx + R * 0.04)},${f1(cy + R * 0.14)}Z" fill="${INK}"/></g>`;
    g += `<g id="${id}-sh"><path d="M${f1(cx)},${f1(cy + R * 0.22)}V${f1(cy - R * 0.86)}" stroke="#d8302a" stroke-width="${f1(1.4 * k)}" stroke-linecap="round"/><circle cx="${f1(cx)}" cy="${f1(cy + R * 0.16)}" r="${f1(R * 0.05)}" fill="#d8302a"/></g>`;
    g += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(R * 0.07)}" fill="#c8a050" stroke="${INK}" stroke-width="${f1(1.2 * k)}"/>`;
    g += `<path d="M${f1(cx - R * 0.82)},${f1(cy - R * 0.18)}A${f1(R * 0.86)},${f1(R * 0.86)} 0 0 1 ${f1(cx + R * 0.18)},${f1(cy - R * 0.82)}A${f1(R * 0.7)},${f1(R * 0.7)} 0 0 0 ${f1(cx - R * 0.82)},${f1(cy - R * 0.18)}Z" fill="#ffffff" opacity=".42"/></g>`;
    return g;
  }
  function clockDraw(id, aH, aM, aS, trail) {
    const C = ST[id].clock, rot = (a) => `rotate(${f1(a)} ${f1(C.cx)} ${f1(C.cy)})`;
    el(`${id}-hh`).setAttribute("transform", rot(aH));
    el(`${id}-mh`).setAttribute("transform", rot(aM));
    el(`${id}-sh`).setAttribute("transform", rot(aS));
    const tr = el(`${id}-ctr`);
    if (Math.abs(trail) < 4) { tr.setAttribute("opacity", "0"); return; }
    const a1 = aM + clamp(trail, -175, 175), d = C.R * 0.82, p = (a) => [C.cx + Math.sin((a * Math.PI) / 180) * d, C.cy - Math.cos((a * Math.PI) / 180) * d];
    tr.setAttribute("d", `M${f1(C.cx)},${f1(C.cy)}L${P2(p(aM))}A${f1(d)},${f1(d)} 0 0 ${a1 > aM ? 1 : 0} ${P2(p(a1))}Z`);
    tr.setAttribute("opacity", f1(clamp(Math.abs(trail) / 80, 0, 1) * 0.32));
  }
  const clockAngles = (hhmm) => { const [h, m] = (hhmm || "07:40").split(":").map(Number); return [(h % 12) * 30 + m * 0.5, m * 6]; };
  // ---- small props in the room, placed by world point and drawn at that depth's scale ----
  const stool3 = (X, Z) => {
    // a blue plastic stool (เก้าอี้พลาสติก): a round-cornered seat 0.3 m across, 0.42 m up, a skirt with a cut-out, four splayed tapered legs
    const [x, y] = R3(X, 0.42, Z), k = SHOP.F / Z / 100, w = 30 * k, [, yf] = R3(X, 0, Z), h = yf - y, lw = f1(Math.max(1.2, 0.16 * k));
    return `<g transform="translate(${f1(x)},${f1(y)})"><ellipse cx="0" cy="${f1(h)}" rx="${f1(w * 0.72)}" ry="${f1(w * 0.1)}" fill="#1a1410" opacity=".28"/>
      <path d="M${f1(-w * 0.36)},${f1(w * 0.1)}L${f1(-w * 0.56)},${f1(h)}H${f1(-w * 0.34)}L${f1(-w * 0.18)},${f1(w * 0.1)}ZM${f1(w * 0.36)},${f1(w * 0.1)}L${f1(w * 0.56)},${f1(h)}H${f1(w * 0.34)}L${f1(w * 0.18)},${f1(w * 0.1)}Z" fill="#1e4e8a" stroke="${INK}" stroke-width="${lw}"/>
      <path d="M${f1(-w * 0.45)},${f1(h * 0.62)}H${f1(w * 0.45)}" stroke="#1e4e8a" stroke-width="${f1(w * 0.05)}"/>
      <path d="M${f1(-w * 0.5)},0H${f1(w * 0.5)}L${f1(w * 0.44)},${f1(w * 0.3)}H${f1(-w * 0.44)}Z" fill="url(#tdStool)" stroke="${INK}" stroke-width="${lw}"/><path d="M${f1(-w * 0.14)},${f1(w * 0.3)}Q0,${f1(w * 0.12)} ${f1(w * 0.14)},${f1(w * 0.3)}Z" fill="#14325a"/>
      <path d="M${f1(-w * 0.52)},0Q${f1(-w * 0.5)},${f1(-w * 0.13)} 0,${f1(-w * 0.14)}Q${f1(w * 0.5)},${f1(-w * 0.13)} ${f1(w * 0.52)},0Z" fill="#4a8ad4" stroke="${INK}" stroke-width="${lw}"/><ellipse cx="0" cy="${f1(-w * 0.07)}" rx="${f1(w * 0.1)}" ry="${f1(w * 0.025)}" fill="#14325a" opacity=".6"/></g>`;
  };
  const table3 = (X0, X1, Z0, Z1, c = "url(#tdRedTop)") => {
    const top = 0.72, lg = (X, Z) => `M${P2(R3(X, top - 0.03, Z))}L${P2(R3(X, 0, Z))}`;
    let g = `<path d="${Q3([X0 - 0.08, 0, Z0 - 0.1], [X1 + 0.08, 0, Z0 - 0.1], [X1 + 0.12, 0, Z1 + 0.1], [X0 - 0.12, 0, Z1 + 0.1])}" fill="#1a1410" opacity=".16"/>`;
    g += `<path d="${lg(X0 + 0.06, Z1 - 0.06)}${lg(X1 - 0.06, Z1 - 0.06)}" stroke="#7a8286" stroke-width="${f1(SHOP.F / Z1 / 30)}"/>`;
    g += `<path d="${Q3([X0, top, Z0], [X1, top, Z0], [X1, top, Z1], [X0, top, Z1])}" fill="${c}" stroke="${INK}" stroke-width="2"/>`;
    g += `<path d="${Q3([X0, top - 0.035, Z0], [X1, top - 0.035, Z0], [X1, top, Z0], [X0, top, Z0])}" fill="#d8dcdc" stroke="${INK}" stroke-width="1.6"/>`;
    g += `<path d="${lg(X0 + 0.06, Z0 + 0.06)}${lg(X1 - 0.06, Z0 + 0.06)}" stroke="#9aa2a6" stroke-width="${f1(SHOP.F / Z0 / 30)}"/>`;
    g += `<path d="${Q3([X0 + 0.05, top + 0.001, Z0 + 0.04], [X1 - 0.3, top + 0.001, Z0 + 0.04], [X1 - 0.45, top + 0.001, Z1 - 0.05], [X0 + 0.05, top + 0.001, Z1 - 0.05])}" fill="#ffffff" opacity=".1"/>`;
    return g;
  };
  // the big ice cooler (กระติกน้ำแข็ง): a white box with a blue lid, its left side toward us when it stands right of the eye line
  const cooler3 = (X0, X1, Z0, Z1, h = 0.48) => {
    const lw = SHOP.F / Z0 / 120;
    let g = `<path d="${Q3([X0 - 0.06, 0, Z0 - 0.05], [X1, 0, Z0 - 0.05], [X1 + 0.08, 0, Z1], [X0, 0, Z1 + 0.05])}" fill="#1a1410" opacity=".22"/>`;
    g += `<path d="${Q3([X0, 0, Z0], [X0, 0, Z1], [X0, h, Z1], [X0, h, Z0])}" fill="#c8d2d6" stroke="${INK}" stroke-width="${f1(lw)}"/>`;
    g += `<path d="${Q3([X0, 0, Z0], [X1, 0, Z0], [X1, h, Z0], [X0, h, Z0])}" fill="#f2f6f6" stroke="${INK}" stroke-width="${f1(lw)}"/>`;
    g += `<path d="${Q3([X0 - 0.01, h, Z0 - 0.01], [X1 + 0.01, h, Z0 - 0.01], [X1 + 0.01, h + 0.06, Z0 - 0.01], [X0 - 0.01, h + 0.06, Z0 - 0.01])}" fill="#2a6ab8" stroke="${INK}" stroke-width="${f1(lw)}"/><path d="${Q3([X0 - 0.01, h + 0.06, Z0 - 0.01], [X1 + 0.01, h + 0.06, Z0 - 0.01], [X1 + 0.01, h + 0.06, Z1], [X0 - 0.01, h + 0.06, Z1])}" fill="#4a8ad4" stroke="${INK}" stroke-width="${f1(lw)}"/>`;
    const [lx, ly] = R3((X0 + X1) / 2, h * 0.5, Z0);
    g += `<text x="${f1(lx)}" y="${f1(ly + lw * 4)}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="${f1(lw * 13)}" fill="#2a6ab8">น้ำแข็ง</text><path d="${L3([X0 + 0.04, h * 0.85, Z0], [X1 - 0.04, h * 0.85, Z0])}" stroke="#dfe6e8" stroke-width="${f1(lw * 2)}"/>`;
    return g;
  };
  // the condiment rack (เครื่องปรุง: vinegar with chillies, fish sauce, chilli flakes, sugar) at a world point
  const condiments = (X, Y, Z) => {
    const [x, y] = R3(X, Y, Z), k = SHOP.F / Z / 100, w = 5.2 * k;
    let g = `<g transform="translate(${f1(x)},${f1(y)})"><rect x="${f1(-w * 2.3)}" y="${f1(-w * 0.5)}" width="${f1(w * 4.6)}" height="${f1(w * 0.5)}" fill="#b8c0c2" stroke="${INK}" stroke-width="1"/><path d="M0,${f1(-w * 0.5)}V${f1(-w * 2.6)}" stroke="#9aa2a6" stroke-width="${f1(Math.max(1, w * 0.18))}"/>`;
    ["#e8d8a0", "#a85a2a", "#c8382a", "#f4f0e8"].forEach((c, i) => { const cx = -w * 1.7 + i * w * 1.14; g += `<rect x="${f1(cx - w * 0.5)}" y="${f1(-w * 1.6)}" width="${f1(w)}" height="${f1(w * 1.1)}" rx="${f1(w * 0.2)}" fill="${c}" stroke="${INK}" stroke-width="1"/><rect x="${f1(cx - w * 0.5)}" y="${f1(-w * 1.75)}" width="${f1(w)}" height="${f1(w * 0.3)}" fill="#f4f6f6" stroke="${INK}" stroke-width=".8"/>`; });
    return g + `</g>`;
  };
  const tissue = (X, Y, Z) => { const [x, y] = R3(X, Y, Z), k = SHOP.F / Z / 100, w = 12 * k; return `<g transform="translate(${f1(x)},${f1(y)})"><rect x="${f1(-w / 2)}" y="${f1(-w * 0.55)}" width="${f1(w)}" height="${f1(w * 0.55)}" rx="${f1(w * 0.06)}" fill="#f48ab0" stroke="${INK}" stroke-width="1.2"/><path d="M${f1(-w * 0.12)},${f1(-w * 0.55)}q${f1(w * 0.12)},${f1(-w * 0.3)} ${f1(w * 0.24)},0" fill="#ffffff" stroke="${INK}" stroke-width="1"/><path d="M${f1(-w * 0.4)},${f1(-w * 0.3)}h${f1(w * 0.8)}" stroke="#ffffff" stroke-width="${f1(Math.max(1, w * 0.06))}" opacity=".6"/></g>`; };
  const tumbler = (X, Y, Z) => { const [x, y] = R3(X, Y, Z), k = SHOP.F / Z / 100, w = 3.6 * k, h = 9 * k; return `<g transform="translate(${f1(x)},${f1(y)})"><path d="M${f1(-w)},${f1(-h)}L${f1(-w * 0.8)},0H${f1(w * 0.8)}L${f1(w)},${f1(-h)}Z" fill="#dff2f6" opacity=".55" stroke="#5a7a84" stroke-width="1"/><path d="M${f1(-w * 0.94)},${f1(-h * 0.62)}L${f1(-w * 0.82)},0H${f1(w * 0.82)}L${f1(w * 0.94)},${f1(-h * 0.62)}Z" fill="#9fd4dc" opacity=".55"/><path d="M${f1(-w * 0.6)},${f1(-h * 0.9)}V${f1(-h * 0.1)}" stroke="#fff" stroke-width="${f1(Math.max(1, w * 0.18))}" opacity=".8"/></g>`; };

  function shopRoom(L, id, o, P) {
    const r = mk(o.seed || 41), { VY, ZB, XL, XR, H } = SHOP;
    put(L.sky, `<rect x="-800" y="-800" width="2800" height="3600" fill="${P.sky[2]}"/>`);
    let s = `<defs><linearGradient id="${id}-oG" gradientUnits="userSpaceOnUse" x1="0" y1="${VY - 760}" x2="0" y2="${VY + 4}"><stop offset="0" stop-color="${P.sky[0]}"/><stop offset=".5" stop-color="${P.sky[1]}"/><stop offset=".85" stop-color="${P.sky[2]}"/><stop offset="1" stop-color="${P.sky[3]}"/></linearGradient>
      <linearGradient id="${id}-osG" gradientUnits="userSpaceOnUse" x1="0" y1="${VY}" x2="0" y2="${VY + 52}"><stop offset="0" stop-color="${P.sea[1]}"/><stop offset=".45" stop-color="${P.sea[3]}"/><stop offset="1" stop-color="${P.sea[5]}"/></linearGradient>
      <linearGradient id="${id}-obG" gradientUnits="userSpaceOnUse" x1="0" y1="${VY + 46}" x2="0" y2="${VY + 420}"><stop offset="0" stop-color="${P.wet[1]}"/><stop offset=".12" stop-color="${P.sand[1]}"/><stop offset="1" stop-color="${P.sand[0]}"/></linearGradient>
      <linearGradient id="${id}-ceG" gradientUnits="userSpaceOnUse" x1="0" y1="-700" x2="0" y2="${f1(R3(0, H, ZB)[1])}"><stop offset="0" stop-color="#2e302e"/><stop offset=".65" stop-color="#5c605c"/><stop offset="1" stop-color="#8a8e88"/></linearGradient>
      <linearGradient id="${id}-flG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(R3(0, 0, ZB)[1])}" x2="0" y2="1950"><stop offset="0" stop-color="#8a5c34"/><stop offset=".45" stop-color="#a8723e"/><stop offset="1" stop-color="#c08a52"/></linearGradient>
      <linearGradient id="${id}-dk" gradientUnits="userSpaceOnUse" x1="-100" y1="0" x2="900" y2="0"><stop offset="0" stop-color="#0e1a1c" stop-opacity=".5"/><stop offset=".6" stop-color="#0e1a1c" stop-opacity=".12"/><stop offset="1" stop-color="#0e1a1c" stop-opacity="0"/></linearGradient>
      <linearGradient id="${id}-sun" gradientUnits="userSpaceOnUse" x1="1080" y1="0" x2="300" y2="0"><stop offset="0" stop-color="#fff4d0" stop-opacity=".5"/><stop offset="1" stop-color="#fff4d0" stop-opacity="0"/></linearGradient></defs>`;
    // ---- outside, seen through the open front (drawn in the set itself, so its horizon stays on the eye line in any framing) ----
    s += `<rect x="560" y="${VY - 1400}" width="1500" height="1404" fill="url(#${id}-oG)"/><circle cx="1300" cy="${VY - 380}" r="560" fill="url(#qkSun)" opacity="${P.sun}"/>`;
    for (let k = 0; k < 3; k++) s += cloud2(880 + k * 300 + r() * 80, VY - 120 - r() * 160, 200 + r() * 120, 70 + r() * 30, r, P.cloud, P.cl[0], P.cl[1]);
    s += karst(id, 9, 1010, VY + 3, 64, 58, r, P, 0.72).g + karst(id, 10, 1110, VY + 3, 44, 40, r, P, 0.8).g;
    s += `<rect x="560" y="${VY}" width="1500" height="52" fill="url(#${id}-osG)"/>`;
    for (let k = 0; k < 18; k++) { const y = VY + 3 + Math.pow(r(), 1.3) * 44, x = 800 + r() * 500; s += `<path d="M${f1(x)},${f1(y)}h${f1(8 + (y - VY) * 0.8 * r())}" stroke="#fff" stroke-width="${f1(1 + (y - VY) / 30)}" opacity="${f1(0.35 + r() * 0.4)}" stroke-linecap="round"/>`; }
    s += `<rect x="560" y="${VY + 46}" width="1500" height="900" fill="url(#${id}-obG)"/><path d="M560,${VY + 50}Q900,${VY + 44} 2060,${VY + 52}" stroke="#ffffff" stroke-width="3" fill="none" opacity=".8"/>`;
    s += `<g transform="translate(1020,${VY + 104}) rotate(-3) scale(.11)">${CS(0, 46, 520, 40, 0.9)}${Tide.longtail({ hull: "#2f6fa0", band: "#d8423a", no: false, flip: true, seed: 47, k: 3 })}</g>`;
    s += coco(1050, VY + 380, 0.9, -0.05, (o.seed || 41) + 7, { pal: P.leaf, fl: 0.7 });
    // the deck outside the opening, its rail and the blue awning above it (all beyond the wall line X = 2.1)
    s += `<path d="${Q3([XR, 0, ZB + 2.5], [XR + 1.3, 0, ZB + 2.5], [XR + 1.3, 0, 1.2], [XR, 0, 1.2])}" fill="#b8844e"/>`;
    for (let k = 1; k < 8; k++) s += `<path d="${L3([XR + k * 0.16, 0.001, ZB + 2.5], [XR + k * 0.16, 0.001, 1.2])}" stroke="#8a5a32" stroke-width="2" opacity=".6"/>`;
    s += `<path d="${Q3([XR, 2.46, ZB], [XR + 1.0, 2.2, ZB], [XR + 1.0, 2.2, 1.05], [XR, 2.46, 1.05])}" fill="url(#tdTarpLit)" opacity=".94"/>`;
    for (let Z = ZB - 0.3; Z > 1.2; Z -= 0.3) s += `<path d="${L3([XR, 2.46, Z], [XR + 1.0, 2.2, Z])}" stroke="#2a62a8" stroke-width="2" opacity=".4"/>`;
    let hm = "";
    for (let Z = ZB; Z > 1.2; Z -= 0.22) { const a0 = R3(XR + 1.0, 2.2, Z), a1 = R3(XR + 1.0, 2.2, Z - 0.22), m0 = R3(XR + 1.0, 2.11, Z - 0.11); hm += `M${P2(a0)}Q${P2(m0)} ${P2(a1)}`; }
    s += `<path d="${hm}" stroke="#14325a" stroke-width="2.5" fill="#2a6ab0"/><path d="${L3([XR + 1.0, 2.2, ZB], [XR + 1.0, 2.2, 1.2])}" stroke="#14325a" stroke-width="2.5"/>`;
    // ---- the room: the ceiling, the left wall, the back wall ----
    s += `<path d="${Q3([XL, H, ZB], [XR, H, ZB], [XR, H, 1.02], [XL, H, 1.02])}" fill="url(#${id}-ceG)"/>`;
    let cg = "";
    for (let X = XL + 0.05; X < XR; X += 0.11) cg += `<path d="${L3([X, H, ZB], [X, H, 1.05])}" stroke="${Math.round(X * 100) % 2 ? "#b8bcb6" : "#3a3c3a"}" stroke-width="1.6" opacity=".35"/>`;
    for (let k = 0; k < 7; k++) { const X = XL + 0.3 + r() * 3.4; cg += `<path d="${L3([X, H, ZB - r()], [X + 0.03, H, 1.3 + r() * 2])}" stroke="#a86a3a" stroke-width="5" opacity=".22"/>`; }
    [5.0, 4.1, 3.3, 2.6, 2.05, 1.6].forEach((Z) => { cg += `<path d="${Q3([XL, H - 0.11, Z], [XR, H - 0.11, Z], [XR, H, Z], [XL, H, Z])}" fill="#6a4a2e" stroke="#2a1c12" stroke-width="2"/><path d="${L3([XL, H - 0.11, Z], [XR, H - 0.11, Z])}" stroke="#c89464" stroke-width="2" opacity=".6"/>`; });
    s += cg;
    s += `<path d="${Q3([XL, 0, ZB], [XL, 0, 1.02], [XL, H, 1.02], [XL, H, ZB])}" fill="#3e7e78"/>`;
    for (let Z = ZB - 0.2; Z > 1.2; Z -= 0.2) s += `<path d="${L3([XL, 0, Z], [XL, H, Z])}" stroke="#2a5e5a" stroke-width="2" opacity=".6"/>`;
    s += `<path d="${Q3([XL, 0, ZB], [XR, 0, ZB], [XR, H, ZB], [XL, H, ZB])}" fill="url(#tdWallIn)"/>`;
    let pl = "";
    for (let X = XL + 0.17; X < XR; X += 0.17) pl += `<path d="${L3([X, 0, ZB], [X, H, ZB])}" stroke="#3e7e78" stroke-width="2" opacity=".7"/>`;
    for (let k = 0; k < 16; k++) { const X = XL + r() * (XR - XL - 0.1), Y = r() * 2.6, [x, y] = R3(X, Y, ZB); pl += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(5 + r() * 14)}" height="${f1(14 + r() * 40)}" fill="#dceee6" opacity=".2"/>`; }
    s += pl;
    // ---- on the back wall: the drinks fridge, the menu board, the shrine, the tube lamp, the photo and the clipping, the clock, the calendar, the shelves ----
    const [fx0, fy0] = R3(-1.62, 1.85, 5.0), [fx1, fy1] = R3(-1.02, 0, 5.0), [fsx] = R3(-1.02, 0, 5.55), fw = fx1 - fx0, fh = fy1 - fy0;
    let fr = `<path d="M${f1(fx1)},${f1(fy0)}L${f1(fsx)},${f1(R3(-1.02, 1.85, 5.55)[1])}V${f1(R3(-1.02, 0, 5.55)[1])}L${f1(fx1)},${f1(fy1)}Z" fill="#b8c4c6" stroke="${INK}" stroke-width="2"/>`;
    fr += `<rect x="${f1(fx0)}" y="${f1(fy0)}" width="${f1(fw)}" height="${f1(fh)}" rx="5" fill="#f2f4f2" stroke="${INK}" stroke-width="2.5"/><rect x="${f1(fx0)}" y="${f1(fy0)}" width="${f1(fw)}" height="${f1(fh * 0.12)}" rx="5" fill="#d8302a" stroke="${INK}" stroke-width="2"/>`;
    fr += `<text x="${f1(fx0 + fw / 2)}" y="${f1(fy0 + fh * 0.09)}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="${f1(fh * 0.06)}" fill="#ffffff">เย็นชื่นใจ</text>`;
    const gx0 = fx0 + fw * 0.09, gy0 = fy0 + fh * 0.15, gw = fw * 0.82, gh = fh * 0.72;
    fr += `<rect x="${f1(gx0)}" y="${f1(gy0)}" width="${f1(gw)}" height="${f1(gh)}" rx="3" fill="url(#tdFridge)" stroke="${INK}" stroke-width="2"/>`;
    for (let row = 0; row < 5; row++) {
      const sy = gy0 + gh * (0.19 + row * 0.2);
      fr += `<path d="M${f1(gx0)},${f1(sy)}H${f1(gx0 + gw)}" stroke="#9ab4bc" stroke-width="2.5"/>`;
      for (let i = 0; i < 6; i++) { const bx = gx0 + gw * (0.1 + i * 0.16), c = ["#3aa84a", "#f2882a", "#5a2a1a", "#d8eef4", "#f2d02a", "#d8302a"][(i + row * 2) % 6], bh = gh * (0.13 + (i % 2) * 0.02); fr += `<rect x="${f1(bx - gw * 0.045)}" y="${f1(sy - bh)}" width="${f1(gw * 0.09)}" height="${f1(bh)}" rx="${f1(gw * 0.03)}" fill="${c}" stroke="${INK}" stroke-width="1"/><rect x="${f1(bx - gw * 0.02)}" y="${f1(sy - bh - gh * 0.02)}" width="${f1(gw * 0.04)}" height="${f1(gh * 0.025)}" fill="#f4f4f4" stroke="${INK}" stroke-width=".8"/>`; }
    }
    fr += `<path d="M${f1(gx0 + gw * 0.12)},${f1(gy0)}L${f1(gx0 + gw * 0.32)},${f1(gy0)}L${f1(gx0 + gw * 0.05)},${f1(gy0 + gh)}H${f1(gx0)}Z" fill="#ffffff" opacity=".35"/><rect x="${f1(gx0 + gw * 0.9)}" y="${f1(gy0 + gh * 0.4)}" width="${f1(gw * 0.05)}" height="${f1(gh * 0.2)}" rx="2" fill="#9aa2a6" stroke="${INK}" stroke-width="1"/>`;
    s += fr;
    // the menu board, chalk on green
    const [mx0, my0] = R3(-0.95, 2.05, ZB), [mx1, my1] = R3(-0.42, 1.2, ZB), mw = mx1 - mx0, mh = my1 - my0;
    s += `<rect x="${f1(mx0 + 3)}" y="${f1(my0 + 5)}" width="${f1(mw)}" height="${f1(mh)}" fill="#14262a" opacity=".3"/><rect x="${f1(mx0)}" y="${f1(my0)}" width="${f1(mw)}" height="${f1(mh)}" rx="3" fill="#8a5a32" stroke="${INK}" stroke-width="2"/><rect x="${f1(mx0 + 5)}" y="${f1(my0 + 5)}" width="${f1(mw - 10)}" height="${f1(mh - 10)}" fill="#2e4a3c"/>`;
    s += `<text x="${f1(mx0 + mw / 2)}" y="${f1(my0 + 25)}" text-anchor="middle" font-family="Mali" font-weight="700" font-size="17" fill="#f4e8a0">เมนู</text>`;
    s += [["ปลาเผา", "150"], ["หมึกย่าง", "120"], ["กุ้งเผา", "200"], ["ข้าวผัดปู", "80"], ["ส้มตำ", "50"]].map(([a, b], i) => `<text x="${f1(mx0 + 10)}" y="${f1(my0 + 50 + i * 22)}" font-family="Mali" font-weight="600" font-size="13" fill="#f4f0e2">${a}</text><text x="${f1(mx1 - 10)}" y="${f1(my0 + 50 + i * 22)}" text-anchor="end" font-family="Mali" font-weight="600" font-size="13" fill="#f4f0e2">${b}</text>`).join("");
    // the shrine shelf high up: a small gold Buddha, a marigold garland, two little red lamps
    const [sx, sy] = R3(-0.7, 2.42, ZB);
    s += `<g transform="translate(${f1(sx)},${f1(sy)})"><path d="M-46,0H46L40,10H-40Z" fill="#b82a1e" stroke="${INK}" stroke-width="1.6"/><path d="M-30,10L-22,26M30,10L22,26" stroke="#8a2414" stroke-width="4"/><rect x="-46" y="-3" width="92" height="4" fill="#e8c050"/>
      <path d="M-9,-3Q-11,-14 -6,-20Q-8,-28 0,-31Q8,-28 6,-20Q11,-14 9,-3Z" fill="#e8b830" stroke="${INK}" stroke-width="1.3"/><circle cx="0" cy="-27" r="4" fill="#f2c840" stroke="${INK}" stroke-width="1"/>
      <path d="M-26,-3V-14M26,-3V-14" stroke="#e8e0c8" stroke-width="3"/><circle cx="-26" cy="-16" r="3" fill="#ff5a3a"/><circle cx="26" cy="-16" r="3" fill="#ff5a3a"/><circle cx="-26" cy="-16" r="9" fill="url(#tdBeacon)" opacity=".5"/><circle cx="26" cy="-16" r="9" fill="url(#tdBeacon)" opacity=".5"/>
      <path d="M-42,8Q0,30 42,8" stroke="#f4a020" stroke-width="5" fill="none" stroke-dasharray="3 2"/><path d="M-40,9Q0,26 40,9" stroke="#ffe7a0" stroke-width="2" fill="none" stroke-dasharray="2 3"/><path d="M0,20V34" stroke="#f4a020" stroke-width="4"/><circle cx="0" cy="36" r="4" fill="#d8302a"/></g>`;
    // the tube lamp (off in the daytime)
    s += `<path d="${L3([-1.45, 2.7, ZB], [-1.0, 2.7, ZB])}" stroke="#9aa2a6" stroke-width="8" stroke-linecap="round"/><path d="${L3([-1.43, 2.69, ZB], [-1.02, 2.69, ZB])}" stroke="#f4f6f2" stroke-width="5" stroke-linecap="round"/>`;
    // the clue: the old photo (two young fishermen on a longtail) and the clipping of 27 Dec 2004, right above where ยาย stands
    const [px, py] = R3(-0.18, 1.82, ZB), [cx2, cy2] = R3(0.29, 1.8, ZB);
    s += `<g id="${id}-clue"><path d="M${f1(px)},${f1(py - 46)}L${f1(px - 30)},${f1(py - 34)}M${f1(px)},${f1(py - 46)}L${f1(px + 30)},${f1(py - 34)}" stroke="#4a3a2a" stroke-width="1.4"/><circle cx="${f1(px)}" cy="${f1(py - 46)}" r="2.4" fill="#5a5a5a"/>${TideCast.photo(f1(px), f1(py), 0.395, { id: `${id}-photo` })}${TideCast.clipping(f1(cx2), f1(cy2), 0.2, { id: `${id}-clip`, rot: -4 })}<rect x="${f1(cx2 - 12)}" y="${f1(cy2 - 30)}" width="16" height="6" fill="#f4f0e0" opacity=".85" transform="rotate(-10 ${f1(cx2 - 4)} ${f1(cy2 - 27)})"/></g>`;
    // the clock with its frame of shells (Tide.clockBack spins its hands)
    const [ccx, ccy] = R3(0.72, 2.24, ZB), CR = 0.24 * SHOP.F / ZB;
    s += clockSVG(id, ccx, ccy, CR);
    // the calendar: a temple on a hill, ธันวาคม, the 26th ringed
    const [kx0, ky0] = R3(1.2, 2.56, ZB), [kx1, ky1] = R3(1.52, 1.92, ZB), kw = kx1 - kx0, kh = ky1 - ky0;
    s += `<path d="M${f1(kx0 + kw / 2)},${f1(ky0 - 6)}L${f1(kx0 + 8)},${f1(ky0)}M${f1(kx0 + kw / 2)},${f1(ky0 - 6)}L${f1(kx1 - 8)},${f1(ky0)}" stroke="#5a4a3a" stroke-width="1.2"/><rect x="${f1(kx0 + 3)}" y="${f1(ky0 + 4)}" width="${f1(kw)}" height="${f1(kh)}" fill="#14262a" opacity=".25"/><rect x="${f1(kx0)}" y="${f1(ky0)}" width="${f1(kw)}" height="${f1(kh)}" fill="#fbf8f0" stroke="${INK}" stroke-width="1.6"/>
      <rect x="${f1(kx0 + 3)}" y="${f1(ky0 + 3)}" width="${f1(kw - 6)}" height="${f1(kh * 0.42)}" fill="#7ab8e0"/><path d="M${f1(kx0 + 3)},${f1(ky0 + 3 + kh * 0.42)}L${f1(kx0 + kw * 0.35)},${f1(ky0 + kh * 0.24)}L${f1(kx0 + kw * 0.7)},${f1(ky0 + kh * 0.36)}L${f1(kx1 - 3)},${f1(ky0 + kh * 0.28)}V${f1(ky0 + 3 + kh * 0.42)}Z" fill="#3a8a4a"/><path d="M${f1(kx0 + kw * 0.5)},${f1(ky0 + kh * 0.1)}L${f1(kx0 + kw * 0.44)},${f1(ky0 + kh * 0.3)}H${f1(kx0 + kw * 0.56)}Z" fill="#f2c840" stroke="${INK}" stroke-width=".8"/>
      <rect x="${f1(kx0)}" y="${f1(ky0 + kh * 0.45)}" width="${f1(kw)}" height="${f1(kh * 0.1)}" fill="#d8302a"/><text x="${f1(kx0 + kw / 2)}" y="${f1(ky0 + kh * 0.53)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${f1(kh * 0.07)}" fill="#fff">ธันวาคม</text>`;
    for (let i = 0; i < 35; i++) { const gx = kx0 + 5 + (i % 7) * ((kw - 10) / 7), gy = ky0 + kh * 0.6 + Math.floor(i / 7) * (kh * 0.075); s += `<rect x="${f1(gx)}" y="${f1(gy)}" width="${f1((kw - 10) / 7 - 1.5)}" height="${f1(kh * 0.05)}" fill="${i % 7 === 0 ? "#f2c0b8" : "#d8d4c8"}"/>`; }
    const gx26 = kx0 + 5 + 5 * ((kw - 10) / 7) + (kw - 10) / 14, gy26 = ky0 + kh * 0.6 + 3 * (kh * 0.075) + kh * 0.025;
    s += `<ellipse cx="${f1(gx26)}" cy="${f1(gy26)}" rx="${f1((kw - 10) / 10)}" ry="${f1(kh * 0.045)}" fill="none" stroke="#d8302a" stroke-width="1.6"/>`;
    // the shelves: fish sauce, soy sauce, chilli paste, cans; a transistor radio, packs of crisps, mosquito coils, plastic cups
    const shelf = (Y, items) => {
      const [ax, ay] = R3(0.92, Y, ZB), [bx] = R3(1.98, Y, ZB);
      let g = `<rect x="${f1(ax)}" y="${f1(ay)}" width="${f1(bx - ax)}" height="5" fill="#a8743e" stroke="${INK}" stroke-width="1.4"/><path d="M${f1(ax + 10)},${f1(ay + 5)}l8,10M${f1(bx - 10)},${f1(ay + 5)}l-8,10" stroke="#5a5048" stroke-width="2.4"/>`;
      let x = ax + 6;
      items.forEach(([w, h, c, kind]) => {
        if (kind === "bottle") g += `<path d="M${f1(x)},${f1(ay)}V${f1(ay - h * 0.62)}Q${f1(x)},${f1(ay - h * 0.75)} ${f1(x + w * 0.3)},${f1(ay - h * 0.8)}V${f1(ay - h)}H${f1(x + w * 0.7)}V${f1(ay - h * 0.8)}Q${f1(x + w)},${f1(ay - h * 0.75)} ${f1(x + w)},${f1(ay - h * 0.62)}V${f1(ay)}Z" fill="${c}" stroke="${INK}" stroke-width="1.2"/><rect x="${f1(x + w * 0.28)}" y="${f1(ay - h - 3)}" width="${f1(w * 0.44)}" height="4" fill="#d8302a"/><rect x="${f1(x + 1)}" y="${f1(ay - h * 0.45)}" width="${f1(w - 2)}" height="${f1(h * 0.2)}" fill="#f4ecd0" opacity=".9"/>`;
        else if (kind === "radio") g += `<rect x="${f1(x)}" y="${f1(ay - h)}" width="${f1(w)}" height="${f1(h)}" rx="3" fill="${c}" stroke="${INK}" stroke-width="1.4"/><rect x="${f1(x + w * 0.08)}" y="${f1(ay - h * 0.8)}" width="${f1(w * 0.45)}" height="${f1(h * 0.6)}" rx="2" fill="#3a3430"/><circle cx="${f1(x + w * 0.75)}" cy="${f1(ay - h * 0.55)}" r="${f1(h * 0.18)}" fill="#e8dcc0" stroke="${INK}" stroke-width="1"/><path d="M${f1(x + w * 0.85)},${f1(ay - h)}l${f1(w * 0.3)},${f1(-h * 0.8)}" stroke="#9aa2a6" stroke-width="1.6"/>`;
        else if (kind === "bag") g += `<path d="M${f1(x)},${f1(ay)}L${f1(x + 2)},${f1(ay - h)}Q${f1(x + w / 2)},${f1(ay - h - 4)} ${f1(x + w - 2)},${f1(ay - h)}L${f1(x + w)},${f1(ay)}Z" fill="${c}" stroke="${INK}" stroke-width="1.2"/><circle cx="${f1(x + w / 2)}" cy="${f1(ay - h * 0.5)}" r="${f1(w * 0.22)}" fill="#fff" opacity=".7"/>`;
        else g += `<rect x="${f1(x)}" y="${f1(ay - h)}" width="${f1(w)}" height="${f1(h)}" rx="1.5" fill="${c}" stroke="${INK}" stroke-width="1.2"/><rect x="${f1(x)}" y="${f1(ay - h * 0.7)}" width="${f1(w)}" height="${f1(h * 0.3)}" fill="#ffffff" opacity=".45"/>`;
        x += w + 3;
      });
      return g;
    };
    s += shelf(1.32, [[13, 40, "#7a3a14", "bottle"], [13, 40, "#7a3a14", "bottle"], [13, 36, "#2a1a10", "bottle"], [18, 22, "#c8382a", "can"], [18, 22, "#2a8ad0", "can"], [16, 28, "#e8a020", "can"], [13, 40, "#7a3a14", "bottle"], [24, 26, "#5aa84a", "can"]]);
    s += shelf(1.66, [[48, 30, "#c8302a", "radio"], [24, 34, "#f2c02a", "bag"], [24, 34, "#3a9ad8", "bag"], [24, 34, "#e86a2a", "bag"], [26, 22, "#3a8a3a", "box"], [16, 30, "#f4f2ea", "can"]]);
    // a crate of soda bottles on the floor under the shelves
    const [crx, cry] = R3(1.35, 0.36, 5.45), [crx1, cry1] = R3(1.92, 0, 5.45);
    s += `<rect x="${f1(crx)}" y="${f1(cry)}" width="${f1(crx1 - crx)}" height="${f1(cry1 - cry)}" fill="#f2c02a" stroke="${INK}" stroke-width="1.6"/>${[0.2, 0.4, 0.6, 0.8].map((u) => `<rect x="${f1(lerp(crx, crx1, u) - 5)}" y="${f1(cry - 18)}" width="10" height="22" rx="3" fill="#3a8a4a" stroke="${INK}" stroke-width="1"/>`).join("")}<path d="M${f1(crx)},${f1(cry + (cry1 - cry) * 0.4)}H${f1(crx1)}" stroke="#c89a1a" stroke-width="2"/>`;
    // the back wall darkens away from the open front
    s += `<path d="${Q3([XL, 0, ZB], [XR, 0, ZB], [XR, H, ZB], [XL, H, ZB])}" fill="url(#${id}-dk)"/>`;
    // ---- the open front on the right: the rail, the posts, the eave beam and the wall over it ----
    let fz = `<path d="${Q3([XR, 0.84, ZB], [XR, 0.84, 1.2], [XR, 0.94, 1.2], [XR, 0.94, ZB])}" fill="#b07a46" stroke="${INK}" stroke-width="2"/><path d="${Q3([XR, 0.06, ZB], [XR, 0.06, 1.2], [XR, 0.13, 1.2], [XR, 0.13, ZB])}" fill="#9a6a3e" stroke="${INK}" stroke-width="1.6"/>`;
    for (let Z = ZB - 0.13; Z > 1.3; Z -= 0.13) fz += `<path d="${Q3([XR, 0.13, Z], [XR, 0.13, Z - 0.045], [XR, 0.84, Z - 0.045], [XR, 0.84, Z])}" fill="#a8743e" stroke="${INK}" stroke-width="1.2"/>`;
    fz += `<path d="${L3([XR, 0.94, ZB], [XR, 0.94, 1.2])}" stroke="#e8bc84" stroke-width="2" opacity=".8"/>`;
    fz += `<path d="${Q3([XR, 2.36, ZB], [XR, 2.36, 1.02], [XR, H, 1.02], [XR, H, ZB])}" fill="#4f948e"/><path d="${Q3([XR, 2.34, ZB], [XR, 2.34, 1.02], [XR, 2.48, 1.02], [XR, 2.48, ZB])}" fill="#8a5a32" stroke="${INK}" stroke-width="2"/>`;
    [ZB, 4.2, 2.8].forEach((Z) => { fz += `<path d="${Q3([XR - 0.13, 0, Z - 0.13], [XR - 0.13, 0, Z], [XR - 0.13, 2.4, Z], [XR - 0.13, 2.4, Z - 0.13])}" fill="#7a4e2a" stroke="${INK}" stroke-width="1.6"/><path d="${Q3([XR - 0.13, 0, Z - 0.13], [XR, 0, Z - 0.13], [XR, 2.4, Z - 0.13], [XR - 0.13, 2.4, Z - 0.13])}" fill="#a8743e" stroke="${INK}" stroke-width="2"/>`; });
    // a shell chime and two glass floats in rope nets hanging from the eave beam
    const [chx, chy] = R3(XR - 0.05, 2.34, 4.75);
    fz += `<g transform="translate(${f1(chx)},${f1(chy)})"><path d="M-8,0V40M0,0V54M8,0V34" stroke="#6a5a4a" stroke-width="1.2"/>${[[-8, 44], [0, 58], [8, 38]].map(([x, y]) => `<path d="M${x},${y + 6}c-5,-2 -6,-8 -3,-12q3,-2 6,0c3,4 2,10 -3,12z" fill="#f6e4d4" stroke="${INK}" stroke-width="1"/>`).join("")}</g>`;
    [[XR - 0.1, 3.5, "#5ab8a0"], [XR - 0.1, 3.05, "#7aa8d8"]].forEach(([X, Z, c]) => { const [bx, by] = R3(X, 2.34, Z), k = SHOP.F / Z / 100, rr = 9 * k; fz += `<path d="M${f1(bx)},${f1(by)}V${f1(by + rr * 1.6)}" stroke="#8a7a5a" stroke-width="1.6"/><circle cx="${f1(bx)}" cy="${f1(by + rr * 2.6)}" r="${f1(rr)}" fill="${c}" opacity=".85" stroke="${INK}" stroke-width="1.4"/><path d="M${f1(bx - rr)},${f1(by + rr * 2.6)}Q${f1(bx)},${f1(by + rr * 3.2)} ${f1(bx + rr)},${f1(by + rr * 2.6)}M${f1(bx)},${f1(by + rr * 1.6)}V${f1(by + rr * 3.6)}" stroke="#8a7a5a" stroke-width="1.2" fill="none"/><circle cx="${f1(bx - rr * 0.35)}" cy="${f1(by + rr * 2.25)}" r="${f1(rr * 0.25)}" fill="#fff" opacity=".7"/>`; });
    s += fz;
    // ---- the floor: wide planks running in, the morning sun lying across them from the open front ----
    s += `<path d="${Q3([XL, 0, ZB], [XR, 0, ZB], [XR, 0, 1.02], [XL, 0, 1.02])}" fill="url(#${id}-flG)"/>`;
    let fl = "";
    for (let X = XL + 0.19; X < XR; X += 0.19) fl += `<path d="${L3([X, 0, ZB], [X, 0, 1.05])}" stroke="#5a3a1e" stroke-width="2" opacity=".55"/>`;
    for (let k = 0; k < 22; k++) { const X = XL + Math.floor(r() * 20) * 0.19, Z = 1.6 + r() * 3.8; fl += `<path d="${L3([X, 0, Z], [X + 0.19, 0, Z])}" stroke="#5a3a1e" stroke-width="2" opacity=".5"/>`; }
    for (let k = 0; k < 10; k++) { const X = XL + 0.1 + r() * 3.6, Z = 1.8 + r() * 3.5; fl += `<path d="${L3([X, 0, Z], [X + 0.02, 0, Z - 0.4 - r() * 0.6])}" stroke="#e2b07a" stroke-width="2.5" opacity=".25"/>`; }
    for (let k = 0; k < 40; k++) { const X = XL + 0.05 + r() * 3.7, Z = 1.6 + r() * 3.8, l = 0.3 + r() * 0.8; fl += `<path d="${L3([X, 0, Z], [X + 0.01, 0, Z - l])}" stroke="${k % 2 ? "#6a4424" : "#d8a470"}" stroke-width="${f1(1 + 2.5 / Z)}" opacity=".3"/>`; }
    for (let k = 0; k < 6; k++) { const [x, y] = R3(XL + 0.3 + r() * 3.2, 0, 1.8 + r() * 3), k2 = 60 / (y - 860 + 60); fl += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(14 * (1 - k2))}" ry="${f1(4 * (1 - k2))}" fill="none" stroke="#6a4424" stroke-width="1.6" opacity=".35"/>`; }
    fl += `<path d="${Q3([1.0, 0.001, ZB], [XR - 0.05, 0.001, ZB], [XR - 0.05, 0.001, 1.6], [1.3, 0.001, 1.6])}" fill="#fff6e0" opacity=".07"/>`;
    s += fl;
    // the morning sun through the open front: warm patches on the floor, striped by the rail's balusters, the posts' long shadows
    [[ZB - 0.14, 4.33], [4.06, 2.93], [2.66, 1.55]].forEach(([za, zb]) => {
      const sh = 0.55, P0 = [XR - 0.02, za], P1 = [XR - 0.02, zb], P3 = [0.75, za + sh], P2_ = [0.75, zb + sh];
      s += `<path d="${Q3([P0[0], 0.002, P0[1]], [P1[0], 0.002, P1[1]], [P2_[0], 0.002, P2_[1]], [P3[0], 0.002, P3[1]])}" fill="#ffe6a0" opacity=".36"/>`;
      let st = "";
      for (let Z = za - 0.07; Z > zb; Z -= 0.13) st += `M${P2(R3(XR - 0.05, 0.003, Z))}L${P2(R3(1.35, 0.003, Z + sh * 0.56))}`;
      s += `<path d="${st}" stroke="#8a5a32" stroke-width="5" opacity=".3"/>`;
    });
    s += `<path d="${Q3([XL, 0, ZB], [XR, 0, ZB], [XR, 0, ZB - 0.35], [XL, 0, ZB - 0.35])}" fill="#1a1410" opacity=".22"/><path d="${Q3([XL, 0, ZB], [XL + 0.4, 0, ZB], [XL + 0.4, 0, 1.05], [XL, 0, 1.05])}" fill="#1a1410" opacity=".25"/>`;
    s += `<path d="${Q3([XL, 0, ZB], [0.6, 0, ZB], [0.2, 0, 1.05], [XL, 0, 1.05])}" fill="url(#${id}-dk)" opacity=".7"/><path d="${Q3([XL, H, ZB], [0.6, H, ZB], [0.2, H, 1.05], [XL, H, 1.05])}" fill="url(#${id}-dk)" opacity=".8"/>`;
    // ---- under the ceiling: a fishing net strung across with floats, a ceiling fan, a bulb ----
    let ce = "";
    const NZ = 3.95, rope = (u) => [lerp(-1.45, 1.95, u), 2.78 - 0.3 * Math.sin(Math.PI * u), NZ];
    ce += `<path d="${Array.from({ length: 21 }, (_, i) => `${i ? "L" : "M"}${P2(R3(...rope(i / 20)))}`).join("")}" stroke="#8a7a5a" stroke-width="2.4" fill="none"/>`;
    let net = "";
    for (let i = 0; i <= 20; i++) { const [X, Y] = rope(i / 20), drop = 0.18 + 0.12 * Math.sin(i * 1.7); net += `M${P2(R3(X, Y, NZ))}L${P2(R3(X + 0.08, Y - drop, NZ - 0.05))}`; }
    for (let i = 0; i < 20; i++) { const [X, Y] = rope((i + 0.5) / 20); net += `M${P2(R3(X - 0.08, Y - 0.1, NZ))}L${P2(R3(X + 0.08, Y - 0.12, NZ))}`; }
    ce += `<path d="${net}" stroke="#a89a7a" stroke-width="1.2" opacity=".6" fill="none"/>`;
    [[0.08, "#f2882a", 1], [0.2, "#5ab8a0", 0], [0.33, "#f4f2ea", 1], [0.46, "#7aa8d8", 0], [0.6, "#f2c02a", 1], [0.73, "#5ab8a0", 0], [0.86, "#f2882a", 1]].forEach(([u, c, plastic], i) => {
      const [X, Y] = rope(u), Yb = Y - 0.16 - (i % 2) * 0.08, [bx, by] = R3(X, Yb, NZ), [tx, ty] = R3(X, Y, NZ), rr = (plastic ? 0.075 : 0.09) * SHOP.F / NZ;
      ce += `<path d="M${f1(tx)},${f1(ty)}L${f1(bx)},${f1(by - rr)}" stroke="#8a7a5a" stroke-width="1.4"/>`;
      ce += plastic ? `<ellipse cx="${f1(bx)}" cy="${f1(by)}" rx="${f1(rr * 1.25)}" ry="${f1(rr)}" fill="${c}" stroke="${INK}" stroke-width="1.6"/><path d="M${f1(bx - rr * 1.25)},${f1(by)}H${f1(bx + rr * 1.25)}" stroke="${INK}" stroke-width="1" opacity=".5"/><ellipse cx="${f1(bx - rr * 0.4)}" cy="${f1(by - rr * 0.4)}" rx="${f1(rr * 0.35)}" ry="${f1(rr * 0.2)}" fill="#fff" opacity=".55"/>`
        : `<circle cx="${f1(bx)}" cy="${f1(by)}" r="${f1(rr)}" fill="${c}" opacity=".85" stroke="${INK}" stroke-width="1.6"/><path d="M${f1(bx - rr)},${f1(by)}Q${f1(bx)},${f1(by + rr * 0.5)} ${f1(bx + rr)},${f1(by)}M${f1(bx)},${f1(by - rr)}V${f1(by + rr)}M${f1(bx - rr * 0.7)},${f1(by - rr * 0.7)}Q${f1(bx)},${f1(by - rr * 0.2)} ${f1(bx + rr * 0.7)},${f1(by - rr * 0.7)}" stroke="#8a7a5a" stroke-width="1.2" fill="none"/><circle cx="${f1(bx - rr * 0.35)}" cy="${f1(by - rr * 0.4)}" r="${f1(rr * 0.22)}" fill="#fff" opacity=".75"/>`;
    });
    // a string of little plastic flags (ธงทิว) across the room, dried squid on a line by the open front
    const bz = 2.9, bun = (u) => [lerp(-1.6, 2.05, u), 2.8 - 0.18 * Math.sin(Math.PI * u), bz];
    ce += `<path d="${Array.from({ length: 25 }, (_, i) => `${i ? "L" : "M"}${P2(R3(...bun(i / 24)))}`).join("")}" stroke="#6a5a4a" stroke-width="1.6" fill="none"/>`;
    for (let i = 0; i < 24; i++) { const [X0, Y0] = bun(i / 24), [X1, Y1] = bun((i + 0.8) / 24), a0 = R3(X0, Y0, bz), a1 = R3(X1, Y1, bz), m = R3((X0 + X1) / 2, (Y0 + Y1) / 2 - 0.13, bz); ce += `<path d="M${P2(a0)}L${P2(m)}L${P2(a1)}Z" fill="${["#e84a3a", "#f2c02a", "#3a9ad8", "#5ab84a", "#e86ab0", "#f2882a"][i % 6]}" stroke="${INK}" stroke-width="1"/>`; }
    const sqz = 3.3, [qa] = [R3(1.35, 2.42, sqz)], [qb] = [R3(2.0, 2.42, sqz)];
    ce += `<path d="M${P2(qa)}L${P2(qb)}" stroke="#6a5a4a" stroke-width="1.4"/>`;
    for (let i = 0; i < 4; i++) { const [x, y] = R3(1.45 + i * 0.16, 2.42, sqz), k = SHOP.F / sqz / 100; ce += `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(k / 2.4)})"><path d="M0,0V6" stroke="#6a5a4a" stroke-width="2"/><path d="M-9,6Q0,0 9,6L7,40Q0,46 -7,40Z" fill="#d89a5a" stroke="${INK}" stroke-width="1.6" opacity=".95"/>${[-6, -3, 0, 3, 6].map((dx) => `<path d="M${dx},40q${dx * 0.4},14 ${dx * 0.2},26" stroke="#c8864a" stroke-width="2.2" fill="none"/>`).join("")}<ellipse cx="0" cy="18" rx="4" ry="8" fill="#f2c890" opacity=".6"/></g>`; }
    const [fnx, fny] = R3(0.15, 2.58, 3.3), [fnt] = [R3(0.15, H, 3.3)[1]], bl = 0.62 * SHOP.F / 3.3;
    ce += `<path d="M${f1(fnx)},${f1(fnt)}V${f1(fny)}" stroke="#4a4a48" stroke-width="5"/>`;
    [15, 135, 255].forEach((a) => { const ex = Math.cos((a * Math.PI) / 180) * bl, ey = Math.sin((a * Math.PI) / 180) * bl * 0.26; ce += `<path d="M${f1(fnx)},${f1(fny)}L${f1(fnx + ex - ey * 0.4)},${f1(fny + ey - 6)}Q${f1(fnx + ex * 1.04)},${f1(fny + ey)} ${f1(fnx + ex + ey * 0.4)},${f1(fny + ey + 6)}Z" fill="#e8e2d2" stroke="${INK}" stroke-width="1.6"/>`; });
    ce += `<ellipse cx="${f1(fnx)}" cy="${f1(fny + 4)}" rx="22" ry="11" fill="#c8ccc8" stroke="${INK}" stroke-width="1.8"/>`;
    const [lbx, lby] = R3(-0.55, 2.35, 3.0), [, lbt] = R3(-0.55, H, 3.0);
    ce += `<path d="M${f1(lbx)},${f1(lbt)}V${f1(lby)}" stroke="#2e2a26" stroke-width="2"/><path d="M${f1(lbx - 26)},${f1(lby + 20)}L${f1(lbx - 8)},${f1(lby)}H${f1(lbx + 8)}L${f1(lbx + 26)},${f1(lby + 20)}Z" fill="#2e7a6a" stroke="${INK}" stroke-width="1.6"/><circle cx="${f1(lbx)}" cy="${f1(lby + 24)}" r="8" fill="#f8f2dc" stroke="${INK}" stroke-width="1.2"/>`;
    s += ce;
    // ---- the far table by the open front (behind anyone standing in the room): stools, a glass of water, the condiments, tissues ----
    s += stool3(1.0, 4.85) + table3(1.2, 1.92, 4.35, 5.05) + condiments(1.36, 0.72, 4.8) + tissue(1.78, 0.72, 4.85) + tumbler(1.58, 0.72, 4.5) + stool3(1.62, 3.95);
    put(L.set, s);
    // ---- in front of the cast (#id-front, after the actors in L.act): the counter ยาย stands behind, what's on it, the near table, stools, the cooler ----
    let g = `<path d="${Q3([-0.85, 0, 4.0], [0.5, 0, 4.0], [0.5, 0.91, 4.0], [-0.85, 0.91, 4.0])}" fill="url(#tdCtr)" stroke="${INK}" stroke-width="2.5"/>`;
    for (let X = -0.79; X < 0.5; X += 0.075) g += `<path d="${L3([X, 0.1, 4.0], [X, 0.91, 4.0])}" stroke="#2e6e68" stroke-width="1.6" opacity=".7"/>`;
    g += `<path d="${Q3([-0.85, 0, 4.0], [0.5, 0, 4.0], [0.5, 0.1, 4.0], [-0.85, 0.1, 4.0])}" fill="#2a4e4a" stroke="${INK}" stroke-width="1.6"/>`;
    g += `<path d="${Q3([-0.89, 0.95, 3.96], [0.54, 0.95, 3.96], [0.54, 0.95, 4.62], [-0.89, 0.95, 4.62])}" fill="#d8a46c" stroke="${INK}" stroke-width="2"/><path d="${Q3([-0.89, 0.905, 3.96], [0.54, 0.905, 3.96], [0.54, 0.95, 3.96], [-0.89, 0.95, 3.96])}" fill="#a8743e" stroke="${INK}" stroke-width="2"/>`;
    // a string of snack packets clipped along the front
    g += `<path d="${L3([-0.8, 0.86, 3.98], [0.45, 0.86, 3.98])}" stroke="#5a4a3a" stroke-width="1.6"/>`;
    for (let i = 0; i < 7; i++) { const X = -0.72 + i * 0.17, [bx, by] = R3(X, 0.86, 3.98), w = 30, h = 40, c = ["#f2c02a", "#e8402a", "#3a9ad8", "#5ab84a", "#f2882a", "#e84a9a", "#f2c02a"][i]; g += `<path d="M${f1(bx - w / 2)},${f1(by)}H${f1(bx + w / 2)}L${f1(bx + w / 2 - 2)},${f1(by + h)}Q${f1(bx)},${f1(by + h + 4)} ${f1(bx - w / 2 + 2)},${f1(by + h)}Z" fill="${c}" stroke="${INK}" stroke-width="1.4"/><circle cx="${f1(bx)}" cy="${f1(by + h * 0.5)}" r="7" fill="#fff" opacity=".75"/><rect x="${f1(bx - 3)}" y="${f1(by - 4)}" width="6" height="7" fill="#d8dcdc" stroke="${INK}" stroke-width="1"/>`; }
    // on the counter: two jars of sweets, a basket of limes, the QR stand, the cash tin and a calculator, a small fan
    const onC = (X, Z = 4.3) => R3(X, 0.95, Z);
    [[-0.74, "#e8402a"], [-0.58, "#3a9ad8"]].forEach(([X, c]) => { const [x, y] = onC(X); g += `<rect x="${f1(x - 18)}" y="${f1(y - 50)}" width="36" height="50" rx="7" fill="#e8f4f6" opacity=".7" stroke="${INK}" stroke-width="1.6"/>${Array.from({ length: 9 }, (_, i) => `<circle cx="${f1(x - 11 + (i % 3) * 11)}" cy="${f1(y - 8 - Math.floor(i / 3) * 10)}" r="4.5" fill="${["#f2c02a", "#e84a9a", "#5ab84a", c][i % 4]}"/>`).join("")}<rect x="${f1(x - 20)}" y="${f1(y - 58)}" width="40" height="10" rx="3" fill="${c}" stroke="${INK}" stroke-width="1.4"/><path d="M${f1(x - 12)},${f1(y - 44)}V${f1(y - 8)}" stroke="#fff" stroke-width="3" opacity=".7"/>`; });
    { const [x, y] = onC(-0.33); g += `<path d="M${f1(x - 30)},${f1(y - 16)}Q${f1(x)},${f1(y + 6)} ${f1(x + 30)},${f1(y - 16)}Z" fill="#c8a060" stroke="${INK}" stroke-width="1.6"/>${[-18, -6, 6, 18, -12, 0, 12].map((dx, i) => `<circle cx="${f1(x + dx)}" cy="${f1(y - 18 - (i > 3 ? 8 : 0))}" r="7" fill="#7ab83a" stroke="${INK}" stroke-width="1.2"/>`).join("")}`; }
    { const [x, y] = onC(-0.04, 4.15); g += `<path d="M${f1(x - 20)},${f1(y)}L${f1(x - 16)},${f1(y - 54)}H${f1(x + 16)}L${f1(x + 20)},${f1(y)}Z" fill="#f4f6f8" stroke="${INK}" stroke-width="1.6"/><rect x="${f1(x - 14)}" y="${f1(y - 52)}" width="28" height="10" fill="#1e4e94"/><text x="${f1(x)}" y="${f1(y - 44)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="7" fill="#fff">สแกนจ่าย</text><rect x="${f1(x - 11)}" y="${f1(y - 38)}" width="22" height="22" fill="#fff" stroke="${INK}" stroke-width="1"/>${[[0, 0], [14, 0], [0, 14]].map(([a, b]) => `<rect x="${f1(x - 10 + a)}" y="${f1(y - 37 + b)}" width="6" height="6" fill="${INK}"/>`).join("")}${Array.from({ length: 8 }, (_, i) => `<rect x="${f1(x - 3 + (i % 3) * 3)}" y="${f1(y - 30 + Math.floor(i / 3) * 4)}" width="2.4" height="2.4" fill="${INK}"/>`).join("")}`; }
    { const [x, y] = onC(0.22); g += `<rect x="${f1(x - 26)}" y="${f1(y - 22)}" width="44" height="22" rx="3" fill="#c8302a" stroke="${INK}" stroke-width="1.6"/><rect x="${f1(x - 26)}" y="${f1(y - 25)}" width="44" height="6" rx="2" fill="#e85a46" stroke="${INK}" stroke-width="1.2"/><rect x="${f1(x + 22)}" y="${f1(y - 12)}" width="18" height="12" rx="2" fill="#3a3c40" stroke="${INK}" stroke-width="1.2"/><rect x="${f1(x + 25)}" y="${f1(y - 10)}" width="12" height="3" fill="#bfe0a0"/>`; }
    { const [x, y] = onC(0.43, 4.4); g += `<path d="M${f1(x)},${f1(y)}V${f1(y - 26)}" stroke="#d8dcdc" stroke-width="4"/><ellipse cx="${f1(x)}" cy="${f1(y)}" rx="12" ry="4" fill="#e8ecec" stroke="${INK}" stroke-width="1.2"/><circle cx="${f1(x)}" cy="${f1(y - 36)}" r="17" fill="#cfe6ee" opacity=".85" stroke="${INK}" stroke-width="1.6"/><path d="M${f1(x - 12)},${f1(y - 36)}H${f1(x + 12)}M${f1(x)},${f1(y - 48)}V${f1(y - 24)}" stroke="#7a9aa8" stroke-width="1.4"/><circle cx="${f1(x)}" cy="${f1(y - 36)}" r="4" fill="#3a8ad0"/>`; }
    // the near table on the left with its stools (the cup insert's table is the far one by the open front)
    g += stool3(-1.1, 2.75) + table3(-0.95, -0.25, 2.55, 3.2) + condiments(-0.52, 0.72, 2.95) + tissue(-0.8, 0.72, 3.0) + stool3(-0.08, 2.95);
    // nearer still: the ice cooler by the open front, a stool left out in the middle of the floor, a pair of rubber sandals
    g += cooler3(1.3, 1.95, 2.45, 2.9) + stool3(0.1, 1.95);
    { const [x, y] = R3(-0.45, 0, 2.05), k = SHOP.F / 2.05 / 100; g += [0, 1].map((i) => `<g transform="translate(${f1(x + i * 9 * k)},${f1(y + i * 2 * k)}) rotate(${i ? 14 : -6})"><path d="M${f1(-4 * k)},0C${f1(-4.5 * k)},${f1(-2 * k)} ${f1(4 * k)},${f1(-2.4 * k)} ${f1(13 * k)},${f1(-1.6 * k)}C${f1(15 * k)},${f1(-0.6 * k)} ${f1(14 * k)},${f1(1.2 * k)} ${f1(11 * k)},${f1(1.3 * k)}C${f1(4 * k)},${f1(1.6 * k)} ${f1(-4 * k)},${f1(1.4 * k)} ${f1(-4 * k)},0Z" fill="#2a8ad0" stroke="${INK}" stroke-width="1.6"/><path d="M${f1(2 * k)},${f1(-1.2 * k)}Q${f1(5 * k)},${f1(-3.6 * k)} ${f1(8 * k)},${f1(-1.4 * k)}" stroke="#f2f2f2" stroke-width="${f1(0.9 * k)}" fill="none"/></g>`).join(""); }
    front(L, `${id}-front`, g);
    put(L.fg, `<g transform="translate(1100,-40)"><path d="M0,0V210M-24,0V160M24,0V250" stroke="#6a5a4a" stroke-width="3"/>${[[0, 220], [-24, 170], [24, 262]].map(([x, y]) => `<path d="M${x},${y + 16}c-12,-5 -15,-20 -8,-30q8,-6 16,0c8,10 5,25 -8,30z" fill="#f6e4d4" stroke="${INK}" stroke-width="2.4"/>`).join("")}</g>`);
    ST[id] = { kind: "shop", view: "room", clock: { cx: ccx, cy: ccy, R: CR } };
    const [h0, m0] = clockAngles(o.clock);
    clockDraw(id, h0, m0, 0, 0);
  }
  // spin the room clock's hands back o.hours (2) and settle on o.to ("07:40") — the room holds still; a little anticipation, a little
  // overshoot (o.ease "back.inOut(1.2)"), the spin taking o.spin (0.8) of the call; once settled, the second hand ticks on
  Tide.clockBack = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, hrs = o.hours ?? 2, [hE, mE] = clockAngles(o.to), spin = (o.spin ?? 0.8) * dur, E = gsap.parseEase(o.ease || "back.inOut(1.2)");
    const ang = (tt) => {
      if (tt >= spin) { const w = tt - spin; return [hE, mE, Math.floor(w) * 6 + 6 * sm(0, 0.1, w - Math.floor(w))]; }
      const k = E(clamp(tt / spin, 0, 1));
      return [lerp(hE + hrs * 30, hE, k), lerp(mE + hrs * 360, mE, k), lerp(hrs * 1080, 0, k)];
    };
    const draw = (tt) => { const [h, m, s] = ang(tt), m0 = ang(Math.max(0, tt - 0.07))[1]; clockDraw(id, h, m, s, tt < spin ? m0 - m : 0); };
    draw(0);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => draw(c.t) }, t0);
  };

  // ---------------- the "wall" view: a close insert of the photo and the clipping on the plank wall; ยาย's hand wipes the glass ----------------
  const WALL = { px: 470, py: 820, ps: 2.0, sh: [1250, 1230], l1: 430, l2: 400 };
  // ยาย's right hand from the back, fingers along −y from the wrist at (0, 0), pressing a checked cloth (ผ้าขาวม้า) to the glass
  const yaiHand = () => {
    const sk = "#c8946a", skD = "#a8744e";
    let g = `<path d="M-118,-150C-140,-200 -96,-262 -40,-268C10,-290 74,-262 104,-226C136,-186 124,-120 100,-86C120,-50 96,10 52,16C10,28 -40,22 -70,-6C-110,-30 -132,-90 -118,-150Z" fill="url(#tdPakama)" stroke="${INK}" stroke-width="3"/>`;
    g += `<path d="M-96,-180Q-40,-160 10,-196M-80,-90Q-20,-110 40,-80M30,-250Q50,-200 96,-180" stroke="#8a6a5a" stroke-width="3" fill="none" opacity=".5"/>`;
    g += `<path d="M-52,8C-60,-30 -60,-78 -48,-108L50,-110C60,-78 58,-30 50,8Z" fill="${sk}" stroke="${INK}" stroke-width="3.2"/>`;
    [[-36, -104, 82, -7, 23], [-12, -108, 92, -2, 24], [12, -106, 86, 4, 23], [34, -98, 66, 10, 20]].forEach(([x, y, len, a, w], i) => {
      g += `<g transform="translate(${x},${y}) rotate(${a})"><rect x="${-w / 2}" y="${-len}" width="${w}" height="${len + 8}" rx="${w / 2}" fill="${sk}" stroke="${INK}" stroke-width="3"/><rect x="${-w * 0.32}" y="${-len + 3}" width="${w * 0.64}" height="${w * 0.75}" rx="${w * 0.3}" fill="#e8c0a0" stroke="${skD}" stroke-width="1.4"/><path d="M${-w * 0.3},${-len * 0.45}q${w * 0.3},4 ${w * 0.6},0M${-w * 0.26},${-len * 0.48}q${w * 0.26},3 ${w * 0.52},0" stroke="${skD}" stroke-width="1.6" fill="none"/>${i === 2 ? `<rect x="${-w / 2 - 1}" y="${-len * 0.2}" width="${w + 2}" height="7" rx="3" fill="#e8b830" stroke="${INK}" stroke-width="1.6"/>` : ""}</g>`;
    });
    g += `<path d="M-48,-30C-80,-44 -100,-72 -104,-100C-106,-114 -88,-118 -82,-104C-76,-86 -64,-70 -44,-62Z" fill="${sk}" stroke="${INK}" stroke-width="3"/><path d="M-98,-108q6,-4 12,0" stroke="${skD}" stroke-width="1.6" fill="none"/>`;
    g += `<path d="M-34,-100q6,-6 12,0M-10,-104q6,-6 12,0M14,-102q6,-6 12,0M36,-94q5,-5 10,0" stroke="${skD}" stroke-width="2" fill="none"/><path d="M-20,-60Q0,-40 30,-56M-26,-30Q0,-20 24,-30" stroke="${skD}" stroke-width="1.6" fill="none" opacity=".7"/><path d="M-40,-94Q-10,-86 30,-96" stroke="#e8b890" stroke-width="5" fill="none" opacity=".5"/>`;
    return g;
  };
  function shopWall(L, id, o, P) {
    const r = mk(o.seed || 43), { px, py, ps } = WALL, gx0 = px - 98 * ps, gy0 = py - 74 * ps, gw = 196 * ps, gh = 148 * ps;
    put(L.sky, `<rect x="-800" y="-800" width="2800" height="3600" fill="#4f908a"/>`);
    let s = `<defs><linearGradient id="${id}-lg" gradientUnits="userSpaceOnUse" x1="-100" y1="0" x2="1180" y2="0"><stop offset="0" stop-color="#0e1a1c" stop-opacity=".42"/><stop offset=".55" stop-color="#0e1a1c" stop-opacity=".08"/><stop offset="1" stop-color="#fff6dc" stop-opacity=".18"/></linearGradient>
      <clipPath id="${id}-gc"><rect x="${f1(gx0)}" y="${f1(gy0)}" width="${f1(gw)}" height="${f1(gh)}"/></clipPath>
      <mask id="${id}-dm" maskUnits="userSpaceOnUse" x="-300" y="-300" width="1700" height="2600"><rect x="-300" y="-300" width="1700" height="2600" fill="#fff"/><path id="${id}-dtr" d="" stroke="#000" stroke-width="170" fill="none" stroke-linecap="round" stroke-linejoin="round"/></mask></defs>`;
    // the wall: turquoise planks with grain and knots, worn paint, nail heads, dark gaps
    for (let k = 0; k < 11; k++) {
      const x0 = -260 + k * 132, c = mix("#5aa49c", "#7cc4ba", r());
      s += `<rect x="${x0}" y="-300" width="132" height="2600" fill="${c}"/>`;
      for (let j = 0; j < 4; j++) { const gx = x0 + 18 + j * 30 + r() * 10; let d = `M${f1(gx)},-300`; for (let y = -200; y <= 2300; y += 100) d += `L${f1(gx + 5 * Math.sin(y * 0.01 + k + j))},${y}`; s += `<path d="${d}" stroke="#3e8078" stroke-width="2" fill="none" opacity=".3"/>`; }
      const ky = 100 + r() * 1700; s += `<ellipse cx="${f1(x0 + 40 + r() * 50)}" cy="${f1(ky)}" rx="9" ry="20" fill="none" stroke="#3e8078" stroke-width="2.5" opacity=".5"/>`;
      for (let j = 0; j < 3; j++) s += `<path d="${blob(x0 + r() * 132, r() * 1900, 20 + r() * 40, r, 7)}" fill="#e2f0ea" opacity="${f1(0.12 + r() * 0.12)}"/>`;
      [260, 1520].forEach((ny) => { s += `<circle cx="${x0 + 66}" cy="${ny}" r="5" fill="#5a5a56" stroke="${INK}" stroke-width="1.4"/><path d="M${x0 + 64},${ny + 4}v20" stroke="#8a4a2a" stroke-width="3" opacity=".35"/>`; });
      s += `<path d="M${x0},-300V2300" stroke="#264e4a" stroke-width="6" opacity=".75"/>`;
    }
    // a calendar cropped by the top edge: ธันวาคม, the 26th ringed in red pen
    s += `<g transform="translate(70,-30) rotate(-1.5)"><rect x="6" y="8" width="330" height="430" fill="#0e1a1c" opacity=".25"/><rect width="330" height="430" fill="#fbf8f0" stroke="${INK}" stroke-width="3"/><rect y="150" width="330" height="40" fill="#d8302a"/><text x="165" y="180" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="28" fill="#fff">ธันวาคม</text>
      <rect x="10" y="0" width="310" height="140" fill="#7ab8e0"/><path d="M10,140L120,70L200,110L320,60V140Z" fill="#3a8a4a"/><path d="M160,22L148,70H172Z" fill="#f2c840" stroke="${INK}" stroke-width="2"/>
      ${["อา", "จ", "อ", "พ", "พฤ", "ศ", "ส"].map((d, i) => `<text x="${30 + i * 45}" y="214" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="15" fill="${i === 0 ? "#d8302a" : "#5a5048"}">${d}</text>`).join("")}
      ${Array.from({ length: 31 }, (_, i) => { const n = i + 1, c = (n + 0) % 7, w = Math.floor((n + 0) / 7); return `<text x="${30 + c * 45}" y="${246 + w * 36}" text-anchor="middle" font-family="Kanit" font-weight="500" font-size="20" fill="${c === 0 ? "#d8302a" : "#2e2a26"}">${n}</text>`; }).join("")}
      <ellipse cx="${30 + (26 % 7) * 45}" cy="${239 + Math.floor(26 / 7) * 36}" rx="21" ry="16" fill="none" stroke="#d8302a" stroke-width="3" transform="rotate(-8 ${30 + (26 % 7) * 45} ${239 + Math.floor(26 / 7) * 36})"/></g>`;
    // the photo on its nail and string, its glass dusty until the cloth goes over it
    s += `<path d="M${px},${py - 250}L${px - 94},${py - 172}M${px},${py - 250}L${px + 94},${py - 172}" stroke="#3a2a1a" stroke-width="2.6"/><circle cx="${px}" cy="${py - 252}" r="7" fill="#6a6a66" stroke="${INK}" stroke-width="2"/>`;
    s += TideCast.photo(px, py, ps, { id: `${id}-photo` });
    let dust = `<rect x="${f1(gx0)}" y="${f1(gy0)}" width="${f1(gw)}" height="${f1(gh)}" fill="#f0eadc" opacity=".46"/>`;
    for (let k = 0; k < 70; k++) dust += `<circle cx="${f1(gx0 + r() * gw)}" cy="${f1(gy0 + r() * gh)}" r="${f1(1 + r() * 2.4)}" fill="#fbf8f0" opacity="${f1(0.4 + r() * 0.4)}"/>`;
    for (let k = 0; k < 6; k++) { const x = gx0 + r() * gw; dust += `<path d="M${f1(x)},${f1(gy0)}l${f1(-30 + r() * 60)},${f1(gh)}" stroke="#fbf8f0" stroke-width="${f1(6 + r() * 10)}" opacity=".18"/>`; }
    s += `<g clip-path="url(#${id}-gc)"><g mask="url(#${id}-dm)">${dust}</g><path id="${id}-glint" d="M-70,${f1(gy0 - 20)}H30L-150,${f1(gy0 + gh + 20)}H-250Z" fill="#ffffff" opacity="0"/></g>`;
    // the clipping, taped on with yellowed tape
    s += TideCast.clipping(800, 1230, 1.08, { id: `${id}-clip`, rot: 5 });
    s += [[660, 1088, -20], [950, 1110, 18], [645, 1350, 12]].map(([x, y, a]) => `<rect x="${x - 28}" y="${y - 10}" width="56" height="20" fill="#f2e6b8" opacity=".75" stroke="#c8b888" stroke-width="1" transform="rotate(${a} ${x} ${y})"/>`).join("");
    // ยาย's งอบ (the woven farmer's hat) hung on a nail
    s += `<g transform="translate(860,300) rotate(-8)"><path d="M0,-118V-60" stroke="#5a4a3a" stroke-width="2.4"/><circle cx="0" cy="-122" r="6" fill="#6a6a66" stroke="${INK}" stroke-width="1.8"/><ellipse cx="14" cy="18" rx="196" ry="72" fill="#0e1a1c" opacity=".22"/>
      <path d="M-190,10C-150,-40 -60,-70 0,-72C60,-70 150,-40 190,10C150,50 60,64 0,64C-60,64 -150,50 -190,10Z" fill="#d8b878" stroke="${INK}" stroke-width="3.4"/>
      ${Array.from({ length: 16 }, (_, i) => { const a = (i / 16) * Math.PI * 2; return `<path d="M0,0L${f1(Math.cos(a) * 188)},${f1(Math.sin(a) * 66)}" stroke="#a8884a" stroke-width="2" opacity=".55"/>`; }).join("")}
      ${[0.3, 0.55, 0.8].map((u) => `<ellipse cx="0" cy="0" rx="${f1(190 * u)}" ry="${f1(68 * u)}" fill="none" stroke="#b89a5a" stroke-width="2.4" opacity=".6"/>`).join("")}
      <path d="M-56,-10C-50,-60 50,-60 56,-10C40,10 -40,10 -56,-10Z" fill="#c8a462" stroke="${INK}" stroke-width="2.6"/><path d="M-40,-24C-30,-50 30,-50 40,-24" stroke="#e8cc8e" stroke-width="5" fill="none" opacity=".7"/><path d="M-60,-6C-40,8 40,8 60,-6" stroke="#8a2a2a" stroke-width="7" fill="none"/></g>`;
    // the ledge below: a cowrie, a small conch, a glass of water with a jasmine garland and a marigold (an offering)
    s += `<rect x="-200" y="1580" width="1500" height="26" fill="#a8743e" stroke="${INK}" stroke-width="3"/><rect x="-200" y="1606" width="1500" height="22" fill="#5a3a1e" opacity=".55"/><path d="M-200,1584H1300" stroke="#e2b880" stroke-width="3" opacity=".6"/>`;
    s += `<g transform="translate(260,1580)"><ellipse cx="0" cy="-2" rx="44" ry="10" fill="#000" opacity=".2"/><path d="M-40,0C-44,-30 -10,-48 20,-40C44,-32 46,-8 40,0Z" fill="#f2e2cc" stroke="${INK}" stroke-width="2.6"/><path d="M-30,-6Q0,-14 32,-6" stroke="#8a6a4a" stroke-width="2.2" fill="none"/>${[-24, -12, 0, 12, 24].map((x) => `<path d="M${x},-6v-4" stroke="#8a6a4a" stroke-width="1.6"/>`).join("")}</g>`;
    s += `<g transform="translate(420,1580)"><ellipse cx="0" cy="-2" rx="50" ry="10" fill="#000" opacity=".2"/><path d="M-50,-4C-50,-40 -10,-60 30,-50L56,-62L48,-40C56,-20 40,-2 10,0Z" fill="#f4d2b8" stroke="${INK}" stroke-width="2.6"/><path d="M-30,-14Q-10,-40 20,-38M-20,-6Q10,-24 34,-26" stroke="#c8906a" stroke-width="2.4" fill="none"/><path d="M30,-50Q40,-30 30,-12" stroke="#f8e8d8" stroke-width="5" fill="none"/></g>`;
    s += `<g transform="translate(860,1580)"><path d="M-26,0L-30,-70H30L26,0Z" fill="#e8f4f6" opacity=".6" stroke="#5a7a84" stroke-width="2.4"/><path d="M-28,-44H28L26,0H-26Z" fill="#a8dce6" opacity=".55"/><path d="M-18,-64V-8" stroke="#fff" stroke-width="5" opacity=".7"/>
      <path d="M0,-70C-40,-110 -10,-160 6,-190" stroke="#f8f8f0" stroke-width="12" fill="none" stroke-dasharray="9 4" stroke-linecap="round"/><path d="M6,-190q20,-14 30,6q-14,18 -30,-6z" fill="#f4a020" stroke="${INK}" stroke-width="2"/><path d="M0,-70C30,-100 40,-130 30,-160" stroke="#3a8a3a" stroke-width="4" fill="none"/></g>`;
    s += `<rect x="-300" y="-300" width="1700" height="2600" fill="url(#${id}-lg)"/>`;
    // the counter's top along the bottom of the frame, nearer than the wall: its edge, a jar of sweets, the QR stand
    s += `<path d="M-300,1790L1400,1772V2300H-300Z" fill="#c89464" stroke="${INK}" stroke-width="4"/><path d="M-300,1798L1400,1780" stroke="#f0c890" stroke-width="5" opacity=".7"/><path d="M-300,1840L1400,1822V2300H-300Z" fill="#a8743e" opacity=".6"/>`;
    s += `<g transform="translate(130,1800)"><rect x="-80" y="-180" width="160" height="200" rx="26" fill="#e8f4f6" opacity=".72" stroke="${INK}" stroke-width="4"/>${Array.from({ length: 12 }, (_, i) => `<circle cx="${-48 + (i % 4) * 32}" cy="${-30 - Math.floor(i / 4) * 34}" r="15" fill="${["#f2c02a", "#e84a9a", "#5ab84a", "#e8402a"][i % 4]}"/>`).join("")}<rect x="-90" y="-214" width="180" height="40" rx="10" fill="#e8402a" stroke="${INK}" stroke-width="4"/><path d="M-52,-160V-20" stroke="#fff" stroke-width="10" opacity=".6"/></g>`;
    s += `<g transform="translate(980,1785) rotate(3)"><path d="M-62,0L-52,-170H52L62,0Z" fill="#f4f6f8" stroke="${INK}" stroke-width="4"/><rect x="-46" y="-164" width="92" height="30" fill="#1e4e94"/><text x="0" y="-142" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="21" fill="#fff">สแกนจ่าย</text><rect x="-36" y="-122" width="72" height="72" fill="#fff" stroke="${INK}" stroke-width="2"/>${[[0, 0], [46, 0], [0, 46]].map(([a, b]) => `<rect x="${-33 + a}" y="${-119 + b}" width="20" height="20" fill="${INK}"/><rect x="${-29 + a}" y="${-115 + b}" width="12" height="12" fill="#fff"/><rect x="${-26 + a}" y="${-112 + b}" width="6" height="6" fill="${INK}"/>`).join("")}${Array.from({ length: 14 }, (_, i) => `<rect x="${-8 + (i % 4) * 9}" y="${-94 + Math.floor(i / 4) * 11}" width="7" height="7" fill="${INK}"/>`).join("")}</g>`;
    put(L.set, s);
    // ยาย's arm comes in from the right: the sleeve of her cream blouse with its lace cuff, her hand on the cloth (redrawn by wipeDraw)
    front(L, `${id}-wipeL`, `<g id="${id}-wipe" opacity="0"><g opacity=".2" fill="#0e1a1c"><path id="${id}-wsA" d=""/><path id="${id}-wsF" d=""/><circle id="${id}-wsH" r="120"/></g>
      <path id="${id}-wua" d="" fill="#efe0c4" stroke="${INK}" stroke-width="3.5"/><path id="${id}-wuaS" d="" fill="#d4c09c" opacity=".8"/><path id="${id}-wfa" d="" fill="#f6ead2" stroke="${INK}" stroke-width="3.5"/><path id="${id}-wfaS" d="" fill="#dccaa8" opacity=".8"/><path id="${id}-wfo" d="" stroke="#b8a482" stroke-width="3" fill="none" stroke-linecap="round"/>
      <g id="${id}-wh">${yaiHand()}</g><g id="${id}-wc"><path d="M-62,0Q-46,14 -31,0Q-15,14 0,0Q15,14 31,0Q46,14 62,0V-18H-62Z" fill="#efe2c4" stroke="${INK}" stroke-width="2.4"/>${[-46, -16, 16, 46].map((x) => `<circle cx="${x}" cy="-6" r="3.4" fill="none" stroke="#b8a47a" stroke-width="1.6"/>`).join("")}<path d="M-62,-18H62" stroke="#b8a47a" stroke-width="3"/></g></g>`);
    ST[id] = { kind: "shop", view: "wall", glass: [gx0, gy0, gw, gh] };
    wipeDraw(id, 0, -1);
  }
  // the cloth's centre on the glass at wipe progress p (0 … 1): it comes in from the right, rubs round in loops working from the right
  // side of the glass to the left, then lifts away
  const WP = { a: 0.13, b: 0.82 };
  const wipeAt = (p) => {
    const q = clamp((p - WP.a) / (WP.b - WP.a), 0, 1), th = q * Math.PI * 2 * 3.3;
    return [lerp(585, 372, sm(0, 1, q)) + 84 * Math.cos(th), WALL.py + 6 + 62 * Math.sin(th) + 26 * Math.sin(q * Math.PI * 1.3)];
  };
  function wipeDraw(id, t, p) {
    const g = el(`${id}-wipe`);
    if (p < 0 || p >= 0.985) { g.setAttribute("opacity", "0"); el(`${id}-dtr`).setAttribute("d", p >= 0.985 ? el(`${id}-dtr`).getAttribute("d") : ""); }
    // the clean trail the cloth has left (masks the dust off the glass)
    const pts = [];
    if (p > WP.a) for (let q = WP.a; q <= Math.min(p, WP.b) + 1e-6; q += 0.004) pts.push(wipeAt(q));
    el(`${id}-dtr`).setAttribute("d", pts.length > 1 ? `M${pts.map(P2).join("L")}` : "");
    // the glint runs across the clean glass once the hand has gone
    const G = ST[id].glass, gq = clamp((p - 0.86) / 0.13, 0, 1);
    el(`${id}-glint`).setAttribute("transform", `translate(${f1(G[0] + lerp(-40, G[2] + 300, gq))},0)`);
    el(`${id}-glint`).setAttribute("opacity", f1(0.55 * Math.sin(Math.PI * gq)));
    if (p < 0 || p >= 0.985) return;
    g.setAttribute("opacity", "1");
    // the cloth: in from off the right edge, the loops, then away
    const off = [1320, 1260], c = p < WP.a ? (() => { const k = gsap.parseEase("power2.out")(p / WP.a), e = wipeAt(WP.a); return [lerp(off[0], e[0], k), lerp(off[1], e[1], k)]; })()
      : p > WP.b ? (() => { const k = gsap.parseEase("power2.in")(clamp((p - WP.b) / 0.15, 0, 1)), e = wipeAt(WP.b); return [lerp(e[0], off[0], k), lerp(e[1], off[1] + 80, k)]; })() : wipeAt(p);
    const S0 = WALL.sh, dx = S0[0] - c[0], dy = S0[1] - c[1], dl = Math.hypot(dx, dy) || 1, W = [c[0] + (dx / dl) * 128, c[1] + (dy / dl) * 128];
    const E = elbowOf(S0, W, WALL.l1, WALL.l2, -1), ang = (Math.atan2(W[1] - E[1], W[0] - E[0]) * 180) / Math.PI + 90 + 8 * Math.sin(t * 9);
    el(`${id}-wua`).setAttribute("d", limb(S0, E, 136, 116));
    el(`${id}-wfa`).setAttribute("d", limb(E, W, 112, 98));
    // shade along the underside of the sleeve, creases at the elbow and where the cuff gathers
    const side = (A, B, wa, wb, f) => { const dx = B[0] - A[0], dy = B[1] - A[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l; return limb([A[0] - nx * wa * f, A[1] - ny * wa * f], [B[0] - nx * wb * f, B[1] - ny * wb * f], wa * 0.42, wb * 0.42); };
    el(`${id}-wuaS`).setAttribute("d", side(S0, E, 136, 116, 0.26));
    el(`${id}-wfaS`).setAttribute("d", side(E, W, 112, 98, 0.26));
    const cr = (u, w, bend) => { const px = lerp(E[0], W[0], u), py = lerp(E[1], W[1], u), dx = W[0] - E[0], dy = W[1] - E[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l; return `M${P2([px + nx * w, py + ny * w])}Q${P2([px + (dx / l) * bend, py + (dy / l) * bend])} ${P2([px - nx * w * 0.6, py - ny * w * 0.6])}`; };
    el(`${id}-wfo`).setAttribute("d", cr(0.12, 40, 18) + cr(0.22, 34, 14) + cr(0.78, 30, -10) + cr(0.86, 26, -8));
    el(`${id}-wsA`).setAttribute("d", limb([S0[0] - 40, S0[1] + 50], [E[0] - 40, E[1] + 50], 136, 116));
    el(`${id}-wsF`).setAttribute("d", limb([E[0] - 40, E[1] + 50], [W[0] - 26, W[1] + 34], 112, 98));
    el(`${id}-wsH`).setAttribute("cx", f1(c[0] - 20)); el(`${id}-wsH`).setAttribute("cy", f1(c[1] + 26));
    el(`${id}-wh`).setAttribute("transform", `translate(${P2(W)}) rotate(${f1(ang)})`);
    el(`${id}-wc`).setAttribute("transform", `translate(${P2(W)}) rotate(${f1(ang)}) translate(0,18)`);
  }
  // ยาย wipes the old photo: her hand comes in with the cloth, rubs the dust off the glass in loops, lifts away; a glint crosses the glass
  Tide.wipe = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 };
    wipeDraw(id, t0, 0);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => wipeDraw(id, t0 + c.t, c.t / dur) }, t0);
  };

  // ---------------- the "table" view: a glass of water on the red table by the open front; the sea glitters behind ----------------
  function shopTable(L, id, o, P) {
    const r = mk(o.seed || 47), HZ = 880;
    // outside (L.sky / L.far, so the shot can soften it): the sky, the sea with its glitter, the beach, a longtail out on the water
    let sk = `<defs><linearGradient id="${id}-skG" gradientUnits="userSpaceOnUse" x1="0" y1="-200" x2="0" y2="${HZ + 4}"><stop offset="0" stop-color="${P.sky[0]}"/><stop offset=".5" stop-color="${P.sky[1]}"/><stop offset=".85" stop-color="${P.sky[2]}"/><stop offset="1" stop-color="${P.sky[3]}"/></linearGradient></defs>`;
    sk += `<rect x="-800" y="-800" width="2800" height="${HZ + 810}" fill="url(#${id}-skG)"/><circle cx="880" cy="420" r="620" fill="url(#qkSun)" opacity="${P.sun}"/>`;
    for (let k = 0; k < 4; k++) sk += cloud2(-100 + k * 380 + r() * 100, HZ - 200 - r() * 260, 300 + r() * 200, 100 + r() * 40, r, P.cloud, P.cl[0], P.cl[1]);
    put(L.sky, sk);
    let f = `<defs><linearGradient id="${id}-seG" gradientUnits="userSpaceOnUse" x1="0" y1="${HZ}" x2="0" y2="1080"><stop offset="0" stop-color="${P.sea[1]}"/><stop offset=".35" stop-color="${P.sea[3]}"/><stop offset="1" stop-color="${P.sea[5]}"/></linearGradient></defs>`;
    f += karst(id, 0, 160, HZ + 4, 150, 140, r, P, 0.7).g + karst(id, 1, 900, HZ + 4, 110, 96, r, P, 0.78).g;
    f += `<rect x="-800" y="${HZ}" width="2800" height="200" fill="url(#${id}-seG)"/><rect x="-800" y="${HZ - 10}" width="2800" height="16" fill="${P.haze}" opacity=".45"/>`;
    for (let k = 0; k < 40; k++) { const y = HZ + 4 + Math.pow(r(), 1.4) * 190, x = -200 + r() * 1500; f += `<path d="M${f1(x)},${f1(y)}h${f1(10 + (y - HZ) * 0.5 * r())}" stroke="#fff" stroke-width="${f1(1.2 + (y - HZ) / 60)}" opacity="${f1(0.3 + r() * 0.4)}" stroke-linecap="round"/>`; }
    f += `<g transform="translate(700,${HZ + 60}) scale(.13)">${Tide.longtail({ hull: "#2e8a5a", band: "#f2c02a", no: false, water: P.sea[3], seed: 51, k: 2 })}</g>`;
    f += `<rect x="-800" y="1072" width="2800" height="400" fill="${P.sand[1]}"/><path d="M-800,1076Q540,1066 2000,1078" stroke="#fff" stroke-width="5" fill="none" opacity=".85"/><rect x="-800" y="1080" width="2800" height="30" fill="${P.wet[1]}" opacity=".6"/>`;
    const GL = Array.from({ length: 30 }, () => ({ x: 60 + r() * 960, y: HZ + 10 + Math.pow(r(), 0.7) * 170, R: 14 + r() * 30, f: 1.6 + r() * 3.4, ph: r() * 6, o: 0.6 + r() * 0.4 }));
    f += GL.map((q, k) => `<circle id="${id}-gl${k}" cx="${f1(q.x)}" cy="${f1(q.y)}" r="${f1(q.R)}" fill="url(#tdGlint)" opacity="0"/>`).join("");
    put(L.far, f);
    // the open front of the shop round the view: the eave and the awning's underside along the top, two posts, the rail at the deck's edge
    let s = `<path d="M-300,-300H1400V130Q540,90 -300,130Z" fill="#2e2c2a"/><path d="M-300,130Q540,90 1400,130V290H-300Z" fill="url(#tdTarpLit)"/>`;
    for (let k = 0; k < 14; k++) s += `<path d="M${-260 + k * 120},${f1(118 - Math.sin(k) * 4)}L${-300 + k * 128},290" stroke="#2a62a8" stroke-width="3" opacity=".45"/>`;
    let hem = "M-300,290";
    for (let x = -300; x < 1400; x += 60) hem += `Q${x + 30},330 ${x + 60},290`;
    s += `<path d="${hem}V270H-300Z" fill="#2a6ab0" stroke="#14325a" stroke-width="3"/><path d="M-300,276H1400" stroke="#7ab8f0" stroke-width="4" opacity=".6"/>`;
    s += `<rect x="-60" y="100" width="110" height="1200" fill="url(#tdWoodH)" stroke="${INK}" stroke-width="4"/><rect x="1020" y="100" width="110" height="1200" fill="url(#tdWoodH)" stroke="${INK}" stroke-width="4"/><path d="M-10,110V1290M1072,110V1290" stroke="#e2b880" stroke-width="5" opacity=".45"/>`;
    s += `<rect x="-300" y="1050" width="1700" height="34" fill="#b07a46" stroke="${INK}" stroke-width="3"/><path d="M-300,1056H1400" stroke="#e8bc84" stroke-width="3" opacity=".8"/>`;
    for (let x = -260; x < 1400; x += 58) s += `<rect x="${x}" y="1084" width="20" height="120" fill="#a8743e" stroke="${INK}" stroke-width="2"/>`;
    s += `<rect x="-300" y="1190" width="1700" height="120" fill="#9a6a3e"/>${Array.from({ length: 5 }, (_, k) => `<path d="M-300,${1204 + k * 22}H1400" stroke="#6a4424" stroke-width="2" opacity=".6"/>`).join("")}`;
    // two blue stools on the far side of the table
    s += `<g transform="translate(250,1236)"><path d="M-70,0L-78,60H-60L-52,0ZM70,0L78,60H60L52,0Z" fill="#1e4e8a" stroke="${INK}" stroke-width="2.4"/><path d="M-84,-8H84L76,12H-76Z" fill="url(#tdStool)" stroke="${INK}" stroke-width="2.6"/></g><g transform="translate(850,1230)"><path d="M-70,0L-78,60H-60L-52,0ZM70,0L78,60H60L52,0Z" fill="#1e4e8a" stroke="${INK}" stroke-width="2.4"/><path d="M-84,-8H84L76,12H-76Z" fill="url(#tdStool)" stroke="${INK}" stroke-width="2.6"/></g>`;
    // the table: a red top running toward us, its aluminium edge, the light off the sea lying on it
    s += `<path d="M30,1262H1050L1460,2040H-380Z" fill="url(#tdRedTop)" stroke="${INK}" stroke-width="4"/><path d="M30,1262H1050" stroke="#e8ecec" stroke-width="7"/><path d="M30,1268H1050" stroke="#9aa2a6" stroke-width="2"/>`;
    s += `<path d="M120,1290H960L1060,1480H20Z" fill="#fff4dc" opacity=".14"/><path d="M-100,1700L1180,1640" stroke="#ffffff" stroke-width="30" opacity=".05"/>`;
    // the condiment rack and a tissue box at the back of the table, a bowl of น้ำปลาพริก with a spoon at the front left
    s += `<g transform="translate(860,1330)"><ellipse cx="0" cy="6" rx="110" ry="16" fill="#1a1410" opacity=".25"/><rect x="-100" y="-10" width="200" height="16" rx="3" fill="#b8c0c2" stroke="${INK}" stroke-width="2.4"/><path d="M0,-10V-120" stroke="#9aa2a6" stroke-width="7"/><circle cx="0" cy="-124" r="9" fill="#c8ccce" stroke="${INK}" stroke-width="2"/>
      ${["#e8d8a0", "#a85a2a", "#c8382a", "#f4f0e8"].map((c, i) => `<g transform="translate(${-75 + i * 50},0)"><rect x="-21" y="-62" width="42" height="54" rx="8" fill="${c}" stroke="${INK}" stroke-width="2.4"/><rect x="-22" y="-70" width="44" height="12" rx="3" fill="#f4f6f6" stroke="${INK}" stroke-width="2"/><path d="M-12,-52V-16" stroke="#fff" stroke-width="5" opacity=".55"/>${i === 0 ? `<circle cx="4" cy="-30" r="5" fill="#3a8a3a"/><circle cx="-6" cy="-22" r="4" fill="#5aa84a"/>` : i === 2 ? `<circle cx="-4" cy="-30" r="4" fill="#8a1a10"/><circle cx="6" cy="-20" r="3" fill="#8a1a10"/>` : ""}</g>`).join("")}</g>`;
    s += `<g transform="translate(200,1320)"><rect x="-70" y="-60" width="140" height="62" rx="6" fill="#f48ab0" stroke="${INK}" stroke-width="2.6"/><path d="M-14,-60q14,-34 28,0" fill="#fff" stroke="${INK}" stroke-width="2"/><path d="M-56,-30h112" stroke="#fff" stroke-width="4" opacity=".55"/></g>`;
    s += `<g transform="translate(170,1740)"><ellipse cx="10" cy="40" rx="150" ry="34" fill="#1a1410" opacity=".22"/><path d="M-140,-10Q-130,60 0,64Q130,60 140,-10Z" fill="#f4f2ee" stroke="${INK}" stroke-width="3.4"/><ellipse cx="0" cy="-10" rx="140" ry="32" fill="#f8f6f2" stroke="${INK}" stroke-width="3.4"/><ellipse cx="0" cy="-6" rx="116" ry="22" fill="#a8642a"/>${[[-50, -10], [-20, -2], [16, -12], [44, -4], [-4, 6], [64, -14]].map(([x, y], i) => `<ellipse cx="${x}" cy="${y}" rx="${i % 2 ? 7 : 9}" ry="4" fill="${i % 3 ? "#d8302a" : "#3a9a3a"}"/>`).join("")}<path d="M-90,-10Q-40,-26 30,-22" stroke="#e8b070" stroke-width="5" fill="none" opacity=".6"/>
      <g id="${id}-spoon"><path d="M30,-8L190,-70" stroke="#c8ccce" stroke-width="11" stroke-linecap="round"/><path d="M30,-8L190,-70" stroke="#ffffff" stroke-width="3" opacity=".7"/><ellipse cx="22" cy="-4" rx="28" ry="12" fill="#d8dcdc" stroke="${INK}" stroke-width="2.4" transform="rotate(-20 22 -4)"/></g></g>`;
    // the glass of water (#id-cup trembles): its shadow and the caustic it throws toward us, the water, the rings on the surface, the glass
    const CX = 540, BY0 = 1500, TOP = 1150, RW = 96, BW = 76, WS = 1272, wW = BW + ((RW - BW) * (BY0 - WS)) / (BY0 - TOP);
    let c = `<defs><linearGradient id="${id}-shG" gradientUnits="userSpaceOnUse" x1="0" y1="${BY0}" x2="0" y2="${BY0 + 300}"><stop offset="0" stop-color="#4a1208" stop-opacity=".4"/><stop offset="1" stop-color="#4a1208" stop-opacity="0"/></linearGradient>
      <clipPath id="${id}-wc"><path d="M${f1(CX - wW)},${WS}L${CX - BW},${BY0}H${CX + BW}L${f1(CX + wW)},${WS}Z"/></clipPath></defs>`;
    c += `<path d="M${CX - BW},${BY0}C${CX - BW - 30},${BY0 + 140} ${CX - 70},${BY0 + 260} ${CX - 40},${BY0 + 300}H${CX + 40}C${CX + 70},${BY0 + 260} ${CX + BW + 30},${BY0 + 140} ${CX + BW},${BY0}Z" fill="url(#${id}-shG)"/>`;
    c += `<g id="${id}-caus"><ellipse cx="${CX}" cy="${BY0 + 120}" rx="70" ry="40" fill="url(#tdCaus)"/>${[0, 1, 2].map((k) => `<path id="${id}-cw${k}" d="M${CX - 50 + k * 10},${BY0 + 100 + k * 16}q25,-10 50,0t50,0" stroke="#fffbe6" stroke-width="4" fill="none" opacity=".75" stroke-linecap="round"/>`).join("")}</g>`;
    c += `<ellipse cx="${CX}" cy="${TOP}" rx="${RW}" ry="17" fill="none" stroke="#7a9aa4" stroke-width="2.4" opacity=".7"/>`;
    c += `<path d="M${f1(CX - wW)},${WS}L${CX - BW},${BY0}H${CX + BW}L${f1(CX + wW)},${WS}Z" fill="#c4eef4" opacity=".55"/>`;
    // seen through the water: the rail's balusters magnified and pulled apart, the red of the table at the bottom, a few bubbles on the glass
    c += `<g clip-path="url(#${id}-wc)">${[-2, -1, 0, 1, 2].map((i) => `<rect x="${f1(CX + i * 46 - 13)}" y="${WS}" width="26" height="${f1(BY0 - WS)}" fill="#a8743e" opacity=".22"/>`).join("")}<rect x="${CX - 100}" y="${WS + 6}" width="200" height="26" fill="${P.sea[4]}" opacity=".35"/><rect x="${CX - 100}" y="${BY0 - 60}" width="200" height="60" fill="#e04a36" opacity=".16"/>
      ${[[-50, 40, 4], [40, 90, 3], [-20, 150, 3.5], [55, 170, 2.5], [-60, 120, 2.5], [10, 60, 2]].map(([dx, dy, rr]) => `<circle cx="${CX + dx}" cy="${WS + dy}" r="${rr}" fill="none" stroke="#ffffff" stroke-width="1.4" opacity=".8"/>`).join("")}</g>`;
    c += `<ellipse id="${id}-ws" cx="${CX}" cy="${WS}" rx="${f1(wW)}" ry="15" fill="#e2f6fa" stroke="#ffffff" stroke-width="3"/>`;
    c += [0, 1, 2, 3].map((k) => `<ellipse id="${id}-r${k}" cx="${CX}" cy="${WS}" rx="1" ry="1" fill="none" stroke="#6aa8b8" stroke-width="2.4" opacity="0"/>`).join("");
    c += `<path d="M${CX - RW},${TOP}L${CX - BW},${BY0}M${CX + RW},${TOP}L${CX + BW},${BY0}" stroke="${INK}" stroke-width="3" opacity=".75"/><path d="M${CX - RW + 6},${TOP + 8}L${CX - BW + 6},${BY0 - 10}" stroke="#ffffff" stroke-width="7" opacity=".7"/><path d="M${CX + RW - 16},${TOP + 20}L${CX + BW - 14},${BY0 - 30}" stroke="#ffffff" stroke-width="4" opacity=".5"/>`;
    c += `<ellipse cx="${CX}" cy="${BY0}" rx="${BW}" ry="13" fill="#d8eef2" opacity=".75" stroke="${INK}" stroke-width="3"/><ellipse cx="${CX}" cy="${BY0 - 6}" rx="${BW - 10}" ry="8" fill="none" stroke="#ffffff" stroke-width="3" opacity=".7"/>`;
    c += `<path d="M${CX - RW},${TOP}A${RW},17 0 0 0 ${CX + RW},${TOP}" stroke="${INK}" stroke-width="3" fill="none"/><path d="M${CX - RW + 10},${TOP + 4}A${RW - 10},13 0 0 0 ${CX + RW - 10},${TOP + 4}" stroke="#ffffff" stroke-width="4" fill="none" opacity=".8"/>`;
    s += `<g id="${id}-cup">${c}</g>`;
    put(L.set, s);
    ST[id] = { kind: "shop", view: "table", GL, cup: { x: CX, y: WS, rx: wW, ry: 15 } };
    cupDraw(id, 0, 0);
  }
  function cupDraw(id, t, a) {
    const S = ST[id], C = S.cup, dx = a * 1.8 * (Math.sin(t * 47) + 0.6 * Math.sin(t * 83 + 1.3)), dy = a * 0.9 * Math.sin(t * 61 + 0.4);
    el(`${id}-cup`).setAttribute("transform", `translate(${f1(dx)},${f1(dy)})`);
    for (let k = 0; k < 4; k++) {
      const q = (t / 0.55 + k / 4) % 1, e = el(`${id}-r${k}`);
      e.setAttribute("rx", f1(Math.max(1, C.rx * 0.92 * q)));
      e.setAttribute("ry", f1(Math.max(1, C.ry * 0.92 * q)));
      e.setAttribute("opacity", f1(clamp(a * 2.4, 0, 0.9) * (1 - q) * sm(0, 0.12, q)));
    }
    el(`${id}-ws`).setAttribute("ry", f1(C.ry * (1 + a * 0.2 * Math.sin(t * 31))));
    el(`${id}-caus`).setAttribute("transform", `translate(${f1(dx * 2.4)},${f1(dy * 2.4)})`);
    for (let k = 0; k < 3; k++) el(`${id}-cw${k}`).setAttribute("transform", `translate(${f1(8 * Math.sin(t * 1.7 + k * 2) + a * 6 * Math.sin(t * 29 + k))},0)`);
    S.GL.forEach((q, k) => el(`${id}-gl${k}`).setAttribute("opacity", f1(q.o * Math.pow(Math.max(0, Math.sin(t * q.f + q.ph)), 3))));
    el(`${id}-spoon`).setAttribute("transform", `rotate(${f1(a * 3 * Math.sin(t * 53))} 30 -8)`);
  }
  // the glass of water barely trembles: faint rings run out across the surface, the glass shivers a pixel or two, the caustic quivers;
  // o.amp (0.3) how hard, o.grow true makes it build through the call; the sea keeps glittering behind
  Tide.cupShake = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, amp = o.amp ?? 0.3, A = (tt) => amp * sm(0, 0.35, tt) * (o.grow ? lerp(0.35, 1, tt / dur) : 1);
    cupDraw(id, t0, 0);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => cupDraw(id, t0 + c.t, A(c.t)) }, t0);
  };

  // ---------------- the "door" view: the shop's front from the beach after everyone has gone ----------------
  // a low camera on the sand (the eye 1 m up, horizon y 1130): the folding doors left open on the dark shop, the empty space on the back
  // wall where the photo hung (the clipping still there), one of ยาย's brown slippers on the middle step, the coconut-rib broom fallen
  // down the steps, a stool tipped over, the menu sheet flapping on the post; ยาย's prints — one sandal, one bare foot — go off to the left,
  // toward the hotel. Tide.doorWind moves it (a loose door leaf swings, the sheet flaps, the awning's hem and the shell chime stir).
  function shopDoor(L, id, o, P) {
    const r = mk(o.seed || 53), HZ = 1130;
    sky(L, id, P, HZ, { seed: (o.seed || 53) + 1, sunX: 1500, sunY: 140 });
    // far: the jungle hill behind the village (the warning tower on its shoulder, its beacon blinking), the hotel's upper floors at the left
    let f = `<path d="M-400,${HZ}L-400,560Q-100,380 260,330Q620,250 900,300Q1200,360 1500,520V${HZ}Z" fill="${P.green[0]}"/>`;
    for (let k = 0; k < 60; k++) { const x = -300 + r() * 1700, y = 360 + r() * 700; f += crown(x, y, 50 + r() * 50, r, [T(P.green[0], -0.1), P.green[1], P.green[2], T(P.green[2], 0.2)], 7); }
    f += `<rect x="-400" y="300" width="1900" height="${HZ - 300}" fill="${P.haze}" opacity=".3"/>`;
    f += Tide.tower(1010, 980, 0.42, id);
    put(L.far, f);
    let m = `<g transform="translate(-438,1250) scale(2.6)">${hotel(id + "h", 0, 0, 1)}</g>`;
    m += coco(1180, 1250, 1.25, -0.08, (o.seed || 53) + 9, { pal: P.leaf, fl: 0.8 });
    put(L.mid, m);
    // the sand in front, with the morning's prints scuffed into it and ยาย's going off to the left
    let s = `<defs><linearGradient id="${id}-sG" gradientUnits="userSpaceOnUse" x1="0" y1="${HZ + 120}" x2="0" y2="1950"><stop offset="0" stop-color="${P.sand[2]}"/><stop offset=".5" stop-color="${P.sand[1]}"/><stop offset="1" stop-color="${P.sand[0]}"/></linearGradient>
      <linearGradient id="${id}-iG" gradientUnits="userSpaceOnUse" x1="0" y1="560" x2="0" y2="1220"><stop offset="0" stop-color="#14201e"/><stop offset=".7" stop-color="#22302e"/><stop offset="1" stop-color="#3a4440"/></linearGradient></defs>`;
    s += `<rect x="-400" y="${HZ + 100}" width="1900" height="900" fill="url(#${id}-sG)"/>`;
    for (let k = 0; k < 30; k++) { const y = HZ + 240 + Math.pow(r(), 0.8) * 560, x = -200 + r() * 1500, w = 40 + r() * 160 * ((y - HZ) / 600); s += `<path d="M${f1(x)},${f1(y)}q${f1(w / 2)},${f1(-4 - r() * 4)} ${f1(w)},0" stroke="#fff" stroke-width="2.5" fill="none" opacity=".35"/>`; }
    for (let k = 0; k < 26; k++) { const y = HZ + 260 + r() * 520, sc = (y - HZ) / 500, x = -150 + r() * 1400, a = r() * 180; s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(16 * sc)}" ry="${f1(6 * sc)}" fill="${T(P.sand[2], -0.18)}" opacity=".35" transform="rotate(${f1((a - 90) * 0.15)} ${f1(x)} ${f1(y)})"/>`; }
    // ยาย's trail: one brown sandal, one bare foot, from the foot of the steps off to the left toward the hotel (the toes point the way)
    const dent = T(P.sand[2], -0.32), lip = "#fbf2dc";
    const print = (x, y, sc, bare) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(sc)},${f1(sc * 0.55)}) rotate(4)">${bare
      ? `<path d="M-30,-2C-32,-14 -16,-17 -4,-12C6,-8 14,-10 26,-12C40,-14 46,-6 44,2C42,10 32,12 22,9C12,6 4,6 -6,10C-20,15 -28,8 -30,-2Z" fill="${dent}" opacity=".85"/><path d="M-26,6C-18,12 -6,8 4,7" stroke="${lip}" stroke-width="3" fill="none" opacity=".75"/>${[[-42, -14, 7], [-45, -4, 5.5], [-44, 5, 5], [-41, 13, 4.5], [-36, 20, 4]].map(([a, b, rr]) => `<ellipse cx="${a}" cy="${b}" rx="${rr}" ry="${f1(rr * 0.85)}" fill="${dent}" opacity=".85"/>`).join("")}`
      : `<path d="M-44,0C-44,-12 -20,-17 8,-15C30,-13 46,-8 46,1C46,10 30,14 6,13C-22,12 -44,10 -44,0Z" fill="${dent}" opacity=".85"/><path d="M-26,-14Q-22,0 -26,13M-18,-15Q-14,0 -18,14" stroke="${T(P.sand[2], -0.5)}" stroke-width="2.4" fill="none" opacity=".6"/><path d="M-42,5C-30,12 10,14 40,7" stroke="${lip}" stroke-width="3" fill="none" opacity=".7"/>`}</g>`;
    [[492, 1446, 1.3, 0], [384, 1484, 1.45, 1], [270, 1526, 1.62, 0], [150, 1572, 1.8, 1], [24, 1622, 2.0, 0], [-110, 1676, 2.2, 1]].forEach(([x, y, sc, b]) => { s += print(x, y, sc, b); });
    // things the wind and the hurry left on the sand: shells, a plastic cup, a crumpled bag, twigs, streaks of blown sand
    for (let k = 0; k < 14; k++) { const x = 80 + r() * 960, y = 1560 + r() * 340, sz = 7 + r() * 9; s += `<path d="M${f1(x - sz)},${f1(y)}a${f1(sz)},${f1(sz * 0.7)} 0 0 1 ${f1(sz * 2)},0l${f1(-sz)},${f1(sz * 0.5)}z" fill="${["#f8f2ea", "#f4d8cc", "#e8dcc0"][k % 3]}" stroke="#9a8a72" stroke-width="1.4"/>`; }
    s += `<g transform="translate(760,1700) rotate(70)"><path d="M-18,-26L18,-26L13,26H-13Z" fill="#f4f6f6" opacity=".9" stroke="#8a9a9e" stroke-width="2"/><ellipse cx="0" cy="-26" rx="18" ry="5" fill="#dfe6e8" stroke="#8a9a9e" stroke-width="2"/></g>`;
    s += `<path d="M880,1820q30,-30 60,-8q20,-26 50,0q-10,30 -50,24q-30,16 -60,-16z" fill="#e8eef0" opacity=".85" stroke="#9aa6aa" stroke-width="2"/>`;
    for (let k = 0; k < 8; k++) { const x = -40 + r() * 1100, y = 1400 + r() * 480; s += `<path d="M${f1(x)},${f1(y)}h${f1(80 + r() * 160)}" stroke="#fbf2dc" stroke-width="3" opacity=".35" stroke-linecap="round"/>`; }
    put(L.set, s);
    // the shop: the dark inside seen through the open folding doors, the empty space where the photo hung, the clipping still there
    const DX = (X) => 540 + 220 * X, YD = 1218, YR = 600;
    let sh = `<rect x="-300" y="${YR}" width="1700" height="${YD - YR}" fill="url(#${id}-iG)"/>`;
    sh += `<rect x="${f1(DX(-0.6))}" y="${YR + 60}" width="${f1(DX(1.45) - DX(-0.6))}" height="360" fill="#2e4a46" opacity=".55"/>`;
    for (let k = 0; k < 9; k++) sh += `<path d="M${f1(DX(-0.6) + k * 52)},${YR + 60}V${YR + 420}" stroke="#1a2a28" stroke-width="2" opacity=".6"/>`;
    sh += `<rect x="560" y="850" width="56" height="44" fill="#4a6a64" opacity=".85"/><rect x="560" y="850" width="56" height="44" fill="none" stroke="#1a2a28" stroke-width="1.5" opacity=".6"/><circle cx="588" cy="836" r="2.6" fill="#8a8a86"/><path d="M588,836L566,850M588,836L610,850" stroke="#5a5a56" stroke-width="1" opacity=".5"/>`;
    sh += `<g opacity=".8">${TideCast.clipping(650, 872, 0.13, { rot: -4 })}</g><circle cx="740" cy="800" r="26" fill="#3a5450" stroke="#1a2a28" stroke-width="2"/><path d="M740,800V782M740,800l12,6" stroke="#1a2a28" stroke-width="3"/>`;
    sh += `<path d="M${f1(DX(-0.6))},1010H${f1(DX(0.9))}V${YD}H${f1(DX(-0.6))}Z" fill="#1a2624"/><path d="M${f1(DX(-0.6))},1010H${f1(DX(0.9))}" stroke="#4a5a54" stroke-width="3"/>`;
    sh += `<path d="M${f1(DX(-0.5))},${YD}L${f1(DX(-0.2))},1150H${f1(DX(1.2))}L${f1(DX(1.4))},${YD}Z" fill="#e8dcb8" opacity=".16"/>`;
    sh += [[-0.3, "#c8742a"], [0.15, "#4a7a8a"], [0.6, "#c8a02a"], [1.1, "#4a7a6a"]].map(([X, c]) => `<path d="M${f1(DX(X))},${YR}V${YR + 40}" stroke="#2a2a28" stroke-width="1.5"/><circle cx="${f1(DX(X))}" cy="${YR + 52}" r="12" fill="${c}" opacity=".45"/>`).join("");
    // the front wall either side, the folding doors (บานเฟี้ยม): folded back in the middle, shut on the left, a loose leaf on the right
    const leaf = (x, w, c = "#4f948e") => `<rect x="${f1(x)}" y="${YR}" width="${f1(w)}" height="${YD - YR}" fill="${c}" stroke="${INK}" stroke-width="3"/><rect x="${f1(x + w * 0.16)}" y="${YR + 40}" width="${f1(w * 0.68)}" height="230" fill="none" stroke="#2e6a64" stroke-width="3"/><rect x="${f1(x + w * 0.16)}" y="${YR + 320}" width="${f1(w * 0.68)}" height="230" fill="none" stroke="#2e6a64" stroke-width="3"/><path d="M${f1(x + w * 0.2)},${YR + 44}V${YR + 266}" stroke="#a8d8d0" stroke-width="3" opacity=".4"/>`;
    for (let k = 0; k < 5; k++) sh += leaf(DX(-2.6) + k * 98, 98);
    sh += `<g transform="translate(${f1(DX(-0.6))},0) scale(.32,1)">${leaf(0, 98)}${leaf(98, 98)}</g><g transform="translate(${f1(DX(1.45))},0) scale(-.3,1)">${leaf(0, 98)}${leaf(98, 98)}</g>`;
    sh += `<g id="${id}-dr">${leaf(DX(1.6), 98, "#58a098")}</g>`;
    for (let k = 0; k < 3; k++) sh += leaf(DX(2.15) + k * 98, 98);
    // posts, the eave, the blue awning with its scalloped hem (redrawn), the tin roof, the sign
    [-2.65, -0.62, 1.47, 3.45].forEach((X) => { sh += `<rect x="${f1(DX(X) - 14)}" y="430" width="28" height="${YD - 430}" fill="url(#tdWoodH)" stroke="${INK}" stroke-width="3"/>`; });
    sh += `<path d="M-200,470H1400L1480,540H-280Z" fill="url(#tdTin)" stroke="${INK}" stroke-width="3"/><path id="${id}-awn" d="" fill="url(#tdTarp)" stroke="${INK}" stroke-width="3"/><path d="M-280,548H1480" stroke="#7ab8f0" stroke-width="5" opacity=".6"/>`;
    sh += `<rect x="262" y="250" width="740" height="170" rx="12" fill="#f8f4ea" stroke="#1e4e94" stroke-width="10"/><path d="M340,420V470M930,420V470" stroke="#6a5a4a" stroke-width="12"/>
      <text x="632" y="352" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="96" fill="#d8302a" stroke="#7a1410" stroke-width="2.5">ร้านยายพร</text>
      <text x="632" y="400" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="36" fill="#1e4e94">อาหารทะเลสด · ปลาเผา หมึกย่าง</text>`;
    // the shell chime under the eave, the menu sheet taped to the post (redrawn), the ice cooler with its lid thrown open
    sh += `<g id="${id}-chime" transform="translate(${f1(DX(0.2))},560)"><path d="M-14,0V70M0,0V96M14,0V58" stroke="#6a5a4a" stroke-width="2"/>${[[-14, 78], [0, 104], [14, 66]].map(([x, y]) => `<path d="M${x},${y + 10}c-9,-3 -11,-14 -6,-21q6,-4 12,0c6,7 4,18 -6,21z" fill="#f6e4d4" stroke="${INK}" stroke-width="1.8"/>`).join("")}</g>`;
    sh += `<g transform="translate(${f1(DX(1.47) + 16)},820)"><rect x="-4" y="-6" width="26" height="12" fill="#f2e6b8" opacity=".85" transform="rotate(-12)"/><g id="${id}-pap"><path d="M0,0H96V130H0Z" fill="#fbf8f0" stroke="${INK}" stroke-width="2.4"/>${["ปลาเผา", "หมึกย่าง", "ข้าวผัด"].map((t, i) => `<text x="10" y="${30 + i * 30}" font-family="Mali" font-weight="700" font-size="17" fill="#2e2a26">${t}</text>`).join("")}</g></g>`;
    // the deck: its front edge on stumps, the dark space under it
    sh += `<rect x="-300" y="${YD}" width="1700" height="132" fill="#1a1410" opacity=".55"/>${[-2.4, -1.2, 2.1, 3.2].map((X) => `<rect x="${f1(DX(X) - 12)}" y="${YD}" width="24" height="132" fill="#bcb6aa" stroke="${INK}" stroke-width="2.4"/>`).join("")}`;
    sh += `<rect x="-300" y="${YD - 18}" width="1700" height="18" fill="#c89464" stroke="${INK}" stroke-width="2.4"/><rect x="-300" y="${YD}" width="1700" height="26" fill="#a8743e" stroke="${INK}" stroke-width="2.4"/>`;
    sh += `<g transform="translate(${f1(DX(-1.9))},${YD - 10})"><rect x="-60" y="-80" width="120" height="80" rx="8" fill="#f4f6f4" stroke="${INK}" stroke-width="2.6"/><path d="M-60,-80L-74,-148L52,-136L60,-80Z" fill="#dfe6e8" stroke="${INK}" stroke-width="2.4"/><text x="0" y="-30" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="20" fill="#2a6ab8">น้ำแข็ง</text></g>`;
    sh += `<path d="M-300,${YD - 18}H1400V${YD + 40}H-300Z" fill="#1a1410" opacity=".18"/>`;
    // the steps down to the sand
    const ST3 = [[1251, 1259, 1294, 1.0], [1294, 1305, 1342, 1.06], [1342, 1358, 1398, 1.13]];
    ST3.forEach(([yb, yf, yr, k]) => { const w = 170 * k, cx = DX(0.42); sh += `<path d="M${f1(cx - w + 6)},${yb}H${f1(cx + w - 6)}L${f1(cx + w)},${yf}H${f1(cx - w)}Z" fill="#d8a46c" stroke="${INK}" stroke-width="2.2"/><rect x="${f1(cx - w)}" y="${yf}" width="${f1(w * 2)}" height="${yr - yf}" fill="#a8743e" stroke="${INK}" stroke-width="2.4"/><path d="M${f1(cx - w)},${yf + 4}H${f1(cx + w)}" stroke="#e2b880" stroke-width="3" opacity=".6"/>`; });
    // the coconut-rib broom (ไม้กวาดทางมะพร้าว) fallen from the deck down past the steps, its ribs fanned out on the sand
    { const A = [985, 1200], B = [835, 1372]; sh += `<path d="M${A[0]},${A[1]}L${B[0]},${B[1]}" stroke="#2a1c10" stroke-width="12" stroke-linecap="round" opacity=".25" transform="translate(6,8)"/><path d="M${A[0]},${A[1]}L${B[0]},${B[1]}" stroke="#c8a870" stroke-width="10" stroke-linecap="round"/><path d="M${A[0]},${A[1]}L${B[0]},${B[1]}" stroke="#ecd8a8" stroke-width="3"/>`;
      let ribs = ""; for (let i = 0; i < 34; i++) { const u = i / 33, ex = B[0] - 150 + u * 120 + Math.sin(i * 3.1) * 8, ey = B[1] + 120 + Math.sin(u * Math.PI) * 26 - u * 40; ribs += `M${B[0]},${B[1]}Q${f1((B[0] + ex) / 2 + 6)},${f1((B[1] + ey) / 2 + 4)} ${f1(ex)},${f1(ey)}`; }
      sh += `<path d="${ribs}" stroke="#2a1c10" stroke-width="3" fill="none" opacity=".2" transform="translate(6,6)"/><path d="${ribs}" stroke="#7a6a3e" stroke-width="2.6" fill="none"/><path d="${ribs}" stroke="#a89660" stroke-width="1.2" fill="none" opacity=".8"/><path d="M${B[0] - 12},${B[1] - 6}l24,14M${B[0] - 8},${B[1] - 14}l24,14" stroke="#d8302a" stroke-width="6" stroke-linecap="round"/>`; }
    // one of ยาย's brown sandals on the middle step: the sole, the wide band across it
    sh += `<g transform="translate(${f1(DX(0.05))},1290) rotate(-10) scale(1.15,.8)"><ellipse cx="6" cy="18" rx="64" ry="12" fill="#2a1c10" opacity=".3"/><path d="M-58,4C-60,-14 -40,-24 -14,-22C8,-20 20,-26 40,-24C60,-22 64,-6 62,4C60,16 44,22 24,20C6,18 -6,22 -24,24C-46,26 -56,18 -58,4Z" fill="#3a2414" stroke="${INK}" stroke-width="3"/>
      <path d="M-52,1C-53,-12 -38,-18 -14,-16C8,-14 20,-20 38,-18C54,-16 57,-5 55,3C52,12 40,15 24,13C6,11 -8,15 -24,17C-42,18 -51,12 -52,1Z" fill="#9a6a3e"/><path d="M-46,-6C-30,-12 20,-14 50,-8" stroke="#c8925a" stroke-width="2.4" fill="none" opacity=".8"/>
      <path d="M14,-26C10,-4 12,10 18,24L38,22C34,8 34,-8 38,-26Z" fill="#5a3a22" stroke="${INK}" stroke-width="2.8"/><path d="M20,-20C18,-4 20,8 24,18" stroke="#9a6a40" stroke-width="2.4" fill="none"/></g>`;
    // a blue plastic stool knocked over on the sand left of the steps, upside down, its legs in the air
    sh += `<g transform="translate(250,1420) rotate(-8)"><ellipse cx="6" cy="6" rx="110" ry="14" fill="#1a1410" opacity=".25"/><path d="M-60,-20L-74,-150H-50L-38,-20ZM60,-20L74,-150H50L38,-20Z" fill="#1e4e8a" stroke="${INK}" stroke-width="2.8"/><path d="M-30,-20L-30,-130H-14L-16,-20ZM30,-20L30,-130H14L16,-20Z" fill="#163e70" stroke="${INK}" stroke-width="2.4"/><path d="M-66,-96H66" stroke="#1e4e8a" stroke-width="7"/>
      <path d="M-82,0Q-84,-14 -70,-20H70Q84,-14 82,0Q60,8 0,8Q-60,8 -82,0Z" fill="url(#tdStool)" stroke="${INK}" stroke-width="3"/><path d="M-70,-20L-62,-34H62L70,-20Z" fill="#2a6ab8" stroke="${INK}" stroke-width="2.4"/><path d="M-20,-34Q0,-22 20,-34" fill="#14325a"/></g>`;
    put(L.set, sh);
    put(L.fg, `<g transform="translate(1150,-60) rotate(32)">${coco(0, 0, 1.2, 0, 61, { trunk: false, pal: [T(P.leaf[0], -0.3), T(P.leaf[1], -0.25), P.leaf[1]] })}</g>`);
    ST[id] = { kind: "shop", view: "door", hx: DX(1.6) };
    doorDraw(id, 0, 0, false);
  }
  function doorDraw(id, t, a, siren) {
    const S = ST[id];
    el(`${id}-dr`).setAttribute("transform", `translate(${f1(S.hx)},0) scale(${f1(0.62 + 0.3 * a * Math.sin(t * 1.25) + 0.08 * a * Math.sin(t * 3.1))},1) translate(${f1(-S.hx)},0)`);
    el(`${id}-pap`).setAttribute("transform", `rotate(${f1(-6 + 10 * a * Math.sin(t * 4.4) * Math.sin(t * 1.3))}) skewY(${f1(6 * a * Math.sin(t * 6.1))})`);
    el(`${id}-chime`).setAttribute("transform", `translate(${f1(540 + 220 * 0.2)},560) rotate(${f1(6 * a * Math.sin(t * 2.2))})`);
    let hem = "M-280,548H1480V572";
    for (let x = 1480; x > -280; x -= 64) { const w = 6 * a * Math.sin(x * 0.02 + t * 7); hem += `Q${f1(x - 32)},${f1(610 + w)} ${f1(x - 64)},${f1(572 + w * 0.5)}`; }
    el(`${id}-awn`).setAttribute("d", hem + "Z");
    const bc = el(`${id}-beacon`);
    if (bc) bc.setAttribute("opacity", siren ? f1(Math.max(0, Math.sin(t * 9))) : "0");
  }
  // the wind through the empty shop: the loose door leaf swings, the menu sheet flaps on its tape, the awning's hem ripples, the shell
  // chime sways; o.amp (1), o.siren (true) blinks the tower's beacon on the hill
  Tide.doorWind = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, amp = o.amp ?? 1;
    doorDraw(id, t0, amp, o.siren !== false);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => doorDraw(id, t0 + c.t, amp, o.siren !== false) }, t0);
  };
  function tideShop(L, o = {}) {
    const id = o.id || "sh", v = o.view || "room", P = PAL[o.time || (v === "door" ? "eerie" : "morning")];
    return v === "wall" ? shopWall(L, id, o, P) : v === "table" ? shopTable(L, id, o, P) : v === "door" ? shopDoor(L, id, o, P) : shopRoom(L, id, o, P);
  }

  // ตังค์'s hand reaching for a fish on the opener's sand (Sets.tideSand o.hand): his right arm from the bottom right corner, the edge of
  // his yellow tank top at the shoulder, the hand seen from above (thumb on the left), a soft shadow on the sand (the sun is up on the left)
  const TANGK = { skin: "#d49c6c", l1: 300, l2: 285 };
  const tangHand = () => {
    const sk = TANGK.skin, skD = "#b07a4e", skL = "#ecc09a";
    // the palm runs on into the wrist (no seam with the forearm under it): filled, then outlined on its sides and knuckles only
    const palm = "M-21,22C-24,8 -30,-14 -29,-34C-28,-48 -25,-56 -22,-60L24,-61C29,-52 31,-40 30,-26C29,-8 24,8 21,22Z";
    let g = `<path d="${palm}" fill="${sk}"/><path d="M-21,22C-24,8 -30,-14 -29,-34C-28,-48 -25,-56 -22,-60M24,-61C29,-52 31,-40 30,-26C29,-8 24,8 21,22" stroke="${INK}" stroke-width="3" fill="none" stroke-linecap="round"/>`;
    g += `<path d="M14,18C20,4 26,-14 26,-30C26,-42 24,-52 22,-58L28,-56C31,-42 31,-22 27,-6C25,6 22,14 20,22Z" fill="${skD}" opacity=".35"/><path d="M-12,-46Q4,-40 20,-48" stroke="${skL}" stroke-width="5" fill="none" opacity=".6"/>`;
    g += `<g id="HF">`;
    // four fingers, each in two parts with a slight bend, a nail, a crease at the joint
    [[-17, -57, 44, -9, 13.5], [-5, -60, 49, -3, 14], [7, -59, 45, 3, 13.5], [18, -54, 35, 10, 12]].forEach(([x, y, len, a, w]) => {
      const l1 = len * 0.5, l2 = len * 0.52;
      g += `<g transform="translate(${x},${y}) rotate(${a})"><rect x="${-w / 2}" y="${-l1 - 2}" width="${w}" height="${l1 + 8}" rx="${w / 2}" fill="${sk}" stroke="${INK}" stroke-width="2.8"/>
        <g transform="translate(0,${-l1 + 2}) rotate(${a > 0 ? 6 : -4})"><rect x="${-w * 0.47}" y="${-l2}" width="${w * 0.94}" height="${l2 + 4}" rx="${w * 0.47}" fill="${sk}" stroke="${INK}" stroke-width="2.8"/><rect x="${-w * 0.3}" y="${-l2 + 2.5}" width="${w * 0.6}" height="${w * 0.66}" rx="${w * 0.28}" fill="#efcdb0" stroke="${skD}" stroke-width="1.2"/></g>
        <path d="M${-w * 0.3},${-l1 + 3}q${w * 0.3},3 ${w * 0.6},0" stroke="${skD}" stroke-width="1.5" fill="none"/><path d="M${w * 0.22},${-l1 + 4}V4" stroke="${skD}" stroke-width="2.2" opacity=".35"/></g>`;
    });
    g += `</g>`;
    // the thumb, out to the left and forward
    g += `<path d="M-27,-14C-40,-20 -52,-34 -56,-50C-58,-58 -50,-62 -46,-56C-41,-46 -34,-38 -25,-34Z" fill="${sk}" stroke="${INK}" stroke-width="2.8"/><path d="M-53,-52q4,-5 9,-1" stroke="#efcdb0" stroke-width="3" fill="none"/><path d="M-42,-36Q-38,-30 -30,-28" stroke="${skD}" stroke-width="1.4" fill="none"/>`;
    g += `<path d="M-15,-56q4,-4 8,0M-3,-59q4,-4 8,0M9,-58q4,-4 8,0M19,-53q3,-3 7,0" stroke="${skD}" stroke-width="1.8" fill="none"/><path d="M-6,-18Q4,-12 14,-20" stroke="${skD}" stroke-width="1.4" fill="none" opacity=".5"/>`;
    return g;
  };
  // a silhouette of the hand for its shadow (local coordinates as above)
  const TANG_SIL = "M-27,6C-32,-18 -31,-44 -30,-56L-26,-98Q-19,-104 -12,-98L-8,-104Q0,-112 8,-104L12,-100Q19,-104 25,-96L30,-84Q36,-82 36,-74L31,-44C31,-18 31,-8 26,6Z";
  function handParts(id) {
    return `<g id="${id}-hshd" opacity=".26"><path id="${id}-hsA" d="" fill="#3a2410"/><path id="${id}-hsF" d="" fill="#3a2410"/><path id="${id}-hsH" d="${TANG_SIL}" fill="#3a2410"/></g>
      <g id="${id}-hand"><path id="${id}-hua" d="" fill="${TANGK.skin}" stroke="${INK}" stroke-width="3"/><path id="${id}-hfa" d="" fill="${TANGK.skin}" stroke="${INK}" stroke-width="3"/><path id="${id}-hfs" d="" fill="#a8704a" opacity=".35"/>
      <g id="${id}-hh">${tangHand().replace('id="HF"', `id="${id}-hf"`)}</g>
      <g id="${id}-htop"><path d="M-120,30C-130,-40 -60,-110 20,-100C110,-90 170,-20 160,60L160,240H-120Z" fill="url(#tdTankTop)" stroke="${INK}" stroke-width="3.5"/><path d="M-96,8C-80,-56 -20,-84 40,-76" stroke="#c8901a" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M-96,8C-80,-56 -20,-84 40,-76" stroke="#ffe680" stroke-width="3" fill="none" opacity=".7"/>
        <g transform="translate(70,40) rotate(-20)"><path d="M-30,0C-18,-16 10,-16 20,-4L32,-12L30,0L32,12L20,4C10,16 -18,16 -30,0Z" fill="#2a6ab8" stroke="${INK}" stroke-width="2.4"/><circle cx="-18" cy="-2" r="3" fill="#fff"/></g></g></g>`;
  }
  // redraw the reach at progress p (0 the hand just in from the corner … 1 its fingertips at the fish), t the clock for a small tremble
  function reachDraw(id, t, p) {
    const S = ST[id], H = S.hand, k = gsap.parseEase("power2.out")(clamp(p / 0.82, 0, 1)), tr = sm(0.55, 0.8, p) * (1 - sm(0.9, 1, p));
    const W = [lerp(H.from[0], H.to[0], k) + 4 * tr * Math.sin(t * 11), lerp(H.from[1], H.to[1], k) + 3 * tr * Math.sin(t * 13 + 1)];
    const Sh = H.sh, E = elbowOf(Sh, W, TANGK.l1, TANGK.l2, 1);
    // the hand points from the wrist on toward the fish, the fingers curl a little as they get there; it lifts off the sand (bigger, a longer
    // shadow) on the way and comes down near the fish
    const aim = (Math.atan2(H.aim[1] - W[1], H.aim[0] - W[0]) * 180) / Math.PI + 90, lift = Math.sin(Math.PI * clamp(p / 0.85, 0, 1)), sc = 1 + 0.06 * lift;
    el(`${id}-hua`).setAttribute("d", limb(Sh, E, 66, 56));
    el(`${id}-hfa`).setAttribute("d", limb(E, [W[0] - (W[0] - E[0]) * 0.02, W[1] - (W[1] - E[1]) * 0.02], 56, 42));
    el(`${id}-hfs`).setAttribute("d", limb([lerp(E[0], W[0], 0.1) + 8, lerp(E[1], W[1], 0.1) + 6], [lerp(E[0], W[0], 0.85) + 6, lerp(E[1], W[1], 0.85) + 5], 18, 12));
    el(`${id}-hh`).setAttribute("transform", `translate(${P2(W)}) rotate(${f1(aim)}) scale(${f1(sc)})`);
    el(`${id}-hf`).setAttribute("transform", `translate(0,-56) scale(1,${f1(1 - 0.16 * sm(0.84, 1, p))}) translate(0,56)`);
    el(`${id}-htop`).setAttribute("transform", `translate(${P2(Sh)}) rotate(${f1((Math.atan2(E[1] - Sh[1], E[0] - Sh[0]) * 180) / Math.PI - 220)})`);
    const so = 14 + 34 * lift, sx = so * 0.85, sy = so;
    el(`${id}-hsA`).setAttribute("d", limb([Sh[0] + sx * 1.6, Sh[1] + sy * 1.6], [E[0] + sx * 1.3, E[1] + sy * 1.3], 66, 56));
    el(`${id}-hsF`).setAttribute("d", limb([E[0] + sx * 1.3, E[1] + sy * 1.3], [W[0] + sx, W[1] + sy], 56, 44));
    el(`${id}-hsH`).setAttribute("transform", `translate(${f1(W[0] + sx)},${f1(W[1] + sy)}) rotate(${f1(aim)}) scale(${f1(sc)})`);
    el(`${id}-hshd`).setAttribute("opacity", f1(0.3 - 0.08 * lift));
  }
  // ตังค์'s hand reaches in from the corner toward the fish (o.to the wrist's end point, o.aim where the fingers point; default fish 0),
  // slowing as it gets there with a little hesitant tremble, the fingers curling at the end
  Tide.reach = (tl, id, t0, dur, o = {}) => {
    const S = ST[id], c = { t: 0 };
    if (o.to) S.hand.to = o.to;
    if (o.aim) S.hand.aim = o.aim;
    reachDraw(id, t0, 0);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => reachDraw(id, t0 + c.t, c.t / dur) }, t0);
  };

  function tideBeach(L, o = {}) { return (o.view || "sea") === "land" ? landView(L, o) : seaView(L, o); }
  Object.assign(Sets, { tideBeach, tideWave, tideHill, tideSand, tideShop });
})();
