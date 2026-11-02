// "รูพญานาค" v2 sets (style frames v2): drawn in screen space (camera fr(540,960,1,540,960) = identity), closer and denser.
//   Sets.rupWorld2(L, o)  harvest morning in Loei: karst peaks + Mekong mist, plots in perspective (standing gold / cut stubble /
//                         straw stacks ลอมฟาง), the sim with naga stair rails, the broadcast tower, the village sign, a parked motorbike,
//                         the headman's pump and pipe by the canal, big foreground panicles. Low warm sun from the left, long shadows.
//   Sets.rupRim2(L, o)    close on the hole (o.time "night" | "day"): a torn rim, the inside wall in strata (topsoil · red laterite with
//                         nodules · clay · limestone), muddy water and rubble at the bottom, roots and rice clumps hanging in, rings of
//                         cracks spreading out, clods falling. Night: the lucky-number board, a stall (no logos) with bulbs, plastic
//                         chairs, villagers kneeling with incense on the far rim, a motorbike headlight raking across, smoke past camera.
//   Sets.rupCut2(L, o)    the cross-section as a 3D block (like ทะเลลด): ยาย's house, the well and the headman's pump on top; the water
//                         table drops while the pump runs, sand pours into the cave, the roof thins and gives (Rup.cutLife ids).
//   Rup2.phoneLight(L, x, y, fx, fy)  a soft wedge of screen light from a phone (x,y) up onto a face (fx,fy)
//   Rup2.life2(tl, id, t0, dur)       smoke drift, bulbs, clods, beam sweep, panicle sway
(function () {
  const Rup2 = (window.Rup2 = window.Rup2 || {});
  const f = (v) => (+v).toFixed(1);
  const LINE = "#2a1c16";
  const ln = (w = 3) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const rng = Rup.rng, mix = Rup.mix;

  Sets.DEFS += `
    <linearGradient id="r2SkyDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5c9ed8"/><stop offset=".5" stop-color="#a8d0ec"/><stop offset=".85" stop-color="#f8e2b8"/><stop offset="1" stop-color="#ffd59a"/></linearGradient>
    <linearGradient id="r2SkyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060a1c"/><stop offset=".6" stop-color="#121c40"/><stop offset="1" stop-color="#26325a"/></linearGradient>
    <linearGradient id="r2Mist" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6e4" stop-opacity="0"/><stop offset=".5" stop-color="#fff6e4" stop-opacity=".85"/><stop offset="1" stop-color="#fff6e4" stop-opacity="0"/></linearGradient>
    <linearGradient id="r2MistN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a9ac8" stop-opacity="0"/><stop offset=".5" stop-color="#8a9ac8" stop-opacity=".45"/><stop offset="1" stop-color="#8a9ac8" stop-opacity="0"/></linearGradient>
    <linearGradient id="r2Gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8c25a"/><stop offset="1" stop-color="#c8962e"/></linearGradient>
    <linearGradient id="r2Stub" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8a870"/><stop offset="1" stop-color="#a8844e"/></linearGradient>
    <linearGradient id="r2Water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6a44"/><stop offset="1" stop-color="#4a3420"/></linearGradient>
    <linearGradient id="r2Throat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".7" stop-color="#0a0604" stop-opacity=".75"/><stop offset="1" stop-color="#050302" stop-opacity=".95"/></linearGradient>
    <linearGradient id="r2Beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff4d0" stop-opacity=".75"/><stop offset="1" stop-color="#fff4d0" stop-opacity="0"/></linearGradient>
    <linearGradient id="r2BeamL" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#fff4d0" stop-opacity=".8"/><stop offset="1" stop-color="#fff4d0" stop-opacity="0"/></linearGradient>
    <linearGradient id="r2Phone" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#dcecff" stop-opacity=".8"/><stop offset="1" stop-color="#dcecff" stop-opacity="0"/></linearGradient>
    <radialGradient id="r2Pool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffc870" stop-opacity=".55"/><stop offset="1" stop-color="#ff9a40" stop-opacity="0"/></radialGradient>
    <radialGradient id="r2SunWash" cx=".1" cy=".45" r=".9"><stop offset="0" stop-color="#ffd890" stop-opacity=".5"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>`;

  // ---------------- world pieces ----------------
  // Loei karst: steep limestone towers with cliff faces, layered in haze
  Rup2.karst = (y, c, r, n = 7, h = 260, x0 = -200, x1 = 1300) => {
    let g = "";
    for (let k = 0; k < n; k++) { const cx = x0 + (k + r() * 0.6) * (x1 - x0) / n, w = 70 + r() * 90, hh = h * (0.6 + r() * 0.6), tilt = (r() - 0.5) * 30;
      const top = y - hh, cap = mix(c, "#5a8a5a", 0.16);
      g += `<path d="M${f(cx - w * 1.5)},${y}C${f(cx - w * 1.1)},${f(y - hh * 0.2)} ${f(cx - w * 1.02)},${f(y - hh * 0.5)} ${f(cx - w + tilt)},${f(top + hh * 0.18)}C${f(cx - w * 0.9 + tilt)},${f(top - 10)} ${f(cx - w * 0.2 + tilt)},${f(top - 26)} ${f(cx + w * 0.3 + tilt)},${f(top - 8)}C${f(cx + w * 0.9 + tilt)},${f(top + 6)} ${f(cx + w + tilt)},${f(top + hh * 0.2)} ${f(cx + w * 0.96)},${f(y - hh * 0.45)}C${f(cx + w * 1.05)},${f(y - hh * 0.2)} ${f(cx + w * 1.4)},${f(y - 8)} ${f(cx + w * 1.6)},${y}Z" fill="${c}"/>
        <path d="M${f(cx - w + tilt)},${f(top + hh * 0.18)}C${f(cx - w * 0.9 + tilt)},${f(top - 10)} ${f(cx - w * 0.2 + tilt)},${f(top - 26)} ${f(cx + w * 0.3 + tilt)},${f(top - 8)}C${f(cx + w * 0.9 + tilt)},${f(top + 6)} ${f(cx + w + tilt)},${f(top + hh * 0.2)} ${f(cx + w * 0.98)},${f(top + hh * 0.26)}Q${f(cx + tilt)},${f(top + hh * 0.12)} ${f(cx - w * 0.98 + tilt)},${f(top + hh * 0.3)}Z" fill="${cap}"/>
        ${[0, 1, 2].map((j) => `<path d="M${f(cx - w * 0.6 + j * w * 0.6 + tilt * 0.5)},${f(top + hh * 0.25)}l${f((r() - 0.5) * 10)},${f(hh * (0.3 + r() * 0.3))}" stroke="${mix(c, "#ffffff", 0.22)}" stroke-width="4" opacity=".55"/>`).join("")}`; }
    return g;
  };
  // a straw stack (ลอมฟาง): a dome of straw round a pole, lit on one side, with loose straw at its foot
  Rup2.stack = (x, y, s = 1, lit = "#f0d68a", sh = "#b8904e") => `<g transform="translate(${f(x)},${f(y)}) scale(${s})">
    <ellipse cx="34" cy="4" rx="120" ry="16" fill="#3a2a14" opacity=".28"/>
    <path d="M-70,0Q-76,-80 -20,-118Q0,-130 20,-118Q76,-80 70,0Z" fill="${sh}" ${ln(2.4)}/><path d="M-70,0Q-76,-80 -20,-118Q-6,-126 2,-122Q-30,-70 -24,0Z" fill="${lit}"/>
    ${Array.from({ length: 9 }, (_, k) => `<path d="M${-60 + k * 15},${-6 - (k % 3) * 4}q${(k - 4) * 2},-40 ${(k - 4) * 4},-${70 + (k % 2) * 20}" stroke="#8a6a34" stroke-width="1.6" fill="none" opacity=".55"/>`).join("")}
    <path d="M0,-124V-160" stroke="#5a3a1e" stroke-width="6"/>${[-50, -20, 20, 50].map((d) => `<path d="M${d - 10},0l${d > 0 ? 18 : -18},6" stroke="#d8b860" stroke-width="3"/>`).join("")}</g>`;
  // a sheaf of cut rice standing
  Rup2.sheaf = (x, y, s = 1) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})"><path d="M-14,0L-4,-60L4,-60L14,0Z" fill="#c8a050" ${ln(1.6)}/><path d="M-8,-36H8" stroke="#6a4a1e" stroke-width="4"/>
    ${[-14, -6, 2, 10].map((d) => `<path d="M${d},-60q${d * 1.6},-14 ${d * 2.6 + 6},-4" stroke="#e8c060" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
  // the village sim with naga stair balustrades
  Rup2.sim = (x, y, s = 1, tint = (c) => c) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})">
    ${Rup.sim(0, -40, 1)}
    <path d="M-80,-40L-80,0L80,0L80,-40Z" fill="${tint("#e8dcc4")}" ${ln(2.4)}/>${[0, 1, 2, 3].map((k) => `<path d="M-80,${-30 + k * 10}H80" stroke="${tint("#c8b89c")}" stroke-width="2"/>`).join("")}
    ${[-1, 1].map((d) => `<g transform="scale(${d},1)"><path d="M86,0Q120,-10 140,-60Q150,-90 128,-104" stroke="${LINE}" stroke-width="22" fill="none" stroke-linecap="round"/>
      <path d="M86,0Q120,-10 140,-60Q150,-90 128,-104" stroke="${tint("#3a8a5a")}" stroke-width="16" fill="none" stroke-linecap="round"/>
      <path d="M86,0Q120,-10 140,-60Q150,-90 128,-104" stroke="${tint("#f0c040")}" stroke-width="3" fill="none" stroke-dasharray="4 6"/>
      ${[0, 1, 2, 3, 4].map((k) => `<path d="M${118 + k * 6},${-112 - k * 2}q4,-18 12,-24" stroke="${tint("#f0c040")}" stroke-width="5" stroke-linecap="round" fill="none"/>`).join("")}
      <circle cx="122" cy="-104" r="3" fill="#fff"/></g>`).join("")}</g>`;
  // the broadcast tower (หอกระจายข่าว): a steel pole with three horn speakers and a little sign
  Rup2.tower = (x, y, s = 1, tint = (c) => c) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})">
    <path d="M-8,0L-3,-420H3L8,0Z" fill="${tint("#8a929a")}" ${ln(2)}/>${[1, 2, 3, 4, 5, 6].map((k) => `<path d="M-6,${-k * 60}L6,${-k * 60 - 30}" stroke="${tint("#6a727a")}" stroke-width="2"/>`).join("")}
    ${[[-1, -400, -18], [1, -400, 18], [-1, -330, -24]].map(([d, yy, a]) => `<g transform="translate(0,${yy}) rotate(${a})"><path d="M0,-6L${d * 44},-22L${d * 44},22L0,6Z" fill="${tint("#d8dcd8")}" ${ln(2)}/><ellipse cx="${d * 44}" cy="0" rx="7" ry="22" fill="${tint("#5a6066")}" ${ln(2)}/></g>`).join("")}
    <rect x="-46" y="-250" width="92" height="40" rx="5" fill="${tint("#2a6aa8")}" ${ln(2)}/><text x="0" y="-224" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="17" fill="#fff">หอกระจายข่าว</text></g>`;
  // the village sign (fictional village): a concrete board on two posts
  Rup2.vsign = (x, y, s = 1, tint = (c) => c) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})">
    <ellipse cx="20" cy="4" rx="170" ry="14" fill="#2a1a10" opacity=".3"/><path d="M-110,0V-150M110,0V-150" stroke="${tint("#c8c4b8")}" stroke-width="22"/><path d="M-110,0V-150M110,0V-150" stroke="${LINE}" stroke-width="2" opacity=".5"/>
    <rect x="-160" y="-290" width="320" height="150" rx="8" fill="${tint("#f2eee4")}" ${ln(3)}/><rect x="-148" y="-278" width="296" height="126" rx="4" fill="none" stroke="${tint("#2a6aa8")}" stroke-width="5"/>
    <text x="0" y="-228" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="${tint("#1a3a6a")}">บ้านโนนนาค</text>
    <text x="0" y="-182" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="24" fill="${tint("#1a3a6a")}">หมู่ 7 · จ.เลย</text>
    <path d="M-160,-150L160,-150" stroke="#000" stroke-width="5" opacity=".12"/><path d="M60,-290q8,40 -4,80" stroke="${tint("#6a6a5a")}" stroke-width="2" opacity=".4" fill="none"/></g>`;
  // a step-through motorbike parked on its stand (o.beam: headlight on, raking left)
  Rup2.moto = (x, y, s = 1, o = {}) => { const t = o.tint || ((c) => c), body = t(o.c || "#c8302a");
    return `<g transform="translate(${f(x)},${f(y)}) scale(${s * (o.flip ? -1 : 1)},${s})">
    <ellipse cx="0" cy="4" rx="150" ry="14" fill="#000" opacity=".35"/>
    ${[-96, 96].map((wx) => `<circle cx="${wx}" cy="-44" r="44" fill="${t("#1a1a1e")}" ${ln(2.4)}/><circle cx="${wx}" cy="-44" r="22" fill="${t("#9aa0a6")}" ${ln(2)}/><circle cx="${wx}" cy="-44" r="6" fill="${t("#3a3a40")}"/>`).join("")}
    <path d="M-96,-44L-30,-70L40,-70L96,-44" stroke="${t("#4a4a52")}" stroke-width="10" fill="none"/>
    <path d="M-120,-96Q-110,-130 -40,-130L20,-128Q40,-100 30,-80L-90,-80Q-118,-82 -120,-96Z" fill="${body}" ${ln(2.6)}/>
    <path d="M-110,-132Q-70,-146 -30,-136L-30,-128L-108,-124Z" fill="${t("#1a1a1e")}" ${ln(2.2)}/>
    <path d="M30,-80L70,-160L96,-170" stroke="${t("#6a6e74")}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M40,-80Q70,-120 110,-120L104,-80Z" fill="${body}" ${ln(2.4)}/>
    <path d="M86,-172H120" stroke="${t("#1a1a1e")}" stroke-width="10" stroke-linecap="round"/><path d="M100,-150l26,-4l4,22l-26,4Z" fill="${o.beam ? "#fff6d8" : t("#e8e4d8")}" ${ln(2)}/>
    <path d="M-20,-30l-10,40" stroke="${t("#4a4a52")}" stroke-width="6"/></g>`; };
  // the headman's pump: a diesel engine on a skid, flywheel, a fat blue PVC pipe into the canal and out to the field
  Rup2.pump = (x, y, s = 1, tint = (c) => c) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})">
    <ellipse cx="0" cy="6" rx="170" ry="18" fill="#000" opacity=".3"/><rect x="-130" y="-20" width="260" height="22" fill="${tint("#5a3a24")}" ${ln(2.4)}/>
    <rect x="-100" y="-130" width="150" height="110" rx="10" fill="${tint("#c83a2a")}" ${ln(3)}/><rect x="-90" y="-150" width="90" height="26" rx="5" fill="${tint("#3a3a40")}" ${ln(2.4)}/>
    <path d="M-60,-150V-200h18" stroke="${tint("#3a3a40")}" stroke-width="9" fill="none"/><circle cx="76" cy="-74" r="48" fill="${tint("#2a2a30")}" ${ln(3)}/><circle cx="76" cy="-74" r="10" fill="${tint("#9aa0a6")}"/>
    ${[0, 1, 2, 3].map((k) => `<path d="M${-86 + k * 10},-120v86" stroke="${tint("#9a2a1e")}" stroke-width="3"/>`).join("")}
    <path d="M-100,-60H-170Q-210,-60 -220,-20L-230,60" stroke="${LINE}" stroke-width="40" fill="none"/><path d="M-100,-60H-170Q-210,-60 -220,-20L-230,60" stroke="${tint("#2a7ac8")}" stroke-width="32" fill="none"/>
    <path d="M50,-110Q200,-140 330,-60L420,-30" stroke="${LINE}" stroke-width="40" fill="none"/><path d="M50,-110Q200,-140 330,-60L420,-30" stroke="${tint("#2a7ac8")}" stroke-width="32" fill="none"/>
    <path d="M60,-118Q200,-148 330,-68" stroke="#fff" stroke-width="5" fill="none" opacity=".35"/></g>`;
  // a plastic chair
  Rup2.chair = (x, y, s = 1, c = "#c8302a") => `<g transform="translate(${f(x)},${f(y)}) scale(${s})"><path d="M-40,0L-34,-60M40,0L34,-60" stroke="${mix(c, "#000", 0.25)}" stroke-width="8"/>
    <path d="M-46,-60H46L40,-74H-40Z" fill="${c}" ${ln(2)}/><path d="M-40,-74Q-44,-150 -30,-160H30Q44,-150 40,-74Z" fill="${c}" ${ln(2)}/>${[-16, 0, 16].map((d) => `<path d="M${d},-150V-96" stroke="${mix(c, "#000", 0.3)}" stroke-width="5"/>`).join("")}</g>`;
  // the stall: a table with cloth, a striped umbrella, incense bundles, garlands, candles, a tray of paper slips — no logos
  Rup2.stall = (x, y, s = 1, o = {}) => { const t = o.tint || ((c) => c);
    return `<g transform="translate(${f(x)},${f(y)}) scale(${s})">
    <ellipse cx="0" cy="6" rx="200" ry="18" fill="#000" opacity=".3"/><path d="M0,0V-330" stroke="${t("#5a5a5a")}" stroke-width="7"/>
    <path d="M-220,-300Q0,-380 220,-300L200,-288Q0,-350 -200,-288Z" fill="${t("#e8e4dc")}" ${ln(2.4)}/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${-220 + k * 74},${-300 + Math.abs(k - 3) * 6}L0,-352L${-146 + k * 74},${-300 + Math.abs(k - 2) * 6}Z" fill="${t(k % 2 ? "#2a6ac8" : "#e8e4dc")}" opacity=".95"/>`).join("")}
    <rect x="-170" y="-110" width="340" height="18" fill="${t("#8a5a3a")}" ${ln(2)}/><path d="M-170,-92H170L160,0H-160Z" fill="${t("#d8402a")}" ${ln(2)}/>
    <path d="M-170,-92${Array.from({ length: 8 }, (_, k) => `q21,16 42.5,0`).join("")}" stroke="${t("#f0c040")}" stroke-width="5" fill="none"/>
    ${[-130, -100, -70].map((d, k) => `<g transform="translate(${d},-110)"><path d="M-10,0L-6,-70M0,0V-72M10,0L6,-70" stroke="${t("#c8402a")}" stroke-width="4"/><path d="M-12,-30H12" stroke="${t("#f0d050")}" stroke-width="7"/></g>`).join("")}
    ${[-20, 30, 80].map((d) => `<g transform="translate(${d},-112)"><path d="M-22,0q22,-50 44,0" fill="none" stroke="${t("#f09a20")}" stroke-width="10" stroke-dasharray="2 7" stroke-linecap="round"/></g>`).join("")}
    <rect x="110" y="-130" width="50" height="20" fill="${t("#f6f2e8")}" ${ln(1.6)}/>${[0, 1, 2].map((k) => `<rect x="${114 + k * 14}" y="-128" width="10" height="16" fill="${t("#e8c8a0")}" ${ln(1)}/>`).join("")}
    ${o.bulbs ? `<path d="M-210,-296Q-100,-250 0,-268T210,-296" stroke="#2a2a2a" stroke-width="2" fill="none"/>${Array.from({ length: 9 }, (_, k) => { const bx = -200 + k * 50, by = -284 + Math.sin(k * 0.9) * 10 + (k > 0 && k < 8 ? 16 : 0); return `<g class="${o.id}-bulb"><path d="M${bx},${by}v8" stroke="#2a2a2a" stroke-width="2"/><ellipse cx="${bx}" cy="${by + 16}" rx="7" ry="9" fill="#fff0b8" stroke="#a88a40" stroke-width="1.4"/></g>`; }).join("")}` : ""}</g>`; };
  // a static lucky-number board in the world (the opening card animates its own copy)
  Rup2.board = (x, y, s = 1, nums = [9, 2, 7], tint = (c) => c) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})">
    <path d="M-170,0L-150,-260M170,0L150,-260" stroke="${tint("#5a3418")}" stroke-width="14"/><ellipse cx="0" cy="6" rx="210" ry="16" fill="#000" opacity=".3"/>
    <rect x="-210" y="-470" width="420" height="230" rx="10" fill="${tint("#6a3418")}" ${ln(3)}/>
    <clipPath id="r2bc${Math.round(x)}"><rect x="-206" y="-466" width="412" height="30"/></clipPath><g clip-path="url(#r2bc${Math.round(x)})">${RupUI.scales(-210, -472, 420, 2, 22, tint("#e0a83a"), tint("#c88a2a"))}</g>
    <rect x="-190" y="-430" width="380" height="172" rx="6" fill="${tint("#22302a")}" ${ln(2)}/>
    <text x="0" y="-392" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="${tint("#ffd84a")}">เลขเด็ดรูพญานาค</text>
    ${nums.map((d, k) => `<rect x="${-140 + k * 100}" y="-372" width="80" height="100" rx="8" fill="#0e0a08" ${ln(2)}/><text x="${-100 + k * 100}" y="-292" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="80" fill="${tint("#f6efe0")}">${d}</text>`).join("")}</g>`;

  // a soft wedge of phone light up onto a face, and a candle's light pool on the ground (flattened, not a glow ball)
  Rup2.phoneLight = (L, x, y, fx, fy, w = 90) => put(L.light, `<path d="M${x - 10},${y}L${fx - w},${fy}Q${fx},${fy - w * 0.6} ${fx + w},${fy}L${x + 10},${y}Z" fill="url(#r2Phone)" style="mix-blend-mode:screen" opacity=".55"/>
    <ellipse cx="${fx}" cy="${fy + 10}" rx="${w * 0.7}" ry="${w * 0.55}" fill="#dcecff" opacity=".12" style="mix-blend-mode:screen"/>`);
  Rup2.pool = (x, y, rx, ry = rx * 0.28) => `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx)}" ry="${f(ry)}" fill="url(#r2Pool)" style="mix-blend-mode:screen"/>`;
  // foreground panicles: big, sharp, heavy heads drooping, framing the bottom edge
  Rup2.fgRice = (x0, x1, yb, r, tint = (c) => c, n = 22) => { let g = "";
    for (let k = 0; k < n; k++) { const x = x0 + (k + r() * 0.8) * (x1 - x0) / n, h = 380 + r() * 320, lean = (r() - 0.4) * 120, c = k % 3 ? "#b8902e" : "#d8b048";
      g += `<path d="M${f(x)},${yb}Q${f(x + lean * 0.3)},${f(yb - h * 0.6)} ${f(x + lean)},${f(yb - h)}" stroke="${tint("#6a7a2a")}" stroke-width="11" fill="none" stroke-linecap="round"/>
        <path d="M${f(x + lean - 40)},${f(yb - h - 30)}Q${f(x)},${f(yb - h * 1.2)} ${f(x + lean * 0.7)},${f(yb - h * 0.7)}" stroke="${tint("#7a8a34")}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".8"/>`;
      let p = ""; for (let j = 0; j < 11; j++) { const u = j / 10, px = x + lean + u * (lean > 0 ? 70 : -70) + Math.sin(u * 3) * 14, py = yb - h + u * 190;
        p += `<ellipse cx="${f(px)}" cy="${f(py)}" rx="11" ry="20" fill="${tint(j % 2 ? c : "#f0d070")}" stroke="${tint("#7a5a1a")}" stroke-width="1.4" transform="rotate(${f(-20 + u * 30)} ${f(px)} ${f(py)})"/>`; }
      g += `<g class="r2-pan">${p}</g>`; }
    return g; };

  // ---------------- the field world, closer ----------------
  Sets.rupWorld2 = (L, o = {}) => {
    const id = o.id || "rw2", r = rng(o.seed || 41), HZ = o.horizon ?? 760;
    let sky = `<rect x="-600" y="-400" width="2300" height="${HZ + 500}" fill="url(#r2SkyDay)"/><circle cx="120" cy="${HZ - 90}" r="58" fill="#fff4d0"/>`;
    for (let k = 0; k < 6; k++) { const cx = -100 + k * 260 + r() * 80, cy = 140 + (k % 3) * 90, w = 220 + r() * 160; let c = "";
      for (let j = 0; j < 6; j++) c += `<ellipse cx="${f(cx + (j - 2.5) * w * 0.16)}" cy="${f(cy - Math.sin(j / 5 * Math.PI) * 34)}" rx="${f(w * 0.17)}" ry="${f(30 + r() * 14)}"/>`;
      sky += `<g fill="#fffaf0" opacity=".9">${c}</g><ellipse cx="${f(cx)}" cy="${f(cy + 18)}" rx="${f(w * 0.5)}" ry="16" fill="#f0d8c0" opacity=".9"/>`; }
    put(L.sky, sky);
    let far = Rup2.karst(HZ - 40, "#9aaecc", r, 8, 300) + Rup2.karst(HZ - 10, "#7f96b8", r, 7, 220) + `<rect x="-600" y="${HZ - 40}" width="2300" height="70" fill="url(#r2Mist)"/>`;
    far += `<rect x="-600" y="${HZ}" width="2300" height="40" fill="#c8d2cc"/><rect x="-600" y="${HZ - 30}" width="2300" height="110" fill="url(#r2Mist)"/>`;
    for (let k = 0; k < 14; k++) far += Rup.palm(-200 + k * 110 + r() * 50, HZ + 70 + r() * 10, 120 + r() * 60, 0.62, "#4a6a48", r);
    put(L.far, far);
    let mid = `<rect x="-600" y="${HZ + 60}" width="2300" height="120" fill="#7a9a4a"/>`;
    for (let k = 0; k < 6; k++) mid += Rup.bamboo(-100 + k * 240 + r() * 60, HZ + 150, 150 + r() * 40, 0.8, "#5a8a3a", r);
    mid += Rup2.sim(250, HZ + 160, 0.5);
    mid += Rup.house(760, HZ + 168, 0.42, { granary: true, wall: "#8a5a3a", roof: "#7a8a96", cloth: "#3a6ac8" });
    for (let k = 0; k < 7; k++) mid += Rup.tree(-80 + k * 200 + r() * 60, HZ + 172, 120 + r() * 50, ["#3e6a34", "#4a7a3a", "#36602e"][k % 3], r);
    mid += Rup2.tower(980, HZ + 175, 0.75);
    put(L.mid, mid);
    // plots: rows of fields in perspective, separated by bunds, mixed gold / stubble / stacks
    const GY = HZ + 170, VX = 540, VY = HZ - 260;
    let s = `<rect x="-600" y="${GY}" width="2300" height="${2200 - GY}" fill="url(#r2Gold)"/>`;
    const rows = [GY, GY + 50, GY + 130, GY + 260, GY + 470, GY + 800, 2100], cols = [-1400, -700, -150, 300, 760, 1250, 1900, 2600];
    const xAt = (cx, yy) => VX + (cx - VX) * (yy - VY) / (2100 - VY);
    for (let i = 0; i < rows.length - 1; i++) for (let j = 0; j < cols.length - 1; j++) {
      const ya = rows[i], yb = rows[i + 1], p = [[xAt(cols[j], ya), ya], [xAt(cols[j + 1], ya), ya], [xAt(cols[j + 1], yb), yb], [xAt(cols[j], yb), yb]];
      const kind = o.plots ? o.plots[(i * 7 + j) % o.plots.length] : ["g", "c", "g", "s", "g", "c", "g"][(i * 3 + j * 2) % 7];
      const d = `M${p.map((q) => q.map(f).join(",")).join("L")}Z`, t = (ya - GY) / (2100 - GY);
      s += `<clipPath id="${id}-p${i}${j}"><path d="${d}"/></clipPath><g clip-path="url(#${id}-p${i}${j})"><path d="${d}" fill="${kind === "g" ? "url(#r2Gold)" : "url(#r2Stub)"}"/>`;
      const n = Math.round(40 + (yb - ya) * 1.2), sz = 4 + t * 26;
      for (let q = 0; q < n; q++) { const yy = ya + r() * (yb - ya), xx = xAt(cols[j] + r() * (cols[j + 1] - cols[j]), yy), sc = 0.3 + (yy - GY) / (2100 - GY) * 1.6;
        if (kind === "g") s += `<path d="M${f(xx)},${f(yy)}q${f(-3 * sc)},${f(-14 * sc)} ${f(-9 * sc)},${f(-20 * sc)}M${f(xx)},${f(yy)}q${f(2 * sc)},${f(-16 * sc)} ${f(8 * sc)},${f(-22 * sc)}" stroke="${r() > 0.5 ? "#f6d878" : "#a87a20"}" stroke-width="${f(1 + sc * 2.4)}" fill="none" stroke-linecap="round"/>`;
        else s += `<path d="M${f(xx)},${f(yy)}v${f(-6 * sc)}M${f(xx + 4 * sc)},${f(yy)}v${f(-5 * sc)}" stroke="${r() > 0.5 ? "#8a6a3a" : "#d8c088"}" stroke-width="${f(0.8 + sc * 1.6)}"/>`; }
      if (kind === "s") { const cx = (p[0][0] + p[1][0] + p[2][0] + p[3][0]) / 4, cy = (ya + yb) / 2 + (yb - ya) * 0.2, sc = 0.25 + (cy - GY) / (2100 - GY) * 1.5;
        s += Rup2.stack(cx - 60 * sc, cy, sc) + Rup2.stack(cx + 90 * sc, cy + 10 * sc, sc * 0.85) + Rup2.sheaf(cx + 20 * sc, cy + 30 * sc, sc) + Rup2.sheaf(cx + 50 * sc, cy + 34 * sc, sc); }
      if (kind === "c") { const cx = (p[0][0] + p[2][0]) / 2, cy = (ya + yb) / 2, sc = 0.25 + (cy - GY) / (2100 - GY) * 1.5; s += Rup2.sheaf(cx, cy, sc) + Rup2.sheaf(cx + 40 * sc, cy + 6 * sc, sc); }
      s += `</g>`;
      s += `<path d="${d}" fill="none" stroke="#9a7a48" stroke-width="${f(2 + t * 18)}" stroke-linejoin="round"/><path d="${d}" fill="none" stroke="#6a8a3a" stroke-width="${f(0.6 + t * 4)}" stroke-linejoin="round" opacity=".7"/>`; }
    // the dirt road from camera to the village
    s += `<path d="M${o.roadX ?? 380},2100C${(o.roadX ?? 380) + 40},1500 520,1100 560,${GY}L600,${GY}C640,1100 ${(o.roadX ?? 380) + 420},1500 ${(o.roadX ?? 380) + 560},2100Z" fill="#c8a878" ${ln(2)}/>
      <path d="M${(o.roadX ?? 380) + 200},2100C${(o.roadX ?? 380) + 230},1500 560,1100 580,${GY}" stroke="#a88a5a" stroke-width="10" fill="none" opacity=".5"/>`;
    // the canal + the headman's pump at the right
    s += `<path d="M900,${GY + 120}Q980,1300 1300,1500L1300,1600Q940,1360 860,${GY + 120}Z" fill="#6a8aa0"/><path d="M880,${GY + 130}Q960,1320 1300,1520" stroke="#cfe0ea" stroke-width="3" fill="none" opacity=".6"/>`;
    s += Rup2.pump(990, 1330, 0.5);
    // the village sign at the left of the road, the motorbike by it
    s += Rup2.vsign(170, 1380, 0.9) + Rup2.moto(250, 1470, 0.7, { c: "#2a6ac8" });
    // sun wash: warm low light from the left
    put(L.set, s);
    put(L.light, `<rect x="0" y="0" width="1080" height="1920" fill="url(#r2SunWash)" style="mix-blend-mode:screen"/>`);
    if (o.fgRice !== false) put(L.fg, `<g id="${id}-fg">${Rup2.fgRice(-120, 200, 2000, rng(5), (c) => c, 6)}${Rup2.fgRice(900, 1200, 2000, rng(9), (c) => c, 5)}</g>`);
  };

  // ---------------- close on the hole ----------------
  Rup2.hole = (o) => {
    const id = o.id, x = o.x, y = o.y, rx = o.rx, ry = o.ry, t = o.tint || ((c) => c), r = rng(o.seed || 77), N = 72;
    const R = (a) => 1 + 0.07 * Math.sin(3 * a + 0.7) + 0.045 * Math.sin(7 * a + 2.1) + 0.03 * Math.sin(13 * a);
    const pts = Array.from({ length: N }, (_, k) => { const a = (k / N) * Math.PI * 2, j = 1 + (r() - 0.5) * 0.05; return [Math.cos(a) * rx * R(a) * j, Math.sin(a) * ry * R(a) * j]; });
    const rim = `M${pts.map((p) => p.map(f).join(",")).join("L")}Z`;
    let g = `<g id="${id}-hole" transform="translate(${x},${y})">`;
    // cracks: concentric jagged arcs and radial splits spreading out
    for (let k = 0; k < (o.nc ?? 10); k++) { const Rk = 1.18 + (k % 4) * 0.16 + r() * 0.05, a0 = (r() * 2 - 1) * Math.PI, a1 = a0 + 0.5 + r() * 1.1;
      let d = ""; for (let j = 0; j <= 18; j++) { const a = a0 + (a1 - a0) * j / 18, jj = (r() - 0.5) * 0.05; d += `${j ? "L" : "M"}${f(Math.cos(a) * rx * (Rk + jj))},${f(Math.sin(a) * ry * (Rk + jj) * 1.06)}`; }
      g += `<path id="${id}-ck${k}" class="${id}-ck" d="${d}" stroke="${t("#24160c")}" stroke-width="${f(3 + r() * 3)}" fill="none" stroke-linecap="round" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="0"/>`; }
    for (let k = 0; k < 14; k++) { const a = r() * Math.PI * 2, r0 = 1.05, r1 = 1.3 + r() * 0.5; let d = `M${f(Math.cos(a) * rx * r0)},${f(Math.sin(a) * ry * r0)}`;
      for (let j = 1; j <= 5; j++) { const rr = r0 + (r1 - r0) * j / 5, aa = a + (r() - 0.5) * 0.12; d += `L${f(Math.cos(aa) * rx * rr)},${f(Math.sin(aa) * ry * rr)}`; }
      g += `<path d="${d}" stroke="${t("#2a1a0e")}" stroke-width="${f(2 + r() * 2)}" fill="none" stroke-linecap="round"/>`; }
    // slumped broken ground ring
    g += `<path d="${rim}" transform="scale(1.12,1.2)" fill="${t("#7a5a32")}"/>`;
    for (let k = 0; k < 30; k++) { const a = (k / 30) * Math.PI * 2, rr = 1.04 + r() * 0.12, cx = Math.cos(a) * rx * rr, cy = Math.sin(a) * ry * rr;
      g += `<path d="M${f(cx - 14)},${f(cy)}l${f(10 + r() * 10)},${f(-8 - r() * 6)}l${f(16 + r() * 8)},${f(5 + r() * 5)}l-6,10Z" fill="${t(k % 2 ? "#5a3e20" : "#9a7a48")}" ${ln(1.4)}/>`; }
    // inside: strata on the far wall, darkening to a muddy pool with rubble
    const D = ry * 1.25;
    g += `<clipPath id="${id}-hc"><path d="${rim}"/></clipPath><g clip-path="url(#${id}-hc)">`;
    const farPts = pts.slice(N / 2).concat([pts[0]]);
    const arc = (dy, sc) => farPts.map((p) => [p[0] * sc, p[1] * sc + dy]);
    const bandPath = (d0, d1, s0, s1) => { const A = arc(d0, s0), B = arc(d1, s1).reverse(); return `M${A.map((p) => p.map(f).join(",")).join("L")}L${B.map((p) => p.map(f).join(",")).join("L")}Z`; };
    g += `<rect x="${-rx * 1.3}" y="${-ry * 1.3}" width="${rx * 2.6}" height="${ry * 2.6}" fill="${t("#0c0806")}"/>`;
    const bands = [[0, 0.12, "#3a2414"], [0.12, 0.42, "#a8442a"], [0.42, 0.66, "#a88a62"], [0.66, 1.0, "#bab4a2"], [1.0, 1.3, "#5a5448"]];
    bands.forEach(([a0, b0, c], k) => { const d0 = a0 * ry * 0.95, d1 = b0 * ry * 0.95, s0 = 1 - a0 * 0.12, s1 = 1 - b0 * 0.12;
      g += `<path d="${bandPath(d0, d1, s0, s1)}" fill="${t(c)}"/><path d="M${arc(d1, s1).map((p) => p.map(f).join(",")).join("L")}" stroke="${t(mix(c, "#000000", 0.35))}" stroke-width="3" fill="none"/>`; });
    for (let k = 0; k < 40; k++) { const q = farPts[Math.floor(r() * farPts.length)], dd = (0.14 + r() * 0.26) * ry * 0.95, sc = 1 - (dd / ry) * 0.12; g += `<ellipse cx="${f(q[0] * sc)}" cy="${f(q[1] * sc + dd)}" rx="${f(3 + r() * 5)}" ry="${f(2 + r() * 3)}" fill="${t("#6a2414")}" opacity=".75"/>`; }
    for (let k = 0; k < 16; k++) { const q = farPts[Math.floor(r() * farPts.length)], dd = (0.68 + r() * 0.26) * ry * 0.95, sc = 1 - (dd / ry) * 0.12; g += `<path d="M${f(q[0] * sc)},${f(q[1] * sc + dd)}h${f(24 + r() * 26)}v${f(14 + r() * 10)}h${f(-24 - r() * 26)}Z" fill="none" stroke="${t("#8a8270")}" stroke-width="2"/>`; }
    for (let k = 0; k < 22; k++) { const q = farPts[Math.floor(r() * farPts.length)]; g += `<path d="M${f(q[0])},${f(q[1])}q${f((r() - 0.5) * 16)},${f(20 + r() * 30)} ${f((r() - 0.5) * 10)},${f(40 + r() * 70)}" stroke="${t("#24160c")}" stroke-width="${f(1.4 + r() * 1.8)}" fill="none"/>`; }
    // shadow falling down the wall into the throat
    g += `<path d="${bandPath(ry * 0.6, ry * 1.4, 0.93, 0.8)}" fill="url(#r2Throat)"/>`;
    g += `<ellipse id="${id}-pool" cx="0" cy="${f(ry * 0.62)}" rx="${f(rx * 0.42)}" ry="${f(ry * 0.16)}" fill="${t("#3a2a18")}"/><ellipse cx="0" cy="${f(ry * 0.6)}" rx="${f(rx * 0.4)}" ry="${f(ry * 0.13)}" fill="${t("#5a4026")}" opacity=".9"/>
      <path d="M${f(-rx * 0.18)},${f(ry * 0.6)}h${f(rx * 0.12)}M${f(rx * 0.06)},${f(ry * 0.64)}h${f(rx * 0.14)}" stroke="${t("#a88a60")}" stroke-width="2.4" opacity=".6"/>`;
    for (let k = 0; k < 9; k++) { const bx = (r() - 0.5) * rx * 0.8, by = ry * (0.52 + r() * 0.18); g += `<path d="M${f(bx)},${f(by)}l${f(8 + r() * 12)},${f(-6 - r() * 6)}l${f(10 + r() * 8)},${f(5 + r() * 3)}l-3,6Z" fill="${t(k % 2 ? "#3a3026" : "#5a4e40")}"/>`; }
    // the near wall's overhang shadow just under the near lip
    g += `<path d="M${pts.slice(0, N / 2 + 1).map((p) => p.map(f).join(",")).join("L")}L${f(-rx * 0.9)},${f(ry * 0.2)}Q0,${f(ry * 0.55)} ${f(rx * 0.9)},${f(ry * 0.2)}Z" fill="#000" opacity=".55"/>`;
    g += `</g>`;
    // the near lip: torn edge seen from the front, undercut, roots and rice clumps hanging into the dark
    const near = pts.slice(0, N / 2 + 1);
    g += `<path d="M${near.map((p) => p.map(f).join(",")).join("L")}L${f(-rx * 1.02)},${f(ry * 0.22)}Q0,${f(ry * 1.3)} ${f(rx * 1.02)},${f(ry * 0.22)}Z" fill="${t("#3a2414")}" opacity=".0"/>`;
    g += `<path d="M${near.map((p) => p.map(f).join(",")).join("L")}" fill="none" stroke="${t("#2a180c")}" stroke-width="16" stroke-linejoin="round"/>
      <path d="M${near.map((p) => p.map(f).join(",")).join("L")}" fill="none" stroke="${t("#6a4424")}" stroke-width="6" stroke-linejoin="round" transform="translate(0,6)"/>`;
    const far = pts.slice(N / 2);
    g += `<path d="M${far.map((p) => p.map(f).join(",")).join("L")}" fill="none" stroke="${t(o.night ? "#9ab0d8" : "#e8c890")}" stroke-width="5" stroke-linejoin="round"/>`;
    for (let k = 0; k < 22; k++) { const p = near[Math.floor(r() * near.length)], len = 30 + r() * 80;
      g += `<path d="M${f(p[0])},${f(p[1])}q${f((r() - 0.5) * 20)},${f(len * 0.5)} ${f((r() - 0.5) * 26)},${f(len)}" stroke="${t("#2a1a0e")}" stroke-width="${f(1.6 + r() * 2)}" fill="none" stroke-linecap="round" class="${id}-root"/>`; }
    for (let k = 0; k < 7; k++) { const p = near[3 + Math.floor(r() * (near.length - 6))]; const cx = p[0], cy = p[1] + 6;
      g += `<g transform="translate(${f(cx)},${f(cy)})" class="${id}-clump"><ellipse cx="0" cy="0" rx="22" ry="10" fill="${t("#5a3a1e")}" ${ln(1.6)}/>${[-14, -6, 2, 10].map((d) => `<path d="M${d},4q${d * 0.4},40 ${d * 1.2},70" stroke="${t(d % 4 ? "#c89a3a" : "#e8c060")}" stroke-width="4" fill="none" stroke-linecap="round"/><ellipse cx="${d * 1.2}" cy="76" rx="5" ry="10" fill="${t("#e8c060")}"/>`).join("")}</g>`; }
    // rice at the far lip leaning in
    for (let k = 0; k < 40; k++) { const p = far[Math.floor(r() * far.length)]; g += `<path d="M${f(p[0])},${f(p[1])}q${f(-p[0] * 0.05)},-26 ${f(-p[0] * 0.14)},-40" stroke="${t(k % 2 ? "#e8c060" : "#b88a2a")}" stroke-width="4" fill="none" stroke-linecap="round"/>`; }
    g += `</g>`;
    // falling clods
    g += `<g transform="translate(${x},${y})">${Array.from({ length: 12 }, (_, k) => `<path class="${id}-clod" d="M${f((r() - 0.5) * rx * 1.4)},${f(ry * (0.2 + r() * 0.4))}l6,-5l7,4l-3,7l-8,1Z" fill="${t("#5a3a1e")}" opacity="0"/>`).join("")}</g>`;
    return g;
  };

  Sets.rupRim2 = (L, o = {}) => {
    const id = o.id || "rr2", night = (o.time || "night") === "night", r = rng(o.seed || 13), HZ = o.horizon ?? 520;
    const t = (c) => night ? mix(c, "#18224a", 0.6) : c;
    let sky = `<rect x="-600" y="-400" width="2300" height="${HZ + 600}" fill="url(#${night ? "r2SkyNight" : "r2SkyDay"})"/>`;
    if (night) { for (let k = 0; k < 70; k++) sky += `<circle cx="${f(-100 + r() * 1300)}" cy="${f(-100 + r() * (HZ + 50))}" r="${f(0.8 + r() * 1.6)}" fill="#f4f0ff" opacity="${f(0.3 + r() * 0.6)}"/>`;
      sky += `<circle cx="860" cy="150" r="40" fill="#f8f2dc"/><circle cx="848" cy="142" r="8" fill="#e4dcc0"/>`; }
    put(L.sky, sky);
    put(L.far, Rup2.karst(HZ + 30, t("#6a7aa0"), r, 7, 200) + `<rect x="-600" y="${HZ}" width="2300" height="80" fill="url(#${night ? "r2MistN" : "r2Mist"})"/>`);
    let mid = `<rect x="-600" y="${HZ + 40}" width="2300" height="140" fill="${t("#5a7a3e")}"/>`;
    for (let k = 0; k < 6; k++) mid += Rup.bamboo(-100 + k * 240 + r() * 60, HZ + 140, 140, 0.8, t("#4a7a34"), r);
    mid += Rup.house(160, HZ + 150, 0.38, { granary: false, wall: t("#8a5a3a"), roof: t("#7a8a96") }) + Rup2.tower(930, HZ + 160, 0.6, t);
    for (let k = 0; k < 5; k++) mid += Rup.palm(-40 + k * 280 + r() * 60, HZ + 160, 200, 0.85, t("#3a5a34"), r);
    put(L.mid, mid);
    const GY = HZ + 150;
    let s = `<rect x="-600" y="${GY}" width="2300" height="${2200 - GY}" fill="${t("#9a7a40")}"/>`;
    for (let k = 0; k < 900; k++) { const yy = GY + Math.pow(r(), 1.3) * (2100 - GY), sc = 0.3 + (yy - GY) / (2100 - GY) * 1.4, xx = -100 + r() * 1300;
      s += `<path d="M${f(xx)},${f(yy)}q${f(-3 * sc)},${f(-14 * sc)} ${f(-9 * sc)},${f(-20 * sc)}" stroke="${t(r() > 0.5 ? "#e8c868" : "#8a6a24")}" stroke-width="${f(1 + sc * 2)}" fill="none" stroke-linecap="round"/>`; }
    s += `<path d="M-100,${GY + 60}Q540,${GY + 40} 1200,${GY + 70}" stroke="${t("#a88a5a")}" stroke-width="14" fill="none"/>`;
    // far rim props (behind the hole)
    const hy = o.holeY ?? 1240;
    if (o.props !== false) {
      s += Rup2.board(150, hy - 230, 0.62, [9, 2, 7], t) + Rup2.stall(860, hy - 250, 0.55, { tint: t, bulbs: night, id }) + Rup2.chair(700, hy - 220, 0.5, t("#c8302a")) + Rup2.chair(740, hy - 214, 0.5, t("#2a6ac8"));
      s += Rup2.moto(1040, hy - 160, 0.6, { tint: t, c: "#c8302a", beam: night, flip: true });
    }
    put(L.set, s);
    if (o.pumpAt) { const q = o.pumpAt;
      put(L.set, `<g transform="translate(${q.x},${q.y}) scale(${q.s ?? 1})">${Rup2.pump(0, 0, 1, t)}
        <g id="${id}-gush" transform="translate(420,-30)">${[0, 1, 2, 3, 4].map((k) => `<path class="${id}-gw" d="M0,0q${40 + k * 12},${-20 + k * 6} ${90 + k * 20},${60 + k * 14}" stroke="#cfe6f4" stroke-width="${10 - k}" fill="none" stroke-linecap="round" stroke-dasharray="18 14" opacity=".85"/>`).join("")}</g></g>`); }
    if (o.rope) { const hx = o.holeX ?? 540, hr = o.rx ?? 400, hv = o.ry ?? 150; let r2 = "";
      const pts = Array.from({ length: 10 }, (_, k) => { const a = (k / 10) * Math.PI * 2; return [hx + Math.cos(a) * hr * 1.55, hy + Math.sin(a) * hv * 1.75]; });
      pts.forEach(([px, py]) => { r2 += `<path d="M${f(px)},${f(py)}v-90" stroke="#5a3a1e" stroke-width="8"/>`; });
      r2 += `<path d="M${pts.concat([pts[0]]).map(([px, py]) => `${f(px)},${f(py - 76)}`).join("L")}" stroke="#d8241e" stroke-width="5" fill="none"/>`;
      put(L.set, r2); }
    put(L.set, Rup2.hole({ id, x: o.holeX ?? 540, y: hy, rx: o.rx ?? 400, ry: o.ry ?? 150, tint: t, night, nc: 12 }));
    // offerings on the near-ish rim: incense pots and candles with ground light pools
    if (o.offer !== false) { let g = "";
      [[-0.95, -0.85], [0.75, -0.95], [-1.15, 0.2], [1.1, 0.3]].forEach(([u, v], k) => { const px = (o.holeX ?? 540) + u * (o.rx ?? 400), py = hy + v * (o.ry ?? 150) * 1.4;
        g += `<g transform="translate(${f(px)},${f(py)})"><rect x="-22" y="-28" width="44" height="28" rx="5" fill="${t("#7aa04a")}" ${ln(2)}/>${[-12, -4, 4, 12].map((dx) => `<path d="M${dx},-28L${dx + (r() - 0.5) * 6},-86" stroke="#c8402a" stroke-width="3"/><circle cx="${dx}" cy="-87" r="2.6" fill="#ffcf6a"/>`).join("")}
          <path d="M-26,6q26,18 52,0" stroke="#f0a020" stroke-width="10" fill="none" stroke-dasharray="2 8" stroke-linecap="round"/>
          <rect x="30" y="-40" width="8" height="34" fill="#fff8e8" ${ln(1.4)}/><path class="${id}-fl" d="M34,-40q-6,-10 0,-20q6,10 0,20Z" fill="#ffd060"/></g>`;
        if (night) g += Rup2.pool(px + 20, py + 4, 110); });
      put(L.set, g); }
    // smoke drifting across the camera
    put(L.fg, `<g id="${id}-smoke" opacity="${night ? 0.5 : 0.35}">${[0, 1, 2].map((k) => `<path d="M${-200 + k * 120},${1500 - k * 260}c120,-60 220,40 360,-20s260,-60 380,10s240,20 420,-40" stroke="#e8e4dc" stroke-width="${40 - k * 8}" fill="none" stroke-linecap="round" filter="url(#rpBlur16)"/>`).join("")}</g>`);
    if (night && o.beam !== false) put(L.light, `<path id="${id}-beam" d="M974,${hy - 250}L-200,${hy - 430}L-200,${hy - 40}Z" fill="url(#r2BeamL)" style="mix-blend-mode:screen" opacity=".55"/>`);
    if (o.fgRice !== false) put(L.fg, `<g id="${id}-fg">${Rup2.fgRice(-120, 180, 2000, rng(3), t, 5)}${Rup2.fgRice(920, 1200, 2000, rng(8), t, 4)}</g>`);
  };

  // ---------------- the 3D block cutaway ----------------
  Sets.rupCut2 = (L, o = {}) => {
    Sets.rupCut(L, { ...o, pump: false });
    const id = o.id || "rc";
    // on the top skin: ยาย's house (left), the concrete well with its casing going down, the headman's pump with its blue pipe (right)
    let g = Rup.house(250, 668, 0.5, { granary: true, wall: "#8a5a3a", roof: "#7a8a96", cloth: "#c8403a" });
    const px = 820, face = 700, pumpY = o.pumpY ?? 1500;
    g += `<rect x="${px - 9}" y="${face - 40}" width="18" height="${pumpY - face + 40}" fill="#9aa6ae" ${ln(2.4)}/><rect x="${px - 20}" y="${pumpY}" width="40" height="70" rx="8" fill="#5a6a78" ${ln(2.4)}/>
      ${[0, 1, 2, 3, 4].map((k) => `<path id="${id}-arrow${k}" d="M${px},${pumpY - 40 - k * 150}l-14,22h28Z" fill="#2a7ab8" opacity="0"/>`).join("")}
      ${Rup2.pump(px + 40, face - 34, 0.42)}
      <g transform="translate(560,${face - 30})"><rect x="-40" y="-30" width="80" height="34" fill="#c8c4b8" ${ln(2)}/><ellipse cx="0" cy="-30" rx="40" ry="10" fill="#d8d4c8" ${ln(2)}/><ellipse cx="0" cy="-29" rx="32" ry="7" fill="#7a5a3a"/></g>
      <path d="M560,${face - 20}V${face + 200}" stroke="#9aa6ae" stroke-width="8" opacity=".8"/>`;
    for (let k = 0; k < 4; k++) g += Rup2.sheaf(120 + k * 50, 690, 0.55);
    put(L.set, g);
  };

  // rain (rule V1b, owner 2 Nov 2569: "ดูแล้วปวดตามาก ฝนมันเยอะไป"): at most ~90 thin, faint streaks, BEHIND the characters
  // (set layer, never fg / over captions or cards), falling slowly (one loop >= 1.1 s). Show a heavy storm with other cues:
  // Rup2.rainVeil (far curtains), Rup2.splashes (rings on the ground), Rup2.drips (eaves), thunder in the mix.
  Rup2.rain = (L, id, n = 70, o = {}) => { const r = rng(o.seed || 61); n = Math.min(n, 90); let g = `<g id="${id}-rain" opacity="${Math.min(o.op ?? 0.3, 0.35)}">`;
    for (let k = 0; k < n; k++) { const x = -200 + r() * 1500, y = -300 + r() * 2400, l = (o.len || 46) + r() * 30; g += `<path d="M${f(x)},${f(y)}l${f(-l * 0.25)},${f(l)}" stroke="#c8d8f0" stroke-width="${f((o.w || 1.1) + r() * 0.7)}" stroke-linecap="round"/>`; }
    put(o.layer || L.set, g + `</g>`); };
  Rup2.rainLife = (tl, id, t0, dur, per = 1.2) => tl.fromTo(`#${id}-rain`, { x: 0, y: 0 }, { x: -150, y: 600, duration: Math.max(1.1, per), repeat: Math.ceil(dur / Math.max(1.1, per)), ease: "none", immediateRender: false }, t0);
  // far rain curtains: soft slanted grey bands over the horizon, drifting slowly (reads as a downpour without streaks near the eye)
  Rup2.rainVeil = (L, id, o = {}) => { const top = o.top ?? 500, h = o.h ?? 600;
    put(L.far, `<defs><linearGradient id="${id}-vg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9aa8bc" stop-opacity="0"/><stop offset=".35" stop-color="#9aa8bc" stop-opacity=".5"/><stop offset="1" stop-color="#9aa8bc" stop-opacity=".15"/></linearGradient></defs>
      <g id="${id}-veil" opacity="${o.op ?? 0.45}">${[-300, 40, 380, 720, 1060].map((x, k) => `<path d="M${x},${top}l${180 + (k % 2) * 60},0l-120,${h}l-${180 + (k % 2) * 60},0z" fill="url(#${id}-vg)"/>`).join("")}</g>`); };
  Rup2.veilLife = (tl, id, t0, dur) => tl.fromTo(`#${id}-veil`, { x: 0, opacity: 0.35 }, { x: -60, opacity: 0.55, duration: dur, ease: "sine.inOut", immediateRender: false }, t0);
  // splash rings where the rain hits the yard / puddles (set layer, on the ground)
  Rup2.splashes = (L, id, n = 14, o = {}) => { const r = rng(o.seed || 71), x0 = o.x0 ?? 60, x1 = o.x1 ?? 1040, y0 = o.y0 ?? 1260, y1 = o.y1 ?? 1800; let g = "";
    for (let k = 0; k < n; k++) { const y = y0 + r() * (y1 - y0), s = 0.6 + (y - y0) / (y1 - y0) * 0.8; g += `<ellipse class="${id}-sp" cx="${f(x0 + r() * (x1 - x0))}" cy="${f(y)}" rx="${f(14 * s)}" ry="${f(4 * s)}" fill="none" stroke="#c8d4e4" stroke-width="2" opacity="0"/>`; }
    put(L.set, g); };
  Rup2.splashLife = (tl, id, t0, dur) => document.querySelectorAll(`.${id}-sp`).forEach((el, k) => { const per = 1.1 + (k % 4) * 0.15;
    tl.fromTo(el, { scale: 0.3, opacity: 0.7, transformOrigin: "50% 50%" }, { scale: 2.2, opacity: 0, transformOrigin: "50% 50%", duration: per, ease: "power1.out", repeat: Math.ceil(dur / per), immediateRender: false }, t0 + (k * 0.37) % per); });
  // water dripping from an eave or a floor edge: pts = [[x, yTop, yGround], ...]
  Rup2.drips = (L, id, pts) => put(L.set, pts.map(([x, y]) => `<g class="${id}-dr"><path d="M${x},${y}q-5,10 0,14q5,-4 0,-14z" fill="#c8dcf0" opacity=".85"/></g>`).join(""));
  Rup2.dripLife = (tl, id, t0, dur, pts) => document.querySelectorAll(`.${id}-dr`).forEach((el, k) => { const per = 1.0 + (k % 3) * 0.2, fall = pts[k][2] - pts[k][1];
    tl.fromTo(el, { y: 0, opacity: 1 }, { y: fall, opacity: 0.6, duration: per * 0.7, ease: "power2.in", repeat: Math.ceil(dur / per), repeatDelay: per * 0.3, immediateRender: false }, t0 + (k * 0.29) % per); });
  // a spirit house (ศาล) on a post with naga finials, garlands and incense
  Rup2.shrine = (x, y, s = 1, t = (c) => c) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})"><ellipse cx="0" cy="4" rx="90" ry="14" fill="#000" opacity=".3"/>
    <path d="M-10,0V-170M10,0V-170" stroke="${t("#e8dcc4")}" stroke-width="12"/><rect x="-70" y="-180" width="140" height="14" fill="${t("#d8c8a8")}" ${ln(2)}/>
    <rect x="-50" y="-270" width="100" height="90" fill="${t("#f2e6c8")}" ${ln(2.4)}/><rect x="-16" y="-250" width="32" height="70" fill="${t("#3a2414")}"/>
    <path d="M-74,-268L0,-340L74,-268Z" fill="${t("#c8402a")}" ${ln(2.4)}/><path d="M-74,-268q-14,-6 -16,-24M74,-268q14,-6 16,-24" stroke="${t("#f0c040")}" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M0,-340q6,-20 -2,-34q14,8 12,22" stroke="${t("#f0c040")}" stroke-width="6" fill="none"/><path d="M-60,-180q60,30 120,0" stroke="#f09a20" stroke-width="10" fill="none" stroke-dasharray="2 8" stroke-linecap="round"/>
    ${[-30, 30].map((dx) => `<path d="M${dx},-180v-30" stroke="#c8402a" stroke-width="3"/>`).join("")}</g>`;
  // a distance marker on the bund
  Rup2.marker = (x, y, s = 1, text = "100 ม.", t = (c) => c) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})"><path d="M0,0V-130" stroke="${t("#5a3a1e")}" stroke-width="8"/>
    <rect x="-56" y="-176" width="112" height="56" rx="6" fill="${t("#f2eee4")}" ${ln(2.4)}/><text x="0" y="-136" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="${t("#b8241e")}">${text}</text></g>`;
  // the rice barn sinking upright into a new hole (EP.3): drawn over ยาย's yard where Rup.house puts the granary (granary:false there)
  // a walk-in granary (เล้าข้าว) on stilts, scale S: the doorway (97×163 at S 2.2, sill at y-224) fits ยาย at s 0.23
  Rup2.barn = (L, id, o = {}) => { const x = o.x ?? 916, y = o.y ?? 1240, t = o.tint || ((c) => c), r = rng(o.seed || 83), S = o.s ?? 2.2;
    const cracks = Array.from({ length: 9 }, (_, k) => { const a = (k / 9) * Math.PI * 2 + r() * 0.3; let px = Math.cos(a) * 110, py = 6 + Math.sin(a) * 26, d = `M${f(px)},${f(py)}`;
      for (let j = 0; j < 4; j++) { px += Math.cos(a) * (40 + r() * 30) + (r() - 0.5) * 30; py += Math.sin(a) * (12 + r() * 8) + (r() - 0.5) * 8; d += `L${f(px)},${f(py)}`; }
      return `<path class="${id}-ck" d="${d}" stroke="${t("#1a0e08")}" stroke-width="${f(4 + r() * 3)}" fill="none" stroke-linecap="round" stroke-dasharray="400" stroke-dashoffset="400"/>`; }).join("");
    put(L.set, `<g transform="translate(${x},${y})">
      ${cracks}
      <ellipse id="${id}-bh" cx="0" cy="6" rx="0" ry="0" fill="#0c0806"/>
      <ellipse id="${id}-bw" cx="0" cy="10" rx="0" ry="0" fill="${t("#5a4430")}" opacity=".95"/>
      ${[0, 1, 2].map((k) => `<ellipse class="${id}-rip" cx="0" cy="10" rx="20" ry="5" stroke="${t("#c8d0d8")}" stroke-width="3" fill="none" opacity="0"/>`).join("")}
      <clipPath id="${id}-bc"><rect x="-320" y="-720" width="640" height="${o.clipY ?? 726}"/></clipPath>
      <g clip-path="url(#${id}-bc)"><g id="${id}-barn"><g transform="scale(${S})"><rect x="-56" y="-90" width="10" height="90" fill="${t("#5a3a24")}"/><rect x="46" y="-90" width="10" height="90" fill="${t("#5a3a24")}"/>
        <rect x="-64" y="-200" width="128" height="112" fill="${t("#a06a3a")}" ${ln(2.4)}/>${[0, 1, 2, 3, 4].map((k) => `<path d="M-64,${-190 + k * 22}H64" stroke="${t("#7a4a28")}" stroke-width="2"/>`).join("")}
        <rect x="-22" y="-176" width="44" height="74" fill="${t("#1a0e08")}"/><path d="M-22,-102h44v-8l-44,-10z" fill="${t("#e8c060")}" opacity=".7"/>
        <rect id="${id}-door" x="-22" y="-176" width="44" height="74" fill="${t("#6a3e22")}" ${ln(1.2)}/><circle cx="14" cy="-138" r="2.6" fill="${t("#2a1a10")}"/>
        <path d="M-50,-90v-8M50,-90v-8" stroke="${t("#4a2c18")}" stroke-width="4"/><path d="M-30,-6L-20,-90M30,-6L20,-90M-24,-30H24M-26,-60H26" stroke="${t("#6a4a2c")}" stroke-width="4" opacity="${o.ladder === false ? 0 : 1}"/>
        ${[0, 1, 2, 3, 4, 5].map((k) => `<path class="${id}-grain" d="M${-14 + k * 6},-104q2,6 0,12" stroke="${t("#e8c060")}" stroke-width="5" stroke-linecap="round" opacity="0"/>`).join("")}
        <path id="${id}-roof" d="M-88,-196L0,-266L88,-196Z" fill="${t("#8a8a7a")}" ${ln(1.6)}/></g></g></g>
      <path id="${id}-lip" d="M-250,8Q0,64 250,8" stroke="${t("#4a2c18")}" stroke-width="0" fill="none"/>
      ${Array.from({ length: 14 }, (_, k) => `<circle class="${id}-clod" cx="${f(-200 + k * 30)}" cy="0" r="${f(6 + r() * 9)}" fill="${t(k % 2 ? "#4a3220" : "#6a4a30")}" opacity="0"/>`).join("")}
      ${Array.from({ length: 14 }, (_, k) => `<circle class="${id}-dust" cx="${-230 + k * 36}" cy="${-10 - (k % 3) * 14}" r="${30 + (k % 4) * 14}" fill="${t("#9a8a70")}" opacity="0"/>`).join("")}</g>`); };
  // lightning (V1b): the SKY lights up (sky layer, fading out above the horizon), never the whole frame white; one strike = 2 flickers
  Rup2.flashLayer = (L, id) => put(L.sky, `<defs><linearGradient id="${id}-fg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef3ff" stop-opacity="1"/><stop offset=".6" stop-color="#c8d6f8" stop-opacity=".7"/><stop offset="1" stop-color="#b8c8f0" stop-opacity="0"/></linearGradient></defs>
    <rect id="${id}-fl" x="-600" y="-600" width="2400" height="1700" fill="url(#${id}-fg)" opacity="0"/>`);
  Rup2.bolt = (tl, id, t) => { tl.fromTo(`#${id}-fl`, { opacity: 0 }, { opacity: 1, duration: 0.05, immediateRender: false }, t);
    tl.to(`#${id}-fl`, { opacity: 0.2, duration: 0.1 }, t + 0.07); tl.to(`#${id}-fl`, { opacity: 0.75, duration: 0.05 }, t + 0.2); tl.to(`#${id}-fl`, { opacity: 0, duration: 0.5, ease: "power2.out" }, t + 0.27); };
  // the warning before the fall: cracks run out from the barn's feet, it creaks side to side, grain trickles from the door
  Rup2.barnCreak = (tl, id, t0, dur) => {
    document.querySelectorAll(`.${id}-ck`).forEach((el, k) => tl.fromTo(el, { attr: { "stroke-dashoffset": 400 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.9, ease: "power2.out", immediateRender: false }, t0 + (k % 5) * 0.12));
    tl.fromTo(`#${id}-barn`, { rotation: 0, transformOrigin: "50% 100%" }, { rotation: 1.6, transformOrigin: "50% 100%", duration: 0.28, yoyo: true, repeat: Math.max(1, Math.floor(dur / 0.28) - 1), ease: "sine.inOut", immediateRender: false }, t0 + 0.2);
    document.querySelectorAll(`.${id}-grain`).forEach((el, k) => tl.fromTo(el, { opacity: 0, y: 0 }, { opacity: 1, y: 70, duration: 0.5, repeat: Math.ceil(dur / 0.5), ease: "power1.in", immediateRender: false }, t0 + 0.4 + k * 0.08));
  };
  Rup2.barnSink = (tl, id, t0, dur, o = {}) => { const a = o.at ?? 0.4, d = o.sinkDur ?? 2.4;
    document.querySelectorAll(`.${id}-ck`).forEach((el) => tl.set(el, { attr: { "stroke-dashoffset": 0 } }, t0));
    tl.fromTo(`#${id}-bh`, { attr: { rx: 80, ry: 18 } }, { attr: { rx: 260, ry: 60 }, duration: 0.5, ease: "power3.out", immediateRender: false }, t0 + a);
    tl.fromTo(`#${id}-barn`, { y: 0, rotation: 1.2, transformOrigin: "50% 100%" }, { y: 60, rotation: -3, transformOrigin: "50% 100%", duration: 0.35, ease: "power2.in", immediateRender: false }, t0 + a);
    tl.to(`#${id}-barn`, { y: 760, rotation: -11, duration: d, ease: "power3.in" }, t0 + a + 0.45);
    tl.fromTo(`#${id}-lip`, { attr: { "stroke-width": 0 } }, { attr: { "stroke-width": 20 }, duration: 0.3, immediateRender: false }, t0 + a + 0.2);
    document.querySelectorAll(`.${id}-clod`).forEach((el, k) => { const dx = (k - 6.5) * 30, up = 200 + (k % 4) * 70;
      tl.fromTo(el, { opacity: 1, x: 0, y: 0 }, { x: dx, y: -up, duration: 0.45, ease: "power2.out", immediateRender: false }, t0 + a + 0.15 + (k % 3) * 0.06);
      tl.to(el, { y: 40, x: dx * 1.4, duration: 0.5, ease: "power2.in" }, t0 + a + 0.6 + (k % 3) * 0.06); tl.to(el, { opacity: 0, duration: 0.1 }, t0 + a + 1.05 + (k % 3) * 0.06); });
    document.querySelectorAll(`.${id}-dust`).forEach((el, k) => tl.fromTo(el, { opacity: 0, y: 0, scale: 0.5, transformOrigin: "50% 50%" }, { opacity: 0.75, y: -220 - k * 12, scale: 2.2, transformOrigin: "50% 50%", duration: 1.8, ease: "power2.out", immediateRender: false }, t0 + a + 0.5 + k * 0.06));
    const w = t0 + a + d + 0.2;
    tl.fromTo(`#${id}-bw`, { attr: { rx: 0, ry: 0 } }, { attr: { rx: 244, ry: 54 }, duration: 0.6, ease: "power2.out", immediateRender: false }, w);
    document.querySelectorAll(`.${id}-rip`).forEach((el, k) => tl.fromTo(el, { opacity: 0.8, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 0, scale: 6, transformOrigin: "50% 50%", duration: 0.9, repeat: 2, ease: "sine.out", immediateRender: false }, w + 0.2 + k * 0.3));
  };

  Rup2.life2 = (tl, id, t0, dur) => {
    document.querySelectorAll(`.${id}-gw`).forEach((el, k) => tl.fromTo(el, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -64 }, duration: 0.4, repeat: Math.ceil(dur / 0.4), ease: "none", immediateRender: false }, t0 + k * 0.05));
    tl.fromTo(`#${id}-smoke`, { x: -60 }, { x: 80, duration: dur, ease: "sine.inOut", immediateRender: false }, t0);
    document.querySelectorAll(`.${id}-bulb`).forEach((el, k) => tl.fromTo(el, { opacity: 0.75 }, { opacity: 1, duration: 0.3 + (k % 3) * 0.1, yoyo: true, repeat: Math.ceil(dur / 0.3), ease: "sine.inOut", immediateRender: false }, t0));
    document.querySelectorAll(`.${id}-fl`).forEach((el, k) => tl.fromTo(el, { scaleY: 0.8, transformOrigin: "50% 100%" }, { scaleY: 1.2, transformOrigin: "50% 100%", duration: 0.13 + k * 0.02, yoyo: true, repeat: Math.ceil(dur / 0.13), ease: "sine.inOut", immediateRender: false }, t0));
    document.querySelectorAll(`.${id}-clod`).forEach((el, k) => { const per = 0.9 + (k % 4) * 0.2;
      tl.fromTo(el, { y: 0, opacity: 1, rotation: 0, transformOrigin: "50% 50%" }, { y: 140 + (k % 3) * 40, opacity: 0, rotation: 200, transformOrigin: "50% 50%", duration: per, ease: "power2.in", repeat: Math.ceil(dur / per), immediateRender: false }, t0 + (k * 0.27) % per); });
    tl.fromTo(`#${id}-beam`, { opacity: 0.35 }, { opacity: 0.6, duration: 1.4, yoyo: true, repeat: Math.ceil(dur / 1.4), ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`.${id}-root`, { skewX: -3 }, { skewX: 3, duration: 1.2, yoyo: true, repeat: Math.ceil(dur / 1.2), ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`.r2-pan`, { x: -4 }, { x: 5, duration: 1.7, yoyo: true, repeat: Math.ceil(dur / 1.7), stagger: 0.07, ease: "sine.inOut", immediateRender: false }, t0);
  };
})();
