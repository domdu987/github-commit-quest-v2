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
    // the road itself, readable in half a second: an asphalt tile with a road running away in perspective (yellow edge lines, a white
    // dashed centre line converging, reflective studs that glint, gravel shoulders), on a dusk-sky backing
    road: (id, r) => { const R = r * 0.95, rr = rnd(r * 3); let agg = "";
      for (let k = 0; k < 40; k++) agg += `<circle cx="${f(-R + rr() * 2 * R)}" cy="${f(-R * 0.2 + rr() * R * 1.15)}" r="${f(1 + rr() * 2.4)}" fill="${rr() < 0.5 ? "#6a6e76" : "#1e2026"}" opacity=".7"/>`;
      const top = -R * 0.18, bot = R * 0.95, wT = r * 0.16, wB = R * 0.98, road = `M${f(-wT)},${f(top)}L${f(wT)},${f(top)}L${f(wB)},${f(bot)}L${f(-wB)},${f(bot)}Z`;
      const dash = [0, 1, 2, 3].map((k) => { const a = k / 4, b = a + 0.12, y1 = top + (bot - top) * a * a, y2 = top + (bot - top) * b * b, w1 = 2 + 10 * a, w2 = 2 + 10 * b;
        return `<path d="M${f(-w1)},${f(y1)}L${f(w1)},${f(y1)}L${f(w2)},${f(y2)}L${f(-w2)},${f(y2)}Z" fill="#f4f4ee"/>`; }).join("");
      const studs = [0.3, 0.55, 0.8].map((a, k) => { const y = top + (bot - top) * a, x = wT + (wB - wT) * a - 10 - a * 12;
        return `<circle id="${id}-stud${k}" cx="${f(x)}" cy="${f(y)}" r="${f(3 + a * 5)}" fill="#ff5a3a" ${O(1.5)}/><circle id="${id}-studL${k}" cx="${f(-x)}" cy="${f(y)}" r="${f(3 + a * 5)}" fill="#fff6c0" ${O(1.5)}/>`; }).join("");
      return `<rect x="${f(-R)}" y="${f(-R + r * 0.12)}" width="${f(2 * R)}" height="${f(2 * R)}" rx="${f(r * 0.22)}" fill="#14161c" ${O(5)}/>
        <rect x="${f(-R)}" y="${f(-R)}" width="${f(2 * R)}" height="${f(2 * R)}" rx="${f(r * 0.22)}" fill="url(#${id}-mat)" ${O(5)}/>
        <clipPath id="${id}-rc"><rect x="${f(-R + 4)}" y="${f(-R + 4)}" width="${f(2 * R - 8)}" height="${f(2 * R - 8)}" rx="${f(r * 0.2)}"/></clipPath>
        <g clip-path="url(#${id}-rc)"><rect x="${f(-R)}" y="${f(-R)}" width="${f(2 * R)}" height="${f(R * 0.82)}" fill="#f08a4a" opacity=".55"/><rect x="${f(-R)}" y="${f(top - 6)}" width="${f(2 * R)}" height="${f(R * 1.3)}" fill="#8a7a5a"/>
          <path d="${road}" fill="#3a3e46"/>${agg}<path d="M${f(-wT + 3)},${f(top)}L${f(-wB + 18)},${f(bot)}M${f(wT - 3)},${f(top)}L${f(wB - 18)},${f(bot)}" stroke="#f4c430" stroke-width="${f(r * 0.05)}"/>${dash}${studs}</g>
        <rect x="${f(-R)}" y="${f(-R)}" width="${f(2 * R)}" height="${f(2 * R)}" rx="${f(r * 0.22)}" fill="none" ${O(5)}/>`; },
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
    road: { plate: "road", mat: ["#5a6070", "#2a2e38", "#14161c"], glow: "#fff6c0", flash: "#ffffff", spark: ["#fff2a0", "#ffb030", "#ffffff"], burst: "sparks", idle: "glint", hit: "clang", accent: "#f4f6f0", ink: "#ffffff", text: "#ffffff" },
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
    if (th.idle === "glint") { for (let k = 0; k * 1.0 < dur; k++) tl.fromTo(`#${id}-halo`, { opacity: 1 }, { opacity: 0.4, duration: 0.12, ease: "power2.out", immediateRender: false }, t0 + 0.5 + k * 1.0);
      for (let j = 0; j < 3; j++) if (document.getElementById(`${id}-stud${j}`)) for (let k = 0; k * 0.9 < dur; k++) { tl.fromTo([`#${id}-stud${j}`, `#${id}-studL${j}`], { scale: 1.8, transformOrigin: "50% 50%", opacity: 1 }, { scale: 1, transformOrigin: "50% 50%", duration: 0.3, ease: "power2.out", immediateRender: false }, t0 + k * 0.9 + j * 0.12); } }
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

  // ---------- boards: rule cards as REAL OBJECTS from the story's world (owner 1 Nov: "ภาพ 1 ให้เข้าตามธีมเรื่องดิ", reference: ทะเลลด's
  // driftwood board). IconFX.board(tl, layer, { skin, title, sub, items: [{ text, art }], active, done, at: [s per row], t, dur, y, out })
  //   text may mark words with <u>…</u> (drawn in the skin's accent colour). The active row is highlighted with the material's own tool;
  //   done rows get a tick in that tool. Skins: clipboard (zombie/skytrain) · chalk (school) · tailgate (road) · canal (water) ·
  //   fieldbook (military) · yant (ghost). Every skin: a seeded material texture, a font that fits the material, 2–3 props that move,
  //   an entrance that follows the object's physics, and life for the whole time it is on screen. Returns { id, cues }.
  const plain = (s) => s.replace(/<\/?u>/g, "");
  const marked = (s, c) => s.replace(/<u>(.*?)<\/u>/g, `<tspan fill="${c}">$1</tspan>`);
  const SK = {
    clipboard: { font: "Sriracha", size: 66, ink: "#1d3a8a", acc: "#d8312a", later: "#8a90a0", tool: "marker", enter: "thrust", sound: "thud", hiSound: "rustle", titleFont: "Sriracha", titleC: "#1d3a8a" },
    chalk: { font: "Mali", size: 64, ink: "#f4f2e8", acc: "#ffd84a", later: "#7a8a7e", tool: "chalk", enter: "hang", sound: "creak", hiSound: "rustle", titleFont: "Mali", titleC: "#ffffff" },
    tailgate: { font: "Kanit", size: 60, ink: "#fffaf0", acc: "#ffd84a", later: "#f0b8a8", tool: "spray", enter: "drop", sound: "clang", hiSound: "hiss", titleFont: "Kanit", titleC: "#fffaf0" },
    canal: { font: "Kanit", size: 60, ink: "#14161c", acc: "#c8201a", later: "#8a8478", tool: "brush", enter: "swing", sound: "creak", hiSound: "rustle", titleFont: "Kanit", titleC: "#c8201a" },
    fieldbook: { font: "Sriracha", size: 62, ink: "#2a2a24", acc: "#b8201a", later: "#8a866e", tool: "grease", enter: "slap", sound: "thud", hiSound: "rustle", titleFont: "Kanit", titleC: "#2a3018" },
    seatcard: { font: "Kanit", size: 60, ink: "#14204a", acc: "#d8312a", later: "#8a90a0", tool: "pen", enter: "pocket", sound: "rustle", hiSound: "rustle", titleFont: "Kanit", titleC: "#ffffff" },
    yant: { font: "Sriracha", size: 62, ink: "#5a1208", acc: "#c8201a", later: "#a89878", tool: "gold", enter: "unfurl", sound: "whoosh", hiSound: "ching", titleFont: "Sriracha", titleC: "#a8180c" },
  };
  // seeded material textures inside (x, y, w, h)
  const tex = {
    brushed: (x, y, w, h, seed) => { const r = rnd(seed); let s = ""; for (let k = 0; k < 60; k++) { const yy = y + r() * h; s += `<path d="M${f(x)},${f(yy)}H${f(x + w)}" stroke="${r() < 0.5 ? "#ffffff" : "#5a606a"}" stroke-width="${f(0.6 + r() * 1.4)}" opacity="${f(0.08 + r() * 0.14)}"/>`; } return s; },
    paper: (x, y, w, h, seed) => { const r = rnd(seed); let s = ""; for (let k = 0; k < 14; k++) s += `<ellipse cx="${f(x + r() * w)}" cy="${f(y + r() * h)}" rx="${f(20 + r() * 60)}" ry="${f(8 + r() * 22)}" fill="#c8b890" opacity="${f(0.04 + r() * 0.06)}"/>`; return s; },
    prints: (x, y, n, seed) => { const r = rnd(seed); let s = ""; for (let k = 0; k < n; k++) { const cx = x + r() * 120, cy = y + r() * 90, a = r() * 60 - 30;
      s += `<g transform="translate(${f(cx)},${f(cy)}) rotate(${f(a)})"><ellipse rx="22" ry="28" fill="#3a3028" opacity=".16"/>${[8, 13, 18, 23].map((q) => `<ellipse rx="${q * 0.8}" ry="${q}" fill="none" stroke="#2a2018" stroke-width="1.4" opacity=".14"/>`).join("")}</g>`; } return s; },
    slate: (x, y, w, h, seed) => { const r = rnd(seed); let s = ""; for (let k = 0; k < 10; k++) { const cx = x + r() * w, cy = y + r() * h; s += `<path d="M${f(cx - 80)},${f(cy)}q40,${f(-20 + r() * 40)} 80,0t80,0" stroke="#e8f0e8" stroke-width="${f(18 + r() * 26)}" fill="none" opacity="${f(0.04 + r() * 0.05)}" stroke-linecap="round"/>`; } return s; },
    rust: (x, y, w, h, seed) => { const r = rnd(seed); let s = ""; for (let k = 0; k < 16; k++) { const cx = x + (r() < 0.6 ? (r() < 0.5 ? r() * 90 : w - r() * 90) : r() * w), cy = y + (r() < 0.5 ? r() * 70 : h - r() * 70);
      s += `<ellipse cx="${f(cx)}" cy="${f(cy)}" rx="${f(10 + r() * 34)}" ry="${f(6 + r() * 20)}" fill="${r() < 0.5 ? "#a8521a" : "#7a3410"}" opacity="${f(0.35 + r() * 0.4)}"/>`; }
      for (let k = 0; k < 6; k++) { const cx = x + 40 + r() * (w - 80); s += `<path d="M${f(cx)},${f(y + h - 60)}q${f(-4 + r() * 8)},30 0,${f(40 + r() * 50)}" stroke="#8a3e14" stroke-width="${f(3 + r() * 4)}" opacity=".45" fill="none"/>`; } return s; },
    mud: (x, y, w, h, seed) => { const r = rnd(seed); let s = ""; for (let k = 0; k < 40; k++) { const cx = x + r() * w, cy = y + h - r() * h * 0.45; s += `<circle cx="${f(cx)}" cy="${f(cy)}" r="${f(2 + r() * 9)}" fill="#5a4630" opacity="${f(0.25 + r() * 0.4)}"/>`; }
      s += `<path d="M${x},${y + h}Q${x + w * 0.3},${y + h - 70} ${x + w * 0.55},${y + h - 30}T${x + w},${y + h - 50}V${y + h}Z" fill="#5a4630" opacity=".45"/>`; return s; },
    canvas: (x, y, w, h, seed) => { let s = ""; for (let k = 0; k < w; k += 9) s += `<path d="M${x + k},${y}V${y + h}" stroke="#2a3018" stroke-width="1" opacity=".12"/>`; for (let k = 0; k < h; k += 9) s += `<path d="M${x},${y + k}H${x + w}" stroke="#2a3018" stroke-width="1" opacity=".12"/>`;
      const r = rnd(seed); for (let k = 0; k < 8; k++) s += `<ellipse cx="${f(x + r() * w)}" cy="${f(y + r() * h)}" rx="${f(30 + r() * 50)}" ry="${f(14 + r() * 20)}" fill="#3a3a20" opacity="${f(0.06 + r() * 0.08)}"/>`; return s; },
    cloth: (x, y, w, h, seed) => { const r = rnd(seed); let s = ""; for (let k = 0; k < 10; k++) s += `<ellipse cx="${f(x + r() * w)}" cy="${f(y + r() * h)}" rx="${f(26 + r() * 60)}" ry="${f(12 + r() * 30)}" fill="#a88a50" opacity="${f(0.06 + r() * 0.1)}"/>`;
      for (let k = 0; k < w; k += 7) s += `<path d="M${x + k},${y}V${y + h}" stroke="#8a7040" stroke-width=".8" opacity=".1"/>`; return s; },
  };
  // the highlight tool strokes (x0..x1 at row y): returns markup with id (animated by clip width or dash)
  const hiTool = (tool, id, x0, x1, y) => {
    if (tool === "marker") return `<path id="${id}" d="M${x0},${y - 38}Q${(x0 + x1) / 2},${y - 50} ${x1},${y - 40}L${x1 + 8},${y + 22}Q${(x0 + x1) / 2},${y + 30} ${x0 - 6},${y + 18}Z" fill="#fff23a" opacity=".62"/>`;
    if (tool === "chalk") return `<path id="${id}" d="M${x0},${y + 26}Q${(x0 + x1) / 2},${y + 14} ${x1},${y + 28}" stroke="#ffd84a" stroke-width="9" fill="none" stroke-linecap="round" stroke-dasharray="1 0.02" pathLength="1" opacity=".9"/>`;
    if (tool === "spray") { let d = ""; const r = rnd(x1); for (let k = 0; k < 70; k++) d += `<circle cx="${f(x0 + r() * (x1 - x0))}" cy="${f(y - 46 + r() * 76)}" r="${f(1 + r() * 3)}" fill="#ff7a1a" opacity="${f(0.3 + r() * 0.5)}"/>`;
      return `<g id="${id}"><rect x="${x0}" y="${y - 40}" width="${x1 - x0}" height="62" rx="26" fill="#ff8a2a" opacity=".55" filter="url(#ifxBlur3)"/>${d}</g>`; }
    if (tool === "brush") return `<path id="${id}" d="M${x0},${y - 30}Q${(x0 + x1) / 2},${y - 44} ${x1},${y - 34}L${x1 + 12},${y + 14}Q${(x0 + x1) / 2},${y + 26} ${x0 - 8},${y + 16}Z" fill="#ffd23a" opacity=".55"/>`;
    if (tool === "grease") return `<ellipse id="${id}" cx="${(x0 + x1) / 2}" cy="${y - 10}" rx="${(x1 - x0) / 2 + 26}" ry="52" fill="none" stroke="#c8201a" stroke-width="8" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" transform="rotate(-2 ${(x0 + x1) / 2} ${y - 10})"/>`;
    if (tool === "pen") return `<path id="${id}" d="M${x0 - 10},${y + 26}Q${(x0 + x1) / 2},${y + 34} ${x1 + 10},${y + 22}" stroke="#d8312a" stroke-width="7" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>`;
    return `<path id="${id}" d="M${x0},${y - 30}Q${(x0 + x1) / 2},${y - 40} ${x1},${y - 30}L${x1 + 6},${y + 18}Q${(x0 + x1) / 2},${y + 26} ${x0 - 6},${y + 16}Z" fill="#e8b830" opacity=".5"/>`;
  };
  const tick = (tool, id, x, y) => { const c = tool === "chalk" ? "#f4f2e8" : tool === "spray" ? "#1e9a50" : tool === "gold" ? "#c8901a" : tool === "grease" ? "#b8201a" : "#d8312a";
    return `<path id="${id}" d="M${x},${y - 6}l22,26l46,-58" stroke="${c}" stroke-width="${tool === "spray" ? 17 : 13}" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>`; };

  // the object for each skin: { back, front, life(tl,id,t,dur), enter(tl,id,t) } — back = the material + its fixtures, front = props over the rows
  const objects = {
    clipboard: (id, X, Y, W, H, o) => ({
      back: `<rect x="${X + 10}" y="${Y + 22}" width="${W}" height="${H}" rx="34" fill="#000" opacity=".3"/>
        <rect x="${X}" y="${Y}" width="${W}" height="${H}" rx="34" fill="url(#ifxAlu)" ${O(5)}/>${tex.brushed(X, Y, W, H, 3)}
        <g id="${id}-paper"><path d="M${X + 46},${Y + 120}H${X + W - 46}V${Y + H - 90}L${X + W - 110},${Y + H - 40}H${X + 46}Z" fill="#fbf8ee" ${O(3)}/>${tex.paper(X + 46, Y + 120, W - 92, H - 160, 9)}
          ${Array.from({ length: Math.floor((H - 260) / 60) }, (_, k) => `<path d="M${X + 60},${Y + 260 + k * 60}H${X + W - 60}" stroke="#7ab0e0" stroke-width="2" opacity=".55"/>`).join("")}<path d="M${X + 130},${Y + 130}V${Y + H - 50}" stroke="#e86a6a" stroke-width="2.5" opacity=".6"/>
          ${tex.prints(X + W - 260, Y + H - 260, 3, 17)}${tex.prints(X + 70, Y + 150, 2, 23)}<ellipse cx="${X + W - 170}" cy="${Y + 210}" rx="58" ry="52" fill="none" stroke="#7a5a3a" stroke-width="7" opacity=".18"/>
          <g id="${id}-curl"><path d="M${X + W - 110},${Y + H - 40}L${X + W - 46},${Y + H - 90}Q${X + W - 96},${Y + H - 96} ${X + W - 110},${Y + H - 40}Z" fill="#e2dccb" ${O(3)}/></g></g>
        <g transform="translate(${X + W / 2},${Y + 40})"><rect x="-150" y="-36" width="300" height="104" rx="22" fill="url(#ifxAluD)" ${O(5)}/><rect x="-110" y="-60" width="220" height="40" rx="18" fill="url(#ifxAlu)" ${O(4)}/><circle cx="-120" cy="18" r="9" fill="#c8ccd2" ${O(2)}/><circle cx="120" cy="18" r="9" fill="#c8ccd2" ${O(2)}/>
          <path d="M-90,60Q0,80 90,60" stroke="#5a606a" stroke-width="6" fill="none"/></g>`,
      front: `<g transform="translate(${X + W - 120},${Y + 40})"><g id="${id}-tag"><path d="M0,0V74" stroke="#3a3a3a" stroke-width="3"/><g transform="translate(0,74) rotate(4)"><rect x="-58" y="0" width="116" height="160" rx="12" fill="#f4c430" ${O(4)}/>
          ${Array.from({ length: 5 }, (_, k) => `<path d="M${-58 + k * 30},160l40,-40v22l-18,18z" fill="${INK}"/>`).join("")}<circle cy="18" r="8" fill="#fff" ${O(2)}/><text y="72" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="${INK}">ห้าม</text><text y="104" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="26" fill="${INK}">ใช้งาน</text></g></g></g>
        <g transform="translate(${X + 26},${Y + 40})"><g id="${id}-pen"><path d="M0,0Q-30,120 -10,220" stroke="#3a3a3a" stroke-width="3" fill="none"/><g transform="translate(-10,220) rotate(-8)"><rect x="-13" y="0" width="26" height="150" rx="10" fill="#1d3a8a" ${O(4)}/><rect x="-13" y="0" width="26" height="40" rx="10" fill="#2a2e36" ${O(3)}/><path d="M-10,150L0,176L10,150Z" fill="#3a3a3a" ${O(3)}/><rect x="-4" y="44" width="8" height="70" rx="4" fill="#fff" opacity=".35"/></g></g></g>`,
      enter: (tl, t) => { tl.fromTo(`#${id}-m`, { y: 1300 }, { y: 0, duration: 0.5, ease: "power3.out", immediateRender: false }, t);
        tl.fromTo(`#${id}-k`, { scale: 1.55, rotation: -14, svgOrigin: `540 ${Y + H / 2}` }, { scale: 1, rotation: -1.5, svgOrigin: `540 ${Y + H / 2}`, duration: 0.5, ease: "power3.out", immediateRender: false }, t);
        tl.fromTo(`#${id}-sw`, { rotation: 3, svgOrigin: `540 ${Y + H}` }, { rotation: 0, svgOrigin: `540 ${Y + H}`, duration: 0.9, ease: "elastic.out(1,0.35)", immediateRender: false }, t + 0.45); return t + 0.42; },
      life: (tl, t, dur) => { const R = (p) => Math.ceil(dur / p);
        tl.fromTo(`#${id}-m`, { y: 0 }, { y: -8, duration: 1.1, yoyo: true, repeat: R(1.1), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-sw`, { rotation: -0.8, svgOrigin: `540 ${Y + H}` }, { rotation: 0.8, svgOrigin: `540 ${Y + H}`, duration: 1.4, yoyo: true, repeat: R(1.4), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-tag`, { rotation: -10, svgOrigin: "0 0" }, { rotation: 12, svgOrigin: "0 0", duration: 0.8, yoyo: true, repeat: R(0.8), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-pen`, { rotation: 8, svgOrigin: "0 0" }, { rotation: -8, svgOrigin: "0 0", duration: 1.0, yoyo: true, repeat: R(1.0), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-curl`, { scaleY: 1, svgOrigin: `${X + W - 46} ${Y + H - 90}` }, { scaleY: 1.5, svgOrigin: `${X + W - 46} ${Y + H - 90}`, duration: 0.45, yoyo: true, repeat: R(0.45), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-paper`, { skewX: 0, svgOrigin: `540 ${Y + 120}` }, { skewX: 0.6, svgOrigin: `540 ${Y + 120}`, duration: 0.7, yoyo: true, repeat: R(0.7), ease: "sine.inOut", immediateRender: false }, t); } }),
    chalk: (id, X, Y, W, H) => ({
      back: `<path d="M${X + 140},-40L${X + 200},${Y}M${X + W - 140},-40L${X + W - 200},${Y}" stroke="#3a3a3a" stroke-width="5"/>
        <rect x="${X + 10}" y="${Y + 22}" width="${W}" height="${H}" rx="14" fill="#000" opacity=".3"/>
        <rect x="${X}" y="${Y}" width="${W}" height="${H}" rx="14" fill="#8a5a30" ${O(5)}/><rect x="${X + 26}" y="${Y + 26}" width="${W - 52}" height="${H - 52}" rx="6" fill="url(#ifxSlate)" ${O(4)}/>${tex.slate(X + 26, Y + 26, W - 52, H - 52, 5)}
        ${Array.from({ length: 6 }, (_, k) => `<path d="M${X + 4},${Y + 20 + k * (H / 6)}h${W - 8}" stroke="#6a4020" stroke-width="2" opacity=".3"/>`).join("")}
        <rect x="${X - 10}" y="${Y + H - 8}" width="${W + 20}" height="34" rx="8" fill="#9a6a3a" ${O(4)}/>`,
      front: `<g transform="translate(${X + W - 260},${Y + H - 14})"><g id="${id}-eraser"><rect x="0" y="-34" width="120" height="40" rx="8" fill="#2a3a8a" ${O(3)}/><rect x="0" y="-8" width="120" height="14" fill="#f4f2e8" opacity=".9"/></g></g>
        <g transform="translate(${X + 140},${Y + H - 14})"><g id="${id}-chalk"><rect x="0" y="-16" width="90" height="18" rx="8" fill="#f8f6ee" ${O(2.5)}/><rect x="104" y="-16" width="50" height="18" rx="8" fill="#ffd84a" ${O(2.5)}/></g></g>
        <g id="${id}-dust">${Array.from({ length: 10 }, (_, k) => `<circle cx="${X + 180 + k * 70}" cy="${Y + H - 40}" r="${3 + (k % 3) * 2}" fill="#ffffff" opacity="0"/>`).join("")}</g>`,
      enter: (tl, t) => { tl.fromTo(`#${id}-m`, { y: -1300 }, { y: 0, duration: 0.5, ease: "power3.out", immediateRender: false }, t);
        tl.fromTo(`#${id}-sw`, { rotation: 5, svgOrigin: `540 -600` }, { rotation: 0, svgOrigin: `540 -600`, duration: 1.4, ease: "elastic.out(1,0.3)", immediateRender: false }, t + 0.4); return t + 0.45; },
      life: (tl, t, dur) => { const R = (p) => Math.ceil(dur / p);
        tl.fromTo(`#${id}-sw`, { rotation: -0.5, svgOrigin: `540 -600` }, { rotation: 0.5, svgOrigin: `540 -600`, duration: 1.6, yoyo: true, repeat: R(1.6), ease: "sine.inOut", immediateRender: false }, t + 1);
        tl.fromTo(`#${id}-eraser`, { x: 0 }, { x: -30, duration: 0.9, yoyo: true, repeat: R(0.9), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-chalk`, { rotation: -3, svgOrigin: "45 0" }, { rotation: 3, svgOrigin: "45 0", duration: 0.7, yoyo: true, repeat: R(0.7), ease: "sine.inOut", immediateRender: false }, t);
        document.querySelectorAll(`#${id}-dust circle`).forEach((c, k) => tl.fromTo(c, { y: 0, opacity: 0.6 }, { y: -120 - k * 10, x: (k % 2 ? 20 : -20), opacity: 0, duration: 1.6, repeat: R(1.6), ease: "sine.out", immediateRender: false }, t + k * 0.17)); } }),
    // a truck's steel tailgate (owner: "ถนนเหมือนไม้เลย" → it must read as STEEL): pressed ribs (lit top edge, shadowed lower edge, rounded
    // ends), a silver frame with highlights, bolt heads along it, lock handles both sides, hinges and pins below, rust running from the bolts,
    // dents, a band of mud spray at the bottom, a hazard stripe, a metal sheen sweeping across
    tailgate: (id, X, Y, W, H) => { const rr = rnd(77), ribs = Math.floor((H - 150) / 64);
      let ribsS = ""; for (let k = 0; k < ribs; k++) { const y = Y + 120 + k * 64;
        ribsS += `<rect x="${X + 70}" y="${y}" width="${W - 140}" height="38" rx="19" fill="#9a2a1e"/><rect x="${X + 70}" y="${y}" width="${W - 140}" height="38" rx="19" fill="url(#ifxRib)"/>
          <path d="M${X + 88},${y + 4}H${X + W - 88}" stroke="#ff9a7a" stroke-width="4" stroke-linecap="round" opacity=".8"/><path d="M${X + 88},${y + 36}H${X + W - 88}" stroke="#4a0e0a" stroke-width="5" stroke-linecap="round" opacity=".7"/>`; }
      let bolts = ""; for (let k = 0; k < 9; k++) { const bx = X + 60 + k * (W - 120) / 8;
        [[bx, Y + 34], [bx, Y + H - 34]].forEach(([a, b]) => { bolts += `<circle cx="${f(a)}" cy="${b}" r="11" fill="#c8ccd2" ${O(2)}/><path d="M${f(a - 6)},${b}h12" stroke="#5a606a" stroke-width="3"/>`;
          if (rr() < 0.45) bolts += `<path d="M${f(a)},${b + 10}q${f(-3 + rr() * 6)},${f(30 + rr() * 30)} 0,${f(60 + rr() * 50)}" stroke="#8a3e14" stroke-width="${f(4 + rr() * 4)}" opacity=".55" fill="none" stroke-linecap="round"/>`; }); }
      let dents = ""; for (let k = 0; k < 4; k++) { const dx = X + 160 + rr() * (W - 320), dy = Y + 140 + rr() * (H - 260); dents += `<ellipse cx="${f(dx)}" cy="${f(dy)}" rx="${f(26 + rr() * 30)}" ry="${f(10 + rr() * 12)}" fill="#3a0a06" opacity=".22"/><path d="M${f(dx - 20)},${f(dy - 6)}q20,-8 40,0" stroke="#ffb0a0" stroke-width="3" opacity=".45" fill="none"/>`; }
      let mud = ""; for (let k = 0; k < 60; k++) { const mx = X + rr() * W, my = Y + H - 20 - Math.pow(rr(), 2) * 130; mud += `<ellipse cx="${f(mx)}" cy="${f(my)}" rx="${f(2 + rr() * 10)}" ry="${f(2 + rr() * 6)}" fill="#4a3a28" opacity="${f(0.35 + rr() * 0.4)}"/>`; }
      return {
      back: `<rect x="${X + 10}" y="${Y + 22}" width="${W}" height="${H}" rx="22" fill="#000" opacity=".35"/>
        <rect x="${X}" y="${Y}" width="${W}" height="${H}" rx="22" fill="url(#ifxSteelF)" ${O(5)}/><rect x="${X + 8}" y="${Y + 8}" width="${W - 16}" height="10" rx="5" fill="#ffffff" opacity=".7"/>
        <rect x="${X + 40}" y="${Y + 54}" width="${W - 80}" height="${H - 108}" rx="10" fill="#b8321f" ${O(4)}/>${ribsS}
        <path d="M${X + 40},${Y + 54}H${X + W - 40}" stroke="#ff8a6a" stroke-width="4" opacity=".7"/>${dents}
        <g transform="translate(${X + 40},${Y + H - 108})"><clipPath id="${id}-hz"><rect width="${W - 80}" height="36"/></clipPath><rect width="${W - 80}" height="36" fill="#f4f4ee"/><g clip-path="url(#${id}-hz)">${Array.from({ length: Math.ceil((W - 80) / 40) + 1 }, (_, k) => `<path d="M${k * 40},36l26,-36h18l-26,36z" fill="#d8201a"/>`).join("")}</g><rect width="${W - 80}" height="36" fill="none" ${O(3)}/></g>
        ${mud}${bolts}
        ${[[X + 4, 1], [X + W - 4, -1]].map(([a, sg]) => `<g transform="translate(${a},${Y + H / 2})"><rect x="${sg > 0 ? -34 : -10}" y="-60" width="44" height="120" rx="10" fill="url(#ifxSteelF)" ${O(4)}/><rect x="${sg > 0 ? -24 : 0}" y="-40" width="24" height="80" rx="8" fill="#5a606a" ${O(3)}/><circle cx="${sg > 0 ? -12 : 12}" cy="-48" r="7" fill="#2a2e36"/></g>`).join("")}
        ${[X + 170, X + W / 2, X + W - 170].map((a) => `<g transform="translate(${a},${Y + H})"><rect x="-44" y="-10" width="88" height="30" rx="8" fill="url(#ifxSteelF)" ${O(3)}/><rect x="-6" y="-16" width="12" height="42" rx="5" fill="#8a929c" ${O(2)}/></g>`).join("")}
        <g clip-path="url(#${id}-gclip)"><rect id="${id}-sheen" x="${X - 300}" y="${Y}" width="140" height="${H}" fill="#ffffff" opacity=".22" transform="skewX(-20)"/></g>
        <defs><clipPath id="${id}-gclip"><rect x="${X}" y="${Y}" width="${W}" height="${H}" rx="22"/></clipPath></defs>
        ${[[X + 60, Y + 60], [X + W - 60, Y + 60]].map(([a, b], k) => `<g transform="translate(${a},${b})"><circle r="24" fill="#2a2e36" ${O(3)}/><circle id="${id}-rf${k}" r="17" fill="#ff6a2a" ${O(2)}/><circle cx="-5" cy="-6" r="4" fill="#fff" opacity=".8"/></g>`).join("")}`,
      front: `${[[X - 6, 1], [X + W + 6, -1]].map(([a, sg], k) => `<g transform="translate(${a},${Y + 10})"><g id="${id}-ch${k}">${Array.from({ length: 9 }, (_, j) => `<ellipse cx="${sg * j * 3}" cy="${j * 26}" rx="8" ry="14" fill="none" stroke="#9aa2ac" stroke-width="5"/>`).join("")}</g></g>`).join("")}`,
      enter: (tl, t) => { tl.fromTo(`#${id}-m`, { y: -1400 }, { y: 0, duration: 0.42, ease: "power3.in", immediateRender: false }, t);
        tl.fromTo(`#${id}-sw`, { scaleY: 0.86, scaleX: 1.04, svgOrigin: `540 ${Y + H}` }, { scaleY: 1, scaleX: 1, svgOrigin: `540 ${Y + H}`, duration: 0.6, ease: "elastic.out(1.2,0.3)", immediateRender: false }, t + 0.42); return t + 0.42; },
      life: (tl, t, dur) => { const R = (p) => Math.ceil(dur / p);
        tl.fromTo(`#${id}-k`, { y: 0 }, { y: 3, duration: 0.07, yoyo: true, repeat: R(0.07), ease: "sine.inOut", immediateRender: false }, t);
        [0, 1].forEach((k) => tl.fromTo(`#${id}-ch${k}`, { rotation: -6, svgOrigin: "0 0" }, { rotation: 6, svgOrigin: "0 0", duration: 0.5 + k * 0.1, yoyo: true, repeat: R(0.5), ease: "sine.inOut", immediateRender: false }, t));
        tl.fromTo(`#${id}-sheen`, { x: 0 }, { x: W + 600, duration: 1.4, repeat: R(1.8), repeatDelay: 0.4, ease: "power1.inOut", immediateRender: false }, t);
        for (let k = 0; k < 2; k++) for (let j = 0; j * 1.4 < dur; j++) tl.fromTo(`#${id}-rf${k}`, { attr: { fill: "#fff2c0" } }, { attr: { fill: "#ff6a2a" }, duration: 0.35, ease: "power2.out", immediateRender: false }, t + 0.2 + j * 1.4 + k * 0.2); } }; },
    canal: (id, X, Y, W, H) => ({
      back: `<rect x="${X + W / 2 - 30}" y="${Y + H - 10}" width="60" height="700" fill="url(#ifxPost)" ${O(4)}/>
        <rect x="${X + 10}" y="${Y + 22}" width="${W}" height="${H}" rx="18" fill="#000" opacity=".35"/>
        <rect x="${X}" y="${Y}" width="${W}" height="${H}" rx="18" fill="#f2efe4" ${O(5)}/><rect x="${X + 20}" y="${Y + 20}" width="${W - 40}" height="${H - 40}" rx="12" fill="none" stroke="#c8201a" stroke-width="16"/>
        ${tex.rust(X, Y, W, H, 41)}${[[X + 40, Y + 40], [X + W - 40, Y + 40], [X + 40, Y + H - 40], [X + W - 40, Y + H - 40]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="11" fill="#8a3e14" ${O(2)}/><path d="M${a - 6},${b}h12" stroke="#2a1a10" stroke-width="3"/>`).join("")}
        <g id="${id}-ripple" opacity=".18">${Array.from({ length: 5 }, (_, k) => `<path d="M${X},${Y + 200 + k * 120}q120,-24 240,0t240,0t240,0t240,0" stroke="#8ad0ff" stroke-width="10" fill="none"/>`).join("")}</g>`,
      front: `<g transform="translate(${X + W - 8},${Y + 140})"><g id="${id}-ring"><path d="M0,0V60" stroke="#e8e0c8" stroke-width="5"/><g transform="translate(0,140)"><circle r="80" fill="#ff7a2a" ${O(4)}/><circle r="44" fill="#2a3a4a" ${O(4)}/>${[0, 1, 2, 3].map((k) => `<path d="M${f(Math.cos(k * 1.571 + 0.4) * 44)},${f(Math.sin(k * 1.571 + 0.4) * 44)}L${f(Math.cos(k * 1.571 + 0.4) * 80)},${f(Math.sin(k * 1.571 + 0.4) * 80)}A80,80 0 0 1 ${f(Math.cos(k * 1.571 + 0.9) * 80)},${f(Math.sin(k * 1.571 + 0.9) * 80)}L${f(Math.cos(k * 1.571 + 0.9) * 44)},${f(Math.sin(k * 1.571 + 0.9) * 44)}Z" fill="#fdfaf2" ${O(2)}/>`).join("")}</g></g></g>
        <g id="${id}-drips">${Array.from({ length: 5 }, (_, k) => `<path d="M${X + 120 + k * 170},${Y + H}q-8,14 0,22q8,-8 0,-22z" fill="#8ad0ff" ${O(1.5)} opacity="0"/>`).join("")}</g>`,
      enter: (tl, t) => { tl.fromTo(`#${id}-m`, { y: -1100 }, { y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }, t);
        tl.fromTo(`#${id}-sw`, { rotation: 16, svgOrigin: `${X + 40} ${Y + 40}` }, { rotation: 0, svgOrigin: `${X + 40} ${Y + 40}`, duration: 1.4, ease: "elastic.out(1,0.28)", immediateRender: false }, t + 0.4); return t + 0.45; },
      life: (tl, t, dur) => { const R = (p) => Math.ceil(dur / p);
        tl.fromTo(`#${id}-sw`, { rotation: -0.6, svgOrigin: `${X + 40} ${Y + 40}` }, { rotation: 0.6, svgOrigin: `${X + 40} ${Y + 40}`, duration: 1.5, yoyo: true, repeat: R(1.5), ease: "sine.inOut", immediateRender: false }, t + 1);
        tl.fromTo(`#${id}-ring`, { rotation: -9, svgOrigin: "0 0" }, { rotation: 9, svgOrigin: "0 0", duration: 0.9, yoyo: true, repeat: R(0.9), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-ripple`, { x: 0 }, { x: -240, duration: 2.4, repeat: R(2.4), ease: "none", immediateRender: false }, t);
        document.querySelectorAll(`#${id}-drips path`).forEach((d, k) => tl.fromTo(d, { y: 0, opacity: 1 }, { y: 220, opacity: 0, duration: 0.8, repeat: R(1.3), repeatDelay: 0.5, ease: "power2.in", immediateRender: false }, t + k * 0.29)); } }),
    fieldbook: (id, X, Y, W, H) => ({
      back: `<rect x="${X + 10}" y="${Y + 22}" width="${W}" height="${H}" rx="26" fill="#000" opacity=".35"/>
        <rect x="${X}" y="${Y}" width="${W}" height="${H}" rx="26" fill="#5a6238" ${O(5)}/>${tex.canvas(X, Y, W, H, 43)}
        <rect x="${X + 16}" y="${Y + 16}" width="${W - 32}" height="${H - 32}" rx="18" fill="none" stroke="#c8c098" stroke-width="3" stroke-dasharray="12 9"/>
        <rect x="${X + 40}" y="${Y + 140}" width="${W - 80}" height="${H - 190}" rx="6" fill="#efe8cc" ${O(3)}/>${tex.paper(X + 40, Y + 140, W - 80, H - 190, 47)}
        ${Array.from({ length: Math.floor((W - 80) / 60) }, (_, k) => `<path d="M${X + 40 + k * 60},${Y + 140}V${Y + H - 50}" stroke="#9ab08a" stroke-width="1.4" opacity=".5"/>`).join("")}${Array.from({ length: Math.floor((H - 190) / 60) }, (_, k) => `<path d="M${X + 40},${Y + 140 + k * 60}H${X + W - 40}" stroke="#9ab08a" stroke-width="1.4" opacity=".5"/>`).join("")}`,
      front: `<g transform="translate(${X + W - 150},${Y - 10})"><g id="${id}-strap"><rect x="-34" y="0" width="68" height="300" rx="10" fill="#6a4a2a" ${O(4)}/><rect x="-44" y="210" width="88" height="56" rx="8" fill="none" stroke="#c8b070" stroke-width="9"/><path d="M0,214V262" stroke="#c8b070" stroke-width="7"/></g></g>
        <g transform="translate(${X + 90},${Y + H - 30})"><g id="${id}-pencil"><rect x="0" y="-12" width="170" height="24" rx="6" fill="#d8a020" ${O(3)}/><path d="M170,-12L204,0L170,12Z" fill="#e8c890" ${O(3)}/><path d="M196,-3L204,0L196,3Z" fill="#2a2a2a"/><rect x="-24" y="-12" width="26" height="24" rx="4" fill="#e88a8a" ${O(3)}/></g></g>
        <g id="${id}-dust">${Array.from({ length: 10 }, (_, k) => `<circle cx="${X + 80 + k * 85}" cy="${Y + H + 10}" r="${5 + (k % 3) * 3}" fill="#a8906a" opacity="0"/>`).join("")}</g>`,
      enter: (tl, t) => { tl.fromTo(`#${id}-m`, { y: -200 }, { y: 0, duration: 0.32, ease: "power4.in", immediateRender: false }, t);
        tl.fromTo(`#${id}-k`, { scale: 1.35, svgOrigin: `540 ${Y + H / 2}` }, { scale: 1, svgOrigin: `540 ${Y + H / 2}`, duration: 0.32, ease: "power4.in", immediateRender: false }, t);
        tl.fromTo(`#${id}-sw`, { scaleY: 0.94, svgOrigin: `540 ${Y + H}` }, { scaleY: 1, svgOrigin: `540 ${Y + H}`, duration: 0.4, ease: "elastic.out(1.2,0.3)", immediateRender: false }, t + 0.32);
        document.querySelectorAll(`#${id}-dust circle`).forEach((c, k) => tl.fromTo(c, { y: 0, x: 0, opacity: 0.8, scale: 0.6 }, { y: -40 - (k % 4) * 30, x: (k - 5) * 22, opacity: 0, scale: 2.2, duration: 0.9, ease: "power2.out", immediateRender: false }, t + 0.32)); return t + 0.32; },
      life: (tl, t, dur) => { const R = (p) => Math.ceil(dur / p);
        tl.fromTo(`#${id}-strap`, { rotation: -4, svgOrigin: "0 0" }, { rotation: 4, svgOrigin: "0 0", duration: 1.1, yoyo: true, repeat: R(1.1), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-pencil`, { rotation: 0, svgOrigin: "0 0" }, { rotation: -6, svgOrigin: "0 0", duration: 0.9, yoyo: true, repeat: R(0.9), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-m`, { y: 0 }, { y: -6, duration: 1.3, yoyo: true, repeat: R(1.3), ease: "sine.inOut", immediateRender: false }, t); } }),
    seatcard: (id, X, Y, W, H, o) => { const nv = o.band || "#1d2c5e", gd = o.gold || "#f4c430";
      return {
      back: `<rect x="${X + 8}" y="${Y + 18}" width="${W}" height="${H + 120}" rx="30" fill="#000" opacity=".3"/>
        <rect x="${X}" y="${Y}" width="${W}" height="${H + 120}" rx="30" fill="#fbfaf6" ${O(5)}/>${tex.paper(X, Y, W, H, 61)}
        <path d="M${X},${Y + 30}Q${X},${Y} ${X + 30},${Y}H${X + W - 30}Q${X + W},${Y} ${X + W},${Y + 30}V${Y + 150}H${X}Z" fill="${nv}" ${O(5)}/><rect x="${X}" y="${Y + 150}" width="${W}" height="12" fill="${gd}"/>
        <text x="${X + 40}" y="${Y + 62}" font-family="Kanit" font-weight="800" font-size="30" fill="${gd}">${o.brand || "ฟ้าราม แอร์"} · SAFETY</text>
        <g transform="translate(${X + W - 90},${Y + 76}) rotate(-8)"><path d="M-40,0L30,-8L40,4L-30,14Z" fill="#fff"/><path d="M-6,-2L-24,-26H-12L10,-4Z" fill="#fff"/></g>
        <path d="M${X + W / 2},${Y + 170}V${Y + H + 110}" stroke="#d8d4c8" stroke-width="3" stroke-dasharray="10 8"/>
        <path d="M${X + 40},${Y + H - 40}h${W - 80}" stroke="#e8e4d8" stroke-width="2"/>
        <g opacity=".5">${[0, 1, 2].map((k) => `<g transform="translate(${X + 120 + k * 120},${Y + H + 40})"><circle r="26" fill="#e8ecf2" ${O(2)}/><path d="M-10,8V-6h20V8M0,-6V-16" stroke="${nv}" stroke-width="4" fill="none"/></g>`).join("")}<text x="${X + W - 60}" y="${Y + H + 52}" text-anchor="end" font-family="Kanit" font-weight="700" font-size="26" fill="#8a90a0">โปรดอ่านก่อนออกเดินทาง</text></g>
        <path id="${id}-gloss" d="M${X + 80},${Y + 170}L${X + 260},${Y + 170}L${X + 120},${Y + H + 100}L${X - 60},${Y + H + 100}Z" fill="#ffffff" opacity=".22"/>`,
      front: "",
      over: o.pocket === false ? "" : `<g transform="translate(0,${Y + H - 10})"><defs><linearGradient id="${id}-fab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#24346a"/><stop offset=".55" stop-color="#24346a" stop-opacity=".85"/><stop offset="1" stop-color="#24346a" stop-opacity="0"/></linearGradient></defs><rect x="-40" y="0" width="1160" height="300" fill="url(#${id}-fab)"/>${Array.from({ length: 10 }, (_, k) => `<path d="M-40,${k * 18}H1160" stroke="#1a2650" stroke-width="3" opacity="${(0.5 - k * 0.045).toFixed(2)}"/>`).join("")}
        <path d="M20,0H1060V140Q540,170 20,140Z" fill="#2a3c78" ${O(5)}/>${Array.from({ length: 34 }, (_, k) => `<path d="M${30 + k * 31},6V136" stroke="#14204a" stroke-width="3" opacity=".55"/>`).join("")}<path d="M20,4H1060" stroke="#4a5c98" stroke-width="12"/><path d="M20,4H1060" stroke="${INK}" stroke-width="4"/>
        <g transform="translate(860,60)"><g id="${id}-belt"><rect x="-60" y="0" width="120" height="44" rx="10" fill="#c8ccd2" ${O(4)}/><rect x="-30" y="10" width="60" height="24" rx="6" fill="#8a929c"/><path d="M-60,22H-180" stroke="#5a6070" stroke-width="30"/></g></g></g>`,
      enter: (tl, t) => { tl.fromTo(`#${id}-m`, { y: 900 }, { y: 0, duration: 0.55, ease: "power3.out", immediateRender: false }, t);
        tl.fromTo(`#${id}-k`, { rotation: 4, svgOrigin: `540 ${Y + H}` }, { rotation: -1, svgOrigin: `540 ${Y + H}`, duration: 0.9, ease: "elastic.out(1,0.45)", immediateRender: false }, t + 0.3); return t + 0.5; },
      life: (tl, t, dur) => { const R = (p) => Math.ceil(dur / p);
        tl.fromTo(`#${id}-sw`, { rotation: -0.6, svgOrigin: `540 ${Y + H}` }, { rotation: 0.6, svgOrigin: `540 ${Y + H}`, duration: 1.2, yoyo: true, repeat: R(1.2), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-gloss`, { x: -120, opacity: 0.1 }, { x: 780, opacity: 0.3, duration: 1.8, repeat: R(1.8), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-belt`, { rotation: -6, svgOrigin: "-60 22" }, { rotation: 6, svgOrigin: "-60 22", duration: 0.7, yoyo: true, repeat: R(0.7), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-m`, { y: 0 }, { y: -6, duration: 0.11, yoyo: true, repeat: R(0.11), ease: "sine.inOut", immediateRender: false }, t); } }; },
    yant: (id, X, Y, W, H) => { const burnt = `M${X},${Y + 20}H${X + W}V${Y + H}` + Array.from({ length: 12 }, (_, k) => `L${X + W - (k + 1) * W / 12},${Y + H + (k % 2 ? 26 : -4)}`).join("") + "Z";
      return {
      back: `<path d="M${X - 40},${Y}H${X + W + 40}" stroke="#8a6a30" stroke-width="22" stroke-linecap="round"/><path d="M${X - 40},${Y}H${X + W + 40}" stroke="#c8a060" stroke-width="8" stroke-linecap="round" opacity=".6"/>
        <path d="M${X + 140},${Y}L${X + 540 - 70},-40L${X + W - 140},${Y}" stroke="#c8201a" stroke-width="5" fill="none"/>
        <g id="${id}-cloth"><path d="${burnt}" fill="#000" opacity=".3" transform="translate(10,20)"/><path d="${burnt}" fill="url(#ifxCloth)" ${O(5)}/>${tex.cloth(X, Y, W, H, 53)}
          <rect x="${X + 24}" y="${Y + 44}" width="${W - 48}" height="${H - 90}" fill="none" stroke="#b8201a" stroke-width="5"/><rect x="${X + 36}" y="${Y + 56}" width="${W - 72}" height="${H - 114}" fill="none" stroke="#b8201a" stroke-width="2" stroke-dasharray="14 6"/>
          ${Array.from({ length: 8 }, (_, k) => `<path d="M${X + 60 + k * 112},${Y + H - 70}l20,-20l20,20l-20,20z" fill="none" stroke="#b8201a" stroke-width="3" opacity=".7"/>`).join("")}
          <path d="M${X + W - 110},${Y + H - 170}c-30,-10 -30,30 0,26c40,-6 30,-60 -10,-60c-50,0 -60,70 0,80c50,6 60,-30 70,-80" stroke="#b8201a" stroke-width="5" fill="none" opacity=".55"/>
          ${Array.from({ length: 10 }, (_, k) => `<ellipse cx="${X + 30 + k * 95}" cy="${Y + H - 8 + (k % 2) * 20}" rx="24" ry="9" fill="#3a2010" opacity=".35"/>`).join("")}</g>`,
      front: `<g transform="translate(${X + W - 70},${Y + H + 120})"><rect x="-26" y="0" width="52" height="150" rx="6" fill="#fff4d8" ${O(4)}/><g id="${id}-flame"><path d="M0,0C-24,-36 -8,-74 0,-96C8,-74 24,-36 0,0Z" fill="#ffb030" ${O(3)}/><path d="M0,-10C-10,-28 -4,-48 0,-60C4,-48 10,-28 0,-10Z" fill="#fff2a0"/></g>
          <circle cy="-40" r="110" fill="url(#ifxCandle)" opacity=".6"/>${Array.from({ length: 4 }, (_, k) => `<circle id="${id}-sm${k}" cy="-100" r="${18 + k * 6}" fill="#c8c0b8" opacity="0"/>`).join("")}</g>`,
      enter: (tl, t) => { tl.fromTo(`#${id}-m`, { y: -900 }, { y: 0, duration: 0.4, ease: "power3.out", immediateRender: false }, t);
        tl.fromTo(`#${id}-cloth`, { scaleY: 0.05, svgOrigin: `540 ${Y}` }, { scaleY: 1, svgOrigin: `540 ${Y}`, duration: 0.7, ease: "elastic.out(1,0.45)", immediateRender: false }, t + 0.35); return t + 0.6; },
      life: (tl, t, dur) => { const R = (p) => Math.ceil(dur / p);
        tl.fromTo(`#${id}-cloth`, { skewX: -1.2, svgOrigin: `540 ${Y}` }, { skewX: 1.2, svgOrigin: `540 ${Y}`, duration: 1.3, yoyo: true, repeat: R(1.3), ease: "sine.inOut", immediateRender: false }, t);
        tl.fromTo(`#${id}-flame`, { scaleY: 0.85, rotation: -6, svgOrigin: "0 0" }, { scaleY: 1.12, rotation: 6, svgOrigin: "0 0", duration: 0.18, yoyo: true, repeat: R(0.18), ease: "sine.inOut", immediateRender: false }, t);
        for (let k = 0; k < 4; k++) tl.fromTo(`#${id}-sm${k}`, { y: 0, x: 0, opacity: 0.35 }, { y: -260, x: (k % 2 ? 30 : -30), opacity: 0, scale: 2, duration: 2.2, repeat: R(2.2), ease: "sine.out", immediateRender: false }, t + k * 0.55); } }; },
  };
  const boardDefs = (layer) => { if (document.getElementById("ifxAlu")) return;
    put(layer, `<defs><linearGradient id="ifxAlu" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8ecf0"/><stop offset=".45" stop-color="#b8c0ca"/><stop offset=".7" stop-color="#d8dee4"/><stop offset="1" stop-color="#8a929c"/></linearGradient>
      <linearGradient id="ifxAluD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8d0d8"/><stop offset="1" stop-color="#6a727c"/></linearGradient>
      <linearGradient id="ifxSlate" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a4a3a"/><stop offset="1" stop-color="#14281e"/></linearGradient>
      <linearGradient id="ifxSteelF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f6f8"/><stop offset=".3" stop-color="#b8c0ca"/><stop offset=".55" stop-color="#e2e6ea"/><stop offset="1" stop-color="#7a828c"/></linearGradient><linearGradient id="ifxRib" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a5a"/><stop offset=".35" stop-color="#d8442e"/><stop offset=".7" stop-color="#a82a1c"/><stop offset="1" stop-color="#6a160e"/></linearGradient>
      <linearGradient id="ifxPost" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a606a"/><stop offset=".5" stop-color="#9aa2ac"/><stop offset="1" stop-color="#4a505a"/></linearGradient>
      <linearGradient id="ifxCloth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf2d4"/><stop offset="1" stop-color="#e8d4a0"/></linearGradient>
      <radialGradient id="ifxCandle"><stop offset="0" stop-color="#ffd27a" stop-opacity=".8"/><stop offset="1" stop-color="#ffb040" stop-opacity="0"/></radialGradient>
      <filter id="ifxBlur8" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="8"/></filter><filter id="ifxBlur3" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="3"/></filter></defs>`); };

  IconFX.board = (tl, layer, o = {}) => {
    const sk = SK[o.skin] || SK.clipboard, id = o.id || `ifb${seq++}`, items = o.items || [], act = o.active ?? 0, done = o.done || [];
    const EX = o.skin === "clipboard" ? 80 : 0, Y = o.y ?? 300, X = 70, W = 940, rowH = 170, H = 290 + EX + items.length * rowH, t0 = o.t ?? 0, dur = o.dur ?? 3;
    const at = o.at || items.map((_, k) => 0.55 + k * 0.15), rowY = (k) => Y + 300 + EX + k * rowH;
    boardDefs(layer);
    const obj = objects[o.skin || "clipboard"](id, X, Y, W, H, o);
    const tx = X + (o.skin === "canal" || o.skin === "tailgate" ? 220 : 210);
    let rows = "";
    items.forEach((it, k) => { const st = k === act ? "act" : done.includes(k) ? "done" : "later", y = rowY(k), fs = Math.min(sk.size, Math.floor((X + W - tx - 110) / (plain(it.text).length * 0.5))), tw = Math.min(W - 300, plain(it.text).length * fs * 0.5 + 30);
      const col = st === "later" ? sk.later : sk.ink;
      rows += `<g id="${id}-r${k}" opacity="${st === "later" ? 0.55 : 0}">${st === "act" ? `<defs><clipPath id="${id}-hc"><rect id="${id}-hcr" x="${tx - 20}" y="${y - 80}" width="0" height="130"/></clipPath></defs><g clip-path="url(#${id}-hc)">${hiTool(sk.tool, `${id}-hl`, tx - 10, tx + tw, y)}</g>` : ""}
        ${it.art ? `<g transform="translate(${X + 120},${y - 18}) scale(.5)"><g id="${id}-a${k}">${it.art}</g></g>` : ""}
        ${o.skin === "tailgate" ? `<text x="${tx}" y="${y + 12}" font-family="Kanit" font-weight="900" font-size="${fs}" fill="none" stroke="#3a0a06" stroke-width="10" stroke-linejoin="round">${plain(it.text)}</text>` : ""}<text x="${tx}" y="${y + 12}" font-family="${sk.font}" font-weight="${sk.font === "Kanit" ? 900 : 400}" font-size="${fs}" fill="${col}"${sk.tool === "chalk" ? ` opacity=".92"` : ""}>${st === "later" ? plain(it.text) : marked(it.text, sk.acc)}</text>
        ${sk.tool === "spray" && st !== "later" ? `<text x="${tx}" y="${y + 12}" font-family="Kanit" font-weight="900" font-size="${fs}" fill="none" stroke="${col}" stroke-width="7" opacity=".14" filter="url(#ifxBlur3)">${plain(it.text)}</text>` : ""}
        ${st === "done" ? tick(sk.tool, `${id}-tk${k}`, tx + tw + 20, y) : ""}</g>`; });
    const title = o.skin === "fieldbook"
      ? `<text x="${X + 60}" y="${Y + 104}" font-family="Kanit" font-weight="900" font-size="70" fill="#f0e8c0" opacity=".45" filter="url(#ifxBlur3)">${o.title || ""}</text>${Array.from({ length: 50 }, (_, k) => { const r2 = rnd(k + 5); return `<circle cx="${f(X + 60 + r2() * 420)}" cy="${f(Y + 40 + r2() * 80)}" r="${f(1 + r2() * 2.4)}" fill="#f0e8c0" opacity="${f(0.2 + r2() * 0.4)}"/>`; }).join("")}<text x="${X + 60}" y="${Y + 100}" font-family="Kanit" font-weight="900" font-size="70" fill="#f0e8c0">${o.title || ""}</text>`
      : o.skin === "seatcard" ? `<text x="${X + 40}" y="${Y + 128}" font-family="Kanit" font-weight="900" font-size="56" fill="#ffffff">${o.title || ""}</text>`
      : `<text x="540" y="${Y + (o.skin === "clipboard" ? 210 : 140)}" text-anchor="middle" font-family="${sk.titleFont}" font-weight="${sk.titleFont === "Kanit" ? 900 : 400}" font-size="${o.skin === "clipboard" ? 74 : 84}" fill="${sk.titleC}">${o.title || ""}</text>
        ${o.sub ? `<text x="540" y="${Y + (o.skin === "clipboard" ? 268 : 196)}" text-anchor="middle" font-family="${sk.font}" font-size="34" fill="${sk.later}">${o.sub}</text>` : ""}
        <path d="M${540 - 200},${Y + (o.skin === "clipboard" ? 226 : 160)}Q540,${Y + (o.skin === "clipboard" ? 240 : 174)} ${540 + 200},${Y + (o.skin === "clipboard" ? 226 : 160)}" stroke="${sk.acc}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".8"/>`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-m"><g id="${id}-k"><g id="${id}-sw">${obj.back}${title}${rows}${obj.front}</g></g></g>${obj.over || ""}</g>`);
    const cuesOut = [];
    tl.set(`#${id}`, { opacity: 1 }, t0);
    const land = obj.enter(tl, t0); cue(t0, "whoosh", 0.26); cue(land, sk.sound, 0.5); cuesOut.push({ t: land, type: sk.sound });
    obj.life(tl, land + 0.4, dur - (land - t0) - 0.2);
    items.forEach((_, k) => { if (k === act || done.includes(k)) tl.fromTo(`#${id}-r${k}`, { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "power2.out", immediateRender: false }, t0 + at[k]); });
    if (act >= 0 && act < items.length) { const ta = t0 + at[act];
      tl.fromTo(`#${id}-hcr`, { attr: { width: 0 } }, { attr: { width: W - 200 }, duration: 0.55, ease: "power1.inOut", immediateRender: false }, ta + 0.2);
      if (sk.tool === "chalk" || sk.tool === "grease" || sk.tool === "pen") tl.fromTo(`#${id}-hl`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power1.inOut", immediateRender: false }, ta + 0.2);
      if (document.getElementById(`${id}-a${act}`)) { tl.fromTo(`#${id}-a${act}`, { scale: 0.2, rotation: -40, svgOrigin: "0 0" }, { scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.45, ease: "back.out(2.8)", immediateRender: false }, ta);
        tl.to(`#${id}-a${act}`, { scale: 1.12, svgOrigin: "0 0", duration: 0.4, yoyo: true, repeat: Math.max(1, Math.ceil((dur - at[act]) / 0.4)), ease: "sine.inOut" }, ta + 0.5); }
      cue(ta + 0.2, sk.hiSound, 0.26); cuesOut.push({ t: ta + 0.2, type: sk.hiSound }); }
    done.forEach((d) => { tl.fromTo(`#${id}-tk${d}`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.3, ease: "power2.out", immediateRender: false }, t0 + at[d] + 0.3); cue(t0 + at[d] + 0.3, "tap", 0.3); });
    if (o.out !== false) { tl.to(`#${id}-m`, { y: o.skin === "clipboard" || o.skin === "seatcard" ? 1300 : -1300, duration: 0.32, ease: "power2.in" }, t0 + dur - 0.32); tl.set(`#${id}`, { opacity: 0 }, t0 + dur); cue(t0 + dur - 0.32, "whoosh", 0.2); }
    return { id, cues: cuesOut };
  };

  // ---------- stock art (drawn in a ±100 box) so lanes can start fast ----------
  IconFX.ART = {
    bell: `<circle r="62" fill="#f4c430" ${O(5)}/><circle r="42" fill="#fff6c8" ${O(4)}/><path d="M-20,14Q-20,-24 0,-24Q20,-24 20,14L26,20H-26Z" fill="${INK}"/><circle cy="28" r="7" fill="${INK}"/>`,
    noTrack: `<g><rect x="-70" y="10" width="140" height="16" rx="6" fill="#c8ccd2" ${O(4)}/><rect x="-70" y="40" width="140" height="16" rx="6" fill="#c8ccd2" ${O(4)}/>${[-50, -10, 30].map((x) => `<rect x="${x}" y="0" width="24" height="64" fill="#7a5a3a" ${O(3)}/>`).join("")}
      <path d="M-30,-70L-62,-6H-34L-44,30L4,-34H-22Z" fill="#ffd84a" ${O(4)}/></g><circle r="84" fill="none" stroke="#e8382c" stroke-width="16"/><path d="M-60,-60L60,60" stroke="#e8382c" stroke-width="16" stroke-linecap="round"/>`,
    // stopwatch("2 วิ"): the number big under the hand, the unit small on its own line below (so "2วิ" never reads as "25" on a phone)
    stopwatch: (s) => { const m = String(s).match(/^\s*([\d.]+)\s*(.*)$/), n = m ? m[1] : String(s), u0 = m ? m[2] : "", u = u0 === "วิ" ? "วินาที" : u0;
      return `<circle cy="10" r="66" fill="#fdfaf2" ${O(5)}/><rect x="-12" y="-78" width="24" height="18" rx="5" fill="${INK}"/><path d="M0,0V-40" stroke="#e8382c" stroke-width="9" stroke-linecap="round"/><circle cy="0" r="8" fill="${INK}"/>
        <text y="${u ? 44 : 58}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${u ? 40 : 36}" fill="${INK}">${n}</text>${u ? `<text y="66" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="19" fill="#5a5444">${u}</text>` : ""}`; },
    gangway: `<rect x="-50" y="-70" width="100" height="140" rx="10" fill="#c8ced4" ${O(4)}/><rect x="-32" y="-52" width="64" height="66" rx="8" fill="#1a2030" ${O(3)}/><rect x="-74" y="26" width="148" height="38" rx="8" fill="#c8642c" ${O(4)}/><rect x="-62" y="-4" width="50" height="32" rx="5" fill="#2f6fd0" ${O(3)}/>`,
    log: `<rect x="-80" y="-24" width="160" height="56" rx="26" fill="#8a5a30" ${O(5)}/><ellipse cx="80" cy="4" rx="16" ry="28" fill="#d8a870" ${O(4)}/><path d="M76,-6a6,6 0 1 0 8,10" stroke="#8a5a30" stroke-width="3" fill="none"/><path d="M-60,-10h70M-40,14h80" stroke="#6a4020" stroke-width="4"/>`,
    car: `<path d="M-70,20L-56,-16Q-50,-30 -34,-30H34Q50,-30 56,-16L70,20V44H-70Z" fill="#e8382c" ${O(5)}/><path d="M-44,-14L-36,-24H36L44,-14Z" fill="#9fd8ff" ${O(3)}/><circle cx="-40" cy="46" r="16" fill="#2a2e36" ${O(4)}/><circle cx="40" cy="46" r="16" fill="#2a2e36" ${O(4)}/><circle cx="-58" cy="12" r="7" fill="#fff6c0"/><circle cx="58" cy="12" r="7" fill="#fff6c0"/>`,
    carSmall: `<g transform="translate(0,52) scale(.5)"><path d="M-70,20L-56,-16Q-50,-30 -34,-30H34Q50,-30 56,-16L70,20V44H-70Z" fill="#e8382c" ${O(6)}/><path d="M-44,-14L-36,-24H36L44,-14Z" fill="#9fd8ff" ${O(4)}/><circle cx="-40" cy="46" r="16" fill="#2a2e36" ${O(5)}/><circle cx="40" cy="46" r="16" fill="#2a2e36" ${O(5)}/><circle cx="-58" cy="12" r="8" fill="#fff6c0"/><circle cx="58" cy="12" r="8" fill="#fff6c0"/></g>`,
    buoy: `<circle r="30" fill="#ff7a2a" ${O(4)}/><circle r="14" fill="#5ab8e8" ${O(3)}/>`,
    candle: `<rect x="-18" y="-10" width="36" height="80" rx="6" fill="#fff4d8" ${O(4)}/><path d="M0,-10C-16,-34 -6,-60 0,-74C6,-60 16,-34 0,-10Z" fill="#ffb030" ${O(3)}/><path d="M0,-18C-6,-30 -2,-44 0,-52C2,-44 6,-30 0,-18Z" fill="#fff2a0"/>`,
    helmet: `<path d="M-74,20Q-74,-62 0,-62Q74,-62 74,20Z" fill="#4a5a32" ${O(5)}/><path d="M-90,20H90" stroke="${INK}" stroke-width="10" stroke-linecap="round"/><path d="M-40,-30q40,-24 80,0" stroke="#6a7a4a" stroke-width="6" fill="none"/>`,
  };
})();
