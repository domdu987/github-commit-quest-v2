// IconFX: themed 2.5D icons and cards with real motion, shared by every lane (owner 1 Nov 2569: "Icon ขยับสวยยัง เอฟเฟคต่างๆ ดียัง …
// ทำใหม่ให้ดีกว่านี้ดิ icon เอฟเฟคต่างๆทำให้เข้ากับธีมเรื่องด้วย"). Replaces SU.medal / SU.sheen / SU.fxGo for new work. See README-iconfx.md.
//
//   IconFX.enter(tl, layer, o)  → { id, hit }   an icon launches in big (r ≥ 135 = ¼ of the width), squash → stretch → overshoot → settle,
//        with a speed trail, a themed burst and a glow flash; `hit` is the impact time (put the mix's hit sound there)
//        o: { theme, art, x, y, r = 150, t, from: "below"|"left"|"right"|"above", label, idle (seconds to keep it alive after landing),
//             exit: "dock" | "fly" | "none", dockX, dockY, dockR (≥ 77 = 1/7 of the width) }
//   IconFX.idle(tl, id, t0, dur, theme)   float, 3D tilt (scaleX + skew), the highlight sliding with the tilt, a sheen every ~2 s, a glow pulse,
//        and the theme's own life (neon flicker, reflector glint, bubbles, dust, candle sway)
//   IconFX.exit(tl, id, t, o)  "dock" (shrinks to a corner and stays, r ≥ 77) or "fly" (whips off with a trail); never just vanishes
//   IconFX.card(tl, layer, o)  → { id, cues }   a themed card that flips in with depth and a shadow; items arrive one by one; "ok" items draw
//        a ✓ with a sparkle, "no" items get a ✗ that shakes with a red flash. o: { theme, title, items: [{ text, sub, mark: "ok"|"no"|null, art }],
//        x, y, w, t, dur, step }
//   IconFX.THEMES   zombie · road · roadWarn · water · military · ghost · plain  (frame, material, colours, particles, sound)
//   IconFX.cues     every hit the page scheduled: [{ t, type, gain }]: dump it (window.IconFX.cues) or rebuild it from the documented offsets
//   IconFX.HIT = 0.30 (enter → impact), IconFX.TICK = 0.22 (card item → ✓ stroke done), IconFX.CROSS = 0.18 (card item → ✗ slam)
(function () {
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f = (v) => (+v).toFixed(1);
  const INK = "#1b1714";
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  let seq = 0;
  const rnd = (s) => { let x = s * 9301 + 49297; return () => ((x = (x * 9301 + 49297) % 233280) / 233280); };

  // ---------- themes: the plate (frame + material), colours, the burst particles, the idle life, the hit sound ----------
  const plates = {
    // scratched steel plate, rivets, a red emergency rim that flickers like a dying neon
    zombie: (id, r) => { const R = r * 0.92, rr = rnd(r);
      let sc = ""; for (let k = 0; k < 9; k++) { const x = -R + rr() * 2 * R, y = -R + rr() * 2 * R, l = 14 + rr() * 40, a = rr() * 3;
        sc += `<path d="M${f(x)},${f(y)}l${f(Math.cos(a) * l)},${f(Math.sin(a) * l)}" stroke="#ffffff" stroke-width="${f(1 + rr() * 1.6)}" opacity=".35"/>`; }
      return `<rect x="${f(-R)}" y="${f(-R * 0.86 + r * 0.12)}" width="${f(2 * R)}" height="${f(2 * R * 0.86)}" rx="${f(r * 0.16)}" fill="#3a3e46" ${O(5)}/>
        <rect x="${f(-R)}" y="${f(-R * 0.86)}" width="${f(2 * R)}" height="${f(2 * R * 0.86)}" rx="${f(r * 0.16)}" fill="url(#${id}-mat)" ${O(5)}/>
        <rect id="${id}-neon" x="${f(-R + 8)}" y="${f(-R * 0.86 + 8)}" width="${f(2 * R - 16)}" height="${f(2 * R * 0.86 - 16)}" rx="${f(r * 0.12)}" fill="none" stroke="#ff3a2a" stroke-width="${f(r * 0.05)}" filter="url(#${id}-glow)"/>
        ${sc}${[[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([a, b]) => `<circle cx="${f(a * (R - r * 0.12))}" cy="${f(b * (R * 0.86 - r * 0.12))}" r="${f(r * 0.045)}" fill="#c8ccd2" ${O(2)}/>`).join("")}`; },
    // the green highway sign: rounded panel, white border, reflective sheen
    road: (id, r) => { const W = r * 1.9, H = r * 1.5;
      return `<rect x="${f(-W / 2)}" y="${f(-H / 2 + r * 0.1)}" width="${f(W)}" height="${f(H)}" rx="${f(r * 0.14)}" fill="#0a4a2a" ${O(5)}/>
        <rect x="${f(-W / 2)}" y="${f(-H / 2)}" width="${f(W)}" height="${f(H)}" rx="${f(r * 0.14)}" fill="url(#${id}-mat)" ${O(5)}/>
        <rect x="${f(-W / 2 + 10)}" y="${f(-H / 2 + 10)}" width="${f(W - 20)}" height="${f(H - 20)}" rx="${f(r * 0.1)}" fill="none" stroke="#f4f6f0" stroke-width="${f(r * 0.045)}"/>
        <path d="M${f(-r * 0.3)},${f(H / 2)}v${f(r * 0.5)}M${f(r * 0.3)},${f(H / 2)}v${f(r * 0.5)}" stroke="#8a929c" stroke-width="${f(r * 0.08)}"/>`; },
    // the yellow diamond warning sign
    roadWarn: (id, r) => { const R = r * 1.08;
      return `<path d="M0,${f(-R + r * 0.1)}L${f(R)},${f(r * 0.1)}L0,${f(R + r * 0.1)}L${f(-R)},${f(r * 0.1)}Z" fill="#8a6a00" ${O(5)}/>
        <path d="M0,${f(-R)}L${f(R)},0L0,${f(R)}L${f(-R)},0Z" fill="url(#${id}-mat)" ${O(5)}/>
        <path d="M0,${f(-R + 16)}L${f(R - 16)},0L0,${f(R - 16)}L${f(-R + 16)},0Z" fill="none" stroke="${INK}" stroke-width="${f(r * 0.05)}"/>`; },
    // a life buoy: orange/white ring around a glassy bubble
    water: (id, r) => { const R = r * 0.98;
      return `<circle cy="${f(r * 0.1)}" r="${f(R)}" fill="#a83a10" ${O(5)}/><circle r="${f(R)}" fill="#ff7a2a" ${O(5)}/>
        ${[0, 1, 2, 3].map((k) => `<path d="M0,0L${f(Math.cos(k * Math.PI / 2 + 0.4) * R)},${f(Math.sin(k * Math.PI / 2 + 0.4) * R)}A${f(R)},${f(R)} 0 0 1 ${f(Math.cos(k * Math.PI / 2 + 1.1) * R)},${f(Math.sin(k * Math.PI / 2 + 1.1) * R)}Z" fill="#fdfaf2"/>`).join("")}
        <circle r="${f(R)}" fill="none" ${O(5)}/><circle r="${f(R * 0.66)}" fill="url(#${id}-mat)" ${O(4)}/>
        <path d="M${f(-R * 0.5)},${f(-R * 0.2)}A${f(R * 0.56)},${f(R * 0.56)} 0 0 1 ${f(-R * 0.1)},${f(-R * 0.52)}" fill="none" stroke="#ffffff" stroke-width="${f(r * 0.06)}" stroke-linecap="round" opacity=".85"/>`; },
    // a dog tag on its ball chain, stamped steel
    military: (id, r) => { const W = r * 1.5, H = r * 1.86;
      return `<path d="M${f(-W * 0.2)},${f(-H / 2 - r * 0.5)}Q0,${f(-H / 2 - r * 0.9)} ${f(W * 0.2)},${f(-H / 2 - r * 0.5)}" fill="none" stroke="#9aa2ac" stroke-width="${f(r * 0.04)}" stroke-dasharray="${f(r * 0.04)} ${f(r * 0.03)}"/>
        <rect x="${f(-W / 2)}" y="${f(-H / 2 + r * 0.1)}" width="${f(W)}" height="${f(H)}" rx="${f(W * 0.36)}" fill="#4a4e3a" ${O(5)}/>
        <rect x="${f(-W / 2)}" y="${f(-H / 2)}" width="${f(W)}" height="${f(H)}" rx="${f(W * 0.36)}" fill="url(#${id}-mat)" ${O(5)}/>
        <circle cy="${f(-H / 2 + r * 0.22)}" r="${f(r * 0.09)}" fill="#2a2e22" ${O(3)}/><rect x="${f(-W / 2 + 14)}" y="${f(H / 2 - r * 0.42)}" width="${f(W - 28)}" height="${f(r * 0.2)}" rx="6" fill="#3a3f2a" opacity=".55"/>`; },
    // a yant cloth: cream cloth, red border and script, hanging from a cord
    ghost: (id, r) => { const W = r * 1.6, H = r * 1.9;
      return `<path d="M${f(-W * 0.4)},${f(-H / 2)}Q0,${f(-H / 2 - r * 0.4)} ${f(W * 0.4)},${f(-H / 2)}" fill="none" stroke="#c8302a" stroke-width="${f(r * 0.04)}"/>
        <path d="M${f(-W / 2)},${f(-H / 2 + r * 0.08)}H${f(W / 2)}V${f(H / 2 + r * 0.08)}L${f(W * 0.3)},${f(H / 2 - r * 0.04 + r * 0.08)}L${f(W * 0.1)},${f(H / 2 + r * 0.1)}L${f(-W * 0.12)},${f(H / 2 - r * 0.02 + r * 0.08)}L${f(-W / 2)},${f(H / 2 + r * 0.08)}Z" fill="#8a6a40" ${O(5)}/>
        <path d="M${f(-W / 2)},${f(-H / 2)}H${f(W / 2)}V${f(H / 2)}L${f(W * 0.3)},${f(H / 2 - r * 0.04)}L${f(W * 0.1)},${f(H / 2 + r * 0.02)}L${f(-W * 0.12)},${f(H / 2 - r * 0.02)}L${f(-W / 2)},${f(H / 2)}Z" fill="url(#${id}-mat)" ${O(5)}/>
        <rect x="${f(-W / 2 + 12)}" y="${f(-H / 2 + 12)}" width="${f(W - 24)}" height="${f(H - 34)}" fill="none" stroke="#c8302a" stroke-width="${f(r * 0.03)}" stroke-dasharray="${f(r * 0.1)} ${f(r * 0.04)}"/>
        ${[0, 1, 2].map((k) => `<path d="M${f(-W * 0.36)},${f(-H * 0.38 + k * r * 0.12)}q${f(r * 0.1)},${f(-r * 0.06)} ${f(r * 0.2)},0t${f(r * 0.2)},0t${f(r * 0.2)},0" fill="none" stroke="#c8302a" stroke-width="${f(r * 0.025)}" opacity=".7"/>`).join("")}`; },
    plain: (id, r) => `<circle cy="${f(r * 0.12)}" r="${f(r)}" fill="#8a9ab0" ${O(5)}/><circle r="${f(r)}" fill="url(#${id}-mat)" ${O(5)}/>`,
  };
  const T = {
    zombie: { plate: "zombie", mat: ["#9aa2ac", "#5a606a", "#2e3238"], glow: "#ff3a2a", flash: "#ff4a2a", spark: ["#ff6a3a", "#ffd0a0", "#c8ccd2"], burst: "debris", idle: "flicker", hit: "slam", accent: "#ff3a2a", ink: "#ffffff", text: "#ffe8e0" },
    road: { plate: "road", mat: ["#3ac07a", "#14864a", "#0a5a30"], glow: "#fff6c0", flash: "#ffffff", spark: ["#fff2a0", "#ffb030", "#ffffff"], burst: "sparks", idle: "glint", hit: "clang", accent: "#f4f6f0", ink: "#ffffff", text: "#ffffff" },
    roadWarn: { plate: "roadWarn", mat: ["#fff27a", "#f4c430", "#c89a10"], glow: "#fff6c0", flash: "#ffffff", spark: ["#fff2a0", "#ffb030", "#8a8680"], burst: "gravel", idle: "glint", hit: "clang", accent: INK, ink: INK, text: INK },
    water: { plate: "water", mat: ["#d8f4ff", "#5ab8e8", "#1a5a9a"], glow: "#8ae0ff", flash: "#c8f0ff", spark: ["#e8faff", "#8ad8ff", "#ffffff"], burst: "bubbles", idle: "bubbles", hit: "splash", accent: "#ff7a2a", ink: "#0a2a4a", text: "#ffffff" },
    military: { plate: "military", mat: ["#d8dcc8", "#9aa088", "#5a604a"], glow: "#e8e0a0", flash: "#fff6d0", spark: ["#8a6a40", "#c8a070", "#5a4a30"], burst: "dirt", idle: "dust", hit: "thud", accent: "#3a4a2a", ink: INK, text: "#f0ead0" },
    ghost: { plate: "ghost", mat: ["#fff8e0", "#f0e2b8", "#d8c08a"], glow: "#ffb84a", flash: "#ffe0a0", spark: ["#ffd27a", "#ff8a3a", "#c8c0b8"], burst: "smoke", idle: "candle", hit: "gong", accent: "#c8302a", ink: "#5a1a10", text: "#fff2d8" },
    plain: { plate: "plain", mat: ["#ffffff", "#dbe6f1", "#a7b6c8"], glow: "#ffffff", flash: "#ffffff", spark: ["#ffd84a", "#ffffff", "#8ad0ff"], burst: "sparks", idle: "none", hit: "pop", accent: "#2fa864", ink: INK, text: INK },
  };

  const defs = (id, th, r) => { const m = th.mat;
    return `<defs><radialGradient id="${id}-mat" cx=".32" cy=".26" r=".95"><stop offset="0" stop-color="${m[0]}"/><stop offset=".55" stop-color="${m[1]}"/><stop offset="1" stop-color="${m[2]}"/></radialGradient>
      <radialGradient id="${id}-gl"><stop offset="0" stop-color="${th.glow}" stop-opacity=".9"/><stop offset=".45" stop-color="${th.glow}" stop-opacity=".35"/><stop offset="1" stop-color="${th.glow}" stop-opacity="0"/></radialGradient>
      <radialGradient id="${id}-hl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffffff" stop-opacity=".75"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
      <filter id="${id}-glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="${f(r * 0.04)}" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <filter id="${id}-blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="${f(r * 0.06)}"/></filter>
      <clipPath id="${id}-cp"><circle r="${f(r * 1.05)}"/></clipPath></defs>`; };

  // the icon body: shadow, glow halo, plate, art, the sliding highlight and the sheen bar (both clipped)
  const body = (id, th, r, art, label) => `${defs(id, th, r)}
    <ellipse id="${id}-shadow" cy="${f(r * 1.32)}" rx="${f(r * 0.9)}" ry="${f(r * 0.16)}" fill="#000" opacity=".35" filter="url(#${id}-blur)"/>
    <circle id="${id}-halo" r="${f(r * 1.7)}" fill="url(#${id}-gl)" opacity=".55"/>
    <g id="${id}-tilt"><g id="${id}-pop"><g id="${id}-body">${plates[th.plate](id, r)}
      <g id="${id}-art" transform="scale(${f(r / 100)})">${art || ""}</g>
      <g clip-path="url(#${id}-cp)"><ellipse id="${id}-hl" cx="${f(-r * 0.3)}" cy="${f(-r * 0.4)}" rx="${f(r * 0.7)}" ry="${f(r * 0.45)}" fill="url(#${id}-hl)" opacity=".55"/>
        <g transform="rotate(24)"><rect id="${id}-sh" x="${f(-r * 0.16)}" y="${f(-r * 1.6)}" width="${f(r * 0.3)}" height="${f(r * 3.2)}" fill="#ffffff" opacity="0"/></g></g></g>
      ${label ? `<g transform="translate(0,${f(r * 1.25)})"><rect x="${f(-r * 1.1)}" y="${f(-r * 0.24)}" width="${f(r * 2.2)}" height="${f(r * 0.46)}" rx="${f(r * 0.14)}" fill="#14161c" ${O(4)}/><text y="${f(r * 0.1)}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${f(r * 0.28)}" fill="${th.text === INK ? "#ffffff" : th.text}">${label}</text></g>` : ""}</g></g>`;

  // particles for the burst (markup; fired by burstGo)
  const burstMk = (id, th, r, n = 14) => { const rr = rnd(r + n); let s = "";
    for (let j = 0; j < n; j++) { const c = th.spark[j % th.spark.length], k = th.burst;
      const shape = k === "bubbles" ? `<circle r="${f(r * 0.05 + rr() * r * 0.05)}" fill="none" stroke="${c}" stroke-width="3"/>`
        : k === "smoke" ? `<circle r="${f(r * 0.12 + rr() * r * 0.1)}" fill="${c}" opacity=".5"/>`
        : k === "debris" || k === "gravel" || k === "dirt" ? `<path d="M0,${f(-r * 0.05)}L${f(r * 0.06)},${f(r * 0.02)}L${f(-r * 0.02)},${f(r * 0.06)}Z" fill="${c}" ${O(1.5)}/>`
        : `<path d="M0,-${f(r * 0.09)}L${f(r * 0.02)},-${f(r * 0.02)}L${f(r * 0.09)},0L${f(r * 0.02)},${f(r * 0.02)}L0,${f(r * 0.09)}L-${f(r * 0.02)},${f(r * 0.02)}L-${f(r * 0.09)},0L-${f(r * 0.02)},-${f(r * 0.02)}Z" fill="${c}"/>`;
      s += `<g id="${id}-p${j}" opacity="0">${shape}</g>`; }
    return `<circle id="${id}-ring" r="${f(r)}" fill="none" stroke="${th.glow}" stroke-width="${f(r * 0.08)}" opacity="0"/>${s}`; };
  const burstGo = (tl, id, th, r, t, n = 14) => {
    tl.fromTo(`#${id}-ring`, { attr: { r: r * 0.6 }, opacity: 0.95 }, { attr: { r: r * 2.1 }, opacity: 0, duration: 0.5, ease: "power2.out", immediateRender: false }, t);
    for (let j = 0; j < n; j++) { const a = (j / n) * Math.PI * 2 + (j % 3) * 0.3, d = r * (1.4 + (j % 4) * 0.28), up = th.burst === "bubbles" || th.burst === "smoke";
      const tx = Math.cos(a) * d * (up ? 0.5 : 1), ty = up ? -r * (1.2 + (j % 5) * 0.3) : Math.sin(a) * d + (th.burst === "gravel" || th.burst === "dirt" || th.burst === "debris" ? r * 0.6 : 0);
      tl.fromTo(`#${id}-p${j}`, { x: 0, y: 0, scale: 0.4, rotation: 0, opacity: 1 }, { x: tx, y: ty, scale: up ? 1.6 : 1.1, rotation: 200 + j * 20, opacity: 0, duration: 0.6 + (j % 4) * 0.12, ease: up ? "power1.out" : "power3.out", immediateRender: false }, t); } };

  const cues = [];
  const cue = (t, type, gain) => cues.push({ t: +t.toFixed(3), type, gain });

  const IconFX = (window.IconFX = { THEMES: T, cues, HIT: 0.3, TICK: 0.22, CROSS: 0.18 });

  // ---------- enter ----------
  IconFX.enter = (tl, layer, o = {}) => {
    const th = T[o.theme] || T.plain, r = Math.max(135, o.r ?? 150), id = o.id || `ifx${seq++}`, x = o.x ?? 540, y = o.y ?? 760, t0 = o.t ?? 0;
    const from = o.from || "below", dx = from === "left" ? -900 : from === "right" ? 900 : 0, dy = from === "below" ? 1100 : from === "above" ? -1100 : 0;
    put(layer, `<g transform="translate(${x},${y})"><g id="${id}" opacity="0"><g id="${id}-fly">
      ${[3, 2, 1].map((k) => `<g id="${id}-tr${k}" opacity="0"><use href="#${id}-body" opacity="${f(0.16 * (4 - k))}"/></g>`).join("")}
      ${body(id, th, r, o.art, o.label)}</g><g id="${id}-fx">${burstMk(id, th, r)}</g>
      <circle id="${id}-flash" r="${f(r * 2.4)}" fill="url(#${id}-gl)" opacity="0"/></g></g>`);
    const hit = t0 + IconFX.HIT;
    tl.set(`#${id}`, { opacity: 1 }, t0);
    // anticipation: a squash at the start of the path, then the launch (stretched along the motion), the impact overshoot, settle
    tl.fromTo(`#${id}-fly`, { x: dx, y: dy }, { x: 0, y: 0, duration: IconFX.HIT, ease: "power3.in", immediateRender: false }, t0);
    tl.fromTo(`#${id}-pop`, { scaleX: dy ? 0.7 : 1.35, scaleY: dy ? 1.35 : 0.7, svgOrigin: "0 0" }, { scaleX: 1, scaleY: 1, svgOrigin: "0 0", duration: IconFX.HIT, ease: "power2.in", immediateRender: false }, t0);
    tl.fromTo(`#${id}-pop`, { scaleX: dy ? 1.3 : 0.75, scaleY: dy ? 0.75 : 1.3, svgOrigin: "0 0" }, { scaleX: 1, scaleY: 1, svgOrigin: "0 0", duration: 0.55, ease: "elastic.out(1.2,0.35)", immediateRender: false }, hit);
    tl.fromTo(`#${id}-tilt`, { rotation: dx ? (dx < 0 ? -18 : 18) : -10, svgOrigin: "0 0" }, { rotation: 0, svgOrigin: "0 0", duration: 0.7, ease: "elastic.out(1,0.4)", immediateRender: false }, hit);
    // the speed trail: three ghosts lagging along the path, gone at the impact
    [1, 2, 3].forEach((k) => { tl.fromTo(`#${id}-tr${k}`, { x: dx * (0.12 * k), y: dy * (0.12 * k), opacity: 1 }, { x: dx * 0.06 * k * 0.2, y: dy * 0.06 * k * 0.2, opacity: 1, duration: IconFX.HIT, ease: "power3.in", immediateRender: false }, t0);
      tl.to(`#${id}-tr${k}`, { opacity: 0, duration: 0.08 }, hit); });
    // impact: the glow flash, the burst, a halo swell, the shadow lands
    tl.fromTo(`#${id}-flash`, { opacity: 0.95, scale: 0.4, svgOrigin: "0 0" }, { opacity: 0, scale: 1.3, svgOrigin: "0 0", duration: 0.45, ease: "power2.out", immediateRender: false }, hit);
    tl.fromTo(`#${id}-halo`, { scale: 1.5, opacity: 1, svgOrigin: "0 0" }, { scale: 1, opacity: 0.55, svgOrigin: "0 0", duration: 0.5, ease: "power2.out", immediateRender: false }, hit);
    tl.fromTo(`#${id}-shadow`, { scaleX: 0.3, opacity: 0, svgOrigin: `0 ${r * 1.32}` }, { scaleX: 1, opacity: 0.35, svgOrigin: `0 ${r * 1.32}`, duration: 0.3, ease: "power2.out", immediateRender: false }, hit);
    burstGo(tl, id, th, r, hit);
    cue(t0 + 0.02, "whoosh", 0.3); cue(hit, th.hit, 0.55); cue(hit + 0.02, "sting", 0.18);
    const idleDur = o.idle ?? 1.6;
    if (idleDur > 0) IconFX.idle(tl, id, hit + 0.45, idleDur, o.theme, r);
    const ex = o.exit || "dock";
    if (ex !== "none") IconFX.exit(tl, id, hit + 0.45 + idleDur, { mode: ex, x, y, r, dockX: o.dockX, dockY: o.dockY, dockR: o.dockR, theme: o.theme });
    return { id, hit, r };
  };

  // ---------- idle: clearly alive on a phone ----------
  IconFX.idle = (tl, id, t0, dur, theme, r = 150) => {
    const th = T[theme] || T.plain, n = Math.max(1, Math.ceil(dur / 1.2));
    tl.to(`#${id}-fly`, { y: -r * 0.12, duration: 0.6, yoyo: true, repeat: n * 2 - 1, ease: "sine.inOut" }, t0);
    // pseudo-3D turn: squeeze X and skew Y one way then the other; the highlight slides against the turn
    tl.fromTo(`#${id}-tilt`, { scaleX: 1, skewY: 0, svgOrigin: "0 0" }, { scaleX: 0.84, skewY: 7, svgOrigin: "0 0", duration: 0.6, yoyo: true, repeat: n * 2 - 1, ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-hl`, { x: 0 }, { x: r * 0.7, duration: 0.6, yoyo: true, repeat: n * 2 - 1, ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-shadow`, { scaleX: 1, svgOrigin: `0 ${r * 1.32}` }, { scaleX: 0.82, svgOrigin: `0 ${r * 1.32}`, duration: 0.6, yoyo: true, repeat: n * 2 - 1, ease: "sine.inOut", immediateRender: false }, t0);
    for (let k = 0; k * 2.0 < dur; k++) tl.fromTo(`#${id}-sh`, { x: -r * 1.8, opacity: 0.75 }, { x: r * 1.8, opacity: 0.75, duration: 0.5, ease: "power1.inOut", immediateRender: false }, t0 + 0.2 + k * 2.0);
    tl.fromTo(`#${id}-halo`, { opacity: 0.35, scale: 0.92, svgOrigin: "0 0" }, { opacity: 0.8, scale: 1.08, svgOrigin: "0 0", duration: 0.5, yoyo: true, repeat: Math.ceil(dur / 0.5), ease: "sine.inOut", immediateRender: false }, t0);
    // the theme's life
    if (th.idle === "flicker" && document.getElementById(`${id}-neon`)) for (let k = 0; k * 0.9 < dur; k++) tl.fromTo(`#${id}-neon`, { opacity: 1 }, { opacity: 0.15, duration: 0.05, yoyo: true, repeat: 3, ease: "none", immediateRender: false }, t0 + 0.3 + k * 0.9 + (k % 2) * 0.17);
    if (th.idle === "glint") for (let k = 0; k * 1.0 < dur; k++) tl.fromTo(`#${id}-halo`, { opacity: 1 }, { opacity: 0.4, duration: 0.12, ease: "power2.out", immediateRender: false }, t0 + 0.5 + k * 1.0);
    if (th.idle === "candle") tl.fromTo(`#${id}-tilt`, { rotation: -3, svgOrigin: `0 ${-r}` }, { rotation: 3, svgOrigin: `0 ${-r}`, duration: 0.9, yoyo: true, repeat: Math.ceil(dur / 0.9), ease: "sine.inOut", immediateRender: false }, t0);
    if (th.idle === "bubbles" || th.idle === "dust") for (let k = 0; k * 0.8 < dur; k++) { const j = k % 14;
      tl.fromTo(`#${id}-p${j}`, { x: (j % 2 ? 1 : -1) * r * (0.3 + (j % 3) * 0.2), y: th.idle === "bubbles" ? r * 0.6 : r * 0.9, opacity: 0.9, scale: 0.6 }, { y: th.idle === "bubbles" ? -r * 1.4 : r * 0.5, x: (j % 2 ? 1 : -1) * r * (0.5 + (j % 3) * 0.2), opacity: 0, scale: 1.2, duration: 1.1, ease: "sine.out", immediateRender: false }, t0 + k * 0.8); }
  };

  // ---------- exit: dock to a corner (stays, r ≥ 77) or fly off with a trail ----------
  IconFX.exit = (tl, id, t, o = {}) => {
    const r = o.r ?? 150;
    if (o.mode === "fly") { [1, 2, 3].forEach((k) => tl.fromTo(`#${id}-tr${k}`, { opacity: 0.9, x: 0, y: 0 }, { opacity: 0, x: -260 * k, y: 120 * k, duration: 0.35, ease: "power2.in", immediateRender: false }, t));
      tl.to(`#${id}-fly`, { x: 1100, y: -500, duration: 0.35, ease: "back.in(2)" }, t); tl.to(`#${id}-pop`, { scaleX: 1.4, scaleY: 0.7, svgOrigin: "0 0", duration: 0.35, ease: "power2.in" }, t);
      tl.set(`#${id}`, { opacity: 0 }, t + 0.36); cue(t, "whoosh", 0.26); return; }
    const dr = Math.max(77, o.dockR ?? 80), s = dr / r, dX = (o.dockX ?? 930) - (o.x ?? 540), dY = (o.dockY ?? 300) - (o.y ?? 760);
    tl.to(`#${id}-fly`, { x: dX / s, y: dY / s, duration: 0.45, ease: "power3.inOut" }, t);
    tl.to(`#${id}`, { scale: s, svgOrigin: "0 0", duration: 0.45, ease: "power3.inOut" }, t);
    tl.to(`#${id}-tilt`, { rotation: 360, svgOrigin: "0 0", duration: 0.45, ease: "power2.inOut" }, t);
    cue(t, "whoosh", 0.2); cue(t + 0.45, "pop", 0.2);
    // docked: keep it alive at a slower pace
    IconFX.idle(tl, id, t + 0.5, o.dockFor ?? 2.4, o.theme, r);
  };

  // ---------- cards ----------
  const cardFrame = (th, w, h, title) => { const m = th.mat;
    if (th.plate === "zombie") return `<rect x="${-w / 2}" y="16" width="${w}" height="${h}" rx="22" fill="#1a1c22"/><rect x="${-w / 2}" y="0" width="${w}" height="${h}" rx="22" fill="#2a2e36" ${O(6)}/>
      <rect x="${-w / 2 + 10}" y="10" width="${w - 20}" height="${h - 20}" rx="16" fill="none" stroke="#ff3a2a" stroke-width="6" opacity=".8"/><rect x="${-w / 2}" y="0" width="${w}" height="110" rx="22" fill="#8a1a14" ${O(6)}/>
      <path d="M${-w / 2},104H${w / 2}" stroke="#ffd84a" stroke-width="10" stroke-dasharray="26 18"/><text x="${-w / 2 + 40}" y="74" font-family="Kanit" font-weight="900" font-size="50" fill="#fff">${title}</text>`;
    if (th.plate === "road" || th.plate === "roadWarn") return `<rect x="${-w / 2}" y="16" width="${w}" height="${h}" rx="22" fill="#0a3a20"/><rect x="${-w / 2}" y="0" width="${w}" height="${h}" rx="22" fill="#14864a" ${O(6)}/>
      <rect x="${-w / 2 + 12}" y="12" width="${w - 24}" height="${h - 24}" rx="16" fill="none" stroke="#fff" stroke-width="7"/><text x="${-w / 2 + 44}" y="84" font-family="Kanit" font-weight="900" font-size="52" fill="#fff">${title}</text>`;
    if (th.plate === "ghost") return `<rect x="${-w / 2}" y="16" width="${w}" height="${h}" fill="#8a6a40"/><rect x="${-w / 2}" y="0" width="${w}" height="${h}" fill="${m[1]}" ${O(6)}/>
      <rect x="${-w / 2 + 14}" y="14" width="${w - 28}" height="${h - 28}" fill="none" stroke="#c8302a" stroke-width="6" stroke-dasharray="20 8"/><text x="${-w / 2 + 44}" y="84" font-family="Kanit" font-weight="900" font-size="52" fill="#8a1a14">${title}</text>`;
    return `<rect x="${-w / 2}" y="16" width="${w}" height="${h}" rx="26" fill="${m[2]}"/><rect x="${-w / 2}" y="0" width="${w}" height="${h}" rx="26" fill="${m[0]}" ${O(6)}/>
      <rect x="${-w / 2}" y="0" width="${w}" height="110" rx="26" fill="${m[1]}" ${O(6)}/><text x="${-w / 2 + 40}" y="76" font-family="Kanit" font-weight="900" font-size="50" fill="${th.text === INK ? "#fff" : th.text}">${title}</text>`; };
  IconFX.card = (tl, layer, o = {}) => {
    const th = T[o.theme] || T.plain, id = o.id || `ifc${seq++}`, w = o.w ?? 900, items = o.items || [], step = o.step ?? 0.45, rowH = 190;
    const h = 150 + items.length * rowH, x = o.x ?? 540, y = o.y ?? 420, t0 = o.t ?? 0, dur = o.dur ?? 3, tx = th.plate === "zombie" ? "#ffffff" : th.plate === "ghost" ? "#3a1a10" : th.plate === "road" || th.plate === "roadWarn" ? "#ffffff" : INK;
    let g = `<g transform="translate(${x},${y})"><g id="${id}" opacity="0"><ellipse id="${id}-sh" cy="${h + 40}" rx="${w * 0.45}" ry="30" fill="#000" opacity=".35"/><g id="${id}-flip">${cardFrame(th, w, h, o.title || "")}`;
    items.forEach((it, k) => { const iy = 170 + k * rowH + rowH / 2 - 30;
      g += `<g id="${id}-i${k}" opacity="0"><g transform="translate(${-w / 2 + 110},${iy})"><g id="${id}-ic${k}">${it.art ? body(`${id}-m${k}`, th, 70, it.art) : ""}</g></g>
        <text x="${-w / 2 + 210}" y="${iy - 4}" font-family="Kanit" font-weight="900" font-size="58" fill="${tx}">${it.text}</text>
        ${it.sub ? `<text x="${-w / 2 + 210}" y="${iy + 54}" font-family="Kanit" font-weight="800" font-size="44" fill="${th.accent === INK ? "#c8302a" : th.accent}">${it.sub}</text>` : ""}
        ${it.mark === "ok" ? `<g transform="translate(${w / 2 - 90},${iy})"><circle id="${id}-ok${k}" r="52" fill="#2fa864" ${O(5)}/><path id="${id}-ck${k}" d="M-24,0l16,18l32,-36" stroke="#fff" stroke-width="13" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/><g id="${id}-cx${k}">${burstMk(`${id}-cs${k}`, T.plain, 60, 10)}</g></g>` : ""}
        ${it.mark === "no" ? `<g transform="translate(${w / 2 - 90},${iy})"><g id="${id}-no${k}"><circle r="52" fill="#e8382c" ${O(5)}/><path d="M-22,-22L22,22M22,-22L-22,22" stroke="#fff" stroke-width="13" stroke-linecap="round"/></g></g>` : ""}</g>`; });
    g += `</g></g></g>`;
    put(layer, g);
    const out = [];
    tl.set(`#${id}`, { opacity: 1 }, t0);
    // the flip: in from edge-on (scaleX 0 + skew) with a swinging shadow, overshoot, settle
    tl.fromTo(`#${id}-flip`, { scaleX: 0.02, skewY: -14, y: -80, svgOrigin: `0 ${h / 2}` }, { scaleX: 1, skewY: 0, y: 0, svgOrigin: `0 ${h / 2}`, duration: 0.55, ease: "back.out(1.6)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sh`, { scaleX: 0.1, svgOrigin: `0 ${h + 40}` }, { scaleX: 1, svgOrigin: `0 ${h + 40}`, duration: 0.55, ease: "back.out(1.6)", immediateRender: false }, t0);
    tl.to(`#${id}-flip`, { skewY: 1.5, scaleX: 0.985, svgOrigin: `0 ${h / 2}`, duration: 0.8, yoyo: true, repeat: Math.ceil(dur / 0.8), ease: "sine.inOut" }, t0 + 0.6);
    cue(t0, "whoosh", 0.28);
    items.forEach((it, k) => { const ti = t0 + 0.45 + k * step;
      tl.fromTo(`#${id}-i${k}`, { opacity: 0, x: 120 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, ti);
      if (it.art) { tl.fromTo(`#${id}-ic${k}`, { scale: 0.2, rotation: -50, svgOrigin: "0 0" }, { scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.45, ease: "back.out(3)", immediateRender: false }, ti + 0.05);
        for (let s = 0; s * 2 < dur; s++) tl.fromTo(`#${id}-m${k}-sh`, { x: -130, opacity: 0.7 }, { x: 130, opacity: 0.7, duration: 0.45, immediateRender: false }, ti + 0.6 + s * 2); }
      cue(ti, "click", 0.22);
      if (it.mark === "ok") { const tk = ti + IconFX.TICK;
        tl.fromTo(`#${id}-ok${k}`, { scale: 0.1, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.3, ease: "back.out(3)", immediateRender: false }, ti + 0.05);
        tl.fromTo(`#${id}-ck${k}`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.18, ease: "power2.out", immediateRender: false }, tk - 0.18);
        burstGo(tl, `${id}-cs${k}`, T.plain, 60, tk, 10); cue(tk, "ding", 0.3); out.push({ t: tk, type: "ding" }); }
      if (it.mark === "no") { const tc = ti + IconFX.CROSS;
        tl.fromTo(`#${id}-no${k}`, { scale: 2.2, opacity: 0, svgOrigin: "0 0" }, { scale: 1, opacity: 1, svgOrigin: "0 0", duration: 0.16, ease: "power4.in", immediateRender: false }, ti + 0.02);
        tl.fromTo(`#${id}-no${k}`, { x: -16 }, { x: 0, duration: 0.4, ease: "elastic.out(1.2,0.25)", immediateRender: false }, tc);
        put(layer, `<rect id="${id}-rf${k}" width="1080" height="1920" fill="#ff2a1a" opacity="0"/>`);
        tl.fromTo(`#${id}-rf${k}`, { opacity: 0.35 }, { opacity: 0, duration: 0.35, ease: "power2.out", immediateRender: false }, tc);
        cue(tc, "buzz", 0.3); cue(tc, "thud", 0.3); out.push({ t: tc, type: "buzz" }); } });
    if (o.out !== false) { tl.to(`#${id}-flip`, { scaleX: 0.02, skewY: 14, svgOrigin: `0 ${h / 2}`, duration: 0.3, ease: "power2.in" }, t0 + dur - 0.3); tl.set(`#${id}`, { opacity: 0 }, t0 + dur); cue(t0 + dur - 0.3, "whoosh", 0.18); }
    return { id, cues: out };
  };

  // ---------- stock art (drawn in a ±100 box) so lanes can start fast ----------
  IconFX.ART = {
    bell: `<circle r="62" fill="#f4c430" ${O(5)}/><circle r="42" fill="#fff6c8" ${O(4)}/><path d="M-20,14Q-20,-24 0,-24Q20,-24 20,14L26,20H-26Z" fill="${INK}"/><circle cy="28" r="7" fill="${INK}"/>`,
    noTrack: `<g><rect x="-70" y="10" width="140" height="16" rx="6" fill="#c8ccd2" ${O(4)}/><rect x="-70" y="40" width="140" height="16" rx="6" fill="#c8ccd2" ${O(4)}/>${[-50, -10, 30].map((x) => `<rect x="${x}" y="0" width="24" height="64" fill="#7a5a3a" ${O(3)}/>`).join("")}
      <path d="M-30,-70L-62,-6H-34L-44,30L4,-34H-22Z" fill="#ffd84a" ${O(4)}/></g><circle r="84" fill="none" stroke="#e8382c" stroke-width="16"/><path d="M-60,-60L60,60" stroke="#e8382c" stroke-width="16" stroke-linecap="round"/>`,
    stopwatch: (s) => `<circle cy="10" r="66" fill="#fdfaf2" ${O(5)}/><rect x="-12" y="-78" width="24" height="18" rx="5" fill="${INK}"/><path d="M0,10V-36" stroke="#e8382c" stroke-width="9" stroke-linecap="round"/><circle cy="10" r="8" fill="${INK}"/><text y="64" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="${INK}">${s}</text>`,
    gangway: `<rect x="-50" y="-70" width="100" height="140" rx="10" fill="#c8ced4" ${O(4)}/><rect x="-32" y="-52" width="64" height="66" rx="8" fill="#1a2030" ${O(3)}/><rect x="-74" y="26" width="148" height="38" rx="8" fill="#c8642c" ${O(4)}/><rect x="-62" y="-4" width="50" height="32" rx="5" fill="#2f6fd0" ${O(3)}/>`,
    log: `<rect x="-80" y="-24" width="160" height="56" rx="26" fill="#8a5a30" ${O(5)}/><ellipse cx="80" cy="4" rx="16" ry="28" fill="#d8a870" ${O(4)}/><path d="M76,-6a6,6 0 1 0 8,10" stroke="#8a5a30" stroke-width="3" fill="none"/><path d="M-60,-10h70M-40,14h80" stroke="#6a4020" stroke-width="4"/>`,
    buoy: `<circle r="30" fill="#ff7a2a" ${O(4)}/><circle r="14" fill="#5ab8e8" ${O(3)}/>`,
    candle: `<rect x="-18" y="-10" width="36" height="80" rx="6" fill="#fff4d8" ${O(4)}/><path d="M0,-10C-16,-34 -6,-60 0,-74C6,-60 16,-34 0,-10Z" fill="#ffb030" ${O(3)}/><path d="M0,-18C-6,-30 -2,-44 0,-52C2,-44 6,-30 0,-18Z" fill="#fff2a0"/>`,
    helmet: `<path d="M-74,20Q-74,-62 0,-62Q74,-62 74,20Z" fill="#4a5a32" ${O(5)}/><path d="M-90,20H90" stroke="${INK}" stroke-width="10" stroke-linecap="round"/><path d="M-40,-30q40,-24 80,0" stroke="#6a7a4a" stroke-width="6" fill="none"/>`,
  };
})();
