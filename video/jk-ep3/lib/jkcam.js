// สกิลจอมโกหก · cinematic camera vocabulary on top of the engine's 2.5-D camera (pan / zoom / parallax / shake / per-layer DOF):
//   JKC.move(camA, camB, at, glide)   one framing easing into another at `at` (crane down, dolly in, snap zoom with a short glide)
//   JKC.dutch(deg, base?)             a constant roll (a tilted, uneasy frame), on top of any other shake function
//   JKC.hand(amp, roll, base?)        hand-held wander           JKC.pov(bob, step)   a walking first-person bob
//   JKC.impact(t0, dur, amp, base?)   a decaying hit shake from t0 (a fall, a landing, a bang)
//   JKC.ots(L, { side, color })       over-the-shoulder: a soft dark shoulder + head in the near corner (screen space)
//   JKC.rack(tl, L, at, from, to, d)  rack focus: tween the per-layer blur, e.g. { act: 8 } → { act: 0 }
//   JKC.whipOut / whipIn(tl, id, at, dir)   a whip pan out of one shot and into the next
//   JKC.bars(tl, L, at, dur, h)       letterbox bars for a cinematic beat (slide in, slide out at the end)
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const norm = (b) => (typeof b === "number" ? { x: b, y: 0, r: 0 } : { x: b?.x || 0, y: b?.y || 0, r: b?.r || 0 });
  const move = (a, b, at, glide = 0.6, ease) => ({ keys: [{ t: 0, ...a, drift: { s: 0.01 } }, { t: at, ...b, glide, ...(ease ? { ease } : {}) }] });
  const dutch = (deg, base) => (t) => { const o = norm(base ? base(t) : 0); return { x: o.x, y: o.y, r: o.r + deg }; };
  const hand = (amp = 5, roll = 0.5, base) => (t) => { const o = norm(base ? base(t) : 0);
    return { x: o.x + amp * (Math.sin(t * 1.7) * 0.6 + Math.sin(t * 2.9 + 1) * 0.4), y: o.y + amp * 0.6 * (Math.sin(t * 1.3 + 2) * 0.5 + Math.sin(t * 3.7) * 0.5), r: o.r + roll * Math.sin(t * 0.9 + 0.5) }; };
  const pov = (bob = 10, step = 5.5) => (t) => ({ x: 4 * Math.sin((t * step) / 2), y: bob * Math.abs(Math.sin(t * step)), r: 1.2 * Math.sin((t * step) / 2) });
  const impact = (t0, dur = 0.5, amp = 14, base) => (t) => { const o = norm(base ? base(t) : 0); if (t < t0 || t > t0 + dur) return o; const k = 1 - (t - t0) / dur;
    return { x: o.x + amp * Math.sin((t - t0) * 70) * k, y: o.y + amp * 0.5 * Math.cos((t - t0) * 55) * k, r: o.r + 1.5 * Math.sin((t - t0) * 40) * k }; };
  const ots = (L, o = {}) => { const side = o.side || "left", c = o.color || "#202a44", W = window.STAGE_W || 1080, H = window.STAGE_H || 1920;
    const g = document.createElementNS(NS, "g"); (L.screen || L.light).appendChild(g);
    g.innerHTML = `<g transform="translate(${side === "left" ? 0 : W},${H}) scale(${side === "left" ? 1 : -1},1)" opacity="${o.op ?? 0.94}" filter="url(#jkiSoft)">
      <path d="M-200,0V-700Q-200,-900 -20,-940Q140,-960 220,-820Q300,-700 520,-640Q620,-610 640,-500V0Z" fill="${c}"/><circle cx="90" cy="-1120" r="${o.head ?? 230}" fill="${o.hair || "#1a1620"}"/></g>`; return g; };
  const rack = (tl, L, at, from, to, dur = 0.7) => { const p = { ...from }; const apply = () => Object.keys(p).forEach((k) => { if (L[k]) L[k].style.filter = p[k] > 0.05 ? `blur(${(+p[k]).toFixed(1)}px)` : "none"; });
    tl.to(p, { ...to, duration: dur, ease: "sine.inOut", onUpdate: apply, onStart: apply }, at); };
  // the whip's motion blur is an SVG filter bounded to the frame (a CSS blur on the world group would have to raster an 8000-px surface and drops out)
  const whipF = (id) => { const W = window.STAGE_W || 1080, H = window.STAGE_H || 1920, d = document.getElementById(`${id}-defs`);
    if (!document.getElementById(`${id}-whip`)) d.insertAdjacentHTML("beforeend", `<filter id="${id}-whip" filterUnits="userSpaceOnUse" x="-200" y="-200" width="${W + 400}" height="${H + 400}"><feGaussianBlur id="${id}-whipb" stdDeviation="0 0"/></filter>`);
    return document.getElementById(`${id}-whipb`); };
  const whipOut = (tl, id, at, dir = 1, dur = 0.16) => { const w = document.getElementById(`${id}-world`), b = whipF(id);
    tl.set(w, { attr: { filter: `url(#${id}-whip)` } }, at); tl.fromTo(b, { attr: { stdDeviation: "0 0" } }, { attr: { stdDeviation: "22 0" }, duration: dur, ease: "power2.in", immediateRender: false }, at);
    tl.fromTo(w, { x: 0 }, { x: -dir * 700, duration: dur, ease: "power2.in", immediateRender: false }, at); };
  const whipIn = (tl, id, at, dir = 1, dur = 0.16) => { const w = document.getElementById(`${id}-world`), b = whipF(id);
    tl.set(w, { attr: { filter: `url(#${id}-whip)` } }, at); tl.fromTo(b, { attr: { stdDeviation: "22 0" } }, { attr: { stdDeviation: "0 0" }, duration: dur, ease: "power2.out", immediateRender: false }, at);
    tl.fromTo(w, { x: dir * 700 }, { x: 0, duration: dur, ease: "power2.out", immediateRender: false }, at); tl.set(w, { attr: { filter: "none" } }, at + dur + 0.02); };
  const bars = (tl, L, at, dur, h = 150, o = {}) => { const W = window.STAGE_W || 1080, H = window.STAGE_H || 1920, g = document.createElementNS(NS, "g"); (L.screen || L.light).appendChild(g);
    g.innerHTML = `<rect x="-100" y="${-h}" width="${W + 200}" height="${h}" fill="#05060a"/><rect x="-100" y="${H}" width="${W + 200}" height="${h}" fill="#05060a"/>`;
    const [a, b] = g.children; tl.fromTo(a, { y: 0 }, { y: h, duration: 0.45, ease: "power2.out", immediateRender: false }, at); tl.fromTo(b, { y: 0 }, { y: -h, duration: 0.45, ease: "power2.out", immediateRender: false }, at);
    if (o.out !== false) { tl.to(a, { y: 0, duration: 0.35, ease: "power2.in" }, at + dur - 0.36); tl.to(b, { y: 0, duration: 0.35, ease: "power2.in" }, at + dur - 0.36); } return g; };

  // ---- viewpoints that are not just a framing: a mask, a look down from the sky, a look up the shaft, the back of a head ----
  const G = (layer, html) => { const g = document.createElementNS(NS, "g"); layer.appendChild(g); if (html) g.innerHTML = html; return g; };
  // through the two eye holes of the bucket (screen space); pair with shake: JKC.pov(...) for the head bob
  const bucketPOV = (L, o = {}) => { const W = window.STAGE_W || 1080, H = window.STAGE_H || 1920, cy = o.cy ?? 900, rx = o.rx ?? 200, ry = o.ry ?? 250, x1 = o.x1 ?? 318, x2 = o.x2 ?? 762;
    const hole = (cx) => `M${cx - rx},${cy}a${rx},${ry} 0 1,0 ${2 * rx},0a${rx},${ry} 0 1,0 ${-2 * rx},0`;
    return G((L.screen || L.light), `<g id="${o.id || "bpov"}"><path d="M-100,-100H${W + 100}V${H + 100}H-100Z ${hole(x1)} ${hole(x2)}" fill="#1c1308" fill-rule="evenodd"/>
      ${[x1, x2].map((cx) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx + 6}" ry="${ry + 6}" fill="none" stroke="#000" stroke-width="34" opacity=".55" filter="url(#jkiSoft)"/><ellipse cx="${cx}" cy="${cy}" rx="${rx - 2}" ry="${ry - 2}" fill="none" stroke="#6a4a26" stroke-width="5" opacity=".7"/>`).join("")}
      ${[260, 420, 1380, 1560].map((y) => `<path d="M-100,${y}Q${W / 2},${y + 30} ${W + 100},${y}" stroke="#2a1c0c" stroke-width="3" fill="none" opacity=".6"/>`).join("")}</g>`); };
  // the back of the hero's head and shoulders, bottom centre: we are looking over him at whatever he is looking at
  const back = (L, o = {}) => { const W = window.STAGE_W || 1080, H = window.STAGE_H || 1920, c = o.color || "#202a44", s = o.s ?? 1;
    return G((L.screen || L.light), `<g transform="translate(${W / 2},${H}) scale(${s})" opacity="${o.op ?? 0.95}" filter="url(#jkiSoft)"><path d="M-560,0V-300Q-540,-440 -380,-470L-150,-500Q-60,-640 0,-650Q60,-640 150,-500L380,-470Q540,-440 560,-300V0Z" fill="${c}"/><circle cy="-760" r="${o.head ?? 250}" fill="${o.hair || "#1a1410"}"/><path d="M-250,-760Q-260,-900 -140,-990Q0,-1060 140,-990Q260,-900 250,-760Z" fill="${o.hair || "#1a1410"}"/></g>`); };
  // bird's-eye: the town plaza rushing up at us while we fall (an overlay for the first beat of a shot), then gone
  const topdownTown = (tl, L, at, dur, o = {}) => { const W = window.STAGE_W || 1080, H = window.STAGE_H || 1920, cx = W / 2, cy = H / 2;
    let r0 = o.seed || 23; const rnd = () => { r0 = (r0 * 16807) % 2147483647; return (r0 - 1) / 2147483646; };
    const roofs = ["#a8484a", "#8a5a3a", "#6a5a7a", "#b86a3a", "#7a3a3a"]; let h = `<rect x="-2000" y="-2000" width="4000" height="4000" fill="#b8a488"/><circle r="430" fill="url(#jkCobble)"/><circle r="430" fill="#8a6a4a" opacity=".12"/>`;
    for (let k = 0; k < 26; k++) { const a = rnd() * 6.283, d = 520 + rnd() * 600, w = 110 + rnd() * 120, hh = 90 + rnd() * 90, x = Math.cos(a) * d, y = Math.sin(a) * d, c = roofs[k % 5], rot = (rnd() * 40 - 20).toFixed(0);
      h += `<g transform="translate(${x.toFixed(0)},${y.toFixed(0)}) rotate(${rot})"><rect x="${-w / 2 + 14}" y="${-hh / 2 + 18}" width="${w}" height="${hh}" fill="#000" opacity=".22"/><rect x="${-w / 2}" y="${-hh / 2}" width="${w}" height="${hh}" fill="${c}"/><path d="M${-w / 2},0H${w / 2}" stroke="#000" stroke-opacity=".25" stroke-width="6"/><rect x="${-w / 2}" y="${-hh / 2}" width="${w}" height="${hh / 2}" fill="#fff" opacity=".12"/></g>`; }
    h += `<g transform="translate(0,-520)"><rect x="-266" y="-176" width="520" height="340" fill="#000" opacity=".25"/><rect x="-280" y="-190" width="520" height="340" fill="#7a3a3a"/><path d="M-280,-20H240" stroke="#000" stroke-opacity=".3" stroke-width="8"/><rect x="-280" y="-190" width="520" height="170" fill="#fff" opacity=".12"/></g>
      <g transform="translate(-300,120)"><circle r="92" fill="#9aa4ac"/><circle r="70" fill="#8ac0d8"/><circle r="22" fill="#a8b0b8"/></g>
      ${[[80, -60, "#d8443a"], [140, 40, "#3a6aa8"], [-40, 220, "#e8d8b8"], [260, 160, "#5a5e66"], [-180, -220, "#f6a830"]].map(([x, y, c]) => `<circle cx="${x}" cy="${y}" r="13" fill="${c}"/><circle cx="${x}" cy="${y - 10}" r="8" fill="#c8a080"/>`).join("")}
      <g transform="translate(-540,-300)"><rect x="-120" y="-30" width="240" height="60" fill="#d8443a"/>${[...Array(4)].map((_, k) => `<rect x="${-120 + k * 60}" y="-30" width="30" height="60" fill="#f4ecd8"/>`).join("")}</g>`;
    const g = G((L.screen || L.light), `<g id="${o.id || "tdown"}"><g transform="translate(${cx},${cy})"><g class="td-in">${h}</g></g><rect x="-100" y="-100" width="${W + 200}" height="${H + 200}" fill="#fff" opacity="0" class="td-fl"/></g>`);
    const inner = g.querySelector(".td-in"), fl = g.querySelector(".td-fl");
    tl.set(g, { opacity: 0 }, 0); tl.set(g, { opacity: 1 }, at);
    tl.fromTo(inner, { scale: o.from ?? 0.32, rotation: o.rot ?? -6, svgOrigin: "0 0" }, { scale: o.to ?? 3.4, rotation: 0, svgOrigin: "0 0", duration: dur, ease: "power2.in", immediateRender: false }, at);
    tl.fromTo(fl, { opacity: 0 }, { opacity: 1, duration: 0.12, ease: "power1.in", immediateRender: false }, at + dur - 0.12); tl.set(g, { opacity: 0 }, at + dur);
    tl.fromTo(fl, { opacity: 1 }, { opacity: 0, duration: 0.25, immediateRender: false }, at + dur); tl.set(fl, { opacity: 0 }, at + dur + 0.26); return g; };
  // looking up the shaft while falling: the bright manhole opening shrinks, brick rings rush outward past us
  const shaftPOV = (tl, L, at, dur, o = {}) => { const W = window.STAGE_W || 1080, H = window.STAGE_H || 1920, cx = W / 2, cy = o.cy ?? 760;
    let rings = ""; for (let k = 0; k < 7; k++) rings += `<circle class="sh-r" cx="${cx}" cy="${cy}" r="120" fill="none" stroke="#5a4a44" stroke-width="40" stroke-dasharray="46 22" opacity="0"/>`;
    const g = G((L.screen || L.light), `<g id="${o.id || "shaft"}"><rect x="-100" y="-100" width="${W + 200}" height="${H + 200}" fill="#07060a"/>${rings}
      <circle class="sh-o" cx="${cx}" cy="${cy}" r="500" fill="#f6d8a0"/><circle class="sh-o2" cx="${cx}" cy="${cy}" r="500" fill="url(#jkSun)" opacity=".8"/><path class="sh-me" d="M${cx - 60},${cy - 180}q60,-80 120,0v120q-60,40 -120,0z" fill="#1a1a22" opacity=".9"/></g>`);
    tl.set(g, { opacity: 0 }, 0); tl.set(g, { opacity: 1 }, at);
    [".sh-o", ".sh-o2"].forEach((c) => tl.fromTo(g.querySelector(c), { attr: { r: 520 } }, { attr: { r: 26 }, duration: dur, ease: "power2.out", immediateRender: false }, at));
    tl.fromTo(g.querySelector(".sh-me"), { scale: 1, svgOrigin: `${cx} ${cy}` }, { scale: 0.05, svgOrigin: `${cx} ${cy}`, duration: dur, ease: "power2.out", immediateRender: false }, at);
    [...g.querySelectorAll(".sh-r")].forEach((r, k) => { const p = 0.55, ph = (k / 7) * p, reps = Math.ceil(dur / p) + 1;
      tl.fromTo(r, { attr: { r: 60 }, opacity: 0.9 }, { attr: { r: 1400 }, opacity: 0, duration: p, repeat: reps, ease: "power1.in", immediateRender: false }, at + ph); });
    tl.set(g, { opacity: 0 }, at + dur + 0.01); return g; };
  window.JKC = { move, dutch, hand, pov, impact, ots, rack, whipOut, whipIn, bars, bucketPOV, back, topdownTown, shaftPOV };
})();
