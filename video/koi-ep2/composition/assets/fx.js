// Screen effects for suspense beats: heartbeat vignette, tunnel vision, letterbox bars, RGB-split glitch,
// zoom punch, desaturation, speed lines, light flicker, string lights dying, and the first-person torch POV.
// Everything is placed on the shot timeline (seeded randomness only), so frames seek deterministically.
(function () {
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);

  function setup(root) {
    let lines = "";
    const r = mk(77);
    for (let i = 0; i < 46; i++) {
      const a = r() * Math.PI * 2, r0 = 380 + r() * 260, r1 = r0 + 260 + r() * 420;
      lines += `<path d="M${540 + Math.cos(a) * r0},${960 + Math.sin(a) * r0}L${540 + Math.cos(a) * r1},${960 + Math.sin(a) * r1}" stroke="#f4ecd8" stroke-width="${2 + r() * 4}" stroke-linecap="round" opacity="${0.25 + r() * 0.5}"/>`;
    }
    root.insertAdjacentHTML("beforeend", `
      <div id="fxred" style="z-index:54;position:absolute;inset:0;pointer-events:none;opacity:0;background:radial-gradient(ellipse 70% 58% at 50% 48%, transparent 40%, rgba(150,18,22,.62) 100%)"></div>
      <div id="fxtun" style="z-index:54;position:absolute;inset:-200px;pointer-events:none;opacity:0;background:radial-gradient(circle at 50% 46%, transparent 26%, rgba(0,0,0,.94) 58%)"></div>
      <svg id="fxspeed" width="1080" height="1920" style="z-index:53;position:absolute;inset:0;pointer-events:none;opacity:0">${lines}</svg>
      <div id="lbT" style="z-index:59;position:absolute;left:0;right:0;top:0;height:120px;background:#000;transform:translateY(-100%)"></div>
      <div id="lbB" style="z-index:59;position:absolute;left:0;right:0;bottom:0;height:120px;background:#000;transform:translateY(100%)"></div>`);
  }

  // two-beat pulse of a red vignette, `period` seconds per beat
  function heart(tl, t0, dur, period = 0.75, amt = 0.75) {
    for (let t = 0; t < dur - 0.1; t += period) {
      tl.fromTo("#fxred", { opacity: amt }, { opacity: amt * 0.25, duration: 0.16, ease: "power2.out", immediateRender: false }, t0 + t);
      tl.fromTo("#fxred", { opacity: amt * 0.8 }, { opacity: 0, duration: Math.min(0.4, period - 0.2), ease: "power2.out", immediateRender: false }, t0 + t + 0.18);
    }
  }
  function tunnel(tl, t0, t1, amt = 1) {
    tl.fromTo("#fxtun", { opacity: 0, scale: 1.4 }, { opacity: amt, scale: 1, duration: 0.6, ease: "power2.out", immediateRender: false }, t0);
    tl.to("#fxtun", { opacity: 0, scale: 1.4, duration: 0.4 }, t1);
  }
  function letterbox(tl, t0, t1) {
    tl.fromTo("#lbT", { yPercent: -100 }, { yPercent: 0, duration: 0.45, ease: "power2.out", immediateRender: false }, t0);
    tl.fromTo("#lbB", { yPercent: 100 }, { yPercent: 0, duration: 0.45, ease: "power2.out", immediateRender: false }, t0);
    if (t1 !== undefined) { tl.to("#lbT", { yPercent: -100, duration: 0.3 }, t1); tl.to("#lbB", { yPercent: 100, duration: 0.3 }, t1); }
  }
  // chromatic split + jitter on a shot container
  function glitch(tl, sel, t0, dur, amp = 10, seed = 3) {
    const r = mk(seed);
    for (let t = 0; t < dur; t += 0.05) {
      const d = Math.round((r() - 0.3) * amp), j = Math.round((r() - 0.5) * amp * 1.4);
      tl.set(sel, { x: j, filter: `drop-shadow(${d}px 0 0 rgba(255,40,60,.75)) drop-shadow(${-d}px 0 0 rgba(40,220,255,.75))` }, t0 + t);
    }
    tl.set(sel, { clearProps: "transform,filter" }, t0 + dur); // a lingering transform would trap the HUD under the overlays
  }
  function punch(tl, sel, t, amt = 1.1, back = 0.5) {
    tl.fromTo(sel, { scale: 1 }, { scale: amt, duration: 0.12, ease: "power3.out", transformOrigin: "50% 45%", immediateRender: false }, t);
    tl.to(sel, { scale: 1, duration: back, ease: "power2.inOut" }, t + 0.14);
  }
  function hold(tl, sel, t0, t1, scale) { // slow push that stays (focus), released at t1
    tl.fromTo(sel, { scale: 1 }, { scale, duration: t1 - t0, ease: "sine.inOut", transformOrigin: "50% 45%", immediateRender: false }, t0);
  }
  function desat(tl, sel, t0, t1, s = 0.25) {
    tl.fromTo(sel, { filter: "saturate(1) contrast(1)" }, { filter: `saturate(${s}) contrast(1.18)`, duration: 0.35, immediateRender: false }, t0);
    if (t1 !== undefined) tl.to(sel, { filter: "saturate(1) contrast(1)", duration: 0.4 }, t1);
  }
  function speed(tl, t0, t1) {
    tl.set("#fxspeed", { opacity: 1 }, t0);
    for (let t = t0; t < t1; t += 0.08) tl.set("#fxspeed", { rotation: ((t * 997) % 7) - 3, scale: 1 + ((t * 431) % 5) / 40, transformOrigin: "50% 50%" }, t);
    tl.set("#fxspeed", { opacity: 0 }, t1);
  }
  // irregular on/off flicker of anything (torch beam, lamps)
  function flicker(tl, sel, t0, dur, seed = 9, prop = "opacity") {
    const r = mk(seed);
    let t = 0;
    while (t < dur) {
      const off = 0.04 + r() * 0.09, on = 0.05 + r() * 0.22;
      tl.set(sel, { [prop]: 0.08 }, t0 + t); tl.set(sel, { [prop]: 1 }, t0 + t + off);
      t += off + on;
    }
  }
  // camp string lights die one by one (classes from camp.js)
  function lightsOut(tl, scope, t0, gap = 0.22) {
    for (let i = 0; i < 9; i++) {
      tl.set(`${scope} .bulbglow[data-i="${i}"]`, { opacity: 0 }, t0 + i * gap);
      tl.set(`${scope} .bulb[data-i="${i}"]`, { attr: { fill: "#4a4438" } }, t0 + i * gap);
    }
  }

  // ---------- first-person torch POV ----------
  // keys: [{t, x, y, r}] beam target on screen; arm: {sleeve, skin}; returns the extra() markup + a driver
  function pov(id, o) {
    const sleeve = o.sleeve || "#9c4a3c", skin = o.skin || "#d6a27c", INK = "#2e2a26";
    const markup = `<defs><radialGradient id="${id}-hg"><stop offset="0" stop-color="#000"/><stop offset=".55" stop-color="#000"/><stop offset="1" stop-color="#fff"/></radialGradient>
        <mask id="${id}-mask" maskUnits="userSpaceOnUse" x="-200" y="-200" width="1480" height="2320"><rect x="-200" y="-200" width="1480" height="2320" fill="#fff"/>
        <circle id="${id}-hole" cx="540" cy="900" r="260" fill="url(#${id}-hg)"/></mask></defs>
      <rect x="-200" y="-200" width="1480" height="2320" fill="#010203" opacity="${o.dark ?? 0.9}" mask="url(#${id}-mask)"/>
      <g id="${id}-beam"><path id="${id}-cone" fill="#fff3c8" opacity=".07"/><circle id="${id}-pool" cx="540" cy="900" r="240" fill="#fff3c8" opacity=".06"/></g>
      <g id="${id}-arm"><path d="M-70,40L-44,-400H44L70,40Z" fill="${sleeve}" stroke="${INK}" stroke-width="5"/>
        ${o.cuff ? `<path d="M-46,-380H46" stroke="${o.cuff}" stroke-width="16"/>` : ""}
        <ellipse cx="0" cy="-452" rx="52" ry="60" fill="${skin}" stroke="${INK}" stroke-width="5"/><path d="M-40,-470q20,-14 40,0M-30,-440q20,-12 46,0" stroke="${INK}" stroke-width="3.5" fill="none" opacity=".5"/>
        <rect x="-28" y="-660" width="56" height="210" rx="12" fill="#3d3833" stroke="${INK}" stroke-width="5"/><rect x="-38" y="-690" width="76" height="40" rx="9" fill="#5a5550" stroke="${INK}" stroke-width="5"/>
        <ellipse cx="0" cy="-690" rx="32" ry="9" fill="#fff4d0"/></g>`;
    const PIV = { x: o.pivotX ?? 900, y: 2080 }, R = 690;
    const sm = (k) => k * k * (3 - 2 * k);
    function at(keys, t) {
      let i = 0;
      while (i + 1 < keys.length && keys[i + 1].t <= t) i++;
      const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
      const k = b.t > a.t ? sm(Math.max(0, Math.min(1, (t - a.t) / (b.t - a.t)))) : 0;
      return { x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, r: a.r + (b.r - a.r) * k };
    }
    function drive(tl, t0, dur) {
      const hole = document.getElementById(`${id}-hole`), pool = document.getElementById(`${id}-pool`), cone = document.getElementById(`${id}-cone`), arm = document.getElementById(`${id}-arm`);
      const c = { t: 0 };
      const go = () => {
        const p = at(o.keys, c.t);
        const shake = o.shake ? o.shake(c.t) : { x: 0, y: 0 };
        const x = p.x + shake.x, y = p.y + shake.y;
        hole.setAttribute("cx", x.toFixed(1)); hole.setAttribute("cy", y.toFixed(1)); hole.setAttribute("r", p.r.toFixed(1));
        pool.setAttribute("cx", x.toFixed(1)); pool.setAttribute("cy", y.toFixed(1)); pool.setAttribute("r", (p.r * 0.85).toFixed(1));
        const th = Math.atan2(x - PIV.x, PIV.y - y);
        const bob = 10 * Math.sin(c.t * 2.4);
        arm.setAttribute("transform", `translate(${PIV.x} ${PIV.y + bob}) rotate(${(th * 180 / Math.PI).toFixed(2)})`);
        const lx = PIV.x + Math.sin(th) * R, ly = PIV.y + bob - Math.cos(th) * R, nx = Math.cos(th), ny = Math.sin(th);
        cone.setAttribute("d", `M${lx - nx * 26},${ly - ny * 26}L${x - nx * p.r * 0.9},${y - ny * p.r * 0.9}L${x + nx * p.r * 0.9},${y + ny * p.r * 0.9}L${lx + nx * 26},${ly + ny * 26}Z`);
      };
      tl.to(c, { t: dur, duration: dur, ease: "none", onUpdate: go }, t0);
      go();
      (o.flicker || []).forEach(([ft, fd], k) => {
        flicker(tl, `#${id}-beam`, t0 + ft, fd, 20 + k);
        flicker(tl, `#${id}-hole`, t0 + ft, fd, 20 + k);
      });
      (o.off || []).forEach(([a, b]) => { tl.set([`#${id}-beam`, `#${id}-hole`], { opacity: 0 }, t0 + a); if (b !== undefined) tl.set([`#${id}-beam`, `#${id}-hole`], { opacity: 1 }, t0 + b); });
    }
    return { markup, drive };
  }

  window.Fx = { setup, heart, tunnel, letterbox, glitch, punch, hold, desat, speed, flicker, lightsOut, pov };
})();
