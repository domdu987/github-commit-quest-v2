// สกิลจอมโกหก · v2 look: depth dressing for the jk sets — contact shadows under the furniture, light cones under the lamps,
// long cast shadows from the sun, haze on the far layers, drifting dust / sparks / pollen on the shot clock, a few birds.
// The engine calls JKD.dress[set](L, tl, sh, id, setOpts) right after the set is built (before the cast). Load after jkset.js.
(function () {
  const f = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  const NS = "http://www.w3.org/2000/svg";
  const Q = new URLSearchParams(location.search);   // debugging switches: ?nodepth=1 ?nomotes=1 ?nodeco=1
  const G = (layer, html) => { const g = document.createElementNS(NS, "g"); layer.appendChild(g); if (html) g.innerHTML = html; return g; };
  Sets.DEFS += `<linearGradient id="jkdAO" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></linearGradient>
    <linearGradient id="jkdAOup" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".4"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
    <linearGradient id="jkdCyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".32"/><stop offset=".28" stop-color="#000" stop-opacity="0"/><stop offset=".62" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>
    <linearGradient id="jkdCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2a8" stop-opacity=".42"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></linearGradient>
    <linearGradient id="jkdMoon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe0ff" stop-opacity=".22"/><stop offset="1" stop-color="#cfe0ff" stop-opacity="0"/></linearGradient>
    <radialGradient id="jkdSoftL"><stop offset="0" stop-color="#fff2d0" stop-opacity=".3"/><stop offset="1" stop-color="#fff2d0" stop-opacity="0"/></radialGradient>`;
  // ---- building blocks ----
  const ao = (x, y, rx, ry, op = 0.35, blur = 10) => `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx)}" ry="${f(ry)}" fill="#000" opacity="${op}" style="filter:blur(${blur}px)"/>`;
  const band = (y, h, op = 1, up = false, x = -2400, w = 6200) => `<rect x="${x}" y="${f(y)}" width="${w}" height="${f(h)}" fill="url(#${up ? "jkdAOup" : "jkdAO"})" opacity="${op}"/>`;
  const cyl = (x, y, w, h, op = 1, rx = 0) => `<rect x="${f(x)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" rx="${rx}" fill="url(#jkdCyl)" opacity="${op}"/>`;
  const cone = (x, y, top, len, op = 1, g = "jkdCone") => (op = op * 0.6) && `<path d="M${f(x - top)},${f(y)}H${f(x + top)}L${f(x + top + len * 0.55)},${f(y + len)}H${f(x - top - len * 0.55)}Z" fill="url(#${g})" opacity="${op}" style="filter:blur(14px)"/>`;
  // a long shadow thrown on the ground by a block standing on it (dx: how far the top edge slides, i.e. the sun's direction)
  const cast = (x, w, y, h, dx, op = 0.3, blur = 8) => `<path d="M${f(x)},${f(y)}H${f(x + w)}L${f(x + w + dx)},${f(y + h)}H${f(x + dx)}Z" fill="#000" opacity="${op}" style="filter:blur(${blur}px)"/>`;
  // particles on the shot clock: n dots drifting (dx,dy) per period with a twinkle
  const motes = (layer, tl, sh, o) => { if (Q.get("nomotes")) return null; const r = mk(o.seed || 7), n = o.n ?? 14, g = G(layer), ids = [];
    for (let k = 0; k < n; k++) { const x = o.x + r() * o.w, y = o.y + r() * o.h, rr = (o.r ?? 3) * (0.6 + r() * 0.9);
      g.insertAdjacentHTML("beforeend", `<circle class="jkdm" cx="${f(x)}" cy="${f(y)}" r="${f(rr)}" fill="${o.color || "#fff2c8"}" opacity="0"${o.blur ? ` style="filter:blur(${o.blur}px)"` : ""}/>`); }
    [...g.children].forEach((el, k) => { const p = (o.period ?? 4) * (0.7 + r() * 0.6), ph = r() * p, dx = (o.dx ?? 30) * (r() - 0.5) * 2, dy = (o.dy ?? -60) * (0.5 + r());
      const reps = Math.ceil(sh.dur / p) + 1;
      tl.fromTo(el, { x: 0, y: 0 }, { x: dx, y: dy, duration: p, repeat: reps, ease: "none", immediateRender: false }, Math.max(0, sh.start - ph));
      tl.fromTo(el, { opacity: 0 }, { opacity: o.op ?? 0.75, duration: p / 2, repeat: reps * 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, Math.max(0, sh.start - ph)); });
    return g; };
  // the lamp light breathes a little (practical lights never sit still)
  const breathe = (tl, el, sh, lo = 0.82, hi = 1, period = 1.3) => tl.fromTo(el, { opacity: hi }, { opacity: lo, duration: period / 2, repeat: Math.ceil(sh.dur / period) * 2 + 1, yoyo: true, ease: "sine.inOut", immediateRender: false }, sh.start);
  // a few birds crossing the far sky
  const birds = (layer, tl, sh, x0, y0, n = 3, color = "#3a3a4a") => { const g = G(layer), r = mk(31);
    for (let k = 0; k < n; k++) g.insertAdjacentHTML("beforeend", `<g class="jkdb"><path d="M-14,0q7,-9 14,0q7,-9 14,0" stroke="${color}" stroke-width="3" fill="none" transform="translate(${f(x0 + k * 60 + r() * 40)},${f(y0 + k * 22 + r() * 30)})"/></g>`);
    [...g.children].forEach((el, k) => { tl.fromTo(el, { x: 0 }, { x: 520 + k * 60, y: -60 - k * 20, duration: sh.dur + 2, ease: "none", immediateRender: false }, Math.max(0, sh.start - 1));
      tl.fromTo(el.firstChild, { scaleY: 1, svgOrigin: "0 0" }, { scaleY: -1, duration: 0.22, repeat: Math.ceil(sh.dur / 0.22) + 8, yoyo: true, ease: "sine.inOut", immediateRender: false }, Math.max(0, sh.start - 1)); }); };


  // ---- set dressing: the small things that make a place feel lived in (all world coordinates; ground 1400) ----
  const T = (x, y, size, text, o = {}) => `<text x="${f(x)}" y="${f(y)}" text-anchor="${o.anchor || "middle"}" font-family="Kanit" font-weight="${o.w || 800}" font-size="${size}" fill="${o.fill || "#222"}"${o.op ? ` opacity="${o.op}"` : ""}${o.tf ? ` transform="${o.tf}"` : ""}>${text}</text>`;
  const bottle = (x, y, h, c) => `<g transform="translate(${x},${y})"><path d="M-9,0V${-h * 0.6}Q-9,${-h * 0.72} -4,${-h * 0.78}V${-h}H4V${-h * 0.78}Q9,${-h * 0.72} 9,${-h * 0.6}V0Z" fill="${c}"/><path d="M-5,${-h * 0.1}V${-h * 0.6}" stroke="#fff" stroke-width="3" opacity=".45"/><rect x="-6" y="${-h * 0.5}" width="12" height="${h * 0.22}" fill="#f4ecd8" opacity=".8"/></g>`;
  const mug = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-14,0V-30H14V0Z" fill="#c8a050"/><path d="M14,-24q12,0 12,10q0,10 -12,10" stroke="#c8a050" stroke-width="5" fill="none"/><ellipse cy="-30" rx="14" ry="5" fill="#f4e4b0"/></g>`;
  const poster = (x, y, w, h, rot, c, lines) => `<g transform="translate(${x},${y}) rotate(${rot})"><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" fill="${c}"/><rect x="${-w / 2 + 8}" y="${-h / 2 + 8}" width="${w - 16}" height="${h - 16}" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="3"/>
    ${lines.map(([t, dy, sz, col]) => T(0, dy, sz, t, { fill: col || "#2a2420", w: 900 })).join("")}<path d="M${-w / 2},${h / 2 - 20}l14,-10l10,30Z" fill="#000" opacity=".18"/></g>`;
  const bunting = (x0, y0, x1, y1, n, sag = 60) => { let h = `<path d="M${x0},${y0}Q${(x0 + x1) / 2},${(y0 + y1) / 2 + sag} ${x1},${y1}" stroke="#5a3a24" stroke-width="4" fill="none"/>`;
    for (let k = 0; k < n; k++) { const t = (k + 0.5) / n, x = x0 + (x1 - x0) * t, y = (1 - t) * (1 - t) * y0 + 2 * (1 - t) * t * ((y0 + y1) / 2 + sag) + t * t * y1;
      h += `<path d="M${f(x - 16)},${f(y)}L${f(x)},${f(y + 34)}L${f(x + 16)},${f(y)}Z" fill="${["#d8443a", "#f6d36a", "#3a8ac8", "#6ac87a", "#f4ecd8"][k % 5]}"/>`; } return h; };
  const smoke = (layer, tl, sh, x, y, n = 5) => { const g = G(layer); for (let k = 0; k < n; k++) g.insertAdjacentHTML("beforeend", `<circle cx="${x}" cy="${y}" r="${12 + k * 4}" fill="#e8e4e0" opacity="0" style="filter:blur(4px)"/>`);
    [...g.children].forEach((el, k) => { const p = 3.2, reps = Math.ceil(sh.dur / p) + 1, ph = k * (p / n);
      tl.fromTo(el, { x: 0, y: 0, scale: 0.5, svgOrigin: `${x} ${y}` }, { x: 60 + k * 10, y: -170, scale: 1.8, svgOrigin: `${x} ${y}`, duration: p, repeat: reps, ease: "none", immediateRender: false }, Math.max(0, sh.start - ph));
      tl.fromTo(el, { opacity: 0 }, { opacity: 0.45, duration: p / 2, repeat: reps * 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, Math.max(0, sh.start - ph)); }); };
  const cat = (x, y, s = 1, c = "#1a1a22") => `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="-16" rx="30" ry="16" fill="${c}"/><circle cx="26" cy="-30" r="13" fill="${c}"/><path d="M18,-40l-2,-12l9,6zM34,-40l2,-12l-9,6z" fill="${c}"/><path d="M-28,-14q-24,4 -20,-26" stroke="${c}" stroke-width="7" fill="none" stroke-linecap="round"/><circle cx="30" cy="-31" r="2.2" fill="#9ad83a"/><circle cx="22" cy="-31" r="2.2" fill="#9ad83a"/></g>`;
  const pigeon = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse rx="14" ry="9" fill="#6a6a78"/><circle cx="12" cy="-7" r="6" fill="#5a5a68"/><path d="M-14,2l-8,-4" stroke="#5a5a68" stroke-width="3"/><path d="M4,8l0,5M-4,8l0,5" stroke="#d87a3a" stroke-width="2"/></g>`;
  const deco = {
    jkCity: (L, tl, sh, id, o) => {
      put(L.mid, `<g transform="translate(1340,1150)">${[...Array(6)].map((_, k) => `<rect x="${k * 36}" y="0" width="22" height="200" fill="#f4ecd8" opacity=".7"/>`).join("")}</g>`);   // zebra crossing on the road
      put(L.set, `<g transform="translate(160,1400)"><rect x="-10" y="-420" width="20" height="420" fill="#4a4a54"/><rect x="-110" y="-440" width="220" height="24" rx="6" fill="#5a5a66"/><rect x="-100" y="-416" width="200" height="140" rx="8" fill="#8ac8ff" opacity=".85"/>
          ${T(0, -358, 36, "BUS", { fill: "#1a2a4a", w: 900 })}${T(0, -318, 22, "สาย 112", { fill: "#2a4a8a", w: 800 })}<rect x="-80" y="-60" width="160" height="14" rx="4" fill="#6a6a72"/><path d="M-60,-46V0M60,-46V0" stroke="#4a4a54" stroke-width="8"/></g>
        <g transform="translate(1330,1400)"><rect x="-26" y="-700" width="52" height="700" fill="#3a3a44"/><rect x="-60" y="-690" width="120" height="330" rx="14" fill="#1a1a22"/><circle cy="-600" r="30" fill="#ff3a2a" opacity=".95"/><circle cy="-520" r="30" fill="#5a4a20"/><circle cy="-440" r="30" fill="#2a5a30"/>
          <g transform="translate(70,-620)"><rect x="-6" y="0" width="12" height="260" fill="#2a2a32"/><rect x="-40" y="-20" width="80" height="330" rx="10" fill="#ff5ab0" opacity=".9"/>${T(0, 60, 42, "24", { fill: "#fff", w: 900 })}${T(0, 120, 30, "ชม.", { fill: "#fff", w: 900 })}${T(0, 190, 26, "เปิด", { fill: "#fff", w: 800 })}${T(0, 240, 26, "ตลอด", { fill: "#fff", w: 800 })}</g></g>
        <g transform="translate(520,1400)"><path d="M-30,0L-24,-60H24L30,0Z" fill="#c8664a"/><ellipse cy="-60" rx="24" ry="8" fill="#a8503a"/><path d="M-20,-66q-20,-50 -2,-80M0,-66q0,-60 14,-84M20,-66q24,-46 4,-78" stroke="#3a7a4a" stroke-width="8" fill="none" stroke-linecap="round"/></g>
        <g transform="translate(300,1400)"><circle cx="-60" cy="-30" r="30" fill="none" stroke="#2a2a32" stroke-width="6"/><circle cx="60" cy="-30" r="30" fill="none" stroke="#2a2a32" stroke-width="6"/><path d="M-60,-30L-20,-90H30L60,-30M-20,-90L0,-30M30,-90L10,-110" stroke="#d8443a" stroke-width="6" fill="none"/></g>
        ${pigeon(900, 1396)}${pigeon(950, 1398, 0.9)}${pigeon(240, 1480, 1.1)}
        <g transform="translate(-200,1400)"><rect x="-40" y="-200" width="80" height="200" rx="10" fill="#4a7a9a"/><rect x="-30" y="-150" width="60" height="100" rx="6" fill="#dff4ff" opacity=".9"/><rect x="-24" y="-190" width="48" height="24" rx="4" fill="#ff8a3a"/></g>`);
      put(L.glow, `<g style="mix-blend-mode:screen"><rect x="1360" y="750" width="80" height="330" rx="20" fill="#ff5ab0" opacity=".35" style="filter:blur(22px)"/><circle cx="1330" cy="800" r="60" fill="#ff3a2a" opacity=".45" style="filter:blur(16px)"/><rect x="60" y="990" width="200" height="140" fill="#8ac8ff" opacity=".3" style="filter:blur(18px)"/></g>`);
    },
    jkCloud: (L, tl, sh, id, o) => {
      put(L.far, `<g transform="translate(-700,760)" opacity=".55"><ellipse rx="220" ry="40" fill="#e8e0e8"/><ellipse cy="-20" rx="160" ry="30" fill="#f4eef4"/><rect x="-40" y="-120" width="80" height="100" fill="#f0e2c8"/><path d="M-60,-120L0,-170L60,-120Z" fill="#e8c86a"/></g>
        <path d="M-400,900Q780,-100 1960,900" stroke="url(#jkRay)" stroke-width="60" fill="none" opacity=".25" style="filter:blur(20px)"/>`);
      put(L.set, `<g transform="translate(330,1400)"><rect x="-8" y="-330" width="16" height="330" fill="#c8a43a"/><g transform="translate(0,-300)"><path d="M-110,-30H90L120,0L90,30H-110Z" fill="#f6d36a"/>${T(-8, 11, 30, "ต่อแถว สุ่มสกิล", { fill: "#5a3a24", w: 900 })}</g><g transform="translate(0,-230)"><path d="M-100,-26H70L96,0L70,26H-100Z" fill="#f4ecd8"/>${T(-14, 9, 24, "ไม่รับคืนนะจ๊ะ", { fill: "#a8243a", w: 900 })}</g></g>`);
      const g = G(L.mid, [[-200, 760], [160, 640], [1500, 700], [1900, 820]].map(([x, y], k) => `<g class="lan"><g transform="translate(${x},${y})"><path d="M-30,-40Q-40,0 -30,40H30Q40,0 30,-40Z" fill="#ffb060" opacity=".9"/><rect x="-18" y="-50" width="36" height="12" rx="4" fill="#a8243a"/><rect x="-18" y="38" width="36" height="12" rx="4" fill="#a8243a"/><circle r="34" fill="#ffd890" opacity=".35" style="filter:blur(10px)"/></g></g>`).join(""));
      [...g.children].forEach((el, k) => { const p = 4 + k * 0.7; tl.fromTo(el, { y: 0 }, { y: -26, duration: p / 2, repeat: Math.ceil(sh.dur / p) * 2 + 1, yoyo: true, ease: "sine.inOut", immediateRender: false }, Math.max(0, sh.start - k * 0.9)); });
    },
    jkTown: (L, tl, sh, id, o) => {
      put(L.set, `${bunting(560, 430, 1440, 430, 14, 50)}${bunting(-200, 760, 560, 430, 10, 60)}
        <g transform="translate(60,1400)"><rect x="-160" y="-220" width="320" height="220" fill="#8a5a34"/><rect x="-170" y="-236" width="340" height="24" rx="6" fill="#6a4a2a"/><path d="M-200,-236L-170,-360H170L200,-236Z" fill="#d8443a"/>${[...Array(6)].map((_, k) => `<path d="M${-170 + k * 56 + 10},-360L${-200 + k * 66 + 12},-236H${-200 + k * 66 + 40}L${-170 + k * 56 + 38},-360Z" fill="#f4ecd8"/>`).join("")}
          ${[[-110, "#e8a030"], [-50, "#d8443a"], [10, "#6ac87a"], [70, "#f6d36a"], [120, "#c87ac8"]].map(([x, c]) => `<g transform="translate(${x},-250)">${[0, 1, 2].map((j) => `<circle cx="${(j - 1) * 14}" cy="${j === 1 ? -14 : 0}" r="11" fill="${c}"/>`).join("")}</g>`).join("")}
          <rect x="-150" y="-300" width="300" height="40" rx="6" fill="#f4ecd8"/>${T(0, -270, 24, "ผลไม้สด · ของดีเมืองนี้", { fill: "#5a3a24", w: 900 })}</g>
        ${[[-330, -300], [330, -300]].map(([x, y]) => `<g transform="translate(${1000 + x},${1180 + y + 48})"><rect x="-40" y="-14" width="80" height="20" rx="4" fill="#8a5a34"/>${[-24, 0, 24].map((dx) => `<circle cx="${dx}" cy="-22" r="9" fill="${["#d8443a", "#f6d36a", "#ff8ab0"][(dx + 24) / 24]}"/>`).join("")}<path d="M-30,-14q0,-12 8,-14M30,-14q0,-12 -8,-14" stroke="#4a8a4a" stroke-width="4" fill="none"/></g>`).join("")}
        <g transform="translate(1780,1180)"><rect x="-60" y="-140" width="120" height="140" fill="#9a9a9a"/><ellipse cy="-140" rx="60" ry="14" fill="#7a7a7a"/><rect x="-8" y="-260" width="16" height="120" fill="#5a3a24"/><path d="M-70,-260H70L0,-320Z" fill="#a8484a"/></g>`);
      smoke(L.mid, tl, sh, 1000 + 180, 1180 - 1030 + 300, 5);
    },
    jkAlley: (L, tl, sh, id, o) => {
      put(L.set, `${poster(230, 700, 190, 250, -4, "#e8d8b8", [["WANTED", -70, 34, "#a8243a"], ["จอมโกหก", -20, 26], ["?", 50, 70, "#2a2420"], ["ค่าหัว 0 เหรียญ", 100, 18]])}
        ${poster(1430, 820, 170, 210, 3, "#d8c8a0", [["กิลด์ผู้กล้า", -60, 24, "#5a3a24"], ["รับสมัคร", -20, 26], ["ระดับ F", 30, 22, "#a8243a"], ["ไม่รับ", 70, 22, "#a8243a"]])}
        <g transform="translate(1560,300)"><rect x="-14" y="0" width="28" height="1100" fill="#2e2a30"/><rect x="-18" y="40" width="36" height="20" fill="#3a3640"/><rect x="-18" y="500" width="36" height="20" fill="#3a3640"/><path d="M14,0q50,0 50,50v30" stroke="#2e2a30" stroke-width="28" fill="none"/></g>
        <g transform="translate(170,1400)"><rect x="-50" y="-130" width="100" height="130" rx="8" fill="#4a5a4a"/><rect x="-56" y="-142" width="112" height="20" rx="6" fill="#3a4a3a"/><path d="M-30,-142V-160H30V-142" stroke="#3a4a3a" stroke-width="8" fill="none"/><path d="M40,-150q20,-30 30,-10" stroke="#e8d8b8" stroke-width="6" fill="none"/></g>
        ${cat(1290, 1200, 1.1)}<ellipse cx="1060" cy="1520" rx="150" ry="22" fill="#ffd090" opacity=".16"/><ellipse cx="1060" cy="1520" rx="150" ry="22" fill="none" stroke="#ffe0a0" stroke-opacity=".25" stroke-width="2"/>
        <g transform="translate(700,1400)"><rect x="-60" y="-80" width="120" height="80" fill="#6a4a2a"/><path d="M-60,-80L60,0M60,-80L-60,0" stroke="#4a3018" stroke-width="6"/>${T(0, -32, 18, "กิลด์", { fill: "#e8d8b8", w: 900, op: 0.7 })}</g>`);
      put(L.far, `<path d="M-2400,900H3800" stroke="#c8d8ff" stroke-opacity=".18" stroke-width="3"/>`);
    },
    jkTavern: (L, tl, sh, id, o) => {
      put(L.mid, `<g transform="translate(1250,640)"><rect x="-250" y="0" width="500" height="14" fill="#4a2e1c"/><rect x="-250" y="14" width="500" height="8" fill="#2a180e" opacity=".6"/>
          ${[[-200, 70, "#3a8a5a"], [-160, 52, "#c84a3a"], [-120, 76, "#d8b84a"], [-70, 60, "#5a7ac8"], [-30, 70, "#3a8a5a"], [20, 56, "#a84a8a"], [70, 72, "#c84a3a"], [120, 60, "#d8b84a"], [170, 74, "#5a7ac8"], [210, 50, "#3a8a5a"]].map(([x, h, c]) => bottle(x, 0, h, c)).join("")}
          ${[-180, -100, -20, 60, 140, 220].map((x) => `<g transform="translate(${x},40)"><path d="M0,0v16" stroke="#2a180e" stroke-width="3"/>${mug(0, 50, 0.9)}</g>`).join("")}</g>
        <g transform="translate(1250,470)"><circle r="56" fill="#8a5a34"/><circle r="44" fill="#d8443a"/><circle r="30" fill="#f6d36a"/><path d="M-48,-48L48,48M48,-48L-48,48" stroke="#c8c8cc" stroke-width="8"/><circle r="12" fill="#5a3a24"/></g>
        ${[-300, 620, 1540].map((x) => `<g transform="translate(${x},280)"><path d="M0,0v60" stroke="#5a3a24" stroke-width="3"/>${[0, 1, 2, 3].map((k) => `<ellipse cx="${(k % 2 ? 8 : -8)}" cy="${70 + k * 16}" rx="12" ry="9" fill="${["#e8e0c8", "#d8c8a0"][k % 2]}"/>`).join("")}</g>`).join("")}
        <g transform="translate(-900,560)"><rect x="-130" y="-70" width="260" height="140" rx="10" fill="#4a2e1c"/><rect x="-118" y="-58" width="236" height="116" rx="6" fill="#e8d8b8"/>${T(0, -14, 28, "เมนูวันนี้", { fill: "#5a3a24", w: 900 })}${T(0, 24, 20, "สตูว์ · ขนมปัง · เบียร์", { fill: "#3a2a20", w: 800 })}</g>`);
      put(L.set, `<g transform="translate(1600,1400)">${[[0, 0], [90, 0], [45, -120]].map(([x, y]) => `<g transform="translate(${x},${y})"><path d="M-40,-120Q-50,-60 -40,0H40Q50,-60 40,-120Z" fill="#7a4e2a"/><path d="M-44,-96H44M-46,-30H46" stroke="#4a4a52" stroke-width="7"/><ellipse cy="-120" rx="40" ry="10" fill="#5a3a20"/></g>`).join("")}</g>
        <ellipse cx="500" cy="1500" rx="420" ry="90" fill="#8a3a3a" opacity=".22"/><ellipse cx="500" cy="1500" rx="380" ry="74" fill="none" stroke="#f6d36a" stroke-opacity=".2" stroke-width="6"/>
        ${[[290, 1164], [690, 1164]].map(([x, y]) => `${mug(x + 110, y, 1)}<g transform="translate(${x - 110},${y})"><ellipse rx="26" ry="8" fill="#e8e2d6"/><ellipse cy="-5" rx="18" ry="5" fill="#c8a050"/><path d="M-10,-6q10,-10 20,0" stroke="#a86a3a" stroke-width="3" fill="none"/></g>`).join("")}`);
    },
  };

  const dress = {};
  // ---- Earth at dusk: the sun low on the right throws long shadows left; the lamp and the office window glow ----
  dress.jkCity = (L, tl, sh, id, o) => {
    put(L.mid, `${[-700, -300, 140, 560, 980, 1420, 1860].map((x) => ao(x, 1232, 112, 14, 0.4, 8)).join("")}<rect x="-2400" y="760" width="6200" height="400" fill="#f6c090" opacity=".08"/>`);
    put(L.set, `${band(1300, 70, 0.5)}${cast(840, 440, 1360, 160, -260, 0.18, 10)}${cast(370, 20, 1400, 120, -300, 0.25, 6)}${cast(430, 420, 1400, 90, -200, 0.14, 10)}
      ${ao(640, 1402, 150, 16, 0.3)}${ao(380, 1402, 60, 12, 0.4)}${cyl(840, 800, 440, 560, 0.55)}<rect x="840" y="800" width="440" height="560" fill="url(#jkdAOup)" opacity=".35"/>
      ${o.manhole ? ao(1180, 1526, 150, 30, 0.35) : ""}`);
    const g = G(L.glow, `<g style="mix-blend-mode:screen">${cone(480, 630, 40, 760, 0.7)}<ellipse cx="1060" cy="1140" rx="260" ry="200" fill="url(#jkdSoftL)" opacity=".45"/></g>`);
    breathe(tl, g.firstChild.firstChild, sh, 0.8, 1, 1.7);
    motes(L.set, tl, sh, { x: 300, y: 700, w: 400, h: 700, n: 10, r: 2.4, color: "#ffe8b0", dy: -40, period: 5, op: 0.5, seed: 3 });
    const win = [...L.far.querySelectorAll('rect[fill="#ffd890"]')].filter((_, k) => k % 7 === 0).slice(0, 24);
    win.forEach((w, k) => breathe(tl, w, sh, 0.25, 0.9, 1.1 + (k % 5) * 0.37));
  };
  // ---- the clouds: rays that breathe, gold sparkles, a round machine, shadows under everything ----
  dress.jkCloud = (L, tl, sh, id, o) => {
    put(L.set, `${ao(820, 1404, 190, 22, 0.28)}${ao(1260, 1404, 220, 22, 0.22)}${[100, 280, 460].map((x) => ao(x, 1402, 34, 8, 0.35, 5)).join("")}
      ${cyl(670, 1070, 300, 330, 0.7, 24)}<rect x="670" y="1340" width="300" height="60" fill="url(#jkdAO)" opacity=".35"/>
      <ellipse cx="820" cy="860" rx="190" ry="190" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="3"/><ellipse cx="760" cy="790" rx="70" ry="38" fill="#fff" opacity=".35" transform="rotate(-30 760 790)" style="filter:blur(10px)"/>`);
    put(L.mid, `<rect x="-2400" y="1000" width="6200" height="400" fill="#dfe8f8" opacity=".14"/>`);
    const g = G(L.glow, `<g style="mix-blend-mode:screen"><path d="M300,-200H420L760,1500H200Z" fill="url(#jkRay)" opacity=".16" style="filter:blur(20px)"/><path d="M1100,-200H1180L1500,1500H1240Z" fill="url(#jkRay)" opacity=".14" style="filter:blur(20px)"/></g>`);
    [...g.firstChild.children].forEach((el, k) => breathe(tl, el, sh, 0.35, 1, 2.6 + k * 0.7));
    motes(L.set, tl, sh, { x: 200, y: 700, w: 900, h: 700, n: 18, r: 3, color: "#fff4c0", dy: -90, dx: 24, period: 4, op: 0.85, seed: 11 });
    motes(L.fg, tl, sh, { x: -100, y: 600, w: 1300, h: 1300, n: 5, r: 9, color: "#fff8e0", dy: -60, period: 6, op: 0.35, blur: 6, seed: 12 });
  };
  // ---- the town: afternoon sun from the upper left, long shadows across the plaza, pollen in the rays, birds ----
  dress.jkTown = (L, tl, sh, id, o) => {
    put(L.mid, `<rect x="-2400" y="900" width="6200" height="300" fill="#f4e0b8" opacity=".12"/>${band(1100, 80, 0.45)}`);
    put(L.set, `${cast(620, 760, 1180, 330, 260, o.dusk ? 0.12 : 0.2, 14)}${cast(40, 400, 1300, 160, 150, 0.14, 12)}${[500, 1500].map((x) => cast(x - 6, 12, 1180, 180, 130, 0.22, 5)).join("")}
      ${ao(240, 1340, 220, 30, 0.25)}${ao(1000, 1184, 400, 26, 0.3)}${ao(750, 1184, 20, 8, 0.45, 4)}${ao(1250, 1184, 20, 8, 0.45, 4)}
      <rect x="620" y="420" width="60" height="760" fill="url(#jkdAOup)" opacity=".25" transform="rotate(90 650 800)"/><rect x="620" y="420" width="760" height="760" fill="url(#jkdAO)" opacity=".18"/>
      <radialGradient id="${id}-plaza" cx=".45" cy=".3" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".12"/><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></radialGradient>
      <rect x="-800" y="1180" width="2700" height="900" fill="url(#${id}-plaza)"/>`);
    if (!o.dusk) { motes(L.set, tl, sh, { x: -200, y: 400, w: 900, h: 900, n: 16, r: 2.6, color: "#fff0b0", dy: -50, dx: 40, period: 5, op: 0.6, seed: 17 }); birds(L.far, tl, sh, -300, 560, 3); }
    else { const g = G(L.glow, `<g style="mix-blend-mode:screen">${cone(670, 920, 30, 420, 0.8)}${cone(1330, 920, 30, 420, 0.8)}</g>`); [...g.firstChild.children].forEach((el, k) => breathe(tl, el, sh, 0.7, 1, 1.1 + k * 0.3)); }
  };
  // ---- the alley: one lamp over the back door does all the work ----
  dress.jkAlley = (L, tl, sh, id, o) => {
    put(L.set, `${band(1330, 70, 0.7)}${ao(520, 1402, 110, 16, 0.5)}${ao(310, 1402, 90, 14, 0.5)}${ao(1160, 1402, 74, 14, 0.5)}${ao(1290, 1402, 74, 14, 0.5)}${ao(860, 1404, 130, 14, 0.4)}
      <path d="M430,1250H610L640,1400H400Z" fill="#ffd890" opacity=".07"/><path d="M440,1250H600" stroke="#ffe0a0" stroke-width="4" opacity=".35"/>
      <ellipse cx="1000" cy="1470" rx="420" ry="46" fill="#ffd090" opacity=".08" style="filter:blur(14px)"/>`);
    const g = G(L.glow, `<g style="mix-blend-mode:screen">${cone(1016, 870, 30, 560, 0.85)}</g>`);
    breathe(tl, g.firstChild.firstChild, sh, 0.78, 1, 1.5);
    motes(L.set, tl, sh, { x: 820, y: 880, w: 400, h: 500, n: 12, r: 2.6, color: "#ffe6b8", dy: -40, dx: 20, period: 4.5, op: 0.6, seed: 5 });
    motes(L.set, tl, sh, { x: -200, y: 700, w: 700, h: 500, n: 5, r: 3.2, color: "#b8ffb0", dy: 30, dx: 60, period: 6, op: 0.7, seed: 6 });   // fireflies
  };
  // ---- the tavern: lantern cones, embers from the fire, dust in the light, shadows under the furniture ----
  dress.jkTavern = (L, tl, sh, id, o) => {
    const lamps = [[-900, 360], [100, 330], [1000, 360], [1900, 330]];
    put(L.mid, `${band(220, 90, 0.6)}${band(1100, 80, 0.5)}<rect x="-2400" y="280" width="6200" height="900" fill="url(#jkdAOup)" opacity=".12"/>`);
    put(L.set, `${[[290, 1400, 160], [690, 1400, 160]].map(([x, y, rx]) => ao(x, y + 2, rx, 18, 0.45)).join("")}${[150, 440, 560, 840].map((x) => ao(x, 1402, 44, 10, 0.5, 6)).join("")}
      ${ao(1250, 1404, 290, 20, 0.45)}${[[290, 1164], [690, 1164]].map(([x, y]) => `<rect x="${x - 150}" y="${y}" width="300" height="6" fill="#fff" opacity=".18"/>`).join("")}
      <path d="M1620,420H1920L1980,1400H1560Z" fill="url(#jkdMoon)" opacity=".5" style="filter:blur(16px)"/>
      <path d="M-520,1180Q-380,1100 -240,1180" fill="none" stroke="#ff9a3a" stroke-width="3" opacity=".25"/>`);
    const g = G(L.glow, `<g style="mix-blend-mode:screen">${lamps.map(([x, y]) => cone(x, y + 40, 26, 640, 0.75)).join("")}<ellipse cx="-380" cy="1120" rx="260" ry="90" fill="url(#jkdSoftL)" opacity=".5"/></g>`);
    [...g.firstChild.children].slice(0, 4).forEach((el, k) => breathe(tl, el, sh, 0.72, 1, 1.2 + k * 0.23));
    motes(L.set, tl, sh, { x: -80, y: 380, w: 1300, h: 800, n: 16, r: 2.4, color: "#ffe8c0", dy: -36, dx: 24, period: 5, op: 0.55, seed: 21 });
    motes(L.set, tl, sh, { x: -470, y: 900, w: 180, h: 260, n: 9, r: 2.2, color: "#ffb050", dy: -220, dx: 50, period: 1.6, op: 0.9, seed: 22 });   // embers
  };
  Object.keys(dress).forEach((k) => { const d = dress[k]; dress[k] = (L, tl, sh, id, o) => { if (Q.get("nodepth")) return; if (deco[k] && !Q.get("nodeco")) deco[k](L, tl, sh, id, o); d(L, tl, sh, id, o); }; });
  window.JKD = { dress, deco, ao, band, cyl, cone, cast, motes, breathe, birds, smoke };
})();
