// Story opener for EP.1 of every new story (user rule, 24 ต.ค. 2026): the story title and "EP.1" hang in the
// night sky, then the camera dives down through the clouds and lands on the first scene of the story.
// The user asked for it scary and suspenseful: the title flickers in like a dying neon sign and glitches, a cloud
// swallows the moon, pale eyes open one by one in the sea of clouds, a hand rises out of it and waves, then the
// camera drops faster and faster (shake, speed lines), a face flashes inside the cloud, and the landing hits hard.
// Usage on the first shot of EP.1 (any outdoor set), with o = { title, ep, name, kick, land, at, glide }:
//   add("open", { set: "...", setOpts, dark, cam: { keys: Opener.cam(o) }, shake: Opener.shake(o),
//     extra(L, id) { Opener.extra(L, id, o); }, captions: caps("open"), fx(tl, id, t0) { Opener.fx(tl, id, t0, o); } });
// land = fr(...) framing of the first scene; at = when the dive starts (s); glide = how long the fall takes (s);
// rise = how far above the landing the camera starts (world px, default 2600); hand:false / eyes:0 to leave them out.
// mix.py: *[(k, t, typ, g) for k, t, typ, g in OPENER_CUES] with the cue list from Opener.cues (copied by hand).
(function () {
  const PAR = { sky: 0.05, far: 0.25, mid: 0.6, set: 1, fg: 1.5 };
  const f1 = (v) => Math.round(v * 10) / 10;
  const rng = (s) => () => ((s = (s * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const RISE = 2600, INK = "#14100e";
  const AT = (o) => o.at ?? 1.9, GL = (o) => o.glide ?? 1.8;

  const FONT = "font: 900 230px/1.15 Kanit; letter-spacing: -2px; white-space: nowrap;";
  const CSS = `
    .op { position: absolute; left: 0; right: 0; top: 300px; z-index: 54; text-align: center; font-family: Kanit; pointer-events: none; }
    .op-kick { font: 700 32px/1 Kanit; letter-spacing: 14px; margin-right: -14px; color: #b8a69c; opacity: 0; text-shadow: 0 2px 10px #000; }
    .op-tw { position: relative; display: inline-block; margin-top: 22px; }
    .op-title { ${FONT} color: #ece4d8; text-shadow: 0 0 22px rgba(214,34,26,.85), 0 0 70px rgba(150,10,10,.75), 0 10px 0 rgba(0,0,0,.6); }
    .op-title i { display: inline-block; font-style: normal; opacity: 0; }
    .op-r, .op-c, .op-sl { position: absolute; left: 0; top: 0; ${FONT} opacity: 0; }
    .op-r { color: rgba(255,34,44,.9); mix-blend-mode: screen; } .op-c { color: rgba(40,226,255,.8); mix-blend-mode: screen; }
    .op-sl { color: #f4ecd8; clip-path: inset(44% 0 36% 0); text-shadow: 0 0 20px rgba(214,34,26,.9); }
    .op-drip { position: absolute; top: 78%; width: 12px; border-radius: 0 0 8px 8px; background: linear-gradient(#7d0f0c, #b3261e); transform: scaleY(0); transform-origin: 50% 0; box-shadow: 0 0 10px rgba(180,20,20,.6); }
    .op-drip::after { content: ""; position: absolute; left: -4px; bottom: -10px; width: 20px; height: 20px; border-radius: 50%; background: #b3261e; }
    .op-line { width: 620px; height: 4px; margin: 14px auto 0; border-radius: 2px; transform: scaleX(0);
      background: linear-gradient(90deg, transparent, #c8392b, transparent); box-shadow: 0 0 18px #c8392b; }
    .op-ep { display: inline-flex; align-items: center; gap: 22px; margin-top: 30px; opacity: 0; }
    .op-ep b { font: 900 64px/1 Kanit; color: #fff4ea; background: #b3261e; padding: 12px 26px 16px; border-radius: 16px; letter-spacing: 1px;
      box-shadow: 0 0 0 5px rgba(0,0,0,.45), 0 0 34px rgba(210,30,24,.75); }
    .op-ep span { font: 900 66px/1 Kanit; color: #ece4d8; text-shadow: 0 4px 0 rgba(0,0,0,.6), 0 0 22px rgba(0,0,0,.9); white-space: nowrap; }`;
  if (typeof document !== "undefined" && !document.getElementById("op-css")) document.head.insertAdjacentHTML("beforeend", `<style id="op-css">${CSS}</style>`);

  // a soft cloud: overlapping ellipses with a moonlit rim on top
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
  // a pair of pale eyes in the cloud, shut (scaleY ~0) until fx opens them
  const eyePair = (id, x, y, s) => `<g id="${id}" transform="translate(${f1(x)},${f1(y)}) scale(${s},0.02)">
      ${[-38, 38].map((dx) => `<ellipse cx="${dx}" cy="0" rx="50" ry="30" fill="#efe6c4" opacity=".3"/><ellipse cx="${dx}" cy="0" rx="23" ry="13" fill="#f6efd6"/><circle cx="${dx + 3}" cy="1" r="6" fill="${INK}"/>`).join("")}</g>`;
  // a thin pale arm and hand, rising out of the clouds (pivot at the bottom of the arm)
  const handUp = (id, x, y) => `<g id="${id}" transform="translate(${f1(x)},${f1(y + 380)}) rotate(0)">
      <path d="M-22,0C-24,-120 -20,-220 -16,-300L16,-300C20,-220 24,-120 22,0Z" fill="#bfc8c3" stroke="${INK}" stroke-width="5"/>
      <path d="M-30,-296C-36,-340 -30,-372 -4,-378C22,-380 34,-352 30,-300Z" fill="#c9d1cc" stroke="${INK}" stroke-width="5"/>
      ${[[-24, -360, -34, -452], [-8, -374, -12, -478], [8, -374, 10, -476], [22, -362, 32, -446]].map(([a, b, c, d]) =>
        `<path d="M${a},${b}Q${(a + c) / 2 - 4},${(b + d) / 2} ${c},${d}" stroke="${INK}" stroke-width="15" stroke-linecap="round" fill="none"/><path d="M${a},${b}Q${(a + c) / 2 - 4},${(b + d) / 2} ${c},${d}" stroke="#c9d1cc" stroke-width="7" stroke-linecap="round" fill="none"/>`).join("")}
      <path d="M-28,-318Q-58,-336 -66,-372" stroke="${INK}" stroke-width="15" stroke-linecap="round" fill="none"/><path d="M-28,-318Q-58,-336 -66,-372" stroke="#c9d1cc" stroke-width="7" stroke-linecap="round" fill="none"/>
      <path d="M-10,-150q8,6 0,14M6,-230q-8,6 0,14" stroke="#8e9893" stroke-width="3" fill="none"/></g>`;
  // the face that flashes for two frames inside the cloud (screen space, above the whiteout)
  const FACE = `<g transform="translate(540,900)">
      <path d="M-300,-420C-360,-100 -330,260 -250,520L250,520C330,260 360,-100 300,-420C200,-560 -200,-560 -300,-420Z" fill="${INK}" opacity=".85"/>
      <ellipse cx="0" cy="0" rx="230" ry="320" fill="#d6dcd6"/><ellipse cx="0" cy="40" rx="230" ry="280" fill="#c2cac5" opacity=".5"/>
      <ellipse cx="-88" cy="-40" rx="56" ry="70" fill="${INK}"/><ellipse cx="88" cy="-40" rx="56" ry="70" fill="${INK}"/>
      <circle cx="-80" cy="-34" r="8" fill="#f3ecd2"/><circle cx="96" cy="-34" r="8" fill="#f3ecd2"/>
      <path d="M-46,150C-40,110 40,110 46,150C50,230 30,300 0,306C-30,300 -50,230 -46,150Z" fill="${INK}"/>
      <path d="M-300,-420C-240,-200 -230,0 -250,300M300,-420C240,-200 230,0 250,300M-120,-330C-150,-150 -170,40 -190,200M130,-330C160,-150 175,40 196,210" stroke="${INK}" stroke-width="22" fill="none" opacity=".9"/></g>`;

  // the sky stack above the first scene: moon and stars slide up out of frame on the way down; a sea of clouds
  // under the camera at the start (eyes and the hand live in it); big puffs that rush past the lens mid-dive
  function extra(L, id, o) {
    const r = rng(o.seed || 411), land = o.land, c0 = land.y - (o.rise ?? RISE);
    const cx0 = land.x + (o.dx ?? -40);
    const at = (p, ys) => ys + c0 * p, ax = (p, xs) => xs + cx0 * p; // world point in layer p that sits at screen (xs, ys) at the top
    const body = o.cloud || "#1c2230", rim = o.rim || "#3a4258";
    let sky = "";
    for (let k = 0; k < 120; k++) {
      const x = ax(PAR.far, -400 + r() * 1900), y = at(PAR.far, -300 + r() * 1700), big = r() < 0.1;
      sky += `<circle class="op-tw" data-i="${k % 7}" cx="${f1(x)}" cy="${f1(y)}" r="${f1(big ? 2.6 + r() * 1.6 : 1 + r() * 1.4)}" fill="#dfe2ee" opacity="${(0.25 + r() * 0.5).toFixed(2)}"/>`;
    }
    const mx = f1(ax(PAR.far, 850)), my = f1(at(PAR.far, 190));
    sky += `<g id="${id}-opmoon"><circle cx="${mx}" cy="${my}" r="340" fill="#b4281e" opacity=".07"/><circle cx="${mx}" cy="${my}" r="200" fill="#c9a89a" opacity=".1"/>
      <circle cx="${mx}" cy="${my}" r="92" fill="#e6dccb"/><circle cx="${mx + 26}" cy="${my - 14}" r="16" fill="#cbbfa8"/><circle cx="${mx - 30}" cy="${my + 24}" r="11" fill="#cbbfa8"/><circle cx="${mx + 6}" cy="${my + 40}" r="8" fill="#cbbfa8"/></g>`;
    L.far.insertAdjacentHTML("afterbegin", `<g id="${id}-opsky">${sky}</g>`);
    // the cloud that swallows the moon
    L.far.insertAdjacentHTML("beforeend", `<g id="${id}-opveil" transform="translate(0,0)">${cloud(r, ax(PAR.far, 1180), at(PAR.far, 200), 560, 170, body, rim, 1)}${cloud(r, ax(PAR.far, 1300), at(PAR.far, 290), 420, 120, body, rim, 0.9)}</g>`);
    // the sea of clouds: a back row, the eyes and the hand, a front row (set layer, gone by the landing)
    let back = "", front = "", mid = "";
    for (let k = 0; k < 9; k++) back += cloud(r, ax(PAR.set, -360 + k * 230 + r() * 60), at(PAR.set, 1540 + (k % 3) * 70 + r() * 50), 520 + r() * 200, 200 + r() * 80, body, rim, 0.95);
    for (let k = 0; k < 6; k++) front += cloud(r, ax(PAR.set, -160 + k * 280), at(PAR.set, 1860 + r() * 140), 620, 260, body, rim, 1);
    const EY = [[150, 1600, 0.9], [330, 1690, 1.15], [540, 1610, 0.8], [700, 1720, 1.25], [930, 1630, 0.95], [80, 1760, 1.2], [440, 1790, 1.3], [810, 1560, 0.7], [620, 1840, 1.4]];
    EY.slice(0, o.eyes ?? EY.length).forEach(([x, y, s], k) => (mid += eyePair(`${id}-ope${k}`, ax(PAR.set, x), at(PAR.set, y), s)));
    if (o.hand !== false) mid += handUp(`${id}-ophand`, ax(PAR.set, 900), at(PAR.set, 1700));
    L.set.insertAdjacentHTML("beforeend", `<g id="${id}-opsea">${back}${mid}${front}</g>`);
    // puffs that rush past the lens mid-dive (fg layer, blurred by the engine)
    const cm = c0 + (land.y - c0) * 0.4;
    let fg = "";
    [[-60, -300, 900], [1150, 60, 980], [420, 420, 1100], [140, 760, 900], [980, 1000, 900]].forEach(([x, dy, w]) =>
      (fg += cloud(r, x + cx0 * PAR.fg, 960 + dy + cm * PAR.fg, w, w * 0.42, body, rim, 0.95)));
    L.fg.insertAdjacentHTML("beforeend", `<g id="${id}-oppuff">${fg}</g>`);
    // the face, above the engine's whiteout rect
    document.getElementById(`${id}-fog`).insertAdjacentHTML("afterend", `<g id="${id}-opface" opacity="0">${FACE}</g>`);
  }

  // camera: hold high over the landing (a slow creeping push), then a fall that keeps speeding up into the landing
  function cam(o) {
    const land = o.land, rise = o.rise ?? RISE, at = AT(o), glide = GL(o);
    return [
      { t: 0, x: land.x + (o.dx ?? -40), y: land.y - rise, s: o.s0 ?? land.s * 0.9, drift: { x: 10, y: 24, s: 0.02 } },
      { t: at + glide, glide, ease: "drop", ...land, drift: land.drift || { s: 0.02 } },
    ];
  }
  // shake: a shiver when the eyes open, a rising rattle through the fall, a hard hit on the landing
  function shake(o) {
    const at = AT(o), land = at + GL(o);
    return (t) => {
      let a = 0;
      if (t > 1.1 && t < at) a = 1.2;
      if (t >= at && t < land) a = 2 + 12 * Math.pow((t - at) / (land - at), 1.5);
      if (t >= land) a = 26 * Math.exp(-(t - land) * 7);
      return a * (Math.sin(t * 41) + 0.6 * Math.sin(t * 67 + 1));
    };
  }

  function fx(tl, id, t0, o) {
    const at = AT(o), glide = GL(o), land = at + glide, r = rng(o.seed || 977);
    const seg = typeof Intl !== "undefined" && Intl.Segmenter ? [...new Intl.Segmenter("th", { granularity: "grapheme" }).segment(o.title)].map((g) => g.segment) : [...o.title];
    const clip = document.getElementById(id);
    const drips = [0.18, 0.41, 0.63, 0.84].map((x, k) => `<i class="op-drip" style="left:${Math.round(x * 100)}%;height:${[70, 120, 54, 96][k]}px"></i>`).join("");
    clip.insertAdjacentHTML("beforeend", `<div class="op" id="${id}-op">
      ${o.kick ? `<div class="op-kick">${o.kick}</div>` : ""}
      <div class="op-tw"><div class="op-title">${seg.map((g) => `<i>${g}</i>`).join("")}</div>
        <div class="op-r">${o.title}</div><div class="op-c">${o.title}</div><div class="op-sl">${o.title}</div>${drips}</div>
      <div class="op-line"></div>
      <div class="op-ep"><b>${o.ep || "EP.1"}</b>${o.name ? `<span>${o.name}</span>` : ""}</div></div>`);
    const q = (s) => `#${id}-op ${s}`, A = (t) => t0 + t;
    if (o.kick) tl.fromTo(q(".op-kick"), { opacity: 0 }, { opacity: 0.9, duration: 0.5, immediateRender: false }, A(0.05));
    // letters stutter on like a dying neon sign
    clip.querySelectorAll(`#${id}-op .op-title i`).forEach((el, k) => {
      let t = 0.15 + k * 0.09;
      [1, 0.1, 1, 0, 0.6, 1].forEach((v, j) => { tl.set(el, { opacity: v }, A(t)); t += 0.03 + r() * 0.05 + (j === 3 ? 0.06 : 0); });
    });
    // glitch bursts: RGB split, a sliced band thrown sideways
    const burst = (t, dur, amp) => {
      for (let u = 0; u < dur; u += 1 / 30) {
        const d = Math.round((r() - 0.5) * amp);
        tl.set(q(".op-r"), { opacity: 0.85, x: d + amp * 0.3, y: Math.round((r() - 0.5) * 6) }, A(t + u));
        tl.set(q(".op-c"), { opacity: 0.8, x: -d - amp * 0.3 }, A(t + u));
        tl.set(q(".op-sl"), { opacity: r() < 0.7 ? 1 : 0, x: Math.round((r() - 0.5) * amp * 3) }, A(t + u));
      }
      tl.set([q(".op-r"), q(".op-c"), q(".op-sl")], { opacity: 0, x: 0, y: 0 }, A(t + dur));
    };
    [[0.55, 0.12, 14], [1.18, 0.18, 22], [1.62, 0.1, 16], [at - 0.12, 0.2, 30]].forEach(([t, d, a]) => burst(t, d, a));
    // a constant small tremble of the title while it hangs there
    for (let t = 0.2; t < at; t += 1 / 15) tl.set(q(".op-tw"), { x: Math.round((r() - 0.5) * 4), y: Math.round((r() - 0.5) * 3) }, A(t));
    tl.fromTo(q(".op-line"), { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power2.inOut", immediateRender: false }, A(0.5));
    // the EP plate stamps down, the title starts to bleed
    tl.fromTo(q(".op-ep"), { opacity: 0, scale: 1.9 }, { opacity: 1, scale: 1, duration: 0.14, ease: "power4.in", immediateRender: false }, A(0.82));
    tl.fromTo(q(".op-ep"), { x: 0 }, { x: 8, duration: 0.04, repeat: 5, yoyo: true, immediateRender: false }, A(0.96));
    clip.querySelectorAll(`#${id}-op .op-drip`).forEach((el, k) =>
      tl.fromTo(el, { scaleY: 0 }, { scaleY: 1, duration: 0.9 + k * 0.25, ease: "power1.in", immediateRender: false }, A(1.0 + k * 0.17)));
    // a cloud swallows the moon and the night gets darker
    tl.fromTo(`#${id}-opveil`, { attr: { transform: "translate(0,0)" } }, { attr: { transform: "translate(-360,0)" }, duration: 0.9, ease: "power1.inOut", immediateRender: false }, A(0.7));
    tl.to(`#${id}-opmoon`, { opacity: 0.35, duration: 0.5 }, A(1.05));
    const dk = document.getElementById(`${id}-dark`), d0 = +dk.getAttribute("opacity");
    tl.fromTo(dk, { opacity: d0 }, { opacity: Math.min(0.9, d0 + 0.2), duration: 0.5, immediateRender: false }, A(1.05));
    tl.to(dk, { opacity: d0, duration: 0.6 }, A(land - 0.3));
    // eyes open in the clouds, one after another; they all blink as the camera tips over
    [2, 5, 0, 7, 3, 8, 1, 4, 6].forEach((k, n) => {
      const el = document.getElementById(`${id}-ope${k}`);
      if (!el) return;
      const tr = el.getAttribute("transform"), open = tr.replace(/scale\(([^,]+),[^)]+\)/, "scale($1,1)");
      tl.fromTo(el, { attr: { transform: tr } }, { attr: { transform: open }, duration: 0.12, ease: "back.out(3)", immediateRender: false }, A(1.15 + n * 0.08));
      tl.to(el, { attr: { transform: tr }, duration: 0.06 }, A(at - 0.3));
      tl.to(el, { attr: { transform: open }, duration: 0.08 }, A(at - 0.18));
    });
    // a hand rises out of the clouds and waves you down
    const hd = document.getElementById(`${id}-ophand`);
    if (hd) {
      const m = hd.getAttribute("transform").match(/translate\(([-\d.]+),([-\d.]+)\)/), hx = +m[1], hy = +m[2] - 380;
      const H = (y, a) => `translate(${hx},${f1(y)}) rotate(${a})`;
      const top = hy + 190; // the elbow stays inside the front row of clouds
      tl.fromTo(hd, { attr: { transform: H(hy + 380, 0) } }, { attr: { transform: H(top, -4) }, duration: 0.7, ease: "power2.out", immediateRender: false }, A(1.3));
      for (let k = 0, t = 2.0; t < at + 0.2; k++, t += 0.32) tl.to(hd, { attr: { transform: H(top, k % 2 ? -12 : 10) }, duration: 0.32, ease: "sine.inOut" }, A(t));
    }
    // stars twinkle
    for (let i = 0; i < 7; i++) tl.fromTo(`#${id}-opsky .op-tw[data-i="${i}"]`, { opacity: 0.9 }, { opacity: 0.2, duration: 0.45 + i * 0.09, repeat: Math.ceil(land / (0.45 + i * 0.09)), yoyo: true, ease: "sine.inOut", immediateRender: false }, A(i * 0.07));
    // the drop: the title is left behind, speed lines, a heartbeat vignette while the eyes watch
    tl.to(`#${id}-op`, { y: -620, scale: 1.2, opacity: 0, filter: "blur(10px)", duration: glide * 0.55, ease: "power2.in" }, A(at));
    if (window.Fx) { Fx.speed(tl, A(at + 0.25), A(land - 0.1)); Fx.heart(tl, A(1.15), at - 1.15, 0.5, 0.5); }
    // through the cloud: whiteout, and a face for two frames in the middle of it
    const fog = document.getElementById(`${id}-fog`);
    fog.setAttribute("fill", o.cloud ? o.cloud : "#2b3242");
    tl.fromTo(fog, { opacity: 0 }, { opacity: 0.9, duration: glide * 0.2, ease: "power1.in", immediateRender: false }, A(at + glide * 0.38));
    tl.to(fog, { opacity: 0, duration: glide * 0.3, ease: "power1.out" }, A(at + glide * 0.62));
    const fT = at + glide * 0.52;
    tl.set(`#${id}-opface`, { opacity: 0.7 }, A(fT)); tl.set(`#${id}-opface`, { opacity: 0 }, A(fT + 0.07));
    tl.set(`#${id}-opface`, { opacity: 0.4 }, A(fT + 0.14)); tl.set(`#${id}-opface`, { opacity: 0 }, A(fT + 0.18));
    tl.to([`#${id}-opsea`, `#${id}-oppuff`], { opacity: 0, duration: 0.3, ease: "power1.in" }, A(land - 0.35));
    // the landing hits: a red pulse and a glitch
    if (window.Fx) Fx.glitch(tl, `#${id}`, A(land), 0.16, 14, 5);
    tl.fromTo("#fxred", { opacity: 0.85 }, { opacity: 0, duration: 0.6, ease: "power2.out", immediateRender: false }, A(land));
  }

  // sound cues in mix.py format (shot key, seconds into the shot, sfx type, gain); at/glide as in the shot
  const cues = (k, o) => {
    const at = AT(o), gl = GL(o), land = at + gl;
    return [[k, 0.0, "swell", 0.6], [k, 0.55, "glitch", 0.35], [k, 0.82, "boom", 0.45], [k, 1.15, "sting", 0.5], [k, 1.18, "glitch", 0.45],
      [k, at - 0.9, "riser", 0.7], [k, at - 0.12, "glitch", 0.5], [k, at, "whoosh", 0.9], [k, at + gl * 0.45, "whoosh", 0.8],
      [k, at + gl * 0.52, "sting", 0.9], [k, land - 0.02, "boom", 0.9], [k, land, "glitch", 0.5]];
  };

  window.Opener = { extra, cam, shake, fx, cues, CSS };
})();
