// Sets and props for "วันที่ 100": a rural primary school turned camp, a hundred days after the plague ("ห่าลง").
// The yard with its concrete fence, sliding iron gate, wooden classroom block, flagpole and the tall water tank;
// the classroom with the big green blackboard; the abandoned fresh market; the dirt road through the paddies;
// close-ups of a bulging can, the gate bolt, the tank gauge and the old radio; น้องปั้น's crayon drawing;
// a top-down map of the compound. Same layer contract as sets.js / zom.js (sky far mid set act fg + glow/light).
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);
  const G = 1500;

  Sets.DEFS += `
    <linearGradient id="fDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb6dc"/><stop offset=".7" stop-color="#d9e6ea"/><stop offset="1" stop-color="#f1e9d6"/></linearGradient>
    <linearGradient id="fNoon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fc3ea"/><stop offset=".75" stop-color="#eef2ea"/><stop offset="1" stop-color="#fff3d6"/></linearGradient>
    <linearGradient id="fDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2f52"/><stop offset=".5" stop-color="#b9566a"/><stop offset=".85" stop-color="#f2a05a"/><stop offset="1" stop-color="#ffd37a"/></linearGradient>
    <linearGradient id="fNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070f"/><stop offset="1" stop-color="#162035"/></linearGradient>
    <linearGradient id="fMorn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9d4e6"/><stop offset=".8" stop-color="#f6e7cf"/><stop offset="1" stop-color="#ffdca8"/></linearGradient>
    <linearGradient id="fPaddy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fae5a"/><stop offset="1" stop-color="#6d8f3e"/></linearGradient>
    <linearGradient id="fPaddyD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4a3e"/><stop offset="1" stop-color="#2f3328"/></linearGradient>
    <linearGradient id="fDirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8a06a"/><stop offset="1" stop-color="#a77f4e"/></linearGradient>
    <linearGradient id="fConc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9d4c8"/><stop offset="1" stop-color="#b3ada0"/></linearGradient>
    <linearGradient id="fTin" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8d9299"/><stop offset=".5" stop-color="#b9bec4"/><stop offset="1" stop-color="#7f858c"/></linearGradient>
    <linearGradient id="fBoard" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f5a46"/><stop offset="1" stop-color="#1f3f31"/></linearGradient>
    <linearGradient id="fCan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8d9299"/><stop offset=".35" stop-color="#e3e6e8"/><stop offset=".7" stop-color="#aeb3b8"/><stop offset="1" stop-color="#6f757b"/></linearGradient>
    <radialGradient id="fSun"><stop offset="0" stop-color="#fff2c0" stop-opacity=".95"/><stop offset=".35" stop-color="#ffd37a" stop-opacity=".5"/><stop offset="1" stop-color="#ffb060" stop-opacity="0"/></radialGradient>
    <radialGradient id="fLamp"><stop offset="0" stop-color="#ffd58a" stop-opacity=".3"/><stop offset=".4" stop-color="#ffb35c" stop-opacity=".07"/><stop offset="1" stop-color="#ffb35c" stop-opacity="0"/></radialGradient>
    <radialGradient id="fDial"><stop offset="0" stop-color="#ffd27a" stop-opacity=".9"/><stop offset=".5" stop-color="#ff9a3c" stop-opacity=".3"/><stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/></radialGradient>
    <radialGradient id="fRing"><stop offset=".6" stop-color="#ff5a3a" stop-opacity="0"/><stop offset=".9" stop-color="#ff5a3a" stop-opacity=".5"/><stop offset="1" stop-color="#ff5a3a" stop-opacity="0"/></radialGradient>
    <pattern id="fPaper" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="#f3ecd9"/><path d="M0,59.5H60" stroke="#cdbfa3" stroke-width="1.5"/></pattern>
    <pattern id="fGrid" width="48" height="48" patternUnits="userSpaceOnUse"><rect width="48" height="48" fill="#f7f1e2"/><path d="M0,47.5H48M47.5,0V48" stroke="#d8cbb2" stroke-width="1.4"/></pattern>
    <pattern id="fMesh" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M0,13L13,0L26,13L13,26Z" fill="none" stroke="#9aa0a6" stroke-width="2.2"/></pattern>
    <linearGradient id="fMapWat" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9cc6c6"/><stop offset=".55" stop-color="#6a9a9c"/><stop offset="1" stop-color="#557f84"/></linearGradient>
    <pattern id="fMapRice" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(-6)"><path d="M0,11H22" stroke="#1d2a10" stroke-opacity=".1" stroke-width="4"/></pattern>
    <pattern id="fMapTin" width="18" height="18" patternUnits="userSpaceOnUse"><rect width="18" height="18" fill="#9aa2a5"/><rect width="8" height="18" fill="#bcc3c5"/></pattern>
    <radialGradient id="fMapCS"><stop offset="0" stop-color="#0d1208" stop-opacity=".26"/><stop offset=".6" stop-color="#0d1208" stop-opacity=".12"/><stop offset="1" stop-color="#0d1208" stop-opacity="0"/></radialGradient>
    <radialGradient id="fMapSun" cx=".2" cy=".1" r="1.05"><stop offset="0" stop-color="#ffe9b8" stop-opacity=".3"/><stop offset=".4" stop-color="#ffd590" stop-opacity=".06"/><stop offset=".75" stop-color="#0b0e08" stop-opacity=".12"/><stop offset="1" stop-color="#0b0e08" stop-opacity=".5"/></radialGradient>
    <radialGradient id="fPinGloss" cx=".36" cy=".3" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></radialGradient>
    <filter id="fChalk" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.2"/></filter>
    <filter id="fCrayon" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".6" numOctaves="2" seed="9" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="4"/></filter>`;

  const SKY = { day: "fDay", noon: "fNoon", dusk: "fDusk", night: "fNight", morning: "fMorn" };
  const sky = (L, time) => put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#${SKY[time] || "fDay"})"/>`);
  const sunMoon = (L, time, x = 820, y = 420) => {
    if (time === "night") put(L.sky, `<circle cx="${x}" cy="${y - 80}" r="150" fill="url(#moonhalo)"/><circle cx="${x}" cy="${y - 80}" r="46" fill="#e9eef5"/><circle cx="${x - 16}" cy="${y - 92}" r="9" fill="#cfd6e0"/><circle cx="${x + 14}" cy="${y - 66}" r="6" fill="#cfd6e0"/>`);
    else if (time === "dusk") put(L.sky, `<circle cx="${x}" cy="${y + 520}" r="420" fill="url(#fSun)"/><circle cx="${x}" cy="${y + 520}" r="120" fill="#ffd37a"/>`);
    else put(L.sky, `<circle cx="${x}" cy="${y - 200}" r="380" fill="url(#fSun)"/><circle cx="${x}" cy="${y - 200}" r="210" fill="url(#dSunBloom)"/><circle cx="${x}" cy="${y - 200}" r="58" fill="#fffbe8"/>`);
  };
  // ---------------- far ground v2 (user 28 Oct: "วิวหลัง … ดีแล้วรึยัง"): the view past the fence in layers, each paler and bluer with
  // distance — two mountain ranges (the radio mast on the near ridge, planted for the finale), a soft haze, a tree line of rain
  // trees, sugar palms and bamboo with the village roofs and a temple's tiered roof poking through, then the paddies: strips of
  // different greens, flooded ones holding the sky, dykes, a dirt track, lone trees, power poles with sagging wires, birds ----------------
  function paddies(r, time, y0, o = {}) {
    const night = time === "night", dusk = time === "dusk", noon = time === "noon", morn = time === "morning";
    const P = night ? { m1: "#1c2840", m2: "#16213a", hz: "#2a3a5a", t1: "#121a2a", t2: "#0e1522", roof: "#1a2232", f: ["#1b2432", "#18202c", "#1e2836"], w: "#2a3c5a", dyke: "#141a22", pole: "#2a3040", lit: "#3a4a6a" }
      : dusk ? { m1: "#8a6a8a", m2: "#6c4f72", hz: "#e8a080", t1: "#4f3a56", t2: "#3f2e46", roof: "#5a3a3a", f: ["#6a5a46", "#5e5240", "#74644c"], w: "#e8a070", dyke: "#4a3a2c", pole: "#3a2a30", lit: "#ffb070" }
      : morn ? { m1: "#a9bccb", m2: "#93a9b9", hz: "#f2e2d4", t1: "#6f8a74", t2: "#5a7660", roof: "#9a6a5a", f: ["#8aa65a", "#7f9c50", "#96b064"], w: "#cfe0ea", dyke: "#6a7a44", pole: "#6b5a44", lit: "#fff2d8" }
      : { m1: noon ? "#b8c8d2" : "#a3b8c8", m2: noon ? "#a2b6c2" : "#8aa3b4", hz: noon ? "#f4f0e2" : "#e6ece8", t1: noon ? "#7f9a80" : "#6c8c70", t2: noon ? "#6a8a66" : "#567a52", roof: "#a5604a", f: ["#8fae5a", "#82a24e", "#9cb866"], w: "#c9dfe8", dyke: "#6a7d3c", pole: "#6b5a44", lit: "#fff6dc" };
    const ridge = (yBase, amp, step, seed) => { const q = mk(seed); let d = `M-1500,${yBase + 200}L-1500,${yBase}`; for (let x = -1500; x <= 2700; x += step) d += `L${x},${f1(yBase - amp * (0.4 + 0.6 * Math.abs(Math.sin(x / 520 + seed))) - q() * amp * 0.35)}`; return d + `L2700,${yBase + 200}Z`; };
    let s = `<rect x="-1500" y="${y0 - 10}" width="4200" height="1500" fill="${P.f[0]}"/>`;
    // two ranges and the haze between them; ridge light on the sun side
    s += `<path d="${ridge(y0 - 120, 190, 70, 3)}" fill="${P.m1}"/><path d="${ridge(y0 - 50, 130, 60, 7)}" fill="${P.m2}"/>`;
    s += `<path d="${ridge(y0 - 50, 130, 60, 7).replace(/Z$/, "")}" fill="none" stroke="${P.lit}" stroke-opacity="${night ? 0.15 : 0.25}" stroke-width="3" transform="translate(-3,-2)"/>`;
    s += `<rect x="-1500" y="${y0 - 120}" width="4200" height="140" fill="${P.hz}" opacity="${night ? 0.18 : 0.35}"/>`;
    // the radio mast on the near ridge (planted for the finale)
    s += `<path d="M1150,${y0 - 150}V${y0 - 330}M1138,${y0 - 310}h24M1142,${y0 - 260}h16M1146,${y0 - 210}h8M1150,${y0 - 330}L1128,${y0 - 150}M1150,${y0 - 330}L1172,${y0 - 150}" stroke="${night ? "#3a4660" : "#5c6f82"}" stroke-width="3"/><circle class="beacon" cx="1150" cy="${y0 - 334}" r="5" fill="#ff3b30" opacity=".8"/>`;
    // the tree line: a lumpy canopy band, rain trees, sugar palms, bamboo, the village roofs and a temple roof
    let canopy = `M-1500,${y0 + 20}`; for (let x = -1500; x <= 2700; x += 40) canopy += `Q${x + 20},${f1(y0 - 34 - r() * 26)} ${x + 40},${f1(y0 - 6 - r() * 14)}`; canopy += `L2700,${y0 + 30}L-1500,${y0 + 30}Z`;
    s += `<path d="${canopy}" fill="${P.t1}"/>`;
    for (let k = 0; k < 16; k++) { const x = -1400 + k * 270 + r() * 120, h = 60 + r() * 50; s += `<path d="M${f1(x)},${y0}v-${f1(h * 0.6)}" stroke="${P.t2}" stroke-width="6"/><ellipse cx="${f1(x)}" cy="${f1(y0 - h * 0.75)}" rx="${f1(h * 0.75)}" ry="${f1(h * 0.42)}" fill="${P.t2}"/><ellipse cx="${f1(x - h * 0.2)}" cy="${f1(y0 - h * 0.85)}" rx="${f1(h * 0.4)}" ry="${f1(h * 0.24)}" fill="${P.t1}" opacity=".7"/>`; }
    for (let k = 0; k < 12; k++) { const x = -1300 + k * 340 + r() * 160, h = 120 + r() * 60;   // sugar palms
      s += `<path d="M${f1(x)},${y0 + 4}Q${f1(x + 4)},${f1(y0 - h * 0.5)} ${f1(x + 2)},${f1(y0 - h)}" stroke="${P.t2}" stroke-width="5" fill="none"/>${Array.from({ length: 7 }, (_, j) => { const a = -Math.PI * (0.05 + j * 0.15); return `<path d="M${f1(x + 2)},${f1(y0 - h)}q${f1(Math.cos(a) * 14)},${f1(Math.sin(a) * 14 - 6)} ${f1(Math.cos(a) * 30)},${f1(Math.sin(a) * 26 + 6)}" stroke="${P.t2}" stroke-width="5" fill="none" stroke-linecap="round"/>`; }).join("")}`; }
    for (let k = 0; k < 7; k++) { const x = -1200 + k * 560 + r() * 200;   // bamboo clumps
      s += Array.from({ length: 6 }, (_, j) => `<path d="M${f1(x + j * 8)},${y0}q${f1(-30 + j * 12)},-60 ${f1(-50 + j * 22)},-${f1(90 + (j % 3) * 18)}" stroke="${P.t2}" stroke-width="4" fill="none"/>`).join(""); }
    const roof = (x, w, h, col) => `<path d="M${x - w / 2},${y0 - 6}V${y0 - h * 0.5}L${x},${y0 - h}L${x + w / 2},${y0 - h * 0.5}V${y0 - 6}Z" fill="${col}"/><path d="M${x - w / 2 - 6},${y0 - h * 0.5}L${x},${y0 - h - 4}L${x + w / 2 + 6},${y0 - h * 0.5}" stroke="${P.t2}" stroke-width="3" fill="none"/>`;
    [[-1050, 70, 46], [-920, 54, 38], [-300, 64, 44], [520, 58, 40], [1720, 72, 48], [1860, 52, 36], [2200, 60, 42]].forEach(([x, w, h]) => (s += roof(x, w, h, P.roof)));
    // the temple roof: three stacked gables with chofa hooks at the ends, a small spire behind
    s += `<g transform="translate(-60,${y0 - 8})" fill="${night ? "#2a2a38" : dusk ? "#6a3a32" : "#b0583a"}">${[[0, 0, 150, 60], [0, -40, 112, 54], [0, -78, 74, 48]].map(([x, y, w, h]) => `<path d="M${-w / 2},${y}L${-w / 2 + 16},${y - h * 0.3}L0,${y - h}L${w / 2 - 16},${y - h * 0.3}L${w / 2},${y}Z"/><path d="M${-w / 2 + 2},${y - 2}q-8,-14 -2,-26M${w / 2 - 2},${y - 2}q8,-14 2,-26" stroke="${night ? "#3a3a48" : "#e0b04a"}" stroke-width="4" fill="none"/>`).join("")}<path d="M60,-60L70,-150L80,-60Z" fill="${night ? "#2a2a38" : "#d9cfb8"}"/></g>`;
    // the paddies: strips that widen toward us, flooded ones catch the sky, dykes between, a dirt track, lone trees
    let y = y0 + 22;
    for (let k = 0; k < 9; k++) { const h = 8 + k * k * 3.2, wet = k % 3 === 1;
      s += `<rect x="-1500" y="${f1(y)}" width="4200" height="${f1(h)}" fill="${wet ? P.w : P.f[k % 3]}" opacity="${wet ? 0.85 : 1}"/>`;
      if (wet && !night) s += `<path d="M${-1400 + r() * 400},${f1(y + h * 0.4)}h${f1(600 + r() * 600)}M${400 + r() * 600},${f1(y + h * 0.6)}h${f1(400 + r() * 500)}" stroke="#fff" stroke-opacity=".3" stroke-width="${f1(Math.max(2, h * 0.12))}"/>`;
      s += `<path d="M-1500,${f1(y + h)}H2700" stroke="${P.dyke}" stroke-width="${f1(2 + k * 0.9)}" opacity=".75"/>`;
      y += h;
    }
    s += `<path d="M-200,${y0 + 24}C200,${y0 + 80} 600,${y0 + 160} 1400,${y0 + 380}" stroke="${night ? "#2a2a2a" : dusk ? "#8a6a4a" : "#c9b082"}" stroke-width="22" fill="none" opacity=".75"/>`;
    for (let k = 0; k < 6; k++) { const x = -900 + k * 620 + r() * 200, yy = y0 + 60 + r() * 120, h = 50 + r() * 40; s += `<path d="M${f1(x)},${f1(yy)}v-${f1(h * 0.5)}" stroke="${night ? "#1a2030" : "#5a4a34"}" stroke-width="6"/><ellipse cx="${f1(x)}" cy="${f1(yy - h * 0.7)}" rx="${f1(h * 0.6)}" ry="${f1(h * 0.42)}" fill="${night ? "#1c2636" : dusk ? "#4a4452" : "#4f7a44"}"/><ellipse cx="${f1(x - h * 0.2)}" cy="${f1(yy - h * 0.82)}" rx="${f1(h * 0.3)}" ry="${f1(h * 0.2)}" fill="${night ? "#24304a" : dusk ? "#6a5462" : "#6a9a54"}"/>`; }
    // power poles along the track, wires sagging, one leaning
    for (let k = 0; k < 5; k++) { const x = -800 + k * 640 + (k === 2 ? 60 : 0); s += `<g transform="translate(${x},${y0 + 20}) rotate(${k === 2 ? -7 : 0})"><path d="M0,0V-250M-40,-224H40M-30,-196H30" stroke="${P.pole}" stroke-width="7"/><circle cx="-36" cy="-230" r="4" fill="${P.pole}"/><circle cx="36" cy="-230" r="4" fill="${P.pole}"/></g>`; }
    s += [0, 1].map((j) => `<path d="M-840,${y0 - 210 + j * 28}Q-520,${y0 - 150 + j * 28} -160,${y0 - 210 + j * 28}T480,${y0 - 210 + j * 28}T1120,${y0 - 210 + j * 28}T1760,${y0 - 210 + j * 28}" stroke="${P.pole}" stroke-width="2.2" fill="none"/>`).join("");
    // birds over the fields (flife .bird)
    if (!night) s += [[-300, y0 - 420], [-240, y0 - 450], [-190, y0 - 410], [900, y0 - 520], [960, y0 - 545]].map(([x, yy], k) => `<path class="bird" d="M${x - 12},${yy}q6,-8 12,0q6,-8 12,0" stroke="${dusk ? "#2a1a24" : "#3a3f45"}" stroke-width="3" fill="none" stroke-linecap="round" data-k="${k}"/>`).join("");
    return s;
  }

  // ---------------- the school yard (seen from inside): fence across the back with the sliding gate, classroom block left, water tank right ----------------
  // ids: #id-gate (slides open along x), #id-bolt, #id-tank, #id-level (float in the gauge tube), #id-flag, #id-lamp (night lantern)
  function schoolYard(L, o = {}) {
    const id = o.id || "sy", t = o.time || "day", night = t === "night", r = mk(o.seed || 41), FY = 1180; // fence foot line
    sky(L, t); sunMoon(L, t, o.sunX ?? 760, 420);
    put(L.far, paddies(r, t, 1040));
    // fence: concrete plinth, square posts, iron bars between; a sliding gate of vertical bars in the middle-right
    let s = `<rect x="-1200" y="${FY}" width="3500" height="60" fill="url(#fConc)" ${OUT}/>`;
    for (let x = -1320; x < 2300; x += 220) {
      if (x > 420 && x < 900) continue; // the gate opening
      const brk = o.breakAt === x;   // this section can fall inward (#id-fseg): rotated about its foot on the yard side
      if (brk) s += `<g id="${id}-fseg" transform="rotate(${o.fallen ? -82 : 0} ${x + 230} ${FY + 4})">`;
      s += `<rect x="${x}" y="${FY - 330}" width="40" height="340" fill="#cfc9bb" ${OUT}/><rect x="${x + 36}" y="${FY - 316}" width="186" height="30" fill="#5b6066" ${OUT}/><rect x="${x + 36}" y="${FY - 120}" width="186" height="26" fill="#5b6066" ${OUT}/>`;
      for (let b = 0; b < 6; b++) s += `<rect x="${x + 50 + b * 30}" y="${FY - 300}" width="12" height="190" fill="#3f454b"/>`;
      if (brk) s += `<path d="M${x + 60},${FY - 310}l-10,30l14,20M${x + 150},${FY - 120}l12,-24" stroke="#2e2a26" stroke-width="3" fill="none"/></g>`;
      if (brk && o.fallen) s += `<path d="M${x + 180},${FY + 30}q60,-20 120,10M${x + 200},${FY + 50}q50,-10 90,20" stroke="#5a4630" stroke-width="10" fill="none" stroke-linecap="round"/>`;
    }
    // the short run between the gate's right post (x 940) and the next post (x 1100)
    s += `<rect x="936" y="${FY - 316}" width="168" height="30" fill="#5b6066" ${OUT}/><rect x="936" y="${FY - 120}" width="168" height="26" fill="#5b6066" ${OUT}/>`;
    for (let b = 0; b < 5; b++) s += `<rect x="${956 + b * 30}" y="${FY - 300}" width="12" height="190" fill="#3f454b"/>`;
    s += `<rect x="400" y="${FY - 400}" width="44" height="410" fill="#cfc9bb" ${OUT}/><rect x="896" y="${FY - 400}" width="44" height="410" fill="#cfc9bb" ${OUT}/><rect x="400" y="${FY - 420}" width="540" height="30" fill="#c8302a" ${OUT}/>`;
    s += `<text x="670" y="${FY - 435}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#f4ecd8" stroke="${INK}" stroke-width="5" paint-order="stroke">โรงเรียนบ้านหนองน้ำใส</text>`;
    // the gate: a frame of iron bars on a rail, slides to the right (+x) to open
    const gx = 444 + (o.gate || 0) * 440;
    s += `<g id="${id}-gate" transform="translate(${gx},0)"><rect x="0" y="${FY - 380}" width="452" height="380" fill="none" stroke="#3a3f45" stroke-width="18"/>`;
    for (let b = 0; b < 14; b++) s += `<rect x="${12 + b * 32}" y="${FY - 372}" width="10" height="364" fill="#3f454b"/>`;
    s += `<rect x="0" y="${FY - 230}" width="452" height="18" fill="#3a3f45"/><g id="${id}-bolt"><rect x="-70" y="${FY - 210}" width="130" height="22" rx="8" fill="#8d9299" ${OUT}/><rect x="-78" y="${FY - 222}" width="30" height="46" rx="6" fill="#5b6066" ${OUT}/></g></g>`;
    s += `<rect x="400" y="${FY - 8}" width="540" height="12" fill="#3a3f45"/>`;
    // classroom block (left, behind a gravel apron): raised wooden building, tin roof, long veranda, shuttered windows
    // the classroom block (left, behind a gravel apron): a Thai village school on concrete stumps — a long veranda with square posts
    // and a slatted rail, cream plank walls with green louvred windows, a double door up three steps, a deep hipped roof of red tiles
    // with a gutter and a fretwork vent, the school's name on the gable
    const tiles = Array.from({ length: 7 }, (_, k) => { const y = -470 - k * 19, x0 = -90 + k * 30, x1 = 990 - k * 30; return `<path d="M${x0},${y}H${x1}" stroke="#8a3a26" stroke-width="3"/>${Array.from({ length: Math.floor((x1 - x0) / 34) }, (_, j) => `<path d="M${x0 + 17 + j * 34},${y}v-17" stroke="#8a3a26" stroke-width="1.6" opacity=".7"/>`).join("")}`; }).join("");
    const louvre = (x) => `<rect x="${x}" y="-420" width="120" height="170" fill="#2f5a4a" ${OUT}/>${Array.from({ length: 9 }, (_, j) => `<path d="M${x + 6},${-410 + j * 18}h108" stroke="#6f9a80" stroke-width="7"/><path d="M${x + 6},${-406 + j * 18}h108" stroke="#1d3a30" stroke-width="2"/>`).join("")}<path d="M${x + 60},-420v170" stroke="#2f5a4a" stroke-width="6"/><rect x="${x - 8}" y="-250" width="136" height="12" fill="#d8c48a" ${OUT}/>`;
    s += `<g id="${id}-bldg" transform="translate(-620,${FY - 20})">
      ${[0, 180, 360, 540, 720, 880].map((x) => `<rect x="${x - 14}" y="-104" width="28" height="104" fill="#a9a293" ${OUT}/><rect x="${x + 4}" y="-104" width="10" height="104" fill="#000" opacity=".18"/>`).join("")}
      <rect x="-40" y="-470" width="940" height="350" fill="#e9d9a6" ${OUT}/>
      ${louvre(40)}${louvre(240)}${louvre(560)}${louvre(760)}
      <rect x="390" y="-430" width="130" height="310" fill="#2f5a4a" ${OUT}/><path d="M455,-430v310" stroke="#1d3a30" stroke-width="4"/><rect x="402" y="-414" width="44" height="120" fill="#3c6e5a"/><rect x="464" y="-414" width="44" height="120" fill="#3c6e5a"/><rect x="402" y="-276" width="44" height="140" fill="#3c6e5a"/><rect x="464" y="-276" width="44" height="140" fill="#3c6e5a"/><circle cx="445" cy="-270" r="5" fill="#d8c48a"/><circle cx="465" cy="-270" r="5" fill="#d8c48a"/>
      <rect x="-60" y="-124" width="980" height="24" fill="#7a4a2e" ${OUT}/>
      <path d="M380,-100h150v34h20v34h20V0H360V-32h-20v-32h20Z" fill="#c9c3b6" ${OUT}/><path d="M360,-64h190M340,-32h230" stroke="#9a948a" stroke-width="3"/>
      ${[-20, 220, 690, 900].map((x) => `<rect x="${x - 16}" y="-470" width="32" height="350" fill="#8a5a3a" ${OUT}/><rect x="${x + 6}" y="-470" width="10" height="350" fill="#000" opacity=".2"/><rect x="${x - 14}" y="-470" width="4" height="350" fill="#fff" opacity=".18"/>`).join("")}
      ${[[-4, 204], [236, 366], [544, 674], [706, 884]].map(([x0, x1]) => `<rect x="${x0}" y="-210" width="${x1 - x0}" height="14" fill="#8a5a3a" ${OUT}/>${Array.from({ length: Math.floor((x1 - x0) / 22) }, (_, j) => `<rect x="${x0 + 8 + j * 22}" y="-196" width="9" height="72" fill="#9a6a44" stroke="${INK}" stroke-width="1.5"/>`).join("")}`).join("")}
      <path d="M366,-210v90M544,-210v90" stroke="#8a5a3a" stroke-width="12"/><path d="M366,-196L346,-40M544,-196L568,-40" stroke="#6b4a2e" stroke-width="7" stroke-linecap="round"/>
      <path d="M-100,-470L120,-600H780L1000,-470Z" fill="#c4553a" ${OUT}/>${tiles}<path d="M-100,-470L120,-600H780L1000,-470" fill="none" stroke="${INK}" stroke-width="4"/>
      <path d="M120,-600H780" stroke="#e88a63" stroke-width="6"/><rect x="-104" y="-474" width="1108" height="16" fill="#6b3a26" ${OUT}/><rect x="-104" y="-462" width="1108" height="8" fill="#9aa0a6" ${OUT}/>
      <path d="M340,-600L450,-680L560,-600Z" fill="#e9d9a6" ${OUT}/>${Array.from({ length: 5 }, (_, j) => `<path d="M${380 + j * 18},-604l${10 - j * 2},${-20 - j * 3}" stroke="#8a5a3a" stroke-width="3"/>`).join("")}<path d="M330,-598L450,-688L570,-598" stroke="#c4553a" stroke-width="10" fill="none" stroke-linejoin="round"/><path d="M330,-598q-14,-6 -12,-22M570,-598q14,-6 12,-22" stroke="#e0b04a" stroke-width="5" fill="none"/>
      <rect x="290" y="-560" width="320" height="52" rx="8" fill="#1f3f31" ${OUT}/><text x="450" y="-524" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#f4ecd8">โรงเรียนบ้านหนองน้ำใส</text></g>`;
    // flagpole with a faded, torn flag
    s += `<g id="${id}-flag" transform="translate(300,${FY + 60})"><rect x="-70" y="-30" width="140" height="30" fill="url(#fConc)" ${OUT}/><path d="M0,-30V-700" stroke="#9aa0a6" stroke-width="10"/><circle cy="-706" r="9" fill="#c9a55a" ${OUT}/>
      <path id="${id}-flagc" d="M6,-690h150l-10,30l8,30l-12,30h-136z" fill="#c8392b"/><path d="M6,-660h146v20h-146z" fill="#f4ecd8"/><path d="M6,-640h140v-14h-140z" fill="#2f4a8a"/></g>`;
    // water tank: a concrete tank on four legs with a ladder, a pipe down to a tap, and a clear gauge tube with marks (#id-level = the float)
    s += `<g id="${id}-tank" transform="translate(1260,${FY + 40})"><path d="M-130,0V-520M130,0V-520M-70,0V-520M70,0V-520" stroke="#8a857a" stroke-width="18"/><path d="M-130,-120L130,-260M130,-120L-130,-260M-130,-380L130,-500M130,-380L-130,-500" stroke="#8a857a" stroke-width="7"/>
      <rect x="-190" y="-540" width="380" height="40" fill="#9aa0a6" ${OUT}/><rect x="-170" y="-840" width="340" height="300" rx="20" fill="url(#fConc)" ${OUT}/><path d="M-170,-760H170M-170,-620H170" stroke="#9f9a8e" stroke-width="5"/>
      <ellipse cx="0" cy="-840" rx="170" ry="26" fill="#bdb7aa" ${OUT}/><rect x="-60" y="-868" width="120" height="30" rx="8" fill="#5b6066" ${OUT}/>
      <path d="M150,-860V-600M150,-860h44" stroke="#8a857a" stroke-width="10"/><rect x="170" y="-470" width="26" height="470" fill="#8a857a"/>${Array.from({ length: 9 }, (_, k) => `<path d="M146,${-500 + k * 56}h74" stroke="#8a857a" stroke-width="8"/>`).join("")}
      <rect x="-230" y="-820" width="26" height="270" rx="12" fill="#dfe9ee" ${OUT}/>${Array.from({ length: 6 }, (_, k) => `<path d="M-236,${-800 + k * 48}h-18" stroke="${INK}" stroke-width="3"/>`).join("")}
      <rect id="${id}-level" x="-226" y="${-820 + 270 * (1 - (o.level ?? 0.72))}" width="18" height="${270 * (o.level ?? 0.72)}" fill="#6fb3d6"/>
      <path d="M-100,-540V-40h-60" stroke="#8a857a" stroke-width="10" fill="none"/><rect x="-190" y="-60" width="40" height="30" rx="6" fill="#c9a55a" ${OUT}/><rect x="-250" y="0" width="160" height="14" fill="#8a857a"/><circle cx="-180" cy="-20" r="10" fill="#6fb3d6" opacity=".7"/></g>`;
    put(L.set, s);
    // the yard: packed dirt with grass, puddles and a drain, closer to us
    let g = `<rect x="-1200" y="${FY + 60}" width="3500" height="1300" fill="url(#fDirt)"/>`;
    for (let k = 0; k < 40; k++) { const x = -1100 + r() * 3400, y = FY + 90 + r() * 900; g += `<path d="M${f1(x)},${f1(y)}q6,-26 12,0q6,-22 12,0q6,-18 12,0" stroke="#6f8f3e" stroke-width="4" fill="none"/>`; }
    g += `<ellipse cx="500" cy="${FY + 400}" rx="220" ry="40" fill="#8f6f45" opacity=".35"/><ellipse cx="1500" cy="${FY + 600}" rx="300" ry="50" fill="#8f6f45" opacity=".35"/>`;
    put(L.set, g);
    if (o.hill) put(L.far, `<g id="${id}-hill"><path d="M1000,780Q1400,520 1800,620T2500,720V1100H1000Z" fill="${night ? "#121816" : "#5f7a4a"}"/><circle id="${id}-blinkg" cx="1640" cy="602" r="44" fill="url(#fLamp)" opacity="0"/><circle id="${id}-blink" cx="1640" cy="602" r="8" fill="#fff8d0" opacity="0"/></g>`);
    if (o.genX !== undefined) put(L.set, Sets.props.generator(`${id}-gen`, o.genX, FY + 320, 0.75, !!o.genOn));
    if (night || o.lamp) put(L.glow, `<g id="${id}-lamp"><circle cx="${o.lampX ?? -200}" cy="${FY - 260}" r="420" fill="url(#fLamp)" opacity=".7"/></g>`);
    if (night) put(L.glow, Array.from({ length: 26 }, (_, k) => `<circle class="mote" cx="${f1(-400 + r() * 1900)}" cy="${f1(700 + r() * 900)}" r="${f1(3 + r() * 4)}" fill="#d8f0a0" opacity="${(0.2 + r() * 0.5).toFixed(2)}"/>`).join(""));
    if (t === "noon") put(L.glow, `<rect x="-1200" y="900" width="3500" height="400" fill="url(#zHaze)" opacity=".8"/>`);
    if (o.dress !== false && window.Dress) yardDress(L, id, o, FY, t);
  }

  // ---------------- set dressing for the school yard (user 28 Oct: "ฉากมันยังเฉยๆ … เก็บรายละเอียดหน่อย") ----------------
  // weathered fence (capped posts, shaded faces, rust runs, moss, razor wire, a tin patch, can alarms, a rule board),
  // a lived-in camp (tarp lean-to, cold fire ring, chairs, firewood, a vegetable bed, jerry cans, tyres, the water jar, laundry
  // under the eaves), a textured yard (dirt grain, tyre tracks, the worn path from the gate, pebbles, leaves, weeds, a puddle)
  // and the fence's own shadow striping the yard when the sun is up. o.dress === false skips all of it.
  function yardDress(L, id, o, FY, t) {
    const D = Dress, night = t === "night", r = mk((o.seed || 41) + 101), sunX = o.sunX ?? 760;
    const sunLen = { noon: 70, day: 230, morning: 330, dusk: 430 }[t] || 0;
    const posts = []; for (let x = -1320; x < 2300; x += 220) if (!(x > 420 && x < 900) && o.breakAt !== x) posts.push(x);
    // the ground: grain, damp shade along the wall foot, the worn path from the gate, tyre tracks, a puddle, litter
    let g = `<rect x="-1200" y="${FY + 60}" width="3500" height="1300" fill="url(#dDirt)" opacity="${night ? 0.6 : 1}"/>`;
    g += `<rect x="-1200" y="${FY + 60}" width="3500" height="90" fill="url(#dAO)" opacity=".8"/>`;
    g += `<path d="M560,${FY + 60}C600,${FY + 260} 420,${FY + 420} 520,${FY + 900}L940,${FY + 900}C860,${FY + 420} 980,${FY + 240} 880,${FY + 60}Z" fill="#e0c08a" opacity="${night ? 0.08 : 0.22}"/>`;
    g += D.tracks(700, FY + 70, 760, FY + 420, 380, FY + 1000, 120, night ? 0.1 : 0.16);
    if (sunLen) { // the fence's shadow, thrown toward us and away from the sun
      const sh = (x, w) => { const dx = (x - sunX) * (sunLen / 900); return `<path d="M${x},${FY + 62}h${w}l${f1(dx * 1.04)},${sunLen}h${-w * 1.2}z"/>`; };
      let p = posts.map((x) => sh(x, 40)).join("");
      posts.forEach((x) => { if (x + 220 > 420 && x < 900) return; for (let b = 0; b < 6; b++) p += sh(x + 50 + b * 30, 12); });
      if (!o.gate) for (let b = 0; b < 14; b++) p += sh(444 + 12 + b * 32, 10);
      g += `<g fill="#2a1a0c" opacity="${t === "noon" ? 0.14 : 0.2}">${p}</g>`;
    }
    g += D.puddle(1180, FY + 470, 150, 30, night) + D.puddle(-260, FY + 620, 110, 22, night);
    g += D.pebbles(-1100, 2200, FY + 80, FY + 760, 70, 61, 7) + D.leaves(-1000, 2100, FY + 80, FY + 700, 46, 67);
    g += D.tufts(-1100, 2200, FY + 120, FY + 800, 34, 71, 34, t === "noon") + D.weeds(-1200, 2300, FY + 64, 73, 54);
    // the near ground, closer to the lens: bigger clumps and stones, rocks, a rusty can on its side, a child's red ball
    g += D.tufts(-1100, 2200, FY + 560, FY + 900, 24, 79, 74, t === "noon") + D.pebbles(-1000, 2100, FY + 540, FY + 900, 20, 83, 15) + D.leaves(-1000, 2100, FY + 520, FY + 900, 26, 87);
    g += [[-150, FY + 760, 1.3], [1250, FY + 820, 1.6], [430, FY + 900, 1.1]].map(([x, y, k]) => D.at(x, y, k, `<ellipse cx="14" cy="4" rx="70" ry="14" fill="#0b0d08" opacity=".28"/><path d="M-62,0C-68,-18 -56,-38 -34,-46L-12,-58L18,-54C42,-46 60,-28 60,0Z" fill="${night ? "#8a8478" : "#a39a88"}" stroke="${INK}" stroke-width="3"/><path d="M-34,-46L-12,-58L18,-54L4,-30Z" fill="#fff" opacity=".22"/><path d="M18,-54C42,-46 60,-28 60,0H14L4,-30Z" fill="#000" opacity=".16"/><path d="M-50,-12l18,-6M24,-20l10,8" stroke="${INK}" stroke-width="2" opacity=".4"/>`)).join("");
    g += D.at(700, FY + 700, 1.2, `<ellipse cx="6" cy="16" rx="40" ry="8" fill="#0b0d08" opacity=".3"/><rect x="-30" y="-8" width="60" height="24" rx="5" fill="url(#fCan)" stroke="${INK}" stroke-width="2.5" transform="rotate(-8)"/><rect x="-14" y="-8" width="24" height="24" fill="#c8392b" opacity=".75" transform="rotate(-8)"/>${D.rust(-24, -6, 18, 20)}<ellipse cx="32" cy="0" rx="5" ry="12" fill="#cfd3d6" stroke="${INK}" stroke-width="2" transform="rotate(-8)"/>`)
      + D.at(1020, FY + 640, 1.1, `<ellipse cx="8" cy="22" rx="34" ry="7" fill="#0b0d08" opacity=".3"/><circle cy="0" r="24" fill="#d8392b" stroke="${INK}" stroke-width="3"/><path d="M-22,-6q22,10 44,0M-12,-20q12,22 6,42" stroke="#f4ecd8" stroke-width="4" fill="none"/><circle cx="-8" cy="-10" r="6" fill="#fff" opacity=".4"/>`);
    put(L.set, g);
    // the fence: caps, shaded right faces, streaks under the caps, rust on the rails, moss at the feet, bar highlights
    let f = "";
    posts.forEach((x, k) => {
      f += `<rect x="${x - 6}" y="${FY - 346}" width="52" height="18" fill="#ddd7c9" stroke="${INK}" stroke-width="3"/><rect x="${x + 26}" y="${FY - 328}" width="14" height="336" fill="#000" opacity=".14"/><rect x="${x + 3}" y="${FY - 328}" width="5" height="330" fill="#fff" opacity=".28"/>`;
      f += `<rect x="${x}" y="${FY - 328}" width="40" height="336" fill="url(#dConc)"/>` + D.streak(x + 4, FY - 328, 18 + (k % 3) * 6, 140 + (k % 4) * 40, 0.9) + D.moss(x - 8, FY + 8, 56, mk(80 + k));
      if (k % 3 === 1) f += D.chip(x + 24, FY - 300, 16) + D.crack(x + 12, FY - 220, 70, 8, 0.4);
      if (x + 220 > 420 && x < 900) return;
      f += `<rect x="${x + 36}" y="${FY - 316}" width="186" height="5" fill="#fff" opacity=".18"/><rect x="${x + 36}" y="${FY - 120}" width="186" height="4" fill="#fff" opacity=".16"/>`;
      f += D.rust(x + 60 + (k % 4) * 30, FY - 290, 22, 90, 0.8) + D.rust(x + 120 - (k % 3) * 20, FY - 96, 20, 60, 0.7);
      for (let b = 0; b < 6; b++) f += `<rect x="${x + 50 + b * 30}" y="${FY - 300}" width="3" height="190" fill="#9aa0a6" opacity=".55"/>`;
    });
    f += D.barbed(-1320, 400, FY - 352, 22) + D.barbed(940, 2300, FY - 352, 22);
    // a sheet of roofing tin wired over a gap (left), planks nailed across another (right)
    f += `<g transform="translate(-856,${FY - 300}) rotate(-2)"><rect width="190" height="230" fill="#9aa2a5" stroke="${INK}" stroke-width="3"/><rect width="190" height="230" fill="url(#dTinV)"/>${D.rust(20, 0, 60, 160)}${D.rust(120, 90, 40, 120)}<path d="M10,14l-14,-10M180,14l14,-10M10,216l-14,10" stroke="#5b6066" stroke-width="3"/></g>`;
    f += `<g transform="translate(1564,${FY - 250})">${[0, 1, 2].map((k) => `<g transform="rotate(${[-6, 3, -2][k]} 90 ${k * 62})"><rect x="-10" y="${k * 62}" width="210" height="40" fill="#a5804f" stroke="${INK}" stroke-width="3"/><rect x="-10" y="${k * 62}" width="210" height="40" fill="url(#dPlankH)"/><circle cx="6" cy="${k * 62 + 20}" r="3.5" fill="#3a3330"/><circle cx="184" cy="${k * 62 + 20}" r="3.5" fill="#3a3330"/></g>`).join("")}</g>`;
    // can alarms strung along the bars, the camp's rule board hung by the gate
    f += D.canAlarm(-1080, -660, FY - 230, 37) + D.canAlarm(-440, 0, FY - 236, 39) + D.canAlarm(980, 1320, FY - 232, 41) + D.canAlarm(1540, 1980, FY - 226, 43);
    f += `<g transform="translate(190,${FY - 300}) rotate(-3)"><path d="M20,0L60,-40M180,0L140,-40" stroke="#c9b48a" stroke-width="2.5"/><rect x="0" y="0" width="200" height="104" fill="#e7dcc0" stroke="${INK}" stroke-width="3"/><rect x="0" y="0" width="200" height="104" fill="url(#dPlankH)"/>
      <text x="100" y="44" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#c8392b">กลับก่อนมืด</text><text x="100" y="84" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="24" fill="#2e2a26">ปิดประตูทุกครั้ง</text></g>`;
    put(L.set, f);
    // the classroom block: board grain on the walls, grime at the foot, dark crawlspace under the raised floor, a boarded window,
    // the bell, laundry under the eaves, plants and slippers on the veranda, a broom; a rain barrel at the downpipe
    const B = document.getElementById(`${id}-bldg`);
    if (B) B.insertAdjacentHTML("beforeend", `<rect x="-40" y="-470" width="940" height="350" fill="url(#dPlankH)" opacity=".8"/><rect x="-40" y="-250" width="940" height="130" fill="url(#dGrime)"/><rect x="-60" y="-100" width="980" height="100" fill="#120d08" opacity=".5"/>
      <rect x="-40" y="-454" width="940" height="30" fill="#000" opacity=".22"/>${D.streak(130, -454, 40, 180, 0.6)}${D.streak(640, -454, 30, 150, 0.5)}${D.rust(150, -600, 60, 110)}${D.rust(640, -580, 50, 90)}
      ${[[-10, 0], [40, 1]].map(([dy, k]) => `<g transform="translate(240,${-400 + dy * 4}) rotate(${k ? -8 : 7} 60 95)"><rect x="-8" y="70" width="136" height="24" fill="#a5804f" stroke="${INK}" stroke-width="3"/><rect x="-8" y="70" width="136" height="24" fill="url(#dPlankH)"/><circle cx="4" cy="82" r="3" fill="#3a3330"/><circle cx="116" cy="82" r="3" fill="#3a3330"/></g>`).join("")}
      <g transform="translate(860,-440)"><path d="M0,-28V-10" stroke="#3a3330" stroke-width="3"/><path d="M-18,22Q-18,-12 0,-12Q18,-12 18,22Z" fill="#c9a24a" stroke="${INK}" stroke-width="3"/><path d="M-10,16q0,-18 6,-22" stroke="#fff" stroke-opacity=".45" stroke-width="3" fill="none"/><circle cy="26" r="4" fill="#5a4a2a"/><path d="M0,26v40" stroke="#c9b48a" stroke-width="2"/></g>
      ${D.laundry(-20, 360, -446, 47)}${D.potPlant(80, -124, 0.7)}${D.potPlant(620, -124, 0.62, 1)}${D.shoes(250, -126, 0.8)}${D.broom(780, -124, 0.62, -10)}${D.bucket(820, -124, 0.6, "#c8392b")}`);
    // camp at the left: tarp lean-to off the classroom, a cold fire ring with its pot, chairs round it, firewood, the jar, a bike;
    // stores at the right by the tank: vegetable bed, tyres, jerry cans, a drum under the downpipe
    let c = D.tarp(-700, FY - 160, -300, FY - 120, 50) + `<path d="M-300,${FY - 120}V${FY + 140}M-700,${FY - 160}V${FY + 130}" stroke="#6b4a2e" stroke-width="10"/>`;
    c += D.firewood(-110, FY + 116, 0.62) + D.campfire(-470, FY + 230, 0.85, false) + D.chair(-640, FY + 236, 0.78, "#2f6fb8") + D.chair(-300, FY + 250, 0.78, "#c8392b") + D.chairStack(-80, FY + 120, 0.6, "#e8e4da", 3);
    c += D.jar(220, FY + 118, 0.62) + D.bike(40, FY + 110, 0.62);
    c += D.garden(1900, FY + 200, 300) + D.tires(1500, FY + 130, 0.66) + D.jerry(1420, FY + 112, 0.62, "#c8392b") + D.jerry(1466, FY + 118, 0.6, "#2f6f3a") + D.drum(1640, FY + 120, 0.7, "#2f5f8a");
    c += D.sandbags(-980, FY + 100, 0.62, 4, 2) + D.banana(-1080, FY + 140, 0.7, 29) + D.bush(2190, FY + 150, 0.8, 31) + D.banana(2300, FY + 120, 0.6, 33);
    put(L.set, c);
    // the village beyond the fence: stilt houses, a coconut palm and bananas (mid layer, so haze sits over them)
    const tone = night ? "night" : t === "dusk" ? "dusk" : "day";
    put(L.mid, D.stiltHouse(1760, FY - 10, 0.72, tone, 61) + D.stiltHouse(-1340, FY - 6, 0.66, tone, 67) + D.banana(1420, FY - 4, 0.62, 71) + D.banana(-980, FY, 0.55, 73)
      + `<g transform="translate(2080,${FY})"><path d="M0,0Q16,-200 -10,-430" stroke="${night ? "#2a2a2e" : "#7a6a4a"}" stroke-width="16" fill="none"/>${Array.from({ length: 8 }, (_, k) => { const a = -Math.PI * (0.05 + k * 0.125); return `<path d="M-10,-430q${(Math.cos(a) * 70).toFixed(0)},${(Math.sin(a) * 70 - 30).toFixed(0)} ${(Math.cos(a) * 150).toFixed(0)},${(Math.sin(a) * 120 + 40).toFixed(0)}" stroke="${night ? "#1c2430" : "#4f7a34"}" stroke-width="12" fill="none" stroke-linecap="round"/>`; }).join("")}<circle cx="-4" cy="-420" r="10" fill="${night ? "#2a2a2e" : "#6b5a2a"}"/></g>`);
    // the tank: water stains down the drum, moss, rust on the legs
    const T = document.getElementById(`${id}-tank`);
    if (T) T.insertAdjacentHTML("beforeend", `<rect x="-170" y="-840" width="340" height="300" fill="url(#dConc)"/>${D.streak(-120, -800, 60, 240, 0.9)}${D.streak(40, -780, 40, 200, 0.7)}${D.moss(-170, -540, 340, mk(9))}${D.rust(-140, -500, 20, 300)}${D.rust(120, -480, 18, 260)}`);
    // dust hanging in the sunlight by day (flife .mote drifts and twinkles them)
    if (!night) put(L.glow, Array.from({ length: 22 }, () => `<circle class="mote" cx="${f1(-300 + r() * 1700)}" cy="${f1(500 + r() * 1100)}" r="${f1(2 + r() * 3.5)}" fill="#fff4d0" opacity="${(0.25 + r() * 0.4).toFixed(2)}"/>`).join(""));
    // the sky by day: a few cumulus banks lit from the sun's side (they drift, flife .cloud)
    if (!night) { const lit = t === "dusk" ? "#f6c29a" : "#f4f7f9", belly = t === "dusk" ? "#c07a86" : "#c3cfd9";
      put(L.sky, [[-620, 330, 0.9], [420, 210, 0.62], [1500, 360, 1.0], [-1100, 150, 0.55]].map(([x, y, k]) => `<g class="cloud" opacity="${t === "dusk" ? 0.5 : 0.7}" transform="translate(${x},${y}) scale(${k})">
        <path d="M-230,40C-250,0 -200,-30 -160,-20C-150,-70 -80,-90 -40,-60C-20,-110 70,-110 90,-56C130,-80 200,-60 196,-10C240,-6 250,40 214,46Z" fill="${belly}"/>
        <path d="M-226,30C-240,-4 -196,-26 -160,-16C-148,-62 -84,-80 -44,-52C-22,-100 66,-100 86,-48C124,-70 190,-54 188,-8C226,-4 232,26 206,30C120,10 -120,14 -226,30Z" fill="${lit}"/>
        <path d="M-130,-30C-100,-56 -60,-60 -40,-40M20,-80C50,-90 80,-76 86,-50" stroke="#fff" stroke-width="6" stroke-opacity=".7" fill="none" stroke-linecap="round"/></g>`).join("")); }
  }

  // ---------------- the classroom: green blackboard on the back wall, teacher's desk, little desks, shutters with light ----------------
  // ids: #id-board (chalk area 160..920 × 330..880), #id-desk, #id-cans (12 cans, #id-bulge = the swollen one), #id-radio, #id-lamp
  function classroom(L, o = {}) {
    const id = o.id || "cr", night = !!o.night, r = mk(o.seed || 17);
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#1a1d1c"/>`);
    let s = `<rect x="-1200" y="-800" width="3500" height="${G + 800}" fill="${night ? "#5a5248" : "#e8dcc6"}"/><rect x="-1200" y="${G - 40}" width="3500" height="40" fill="#8a7a62"/>`;
    s += `<rect x="-1200" y="${G}" width="3500" height="1300" fill="#b98f62"/>${Array.from({ length: 24 }, (_, k) => `<path d="M${-1200 + k * 150},${G}V2800" stroke="#a37c52" stroke-width="4"/>`).join("")}`;
    if (o.dress !== false && window.Dress) s += classUnder(o, night);
    // the blackboard with its chalk tray; faded old lessons in the corner
    s += `<rect x="130" y="300" width="820" height="610" rx="10" fill="#7a5a3e" ${OUT}/><rect x="160" y="330" width="760" height="550" fill="url(#fBoard)"/><rect x="130" y="910" width="820" height="26" fill="#5f442d" ${OUT}/>
      <rect x="700" y="915" width="60" height="12" rx="4" fill="#f4ecd8"/><rect x="780" y="915" width="44" height="12" rx="4" fill="#f4ecd8"/><rect x="200" y="912" width="120" height="18" rx="4" fill="#3a3330"/>
      <g id="${id}-board"></g>`;
    // Thai alphabet poster, a clock stopped at 6:40, the national flag strip, a shelf with the old radio
    s += `<rect x="-220" y="360" width="260" height="360" fill="#f4ecd8" ${OUT}/>${["ก ไก่", "ข ไข่", "ค ควาย", "ง งู"].map((t, k) => `<text x="-90" y="${430 + k * 80}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="${["#c8392b", "#2f4a8a", "#1f3f31", "#b07f2c"][k]}">${t}</text>`).join("")}
      <g transform="translate(1080,400)"><circle r="70" fill="#f4ecd8" ${OUT}/><circle r="60" fill="none" stroke="#2e2a26" stroke-width="2"/><path d="M0,0L0,-44M0,0L28,22" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><circle r="5" fill="${INK}"/></g>
      <rect x="1000" y="620" width="360" height="22" fill="#8a6a42" ${OUT}/><rect x="1000" y="642" width="12" height="90" fill="#8a6a42"/><rect x="1348" y="642" width="12" height="90" fill="#8a6a42"/>`;
    s += `<g id="${id}-radio" transform="translate(1180,620)"><rect x="-120" y="-150" width="240" height="150" rx="14" fill="#6b4a2e" ${OUT}/><rect x="-100" y="-130" width="110" height="70" rx="8" fill="#1a1512" ${OUT}/><rect x="-96" y="-126" width="102" height="62" rx="6" fill="#2a1a0a"/>
      <g id="${id}-dialw"><rect x="-96" y="-126" width="102" height="62" rx="6" fill="#ffb35c" opacity="0"/></g>${Array.from({ length: 7 }, (_, k) => `<path d="M${-86 + k * 15},-118v12" stroke="#c9a55a" stroke-width="2"/>`).join("")}<rect id="${id}-needle" x="-40" y="-124" width="3" height="58" fill="#ff3b30"/>
      <rect x="20" y="-130" width="90" height="110" rx="6" fill="#2a2420"/>${Array.from({ length: 6 }, (_, k) => `<path d="M${30 + k * 14},-125v100" stroke="#c9a55a" stroke-width="3" opacity=".5"/>`).join("")}
      <circle cx="-72" cy="-32" r="18" fill="#c9a55a" ${OUT}/><circle cx="-20" cy="-32" r="18" fill="#c9a55a" ${OUT}/><path d="M100,-150L190,-330" stroke="#9aa0a6" stroke-width="6"/></g>`;
    // window with wooden shutters on the left wall, slats of light
    s += `<rect x="-640" y="300" width="330" height="520" fill="${night ? "#0b1020" : "#dfeef5"}" ${OUT}/><rect x="-680" y="300" width="50" height="520" fill="#6f8f58" ${OUT}/><rect x="-320" y="300" width="50" height="520" fill="#6f8f58" ${OUT}/>${Array.from({ length: 9 }, (_, k) => `<path d="M-640,${340 + k * 54}h330" stroke="#5a7a44" stroke-width="7"/>`).join("")}`;
    // teacher's desk (right front) + chair, little desks in rows (left)
    s += `<g id="${id}-desk" transform="translate(760,${G})"><rect x="-260" y="-320" width="520" height="30" fill="#8a6a42" ${OUT}/><rect x="-240" y="-290" width="480" height="150" fill="#a07a4a" ${OUT}/><rect x="-200" y="-260" width="140" height="40" rx="4" fill="#6f4f2e"/><path d="M-230,-140V0M230,-140V0" stroke="#5f442d" stroke-width="14"/></g>`;
    for (let k = 0; k < 3; k++) s += `<g transform="translate(${-420 + k * 240},${G - k * 10})"><rect x="-90" y="-260" width="180" height="20" fill="#c9a06c" ${OUT}/><path d="M-70,-240V0M70,-240V0" stroke="#5b6066" stroke-width="10"/><rect x="-60" y="-140" width="120" height="14" fill="#5b6066"/></g>`;
    // children's drawings pinned by the door (น้องปั้น's gallery)
    s += `${[[1420, 340], [1560, 360], [1440, 540]].map(([x, y], k) => `<g transform="translate(${x},${y}) rotate(${-4 + k * 5})"><rect width="120" height="150" fill="#f4ecd8" ${OUT}/><circle cx="60" cy="8" r="7" fill="#c8392b"/><path d="M20,120l20,-40l20,30l20,-50l20,60" stroke="#${["c8392b", "2f4a8a", "6f8f3e"][k]}" stroke-width="5" fill="none"/><circle cx="90" cy="40" r="14" fill="none" stroke="#f2c55c" stroke-width="5"/></g>`).join("")}`;
    put(L.set, s);
    if (o.dress !== false && window.Dress) { classDress(L, id, o, night);
      document.getElementById(`${id}-board`).insertAdjacentHTML("afterbegin", `<g opacity=".07" fill="#fff">${[[300, 420, 160, 40], [620, 560, 220, 50], [420, 760, 260, 60], [760, 400, 120, 30], [260, 640, 120, 36]].map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" transform="rotate(-6 ${x} ${y})"/>`).join("")}</g><path d="M170,860q200,-14 420,4" stroke="#fff" stroke-opacity=".08" stroke-width="16" fill="none"/>`); }
    if (o.cans) { // the haul laid out on the desk: twelve cans, one of them swollen (#id-bulge), a candle lantern beside them
      let c = `<g id="${id}-cans">`;
      const n = typeof o.cans === "number" ? o.cans : 12, bi = o.bulge ?? (n > 8 ? 8 : n - 2);
      for (let k = 0; k < n; k++) { const x = 540 + (k % 6) * 72, y = G - 320 - Math.floor(k / 6) * 56, b = k === bi; c += `<g id="${b ? `${id}-bulge` : `${id}-c${k}`}" transform="translate(${x},${y})"><rect x="-26" y="-70" width="52" height="70" rx="6" fill="url(#fCan)" ${OUT}/><rect x="-26" y="-50" width="52" height="32" fill="${["#c8392b", "#2f6fb8", "#e8b830", "#4f8a55"][k % 4]}" opacity=".85"/><path d="M-26,-70q26,${b ? -26 : -8} 52,0" fill="#cfd3d6" ${OUT}/>${b ? `<path d="M-18,-78q18,-12 36,0" stroke="#8d9299" stroke-width="2" fill="none"/>` : ""}</g>`; }
      c += `</g>`;
      put(L.set, c);
    }
    if (o.gen) { const gx = o.genX ?? -300; put(L.set, Sets.props.generator(`${id}-gen`, gx, G, 0.8, !!o.genOn));
      put(L.act, `<g id="${id}-co" opacity="${o.genOn ? 1 : 0}">${[0, 1, 2, 3].map((k) => `<path class="cowisp" d="M${gx + 152 + k * 10},${G - 236}q-40,-70 10,-140t-10,-150" stroke="#d8dde2" stroke-width="${11 - k * 2}" fill="none" stroke-linecap="round" opacity=".16"/>`).join("")}</g>`); }
    if (o.fan) put(L.set, Fence.FAN(id, o.fanX ?? 540, o.fanY ?? 110));
    if (o.bulb) { put(L.set, Fence.BULB(id, o.bulbX ?? 760, 120)); put(L.glow, `<g id="${id}-bulb" opacity="${o.bulbOn ? 1 : 0}"><circle cx="${o.bulbX ?? 760}" cy="180" r="800" fill="url(#fLamp)"/></g>`); }
    if (night) { put(L.glow, `<circle id="${id}-lamp" cx="${o.lampX ?? 760}" cy="${o.lampY ?? 1120}" r="520" fill="url(#fLamp)" opacity=".85"/>`); put(L.set, `<g transform="translate(${o.lampX ?? 760},${G - 320})"><rect x="-24" y="-130" width="48" height="130" rx="8" fill="#3a3330" ${OUT}/><rect x="-14" y="-110" width="28" height="80" fill="#ffd58a"/><path d="M-30,-140h60l-8,-16h-44z" fill="#5b6066" ${OUT}/></g>`); }
    else { put(L.glow, [0, 1, 2, 3].map((k) => `<path d="M${-620 + k * 80},${340}l40,0L${-300 + k * 70},${G + 60}l-70,0Z" fill="url(#zRay)" opacity=".6"/>`).join("")); }
  }
  // ---------------- set dressing for the classroom (user 28 Oct: "ฉากและสิ่งของละเอียดขึ้น") ----------------
  // painted dado with a trim rail, plaster stains, cracks and peeling paint, a damp patch from the roof; dead fluorescent tubes;
  // a map of Thailand and a crossed-off calendar (the camp's own count), a bookshelf with a globe and the first-aid box, rolled
  // sleeping mats under the window, bottled water and stores by the door, a broom and bin; window bars; boards with grain and
  // scuffs, dark where the floor meets the wall. o.dress === false skips it.
  function classUnder(o, night) {
    const D = Dress, r = mk((o.seed || 17) + 223), wall = night ? "#4a443c" : "#9fb39f";
    let s = `<rect x="-1200" y="-800" width="3500" height="${G + 760}" fill="url(#dConc)" opacity=".7"/>`;
    s += `<rect x="-1200" y="${G - 400}" width="3500" height="360" fill="${wall}"/><rect x="-1200" y="${G - 400}" width="3500" height="360" fill="url(#dGrime)"/><rect x="-1200" y="${G - 412}" width="3500" height="16" fill="${night ? "#3a342d" : "#6f8a74"}" stroke="${INK}" stroke-width="3"/><rect x="-1200" y="${G - 410}" width="3500" height="4" fill="#fff" opacity=".18"/>`;
    s += D.streak(-60, -800, 120, 1100, 0.6) + D.streak(1320, -800, 90, 900, 0.5) + D.crack(-460, 230, 120, 10, 0.45) + D.crack(1580, 820, 90, -20, 0.4) + D.crack(980, 1000, 70, 5, 0.35);
    // the floor: board grain, scuffs, a stray sheet of paper and a pencil, the dark seam along the wall foot
    s += `<rect x="-1200" y="${G}" width="3500" height="1300" fill="url(#dPlankH)" opacity=".5"/><rect x="-1200" y="${G}" width="3500" height="70" fill="url(#dAO)"/>`;
    s += `<g transform="translate(200,${G + 210}) rotate(-12)"><rect width="110" height="80" fill="#f4ecd8" stroke="${INK}" stroke-width="2"/><path d="M14,20h80M14,36h70M14,52h76" stroke="#9aa0a6" stroke-width="3"/></g><g transform="translate(1260,${G + 300}) rotate(24)"><rect width="90" height="9" rx="3" fill="#e8b830" stroke="${INK}" stroke-width="2"/><path d="M90,0l14,4.5l-14,4.5z" fill="#d9c9a0" stroke="${INK}" stroke-width="2"/></g>`;
    s += Array.from({ length: 10 }, () => `<path d="M${(-900 + r() * 2600).toFixed(0)},${(G + 60 + r() * 600).toFixed(0)}q${(30 + r() * 40).toFixed(0)},-6 ${(70 + r() * 60).toFixed(0)},2" stroke="#000" stroke-opacity=".12" stroke-width="4" fill="none" stroke-linecap="round"/>`).join("");
    return s;
  }
  function classDress(L, id, o, night) {
    const D = Dress, r = mk((o.seed || 17) + 211), wall = night ? "#4a443c" : "#9fb39f";
    let s = "";
    // dead fluorescent tubes on the ceiling line
    s += [-260, 1180].map((x) => `<g transform="translate(${x},140)"><path d="M-10,-200V-20M150,-200V-20" stroke="#5b6066" stroke-width="3"/><rect x="-40" y="-24" width="230" height="22" rx="6" fill="#d9d4c8" stroke="${INK}" stroke-width="3"/><rect x="-30" y="-2" width="210" height="12" rx="6" fill="#eef0ea" stroke="${INK}" stroke-width="2.5"/><path d="M-24,4h60" stroke="#8d9299" stroke-width="3"/></g>`).join("");
    // a map of Thailand (left wall) and the calendar with the days crossed off (right of the drawings)
    s += `<g transform="translate(-1040,330) rotate(-1.5)"><rect width="270" height="360" fill="#e9e1c8" stroke="${INK}" stroke-width="3"/><rect x="12" y="12" width="246" height="300" fill="#a9cbd9"/>
      <path d="M108,40C140,36 150,70 140,96C160,110 176,104 186,128C196,160 176,176 160,180C150,204 160,226 150,246C140,276 126,300 118,288C112,262 128,232 116,210C100,190 84,170 92,140C80,110 86,70 108,40Z" fill="#9fc27a" stroke="#4c6a2c" stroke-width="3"/>
      <circle cx="132" cy="168" r="6" fill="#c8392b"/><text x="135" y="342" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="28" fill="#2e2a26">แผนที่ประเทศไทย</text><circle cx="135" cy="-4" r="7" fill="#c8392b"/></g>`;
    s += `<g transform="translate(1730,350) rotate(2)"><rect width="190" height="250" fill="#f4ecd8" stroke="${INK}" stroke-width="3"/><rect width="190" height="46" fill="#c8392b"/><text x="95" y="34" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="28" fill="#f4ecd8">ตุลาคม</text>
      ${Array.from({ length: 28 }, (_, k) => { const cx = 18 + (k % 7) * 25, cy = 64 + Math.floor(k / 7) * 42; return `<rect x="${cx - 9}" y="${cy}" width="18" height="30" fill="none" stroke="#c9bfa8" stroke-width="1.5"/>${k < 23 ? `<path d="M${cx - 8},${cy + 2}l16,26M${cx + 8},${cy + 2}l-16,26" stroke="#c8392b" stroke-width="2.5"/>` : ""}`; }).join("")}<circle cx="95" cy="-6" r="6" fill="#3a3330"/></g>`;
    // bookshelf with a globe and the first-aid box (far left), bars on the window, rolled mats under it
    s += `<g transform="translate(-1150,${G})"><path d="M0,0V-470H360V0" fill="#8a6a42" stroke="${INK}" stroke-width="4"/><rect x="0" y="-470" width="360" height="470" fill="url(#dPlankH)" opacity=".6"/>${[-350, -230, -110].map((y) => `<rect x="10" y="${y}" width="340" height="14" fill="#6f4f2e" stroke="${INK}" stroke-width="2"/>`).join("")}
      ${Array.from({ length: 18 }, (_, k) => { const sh = Math.floor(k / 6), x = 20 + (k % 6) * 52 + r() * 6, h = 70 + r() * 30, c = ["#c8392b", "#2f6fb8", "#e8b830", "#4f8a55", "#8e2a2a", "#e8dcc6"][Math.floor(r() * 6)]; return `<rect x="${x.toFixed(0)}" y="${(-350 + sh * 120 - h).toFixed(0)}" width="${(22 + r() * 18).toFixed(0)}" height="${h.toFixed(0)}" fill="${c}" stroke="${INK}" stroke-width="2" transform="rotate(${k % 5 === 4 ? 14 : 0} ${x.toFixed(0)} ${-350 + sh * 120})"/>`; }).join("")}
      <g transform="translate(80,-470)"><path d="M0,0v-14M-30,0h60" stroke="#5b6066" stroke-width="5"/><circle cx="0" cy="-58" r="44" fill="#6fa6c9" stroke="${INK}" stroke-width="3"/><path d="M-26,-80q16,-6 22,10q8,18 -6,30M14,-90q20,10 18,34" stroke="#9fc27a" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M-44,-58a44,44 0 0 1 88,0" stroke="#3a3330" stroke-width="3" fill="none" transform="rotate(-20 0 -58)"/></g>
      <g transform="translate(230,-470)"><rect x="0" y="-70" width="100" height="70" rx="6" fill="#f4ecd8" stroke="${INK}" stroke-width="3"/><path d="M50,-58v46M28,-35h44" stroke="#c8392b" stroke-width="12"/></g></g>`;
    s += `${Array.from({ length: 6 }, (_, k) => `<rect x="${-620 + k * 52}" y="300" width="10" height="520" fill="#3f454b"/>`).join("")}<path d="M-640,560h330" stroke="#3f454b" stroke-width="8"/>`;
    s += D.mats(-520, G - 8, 0.9) + D.bottles(1480, G, 0.9, 6) + D.stores(1700, G, 0.85) + D.broom(1880, G, 0.9, -8) + D.bucket(1960, G, 0.8, "#4f8a55");
    // where the camera actually looks: the school motto over the board, a string of the children's paintings under it,
    // erased-chalk haze on the board, books and a pencil mug on the teacher's desk, a woven mat with a pillow and blanket on the floor
    s += `<g transform="translate(540,250)"><path d="M-330,-30Q0,-4 330,-30L320,30Q0,50 -320,30Z" fill="#f2e6c8" stroke="${INK}" stroke-width="3"/><path d="M-330,-30l-30,40l40,10M330,-30l30,40l-40,10" fill="#c8392b" stroke="${INK}" stroke-width="2.5"/>
      <text x="0" y="12" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#2f4a8a">ความรู้คู่คุณธรรม</text><path d="M-300,-24q300,22 600,0" stroke="#c9b48a" stroke-width="2" fill="none"/></g>`;
    const KIDART = [   // eight different crayon pictures: house, sun over hills, fish, flower, cat, tree, family, boat
      (c) => `<path d="M-18,60V36L0,20L18,36V60Z" fill="none" stroke="${c}" stroke-width="4"/><rect x="-5" y="44" width="10" height="16" fill="${c}"/>`,
      (c) => `<path d="M-26,62Q-10,40 4,58Q16,44 28,62" stroke="#4f8a55" stroke-width="4" fill="none"/><circle cx="12" cy="28" r="10" fill="#f2c55c"/>`,
      (c) => `<path d="M-20,44Q0,28 16,44Q0,60 -20,44ZM16,44l12,-10v20z" fill="${c}"/><circle cx="-10" cy="42" r="2.5" fill="#2e2a26"/>`,
      (c) => `<path d="M0,64V40" stroke="#4f8a55" stroke-width="4"/>${[0, 72, 144, 216, 288].map((a) => `<circle cx="${(Math.cos((a * Math.PI) / 180) * 9).toFixed(1)}" cy="${(32 + Math.sin((a * Math.PI) / 180) * 9).toFixed(1)}" r="6" fill="${c}"/>`).join("")}<circle cx="0" cy="32" r="5" fill="#f2c55c"/>`,
      (c) => `<path d="M-18,30l4,-14l8,10h12l8,-10l4,14q2,22 -18,24q-20,-2 -18,-24z" fill="none" stroke="${c}" stroke-width="4"/><circle cx="-7" cy="34" r="2.5" fill="#2e2a26"/><circle cx="7" cy="34" r="2.5" fill="#2e2a26"/>`,
      (c) => `<path d="M0,66V44" stroke="#8a5a3a" stroke-width="6"/><circle cx="0" cy="32" r="16" fill="#4f8a55"/>`,
      (c) => `${[-16, 0, 14].map((x, k) => `<circle cx="${x}" cy="${30 + k * 3}" r="5" fill="none" stroke="${["#2f6fb8", "#c8392b", "#e8b830"][k]}" stroke-width="3"/><path d="M${x},${36 + k * 3}v14m-6,-8h12m-10,18l4,-10l4,10" stroke="${["#2f6fb8", "#c8392b", "#e8b830"][k]}" stroke-width="3" fill="none"/>`).join("")}`,
      (c) => `<path d="M-24,50h48l-8,12h-32z" fill="${c}"/><path d="M0,50V22l16,24z" fill="#f4ecd8" stroke="#2e2a26" stroke-width="2"/><path d="M-28,66q14,-6 28,0t28,0" stroke="#2f6fb8" stroke-width="3" fill="none"/>`,
    ];
    s += `<path d="M120,968Q530,1004 960,968" stroke="#c9b48a" stroke-width="2.5" fill="none"/>${Array.from({ length: 8 }, (_, k) => { const x = 160 + k * 100, y = 968 + 4 * 36 * ((x - 120) / 840) * (1 - (x - 120) / 840), c = ["#c8392b", "#2f6fb8", "#e8b830", "#4f8a55", "#8e2a2a", "#d96a8a", "#2f6fb8", "#c8392b"][k];
      return `<g transform="translate(${x},${y.toFixed(0)}) rotate(${[-5, 3, -2, 6, -4, 2, -6, 4][k]}) scale(.82)"><rect x="-36" y="6" width="72" height="80" fill="${["#f4ecd8", "#efe6cf", "#f6efe0", "#ece2c8"][k % 4]}" stroke="${INK}" stroke-width="2"/><rect x="-8" y="-2" width="16" height="12" fill="#e8b830" stroke="${INK}" stroke-width="1.5"/>${KIDART[k](c)}</g>`; }).join("")}`;
    s += `<g transform="translate(980,${G - 320})"><rect x="-44" y="-26" width="80" height="26" fill="#2f6fb8" stroke="${INK}" stroke-width="2.5"/><rect x="-40" y="-48" width="72" height="22" fill="#c8392b" stroke="${INK}" stroke-width="2.5"/><rect x="-36" y="-66" width="64" height="18" fill="#e8dcc6" stroke="${INK}" stroke-width="2.5"/></g>
      <g transform="translate(470,${G - 320})"><path d="M-18,0v-46h36v46z" fill="#e8dcc6" stroke="${INK}" stroke-width="2.5"/><path d="M-10,-46l-6,-30M2,-46l4,-34M10,-46l12,-26" stroke="#e8b830" stroke-width="5" stroke-linecap="round"/><path d="M-10,-40v34" stroke="#fff" stroke-opacity=".5" stroke-width="4"/></g>`;
    s += `<g transform="translate(-40,${G + 110})"><path d="M-260,0L380,0L420,150L-300,150Z" fill="#c9a24a" stroke="${INK}" stroke-width="3"/>${Array.from({ length: 14 }, (_, k) => `<path d="M${-280 + k * 50},0l${-6 + k * 1},150" stroke="#a5803a" stroke-width="3"/>`).join("")}<path d="M-270,40H395M-285,95H408" stroke="#b8442a" stroke-width="6" opacity=".6"/>
      <rect x="-200" y="18" width="150" height="60" rx="26" fill="#e8e4da" stroke="${INK}" stroke-width="3"/><path d="M-190,40q60,-12 130,0" stroke="#c9c3b6" stroke-width="3" fill="none"/><path d="M60,30h240l30,90h-280z" fill="#4f6a8a" stroke="${INK}" stroke-width="3"/><path d="M70,60h246M78,90h252" stroke="#3c5470" stroke-width="5"/></g>`;
    put(L.set, s);
  }
  // chalk strokes on the board (set id of the classroom): text lines with a chalk filter, each wrapped for clip reveals
  function chalk(id, lines) {
    const el = document.getElementById(`${id}-board`);
    el.insertAdjacentHTML("beforeend", lines.map((ln, k) => `<g class="chalk" id="${id}-ch${k}" opacity="${ln.hide ? 0 : 1}"><text x="${ln.x}" y="${ln.y}" text-anchor="${ln.anchor || "start"}" font-family="Kanit" font-weight="${ln.w || 700}" font-size="${ln.size || 50}" fill="${ln.color || "#f4ecd8"}" opacity=".92" filter="url(#fChalk)" style="letter-spacing:2px">${ln.text}</text></g>`).join(""));
  }

  // ---------------- the abandoned fresh market: tin roof with holes, concrete stalls, metal shelves with the last cans, a vendor standing still in the gap ----------------
  // ids: #id-gap (where ha3 stands, x≈300), #id-cans (the cans on the near shelf), #id-fall (a can that drops)
  function market(L, o = {}) {
    const id = o.id || "mk", r = mk(o.seed || 53);
    sky(L, o.time || "day");
    put(L.far, paddies(r, o.time || "day", 980));
    // back: roof underside with holes, a long back wall of shuttered shophouses, hanging tarps
    let s = `<path d="M-1200,-800H2300V560H-1200Z" fill="#4a4f55"/>${Array.from({ length: 20 }, (_, k) => `<path d="M${-1200 + k * 180},-800V560" stroke="#3a3f45" stroke-width="6"/>`).join("")}`;
    s += `<path d="M-1200,560H2300V700H-1200Z" fill="#8d9299" ${OUT}/>`;
    s += `${[[-600, 90], [100, 140], [900, 70], [1500, 120]].map(([x, w]) => `<ellipse cx="${x}" cy="200" rx="${w}" ry="${w * 0.4}" fill="#f6ecd2"/>`).join("")}`;
    s += `<rect x="-1200" y="700" width="3500" height="${G - 700}" fill="#c8c0ae"/>${Array.from({ length: 12 }, (_, k) => `<rect x="${-1150 + k * 300}" y="760" width="220" height="${G - 760}" fill="#9aa0a6" ${OUT}/>${Array.from({ length: 9 }, (_, j) => `<path d="M${-1150 + k * 300},${790 + j * 60}h220" stroke="#7f858c" stroke-width="5"/>`).join("")}`).join("")}`;
    s += `${[[-400, "#2f6fb8"], [500, "#c8392b"], [1300, "#e8b830"]].map(([x, c]) => `<path d="M${x},700l-60,260l120,-40l40,220l80,-180l40,60V700Z" fill="${c}" opacity=".7"/>`).join("")}`;
    put(L.mid, s);
    const dressed = o.dress !== false && window.Dress, floor = dressed ? marketDress(L, id, o) : "";
    // the floor and the stalls: concrete tables in two rows, overturned baskets, a puddle, the near shelf of cans
    let t = `<rect x="-1200" y="${G - 60}" width="3500" height="1400" fill="#8f8a7c"/><path d="M-1200,${G + 300}H2300" stroke="#6f6a5e" stroke-width="6"/><ellipse cx="900" cy="${G + 240}" rx="260" ry="40" fill="#5f6a70" opacity=".6"/>`;
    t += floor;
    const stall = (x, y, w) => `<g transform="translate(${x},${y})"><rect x="0" y="-120" width="${w}" height="28" fill="#cfc9bb" ${OUT}/><rect x="10" y="-92" width="${w - 20}" height="92" fill="#b3ada0" ${OUT}/><path d="M${w * 0.5},-92V0" stroke="#9f9a8e" stroke-width="4"/></g>`;
    t += stall(-700, G - 80, 500) + stall(-100, G - 80, 300) + stall(1040, G - 80, 520);
    // a metal shelf unit left of centre with a gap beside it (the vendor stands in #id-gap), a few cans left on it
    t += `<g transform="translate(-560,${G})"><rect x="0" y="-620" width="420" height="620" fill="none" stroke="#5b6066" stroke-width="16"/>${[-520, -400, -280, -160].map((y) => `<rect x="0" y="${y}" width="420" height="14" fill="#5b6066"/>`).join("")}
      ${[[40, -530, "#c8392b"], [110, -530, "#2f6fb8"], [320, -410, "#e8b830"], [60, -290, "#4f8a55"], [240, -290, "#c8392b"], [300, -170, "#2f6fb8"]].map(([x, y, c]) => `<g><rect x="${x}" y="${y}" width="44" height="60" rx="5" fill="url(#fCan)" ${OUT}/><rect x="${x}" y="${y + 18}" width="44" height="26" fill="${c}" opacity=".85"/></g>`).join("")}</g>`;
    t += `<rect id="${id}-gap" x="-120" y="${G - 640}" width="240" height="640" fill="#2a2724"/>`;
    t += `<g transform="translate(240,${G})"><rect x="0" y="-620" width="420" height="620" fill="none" stroke="#5b6066" stroke-width="16"/>${[-520, -400, -280, -160].map((y) => `<rect x="0" y="${y}" width="420" height="14" fill="#5b6066"/>`).join("")}
      <g id="${id}-cans">${[[30, -290, "#c8392b"], [84, -290, "#e8b830"], [138, -290, "#2f6fb8"], [192, -290, "#4f8a55"], [246, -290, "#c8392b"], [300, -290, "#e8b830"], [40, -170, "#2f6fb8"], [100, -170, "#c8392b"], [160, -170, "#4f8a55"], [220, -170, "#e8b830"], [290, -170, "#2f6fb8"], [350, -170, "#c8392b"]].map(([x, y, c], k) => `<g id="${id}-sc${k}" transform="translate(${x},${y})"><rect x="0" y="0" width="44" height="60" rx="5" fill="url(#fCan)" ${OUT}/><rect x="0" y="18" width="44" height="26" fill="${c}" opacity=".85"/>${k === 8 ? `<path d="M0,0q22,-18 44,0" fill="#cfd3d6" ${OUT}/>` : ""}</g>`).join("")}</g></g>`;
    t += `<g id="${id}-fall" transform="translate(470,${G - 310})"><rect x="0" y="0" width="44" height="60" rx="5" fill="url(#fCan)" ${OUT}/><rect x="0" y="18" width="44" height="26" fill="#e8b830" opacity=".85"/></g>`;
    t += `<g transform="translate(1180,${G})"><ellipse cx="0" cy="-20" rx="90" ry="40" fill="#b07f2c" ${OUT}/><path d="M-80,-30q80,-60 160,0" fill="none" stroke="#8a6a42" stroke-width="6"/></g><path d="M1500,${G - 10}l60,-60l40,40" stroke="#5b6066" stroke-width="8" fill="none"/>`;
    put(L.set, t);
    put(L.glow, `${[[-600, 90], [100, 140], [900, 70], [1500, 120]].map(([x, w]) => `<path d="M${x - w},200L${x + w},200L${x + w * 2.4},${G + 100}L${x - w * 2.4},${G + 100}Z" fill="url(#zRay)" opacity=".5"/>`).join("")}`);
    put(L.glow, Array.from({ length: 30 }, () => `<circle class="zdust" cx="${f1(-900 + r() * 2800)}" cy="${f1(300 + r() * 1100)}" r="${f1(1.6 + r() * 3)}" fill="#fff2dc" opacity="${f1(0.3 + r() * 0.4)}"/>`).join(""));
  }

  // ---------------- set dressing for the market (user 28 Oct: EP.1 sets to the yard's level) ----------------
  // shop signs over the shutters, rusted and tagged shutters, roof trusses and dead bulbs on a wire, a market banner, a wall clock;
  // on the floor: tiles with stains and a drain, stacked plastic crates, sacks, a toppled market umbrella, baskets of rotten
  // vegetables, a hanging scale, cardboard and plastic bags. Kept off the two shelf units and the gap where she stands.
  function marketDress(L, id, o) {
    const D = Dress, r = mk((o.seed || 53) + 307);
    let m = `<rect x="-1200" y="700" width="3500" height="${G - 700}" fill="url(#dConc)"/>`;
    m += Array.from({ length: 12 }, (_, k) => { const x = -1150 + k * 300; return D.rust(x + 30 + (k % 3) * 50, 780, 40, 300, 0.8) + D.streak(x + 120, 760, 60, 400, 0.7); }).join("");
    const SIGNS = [["ของชำ", "#c8392b"], ["ผลไม้", "#4f8a55"], ["ข้าวสาร", "#2f6fb8"], ["หมู·ไก่", "#b8463a"], ["ผัก", "#6f8f3e"], ["ปลา", "#2f4a8a"], ["ร้านทอง", "#c9a24a"], ["ขนม", "#d96a8a"], ["น้ำแข็ง", "#5a8ab8"], ["อะไหล่", "#5b6066"], ["ยา", "#c8392b"], ["ผ้า", "#8e2a2a"]];
    m += SIGNS.map(([t, c], k) => { const x = -1150 + k * 300, tilt = k % 4 === 2 ? 6 : k % 5 === 3 ? -4 : 0;
      return `<g transform="translate(${x},712) rotate(${tilt} 110 22)"><rect width="220" height="44" fill="${c}" stroke="${INK}" stroke-width="3"/><rect width="220" height="44" fill="url(#dGrime)"/><text x="110" y="33" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="#f4ecd8" opacity=".92">${t}</text></g>`; }).join("");
    m += [[-860, "ไม่มีคน"], [640, "ปิด"]].map(([x, t]) => `<text x="${x}" y="${G - 220}" font-family="Kanit" font-weight="900" font-size="54" fill="#c8392b" opacity=".55" transform="rotate(-6 ${x} ${G - 220})">${t}</text>`).join("");   // spray paint on the shutters
    m += `${Array.from({ length: 7 }, (_, k) => `<path d="M${-1200 + k * 600},-800L${-900 + k * 600},560M${-600 + k * 600},-800L${-900 + k * 600},560" stroke="#3a3f45" stroke-width="10"/>`).join("")}<path d="M-1200,380H2300" stroke="#3a3f45" stroke-width="14"/>`;   // roof trusses
    m += `<path d="M-1200,470Q-500,540 200,470T1600,470T2300,470" stroke="#2a2a2a" stroke-width="3" fill="none"/>${[-860, -340, 180, 700, 1220, 1740].map((x, k) => `<path d="M${x},${492 + (k % 2) * 10}v34" stroke="#2a2a2a" stroke-width="3"/><circle cx="${x}" cy="${540 + (k % 2) * 10}" r="13" fill="#e8e4da" stroke="${INK}" stroke-width="2.5"/><rect x="${x - 7}" y="${520 + (k % 2) * 10}" width="14" height="10" fill="#8d9299"/>`).join("")}`;
    m += `<g transform="translate(240,600)"><path d="M-420,0Q0,30 420,0V70Q0,96 -420,70Z" fill="#e8d6a0" stroke="${INK}" stroke-width="3"/><text x="0" y="52" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#c8392b">ตลาดสดเทศบาล</text><path d="M-420,0l-40,-60M420,0l40,-60" stroke="#c9b48a" stroke-width="3"/>${D.streak(-300, 10, 80, 80, 0.6)}</g>`;
    m += `<g transform="translate(1660,640)"><circle r="46" fill="#f4ecd8" stroke="${INK}" stroke-width="4"/><path d="M0,0V-30M0,0L20,14" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><path d="M-30,30l60,-60" stroke="#c8392b" stroke-width="3" opacity=".5"/></g>`;
    put(L.mid, m);
    // the floor: worn tiles, a drain channel, stains
    let f = `<rect x="-1200" y="${G - 60}" width="3500" height="1400" fill="url(#dTile)" opacity=".9"/><rect x="-1200" y="${G - 60}" width="3500" height="60" fill="url(#dAO)"/><rect x="-1200" y="${G + 420}" width="3500" height="26" fill="#3a3f45"/>${Array.from({ length: 40 }, (_, k) => `<path d="M${-1200 + k * 90},${G + 422}v22" stroke="#6b7177" stroke-width="5"/>`).join("")}`;
    f += [[-300, G + 140, 220, 40], [1400, G + 300, 260, 50], [600, G + 600, 300, 50]].map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#3a3020" opacity=".18"/>`).join("");
    f += D.leaves(-1100, 2200, G + 60, G + 800, 30, 307) + D.pebbles(-1100, 2200, G + 60, G + 800, 24, 311, 7);
    // crates, sacks, the umbrella, baskets of rot, a scale, cardboard and bags
    const crate = (x, y, c, k = 0) => D.at(x, y, 1, `<rect x="-60" y="-70" width="120" height="70" fill="${c}" stroke="${INK}" stroke-width="3"/>${[0, 1, 2, 3].map((j) => `<rect x="${-48 + j * 26}" y="-56" width="16" height="40" rx="4" fill="#000" opacity=".25"/>`).join("")}<rect x="-60" y="-70" width="120" height="8" fill="#fff" opacity=".2"/>`, k);
    f += crate(-900, G - 60, "#2f6fb8") + crate(-900, G - 130, "#c8392b") + crate(-780, G - 60, "#4f8a55") + crate(-890, G - 200, "#e8b830", -6);
    f += D.sandbags(1520, G - 40, 0.55, 3, 2, 313).replace(/#c2ad7c|#b39d6c|#cdb98a/g, (c) => ({ "#c2ad7c": "#e8e2d0", "#b39d6c": "#d9d2be", "#cdb98a": "#f0ebdc" })[c]);
    f += D.at(1900, G + 40, 1, `<path d="M-200,-20Q0,-160 200,-20Z" fill="#c8392b" stroke="${INK}" stroke-width="3"/>${[-150, -75, 0, 75, 150].map((x) => `<path d="M0,-20L${x},-${x === 0 ? 150 : 110 - Math.abs(x) * 0.2}" stroke="#8a1a1a" stroke-width="3"/>`).join("")}<path d="M-120,-60Q0,-150 120,-60" stroke="#f4ecd8" stroke-width="20" fill="none" opacity=".7"/><path d="M0,-20L60,120" stroke="#5b6066" stroke-width="8"/>`, 24);
    f += [[880, G - 80, "#7a6a2a"], [1000, G - 80, "#5a7a3a"]].map(([x, y, c]) => D.at(x, y, 1, `<path d="M-60,0L-70,-60H70L60,0Z" fill="#c9a24a" stroke="${INK}" stroke-width="3"/>${Array.from({ length: 6 }, (_, j) => `<path d="M${-60 + j * 22},-58l6,56" stroke="#a5803a" stroke-width="3"/>`).join("")}${[-36, -6, 26].map((cx) => `<circle cx="${cx}" cy="-64" r="18" fill="${c}" stroke="${INK}" stroke-width="2"/>`).join("")}<circle cx="-30" cy="-72" r="5" fill="#2a2a1a"/><path d="M20,-80q4,-14 12,-16" stroke="#3a4a1a" stroke-width="3" fill="none"/>`)).join("");
    f += D.at(780, G - 120, 1, `<path d="M0,-420V-170" stroke="#3a3330" stroke-width="3"/><circle cy="-130" r="44" fill="#d9dde0" stroke="${INK}" stroke-width="3"/><circle cy="-130" r="34" fill="#f4ecd8"/><path d="M0,-130l18,-20" stroke="#c8392b" stroke-width="4"/><path d="M-50,-80h100l-20,40h-60z" fill="#c9cdd1" stroke="${INK}" stroke-width="3"/>`);
    f += [[1250, G + 220, -10], [-600, G + 520, 14], [300, G + 380, 4]].map(([x, y, a]) => D.at(x, y, 1, `<path d="M-30,0q-10,-40 10,-50q30,-10 40,10q14,30 -10,40z" fill="#f4f4ee" opacity=".85" stroke="${INK}" stroke-width="2"/><path d="M-6,-48q6,-14 14,-10" stroke="#e8e4da" stroke-width="4" fill="none"/>`, a)).join("");
    f += D.at(-300, G - 70, 1, `<path d="M-70,0V-90L70,-110V-10Z" fill="#b8925a" stroke="${INK}" stroke-width="3"/><path d="M-70,-90L-20,-120L120,-136L70,-110Z" fill="#c9a46a" stroke="${INK}" stroke-width="3"/><path d="M-60,-60L60,-76" stroke="#8a6a3a" stroke-width="3"/>`);
    return f;
  }

  // ---------------- close-up: two hands holding a can whose lid has domed (#id-lid); optional child's hand from below (#id-kid) ----------------
  function canClose(L, o = {}) {
    const id = o.id || "cc", t = o.time || "dusk";
    sky(L, t);
    // behind the can, out of focus: at dusk the yard (the fence's bars as soft dark bands against the low sun, sun bokeh, warm ground);
    // at night the classroom (the board, the desk edge, the lamp and its bokeh) — soft shapes only, no blur filter
    if (t === "night") put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2a2520"/><rect x="-400" y="120" width="1700" height="620" rx="40" fill="#1e2a24" opacity=".85"/><rect x="-460" y="740" width="1820" height="40" rx="16" fill="#3a2e22" opacity=".8"/>
      <rect x="-1200" y="900" width="3500" height="1600" fill="#3a3026"/><rect x="-1200" y="880" width="3500" height="40" fill="#4a3e30"/>${[[220, 820, 120, 0.5], [880, 860, 80, 0.35], [1000, 760, 50, 0.3], [-100, 840, 60, 0.25]].map(([x, y, rr, op]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="url(#dEmber)" opacity="${op}"/>`).join("")}${[[620, 840], [700, 846], [780, 840]].map(([x, y], k) => `<rect x="${x}" y="${y - 70}" width="56" height="70" rx="8" fill="${["#7a3a2a", "#2a4a6a", "#7a6a2a"][k]}" opacity=".45"/>`).join("")}`);
    else put(L.far, `<rect x="-1200" y="880" width="3500" height="1700" fill="#8a6a42"/><rect x="-1200" y="860" width="3500" height="40" fill="#a07a4a"/>${Array.from({ length: 16 }, (_, k) => `<rect x="${-1100 + k * 160}" y="300" width="${k % 4 === 0 ? 70 : 30}" height="620" rx="12" fill="#3a2a2a" opacity="${k % 4 === 0 ? 0.42 : 0.28}"/>`).join("")}<rect x="-1200" y="420" width="3500" height="26" rx="12" fill="#3a2a2a" opacity=".3"/>
      ${[[760, 620, 140, 0.55], [300, 520, 70, 0.35], [980, 420, 50, 0.3], [120, 700, 90, 0.25]].map(([x, y, rr, op]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="url(#dSunBloom)" opacity="${op}"/>`).join("")}<rect x="-1200" y="880" width="3500" height="300" fill="#ffb070" opacity=".12"/>`);
    if (t === "night") put(L.glow, `<circle cx="300" cy="700" r="600" fill="url(#fLamp)" opacity=".7"/>`);
    // the can: big, centred, label torn, rust at the seam, the lid domed up (bulge = o.bulge 0..1)
    const b = o.bulge ?? 1;
    put(L.set, `<g id="${id}-can" transform="translate(540,1180)"><rect x="-230" y="-300" width="460" height="560" rx="30" fill="url(#fCan)" ${OUT}/>
      <rect x="-230" y="-140" width="460" height="260" fill="#c8392b" opacity=".9"/><rect x="-230" y="-140" width="460" height="40" fill="#f2c55c"/><text x="0" y="40" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="88" fill="#fff4ea" stroke="${INK}" stroke-width="6" paint-order="stroke">อาหารกระป๋อง</text>
      <path d="M-230,-140l40,80l-40,60Z" fill="#b3ada0"/><path d="M-120,-300v20M60,-300v20" stroke="#8a4a1a" stroke-width="8"/>${[[-200, -200], [180, -60], [-170, 160]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="14" fill="#8a4a1a" opacity=".7"/>`).join("")}
      <ellipse cx="0" cy="260" rx="230" ry="40" fill="#8d9299" ${OUT}/>
      ${[-280, -250, -220, 160, 190, 220].map((y) => `<path d="M-226,${y}Q0,${y + 22} 226,${y}" stroke="#7d848a" stroke-width="4" fill="none" opacity=".7"/><path d="M-226,${y + 4}Q0,${y + 26} 226,${y + 4}" stroke="#fff" stroke-width="2" fill="none" opacity=".35"/>`).join("")}
      <rect x="-176" y="-300" width="22" height="560" fill="#fff" opacity=".28"/><rect x="-130" y="-300" width="8" height="560" fill="#fff" opacity=".2"/><rect x="150" y="-300" width="60" height="560" fill="#000" opacity=".14"/><path d="M196,-300V260" stroke="#6b7177" stroke-width="3"/>
      <g transform="translate(-120,-60)"><path d="M-60,0Q-20,-34 40,-10Q70,-24 82,-36V24Q70,12 40,10Q-20,34 -60,0Z" fill="#f2c55c" stroke="${INK}" stroke-width="3"/><circle cx="-38" cy="-4" r="5" fill="${INK}"/><path d="M0,-14q8,14 0,28" stroke="${INK}" stroke-width="2" fill="none"/></g>
      <text x="80" y="-52" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="#f4ecd8">ปลาในซอสมะเขือเทศ</text><text x="0" y="96" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="22" fill="#f4ecd8" opacity=".8">น้ำหนักสุทธิ 155 ก. · EXP 03/26</text>
      <g transform="translate(120,64)"><rect x="0" y="0" width="80" height="44" fill="#f4ecd8"/>${Array.from({ length: 16 }, (_, k) => `<rect x="${4 + k * 4.6}" y="4" width="${k % 3 ? 2 : 3.4}" height="32" fill="${INK}"/>`).join("")}</g>
      ${[[-150, -300, 30, 160], [90, -300, 24, 120], [-60, 120, 26, 140]].map(([x, y, w, h]) => `<path d="M${x},${y}h${w}l-6,${h}h-${w - 12}z" fill="url(#dRust)"/>`).join("")}
      <path d="M140,150q30,20 60,0q-10,40 -30,50q-24,-10 -30,-50z" fill="#000" opacity=".18"/><path d="M146,148q24,14 48,0" stroke="#fff" stroke-width="3" fill="none" opacity=".4"/>
      <g id="${id}-lid"><path d="M-230,-300q0,-40 40,-40h380q40,0 40,40q-230,${-150 * b} -460,0z" fill="#dfe3e6" ${OUT}/><path d="M-190,-340q190,${-110 * b} 380,0" stroke="#a9b0b6" stroke-width="3" fill="none"/><path d="M-150,-350q150,${-60 * b} 300,-10" stroke="#fff" stroke-width="5" fill="none" opacity=".5"/><path d="M-60,-370l20,-20M20,-380l24,-22" stroke="#8a4a1a" stroke-width="4"/></g></g>`);
    // our hands on the can (POV): real grips, fingers wrapping over the label, thumbs hooked at the rim, forearms into the bottom corners (Hand.grip)
    const HC = { skin: o.skin || "#ecc29c", skinS: o.skinS, sleeve: o.sleeve || "#9fc5d8", sleeveS: o.sleeveS };
    put(L.fg, `<g id="${id}-hl" transform="translate(310,1200)">${Hand.grip(HC)}</g><g id="${id}-hr" transform="translate(770,1200) scale(-1,1)">${Hand.grip(HC)}</g>`);
    // o.release: a second pair of open hands (palms to us, fingers spread) hidden at the bottom corners, for the moment we let go —
    // shots fade #id-hl/#id-hr out and #id-hlo/#id-hro in so the hands are never left as fists clenched round nothing
    if (o.release) put(L.fg, `<g id="${id}-hlo" opacity="0" transform="translate(250,1420) rotate(-16) scale(1.6)">${Hand.open(HC)}</g><g id="${id}-hro" opacity="0" transform="translate(830,1420) rotate(16) scale(-1.6,1.6)">${Hand.open(HC)}</g>`);
    L.fg.classList.remove("fgblur");
    if (o.kid) put(L.act, `<g id="${id}-kid" transform="translate(-300,1500)"><g transform="scale(0.62)">${Hand.open({ skin: "#efc6a0", sleeve: "#f6f6f2", sleeveS: "#d8d4c8" })}</g></g>`);
  }

  // ---------------- the dirt road through the paddies (actors walk on y=G): heat shimmer at noon (#id-shim), the sun low at dusk ----------------
  function fieldRoad(L, o = {}) {
    const id = o.id || "fr", t = o.time || "noon", r = mk(o.seed || 29);
    sky(L, t); sunMoon(L, t, o.sunX ?? 640, 500);
    put(L.far, paddies(r, t, 1020));
    // the road converging to the horizon, with ruts; paddies either side with stubble and a buffalo wallow
    let s = `<path d="M-200,${G + 900}L430,1030H650L1280,${G + 900}Z" fill="url(#fDirt)" ${OUT}/><path d="M80,${G + 900}L500,1040M1000,${G + 900}L580,1040" stroke="#8f6f45" stroke-width="10" fill="none" opacity=".6"/>`;
    s += `<rect x="-1200" y="1030" width="3500" height="60" fill="${t === "night" ? "#2a3024" : t === "dusk" ? "#5c5a3a" : "#7d9a4a"}"/>`;
    s += `<path d="M-1200,1090H420L-200,${G + 900}H-1200Z M1300,${G + 900}L660,1090H2300V${G + 900}Z" fill="${t === "night" ? "#1f261b" : t === "dusk" ? "#6b5a38" : "#9fb860"}"/>`;
    for (let k = 0; k < 60; k++) { const u = r(), x = u < 0.5 ? -1100 + r() * 1300 : 900 + r() * 1300, y = 1120 + r() * 900; s += `<path d="M${f1(x)},${f1(y)}q5,-22 10,0q5,-18 10,0" stroke="${t === "night" ? "#2f3828" : "#6f8f3e"}" stroke-width="3" fill="none"/>`; }
    s += `<path d="M-1200,${G + 300}h1000M1300,${G + 500}h1100" stroke="${t === "night" ? "#2a3024" : "#5d7a35"}" stroke-width="6" opacity=".5"/>`;
    s += `<g transform="translate(-700,1180)"><ellipse rx="140" ry="40" fill="#6f6a4a" opacity=".6"/><path d="M-60,-10q20,-50 60,-50t60,50" fill="#3a3330" ${OUT}/><path d="M-20,-60q-20,-30 -40,-20M20,-60q20,-30 40,-20" stroke="${INK}" stroke-width="6" fill="none"/></g>`;
    put(L.set, s);
    if (o.dress !== false && window.Dress) fieldDress(L, id, o, t);
    if (t === "noon") put(L.glow, `<g id="${id}-shim">${Array.from({ length: 14 }, (_, k) => `<path d="M-1200,${1050 + k * 22}q200,8 400,0t400,0t400,0t400,0t400,0t400,0t400,0t400,0" stroke="#fff6dc" stroke-width="3" fill="none" opacity=".18"/>`).join("")}</g><rect x="-1200" y="980" width="3500" height="300" fill="url(#zHaze)" opacity=".9"/>`);
    if (t === "dusk") put(L.glow, `<rect x="-1200" y="900" width="3500" height="1300" fill="#ff9a3c" opacity=".12"/>`);
  }

  // ---------------- set dressing for the field road (user 28 Oct: EP.1 sets to the yard's level) ----------------
  // rice planted in rows that run to the horizon (clipped to each field), flooded patches holding the sky, a grass verge and
  // stones along both edges, gravel and potholes on the track, a kilometre post, a motorbike dumped in the paddy, a line of
  // fence posts with a sagging wire on the right
  function fieldDress(L, id, o, t) {
    const D = Dress, r = mk((o.seed || 29) + 401), night = t === "night", dusk = t === "dusk";
    const leftF = `M-1200,1090H420L-200,${G + 900}H-1200Z`, rightF = `M1300,${G + 900}L660,1090H2300V${G + 900}Z`, road = `M-200,${G + 900}L430,1030H650L1280,${G + 900}Z`;
    const rowC = night ? "#141a12" : dusk ? "#4a3e26" : "#5f7f34", tipC = night ? "#2a3424" : dusk ? "#8a7a4a" : "#b8d070";
    let s = `<clipPath id="${id}-fl"><path d="${leftF} ${rightF}"/></clipPath><clipPath id="${id}-rd"><path d="${road}"/></clipPath>`;
    let rows = ""; for (let k = -40; k <= 40; k++) { const xb = 540 + k * 70; rows += `<path d="M540,1040L${xb},${G + 900}" stroke="${rowC}" stroke-width="${f1(3 + Math.abs(k) * 0.08)}" stroke-dasharray="10 9"/>`; }
    for (let k = 0; k < 14; k++) { const y = 1100 + k * k * 7; rows += `<path d="M-1200,${y}H2300" stroke="${tipC}" stroke-width="${f1(1 + k * 0.4)}" opacity=".35"/>`; }
    // flooded patches in perspective
    [[-900, 1180, 300, 60], [1500, 1260, 420, 80], [-600, 1600, 520, 120], [1700, 1900, 600, 150]].forEach(([x, y, w, h]) => { rows += `<path d="M${x - w / 2},${y + h}L${x - w * 0.4},${y}H${x + w * 0.4}L${x + w / 2},${y + h}Z" fill="${night ? "#2a3a52" : dusk ? "#e8a070" : "#b9d6e0"}" opacity=".75"/><path d="M${x - w * 0.3},${y + h * 0.5}h${w * 0.5}" stroke="#fff" stroke-opacity=".35" stroke-width="${f1(h * 0.08)}"/>`; });
    s += `<g clip-path="url(#${id}-fl)">${rows}</g>`;
    // the track: gravel grain, ruts, potholes with water
    s += `<g clip-path="url(#${id}-rd)"><rect x="-1200" y="1000" width="3500" height="1500" fill="url(#dDirt)"/>${[[520, 1300, 70, 14], [700, 1650, 120, 22], [380, 2000, 160, 30]].map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#3e3020" opacity=".4"/><ellipse cx="${x}" cy="${y - 2}" rx="${rx * 0.8}" ry="${ry * 0.6}" fill="${night ? "#2a3a52" : dusk ? "#d89a6a" : "#a9c6d0"}" opacity=".8"/>`).join("")}</g>`;
    // verges: tufts and stones along both edges, bigger toward us
    for (let k = 0; k < 26; k++) { const u = k / 26, y = 1060 + u * u * 1300, xl = 430 - (630 * (y - 1030)) / (G + 900 - 1030), xr = 650 + (630 * (y - 1030)) / (G + 900 - 1030), h = 18 + u * 70;
      s += D.tuft(xl - 10 - r() * 30 * (1 + u), y, h, r, t === "noon") + D.tuft(xr + 10 + r() * 30 * (1 + u), y + 6, h, r, t === "noon"); }
    s += D.pebbles(-200, 1300, 1300, 2300, 30, 409, 10);
    // a kilometre post, a dumped motorbike, fence posts with a wire running off to the right
    s += D.at(1000, 1640, 1.1, `<ellipse cx="10" cy="4" rx="40" ry="8" fill="#0b0d08" opacity=".3"/><path d="M-26,0V-120Q-26,-150 0,-150Q26,-150 26,-120V0Z" fill="#f2efe6" stroke="${INK}" stroke-width="3"/><path d="M-26,-120Q-26,-150 0,-150Q26,-150 26,-120Z" fill="#c8392b"/><text x="0" y="-70" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="${INK}">12</text><rect x="8" y="-148" width="18" height="146" fill="#000" opacity=".12"/>`);
    s += D.at(-60, 1820, 1.15, `<ellipse cx="0" cy="6" rx="190" ry="20" fill="#0b0d08" opacity=".3"/><g transform="rotate(-8)"><circle cx="-110" cy="-50" r="52" fill="none" stroke="#1d1d1d" stroke-width="16"/><circle cx="110" cy="-40" r="52" fill="none" stroke="#1d1d1d" stroke-width="16"/><path d="M-110,-50L-30,-120H60L110,-40" stroke="#5b6066" stroke-width="10" fill="none"/><path d="M-60,-120Q0,-170 70,-130L60,-100H-40Z" fill="#c8392b" stroke="${INK}" stroke-width="3"/><path d="M-80,-140h50" stroke="#1d1d1d" stroke-width="14" stroke-linecap="round"/><path d="M60,-120l40,-50h30" stroke="#1d1d1d" stroke-width="7" fill="none"/>${D.rust(-40, -120, 30, 50)}</g>`);
    let fence = ""; for (let k = 0; k < 7; k++) { const u = k / 6, x = 760 + u * 1500, y = 1110 + u * u * 1100, h = 40 + u * 220; fence += `<rect x="${f1(x - 3 - u * 8)}" y="${f1(y - h)}" width="${f1(6 + u * 16)}" height="${f1(h)}" fill="${night ? "#2a2420" : "#6b4a2e"}" stroke="${INK}" stroke-width="${f1(1 + u * 2)}"/>`; }
    fence += `<path d="M757,1080Q1100,1150 1400,1240T2260,1990" stroke="#9aa0a6" stroke-width="2.5" fill="none"/>`;
    s += fence;
    put(L.set, s);
  }

  // ---------------- close-up of the gate from inside: bars, the cross rail, the bolt (#id-bolt slides x), arms through the bars (#id-arms) ----------------
  function gateClose(L, o = {}) {
    const id = o.id || "gc", t = o.time || "dusk", r = mk(o.seed || 61);
    sky(L, t); sunMoon(L, t, 300, 600);
    put(L.far, paddies(r, t, 1100));
    put(L.mid, `<path d="M-1200,1180L2300,1180V${G + 900}H-1200Z" fill="url(#fDirt)"/>`);
    // outside: the road up to the gate, dusk haze
    let s = `<g id="${id}-arms" opacity="${o.arms ? 1 : 0}">${[[260, 1120, -10], [520, 1060, 8], [760, 1140, -4]].map(([x, y, a]) => `<g transform="translate(${x},${y}) rotate(${a})"><path d="M0,0C-10,80 -6,160 0,240" stroke="${INK}" stroke-width="54" stroke-linecap="round" fill="none"/><path d="M0,0C-10,80 -6,160 0,240" stroke="#9dac92" stroke-width="44" stroke-linecap="round" fill="none"/><path d="M-30,250l-10,36M-8,256l-2,40M14,254l6,38M30,246l16,30" stroke="#9dac92" stroke-width="14" stroke-linecap="round"/><path d="M-40,286l-6,14M-10,296l0,14M20,292l4,14M46,276l8,12" stroke="#1b1612" stroke-width="7" stroke-linecap="round"/><circle cx="4" cy="60" r="12" fill="#7a1414" opacity=".8"/></g>`).join("")}</g>`;
    put(L.set, s);
    // the gate itself: thick bars, two rails, the bolt on our side
    let g = `<rect x="-1200" y="${G + 40}" width="3500" height="40" fill="#3a3f45"/><g id="${id}-bars">`;
    for (let b = -10; b < 12; b++) g += `<rect x="${-80 + b * 110}" y="-200" width="34" height="${G + 260}" fill="#3f454b" ${OUT}/>`;
    g += `<rect x="-1300" y="560" width="2580" height="60" fill="#3a3f45" ${OUT}/><rect x="-1300" y="1360" width="2580" height="60" fill="#3a3f45" ${OUT}/>`;
    g += `<rect x="-1300" y="-240" width="2580" height="60" fill="#3a3f45" ${OUT}/>`;
    g += `<g id="${id}-bolt" transform="translate(${o.bolt ?? 0},0)"><rect x="620" y="1180" width="560" height="60" rx="20" fill="#8d9299" ${OUT}/><rect x="560" y="1150" width="110" height="120" rx="14" fill="#5b6066" ${OUT}/><rect x="1150" y="1160" width="40" height="100" rx="8" fill="#5b6066" ${OUT}/></g>`;
    if (window.Dress) { for (let b = -10; b < 12; b++) g += `<rect x="${-74 + b * 110}" y="-200" width="7" height="${G + 260}" fill="#9aa0a6" opacity=".5"/>` + (b % 3 === 0 ? Dress.rust(-76 + b * 110, 600 + (b % 4) * 80, 28, 380) : "");
      g += `<g transform="translate(1260,1290)"><path d="M0,0q-20,40 -6,80q16,40 -4,80" stroke="#7d848a" stroke-width="12" fill="none" stroke-dasharray="18 6"/><g transform="translate(-14,170)"><path d="M-22,0V-24Q-22,-46 0,-46Q22,-46 22,-24V0" stroke="#9aa0a6" stroke-width="9" fill="none"/><rect x="-34" y="-4" width="68" height="62" rx="8" fill="#c9a24a" stroke="${INK}" stroke-width="3"/><circle cy="22" r="7" fill="${INK}"/><path d="M0,26v14" stroke="${INK}" stroke-width="4"/><rect x="-30" y="0" width="12" height="54" fill="#fff" opacity=".25"/></g></g>`; }
    g += `</g><rect x="1180" y="-240" width="80" height="${G + 320}" fill="#5b6066" ${OUT}/><rect x="1260" y="-300" width="80" height="${G + 400}" fill="#cfc9bb" ${OUT}/><rect x="1160" y="1130" width="200" height="160" rx="10" fill="none" stroke="#5b6066" stroke-width="14"/>`;
    // beyond the gate pillar the fence goes on: rails and bars up close, another concrete post (so a drifting camera never finds open ground)
    g += `<rect x="1340" y="560" width="1100" height="60" fill="#3a3f45" ${OUT}/><rect x="1340" y="1360" width="1100" height="60" fill="#3a3f45" ${OUT}/>${Array.from({ length: 10 }, (_, b) => `<rect x="${1390 + b * 110}" y="420" width="34" height="${G - 300}" fill="#3f454b" ${OUT}/>`).join("")}<rect x="1900" y="300" width="110" height="${G - 120}" fill="#cfc9bb" ${OUT}/>`;
    put(L.fg, g);
    L.fg.classList.remove("fgblur");
    if (t === "dusk") put(L.glow, `<rect x="-1200" y="800" width="3500" height="1400" fill="#ff9a3c" opacity=".12"/>`);
  }

  // ---------------- morning close-up of the tank's gauge: a clear tube with marks, the float (#id-float) one notch lower; เจ๊หงส์'s finger (#id-finger) ----------------
  function tankClose(L, o = {}) {
    const id = o.id || "tk";
    sky(L, "morning");
    put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#d9d4c8"/><rect x="-1200" y="-800" width="1300" height="3600" fill="#cfc9bb"/><path d="M-1200,400H2300M-1200,1000H2300" stroke="#9f9a8e" stroke-width="6"/>`);
    if (window.Dress) put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#dConc)"/>${Dress.streak(-200, -800, 140, 1600, 0.7)}${Dress.streak(900, -800, 90, 1300, 0.6)}${Dress.streak(1500, 400, 120, 900, 0.5)}${Dress.moss(-1200, 1990, 3500, mk(13))}${Dress.crack(1200, 300, 180, 15, 0.45)}`);
    put(L.mid, `<rect x="700" y="-800" width="90" height="3600" fill="#8a857a" ${OUT}/>${Array.from({ length: 10 }, (_, k) => `<path d="M640,${-700 + k * 300}h210" stroke="#8a857a" stroke-width="26"/>`).join("")}`);
    let s = `<rect x="300" y="200" width="150" height="1500" rx="60" fill="#e8f1f5" ${OUT}/>${Array.from({ length: 10 }, (_, k) => `<path d="M300,${320 + k * 140}h-70" stroke="${INK}" stroke-width="8"/><text x="200" y="${338 + k * 140}" text-anchor="end" font-family="Kanit" font-weight="700" font-size="52" fill="${INK}">${10 - k}</text>`).join("")}`;
    s += `<rect id="${id}-water" x="312" y="${320 + 140 * (10 - (o.level ?? 7))}" width="126" height="${1380 - 140 * (10 - (o.level ?? 7))}" rx="50" fill="#6fb3d6" opacity=".85"/>`;
    s += `<g id="${id}-float" transform="translate(375,${320 + 140 * (10 - (o.level ?? 7))})"><rect x="-56" y="-30" width="112" height="60" rx="16" fill="#c8392b" ${OUT}/><path d="M-70,0h140" stroke="#c8392b" stroke-width="8"/></g>`;
    s += `<path d="M375,1700v120h300" stroke="#8a857a" stroke-width="18" fill="none"/>${[[380, 1740], [400, 1790]].map(([x, y]) => `<path d="M${x},${y}c8,14 10,22 2,26c-8,-4 -8,-12 -2,-26z" fill="#6fb3d6"/>`).join("")}`;
    // a pencil mark from last night at the old level, now one notch above the float
    s += `<g id="${id}-mark"><path d="M240,${330 + 140 * (10 - (o.level ?? 7) - 1)}h130" stroke="#c8392b" stroke-width="6" stroke-dasharray="14 8"/><text x="470" y="${346 + 140 * (10 - (o.level ?? 7) - 1)}" font-family="Kanit" font-weight="700" font-size="40" fill="#c8392b">เมื่อคืน</text></g>`;
    put(L.set, s);
    put(L.fg, `<g id="${id}-finger" transform="translate(900,1500)"><g transform="scale(0.8)">${Hand.point({ skin: "#e6b48c", skinS: "#c48a62", sleeve: "#d96a8a", sleeveS: "#b04f6e" })}</g></g>`);
    L.fg.classList.remove("fgblur");
    put(L.glow, `<path d="M-300,-200L-100,-200L600,1900L300,1900Z" fill="url(#zRay)" opacity=".7"/>`);
  }

  // ---------------- night: the old radio on the shelf, its dial glowing when it wakes (#id-dialw), needle (#id-needle); the room dark ----------------
  function radioClose(L, o = {}) {
    const id = o.id || "rc";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#0b0d12"/>`);
    put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2a2620"/><rect x="-1200" y="1180" width="3500" height="40" fill="#5a4630"/><rect x="-1200" y="1220" width="3500" height="1200" fill="#3a2e20"/>`);
    let s = `<g transform="translate(540,1180)"><rect x="-420" y="-470" width="840" height="470" rx="40" fill="#6b4a2e" ${OUT}/><rect x="-400" y="-450" width="800" height="430" rx="30" fill="#7a5a3e"/>
      <rect x="-360" y="-410" width="400" height="220" rx="16" fill="#1a1512" ${OUT}/><rect x="-350" y="-400" width="380" height="200" rx="12" fill="#2a1a0a"/>
      <g id="${id}-dialw" opacity="0"><rect x="-350" y="-400" width="380" height="200" rx="12" fill="#ffb35c" opacity=".55"/></g>
      ${Array.from({ length: 13 }, (_, k) => `<path d="M${-330 + k * 30},${-380}v${k % 3 ? 16 : 30}" stroke="#e9d9a8" stroke-width="3"/>`).join("")}<text x="-160" y="-230" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#e9d9a8" opacity=".8">AM 530 · 700 · 900 · 1200 · 1600</text>
      <rect id="${id}-needle" x="-200" y="-396" width="5" height="190" fill="#ff3b30"/>
      <rect x="80" y="-410" width="280" height="330" rx="14" fill="#2a2420" ${OUT}/>${Array.from({ length: 11 }, (_, k) => `<path d="M${100 + k * 24},-400v310" stroke="#c9a55a" stroke-width="5" opacity=".55"/>`).join("")}
      <circle cx="-260" cy="-110" r="56" fill="#c9a55a" ${OUT}/><circle cx="-100" cy="-110" r="56" fill="#c9a55a" ${OUT}/><path d="M-260,-150v30M-100,-150v30" stroke="${INK}" stroke-width="6"/><text x="-180" y="-30" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#e9d9a8" opacity=".7">THANARAT · 1979</text>
      <path d="M360,-470L560,-900" stroke="#9aa0a6" stroke-width="10"/><circle cx="560" cy="-900" r="10" fill="#9aa0a6"/>
      <rect x="-440" y="0" width="880" height="26" fill="#5a4630" ${OUT}/></g>`;
    s += `<g transform="translate(-180,1180)"><rect x="-60" y="-220" width="120" height="220" rx="10" fill="#3a3330" ${OUT}/><rect x="-40" y="-190" width="80" height="140" fill="#2a2420"/></g>`;
    if (window.Dress) s += `<g transform="translate(540,1180)"><rect x="-400" y="-450" width="800" height="430" rx="30" fill="url(#dWood)" opacity=".5"/></g>
      <g transform="translate(1080,1180)"><rect x="-50" y="-120" width="100" height="120" rx="12" fill="#cfe6ee" fill-opacity=".35" stroke="${INK}" stroke-width="3"/><rect x="-18" y="-96" width="36" height="96" fill="#f4ecd8" stroke="${INK}" stroke-width="2"/><path class="flame" d="M0,-96c-14,-20 -6,-40 0,-56c6,16 14,36 0,56z" fill="#ffb35c"/><path d="M0,-100c-6,-10 -2,-20 0,-28c2,8 6,18 0,28z" fill="#fff2c0"/></g>
      <g transform="translate(-520,1180)">${[["#2f4a8a", 0], ["#8e2a2a", -34], ["#4f8a55", -62]].map(([c, y], k) => `<rect x="${-110 + k * 10}" y="${y - 34}" width="${220 - k * 20}" height="34" fill="${c}" stroke="${INK}" stroke-width="3"/><path d="M${-100 + k * 10},${y - 17}h${200 - k * 20}" stroke="#f4ecd8" stroke-width="2" opacity=".5"/>`).join("")}</g>
      <g transform="translate(-330,1180)">${[0, 1, 2, 3].map((k) => `<rect x="${k * 30}" y="-64" width="26" height="64" rx="4" fill="${k % 2 ? "#c9a24a" : "#2a2a2a"}" stroke="${INK}" stroke-width="2"/><rect x="${k * 30 + 8}" y="-70" width="10" height="7" fill="#9aa0a6"/>`).join("")}</g>
      <g transform="translate(1260,780) rotate(4)"><rect width="150" height="190" fill="#6b4a2e" stroke="${INK}" stroke-width="4"/><rect x="16" y="16" width="118" height="158" fill="#d9cfb8"/><circle cx="56" cy="80" r="16" fill="#7a6a5a"/><circle cx="96" cy="84" r="14" fill="#7a6a5a"/><path d="M30,174q26,-60 52,-60q26,0 52,60" fill="#7a6a5a"/></g>
      ${Dress.streak(-900, -800, 160, 1400, 0.5)}${Dress.streak(1500, -800, 120, 1200, 0.45)}${Dress.crack(-700, 400, 140, 12, 0.5)}`;
    put(L.set, s);
    put(L.glow, `<g id="${id}-glow" opacity="0"><circle cx="380" cy="880" r="520" fill="url(#fDial)"/></g>`);
  }

  // ---------------- น้องปั้น's crayon drawing, full frame on a pinned sheet: the school, five figures by the building, a sixth (#id-six) on top of the tank ----------------
  function drawing(L, o = {}) {
    const id = o.id || "dw";
    if (!o.onPlate) put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#5a4630"/>`);
    let s = o.onPlate ? `<g transform="${o.onPlate}">` : `<g transform="rotate(-2 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    s += C("M200,420q60,-60 120,0M160,480q100,-120 200,0", "#f2c55c", 12) + `<circle cx="260" cy="430" r="60" fill="#f2c55c" opacity=".8" filter="url(#fCrayon)"/>`;
    s += C("M150,1300H930", "#6f8f3e", 14) + C("M150,1300l0,-120M250,1300l0,-120M350,1300l0,-120M450,1300l0,-120M750,1300l0,-120M850,1300l0,-120M930,1300l0,-120M150,1180H930", "#5b6066", 8);
    s += C("M200,1140V820H640V1140M160,820L420,700L680,820M250,900h80v120h-80zM480,900h80v120h-80z", "#c8392b", 10) + `<rect x="200" y="820" width="440" height="320" fill="#f6d6a0" opacity=".6" filter="url(#fCrayon)"/>`;
    s += C("M760,1140V760M880,1140V760M740,760h160v-120h-160z", "#5b6066", 10) + `<rect x="740" y="640" width="160" height="120" fill="#9fc5d8" opacity=".7" filter="url(#fCrayon)"/>`;
    const fig = (x, y, col, h = 1) => `<g transform="translate(${x},${y}) scale(${h})" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="none" stroke="${col}" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,-80l40,40M0,0l-30,60M0,0l30,60" stroke="${col}" stroke-width="8" fill="none" stroke-linecap="round"/><circle cx="-10" cy="-136" r="4" fill="${col}"/><circle cx="10" cy="-136" r="4" fill="${col}"/><path d="M-12,-118q12,10 24,0" stroke="${col}" stroke-width="4" fill="none"/></g>`;
    s += fig(280, 1420, "#2f4a8a") + fig(380, 1430, "#c8392b") + fig(470, 1420, "#6f8f3e") + fig(560, 1430, "#d96a8a") + fig(640, 1450, "#e8b830", 0.7);
    s += `<g id="${id}-six">${fig(820, 640, "#2e2a26", 0.6)}</g>`;
    s += `<text x="540" y="400" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="60" fill="#2f4a8a" filter="url(#fCrayon)">วันที่ 100 บ้านของปั้น</text>`;
    s += `<text x="300" y="1560" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#c8392b" filter="url(#fCrayon)">ครูพิม ก้อง ลุง เจ๊ ปั้น</text></g>`;
    put(L.set, s);
    if (!o.onPlate) put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }

  // ---------------- top-down map of the compound, drawn as a lit 3/4 model (v3, user 28 Oct: "ทำสวยๆหน่อยสิ … ทำให้มีมิติ"):
  // late sun from the upper left, so every block shows its south wall and throws its shadow down-right; paddies (some flooded,
  // catching the sky), a canal, tree clumps and sugar palms, asphalt roads with a few dead cars, the red-roofed school, the water
  // tower, the flag over the court, the market's tin roofs and tarps; cloud shadows drift over it all (flife .cshade).
  // ids: #id-path (route to the market; its paths inherit stroke-dashoffset from the group), #id-rings, #id-ring (sound ring at the market)
  function mapTop(L, o = {}) {
    const id = o.id || "mp", r = mk(o.seed || 314);
    const X0 = -1800, Y0 = -1800, XW = 4600, YH = 5200, n = (v) => v.toFixed(0);
    put(L.sky, `<rect x="${X0}" y="${Y0}" width="${XW}" height="${YH}" fill="#2c3522"/>`);
    // shadow of a box: footprint (x, y, w, d), height h (light from the upper left: the shadow slides by (0.8h, 0.6h))
    const shadow = (x, y, w, d, h, op = 0.34) => { const sx = h * 0.8, sy = h * 0.6;
      return `<path d="M${n(x)},${n(y)}H${n(x + w)}L${n(x + w + sx)},${n(y + sy)}V${n(y + d + sy)}H${n(x + sx)}L${n(x)},${n(y + d)}Z" fill="#0d1208" opacity="${op}"/>`; };
    // a block in 3/4 view: south wall from y+d-h to y+d, roof (gable along x: lit north slope, shaded south slope) shifted up by h
    const block = (x, y, w, d, h, roof, wall, opt = {}) => {
      const e = opt.eave ?? 8, ry = y - h, mid = ry + d / 2;
      let s = shadow(x, y, w, d, h);
      s += `<rect x="${n(x)}" y="${n(y + d - h)}" width="${n(w)}" height="${n(h)}" fill="${wall}" stroke="#1d1a15" stroke-width="3"/>`;
      s += `<rect x="${n(x)}" y="${n(y + d - h)}" width="${n(w)}" height="${n(Math.min(12, h * 0.3))}" fill="#000" opacity=".22"/>`;   // under the eave
      if (opt.windows) for (let k = 0; k < opt.windows; k++) { const wx = x + 26 + (k * (w - 52)) / opt.windows, ww = (w - 52) / opt.windows - 18;
        s += `<rect x="${n(wx)}" y="${n(y + d - h * 0.72)}" width="${n(ww)}" height="${n(h * 0.42)}" fill="#26363d" stroke="#e9e2cf" stroke-width="3"/><rect x="${n(wx + 3)}" y="${n(y + d - h * 0.72 + 3)}" width="${n(ww * 0.35)}" height="${n(h * 0.42 - 6)}" fill="#7fa3ad" opacity=".35"/>`; }
      if (opt.tin) s += `<rect x="${n(x - e)}" y="${n(ry - e)}" width="${n(w + 2 * e)}" height="${n(d + e)}" fill="url(#fMapTin)" stroke="#1d1a15" stroke-width="3"/><rect x="${n(x - e)}" y="${n(mid)}" width="${n(w + 2 * e)}" height="${n(d / 2)}" fill="#000" opacity=".2"/>`;
      else s += `<rect x="${n(x - e)}" y="${n(ry - e)}" width="${n(w + 2 * e)}" height="${n(d / 2 + e)}" fill="${roof[0]}" stroke="#1d1a15" stroke-width="3"/><rect x="${n(x - e)}" y="${n(mid)}" width="${n(w + 2 * e)}" height="${n(d / 2)}" fill="${roof[1]}" stroke="#1d1a15" stroke-width="3"/>`;
      s += `<path d="M${n(x - e)},${n(mid)}H${n(x + w + e)}" stroke="${opt.ridge || "#f2b48a"}" stroke-width="4" opacity=".8"/>`;
      if (opt.tiles) for (let k = 1; k < Math.floor(w / 26); k++) s += `<path d="M${n(x - e + k * 26)},${n(ry - e + 4)}V${n(mid - 3)}M${n(x - e + k * 26)},${n(mid + 4)}V${n(ry + d - 4)}" stroke="#000" stroke-opacity=".12" stroke-width="2"/>`;
      return s;
    };
    const tree = (x, y, R, k = 0) => { const g = ["#3b5724", "#4a6a2a", "#36521f"][k % 3];
      return `<ellipse cx="${n(x + R * 0.62)}" cy="${n(y + R * 0.58)}" rx="${n(R * 1.06)}" ry="${n(R * 0.86)}" fill="#0d1208" opacity=".36"/>
        <circle cx="${n(x)}" cy="${n(y)}" r="${n(R)}" fill="${g}" stroke="#1d2a12" stroke-width="2.5"/><circle cx="${n(x + R * 0.45)}" cy="${n(y + R * 0.2)}" r="${n(R * 0.62)}" fill="${g}"/>
        <circle cx="${n(x - R * 0.2)}" cy="${n(y - R * 0.22)}" r="${n(R * 0.7)}" fill="#5f8a34"/><circle cx="${n(x - R * 0.38)}" cy="${n(y - R * 0.42)}" r="${n(R * 0.36)}" fill="#86b04c"/>`; };
    const palm = (x, y, R) => { const fr = Array.from({ length: 9 }, (_, k) => { const a = (k / 9) * Math.PI * 2 + 0.3; return `M${n(x)},${n(y)}Q${n(x + Math.cos(a + 0.25) * R * 0.6)},${n(y + Math.sin(a + 0.25) * R * 0.6)} ${n(x + Math.cos(a) * R)},${n(y + Math.sin(a) * R)}`; }).join("");
      return `<path d="${fr}" transform="translate(${n(R * 0.9)},${n(R * 0.7)})" stroke="#0d1208" stroke-opacity=".32" stroke-width="12" fill="none" stroke-linecap="round"/><path d="${fr}" stroke="#2f4a1c" stroke-width="12" fill="none" stroke-linecap="round"/><path d="${fr}" stroke="#7aa443" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="${n(x)}" cy="${n(y)}" r="9" fill="#5b4a2a"/>`; };
    const car = (x, y, rot, col) => `<g transform="translate(${x},${y}) rotate(${rot})"><rect x="-54" y="-20" width="120" height="58" rx="16" fill="#0d1208" opacity=".38"/>
      <rect x="-62" y="-29" width="124" height="58" rx="16" fill="${col}" stroke="#1d1a15" stroke-width="3"/><rect x="-26" y="-22" width="56" height="44" rx="8" fill="#000" opacity=".25"/>
      <rect x="-30" y="-22" width="12" height="44" rx="4" fill="#9fc1c9" opacity=".8"/><rect x="26" y="-20" width="9" height="40" rx="4" fill="#9fc1c9" opacity=".55"/><path d="M-56,-23H50" stroke="#fff" stroke-opacity=".3" stroke-width="4"/></g>`;

    // ground: paddy plots on raised bunds; about one in five is flooded and holds a streak of sky
    let s = `<rect x="${X0}" y="${Y0}" width="${XW}" height="${YH}" fill="#a8996a"/>`;
    const greens = ["#7d9a48", "#87a351", "#6f8b3f", "#93ad5a", "#a2b562", "#748f43", "#8fa24e"];
    for (let y = Y0; y < Y0 + YH;) {
      const h = 210 + r() * 130;
      for (let x = X0 + (r() - 0.5) * 120; x < X0 + XW;) {
        const w = 250 + r() * 200, wet = r() < 0.2;
        s += `<rect x="${n(x + 6)}" y="${n(y + 6)}" width="${n(w - 12)}" height="${n(h - 12)}" rx="8" fill="${wet ? "url(#fMapWat)" : greens[Math.floor(r() * greens.length)]}" stroke="#56662d" stroke-opacity=".5" stroke-width="3"/>`;
        if (wet) s += `<path d="M${n(x + 30)},${n(y + h - 40)}L${n(x + w * 0.62)},${n(y + 26)}" stroke="#eef8f4" stroke-opacity=".24" stroke-width="22" stroke-linecap="round"/>`;
        x += w;
      }
      y += h;
    }
    s += `<rect x="${X0}" y="${Y0}" width="${XW}" height="${YH}" fill="url(#fMapRice)" opacity=".8"/>`;
    // the canal: dark banks, water, a broken glint
    const canal = `M${X0},2150C-900,1960 -420,2330 300,2080S1500,1720 ${X0 + XW},1960`, canal2 = `M-760,${Y0}C-640,-900 -1000,-300 -820,300S-560,1400 -420,2200`;
    s += [canal, canal2].map((d) => `<path d="${d}" stroke="#3c4a33" stroke-width="112" fill="none"/><path d="${d}" stroke="#5a8c92" stroke-width="80" fill="none"/><path d="${d}" stroke="#d6eeea" stroke-opacity=".35" stroke-width="8" fill="none" stroke-dasharray="140 90" transform="translate(-14,-12)"/>`).join("");
    // roads: shoulder, asphalt, worn edge lines, centre dashes (the road north past the junction, the road east past the market)
    const roads = `M-200,${Y0}V${Y0 + YH}M-200,1240H${X0 + XW}`;
    s += `<path d="${roads}" stroke="#c4b48a" stroke-width="156" fill="none"/><path d="${roads}" stroke="#4d4b46" stroke-width="112" fill="none"/>
      <path d="M-250,${Y0}V${Y0 + YH}M-150,${Y0}V1190M-150,1290V${Y0 + YH}M-150,1190H${X0 + XW}M-250,1290H${X0 + XW}" stroke="#d9d1b4" stroke-opacity=".45" stroke-width="4" fill="none"/>
      <path d="${roads}" stroke="#e6cd78" stroke-opacity=".8" stroke-width="7" stroke-dasharray="54 46" fill="none"/>`;
    s += `<path d="M540,1180V1240" stroke="#c4b48a" stroke-width="150"/><path d="M540,1180V1240" stroke="#8a7d5e" stroke-width="120"/>`;   // the apron in front of the gate
    // village houses and their trees
    [[1180, 330, 84, 60], [1330, 430, 70, 56], [1170, 520, 64, 50], [1500, 330, 78, 58], [-640, 820, 76, 58], [-560, 980, 66, 52], [260, 1460, 80, 60], [430, 1530, 70, 54], [1720, 1440, 84, 60], [1880, 1560, 70, 52], [-560, -260, 74, 56], [-420, -420, 66, 50]]
      .forEach(([x, y, w, d], k) => { s += block(x, y, w, d, 26, [["#b0583d", "#8a4330"], ["#7d878e", "#5f686f"], ["#a5694a", "#814f37"]][k % 3], "#d9cdb0", { eave: 5, ridge: "#f0d2b2" }); });
    // the compound: worn dirt yard, a concrete court in front of the flagpole, the path from the gate
    s += `<rect x="120" y="420" width="840" height="760" fill="#c4a873"/>`;
    s += Array.from({ length: 16 }, () => `<ellipse cx="${n(170 + r() * 740)}" cy="${n(700 + r() * 440)}" rx="${n(30 + r() * 60)}" ry="${n(14 + r() * 26)}" fill="${r() < 0.5 ? "#d6bd88" : "#8fa252"}" opacity=".55"/>`).join("");
    s += `<path d="M540,1180C540,1060 520,980 540,920" stroke="#dcc595" stroke-width="70" fill="none" stroke-linecap="round" opacity=".8"/>`;
    s += `<rect x="360" y="760" width="360" height="200" fill="#b9b5a8" stroke="#8f8b80" stroke-width="4"/><rect x="380" y="780" width="320" height="160" fill="none" stroke="#f3efe2" stroke-width="5" opacity=".75"/><path d="M540,780V940" stroke="#f3efe2" stroke-width="4" opacity=".7"/><circle cx="540" cy="860" r="34" fill="none" stroke="#f3efe2" stroke-width="4" opacity=".7"/>`;
    // trees inside the wall (a big rain tree in each corner by the gate) and along the roads, canal and plot edges
    const T = [[230, 1060, 66], [880, 1070, 58], [200, 760, 40], [930, 780, 36],
      [-90, 300, 44], [-80, 520, 36], [-320, 700, 48], [-90, 1420, 46], [-330, 1500, 40], [700, 1370, 50], [880, 1330, 38], [1100, 1360, 44], [1260, 1150, 40], [1700, 1130, 46], [1820, 1080, 36],
      [100, 2050, 54], [520, 2180, 46], [900, 1900, 50], [1300, 1840, 44], [-900, 1600, 50], [-980, 600, 46], [-700, 120, 40], [1400, 760, 40], [1600, 880, 48], [1050, 220, 44], [300, 220, 50], [650, 160, 40], [-300, 2400, 56], [1900, 2200, 50], [2100, 900, 52]];
    s += T.map(([x, y, R], k) => tree(x, y, R, k)).join("");
    s += [[-310, 1050, 46], [-300, 160, 40], [1010, 1150, 44], [1180, 1420, 40], [-760, 1300, 42], [760, 1990, 44], [1560, 1660, 40], [400, 1340, 36]].map(([x, y, R]) => palm(x, y, R)).join("");
    // the wall: shadow, south faces, then the coping; posts along the top; the gap at the gate
    const HW = 22, wall = (d) => `<path d="${d}" stroke="#0d1208" stroke-opacity=".3" stroke-width="22" fill="none" transform="translate(16,13)"/><path d="${d}" stroke="#8c8577" stroke-width="16" fill="none"/><path d="${d}" stroke="#e4ddcb" stroke-width="16" fill="none" transform="translate(0,-${HW})"/>`;
    s += wall("M430,1180H120V420H960V1180H650");
    s += `<rect x="112" y="${420 - HW}" width="856" height="${HW}" fill="#a39b8b"/><rect x="112" y="${1180 - HW}" width="318" height="${HW}" fill="#a39b8b"/><rect x="650" y="${1180 - HW}" width="318" height="${HW}" fill="#a39b8b"/>`;
    s += `<path d="M120,${420 - HW}H960M120,${1180 - HW}H430M650,${1180 - HW}H960M120,${420 - HW}V${1180 - HW}M960,${420 - HW}V${1180 - HW}" stroke="#ece6d6" stroke-width="16" fill="none"/>`;
    for (let x = 120; x <= 960; x += 70) if (x < 430 || x > 650) s += `<rect x="${x - 9}" y="${1180 - HW - 10}" width="18" height="18" fill="#cfc8b6" stroke="#5a554a" stroke-width="2"/>`;
    for (let x = 120; x <= 960; x += 70) s += `<rect x="${x - 9}" y="${420 - HW - 10}" width="18" height="18" fill="#cfc8b6" stroke="#5a554a" stroke-width="2"/>`;
    s += `<g><rect x="430" y="${1180 - HW - 6}" width="220" height="${HW + 10}" fill="#b8342a" stroke="#1d1a15" stroke-width="3"/>${Array.from({ length: 10 }, (_, k) => `<rect x="${438 + k * 21}" y="${1180 - HW - 3}" width="7" height="${HW + 4}" fill="#e2574a"/>`).join("")}</g>`;
    // the school (red tiles, cream walls, a row of windows), a tin-roofed canteen, a small toilet block
    s += block(170, 470, 520, 190, 84, ["#d06a48", "#a24a31"], "#e9dec2", { windows: 7, tiles: true });
    s += block(760, 800, 170, 120, 48, null, "#d8cfb8", { tin: true, windows: 2, ridge: "#e6ecee" });
    s += block(170, 920, 110, 70, 36, ["#4f7fa6", "#3a6286"], "#e3dbc6", { eave: 6, ridge: "#a9cbe6" });
    // the water tower: shadow first, four legs, a steel drum
    s += `<path d="M836,600L928,670M884,600L976,670" stroke="#0d1208" stroke-opacity=".3" stroke-width="7"/><ellipse cx="986" cy="690" rx="70" ry="34" fill="#0d1208" opacity=".32"/>`;
    s += `<path d="M830,605L838,475M890,605L882,475M846,590L850,480M874,590L870,480M834,560H886M838,520H882" stroke="#5c5f5e" stroke-width="7" stroke-linecap="round"/>`;
    s += `<rect x="798" y="420" width="124" height="58" fill="url(#fCan)" stroke="#1d1a15" stroke-width="3"/><ellipse cx="860" cy="478" rx="62" ry="20" fill="#7f868c" stroke="#1d1a15" stroke-width="3"/><rect x="799" y="420" width="122" height="56" fill="url(#fCan)"/>
      <ellipse cx="860" cy="420" rx="62" ry="20" fill="#c9d6dc" stroke="#1d1a15" stroke-width="3"/><ellipse cx="852" cy="416" rx="30" ry="8" fill="#fff" opacity=".45"/><path d="M806,446H914" stroke="#1d1a15" stroke-opacity=".3" stroke-width="3"/>`;
    // the flag on its plinth: the pole's long shadow, then the pole and a tattered flag
    s += `<path d="M540,904L650,986" stroke="#0d1208" stroke-opacity=".3" stroke-width="7" stroke-linecap="round"/><path d="M650,986l46,30l-8,22l-46,-30z" fill="#0d1208" opacity=".25"/>
      <rect x="506" y="886" width="68" height="30" rx="6" fill="#d8d1c0" stroke="#1d1a15" stroke-width="3"/><rect x="506" y="904" width="68" height="12" fill="#a9a190"/>
      <path d="M540,900V742" stroke="#1d1a15" stroke-width="9" stroke-linecap="round"/><path d="M540,900V742" stroke="#dfe4e6" stroke-width="5" stroke-linecap="round"/>
      <g id="${id}-mflag"><path d="M543,746h74l-6,8l8,6l-4,8l6,6l-6,8l6,6h-78z" fill="#d8392b" stroke="#1d1a15" stroke-width="2.5"/><path d="M543,755h72M543,780h72" stroke="#f3eee2" stroke-width="8"/><path d="M543,767h74" stroke="#2c3e8f" stroke-width="13"/></g>`;
    // the market: a long tin shed and a row of tarp stalls, crates and a tipped cart
    s += block(1340, 1000, 330, 96, 46, null, "#cfc6ae", { tin: true, windows: 0, ridge: "#e6ecee" });
    [["#c8392b", "#9b2b20"], ["#2f6fb8", "#235892"], ["#e08a2e", "#b86d1f"], ["#3f8f6a", "#2f6e51"]].forEach((c, k) => { s += block(1336 + k * 86, 1134, 74, 56, 30, c, "#b9ad92", { eave: 5, ridge: "#fff1dc" }); });
    s += [[1360, 1214], [1392, 1222], [1600, 1216], [1690, 1150]].map(([x, y]) => `<rect x="${x + 6}" y="${y + 5}" width="22" height="18" fill="#0d1208" opacity=".3"/><rect x="${x}" y="${y}" width="22" height="18" fill="#b98a52" stroke="#1d1a15" stroke-width="2"/>`).join("");
    s += car(1150, 1270, -6, "#8f3d2c") + car(-176, 600, 92, "#d9d6cc") + car(-230, -380, 84, "#4d7f86") + car(2050, 1262, 4, "#6b6f73");
    // the route to the market: a pale halo under a red line (both revealed by the group's stroke-dashoffset)
    s += `<g id="${id}-path" style="stroke-dashoffset:${o.path ? 0 : 1}"><path d="M540,1200V1240H1350" stroke="#fff4d6" stroke-opacity=".6" stroke-width="28" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1"/>
      <path d="M540,1200V1240H1350" stroke="#d2382a" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1"/></g>`;
    s += `<text x="1000" y="1312" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="38" fill="#fff4dc" stroke="#2b2117" stroke-width="9" paint-order="stroke">1.2 กม.</text>`;
    s += `<text x="-760" y="1880" font-family="Kanit" font-weight="700" font-size="40" fill="#f2ecd4" stroke="#2f3a1e" stroke-width="8" paint-order="stroke" opacity=".85">ทุ่งนา</text><text x="1640" y="250" font-family="Kanit" font-weight="700" font-size="40" fill="#f2ecd4" stroke="#2f3a1e" stroke-width="8" paint-order="stroke" opacity=".85">ทุ่งนา</text>`;
    // distance rings around the flag: a dark under-line so they read over the fields, labels as raised tags
    if (o.rings) s += `<g id="${id}-rings">${[[400, "400 ม."], [800, "800 ม."], [1200, "1.2 กม."]].map(([R, t], k) => `<circle cx="540" cy="900" r="${R}" fill="none" stroke="#14180e" stroke-opacity=".45" stroke-width="10"/><circle cx="540" cy="900" r="${R}" fill="none" stroke="#fff3d8" stroke-width="${k === 2 ? 5 : 4}" stroke-dasharray="${k === 2 ? "22 14" : "12 12"}" opacity=".9"/>
      <g transform="translate(${n(540 + R * 0.72)},${n(900 - R * 0.7)})"><rect x="-74" y="-24" width="148" height="56" rx="28" fill="#0d1208" opacity=".35"/><rect x="-74" y="-30" width="148" height="56" rx="28" fill="#fbf6ea" stroke="#1e1b17" stroke-width="3"/><text y="9" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="#1e1b17">${t}</text></g>`).join("")}</g>`;
    if (o.ring) s += `<g id="${id}-ring">${[0, 1, 2].map((k) => `<circle class="fring" cx="1500" cy="1250" r="${120 + k * 120}" fill="none" stroke="#ff5a3a" stroke-width="10" opacity="${0.8 - k * 0.25}"/>`).join("")}</g>`;
    // drifting cloud shadows
    s += [[200, 300, 620, 380], [1500, 1700, 700, 420], [-700, 1300, 560, 340]].map(([x, y, rx, ry]) => `<ellipse class="cshade" cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="url(#fMapCS)"/>`).join("");
    put(L.set, s);
    // the compass, and the late light: warm from the upper left, falling off to the corners (screen space)
    put(L.set, `<g transform="translate(1150,-110)"><circle r="62" fill="#0d1208" opacity=".3" transform="translate(8,8)"/><circle r="62" fill="#fbf6ea" stroke="#1e1b17" stroke-width="4"/><circle r="48" fill="none" stroke="#1e1b17" stroke-opacity=".3" stroke-width="2"/>
      <path d="M0,-50L15,0L0,50L-15,0Z" fill="#e9e2cf" stroke="#1e1b17" stroke-width="3"/><path d="M0,-50L15,0H-15Z" fill="#c8392b"/><text y="-68" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="#fbf6ea" stroke="#1e1b17" stroke-width="7" paint-order="stroke">N</text></g>`);
    put(L.light, `<rect x="0" y="0" width="1080" height="1920" fill="url(#fMapSun)"/><rect x="0" y="0" width="1080" height="1920" fill="url(#fGrid)" opacity="0"/>`);
  }
  // a pin for the map (added by the shot): a glossy drop marker at world (x, y) with a raised label; its ground shadow is #id-sh
  function pin(L, id, x, y, label, col = "#c8392b") {
    const w = Math.max(150, [...label].filter((c) => !/[ัิ-ฺ็-๎]/.test(c)).length * 19 + 74);
    const body = "M0,0C-40,-60 -60,-90 -60,-130a60,60 0 1 1 120,0c0,40 -20,70 -60,130z";
    put(L.act, `<g id="${id}-sh" opacity="0"><ellipse cx="${x + 12}" cy="${y + 4}" rx="40" ry="14" fill="#0d1208" opacity=".5"/></g>
      <g id="${id}" opacity="0"><g transform="translate(${x},${y})"><path d="${body}" fill="${col}" stroke="#1e1b17" stroke-width="5" stroke-linejoin="round"/><path d="${body}" fill="url(#fPinGloss)"/>
      <circle cy="-130" r="24" fill="#fbf6ea" stroke="#1e1b17" stroke-width="3"/><circle cy="-130" r="9" fill="${col}"/>
      <g transform="translate(0,-236)"><rect x="${-w / 2 + 6}" y="-26" width="${w}" height="62" rx="31" fill="#0d1208" opacity=".35"/><rect x="${-w / 2}" y="-34" width="${w}" height="62" rx="31" fill="#fbf6ea" stroke="#1e1b17" stroke-width="3"/>
      <circle cx="${-w / 2 + 30}" cy="-3" r="10" fill="${col}"/><text x="14" y="9" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#1e1b17">${label}</text></g></g></g>`);
  }



  // ---------------- AI-painted plates (assets/art/<name>.png, 1080×1920 at world 0,0): the scene is a picture; only what must move is drawn on top ----------------
  // o.set = plate for the set layer (parallax 1), o.far = optional plate for the far layer, o.fg = keyed foreground piece {name, x, y, s, blur}
  function plate(L, o = {}) {
    const img = (name, x = 0, y = 0, w = 1080, h = 1920, extra = "") => `<image href="assets/art/${name}.png" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="none" ${extra}/>`;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="${o.bg || "#0b0d10"}"/>`);
    if (o.far) put(L.far, img(o.far, -200, -200, 1480, 2320));
    if (o.set) put(L.set, img(o.set, o.x ?? 0, o.y ?? 0, o.w ?? 1080, o.h ?? 1920));
    if (o.fg) { const f = o.fg; put(L.fg, `<g id="${o.id || "pl"}-fg" transform="translate(${f.x},${f.y}) scale(${f.s || 1})">${img(f.name)}</g>`); if (f.blur === false) L.fg.classList.remove("fgblur"); }
    if (o.fgOff) L.fg.classList.remove("fgblur");
  }
  // iron bars drawn over a region so rigs placed behind them read as "outside the fence": x0..x1 at y0..y1, bar pitch p
  function bars(L, id, x0, x1, y0, y1, p = 30, col = "#1a1d22") {
    let s = `<g id="${id}">`;
    for (let x = x0; x < x1; x += p) s += `<rect x="${x}" y="${y0}" width="${Math.round(p * 0.32)}" height="${y1 - y0}" fill="${col}"/>`;
    s += `<rect x="${x0}" y="${y0 + (y1 - y0) * 0.12}" width="${x1 - x0}" height="${Math.round(p * 0.4)}" fill="${col}"/><rect x="${x0}" y="${y1 - (y1 - y0) * 0.2}" width="${x1 - x0}" height="${Math.round(p * 0.4)}" fill="${col}"/></g>`;
    put(L.act, s);
  }
  // the gate panel for the dusk gate plate: a sliding section of bars with its bolt, x = left edge in world space
  function gatePanel(L, id, x, y0 = 150, h = 1200, w = 470) {
    put(L.act, `<g id="${id}" transform="translate(${x},0)"><rect x="0" y="${y0}" width="${w}" height="${h}" fill="none" stroke="#2a2d31" stroke-width="22"/>
      ${Array.from({ length: Math.floor(w / 34) }, (_, b) => `<rect x="${14 + b * 34}" y="${y0 + 8}" width="12" height="${h - 16}" fill="#2f3337"/><rect x="${14 + b * 34}" y="${y0 + 8}" width="4" height="${h - 16}" fill="#4a4f55" opacity=".7"/>`).join("")}
      <rect x="0" y="${y0 + h * 0.45}" width="${w}" height="24" fill="#2a2d31"/><rect x="0" y="${y0 + h * 0.82}" width="${w}" height="24" fill="#2a2d31"/>
      <g id="${id}-bolt"><rect x="-80" y="${y0 + h * 0.47 - 8}" width="150" height="26" rx="10" fill="#8d9299" ${OUT}/><rect x="-92" y="${y0 + h * 0.47 - 22}" width="36" height="54" rx="8" fill="#5b6066" ${OUT}/></g></g>`);
  }

  // ---------------- top-down of the gate: the road and the crowd outside (top), the yard inside (bottom); figures are seen from above ----------------
  // ids: #id-gate (slides along x), #id-z0.. (the crowd, arms toward the bars), #id-in0.. (people inside)
  function gateTop(L, o = {}) {
    const id = o.id || "gtop", FY = 960, r = mk(o.seed || 77);
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2a2420"/>`);
    let s = `<rect x="-1200" y="-800" width="3500" height="${FY + 800}" fill="#5c4a63"/><rect x="-1200" y="${FY - 480}" width="3500" height="420" fill="#8a6a42"/>`;   // dusk road
    s += `<path d="M-1200,${FY - 270}H2300" stroke="#a07a4a" stroke-width="14" stroke-dasharray="90 70"/>`;
    s += `<rect x="-1200" y="${FY}" width="3500" height="2000" fill="url(#fDirt)"/>`;
    if (window.Dress) { const D = Dress;   // grain on the yard and the road, cracks and a pothole on the road, scuffs where the gate runs, weeds along the wall
      s += `<rect x="-1200" y="${FY - 480}" width="3500" height="420" fill="url(#dDirt)"/><rect x="-1200" y="${FY}" width="3500" height="2000" fill="url(#dDirt)"/><rect x="-1200" y="${FY - 480}" width="3500" height="40" fill="url(#dAO)"/>`
        + D.crack(-200, FY - 400, 160, -70, 0.5) + D.crack(1500, FY - 300, 140, -100, 0.5) + `<ellipse cx="200" cy="${FY - 160}" rx="90" ry="40" fill="#3e3020" opacity=".4"/><ellipse cx="200" cy="${FY - 164}" rx="70" ry="28" fill="#c07a60" opacity=".5"/>`
        + `<path d="M440,${FY + 40}h460" stroke="#000" stroke-opacity=".2" stroke-width="10"/>` + D.weeds(-1200, 400, FY + 36, 801, 40) + D.weeds(940, 2300, FY + 36, 803, 40) + D.pebbles(-1100, 2200, FY + 80, FY + 800, 40, 805, 8) + D.leaves(-1100, 2200, FY + 80, FY + 800, 30, 807); }
    for (let k = 0; k < 30; k++) { const x = -1100 + r() * 3400, y = FY + 60 + r() * 900; s += `<path d="M${f1(x)},${f1(y)}q6,-18 12,0q6,-14 12,0" stroke="#6f8f3e" stroke-width="4" fill="none"/>`; }
    // the fence from above: a concrete strip with square posts, the gate opening in the middle
    s += `<rect x="-1200" y="${FY - 30}" width="1644" height="60" fill="#cfc9bb" ${OUT}/><rect x="896" y="${FY - 30}" width="1404" height="60" fill="#cfc9bb" ${OUT}/>`;
    for (let x = -1100; x < 2300; x += 220) { if (x > 420 && x < 900) continue; s += `<rect x="${x - 6}" y="${FY - 42}" width="52" height="84" fill="#b3ada0" ${OUT}/>`; }
    s += `<rect x="400" y="${FY - 46}" width="44" height="92" fill="#b3ada0" ${OUT}/><rect x="896" y="${FY - 46}" width="44" height="92" fill="#b3ada0" ${OUT}/>`;
    s += `<g id="${id}-gate" transform="translate(${444 + (o.gate || 0) * 440},0)"><rect x="0" y="${FY - 16}" width="452" height="32" fill="#3a3f45" ${OUT}/>${Array.from({ length: 14 }, (_, b) => `<rect x="${12 + b * 32}" y="${FY - 22}" width="10" height="44" fill="#5b6066"/>`).join("")}</g>`;
    s += `<rect x="440" y="${FY + 16}" width="456" height="8" fill="#3a3f45"/>`;
    put(L.set, s);
    // the horde from above: shoulders, head, two arms stretched at the bars (ids -z0..; each in a plain outer group so GSAP can move it)
    const fig = (x, y, top, skin, hair, dead) => `<g transform="translate(${x},${y})"><ellipse rx="78" ry="42" fill="${top}" ${OUT}/><path d="M-60,-20L-150,70M60,-20L150,70" stroke="${INK}" stroke-width="40" stroke-linecap="round"/><path d="M-60,-20L-150,70M60,-20L150,70" stroke="${skin}" stroke-width="30" stroke-linecap="round"/>
      ${dead ? `<path d="M-150,70l-10,30M-156,66l-30,18M150,70l10,30M156,66l30,18" stroke="#1b1612" stroke-width="10" stroke-linecap="round"/><ellipse cx="20" cy="10" rx="18" ry="12" fill="#7a1414" opacity=".8"/>` : ""}<circle r="38" fill="${hair}" ${OUT}/><circle cx="-10" cy="-14" r="10" fill="${skin}" opacity=".7"/></g>`;
    const Z = [[560, FY - 150, "#2c3e6b", "#a3ae8e", "#9a948c"], [700, FY - 120, "#e6e8e2", "#b0b9a2", "#1f1a18"], [850, FY - 170, "#4f6a7a", "#98a88f", "#dfe6e2"], [430, FY - 230, "#2c3e6b", "#a3ae8e", "#9a948c"], [1000, FY - 260, "#e6e8e2", "#b0b9a2", "#1f1a18"]];
    put(L.act, Z.map(([x, y, top, skin, hair], k) => `<g id="${id}-z${k}">${fig(x, y, top, skin, hair, true)}</g>`).join(""));
    // inside: ครูพิม and ลุงหมาน shoving the panel (arms up at the gate), ก้อง sprawled on the dirt
    put(L.act, `<g id="${id}-in0">${fig(520, FY + 150, "#9fc5d8", "#ecc29c", "#2b2522", false).replace("L-150,70M60,-20L150,70", "L-110,-110M60,-20L110,-110").replace("L-150,70M60,-20L150,70", "L-110,-110M60,-20L110,-110")}</g>
      <g id="${id}-in1">${fig(760, FY + 150, "#2c3e6b", "#b9805a", "#d9b86a", false).replace("L-150,70M60,-20L150,70", "L-110,-110M60,-20L110,-110").replace("L-150,70M60,-20L150,70", "L-110,-110M60,-20L110,-110")}</g>
      <g id="${id}-in2" transform="translate(300,${FY + 330}) rotate(-70)"><ellipse rx="78" ry="42" fill="#b8463a" ${OUT}/><path d="M-60,-20L-150,40M60,-20L150,40" stroke="${INK}" stroke-width="40" stroke-linecap="round"/><path d="M-60,-20L-150,40M60,-20L150,40" stroke="#d6a27c" stroke-width="30" stroke-linecap="round"/><rect x="-40" y="30" width="80" height="150" rx="30" fill="#4a4e3a" ${OUT}/><circle r="38" fill="#231a16" ${OUT}/><path d="M-30,-30h60" stroke="#e07a4f" stroke-width="10"/></g>`);
    put(L.glow, `<rect x="-1200" y="-800" width="3500" height="${FY}" fill="#ff9a3c" opacity=".1"/>`);
  }

  // looping motion for this story's sets
  function flife(tl, scope, t0, dur) {
    const root = document.querySelector(scope);
    if (!root || root.dataset.flife) return;
    root.dataset.flife = "1";
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    q("[id$='-shim'] path").forEach((el, i) => tl.fromTo(el, { x: -30 + (i % 3) * 10 }, { x: 30, duration: 0.9 + (i % 4) * 0.2, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q("[id$='-flagc']").forEach((el) => tl.fromTo(el, { skewY: -3 }, { skewY: 3, svgOrigin: "6 -690", duration: 0.8, repeat: Math.ceil(dur / 0.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".fly").forEach((el, i) => tl.fromTo(el, { x: -8 - (i % 3) * 3, y: 6 }, { x: 10 + (i % 4) * 3, y: -12 - (i % 3) * 5, duration: 0.22 + (i % 5) * 0.05, repeat: Math.ceil(dur / 0.22), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 7) * 0.03));
    q(".lampf").forEach((el, i) => { const st = 0.16 + (i % 3) * 0.05; for (let t = 0; t < dur; t += st) { const v = 0.82 + Math.abs((Math.sin((t * 7.3 + i) * 13.1) * 43758.5) % 1) * 0.22; tl.to(el, { opacity: v, duration: st, ease: "sine.inOut" }, t0 + t); } });
    q(".mote").forEach((el, i) => { tl.fromTo(el, { x: 0, y: 0 }, { x: 40 + (i % 5) * 18, y: -60 - (i % 4) * 20, duration: 2.6 + (i % 5) * 0.5, repeat: Math.ceil(dur / 2.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, Math.max(0, t0 - (i % 7) * 0.4)); tl.fromTo(el, { opacity: 0.05 }, { opacity: 0.7, duration: 0.9 + (i % 3) * 0.3, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, Math.max(0, t0 - (i % 5) * 0.3)); });
    q(".fanspin").forEach((el) => tl.fromTo(el, { rotation: 0 }, { rotation: 360, duration: 0.9, repeat: Math.ceil(dur / 0.9), ease: "none", transformOrigin: "0px 0px", immediateRender: false }, t0));
    q(".raind").forEach((el) => tl.fromTo(el, { y: -160 }, { y: 160, duration: 0.42, repeat: Math.ceil(dur / 0.42), ease: "none", immediateRender: false }, t0));
    q(".raind2").forEach((el) => tl.fromTo(el, { y: -120 }, { y: 120, duration: 0.6, repeat: Math.ceil(dur / 0.6), ease: "none", immediateRender: false }, t0));
    q(".rsplash ellipse").forEach((el, i) => tl.fromTo(el, { opacity: 0.7, scale: 0.3 }, { opacity: 0, scale: 1.6, transformOrigin: "50% 50%", duration: 0.5, repeat: Math.ceil(dur / 0.5), ease: "power1.out", immediateRender: false }, t0 + (i % 9) * 0.06));
    q(".cowisp").forEach((el, i) => tl.fromTo(el, { y: 20, opacity: 0.16 }, { y: -120, opacity: 0, duration: 2.2 + (i % 3) * 0.4, repeat: Math.ceil(dur / 2.2), ease: "sine.out", immediateRender: false }, t0 + i * 0.5));
    q(".bird").forEach((el, i) => { tl.fromTo(el, { x: 0 }, { x: 240 + (i % 3) * 40, y: -30 + (i % 2) * 20, duration: Math.max(dur, 3) * 1.2, ease: "none", immediateRender: false }, t0); tl.fromTo(el, { scaleY: 1 }, { scaleY: -0.4, transformOrigin: "50% 50%", duration: 0.18, repeat: Math.ceil(dur / 0.18), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.05); });
    q(".cloud").forEach((el, i) => tl.fromTo(el, { x: 0 }, { x: 60 + i * 20, duration: Math.max(dur, 4) * 2, ease: "none", immediateRender: false }, t0));
    q(".canalarm").forEach((el, i) => tl.fromTo(el, { rotation: -0.6 }, { rotation: 0.6, transformOrigin: "50% 0%", duration: 1.3 + i * 0.2, repeat: Math.ceil(dur / 1.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".laundry").forEach((el) => tl.fromTo(el, { skewX: -1.5 }, { skewX: 1.5, transformOrigin: "50% 0%", duration: 1.6, repeat: Math.ceil(dur / 1.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".cshade").forEach((el, i) => tl.fromTo(el, { x: -160 }, { x: 260, y: 90, duration: Math.max(dur, 4) * 1.6, ease: "none", immediateRender: false }, Math.max(0, t0 - i * 0.7)));
    q("[id$='-mflag']").forEach((el) => tl.fromTo(el, { skewY: -4, scaleX: 1 }, { skewY: 4, scaleX: 0.9, svgOrigin: "543 760", duration: 0.55, repeat: Math.ceil(dur / 0.55), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".fring").forEach((el, i) => tl.fromTo(el, { scale: 0.3, opacity: 0.9 }, { scale: 2.2, opacity: 0, svgOrigin: "1500 1250", duration: 1.6, repeat: Math.ceil(dur / 1.6), ease: "power1.out", immediateRender: false }, t0 + i * 0.5));
  }

  // ---------------- depth and light (the v2 look): blurred foreground silhouettes, atmospheric haze between far and set, soft light sources ----------------
  // depth(L, kind): dark out-of-focus shapes in L.fg (parallax 1.5 + the fg blur) — grass | bars | post | desk | branch | shelf
  let DEPN = 0;
  function depth(L, kind, o = {}) {
    const op = Math.min(1, (o.op ?? 0.92) + 0.08), r = mk(o.seed || 7 + DEPN++);
    // v2 (user 28 Oct: the black blurred shapes "looked like smudges"): real things in colour — grass with lit tips and seed heads,
    // a stained concrete post with a vine, iron bars with a highlight, a wooden desk edge, a leafy branch, a rusty shelf upright —
    // still out of focus (fgblur) and darker than the set, so they frame the shot instead of blotting it. A dark o.col = night tones.
    const lum = (h) => { const v = parseInt((h || "#06080a").slice(1), 16); return ((v >> 16) & 255) * 0.3 + ((v >> 8) & 255) * 0.59 + (v & 255) * 0.11; };
    const nightT = o.col ? lum(o.col) < 14 : false, warm = o.col && lum(o.col) >= 14;
    const G3 = nightT ? ["#0c1218", "#141e26", "#1e2a34"] : warm ? ["#1e2a14", "#2e4220", "#4a6430"] : ["#22341a", "#3a5a26", "#5e8a3a"];
    const CON = nightT ? ["#1a1e24", "#262b32", "#323842"] : ["#4a463e", "#6a6458", "#8a8476"];
    const D = {
      grass: () => { let g = `<path d="M-1800,1800q500,-60 1000,0t1000,0t1000,0t1000,0t1000,0V2600H-1800z" fill="${G3[0]}"/>`;
        for (let k = 0; k < 34; k++) { const x = (k < 17 ? -140 : 740) + r() * 460, h = 150 + r() * 280, w = 16 + r() * 22, c = G3[k % 3], lean = (r() - 0.5) * w * 2;
          g += `<path d="M${f1(x)},2000q${f1(-w + lean * 0.3)},${f1(-h * 0.5)} ${f1(w * 0.3 + lean)},${f1(-h)}q${f1(w)},${f1(h * 0.45)} ${f1(w * 1.6)},${f1(h)}z" fill="${c}"/>`;
          if (k % 5 === 0) g += `<path d="M${f1(x + w * 0.3 + lean)},${f1(2000 - h)}q6,-30 2,-60" stroke="${G3[2]}" stroke-width="5" fill="none"/><ellipse cx="${f1(x + w * 0.3 + lean + 2)}" cy="${f1(2000 - h - 70)}" rx="8" ry="20" fill="${nightT ? "#2a2e30" : "#b8a86a"}"/>`; }
        return g; },
      bars: () => [-60, 110, 280].map((x, k) => `<rect x="${x}" y="-400" width="${70 + k * 10}" height="2800" rx="20" fill="${nightT ? "#14181c" : "#2c3035"}"/><rect x="${x + 10}" y="-400" width="14" height="2800" fill="${nightT ? "#262c34" : "#5a6066"}"/><rect x="${x + 40 + k * 8}" y="-400" width="22" height="2800" fill="#000" opacity=".3"/>`).join("")
        + `<rect x="-1200" y="700" width="1570" height="60" fill="${nightT ? "#14181c" : "#2c3035"}"/><rect x="-1200" y="704" width="1570" height="10" fill="${nightT ? "#262c34" : "#5a6066"}"/><path d="M60,760l-20,180M210,760l-12,120" stroke="#7a3a1a" stroke-width="18" opacity=".45"/>`,
      post: () => { const x = o.x ?? -80, w = o.w ?? 220;
        return `<rect x="${x}" y="-400" width="${w}" height="2800" fill="${CON[1]}"/><rect x="${x}" y="-400" width="${w}" height="2800" fill="url(#dConc)"/><rect x="${x + w * 0.62}" y="-400" width="${w * 0.38}" height="2800" fill="${CON[0]}"/><rect x="${x + 8}" y="-400" width="${w * 0.08}" height="2800" fill="${CON[2]}"/>
          <rect x="${x + w * 0.2}" y="200" width="${w * 0.3}" height="900" fill="url(#dStreak)"/><path d="M${x + w * 0.5},2400C${x + w * 0.2},1900 ${x + w * 0.8},1500 ${x + w * 0.4},1000S${x + w * 0.7},400 ${x + w * 0.45},0" stroke="${G3[1]}" stroke-width="10" fill="none"/>${[2100, 1800, 1500, 1200, 900, 600, 300].map((y, k) => `<ellipse cx="${x + w * (k % 2 ? 0.62 : 0.3)}" cy="${y}" rx="44" ry="22" fill="${G3[k % 2 ? 2 : 1]}" transform="rotate(${k % 2 ? -30 : 30} ${x + w * (k % 2 ? 0.62 : 0.3)} ${y})"/>`).join("")}`; },
      desk: () => `<path d="M-1800,1666L2900,1336V2700H-1800z" fill="${nightT ? "#1a1410" : "#4a3220"}"/><path d="M-1800,1666L2900,1336V2700H-1800z" fill="url(#dPlankH)" opacity=".5"/><path d="M-1800,1666L2900,1336l0,40L-1800,1706z" fill="${nightT ? "#2a2018" : "#7a5434"}"/><path d="M-1800,1668L2900,1338" stroke="#fff" stroke-opacity=".15" stroke-width="5"/>`,
      branch: () => { let b = `<path d="M-200,-200C100,-60 380,40 560,0" stroke="${nightT ? "#14100c" : "#3a2a1a"}" stroke-width="34" fill="none" stroke-linecap="round"/><path d="M200,-40C260,-120 320,-160 400,-170M380,20c40,40 60,90 50,140" stroke="${nightT ? "#14100c" : "#3a2a1a"}" stroke-width="14" fill="none" stroke-linecap="round"/>`;
        for (let k = 0; k < 22; k++) { const t = r(), x = -160 + t * 700, y = -150 + t * 160 + (r() - 0.5) * 180, a = -40 + r() * 80, c = G3[k % 3];
          b += `<path d="M${f1(x)},${f1(y)}q40,-26 90,0q-50,26 -90,0z" fill="${c}" transform="rotate(${f1(a)} ${f1(x)} ${f1(y)})"/><path d="M${f1(x)},${f1(y)}h86" stroke="${G3[0]}" stroke-width="2" transform="rotate(${f1(a)} ${f1(x)} ${f1(y)})"/>`; }
        return b; },
      shelf: () => `<rect x="-300" y="-400" width="420" height="2800" fill="${nightT ? "#1a1e24" : "#3e444a"}"/><rect x="-290" y="-400" width="20" height="2800" fill="${nightT ? "#2a2e36" : "#6a7076"}"/>${[900, 1500].map((y) => `<rect x="-300" y="${y}" width="700" height="50" fill="${nightT ? "#1a1e24" : "#3e444a"}"/><rect x="-300" y="${y}" width="700" height="8" fill="${nightT ? "#2a2e36" : "#6a7076"}"/>`).join("")}<rect x="-200" y="300" width="80" height="400" fill="url(#dRust)"/>`,
    };
    // shapes are drawn in screen coordinates for the shot's first camera key (o.cam = {x, y, s}): map them back through the fg parallax (1.5)
    const c = o.cam || { x: 0, y: 0, s: 1 }, ls = 1 + (c.s - 1) * 1.5;
    put(L.fg, `<g opacity="${op}" transform="translate(${f1(540 + c.x * 1.5)},${f1(960 + c.y * 1.5)}) scale(${(1 / ls).toFixed(4)}) translate(-540,-960)">${(D[kind] || D.grass)()}</g>`);
  }
  // haze(L, y, h, col, op): a soft band of atmosphere in the mid layer (parallax .6) so the far ground sits behind the set
  function haze(L, y = 1000, h = 500, col = "#cfd8d4", op = 0.3) {
    op *= 0.5;
    const id = `hz${DEPN++}`;
    put(L.mid, `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity="0"/><stop offset=".55" stop-color="${col}" stop-opacity="${op}"/><stop offset="1" stop-color="${col}" stop-opacity="${op * 0.3}"/></linearGradient><rect x="-1200" y="${y - h}" width="3500" height="${h + 200}" fill="url(#${id})"/>`);
  }
  // light(L, x, y, r, col, op): a soft light source above the darkness (glow layer): core + wide bloom; cls = "lampf" flickers (flife)
  // light(L, x, y, R, col, op, cls): a light SOURCE the professional way — a tight bright core with a short halo at the lamp itself,
  // never a frame-wide wash (the user: "แสงบังจนดูไม่รู้เรื่อง"); the floor gets its light from cone() instead
  function light(L, x, y, R = 500, col = "#ffd58a", op = 0.5, cls = "") {
    (L._lights || (L._lights = [])).push({ x, y, R, col, op });   // the engine aims cast shadows and rim light from these
    if (!Fence.GLOW) return;
    const id = `lt${DEPN++}`;
    put(L.glow, `<radialGradient id="${id}"><stop offset="0" stop-color="#fff6e0" stop-opacity="${Math.min(1, op * 1.1)}"/><stop offset=".12" stop-color="${col}" stop-opacity="${op * 0.55}"/><stop offset=".3" stop-color="${col}" stop-opacity="${op * 0.14}"/><stop offset=".6" stop-color="${col}" stop-opacity="${op * 0.03}"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></radialGradient>
      <g class="${cls}"><circle cx="${x}" cy="${y}" r="${R * 0.5}" fill="url(#${id})"/></g>`);
  }
  // cone(L, x, y, w, h, col, op): the light a lamp at (x, y) throws — a faint narrow beam and a soft pool on the floor at y + h (the pool sits
  // under the actors in the set layer, so people stand IN the light instead of behind a glow)
  function cone(L, x, y, w = 600, h = 900, col = "#ffd58a", op = 0.35, cls = "lampf") {
    if (!Fence.GLOW) return;
    const id = `cn${DEPN++}`;
    put(L.glow, `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity="${op * 0.32}"/><stop offset=".5" stop-color="${col}" stop-opacity="${op * 0.08}"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient>
      <path class="${cls}" d="M${x - 26},${y}L${x + 26},${y}L${x + w * 0.42},${y + h}L${x - w * 0.42},${y + h}Z" fill="url(#${id})"/>`);
    put(L.set, `<radialGradient id="${id}p"><stop offset="0" stop-color="${col}" stop-opacity="${op * 0.5}"/><stop offset=".55" stop-color="${col}" stop-opacity="${op * 0.18}"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></radialGradient>
      <ellipse class="${cls}" cx="${x}" cy="${y + h}" rx="${w * 0.62}" ry="${w * 0.15}" fill="url(#${id}p)"/>`);
  }
  // rays(L, x0, x1, y0, y1, n, col): slanted light shafts (glow layer)
  function rays(L, x0 = -600, x1 = 400, y0 = 300, y1 = 1500, n = 4, col = "#ffd8a0", op = 0.5) {
    if (!Fence.GLOW) return;   // thin, faint shafts: a hint of dust in the air, not a wall of yellow
    const id = `ry${DEPN++}`;
    put(L.glow, `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity="${op * 0.3}"/><stop offset=".7" stop-color="${col}" stop-opacity="${op * 0.06}"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient>
      ${Array.from({ length: n }, (_, k) => { const w = (x1 - x0) / n, x = x0 + k * w; return `<path d="M${x},${y0}h${w * 0.2}L${x + w * 0.2 + (x1 - x0) * 0.6},${y1}h${-w * 0.42}Z" fill="url(#${id})"/>`; }).join("")}`);
  }

  // clouds(L, seed): soft cloud banks high above the set (mid layer, parallax .6) for a camera that starts in the sky and drops through them
  function clouds(L, seed = 5) {
    const r = mk(seed); let s = "";
    for (let k = 0; k < 14; k++) { const x = -900 + r() * 2900, y = -1500 + r() * 1300, w = 260 + r() * 420, op = (0.75 + r() * 0.25).toFixed(2);
      s += `<g opacity="${op}">${[[0, 0, 1], [-0.4, 0.15, 0.7], [0.42, 0.12, 0.75], [0.1, -0.22, 0.6]].map(([dx, dy, k2]) => `<ellipse cx="${f1(x + dx * w)}" cy="${f1(y + dy * w * 0.35)}" rx="${f1(w * 0.55 * k2)}" ry="${f1(w * 0.22 * k2)}" fill="#f1f4f6"/>`).join("")}<ellipse cx="${f1(x)}" cy="${f1(y + w * 0.12)}" rx="${f1(w * 0.6)}" ry="${f1(w * 0.14)}" fill="#c9d3da" opacity=".6"/></g>`; }
    put(L.mid, s);
    put(L.far, `<rect x="-1200" y="-2200" width="3500" height="1500" fill="#dfe8ee" opacity=".35"/>`);
  }

  Object.assign(Sets, { schoolYard, classroom, market, canClose, fieldRoad, gateClose, tankClose, radioClose, drawing, mapTop, gateTop, plate });
  window.Fence = { chalk, pin, flife, paddies, bars, gatePanel, depth, haze, light, cone, rays, clouds, GLOW: true };
  // ======================================================================================================
  // EP.2 "เครื่องปั่นไฟ": the temple fair at noon, the generator POV, the classroom with the generator / fan / bulb /
  // exhaust, the hill with the answering light, น้องปั้น's second drawing
  // ======================================================================================================
  const FAN = (id, x, y) => `<g id="${id}-fan" transform="translate(${x},${y})"><path d="M0,-260V-40" stroke="#5b6066" stroke-width="14"/><g class="fanspin" style="transform-origin:0px 0px">${[0, 1, 2].map((k) => `<path d="M0,0L-30,-26L-230,-18L-220,22L-26,26Z" fill="#dfe3e6" ${OUT} transform="rotate(${k * 120})"/>`).join("")}</g><circle r="34" fill="#9aa0a6" ${OUT}/><circle r="12" fill="#5b6066"/></g>`;
  const BULB = (id, x, y) => `<g id="${id}-bulbbody" transform="translate(${x},${y})"><path d="M0,-200V-70" stroke="#2a2420" stroke-width="5"/><rect x="-18" y="-70" width="36" height="30" rx="4" fill="#9aa0a6" ${OUT}/><circle r="40" cy="0" fill="#f4ecd8" ${OUT}/><path d="M-10,0q10,-24 20,0" stroke="#9aa0a6" stroke-width="3" fill="none"/></g>`;

  // ---------------- the abandoned temple fair at noon: a small ferris wheel (#id-wheel spins), torn striped tents, a stage with speakers, the generator on a cart (#id-cart) ----------------
  function fair(L, o = {}) {
    const id = o.id || "fa", r = mk(o.seed || 83), t = o.time || "noon", G = 1500;
    sky(L, t); sunMoon(L, t, 300, 420);
    put(L.far, paddies(r, t, 1040));
    const R = 330, cx = 1320, cy = 640;
    let w = `<g transform="translate(${cx},${cy})"><path d="M-220,${R + 340}L0,0L220,${R + 340}Z" fill="none" stroke="#5b6066" stroke-width="18"/><path d="M-300,${R + 340}h600" stroke="#5b6066" stroke-width="22"/></g>`;
    w += `<g id="${id}-wheel" transform="translate(${cx},${cy})"><circle r="${R}" fill="none" stroke="#c8392b" stroke-width="14"/><circle r="${R - 70}" fill="none" stroke="#c8392b" stroke-width="6" opacity=".7"/>`;
    for (let k = 0; k < 8; k++) { const a = (k * Math.PI) / 4; w += `<path d="M0,0L${f1(Math.cos(a) * R)},${f1(Math.sin(a) * R)}" stroke="#5b6066" stroke-width="8"/><g transform="translate(${f1(Math.cos(a) * R)},${f1(Math.sin(a) * R)})"><rect x="-44" y="-8" width="88" height="68" rx="12" fill="${["#f2c55c", "#9fc5d8", "#d96a8a", "#6f8f58"][k % 4]}" ${OUT}/></g>`; }
    w += `<circle r="26" fill="#f4ecd8" ${OUT}/></g>`;
    put(L.mid, w);
    let s = `<rect x="-1200" y="${G - 40}" width="3500" height="1400" fill="url(#fDirt)"/>`;
    const fd = o.dress !== false && window.Dress ? fairDress(L, id, o, t) : null;
    if (fd) s += fd.floor + fd.back;
    const tent = (x, col) => `<g transform="translate(${x},${G})"><path d="M-40,0V-420M300,0V-420" stroke="#8a6a42" stroke-width="12"/><path d="M-130,-420L130,-570L390,-420Z" fill="${col}" ${OUT}/>${[0, 1, 2, 3].map((k) => `<path d="M${-110 + k * 130},-420L${-45 + k * 130},-560" stroke="#f4ecd8" stroke-width="24" opacity=".5"/>`).join("")}<path d="M-130,-420l40,70l30,-70l50,100l40,-100l60,80l30,-80l60,50l-20,-50" fill="none" stroke="${INK}" stroke-width="4"/><path d="M-110,-430q30,70 0,140q40,-40 25,-140z" fill="${col}" opacity=".85" ${OUT}/></g>`;
    s += tent(-760, "#d96a8a") + tent(-230, "#f2c55c") + tent(1760, "#6f8f58");
    s += `<g transform="translate(700,${G})"><path d="M-430,-120V-640M430,-120V-640" stroke="#8a6a42" stroke-width="14"/>${fd ? `<ellipse cx="40" cy="6" rx="470" ry="22" fill="#0b0d08" opacity=".3"/>` : ""}<rect x="-400" y="-120" width="800" height="120" fill="#6b4a2e" ${OUT}/>${fd ? fd.stage : ""}<rect x="-360" y="-470" width="110" height="350" fill="#2a2420" ${OUT}/><circle cx="-305" cy="-390" r="30" fill="#1a1512" stroke="#8d9299" stroke-width="6"/><circle cx="-305" cy="-250" r="46" fill="#1a1512" stroke="#8d9299" stroke-width="6"/>
      <g transform="rotate(7 0 -560)"><rect x="-400" y="-620" width="800" height="120" fill="#c8392b" opacity=".85" ${OUT}/><text x="0" y="-532" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#f4ecd8">งานวัดประจำปี</text></g></g>`;
    for (let k = 0; k < 14; k++) { const x = -1100 + r() * 3300, y = G + 60 + r() * 700; s += `<path d="M${f1(x)},${f1(y)}l${f1(20 + r() * 30)},${f1(-6 + r() * 12)}" stroke="#d9d4c8" stroke-width="8" stroke-linecap="round" opacity=".6"/>`; }
    if (fd) s += fd.front;
    put(L.set, s);
    put(L.act, `<g id="${id}-cart" transform="translate(${o.cartX ?? 260},${G})"><rect x="-180" y="-150" width="360" height="30" fill="#5b6066" ${OUT}/><path d="M170,-150L330,-270" stroke="#5b6066" stroke-width="14" stroke-linecap="round"/><circle cx="-110" cy="-50" r="50" fill="#2a2420" stroke="#8d9299" stroke-width="10"/><circle cx="110" cy="-50" r="50" fill="#2a2420" stroke="#8d9299" stroke-width="10"/>${Sets.props.generator(`${id}-gen`, 0, -150, 0.72, false)}</g>`);
    if (t === "noon") put(L.glow, `<rect x="-1200" y="900" width="3500" height="400" fill="url(#zHaze)" opacity=".8"/>`);
    put(L.glow, `<g id="${id}-shim">${[0, 1, 2].map((i) => `<path d="M${-400 + i * 700},1380q200,-30 400,0t400,0" stroke="#fff6dc" stroke-width="6" fill="none" opacity=".25"/>`).join("")}</g>`);
  }

  // ---------------- set dressing for the temple fair (EP.2) ----------------
  // the temple's ordination hall behind the tents (tiered red-and-gold roof, white walls), flag bunting and dead fairy lights
  // strung between poles, a balloon-dart stall with burst balloons and dusty prize bears, a cotton-candy cart, folding tables and
  // plastic chairs knocked over, cups and paper litter, a fallen banner, dry grass and dirt grain
  function fairDress(L, id, o, t) {
    const D = Dress, r = mk((o.seed || 83) + 503), G = 1500;
    put(L.mid, `<g transform="translate(60,${G - 120})"><rect x="-260" y="-300" width="520" height="300" fill="#f2ede0" stroke="${INK}" stroke-width="4"/><rect x="-260" y="-300" width="520" height="300" fill="url(#dConc)"/>
      ${[-180, -60, 60, 180].map((x) => `<rect x="${x - 26}" y="-250" width="52" height="150" fill="#3a2a22" stroke="${INK}" stroke-width="3"/><path d="M${x - 26},-250l26,-30l26,30" fill="#c9a24a" stroke="${INK}" stroke-width="2"/>`).join("")}
      ${[[0, -300, 620, 90], [0, -380, 500, 90], [0, -460, 360, 90]].map(([x, y, w, h]) => `<path d="M${-w / 2},${y}L${-w / 2 + 40},${y - h * 0.4}L0,${y - h}L${w / 2 - 40},${y - h * 0.4}L${w / 2},${y}Z" fill="#b8342a" stroke="${INK}" stroke-width="4"/><path d="M${-w / 2},${y}L0,${y - h}L${w / 2},${y}" stroke="#e0b04a" stroke-width="6" fill="none"/><path d="M${-w / 2 + 2},${y}q-16,-26 -4,-48M${w / 2 - 2},${y}q16,-26 4,-48" stroke="#e0b04a" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("")}
      <path d="M0,-560v-80" stroke="#e0b04a" stroke-width="8"/><circle cy="-646" r="10" fill="#e0b04a"/></g>`);
    // floor: dirt grain, the dark band where the ground meets the stalls, trampled paths, tyre tracks, the noon shadows of tents
    // and poles (short, falling right of the sun), dry tufts and pebbles
    let floor = `<rect x="-1200" y="${G - 40}" width="3500" height="1400" fill="url(#dDirt)"/><rect x="-1200" y="${G - 40}" width="3500" height="90" fill="url(#dAO)" opacity=".7"/>`;
    floor += `<path d="M-300,${G + 1400}Q200,${G + 500} 500,${G + 60}L900,${G + 60}Q760,${G + 520} 900,${G + 1400}Z" fill="#e2c48e" opacity=".32"/>` + D.tracks(-900, G + 1300, -200, G + 500, 300, G + 80, 110, 0.12);
    floor += [[-760, 330], [-230, 330], [1760, 330]].map(([x, w]) => `<ellipse cx="${x + 170}" cy="${G + 14}" rx="${w}" ry="30" fill="#0b0d08" opacity=".2"/>`).join("");
    floor += [-1000, -380, 360, 1100, 1900].map((x) => `<path d="M${x},${G}l140,24" stroke="#0b0d08" stroke-opacity=".22" stroke-width="14" stroke-linecap="round"/>`).join("");
    floor += D.tufts(-1100, 2200, G + 20, G + 700, 44, 509, 34, true) + D.pebbles(-1100, 2200, G + 20, G + 760, 40, 511, 8) + D.leaves(-1000, 2100, G + 60, G + 760, 26, 513);
    // the stage front: planks, a pleated red-and-white skirt with a scalloped valance, a dusty step box
    const stage = `<rect x="-400" y="-120" width="800" height="120" fill="url(#dPlankH)"/><path d="M-400,-118H400" stroke="#e8c89a" stroke-opacity=".5" stroke-width="4"/>
      ${Array.from({ length: 16 }, (_, k) => `<rect x="${-400 + k * 50}" y="-96" width="50" height="96" fill="${k % 2 ? "#f4ecd8" : "#c8392b"}"/><path d="M${-400 + k * 50 + 46},-96V0" stroke="#000" stroke-opacity=".18" stroke-width="5"/>`).join("")}
      <path d="M-400,-96${Array.from({ length: 16 }, () => "q25,26 50,0").join("")}" fill="#e0b04a" stroke="${INK}" stroke-width="3"/><rect x="-400" y="-96" width="800" height="96" fill="url(#dGrime)" opacity=".7"/><rect x="-400" y="-120" width="800" height="120" fill="none" stroke="${INK}" stroke-width="4"/>
      <g transform="translate(250,0)"><rect x="0" y="-56" width="120" height="56" fill="#8a6a42" stroke="${INK}" stroke-width="3"/><rect x="0" y="-56" width="120" height="56" fill="url(#dPlankH)"/></g>`;
    let s = "";
    // bunting and dead fairy lights between poles
    const poles = [-1000, -380, 360, 1100, 1900];
    s += poles.map((x) => `<path d="M${x},${G}V${G - 760}" stroke="#7a5a3a" stroke-width="10"/>`).join("");
    for (let k = 0; k + 1 < poles.length; k++) { const a = poles[k], b = poles[k + 1], y0 = G - 740, sag = 90;
      s += `<path d="M${a},${y0}Q${(a + b) / 2},${y0 + sag * 2} ${b},${y0}" stroke="#d9d4c8" stroke-width="2" fill="none"/>`;
      for (let j = 1; j < 12; j++) { const u = j / 12, x = a + (b - a) * u, y = y0 + 4 * sag * u * (1 - u), c = ["#c8392b", "#e8b830", "#2f6fb8", "#4f8a55", "#d96a8a"][(j + k) % 5];
        s += `<path d="M${f1(x - 14)},${f1(y)}h28l-14,34z" fill="${c}" opacity=".85" stroke="${INK}" stroke-width="1.5" transform="rotate(${f1((r() - 0.5) * 16)} ${f1(x)} ${f1(y)})"/>`; }
      s += `<path d="M${a},${y0 + 60}Q${(a + b) / 2},${y0 + 60 + sag * 1.4} ${b},${y0 + 60}" stroke="#2a2a2a" stroke-width="2" fill="none"/>${Array.from({ length: 8 }, (_, j) => { const u = (j + 0.5) / 8, x = a + (b - a) * u, y = y0 + 60 + 2.8 * sag * u * (1 - u); return `<circle cx="${f1(x)}" cy="${f1(y + 8)}" r="6" fill="${["#f2c55c", "#e07a6a", "#7ab0d8"][j % 3]}" opacity=".6" stroke="${INK}" stroke-width="1.5"/>`; }).join("")}`; }
    // the balloon-dart stall: a board of burst balloons, a shelf of dusty bears
    s += D.at(-1180, G, 1, `<rect x="-20" y="-420" width="380" height="420" fill="#8a5a3a" stroke="${INK}" stroke-width="4"/><rect x="0" y="-400" width="340" height="230" fill="#2f4a6a"/>${Array.from({ length: 15 }, (_, j) => { const x = 30 + (j % 5) * 64, y = -370 + Math.floor(j / 5) * 70, c = ["#c8392b", "#e8b830", "#4f8a55", "#d96a8a", "#2f6fb8"][j % 5]; return j % 3 === 1 ? `<path d="M${x - 10},${y + 4}l8,-6l6,10l8,-8" stroke="${c}" stroke-width="5" fill="none"/>` : `<ellipse cx="${x}" cy="${y}" rx="18" ry="22" fill="${c}" opacity=".8" stroke="${INK}" stroke-width="2"/><path d="M${x},${y + 22}v12" stroke="#d9d4c8" stroke-width="2"/>`; }).join("")}
      <rect x="0" y="-160" width="340" height="16" fill="#6b4a2e"/>${[40, 120, 200, 280].map((x, j) => `<g transform="translate(${x},-160)"><ellipse cy="-30" rx="26" ry="30" fill="${["#c9a06c", "#e8b8c8", "#9fc5d8", "#e8dcc6"][j]}" stroke="${INK}" stroke-width="2"/><circle cy="-70" r="20" fill="${["#c9a06c", "#e8b8c8", "#9fc5d8", "#e8dcc6"][j]}" stroke="${INK}" stroke-width="2"/><circle cx="-14" cy="-86" r="7" fill="${["#c9a06c", "#e8b8c8", "#9fc5d8", "#e8dcc6"][j]}" stroke="${INK}" stroke-width="2"/><circle cx="14" cy="-86" r="7" fill="${["#c9a06c", "#e8b8c8", "#9fc5d8", "#e8dcc6"][j]}" stroke="${INK}" stroke-width="2"/></g>`).join("")}<rect x="-20" y="-420" width="380" height="420" fill="url(#dGrime)"/>`);
    // a cotton-candy cart, knocked-over tables and chairs, litter, the fallen banner
    s += D.at(1500, G + 40, 1, `<rect x="-120" y="-200" width="240" height="150" fill="#f2ede0" stroke="${INK}" stroke-width="3"/><path d="M-130,-200H130L110,-260H-110Z" fill="#d96a8a" stroke="${INK}" stroke-width="3"/><ellipse cx="-50" cy="-300" rx="40" ry="44" fill="#f2c2d6" stroke="${INK}" stroke-width="2"/><ellipse cx="40" cy="-296" rx="36" ry="40" fill="#c2dcf2" stroke="${INK}" stroke-width="2"/><path d="M-50,-256v56M40,-256v56" stroke="#e8dcc6" stroke-width="4"/>
      <circle cx="-80" cy="-30" r="30" fill="none" stroke="#3a3a3a" stroke-width="8"/><circle cx="80" cy="-30" r="30" fill="none" stroke="#3a3a3a" stroke-width="8"/><text x="0" y="-110" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="#d96a8a">สายไหม</text>`);
    const back = s; s = "";
    s += D.chair(-560, G + 150, 0.9, "#c8392b", 84) + D.chair(1000, G + 240, 0.9, "#2f6fb8") + D.chair(1160, G + 200, 0.86, "#e8e4da", -78);
    s += D.at(-120, G + 300, 1, `<path d="M-200,0L200,-20L210,0L-190,20Z" fill="#e8e4da" stroke="${INK}" stroke-width="3"/><path d="M-160,14L-150,90M160,-6L180,70" stroke="#5b6066" stroke-width="7"/>`, 8);
    s += [[200, G + 420], [700, G + 520], [-700, G + 480], [1300, G + 600]].map(([x, y], j) => D.at(x, y, 1, j % 2 ? `<path d="M-14,0l4,-26h20l4,26z" fill="#f4f4ee" stroke="${INK}" stroke-width="2" transform="rotate(80)"/>` : `<path d="M-24,0q4,-14 24,-12q20,4 24,12q-24,8 -48,0z" fill="#e8e4da" opacity=".9" stroke="${INK}" stroke-width="1.5"/>`)).join("");
    // closer litter: paper cups, a flip-flop, burst balloon skins, ticket stubs, a plastic bag, a skewer stick
    s += [[-380, G + 760, 0], [420, G + 880, 1], [980, G + 820, 2], [-860, G + 920, 3], [160, G + 1060, 4], [1500, G + 960, 5], [-150, G + 640, 2], [1220, G + 700, 0]].map(([x, y, k]) => D.at(x, y, 1.2, [
      `<ellipse cx="6" cy="4" rx="34" ry="7" fill="#0b0d08" opacity=".2"/><path d="M-26,-10l52,-6l-4,22l-44,4z" fill="#f4f4ee" stroke="${INK}" stroke-width="2"/><ellipse cx="-26" cy="0" rx="5" ry="10" fill="#e8e4da" stroke="${INK}" stroke-width="2"/><path d="M-10,-12l2,22" stroke="#c8392b" stroke-width="4"/>`,
      `<ellipse cx="4" cy="3" rx="40" ry="8" fill="#0b0d08" opacity=".2"/><path d="M-40,0q0,-16 34,-16h20q24,0 26,12q0,8 -26,8z" fill="#2f6fb8" stroke="${INK}" stroke-width="2"/><path d="M-6,-14q8,10 22,10" stroke="#e8e4da" stroke-width="4" fill="none"/>`,
      `<path d="M-14,0q-6,-14 6,-18q14,4 8,18q-6,6 -14,0z" fill="#c8392b" opacity=".85" stroke="${INK}" stroke-width="1.5"/><path d="M0,0q10,6 22,2" stroke="#d9d4c8" stroke-width="2" fill="none"/>`,
      `<rect x="-16" y="-8" width="32" height="16" fill="#e8b830" stroke="${INK}" stroke-width="1.5" transform="rotate(-12)"/><rect x="10" y="-2" width="28" height="14" fill="#d96a8a" stroke="${INK}" stroke-width="1.5" transform="rotate(20)"/>`,
      `<ellipse cx="4" cy="4" rx="46" ry="9" fill="#0b0d08" opacity=".18"/><path d="M-40,0q-6,-30 20,-34q10,-12 22,0q30,4 22,34q-30,8 -64,0z" fill="#f4f4ee" fill-opacity=".75" stroke="${INK}" stroke-width="2"/><path d="M-20,-20q10,8 24,2" stroke="#fff" stroke-width="4" fill="none" opacity=".7"/>`,
      `<path d="M-40,0l80,-10" stroke="#d9b98a" stroke-width="4" stroke-linecap="round"/><ellipse cx="-30" cy="-2" rx="10" ry="6" fill="#f2c2d6" opacity=".8"/>`][k])).join("");
    return { floor, back, stage, front: s };
  }

  // ---------------- first person at the generator: the red machine filling the frame, our hand on the starter handle (#id-hand, cord #id-cord), the bulb above (#id-bulb), the fan ----------------
  function genClose(L, o = {}) {
    const id = o.id || "gp";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#0e0f12"/>`);
    put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2a2620"/><rect x="-1200" y="1150" width="3500" height="40" fill="#5a4630"/><rect x="-1200" y="1190" width="3500" height="1300" fill="#3a2e20"/>`);
    put(L.mid, `<rect x="-300" y="260" width="1680" height="620" rx="10" fill="#1f3f31" opacity=".85" ${OUT}/><rect x="-1000" y="300" width="300" height="520" fill="#0b1020" ${OUT}/>`);
    if (o.dress !== false && window.Dress) { put(L.far, `<rect x="-1200" y="-800" width="3500" height="1950" fill="url(#dConc)" opacity=".6"/><rect x="-1200" y="900" width="3500" height="250" fill="url(#dGrime)"/><rect x="-1200" y="1190" width="3500" height="1300" fill="url(#dPlankH)" opacity=".7"/><rect x="-1200" y="1190" width="3500" height="60" fill="url(#dAO)"/>`);
      put(L.mid, `<rect x="-320" y="240" width="1720" height="660" rx="12" fill="none" stroke="#6b4a2e" stroke-width="24"/><rect x="-300" y="880" width="1680" height="22" fill="#7a5a3e" stroke="${INK}" stroke-width="3"/><path d="M-200,400q300,-30 700,10M-150,520q400,20 900,-6M900,360q200,20 380,0" stroke="#e8f2ec" stroke-width="16" opacity=".08" fill="none" stroke-linecap="round"/><path d="M-100,600h300M-100,660h240M1000,700h220" stroke="#e8f2ec" stroke-width="5" opacity=".18"/><rect x="200" y="868" width="40" height="12" fill="#f4ecd8"/><rect x="260" y="870" width="30" height="10" fill="#f2c2d6"/>`); }
    put(L.set, `${BULB(id, 540, 170)}${o.fan ? FAN(id, 540, 60) : ""}${Sets.props.generator(`${id}-gen`, 540, 1560, 1.55, false)}<path id="${id}-cord" d="M664,1343L760,1560" stroke="#1a1512" stroke-width="8" fill="none"/>`);
    put(L.fg, `<g id="${id}-hand" transform="translate(760,1560)"><g transform="rotate(-70) scale(0.75)">${Hand.grip({ skin: o.skin || "#b9805a", sleeve: o.sleeve || "#2c3e6b" })}</g><rect x="-44" y="-18" width="88" height="36" rx="12" fill="#2a2420" ${OUT}/></g>`);
    L.fg.classList.remove("fgblur");
    put(L.glow, `<g id="${id}-bulb" opacity="0"><circle cx="540" cy="200" r="900" fill="url(#fLamp)"/></g><circle id="${id}-pilot" cx="664" cy="1343" r="16" fill="#ff3b30" opacity="0"/>`);
  }

  // ---------------- น้องปั้น's drawing of day 101: the school at night, the light on the hill, five of them under the fan, a man lying at the gate ----------------
  function drawing2(L, o = {}) {
    const id = o.id || "dw";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#5a4630"/>`);
    let s = `<g transform="rotate(-2 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    s += `<rect x="140" y="440" width="800" height="720" fill="#2f4a8a" opacity=".22" filter="url(#fCrayon)"/>`;   // the night sky, scribbled
    s += C("M240,520q40,-50 80,0", "#f4ecd8", 10) + `<circle cx="280" cy="520" r="44" fill="#f4ecd8" opacity=".8" filter="url(#fCrayon)"/>`;   // the moon
    s += C("M620,860Q740,700 880,760T930,860", "#5b6066", 14) + `<g id="${id}-hl"><circle cx="800" cy="720" r="22" fill="#f2c55c" filter="url(#fCrayon)"/>${C("M800,660v-40M760,680l-30,-30M840,680l30,-30M750,730h-50M850,730h50", "#f2c55c", 8)}</g>`;   // the hill and the light
    s += C("M150,1300H930", "#6f8f3e", 14) + C("M150,1300l0,-120M250,1300l0,-120M350,1300l0,-120M750,1300l0,-120M850,1300l0,-120M930,1300l0,-120M150,1180H930", "#5b6066", 8);
    s += C("M200,1140V860H640V1140M160,860L420,740L680,860M250,940h80v120h-80zM480,940h80v120h-80z", "#c8392b", 10) + `<rect x="200" y="860" width="440" height="280" fill="#f6d6a0" opacity=".6" filter="url(#fCrayon)"/>`;
    s += C("M420,780v60M380,820h80", "#2e2a26", 8);   // the fan on the roof line
    const fig = (x, y, col, h = 1) => `<g transform="translate(${x},${y}) scale(${h})" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="none" stroke="${col}" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,-80l40,40M0,0l-30,60M0,0l30,60" stroke="${col}" stroke-width="8" fill="none" stroke-linecap="round"/></g>`;
    s += fig(280, 1420, "#2f4a8a") + fig(380, 1430, "#c8392b") + fig(470, 1420, "#6f8f3e") + fig(560, 1430, "#d96a8a") + fig(640, 1450, "#e8b830", 0.7);
    s += `<g id="${id}-man" transform="translate(520,1240) rotate(-90)">${fig(0, 0, "#2e2a26", 0.65)}</g>`;   // the man lying across the gate
    s += `<text x="540" y="400" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="60" fill="#2f4a8a" filter="url(#fCrayon)">วันที่ 101 แสงบนเขา</text>`;
    s += `<text x="300" y="1560" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#c8392b" filter="url(#fCrayon)">ครูพิม ก้อง ลุง เจ๊ ปั้น</text></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }

  // ================= EP.3 "คนแปลกหน้า" =================
  // a kitchen knife in local coordinates: handle at the origin, blade along +x (so a Hand.grip at the origin holds it)
  const KNIFE = (id = "", s = 1) => `<g ${id ? `id="${id}"` : ""} transform="scale(${s})"><rect x="-150" y="-26" width="150" height="52" rx="12" fill="#3a2e22" ${OUT}/><path d="M-120,-26h30M-80,-26h30" stroke="#5a4a38" stroke-width="6"/><path d="M0,-30H330Q420,-30 460,-4L380,30H0Z" fill="#cfd4d8" ${OUT}/><path d="M0,0H370" stroke="#f4f6f8" stroke-width="6"/><path d="M10,-30H330Q400,-30 440,-8" stroke="#8d9299" stroke-width="4" fill="none"/></g>`;

  // ---------------- close-up of ภู's leg on the road: the cargo trouser, the gash with dirt in it (#id-gash, #id-dirt), the flap of cloth (#id-flap),
  // the pour of water (#id-pour), his own hand with a cloth (#id-hand), the bandage wrap (#id-wrap). o.time morning|day ----------------
  function woundClose(L, o = {}) {
    const id = o.id || "wd", t = o.time || "morning";
    sky(L, t);
    put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#fDirt)"/>${Array.from({ length: 40 }, (_, k) => { const r = mk(31 + k)(); return `<ellipse cx="${-1100 + ((k * 587) % 3400)}" cy="${-700 + ((k * 331) % 3300)}" rx="${18 + r * 30}" ry="${8 + r * 12}" fill="#8a6a42" opacity=".35"/>`; }).join("")}`);
    if (o.dress !== false && window.Dress) { const D = Dress; put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#dDirt)"/>${D.pebbles(-1100, 2300, -700, 2700, 120, 281, 12)}${D.leaves(-1100, 2300, -700, 2700, 40, 283)}${D.tufts(-1100, 2300, -700, 2700, 26, 285, 50, true)}`); }
    // the leg lies across the frame, lower-left to upper-right: a wide cargo trouser leg with a side pocket, the boot at the right
    let s = `<g transform="rotate(-18 540 1000)"><rect x="-400" y="1296" width="1760" height="90" fill="url(#dAO)"/><path d="M-400,700H1300V1300H-400Z" fill="#4a5560" ${OUT}/>${o.dress !== false ? `<path d="M-300,760q60,120 20,240M0,1180q80,-60 180,-20M980,760q-40,90 10,200M1120,1180q-60,-50 -150,-40" stroke="#38424b" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-340,1060q40,-30 90,-6M1000,1040q40,-20 80,6" stroke="#6a7682" stroke-width="5" fill="none"/><ellipse cx="-150" cy="900" rx="80" ry="34" fill="#6b4a2e" opacity=".25"/><ellipse cx="1100" cy="1180" rx="70" ry="28" fill="#6b4a2e" opacity=".3"/>` : ""}<path d="M-400,700H1300V760H-400Z" fill="#5c6974"/><path d="M-400,1240H1300V1300H-400Z" fill="#38424b"/>
      <path d="M-400,1000H1300" stroke="#3d4852" stroke-width="6" stroke-dasharray="40 30" opacity=".6"/><rect x="760" y="820" width="190" height="150" rx="10" fill="#5c6974" ${OUT}/><path d="M760,860h190" stroke="#2e2a26" stroke-width="4"/>
      <g transform="translate(1300,1000)"><path d="M0,-300Q160,-320 200,-140L240,300H0Z" fill="#1e1e1e" ${OUT}/><path d="M20,-240h140" stroke="#5b6066" stroke-width="10"/><path d="M30,-150h140M30,-70h140" stroke="#5b6066" stroke-width="10"/></g>`;
    // the gash: the cloth torn wide at the shin, the skin, a deep cut with dirt and rust-dark edges
    s += `<g id="${id}-flap"><path d="M180,780Q400,730 640,790Q560,1020 440,1230Q300,1150 160,1240Q130,1000 180,780Z" fill="#d39a6e" ${OUT}/>
      <path d="M180,780Q400,730 640,790" stroke="#2e2a26" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="30 14"/><path d="M640,790Q560,1020 440,1230" stroke="#2e2a26" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="30 14"/></g>
      <g id="${id}-skin"><path d="M200,790Q400,750 620,800Q550,1010 440,1210Q310,1140 180,1220Q150,1000 200,790Z" fill="#d39a6e"/><path d="M220,820q180,-30 360,10" stroke="#e8b48e" stroke-width="14" fill="none" opacity=".6"/></g>
      <g id="${id}-gash"><path d="M260,860Q400,960 560,1120" stroke="#5a0f0f" stroke-width="54" stroke-linecap="round" fill="none"/><path d="M260,860Q400,960 560,1120" stroke="#8f1b1b" stroke-width="28" stroke-linecap="round" fill="none"/><path d="M290,880Q400,960 540,1100" stroke="#c0392b" stroke-width="8" stroke-linecap="round" fill="none" opacity=".7"/>
      <path d="M280,910q-30,40 -16,90M520,1080q30,50 10,100M400,980q-40,30 -36,70" stroke="#8f1b1b" stroke-width="9" fill="none" opacity=".8" stroke-linecap="round"/></g>
      <g id="${id}-dirt">${[[300, 890], [340, 925], [390, 960], [430, 1000], [470, 1040], [510, 1082], [360, 905], [450, 985], [320, 950], [495, 1120]].map(([x, y], k) => `<circle cx="${x}" cy="${y}" r="${7 + (k % 3) * 3}" fill="#3a2a16"/>`).join("")}<path d="M330,870l10,-14M470,1010l14,-10M400,940l-12,-12" stroke="#6b4a2e" stroke-width="6" stroke-linecap="round"/><path d="M300,870q40,-12 80,0M440,1030q30,-14 60,0" stroke="#6b4a2e" stroke-width="4" fill="none" opacity=".8"/></g>
      <g id="${id}-pour" opacity="0"><path d="M400,420Q400,700 400,920" stroke="#9fd0ea" stroke-width="30" stroke-linecap="round" fill="none" opacity=".8"/><path d="M400,420Q400,700 400,920" stroke="#e8f6ff" stroke-width="10" stroke-linecap="round" fill="none"/>${[[340, 980], [460, 1010], [400, 1060], [520, 1100]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="30" ry="10" fill="#9fd0ea" opacity=".7"/>`).join("")}</g>
      <g id="${id}-wrap" opacity="0">${[0, 1, 2, 3, 4].map((k) => `<path d="M${120 + k * 95},${740 + k * 8}L${180 + k * 95},${1260 + k * 8}" stroke="#f4ecd8" stroke-width="70" stroke-linecap="butt"/>`).join("")}${[0, 1, 2, 3, 4].map((k) => `<path d="M${150 + k * 95},${740 + k * 8}L${210 + k * 95},${1260 + k * 8}" stroke="#d9d0bc" stroke-width="3"/>`).join("")}<path d="M560,800l40,-30M560,1180l40,30" stroke="#d9d0bc" stroke-width="6"/></g></g>`;
    put(L.set, s);
    // his own hand: a grip with a folded rag, coming in from the lower right (a rescue volunteer's hand)
    put(L.act, `<g id="${id}-hand" transform="translate(760,1300) rotate(-30) scale(0.7)" opacity="${o.hand ? 1 : 0}"><g transform="translate(-120,-40) rotate(20)"><rect x="-90" y="-60" width="180" height="120" rx="10" fill="#f4ecd8" ${OUT}/><path d="M-70,-30h140M-70,0h140M-70,30h140" stroke="#d9d0bc" stroke-width="3"/></g>${Hand.grip({ skin: "#d39a6e", sleeve: "#6b7a5a" })}</g>`);
    // the jerrycan of water above, tipped (its mouth where the pour starts)
    put(L.act, `<g id="${id}-can" transform="translate(440,300) rotate(55)" opacity="${o.can ? 1 : 0}"><rect x="-90" y="-130" width="180" height="260" rx="18" fill="#dfe6e2" ${OUT}/><rect x="-30" y="-170" width="60" height="50" rx="8" fill="#5b6066" ${OUT}/><path d="M-60,-60h120" stroke="#9fc5d8" stroke-width="10"/><text y="40" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#2f4a8a" transform="rotate(-55)">น้ำ</text></g>`);
    if (t === "morning") put(L.glow, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#ffdca8" opacity=".08"/>`);
  }

  // ---------------- the drawing of day 102: six crayon figures inside the fence, ภู (grey-green) standing at the fence, and a black scribbled figure outside ----------------
  function drawing3(L, o = {}) {
    const id = o.id || "dw3";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#5a4630"/>`);
    let s = `<g transform="rotate(2 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    s += `<rect x="140" y="440" width="800" height="720" fill="#2f4a8a" opacity=".22" filter="url(#fCrayon)"/>`;
    s += C("M240,520q40,-50 80,0", "#f4ecd8", 10) + `<circle cx="280" cy="520" r="44" fill="#f4ecd8" opacity=".8" filter="url(#fCrayon)"/>`;
    s += C("M200,1140V860H640V1140M160,860L420,740L680,860M250,940h80v120h-80zM480,940h80v120h-80z", "#c8392b", 10) + `<rect x="200" y="860" width="440" height="280" fill="#f6d6a0" opacity=".6" filter="url(#fCrayon)"/>`;
    // the fence: a long line with posts, running down the right side of the page
    s += C("M150,1300H930", "#6f8f3e", 14) + C("M150,1300l0,-120M250,1300l0,-120M350,1300l0,-120M750,1300l0,-120M850,1300l0,-120M930,1300l0,-120M150,1180H930", "#5b6066", 8);
    s += C("M700,1180V1560M760,1180V1560", "#5b6066", 8) + C("M700,1180h60M700,1320h60M700,1460h60", "#5b6066", 8);   // the gate bars, drawn tall
    const fig = (x, y, col, h = 1) => `<g transform="translate(${x},${y}) scale(${h})" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="none" stroke="${col}" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,-80l40,40M0,0l-30,60M0,0l30,60" stroke="${col}" stroke-width="8" fill="none" stroke-linecap="round"/></g>`;
    s += fig(230, 1440, "#2f4a8a") + fig(320, 1450, "#c8392b") + fig(410, 1440, "#6f8f3e") + fig(500, 1450, "#d96a8a") + fig(580, 1470, "#e8b830", 0.7);
    // ภู at the gate, inside, arm out through the bars; and the one outside, scribbled black, no face
    s += `<g id="${id}-phu">${fig(660, 1440, "#4e6a5a")}${C("M660,1360l80,-20", "#4e6a5a", 8)}</g>`;
    s += `<g id="${id}-dark"><g transform="translate(850,1430)" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="#2e2a26" stroke="#2e2a26" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,-80l40,40M0,0l-30,60M0,0l30,60" stroke="#2e2a26" stroke-width="10" fill="none" stroke-linecap="round"/>
      <path d="M-50,-170q30,-30 60,10q20,30 -10,60q-40,20 -70,-10q-20,-40 20,-60" stroke="#2e2a26" stroke-width="4" fill="none" opacity=".8"/><path d="M-30,-60q-30,30 -10,70M30,-60q30,30 10,70" stroke="#2e2a26" stroke-width="4" fill="none"/></g></g>`;
    s += `<text x="540" y="400" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="60" fill="#2f4a8a" filter="url(#fCrayon)">วันที่ 102 พี่ภู</text>`;
    s += `<text x="330" y="1600" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#c8392b" filter="url(#fCrayon)">ครู ก้อง ลุง เจ๊ ปั้น พี่ภู</text><text id="${id}-who" x="850" y="1600" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#2e2a26" filter="url(#fCrayon)">?</text></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }

  // ================= EP.4 "รั้วล้ม" =================
  // rain: a sheet of thin streaks in the foreground layer; flife drives .raind groups downward in a loop. o.n streaks, o.op opacity
  function rain(L, o = {}) {
    const n = o.n ?? 90, r = mk(o.seed || 17), op = o.op ?? 0.55;
    put(L.fg, `<g class="raind" opacity="${op}">${Array.from({ length: n }, () => { const x = -1200 + r() * 3500, y = -900 + r() * 2200, l = 60 + r() * 90; return `<path d="M${f1(x)},${f1(y)}l-14,${f1(l)}" stroke="#dfe8f0" stroke-width="${(2 + r() * 2).toFixed(1)}" stroke-linecap="round" opacity="${(0.35 + r() * 0.5).toFixed(2)}"/>`; }).join("")}</g>
      <g class="raind2" opacity="${op * 0.6}">${Array.from({ length: Math.floor(n * 0.6) }, () => { const x = -1200 + r() * 3500, y = -900 + r() * 2200, l = 40 + r() * 60; return `<path d="M${f1(x)},${f1(y)}l-10,${f1(l)}" stroke="#c9d6e0" stroke-width="1.6" stroke-linecap="round" opacity="${(0.3 + r() * 0.4).toFixed(2)}"/>`; }).join("")}</g>`);
    L.fg.classList.remove("fgblur");
    if (o.splash !== false) put(L.set, `<g class="rsplash">${Array.from({ length: 24 }, (_, k) => `<ellipse cx="${-1000 + ((k * 433) % 3200)}" cy="${1480 + ((k * 97) % 400)}" rx="${10 + (k % 3) * 6}" ry="4" fill="none" stroke="#dfe8f0" stroke-width="3" opacity="0"/>`).join("")}</g>`);
  }

  // ---------------- the back door of the school building, from inside the corridor at night: two wooden panels (#id-dl, #id-dr) that swing shut toward the middle,
  // the timber bar (#id-bar) that drops into its brackets, and through the opening the yard in the rain ----------------
  function backDoor(L, o = {}) {
    const id = o.id || "bd";
    sky(L, "night");
    // what is outside the door: the yard at night (dirt, the far fence line), rain
    put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2c3a4c"/><circle cx="700" cy="300" r="90" fill="#dfe6e2" opacity=".8"/><circle cx="700" cy="300" r="300" fill="#9fb8d8" opacity=".16"/><rect x="-1200" y="1000" width="3500" height="1600" fill="#6b5a3e"/><path d="M-1200,1000H2300" stroke="#5b6066" stroke-width="30"/>`);
    put(L.mid, `<rect x="-1200" y="1180" width="3500" height="900" fill="#5a4630"/><ellipse cx="560" cy="1500" rx="700" ry="90" fill="#6b5a3e" opacity=".6"/>`);
    // the corridor wall around the door, the frame, the floor
    const W = 1080, DX = 300, DW = 480, DT = 420, DB = 1560;
    let s = `<rect x="-1200" y="-800" width="3500" height="3600" fill="#d9cfb8" ${OUT}/><rect x="-1200" y="${DB}" width="3500" height="1200" fill="#8a6a42" ${OUT}/><path d="M-1200,${DB}H2300" stroke="#5a3d24" stroke-width="8"/>
      ${Array.from({ length: 12 }, (_, k) => `<path d="M${-1200 + k * 300},${DB}L${-1300 + k * 300},2700" stroke="#5a3d24" stroke-width="4" opacity=".5"/>`).join("")}
      <rect x="-1200" y="${DT - 60}" width="3500" height="24" fill="#b3ada0"/><path d="M-1200,1300H${DX - 40}M${DX + DW + 40},1300H2300" stroke="#c4b99f" stroke-width="30"/>`;
    s = s.replace(`<rect x="-1200" y="-800" width="3500" height="3600" fill="#d9cfb8" ${OUT}/>`, `<path d="M-1200,-800H2300V2800H-1200Z M${DX - 40},${DT - 40}V${DB}H${DX + DW + 40}V${DT - 40}Z" fill="#d9cfb8" fill-rule="evenodd" ${OUT}/>`);
    if (o.dress !== false && window.Dress) { const D = Dress, hole = `M-1200,-800H2300V2800H-1200Z M${DX - 40},${DT - 40}V${DB}H${DX + DW + 40}V${DT - 40}Z`;
      s += `<path d="${hole}" fill="url(#dConc)" fill-rule="evenodd"/><path d="M-1200,${DB - 260}H${DX - 40}V${DB}H-1200ZM${DX + DW + 40},${DB - 260}H2300V${DB}H${DX + DW + 40}Z" fill="url(#dGrime)"/>${D.streak(-700, DT - 36, 50, 300, 0.8)}${D.streak(1200, DT - 36, 70, 360, 0.8)}${D.crack(-200, 700, 140, 20, 0.5)}${D.crack(1000, 1000, 120, -30, 0.45)}
        <path d="M-1200,${DB - 140}H${DX - 40}M${DX + DW + 40},${DB - 140}H2300" stroke="#9a8a6a" stroke-width="10"/>
        <rect x="${DX - 40}" y="${DT - 40}" width="40" height="${DB - DT + 40}" fill="#7a5a3e" stroke="${INK}" stroke-width="3"/><rect x="${DX + DW}" y="${DT - 40}" width="40" height="${DB - DT + 40}" fill="#7a5a3e" stroke="${INK}" stroke-width="3"/><rect x="${DX - 40}" y="${DT - 40}" width="${DW + 80}" height="40" fill="#7a5a3e" stroke="${INK}" stroke-width="3"/><rect x="${DX - 40}" y="${DT - 40}" width="${DW + 80}" height="${DB - DT + 40}" fill="none" stroke="#fff" stroke-opacity=".15" stroke-width="2"/>
        <g transform="translate(-460,620)"><rect x="0" y="0" width="420" height="300" fill="#b48a56" stroke="${INK}" stroke-width="4"/><rect x="14" y="14" width="392" height="272" fill="#c9a06c"/>${[[30, 30, 120, 150, -3, "#f2ede0"], [170, 26, 110, 90, 4, "#f2e27a"], [300, 40, 90, 120, -5, "#f2ede0"], [180, 140, 130, 120, 2, "#d9e8f2"], [40, 200, 110, 70, 6, "#f2c2d6"]].map(([x, y, w, h, a, c]) => `<g transform="rotate(${a} ${x + w / 2} ${y + h / 2})"><rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}" stroke="${INK}" stroke-width="1.5"/><path d="M${x + 12},${y + 24}h${w - 24}M${x + 12},${y + 42}h${w - 40}M${x + 12},${y + 60}h${w - 30}" stroke="#8a857a" stroke-width="3"/><circle cx="${x + w / 2}" cy="${y + 8}" r="5" fill="#c8392b"/></g>`).join("")}</g>
        <path d="M-1200,${DT - 140}H2300" stroke="#9aa0a6" stroke-width="12"/><path d="M-1200,${DT - 144}H2300" stroke="#fff" stroke-opacity=".35" stroke-width="3"/><rect x="1060" y="${DT - 166}" width="60" height="52" rx="6" fill="#b3ada0" stroke="${INK}" stroke-width="3"/><path d="M1090,${DT - 114}V${DT - 30}" stroke="#2a2420" stroke-width="4"/><circle cx="1090" cy="${DT - 14}" r="18" fill="#f4e6b8" stroke="${INK}" stroke-width="3"/>
        <rect x="-1200" y="${DB}" width="3500" height="1200" fill="url(#dPlankH)" opacity=".6"/><rect x="-1200" y="${DB}" width="3500" height="70" fill="url(#dAO)"/>
        <path d="M${DX - 60},${DB + 20}Q${DX + DW / 2},${DB + 90} ${DX + DW + 60},${DB + 20}Q${DX + DW + 120},${DB + 200} ${DX + DW / 2},${DB + 230}Q${DX - 160},${DB + 200} ${DX - 60},${DB + 20}Z" fill="#3a3a4a" opacity=".35"/><path d="M${DX + 40},${DB + 80}q${DW / 2 - 40},26 ${DW - 80},0" stroke="#cfe0f2" stroke-opacity=".35" stroke-width="5" fill="none"/>
        ${[[DX + 60, DB + 260], [DX + 160, DB + 330], [DX + 100, DB + 430], [DX + 230, DB + 500]].map(([x, y], k) => `<path d="M${x},${y}q-14,-26 0,-40q16,8 12,40z" fill="#3a2a1a" opacity=".35" transform="rotate(${k % 2 ? 12 : -12} ${x} ${y})"/>`).join("")}${D.leaves(DX - 200, DX + DW + 200, DB + 40, DB + 400, 14, 271)}${D.broom(1400, DB, 0.9, -10)}${D.bucket(1500, DB + 20, 0.9, "#2f6fb8")}`;
      put(L.glow, `<circle cx="1090" cy="${DT - 14}" r="380" fill="url(#fLamp)" opacity=".55"/>`); }
    put(L.set, s);
    // a hole in the wall: we see the night through it (the far/mid layers show through this rect because L.set is painted over them except here)
    // the panels: each a frame of planks with a cross brace; they hinge at the outer jambs and are drawn closed at translate(0)
    const panel = (pid, flip) => `<g id="${pid}" transform="translate(${flip ? DX + DW : DX},0) scale(${flip ? -1 : 1},1)"><g transform="translate(${flip ? -0 : 0},0)"><rect x="0" y="${DT}" width="${DW / 2}" height="${DB - DT}" fill="#6b4a2e" ${OUT}/>
      ${[0, 1, 2].map((k) => `<rect x="${12 + k * 76}" y="${DT + 12}" width="64" height="${DB - DT - 24}" fill="#7a5a3e" stroke="#4a3220" stroke-width="3"/>`).join("")}
      <rect x="0" y="${DT}" width="${DW / 2}" height="${DB - DT}" fill="url(#dWood)" opacity=".7"/><rect x="0" y="${DB - 220}" width="${DW / 2}" height="220" fill="url(#dGrime)"/>
      <path d="M14,${DT + 40}L${DW / 2 - 14},${DB - 40}" stroke="#4a3220" stroke-width="22"/><rect x="0" y="${(DT + DB) / 2 - 20}" width="${DW / 2}" height="40" fill="#5a3d24" ${OUT}/>
      <circle cx="${DW / 2 - 40}" cy="${(DT + DB) / 2 + 80}" r="18" fill="#3a3f45" ${OUT}/></g></g>`;
    put(L.act, `<g id="${id}-doors">${panel(`${id}-dl`, false)}${panel(`${id}-dr`, true)}</g>
      <g id="${id}-brk"><rect x="${DX - 70}" y="${(DT + DB) / 2 + 20}" width="60" height="110" rx="8" fill="#3a3f45" ${OUT}/><rect x="${DX + DW + 10}" y="${(DT + DB) / 2 + 20}" width="60" height="110" rx="8" fill="#3a3f45" ${OUT}/></g>
      <g id="${id}-bar" opacity="${o.barred ? 1 : 0}" transform="translate(0,${o.barred ? 0 : -500})"><rect x="${DX - 90}" y="${(DT + DB) / 2 + 36}" width="${DW + 180}" height="76" rx="10" fill="#8a6a42" ${OUT}/><path d="M${DX - 60},${(DT + DB) / 2 + 60}H${DX + DW + 60}" stroke="#5a3d24" stroke-width="6"/></g>`);
    // the open state: panels swung back (we animate them from open to closed with scaleX about their hinges)
    if (!o.closed) { const l = document.getElementById(`${id}-dl`), r = document.getElementById(`${id}-dr`); l.setAttribute("transform", `translate(${DX},0) scale(${o.open ?? 0.25},1)`); r.setAttribute("transform", `translate(${DX + DW},0) scale(${-(o.open ?? 0.25)},1)`); }
    put(L.glow, `<rect x="${DX - 40}" y="${DT - 40}" width="${DW + 80}" height="${DB - DT + 40}" fill="#9fb8d8" opacity=".14"/>`);
  }

  // ---------------- the drawing of day 103: the broken fence, five inside, ลุง standing beyond the fence; a small box with a face hanging on a post ----------------
  function drawing4(L, o = {}) {
    const id = o.id || "dw4";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#5a4630"/>`);
    let s = `<g transform="rotate(-1.5 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    s += `<rect x="140" y="440" width="800" height="720" fill="#2f4a8a" opacity=".3" filter="url(#fCrayon)"/>`;
    s += Array.from({ length: 30 }, (_, k) => C(`M${170 + (k * 97) % 760},${470 + (k * 53) % 600}l-8,40`, "#9fc5d8", 5)).join("");   // the rain, scribbled
    s += C("M200,1140V860H640V1140M160,860L420,740L680,860M250,940h80v120h-80zM480,940h80v120h-80z", "#c8392b", 10) + `<rect x="200" y="860" width="440" height="280" fill="#f6d6a0" opacity=".6" filter="url(#fCrayon)"/>`;
    s += C("M150,1300H700", "#6f8f3e", 14) + C("M150,1300l0,-120M250,1300l0,-120M350,1300l0,-120M450,1300l0,-120M150,1180H700", "#5b6066", 8);
    s += C("M700,1300l200,-60M720,1290l180,-120M760,1280l140,-20", "#5b6066", 8);   // the fence down, lying flat to the right
    const fig = (x, y, col, h = 1) => `<g transform="translate(${x},${y}) scale(${h})" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="none" stroke="${col}" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,-80l40,40M0,0l-30,60M0,0l30,60" stroke="${col}" stroke-width="8" fill="none" stroke-linecap="round"/></g>`;
    s += fig(230, 1440, "#2f4a8a") + fig(320, 1450, "#c8392b") + fig(410, 1450, "#d96a8a") + fig(490, 1470, "#e8b830", 0.7) + fig(580, 1440, "#4e6a5a");
    s += `<g id="${id}-man">${fig(880, 1200, "#6f8f3e")}${C("M840,1080q40,-10 60,-40", "#6f8f3e", 8)}</g>`;   // ลุง beyond the fence, standing, his hat
    s += C("M860,1070q20,-30 40,0", "#e8b830", 8);
    s += `<g id="${id}-box"><rect x="640" y="1180" width="60" height="50" fill="#2e2a26" filter="url(#fCrayon)"/><path d="M652,1196h10M678,1196h10M655,1218q15,-12 30,0" stroke="#f4ecd8" stroke-width="4" fill="none"/>${C("M670,1180v-60", "#2e2a26", 5)}</g>`;   // the small box with a face, on a string
    s += `<text x="540" y="400" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="60" fill="#2f4a8a" filter="url(#fCrayon)">วันที่ 103 ฝนตก</text>`;
    s += `<text x="420" y="1600" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#c8392b" filter="url(#fCrayon)">ครู ก้อง เจ๊ ปั้น พี่ภู</text><text x="880" y="1600" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#6f8f3e" filter="url(#fCrayon)">ลุง</text></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }
  Object.assign(Sets, { backDoor, drawing4 });
  window.Fence.rain = rain;
  Object.assign(Sets, { woundClose, drawing3 });
  window.Fence.KNIFE = KNIFE;
  Object.assign(Sets, { fair, genClose, drawing2 });
  window.Fence.FAN = FAN; window.Fence.BULB = BULB;

})();
