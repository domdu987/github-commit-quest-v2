// ---------- ทางกลับบ้าน · in-world cards (load after war3.js; owner 1 Nov: "ให้เข้าตามธีมเรื่อง" — no UI boxes) ----------
// Every card is a thing a soldier on this border would carry or leave in the field:
//   WarUI.cover   the squad's FIELD NOTEBOOK: canvas-bound, ruled paper with dirt smudges and a folded corner, two pencil sketches
//                 (behind a bush → the line goes through ✗ / behind a trunk → it stops ✓) drawn stroke by stroke; a stub pencil on a
//                 string and a brass compass swing off the binding
//   WarUI.steps   a CANVAS MAP CASE strap: olive canvas, stitched edges, a buckle; each step is stencil-sprayed with a mist puff and a
//                 riveted tin badge; the strap sways
//   War.spot      a spray-paint ring on the ground around the thing + a CARDBOARD TAG tied with string to a stake beside it
//                 (stencil text), swinging on its knot
//   War.runLine   a chalk-dotted path and a red SPRAY-PAINTED ✗ with drips, over a spray-painted danger ring
//   WarUI.choice  a notebook page "ถ้าเป็นคุณ?" with two hand-drawn tick boxes; the pencil ticks the right one, red pencil crosses the other
(function () {
  const INK = "#2a2420", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const O = (w = 4, c = INK) => `stroke="${c}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  let seq = 0; const nid = () => "wn" + (seq++);
  Sets.DEFS += `
    <linearGradient id="wnPaper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6efd8"/><stop offset="1" stop-color="#e6dabb"/></linearGradient>
    <linearGradient id="wnCanvas" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a8248"/><stop offset=".5" stop-color="#666e3a"/><stop offset="1" stop-color="#4e5428"/></linearGradient>
    <linearGradient id="wnCard" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8b884"/><stop offset="1" stop-color="#b8945e"/></linearGradient>
    <linearGradient id="wnBrass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2d68a"/><stop offset=".5" stop-color="#c89a3a"/><stop offset="1" stop-color="#8a6420"/></linearGradient>
    <linearGradient id="wnTin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8ecef"/><stop offset=".6" stop-color="#a8b0b8"/><stop offset="1" stop-color="#6a747e"/></linearGradient>
    <radialGradient id="wnMist"><stop offset="0" stop-color="#fffaf0" stop-opacity=".7"/><stop offset="1" stop-color="#fffaf0" stop-opacity="0"/></radialGradient>
    <radialGradient id="wnSmudge"><stop offset="0" stop-color="#6a5038" stop-opacity=".22"/><stop offset="1" stop-color="#6a5038" stop-opacity="0"/></radialGradient>
    <filter id="wnRough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".04" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter>
    <filter id="wnSprayS" x="-5%" y="-10%" width="110%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="1" seed="5" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.2"/></filter>
    <filter id="wnSpray" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="1" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="7"/></filter>`;
  // pencil line helper: a path drawn on with pathLength
  const pen = (d, c = "#3a3a44", w = 5, id = "") => `<path ${id ? `id="${id}"` : ""} d="${d}" stroke="${c}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" filter="url(#wnRough)"/>`;
  const drawOn = (tl, sel, t, d = 0.5) => tl.fromTo(sel, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: d, ease: "power1.inOut", immediateRender: false }, t);
  const stencil = (x, y, txt, size, fill, anchor = "middle") => { // stencil letters: the bridges are thin cuts in the paint
    return `<g><text x="${x}" y="${y}" font-family="Kanit" font-weight="900" font-size="${size}" fill="${fill}" text-anchor="${anchor}" letter-spacing="2" filter="url(#wnSpray)">${txt}</text>
      <path d="M${x - 600},${y - size * 0.38}H${x + 600}M${x - 600},${y - size * 0.12}H${x + 600}" stroke="currentColor" stroke-width="0"/></g>`; };

  // ---------------- the field notebook ----------------
  const notebook = (x, y, w, h, id, seed) => { const r = mk(seed);
    let lines = ""; for (let yy = y + 90; yy < y + h - 30; yy += 46) lines += `<path d="M${x + 24},${yy}H${x + w - 24}" stroke="#a8bcd0" stroke-width="2" opacity=".55"/>`;
    let smudge = ""; for (let k = 0; k < 4; k++) smudge += `<ellipse cx="${f1(x + 60 + r() * (w - 120))}" cy="${f1(y + 60 + r() * (h - 120))}" rx="${f1(40 + r() * 60)}" ry="${f1(20 + r() * 30)}" fill="url(#wnSmudge)"/>`;
    return `<rect x="${x - 26}" y="${y - 22}" width="${w + 52}" height="${h + 52}" rx="22" fill="#3a3a22" transform="translate(10,14)" opacity=".5"/>
      <rect x="${x - 26}" y="${y - 22}" width="${w + 52}" height="${h + 52}" rx="22" fill="url(#wnCanvas)" ${O(5)}/>
      <path d="M${x - 14},${y - 10}H${x + w + 14}V${y + h + 18}H${x - 14}Z" fill="none" stroke="#a8ac70" stroke-width="3" stroke-dasharray="10 8" opacity=".7"/>
      <path d="M${x},${y}H${x + w - 70}L${x + w},${y + 70}V${y + h}H${x}Z" fill="url(#wnPaper)" ${O(3)}/>
      <path d="M${x + w - 70},${y}V${y + 70}H${x + w}Z" fill="#d8cca8" ${O(3)}/>
      <path d="M${x + 70},${y + 4}V${y + h - 4}" stroke="#e08a8a" stroke-width="2.4" opacity=".7"/>${lines}${smudge}
      <path d="M${x + 6},${y + h - 14}q60,-8 120,4" stroke="#8a6a48" stroke-width="5" opacity=".2" fill="none"/>`; };
  const tools = (x, y, id) => `<g transform="translate(${x},${y})"><g id="${id}-pc"><path d="M0,0Q-6,90 2,170" stroke="#d8c8a0" stroke-width="3" fill="none"/>
      <g transform="translate(2,170) rotate(8)"><rect x="-9" y="0" width="18" height="110" fill="#e8b830" ${O(3)}/><path d="M-9,110L0,140L9,110Z" fill="#f2d8a8" ${O(3)}/><path d="M-3,132L0,140L3,132Z" fill="#3a3a44"/><rect x="-9" y="-12" width="18" height="14" fill="#c8c0b0" ${O(2.5)}/></g></g></g>
    <g transform="translate(${x + 70},${y - 6})"><g id="${id}-cp"><path d="M0,0V60" stroke="#6a5030" stroke-width="5"/><g transform="translate(0,96)"><circle r="40" fill="url(#wnBrass)" ${O(4)}/><circle r="30" fill="#f6efd8" ${O(2.5)}/>
      <g id="${id}-nd"><path d="M0,-24L6,0L0,24L-6,0Z" fill="#c8282a"/><path d="M0,24L6,0L-6,0Z" fill="#3a3a44"/></g><text y="-14" font-family="Kanit" font-weight="900" font-size="12" fill="${INK}" text-anchor="middle">N</text></g></g></g>`;
  const toolsLife = (tl, id, t0, dur) => {
    tl.fromTo(`#${id}-pc`, { rotation: -10, transformOrigin: "50% 0%" }, { rotation: 10, transformOrigin: "50% 0%", duration: 0.95, repeat: Math.ceil(dur / 0.95), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-cp`, { rotation: 6, transformOrigin: "50% 0%" }, { rotation: -6, transformOrigin: "50% 0%", duration: 1.2, repeat: Math.ceil(dur / 1.2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.2);
    tl.fromTo(`#${id}-nd`, { rotation: -30, transformOrigin: "50% 50%" }, { keyframes: [{ rotation: 25, duration: 0.6, ease: "sine.inOut" }, { rotation: -8, duration: 0.6, ease: "sine.inOut" }, { rotation: 4, duration: 0.8, ease: "sine.inOut" }], repeat: Math.ceil(dur / 2), yoyo: true, immediateRender: false }, t0);
  };
  // the sketches: a crouching man in pencil, a bush / a trunk, the bullet line
  const sketchMan = (x, y, s, id) => `<g transform="translate(${x},${y}) scale(${s})">${pen("M-20,-140a26,26 0 1 0 0.1,0Z", "#3a3a44", 5, `${id}-h`)}${pen("M-50,-150Q-20,-178 12,-150", "#3a3a44", 6, `${id}-hm`)}
    ${pen("M-24,-112Q-46,-60 -30,-4L30,-2Q40,-56 14,-108", "#3a3a44", 5, `${id}-b`)}${pen("M-30,-4L-64,34L-20,40M30,-2L52,40", "#3a3a44", 5, `${id}-l`)}${pen("M-14,-96Q-44,-110 -34,-150", "#3a3a44", 5, `${id}-a`)}</g>`;
  const sketchBush = (x, y, id) => pen(`M${x - 150},${y}Q${x - 170},${y - 90} ${x - 110},${y - 110}Q${x - 100},${y - 170} ${x - 30},${y - 160}Q${x + 10},${y - 210} ${x + 70},${y - 160}Q${x + 140},${y - 170} ${x + 140},${y - 100}Q${x + 190},${y - 60} ${x + 150},${y}`, "#4a7a30", 6, id)
    + pen(`M${x - 90},${y - 70}q20,-10 30,4M${x + 10},${y - 120}q16,-12 30,0M${x + 70},${y - 60}q16,-10 26,4M${x - 40},${y - 30}q14,-8 26,2`, "#4a7a30", 4, id + "x");
  const sketchTrunk = (x, y, id) => pen(`M${x - 60},${y}Q${x - 52},${y - 160} ${x - 44},${y - 320}M${x + 60},${y}Q${x + 52},${y - 160} ${x + 44},${y - 320}M${x - 44},${y - 320}Q${x},${y - 336} ${x + 44},${y - 320}`, "#6a4a2a", 6, id)
    + pen(`M${x - 20},${y - 60}q6,-60 0,-120M${x + 18},${y - 100}q-6,-60 4,-120`, "#6a4a2a", 3.4, id + "x");
  WarUI.cover = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), Y = o.y ?? 360, X = 110, W = 860, PH = 520;
    const page = (py, good) => { const p = `${id}-${good ? "g" : "b"}`, gy = py + 420;
      return `${good ? "" : ""}<text x="${X + 100}" y="${py + 70}" font-family="Sriracha" font-size="60" fill="${good ? "#1e6a3a" : "#a8241e"}">${good ? "กันกระสุน" : "บังตา"}</text>
        ${pen(`M${X + 96},${py + 86}Q${X + 220},${py + 96} ${X + (good ? 380 : 270)},${py + 84}`, good ? "#1e6a3a" : "#a8241e", 6, `${p}-u`)}
        ${pen(`M${X + 40},${gy}Q${X + W / 2},${gy - 8} ${X + W - 40},${gy + 2}`, "#6a5038", 5, `${p}-gr`)}
        ${sketchMan(X + 300, gy, 1.15, `${p}-m`)}${good ? sketchTrunk(X + 560, gy, `${p}-t`) : sketchBush(X + 560, gy, `${p}-t`)}
        ${pen(`M${X + W - 40},${gy - 190}H${good ? X + 620 : X + 330}M${good ? X + 640 : X + 350},${gy - 204}L${good ? X + 620 : X + 330},${gy - 190}L${good ? X + 640 : X + 350},${gy - 176}`, "#c8282a", 8, `${p}-ln`)}
        ${good ? pen(`M${X + 608},${gy - 210}l-16,20M${X + 612},${gy - 186}l-22,4M${X + 606},${gy - 168}l-18,-12`, "#6a4a2a", 4, `${p}-ch`) : ""}
        <g transform="translate(${X + W - 110},${py + 70})">${good ? pen("M-34,0l24,28l52,-64", "#1e8a48", 14, `${p}-mk`) : pen("M-34,-34L34,34M34,-34L-34,34", "#c8282a", 14, `${p}-mk`)}</g>`; };
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-m"><g id="${id}-sw">
      ${notebook(X, Y, W, PH * 2 + 40, id, 21)}<path d="M${X + 10},${Y + PH + 20}H${X + W - 10}" stroke="#a8bcd0" stroke-width="3" stroke-dasharray="12 8"/>
      ${page(Y, false)}${page(Y + PH + 40, true)}${tools(X + W + 10, Y + 40, id)}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 1 }, t0);
    // in: the notebook slaps down from above, lands with a bounce, then breathes as if held
    tl.fromTo(`#${id}-m`, { y: -1500, rotation: -8, transformOrigin: "50% 50%" }, { y: 0, rotation: 0, transformOrigin: "50% 50%", duration: 0.55, ease: "back.out(1.3)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: -0.8, transformOrigin: "50% 100%" }, { rotation: 0.8, transformOrigin: "50% 100%", duration: 1.4, repeat: Math.ceil(dur / 1.4), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.55);
    toolsLife(tl, id, t0 + 0.4, dur);
    ["b", "g"].forEach((p, k) => { const s = `#${id}-${p}`, tb = t0 + 0.55 + k * (o.gap ?? 1.15);
      drawOn(tl, `${s}-u`, tb, 0.3); drawOn(tl, `${s}-gr`, tb + 0.1, 0.3);
      ["h", "hm", "b", "l", "a"].forEach((q, j) => drawOn(tl, `${s}-m-${q}`, tb + 0.15 + j * 0.06, 0.25));
      drawOn(tl, `${s}-t`, tb + 0.3, 0.35); drawOn(tl, `${s}-tx`, tb + 0.5, 0.2);
      drawOn(tl, `${s}-ln`, tb + 0.6, 0.3); if (p === "g") drawOn(tl, `${s}-ch`, tb + 0.88, 0.12);
      drawOn(tl, `${s}-mk`, tb + 0.92, 0.22);
      if (p === "b") RabFX.shakeSel(tl, `#${id}-sw`, tb + 1.0, 8); });
    if (o.out !== false && o.out !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };

  // ---------------- the canvas map-case strap with stencilled steps ----------------
  WarUI.steps = (tl, layer, t0, items, o = {}) => {
    const id = nid(), Y = o.y ?? 300, n = items.length, X = 50, W = 980, H = 280, cw = (W - 80) / n;
    let cells = "";
    items.forEach((it, k) => { const cx = X + 40 + cw * (k + 0.5);
      cells += `<g id="${id}-c${k}"><g transform="translate(${cx},${Y + 90})"><g id="${id}-bd${k}" opacity="0"><circle r="58" fill="#2a2a1a" opacity=".35" transform="translate(4,6)"/><circle r="58" fill="url(#wnTin)" ${O(3.5)}/>
          ${[[-44, -36], [44, -36], [-44, 36], [44, 36]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="4" fill="#5a646e"/>`).join("")}<g transform="translate(-50,-56) scale(.83)">${War.coin(it.icon, 0, 0, 1, `${id}-ic${k}`)}</g></g></g>
        <g transform="translate(${cx},${Y + 232})"><g id="${id}-t${k}" opacity="0"><text x="0" y="0" font-family="Kanit" font-weight="900" font-size="${it.text.length > 8 ? 36 : 46}" fill="${it.red ? "#ffd8a8" : "#fbf6e6"}" text-anchor="middle" letter-spacing="1" stroke="#2a2a14" stroke-width="2" paint-order="stroke" filter="url(#wnSprayS)">${it.text}</text></g>
          <g id="${id}-ms${k}" opacity="0"><ellipse cx="0" cy="-14" rx="${cw * 0.5}" ry="40" fill="url(#wnMist)"/></g></g></g>`; });
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-m"><g id="${id}-sw">
      <path d="M${X - 40},${Y - 40}L${X + 40},${Y}" stroke="#3a3a22" stroke-width="28"/><path d="M${X + W + 40},${Y - 40}L${X + W - 40},${Y}" stroke="#3a3a22" stroke-width="28"/>
      <rect x="${X}" y="${Y}" width="${W}" height="${H}" rx="26" fill="#2a2a14" opacity=".45" transform="translate(8,12)"/>
      <rect x="${X}" y="${Y}" width="${W}" height="${H}" rx="26" fill="url(#wnCanvas)" ${O(5)}/>
      <rect x="${X + 12}" y="${Y + 12}" width="${W - 24}" height="${H - 24}" rx="18" fill="none" stroke="#a8ac70" stroke-width="3" stroke-dasharray="10 8"/>
      ${Array.from({ length: 30 }, (_, k) => `<path d="M${X + 20 + k * 31},${Y + 16}l12,${H - 32}" stroke="#5a6230" stroke-width="2" opacity=".35"/>`).join("")}
      <g transform="translate(${X + W - 16},${Y + H / 2})"><rect x="-22" y="-40" width="44" height="80" rx="6" fill="none" stroke="url(#wnBrass)" stroke-width="9"/><path d="M0,-34V34" stroke="url(#wnBrass)" stroke-width="6"/></g>
      ${cells}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 1 }, t0 + (items[0].at ?? 0) - 0.15);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    // in: the strap swings down off the shoulder, then keeps swaying
    tl.fromTo(`#${id}-m`, { y: -500, rotation: -6, transformOrigin: "50% 0%" }, { y: 0, rotation: 0, transformOrigin: "50% 0%", duration: 0.5, ease: "back.out(1.4)", immediateRender: false }, t0 + (items[0].at ?? 0) - 0.15);
    tl.fromTo(`#${id}-sw`, { rotation: -1.2, transformOrigin: "50% 0%" }, { rotation: 1.2, transformOrigin: "50% 0%", duration: 1.1, repeat: Math.ceil((o.dur ?? 6) / 1.1) + 1, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (items[0].at ?? 0) + 0.35);
    items.forEach((it, k) => { const t = t0 + it.at;
      tl.fromTo(`#${id}-ms${k}`, { opacity: 0.9, scale: 0.5, transformOrigin: "50% 50%" }, { opacity: 0, scale: 1.4, transformOrigin: "50% 50%", duration: 0.6, ease: "power2.out", immediateRender: false }, t);
      tl.fromTo(`#${id}-t${k}`, { opacity: 0 }, { opacity: 1, duration: 0.12, immediateRender: false }, t + 0.05);
      tl.fromTo(`#${id}-bd${k}`, { opacity: 1, scale: 1.8, rotation: -30, transformOrigin: "50% 50%" }, { scale: 1, rotation: 0, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2.4)", immediateRender: false }, t + 0.1);
      tl.fromTo(`#${id}-bd${k}`, { rotation: -4 }, { rotation: 4, transformOrigin: "50% 50%", duration: 0.7, repeat: Math.ceil((o.dur ?? 6) / 0.7), yoyo: true, ease: "sine.inOut", immediateRender: false }, t + 0.5);
      const el = document.getElementById(`${id}-ic${k}`); RabFX.life(tl, el, t + 0.5, o.dur ?? 6); });
  };

  // ---------------- spray ring + cardboard tag on a stake ----------------
  War.spot = (tl, layer, x, y, t0, dur, o = {}) => {
    const id = nid(), R = o.r ?? 120, label = o.label || "", tw = Math.max(170, label.length * 30 + 60), ly = -R * 0.6;
    const side = o.side ?? 1, gx = side * R * 1.05 + (o.tagDx ?? 0), top = o.top ?? -230;
    put(layer, `<g transform="translate(${x},${y})">
      <ellipse id="${id}-ring" rx="${R}" ry="${f1(R * 0.42)}" cy="${f1(R * 0.25)}" fill="none" stroke="#ff5a3a" stroke-width="12" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" filter="url(#wnSpray)" opacity=".92"/>
      <g transform="translate(${gx},${f1(R * 0.3)})"><g id="${id}-st" opacity="0"><path d="M0,0V${top}" stroke="#7a5a34" stroke-width="12" stroke-linecap="round"/><path d="M-3,0V${top}" stroke="#a8865a" stroke-width="3"/>
        <path d="M0,${top + 14}q-8,6 0,14q8,6 0,14" stroke="#d8c8a0" stroke-width="4" fill="none"/>
        <g transform="translate(0,${top + 40})"><g id="${id}-tg"><path d="M0,0V40" stroke="#d8c8a0" stroke-width="3"/>
          <g transform="translate(${-tw / 2},40)"><path d="M0,12L12,0H${tw - 12}L${tw},12V86H0Z" fill="url(#wnCard)" ${O(3.5)}/><circle cx="${tw / 2}" cy="14" r="6" fill="#f6efd8" ${O(2)}/>
            <path d="M8,80H${tw - 8}" stroke="#8a6a3a" stroke-width="2" opacity=".5"/>
            <text x="${tw / 2}" y="64" font-family="Kanit" font-weight="900" font-size="38" fill="#3a2412" text-anchor="middle" letter-spacing="1" filter="url(#wnSprayS)">${label}</text></g></g></g></g></g></g>`);
    tl.set(`#${id}-st`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}-ring`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.45, ease: "power1.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-st`, { opacity: 1, y: -260 }, { y: 0, duration: 0.3, ease: "power3.in", immediateRender: false }, t0 + 0.25);
    tl.fromTo(`#${id}-st`, { scaleY: 0.92, transformOrigin: "50% 100%" }, { scaleY: 1, transformOrigin: "50% 100%", duration: 0.3, ease: "elastic.out(1.2,0.3)", immediateRender: false }, t0 + 0.55);
    tl.fromTo(`#${id}-tg`, { rotation: 28, transformOrigin: "50% 0%" }, { rotation: 0, transformOrigin: "50% 0%", duration: 1.4, ease: "elastic.out(1,0.25)", immediateRender: false }, t0 + 0.55);
    tl.fromTo(`#${id}-tg`, { rotation: -4 }, { rotation: 4, transformOrigin: "50% 0%", duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 1.9);
    if (o.out) tl.to([`#${id}-ring`, `#${id}-st`], { opacity: 0, duration: 0.2 }, t0 + dur - 0.2);
  };

  // ---------------- chalk path + spray-painted ✗ ----------------
  War.runLine = (tl, layer, a, b, t0, dur, o = {}) => {
    const id = nid(), mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2 - (o.arc ?? 80), zr = o.zr ?? 230;
    put(layer, `<g>
      <ellipse id="${id}-z" cx="${b[0]}" cy="${b[1]}" rx="${zr}" ry="${f1(zr * 0.32)}" fill="none" stroke="#ff4a2a" stroke-width="10" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" filter="url(#wnSpray)"/>
      <path id="${id}-l" d="M${a[0]},${a[1]}Q${mx},${my} ${b[0]},${b[1]}" stroke="#f6f2ea" stroke-width="9" fill="none" stroke-dasharray="6 22" stroke-linecap="round" opacity="0" filter="url(#wnRough)"/>
      <g transform="translate(${mx},${my + (o.arc ?? 80) / 2})"><g id="${id}-x">
        <path id="${id}-x1" d="M-60,-60L60,60" stroke="#e8281e" stroke-width="26" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" filter="url(#wnSpray)"/>
        <path id="${id}-x2" d="M60,-60L-60,60" stroke="#e8281e" stroke-width="26" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" filter="url(#wnSpray)"/>
        <g id="${id}-dr" opacity="0"><path d="M58,66v30M-58,66v22M8,8v34" stroke="#e8281e" stroke-width="7" stroke-linecap="round"/></g></g></g></g>`);
    tl.fromTo(`#${id}-z`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power1.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-l`, { opacity: 0.9, strokeDashoffset: 300 }, { strokeDashoffset: 0, duration: dur, ease: "none", immediateRender: false }, t0 + 0.2);
    const xa = t0 + (o.xAt ?? 0.8);
    tl.fromTo(`#${id}-x1`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.16, ease: "power2.in", immediateRender: false }, xa);
    tl.fromTo(`#${id}-x2`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.16, ease: "power2.in", immediateRender: false }, xa + 0.2);
    tl.fromTo(`#${id}-dr`, { opacity: 1, scaleY: 0, transformOrigin: "50% 0%" }, { scaleY: 1, transformOrigin: "50% 0%", duration: 0.9, ease: "power1.out", immediateRender: false }, xa + 0.4);
    RabFX.flash(tl, xa + 0.2, "#ff2a1a", 0.18);
  };

  // ---------------- the choice: a notebook page with tick boxes ----------------
  WarUI.choice = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), X = 150, Y = 520, W = 780, H = 760, opts = [o.a, o.b];
    const row = (k) => { const y = Y + 330 + k * 200;
      return `<rect x="${X + 70}" y="${y - 60}" width="80" height="80" fill="none" stroke="#3a3a44" stroke-width="5" filter="url(#wnRough)" rx="6"/>
        <g transform="translate(${X + 170},${y - 100}) scale(.95)">${War.coin(opts[k].icon, 0, 0, 1, `${id}-ic${k}`)}</g>
        <text x="${X + 310}" y="${y}" font-family="Sriracha" font-size="56" fill="#2a2a3a">${opts[k].text}</text>
        ${k === (o.pick === "a" ? 0 : 1) ? pen(`M${X + 82},${y - 22}l22,26l52,-70`, "#1e8a48", 13, `${id}-ok`) : pen(`M${X + 74},${y - 64}l74,84M${X + 148},${y - 64}l-74,84`, "#c8282a", 11, `${id}-no`)}`; };
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-m"><g id="${id}-sw">${notebook(X, Y, W, H, id, 33)}
      <text x="${X + W / 2}" y="${Y + 150}" font-family="Sriracha" font-size="70" fill="#a8241e" text-anchor="middle">${o.q || "ถ้าเป็นคุณ?"}</text>
      ${pen(`M${X + 150},${Y + 176}Q${X + W / 2},${Y + 190} ${X + W - 150},${Y + 172}`, "#a8241e", 6, `${id}-u`)}
      ${row(0)}${row(1)}${tools(X + W + 10, Y + 60, id)}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 1 }, t0);
    tl.fromTo(`#${id}-m`, { y: -1500, rotation: 6, transformOrigin: "50% 50%" }, { y: 0, rotation: 0, transformOrigin: "50% 50%", duration: 0.55, ease: "back.out(1.3)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: -0.8, transformOrigin: "50% 100%" }, { rotation: 0.8, transformOrigin: "50% 100%", duration: 1.3, repeat: Math.ceil(dur / 1.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.55);
    toolsLife(tl, id, t0 + 0.4, dur);
    drawOn(tl, `#${id}-u`, t0 + 0.6, 0.35);
    [0, 1].forEach((k) => { const el = document.getElementById(`${id}-ic${k}`); QkUI.iconPop(tl, el, t0 + 0.7 + k * 0.15); RabFX.life(tl, el, t0 + 1.2, dur); });
    drawOn(tl, `#${id}-no`, t0 + (o.mark?.at ?? dur - 1.0), 0.3);
    drawOn(tl, `#${id}-ok`, t0 + (o.pickAt ?? dur - 1.4), 0.3);
    RabFX.shakeSel(tl, `#${id}-sw`, t0 + (o.mark?.at ?? dur - 1.0) + 0.3, 8);
  };
})();
