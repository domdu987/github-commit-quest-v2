// "ต่อหัวเสือ" world kit (เลน B · 31 ต.ค. 2569): a village yard in the cool season, the big tamarind behind the village's
// ศาลตายาย with a hornet nest the size of a water jar hanging in it. Built on Sets.village2 (pop2.js) for the sky / far / mid
// layers, with the story's own pieces on top. Seeded RNG only.
//   Sets.hnYard(L, o)    the yard: village2 day (or o.time "dusk"), the tamarind (o.tree x, default 760) with the nest hanging under a
//                        branch, the ศาลตายาย on its post under the tree (o.shrine x), the title plank nailed to the shrine fence
//                        (o.title { x, y, sub }), the pond with lotus and a plank pier (o.pond x | false), the family pickup (o.truck x | false,
//                        o.truckOpen: the driver's door open — the clue in EP.2), a clothesline. o.nest false hides the nest.
//                        ids: ${id}-nest (wrap, no transform; sway it), ${id}-nestHole (the entrance), ${id}-title, ${id}-pond, ${id}-truck
//   Sets.hnNest(L, o)    a hero close-up of the nest under the branch: papery scalloped bands, the entrance, hornets on the shell
//                        (o.crawl n), the shrine's red cloth far below. ids ${id}-nest, ${id}-crawl
//   Sets.hnLegend(L, o)  the หนังตะลุง screen: the เจ้าที่ old man under the tamarind and his "ทหาร" (hornet shadows) — tweens via Hn.legend
//   Hn.hornet(o)         one hornet, side view facing right, ~70 units long at s 1: orange "tiger" head, black eyes, dark brown thorax,
//                        amber-banded abdomen, sting, two pairs of smoky wings (class hnw for the flicker). o.c colours, o.dead (on its back)
//   Hn.swarm(tl, layer, o) a deterministic swarm: o.n hornets around o.cx/o.cy (or o.path [[t, x, y]…] the swarm follows), radius o.rx/o.ry,
//                        o.s size, o.t0, o.dur, o.seed, o.chase (they stream behind the moving centre), o.id. Wings flicker every frame.
//   Hn.shrine(x, y, s, o) the ศาลตายาย: a little teak house on a post, red and yellow cloth tied round the post, the old couple
//                        figurines, zebras, red soda bottles with straws, a marigold garland, incense (o.smoke)
//   Hn.titlePlank(x, y, s, o) the title painted on a weathered plank: "ต่อหัวเสือ" + a painted hornet + o.sub (EP line)
//   Hn.pond(x, y, s, o)  the pond with lotus pads, reeds, a plank pier
//   Hn.nest(x, y, s, o)  the nest itself (SVG) · Hn.legend(tl, id, t0, dur) the legend screen's animation
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const OUT2 = `stroke="${INK}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const Hn = (window.Hn = window.Hn || {});

  Sets.DEFS += `
    <linearGradient id="hnNest" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a7a66"/><stop offset=".35" stop-color="#cdbda2"/><stop offset=".6" stop-color="#b8a68a"/><stop offset="1" stop-color="#6e604e"/></linearGradient>
    <radialGradient id="hnNestAO" cx=".5" cy=".5" r=".5"><stop offset=".6" stop-color="#1a120c" stop-opacity="0"/><stop offset="1" stop-color="#1a120c" stop-opacity=".45"/></radialGradient>
    <linearGradient id="hnHead" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc24a"/><stop offset="1" stop-color="#e07a12"/></linearGradient>
    <linearGradient id="hnAbd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a3a22"/><stop offset="1" stop-color="#26160c"/></linearGradient>
    <linearGradient id="hnBand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd25a"/><stop offset="1" stop-color="#d88a14"/></linearGradient>
    <linearGradient id="hnWing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8eef4" stop-opacity=".75"/><stop offset="1" stop-color="#9aa6b4" stop-opacity=".35"/></linearGradient>
    <linearGradient id="hnTeak" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a4a26"/><stop offset=".5" stop-color="#a86a38"/><stop offset="1" stop-color="#6a3c1e"/></linearGradient>
    <linearGradient id="hnRoof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8402a"/><stop offset="1" stop-color="#8a2618"/></linearGradient>
    <linearGradient id="hnPlank" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8a274"/><stop offset=".5" stop-color="#b08a5c"/><stop offset="1" stop-color="#8e6a44"/></linearGradient>
    <linearGradient id="hnPond" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9cc0b4"/><stop offset=".5" stop-color="#5e8e86"/><stop offset="1" stop-color="#2e5a58"/></linearGradient>
    <linearGradient id="hnPondD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8b08a"/><stop offset=".5" stop-color="#9a6a6a"/><stop offset="1" stop-color="#3a3048"/></linearGradient>
    <radialGradient id="hnScreen" cx=".5" cy=".45" r=".7"><stop offset="0" stop-color="#fff2c8"/><stop offset=".6" stop-color="#f2c47a"/><stop offset="1" stop-color="#a8642a"/></radialGradient>`;

  // ---------------- the hornet ----------------
  // side view facing right, origin at the waist (petiole), ~70 long at s 1
  Hn.hornet = (o = {}) => {
    const s = o.s ?? 1, w = o.wing ?? 1;
    const legs = `<g stroke="#2a1608" stroke-width="3" fill="none" stroke-linecap="round"><path d="M6,6l-6,14l-8,6M14,7l2,16l-4,8M22,6l8,14l2,9"/></g>`;
    const abd = `<g><path d="M0,0C-8,-14 -34,-16 -46,-6C-54,2 -50,14 -40,16C-26,20 -6,14 0,0Z" fill="url(#hnAbd)" ${OUT2}/>
      <path d="M-10,-11C-6,-4 -6,6 -10,13" stroke="url(#hnBand)" stroke-width="7" fill="none"/>
      <path d="M-22,-13C-18,-4 -18,8 -22,16" stroke="url(#hnBand)" stroke-width="6" fill="none"/>
      <path d="M-34,-11C-31,-3 -31,8 -34,15" stroke="#e8a830" stroke-width="4" fill="none"/>
      <path d="M-49,6l-9,4" stroke="#1a0e06" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M-30,-10q10,-3 20,0" stroke="#fff6d8" stroke-width="2" fill="none" opacity=".55"/></g>`;
    const tho = `<ellipse cx="13" cy="-2" rx="13" ry="11" fill="#3a2414" ${OUT2}/><path d="M6,-10q7,-3 14,0" stroke="#d8902a" stroke-width="3" fill="none"/>`;
    const head = `<g transform="translate(30,-3)"><ellipse cx="0" cy="0" rx="10" ry="11" fill="url(#hnHead)" ${OUT2}/>
      <path d="M-2,-9C6,-8 7,4 2,8C-2,4 -4,-4 -2,-9Z" fill="#1a0e06"/><circle cx="2" cy="-4" r="1.6" fill="#fff" opacity=".8"/>
      <path d="M6,6l6,4M5,8l4,6" stroke="#2a1608" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M-2,-10q4,-12 14,-14M2,-9q8,-8 16,-6" stroke="#2a1608" stroke-width="2" fill="none" stroke-linecap="round"/></g>`;
    const wings = `<g class="hnw" transform="translate(12,-10)"><g transform="scale(1,${w})"><path d="M0,0C-14,-18 -44,-26 -52,-18C-56,-10 -32,-4 0,0Z" fill="url(#hnWing)" stroke="#5a6470" stroke-width="1.4"/>
      <path d="M-2,2C-12,-6 -32,-8 -36,-2C-36,4 -20,4 -2,2Z" fill="url(#hnWing)" stroke="#5a6470" stroke-width="1.2"/><path d="M-6,-3L-44,-17" stroke="#5a6470" stroke-width="1" opacity=".6"/></g></g>`;
    const body = o.dead ? `<g transform="rotate(180) translate(0,4)">${legs}${abd}${tho}${head}</g>` : `${legs}${abd}${tho}${head}${wings}`;
    return `<g transform="scale(${s})"${o.cls ? ` class="${o.cls}"` : ""}>${body}</g>`;
  };

  // a swarm, recomputed from timeline time (seek-safe). Each hornet: <g id> translate (no transform on the inner art)
  Hn.swarm = (tl, layer, o = {}) => {
    const r = mk(o.seed || 31), n = o.n || 24, id = o.id || `hs${Math.floor(r() * 1e6)}`, S = o.s ?? 0.5;
    const P = Array.from({ length: n }, (_, k) => ({ ph: r() * 6.28, sp: 0.6 + r() * 0.9, a: r(), b: r(), lag: r(), dir: r() < 0.5 ? -1 : 1, sz: 0.75 + r() * 0.5, k }));
    put(layer, `<g id="${id}" class="hnswarm">${P.map((p, k) => `<g id="${id}-${k}"><g id="${id}-${k}-f">${Hn.hornet({ s: S * p.sz })}</g></g>`).join("")}</g>`);
    const els = P.map((_, k) => document.getElementById(`${id}-${k}`)), fl = P.map((_, k) => document.getElementById(`${id}-${k}-f`));
    const wings = P.map((_, k) => fl[k].querySelector(".hnw > g"));
    const centre = (t) => {
      if (!o.path) return [o.cx ?? 540, o.cy ?? 800];
      const pa = o.path; if (t <= pa[0][0]) return [pa[0][1], pa[0][2]];
      for (let i = 1; i < pa.length; i++) if (t <= pa[i][0]) { const u = (t - pa[i - 1][0]) / (pa[i][0] - pa[i - 1][0]); return [pa[i - 1][1] + (pa[i][1] - pa[i - 1][1]) * u, pa[i - 1][2] + (pa[i][2] - pa[i - 1][2]) * u]; }
      const z = pa[pa.length - 1]; return [z[1], z[2]];
    };
    const rx = o.rx ?? 160, ry = o.ry ?? 110, grow = o.grow;
    const place = (t) => P.forEach((p, k) => {
      const tt = o.chase ? t - p.lag * o.chase : t;
      const [cx, cy] = centre(tt);
      const m = grow ? Math.min(1, Math.max(0.02, (t - (grow[0] + p.a * grow[1])) / 0.6)) : 1;
      const x = cx + Math.sin(t * 3.1 * p.sp + p.ph) * rx * (0.4 + 0.6 * p.a) * m + Math.sin(t * 7.3 + p.ph * 2) * 10;
      const y = cy + Math.cos(t * 2.3 * p.sp * p.dir + p.ph * 1.3) * ry * (0.4 + 0.6 * p.b) * m + Math.sin(t * 9.1 + p.ph) * 8;
      const vx = Math.cos(t * 3.1 * p.sp + p.ph) * p.dir;
      els[k].setAttribute("transform", `translate(${f1(x)},${f1(y)})`);
      fl[k].setAttribute("transform", `scale(${vx < 0 ? -1 : 1},1) rotate(${f1(Math.sin(t * 5 + p.ph) * 12)})`);
      if (wings[k]) wings[k].setAttribute("transform", `scale(1,${(0.25 + 0.75 * Math.abs(Math.sin(t * 95 + p.ph * 7))).toFixed(2)})`);
      if (grow) els[k].setAttribute("opacity", f1(Math.min(1, m * 1.4)));
    });
    place(0);
    const c = { t: 0 };
    tl.set(`#${id}`, { opacity: o.op ?? 1 }, o.t0 || 0);
    tl.to(c, { t: o.dur, duration: o.dur, ease: "none", immediateRender: false, onUpdate: () => place(c.t) }, o.t0 || 0);
    return id;
  };

  // ---------------- the nest ----------------
  // origin at the top (where it hangs from the branch); ~ 300 wide x 380 tall at s 1
  Hn.nest = (x, y, s, o = {}) => {
    const r = mk(o.seed || 77);
    let bands = "";
    // papery scallops: overlapping shell-shaped flaps laid row by row (each row hangs over the one below), tan / grey / cream paper
    const PAP = ["#cbb894", "#a8977c", "#e2d6bc", "#b9a688", "#8f8068"];
    for (let k = 0; k < 15; k++) {
      const yy = 20 + k * 26, sx = k * 37;
      let d = "";
      const w = 46 + r() * 10;
      for (let xx = -180 - (sx % w); xx < 180; xx += w) {
        const dep = 26 + r() * 10, c = PAP[Math.floor(r() * PAP.length)];
        d += `<path d="M${f1(xx)},${yy}C${f1(xx + 2)},${f1(yy + dep)} ${f1(xx + w - 2)},${f1(yy + dep)} ${f1(xx + w)},${yy}Z" fill="${c}" stroke="#5e5040" stroke-width="2.2"/>`
          + `<path d="M${f1(xx + 8)},${f1(yy + dep * 0.55)}C${f1(xx + w * 0.4)},${f1(yy + dep * 0.75)} ${f1(xx + w * 0.6)},${f1(yy + dep * 0.75)} ${f1(xx + w - 8)},${f1(yy + dep * 0.55)}" stroke="#fff6e0" stroke-width="1.6" fill="none" opacity=".5"/>`;
      }
      bands = d + bands;   // lower rows first, so each upper row overlaps the one under it
    }
    const shell = `M0,0C-60,6 -150,60 -156,180C-162,290 -90,380 0,384C90,380 162,290 156,180C150,60 60,6 0,0Z`;
    return `<g transform="translate(${x},${y}) scale(${s})">
      <ellipse cx="10" cy="400" rx="120" ry="16" fill="#1a120c" opacity="${o.shadow ?? 0}"/>
      <path d="M-14,-40L-10,24M14,-40L10,24" stroke="#5a3e26" stroke-width="12" stroke-linecap="round"/>
      <path d="${shell}" fill="url(#hnNest)" ${OUT}/>
      <clipPath id="${o.id || "hnn"}-clip"><path d="${shell}"/></clipPath>
      <g clip-path="url(#${o.id || "hnn"}-clip)">${bands}<path d="${shell}" fill="url(#hnNestAO)"/>
        <path d="M-120,120C-110,70 -70,40 -30,30" stroke="#fff8e8" stroke-width="10" fill="none" opacity=".35" stroke-linecap="round"/></g>
      <g id="${o.id || "hnn"}-hole"><ellipse cx="18" cy="352" rx="30" ry="14" fill="#1a1008" ${OUT3}/><ellipse cx="18" cy="348" rx="22" ry="8" fill="#000"/></g>
    </g>`;
  };

  // ---------------- the ศาลตายาย ----------------
  Hn.shrine = (x, y, s, o = {}) => {
    const fig = (fx, c, hair) => `<g transform="translate(${fx},-262)"><rect x="-9" y="-6" width="18" height="34" rx="6" fill="${c}" ${OUT2}/><circle cy="-14" r="9" fill="#d8a878" ${OUT2}/><path d="M-9,-16q9,-10 18,0" stroke="${hair}" stroke-width="5" fill="none"/></g>`;
    const zebra = (zx, f) => `<g transform="translate(${zx},-226) scale(${f},1)"><path d="M-16,0v-16h26l8,-14l6,4l-6,14v12" fill="#f4f2ec" ${OUT2}/><path d="M-10,-16v16M-2,-16v16M6,-16v14M14,-26l6,2" stroke="#222" stroke-width="3"/></g>`;
    const bottle = (bx) => `<g transform="translate(${bx},-226)"><path d="M-6,0v-22q0,-6 3,-9v-6h6v6q3,3 3,9v22Z" fill="#e8283a" ${OUT2}/><path d="M2,-36l6,-16" stroke="#f4f4f4" stroke-width="2.4"/><rect x="-6" y="-16" width="12" height="6" fill="#fff" opacity=".7"/></g>`;
    const garland = `<g>${Array.from({ length: 9 }, (_, k) => `<circle cx="${-50 + k * 12.5}" cy="${-196 + Math.sin((k / 8) * Math.PI) * 26}" r="7" fill="${k % 2 ? "#ffa82a" : "#ffc63a"}" stroke="#b8681a" stroke-width="1.4"/>`).join("")}</g>`;
    return `<g transform="translate(${x},${y}) scale(${s})">
      <ellipse cx="0" cy="4" rx="120" ry="18" fill="#1a120c" opacity=".35"/>
      <rect x="-90" y="-14" width="180" height="20" rx="4" fill="#cfc6b4" ${OUT3}/>
      <rect x="-14" y="-190" width="28" height="180" fill="url(#hnTeak)" ${OUT3}/>
      <path d="M-15,-120h30v22h-30zM-15,-80h30v14h-30z" fill="#e0282e" ${OUT2}/><path d="M-15,-98h30v10h-30z" fill="#f2c41a" ${OUT2}/><path d="M-15,-66h30v8h-30z" fill="#2aa04a" ${OUT2}/>
      <path d="M15,-110q18,10 14,40q-6,10 -10,0q4,-20 -4,-30" fill="#e0282e" ${OUT2}/>
      <rect x="-92" y="-206" width="184" height="18" rx="3" fill="#8a5a30" ${OUT3}/>
      ${zebra(-70, 1)}${zebra(70, -1)}${bottle(-40)}${bottle(40)}
      <rect x="-60" y="-300" width="120" height="96" fill="url(#hnTeak)" ${OUT3}/>
      <rect x="-40" y="-292" width="80" height="80" fill="#3a1c0c" ${OUT2}/>
      ${fig(-16, "#f2ece0", "#d8d4cc")}${fig(16, "#c8402a", "#d8d4cc")}
      <path d="M-84,-298L0,-368L84,-298Z" fill="url(#hnRoof)" ${OUT3}/><path d="M-84,-298q-14,-4 -20,-18M84,-298q14,-4 20,-18M0,-368l0,-26" stroke="${INK}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <path d="M-56,-318L0,-356L56,-318" stroke="#f2c41a" stroke-width="4" fill="none"/>
      ${garland}
      <g><rect x="-6" y="-212" width="12" height="10" fill="#9a6a3a"/><path d="M-3,-212v-30M0,-212v-34M3,-212v-28" stroke="#c8402a" stroke-width="2"/></g>
      ${o.smoke !== false ? `<path d="M0,-246C10,-270 -12,-290 2,-318C14,-340 -6,-356 6,-380" stroke="#f4f0ea" stroke-width="5" fill="none" opacity=".35" stroke-linecap="round"/>` : ""}
    </g>`;
  };

  // ---------------- the title plank ----------------
  Hn.titlePlank = (x, y, s, o = {}) => `<g transform="translate(${x},${y}) scale(${s})">
      <path d="M-210,-6L-206,-120L214,-116L210,4Z" fill="#1a120c" opacity=".3" transform="translate(10,12)"/>
      <path d="M-214,-4L-210,-124L216,-118L212,6Z" fill="url(#hnPlank)" ${OUT}/>
      <path d="M-190,-96q120,-6 380,2M-196,-30q160,4 390,-2M-150,-64q60,2 120,0" stroke="#7a5634" stroke-width="2.4" fill="none" opacity=".55"/>
      <circle cx="-196" cy="-104" r="6" fill="#6a6a6a" ${OUT2}/><circle cx="196" cy="-100" r="6" fill="#6a6a6a" ${OUT2}/><circle cx="-194" cy="-14" r="6" fill="#6a6a6a" ${OUT2}/><circle cx="194" cy="-10" r="6" fill="#6a6a6a" ${OUT2}/>
      <text x="40" y="-48" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="78" fill="#b8241a" stroke="#fff4dc" stroke-width="10" paint-order="stroke" transform="rotate(-2)">ต่อหัวเสือ</text>
      <g transform="translate(-150,-60) rotate(-18)">${Hn.hornet({ s: 1.15 })}</g>
      ${o.sub ? `<g transform="translate(20,46) rotate(2)"><rect x="-170" y="-30" width="340" height="56" rx="6" fill="#f2e8d0" ${OUT3}/><text x="0" y="8" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="${INK}">${o.sub}</text></g>` : ""}
    </g>`;

  // ---------------- the pond ----------------
  Hn.pond = (x, y, s, o = {}) => {
    const r = mk(o.seed || 55), dusk = o.time === "dusk";
    let p = `<g transform="translate(${x},${y}) scale(${s})">
      <ellipse cx="0" cy="0" rx="430" ry="96" fill="#5a4a2a"/><ellipse cx="0" cy="-4" rx="414" ry="86" fill="url(#${dusk ? "hnPondD" : "hnPond"})" ${OUT3}/>
      <path d="M-300,-30q120,-14 260,-6M-120,30q160,10 320,-4" stroke="#fff" stroke-width="4" fill="none" opacity=".35"/>`;
    for (let k = 0; k < 9; k++) { const px = -340 + r() * 640, py = -50 + r() * 90, pr = 26 + r() * 22; p += `<path d="M${f1(px)},${f1(py)}m${f1(-pr)},0a${f1(pr)},${f1(pr * 0.4)} 0 1 0 ${f1(pr * 2)},0l${f1(-pr)},0Z" fill="#4e8a3a" ${OUT2}/>`; }
    [[-200, -60], [120, -40], [260, -70]].forEach(([lx, ly]) => { p += `<path d="M${lx},${ly}v-70" stroke="#3e6a2a" stroke-width="5"/><path d="M${lx},${ly - 70}c-18,-10 -18,-40 0,-56c18,16 18,46 0,56Z" fill="#f4a0b8" ${OUT2}/><path d="M${lx},${ly - 72}c-6,-14 -2,-30 0,-38" stroke="#fff" stroke-width="2" opacity=".6" fill="none"/>`; });
    for (let k = 0; k < 16; k++) { const rx = -420 + r() * 120 + (k > 7 ? 700 : 0), ry = -40 + r() * 60; p += `<path d="M${f1(rx)},${f1(ry)}q${f1(-6 + r() * 12)},-60 ${f1(-10 + r() * 20)},-${f1(90 + r() * 60)}" stroke="#5a7a34" stroke-width="5" fill="none"/>`; }
    if (o.pier !== false) p += `<g><path d="M260,-20L420,-70L436,-40L276,10Z" fill="url(#hnPlank)" ${OUT3}/><path d="M300,-12v40M380,-36v40" stroke="#5a3e26" stroke-width="8"/></g>`;
    return p + `</g>`;
  };

  // a low bamboo bench (แคร่) — the seat top at y (sitChair rigs put their feet ~ +150·s below it)
  Hn.bench = (x, y, s) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="150" rx="190" ry="16" fill="#1a120c" opacity=".3"/>
    <path d="M-160,0v150M160,0v150M-130,10v140M130,10v140" stroke="#8a6a34" stroke-width="16"/><rect x="-180" y="-16" width="360" height="30" rx="8" fill="#c8a45a" ${OUT3}/>
    ${Array.from({ length: 8 }, (_, k) => `<path d="M${-170 + k * 46},-14v26" stroke="#9a7a3a" stroke-width="3"/>`).join("")}</g>`;

  // ---------------- the yard ----------------
  function hnYard(L, o = {}) {
    const id = o.id || "hy", G = o.ground ?? 1320, t = o.time || "day", dusk = t === "dusk";
    Sets.village2(L, { id: `${id}v`, time: t, ground: G, house: o.house ?? [-380, 0.9], tree: o.tree ?? 760, road: o.road ?? 180, banana: o.banana ?? true, bananaX: o.bananaX ?? 1300, fence: o.fence, rays: o.rays, sunX: o.sunX ?? 260, sunY: o.sunY, seed: o.seed, fg: o.fg });
    const TX = o.tree ?? 760;
    // the nest hangs under the tree's low right limb: a branch drawn out to it
    if (o.nest !== false) {
      const nx = TX + (o.nestDx ?? 150), ny = G - (o.nestUp ?? 840), ns = o.nestS ?? 0.62;
      put(L.set, `<path d="M${TX + 20},${ny - 60}C${TX + 80},${ny - 80} ${nx - 40},${ny - 40} ${nx + 120},${ny - 50}" stroke="#5e3e28" stroke-width="22" fill="none" stroke-linecap="round"/>
        <path d="M${nx + 60},${ny - 48}q30,-30 60,-20" stroke="#5e3e28" stroke-width="10" fill="none"/>
        <g id="${id}-nest">${Hn.nest(nx, ny - 26, ns, { id: `${id}-nst` })}</g>`);
      Hn.NEST = { x: nx, y: ny - 26, s: ns };
    }
    // ripe tamarind pods hanging round the crown (the lure for the slingshot)
    if (o.pods !== false) {
      const r2 = mk(71); let pd = "";
      for (let k = 0; k < 16; k++) { const px = TX - 260 + r2() * 420, py = G - 760 + r2() * 200, rot = -20 + r2() * 40;
        pd += `<g transform="translate(${f1(px)},${f1(py)}) rotate(${f1(rot)})"><path d="M0,0v8" stroke="#5e3e28" stroke-width="3"/><path d="M-6,8C-10,30 -4,52 6,70C10,74 16,70 14,64C6,46 4,28 6,8Z" fill="#8a5a30" stroke="#3e2410" stroke-width="2.4"/>
          <path d="M-2,22q4,4 0,8M2,40q4,4 0,8" stroke="#5a3418" stroke-width="2" fill="none"/></g>`; }
      put(L.set, `<g id="${id}-pods">${pd}</g>`);
    }
    if (o.shrine !== false) put(L.set, Hn.shrine(o.shrine ?? TX - 60, G + 70, o.shrineS ?? 0.95));
    if (o.title) put(L.set, `<g id="${id}-title">${Hn.titlePlank(o.title.x ?? 380, o.title.y ?? G + 220, o.title.s ?? 1, { sub: o.title.sub })}</g>`);
    if (o.pond !== false) put(L.set, `<g id="${id}-pond">${Hn.pond(o.pond ?? 1500, G + 260, o.pondS ?? 1, { time: t })}</g>`);
    if (o.truck !== false && Pop2.truck && o.truck !== undefined) put(L.set, `<g id="${id}-truck"><g transform="translate(${o.truck},${G + 120}) scale(${o.truckS ?? 2.1})">${Pop2.truck({ driver: false })}</g></g>`);
  }

  // ---------------- the nest close-up ----------------
  function hnNest(L, o = {}) {
    const id = o.id || "hc", r = mk(o.seed || 91), dusk = o.time === "dusk";
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3800" fill="url(#${dusk ? "p2SkyDusk" : "p2SkyDay"})"/><circle cx="200" cy="300" r="600" fill="url(#p2Sun)"/>`);
    let f = "";
    for (let k = 0; k < 12; k++) f += `<ellipse cx="${f1(-400 + r() * 1900)}" cy="${f1(-200 + r() * 900)}" rx="${f1(160 + r() * 200)}" ry="${f1(120 + r() * 140)}" fill="${["#4e6e34", "#6a8e3e", "#38542a"][k % 3]}" opacity=".85"/>`;
    put(L.far, `<g filter="url(#p2Soft)">${f}</g>`);
    put(L.set, `<path d="M-300,420C100,380 500,440 1400,360" stroke="#4e3220" stroke-width="58" fill="none" stroke-linecap="round"/>
      <path d="M-300,404C100,366 500,424 1400,346" stroke="#7a5638" stroke-width="12" fill="none" opacity=".6"/>
      ${Array.from({ length: 16 }, (_, k) => `<ellipse cx="${f1(-200 + k * 100 + r() * 40)}" cy="${f1(360 + r() * 60)}" rx="${f1(40 + r() * 30)}" ry="16" transform="rotate(${f1(-40 + r() * 80)} ${f1(-200 + k * 100)} 380)" fill="${k % 2 ? "#5e8a34" : "#7aa648"}" stroke="#2e4a1a" stroke-width="2"/>`).join("")}
      <g id="${id}-nest">${Hn.nest(o.x ?? 560, 420, o.s ?? 2.6, { id: `${id}-n`, seed: 13 })}</g>`);
    // hornets crawling on the shell
    let cr = "";
    for (let k = 0; k < (o.crawl ?? 9); k++) { const a = r(); cr += `<g transform="translate(${f1((o.x ?? 560) - 280 + r() * 560)},${f1(700 + r() * 600)}) rotate(${f1(-40 + r() * 80)})">${Hn.hornet({ s: 1.3 + r() * 0.3, wing: 0.25 })}</g>`; }
    put(L.set, `<g id="${id}-crawl">${cr}</g>`);
    put(L.fg, `<ellipse cx="-80" cy="1700" rx="320" ry="240" fill="#3e5a24"/><ellipse cx="1180" cy="200" rx="300" ry="260" fill="#4e6e2a"/>`);
  }

  // ---------------- the legend screen (หนังตะลุง) ----------------
  function hnLegend(L, o = {}) {
    const id = o.id || "hl";
    put(L.set, `<rect x="-600" y="-400" width="2300" height="2800" fill="#1a0e08"/>
      <rect x="60" y="300" width="960" height="1200" rx="8" fill="url(#hnScreen)" stroke="#5a2a14" stroke-width="22"/>
      <rect x="40" y="280" width="1000" height="22" fill="#8a3a1a"/><rect x="40" y="1496" width="1000" height="22" fill="#8a3a1a"/>
      <g fill="#1a0e08" id="${id}-tree"><path d="M520,1500C500,1300 470,1100 520,900C540,820 600,760 660,700" stroke="#1a0e08" stroke-width="36" fill="none"/>
        <path d="M520,900C440,820 360,780 260,770M560,820C640,760 760,700 860,700" stroke="#1a0e08" stroke-width="20" fill="none"/>
        ${Array.from({ length: 22 }, (_, k) => `<ellipse cx="${200 + (k * 37) % 700}" cy="${560 + ((k * 53) % 260)}" rx="70" ry="38" transform="rotate(${(k * 29) % 60 - 30} ${200 + (k * 37) % 700} ${560 + ((k * 53) % 260)})"/>`).join("")}
        <g transform="translate(760,720)"><path d="M0,0v40" stroke="#1a0e08" stroke-width="6"/><ellipse cx="0" cy="110" rx="70" ry="84"/><circle cx="12" cy="170" r="12" fill="#f2c47a"/></g></g>
      <g id="${id}-man" fill="#1a0e08"><g transform="translate(300,1150)">
        <path d="M-70,340L-50,60Q0,20 50,60L80,340Z"/><path d="M-30,60Q0,140 30,60" fill="#f2c47a" opacity=".55"/>
        <ellipse cx="0" cy="0" rx="42" ry="48"/><path d="M-30,-30L-20,-130L0,-170L20,-130L30,-30Z"/><circle cx="0" cy="-176" r="10"/>
        <path d="M-26,24Q0,130 26,24Z"/><circle cx="18" cy="-6" r="6" fill="#f2c47a"/>
        ${Array.from({ length: 6 }, (_, k) => `<circle cx="0" cy="${-50 - k * 18}" r="4" fill="#f2c47a"/>`).join("")}
        ${Array.from({ length: 8 }, (_, k) => `<circle cx="${-30 + (k % 4) * 20}" cy="${150 + Math.floor(k / 4) * 60}" r="6" fill="#f2c47a"/>`).join("")}
        <path d="M40,90L150,40" stroke="#1a0e08" stroke-width="18" stroke-linecap="round"/><path d="M150,40L160,360" stroke="#1a0e08" stroke-width="9"/>
        <path d="M-60,100L-120,200" stroke="#1a0e08" stroke-width="16" stroke-linecap="round"/><path d="M152,36l18,-24" stroke="#1a0e08" stroke-width="8"/></g></g>
      <g id="${id}-army"></g>`);
    put(L.glow, `<rect x="60" y="300" width="960" height="1200" fill="#ffd890" opacity=".08"/>`);
  }

  Hn.legend = (tl, id, t0, dur, L) => {
    // the "soldiers" pour out of the nest shadow and stream across the screen, all dark shapes
    const army = document.getElementById(`${id}-army`);
    Hn.swarm(tl, army, { id: `${id}-sw`, n: 26, s: 0.9, t0, dur, path: [[0, 760, 830], [dur * 0.45, 640, 900], [dur, 360, 1150]], rx: 200, ry: 140, chase: 0.6, grow: [0.2, 1.2], seed: 4 });
    tl.set(`#${id}-sw path, #${id}-sw ellipse`, { attr: { fill: "#1a0e08", stroke: "#1a0e08" } }, t0);
  };

  Object.assign(Sets, { hnYard, hnNest, hnLegend });
})();
