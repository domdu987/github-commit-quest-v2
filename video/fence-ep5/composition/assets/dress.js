// Set dressing (user, 28 Oct 2026: "ฉากมันยังเฉยๆ … ของแบบมืออาชีพเก็บรายละเอียดหน่อย … ทำฉากกับสิ่งของ ดีกว่านี้"):
// detailed props and surface wear drawn in the same flat, outlined style as the sets — every prop is lit from the upper left
// (a lit face, a shaded face, a highlight edge) and sits on its own contact shadow. Each function returns an SVG string with its
// origin at the point where it touches the ground; `s` scales it. Surfaces (wood, tin, concrete, dirt, tiles) are patterns in DEFS
// so walls and floors get texture without thousands of nodes.
(function () {
  const INK = "#2e2a26", O = (w = 3) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const n = (v) => (Math.round(v * 10) / 10).toString();
  const at = (x, y, s, body, rot = 0) => `<g transform="translate(${n(x)},${n(y)})${rot ? ` rotate(${rot})` : ""}${s !== 1 ? ` scale(${s})` : ""}">${body}</g>`;
  const shadow = (rx, ry = rx * 0.22, dx = rx * 0.18, op = 0.28) => `<ellipse cx="${n(dx)}" cy="2" rx="${n(rx)}" ry="${n(ry)}" fill="#0b0d08" opacity="${op}"/>`;

  Sets.DEFS += `
    <pattern id="dWood" width="64" height="200" patternUnits="userSpaceOnUse"><rect width="64" height="200" fill="#000" opacity="0"/><path d="M0.5,0V200" stroke="#000" stroke-opacity=".28" stroke-width="3"/><path d="M14,0C18,40 10,80 16,120S12,180 16,200M38,0C34,50 42,90 36,140S40,190 38,200M52,20c-6,10 -6,24 0,34" stroke="#000" stroke-opacity=".09" stroke-width="2" fill="none"/><path d="M3,0V200" stroke="#fff" stroke-opacity=".1" stroke-width="2"/><ellipse cx="26" cy="150" rx="4" ry="7" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="2"/></pattern>
    <pattern id="dPlankH" width="300" height="44" patternUnits="userSpaceOnUse"><path d="M0,43.5H300" stroke="#000" stroke-opacity=".38" stroke-width="3"/><path d="M0,2H300" stroke="#fff" stroke-opacity=".1" stroke-width="2"/><path d="M0,16C60,12 120,22 180,16S260,12 300,18M20,30c50,-4 90,4 140,0" stroke="#000" stroke-opacity=".13" stroke-width="2" fill="none"/><path d="M210,0V44" stroke="#000" stroke-opacity=".22" stroke-width="2"/></pattern>
    <pattern id="dTinV" width="28" height="100" patternUnits="userSpaceOnUse"><rect width="28" height="100" fill="#000" opacity="0"/><rect width="9" height="100" fill="#fff" opacity=".16"/><rect x="16" width="9" height="100" fill="#000" opacity=".16"/></pattern>
    <pattern id="dConc" width="90" height="90" patternUnits="userSpaceOnUse"><circle cx="12" cy="18" r="2.2" fill="#000" opacity=".18"/><circle cx="60" cy="9" r="1.8" fill="#000" opacity=".16"/><circle cx="41" cy="52" r="2.6" fill="#000" opacity=".15"/><circle cx="84" cy="22" r="1.4" fill="#000" opacity=".15"/><circle cx="6" cy="58" r="1.6" fill="#fff" opacity=".2"/><circle cx="78" cy="70" r="1.5" fill="#fff" opacity=".18"/><circle cx="20" cy="76" r="1.8" fill="#000" opacity=".09"/><circle cx="70" cy="38" r="1.2" fill="#fff" opacity=".15"/><path d="M30,30l6,4l3,9" stroke="#000" stroke-opacity=".08" stroke-width="1.5" fill="none"/></pattern>
    <pattern id="dDirt" width="160" height="80" patternUnits="userSpaceOnUse"><ellipse cx="18" cy="12" rx="6" ry="2.8" fill="#000" opacity=".2"/><ellipse cx="80" cy="30" rx="3.4" ry="1.8" fill="#000" opacity=".24"/><ellipse cx="118" cy="9" rx="7" ry="3" fill="#fff" opacity=".16"/><ellipse cx="50" cy="52" rx="5" ry="2.2" fill="#000" opacity=".17"/><ellipse cx="104" cy="58" rx="3" ry="1.6" fill="#fff" opacity=".22"/><ellipse cx="30" cy="40" rx="2.2" ry="1.2" fill="#000" opacity=".3"/><ellipse cx="146" cy="44" rx="2.6" ry="1.3" fill="#000" opacity=".28"/><ellipse cx="136" cy="70" rx="5" ry="2" fill="#000" opacity=".14"/><ellipse cx="70" cy="72" rx="2" ry="1" fill="#fff" opacity=".2"/><path d="M60,12q8,-3 16,0M8,66q10,-4 22,0" stroke="#000" stroke-opacity=".14" stroke-width="2" fill="none"/></pattern>
    <pattern id="dTile" width="120" height="120" patternUnits="userSpaceOnUse"><rect width="120" height="120" fill="#000" opacity="0"/><path d="M0,1H120M1,0V120" stroke="#000" stroke-opacity=".22" stroke-width="3"/><path d="M4,4H116" stroke="#fff" stroke-opacity=".1" stroke-width="2"/><rect x="60" y="60" width="58" height="58" fill="#000" opacity=".04"/></pattern>
    <linearGradient id="dGrime" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2016" stop-opacity="0"/><stop offset=".7" stop-color="#2a2016" stop-opacity=".12"/><stop offset="1" stop-color="#2a2016" stop-opacity=".38"/></linearGradient>
    <linearGradient id="dStreak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2e20" stop-opacity=".34"/><stop offset=".6" stop-color="#3a2e20" stop-opacity=".12"/><stop offset="1" stop-color="#3a2e20" stop-opacity="0"/></linearGradient>
    <linearGradient id="dRust" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a3f1c" stop-opacity=".7"/><stop offset=".5" stop-color="#a5552a" stop-opacity=".35"/><stop offset="1" stop-color="#a5552a" stop-opacity="0"/></linearGradient>
    <linearGradient id="dAO" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0d08" stop-opacity=".42"/><stop offset="1" stop-color="#0b0d08" stop-opacity="0"/></linearGradient>
    <linearGradient id="dAOup" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#0b0d08" stop-opacity=".38"/><stop offset="1" stop-color="#0b0d08" stop-opacity="0"/></linearGradient>
    <linearGradient id="dJar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a4a26"/><stop offset=".3" stop-color="#a65c30"/><stop offset=".75" stop-color="#6e3a1e"/><stop offset="1" stop-color="#4f2814"/></linearGradient>
    <linearGradient id="dTarp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f7fc4"/><stop offset="1" stop-color="#2a5d96"/></linearGradient>
    <linearGradient id="dLeaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7fa846"/><stop offset="1" stop-color="#4c7428"/></linearGradient>
    <radialGradient id="dPuddle" cx=".4" cy=".4" r=".7"><stop offset="0" stop-color="#d9e6ea" stop-opacity=".9"/><stop offset=".7" stop-color="#9fb5bd" stop-opacity=".8"/><stop offset="1" stop-color="#6d8790" stop-opacity=".6"/></radialGradient>
    <radialGradient id="dSunBloom"><stop offset="0" stop-color="#fffbe8" stop-opacity=".95"/><stop offset=".25" stop-color="#fff2c0" stop-opacity=".55"/><stop offset=".6" stop-color="#ffd890" stop-opacity=".16"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>
    <radialGradient id="dEmber"><stop offset="0" stop-color="#ffb35c" stop-opacity=".9"/><stop offset=".5" stop-color="#ff7a2a" stop-opacity=".35"/><stop offset="1" stop-color="#ff7a2a" stop-opacity="0"/></radialGradient>`;

  // ---------------- surface wear: streaks, rust runs, cracks, chips, moss, grime ----------------
  const streak = (x, y, w, h, op = 1) => `<rect x="${n(x)}" y="${n(y)}" width="${n(w)}" height="${n(h)}" fill="url(#dStreak)" opacity="${op}"/>`;
  const rust = (x, y, w, h, op = 1) => `<path d="M${n(x)},${n(y)}h${n(w)}l${n(-w * 0.2)},${n(h)}h${n(-w * 0.5)}z" fill="url(#dRust)" opacity="${op}"/>`;
  const crack = (x, y, len = 60, rot = 0, op = 0.5) => at(x, y, 1, `<path d="M0,0l${n(len * 0.2)},${n(len * 0.25)}l${n(-len * 0.08)},${n(len * 0.3)}l${n(len * 0.16)},${n(len * 0.45)}M${n(len * 0.12)},${n(len * 0.42)}l${n(len * 0.2)},${n(len * 0.1)}" stroke="#1d1914" stroke-opacity="${op}" stroke-width="2.5" fill="none" stroke-linecap="round"/>`, rot);
  const chip = (x, y, w = 18) => `<path d="M${n(x)},${n(y)}l${n(w)},${n(w * 0.2)}l${n(-w * 0.3)},${n(w * 0.7)}l${n(-w * 0.6)},${n(-w * 0.2)}z" fill="#000" opacity=".14"/>`;
  const moss = (x, y, w, r = mk(3)) => Array.from({ length: Math.max(2, Math.round(w / 18)) }, (_, k) => `<ellipse cx="${n(x + (k + 0.5) * (w / Math.max(2, Math.round(w / 18))))}" cy="${n(y - r() * 6)}" rx="${n(8 + r() * 8)}" ry="${n(4 + r() * 5)}" fill="${r() < 0.5 ? "#5f7a34" : "#4c6a2c"}" opacity=".75"/>`).join("");

  // ---------------- ground cover ----------------
  // a clump of grass blades (two greens, darker at the root), h = height in px
  function tuft(x, y, h = 40, r = mk(7), dry = false) {
    const c = dry ? ["#9a8a4a", "#b3a35c", "#7a6c38"] : ["#4f7a2c", "#6f9a3c", "#3c5e22"];
    let s = "";
    const nb = 5 + Math.floor(r() * 4);
    for (let k = 0; k < nb; k++) { const dx = (k - nb / 2) * h * 0.12 + (r() - 0.5) * 6, hh = h * (0.55 + r() * 0.5), lean = (r() - 0.5) * h * 0.7;
      s += `<path d="M${n(dx - 3)},0Q${n(dx + lean * 0.3)},${n(-hh * 0.6)} ${n(dx + lean)},${n(-hh)}Q${n(dx + lean * 0.2 + 2)},${n(-hh * 0.5)} ${n(dx + 4)},0z" fill="${c[k % 3]}"/>`; }
    return at(x, y, 1, `<ellipse cx="0" cy="1" rx="${n(h * 0.45)}" ry="${n(h * 0.08)}" fill="#0b0d08" opacity=".22"/>${s}`);
  }
  function tufts(x0, x1, y0, y1, count, seed = 11, h = 36, dry = false) { const r = mk(seed); let s = ""; for (let k = 0; k < count; k++) s += tuft(x0 + r() * (x1 - x0), y0 + r() * (y1 - y0), h * (0.6 + r() * 0.7), r, dry); return s; }
  // weeds along a wall foot: tall grass, a few flower heads
  function weeds(x0, x1, y, seed = 13, h = 60) { const r = mk(seed); let s = ""; for (let x = x0; x < x1; x += 24 + r() * 40) { s += tuft(x, y + r() * 6, h * (0.5 + r() * 0.8), r); if (r() < 0.18) s += `<circle cx="${n(x + 4)}" cy="${n(y - h * 0.9)}" r="5" fill="${r() < 0.5 ? "#f2e27a" : "#f4ecd8"}" stroke="${INK}" stroke-width="1.5"/>`; } return s; }
  function pebbles(x0, x1, y0, y1, count, seed = 17, sz = 8) { const r = mk(seed); let s = ""; for (let k = 0; k < count; k++) { const x = x0 + r() * (x1 - x0), y = y0 + r() * (y1 - y0), w = sz * (0.5 + r()), h = w * 0.6;
    s += `<ellipse cx="${n(x + w * 0.3)}" cy="${n(y + h * 0.5)}" rx="${n(w)}" ry="${n(h * 0.5)}" fill="#0b0d08" opacity=".25"/><ellipse cx="${n(x)}" cy="${n(y)}" rx="${n(w)}" ry="${n(h)}" fill="${["#9c9282", "#b7ad9b", "#857b6b"][k % 3]}"/><ellipse cx="${n(x - w * 0.3)}" cy="${n(y - h * 0.35)}" rx="${n(w * 0.4)}" ry="${n(h * 0.3)}" fill="#fff" opacity=".25"/>`; } return s; }
  function leaves(x0, x1, y0, y1, count, seed = 19) { const r = mk(seed); let s = ""; for (let k = 0; k < count; k++) { const x = x0 + r() * (x1 - x0), y = y0 + r() * (y1 - y0), a = r() * 360, w = 9 + r() * 7;
    s += at(x, y, 1, `<path d="M${n(-w)},0Q0,${n(-w * 0.6)} ${n(w)},0Q0,${n(w * 0.6)} ${n(-w)},0z" fill="${["#b8862e", "#8f6a2a", "#a3542a", "#c9a24a"][k % 4]}" opacity=".9"/><path d="M${n(-w)},0H${n(w)}" stroke="#5a3a1a" stroke-width="1" opacity=".6"/>`, n(a)); } return s; }
  // a puddle that holds the sky: dark rim, pale reflection, a glint, an optional ripple ring (class ripple)
  function puddle(x, y, rx = 120, ry = 26, night = false) {
    return `<g><ellipse cx="${n(x)}" cy="${n(y + 3)}" rx="${n(rx + 8)}" ry="${n(ry + 4)}" fill="#3e3020" opacity=".35"/><ellipse cx="${n(x)}" cy="${n(y)}" rx="${n(rx)}" ry="${n(ry)}" fill="${night ? "#4a5a7a" : "url(#dPuddle)"}"/>
      <path d="M${n(x - rx * 0.6)},${n(y - ry * 0.2)}q${n(rx * 0.4)},${n(-ry * 0.25)} ${n(rx * 0.8)},0" stroke="#fff" stroke-opacity="${night ? 0.45 : 0.6}" stroke-width="4" fill="none" stroke-linecap="round"/><ellipse class="ripple" cx="${n(x + rx * 0.2)}" cy="${n(y)}" rx="${n(rx * 0.25)}" ry="${n(ry * 0.25)}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/></g>`;
  }
  // tyre tracks in dirt: two soft bands with tread marks, following a quadratic from (x0,y0) to (x1,y1)
  function tracks(x0, y0, cx, cy, x1, y1, gap = 90, op = 0.18) {
    return [0, 1].map((k) => { const o = (k - 0.5) * gap; const d = `M${n(x0 + o)},${n(y0)}Q${n(cx + o)},${n(cy)} ${n(x1 + o * 1.6)},${n(y1)}`;
      return `<path d="${d}" stroke="#3a2a18" stroke-opacity="${op}" stroke-width="${n(26 + k * 2)}" fill="none" stroke-linecap="round"/><path d="${d}" stroke="#2a1d10" stroke-opacity="${op * 0.9}" stroke-width="18" fill="none" stroke-dasharray="4 10"/>`; }).join("");
  }

  // ---------------- props ----------------
  // Thai glazed water jar (โอ่งมังกร) with a dragon band, a wooden lid and a dipper
  function jar(x, y, s = 1) {
    return at(x, y, s, `${shadow(92, 18, 20)}<path d="M-58,-6C-96,-40 -98,-150 -62,-196C-44,-214 44,-214 62,-196C98,-150 96,-40 58,-6Z" fill="url(#dJar)" ${O(4)}/>
      <path d="M-70,-120C-30,-104 30,-104 70,-120" stroke="#e0b04a" stroke-width="7" fill="none" opacity=".85"/><path d="M-40,-100c10,-16 22,-16 30,-2s22,14 30,-4" stroke="#e0b04a" stroke-width="4" fill="none" opacity=".8"/>
      <path d="M-62,-150C-66,-110 -60,-60 -44,-24" stroke="#fff" stroke-opacity=".28" stroke-width="10" fill="none" stroke-linecap="round"/>
      <ellipse cx="0" cy="-202" rx="58" ry="12" fill="#3a2414" ${O(3)}/><ellipse cx="0" cy="-212" rx="66" ry="14" fill="#9a7244" ${O(3)}/><path d="M-50,-214H50" stroke="#6f4f2e" stroke-width="3"/><rect x="-8" y="-232" width="16" height="12" rx="4" fill="#6f4f2e" ${O(2)}/>
      <path d="M40,-222l40,-34" stroke="#6b4a2e" stroke-width="7" stroke-linecap="round"/><ellipse cx="86" cy="-262" rx="18" ry="10" fill="#d9c9a0" ${O(2)}/>`);
  }
  // monobloc plastic chair seen three-quarter front (col = red/blue/green/white); rot tips it over
  function chair(x, y, s = 1, col = "#c8392b", rot = 0) {
    const d = shade(col, -0.3), l = shade(col, 0.25);
    return at(x, y, s, `${rot ? "" : shadow(66, 12, 14, 0.24)}<path d="M-30,-136L-34,-8M30,-136L34,-8" stroke="${d}" stroke-width="11" stroke-linecap="round"/>
      <path d="M-40,-140C-44,-190 -46,-232 -40,-252Q0,-266 40,-252C46,-232 44,-190 40,-140Z" fill="${col}" ${O(3)}/><path d="M-26,-238h52M-28,-214h56M-28,-190h56" stroke="${d}" stroke-width="9" stroke-linecap="round"/><path d="M-34,-246Q0,-258 34,-246" stroke="${l}" stroke-width="4" fill="none"/>
      <path d="M-40,-196C-58,-186 -60,-150 -54,-128M40,-196C58,-186 60,-150 54,-128" stroke="${col}" stroke-width="10" fill="none" stroke-linecap="round"/>
      <path d="M-54,-118L54,-118L44,-142L-44,-142Z" fill="${col}" ${O(3)}/><path d="M-54,-118H54V-110H-54Z" fill="${d}" ${O(2)}/><path d="M-38,-134H38" stroke="${l}" stroke-width="3"/>
      <path d="M-48,-112L-56,0M48,-112L56,0" stroke="${col}" stroke-width="12" stroke-linecap="round"/><path d="M-48,-112L-56,0M48,-112L56,0" stroke="${INK}" stroke-width="2" stroke-opacity=".5" fill="none"/>`, rot);
  }
  function chairStack(x, y, s = 1, col = "#2f6fb8", k = 4) { let b = ""; for (let i = 0; i < k; i++) b += at(0, -i * 18, 1, chair(0, 0, 1, col).replace(/<ellipse[^>]*opacity="0.24"\/>/, "")); return at(x, y, s, shadow(66, 13, 14, 0.26) + b); }
  // bicycle leaning on its stand; basket on the front
  function bike(x, y, s = 1, col = "#2f6f6a") {
    const wheel = (cx) => `<circle cx="${cx}" cy="-62" r="62" fill="none" stroke="#1d1d1d" stroke-width="9"/><circle cx="${cx}" cy="-62" r="56" fill="none" stroke="#8d9299" stroke-width="2"/>${Array.from({ length: 6 }, (_, k) => `<path d="M${cx},-62l${n(Math.cos(k * 0.52) * 54)},${n(Math.sin(k * 0.52) * 54)}M${cx},-62l${n(-Math.cos(k * 0.52) * 54)},${n(-Math.sin(k * 0.52) * 54)}" stroke="#b9bec4" stroke-width="1.5"/>`).join("")}<circle cx="${cx}" cy="-62" r="7" fill="#5b6066"/>`;
    return at(x, y, s, `${shadow(150, 14, 30, 0.22)}${wheel(-90)}${wheel(90)}<path d="M-90,-62L-20,-62L40,-150L-40,-150ZM-20,-62L-40,-150L-48,-172M40,-150L90,-62M40,-150L52,-190" stroke="${col}" stroke-width="10" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
      <path d="M-66,-176h40" stroke="#1d1d1d" stroke-width="12" stroke-linecap="round"/><path d="M40,-196h30" stroke="#1d1d1d" stroke-width="7" stroke-linecap="round"/><path d="M60,-182h56l-10,46h-40z" fill="none" stroke="#7d858c" stroke-width="4"/><path d="M64,-170h46M66,-158h42M68,-146h36" stroke="#7d858c" stroke-width="2"/><circle cx="-20" cy="-62" r="14" fill="none" stroke="#5b6066" stroke-width="5"/>`);
  }
  function tires(x, y, s = 1, k = 3) {
    let b = shadow(96, 16, 18, 0.28);
    for (let i = 0; i < k; i++) { const yy = -i * 38; b += `<path d="M-86,${yy - 18}V${yy}A86,22 0 0 0 86,${yy}V${yy - 18}" fill="#24221f" ${O(3)}/><ellipse cx="0" cy="${yy - 18}" rx="86" ry="22" fill="#33302c" ${O(3)}/><ellipse cx="0" cy="${yy - 18}" rx="46" ry="11" fill="#0f0e0c"/>${Array.from({ length: 7 }, (_, j) => `<path d="M${-74 + j * 24},${yy - 6}v10" stroke="#4a4640" stroke-width="3"/>`).join("")}`; }
    return at(x, y, s, b);
  }
  function crate(x, y, s = 1, w = 120, h = 90, col = "#b48a56") {
    const d = shade(col, -0.22);
    return at(x, y, s, `${shadow(w * 0.6, 12, 16, 0.26)}<rect x="${-w / 2}" y="${-h}" width="${w}" height="${h}" fill="${col}" ${O(3)}/>${[0.25, 0.5, 0.75].map((f) => `<path d="M${-w / 2},${n(-h * f)}H${w / 2}" stroke="${d}" stroke-width="3"/>`).join("")}
      <rect x="${-w / 2}" y="${-h}" width="14" height="${h}" fill="${d}"/><rect x="${w / 2 - 14}" y="${-h}" width="14" height="${h}" fill="${d}"/><path d="M${-w / 2 + 14},${-h + 4}L${w / 2 - 14},-4" stroke="${d}" stroke-width="8"/>
      <rect x="${-w / 2}" y="${-h}" width="${w}" height="6" fill="#fff" opacity=".2"/>${[-1, 1].map((k) => `<circle cx="${k * (w / 2 - 7)}" cy="${-h + 10}" r="2.5" fill="#3a3330"/><circle cx="${k * (w / 2 - 7)}" cy="-10" r="2.5" fill="#3a3330"/>`).join("")}`);
  }
  // sandbags: rows of tied sacks, each a little different
  function sandbags(x, y, s = 1, cols = 4, rows = 3, seed = 23) {
    const r = mk(seed); let b = shadow(cols * 50, 16, 20, 0.3);
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols - (j % 2); i++) {
      const cx = (i - (cols - (j % 2) - 1) / 2) * 92, cy = -26 - j * 46, c = ["#c2ad7c", "#b39d6c", "#cdb98a"][Math.floor(r() * 3)];
      b += `<path d="M${n(cx - 48)},${n(cy + 18)}Q${n(cx - 54)},${n(cy - 20)} ${n(cx - 30)},${n(cy - 24)}Q${n(cx)},${n(cy - 30)} ${n(cx + 32)},${n(cy - 24)}Q${n(cx + 54)},${n(cy - 18)} ${n(cx + 48)},${n(cy + 18)}Q${n(cx)},${n(cy + 26)} ${n(cx - 48)},${n(cy + 18)}z" fill="${c}" ${O(3)}/>
        <path d="M${n(cx - 40)},${n(cy + 14)}Q${n(cx)},${n(cy + 20)} ${n(cx + 40)},${n(cy + 14)}" stroke="#000" stroke-opacity=".15" stroke-width="6" fill="none"/><path d="M${n(cx + 40)},${n(cy - 16)}l10,-6M${n(cx + 42)},${n(cy - 10)}l12,0" stroke="#7a6a48" stroke-width="3"/><path d="M${n(cx - 30)},${n(cy - 16)}q20,-6 40,-2" stroke="#fff" stroke-opacity=".25" stroke-width="4" fill="none"/>`;
    }
    return at(x, y, s, b);
  }
  // razor wire: a coil seen at a slant (back strands thin and dark, front strands lit), uneven pitch, barbs as little blades,
  // the straight carrier wire it hangs from
  function barbed(x0, x1, y, r0 = 26, seed = 89) {
    const r = mk(seed); let back = "", front = "";
    for (let x = x0; x < x1;) { const rr = r0 * (0.85 + r() * 0.3), w = rr * 0.55;
      back += `<path d="M${n(x - w)},${n(y)}A${n(w)},${n(rr)} 0 0 1 ${n(x + w)},${n(y)}" fill="none" stroke="#2a2e32" stroke-width="2"/>`;
      front += `<path d="M${n(x + w)},${n(y)}A${n(w)},${n(rr)} 0 0 1 ${n(x - w)},${n(y)}" fill="none" stroke="#8d9399" stroke-width="2.6"/><path d="M${n(x + w * 0.6)},${n(y + rr * 0.6)}A${n(w)},${n(rr)} 0 0 1 ${n(x - w * 0.2)},${n(y + rr * 0.95)}" fill="none" stroke="#d0d5d9" stroke-width="1.4" opacity=".8"/>`;
      for (let j = 0; j < 2; j++) { const a = r() * Math.PI * 2, bx = x + Math.cos(a) * w, by = y + Math.sin(a) * rr; front += `<path d="M${n(bx - 5)},${n(by - 3)}L${n(bx + 5)},${n(by + 3)}M${n(bx - 4)},${n(by + 4)}L${n(bx + 4)},${n(by - 4)}" stroke="#b9bec4" stroke-width="1.8"/>`; }
      x += rr * (0.55 + r() * 0.3); }
    return `<g><path d="M${x0},${y + r0 * 0.9}H${x1}" stroke="#4a4f55" stroke-width="2.5"/>${back}${front}</g>`;
  }
  // a tarp roped between two points (x0,y0) → (x1,y1), sagging; one corner torn
  function tarp(x0, y0, x1, y1, sag = 70, col = "url(#dTarp)") {
    const mx = (x0 + x1) / 2, my = (y0 + y1) / 2 + sag, h = 150;
    return `<path d="M${x0},${y0}Q${mx},${my} ${x1},${y1}L${x1 - 20},${y1 + h}Q${mx},${my + h * 0.6} ${x0 + 30},${y0 + h * 0.9}l-20,-30l10,-20z" fill="${col}" ${O(3)}/>
      <path d="M${x0 + 40},${y0 + 30}Q${mx},${my + 20} ${x1 - 40},${y1 + 26}" stroke="#fff" stroke-opacity=".18" stroke-width="10" fill="none"/>${[0.33, 0.66].map((t) => { const px = x0 + (x1 - x0) * t; return `<path d="M${n(px)},${n(my - sag * 0.3)}v${n(h * 0.8)}" stroke="#000" stroke-opacity=".12" stroke-width="18"/>`; }).join("")}
      <path d="M${x0},${y0}l-40,-60M${x1},${y1}l50,-50" stroke="#c9b48a" stroke-width="3"/><circle cx="${x0}" cy="${y0}" r="5" fill="#d9d4c8" ${O(2)}/><circle cx="${x1}" cy="${y1}" r="5" fill="#d9d4c8" ${O(2)}/>`;
  }
  // a cold campfire (stone ring, charred logs, a pot on a tripod); lit = embers + flames (class flame for flicker)
  function campfire(x, y, s = 1, lit = false) {
    const stones = Array.from({ length: 9 }, (_, k) => { const a = (k / 9) * Math.PI * 2, sx = Math.cos(a) * 80, sy = Math.sin(a) * 22; return `<ellipse cx="${n(sx)}" cy="${n(sy)}" rx="24" ry="15" fill="${["#8f8678", "#a39a8a", "#7a7266"][k % 3]}" ${O(2.5)}/><ellipse cx="${n(sx - 6)}" cy="${n(sy - 5)}" rx="9" ry="5" fill="#fff" opacity=".22"/>`; });
    const back = stones.filter((_, k) => Math.sin((k / 9) * Math.PI * 2) < 0).join(""), front = stones.filter((_, k) => Math.sin((k / 9) * Math.PI * 2) >= 0).join("");
    return at(x, y, s, `${shadow(110, 26, 10, 0.3)}${back}<ellipse cx="0" cy="0" rx="62" ry="16" fill="#1f1a16"/><ellipse cx="0" cy="-2" rx="44" ry="10" fill="#5a5048" opacity=".7"/>
      <path d="M-50,-4L40,-26M-40,-24L50,0" stroke="#2a1d14" stroke-width="14" stroke-linecap="round"/><path d="M-30,-10L20,-22" stroke="#7a3a1a" stroke-width="4" opacity=".7"/>
      ${lit ? `<circle cx="0" cy="-20" r="90" fill="url(#dEmber)"/><g class="flame"><path d="M-26,-14C-30,-60 -6,-70 0,-110C10,-70 34,-58 26,-14Z" fill="#ff8a2a"/><path d="M-12,-14C-14,-44 0,-52 2,-80C10,-50 20,-42 12,-14Z" fill="#ffd36a"/></g>` : `<path class="smoke" d="M0,-30q-20,-50 6,-100t-6,-110" stroke="#cfd3d6" stroke-width="10" stroke-opacity=".18" fill="none" stroke-linecap="round"/>`}
      <path d="M-70,0L0,-210L70,0M0,-210V-150" stroke="#4a3a2a" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-36,-150h72l-8,52h-56z" fill="#3a3e42" ${O(3)}/><path d="M-36,-150q36,-16 72,0" stroke="#6b7177" stroke-width="3" fill="none"/>${front}`);
  }
  function bucket(x, y, s = 1, col = "#2f6fb8") { return at(x, y, s, `${shadow(40, 8, 8)}<path d="M-34,-70L-26,0H26L34,-70Z" fill="${col}" ${O(3)}/><ellipse cx="0" cy="-70" rx="34" ry="8" fill="${shade(col, -0.4)}" ${O(2.5)}/><path d="M-30,-70Q0,-118 30,-70" stroke="#5b6066" stroke-width="3" fill="none"/><path d="M-24,-60L-19,-6" stroke="#fff" stroke-opacity=".3" stroke-width="5"/>`); }
  function broom(x, y, s = 1, rot = -14) { return at(x, y, s, `<path d="M0,0L0,-300" stroke="#8a6a42" stroke-width="8" stroke-linecap="round"/><path d="M-26,0Q-30,-70 -6,-110H6Q30,-70 26,0Z" fill="#c9a55a" ${O(2.5)}/>${Array.from({ length: 7 }, (_, k) => `<path d="M${-18 + k * 6},-4L${-8 + k * 3},-100" stroke="#9a7a3a" stroke-width="1.5"/>`).join("")}<path d="M-12,-96h24" stroke="#c8392b" stroke-width="5"/>`, rot); }
  // a clay pot with a leafy plant (basil / chillies / an ornamental)
  function potPlant(x, y, s = 1, kind = 0) {
    const leaf = (a, l, c) => `<path d="M0,-70Q${n(Math.cos(a) * l * 0.5 - 12)},${n(-70 + Math.sin(a) * l * 0.5 - 10)} ${n(Math.cos(a) * l)},${n(-70 + Math.sin(a) * l)}Q${n(Math.cos(a) * l * 0.5 + 12)},${n(-70 + Math.sin(a) * l * 0.5 + 8)} 0,-70z" fill="${c}" ${O(2)}/>`;
    const L = Array.from({ length: 9 }, (_, k) => leaf(-Math.PI * (0.1 + k * 0.1), 60 + (k % 3) * 18, ["#5f8a34", "#4c7428", "#7aa846"][k % 3])).join("");
    return at(x, y, s, `${shadow(44, 9, 8)}${L}${kind === 1 ? `<circle cx="-20" cy="-118" r="6" fill="#d8392b" ${O(1.5)}/><circle cx="18" cy="-128" r="6" fill="#d8392b" ${O(1.5)}/>` : ""}<path d="M-38,-70h76l-10,70h-56z" fill="#b5653a" ${O(3)}/><rect x="-42" y="-80" width="84" height="14" rx="3" fill="#c97a4a" ${O(2.5)}/><path d="M-26,-60L-22,-8" stroke="#fff" stroke-opacity=".25" stroke-width="5"/>`);
  }
  // a banana plant: pseudo-stem, big ribbed leaves (some torn, one dead and hanging)
  function banana(x, y, s = 1, seed = 29) {
    const r = mk(seed);
    const leaf = (a, l, dead) => { const ex = Math.cos(a) * l, ey = Math.sin(a) * l * 0.7 - 300, c = dead ? "#a0884a" : r() < 0.5 ? "#5f8f34" : "#6f9f3c";
      return `<path d="M0,-300Q${n(ex * 0.4)},${n(ey - 60)} ${n(ex)},${n(ey + (dead ? 120 : 0))}Q${n(ex * 0.55)},${n(ey + 70)} 0,-290z" fill="${c}" ${O(2.5)}/><path d="M0,-296Q${n(ex * 0.45)},${n(ey - 10)} ${n(ex * 0.96)},${n(ey + (dead ? 116 : 2))}" stroke="#d6e2a0" stroke-opacity=".7" stroke-width="3" fill="none"/>${dead ? "" : `<path d="M${n(ex * 0.5)},${n(ey * 0.5 - 150)}l${n(ex * 0.08)},26M${n(ex * 0.7)},${n(ey * 0.7 - 90)}l${n(ex * 0.06)},22" stroke="#3c5e22" stroke-width="2" opacity=".6"/>`}`; };
    return at(x, y, s, `${shadow(120, 18, 30, 0.26)}${leaf(-2.6, 230, false)}${leaf(-0.5, 240, false)}<path d="M-26,0C-30,-120 -20,-240 -10,-310H14C20,-240 28,-120 26,0Z" fill="#7a8a4a" ${O(3)}/><path d="M-14,-20C-16,-120 -8,-220 -2,-300" stroke="#a5b46a" stroke-width="6" fill="none" opacity=".6"/>
      ${leaf(-1.6, 200, false)}${leaf(-3.0, 210, true)}${leaf(-0.1, 190, false)}`);
  }
  // a rounded shrub with lit and shaded masses
  function bush(x, y, s = 1, seed = 31, col = ["#3c5e22", "#4f7a2c", "#6f9a3c"]) {
    const r = mk(seed); let b = shadow(120, 20, 26, 0.3);
    const blobs = Array.from({ length: 7 }, (_, k) => [(-1 + (k / 6) * 2) * 90 + (r() - 0.5) * 20, -50 - Math.sin((k / 6) * Math.PI) * 60 - r() * 20, 46 + r() * 24]);
    blobs.forEach(([bx, by, br]) => (b += `<circle cx="${n(bx)}" cy="${n(by)}" r="${n(br)}" fill="${col[0]}" ${O(2.5)}/>`));
    blobs.forEach(([bx, by, br]) => (b += `<circle cx="${n(bx - br * 0.2)}" cy="${n(by - br * 0.2)}" r="${n(br * 0.72)}" fill="${col[1]}"/>`));
    blobs.slice(1, 6).forEach(([bx, by, br]) => (b += `<circle cx="${n(bx - br * 0.38)}" cy="${n(by - br * 0.4)}" r="${n(br * 0.3)}" fill="${col[2]}"/>`));
    return at(x, y, s, b + `<path d="M-100,-10Q0,6 100,-10" stroke="#000" stroke-opacity=".18" stroke-width="18" fill="none"/>`);
  }
  // a string of empty cans hung along a fence as an alarm (the camp's own idea: "มันเดินตามเสียง" — so do we)
  function canAlarm(x0, x1, y, seed = 37, sag = 26) {
    const r = mk(seed); let b = `<path d="M${x0},${y}Q${(x0 + x1) / 2},${y + sag} ${x1},${y}" stroke="#c9b48a" stroke-width="2.5" fill="none"/>`;
    for (let x = x0 + 30; x < x1 - 20; x += 46 + r() * 30) { const t = (x - x0) / (x1 - x0), yy = y + 4 * sag * t * (1 - t), l = 14 + r() * 16;
      b += `<path d="M${n(x)},${n(yy)}v${n(l)}" stroke="#c9b48a" stroke-width="2"/><g transform="translate(${n(x)},${n(yy + l)}) rotate(${n((r() - 0.5) * 30)})"><rect x="-10" y="0" width="20" height="28" rx="3" fill="url(#fCan)" ${O(2)}/><rect x="-10" y="8" width="20" height="10" fill="${["#c8392b", "#2f6fb8", "#e8b830"][Math.floor(r() * 3)]}" opacity=".7"/></g>`; }
    return `<g class="canalarm">${b}</g>`;
  }
  // a hand-painted board on a stake
  function sign(x, y, s = 1, text = "ห้ามเข้า", col = "#c8392b", rot = -4) {
    return at(x, y, s, `${shadow(40, 8, 10)}<path d="M-6,0V-150" stroke="#6b4a2e" stroke-width="12"/><g transform="rotate(${rot} 0 -170)"><rect x="-110" y="-230" width="220" height="90" fill="#e7dcc0" ${O(3)}/><rect x="-110" y="-230" width="220" height="90" fill="url(#dPlankH)"/>
      <text x="0" y="-170" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="${col}" opacity=".9">${text}</text><circle cx="-96" cy="-218" r="4" fill="#3a3330"/><circle cx="96" cy="-218" r="4" fill="#3a3330"/><path d="M-90,-150q30,8 80,0" stroke="${col}" stroke-width="4" opacity=".5" fill="none"/></g>`);
  }
  // a washing line between two posts with clothes pegged on it: shirts, a sarong, a towel
  function laundry(x0, x1, y, seed = 41) {
    const r = mk(seed), cols = ["#c8392b", "#e8dcc6", "#2f6fb8", "#6f8f58", "#e8b830", "#b8463a"];
    let b = `<path d="M${x0},${y}Q${(x0 + x1) / 2},${y + 40} ${x1},${y}" stroke="#d9d4c8" stroke-width="2.5" fill="none"/>`;
    let k = 0;
    for (let x = x0 + 40; x < x1 - 70; x += 86 + r() * 40, k++) { const t = (x - x0) / (x1 - x0), yy = y + 160 * t * (1 - t), c = cols[Math.floor(r() * cols.length)], d = shade(c, -0.22), kind = k % 3;
      const body = kind === 0 ? `M0,0h18q10,8 20,0h18l22,18l-12,16l-10,-6v66h-56v-66l-10,6l-12,-16z`   // a shirt
        : kind === 1 ? `M2,0h56l6,96q-34,8 -68,0z`                                                       // a sarong
        : `M0,0h50v70l-8,-4l-8,6l-8,-5l-8,6l-8,-5l-10,4z`;                                              // a towel with a frayed hem
      b += `<g transform="translate(${n(x)},${n(yy)}) rotate(${n((r() - 0.5) * 6)})"><path d="${body}" fill="${c}" ${O(2.5)}/>${kind === 1 ? `<path d="M10,20h44M8,44h48M6,68h52" stroke="${d}" stroke-width="5"/>` : `<path d="M${kind ? 34 : 40},6v${kind ? 56 : 76}" stroke="#000" stroke-opacity=".14" stroke-width="16"/>`}<rect x="6" y="-6" width="5" height="14" fill="#e8b830"/><rect x="${kind ? 40 : 46}" y="-6" width="5" height="14" fill="#e8b830"/></g>`; }
    return `<g class="laundry">${b}</g>`;
  }
  // the camp's vegetable bed: a raised plank frame, dark soil, rows of seedlings on stakes
  function garden(x, y, w = 360, seed = 43) {
    const r = mk(seed); let b = `<path d="M${x - w / 2 - 20},${y + 6}h${w + 40}" stroke="#0b0d08" stroke-opacity=".25" stroke-width="16"/><rect x="${x - w / 2}" y="${y - 40}" width="${w}" height="40" fill="#5a3e26" ${O(3)}/><rect x="${x - w / 2}" y="${y - 40}" width="${w}" height="40" fill="url(#dPlankH)"/><path d="M${x - w / 2 + 6},${y - 40}h${w - 12}" stroke="#3a2a1a" stroke-width="10"/>`;
    for (let k = 0; k < Math.floor(w / 46); k++) { const px = x - w / 2 + 26 + k * 46 + (r() - 0.5) * 8;
      b += `<path d="M${n(px + 12)},${y - 40}V${y - 110}" stroke="#a58a5a" stroke-width="4"/>${tuft(px, y - 42, 34 + r() * 20, r).replace(/#4f7a2c|#6f9a3c|#3c5e22/g, (m) => ({ "#4f7a2c": "#5a9a34", "#6f9a3c": "#7cbf46", "#3c5e22": "#3f7a28" })[m])}`; }
    return b + `<path d="M${x - w / 2},${y - 104}H${x + w / 2}" stroke="#d9d4c8" stroke-width="1.5" opacity=".6"/>`;
  }
  function jerry(x, y, s = 1, col = "#c8392b") { return at(x, y, s, `${shadow(44, 8, 10)}<path d="M-34,0V-96L-20,-110H34V0Z" fill="${col}" ${O(3)}/><path d="M-22,-90L22,-20M22,-90L-22,-20" stroke="${shade(col, -0.3)}" stroke-width="6"/><rect x="0" y="-126" width="22" height="18" rx="3" fill="#3a3e42" ${O(2)}/><path d="M-30,-104h24" stroke="#3a3e42" stroke-width="8" stroke-linecap="round"/><path d="M-28,-90V-8" stroke="#fff" stroke-opacity=".25" stroke-width="5"/>`); }
  function firewood(x, y, s = 1, seed = 47) {
    const r = mk(seed); let b = shadow(120, 18, 20, 0.28);
    for (let j = 0; j < 3; j++) for (let i = 0; i < 4 - j; i++) { const cx = (i - (3 - j) / 2) * 52, cy = -26 - j * 44;
      b += `<rect x="${n(cx - 26)}" y="${n(cy - 24)}" width="120" height="48" fill="#6b4a2e" ${O(2.5)}/><circle cx="${n(cx - 26)}" cy="${n(cy)}" r="24" fill="#c9a06c" ${O(2.5)}/><circle cx="${n(cx - 26)}" cy="${n(cy)}" r="14" fill="none" stroke="#a5804f" stroke-width="2"/><circle cx="${n(cx - 26)}" cy="${n(cy)}" r="5" fill="#a5804f"/>`; }
    return at(x, y, s, b);
  }
  function drum(x, y, s = 1, col = "#2f5f8a", rusty = true) {
    const d = shade(col, -0.3);
    return at(x, y, s, `${shadow(64, 12, 14)}<rect x="-54" y="-170" width="108" height="170" fill="${col}" ${O(3)}/><rect x="-54" y="-170" width="30" height="170" fill="#fff" opacity=".12"/><rect x="24" y="-170" width="30" height="170" fill="#000" opacity=".16"/>
      <path d="M-54,-118H54M-54,-58H54" stroke="${d}" stroke-width="7"/>${rusty ? rust(-40, -170, 34, 120) + rust(10, -60, 26, 60) : ""}<ellipse cx="0" cy="-170" rx="54" ry="12" fill="${d}" ${O(3)}/><circle cx="20" cy="-172" r="7" fill="#1d1d1d"/>`);
  }
  // a wooden hand cart with two spoked wheels, tipped on its handles
  function cart(x, y, s = 1) {
    return at(x, y, s, `${shadow(150, 16, 20)}<path d="M-150,-90L130,-90L150,-160H-160Z" fill="#9a7244" ${O(3)}/><rect x="-160" y="-160" width="310" height="70" fill="url(#dPlankH)"/><path d="M150,-125L260,-20" stroke="#6b4a2e" stroke-width="12" stroke-linecap="round"/>
      <circle cx="-40" cy="-56" r="56" fill="none" stroke="#3a2a1a" stroke-width="10"/>${Array.from({ length: 4 }, (_, k) => `<path d="M-40,-56l${n(Math.cos(k * 0.785) * 50)},${n(Math.sin(k * 0.785) * 50)}M-40,-56l${n(-Math.cos(k * 0.785) * 50)},${n(-Math.sin(k * 0.785) * 50)}" stroke="#5a4030" stroke-width="5"/>`).join("")}<circle cx="-40" cy="-56" r="10" fill="#5b6066"/>`);
  }
  // rolled sleeping mats + a mosquito net bundle (camp life inside the classroom)
  function mats(x, y, s = 1) { return at(x, y, s, `${shadow(110, 14, 10)}${[["#c8a24a", -60], ["#4f8a6a", 0], ["#b8463a", 60]].map(([c, dx]) => `<rect x="${dx - 28}" y="-60" width="56" height="60" rx="26" fill="${c}" ${O(3)}/><ellipse cx="${dx}" cy="-30" rx="18" ry="26" fill="${shade(c, -0.25)}"/><path d="M${dx - 20},-58v56" stroke="#fff" stroke-opacity=".2" stroke-width="5"/><path d="M${dx - 28},-34h56" stroke="#e8dcc6" stroke-width="3"/>`).join("")}<path d="M-100,-64q40,-40 100,-30t100,10" stroke="#e8e4da" stroke-width="16" fill="none" opacity=".8"/>`); }
  function shoes(x, y, s = 1, seed = 53) { const r = mk(seed); let b = ""; for (let k = 0; k < 4; k++) { const dx = k * 54 + r() * 10, c = ["#2f4a8a", "#c8392b", "#3a3330", "#6f8f58"][k]; b += `<path d="M${n(dx)},0q0,-14 16,-16h28q8,0 8,10v6z" fill="${c}" ${O(2)}/><path d="M${n(dx + 10)},-10l14,-6" stroke="#fff" stroke-opacity=".4" stroke-width="3"/>`; } return at(x, y, s, shadow(120, 6, 100, 0.2) + b); }
  // stacked canned food / bottled water: the camp's stores
  function stores(x, y, s = 1, seed = 59) {
    const r = mk(seed); let b = shadow(130, 12, 20, 0.26);
    for (let j = 0; j < 3; j++) for (let i = 0; i < 5 - j; i++) { const cx = (i - (4 - j) / 2) * 44, cy = -j * 54;
      b += `<rect x="${n(cx - 20)}" y="${n(cy - 54)}" width="40" height="54" rx="4" fill="url(#fCan)" ${O(2.5)}/><rect x="${n(cx - 20)}" y="${n(cy - 42)}" width="40" height="24" fill="${["#c8392b", "#2f6fb8", "#e8b830", "#4f8a55"][Math.floor(r() * 4)]}" opacity=".85"/><path d="M${n(cx - 20)},${n(cy - 54)}h40" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>`; }
    return at(x, y, s, b);
  }
  function bottles(x, y, s = 1, k = 6) { let b = shadow(k * 18, 8, 10, 0.2); for (let i = 0; i < k; i++) b += `<path d="M${i * 30 - 10},0V-62Q${i * 30 - 10},-74 ${i * 30 - 4},-80V-92H${i * 30 + 8}V-80Q${i * 30 + 14},-74 ${i * 30 + 14},-62V0Z" fill="#cfe6ee" fill-opacity=".75" ${O(2)}/><rect x="${i * 30 - 6}" y="-98" width="16" height="8" rx="2" fill="#2f6fb8"/><rect x="${i * 30 - 10}" y="-50" width="24" height="16" fill="#e8dcc6" opacity=".8"/><path d="M${i * 30 - 6},-60v52" stroke="#fff" stroke-opacity=".6" stroke-width="3"/>`; return at(x - k * 15, y, s, b); }

  // a Thai wooden house on stilts (บ้านใต้ถุนสูง): posts, a plank body with shuttered windows, a steep rusty tin gable with wide
  // eaves, side stairs, a jar and a hammock in the shade underneath. tone = "day" | "dusk" | "night" (faded for distance)
  function stiltHouse(x, y, s = 1, tone = "day", seed = 61) {
    const r = mk(seed), T = tone === "night" ? { w: "#3a3a40", wd: "#2a2a30", roof: "#3a3f48", roofd: "#2c3038", post: "#2a2a2e", win: "#14161c" }
      : tone === "dusk" ? { w: "#8a5a4a", wd: "#6a4238", roof: "#7a6a6a", roofd: "#5a4a50", post: "#5a3a30", win: "#2a1a1a" }
      : { w: "#b07a4a", wd: "#8a5a36", roof: "#9aa2a5", roofd: "#7f878b", post: "#7a5236", win: "#2a2420" };
    let b = shadow(300, 26, 40, 0.3);
    b += [-220, -80, 80, 220].map((px) => `<rect x="${px - 10}" y="-170" width="20" height="170" fill="${T.post}" ${O(3)}/>`).join("");
    b += `<path d="M-60,0q20,-60 60,-60q40,0 60,60" stroke="#c8392b" stroke-width="5" fill="none" opacity=".7"/>` + `<g transform="translate(150,0) scale(.42)">${jar(0, 0, 1).replace(/<g transform="translate\(0,0\)">/, "<g>")}</g>`;
    b += `<rect x="-250" y="-190" width="500" height="22" fill="${T.wd}" ${O(3)}/><rect x="-240" y="-430" width="480" height="240" fill="${T.w}" ${O(3)}/><rect x="-240" y="-430" width="480" height="240" fill="url(#dWood)" opacity=".7"/>`;
    b += [-150, 40].map((wx) => `<rect x="${wx}" y="-380" width="110" height="120" fill="${T.win}" ${O(3)}/><rect x="${wx - 44}" y="-380" width="44" height="120" fill="${T.wd}" ${O(2.5)}/><rect x="${wx + 110}" y="-380" width="44" height="120" fill="${T.wd}" ${O(2.5)}/>${[0, 1, 2].map((j) => `<path d="M${wx - 40},${-360 + j * 36}h36M${wx + 114},${-360 + j * 36}h36" stroke="#000" stroke-opacity=".2" stroke-width="3"/>`).join("")}`).join("");
    b += `<path d="M-300,-420L0,-640L300,-420Z" fill="${T.roof}" ${O(3)}/><path d="M0,-640L300,-420H170Z" fill="${T.roofd}"/><rect x="-300" y="-430" width="600" height="300" fill="url(#dTinV)" opacity=".5" clip-path="polygon(0 0,100% 0,100% 4%,0 4%)"/>
      ${D_RUST(-120, -560, 50, 100)}${D_RUST(90, -520, 40, 80)}<path d="M-320,-410L0,-650L320,-410" stroke="${INK}" stroke-width="5" fill="none" stroke-linejoin="round"/><path d="M-90,-470L-60,-500" stroke="#000" stroke-opacity=".2" stroke-width="4"/>`;
    b += `<path d="M250,-190L330,0M276,-190L356,0" stroke="${T.post}" stroke-width="6"/>${Array.from({ length: 7 }, (_, k) => `<path d="M${260 + k * 11},${-170 + k * 25}h28" stroke="${T.post}" stroke-width="6"/>`).join("")}`;
    return at(x, y, s, b);
  }
  const D_RUST = (x, y, w, h) => rust(x, y, w, h);

  // ---------------- colour helper ----------------
  function shade(hex, k) {
    if (!/^#[0-9a-f]{6}$/i.test(hex)) return hex;
    const c = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16)).map((v) => Math.max(0, Math.min(255, Math.round(k < 0 ? v * (1 + k) : v + (255 - v) * k))));
    return `#${c.map((v) => v.toString(16).padStart(2, "0")).join("")}`;
  }

  window.Dress = { mk, at, shadow, streak, rust, crack, chip, moss, tuft, tufts, weeds, pebbles, leaves, puddle, tracks, jar, chair, chairStack, bike, tires, crate, sandbags, barbed, tarp, campfire, bucket, broom, potPlant, banana, bush, canAlarm, sign, laundry, garden, jerry, firewood, drum, cart, mats, shoes, stores, bottles, stiltHouse, shade };
})();
