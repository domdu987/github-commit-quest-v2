// ---------- หมาดำตาสี่ · V11 pass: 2.5D coins, living cards and effects (load after quakeui.js and rabui.js; overrides RabUI cards) ----------
// Same 2.5D language as ตึกโยก (QkUI): every icon is a coin with a rim (depth), a lit face, a bevel, a gloss and a floating shadow; it
// pops in with squash & stretch (QkUI.iconPop) and keeps a secondary motion (QkUI.iconLife + its own .rbAn loops). Cards are slabs with depth.
//   RabFX.coin(name) / QkUI.ICON.<name>  coins: pupno (puppy + ban) · lick (tongue on a graze) · syringe · clock · house (dog at home) ·
//                                        herb (poultice, crossed) · tell (speech) · shh (finger on lips) · drop (saliva + virus)
//   RabUI.rules(tl, layer, t0, dur, o)   the zinc board: per row a coin sticker; the chalk writes the active rule stroke by stroke with chalk
//                                        dust falling off the stick, a highlighter swipe; done rows tick with a glow ring + sparkles · o.tickAt
//   RabUI.saliva(...)                    a slab card: the saliva drop glints and drips; intact skin → it beads off, ✓ stamp with glow;
//                                        a graze → the wound throbs red, bullet-shaped virus wriggles in and races up a glowing nerve, ✗ stamp
//                                        with a shake and a red flash
//   RabUI.pupAge(...)                    a slab card: 2.5D month blocks rise in turn, 2–6 lift and glow red, the bracket draws, the label pops
//   RabFX.motes(tl, layer, t0, dur, o)   dust in a light beam (o.kind "dust") or fireflies at dusk ("fly"): drifting, twinkling · o.box [x, y, w, h], o.n
//   RabFX.bloom(layer, x, y, r, id)      a soft green bloom for glowing eyes (draw in L.glow), RabFX.pulse(tl, sel, t0, dur, period) its throb
//   RabFX.drool(tl, layer, x, y, t0, dur) a drip forming, stretching, falling, with a glint
//   RabFX.flash(tl, t0, color)           a full-frame flash (impact / wrong), RabFX.shakeSel(tl, sel, t0) a damped shake of one element
(function () {
  const INK = "#2a2420", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  let seq = 0; const nid = () => "rx" + (seq++);
  const PAL = { pupno: ["#ffe2c8", "#fff8f0", "#e0703a", "#a84a1e"], lick: ["#ffd8dc", "#fff4f5", "#d8506a", "#a02a44"], syringe: ["#d6ecfb", "#f6fbff", "#3a8ad0", "#22609a"],
    clock: ["#fde59a", "#fffbe8", "#e3a632", "#a8741a"], house: ["#d8f0c8", "#f7fff2", "#6aaa52", "#44803a"], herb: ["#e4f2cc", "#fbfff2", "#7aa83a", "#4e7a1e"],
    tell: ["#d8f0c8", "#f7fff2", "#2fa864", "#1e7a48"], shh: ["#ffd8d0", "#fff4f0", "#e2382e", "#a81e18"], drop: ["#d6ecfb", "#f6fbff", "#6a5ab8", "#443a8a"] };
  let defs = "";
  for (const [n, [b, l, r, rd]] of Object.entries(PAL)) defs += `<radialGradient id="rbF-${n}" cx=".33" cy=".25" r=".9"><stop offset="0" stop-color="${l}"/><stop offset=".55" stop-color="${b}"/><stop offset="1" stop-color="${r}" stop-opacity=".55"/></radialGradient>
    <linearGradient id="rbR-${n}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${r}"/><stop offset="1" stop-color="${rd}"/></linearGradient>`;
  Sets.DEFS += defs + `
    <radialGradient id="rbBloom"><stop offset="0" stop-color="#eaffc0" stop-opacity=".95"/><stop offset=".25" stop-color="#9aff5a" stop-opacity=".55"/><stop offset="1" stop-color="#5aff4a" stop-opacity="0"/></radialGradient>
    <radialGradient id="rbMote"><stop offset="0" stop-color="#fff6d8" stop-opacity="1"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></radialGradient>
    <radialGradient id="rbFly"><stop offset="0" stop-color="#f4ffb0" stop-opacity="1"/><stop offset=".35" stop-color="#c8ff5a" stop-opacity=".6"/><stop offset="1" stop-color="#c8ff5a" stop-opacity="0"/></radialGradient>
    <radialGradient id="rbWound"><stop offset="0" stop-color="#ff5a4a" stop-opacity=".9"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="rbOkGlow"><stop offset="0" stop-color="#b8ffc8" stop-opacity=".9"/><stop offset="1" stop-color="#5aef8a" stop-opacity="0"/></radialGradient>
    <linearGradient id="rbSlabF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf6"/><stop offset="1" stop-color="#efe6d0"/></linearGradient>
    <linearGradient id="rbBlock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaf0"/><stop offset="1" stop-color="#e2d8c2"/></linearGradient>
    <linearGradient id="rbBlockHot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd2c8"/><stop offset="1" stop-color="#ff8a74"/></linearGradient>`;

  // ---------------- pictograms (0–120 box): [inside the face (clipped), on top] ----------------
  const pup = (x, y, s) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-30,6C-34,-26 -12,-40 6,-40C28,-40 40,-24 38,-2C50,2 54,12 46,18C36,24 20,22 10,24C-10,28 -28,22 -30,6Z" fill="#ecd2a6" ${OUT(3)}/>
    <path d="M-18,-30C-34,-46 -40,-22 -30,-10Z" fill="#9a5a32" ${OUT(2.6)}/><circle cx="12" cy="-12" r="5" fill="${INK}"/><circle cx="13.5" cy="-13.5" r="1.8" fill="#fff"/><ellipse cx="46" cy="8" rx="6" ry="5" fill="${INK}"/></g>`;
  const PICT = {
    pupno: () => [`<g class="rbAn" data-a="wag">${pup(54, 76, 0.95)}</g>`, `<circle cx="60" cy="60" r="40" fill="none" stroke="#7a140e" stroke-width="11" opacity=".5" transform="translate(2,3)"/><circle cx="60" cy="60" r="40" fill="none" stroke="#e2382e" stroke-width="10"/><path d="M32,32L88,88" stroke="#e2382e" stroke-width="10" stroke-linecap="round"/>`],
    lick: () => [`<path d="M14,84Q60,70 106,84V120H14Z" fill="#f0c4a0" ${OUT(3)}/><path d="M48,80L56,96L62,82L70,98L76,80" fill="#c8282a" ${OUT(2.5)}/>
      <g class="rbAn" data-a="lick"><path d="M56,18Q40,40 46,60Q54,76 66,62Q74,44 64,18Z" fill="#e8607a" ${OUT(3)}/><path d="M57,30Q54,46 58,58" stroke="#b83a52" stroke-width="3" fill="none"/></g>`, ""],
    syringe: () => ["", `<g transform="rotate(-38 60 60)" class="rbAn" data-a="push"><rect x="44" y="28" width="32" height="58" rx="6" fill="#e6f4ff" ${OUT(3.5)}/><rect x="48" y="52" width="24" height="30" rx="3" fill="#7ac0f0"/>
      <path d="M50,40H70M50,48H70" stroke="#3a6a9a" stroke-width="2.5"/><rect x="40" y="24" width="40" height="8" rx="3" fill="#c8ccd2" ${OUT(2.5)}/><rect x="56" y="6" width="8" height="20" fill="#c8ccd2" ${OUT(2.5)}/><rect x="48" y="2" width="24" height="7" rx="3" fill="#8a98a4" ${OUT(2.5)}/>
      <path d="M60,86V112" stroke="#8a98a4" stroke-width="4"/><path d="M60,86V112" stroke="${INK}" stroke-width="1.2"/><path d="M50,34V80" stroke="#fff" stroke-width="3" opacity=".6"/></g>`],
    clock: () => ["", `<circle cx="60" cy="62" r="36" fill="#fffbe8" ${OUT(4)}/>${[0, 90, 180, 270].map((a) => `<path d="M60,30V36" stroke="${INK}" stroke-width="4" transform="rotate(${a} 60 62)"/>`).join("")}
      <g class="rbAn" data-a="spin"><path d="M60,62V38" stroke="#e2382e" stroke-width="5" stroke-linecap="round"/></g><path d="M60,62L74,70" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><circle cx="60" cy="62" r="4" fill="${INK}"/>`],
    house: () => [`<path d="M20,64L60,30L100,64V110H20Z" fill="#c8925a" ${OUT(3.5)}/><path d="M12,66L60,24L108,66" fill="none" stroke="#8a3a2a" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M44,110V80Q60,66 76,80V110Z" fill="#2a1c18"/><g class="rbAn" data-a="peek"><circle cx="54" cy="92" r="4" fill="#9aff5a"/><circle cx="66" cy="92" r="4" fill="#9aff5a"/></g>`, ""],
    herb: () => [`<ellipse cx="60" cy="70" rx="38" ry="28" fill="#f0c4a0" ${OUT(3)}/><ellipse cx="60" cy="68" rx="26" ry="17" fill="#6a9a3a" ${OUT(3)}/><path d="M44,64q8,6 16,0q8,6 16,0" stroke="#3a6a1e" stroke-width="3" fill="none"/>`,
      `<g class="rbAn" data-a="xpop"><path d="M30,30L90,90M90,30L30,90" stroke="#7a140e" stroke-width="14" stroke-linecap="round" opacity=".45" transform="translate(2,3)"/><path d="M30,30L90,90M90,30L30,90" stroke="#e2382e" stroke-width="12" stroke-linecap="round"/></g>`],
    tell: () => ["", `<g class="rbAn" data-a="bob"><path d="M22,30H98Q104,30 104,36V74Q104,80 98,80H56L38,96V80H22Q16,80 16,74V36Q16,30 22,30Z" fill="#fff" ${OUT(4)}/>
      <circle cx="42" cy="55" r="6" fill="#2fa864"/><circle cx="60" cy="55" r="6" fill="#2fa864"/><circle cx="78" cy="55" r="6" fill="#2fa864"/></g>`],
    shh: () => [`<circle cx="60" cy="58" r="32" fill="#e8b88e" ${OUT(3)}/><path d="M46,70Q60,76 74,70" stroke="${INK}" stroke-width="4" fill="none"/><circle cx="48" cy="50" r="4" fill="${INK}"/><circle cx="72" cy="50" r="4" fill="${INK}"/>`,
      `<g class="rbAn" data-a="bob"><rect x="55" y="48" width="12" height="42" rx="6" fill="#f2c8a0" ${OUT(3)}/></g>`],
    drop: () => ["", `<g class="rbAn" data-a="drip"><path d="M60,16Q36,52 36,72A24,24 0 0 0 84,72Q84,52 60,16Z" fill="#cfe8ff" ${OUT(4)}/><path d="M48,66Q48,52 56,40" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>
      <g transform="translate(64,74) rotate(-30)"><path d="M-12,-5H6Q13,-5 13,0Q13,5 6,5H-12Z" fill="#7a2a8a" ${OUT(2)}/></g></g>`],
  };
  const coin = (name) => {
    const [inside, top] = PICT[name]();
    return `<ellipse class="quSh" cx="60" cy="120" rx="50" ry="9" fill="url(#quCoinSh)"/>
      <g class="quBob"><g class="quSq">
        <circle cx="60" cy="67" r="52" fill="url(#rbR-${name})" ${OUT(4)}/><path d="M12,67A48,48 0 0 0 108,67" stroke="#000" stroke-width="3" fill="none" opacity=".18"/>
        <circle cx="60" cy="57" r="52" fill="url(#rbF-${name})" ${OUT(4)}/><circle cx="60" cy="57" r="45.5" fill="none" stroke="url(#quBev)" stroke-width="4"/>
        <g transform="translate(60,57) scale(.9) translate(-60,-60)">${inside ? `<g clip-path="url(#quPicClip)">${inside}</g>` : ""}${top}</g>
        <path d="M21,46A41,41 0 0 1 45,19" stroke="#fff" stroke-width="5.5" fill="none" opacity=".72" stroke-linecap="round"/><circle cx="53.5" cy="15.5" r="2.8" fill="#fff" opacity=".7"/>
      </g></g>`;
  };
  Object.keys(PICT).forEach((n) => (QkUI.ICON[n] = () => coin(n)));
  const RabFX = {};
  RabFX.coin = (name, x, y, s = 1, id = "") => `<g transform="translate(${x},${y}) scale(${s})"><g ${id ? `id="${id}"` : ""}>${coin(name)}</g></g>`;
  // the coins' own loops (on top of QkUI.iconLife's float)
  RabFX.life = (tl, root, t, dur) => {
    if (!root) return;
    QkUI.iconLife(tl, root, t, dur);
    const R = (p) => Math.ceil(dur / p) + 1;
    root.querySelectorAll(".rbAn").forEach((e) => {
      const a = e.dataset.a;
      if (a === "wag") tl.fromTo(e, { rotation: -6, svgOrigin: "54 90" }, { rotation: 6, svgOrigin: "54 90", duration: 0.22, repeat: R(0.22), yoyo: true, ease: "sine.inOut", immediateRender: false }, t);
      if (a === "lick") tl.fromTo(e, { scaleY: 0.55, svgOrigin: "60 18" }, { scaleY: 1.08, svgOrigin: "60 18", duration: 0.28, repeat: R(0.28), yoyo: true, ease: "power2.inOut", immediateRender: false }, t);
      if (a === "push") tl.fromTo(e, { y: -4 }, { y: 6, duration: 0.4, repeat: R(0.4), yoyo: true, ease: "power2.in", immediateRender: false }, t);
      if (a === "spin") tl.fromTo(e, { rotation: 0, svgOrigin: "60 62" }, { rotation: 360, svgOrigin: "60 62", duration: 1.2, repeat: R(1.2), ease: "none", immediateRender: false }, t);
      if (a === "peek") tl.fromTo(e, { opacity: 0.2 }, { opacity: 1, duration: 0.5, repeat: R(0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t);
      if (a === "xpop") tl.fromTo(e, { scale: 1, svgOrigin: "60 60" }, { scale: 1.12, svgOrigin: "60 60", duration: 0.3, repeat: R(0.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t);
      if (a === "bob") tl.fromTo(e, { y: 2, rotation: -3, svgOrigin: "60 60" }, { y: -3, rotation: 3, svgOrigin: "60 60", duration: 0.45, repeat: R(0.45), yoyo: true, ease: "sine.inOut", immediateRender: false }, t);
      if (a === "drip") tl.fromTo(e, { scaleY: 0.92, scaleX: 1.05, svgOrigin: "60 96" }, { scaleY: 1.06, scaleX: 0.96, svgOrigin: "60 96", duration: 0.36, repeat: R(0.36), yoyo: true, ease: "sine.inOut", immediateRender: false }, t);
    });
  };
  const pop = (tl, id, t) => { const r = document.getElementById(id); QkUI.iconPop(tl, r, t); };

  // ---------------- effects ----------------
  RabFX.flash = (tl, t0, color = "#ff2a1a", op = 0.45) => tl.fromTo("#flashw", { opacity: 0, backgroundColor: color }, { opacity: op, duration: 0.05, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, t0);
  RabFX.shakeSel = (tl, sel, t0, amp = 14) => tl.fromTo(sel, { x: 0 }, { x: amp, duration: 0.45, ease: (p) => Math.sin(p * Math.PI * 8) * (1 - p), immediateRender: false }, t0);
  RabFX.motes = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), r = mk(o.seed || 7), [bx, by, bw, bh] = o.box || [0, 300, 1080, 1300], fly = o.kind === "fly";
    let g = `<g id="${id}">`;
    const n = o.n ?? (fly ? 14 : 34);
    for (let k = 0; k < n; k++) g += `<g transform="translate(${f1(bx + r() * bw)},${f1(by + r() * bh)})"><circle id="${id}-${k}" r="${f1(fly ? 5 + r() * 4 : 2 + r() * 3.5)}" fill="url(#${fly ? "rbFly" : "rbMote"})" opacity="0"/></g>`;
    put(layer, g + `</g>`);
    for (let k = 0; k < n; k++) {
      const e = `#${id}-${k}`, p = 1.4 + r() * 1.8, dx = (r() - 0.5) * (fly ? 140 : 60), dy = fly ? (r() - 0.5) * 90 : -30 - r() * 50;
      tl.fromTo(e, { x: 0, y: 0 }, { x: dx, y: dy, duration: dur, ease: "sine.inOut", immediateRender: false }, t0);
      tl.fromTo(e, { opacity: 0 }, { opacity: fly ? 1 : 0.5 + r() * 0.5, duration: p / 2, repeat: Math.ceil(dur / (p / 2)), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + r() * 0.8);
    }
  };
  RabFX.bloom = (layer, x, y, r, id) => put(layer, `<circle id="${id}" cx="${f1(x)}" cy="${f1(y)}" r="${r}" fill="url(#rbBloom)" style="mix-blend-mode:screen"/>`);
  RabFX.pulse = (tl, sel, t0, dur, period = 0.9, lo = 0.55) => tl.fromTo(sel, { opacity: lo }, { opacity: 1, duration: period / 2, repeat: Math.ceil(dur / (period / 2)), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
  RabFX.drool = (tl, layer, x, y, t0, dur, s = 1) => {
    const id = nid();
    put(layer, `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}"><path id="${id}-s" d="M-5,0Q-6,10 0,16Q6,10 5,0Z" fill="#e8f4ff" ${OUT(1.6)} opacity=".95"/><circle id="${id}-g" cx="-1.5" cy="6" r="1.8" fill="#fff"/></g>
      <circle id="${id}-d" cx="0" cy="18" r="4.5" fill="#e8f4ff" ${OUT(1.4)} opacity="0"/></g>`);
    const n = Math.max(1, Math.floor(dur / 1.3));
    for (let k = 0; k < n; k++) {
      const a = t0 + k * 1.3;
      tl.fromTo(`#${id}-s`, { scaleY: 0.4, svgOrigin: "0 0" }, { scaleY: 2.2, svgOrigin: "0 0", duration: 0.9, ease: "power1.in", immediateRender: false }, a);
      tl.fromTo(`#${id}-d`, { opacity: 1, y: 14 }, { opacity: 0, y: 140, duration: 0.4, ease: "power2.in", immediateRender: false }, a + 0.9);
      tl.fromTo(`#${id}-g`, { opacity: 0.2 }, { opacity: 1, duration: 0.2, yoyo: true, repeat: 1, immediateRender: false }, a + 0.3);
    }
  };
  const sparks = (cx, cy, id, n = 8, R = 70) => Array.from({ length: n }, (_, k) => { const a = (k / n) * Math.PI * 2; return `<g transform="translate(${f1(cx + Math.cos(a) * R)},${f1(cy + Math.sin(a) * R)})"><path class="${id}-sp" d="M0,-12L3,-3L12,0L3,3L0,12L-3,3L-12,0L-3,-3Z" fill="#fff6b0" opacity="0"/></g>`; }).join("");
  const sparkle = (tl, id, t) => {
    tl.fromTo(`#${id}-ring`, { scale: 0.3, opacity: 1, svgOrigin: `${document.getElementById(id + "-ring").getAttribute("cx")} ${document.getElementById(id + "-ring").getAttribute("cy")}` }, { scale: 1.6, opacity: 0, duration: 0.6, ease: "power2.out", immediateRender: false }, t);
    document.querySelectorAll(`.${id}-sp`).forEach((e, k) => tl.fromTo(e, { opacity: 0, scale: 0.2, svgOrigin: "0 0" }, { opacity: 1, scale: 1.2, svgOrigin: "0 0", duration: 0.25, yoyo: true, repeat: 1, ease: "back.out(3)", immediateRender: false }, t + 0.05 + (k % 3) * 0.05));
  };
  const okStamp = (cx, cy, r, id) => `<circle id="${id}-ring" cx="${cx}" cy="${cy}" r="${r * 1.3}" fill="url(#rbOkGlow)" opacity="0"/>${sparks(cx, cy, id, 8, r * 1.5)}
    <g id="${id}"><g id="${id}-s">${stampSvg(cx, cy, r, true)}</g></g>`;
  const badStamp = (cx, cy, r, id) => `<g id="${id}"><g id="${id}-s">${stampSvg(cx, cy, r, false)}</g></g>`;
  function stampSvg(cx, cy, r, good) {
    return `<circle cx="${cx}" cy="${cy + 8}" r="${r}" fill="${good ? "#0a4a26" : "#6a0e0a"}" stroke="#140e0a" stroke-width="4"/>
      <circle cx="${cx}" cy="${cy}" r="${r}" fill="${good ? "#2fb864" : "#e2382e"}" stroke="#fff" stroke-width="6"/>
      <path d="M${cx - r * 0.6},${cy - r * 0.2}A${r * 0.66},${r * 0.66} 0 0 1 ${cx - r * 0.12},${cy - r * 0.62}" stroke="#fff" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/>
      ${good ? `<path d="M${cx - r * 0.5},${cy}l${r * 0.34},${r * 0.38}l${r * 0.64},${r * 0.72 * -1}" stroke="#fff" stroke-width="${r * 0.24}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`
        : `<path d="M${cx - r * 0.42},${cy - r * 0.42}L${cx + r * 0.42},${cy + r * 0.42}M${cx + r * 0.42},${cy - r * 0.42}L${cx - r * 0.42},${cy + r * 0.42}" stroke="#fff" stroke-width="${r * 0.24}" stroke-linecap="round"/>`}`;
  }
  const stampIn = (tl, id, cx, cy, t) => tl.fromTo(`#${id}-s`, { scale: 2.2, opacity: 0, svgOrigin: `${cx} ${cy}` }, { scale: 1, opacity: 1, svgOrigin: `${cx} ${cy}`, duration: 0.35, ease: "back.out(2.6)", immediateRender: false }, t);
  const slab = (x, y, w, h, r, face = "url(#rbSlabF)", body = "#b8a888") => `<rect x="${x}" y="${y + 14}" width="${w}" height="${h}" rx="${r}" fill="${body}" ${OUT(5)}/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${face}" ${OUT(5)}/>
    <rect x="${x + 16}" y="${y + 8}" width="${w - 32}" height="${Math.min(60, h * 0.3)}" rx="${r * 0.7}" fill="#fff" opacity=".35"/>`;
  const head = (x, w, y, text, color) => `<rect x="${x}" y="${y}" width="${w}" height="96" rx="30" fill="${color}" ${OUT(5)}/><rect x="${x + 14}" y="${y + 8}" width="${w - 28}" height="30" rx="14" fill="#fff" opacity=".22"/>
    <text x="${x + w / 2}" y="${y + 64}" font-family="Kanit" font-weight="900" font-size="46" fill="#fff" text-anchor="middle" stroke="${INK}" stroke-width="6" paint-order="stroke">${text}</text>`;
  const cardIn = (tl, id, t0, dur, out) => {
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { scaleX: 0.6, scaleY: 1.3, y: 120, svgOrigin: "540 700" }, { scaleX: 1, scaleY: 1, y: 0, svgOrigin: "540 700", duration: 0.75, ease: "elastic.out(1, 0.5)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { rotation: -1.2, svgOrigin: "540 300" }, { rotation: 1.2, svgOrigin: "540 300", duration: 1.6, repeat: Math.ceil(dur / 1.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.75);
    if (out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };

  // ---------------- the rule board ----------------
  const RULES = RabUI.RULES, ICONS = ["pupno", "syringe"];
  RabUI.rules = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), act = o.active ?? 0, done = o.done ?? [], Y = o.y ?? 640, W = 820, H = 470;
    const rows = RULES.map((r, k) => {
      const on = k === act, d = done.includes(k), yy = -60 + k * 170;
      return `<g opacity="${on || d ? 1 : 0.32}"><g transform="translate(-370,${yy - 62})">${RabFX.coin(ICONS[k], 0, 0, 1.0, `${id}-c${k}`)}</g>
        <defs><clipPath id="${id}-cp${k}"><rect id="${id}-w${k}" x="-230" y="${yy - 60}" width="${on ? 0 : 640}" height="100"/></clipPath></defs>
        ${on ? `<path id="${id}-u${k}" d="M-236,${yy + 14}Q40,${yy + 26} 380,${yy + 8}" stroke="#ffd23a" stroke-width="26" fill="none" opacity=".35" stroke-linecap="round" stroke-dasharray="640" stroke-dashoffset="640"/>` : ""}
        <g clip-path="url(#${id}-cp${k})"><text x="-226" y="${yy}" font-family="Sriracha" font-size="44" fill="${on ? "#ffe27a" : "#f4f2ea"}" stroke="${on ? "#ffe27a" : "#f4f2ea"}" stroke-width="1.4" stroke-opacity=".5">${r}</text></g>
        ${on ? `<g id="${id}-chalk" opacity="0"><rect x="-8" y="-40" width="16" height="44" rx="5" fill="#fbfaf2" ${OUT(2.5)} transform="rotate(24)"/></g>` : ""}
        ${d ? `<g transform="translate(0,0)">${okStamp(352, yy - 16, 30, `${id}-t${k}`)}</g>` : ""}</g>`;
    }).join("");
    // chalk dust that falls off the stick as it writes
    let dust = ""; const r = mk(11);
    for (let k = 0; k < 18; k++) dust += `<circle class="${id}-du" cx="${f1(-226 + (k / 18) * 600)}" cy="${-60 + act * 170 + 6}" r="${f1(2 + r() * 3)}" fill="#f4f2ea" opacity="0"/>`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-in"><g transform="translate(540,${Y})">
      <ellipse cx="0" cy="${H / 2 + 50}" rx="${W / 2}" ry="30" fill="url(#quSoftSh)" opacity=".7"/>
      ${Rab.zinc(0, 0, 1, { id: id + "-z", w: W, h: H, rot: 0, lines: [] })}
      <text x="0" y="${-H / 2 + 70}" font-family="Kanit" font-weight="900" font-size="46" fill="#ffd23a" text-anchor="middle" stroke="${INK}" stroke-width="7" paint-order="stroke">กฎของยายบัว</text>
      ${rows}${dust}</g></g></g>`);
    cardIn(tl, id, t0, dur, o.out);
    RULES.forEach((_, k) => { pop(tl, `${id}-c${k}`, t0 + 0.25 + k * 0.14); RabFX.life(tl, document.getElementById(`${id}-c${k}`), t0 + 1.0, dur); });
    if (act >= 0) {
      const tw = t0 + (o.writeAt ?? 0.55), wd = o.writeDur ?? 1.0, yy = -60 + act * 170;
      tl.fromTo(`#${id}-w${act}`, { attr: { width: 0 } }, { attr: { width: 640 }, duration: wd, ease: "power1.inOut", immediateRender: false }, tw);
      tl.fromTo(`#${id}-chalk`, { opacity: 1, x: -226, y: yy }, { x: 400, y: yy, duration: wd, ease: "power1.inOut", immediateRender: false }, tw);
      tl.fromTo(`#${id}-chalk`, { rotation: -8, svgOrigin: "0 0" }, { rotation: 8, svgOrigin: "0 0", duration: 0.09, repeat: Math.ceil(wd / 0.09), yoyo: true, ease: "sine.inOut", immediateRender: false }, tw);
      tl.to(`#${id}-chalk`, { opacity: 0, duration: 0.2 }, tw + wd);
      document.querySelectorAll(`.${id}-du`).forEach((e, k) => tl.fromTo(e, { opacity: 0.9, y: 0 }, { opacity: 0, y: 70 + (k % 5) * 14, duration: 0.7, ease: "power1.in", immediateRender: false }, tw + (k / 18) * wd));
      tl.to(`#${id}-u${act}`, { attr: { "stroke-dashoffset": 0 }, duration: 0.45, ease: "power2.out" }, tw + wd + 0.05);
    }
    done.forEach((k, i) => { const t = t0 + (o.tickAt ?? 0.5) + i * 0.3; stampIn(tl, `${id}-t${k}`, 352, -60 + k * 170 - 16, t); sparkle(tl, `${id}-t${k}`, t + 0.15); });
  };

  // ---------------- saliva on skin ----------------
  const virus = (x, y, r = 0, s = 1, cls = "") => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${r}) scale(${s})"><g class="${cls}"><path d="M-16,-7H8Q18,-7 18,0Q18,7 8,7H-16Z" fill="#7a2a8a" ${OUT(2)}/>
    ${[-12, -6, 0, 6].map((a) => `<path d="M${a},-7v-4M${a},7v4" stroke="#7a2a8a" stroke-width="2"/>`).join("")}<path d="M-10,-2H8" stroke="#d8a0e8" stroke-width="2.4"/></g></g>`;
  const skin = (x, w, graze, id) => {
    let s = `<rect x="${x}" y="0" width="${w}" height="64" fill="#f0c4a0" ${OUT(3)}/><rect x="${x}" y="64" width="${w}" height="120" fill="#f8dccc" ${OUT(3)}/><rect x="${x}" y="184" width="${w}" height="210" fill="url(#rbMuscle)" ${OUT(3)}/>`;
    for (let k = 0; k < 6; k++) s += `<path d="M${x + 20},${226 + k * 28}H${x + w - 20}" stroke="#8a2030" stroke-width="3" opacity=".4"/>`;
    s += `<path d="M${x},2H${x + w}" stroke="#fff" stroke-width="4" opacity=".5"/>`;
    if (graze) s += `<circle id="${id}-wg" cx="${x + w / 2}" cy="60" r="90" fill="url(#rbWound)" opacity=".6"/><path d="M${x + w / 2 - 60},0L${x + w / 2 - 30},110L${x + w / 2},40L${x + w / 2 + 26},120L${x + w / 2 + 60},0Z" fill="#b8202a" ${OUT(3)}/>
      <path d="M${x + w / 2 - 40},14L${x + w / 2 - 26},70" stroke="#ff9a9a" stroke-width="3" opacity=".7"/>`;
    return s;
  };
  RabUI.saliva = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), Y = o.y ?? 520;
    const panel = (x, w, graze, k) => `<g transform="translate(0,150)">${skin(x, w, graze, id)}
      <g id="${id}-drop${k}"><path d="M${x + w / 2},-130q-36,52 -36,78a36,36 0 0 0 72,0q0,-26 -36,-78Z" fill="#cfe8ff" ${OUT(3.5)}/><path d="M${x + w / 2 - 14},-60q0,-20 10,-36" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path class="${id}-gl" d="M${x + w / 2 + 12},-74l3,-9l3,9l9,3l-9,3l-3,9l-3,-9l-9,-3Z" fill="#fff"/>
        ${virus(x + w / 2 - 6, -62, 0, 0.9, `${id}-wig`)}${virus(x + w / 2 + 10, -40, 30, 0.8, `${id}-wig`)}</g>
      ${graze ? `<g id="${id}-in" opacity="0">${virus(x + w / 2, 80, 90, 1, `${id}-wig`)}${virus(x + w / 2 - 20, 150, 80, 1, `${id}-wig`)}${virus(x + w / 2 + 16, 240, 100, 1, `${id}-wig`)}</g>
        <path id="${id}-nerve0" d="M${x + w / 2 + 20},260C${x + w / 2 + 120},250 ${x + w - 30},200 ${x + w - 10},60" stroke="#ffd23a" stroke-width="20" fill="none" opacity=".35" stroke-dasharray="420" stroke-dashoffset="420" stroke-linecap="round"/>
        <path id="${id}-nerve" d="M${x + w / 2 + 20},260C${x + w / 2 + 120},250 ${x + w - 30},200 ${x + w - 10},60" stroke="#fff3a0" stroke-width="8" fill="none" stroke-dasharray="420" stroke-dashoffset="420" stroke-linecap="round"/>
        ${badStamp(x + w - 60, 330, 44, `${id}-x`)}` : okStamp(x + w - 60, 330, 44, `${id}-ok`)}
      <text x="${x + w / 2}" y="470" font-family="Kanit" font-weight="900" font-size="38" fill="${graze ? "#c8282a" : "#1e7a48"}" text-anchor="middle">${graze ? "แผล / ถลอก → ติด" : "ผิวปกติ → ไม่ติด"}</text></g>`;
    const s = `${slab(70, -60, 940, 760, 40)}${head(110, 860, -40, 'เชื้ออยู่ใน "น้ำลาย"', "#2e6a8a")}${panel(110, 410, false, 0)}${panel(560, 410, true, 1)}`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-in"><g transform="translate(0,${Y})">${s}</g></g></g>`);
    cardIn(tl, id, t0, dur, o.out);
    [0, 1].forEach((k) => tl.fromTo(`#${id}-drop${k}`, { y: -220 }, { y: 0, duration: 0.6, ease: "bounce.out", immediateRender: false }, t0 + 0.35 + k * 0.25));
    document.querySelectorAll(`.${id}-gl`).forEach((e) => tl.fromTo(e, { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1.1, transformOrigin: "50% 50%", duration: 0.3, repeat: Math.ceil(dur / 0.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.6));
    document.querySelectorAll(`.${id}-wig`).forEach((e, k) => tl.fromTo(e, { rotation: -10, svgOrigin: "0 0" }, { rotation: 10, svgOrigin: "0 0", duration: 0.14 + (k % 3) * 0.03, repeat: Math.ceil(dur / 0.14), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    // intact skin: the drop beads off, ✓
    tl.to(`#${id}-drop0`, { x: -60, y: 30, opacity: 0.25, duration: 0.6, ease: "power2.in" }, t0 + 1.05);
    stampIn(tl, `${id}-ok`, 110 + 410 - 60, 330, t0 + 1.2); sparkle(tl, `${id}-ok`, t0 + 1.3);
    // graze: throbs, virus slips in, races up the nerve, ✗ with a shake and a red flash
    RabFX.pulse(tl, `#${id}-wg`, t0 + 0.5, dur, 0.7, 0.3);
    tl.fromTo(`#${id}-in`, { opacity: 0, y: -100 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.inOut", immediateRender: false }, t0 + 1.1);
    tl.to([`#${id}-nerve0`, `#${id}-nerve`], { attr: { "stroke-dashoffset": 0 }, duration: 0.8, ease: "power2.in" }, t0 + 1.7);
    const xt = t0 + (o.badAt ?? 2.4);
    stampIn(tl, `${id}-x`, 560 + 410 - 60, 330, xt); RabFX.shakeSel(tl, `#${id}-x`, xt + 0.3, 12); RabFX.flash(tl, xt + 0.3, "#ff2a1a", 0.28);
  };

  // ---------------- puppies 2–6 months ----------------
  RabUI.pupAge = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), Y = o.y ?? 600;
    let s = `${slab(70, -60, 940, 600, 40)}${head(110, 860, -40, 'ส่วนใหญ่ถูก "ลูกหมา" กัด', "#c8402e")}`;
    for (let m = 1; m <= 12; m++) {
      const x = 130 + (m - 1) * 70 + 4, hot = m >= 2 && m <= 6;
      s += `<g id="${id}-m${m}"><rect x="${x}" y="${420 + 12}" width="62" height="74" rx="12" fill="${hot ? "#a82a1e" : "#a89a80"}" ${OUT(3)}/>
        <rect x="${x}" y="420" width="62" height="74" rx="12" fill="url(#${hot ? "rbBlockHot" : "rbBlock"})" ${OUT(3)}/><rect x="${x + 6}" y="425" width="50" height="16" rx="6" fill="#fff" opacity=".45"/>
        <text x="${x + 31}" y="472" font-family="Kanit" font-weight="900" font-size="32" fill="${hot ? "#8a1410" : "#7a7060"}" text-anchor="middle">${m}</text></g>`;
    }
    s += `<text x="540" y="542" font-family="Kanit" font-weight="700" font-size="28" fill="#5a5048" text-anchor="middle">อายุ (เดือน)</text>
      <path id="${id}-br" d="M${130 + 70 + 4},408V380H${130 + 5 * 70 + 66}V408" stroke="#c8282a" stroke-width="9" fill="none" stroke-dasharray="560" stroke-dashoffset="560" stroke-linecap="round"/>
      <g transform="translate(${130 + 70 * 3 + 35},350)"><g id="${id}-lab"><rect x="-130" y="-46" width="260" height="70" rx="20" fill="#7a140e"/><rect x="-130" y="-54" width="260" height="70" rx="20" fill="#e2382e" ${OUT(4)}/>
        <text y="-6" font-family="Kanit" font-weight="900" font-size="40" fill="#fff" text-anchor="middle">2–6 เดือน</text></g></g>`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-in"><g transform="translate(0,${Y})">${s}<g id="${id}-pups"></g></g></g></g>`);
    const g = document.getElementById(id + "-pups");
    [[200, 0.55], [400, 0.72], [610, 0.88], [830, 1.0]].forEach(([x, k], i) => put(g, Dog.svg({ id: `${id}-p${i}`, kind: "pup", x, y: 300, s: k * 0.95, flip: i % 2 === 1 })));
    cardIn(tl, id, t0, dur, o.out);
    [0, 1, 2, 3].forEach((i) => Dog.drive(tl, `${id}-p${i}`, t0, dur, i % 2 ? "wag" : "idle"));
    for (let m = 1; m <= 12; m++) tl.fromTo(`#${id}-m${m}`, { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "back.out(2.4)", immediateRender: false }, t0 + 0.3 + m * 0.04);
    for (let m = 2; m <= 6; m++) tl.to(`#${id}-m${m}`, { y: -16, duration: 0.25, ease: "back.out(3)" }, t0 + 1.0 + (m - 2) * 0.08);
    tl.to(`#${id}-br`, { attr: { "stroke-dashoffset": 0 }, duration: 0.45, ease: "power2.out" }, t0 + 1.4);
    tl.fromTo(`#${id}-lab`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.6, ease: "elastic.out(1,0.45)", immediateRender: false }, t0 + 1.7);
    tl.fromTo(`#${id}-lab`, { rotation: -3, svgOrigin: "0 0" }, { rotation: 3, svgOrigin: "0 0", duration: 0.5, repeat: Math.ceil(dur / 0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 2.3);
  };
  window.RabFX = RabFX;
})();
