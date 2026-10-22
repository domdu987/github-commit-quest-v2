// Game-style HUD for the series: small panels at the top of the frame with illustrated, animated
// medallions. Every component is {html(id, o), anim(tl, id, t0, o)} and all motion is placed on the
// shot timeline, so any frame can be seeked deterministically.
(function () {
  const INK = "#2e2a26";
  const O = `stroke="${INK}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"`;
  const mark = (s) => s.replace(/\[([^\]]+)\]/g, '<span class="k">$1</span>');

  // ---------- illustrations (viewBox 0 0 120 120); a-* classes get looping motion ----------
  const ILL = {
    whistle: `<g class="a-bob"><path d="M18,58h34v-12h16a22,22 0 1 1 -22,30H18z" fill="#e07a4f" ${O}/><circle cx="68" cy="68" r="8" fill="${INK}"/>
        <path d="M24,52l-8,-14" ${O} fill="none"/><circle cx="14" cy="34" r="6" fill="none" ${O}/></g>
      ${[0, 1, 2].map((i) => `<path class="a-wave" data-i="${i}" d="M${92 + i * 9},${44 - i * 6}q${10 + i * 4},${24 + i * 6} 0,${48 + i * 12}" fill="none" stroke="#5fa8a0" stroke-width="5" stroke-linecap="round"/>`).join("")}
      <g class="a-pulse"><circle cx="30" cy="96" r="16" fill="#f2c55c" ${O}/><text x="30" y="103" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="20" fill="${INK}">×3</text></g>`,
    hand: `<g class="a-pulse"><path d="M38,98V58q0,-8 7,-8t7,8V30q0,-8 7,-8t7,8v-4q0,-8 7,-8t7,8v8q0,-8 7,-8t7,8v46q0,22 -24,26H62q-14,0 -22,-14L26,66q-4,-8 3,-11t11,4z" fill="#efc6a0" ${O}/>
      <path d="M52,50v14M66,30v34M80,34v30" stroke="#cf9d79" stroke-width="3" fill="none"/></g>`,
    think: `<path d="M30,100V84q-14,-8 -14,-30a40,40 0 0 1 80,0q0,10 8,22l-10,4v14q0,6 -8,6H70v6z" fill="#b9cdd3" ${O}/>
      <g class="a-spin" style="transform-origin:58px 52px"><circle cx="58" cy="52" r="15" fill="#f2c55c" ${O}/>${[0, 45, 90, 135, 180, 225, 270, 315].map((a) => `<rect x="54" y="30" width="8" height="10" fill="#f2c55c" ${O} transform="rotate(${a} 58 52)"/>`).join("")}<circle cx="58" cy="52" r="5" fill="${INK}"/></g>`,
    eye: `<path d="M10,60Q60,10 110,60Q60,110 10,60z" fill="#f4ecd8" ${O}/><g class="a-look"><circle cx="60" cy="60" r="20" fill="#5fa8a0" ${O}/><circle cx="60" cy="60" r="9" fill="${INK}"/><circle cx="66" cy="54" r="4" fill="#fff"/></g>
      <path class="a-lid" d="M10,60Q60,10 110,60Q60,30 10,60z" fill="#efc6a0" ${O} opacity="0"/>`,
    map: `<path d="M14,30l30,-10l32,10l30,-10v70l-30,10l-32,-10l-30,10z" fill="#e9dcc0" ${O}/><path d="M44,20v70M76,30v70" stroke="${INK}" stroke-width="3" opacity=".5"/>
      <path class="a-draw" d="M24,86q14,-6 20,-22t26,-12q14,6 22,-14" fill="none" stroke="#e07a4f" stroke-width="5" stroke-dasharray="6 7" stroke-linecap="round"/>
      <g class="a-bob"><path d="M92,40c-12,-14 -12,-30 0,-30s12,16 0,30z" fill="#e8705a" ${O}/><circle cx="92" cy="22" r="4" fill="#f4ecd8"/></g>`,
    pair: `<g class="a-bob"><circle cx="40" cy="40" r="14" fill="#efc6a0" ${O}/><path d="M18,96q0,-38 22,-38t22,38z" fill="#d9a441" ${O}/></g>
      <g class="a-bob2"><circle cx="80" cy="40" r="14" fill="#e9bc93" ${O}/><path d="M58,96q0,-38 22,-38t22,38z" fill="#b9cdd3" ${O}/></g>
      <path d="M52,76h16" stroke="#e07a4f" stroke-width="7" stroke-linecap="round"/>`,
    elephant: `<g class="a-sway" style="transform-origin:60px 50px"><path class="a-flapL" d="M40,34Q6,26 8,62Q12,86 38,78z" fill="#8a9499" ${O}/><path class="a-flapR" d="M80,34Q114,26 112,62Q108,86 82,78z" fill="#8a9499" ${O}/>
      <path d="M38,40q0,-24 22,-24t22,24v26q0,10 -10,14v20q0,12 -8,14t-6,-10v-20q-20,-4 -20,-18z" fill="#a3acb0" ${O}/>
      <path d="M46,74q-8,8 -18,6M74,74q8,8 18,6" fill="none" stroke="#f4ecd8" stroke-width="6" stroke-linecap="round"/>
      <circle cx="50" cy="48" r="3.5" fill="${INK}"/><circle cx="70" cy="48" r="3.5" fill="${INK}"/></g>
      <g class="a-pulse" style="transform-origin:96px 98px"><circle cx="96" cy="98" r="17" fill="#e8705a" ${O}/><path d="M89,98h6l6,-6v12l-6,-6M104,91l0,0" fill="#f4ecd8" stroke="${INK}" stroke-width="2.5" stroke-linejoin="round"/><path d="M84,110L108,86" stroke="#f4ecd8" stroke-width="4" stroke-linecap="round"/></g>`,
    snake: `<path d="M24,96q-10,-14 6,-20t36,-4t26,-18t-12,-24q-12,-4 -22,6" fill="none" stroke="${INK}" stroke-width="15" stroke-linecap="round"/>
      <path d="M24,96q-10,-14 6,-20t36,-4t26,-18t-12,-24q-12,-4 -22,6" fill="none" stroke="#7fae5a" stroke-width="9" stroke-linecap="round"/>
      <path d="M24,96q-4,4 -10,2" fill="none" stroke="#c8553d" stroke-width="8" stroke-linecap="round"/>
      <g class="a-hiss"><ellipse cx="54" cy="38" rx="15" ry="11" fill="#7fae5a" ${O}/><circle cx="50" cy="35" r="2.6" fill="${INK}"/>
        <path class="a-flick" d="M40,42h-10l-4,-4M30,42l-4,4" fill="none" stroke="#c8553d" stroke-width="3" stroke-linecap="round"/></g>
      <g class="a-pulse" style="transform-origin:96px 96px"><circle cx="96" cy="96" r="17" fill="#f4ecd8" ${O}/><path d="M96,86v20M86,96h20" stroke="#e8705a" stroke-width="7" stroke-linecap="round"/></g>`,
    sos: `<g class="a-shake"><rect x="36" y="14" width="48" height="92" rx="10" fill="#3d3833" ${O}/><rect x="42" y="26" width="36" height="62" rx="4" fill="#cfe2e6"/>
      <text x="60" y="64" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="17" fill="#c8553d">1669</text><circle cx="60" cy="97" r="3.5" fill="#f4ecd8"/></g>
      ${[0, 1].map((i) => `<path class="a-wave" data-i="${i}" d="M${94 + i * 9},${44 - i * 6}q${8 + i * 3},${16 + i * 6} 0,${32 + i * 12}M${26 - i * 9},${44 - i * 6}q${-8 - i * 3},${16 + i * 6} 0,${32 + i * 12}" fill="none" stroke="#e8705a" stroke-width="5" stroke-linecap="round"/>`).join("")}`,
    pill: `<g class="a-bob"><rect x="20" y="44" width="80" height="34" rx="17" fill="#f4ecd8" stroke="${INK}" stroke-width="4" transform="rotate(-30 60 61)"/>
        <path d="M60,44v34" stroke="${INK}" stroke-width="4" transform="rotate(-30 60 61)"/><path d="M60,44h-23a17,17 0 0 0 0,34h23z" fill="#e8705a" transform="rotate(-30 60 61)"/></g>
      <g class="a-pulse"><circle cx="60" cy="60" r="46" fill="none" stroke="#e8705a" stroke-width="8"/><path d="M28,28L92,92" stroke="#e8705a" stroke-width="8" stroke-linecap="round"/></g>`,
    rule: `<circle cx="60" cy="62" r="40" fill="#f4ecd8" ${O}/>${Array.from({ length: 12 }, (_, i) => `<path d="M60,26v6" stroke="${INK}" stroke-width="3" transform="rotate(${i * 30} 60 62)"/>`).join("")}
      <path d="M60,62v-24M60,62L40,74" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><circle cx="60" cy="62" r="5" fill="#e07a4f"/>
      <g class="a-bob"><path d="M96,18a16,16 0 1 0 12,26a13,13 0 1 1 -12,-26z" fill="#f2c55c" ${O}/></g>`,
  };

  // ---------- character portraits built from the rig's own head art ----------
  function face(who, eyes = "normal") {
    const P = (window.Rig && Rig.CAST[who]) || {};
    const E = eyes === "wide"
      ? `<circle cx="-14" cy="-546" r="8" fill="#f4ecd8" stroke="${INK}" stroke-width="3.5"/><circle cx="18" cy="-546" r="8" fill="#f4ecd8" stroke="${INK}" stroke-width="3.5"/><circle cx="-14" cy="-546" r="2.6" fill="${INK}"/><circle cx="18" cy="-546" r="2.6" fill="${INK}"/>`
      : `<g class="f-open"><ellipse cx="-14" cy="-546" rx="4.5" ry="6" fill="${INK}"/><ellipse cx="18" cy="-546" rx="4.5" ry="6" fill="${INK}"/></g>
         <g class="f-shut" opacity="0"><path d="M-21,-545q7,5 14,0M11,-545q7,5 14,0" stroke="${INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/></g>`;
    const hidden = who === "unknown";
    return `<svg viewBox="-64 -624 128 128" class="face">
      ${hidden ? `<ellipse cx="0" cy="-548" rx="44" ry="52" fill="#151b1f" stroke="#8a7fb0" stroke-width="3.5"/><text x="0" y="-526" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="60" fill="#b9a8e8">?</text>` :
      `<rect x="-14" y="-506" width="28" height="30" fill="${P.skinS}" stroke="${INK}" stroke-width="3.5"/>
      <ellipse cx="0" cy="-548" rx="44" ry="52" fill="${P.skin}" stroke="${INK}" stroke-width="3.5"/>
      <path d="M18,-596Q46,-570 40,-520Q30,-500 8,-497Q36,-530 18,-596Z" fill="${P.skinS}" opacity=".55"/>
      ${P.hair}${E}
      <path d="M-24,-562q10,-5 18,-1M10,-563q10,-4 18,1" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round"/>${P.face || ""}
      <path d="M-4,-520q6,4 12,0" stroke="${INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>`}</svg>`;
  }

  const pos = (o) => `${o.side === "right" ? `right:${o.x ?? 36}px` : o.side === "center" ? "left:50%;margin-left:" + -(o.w || 760) / 2 + "px" : `left:${o.x ?? 36}px`};top:${o.top ?? 150}px;${o.w ? `width:${o.w}px;` : ""}`;
  const heart = (fill, cls = "") => `<svg viewBox="0 0 40 36" class="${cls}"><path d="M20,34L5,19A9,9 0 0 1 20,6A9,9 0 0 1 35,19Z" fill="${fill}" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/></svg>`;

  // shared entrance/exit and the looping medallion motion
  function inout(tl, sel, t0, o, from = { y: -26, scale: 0.92 }) {
    tl.fromTo(sel, { opacity: 0, ...from }, { opacity: 1, y: 0, x: 0, scale: 1, duration: 0.42, ease: "back.out(1.7)", immediateRender: false }, t0);
    if (o.end !== undefined) tl.to(sel, { opacity: 0, y: -18, duration: 0.28, ease: "power2.in" }, o.t0abs + o.end);
  }
  function loops(tl, root, t0, t1) {
    const D = Math.max(0.5, t1 - t0);
    const rep = (p) => Math.ceil(D / p) + 1;
    const q = (c) => root.querySelectorAll(c);
    const T = (el, from, to, p, extra = {}) => tl.fromTo(el, from, { ...to, duration: p, repeat: rep(p), yoyo: true, ease: "sine.inOut", immediateRender: false, ...extra }, t0);
    q(".a-pulse").forEach((el) => T(el, { scale: 1 }, { scale: 1.13, transformOrigin: "50% 50%" }, 0.42));
    q(".a-bob").forEach((el) => T(el, { y: -3 }, { y: 4 }, 0.6));
    q(".a-bob2").forEach((el) => T(el, { y: 4 }, { y: -3 }, 0.6));
    q(".a-sway").forEach((el) => T(el, { rotation: -4 }, { rotation: 4 }, 0.9));
    q(".a-flapL").forEach((el) => T(el, { scaleX: 1 }, { scaleX: 0.8, transformOrigin: "100% 50%" }, 0.35));
    q(".a-flapR").forEach((el) => T(el, { scaleX: 1 }, { scaleX: 0.8, transformOrigin: "0% 50%" }, 0.35));
    q(".a-hiss").forEach((el) => T(el, { x: 0 }, { x: -4 }, 0.5));
    q(".a-flick").forEach((el) => T(el, { scaleX: 0.2 }, { scaleX: 1, transformOrigin: "100% 50%" }, 0.16));
    q(".a-shake").forEach((el) => T(el, { rotation: -6 }, { rotation: 6, transformOrigin: "50% 50%" }, 0.09));
    q(".a-look").forEach((el) => T(el, { x: -8 }, { x: 8 }, 0.8));
    q(".a-spin").forEach((el) => tl.fromTo(el, { rotation: 0 }, { rotation: 360 * Math.ceil(D / 3), duration: 3 * Math.ceil(D / 3), ease: "none", transformOrigin: "50% 50%", immediateRender: false }, t0));
    q(".a-wave").forEach((el) => {
      const i = +el.dataset.i;
      tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.25, repeat: rep(0.6), yoyo: true, repeatDelay: 0.1, ease: "power1.inOut", immediateRender: false }, t0 + i * 0.15);
    });
    q(".a-draw").forEach((el) => tl.fromTo(el, { attr: { "stroke-dashoffset": 160 } }, { attr: { "stroke-dashoffset": 0 }, duration: 1.2, ease: "power1.inOut", immediateRender: false }, t0 + 0.2));
    q(".a-lid").forEach((el) => { for (let k = 0.6; k < D; k += 1.6) { tl.set(el, { opacity: 1 }, t0 + k); tl.set(el, { opacity: 0 }, t0 + k + 0.12); } });
    q(".f-open").forEach((el, i) => {
      const shut = el.parentNode.querySelector(".f-shut");
      for (let k = 0.7 + i * 0.4; k < D; k += 2.3) { tl.set(el, { opacity: 0 }, t0 + k); tl.set(shut, { opacity: 1 }, t0 + k); tl.set(el, { opacity: 1 }, t0 + k + 0.12); tl.set(shut, { opacity: 0 }, t0 + k + 0.12); }
    });
  }

  const C = {};

  // knowledge / rule card with an illustrated medallion and a draining time bar
  C.tip = {
    html: (id, o) => `<div id="${id}" class="gui tip ${o.tone || ""}" style="${pos(o)}">
        <div class="med"><svg viewBox="0 0 120 120">${ILL[o.ill] || ""}</svg></div>
        <div class="body"><div class="chip">${o.label || "ความรู้เอาตัวรอด"}</div><div class="txt">${mark(o.text)}</div></div>
        <div class="bar"><i></i></div></div>`,
    anim(tl, id, t0, o) {
      const el = document.getElementById(id);
      inout(tl, `#${id}`, t0, o);
      tl.fromTo(`#${id} .med`, { scale: 0, rotation: -40 }, { scale: 1, rotation: 0, duration: 0.5, ease: "back.out(2.2)", immediateRender: false }, t0 + 0.08);
      tl.fromTo(`#${id} .txt`, { opacity: 0, x: -14 }, { opacity: 1, x: 0, duration: 0.3, immediateRender: false }, t0 + 0.22);
      const end = o.t0abs + (o.end ?? o.t + 3.2);
      tl.fromTo(`#${id} .bar i`, { scaleX: 1 }, { scaleX: 0, transformOrigin: "0% 50%", duration: Math.max(0.3, end - t0 - 0.3), ease: "none", immediateRender: false }, t0 + 0.3);
      loops(tl, el, t0, end);
    },
  };

  // S.T.O.P. steps: four tiles that pop in turn
  C.steps = {
    html: (id, o) => `<div id="${id}" class="gui steps" style="${pos({ side: "center", w: 940, ...o })}">
        <div class="chip">${o.label}</div><div class="row">${o.items.map(([ill, w], i) => `<div class="st" id="${id}-s${i}"><div class="ic"><svg viewBox="0 0 120 120">${ILL[ill]}</svg></div><b>${w}</b></div>${i < o.items.length - 1 ? '<span class="arr">›</span>' : ""}`).join("")}</div>
        <div class="bar"><i></i></div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o);
      o.items.forEach((_, i) => tl.fromTo(`#${id}-s${i}`, { opacity: 0, scale: 0.4, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(2.4)", immediateRender: false }, t0 + 0.25 + i * (o.gap || 0.32)));
      tl.fromTo(`#${id}-s0 .ic`, { boxShadow: "0 0 0 0 rgba(242,197,92,.9)" }, { boxShadow: "0 0 0 16px rgba(242,197,92,0)", duration: 0.8, repeat: 4, ease: "power1.out", immediateRender: false }, t0 + 1.6);
      const end = o.t0abs + (o.end ?? o.t + 3.5);
      tl.fromTo(`#${id} .bar i`, { scaleX: 1 }, { scaleX: 0, transformOrigin: "0% 50%", duration: Math.max(0.3, end - t0 - 0.3), ease: "none", immediateRender: false }, t0 + 0.3);
      loops(tl, document.getElementById(id), t0, end);
    },
  };

  // timed two-way choice: ring drains, numbers count down, the pick lights up
  const RC = 2 * Math.PI * 46;
  C.choice = {
    html: (id, o) => `<div id="${id}" class="gui choice" style="${pos({ side: "center", w: 1000, ...o })}">
        <div class="q">${o.q}</div>
        <div class="opts"><div class="opt A"><span class="key">◀</span><span class="lbt">${o.a}</span>${o.possessed ? `<span class="lbg">${o.possessed.glitch || o.a}</span>` : ""}</div>
          <div class="timer"><svg viewBox="0 0 110 110"><circle cx="55" cy="55" r="46" fill="rgba(16,22,26,.9)" stroke="rgba(244,236,216,.25)" stroke-width="9"/>
            <circle class="ring" cx="55" cy="55" r="46" fill="none" stroke="#f2c55c" stroke-width="9" stroke-linecap="round" stroke-dasharray="${RC}" stroke-dashoffset="0" transform="rotate(-90 55 55)"/></svg>
            ${Array.from({ length: (o.secs || 5) + 1 }, (_, n) => `<b class="n n${n}">${n}</b>`).join("")}</div>
          <div class="opt B"><span>${o.b}</span><span class="key">▶</span></div></div>
        <div class="who">${(o.possessed && o.possessed.who) || o.who || ""}</div>${o.possessed && o.who ? `<div class="who who2">${o.who}</div>` : ""}</div>`,
    anim(tl, id, t0, o) {
      const secs = o.secs || 5;
      const span = o.pickAt !== undefined ? o.pickAt - o.t : secs;
      inout(tl, `#${id}`, t0, o, { y: -40, scale: 0.85 });
      tl.fromTo(`#${id} .opt.A`, { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + 0.15);
      tl.fromTo(`#${id} .opt.B`, { x: 60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + 0.15);
      tl.fromTo(`#${id} .ring`, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": RC }, duration: span, ease: "none", immediateRender: false }, t0);
      tl.fromTo(`#${id} .ring`, { attr: { stroke: "#f2c55c" } }, { attr: { stroke: "#e8705a" }, duration: span * 0.4, immediateRender: false }, t0 + span * 0.6);
      const step = span / secs;
      for (let n = secs; n >= 0; n--) {
        const at = t0 + (secs - n) * step;
        tl.set(`#${id} .n`, { opacity: 0 }, at);
        tl.fromTo(`#${id} .n${n}`, { opacity: 1, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)", immediateRender: false }, at);
      }
      tl.fromTo(`#${id} .timer`, { scale: 1 }, { scale: 1.08, duration: 0.25, repeat: Math.ceil(span / 0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + span * 0.6);
      if (o.possessed) {
        const pa = o.t0abs + o.possessed.at, side = o.possessed.side === "b" ? "B" : "A", other = side === "A" ? "B" : "A";
        const jit = o.pickAt !== undefined ? Math.max(1, Math.floor((o.pickAt - o.possessed.at) / 0.05)) : 60;
        tl.fromTo(`#${id} .opt.${side}`, { x: 0 }, { x: 7, duration: 0.05, repeat: jit, yoyo: true, immediateRender: false }, pa);
        tl.set(`#${id} .opt.${side}`, { backgroundImage: "none", backgroundColor: "rgba(20,26,30,.92)" }, pa);
        tl.to(`#${id} .opt.${side}`, { backgroundColor: "rgba(140,20,30,.92)", scale: 1.16, duration: 0.9, ease: "power2.in" }, pa);
        tl.to(`#${id} .opt.${other}`, { opacity: 0.3, scale: 0.9, duration: 0.6 }, pa + 0.2);
        tl.fromTo(`#${id} .opt.${side}`, { boxShadow: "0 0 0 0 rgba(232,80,80,.9)" }, { boxShadow: "0 0 0 30px rgba(232,80,80,0)", duration: 0.45, repeat: 4, immediateRender: false }, pa);
        [0.15, 0.4, 0.62, 0.8, 0.95].forEach((k, i) => { tl.set(`#${id} .opt.${side} .lbt`, { opacity: i % 2 ? 1 : 0 }, pa + k); tl.set(`#${id} .opt.${side} .lbg`, { opacity: i % 2 ? 0 : 1 }, pa + k); });
        tl.fromTo(`#${id} .who:not(.who2)`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, pa + 0.5);
      }
      if (o.pickAt !== undefined && o.possessed && o.who) {
        tl.to(`#${id} .who:not(.who2)`, { opacity: 0, duration: 0.15 }, o.t0abs + o.pickAt);
        tl.set(`#${id} .opt`, { x: 0 }, o.t0abs + o.pickAt);
      }
      if (o.pickAt !== undefined) {
        const pk = o.t0abs + o.pickAt, win = o.pick === "b" ? "B" : "A", lose = win === "A" ? "B" : "A";
        tl.set(`#${id} .opt.${win}`, { backgroundImage: "none", backgroundColor: "#f2c55c", color: INK }, pk); // the panel gradient would hide the pick colour
        tl.to(`#${id} .opt.${win}`, { scale: 1.14, duration: 0.25, ease: "back.out(3)" }, pk);
        tl.to(`#${id} .opt.${lose}`, { opacity: 0.25, scale: 0.92, duration: 0.25 }, pk);
        tl.fromTo(`#${id} ${o.possessed ? ".who2" : ".who"}`, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, immediateRender: false }, pk + 0.1);
        tl.fromTo(`#${id} .opt.${win}`, { boxShadow: "0 0 0 0 rgba(242,197,92,.9)" }, { boxShadow: "0 0 0 26px rgba(242,197,92,0)", duration: 0.6, repeat: 1, ease: "power1.out", immediateRender: false }, pk);
      }
    },
  };

  // quick-time event: shrinking target ring, hold meter, heartbeat line, success burst
  C.qte = {
    html: (id, o) => `<div id="${id}" class="gui qte" style="${pos({ side: "center", w: 700, ...o })}">
        <div class="lbl">${o.label}</div>
        <div class="btnwrap"><svg class="tgt" viewBox="0 0 200 200"><circle cx="100" cy="100" r="90" fill="none" stroke="#f4ecd8" stroke-width="5" stroke-dasharray="10 10" opacity=".8"/></svg>
          <svg class="hold" viewBox="0 0 200 200"><circle cx="100" cy="100" r="70" fill="rgba(16,22,26,.92)" stroke="rgba(244,236,216,.2)" stroke-width="12"/>
            <circle class="fill" cx="100" cy="100" r="70" fill="none" stroke="#7fd1b9" stroke-width="12" stroke-linecap="round" stroke-dasharray="${2 * Math.PI * 70}" stroke-dashoffset="${2 * Math.PI * 70}" transform="rotate(-90 100 100)"/></svg>
          <div class="key">${o.key || SHH}</div><div class="ok">✓</div></div>
        ${o.meter ? `<div class="meter"><span>${o.meter}</span><div class="mbar"><i></i><b></b></div></div>` : ""}
        <svg class="ecg" viewBox="0 0 600 70" preserveAspectRatio="none"><g class="ecgline"><path d="${Array.from({ length: 8 }, (_, i) => `M${i * 150},40h50l10,-26l12,52l10,-34l8,8h60`).join("")}" fill="none" stroke="#e8705a" stroke-width="5" stroke-linejoin="round"/></g></svg>
        <div class="res">${o.okText || "รอดแล้ว"}</div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { y: -30, scale: 0.8 });
      const ok = o.t0abs + o.okAt;
      const span = ok - t0;
      tl.fromTo(`#${id} .tgt`, { scale: 1.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.7, repeat: Math.ceil(span / 0.7) - 1, ease: "power2.in", immediateRender: false }, t0);
      tl.fromTo(`#${id} .fill`, { attr: { "stroke-dashoffset": 2 * Math.PI * 70 } }, { attr: { "stroke-dashoffset": 0 }, duration: span, ease: "none", immediateRender: false }, t0);
      tl.fromTo(`#${id} .key`, { scale: 1 }, { scale: 0.9, duration: 0.18, repeat: Math.ceil(span / 0.36), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
      tl.fromTo(`#${id} .ecgline`, { x: 0 }, { x: -150, duration: 0.55, repeat: Math.ceil(span / 0.55) + 6, ease: "none", immediateRender: false }, t0);
      tl.set(`#${id} .tgt`, { opacity: 0 }, ok);
      tl.set(`#${id} .key`, { opacity: 0 }, ok);
      tl.fromTo(`#${id} .ok`, { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(3)", immediateRender: false }, ok);
      tl.fromTo(`#${id} .hold`, { scale: 1 }, { scale: 1.12, duration: 0.18, yoyo: true, repeat: 1, immediateRender: false }, ok);
      tl.fromTo(`#${id} .res`, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, ok + 0.1);
      tl.to(`#${id} .ecg path`, { attr: { stroke: "#7fd1b9" }, duration: 0.3 }, ok);
      if (o.meter) { // noise level jitters just under the red line, then falls silent
        let seed = 5; const r = () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
        for (let t = 0; t < span; t += 0.09) tl.set(`#${id} .mbar i`, { scaleX: 0.25 + 0.5 * r() + (t > span * 0.55 && t < span * 0.7 ? 0.22 : 0) }, t0 + t);
        tl.to(`#${id} .mbar i`, { scaleX: 0.04, duration: 0.3 }, ok);
        tl.fromTo(`#${id} .mbar b`, { opacity: 1 }, { opacity: 0.35, duration: 0.2, repeat: Math.ceil(span / 0.2), yoyo: true, immediateRender: false }, t0 + span * 0.55);
      }
    },
  };

  // relationship toast: two portraits, a link, hearts filling
  C.rel = {
    html: (id, o) => `<div id="${id}" class="gui rel" style="${pos({ side: "right", ...o })}">
        <div class="faces"><div class="fm">${face(o.a)}</div><svg class="link" viewBox="0 0 60 30"><path d="M4,15h52M44,5l12,10l-12,10" fill="none" stroke="#f2c55c" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg><div class="fm">${face(o.b)}</div></div>
        <div><div class="chip">ความสัมพันธ์</div><div class="txt">${o.text} <b class="up">▲</b></div>
          <div class="hearts">${Array.from({ length: 5 }, (_, i) => heart(i < o.from ? "#e8705a" : "rgba(244,236,216,.18)", i === o.from ? "new" : "")).join("")}</div></div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { x: 120, y: 0, scale: 1 });
      tl.fromTo(`#${id} .new path`, { attr: { fill: "rgba(244,236,216,.18)" } }, { attr: { fill: "#e8705a" }, duration: 0.2, immediateRender: false }, t0 + 0.7);
      tl.fromTo(`#${id} .new`, { scale: 1 }, { scale: 1.6, duration: 0.2, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, t0 + 0.7);
      tl.fromTo(`#${id} .up`, { y: 6, opacity: 0 }, { y: -2, opacity: 1, duration: 0.3, repeat: 3, yoyo: true, immediateRender: false }, t0 + 0.6);
      loops(tl, document.getElementById(id), t0, o.t0abs + (o.end ?? o.t + 3));
    },
  };

  // character name tag (portrait + name + trait), drawn brush underline
  C.intro = {
    html: (id, o) => `<div id="${id}" class="gui intro" style="${pos(o)}"><div class="fm big">${face(o.who)}</div>
        <div><div class="name">${o.name}</div><div class="trait" style="background:${o.color || "#f2c55c"}">${o.trait}</div>
        <svg class="brush" viewBox="0 0 300 20"><path d="M4,12Q80,2 150,10T296,8" fill="none" stroke="${o.color || "#f2c55c"}" stroke-width="7" stroke-linecap="round" stroke-dasharray="320" stroke-dashoffset="320"/></svg></div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { x: o.side === "right" ? 80 : -80, y: 0, scale: 1 });
      tl.fromTo(`#${id} .fm`, { scale: 0, rotation: -30 }, { scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2.4)", immediateRender: false }, t0 + 0.05);
      tl.fromTo(`#${id} .trait`, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.3, immediateRender: false }, t0 + 0.3);
      tl.fromTo(`#${id} .brush path`, { attr: { "stroke-dashoffset": 320 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power2.out", immediateRender: false }, t0 + 0.35);
      loops(tl, document.getElementById(id), t0, o.t0abs + (o.end ?? o.t + 3));
    },
  };

  // character status pill (heart beats; injured / unknown)
  C.status = {
    html: (id, o) => `<div id="${id}" class="gui status ${o.tone || "danger"}" style="${pos({ side: "right", ...o })}">
        <div class="fm">${face(o.who, o.eyes)}</div><div><div class="nm">${o.name}</div><div class="st">${heart({ unknown: "#8a7fb0", safe: "#7fd1b9" }[o.tone] || "#e8705a", "beat")}<span>${o.text}</span></div></div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { x: 100, y: 0, scale: 1 });
      const end = o.t0abs + (o.end ?? o.t + 3);
      tl.fromTo(`#${id} .beat`, { scale: 1 }, { scale: 1.3, duration: 0.14, repeat: Math.ceil((end - t0) / 0.28), yoyo: true, ease: "power2.out", immediateRender: false }, t0);
      if (o.tone === "unknown") tl.fromTo(`#${id}`, { x: 0 }, { x: 5, duration: 0.05, repeat: 9, yoyo: true, immediateRender: false }, t0 + 0.5);
      tl.fromTo(`#${id}`, { boxShadow: "0 0 0 0 rgba(232,112,90,.8)" }, { boxShadow: "0 0 0 22px rgba(232,112,90,0)", duration: 0.7, repeat: 2, immediateRender: false }, t0 + 0.3);
    },
  };

  // premonition polaroid: develops from white, label, glitch jitter
  const SCENES = {
    snake: `<rect width="300" height="240" fill="#1c2a24"/><ellipse cx="150" cy="226" rx="200" ry="40" fill="#24382c"/>
      ${[30, 80, 230, 270].map((x, i) => `<path d="M${x},240q-6,-50 ${10 - i * 4},-90" stroke="#36513d" stroke-width="5" fill="none"/>`).join("")}
      <path d="M150,200h70q26,0 26,18v8h-96z" fill="#ede3cf" stroke="${INK}" stroke-width="4"/><path d="M160,170h40v32h-40z" fill="#3d4d45" stroke="${INK}" stroke-width="4"/>
      <path d="M40,214q30,-30 60,-6t44,-34" fill="none" stroke="${INK}" stroke-width="16" stroke-linecap="round"/><path d="M40,214q30,-30 60,-6t44,-34" fill="none" stroke="#7fae5a" stroke-width="10" stroke-linecap="round"/>
      <path d="M40,214q-8,6 -18,4" stroke="#c8553d" stroke-width="9" stroke-linecap="round"/><ellipse cx="148" cy="170" rx="14" ry="10" fill="#7fae5a" stroke="${INK}" stroke-width="3"/>
      <circle cx="150" cy="166" r="2.5" fill="#f2c55c"/>`,
  };
  C.polaroid = {
    html: (id, o) => `<div id="${id}" class="gui polaroid" style="${pos({ side: "right", ...o })}">
        <svg width="300" height="240" viewBox="0 0 300 240"><defs><radialGradient id="${id}-vgn"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient></defs>
          <g class="scene">${SCENES[o.scene] || ""}<rect width="300" height="240" fill="url(#${id}-vgn)"/></g><rect class="dev" width="300" height="240" fill="#f4ecd8"/></svg>
        <div class="pc">${o.caption || "ลางบอกเหตุ"}</div><div class="tag">${o.tag || "ภาพที่ยังไม่เกิดขึ้น"}</div></div>`,
    anim(tl, id, t0, o) {
      tl.fromTo(`#${id}`, { opacity: 0, y: -160, rotation: 14 }, { opacity: 1, y: 0, rotation: o.rot ?? -6, duration: 0.55, ease: "back.out(1.6)", immediateRender: false }, t0);
      tl.fromTo(`#${id} .dev`, { opacity: 1 }, { opacity: 0, duration: 1.1, ease: "power1.in", immediateRender: false }, t0 + 0.35);
      tl.fromTo(`#${id} .tag`, { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.3, immediateRender: false }, t0 + 0.6);
      for (let k = 1.4; k < (o.end ?? 3) - 0.3; k += 1.1) tl.fromTo(`#${id} .scene`, { x: 8 }, { x: 0, duration: 0.08, repeat: 2, yoyo: true, immediateRender: false }, t0 + k);
      if (o.end !== undefined) tl.to(`#${id}`, { opacity: 0, y: -40, rotation: 6, duration: 0.3 }, o.t0abs + o.end);
    },
  };

  // incoming message on a phone card
  C.phone = {
    html: (id, o) => `<div id="${id}" class="gui phone" style="${pos({ side: "center", w: 760, ...o })}">
        <div class="hdr"><div class="fm">${face(o.who)}</div><div><div class="nm">${o.name}</div><div class="sig"><i></i><i></i><i></i><i></i><span>สัญญาณกลับมาแล้ว</span></div></div></div>
        <div class="typing"><i></i><i></i><i></i></div>
        <div class="msg">${mark(o.msg)}<div class="time">ส่งเมื่อ <b>${o.time}</b> · เพิ่งได้รับ</div></div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { y: -60, scale: 0.9 });
      document.querySelectorAll(`#${id} .sig i`).forEach((el, i) => tl.fromTo(el, { opacity: 0.2 }, { opacity: 1, duration: 0.1, immediateRender: false }, t0 + 0.25 + i * 0.12));
      const show = t0 + (o.typing ?? 1.0);
      document.querySelectorAll(`#${id} .typing i`).forEach((el, i) => tl.fromTo(el, { y: 0 }, { y: -9, duration: 0.18, repeat: Math.ceil((show - t0) / 0.36), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.3 + i * 0.1));
      tl.set(`#${id} .typing`, { display: "none" }, show);
      tl.fromTo(`#${id} .msg`, { opacity: 0, scale: 0.7, y: 10 }, { opacity: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(2)", immediateRender: false, transformOrigin: "0% 0%" }, show);
      tl.fromTo(`#${id} .time b`, { color: "#2e2a26" }, { color: "#e8705a", duration: 0.3, repeat: 5, yoyo: true, immediateRender: false }, show + 0.8);
    },
  };

  // HUD chips: clock / flashlight battery / signal
  C.hud = {
    html: (id, o) => `<div id="${id}" class="gui hud" style="${pos({ side: "right", ...o })}">${o.items.map((it, i) => {
      if (it.k === "clock") return `<div class="c"><svg viewBox="0 0 120 120" class="ci">${ILL.rule}</svg><b>${it.v}</b></div>`;
      if (it.k === "bat") return `<div class="c"><svg viewBox="0 0 64 32" class="bat"><rect x="2" y="4" width="54" height="24" rx="6" fill="none" stroke="#f4ecd8" stroke-width="3"/><rect x="58" y="11" width="5" height="10" rx="2" fill="#f4ecd8"/>
          <rect class="lvl" x="6" y="8" width="${46 * it.v / 100}" height="16" rx="3" fill="${it.v < 30 ? "#e8705a" : "#7fd1b9"}"/></svg><span class="lb">ไฟฉาย</span><b class="pct">${it.v}%</b></div>`;
      if (it.k === "sig") return `<div class="c sig${it.v ? "" : " none"}"><svg viewBox="0 0 48 36" class="bars">${[0, 1, 2, 3].map((b) => `<rect x="${2 + b * 12}" y="${26 - b * 8}" width="8" height="${8 + b * 8}" rx="2" fill="${b < it.v ? "#7fd1b9" : "rgba(244,236,216,.25)"}"/>`).join("")}${it.v ? "" : `<path class="x" d="M30,4l14,14M44,4l-14,14" stroke="#e8705a" stroke-width="4" stroke-linecap="round"/>`}</svg><span>${it.v ? "มีสัญญาณ" : "ไม่มีสัญญาณ"}</span></div>`;
      return "";
    }).join("")}</div>`,
    anim(tl, id, t0, o) {
      document.querySelectorAll(`#${id} .c`).forEach((el, i) => tl.fromTo(el, { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + i * 0.12));
      if (o.end !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, o.t0abs + o.end);
      tl.fromTo(`#${id} .x`, { opacity: 1 }, { opacity: 0.2, duration: 0.3, repeat: 9, yoyo: true, immediateRender: false }, t0 + 0.4);
      loops(tl, document.getElementById(id), t0, o.t0abs + (o.end ?? 6));
    },
  };

  // chapter title: small label, big name, line drawing out from the centre
  C.chapter = {
    html: (id, o) => `<div id="${id}" class="gui chapter" style="${pos({ side: "center", w: 800, ...o })}"><div class="sm">${o.small}</div><div class="big">${o.big}</div>
        <svg viewBox="0 0 800 20"><path d="M400,10H40M400,10H760" stroke="#f2c55c" stroke-width="4" stroke-linecap="round" stroke-dasharray="360" stroke-dashoffset="360"/><circle cx="400" cy="10" r="7" fill="#f2c55c"/></svg></div>`,
    anim(tl, id, t0, o) {
      tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, t0);
      tl.fromTo(`#${id} .big`, { letterSpacing: "26px", opacity: 0 }, { letterSpacing: "4px", opacity: 1, duration: 0.8, ease: "power3.out", immediateRender: false }, t0 + 0.1);
      tl.fromTo(`#${id} path`, { attr: { "stroke-dashoffset": 360 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.7, ease: "power2.out", immediateRender: false }, t0 + 0.3);
      if (o.end !== undefined) tl.to(`#${id}`, { opacity: 0, y: -14, duration: 0.3 }, o.t0abs + o.end);
    },
  };


  const SHH = `<svg viewBox="0 0 120 120" width="96" height="96"><circle cx="60" cy="60" r="44" fill="#efc6a0" stroke="${INK}" stroke-width="4"/>
    <path d="M40,52q6,-5 12,0M68,52q6,-5 12,0" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M46,78q14,6 28,0" stroke="${INK}" stroke-width="4" fill="none"/>
    <rect x="54" y="56" width="14" height="44" rx="7" fill="#efc6a0" stroke="${INK}" stroke-width="4"/></svg>`;
  const pad2 = (n) => String(n).padStart(2, "0");
  const lerpC = (a, b, k) => { const pa = [1, 3, 5].map((i) => parseInt(a.substr(i, 2), 16)), pb = [1, 3, 5].map((i) => parseInt(b.substr(i, 2), 16)); return "#" + pa.map((v, i) => pad2(Math.round(v + (pb[i] - v) * k).toString(16))).join(""); };
  const clamp01 = (x) => Math.max(0, Math.min(1, x));

  // analog clock whose hands sweep to the time being talked about; the sky inside the dial follows the hour
  C.clock = {
    html: (id, o) => `<div id="${id}" class="gui clockw" style="${pos(o)}">
        <svg class="dial" viewBox="0 0 220 220"><defs><clipPath id="${id}-cc"><circle cx="110" cy="110" r="92"/></clipPath></defs>
          <g clip-path="url(#${id}-cc)"><rect class="sky" width="220" height="220" fill="#e9a36a"/>
            <g class="stars" opacity="0">${[[40, 60], [80, 40], [150, 70], [178, 100], [60, 100], [120, 52]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="2.2" fill="#f4ecd8"/>`).join("")}</g>
            <circle class="sun" cx="66" cy="132" r="24" fill="#ffd27a"/><circle class="moon" cx="154" cy="240" r="17" fill="#f4ecd8"/>
            <path d="M0,166L22,146L36,160L54,132L72,158L92,138L112,162L134,134L152,156L174,130L192,152L220,140V220H0Z" fill="#1b2a30"/></g>
          <circle cx="110" cy="110" r="94" fill="none" stroke="#f4ecd8" stroke-width="9"/>
          ${Array.from({ length: 12 }, (_, i) => `<path d="M110,22v${i % 3 ? 9 : 16}" stroke="#f4ecd8" stroke-width="${i % 3 ? 3 : 5}" transform="rotate(${i * 30} 110 110)"/>`).join("")}
          <g class="hh"><path d="M110,116V64" stroke="${INK}" stroke-width="13" stroke-linecap="round"/><path d="M110,116V64" stroke="#f4ecd8" stroke-width="7" stroke-linecap="round"/></g>
          <g class="mh"><path d="M110,120V34" stroke="${INK}" stroke-width="10" stroke-linecap="round"/><path d="M110,120V34" stroke="#f2c55c" stroke-width="5" stroke-linecap="round"/></g>
          <circle cx="110" cy="110" r="9" fill="#e07a4f" stroke="${INK}" stroke-width="3"/></svg>
        <div class="info"><div class="chip">${o.label}</div><div class="dig">${o.from}</div>${o.sub ? `<div class="sub">${o.who ? `<span class="fm sm">${face(o.who)}</span>` : ""}<span>${mark(o.sub)}</span><span class="dots"><i></i><i></i><i></i></span></div>` : ""}</div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { x: -80, y: 0, scale: 1 });
      const el = document.getElementById(id), q = (c) => el.querySelector(c);
      const toM = (str) => { const [h, m] = str.split(":").map(Number); return h * 60 + m; };
      const a = toM(o.from), b = toM(o.to), p = { m: a };
      const draw = () => {
        const mm = ((p.m % 1440) + 1440) % 1440;
        q(".hh").setAttribute("transform", `rotate(${(mm / 60) * 30} 110 110)`);
        q(".mh").setAttribute("transform", `rotate(${p.m * 6} 110 110)`);
        q(".dig").textContent = `${pad2(Math.floor(mm / 60))}:${pad2(Math.floor(mm % 60))}`;
        const night = clamp01((mm - 17.5 * 60) / 100) * (mm > 8 * 60 ? 1 : 0) || (mm < 5 * 60 ? 1 : 0);
        q(".sky").setAttribute("fill", lerpC("#e9a36a", "#14222c", night));
        q(".sun").setAttribute("cy", (132 + 100 * night).toFixed(1));
        q(".moon").setAttribute("cy", (240 - 150 * night).toFixed(1));
        q(".stars").setAttribute("opacity", night.toFixed(2));
      };
      tl.to(p, { m: b, duration: o.sweep || 1.8, ease: "power2.inOut", onUpdate: draw, immediateRender: false }, t0 + 0.35);
      draw();
      tl.fromTo(`#${id} .dig`, { scale: 1 }, { scale: 1.25, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, t0 + 0.35 + (o.sweep || 1.8));
      if (o.sub) {
        tl.fromTo(`#${id} .sub`, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, t0 + 0.5 + (o.sweep || 1.8));
        document.querySelectorAll(`#${id} .dots i`).forEach((d, i) => tl.fromTo(d, { opacity: 0.2 }, { opacity: 1, duration: 0.3, repeat: 9, yoyo: true, immediateRender: false }, t0 + 0.6 + (o.sweep || 1.8) + i * 0.15));
      }
    },
  };

  // illustrated cards whose artwork acts out the line being said
  const FIG = {
    signal: {
      vb: "0 0 170 200",
      svg: () => `<g class="ph"><rect x="35" y="10" width="100" height="182" rx="16" fill="#3d3833" stroke="${INK}" stroke-width="4"/><rect x="45" y="28" width="80" height="136" rx="5" fill="#cfe2e6"/>
        ${[0, 1, 2, 3].map((i) => `<rect class="b b${i}" x="${56 + i * 16}" y="${130 - i * 18}" width="11" height="${18 + i * 18}" rx="3" fill="#4f8f86"/>`).join("")}
        <path class="x" d="M62,52l46,46M108,52l-46,46" stroke="#e8705a" stroke-width="11" stroke-linecap="round" opacity="0"/><circle cx="85" cy="178" r="5" fill="#f4ecd8"/></g>`,
      anim(tl, id, t0) {
        tl.fromTo(`#${id} .ph`, { rotation: -8 }, { rotation: 8, duration: 0.22, repeat: 5, yoyo: true, transformOrigin: "50% 100%", ease: "sine.inOut", immediateRender: false }, t0 + 0.2);
        [3, 2, 1, 0].forEach((b, k) => tl.to(`#${id} .b${b}`, { attr: { fill: "#9aa3a5" }, opacity: 0.35, duration: 0.15 }, t0 + 0.45 + k * 0.22));
        tl.fromTo(`#${id} .x`, { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.3, ease: "back.out(3)", immediateRender: false }, t0 + 1.4);
        tl.fromTo(`#${id} .x`, { opacity: 1 }, { opacity: 0.3, duration: 0.25, repeat: 8, yoyo: true, immediateRender: false }, t0 + 1.8);
      },
    },
    signalOn: {
      vb: "0 0 170 200",
      svg: () => `<g class="ph"><rect x="35" y="10" width="100" height="182" rx="16" fill="#3d3833" stroke="${INK}" stroke-width="4"/><rect x="45" y="28" width="80" height="136" rx="5" fill="#cfe2e6"/>
        ${[0, 1, 2, 3].map((i) => `<rect class="b b${i}" x="${56 + i * 16}" y="${130 - i * 18}" width="11" height="${18 + i * 18}" rx="3" fill="#9aa3a5" opacity=".35"/>`).join("")}
        <g class="ok" opacity="0"><circle cx="85" cy="62" r="24" fill="#7fd1b9" stroke="${INK}" stroke-width="3"/><path d="M73,62l9,9l16,-18" stroke="${INK}" stroke-width="6" fill="none" stroke-linecap="round"/></g><circle cx="85" cy="178" r="5" fill="#f4ecd8"/></g>`,
      anim(tl, id, t0) {
        [0, 1, 2, 3].forEach((b, k) => tl.to(`#${id} .b${b}`, { attr: { fill: "#4f8f86" }, opacity: 1, duration: 0.15 }, t0 + 0.5 + k * 0.25));
        tl.fromTo(`#${id} .ok`, { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.3, ease: "back.out(3)", immediateRender: false }, t0 + 1.6);
        tl.fromTo(`#${id} .ph`, { y: 0 }, { y: -6, duration: 0.08, repeat: 7, yoyo: true, immediateRender: false }, t0 + 1.7);
      },
    },
    ignition: {
      vb: "0 0 320 220",
      svg: () => `<rect x="6" y="10" width="308" height="204" rx="30" fill="#1f2529" stroke="${INK}" stroke-width="5"/><rect x="16" y="20" width="288" height="184" rx="24" fill="url(#dashg)"/>
        <defs><linearGradient id="dashg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#323b40"/><stop offset="1" stop-color="#1a2024"/></linearGradient></defs>
        <circle cx="100" cy="110" r="72" fill="#12171a" stroke="#4a5358" stroke-width="5"/>
        ${Array.from({ length: 9 }, (_, i) => { const a = (-210 + i * 30) * Math.PI / 180; return `<path d="M${100 + Math.cos(a) * 58},${110 + Math.sin(a) * 58}L${100 + Math.cos(a) * 68},${110 + Math.sin(a) * 68}" stroke="${i > 6 ? "#e8705a" : "#cfd8d6"}" stroke-width="4"/>`; }).join("")}
        <path d="M${100 + Math.cos(Math.PI / 6) * 64},${110 + Math.sin(Math.PI / 6) * 64}A64,64 0 0 0 ${100 + Math.cos(-Math.PI / 6) * 64},${110 + Math.sin(-Math.PI / 6) * 64}" fill="none" stroke="#e8705a" stroke-width="6" opacity=".7"/>
        <g class="needle"><path d="M100,110L52,138" stroke="#f2c55c" stroke-width="7" stroke-linecap="round"/></g><circle cx="100" cy="110" r="10" fill="#f4ecd8"/>
        <text x="100" y="164" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="17" fill="#9aa3a5">RPM ×1000</text>
        <g class="wl wbat"><rect x="190" y="150" width="34" height="22" rx="4" fill="none" stroke="#e8705a" stroke-width="4"/><path d="M196,150v-5M218,150v-5M197,161h8M212,161h8M216,157v8" stroke="#e8705a" stroke-width="3"/></g>
        <g class="wl weng"><path d="M240,170v-16h8l4,-4h14l4,6h6v14h-6l-4,4h-18z" fill="none" stroke="#f0a070" stroke-width="4" stroke-linejoin="round"/></g>
        <circle cx="250" cy="90" r="40" fill="#2a3135" stroke="#9aa3a5" stroke-width="5"/><text x="250" y="48" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="14" fill="#9aa3a5">OFF · ON · START</text>
        <g class="key"><rect x="242" y="44" width="16" height="54" rx="4" fill="#c9bfa8" stroke="${INK}" stroke-width="3"/><circle cx="250" cy="38" r="22" fill="#d9a441" stroke="${INK}" stroke-width="4"/><circle cx="250" cy="38" r="6" fill="#2a2f33"/></g>
        <g class="arc" opacity="0"><path d="M206,60a50,50 0 0 1 30,-34" fill="none" stroke="#f2c55c" stroke-width="5" stroke-linecap="round" stroke-dasharray="6 7"/><path d="M228,22l10,4l-6,9" fill="none" stroke="#f2c55c" stroke-width="5" stroke-linecap="round"/></g>
        <g class="spark" opacity="0"><path d="M286,58l14,-12M290,84l20,0M282,34l8,-16M292,112l14,8" stroke="#f2c55c" stroke-width="5" stroke-linecap="round"/></g>
        <g class="chk" opacity="0"><rect x="196" y="112" width="104" height="30" rx="8" fill="#f2c55c"/><text x="248" y="134" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="${INK}">แชะ!</text></g>
        <g class="stamp" opacity="0" transform="rotate(-12 160 112)"><rect x="40" y="82" width="240" height="62" rx="10" fill="rgba(232,112,90,.15)" stroke="#e8705a" stroke-width="7"/>
          <text x="160" y="126" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="36" fill="#e8705a">สตาร์ทไม่ติด</text></g>`,
      anim(tl, id, t0) {
        const q = (c) => `#${id} ${c}`;
        [0.3, 0.95].forEach((k) => {
          tl.fromTo(q(".key"), { rotation: 0 }, { rotation: 70, duration: 0.18, svgOrigin: "250 90", ease: "back.out(2)", immediateRender: false }, t0 + k);
          tl.fromTo(q(".arc"), { opacity: 1 }, { opacity: 0, duration: 0.35, immediateRender: false }, t0 + k);
          tl.fromTo(q(".needle"), { rotation: 0 }, { rotation: 55, duration: 0.12, svgOrigin: "100 110", ease: "power2.out", yoyo: true, repeat: 3, immediateRender: false }, t0 + k + 0.1);
          tl.fromTo(q(".spark"), { opacity: 1, scale: 0.8 }, { opacity: 0, scale: 1.3, transformOrigin: "50% 50%", duration: 0.3, immediateRender: false }, t0 + k + 0.12);
          tl.fromTo(q(".chk"), { opacity: 1, scale: 0.6 }, { opacity: 0, scale: 1.1, transformOrigin: "50% 50%", duration: 0.45, ease: "power2.out", immediateRender: false }, t0 + k + 0.12);
          tl.fromTo([q(".wbat"), q(".weng")], { opacity: 1 }, { opacity: 0.15, duration: 0.07, repeat: 5, yoyo: true, immediateRender: false }, t0 + k + 0.1);
          tl.to(q(".key"), { rotation: 0, duration: 0.25, svgOrigin: "250 90" }, t0 + k + 0.5);
        });
        tl.set([q(".wbat"), q(".weng")], { opacity: 1 }, t0 + 1.6);
        tl.fromTo(q(".stamp"), { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.22, ease: "power4.in", immediateRender: false }, t0 + 1.6);
        tl.fromTo(`#${id} .art`, { x: 0 }, { x: 7, duration: 0.05, repeat: 5, yoyo: true, immediateRender: false }, t0 + 1.82);
      },
    },
    route: {
      vb: "0 0 300 190",
      svg: (id) => `<rect x="4" y="4" width="292" height="182" rx="18" fill="#e9dcc0" stroke="${INK}" stroke-width="4"/>
        ${[[30, 40], [60, 150], [120, 30], [150, 160], [210, 120], [250, 160], [270, 100], [100, 90], [180, 60]].map(([x, y]) => `<path d="M${x},${y}l10,-22l10,22z" fill="#7fa58a"/>`).join("")}
        <path id="${id}-rt" d="M52,140C100,140 110,90 160,92S230,60 248,44" fill="none" stroke="#7a6c5d" stroke-width="5" stroke-dasharray="3 10" stroke-linecap="round"/>
        <g transform="translate(52,140)"><path d="M-24,0Q-20,-30 0,-32Q20,-30 24,0Z" fill="#d9773f" stroke="${INK}" stroke-width="3"/></g>
        <text x="52" y="172" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="18" fill="${INK}">แคมป์</text>
        <g transform="translate(248,44)"><rect x="-22" y="-20" width="44" height="26" fill="#6b4a3a" stroke="${INK}" stroke-width="3"/><path d="M-28,-18L0,-38L28,-18Z" fill="#3b2c22" stroke="${INK}" stroke-width="3"/><circle cx="-8" cy="-8" r="5" fill="#ffd58a"/></g>
        <text x="236" y="86" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="18" fill="${INK}">ป้อม</text>
        <g class="who"><circle r="20" fill="#6e8f62" stroke="${INK}" stroke-width="4"/><text y="7" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="20" fill="#f4ecd8">โจ้</text></g>
        <g class="q" opacity="0"><circle r="18" fill="#b9a8e8" stroke="${INK}" stroke-width="3"/><text y="8" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="24" fill="${INK}">?</text></g>`,
      anim(tl, id, t0, o) {
        const path = document.getElementById(`${id}-rt`), len = path.getTotalLength(), who = document.querySelector(`#${id} .who`), qm = document.querySelector(`#${id} .q`);
        const p = { k: 0 }, stop = o.stopAt ?? 1;
        const go = () => { const pt = path.getPointAtLength(len * p.k * stop); who.setAttribute("transform", `translate(${pt.x.toFixed(1)},${pt.y.toFixed(1)})`); qm.setAttribute("transform", `translate(${(pt.x + 22).toFixed(1)},${(pt.y - 26).toFixed(1)})`); };
        tl.to(p, { k: 1, duration: o.walk || 2.4, ease: "power1.inOut", onUpdate: go, immediateRender: false }, t0 + 0.3);
        go();
        if (o.lost) { tl.to(`#${id} .who`, { opacity: 0.25, duration: 0.4 }, t0 + 0.3 + (o.walk || 2.4)); tl.fromTo(`#${id} .q`, { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)", immediateRender: false }, t0 + 0.4 + (o.walk || 2.4)); }
      },
    },
    rules: {
      vb: "0 0 300 200",
      svg: () => `<g class="r1"><circle cx="50" cy="52" r="38" fill="#f4ecd8" stroke="${INK}" stroke-width="4"/>${Array.from({ length: 12 }, (_, i) => `<path d="M50,18v6" stroke="${INK}" stroke-width="3" transform="rotate(${i * 30} 50 52)"/>`).join("")}
          <path d="M50,52V28M50,52L30,64" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><circle cx="50" cy="52" r="4" fill="#e07a4f"/>
          <path d="M150,82Q154,30 200,26Q246,30 250,82Z" fill="#d9773f" stroke="${INK}" stroke-width="4"/><path d="M120,90H280" stroke="#e8705a" stroke-width="6" stroke-dasharray="12 8"/>
          <g class="walker"><circle cx="268" cy="46" r="9" fill="#efc6a0" stroke="${INK}" stroke-width="3"/><path d="M268,56v20M268,76l-8,14M268,76l8,14M268,62l-10,8M268,62l10,8" stroke="${INK}" stroke-width="4" stroke-linecap="round"/></g>
          <path class="no1" d="M248,28l40,58M288,28l-40,58" stroke="#e8705a" stroke-width="7" stroke-linecap="round" opacity="0"/></g>
        <g class="r2"><path d="M28,150q22,-34 44,0q-22,34 -44,0z" fill="#f4ecd8" stroke="${INK}" stroke-width="4"/><circle cx="50" cy="150" r="8" fill="${INK}"/>
          ${[0, 1, 2].map((i) => `<path class="w" data-i="${i}" d="M${96 + i * 22},${126 - i * 4}q${12},${24 + i * 4} 0,${48 + i * 8}" stroke="#b9a8e8" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}
          <text x="200" y="146" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="26" fill="#f4ecd8">“…ปิ่น”</text>
          <g transform="translate(208,174)"><path d="M-30,0q30,-18 60,0q-30,18 -60,0z" fill="#efc6a0" stroke="${INK}" stroke-width="4"/><path class="no2" d="M-34,-20l68,40M34,-20l-68,40" stroke="#e8705a" stroke-width="7" stroke-linecap="round" opacity="0"/></g></g>`,
      anim(tl, id, t0, o) {
        tl.fromTo(`#${id} .r2`, { opacity: 0.15 }, { opacity: 1, duration: 0.3, immediateRender: false }, o.t0abs + o.second);
        tl.fromTo(`#${id} .walker`, { x: -40 }, { x: 0, duration: 0.8, ease: "power1.out", immediateRender: false }, t0 + 0.3);
        tl.fromTo(`#${id} .no1`, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.3, ease: "back.out(3)", immediateRender: false }, t0 + 1.1);
        document.querySelectorAll(`#${id} .w`).forEach((w, i) => tl.fromTo(w, { opacity: 0 }, { opacity: 1, duration: 0.25, repeat: 7, yoyo: true, immediateRender: false }, o.t0abs + o.second + i * 0.12));
        tl.fromTo(`#${id} .no2`, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.3, ease: "back.out(3)", immediateRender: false }, o.t0abs + o.second + 1.2);
        tl.set(`#${id} .txt2`, { opacity: 1 }, o.t0abs + o.second);
      },
    },
    snakeid: {
      vb: "0 0 300 200",
      svg: () => `<rect x="4" y="4" width="292" height="192" rx="18" fill="#1d2f2a" stroke="#f4ecd8" stroke-width="3"/>
        <path d="M30,150q40,-50 90,-20t80,-40t70,-30" fill="none" stroke="${INK}" stroke-width="24" stroke-linecap="round"/><path class="body" d="M30,150q40,-50 90,-20t80,-40t70,-30" fill="none" stroke="#7fae5a" stroke-width="16" stroke-linecap="round"/>
        <path d="M30,150q-12,10 -22,6" stroke="#c8553d" stroke-width="13" stroke-linecap="round"/>
        <g class="head"><path d="M262,46c26,-6 36,8 32,16c-4,10 -20,14 -38,6z" fill="#7fae5a" stroke="${INK}" stroke-width="4"/><circle cx="278" cy="52" r="4" fill="#f2c55c"/></g>
        <g class="tag t1"><rect x="16" y="14" width="124" height="30" rx="15" fill="#c8553d"/><text x="78" y="36" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="18" fill="#fff">หางสีแดงอิฐ</text></g>
        <g class="tag t2"><rect x="150" y="150" width="134" height="30" rx="15" fill="#7fae5a"/><text x="217" y="172" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="18" fill="${INK}">ตัวเขียว หัวสามเหลี่ยม</text></g>`,
      anim(tl, id, t0) {
        tl.fromTo(`#${id} .t1`, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.3, immediateRender: false }, t0 + 0.6);
        tl.fromTo(`#${id} .t2`, { opacity: 0, x: 20 }, { opacity: 1, x: 0, duration: 0.3, immediateRender: false }, t0 + 1.0);
        tl.fromTo(`#${id} .head`, { x: 0 }, { x: -6, duration: 0.3, repeat: 9, yoyo: true, immediateRender: false }, t0 + 0.4);
      },
    },
    eyeshine: {
      vb: "0 0 330 190",
      svg: (id) => `<rect x="4" y="4" width="156" height="182" rx="16" fill="#0d1418" stroke="#f4ecd8" stroke-width="3"/><rect x="170" y="4" width="156" height="182" rx="16" fill="#0d1418" stroke="#f4ecd8" stroke-width="3"/>
        <path d="M10,180L60,60L110,70Z" fill="#fff3c8" opacity=".12"/><path d="M176,180L226,60L276,70Z" fill="#fff3c8" opacity=".12"/>
        <g class="cat"><path d="M48,66l12,-26l12,22M96,62l12,-22l10,26" fill="#26343a"/><ellipse cx="84" cy="80" rx="46" ry="34" fill="#26343a"/>
          <circle class="g" cx="66" cy="78" r="15" fill="#d8ff9a" opacity=".35"/><circle class="g" cx="102" cy="78" r="15" fill="#d8ff9a" opacity=".35"/>
          <ellipse cx="66" cy="78" rx="8" ry="6" fill="#e9ffc0"/><ellipse cx="102" cy="78" rx="8" ry="6" fill="#e9ffc0"/></g>
        <g><ellipse cx="248" cy="82" rx="42" ry="48" fill="#d6a27c" stroke="${INK}" stroke-width="3"/><circle cx="232" cy="78" r="9" fill="#fff"/><circle cx="264" cy="78" r="9" fill="#fff"/>
          <circle cx="232" cy="78" r="4" fill="${INK}"/><circle cx="264" cy="78" r="4" fill="${INK}"/><path d="M238,104q10,6 20,0" stroke="${INK}" stroke-width="3" fill="none"/></g>
        <text x="84" y="150" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="24" fill="#d8ff9a">สัตว์ ✓</text>
        <text x="248" y="160" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="24" fill="#e8705a">คน ✕</text>`,
      anim(tl, id, t0) {
        tl.fromTo(`#${id} .g`, { opacity: 0.15, scale: 0.7 }, { opacity: 0.6, scale: 1.25, transformOrigin: "50% 50%", duration: 0.4, repeat: 9, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.3);
      },
    },
  };
  C.figure = {
    html: (id, o) => `<div id="${id}" class="gui fig ${o.tone || ""}" style="${pos(o)}"><div class="art" style="width:${o.artW || 200}px"><svg viewBox="${FIG[o.kind].vb}">${FIG[o.kind].svg(id, o)}</svg></div>
        <div class="body"><div class="chip">${o.label}</div><div class="txt">${mark(o.text)}</div>${o.text2 ? `<div class="txt txt2">${mark(o.text2)}</div>` : ""}</div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { x: o.side === "right" ? 90 : -90, y: 0, scale: 1 });
      tl.fromTo(`#${id} .art`, { scale: 0.6, rotation: -8 }, { scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2)", immediateRender: false }, t0 + 0.05);
      FIG[o.kind].anim(tl, id, t0, o);
      if (o.text2) tl.fromTo(`#${id} .txt2`, { opacity: 0.15 }, { opacity: 1, duration: 0.3, immediateRender: false }, o.t0abs + (o.second ?? o.t + 0.6));
    },
  };

  // sound-direction radar (the source pulses from the rim; 0deg = ahead, 180deg = behind)
  C.radar = {
    html: (id, o) => { const src = o.sources || [{ dir: o.dir, pulses: o.pulses }];
      return `<div id="${id}" class="gui radar" style="${pos(o)}"><svg viewBox="0 0 220 220">
        <circle cx="110" cy="110" r="96" fill="rgba(16,22,26,.9)" stroke="rgba(244,236,216,.5)" stroke-width="3"/>
        <circle cx="110" cy="110" r="64" fill="none" stroke="rgba(244,236,216,.2)" stroke-width="2"/><circle cx="110" cy="110" r="32" fill="none" stroke="rgba(244,236,216,.2)" stroke-width="2"/>
        <text x="110" y="34" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="16" fill="rgba(244,236,216,.6)">หน้า</text>
        <text x="110" y="198" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="16" fill="rgba(244,236,216,.6)">หลัง</text>
        <g class="sweep"><path d="M110,110L110,14A96,96 0 0 1 178,42Z" fill="rgba(127,209,185,.18)"/></g>
        ${src.map((sr, j) => `<g transform="rotate(${sr.dir} 110 110)"><path class="wedge w${j}" d="M110,110L84,20A96,96 0 0 1 136,20Z" fill="${sr.color || "rgba(232,112,90,.35)"}" opacity="0"/>
          ${[0, 1, 2].map((i) => `<circle class="pl s${j}p${i}" cx="110" cy="26" r="10" fill="none" stroke="${sr.ring || "#e8705a"}" stroke-width="5" opacity="0"/>`).join("")}<circle class="src w${j}" cx="110" cy="26" r="9" fill="${sr.ring || "#e8705a"}" opacity="0"/>
          ${sr.label ? `<text class="w${j}" x="110" y="64" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="${sr.ring || "#e8705a"}" opacity="0" transform="rotate(${-sr.dir} 110 64)">${sr.label}</text>` : ""}</g>`).join("")}
        <circle cx="110" cy="112" r="8" fill="#7fd1b9"/></svg>
        <div class="rl"><span class="chip">เสียง</span><b>${o.text}</b></div></div>`; },
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { scale: 0.6, y: 0 });
      const end = o.t0abs + (o.end ?? o.t + 4), src = o.sources || [{ dir: o.dir, pulses: o.pulses }];
      tl.fromTo(`#${id} .sweep`, { rotation: 0 }, { rotation: 360 * Math.ceil((end - t0) / 1.6), duration: 1.6 * Math.ceil((end - t0) / 1.6), ease: "none", svgOrigin: "110 110", immediateRender: false }, t0);
      src.forEach((sr, j) => (sr.pulses || [0.4]).forEach((pt, k) => {
        const at = o.t0abs + pt;
        tl.set(`#${id} .w${j}`, { opacity: 1 }, at);
        tl.fromTo(`#${id} .s${j}p${k % 3}`, { attr: { r: 8 }, opacity: 1 }, { attr: { r: 46 }, opacity: 0, duration: 0.7, ease: "power2.out", immediateRender: false }, at);
        tl.fromTo(`#${id}`, { x: 0 }, { x: 6, duration: 0.05, repeat: 5, yoyo: true, immediateRender: false }, at);
      }));
    },
  };

  // stealth HUD: detection eye + footstep noise; a loud step fills detection and flashes "found"
  C.stealth = {
    html: (id, o) => `<div id="${id}" class="gui stealth" style="${pos(o)}">
        <svg class="seye" viewBox="0 0 120 80"><path d="M6,40Q60,-6 114,40Q60,86 6,40z" fill="#0d1418" stroke="#f4ecd8" stroke-width="4"/>
          <g class="iris"><circle cx="60" cy="40" r="20" fill="#e8705a"/><circle cx="60" cy="40" r="8" fill="#0d1418"/></g>
          <path class="lidT" d="M6,40Q60,-6 114,40Q60,30 6,40z" fill="#2a3a40" stroke="#f4ecd8" stroke-width="3"/><path class="lidB" d="M6,40Q60,86 114,40Q60,50 6,40z" fill="#2a3a40" stroke="#f4ecd8" stroke-width="3"/></svg>
        <div class="rows"><div class="chip">${o.label || "โหมดย่อง"}</div>
          <div class="row"><span>ถูกตรวจจับ</span><div class="sbar det"><i></i></div><b class="pct">0%</b></div>
          <div class="row"><span>เสียงฝีเท้า</span><div class="sbar noi"><i></i></div></div></div>
        <div class="found">ถูกพบ!</div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { x: -80, y: 0, scale: 1 });
      const q = (c) => `#${id} ${c}`, det = { v: 0 }, pct = document.querySelector(q(".pct"));
      const setDet = () => { pct.textContent = Math.round(det.v) + "%"; };
      tl.set(q(".det i"), { scaleX: 0 }, t0); tl.set(q(".noi i"), { scaleX: 0.04 }, t0);
      let acc = 0;
      (o.steps || []).forEach((st) => {
        const at = o.t0abs + st; acc += 6;
        tl.fromTo(q(".noi i"), { scaleX: 0.04 }, { scaleX: 0.22, duration: 0.08, yoyo: true, repeat: 1, immediateRender: false }, at);
        tl.to(q(".det i"), { scaleX: acc / 100, duration: 0.3 }, at);
        tl.to(det, { v: acc, duration: 0.3, onUpdate: setDet }, at);
        tl.fromTo(q(".lidT"), { y: 0 }, { y: -4, duration: 0.15, yoyo: true, repeat: 1, immediateRender: false }, at);
      });
      const ck = o.t0abs + o.creakAt;
      tl.to(q(".noi i"), { scaleX: 1, duration: 0.08 }, ck);
      tl.to(q(".noi i"), { scaleX: 0.3, duration: 0.8 }, ck + 0.3);
      tl.to(q(".det i"), { scaleX: 1, duration: 0.55, ease: "power2.in" }, ck);
      tl.to(det, { v: 100, duration: 0.55, ease: "power2.in", onUpdate: setDet }, ck);
      tl.to(q(".lidT"), { y: -26, duration: 0.4, ease: "power2.in" }, ck + 0.1); tl.to(q(".lidB"), { y: 26, duration: 0.4, ease: "power2.in" }, ck + 0.1);
      tl.fromTo(q(".iris"), { scale: 1 }, { scale: 1.3, transformOrigin: "50% 50%", duration: 0.2, yoyo: true, repeat: 5, immediateRender: false }, ck + 0.55);
      tl.fromTo(q(".found"), { opacity: 0, scale: 2.4, rotation: -14 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.25, ease: "power4.in", immediateRender: false }, ck + 0.55);
      tl.fromTo(`#${id}`, { x: 0 }, { x: 10, duration: 0.05, repeat: 9, yoyo: true, immediateRender: false }, ck + 0.8);
      tl.fromTo(`#${id}`, { boxShadow: "0 0 0 0 rgba(232,80,80,.9)" }, { boxShadow: "0 0 0 30px rgba(232,80,80,0)", duration: 0.5, repeat: 3, immediateRender: false }, ck + 0.55);
    },
  };

  // incoming call on a phone held in the viewer's hand
  C.call = {
    html: (id, o) => `<div id="${id}" class="gui call" style="${pos({ side: "center", w: 520, ...o })}">
        <div class="dev"><div class="scr"><div class="lbl">สายเรียกเข้า…</div><div class="av">${[0, 1, 2].map((i) => `<i class="rg r${i}"></i>`).join("")}<div class="fm">${face(o.who)}</div></div>
          <div class="nm">${o.name}</div><div class="sub">${o.sub || "มือถือ"}</div>
          <div class="bt"><span class="no">✕</span><span class="yes">✆</span></div></div></div>
        <svg class="hand" viewBox="0 0 520 520"><path d="M60,520L110,300Q120,250 170,262L200,330L230,520Z" fill="${o.skin || "#d6a27c"}" stroke="${INK}" stroke-width="6"/>
          <path d="M360,520L400,330Q420,290 450,310L470,420L440,520Z" fill="${o.skin || "#d6a27c"}" stroke="${INK}" stroke-width="6"/><path d="M0,520L40,430L180,520Z" fill="${o.sleeve || "#9c4a3c"}" stroke="${INK}" stroke-width="6"/></svg></div>`,
    anim(tl, id, t0, o) {
      tl.fromTo(`#${id}`, { opacity: 0, y: 260 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out", immediateRender: false }, t0);
      const end = o.t0abs + (o.end ?? o.t + 6), D = end - t0;
      for (let t = 0.5; t < D; t += 1.2) tl.fromTo(`#${id} .dev`, { x: 0, rotation: 0 }, { x: 6, rotation: 1.2, duration: 0.04, repeat: 9, yoyo: true, immediateRender: false }, t0 + t);
      [0, 1, 2].forEach((i) => tl.fromTo(`#${id} .r${i}`, { scale: 1, opacity: 0.8 }, { scale: 2.1, opacity: 0, duration: 1.2, repeat: Math.ceil(D / 1.2), ease: "power1.out", immediateRender: false }, t0 + 0.3 + i * 0.4));
      tl.fromTo(`#${id} .yes`, { scale: 1 }, { scale: 1.18, duration: 0.3, repeat: Math.ceil(D / 0.3), yoyo: true, immediateRender: false }, t0 + 0.5);
      if (o.glitchAt !== undefined) for (let k = 0; k < 4; k++) { tl.set(`#${id} .nm`, { x: 8, color: "#ff9a9a" }, o.t0abs + o.glitchAt + k * 0.5); tl.set(`#${id} .nm`, { x: 0, color: "#f4ecd8" }, o.t0abs + o.glitchAt + k * 0.5 + 0.08); }
    },
  };

  // consequence banner: "X will remember that"
  C.memo = {
    html: (id, o) => `<div id="${id}" class="gui memo" style="${pos(o)}"><div class="fm sm">${face(o.who)}</div><span>${mark(o.text)}</span><i class="shine"></i></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { x: -120, y: 0, scale: 1 });
      tl.fromTo(`#${id} .shine`, { xPercent: -120 }, { xPercent: 420, duration: 0.9, ease: "power2.inOut", immediateRender: false }, t0 + 0.3);
    },
  };

  // first-person tag with a live heart-rate readout
  C.pov = {
    html: (id, o) => `<div id="${id}" class="gui pov" style="${pos(o)}"><div class="top"><span class="rec"></span><span class="lb">มุมมองของ</span><b>${o.name}</b></div>
        <div class="row"><div class="bpmh">${heart("#e8705a", "hb")}</div>
          <svg class="ecg2" viewBox="0 0 300 60" preserveAspectRatio="none"><g class="ecgl"><path d="${Array.from({ length: 8 }, (_, i) => `M${i * 75},34h22l6,-22l9,46l7,-30l5,6h26`).join("")}" fill="none" stroke="#e8705a" stroke-width="5" stroke-linejoin="round"/></g></svg>
          <div class="bnum"><b class="n">${o.bpm[0]}</b><span>BPM</span></div></div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { x: -80, y: 0, scale: 1 });
      const end = o.t0abs + (o.end ?? o.t + 5), n = document.querySelector(`#${id} .n`), p = { v: o.bpm[0] };
      const col = (v) => lerpC("#7fd1b9", "#ff5a4a", clamp01((v - 90) / 80));
      tl.to(p, { v: o.bpm[1], duration: end - t0, ease: "power1.in", immediateRender: false, onUpdate: () => { n.textContent = Math.round(p.v); n.style.color = col(p.v); } }, t0);
      // lub-dub beats whose spacing follows the rising BPM
      let t = 0.1;
      while (t0 + t < end) {
        const bpm = o.bpm[0] + (o.bpm[1] - o.bpm[0]) * Math.pow(t / (end - t0), 1.5), per = 60 / bpm, big = 1.35 + 0.25 * clamp01((bpm - 100) / 80);
        tl.fromTo(`#${id} .hb`, { scale: 1 }, { scale: big, duration: 0.07, ease: "power2.out", immediateRender: false }, t0 + t);
        tl.to(`#${id} .hb`, { scale: 1.08, duration: 0.07 }, t0 + t + 0.07);
        tl.to(`#${id} .hb`, { scale: big * 0.85, duration: 0.06 }, t0 + t + 0.14);
        tl.to(`#${id} .hb`, { scale: 1, duration: Math.max(0.1, per * 0.5) }, t0 + t + 0.2);
        tl.fromTo(`#${id} .bnum`, { scale: 1.12 }, { scale: 1, duration: 0.2, immediateRender: false }, t0 + t);
        t += per;
      }
      tl.fromTo(`#${id} .ecgl`, { x: 0 }, { x: -75, duration: 0.42, repeat: Math.ceil((end - t0) / 0.42), ease: "none", immediateRender: false }, t0);
      tl.fromTo(`#${id} .rec`, { opacity: 1 }, { opacity: 0.2, duration: 0.4, repeat: Math.ceil((end - t0) / 0.4), yoyo: true, immediateRender: false }, t0);
    },
  };

  // minimap with the trail fading out under the walkers
  C.minimap = {
    html: (id, o) => `<div id="${id}" class="gui mm" style="${pos({ side: "right", ...o })}"><svg viewBox="0 0 240 240"><defs><clipPath id="${id}-mc"><circle cx="120" cy="120" r="110"/></clipPath></defs>
        <g clip-path="url(#${id}-mc)"><rect width="240" height="240" fill="#1d2f2a"/>
          ${Array.from({ length: 26 }, (_, i) => `<path d="M${(i * 53) % 230 + 6},${(i * 97) % 220 + 14}l9,-18l9,18z" fill="#2f4a3f"/>`).join("")}
          <path class="trail" d="M120,236C120,190 92,170 104,140S140,104 126,70" fill="none" stroke="#c9b98f" stroke-width="7" stroke-dasharray="4 9" stroke-linecap="round"/>
          <g class="qm"><circle cx="196" cy="44" r="16" fill="#b9a8e8" stroke="${INK}" stroke-width="3"/><text x="196" y="52" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="${INK}">?</text></g></g>
        <circle cx="120" cy="120" r="110" fill="none" stroke="#f4ecd8" stroke-width="5"/><path d="M120,6v14" stroke="#e8705a" stroke-width="5"/><text x="120" y="38" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="16" fill="#e8705a">N</text>
        <g class="me" transform="translate(116,120)"><circle r="16" fill="rgba(127,209,185,.3)"/><path d="M0,-12L9,10L0,5L-9,10Z" fill="#7fd1b9" stroke="${INK}" stroke-width="2"/></g></svg>
        <div class="ml"><span class="chip">${o.label || "แผนที่"}</span><b class="mt">${o.text}</b></div></div>`,
    anim(tl, id, t0, o) {
      inout(tl, `#${id}`, t0, o, { scale: 0.6, y: 0 });
      tl.fromTo(`#${id} .me`, { y: 50 }, { y: 0, duration: o.walk || 2.4, ease: "none", immediateRender: false }, t0 + 0.2);
      tl.fromTo(`#${id} .trail`, { opacity: 1 }, { opacity: 0, duration: 1.2, immediateRender: false }, o.t0abs + o.lostAt);
      tl.fromTo(`#${id} .me circle`, { attr: { r: 14 } }, { attr: { r: 26 }, duration: 0.5, repeat: 9, yoyo: true, immediateRender: false }, o.t0abs + o.lostAt);
      tl.fromTo(`#${id} .qm`, { opacity: 0.4 }, { opacity: 1, duration: 0.4, repeat: 11, yoyo: true, immediateRender: false }, t0);
      tl.fromTo(`#${id} .mt`, { color: "#f4ecd8" }, { color: "#e8705a", duration: 0.3, repeat: 5, yoyo: true, immediateRender: false }, o.t0abs + o.lostAt);
    },
  };

  const PANEL = "background:linear-gradient(180deg,rgba(30,40,44,.93),rgba(15,21,24,.93)); border:2px solid rgba(244,236,216,.42); box-shadow:0 0 0 4px rgba(10,14,16,.55), 0 16px 34px rgba(0,0,0,.5);";
  const CSS = `
    .gui { position:absolute; z-index:58; opacity:0; color:#f4ecd8; font-family:Kanit; }
    .gui .k { display:inline-block; padding:0 .16em; margin:0 .05em; background:#f2c55c; color:${INK}; border-radius:8px; transform:rotate(-2deg); }
    .gui .chip { display:inline-block; font:700 22px/1 Kanit; letter-spacing:2px; color:#10171a; background:#7fd1b9; padding:6px 12px 7px; border-radius:20px; }
    .gui .fm { width:76px; height:76px; border-radius:50%; overflow:hidden; background:radial-gradient(circle at 40% 35%, #3b4a50, #1a2226); border:3px solid #f4ecd8; flex:none; }
    .gui .fm .face { width:100%; height:100%; }
    .tip { ${PANEL} border-radius:28px; display:flex; gap:20px; align-items:center; padding:16px 30px 22px 16px; max-width:1010px; }
    .tip.warn .chip { background:#f0a070; } .tip.danger .chip { background:#e8705a; } .tip.rule .chip { background:#f2c55c; }
    .tip .med, .steps .ic { width:124px; height:124px; flex:none; border-radius:50%; background:radial-gradient(circle at 38% 32%, #fffaf0, #e6d6b4 75%); border:4px solid ${INK}; box-shadow:0 0 0 4px #f4ecd8, 0 6px 14px rgba(0,0,0,.4); display:grid; place-items:center; }
    .tip .med svg { width:104px; height:104px; overflow:visible; }
    .tip .txt { font:900 40px/1.22 Kanit; margin-top:8px; white-space:nowrap; }
    .gui .bar { position:absolute; left:26px; right:26px; bottom:9px; height:5px; border-radius:3px; background:rgba(244,236,216,.15); overflow:hidden; }
    .gui .bar i { position:absolute; inset:0; background:#7fd1b9; }
    .steps { ${PANEL} border-radius:28px; padding:16px 22px 26px; text-align:center; }
    .steps .row { display:flex; align-items:center; justify-content:center; gap:6px; margin-top:12px; }
    .steps .st { display:flex; flex-direction:column; align-items:center; gap:6px; }
    .steps .ic { width:132px; height:132px; } .steps .ic svg { width:108px; height:108px; overflow:visible; }
    .steps .st b { font:900 38px/1 Kanit; } .steps .st:first-child b { color:#f2c55c; }
    .steps .arr { font:900 56px/1 Kanit; color:rgba(244,236,216,.45); margin-top:-40px; }
    .choice { text-align:center; }
    .choice .q { display:inline-block; font:700 34px/1 Kanit; letter-spacing:1px; padding:10px 24px 12px; border-radius:24px; ${PANEL} }
    .choice .opts { display:flex; align-items:center; justify-content:center; gap:22px; margin-top:16px; }
    .choice .opt { display:flex; align-items:center; gap:14px; font:900 44px/1 Kanit; padding:18px 26px 22px; border-radius:22px; ${PANEL} white-space:nowrap; }
    .choice .key { display:grid; place-items:center; width:50px; height:50px; border-radius:12px; background:#f4ecd8; color:${INK}; font-size:26px; box-shadow:0 4px 0 #9c8e76; }
    .choice .timer { position:relative; width:120px; height:120px; flex:none; } .choice .timer svg { width:120px; height:120px; }
    .choice .n { position:absolute; inset:0; display:grid; place-items:center; font:900 54px/1 Kanit; opacity:0; }
    .choice .who2 { position:absolute; left:0; right:0; color:#7fd1b9; } .choice .who { margin-top:14px; font:700 30px/1 Kanit; color:#f2c55c; opacity:0; text-shadow:0 2px 8px #000; }
    .qte { text-align:center; }
    .qte .lbl { display:inline-block; font:900 44px/1 Kanit; letter-spacing:2px; padding:12px 30px 16px; border-radius:26px; ${PANEL} }
    .qte .btnwrap { position:relative; width:220px; height:220px; margin:10px auto 0; }
    .qte .btnwrap svg { position:absolute; inset:0; width:220px; height:220px; overflow:visible; }
    .qte .key { position:absolute; inset:0; display:grid; place-items:center; font:900 38px/1 Kanit; }
    .qte .ok { position:absolute; inset:0; display:grid; place-items:center; font:900 96px/1 Kanit; color:#7fd1b9; opacity:0; }
    .qte .ecg { display:block; width:520px; height:56px; margin:4px auto 0; }
    .qte .res { font:900 40px/1 Kanit; color:#7fd1b9; opacity:0; text-shadow:0 2px 8px #000; }
    .rel { ${PANEL} border-radius:26px; display:flex; align-items:center; gap:16px; padding:14px 22px 16px 14px; }
    .rel .faces { display:flex; align-items:center; gap:2px; } .rel .link { width:44px; height:24px; }
    .rel .chip { background:#f2c55c; } .rel .txt { font:900 32px/1.2 Kanit; margin-top:6px; white-space:nowrap; } .rel .up { color:#7fd1b9; display:inline-block; }
    .rel .hearts { display:flex; gap:6px; margin-top:6px; } .rel .hearts svg { width:30px; height:27px; overflow:visible; }
    .intro { ${PANEL} border-radius:60px 26px 26px 60px; display:flex; align-items:center; gap:18px; padding:10px 30px 12px 10px; }
    .intro .fm.big { width:104px; height:104px; } .intro .name { font:900 52px/1 Kanit; }
    .intro .trait { display:inline-block; margin-top:6px; font:700 26px/1 Kanit; color:${INK}; padding:5px 12px 7px; border-radius:14px; }
    .intro .brush { display:block; width:220px; height:14px; margin-top:4px; }
    .status { ${PANEL} border-radius:44px 22px 22px 44px; display:flex; align-items:center; gap:14px; padding:8px 26px 10px 8px; }
    .status .nm { font:900 34px/1 Kanit; } .status .st { display:flex; align-items:center; gap:8px; margin-top:6px; font:700 28px/1 Kanit; color:#e8705a; }
    .status.unknown .st { color:#b9a8e8; } .status.safe .st { color:#7fd1b9; } .status .st svg { width:28px; height:26px; overflow:visible; }
    .polaroid { background:#f7f1e2; padding:16px 16px 18px; border-radius:6px; box-shadow:0 18px 40px rgba(0,0,0,.6); }
    .polaroid svg { display:block; } .polaroid .pc { font:900 34px/1 Kanit; color:${INK}; text-align:center; margin-top:12px; }
    .polaroid .tag { position:absolute; left:-30px; top:-24px; font:700 24px/1 Kanit; color:#10171a; background:#b9a8e8; padding:6px 14px 8px; border-radius:16px; transform:rotate(-4deg); white-space:nowrap; }
    .phone { ${PANEL} border-radius:34px; padding:18px 26px 24px; }
    .phone .hdr { display:flex; align-items:center; gap:14px; } .phone .nm { font:900 36px/1 Kanit; }
    .phone .sig { display:flex; align-items:flex-end; gap:4px; margin-top:6px; } .phone .sig i { display:block; width:8px; background:#7fd1b9; border-radius:2px; }
    .phone .sig i:nth-child(1) { height:8px; } .phone .sig i:nth-child(2) { height:14px; } .phone .sig i:nth-child(3) { height:20px; } .phone .sig i:nth-child(4) { height:26px; }
    .phone .sig span { margin-left:10px; font:700 22px/1 Kanit; color:#7fd1b9; }
    .phone .typing { display:flex; gap:8px; margin:18px 0 0 6px; padding:16px 22px; background:#e9e1cf; border-radius:22px 22px 22px 6px; width:max-content; }
    .phone .typing i { display:block; width:14px; height:14px; border-radius:50%; background:#7a6c5d; }
    .phone .msg { margin-top:16px; background:#f4ecd8; color:${INK}; font:900 38px/1.25 Kanit; padding:16px 22px 14px; border-radius:24px 24px 24px 6px; opacity:0; }
    .phone .msg .k { background:#e8705a; color:#fff; }
    .phone .time { font:700 22px/1 Kanit; color:#7a6c5d; margin-top:10px; } .phone .time b { font-weight:900; }
    .hud { display:flex; flex-direction:column; align-items:flex-end; gap:10px; opacity:1; }
    .hud .c { ${PANEL} border-radius:22px; display:flex; align-items:center; gap:10px; padding:8px 18px 10px 10px; font:700 26px/1 Kanit; opacity:0; }
    .hud .c b { font:900 34px/1 Kanit; } .hud .ci { width:46px; height:46px; } .hud .bat { width:64px; height:32px; } .hud .bars { width:48px; height:36px; }
    .hud .lb { color:rgba(244,236,216,.7); font-size:22px; } .hud .sig.none span { color:#e8705a; }
    .chapter { text-align:center; text-shadow:0 3px 14px rgba(0,0,0,.8); }
    .chapter .sm { font:700 30px/1 Kanit; letter-spacing:10px; color:#f2c55c; } .chapter .big { font:900 92px/1.1 Kanit; margin-top:6px; }
    .chapter svg { width:800px; height:20px; margin-top:6px; }
    .qte .meter { display:flex; align-items:center; gap:12px; justify-content:center; margin-top:6px; font:700 26px/1 Kanit; }
    .qte .mbar { position:relative; width:300px; height:22px; border-radius:11px; background:rgba(16,22,26,.9); border:2px solid rgba(244,236,216,.5); overflow:hidden; }
    .qte .mbar i { position:absolute; left:0; top:0; bottom:0; width:100%; background:linear-gradient(90deg,#7fd1b9,#f2c55c 70%,#e8705a); transform-origin:0 50%; transform:scaleX(.3); }
    .qte .mbar b { position:absolute; left:72%; top:-2px; bottom:-2px; width:5px; background:#e8705a; }
    .choice .opt { position:relative; } .choice .opt .lbg { position:absolute; left:90px; opacity:0; color:#ff9a9a; }
    .gui .fm.sm { width:54px; height:54px; display:inline-block; vertical-align:middle; }
    .clockw { ${PANEL} border-radius:30px; display:flex; align-items:center; gap:18px; padding:14px 26px 14px 14px; }
    .clockw .dial { width:190px; height:190px; flex:none; }
    .clockw .dig { font:900 74px/1 Kanit; margin-top:6px; letter-spacing:2px; transform-origin:0 50%; }
    .clockw .sub { display:flex; align-items:center; gap:10px; margin-top:8px; font:900 30px/1.1 Kanit; color:#f2c55c; opacity:0; }
    .clockw .dots { display:inline-flex; gap:5px; } .clockw .dots i { width:9px; height:9px; border-radius:50%; background:#f2c55c; display:block; }
    .fig { ${PANEL} border-radius:30px; display:flex; align-items:center; gap:20px; padding:14px 28px 16px 14px; }
    .fig .art { flex:none; background:radial-gradient(circle at 40% 35%, #fffaf0, #e6d6b4 80%); border:4px solid ${INK}; border-radius:24px; padding:8px; box-shadow:0 0 0 4px #f4ecd8; }
    .fig .art svg { display:block; width:100%; height:auto; overflow:visible; }
    .fig.dark .art { background:#0d1418; }
    .fig .txt { font:900 40px/1.2 Kanit; margin-top:8px; white-space:nowrap; } .fig .txt2 { opacity:.15; }
    .fig.warn .chip { background:#f0a070; } .fig.danger .chip { background:#e8705a; } .fig.rule .chip { background:#f2c55c; }
    .radar { display:flex; align-items:center; gap:14px; } .radar svg { width:200px; height:200px; }
    .radar .rl { display:flex; flex-direction:column; gap:8px; font:900 40px/1.1 Kanit; text-shadow:0 2px 10px #000; } .radar .chip { background:#e8705a; width:max-content; }
    .memo { ${PANEL} border-radius:40px; display:flex; align-items:center; gap:12px; padding:8px 26px 8px 8px; font:900 32px/1 Kanit; overflow:hidden; }
    .memo .shine { position:absolute; top:0; bottom:0; left:0; width:30%; background:linear-gradient(90deg,transparent,rgba(242,197,92,.45),transparent); }
    .pov { ${PANEL} border-radius:30px; display:flex; }
    .pov .lb { font:700 24px/1 Kanit; color:rgba(244,236,216,.7); } .pov .rec { width:16px; height:16px; border-radius:50%; background:#e8705a; display:block; }
    .pov .bpm { display:flex; align-items:center; gap:6px; margin-left:10px; color:#e8705a; } .pov .bpm svg { width:30px; height:27px; overflow:visible; }
    .mm { display:flex; flex-direction:column; align-items:center; gap:8px; } .mm svg { width:230px; height:230px; filter:drop-shadow(0 10px 20px rgba(0,0,0,.6)); }

    .gui { --tone: #7fd1b9; --glow: .3; }
    .tip, .fig, .clockw, .steps, .rel, .intro, .status, .phone, .memo, .pov { box-shadow: 0 0 0 4px rgba(10,14,16,.55), 0 0 34px rgba(127,209,185,calc(var(--glow) * .9)), 0 16px 34px rgba(0,0,0,.5); }
    .tip.warn, .fig.warn { box-shadow: 0 0 0 4px rgba(10,14,16,.55), 0 0 34px rgba(240,160,112,calc(var(--glow) * .9)), 0 16px 34px rgba(0,0,0,.5); }
    .tip.danger, .fig.danger, .status.danger { box-shadow: 0 0 0 4px rgba(10,14,16,.55), 0 0 34px rgba(232,112,90,calc(var(--glow) * .9)), 0 16px 34px rgba(0,0,0,.5); }
    .tip.rule, .fig.rule { box-shadow: 0 0 0 4px rgba(10,14,16,.55), 0 0 34px rgba(242,197,92,calc(var(--glow) * .9)), 0 16px 34px rgba(0,0,0,.5); }
    .fx-ring { position: absolute; inset: -4px; border-radius: inherit; padding: 4px; pointer-events: none; --a: 0deg;
      background: conic-gradient(from var(--a), transparent 0deg 210deg, var(--tone) 290deg, #fffbe8 312deg, var(--tone) 330deg, transparent 360deg);
      -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor; mask-composite: exclude; }
    .fx-shw { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
    .fx-sheen { position: absolute; top: -10%; bottom: -10%; left: 0; width: 30%; background: linear-gradient(100deg, transparent, rgba(255,255,255,.2), transparent); transform: translateX(-160%); }
    .fx-flash { position: absolute; inset: 0; border-radius: inherit; background: var(--tone); opacity: 0; pointer-events: none; }
    .fx-shock { position: absolute; inset: -6px; border-radius: 50%; border: 4px solid var(--tone); opacity: 0; pointer-events: none; }
    .fig .fx-shock, .clockw .fx-shock { border-radius: 26px; }
    .fx-spk { position: absolute; left: 50%; top: 50%; width: 10px; height: 10px; margin: -5px; border-radius: 50%; background: #fff3c8; box-shadow: 0 0 10px var(--tone); opacity: 0; pointer-events: none; }
    .tip .txt, .fig .txt { font-size: 44px; } .gui .chip { font-size: 24px; }
    .pov { flex-direction: column; align-items: stretch; gap: 8px; padding: 12px 22px 14px; }
    .pov .top { display: flex; align-items: center; gap: 10px; font: 900 32px/1 Kanit; }
    .pov .row { display: flex; align-items: center; gap: 14px; }
    .pov .bpmh { width: 74px; height: 70px; display: grid; place-items: center; } .pov .bpmh .hb { width: 70px; height: 64px; overflow: visible; filter: drop-shadow(0 0 12px rgba(232,112,90,.8)); }
    .pov .bpmh .fx-shock { border-color: #e8705a; }
    .pov .ecg2 { width: 170px; height: 54px; }
    .pov .bnum { display: flex; align-items: baseline; gap: 6px; } .pov .bnum b { font: 900 60px/1 Kanit; } .pov .bnum span { font: 700 22px/1 Kanit; color: rgba(244,236,216,.7); }

    .call { opacity:0; } .call .dev { position:relative; margin:0 auto; width:420px; height:760px; border-radius:56px; background:#1a1d20; border:6px solid ${INK}; box-shadow:0 30px 60px rgba(0,0,0,.6), 0 0 40px rgba(127,209,185,.25); padding:22px; }
    .call .scr { width:100%; height:100%; border-radius:40px; background:linear-gradient(180deg,#24343c,#0f171b); display:flex; flex-direction:column; align-items:center; padding-top:60px; }
    .call .lbl { font:700 28px/1 Kanit; color:rgba(244,236,216,.75); } .call .av { position:relative; width:180px; height:180px; margin-top:40px; }
    .call .av .fm { position:absolute; inset:0; width:180px; height:180px; border-width:5px; } .call .rg { position:absolute; inset:0; border-radius:50%; border:4px solid #7fd1b9; }
    .call .nm { font:900 76px/1 Kanit; margin-top:36px; } .call .sub { font:700 26px/1 Kanit; color:rgba(244,236,216,.6); margin-top:12px; }
    .call .bt { margin-top:auto; margin-bottom:70px; display:flex; gap:120px; } .call .bt span { width:110px; height:110px; border-radius:50%; display:grid; place-items:center; font:900 54px/1 Kanit; color:#fff; }
    .call .no { background:#e8705a; } .call .yes { background:#4fb37a; } .call .hand { position:absolute; left:0; right:0; bottom:-170px; width:520px; height:520px; }

    .stealth { ${PANEL} border-radius:28px; display:flex; align-items:center; gap:18px; padding:14px 26px 16px 16px; }
    .stealth .seye { width:130px; height:88px; flex:none; } .stealth .rows { display:flex; flex-direction:column; gap:8px; }
    .stealth .row { display:flex; align-items:center; gap:12px; font:700 26px/1 Kanit; } .stealth .row span { width:130px; }
    .stealth .sbar { position:relative; width:260px; height:20px; border-radius:10px; background:rgba(244,236,216,.15); overflow:hidden; border:2px solid rgba(244,236,216,.4); }
    .stealth .sbar i { position:absolute; inset:0; transform-origin:0 50%; transform:scaleX(0); }
    .stealth .det i { background:linear-gradient(90deg,#f2c55c,#e8705a); } .stealth .noi i { background:linear-gradient(90deg,#7fd1b9,#f2c55c 60%,#e8705a); }
    .stealth .pct { font:900 30px/1 Kanit; color:#e8705a; width:70px; }
    .stealth .found { position:absolute; right:-30px; top:-30px; font:900 54px/1 Kanit; color:#fff; background:#d8463a; padding:8px 22px 12px; border-radius:14px; border:4px solid #2e2a26; opacity:0; box-shadow:0 0 30px rgba(232,80,80,.8); }
    .mm .ml { display:flex; flex-direction:column; align-items:center; gap:6px; font:900 32px/1 Kanit; text-shadow:0 2px 10px #000; }`;

  // ---------- living panels: reveal wipe, flash, sparks, a light running round the rim, sheen, glowing keywords ----------
  const TONES = { warn: "#f0a070", danger: "#e8705a", rule: "#f2c55c", safe: "#7fd1b9", unknown: "#b9a8e8" };
  const FXP = ["tip", "steps", "rel", "intro", "status", "phone", "clockw", "fig", "memo", "pov", "stealth"];
  function fxPanel(tl, el, t0, t1) {
    const cls = [...el.classList];
    if (!FXP.some((c) => cls.includes(c))) return;
    const tone = TONES[cls.find((c) => TONES[c])] || "#7fd1b9";
    el.style.setProperty("--tone", tone);
    el.insertAdjacentHTML("afterbegin", `<i class="fx-ring"></i><i class="fx-shw"><i class="fx-sheen"></i></i><i class="fx-flash"></i>`);
    const med = el.querySelector(".med, .dial, .fm.big, .bpmh, .ic");
    if (med) {
      med.style.position = "relative";
      med.insertAdjacentHTML("beforeend", `<i class="fx-shock"></i>` + Array.from({ length: 10 }, (_, i) => `<i class="fx-spk" data-i="${i}"></i>`).join(""));
    }
    const id = `#${el.id}`, D = Math.max(1, t1 - t0);
    // entrance: wipe open left→right with a bright edge, flash, sparks out of the icon
    tl.fromTo(id, { clipPath: "inset(-60px 100% -60px -60px round 30px)" }, { clipPath: "inset(-60px -60px -60px -60px round 30px)", duration: 0.5, ease: "power3.out", immediateRender: false }, t0);
    tl.fromTo(`${id} > .fx-flash`, { opacity: 0.6 }, { opacity: 0, duration: 0.55, ease: "power2.out", immediateRender: false }, t0 + 0.05);
    el.querySelectorAll(".fx-spk").forEach((sp, i) => {
      const a = (i / 10) * Math.PI * 2 + 0.3, r = 70 + (i % 3) * 22;
      tl.fromTo(sp, { x: 0, y: 0, opacity: 1, scale: 1 }, { x: Math.cos(a) * r, y: Math.sin(a) * r, opacity: 0, scale: 0.3, duration: 0.6, ease: "power2.out", immediateRender: false }, t0 + 0.12);
    });
    // text types on; keywords pop and glow
    el.querySelectorAll(".txt, .name, .nm, .dig, .msg").forEach((tx, i) =>
      tl.fromTo(tx, { clipPath: "inset(-20px 100% -20px -10px)" }, { clipPath: "inset(-20px -20px -20px -10px)", duration: 0.55, ease: "power1.inOut", immediateRender: false }, t0 + 0.18 + i * 0.12));
    el.querySelectorAll(".k").forEach((k, i) => {
      tl.fromTo(k, { scale: 0.5 }, { scale: 1.18, duration: 0.18, ease: "back.out(3)", immediateRender: false }, t0 + 0.55 + i * 0.1);
      tl.to(k, { scale: 1, duration: 0.2 }, t0 + 0.75 + i * 0.1);
      tl.fromTo(k, { boxShadow: "0 0 0 0 rgba(242,197,92,.0)" }, { boxShadow: "0 0 22px 4px rgba(242,197,92,.75)", duration: 0.5, repeat: Math.ceil(D / 0.5), yoyo: true, immediateRender: false }, t0 + 0.75);
    });
    // living: light runs round the rim, sheen sweeps, icon shock rings, glow breathes
    tl.fromTo(`${id} > .fx-ring`, { "--a": "0deg" }, { "--a": `${360 * Math.ceil(D / 2.4)}deg`, duration: 2.4 * Math.ceil(D / 2.4), ease: "none", immediateRender: false }, t0);
    for (let t = 0.35; t < D; t += 2.3) tl.fromTo(`${id} .fx-sheen`, { xPercent: -160 }, { xPercent: 420, duration: 0.8, ease: "power2.inOut", immediateRender: false }, t0 + t);
    const art = el.querySelector(".art");
    if (art) tl.fromTo(art, { boxShadow: "0 0 0 4px #f4ecd8, 0 0 0 0 rgba(242,197,92,0)" }, { boxShadow: "0 0 0 4px #f4ecd8, 0 0 26px 6px rgba(242,197,92,.55)", duration: 0.8, repeat: Math.ceil(D / 0.8), yoyo: true, immediateRender: false }, t0 + 0.4);
    if (med) tl.fromTo(`${id} .fx-shock`, { scale: 0.9, opacity: 0.9 }, { scale: 1.7, opacity: 0, duration: 1.1, repeat: Math.ceil(D / 1.1), ease: "power2.out", immediateRender: false }, t0 + 0.3);
    tl.fromTo(id, { "--glow": "0.25" }, { "--glow": "0.6", duration: 0.9, repeat: Math.ceil(D / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
  }

  function add(div, tl, sid, start, u, k) {
    const id = `${sid}-g${k}`;
    div.insertAdjacentHTML("beforeend", C[u.type].html(id, u));
    C[u.type].anim(tl, id, start + u.t, { ...u, t0abs: start });
    fxPanel(tl, document.getElementById(id), start + u.t, start + (u.end ?? u.t + 6));
  }

  window.GameUI = { C, CSS, ILL, face, add, mark };
})();
