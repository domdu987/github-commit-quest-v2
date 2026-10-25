// Story openers with their own scene (user, 25 ต.ค. 2026: "ฉากเป็นแต่ละเรื่อง ep1 ห้ามเหมือนกันนะ" — every story's EP.1 opening
// must look different). opener.js stays the sky-and-clouds opener of หมอกลง; each later story gets a variant built from its own world:
//   OpenerSmoke  ควันหลง: we start inside the burning window; the title burns in the smoke like embers; a charred hand slams
//                onto the lens; the smoke blows out and the camera pulls back to the dorm on fire
//   OpenerWater  มือพราย: we start looking down at the black river; the title surfaces through the ripples; pale hands come up
//                out of the water and drag the letters under; the camera tilts up to the river of krathongs
// Same call shape as Opener: add("open", { set, setOpts, dark, cam: { keys: V.cam(o) }, shake: V.shake(o),
//   extra(L, id) { V.extra(L, id, o); }, captions: caps("open"), fx(tl, id, t0) { V.fx(tl, id, t0, o); } }) with
//   o = { title, ep, name, kick, land, at, glide, start } (start = fr(...) of the first framing). mix.py cues: V.cues(k, o).
(function () {
  const f1 = (v) => Math.round(v * 10) / 10;
  const rng = (s) => () => ((s = (s * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const AT = (o) => o.at ?? 1.9, GL = (o) => o.glide ?? 1.8;
  const FONT = "font: 900 230px/1.15 Kanit; letter-spacing: -2px; white-space: nowrap;";
  const CSS = `
    .op2 { position: absolute; left: 0; right: 0; top: 330px; z-index: 54; text-align: center; font-family: Kanit; pointer-events: none; }
    .op2 .k { font: 700 32px/1 Kanit; letter-spacing: 14px; margin-right: -14px; opacity: 0; text-shadow: 0 2px 10px #000; }
    .op2 .tw { position: relative; display: inline-block; margin-top: 20px; }
    .op2 .t { ${FONT} }
    .op2 .t i { display: inline-block; font-style: normal; opacity: 0; }
    .op2 .ep { display: inline-flex; align-items: center; gap: 22px; margin-top: 30px; opacity: 0; }
    .op2 .ep b { font: 900 64px/1 Kanit; padding: 12px 26px 16px; border-radius: 16px; box-shadow: 0 0 0 5px rgba(0,0,0,.45); }
    .op2 .ep span { font: 900 66px/1 Kanit; color: #ece4d8; text-shadow: 0 4px 0 rgba(0,0,0,.6), 0 0 22px rgba(0,0,0,.9); white-space: nowrap; }
    .op2.ember .k { color: #e8b48a; }
    .op2.ember .t { color: #ffe2b0; text-shadow: 0 0 16px #ff8a2a, 0 0 46px #d8401a, 0 0 90px rgba(200,40,20,.7), 0 10px 0 rgba(0,0,0,.6); }
    .op2.ember .ep b { color: #2a1006; background: linear-gradient(#ffb04a, #e8601c); box-shadow: 0 0 0 5px rgba(0,0,0,.45), 0 0 34px rgba(255,120,30,.8); }
    .op2.ember .spk { position: absolute; width: 10px; height: 10px; border-radius: 50%; background: #ffcf6a; box-shadow: 0 0 12px #ff7a1a; opacity: 0; }
    .op2.water .k { color: #a8d8d0; }
    .op2.water .t { color: #dff4ef; text-shadow: 0 0 18px rgba(110,220,205,.7), 0 0 60px rgba(40,120,120,.6), 0 10px 0 rgba(0,0,0,.6); filter: url(#opRipple); }
    .op2.water .ep b { color: #06201e; background: linear-gradient(#bff0e6, #5fb8aa); box-shadow: 0 0 0 5px rgba(0,0,0,.45), 0 0 34px rgba(110,220,205,.6); }
    .op2.water .drop { position: absolute; width: 12px; height: 18px; border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%; background: #bfe6e0; opacity: 0; }`;
  if (typeof document !== "undefined" && !document.getElementById("op2-css")) document.head.insertAdjacentHTML("beforeend", `<style id="op2-css">${CSS}</style>`);
  // the ripple filter for the water title (added once the page body exists)
  const ripple = () => { if (!document.getElementById("opRipple")) document.body.insertAdjacentHTML("afterbegin", `<svg width="0" height="0" style="position:absolute"><filter id="opRipple" x="-10%" y="-30%" width="120%" height="160%">
      <feTurbulence id="opRippleT" type="fractalNoise" baseFrequency="0.012 0.06" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="18" xChannelSelector="R" yChannelSelector="G"/></filter></svg>`); };
  const graphemes = (s) => (typeof Intl !== "undefined" && Intl.Segmenter ? [...new Intl.Segmenter("th", { granularity: "grapheme" }).segment(s)].map((g) => g.segment) : [...s]);
  // the title block (kick line, the title letter by letter, the EP plate) in one style
  function title(id, o, style) {
    const clip = document.getElementById(id);
    clip.insertAdjacentHTML("beforeend", `<div class="op2 ${style}" id="${id}-op2">${o.kick ? `<div class="k">${o.kick}</div>` : ""}
      <div class="tw"><div class="t">${graphemes(o.title).map((g) => `<i>${g}</i>`).join("")}</div></div>
      <div class="ep"><b>${o.ep || "EP.1"}</b>${o.name ? `<span>${o.name}</span>` : ""}</div></div>`);
    return clip;
  }
  const camKeys = (o) => [
    { t: 0, ...o.start, drift: o.start.drift || { s: 0.04 } },
    { t: AT(o) + GL(o), glide: GL(o), ease: o.ease || "power2.inOut", ...o.land, drift: o.land.drift || { s: 0.02 } },
  ];

  // ================= ควันหลง: smoke, embers, a burnt hand on the lens =================
  const OpenerSmoke = {
    cam: camKeys,
    shake(o) {
      const at = AT(o), land = at + GL(o), slam = o.slam ?? 1.25;
      return (t) => {
        let a = 1.2 + Math.sin(t * 3) * 0.8;
        if (t > slam && t < slam + 0.5) a += 22 * (slam + 0.5 - t) / 0.5;
        if (t >= at && t < land) a += 3;
        if (t >= land) a = 20 * Math.exp(-(t - land) * 7);
        return a * (Math.sin(t * 37) + 0.6 * Math.sin(t * 61 + 1));
      };
    },
    extra(L, id, o) {
      const r = rng(o.seed || 523);
      // screen-space smoke wall (thick, dark brown, lit orange from below), embers, the charred hand print
      let smk = "";
      for (let k = 0; k < 16; k++) {
        const x = -200 + r() * 1480, y = -100 + r() * 2100, rx = 380 + r() * 380, ry = rx * (0.6 + r() * 0.2);
        smk += `<ellipse class="osm" data-dx="${f1((x - 540) * 1.6)}" data-dy="${f1((y - 960) * 1.4)}" cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx)}" ry="${f1(ry)}" fill="url(#op2Smoke)" opacity="${(0.75 + r() * 0.25).toFixed(2)}"/>`;
      }
      let emb = "";
      for (let k = 0; k < 40; k++) emb += `<circle class="oem" data-i="${k}" cx="${f1(r() * 1080)}" cy="${f1(900 + r() * 1100)}" r="${f1(2 + r() * 5)}" fill="${r() < 0.5 ? "#ffcf6a" : "#ff7a2a"}"/>`;
      const hand = `<g id="${id}-ohand" opacity="0" transform="translate(560,1060)"><circle r="420" fill="url(#op2Under)" opacity=".9"/><g fill="#160d08" stroke="#ff8a3a" stroke-width="7" stroke-opacity=".75">
          <path d="M-120,40C-140,-60 -110,-140 -40,-150C40,-160 110,-120 120,-40C130,40 90,140 0,160C-80,170 -110,120 -120,40Z"/>
          ${[[-110, -100, -170, -330, 34], [-50, -140, -70, -420, 38], [20, -150, 30, -430, 38], [80, -120, 120, -380, 34], [120, 0, 240, -110, 32]].map(([a, b, c, d, w]) => `<path d="M${a},${b}L${c},${d}" stroke="#ff8a3a" stroke-opacity=".75" stroke-width="${w * 2 + 14}" stroke-linecap="round"/><path d="M${a},${b}L${c},${d}" stroke="#160d08" stroke-width="${w * 2}" stroke-linecap="round"/>`).join("")}
          <path d="M-120,40C-140,-60 -110,-140 -40,-150C40,-160 110,-120 120,-40C130,40 90,140 0,160C-80,170 -110,120 -120,40Z" stroke="none"/></g>
          <g stroke="#ffb04a" stroke-width="7" fill="none" opacity="1"><path d="M-80,-40l40,30l30,-26l46,40"/><path d="M-60,80l50,-20l40,30"/><path d="M-60,-200l10,60M24,-260l-6,90M96,-230l-14,80"/></g>
          ${[[-70, 190], [-20, 230], [40, 200], [90, 250]].map(([x, l]) => `<path d="M${x},140v${l - 120}" stroke="#160d08" stroke-width="14" stroke-linecap="round" opacity=".7"/>`).join("")}</g>`;
      L.light.insertAdjacentHTML("beforeend", `<defs><radialGradient id="op2Smoke"><stop offset="0" stop-color="#2a1d16"/><stop offset=".55" stop-color="#1c1410" stop-opacity=".95"/><stop offset="1" stop-color="#120c09" stop-opacity="0"/></radialGradient>
        <radialGradient id="op2Under" cx=".5" cy="1"><stop offset="0" stop-color="#ff6a1a" stop-opacity=".55"/><stop offset="1" stop-color="#ff6a1a" stop-opacity="0"/></radialGradient></defs>
        <g id="${id}-osmk">${smk}<rect x="0" y="1100" width="1080" height="820" fill="url(#op2Under)"/></g><g id="${id}-oemb">${emb}</g>${hand}`);
    },
    fx(tl, id, t0, o) {
      const at = AT(o), land = at + GL(o), slam = o.slam ?? 1.25, r = rng(o.seed || 911), A = (t) => t0 + t;
      const clip = title(id, o, "ember"), q = (s) => `#${id}-op2 ${s}`;
      if (o.kick) tl.fromTo(q(".k"), { opacity: 0 }, { opacity: 0.9, duration: 0.5, immediateRender: false }, A(0.05));
      // the letters catch fire one by one and keep flickering like embers
      clip.querySelectorAll(`#${id}-op2 .t i`).forEach((el, k) => {
        const t = 0.2 + k * 0.12;
        tl.fromTo(el, { opacity: 0, filter: "brightness(3) blur(6px)" }, { opacity: 1, filter: "brightness(1) blur(0px)", duration: 0.35, ease: "power2.out", immediateRender: false }, A(t));
        for (let u = t + 0.4; u < at; u += 0.08 + r() * 0.1) tl.set(el, { filter: `brightness(${(0.75 + r() * 0.6).toFixed(2)})` }, A(u));
      });
      // sparks off the title
      const tw = clip.querySelector(`#${id}-op2 .tw`);
      for (let k = 0; k < 14; k++) {
        tw.insertAdjacentHTML("beforeend", `<i class="spk" style="left:${Math.round(5 + r() * 90)}%;top:${Math.round(40 + r() * 50)}%"></i>`);
        const sp = tw.lastElementChild, t = 0.4 + r() * (at - 0.6);
        tl.fromTo(sp, { opacity: 1, x: 0, y: 0 }, { opacity: 0, x: (r() - 0.5) * 80, y: -120 - r() * 160, duration: 0.8 + r() * 0.5, ease: "power1.out", immediateRender: false }, A(t));
      }
      tl.fromTo(q(".ep"), { opacity: 0, scale: 1.9 }, { opacity: 1, scale: 1, duration: 0.14, ease: "power4.in", immediateRender: false }, A(0.9));
      // the smoke churns; embers rise through it
      document.querySelectorAll(`#${id}-osmk .osm`).forEach((el, k) => {
        tl.fromTo(el, { x: 0, y: 0 }, { x: (k % 2 ? 30 : -30), y: -40, duration: at, ease: "sine.inOut", immediateRender: false }, A(0));
        tl.to(el, { x: +el.dataset.dx, y: +el.dataset.dy, opacity: 0, duration: GL(o) * 0.75, ease: "power2.in" }, A(at));
      });
      document.querySelectorAll(`#${id}-oemb .oem`).forEach((el, k) => {
        const p = 0.9 + (k % 5) * 0.25;
        for (let t = (k % 7) * 0.13; t < land + 0.6; t += p) tl.fromTo(el, { y: 0, opacity: 1 }, { y: -500 - (k % 4) * 120, x: ((k % 3) - 1) * 60, opacity: 0, duration: p, ease: "none", immediateRender: false }, A(t));
      });
      // the burnt hand slams onto the lens and slides down
      tl.fromTo(`#${id}-ohand`, { opacity: 0, attr: { transform: "translate(560,1060) scale(1.5)" } }, { opacity: 1, attr: { transform: "translate(560,1060) scale(1)" }, duration: 0.09, ease: "power4.in", immediateRender: false }, A(slam));
      tl.to(`#${id}-ohand`, { attr: { transform: "translate(560,1200) scale(1)" }, duration: at - slam - 0.2, ease: "power1.in" }, A(slam + 0.15));
      tl.to(`#${id}-ohand`, { opacity: 0, duration: 0.3 }, A(at - 0.25));
      if (window.Fx) { Fx.punch(tl, `#${id} .stage`, A(slam + 0.05), 1.1, 0.4); Fx.glitch(tl, `#${id}`, A(slam + 0.05), 0.25, 20, 7); Fx.heart(tl, A(0.4), at - 0.4, 0.5, 0.45); }
      tl.fromTo("#fxred", { opacity: 0.9 }, { opacity: 0, duration: 0.5, immediateRender: false }, A(slam + 0.05));
      // the title crumbles to ash as the smoke blows out
      clip.querySelectorAll(`#${id}-op2 .t i`).forEach((el, k) => tl.to(el, { y: 160 + (k % 3) * 60, rotation: (k % 2 ? 1 : -1) * (10 + k * 4), opacity: 0, filter: "brightness(.3) blur(4px)", duration: 0.7, ease: "power2.in" }, A(at + k * 0.05)));
      tl.to([q(".ep"), q(".k")], { opacity: 0, y: 60, duration: 0.4, ease: "power2.in" }, A(at));
      if (window.Fx) Fx.glitch(tl, `#${id}`, A(land), 0.16, 14, 5);
      tl.fromTo("#fxred", { opacity: 0.8 }, { opacity: 0, duration: 0.6, ease: "power2.out", immediateRender: false }, A(land));
    },
    cues: (k, o) => { const at = AT(o), land = at + GL(o), slam = o.slam ?? 1.25;
      return [[k, 0.0, "swell", 0.6], [k, 0.1, "crackle", 0.9], [k, 0.9, "boom", 0.4], [k, slam, "thud", 1.1], [k, slam, "sting", 1.0], [k, slam + 0.02, "glitch", 0.6],
        [k, at - 0.9, "riser", 0.6], [k, at, "whoosh", 0.9], [k, land - 0.02, "boom", 0.9], [k, land, "glitch", 0.5]]; },
  };

  // ================= มือพราย: the title surfaces in the river and is dragged under =================
  const OpenerWater = {
    cam: camKeys,
    shake(o) {
      const at = AT(o), land = at + GL(o);
      return (t) => {
        let a = 0.8;
        if (t >= at - 0.3 && t < at + 0.3) a = 10;
        if (t >= land) a = 18 * Math.exp(-(t - land) * 7);
        return a * (Math.sin(t * 29) + 0.6 * Math.sin(t * 53 + 1));
      };
    },
    extra(L, id, o) {
      const P = window.Phrai, r = rng(o.seed || 631), cx = o.start.x + 540, cy = o.start.y + 960; // world point at the frame centre at the start
      let s = "";
      const H = [[-300, 220, -14], [-150, 300, 8], [20, 260, -4], [190, 300, 12], [330, 220, -10]];
      s += `<g id="${id}-ohands">${H.map(([dx, dy, a], k) => `<g class="ohd" data-i="${k}" opacity="0">${P ? P.paleHand(cx + dx * 0.55, cy + dy * 0.55 - 40, 0.42, a) : ""}</g>`).join("")}</g>`;
      for (let k = 0; k < 5; k++) s += `<ellipse id="${id}-orip${k}" cx="${f1(cx + H[k][0] * 0.55)}" cy="${f1(cy + H[k][1] * 0.55 - 40)}" rx="30" ry="9" fill="none" stroke="#cfe6e0" stroke-width="4" opacity="0"/>`;
      L.set.insertAdjacentHTML("beforeend", s);
      // a dark wash over the water at the start, lifting as we tilt up
      let d = "";
      for (let k = 0; k < 18; k++) d += `<circle class="obub" data-i="${k}" cx="${f1(r() * 1080)}" cy="${f1(1100 + r() * 800)}" r="${f1(5 + r() * 10)}" fill="none" stroke="#cfe6e0" stroke-width="3" opacity="0"/>`;
      L.light.insertAdjacentHTML("beforeend", `<rect id="${id}-owash" x="0" y="0" width="1080" height="1920" fill="#02070c" opacity=".35"/><g id="${id}-obub">${d}</g>`);
    },
    fx(tl, id, t0, o) {
      const at = AT(o), land = at + GL(o), r = rng(o.seed || 733), A = (t) => t0 + t;
      ripple();
      const clip = title(id, o, "water"), q = (s) => `#${id}-op2 ${s}`;
      if (o.kick) tl.fromTo(q(".k"), { opacity: 0 }, { opacity: 0.9, duration: 0.5, immediateRender: false }, A(0.05));
      // the ripple on the letters keeps moving
      tl.fromTo("#opRippleT", { attr: { seed: 1 } }, { attr: { seed: 40 }, duration: land, ease: "steps(80)", immediateRender: false }, A(0));
      // letters surface one by one from under the water
      clip.querySelectorAll(`#${id}-op2 .t i`).forEach((el, k) => tl.fromTo(el, { opacity: 0, y: 70, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.55, ease: "power2.out", immediateRender: false }, A(0.2 + k * 0.13)));
      tl.fromTo(q(".ep"), { opacity: 0, scale: 1.9 }, { opacity: 1, scale: 1, duration: 0.14, ease: "power4.in", immediateRender: false }, A(0.95));
      // drops fall off the letters
      const tw = clip.querySelector(`#${id}-op2 .tw`);
      for (let k = 0; k < 10; k++) {
        tw.insertAdjacentHTML("beforeend", `<i class="drop" style="left:${Math.round(8 + r() * 84)}%;top:78%"></i>`);
        const dp = tw.lastElementChild, t = 0.7 + r() * (at - 0.9);
        tl.fromTo(dp, { opacity: 0.9, y: 0 }, { opacity: 0, y: 140 + r() * 80, duration: 0.6, ease: "power2.in", immediateRender: false }, A(t));
      }
      // pale hands break the surface round the title, ripples spreading
      document.querySelectorAll(`#${id}-ohands .ohd`).forEach((el, k) => {
        const t = 1.15 + k * 0.12;
        tl.fromTo(el, { opacity: 0, y: 140 }, { opacity: 1, y: 0, duration: 0.45, ease: "power2.out", immediateRender: false }, A(t));
        tl.fromTo(`#${id}-orip${k}`, { opacity: 0.9, attr: { rx: 30, ry: 9 } }, { opacity: 0, attr: { rx: 160, ry: 44 }, duration: 1.2, ease: "power1.out", immediateRender: false }, A(t));
        tl.to(el, { y: -18, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }, A(t + 0.5));
        tl.to(el, { y: 200, opacity: 0, duration: 0.45, ease: "power3.in" }, A(at - 0.15));
      });
      if (window.Fx) Fx.heart(tl, A(1.1), at - 1.1, 0.5, 0.45);
      // ... and drag the letters under
      clip.querySelectorAll(`#${id}-op2 .t i`).forEach((el, k) => tl.to(el, { y: 260, opacity: 0, filter: "blur(10px)", duration: 0.5, ease: "power3.in" }, A(at - 0.25 + k * 0.04)));
      tl.to([q(".ep"), q(".k")], { opacity: 0, y: 160, duration: 0.45, ease: "power3.in" }, A(at - 0.2));
      if (window.Fx) { Fx.glitch(tl, `#${id}`, A(at - 0.2), 0.25, 16, 9); Fx.punch(tl, `#${id} .stage`, A(at - 0.15), 1.06, 0.4); }
      document.querySelectorAll(`#${id}-obub .obub`).forEach((el, k) => tl.fromTo(el, { opacity: 0.8, y: 0 }, { opacity: 0, y: -500 - (k % 4) * 100, duration: 1.0 + (k % 3) * 0.3, ease: "power1.in", immediateRender: false }, A(at - 0.2 + (k % 6) * 0.05)));
      tl.to(`#${id}-owash`, { opacity: 0, duration: GL(o) * 0.8, ease: "power1.inOut" }, A(at));
      if (window.Fx) Fx.glitch(tl, `#${id}`, A(land), 0.16, 12, 5);
      tl.fromTo("#fxred", { opacity: 0.6 }, { opacity: 0, duration: 0.6, ease: "power2.out", immediateRender: false }, A(land));
    },
    cues: (k, o) => { const at = AT(o), land = at + GL(o);
      return [[k, 0.0, "swell", 0.5], [k, 0.1, "bubbles", 0.8], [k, 0.95, "boom", 0.35], ...[0, 1, 2, 3, 4].map((i) => [k, 1.15 + i * 0.12, "plop", 0.55]), [k, 1.15, "sting", 0.8],
        [k, at - 0.9, "riser", 0.5], [k, at - 0.2, "splash", 0.9], [k, at - 0.2, "glitch", 0.5], [k, at, "whoosh", 0.6], [k, land - 0.02, "boom", 0.8], [k, land, "glitch", 0.4]]; },
  };

  window.OpenerSmoke = OpenerSmoke;
  window.OpenerWater = OpenerWater;
})();
