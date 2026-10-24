// Story opener for EP.1 of every new story (user rule, 24 ต.ค. 2026): the story title and "EP.1" hang in the
// sky, then the camera dives down through the clouds and lands on the first scene of the story.
// Use it on the first shot of EP.1 (any outdoor set). With o = { title, ep, name, land, at, glide, night, tint }:
//   add("open", { set: "...", setOpts, dark, cam: { keys: Opener.cam(o) },
//     extra(L, id) { Opener.extra(L, id, o); }, captions: caps("open"), fx(tl, id, t0) { Opener.fx(tl, id, t0, o); } });
// land = fr(...) framing of the first scene; at = when the dive starts (s), glide = how long it takes (s);
// rise = how far above the landing the camera starts (world px, default 2600).
(function () {
  const PAR = { sky: 0.05, far: 0.25, mid: 0.6, set: 1, fg: 1.5 };
  const f1 = (v) => Math.round(v * 10) / 10;
  const rng = (s) => () => ((s = (s * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const RISE = 2600;

  const CSS = `
    .op { position: absolute; left: 0; right: 0; top: 330px; z-index: 54; text-align: center; font-family: Kanit; pointer-events: none; }
    .op-kick { font: 700 34px/1 Kanit; letter-spacing: 14px; color: var(--op-acc); opacity: 0; text-shadow: 0 2px 10px rgba(0,0,0,.7); margin-right: -14px; }
    .op-title { position: relative; display: inline-block; margin-top: 26px; font: 900 220px/1.15 Kanit; letter-spacing: -2px; white-space: nowrap; color: #f4ecd8;
      text-shadow: 0 0 40px var(--op-glow), 0 0 90px var(--op-glow), 0 10px 0 rgba(0,0,0,.5); }
    .op-title i { display: inline-block; font-style: normal; opacity: 0; }
    .op-title .op-sheen { position: absolute; inset: 0; color: transparent; -webkit-background-clip: text; background-clip: text; text-shadow: none;
      background-image: linear-gradient(100deg, transparent 0%, transparent 40%, rgba(255,255,255,.95) 50%, transparent 60%, transparent 100%);
      background-size: 300% 100%; background-position: 120% 0; }
    .op-line { width: 640px; height: 4px; margin: 18px auto 0; border-radius: 2px; transform: scaleX(0);
      background: linear-gradient(90deg, transparent, var(--op-acc), transparent); box-shadow: 0 0 18px var(--op-acc); }
    .op-ep { display: inline-flex; align-items: center; gap: 22px; margin-top: 34px; opacity: 0; }
    .op-ep b { font: 900 64px/1 Kanit; color: #1a1410; background: var(--op-acc); padding: 12px 26px 16px; border-radius: 18px;
      box-shadow: 0 0 0 5px rgba(0,0,0,.35), 0 0 34px var(--op-glow); letter-spacing: 1px; }
    .op-ep span { font: 900 66px/1 Kanit; color: #f4ecd8; text-shadow: 0 4px 0 rgba(0,0,0,.55), 0 0 26px rgba(0,0,0,.8); white-space: nowrap; }`;
  if (typeof document !== "undefined" && !document.getElementById("op-css")) document.head.insertAdjacentHTML("beforeend", `<style id="op-css">${CSS}</style>`);

  // a soft cloud: overlapping ellipses with a moonlit (or sunlit) rim on top
  function cloud(r, cx, cy, w, h, body, rim, op) {
    let s = "", t = "";
    const n = 5 + Math.floor(r() * 4);
    for (let k = 0; k < n; k++) {
      const x = cx - w / 2 + (k + 0.5) * (w / n) + (r() - 0.5) * 30, rx = w / n * (0.8 + r() * 0.6), ry = h * (0.35 + r() * 0.45);
      const y = cy - ry * 0.35 + Math.abs(k - n / 2) * h * 0.06;
      t += `<ellipse cx="${f1(x)}" cy="${f1(y - 6)}" rx="${f1(rx)}" ry="${f1(ry)}" fill="${rim}"/>`;
      s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx)}" ry="${f1(ry)}" fill="${body}"/>`;
    }
    s += `<ellipse cx="${f1(cx)}" cy="${f1(cy + h * 0.15)}" rx="${f1(w * 0.55)}" ry="${f1(h * 0.32)}" fill="${body}"/>`;
    return `<g opacity="${op}">${t}${s}</g>`;
  }

  // the sky stack above the first scene: moon/sun and stars slide up out of frame on the way down, a sea of clouds
  // under the camera at the start, and big puffs that rush past the lens mid-dive
  function extra(L, id, o) {
    const r = rng(o.seed || 411), land = o.land, c0 = land.y - (o.rise ?? RISE), night = o.night !== false;
    const cx0 = land.x + (o.dx ?? -40);
    const at = (p, ys) => ys + c0 * p, ax = (p, xs) => xs + cx0 * p; // world point in layer p that sits at screen (xs, ys) at the top
    const body = o.cloud || (night ? "#2a3347" : "#c9d3de"), rim = o.rim || (night ? "#55648a" : "#f4f1ea");
    // stars + moon in the far layer, behind the set's own far hills
    let sky = "";
    if (night) {
      for (let k = 0; k < 160; k++) {
        const x = ax(PAR.far, -400 + r() * 1900), y = at(PAR.far, -300 + r() * 1700), big = r() < 0.12;
        sky += `<circle class="op-tw" data-i="${k % 7}" cx="${f1(x)}" cy="${f1(y)}" r="${f1(big ? 3 + r() * 2 : 1 + r() * 1.6)}" fill="${big ? "#fff7e0" : "#dfe6ff"}" opacity="${(0.35 + r() * 0.6).toFixed(2)}"/>`;
      }
      const mx = f1(ax(PAR.far, 850)), my = at(PAR.far, 190);
      sky += `<circle cx="${mx}" cy="${f1(my)}" r="330" fill="#f4ecd8" opacity=".05"/><circle cx="${mx}" cy="${f1(my)}" r="200" fill="#f4ecd8" opacity=".08"/>
        <circle cx="${mx}" cy="${f1(my)}" r="92" fill="#f4ecd8"/><circle cx="${mx + 26}" cy="${f1(my - 14)}" r="16" fill="#d9cfb6"/><circle cx="${mx - 30}" cy="${f1(my + 24)}" r="11" fill="#d9cfb6"/><circle cx="${mx + 6}" cy="${f1(my + 40)}" r="8" fill="#d9cfb6"/>`;
    } else {
      const mx = f1(ax(PAR.far, 760)), my = at(PAR.far, 360);
      sky += `<circle cx="${mx}" cy="${f1(my)}" r="380" fill="#fff1c8" opacity=".12"/><circle cx="${mx}" cy="${f1(my)}" r="120" fill="#fff6dc"/>`;
    }
    L.far.insertAdjacentHTML("afterbegin", `<g id="${id}-opsky">${sky}</g>`);
    // the sea of clouds the camera starts above (set layer: it has fully left the frame by the landing)
    let sea = "";
    for (let k = 0; k < 9; k++) sea += cloud(r, ax(PAR.set, -360 + k * 230 + r() * 60), at(PAR.set, 1560 + (k % 3) * 120 + r() * 60), 520 + r() * 200, 200 + r() * 80, body, rim, 0.92);
    for (let k = 0; k < 6; k++) sea += cloud(r, ax(PAR.set, -160 + k * 280), at(PAR.set, 1900 + r() * 200), 620, 260, body, rim, 1);
    L.set.insertAdjacentHTML("beforeend", `<g id="${id}-opsea">${sea}</g>`);
    // puffs that rush past the lens mid-dive (fg layer, blurred by the engine)
    const cm = c0 + (land.y - c0) * 0.4;
    let fg = "";
    [[-60, -300, 900], [1150, 60, 980], [420, 420, 1100], [140, 760, 900], [980, 1000, 900]].forEach(([x, dy, w]) =>
      (fg += cloud(r, x + cx0 * PAR.fg, 960 + dy + cm * PAR.fg, w, w * 0.42, body, rim, 0.95)));
    L.fg.insertAdjacentHTML("beforeend", `<g id="${id}-oppuff">${fg}</g>`);
    // a few thin clouds drifting across the moon (far layer, in front of the stars)
    let thin = "";
    for (let k = 0; k < 4; k++) thin += cloud(r, ax(PAR.far, 140 + k * 300), at(PAR.far, 240 + k * 170), 460, 70, body, rim, 0.55);
    L.far.insertAdjacentHTML("beforeend", `<g id="${id}-opthin">${thin}</g>`);
  }

  // camera: hold high over the landing (a slow float), then an eased dive into the landing framing
  function cam(o) {
    const land = o.land, rise = o.rise ?? RISE, at = o.at ?? 1.6, glide = o.glide ?? 1.9;
    return [
      { t: 0, x: land.x + (o.dx ?? -40), y: land.y - rise, s: o.s0 ?? land.s * 0.9, drift: { x: 14, y: 30, s: 0.012 } },
      { t: at + glide, glide, ...land, drift: land.drift || { s: 0.02 } },
    ];
  }

  // title card in screen space + the timing of the dive (whiteout as the camera passes through the cloud)
  function fx(tl, id, t0, o) {
    const at = o.at ?? 1.6, glide = o.glide ?? 1.9, acc = o.tint || "#f2c55c", glow = o.glow || "rgba(242,197,92,.45)";
    const seg = typeof Intl !== "undefined" && Intl.Segmenter ? [...new Intl.Segmenter("th", { granularity: "grapheme" }).segment(o.title)].map((g) => g.segment) : [...o.title];
    const clip = document.getElementById(id);
    clip.insertAdjacentHTML("beforeend", `<div class="op" id="${id}-op" style="--op-acc:${acc};--op-glow:${glow}">
      ${o.kick ? `<div class="op-kick">${o.kick}</div>` : ""}
      <div class="op-title">${seg.map((g) => `<i>${g}</i>`).join("")}<span class="op-sheen">${o.title}</span></div>
      <div class="op-line"></div>
      <div class="op-ep"><b>${o.ep || "EP.1"}</b>${o.name ? `<span>${o.name}</span>` : ""}</div></div>`);
    const q = (s) => `#${id}-op ${s}`;
    // in: kicker, letters rise out of a blur one by one, the line draws out, a light sweeps the title, the EP plate pops
    if (o.kick) tl.fromTo(q(".op-kick"), { opacity: 0, letterSpacing: "30px" }, { opacity: 0.95, letterSpacing: "14px", duration: 0.6, ease: "power2.out", immediateRender: false }, t0 + 0.05);
    tl.fromTo(q(".op-title i"), { opacity: 0, y: 60, filter: "blur(14px)", scale: 1.25 },
      { opacity: 1, y: 0, filter: "blur(0px)", scale: 1, duration: 0.5, ease: "power3.out", stagger: 0.07, immediateRender: false }, t0 + 0.12);
    tl.fromTo(q(".op-line"), { scaleX: 0 }, { scaleX: 1, duration: 0.55, ease: "power2.inOut", immediateRender: false }, t0 + 0.45);
    tl.fromTo(q(".op-sheen"), { backgroundPosition: "120% 0" }, { backgroundPosition: "-20% 0", duration: 0.9, ease: "power1.inOut", immediateRender: false }, t0 + 0.7);
    tl.fromTo(q(".op-ep"), { opacity: 0, y: 30, scale: 0.7 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2.2)", immediateRender: false }, t0 + 0.75);
    // out: the title is left behind in the sky as the camera drops (rises, grows, blurs away)
    tl.to(`#${id}-op`, { y: -560, scale: 1.18, opacity: 0, filter: "blur(10px)", duration: glide * 0.6, ease: "power2.in" }, t0 + at);
    // stars twinkle
    for (let i = 0; i < 7; i++) tl.fromTo(`#${id}-opsky .op-tw[data-i="${i}"]`, { opacity: 0.9 }, { opacity: 0.25, duration: 0.45 + i * 0.09, repeat: Math.ceil((at + glide) / (0.45 + i * 0.09)), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.07);
    // thin clouds drift across the moon
    tl.fromTo(`#${id}-opthin`, { x: 0 }, { x: -160, duration: at + glide, ease: "none", immediateRender: false }, t0);
    // whiteout through the cloud deck (screen-space fog rect of the engine)
    const fog = document.getElementById(`${id}-fog`);
    fog.setAttribute("fill", o.cloud || (o.night === false ? "#dfe5ec" : "#3a465e"));
    tl.fromTo(fog, { opacity: 0 }, { opacity: 0.88, duration: glide * 0.22, ease: "power1.in", immediateRender: false }, t0 + at + glide * 0.36);
    tl.to(fog, { opacity: 0, duration: glide * 0.34, ease: "power1.out" }, t0 + at + glide * 0.58);
    // the clouds have gone by the landing
    tl.to([`#${id}-opsea`, `#${id}-oppuff`], { opacity: 0, duration: 0.35, ease: "power1.in" }, t0 + at + glide - 0.4);
  }

  window.Opener = { extra, cam, fx, CSS };
})();
