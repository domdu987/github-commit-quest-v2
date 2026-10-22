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
        <div class="opts"><div class="opt A"><span class="key">◀</span><span>${o.a}</span></div>
          <div class="timer"><svg viewBox="0 0 110 110"><circle cx="55" cy="55" r="46" fill="rgba(16,22,26,.9)" stroke="rgba(244,236,216,.25)" stroke-width="9"/>
            <circle class="ring" cx="55" cy="55" r="46" fill="none" stroke="#f2c55c" stroke-width="9" stroke-linecap="round" stroke-dasharray="${RC}" stroke-dashoffset="0" transform="rotate(-90 55 55)"/></svg>
            ${Array.from({ length: (o.secs || 5) + 1 }, (_, n) => `<b class="n n${n}">${n}</b>`).join("")}</div>
          <div class="opt B"><span>${o.b}</span><span class="key">▶</span></div></div>
        <div class="who">${o.who || ""}</div></div>`,
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
      if (o.pickAt !== undefined) {
        const pk = o.t0abs + o.pickAt, win = o.pick === "b" ? "B" : "A", lose = win === "A" ? "B" : "A";
        tl.to(`#${id} .opt.${win}`, { scale: 1.14, backgroundColor: "#f2c55c", color: INK, duration: 0.25, ease: "back.out(3)" }, pk);
        tl.to(`#${id} .opt.${lose}`, { opacity: 0.25, scale: 0.92, duration: 0.25 }, pk);
        tl.fromTo(`#${id} .who`, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, immediateRender: false }, pk + 0.1);
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
          <div class="key">${o.key}</div><div class="ok">✓</div></div>
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
    .choice .who { margin-top:14px; font:700 30px/1 Kanit; color:#f2c55c; opacity:0; text-shadow:0 2px 8px #000; }
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
    .chapter svg { width:800px; height:20px; margin-top:6px; }`;

  function add(div, tl, sid, start, u, k) {
    const id = `${sid}-g${k}`;
    div.insertAdjacentHTML("beforeend", C[u.type].html(id, u));
    C[u.type].anim(tl, id, start + u.t, { ...u, t0abs: start });
  }

  window.GameUI = { C, CSS, ILL, face, add, mark };
})();
