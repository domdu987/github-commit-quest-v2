// Sets, props and cast for "มือพราย": a central-Thai river on Loy Krathong night in the flood season — a full
// moon, a temple and string lights on the far bank, krathongs with candles drifting on dark water, a wooden
// pier (ท่าน้ำ), a house on stilts, a ferry boat — plus a split view under the pier, an underwater view, POV down
// at a krathong, an ankle close-up, the legend in ink and a bedroom with a mosquito net. Same layer contract as
// sets.js (sky / far / mid / set / act / fg, glow above the darkness); seeded RNG only.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);

  Sets.DEFS += `
    <linearGradient id="phSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050815"/><stop offset=".55" stop-color="#0d1838"/><stop offset="1" stop-color="#1c2c55"/></linearGradient>
    <linearGradient id="phDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22284f"/><stop offset=".45" stop-color="#6b4a74"/><stop offset=".8" stop-color="#d9826a"/><stop offset="1" stop-color="#f2b47a"/></linearGradient>
    <linearGradient id="phWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2a4c"/><stop offset=".35" stop-color="#0d1a33"/><stop offset="1" stop-color="#050b17"/></linearGradient>
    <linearGradient id="phWaterD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a6f8a"/><stop offset=".3" stop-color="#3b4766"/><stop offset="1" stop-color="#1d2640"/></linearGradient>
    <linearGradient id="phUnder" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f5a5a"/><stop offset=".3" stop-color="#173634"/><stop offset=".7" stop-color="#0a1b1a"/><stop offset="1" stop-color="#030807"/></linearGradient>
    <linearGradient id="phRay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe6c8" stop-opacity=".28"/><stop offset="1" stop-color="#cfe6c8" stop-opacity="0"/></linearGradient>
    <radialGradient id="phMoon" cx=".42" cy=".4"><stop offset="0" stop-color="#fffbe8"/><stop offset=".7" stop-color="#f1ead0"/><stop offset="1" stop-color="#d9d0ae"/></radialGradient>
    <radialGradient id="phHalo"><stop offset="0" stop-color="#f6efcf" stop-opacity=".5"/><stop offset=".35" stop-color="#9fb0d8" stop-opacity=".18"/><stop offset="1" stop-color="#9fb0d8" stop-opacity="0"/></radialGradient>
    <radialGradient id="phFlame"><stop offset="0" stop-color="#ffe9a8" stop-opacity=".95"/><stop offset=".25" stop-color="#ffbe5c" stop-opacity=".55"/><stop offset=".6" stop-color="#ff9a3c" stop-opacity=".16"/><stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/></radialGradient>
    <radialGradient id="phBulb"><stop offset="0" stop-color="#ffe2a0" stop-opacity=".9"/><stop offset=".4" stop-color="#ffc06a" stop-opacity=".25"/><stop offset="1" stop-color="#ffc06a" stop-opacity="0"/></radialGradient>
    <radialGradient id="phPale" cx=".4" cy=".35"><stop offset="0" stop-color="#232b28"/><stop offset=".7" stop-color="#141917"/><stop offset="1" stop-color="#0a0c0b"/></radialGradient>
    <linearGradient id="phPlank" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a4330"/><stop offset="1" stop-color="#3b2b1f"/></linearGradient>
    <linearGradient id="phWall" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6b4a32"/><stop offset=".5" stop-color="#7d5a3c"/><stop offset="1" stop-color="#5e412c"/></linearGradient>
    <linearGradient id="phNet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe6ee" stop-opacity=".42"/><stop offset="1" stop-color="#c9d2dc" stop-opacity=".26"/></linearGradient>
    <linearGradient id="phSkin" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c88d63"/><stop offset=".5" stop-color="#e3ad84"/><stop offset="1" stop-color="#b9805a"/></linearGradient>
    <radialGradient id="phSiren"><stop offset="0" stop-color="#ff3a3a" stop-opacity=".55"/><stop offset="1" stop-color="#ff3a3a" stop-opacity="0"/></radialGradient>
    <radialGradient id="phSirenB"><stop offset="0" stop-color="#3a7aff" stop-opacity=".55"/><stop offset="1" stop-color="#3a7aff" stop-opacity="0"/></radialGradient>
    <linearGradient id="phPaper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#181512"/><stop offset="1" stop-color="#0d0b09"/></linearGradient>`;

  // ---------------- small drawings ----------------
  // a krathong at (x, y), scale s, seen at three-quarters: banana-leaf petals, a flower cone, candle + 3 incense, optional coins.
  // Wrapped in an untransformed <g class="ktg"> so GSAP can drift it (x/y on a group with a transform attribute would reset it).
  function krathong(x, y, s, o = {}) {
    const petals = Array.from({ length: 10 }, (_, i) => {
      const a = (i / 10) * Math.PI * 2, px = Math.cos(a) * 62, py = Math.sin(a) * 18;
      return `<path d="M${f1(px * 0.8)},${f1(py * 0.8 - 8)}L${f1(px * 1.12)},${f1(py * 1.12 - 30)}L${f1(px * 1.12 + (Math.cos(a + 1.57) * 14))},${f1(py * 1.1 - 4)}Z" fill="${i % 2 ? "#4f8f45" : "#3f7a3a"}" stroke="#1f3a1c" stroke-width="2.5" stroke-linejoin="round"/>`;
    });
    const back = petals.filter((_, i) => i >= 5).join(""), front = petals.filter((_, i) => i < 5).join("");
    const flowers = [[-26, -30, "#f2a33a"], [0, -40, "#f7c04a"], [24, -30, "#f2a33a"], [-12, -52, "#c45cc0"], [14, -52, "#f2a33a"], [0, -64, "#f7c04a"]].map(([fx, fy, c]) =>
      `<circle cx="${fx}" cy="${fy}" r="13" fill="${c}" stroke="#7a4a12" stroke-width="2"/><circle cx="${fx}" cy="${fy}" r="4" fill="#7a4a12" opacity=".6"/>`).join("");
    const coins = o.coins ? [[-34, 4], [-14, 10], [12, 9], [32, 4], [-2, 2]].slice(0, o.coins).map(([cx, cy]) =>
      `<g class="kcoin"><ellipse cx="${cx}" cy="${cy}" rx="10" ry="5" fill="#f2d16a" stroke="#8a6a14" stroke-width="2"/><ellipse cx="${cx - 3}" cy="${cy - 1}" rx="3" ry="1.5" fill="#fff6c8"/></g>`).join("") : "";
    const flame = o.lit === false ? "" : `<path class="kflame" d="M0,-108C-8,-96 -7,-86 0,-82C7,-86 8,-96 0,-108Z" fill="#ffd36a" stroke="#ff9a3c" stroke-width="2"/>`;
    return `<g class="ktg" data-dx="${o.dx ?? 40}" data-ph="${o.ph ?? 0}"><g transform="translate(${f1(x)},${f1(y)}) scale(${s})">
      <ellipse cx="0" cy="14" rx="76" ry="16" fill="#0a1220" opacity=".55"/>
      ${back}<ellipse cx="0" cy="0" rx="66" ry="20" fill="#5c9a4a" stroke="#1f3a1c" stroke-width="3"/>${coins}
      <path d="M-40,-6Q-38,-62 0,-74Q38,-62 40,-6Z" fill="#6aa856" stroke="#1f3a1c" stroke-width="3"/>${flowers}
      <rect x="-5" y="-84" width="10" height="26" rx="2" fill="#f4f0e6" stroke="#7a6a52" stroke-width="2"/>${flame}
      <path d="M14,-72l10,-40M20,-70l18,-34M8,-72l4,-42" stroke="#8a5a3a" stroke-width="2.6"/><circle cx="24" cy="-112" r="3" fill="#ff7a3a"/><circle cx="38" cy="-104" r="3" fill="#ff7a3a"/><circle cx="12" cy="-114" r="3" fill="#ff7a3a"/>
      ${front}</g></g>`;
  }
  // its candle glow (glow layer, above the darkness) + a warm streak reflected below it
  const kglow = (x, y, s, r = 150) => `<g class="kglw"><circle cx="${f1(x)}" cy="${f1(y - 95 * s)}" r="${f1(r * s)}" fill="url(#phFlame)"/></g>`;
  const krefl = (x, y, s) => `<g class="krefl">${[0, 1, 2, 3, 4].map((k) => `<path d="M${f1(x - (24 - k * 4) * s)},${f1(y + (34 + k * 22) * s)}h${f1((48 - k * 8) * s)}" stroke="#ffb35c" stroke-width="${f1(6 * s)}" stroke-linecap="round" opacity="${(0.55 - k * 0.1).toFixed(2)}"/>`).join("")}</g>`;

  // the พราย's colours (user: "ตัวดำๆตาเขียวๆแบบกองกอย"): a coal-black body, a cold green rim so it still reads on dark water,
  // green eyes (class geye flickers in life()) — same palette as หมอกลง's ghosts
  const GBL = "#0a0c0b", GBL2 = "#161b19", GRIM = "#3d6a52", GVEIN = "#2a4a3a", GEYE = ["#7dff6a", "#bfff96", "#f2ffe4"];
  const GOUT = `stroke="${GRIM}" stroke-width="4" stroke-linejoin="round"`;
  // the drowned: a black hand + forearm reaching up from (x, y), fingers long, a green rim
  function paleHand(x, y, s, rot = 0, id = "") {
    return `<g ${id ? `id="${id}"` : ""} transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${s})">
      <path d="M-22,260C-26,170 -24,90 -20,30L20,30C24,90 26,170 22,260Z" fill="url(#phPale)" ${GOUT}/>
      <path d="M-24,40C-30,10 -24,-14 0,-18C24,-14 30,10 24,40Z" fill="${GBL2}" ${GOUT}/>
      ${[[-20, -6, -32, -70], [-8, -14, -12, -92], [6, -14, 8, -96], [18, -8, 26, -80], [24, 16, 44, -10]].map(([x0, y0, x1, y1]) =>
        `<path d="M${x0},${y0}Q${(x0 + x1) / 2 + 3},${(y0 + y1) / 2} ${x1},${y1}" stroke="${GRIM}" stroke-width="13" fill="none" stroke-linecap="round"/><path d="M${x0},${y0}Q${(x0 + x1) / 2 + 3},${(y0 + y1) / 2} ${x1},${y1}" stroke="${GBL2}" stroke-width="8" fill="none" stroke-linecap="round"/><circle cx="${x1}" cy="${y1}" r="4.5" fill="#000"/>`).join("")}
      <path d="M-14,120q6,-10 0,-24M10,170q-6,-14 2,-30" stroke="${GVEIN}" stroke-width="3" fill="none"/></g>`;
  }
  // a green eye: soft glow, the iris, a hot centre
  const gEye = (cx, cy, rx, ry, op = 1) => `<g class="geye" opacity="${op}"><circle cx="${cx}" cy="${cy}" r="${rx * 2.4}" fill="${GEYE[0]}" opacity=".32"/><ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${GEYE[0]}"/><ellipse cx="${cx}" cy="${cy}" rx="${rx * 0.5}" ry="${ry * 0.55}" fill="${GEYE[2]}"/></g>`;
  // the พราย of this story: a drowned woman's head turned up toward the lights — a coal-black face, the wet hair fanned out
  // like weed (class phair sways) and hanging over the face in strands, one green eye burning through, the mouth a dark open gap
  function drownedFace(x, y, s, o = {}) {
    const fan = Array.from({ length: 11 }, (_, i) => { const a = -168 + i * 15.6, rr = 170 + (i % 3) * 40, A = (a * Math.PI) / 180;
      return `<path class="phair" data-i="${i}" d="M0,-30Q${f1(Math.cos(A) * rr * 0.45)},${f1(Math.sin(A) * rr * 0.45 - 50)} ${f1(Math.cos(A) * rr)},${f1(Math.sin(A) * rr - 40)}" stroke="#070d0c" stroke-width="${18 - (i % 3) * 4}" fill="none" stroke-linecap="round"/>`; }).join("");
    const veil = [-52, -40, -28, -16, -4, 32, 44, 54].map((dx, i) => `<path d="M${dx * 0.6},-34C${dx},10 ${dx + (i % 2 ? 6 : -6)},60 ${dx + (i % 2 ? -4 : 4)},${118 + (i % 3) * 14}" stroke="#070d0c" stroke-width="${12 - (i % 3) * 2}" fill="none" stroke-linecap="round"/>`).join("");
    return `<g class="pface" opacity="${o.op ?? 1}"><g transform="translate(${f1(x)},${f1(y)}) scale(${s})">${fan}
      <ellipse cx="0" cy="40" rx="60" ry="78" fill="${GBL}" stroke="${GRIM}" stroke-width="4"/><ellipse cx="10" cy="56" rx="40" ry="50" fill="${GBL2}" opacity=".7"/>
      ${gEye(18, 30, 13, 9)}<path d="M3,20q15,-8 30,0" stroke="${GRIM}" stroke-width="3" fill="none"/>${gEye(-22, 30, 12, 8, 0.85)}
      <ellipse cx="4" cy="86" rx="11" ry="15" fill="#020303" stroke="${GVEIN}" stroke-width="2"/><path d="M-30,64q8,6 0,14M40,62q-8,8 0,14" stroke="${GVEIN}" stroke-width="3" fill="none"/>
      <path d="M-60,4Q-46,-46 0,-50Q46,-46 60,4Q40,-22 0,-24Q-40,-22 -60,4Z" fill="#070d0c"/>${veil}</g></g>`;
  }
  // ferry boat (เรือจ้าง): long low wooden hull seen from the side, bow to the right
  function ferry(x, y, s, o = {}) {
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">
      <path d="M-330,-40H300Q370,-44 400,-96Q396,-30 330,10Q300,30 250,32H-300Q-350,26 -362,-10Q-366,-34 -330,-40Z" fill="#5a3b26" ${OUT}/>
      <path d="M-330,-40H300Q370,-44 400,-96" stroke="#8a5f3c" stroke-width="10" fill="none"/><path d="M-300,4H250" stroke="#3b271a" stroke-width="5"/>
      ${[-220, -60, 100].map((bx) => `<rect x="${bx}" y="-52" width="80" height="14" rx="4" fill="#7a5236" ${OUT}/>`).join("")}
      ${o.oar !== false ? `<path d="M-280,-60L-420,180" stroke="#6a4a2e" stroke-width="12" stroke-linecap="round"/><path d="M-420,180l-20,70l40,-10z" fill="#6a4a2e" ${OUT}/>` : ""}
      ${o.lamp ? `<path d="M330,-60v-90" stroke="#3a2a1c" stroke-width="6"/><rect x="316" y="-176" width="30" height="34" rx="6" fill="#ffcf7a" ${OUT}/>` : ""}</g>`;
  }
  // translucent white gallon (แกลลอน) with a handle, water to a third
  const gallon = (x, y, s, rot = 0) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${s})"><path d="M-40,-60H30Q44,-60 44,-46V40Q44,54 30,54H-30Q-44,54 -44,40V-46Q-44,-60 -40,-60Z" fill="#e9eef0" fill-opacity=".85" ${OUT}/>
    <path d="M-44,10H44V40Q44,54 30,54H-30Q-44,54 -44,40Z" fill="#7fb3c9" opacity=".75"/><path d="M-20,-60v-18h22v18" fill="#e04a3a" ${OUT}/><path d="M14,-60q30,-16 30,20" stroke="${INK}" stroke-width="10" fill="none"/><path d="M14,-60q30,-16 30,20" stroke="#e9eef0" stroke-width="5" fill="none"/></g>`;
  const bottle = (x, y, s, rot = 0) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${s})"><rect x="-8" y="-74" width="16" height="12" rx="3" fill="#3f7fbf"/><path d="M-12,-62h24v8q12,8 12,22v66q0,10 -10,10h-28q-10,0 -10,-10v-66q0,-14 12,-22z" fill="#dff0f6" fill-opacity=".7" ${OUT}/><path d="M-22,10h44v24q0,10 -10,10h-24q-10,0 -10,-10z" fill="#7fb3c9" opacity=".8"/></g>`;
  // bamboo pole from (x0,y0) to (x1,y1)
  const bamboo = (x0, y0, x1, y1, w = 18) => {
    const n = 7, dx = (x1 - x0) / n, dy = (y1 - y0) / n;
    return `<path d="M${x0},${y0}L${x1},${y1}" stroke="${INK}" stroke-width="${w + 8}" stroke-linecap="round"/><path d="M${x0},${y0}L${x1},${y1}" stroke="#c9b26a" stroke-width="${w}" stroke-linecap="round"/>
      ${Array.from({ length: n - 1 }, (_, k) => { const cx = x0 + dx * (k + 1), cy = y0 + dy * (k + 1), L2 = Math.hypot(dx, dy), nx = (-dy / L2) * (w / 2 + 3), ny = (dx / L2) * (w / 2 + 3);
        return `<path d="M${f1(cx - nx)},${f1(cy - ny)}L${f1(cx + nx)},${f1(cy + ny)}" stroke="#7a6a32" stroke-width="5"/>`; }).join("")}`;
  };

  // ---------------- shared backdrops ----------------
  function skyNight(L, o, r) {
    let s = `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#phSky)"/>`;
    for (let i = 0; i < 90; i++) s += `<circle cx="${f1(-700 + r() * 2500)}" cy="${f1(-500 + r() * 1300)}" r="${f1(1 + r() * 2.2)}" fill="#e8ecff" opacity="${(0.3 + r() * 0.6).toFixed(2)}"/>`;
    if (o.moon !== false) { const m = o.moon || { x: 820, y: 260, r: 70 };
      s += `<circle cx="${m.x}" cy="${m.y}" r="${m.r * 5}" fill="url(#phHalo)"/><circle cx="${m.x}" cy="${m.y}" r="${m.r}" fill="url(#phMoon)"/><circle cx="${m.x - m.r * 0.3}" cy="${m.y - m.r * 0.1}" r="${m.r * 0.18}" fill="#d9d0ae" opacity=".5"/><circle cx="${m.x + m.r * 0.25}" cy="${m.y + m.r * 0.3}" r="${m.r * 0.12}" fill="#d9d0ae" opacity=".45"/>`; }
    put(L.sky, s);
  }
  // far bank: tree line, a temple with a tiered roof and chofa, string lights in an arc, small lanterns
  function farBank(L, y, r, o = {}) {
    let s = `<path d="M-900,${y}`;
    for (let x = -900; x <= 2000; x += 60) s += `L${x},${f1(y - 60 - r() * 90)}`;
    s += `L2000,${y + 40}H-900Z" fill="#070c18"/>`;
    const tx = o.temple ?? 260, tw = 260, ty = y - 40;
    s += `<g opacity=".95"><rect x="${tx - tw / 2}" y="${ty - 110}" width="${tw}" height="110" fill="#0b1324"/>
      <path d="M${tx - tw / 2 - 40},${ty - 110}L${tx},${ty - 230}L${tx + tw / 2 + 40},${ty - 110}Z" fill="#0d1730" stroke="#c9a55a" stroke-width="3"/>
      <path d="M${tx - tw / 2 - 10},${ty - 150}L${tx},${ty - 270}L${tx + tw / 2 + 10},${ty - 150}" fill="none" stroke="#c9a55a" stroke-width="3"/>
      <path d="M${tx},${ty - 270}q14,-30 4,-50" stroke="#c9a55a" stroke-width="5" fill="none" stroke-linecap="round"/>
      ${[-80, -30, 30, 80].map((d) => `<rect x="${tx + d - 8}" y="${ty - 90}" width="16" height="40" rx="3" fill="#ffcf7a" opacity=".7"/>`).join("")}</g>`;
    if (o.lights !== false) {
      for (let k = 0; k < 2; k++) {
        const x0 = -700 + k * 1300, x1 = x0 + 1100, sag = 60;
        for (let i = 0; i <= 26; i++) { const u = i / 26, bx = x0 + (x1 - x0) * u, by = y - 150 + Math.sin(u * Math.PI) * sag;
          s += `<circle class="slt" cx="${f1(bx)}" cy="${f1(by)}" r="5" fill="${["#ffcf7a", "#ff8a6a", "#9fd8ff", "#ffe08a"][i % 4]}"/>`; }
      }
    }
    put(L.far, s);
  }
  // river surface from y down: dark water, moon streak, ripples, far krathongs
  function river(L, y, r, o = {}) {
    let s = `<rect x="-900" y="${y}" width="2900" height="${2600 - y}" fill="url(#phWater)"/>`;
    const mx = (o.moon && o.moon.x) || 820;
    for (let k = 0; k < 18; k++) s += `<path class="mrefl" d="M${f1(mx - 20 - r() * 70)},${f1(y + 20 + k * 34)}h${f1(40 + r() * 120)}" stroke="#e8e2c0" stroke-width="${f1(4 + r() * 4)}" stroke-linecap="round" opacity="${(0.6 - k * 0.025).toFixed(2)}"/>`;
    for (let k = 0; k < 40; k++) s += `<path class="rip" d="M${f1(-700 + r() * 2500)},${f1(y + 30 + r() * 1300)}h${f1(30 + r() * 90)}" stroke="#6c7fa8" stroke-width="3" stroke-linecap="round" opacity=".35"/>`;
    put(L.mid, s);
  }

  // ---------------- sets ----------------
  // wide river at night (or dusk): far bank + temple, moon, drifting krathongs, optional pier / stilt house / ferry
  function riverNight(L, o = {}) {
    const id = o.id || "rn", r = mk(o.seed || 41), W = o.water ?? 1100;
    skyNight(L, o, r);
    if (o.dusk) put(L.sky, `<rect x="-900" y="-600" width="2900" height="${W + 600}" fill="url(#phDusk)" opacity=".85"/>`);
    farBank(L, W, r, o);
    river(L, W, r, o);
    let s = "", g = "";
    (o.kt || [[180, W + 260, 0.55], [620, W + 200, 0.45], [880, W + 380, 0.7], [380, W + 520, 0.9], [-80, W + 420, 0.75], [1100, W + 600, 1.0]]).forEach(([x, y, sc, coins], i) => {
      s += krathong(x, y, sc, { coins, dx: 30 + (i % 3) * 18, ph: i }); g += kglow(x, y, sc); s += krefl(x, y, sc);
    });
    if (o.boat) s += ferry(o.boat.x, o.boat.y, o.boat.s || 0.8, o.boat);
    if (o.house) s += stiltHouseSide(o.house.x ?? -260, W + 40, o.house.s || 1, r);
    put(L.set, s); put(L.glow, g);
    if (o.pier) pierSide(L, o.pier, r, id);
  }
  // a house on stilts at the water (side view), lantern on the porch
  function stiltHouseSide(x, y, s, r) {
    return `<g transform="translate(${x},${y}) scale(${s})">
      ${[-260, -120, 20, 160].map((px) => `<rect x="${px}" y="-260" width="22" height="380" fill="#2a1c12" ${OUT}/>`).join("")}
      <rect x="-300" y="-300" width="500" height="44" fill="#3b2a1c" ${OUT}/>
      <path d="M-290,-300V-560H190V-300Z" fill="#4a3424" ${OUT}/>${Array.from({ length: 12 }, (_, k) => `<path d="M${-290 + k * 40},-560V-300" stroke="#2a1c12" stroke-width="4"/>`).join("")}
      <rect x="-200" y="-500" width="110" height="130" fill="#ffc06a" opacity=".85" ${OUT}/><path d="M-145,-500v130" stroke="${INK}" stroke-width="5"/>
      <path d="M-340,-560L-50,-760L240,-560Z" fill="#2a1c12" ${OUT}/><path d="M-50,-760q10,-30 -4,-50" stroke="#2a1c12" stroke-width="10" fill="none"/>
      <path d="M200,-300L330,60" stroke="#3b2a1c" stroke-width="18"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M${214 + k * 24},${-260 + k * 66}h46" stroke="#3b2a1c" stroke-width="10"/>`).join("")}</g>`;
  }
  // a long pier running out into the river (used by riverNight): planks on posts, lamps
  function pierSide(L, p, r, id) {
    const y = p.y, x0 = p.x0 ?? -900, x1 = p.x1 ?? 520;
    let s = `<rect x="${x0}" y="${y}" width="${x1 - x0}" height="34" fill="url(#phPlank)" ${OUT}/>`;
    for (let x = x0 + 40; x < x1; x += 130) s += `<rect x="${x}" y="${y + 30}" width="18" height="260" fill="#241810"/>`;
    if (p.crowd) for (let k = 0; k < (p.crowd === true ? 9 : p.crowd); k++) { const cx = x0 + 120 + k * ((x1 - x0 - 160) / 8) + r() * 30, h = 150 + r() * 70, kid = r() < 0.3;
      s += `<g opacity=".95"><ellipse cx="${f1(cx)}" cy="${f1(y - h * (kid ? 0.7 : 1) - 22)}" rx="${kid ? 16 : 20}" ry="${kid ? 18 : 23}" fill="#0a0f1c"/><path d="M${f1(cx - (kid ? 22 : 30))},${y}L${f1(cx - (kid ? 18 : 24))},${f1(y - h * (kid ? 0.7 : 1))}Q${f1(cx)},${f1(y - h * (kid ? 0.7 : 1) - 12)} ${f1(cx + (kid ? 18 : 24))},${f1(y - h * (kid ? 0.7 : 1))}L${f1(cx + (kid ? 22 : 30))},${y}Z" fill="#0a0f1c"/>
        <path d="M${f1(cx + 14)},${f1(y - h * (kid ? 0.7 : 1) + 4)}q12,10 8,40" stroke="#ffb35c" stroke-width="4" fill="none" opacity=".55"/></g>`; }
    put(L.set, s);
    let g = "";
    for (let x = x0 + 100; x < x1; x += 260) g += `<path d="M${x},${y}v-200" stroke="#1a120c" stroke-width="8"/><circle class="lamp" cx="${x}" cy="${y - 210}" r="12" fill="#ffd38a"/><circle cx="${x}" cy="${y - 210}" r="110" fill="url(#phBulb)"/>`;
    put(L.glow, g);
  }

  // side view on the pier deck: deck top at G, deck ends at x = edge, water surface at o.water beyond and below it.
  // The water in front of anyone in the river is a separate group (#id-wfront) to move on top of the actors with TOP().
  function pierDeck(L, o = {}) {
    const id = o.id || "pd", r = mk(o.seed || 43), G = o.ground ?? 1480, E = o.edge ?? 640, WS = o.water ?? G + 150, FB = o.far ?? 980;
    skyNight(L, { moon: o.moon ?? { x: 860, y: 300, r: 54 } }, r);
    farBank(L, FB, r, o);
    river(L, FB, r, o);
    let s = "", g = "";
    // krathongs further out on the water
    (o.kt || [[820, FB + 160, 0.4], [300, FB + 110, 0.32], [980, FB + 300, 0.55]]).forEach(([x, y, sc, coins], i) => { s += krathong(x, y, sc, { coins, dx: 26 + i * 10, ph: i + 2 }); g += kglow(x, y, sc); });
    // near water (in front of the far river), surface line at WS; the ferry sits in it
    s += `<rect x="${E - 40}" y="${WS}" width="${2000 - E}" height="${2600 - WS}" fill="url(#phWaterD)" opacity=".92"/>`;
    for (let k = 0; k < 16; k++) s += `<path class="rip" d="M${f1(E + r() * 1300)},${f1(WS + 10 + r() * 600)}h${f1(40 + r() * 100)}" stroke="#9fb0d8" stroke-width="4" stroke-linecap="round" opacity=".4"/>`;
    if (o.boat) s += ferry(o.boat.x, o.boat.y ?? WS + 20, o.boat.s || 0.9, o.boat);
    // the deck: planks, front beam, posts down into the water, ladder at the edge
    s += `<rect x="-900" y="${G}" width="${E + 900}" height="46" fill="url(#phPlank)" ${OUT}/>`;
    for (let x = -880; x < E; x += 74) s += `<path d="M${x},${G + 4}v38" stroke="#2a1c12" stroke-width="3"/>`;
    s += `<rect x="-900" y="${G + 46}" width="${E + 900}" height="20" fill="#2a1c12"/>`;
    for (let x = -820; x < E; x += 210) s += `<rect x="${x}" y="${G + 66}" width="26" height="${2600 - G}" fill="#1f150e" ${OUT}/>`;
    s += `<rect x="${E - 30}" y="${G - 10}" width="30" height="${2600 - G}" fill="#2a1c12" ${OUT}/>`;
    if (o.ladder !== false) s += `<g>${[0, 1, 2, 3].map((k) => `<rect x="${E + 6}" y="${G + 40 + k * 70}" width="70" height="14" rx="4" fill="#4a3424" ${OUT}/>`).join("")}<path d="M${E + 8},${G}V${G + 300}M${E + 74},${G + 20}V${G + 300}" stroke="#3b2a1c" stroke-width="10"/></g>`;
    if (o.rail) s += `<path d="M-900,${G - 150}H${E - 60}" stroke="#3b2a1c" stroke-width="12"/>` + Array.from({ length: 14 }, (_, k) => `<rect x="${-880 + k * 110}" y="${G - 160}" width="14" height="160" fill="#3b2a1c"/>`).filter((_, k) => -880 + k * 110 < E - 60).join("");
    if (o.props) s += o.props;
    put(L.set, s);
    if (o.lamps !== false) for (let x = -500; x < E; x += 380) g += `<path d="M${x},${G}v-430" stroke="#1a120c" stroke-width="9"/><circle class="lamp" cx="${x}" cy="${G - 440}" r="14" fill="#ffd38a"/><circle cx="${x}" cy="${G - 440}" r="200" fill="url(#phBulb)"/>`;
    put(L.glow, g);
    // water in front of the swimmer (moved to the top of the act layer by the shot)
    let wf = `<g id="${id}-wfront"><path d="M${E - 40},${WS}Q${E + 300},${WS - 14} ${E + 600},${WS}T${E + 1300},${WS}V2600H${E - 40}Z" fill="#2b3656" opacity=".86"/>`;
    wf += `<path class="rip" d="M${E},${WS}Q${E + 300},${WS - 14} ${E + 600},${WS}T${E + 1300},${WS}" stroke="#b9c6e8" stroke-width="6" fill="none" opacity=".7"/></g>`;
    put(L.act, wf);
  }

  // POV straight down from the edge of the pier: planks across the top, black water, one krathong with coins,
  // a child's arm reaching down (#id-hand) and a pale hand rising toward it from below (#id-phand)
  function pierPOV(L, o = {}) {
    const id = o.id || "pp", r = mk(o.seed || 47), E = o.edge ?? 560;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#040810"/>`);
    let m = `<rect x="-900" y="${E - 40}" width="2900" height="${2600 - E}" fill="url(#phWater)"/>`;
    for (let k = 0; k < 30; k++) m += `<path class="mrefl" d="M${f1(-200 + r() * 1500)},${f1(E + 60 + r() * 1500)}h${f1(30 + r() * 140)}" stroke="#d9d4b8" stroke-width="${f1(3 + r() * 4)}" stroke-linecap="round" opacity="${(0.15 + r() * 0.3).toFixed(2)}"/>`;
    put(L.mid, m);
    let s = "";
    s += `<g id="${id}-faces" opacity="${o.faces ?? 0}">${drownedFace(220, 1500, 0.9, { op: 0.35 })}${drownedFace(900, 1700, 0.8, { op: 0.3 })}</g>`;
    s += `<g id="${id}-phand" opacity="${o.phand ?? 0.6}">${paleHand(560, 1700, 1.5, 6)}</g>`;
    s += `<rect x="-900" y="${E - 40}" width="2900" height="${2600 - E}" fill="#0b1426" opacity=".38"/>`;
    s += krathong(540, 1180, 2.2, { coins: 5, dx: 12 });
    s += `<rect x="-900" y="-600" width="2900" height="${E + 560}" fill="url(#phPlank)"/>`;
    for (let x = -900; x < 2000; x += 130) s += `<path d="M${x},-600V${E - 40}" stroke="#241810" stroke-width="6"/>`;
    for (let x = -880; x < 2000; x += 130) s += `<circle cx="${x + 40}" cy="${E - 80}" r="6" fill="#1a120c"/>`;
    s += `<rect x="-900" y="${E - 46}" width="2900" height="26" fill="#2a1c12" ${OUT}/>`;
    put(L.set, s);
    put(L.glow, kglow(540, 1180, 2.2, 220));
    const tong = CAST_COL.tong;
    put(L.act, `<g id="${id}-hand"><path d="M470,-200L500,${E + 200}" stroke="${INK}" stroke-width="88" stroke-linecap="round"/><path d="M470,-200L500,${E + 120}" stroke="${tong.top}" stroke-width="80" stroke-linecap="round"/>
      <path d="M500,${E + 110}L512,${E + 420}" stroke="${INK}" stroke-width="64" stroke-linecap="round"/><path d="M500,${E + 110}L512,${E + 420}" stroke="${tong.skin}" stroke-width="56" stroke-linecap="round"/>
      <g transform="translate(514,${E + 450})"><ellipse cx="0" cy="0" rx="46" ry="54" fill="${tong.skin}" ${OUT}/>${[-30, -12, 8, 26].map((fx) => `<path d="M${fx},30v46" stroke="${INK}" stroke-width="22" stroke-linecap="round"/><path d="M${fx},30v46" stroke="${tong.skin}" stroke-width="15" stroke-linecap="round"/>`).join("")}</g></g>`);
  }

  // split view at the waterline under the pier: people and krathongs above, the drowned drifting below, following the lights
  function pierSection(L, o = {}) {
    const id = o.id || "ps", r = mk(o.seed || 53), WL = o.wl ?? 820;
    skyNight(L, { moon: { x: 900, y: 140, r: 46 } }, r);
    let s = `<rect x="-900" y="${WL}" width="2900" height="${2600 - WL}" fill="url(#phUnder)"/>`;
    for (let k = 0; k < 5; k++) s += `<path class="ray" d="M${80 + k * 240},${WL}L${170 + k * 240},${WL}L${320 + k * 220},2400L${120 + k * 220},2400Z" fill="url(#phRay)"/>`;
    // pier above water: deck, posts all the way down, legs of people
    s += `<rect x="-900" y="${WL - 220}" width="1500" height="40" fill="url(#phPlank)" ${OUT}/>`;
    for (let x = -840; x < 600; x += 190) s += `<rect x="${x}" y="${WL - 180}" width="24" height="${2600 - WL}" fill="#1a120c" ${OUT}/>`;
    for (let k = 0; k < 7; k++) { const x = -700 + k * 180 + r() * 40;
      s += `<path d="M${x},${WL - 220}V${WL - 420}M${x + 34},${WL - 220}V${WL - 420}" stroke="#0a0f1c" stroke-width="26"/><rect x="${x - 16}" y="${WL - 560}" width="70" height="150" rx="16" fill="#0a0f1c"/>`; }
    // krathongs on the surface, their light shafts in the water
    let g = "";
    (o.kt || [[700, WL, 0.6], [940, WL, 0.5], [1180, WL, 0.55], [420, WL, 0.45]]).forEach(([x, y, sc], i) => { s += krathong(x, y, sc, { dx: 60 + i * 10, ph: i }); g += kglow(x, y, sc, 190); });
    s += `<path class="rip" d="M-900,${WL}H2000" stroke="#9fb0d8" stroke-width="6" opacity=".7"/>`;
    // the drowned, below, faces turned up to the lights
    s += `<g id="${id}-pr">${drownedFace(640, WL + 520, 0.9)}${drownedFace(940, WL + 760, 0.75, { op: 0.75 })}${drownedFace(320, WL + 900, 0.8, { op: 0.6 })}
      ${paleHand(560, WL + 420, 0.9, -12)}${paleHand(1010, WL + 620, 0.8, 10)}</g>`;
    for (let k = 0; k < 18; k++) s += `<g class="bub" data-i="${k}"><circle cx="${f1(300 + r() * 900)}" cy="${f1(WL + 300 + r() * 1100)}" r="${f1(4 + r() * 9)}" fill="none" stroke="#cfe6d8" stroke-width="2.5" opacity=".6"/></g>`;
    put(L.set, s); put(L.glow, g);
  }

  // porch of the house on stilts at dusk / night: plank wall, window, lantern, the river behind the steps
  function porch(L, o = {}) {
    const id = o.id || "po", r = mk(o.seed || 59), G = o.ground ?? 1480, night = o.time === "night";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#${night ? "phSky" : "phDusk"})"/>`);
    if (!night) put(L.sky, `<circle cx="760" cy="760" r="300" fill="#ffe3b0" opacity=".25"/>`);
    farBank(L, 1060, r, { lights: night || o.lights, temple: 900 });
    river(L, 1060, r, { moon: { x: 860 } });
    let s = `<path d="M-900,-600H520V${G}H-900Z" fill="url(#phWall)"/>`;
    for (let x = -880; x < 520; x += 60) s += `<path d="M${x},-600V${G}" stroke="#4a3224" stroke-width="4"/>`;
    s += `<rect x="-120" y="${G - 760}" width="300" height="320" fill="${night ? "#ffc06a" : "#2a1c12"}" opacity="${night ? 0.8 : 1}" ${OUT}/><path d="M30,${G - 760}v320M-120,${G - 600}h300" stroke="${INK}" stroke-width="6"/>
      <rect x="-160" y="${G - 780}" width="40" height="360" fill="#5a3b26" ${OUT}/><rect x="180" y="${G - 780}" width="40" height="360" fill="#5a3b26" ${OUT}/>`;
    s += `<rect x="-900" y="${G}" width="1660" height="40" fill="url(#phPlank)" ${OUT}/><rect x="-900" y="${G + 40}" width="1660" height="900" fill="#1f150e"/>`;
    s += `<path d="M520,${G - 140}H760M520,${G - 140}V${G}" stroke="#3b2a1c" stroke-width="12"/>` + [560, 640, 720].map((x) => `<rect x="${x}" y="${G - 140}" width="12" height="140" fill="#3b2a1c"/>`).join("");
    // o.near: the river right at the foot of the steps (for shots looking down them)
    if (o.near) { s += `<rect x="640" y="${G + 230}" width="1600" height="1200" fill="url(#phWaterD)"/>`; for (let k = 0; k < 14; k++) s += `<path class="rip" d="M${f1(700 + r() * 900)},${f1(G + 260 + r() * 700)}h${f1(40 + r() * 120)}" stroke="#9fb0d8" stroke-width="4" stroke-linecap="round" opacity=".45"/>`; }
    s += `<g>${[0, 1, 2, 3, 4].map((k) => `<rect x="${760 + k * 50}" y="${G + 30 + k * 60}" width="120" height="16" rx="4" fill="#4a3424" ${OUT}/>`).join("")}</g>`;
    if (o.tray) s += `<g transform="translate(${o.tray.x},${G - 8})"><ellipse cx="0" cy="0" rx="150" ry="26" fill="#8a6a46" ${OUT}/>${krathong(-70, -26, 0.55, { lit: false })}${krathong(60, -26, 0.55, { lit: false })}</g>`;
    put(L.set, s);
    put(L.glow, `<path d="M380,${G - 520}v-60" stroke="#1a120c" stroke-width="6"/><rect class="lamp" x="362" y="${G - 520}" width="36" height="46" rx="8" fill="#ffd38a" ${OUT}/><circle cx="380" cy="${G - 496}" r="${night ? 320 : 220}" fill="url(#phBulb)"/>`);
  }

  // night interior: plank floor, the mosquito net (มุ้ง) with a lump inside, the open door to the river steps, wet footprints
  function bedroom(L, o = {}) {
    const id = o.id || "br", r = mk(o.seed || 61), G = o.ground ?? 1500;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#0b0e16"/>`);
    let s = `<path d="M-900,-600H2000V${G}H-900Z" fill="#2a1d14"/>`;
    for (let x = -880; x < 2000; x += 60) s += `<path d="M${x},-600V${G}" stroke="#1f150e" stroke-width="4"/>`;
    // the door on the right: moonlit river outside
    s += `<rect x="700" y="${G - 900}" width="360" height="900" fill="#14203d"/><rect x="700" y="${G - 360}" width="360" height="360" fill="url(#phWater)"/>
      <circle cx="930" cy="${G - 700}" r="46" fill="url(#phMoon)"/>${[0, 1, 2, 3].map((k) => `<path class="mrefl" d="M${880 + (k % 2) * 20},${G - 300 + k * 60}h90" stroke="#e8e2c0" stroke-width="6" stroke-linecap="round" opacity=".5"/>`).join("")}
      <rect x="680" y="${G - 920}" width="40" height="920" fill="#4a3424" ${OUT}/><rect x="1040" y="${G - 920}" width="40" height="920" fill="#4a3424" ${OUT}/><rect x="680" y="${G - 940}" width="400" height="40" fill="#4a3424" ${OUT}/>`;
    s += `<rect x="-900" y="${G}" width="2900" height="1000" fill="url(#phPlank)"/>`;
    for (let y = G + 60; y < 2600; y += 80) s += `<path d="M-900,${y}H2000" stroke="#2a1c12" stroke-width="4"/>`;
    // footprints from the door to the net: wet, toes long (#id-fp0..n revealed one by one)
    const steps = o.prints ?? 7;
    for (let k = 0; k < steps; k++) { const u = k / Math.max(1, steps - 1), x = 860 - u * 640 + (k % 2 ? 26 : -26), y = G + 70 + u * 260;
      s += `<g id="${id}-fp${k}" opacity="${o.printsOn ? 1 : 0}"><ellipse cx="${f1(x)}" cy="${f1(y)}" rx="22" ry="40" fill="#0d1a24" opacity=".85" transform="rotate(${-62} ${f1(x)} ${f1(y)})"/>${[0, 1, 2, 3, 4].map((t) => `<ellipse cx="${f1(x - 44 + t * 4)}" cy="${f1(y - 30 + t * 14)}" rx="7" ry="12" fill="#0d1a24" opacity=".85" transform="rotate(${-62} ${f1(x)} ${f1(y)})"/>`).join("")}
        <ellipse cx="${f1(x + 6)}" cy="${f1(y - 4)}" rx="10" ry="4" fill="#8fa6c8" opacity=".35"/></g>`; }
    // mosquito net hung from the ceiling, a lump (โต้ง) sleeping inside unless o.empty
    s += `<g id="${id}-net"><path d="M-520,${G + 120}L-470,${G - 620}H160L210,${G + 120}Z" fill="url(#phNet)" stroke="#c9d2dc" stroke-width="4"/>
      ${Array.from({ length: 14 }, (_, k) => `<path d="M${-500 + k * 50},${G - 620}L${-520 + k * 52},${G + 120}" stroke="#c9d2dc" stroke-width="1.5" opacity=".5"/>`).join("")}
      ${Array.from({ length: 12 }, (_, k) => `<path d="M-500,${G - 560 + k * 56}H190" stroke="#c9d2dc" stroke-width="1.5" opacity=".35"/>`).join("")}
      <path d="M-470,${G - 620}L-560,-600M160,${G - 620}L240,-600" stroke="#c9d2dc" stroke-width="3" opacity=".6"/></g>`;
    s += `<rect x="-440" y="${G + 40}" width="560" height="60" rx="18" fill="#c94a3a" ${OUT}/>`;
    put(L.set, s);
    put(L.light, `<path d="M700,${G - 900}L1060,${G - 900}L520,${G + 600}L-200,${G + 600}Z" fill="#9fb0d8" opacity=".07"/>`);
  }

  // under the river: green-black water, light from the surface, krathongs as dark shapes overhead, bubbles; pale arms from below
  function underRiver(L, o = {}) {
    const id = o.id || "ur", r = mk(o.seed || 67), SY = o.surface ?? 260;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#phUnder)"/>`);
    let s = `<rect x="-900" y="-600" width="2900" height="${SY + 600}" fill="#3b6a68" opacity=".55"/>`;
    s += `<path class="rip" d="M-900,${SY}Q-600,${SY - 20} -300,${SY}T300,${SY}T900,${SY}T1500,${SY}T2100,${SY}" stroke="#cfe6d8" stroke-width="8" fill="none" opacity=".75"/>`;
    for (let k = 0; k < 6; k++) s += `<path class="ray" d="M${-100 + k * 230},${SY}L${-20 + k * 230},${SY}L${160 + k * 240},2500L${-60 + k * 240},2500Z" fill="url(#phRay)"/>`;
    [[300, SY - 10], [760, SY - 6], [1040, SY - 12]].forEach(([x, y]) => { s += `<g><ellipse cx="${x}" cy="${y + 10}" rx="70" ry="18" fill="#0d1a18" opacity=".8"/><path d="M${x - 50},${y + 6}l20,-40l20,40l20,-46l20,46l20,-40" fill="#0d1a18" opacity=".8"/></g>`; });
    put(L.mid, s);
    let g = "";
    [[300, SY - 10], [760, SY - 6], [1040, SY - 12]].forEach(([x, y]) => (g += `<circle cx="${x}" cy="${y - 20}" r="70" fill="url(#phFlame)" opacity=".8"/>`));
    put(L.glow, g);
    let a = `<g id="${id}-arms">${paleHand(380, 2000, 1.3, 14)}${paleHand(700, 2050, 1.2, -16)}${paleHand(540, 2160, 1.0, 4)}</g>`;
    for (let k = 0; k < 26; k++) a += `<g class="bub" data-i="${k}"><circle cx="${f1(200 + r() * 700)}" cy="${f1(500 + r() * 1300)}" r="${f1(5 + r() * 14)}" fill="none" stroke="#e3f2ea" stroke-width="3" opacity=".7"/></g>`;
    put(L.set, a);
  }

  // ankle close-up on the planks by lantern light: a boy's shin and foot, five grey-green finger marks around it (#id-marks)
  function ankleMarks(L, o = {}) {
    const id = o.id || "am", r = mk(o.seed || 71);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#phPlank)"/>`);
    let s = "";
    for (let y = -560; y < 2600; y += 150) s += `<path d="M-900,${y}H2000" stroke="#241810" stroke-width="7"/>`;
    for (let k = 0; k < 40; k++) s += `<ellipse cx="${f1(-200 + r() * 1500)}" cy="${f1(-100 + r() * 2200)}" rx="${f1(6 + r() * 16)}" ry="${f1(4 + r() * 8)}" fill="#7f9bc0" opacity=".25"/>`;
    put(L.mid, s);
    const sk = CAST_COL.tong.skin;
    let a = `<path d="M180,-300C200,300 230,700 250,980L560,1020C540,700 520,300 520,-300Z" fill="${sk}" ${OUT}/>
      <path d="M250,980C230,1120 260,1240 380,1280L860,1300C930,1300 960,1240 920,1190C860,1130 700,1100 560,1020Z" fill="${sk}" ${OUT}/>
      ${[0, 1, 2, 3, 4].map((t) => `<ellipse cx="${940 - t * 3}" cy="${1210 + t * 18}" rx="${22 - t * 2}" ry="14" fill="${sk}" ${OUT}/>`).join("")}
      <path d="M340,840q40,-20 60,10" stroke="#b9805a" stroke-width="5" fill="none"/>`;
    // the marks: four long fingers wrapping the front of the ankle (bruised grey-green, darker at the tips), a thumb from behind
    const fing = (x0, y0, x1, y1, w) => `<path d="M${x0},${y0}Q${(x0 + x1) / 2},${Math.min(y0, y1) - 26} ${x1},${y1}" stroke="#4f6a5c" stroke-width="${w + 14}" fill="none" stroke-linecap="round" opacity=".28"/>
      <path d="M${x0},${y0}Q${(x0 + x1) / 2},${Math.min(y0, y1) - 26} ${x1},${y1}" stroke="#3d5548" stroke-width="${w}" fill="none" stroke-linecap="round" opacity=".7"/><ellipse cx="${x1}" cy="${y1}" rx="${w * 0.55}" ry="${w * 0.45}" fill="#26362e" opacity=".85"/>`;
    a += `<g id="${id}-marks" opacity="${o.marks ?? 1}">${fing(214, 690, 470, 668, 30)}${fing(218, 752, 500, 738, 32)}${fing(224, 814, 506, 806, 31)}${fing(232, 870, 470, 872, 26)}
      <path d="M548,610C520,690 520,760 540,812" stroke="#3d5548" stroke-width="34" fill="none" stroke-linecap="round" opacity=".6"/><ellipse cx="540" cy="812" rx="16" ry="13" fill="#26362e" opacity=".8"/></g>`;
    a += `<path d="M260,1000c-30,40 -10,90 30,120" stroke="#2f5a3a" stroke-width="7" fill="none" opacity=".8"/>`;
    for (let k = 0; k < 10; k++) a += `<path d="M${f1(240 + r() * 300)},${f1(600 + r() * 600)}c5,9 7,14 2,17c-5,-3 -5,-8 -2,-17z" fill="#cfe2e6" opacity=".8"/>`;
    put(L.set, a);
    put(L.glow, `<circle cx="420" cy="420" r="900" fill="url(#phBulb)" opacity=".5"/>`);
  }

  // the legend in pale ink on a dark page: a swimmer above, the drowned below holding the ankle, hair spreading like weed
  function legendPhrai(L, o = {}) {
    const id = o.id || "lg", r = mk(o.seed || 73);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#phPaper)"/>`);
    let s = `<rect x="70" y="250" width="940" height="1300" rx="20" fill="none" stroke="#c9a55a" stroke-width="4" opacity=".6"/>`;
    for (let k = 0; k < 9; k++) s += `<path d="M110,${520 + k * 6}Q330,${490 + k * 6} 540,${520 + k * 6}T970,${520 + k * 6}" stroke="#d9cfb2" stroke-width="2" fill="none" opacity="${(0.5 - k * 0.04).toFixed(2)}"/>`;
    // swimmer outline
    s += `<g id="${id}-sw" stroke="#e9dfc4" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="380" cy="470" r="34"/><path d="M410,490L620,520L800,500M520,505L470,420M600,515L660,430M620,520L640,700L660,840"/></g>`;
    // the drowned below: long hair, arm up to the ankle
    s += `<g id="${id}-ph" stroke="#9fc3b4" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <ellipse cx="560" cy="1180" rx="60" ry="76"/><path d="M536,1170l-8,6M590,1170l8,6" stroke-width="10"/>
      ${Array.from({ length: 10 }, (_, k) => `<path class="phair" data-i="${k}" d="M${520 + k * 8},1120Q${400 + k * 26},${1000 - k * 6} ${300 + k * 52},${960 + (k % 3) * 30}"/>`).join("")}
      <path d="M600,1110L650,960L660,860"/><path d="M640,860l-24,-34M660,856l-4,-44M676,862l18,-36"/>
      <path d="M560,1256L540,1440M560,1256L620,1430M500,1300L440,1380"/></g>`;
    s += `<path d="M120,1500h840" stroke="#c9a55a" stroke-width="3" opacity=".5"/>`;
    put(L.set, s);
  }

  // where the crowd stands at the edge of the pier at water level: people + their reflections; ตาเหม's boat with no reflection of him
  function reflections(L, o = {}) {
    const id = o.id || "rf", r = mk(o.seed || 79), WL = o.wl ?? 1240;
    skyNight(L, { moon: { x: 880, y: 300, r: 48 } }, r);
    let s = `<rect x="-900" y="${WL}" width="2900" height="${2600 - WL}" fill="url(#phWater)"/>`;
    s += `<rect x="-900" y="${WL - 30}" width="1300" height="30" fill="url(#phPlank)" ${OUT}/>`;
    const figs = [[-120, 1, 0], [20, 0.95, 1], [150, 0.7, 0], [270, 1.05, 2], [-260, 0.9, 0]];
    let up = "", dn = "";
    figs.forEach(([x, k, kind]) => {
      const h = 330 * k, head = kind === 1 ? `<path d="M${x + 18},${WL - 30 - h - 10}q30,20 20,70" stroke="#0a0f1c" stroke-width="14" fill="none" stroke-linecap="round"/>` : kind === 2 ? `<circle cx="${x - 10}" cy="${WL - 30 - h - 26}" r="16" fill="#0a0f1c"/>` : "";
      const body = (sy) => `<ellipse cx="${x}" cy="${WL - 30 - h + sy}" rx="${24 * k}" ry="${28 * k}" fill="#0a0f1c"/>${head}<path d="M${x - 36 * k},${WL - 30}L${x - 30 * k},${WL - 30 - h + 30 * k}Q${x},${WL - 30 - h + 16 * k} ${x + 30 * k},${WL - 30 - h + 30 * k}L${x + 36 * k},${WL - 30}Z" fill="#0a0f1c"/>`;
      up += `<g>${body(0)}<path d="M${x + 24 * k},${WL - 30 - h + 40}q14,30 10,120" stroke="#ffb35c" stroke-width="5" fill="none" opacity=".6"/></g>`;
      dn += `<g transform="translate(0,${2 * WL}) scale(1,-1)" opacity=".42">${body(0)}</g>`;
    });
    s += `<g id="${id}-refl" class="wob">${dn}</g>` + up;
    s += ferry(860, WL + 10, 0.85, { lamp: true, oar: false });
    s += `<g transform="translate(0,${2 * WL + 20}) scale(1,-1)" opacity=".35">${ferry(860, WL + 10, 0.85, { lamp: true, oar: false })}</g>`;
    for (let k = 0; k < 24; k++) s += `<path class="rip" d="M${f1(-700 + r() * 2500)},${f1(WL + 20 + r() * 700)}h${f1(40 + r() * 140)}" stroke="#6c7fa8" stroke-width="4" stroke-linecap="round" opacity=".4"/>`;
    put(L.set, s);
    put(L.glow, `<rect x="1129" y="${WL - 180}" width="20" height="24" rx="5" fill="#ffd38a"/><circle cx="1140" cy="${WL - 170}" r="160" fill="url(#phBulb)"/>`);
  }

  // ---------------- 2539-style legend in shadow puppets (two cloth screens, y 0 / 1600, each 900 tall) ----------------
  // S1: someone sinks under the river (#id-sink) and below, a พราย with hair fanned like weed (#id-phr) · S2: a child kneels at
  // the edge of a pier reaching for a krathong; from under the water a long arm (#id-arm, pivot at its shoulder) reaches up
  function phraiLegend(L, o = {}) {
    const id = o.id || "pl", P = "#170d06", CUT = "#ffd9a0", ROD = "#3a2414", LGY = [0, 1600];
    put(L.sky, `<rect x="-900" y="-1200" width="2900" height="5200" fill="#1c1009"/>`);
    const screen = (y0, y1) => `<rect x="-40" y="${y0}" width="1160" height="${y1 - y0}" fill="#e9a457"/>
      <circle class="lamp" cx="540" cy="${(y0 + y1) / 2}" r="${(y1 - y0) * 0.75}" fill="url(#clothglow)"/>
      ${Array.from({ length: 30 }, (_, k) => `<path d="M${-40 + k * 40},${y0}V${y1}" stroke="#c98a44" stroke-width="1.5" opacity=".25"/>`).join("")}
      <path d="M-40,${y0}H1120" stroke="${P}" stroke-width="18"/><path d="M-40,${y1}H1120" stroke="${P}" stroke-width="18"/>
      <path d="${Array.from({ length: 28 }, (_, k) => `M${-40 + k * 42},${y0 + 8}l21,26l21,-26`).join("")}" fill="${P}"/>
      <path d="${Array.from({ length: 28 }, (_, k) => `M${-40 + k * 42},${y1 - 8}l21,-26l21,26`).join("")}" fill="${P}"/>`;
    const rod = (x, y, len = 220) => `<path d="M${x},${y}V${y + len}" stroke="${ROD}" stroke-width="6"/>`;
    const pup = (x, y, inner, rot = 0, pid = "") => `<g class="pup" data-ox="${x}" data-oy="${y}"${pid ? ` id="${pid}"` : ""}>${rod(x, y)}<g transform="translate(${x},${y}) rotate(${rot})">${inner}</g></g>`;
    const waves = (y) => `<path d="M-40,${y}${Array.from({ length: 24 }, (_, k) => `q24,-22 48,0`).join("")}V${y + 460}H-40Z" fill="${P}" opacity=".9"/>
      ${Array.from({ length: 6 }, (_, k) => `<path d="M${40 + k * 180},${y + 60 + (k % 2) * 40}q30,-14 60,0t60,0" stroke="${CUT}" stroke-width="5" fill="none" opacity=".55"/>`).join("")}`;
    const person = (s) => `<g transform="scale(${s})"><circle cx="0" cy="-200" r="30" fill="${P}"/><path d="M-40,-30L-30,-170H30L40,-30Z" fill="${P}"/><path d="M-14,-30V30M14,-30V30" stroke="${P}" stroke-width="12"/>
      <path d="M-28,-160L-80,-230M28,-160L80,-230" stroke="${P}" stroke-width="12" stroke-linecap="round"/><ellipse cx="0" cy="-120" rx="8" ry="14" fill="${CUT}"/></g>`;
    const phrai = (s, armLen = 0) => `<g transform="scale(${s})">${Array.from({ length: 9 }, (_, k) => { const a = (-160 + k * 17.5) * Math.PI / 180;
        return `<path d="M0,-200Q${f1(Math.cos(a) * 70)},${f1(-200 + Math.sin(a) * 70 - 20)} ${f1(Math.cos(a) * 150)},${f1(-200 + Math.sin(a) * 150 - 30)}" stroke="${P}" stroke-width="10" fill="none" stroke-linecap="round"/>`; }).join("")}
      <circle cx="0" cy="-200" r="32" fill="${P}"/><ellipse cx="10" cy="-204" rx="6" ry="4" fill="${CUT}"/><path d="M-36,-170C-50,-90 -40,-20 -10,30L10,30C40,-20 50,-90 36,-170Z" fill="${P}"/>
      <path d="M-30,-150L-90,-80" stroke="${P}" stroke-width="12" stroke-linecap="round"/></g>`;
    let s = LGY.map((y) => screen(y, y + 900)).join("");
    // S1
    s += `<circle cx="820" cy="150" r="56" fill="${CUT}"/>` + waves(380);
    s += pup(380, 640, person(0.9), 160, `${id}-sink`);
    for (let k = 0; k < 6; k++) s += `<circle class="bub" data-i="${k}" cx="${360 + (k % 3) * 22}" cy="${560 - k * 34}" r="${6 + (k % 3) * 3}" fill="none" stroke="${CUT}" stroke-width="3"/>`;
    s += `<g id="${id}-phr" opacity="0">${pup(720, 860, phrai(1.0), 0)}</g><path d="M470,640Q600,700 650,760" stroke="${CUT}" stroke-width="5" stroke-dasharray="14 12" fill="none" opacity=".7"/>`;
    // S2
    const Y = LGY[1];
    s += waves(Y + 420) + `<rect x="-40" y="${Y + 340}" width="560" height="40" fill="${P}"/>${[40, 220, 400].map((x) => `<rect x="${x}" y="${Y + 380}" width="22" height="400" fill="${P}"/>`).join("")}`;
    s += pup(470, Y + 340, `<g><circle cx="0" cy="-120" r="26" fill="${P}"/><path d="M-30,0L-20,-96H24L34,0Z" fill="${P}" transform="rotate(30 0 0)"/><path d="M20,-80L70,-10" stroke="${P}" stroke-width="11" stroke-linecap="round"/></g>`, 0);
    s += `<g transform="translate(640,${Y + 410})"><path d="M-50,0Q0,-30 50,0Z" fill="${P}"/><path d="M-20,-14Q0,-60 20,-14Z" fill="${P}"/><path d="M0,-58v-26" stroke="${P}" stroke-width="5"/><circle class="lamp" cx="0" cy="-92" r="10" fill="#fff2c8"/></g>`;
    s += pup(800, Y + 860, phrai(1.05), 0) + `<g id="${id}-arm" transform="rotate(0 760 ${Y + 650})"><path d="M760,${Y + 650}L640,${Y + 470}" stroke="${P}" stroke-width="13" stroke-linecap="round"/>
      ${[-16, -4, 8].map((d) => `<path d="M640,${Y + 470}l${d - 10},-34" stroke="${P}" stroke-width="7" stroke-linecap="round"/>`).join("")}</g>`;
    // S3 (y 3200): the พราย herself, close — a coal-black puppet, eyes cut through and lit green (#id-eyes), hair spread like
    // river weed; the lure on the left (a krathong, its coins glowing, #id-lure), her call (#id-call), someone wading on the right
    // (#id-vic) and the long arm that takes his leg (#id-arm3)
    const Y3 = 3200;
    s += screen(Y3, Y3 + 900);
    s += `<g id="${id}-big">${Array.from({ length: 13 }, (_, k) => { const a = (-172 + k * 13.6) * Math.PI / 180;
        return `<path class="phair" data-i="${k}" d="M540,${Y3 + 330}Q${f1(540 + Math.cos(a) * 130)},${f1(Y3 + 300 + Math.sin(a) * 150)} ${f1(540 + Math.cos(a) * 320)},${f1(Y3 + 290 + Math.sin(a) * 270)}" stroke="${P}" stroke-width="${24 - (k % 3) * 6}" fill="none" stroke-linecap="round"/>`; }).join("")}
      <ellipse cx="540" cy="${Y3 + 400}" rx="118" ry="148" fill="${P}"/><path d="M400,${Y3 + 500}C420,${Y3 + 560} 660,${Y3 + 560} 680,${Y3 + 500}L720,${Y3 + 660}H360Z" fill="${P}"/>
      ${[-70, -40, 40, 70].map((dx, k) => `<path d="M${540 + dx},${Y3 + 290}C${540 + dx * 1.1},${Y3 + 380} ${540 + dx * 0.9},${Y3 + 450} ${540 + dx * 1.05},${Y3 + 540 + (k % 2) * 30}" stroke="${P}" stroke-width="12" fill="none"/>`).join("")}
      <ellipse cx="540" cy="${Y3 + 478}" rx="15" ry="22" fill="${CUT}" opacity=".55"/>
      <g id="${id}-eyes" opacity="0">${[494, 586].map((x) => `<circle cx="${x}" cy="${Y3 + 392}" r="60" fill="#7dff6a" opacity=".22"/><ellipse cx="${x}" cy="${Y3 + 392}" rx="24" ry="14" fill="#7dff6a"/><ellipse cx="${x}" cy="${Y3 + 392}" rx="10" ry="7" fill="#f2ffe4"/>`).join("")}</g></g>`;
    s += `<g id="${id}-call" opacity="0">${[0, 1, 2].map((k) => `<path d="M${700 + k * 40},${Y3 + 330 - k * 20}q${30 + k * 10},${50 + k * 14} 0,${100 + k * 40}" stroke="#7dff6a" stroke-width="7" fill="none" stroke-linecap="round" opacity="${0.9 - k * 0.2}"/>`).join("")}</g>`;
    s += `<g id="${id}-lure">${pup(190, Y3 + 610, `<g><path d="M-62,0Q0,-34 62,0Z" fill="${P}"/><path d="M-26,-14Q0,-66 26,-14Z" fill="${P}"/><path d="M0,-60v-22" stroke="${P}" stroke-width="5"/><circle class="lamp" cx="0" cy="-90" r="10" fill="#fff2c8"/>
      ${[-36, -14, 10, 32].map((x) => `<circle class="kcoin" cx="${x}" cy="-6" r="8" fill="#ffe08a"/>`).join("")}</g>`, 0)}</g>`;
    s += pup(880, Y3 + 640, person(0.62), 0, `${id}-vic`);
    s += waves(Y3 + 600);
    s += `<g id="${id}-arm3" opacity="0"><path d="M660,${Y3 + 640}Q760,${Y3 + 790} 868,${Y3 + 668}" stroke="#7dff6a" stroke-width="20" fill="none" stroke-linecap="round" opacity=".45"/><path d="M660,${Y3 + 640}Q760,${Y3 + 790} 868,${Y3 + 668}" stroke="${P}" stroke-width="12" fill="none" stroke-linecap="round"/>
      ${[-14, 0, 14].map((d) => `<path d="M868,${Y3 + 668}l${18 + d * 0.4},${-22 + d}" stroke="${P}" stroke-width="7" stroke-linecap="round"/>`).join("")}</g>`;
    put(L.set, s);
  }

  // ---------------- chapter card: one krathong close up, a paper flag "3 ชั่วโมงก่อน", its candle growing back (time rewinding) ----------------
  function krathongCard(L, o = {}) {
    const id = o.id || "kc", r = mk(o.seed || 83), X = 540, Y = 1260, K = 2.4;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#phWater)"/>`);
    let m = "";
    for (let k = 0; k < 40; k++) m += `<path class="mrefl" d="M${f1(-200 + r() * 1500)},${f1(200 + r() * 1700)}h${f1(30 + r() * 140)}" stroke="#d9d4b8" stroke-width="${f1(3 + r() * 4)}" stroke-linecap="round" opacity="${(0.1 + r() * 0.25).toFixed(2)}"/>`;
    put(L.mid, m);
    let s = krathong(X, Y, K, { lit: false, dx: 12 }) + krefl(X, Y, K);
    // the candle (pivot at its base) and its flame, drawn over the krathong's own candle
    s += `<g id="${id}-candle" transform="translate(${X},${Y - 58 * K}) scale(1,1)"><rect x="-13" y="-70" width="26" height="70" rx="5" fill="#f4f0e6" stroke="#7a6a52" stroke-width="3"/><path d="M-13,-56h26" stroke="#e0d8c4" stroke-width="4"/>
      <g id="${id}-flame"><path class="kflame" d="M0,-122C-18,-96 -16,-80 0,-72C16,-80 18,-96 0,-122Z" fill="#ffd36a" stroke="#ff9a3c" stroke-width="3"/></g></g>`;
    // the flag on a stick
    s += `<g id="${id}-flag"><path d="M${X - 60},${Y - 40}L${X - 120},${Y - 470}" stroke="#c9a86a" stroke-width="8" stroke-linecap="round"/>
      <path d="M${X - 118},${Y - 470}L${X + 250},${Y - 450}L${X + 236},${Y - 330}L${X - 104},${Y - 350}Z" fill="#f4ecd8" stroke="${INK}" stroke-width="4"/>
      <text x="${X + 66}" y="${Y - 375}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#b8261c" transform="rotate(3 ${X + 66} ${Y - 390})">${o.text || "3 ชั่วโมงก่อน"}</text></g>`;
    put(L.set, s);
    put(L.glow, `<g class="kglw" id="${id}-glow"><circle cx="${X}" cy="${Y - 58 * K - 96}" r="420" fill="url(#phFlame)"/></g>`);
  }

  // ---------------- end card: the sign by the pier, wet; a paper note pinned on it names the next episode ----------------
  function pierSign(L, o = {}) {
    const id = o.id || "sg", r = mk(o.seed || 89);
    skyNight(L, { moon: { x: 860, y: 260, r: 50 } }, r);
    river(L, 1300, r, {});
    let s = `<rect x="160" y="900" width="34" height="1300" fill="#3b2a1c" ${OUT}/><rect x="886" y="900" width="34" height="1300" fill="#3b2a1c" ${OUT}/>`;
    s += `<g id="${id}-sign" transform="rotate(-2 540 1000)"><rect x="110" y="560" width="860" height="560" rx="14" fill="#7a5a3c" ${OUT}/>${[640, 720, 800, 880, 960, 1040].map((y) => `<path d="M120,${y}H960" stroke="#5e412c" stroke-width="4"/>`).join("")}
      <rect x="110" y="560" width="860" height="110" rx="14" fill="#b8261c" ${OUT}/><text x="540" y="642" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="74" fill="#fff4ea">ประกาศ</text>
      <text x="540" y="770" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="92" fill="#f4ecd8">ห้ามลงเล่นน้ำ</text>
      <g transform="rotate(4 560 950)"><rect x="300" y="820" width="520" height="250" fill="#f2ecdc" stroke="${INK}" stroke-width="3"/><circle cx="560" cy="836" r="10" fill="#b8261c"/>
        <text x="560" y="900" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#a8140c">${o.ep || "ตอนที่ 2"}</text>
        <text x="560" y="980" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="70" fill="#a8140c">${o.title || "อย่าอุ้มพาดบ่า"}</text>
        <text x="760" y="1046" text-anchor="end" font-family="Kanit" font-weight="700" font-size="30" fill="#5a4a3a">— ตาเหม เรือจ้าง</text></g></g>`;
    for (let k = 0; k < 7; k++) s += `<g class="drip" data-i="${k}"><path d="M${f1(150 + k * 120 + r() * 40)},1112c-7,12 -7,20 0,22c7,-2 7,-10 0,-22z" fill="#9fc3d8" opacity=".85"/></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="760" r="760" fill="url(#phBulb)" opacity=".45"/>`);
  }

  // ---------------- top-down on the planks: the boy who isn't breathing, and the hands that bring him back ----------------
  // #id-chest (scaleY for compressions), #id-hands (two stacked hands on the chest), #id-airway (a hand on the forehead and two
  // fingers under the chin), #id-lips (blue; fill to pink when he breathes), #id-water (water coughed up beside his mouth)
  function cprTop(L, o = {}) {
    const id = o.id || "cp", r = mk(o.seed || 97), sk = CAST_COL.tong.skin, red = "#9a2e27", X = 540;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#phPlank)"/>`);
    let m = "";
    for (let x = -880; x < 2000; x += 150) m += `<path d="M${x},-600V2800" stroke="#241810" stroke-width="8"/>${[0, 1, 2].map((k) => `<circle cx="${x + 20}" cy="${-300 + k * 1100 + (x % 300)}" r="6" fill="#1a120c"/>`).join("")}`;
    m += `<ellipse cx="${X}" cy="1080" rx="520" ry="760" fill="#0d1a24" opacity=".45"/>`;
    // the edge of the pier and the black river beyond it (we look straight down)
    m += `<rect x="960" y="-600" width="1200" height="3400" fill="url(#phWater)"/><rect x="940" y="-600" width="40" height="3400" fill="#2a1c12" ${OUT}/>`;
    for (let k = 0; k < 12; k++) m += `<path class="mrefl" d="M${f1(1000 + r() * 400)},${f1(r() * 2000)}h${f1(30 + r() * 90)}" stroke="#d9d4b8" stroke-width="4" stroke-linecap="round" opacity=".25"/>`;
    for (let k = 0; k < 24; k++) m += `<ellipse cx="${f1(140 + r() * 800)}" cy="${f1(300 + r() * 1500)}" rx="${f1(6 + r() * 18)}" ry="${f1(4 + r() * 10)}" fill="#7f9bc0" opacity=".3"/>`;
    put(L.mid, m);
    // the rescuer's knees on the planks at the left edge (navy track pants)
    put(L.set, `<g opacity=".95">${[880, 1180].map((y) => `<path d="M-120,${y}Q60,${y - 40} 150,${y + 30}Q60,${y + 140} -120,${y + 120}Z" fill="#2b3d5e" ${OUT}/>`).join("")}</g>`);
    let b = `<g id="${id}-body" transform="rotate(-6 ${X} 1100)">
      <path d="M${X - 90},1380L${X - 110},1840Q${X - 104},1880 ${X - 64},1880L${X - 40},1390Z" fill="#7d6e50" ${OUT}/><path d="M${X + 90},1380L${X + 110},1840Q${X + 104},1880 ${X + 64},1880L${X + 40},1390Z" fill="#7d6e50" ${OUT}/>
      <ellipse cx="${X - 86}" cy="1900" rx="38" ry="26" fill="${sk}" ${OUT}/><ellipse cx="${X + 86}" cy="1900" rx="38" ry="26" fill="${sk}" ${OUT}/>
      <path d="M${X - 140},870L${X - 220},1300Q${X - 220},1340 ${X - 190},1344L${X - 150},1340L${X - 120},950Z" fill="${red}" ${OUT}/><path d="M${X + 140},870L${X + 220},1300Q${X + 220},1340 ${X + 190},1344L${X + 150},1340L${X + 120},950Z" fill="${red}" ${OUT}/>
      <ellipse cx="${X - 200}" cy="1360" rx="30" ry="36" fill="${sk}" ${OUT}/><ellipse cx="${X + 200}" cy="1360" rx="30" ry="36" fill="${sk}" ${OUT}/>
      <g id="${id}-chest"><path d="M${X - 150},860Q${X},820 ${X + 150},860L${X + 120},1400H${X - 120}Z" fill="${red}" ${OUT}/><path d="M${X},990l14,28l32,4l-24,22l6,32l-28,-16l-28,16l6,-32l-24,-22l32,-4z" fill="#c9a33a" ${OUT}/>
        <path d="M${X - 40},850Q${X},880 ${X + 40},850" stroke="#7d241e" stroke-width="10" fill="none"/></g>
      <rect x="${X - 34}" y="790" width="68" height="70" fill="${sk}" ${OUT}/>
      <g id="${id}-head"><ellipse cx="${X}" cy="690" rx="120" ry="130" fill="${sk}" ${OUT}/><path d="M${X - 122},650Q${X - 120},540 ${X},530Q${X + 120},540 ${X + 122},650Q${X + 90},590 ${X},586Q${X - 90},590 ${X - 122},650Z" fill="#2a2220" ${OUT}/>
        <path d="M${X - 64},690q22,10 44,0M${X + 20},690q22,10 44,0" stroke="#3a2a22" stroke-width="7" fill="none" stroke-linecap="round"/>
        <ellipse id="${id}-lips" cx="${X}" cy="760" rx="26" ry="11" fill="#6f8fb0" stroke="#3a2a22" stroke-width="4"/>
        ${[[-60, 640], [70, 720], [-30, 760], [40, 620]].map(([dx, dy]) => `<path d="M${X + dx},${dy}c5,9 7,14 2,17c-5,-3 -5,-8 -2,-17z" fill="#cfe2e6" opacity=".85"/>`).join("")}</g>
      <g id="${id}-water" opacity="0"><ellipse cx="${X + 130}" cy="790" rx="90" ry="40" fill="#9fc3d8" opacity=".6"/><path d="M${X + 26},770q50,10 90,20" stroke="#cfe2e6" stroke-width="10" stroke-linecap="round" fill="none"/></g></g>`;
    // the rescuer's hands: stacked on the middle of the chest (sleeves come from the left, white tee)
    const hand = (x, y, rot, k) => `<g transform="translate(${x},${y}) rotate(${rot})"><path d="M-260,-28H-60V28H-260Z" fill="#f2f0ea" ${OUT}/><ellipse cx="0" cy="0" rx="70" ry="54" fill="#e8b48a" ${OUT}/>${[-30, -10, 10, 30].map((fy) => `<path d="M40,${fy}h${42 - Math.abs(fy) * 0.3}" stroke="${INK}" stroke-width="22" stroke-linecap="round"/><path d="M40,${fy}h${42 - Math.abs(fy) * 0.3}" stroke="#e8b48a" stroke-width="15" stroke-linecap="round"/>`).join("")}</g>`;
    b += `<g id="${id}-hands" opacity="${o.hands ?? 0}">${hand(X - 10, 1060, 0, 0)}${hand(X + 4, 1046, -8, 1)}</g>`;
    b += `<g id="${id}-airway" opacity="${o.airway ?? 0}">${hand(X - 30, 600, -20, 2)}<g transform="translate(${X + 120},800) rotate(160)"><path d="M-260,-24H-60V24H-260Z" fill="#f2f0ea" ${OUT}/><ellipse cx="0" cy="0" rx="56" ry="44" fill="#e8b48a" ${OUT}/>
      <path d="M40,-12h60M40,12h56" stroke="${INK}" stroke-width="22" stroke-linecap="round"/><path d="M40,-12h60M40,12h56" stroke="#e8b48a" stroke-width="15" stroke-linecap="round"/></g></g>`;
    put(L.set, b);
    put(L.glow, `<circle cx="180" cy="260" r="900" fill="url(#phBulb)" opacity=".5"/>`);
  }

  // ---------------- the village road under water at night: stilt houses, poles, a sign half drowned, an ambulance stuck far off ----------------
  function floodRoad(L, o = {}) {
    const id = o.id || "fr", r = mk(o.seed || 101), W = o.water ?? 1250;
    skyNight(L, { moon: { x: 300, y: 260, r: 52 } }, r);
    let far = `<path d="M-900,${W - 40}`;
    for (let x = -900; x <= 2000; x += 60) far += `L${x},${f1(W - 120 - r() * 120)}`;
    far += `L2000,${W}H-900Z" fill="#070c18"/>`;
    put(L.far, far);
    let s = "";
    [[-260, 1.0], [1180, 0.9]].forEach(([x, k]) => { s += `<g transform="translate(${x},${W}) scale(${k})"><rect x="-200" y="-520" width="400" height="300" fill="#3b2a1c" ${OUT}/><path d="M-240,-520L0,-700L240,-520Z" fill="#2a1d14" ${OUT}/>
      <rect x="-120" y="-460" width="90" height="110" fill="#ffc06a" opacity=".85" ${OUT}/>${[-170, -60, 60, 170].map((px) => `<rect x="${px - 10}" y="-220" width="20" height="420" fill="#2a1c12"/>`).join("")}</g>`; });
    for (let k = 0; k < 4; k++) { const x = -400 + k * 520; s += `<path d="M${x},${W + 300}V${W - 700}" stroke="#1a120c" stroke-width="18"/><path d="M${x - 70},${W - 650}h140" stroke="#1a120c" stroke-width="10"/>`; }
    s += `<path d="M-400,${W - 640}Q-140,${W - 560} 120,${W - 640}T640,${W - 640}T1160,${W - 640}" stroke="#0d1220" stroke-width="5" fill="none"/>`;
    // the road sign, half under water
    s += `<g transform="translate(300,${W + 40}) rotate(-6)"><path d="M0,0V-260" stroke="#8a9096" stroke-width="12"/><rect x="-170" y="-380" width="340" height="140" rx="10" fill="#2f6f9f" stroke="#eaf4ff" stroke-width="6"/>
      <text x="0" y="-322" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#eaf4ff">โรงพยาบาล</text><text x="0" y="-268" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="#eaf4ff">4 กม. →</text></g>`;
    // the water: dark, the moon streak, debris, ripples; the near part (#id-wfront) goes over anyone wading
    s += `<rect x="-900" y="${W}" width="2900" height="${2600 - W}" fill="url(#phWaterD)" opacity=".95"/>`;
    for (let k = 0; k < 22; k++) s += `<path class="rip" d="M${f1(-500 + r() * 2000)},${f1(W + 20 + r() * 900)}h${f1(40 + r() * 140)}" stroke="#9fb0d8" stroke-width="4" stroke-linecap="round" opacity=".4"/>`;
    s += `<path class="mrefl" d="M280,${W + 60}h60M260,${W + 120}h90M290,${W + 190}h50" stroke="#e8e2c0" stroke-width="7" stroke-linecap="round" opacity=".5"/>`;
    // the ambulance, far down the road, stuck: white van, red cross, the light bar (classes siren / sirenb flash in the shot)
    s += `<g transform="translate(${o.amb ?? 720},${W + 70}) scale(.7)"><rect x="-120" y="-120" width="240" height="110" rx="12" fill="#e9eef0" stroke="#2e2a26" stroke-width="4"/><rect x="60" y="-150" width="70" height="40" rx="6" fill="#e9eef0" stroke="#2e2a26" stroke-width="4"/>
      <path d="M-20,-90h20v-20h16v20h20v16h-20v20h-16v-20h-20z" fill="#d8322a"/><rect x="-60" y="-138" width="50" height="16" fill="#ff3a3a" class="siren"/><rect x="-6" y="-138" width="50" height="16" fill="#3a7aff" class="sirenb"/></g>`;
    s += `<rect x="${(o.amb ?? 720) - 120}" y="${W + 30}" width="240" height="60" fill="#3b4766" opacity=".85"/>`;
    s += [[-120, W + 220], [820, W + 360], [480, W + 620]].map(([x, y], k) => `<g transform="translate(${x},${y}) rotate(${k * 17 - 10})"><rect x="-50" y="-12" width="100" height="24" rx="6" fill="#5a4330" ${OUT}/></g>`).join("");
    put(L.set, s);
    put(L.glow, `<g class="siren"><circle cx="${(o.amb ?? 720) - 20}" cy="${W - 10}" r="260" fill="url(#phSiren)"/></g><g class="sirenb"><circle cx="${(o.amb ?? 720) + 20}" cy="${W - 10}" r="260" fill="url(#phSirenB)"/></g>`);
  }

  // ---------------- from under the river looking up: the ferry's hull on the bright surface, a dozen pale hands pushing it ----------------
  function hullHands(L, o = {}) {
    const id = o.id || "hh", SY = o.surface ?? 420;
    underRiver(L, { ...o, id, surface: SY });
    const hull = `<path d="M-330,-40H300Q370,-44 400,-96Q396,-30 330,10Q300,30 250,32H-300Q-350,26 -362,-10Q-366,-34 -330,-40Z" fill="#0b1614"/>`;
    let s = `<g transform="translate(560,${SY + 20}) scale(1.6,-1.6)">${hull}</g>`;
    const hx = [-420, -330, -240, -150, -60, 30, 120, 210, 300, 390, 480];
    s += `<g id="${id}-hands">${hx.map((dx, k) => `<g class="hhand" data-i="${k}">${paleHand(560 + dx, SY + 92 + (k % 3) * 14, 0.62 + (k % 3) * 0.06, (k % 2 ? 1 : -1) * (4 + (k % 4) * 3))}</g>`).join("")}</g>`;
    s += `<g opacity=".7">${[[-300, 820], [140, 900], [420, 760]].map(([dx, y]) => drownedFace(560 + dx, SY + y, 0.6, { op: 0.6 })).join("")}</g>`;
    put(L.set, s);
  }

  // looping motion: krathongs drift and bob, flames flicker, ripples slide, the moon streak shimmers, hair sways, bubbles rise
  function life(tl, scope, t0, dur) {
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    q(".ktg").forEach((el, i) => {
      tl.fromTo(el, { x: 0 }, { x: +(el.dataset.dx || 40), duration: dur, ease: "none", immediateRender: false }, t0);
      tl.fromTo(el, { y: -3 }, { y: 4, duration: 1.3 + (i % 3) * 0.3, repeat: Math.ceil(dur / 1.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (+(el.dataset.ph || 0)) * 0.2);
    });
    q(".kflame").forEach((el, i) => tl.fromTo(el, { scaleY: 0.86, scaleX: 1.06 }, { scaleY: 1.12, scaleX: 0.92, svgOrigin: "0 -82", duration: 0.11 + (i % 4) * 0.03, repeat: Math.ceil(dur / 0.11), yoyo: true, ease: "none", immediateRender: false }, t0));
    q(".kglw").forEach((el, i) => tl.fromTo(el, { opacity: 0.8 }, { opacity: 1, duration: 0.14 + (i % 3) * 0.05, repeat: Math.ceil(dur / 0.14), yoyo: true, ease: "none", immediateRender: false }, t0));
    q(".rip").forEach((el, i) => tl.fromTo(el, { x: -10, opacity: 0.25 }, { x: 12, opacity: 0.6, duration: 1 + (i % 4) * 0.25, repeat: Math.ceil(dur / 1), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 5) * 0.12));
    q(".mrefl").forEach((el, i) => tl.fromTo(el, { scaleX: 0.7, opacity: 0.25 }, { scaleX: 1.15, opacity: 0.7, transformOrigin: "50% 50%", duration: 0.6 + (i % 4) * 0.2, repeat: Math.ceil(dur / 0.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 6) * 0.1));
    q(".slt").forEach((el, i) => tl.fromTo(el, { opacity: 0.45 }, { opacity: 1, duration: 0.5 + (i % 5) * 0.12, repeat: Math.ceil(dur / 0.5), yoyo: true, ease: "none", immediateRender: false }, t0 + (i % 7) * 0.07));
    q(".lamp").forEach((el, i) => tl.fromTo(el, { opacity: 0.85 }, { opacity: 1, duration: 0.13 + (i % 3) * 0.05, repeat: Math.ceil(dur / 0.13), yoyo: true, ease: "none", immediateRender: false }, t0));
    q(".phair").forEach((el, i) => tl.fromTo(el, { rotation: -4 }, { rotation: 5, svgOrigin: "0 -20", duration: 1.6 + (i % 3) * 0.4, repeat: Math.ceil(dur / 1.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.1));
    q(".pface").forEach((el, i) => tl.fromTo(el, { y: 0 }, { y: -26, duration: 2.4 + i * 0.3, repeat: Math.ceil(dur / 2.4), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".geye").forEach((el, i) => tl.fromTo(el, { opacity: +(el.getAttribute("opacity") || 1) }, { opacity: 0.45 * +(el.getAttribute("opacity") || 1), duration: 0.45 + (i % 4) * 0.12, repeat: Math.ceil(dur / 0.45), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 5) * 0.1));
    q(".hhand").forEach((el, i) => tl.fromTo(el, { y: 0 }, { y: -14, duration: 0.5 + (i % 3) * 0.12, repeat: Math.ceil(dur / 0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 4) * 0.1));
    q(".siren").forEach((el) => { for (let t = 0; t < dur; t += 0.5) { tl.set(el, { opacity: 1 }, t0 + t); tl.set(el, { opacity: 0.15 }, t0 + t + 0.25); } });
    q(".sirenb").forEach((el) => { for (let t = 0; t < dur; t += 0.5) { tl.set(el, { opacity: 0.15 }, t0 + t); tl.set(el, { opacity: 1 }, t0 + t + 0.25); } });
    q(".drip").forEach((el, i) => tl.fromTo(el, { y: 0, opacity: 0.9 }, { y: 140, opacity: 0, duration: 0.9 + (i % 3) * 0.2, repeat: Math.ceil(dur / 0.9), ease: "power2.in", immediateRender: false }, t0 + (i % 5) * 0.17));
    q(".bub").forEach((el, i) => tl.fromTo(el, { y: 0, opacity: 0 }, { y: -260 - (i % 4) * 60, opacity: 0.9, duration: 1.6 + (i % 5) * 0.3, repeat: Math.ceil(dur / 1.6), ease: "power1.in", immediateRender: false }, t0 + (i % 7) * 0.2));
    q(".ray").forEach((el, i) => tl.fromTo(el, { opacity: 0.4 }, { opacity: 0.95, duration: 1.8 + i * 0.3, repeat: Math.ceil(dur / 1.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".wob").forEach((el) => tl.fromTo(el, { skewX: -2, scaleY: 1 }, { skewX: 2, scaleY: 1.03, transformOrigin: "50% 0%", duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
  }

  // ---------------- cast ----------------
  const CAST_COL = { tong: { skin: "#e3ab80", top: "#d8443a" } };
  Object.assign(Rig.CAST, {
    praew: { // แพรว: school swimmer, white tee with a blue wave, navy track pants with a stripe, high ponytail, goggles round her neck
      skin: "#e8b48a", skinS: "#c88f66", top: "#f2f0ea", topS: "#d3d1ca", sleeve: "#f2f0ea", sleeveS: "#d3d1ca", forearm: "#e8b48a", forearmS: "#c88f66",
      pants: "#2b3d5e", pantsS: "#1f2d47", shoe: "#f2f0ea", belt: "#2b3d5e",
      torsoExtra: `<path d="M-40,-410q14,-16 28,0t28,0t28,0" stroke="#2f7fbf" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M-36,-388q14,-14 28,0t28,0t28,0" stroke="#5fb0e0" stroke-width="7" fill="none" stroke-linecap="round"/>
        <path d="M-34,-484Q0,-454 34,-484" stroke="#1f2d47" stroke-width="5" fill="none"/><ellipse cx="-16" cy="-462" rx="14" ry="10" fill="#4fb0e0" ${OUT}/><ellipse cx="16" cy="-462" rx="14" ry="10" fill="#4fb0e0" ${OUT}/><path d="M-2,-462h4" stroke="${INK}" stroke-width="4"/>`,
      hair: `<path d="M-30,-604Q-40,-640 -10,-640Q20,-638 6,-604Z" fill="#1a1513" ${OUT}/><path d="M-6,-630Q-90,-640 -96,-560Q-98,-500 -70,-470Q-80,-530 -40,-590Z" fill="#1a1513" ${OUT}/>
        <path d="M-48,-548Q-54,-606 0,-610Q52,-608 48,-556Q36,-584 2,-586Q-30,-584 -40,-560Q-42,-552 -48,-546Z" fill="#1a1513" ${OUT}/><circle cx="-14" cy="-618" r="10" fill="#2f7fbf" ${OUT}/>`,
      face: `<g fill="#e09a86" opacity=".55"><ellipse cx="-24" cy="-526" rx="7" ry="3.5"/><ellipse cx="30" cy="-526" rx="7" ry="3.5"/></g>`,
    },
    tong: { // โต้ง: ten, red tee with a yellow star, khaki shorts-length trousers, buzz cut, flip-flops
      skin: "#e3ab80", skinS: "#c28a60", top: "#d8443a", topS: "#b3342b", sleeve: "#d8443a", sleeveS: "#b3342b", forearm: "#e3ab80", forearmS: "#c28a60",
      pants: "#b3a07a", pantsS: "#948260", shoe: "#3f7fbf", belt: "#948260",
      torsoExtra: `<path d="M0,-440l9,18l20,3l-15,14l4,20l-18,-10l-18,10l4,-20l-15,-14l20,-3z" fill="#f2c55c" ${OUT}/>`,
      hair: `<path d="M-48,-552Q-50,-608 0,-612Q50,-608 48,-554Q42,-576 0,-580Q-42,-576 -48,-552Z" fill="#2a2220" ${OUT}/>`,
      face: `<g fill="#e09a86" opacity=".5"><ellipse cx="-24" cy="-526" rx="7" ry="3.5"/><ellipse cx="30" cy="-526" rx="7" ry="3.5"/></g>`,
    },
    yai: { // ยายเพิ่ม: lace blouse (คอกระเช้า), purple sash, dark purple sarong, grey bun, reading glasses on a cord
      skin: "#c99a74", skinS: "#a87a56", top: "#efe6d6", topS: "#d3c8b4", sleeve: "#efe6d6", sleeveS: "#d3c8b4", forearm: "#c99a74", forearmS: "#a87a56",
      pants: "#4a2f52", pantsS: "#36213c", shoe: "#2a2420", belt: "#4a2f52",
      torsoExtra: `<path d="M-40,-484Q0,-440 40,-484" stroke="#c9b9a0" stroke-width="5" fill="none"/>${[-24, -8, 8, 24].map((x) => `<circle cx="${x}" cy="${-470 + Math.abs(x) * 0.3}" r="3.5" fill="#c9b9a0"/>`).join("")}
        <path d="M-56,-470L50,-320" stroke="#7a3f8a" stroke-width="26"/><path d="M-56,-470L50,-320" stroke="#9a5aaa" stroke-width="8" opacity=".6"/><path d="M-30,-440Q0,-400 4,-380" stroke="${INK}" stroke-width="2.5" fill="none"/>`,
      hair: `<circle cx="-30" cy="-600" r="26" fill="#b8b0a6" ${OUT}/><path d="M-48,-544Q-52,-610 0,-612Q50,-610 48,-546Q40,-580 0,-584Q-38,-580 -48,-544Z" fill="#b8b0a6" ${OUT}/>
        <path d="M-20,-600q14,-6 30,2M-40,-574q10,-14 26,-18" stroke="#8a8278" stroke-width="4" fill="none"/>`,
      face: `<path d="M-30,-560q8,-3 14,0M14,-560q8,-3 14,0" stroke="#7a5a44" stroke-width="2.5" fill="none"/><path d="M-26,-512q4,4 0,8M30,-512q-4,4 0,8M-34,-540q-4,6 0,12M40,-540q4,6 0,12" stroke="#a87a56" stroke-width="2" fill="none"/>`,
    },
    mhem: { // ตาเหม: the ferryman, งอบ hat, faded indigo shirt, checked cloth (ผ้าขาวม้า) round the waist, grey stubble
      skin: "#b07a52", skinS: "#8f5f3c", top: "#3a4a6a", topS: "#2c3a56", sleeve: "#3a4a6a", sleeveS: "#2c3a56",
      pants: "#2f3438", pantsS: "#22272a", shoe: "#b07a52", belt: "#c8392b",
      torsoExtra: `<rect x="-58" y="-330" width="116" height="36" fill="#c8392b" ${OUT}/>${[-40, -16, 8, 32].map((x) => `<path d="M${x},-330v36" stroke="#f4ecd8" stroke-width="6" opacity=".8"/>`).join("")}<path d="M-56,-312H56" stroke="#f4ecd8" stroke-width="5" opacity=".8"/>
        <path d="M-30,-484L0,-452L30,-484" stroke="#2c3a56" stroke-width="5" fill="none"/>`,
      hair: `<path d="M-46,-560q-5,16 2,30M46,-560q5,16 -2,30" stroke="#8a8278" stroke-width="8" fill="none" stroke-linecap="round"/>
        <path d="M-120,-568Q0,-660 120,-568Q60,-584 0,-586Q-60,-584 -120,-568Z" fill="#c9a86a" ${OUT}/><path d="M-60,-600Q0,-650 60,-600" stroke="#8a6a3a" stroke-width="4" fill="none"/><path d="M-40,-574L-30,-500M40,-574L30,-500" stroke="#5a4a32" stroke-width="2.5"/>`,
      face: `<path d="M-38,-532Q-30,-494 4,-492Q38,-494 42,-532Q32,-510 4,-508Q-24,-510 -38,-532Z" fill="#8a8278" opacity=".45"/><path d="M-30,-560q8,-3 14,0M14,-560q8,-3 14,0" stroke="#5a4a32" stroke-width="3" fill="none"/>`,
    },
  });
  // แพรว / โต้ง soaked: hair flat, clothes darker
  Rig.CAST.tongWet = { ...Rig.CAST.tong, top: "#9a2e27", topS: "#7d241e", sleeve: "#9a2e27", sleeveS: "#7d241e", pants: "#7d6e50", pantsS: "#61553e" };

  Object.assign(Sets, { riverNight, pierDeck, pierPOV, pierSection, porch, bedroom, underRiver, ankleMarks, legendPhrai, reflections, phraiLegend, krathongCard, pierSign, cprTop, floodRoad, hullHands });
  window.Phrai = { GBL, GBL2, GRIM, GVEIN, GEYE, gEye, krathong, kglow, krefl, paleHand, drownedFace, ferry, gallon, bottle, bamboo, life, CAST_COL };
})();
