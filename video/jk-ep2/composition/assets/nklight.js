// นิวเคลียร์ลงกรุงเทพ v3 · light and shadow for the flat cast: every scene gets a source you can point at (the blast behind the car,
// daylight down the car-park ramp, the gap under the steel door, a battery lantern) and the cast answers it.
//   NkL.cast(L, sid, actors, o)      shadows on the floor: a live <use> of each actor, flipped about its ground line, squashed (o.k) and
//                                    sheared (o.sh) away from the light, blurred, fading with distance (follows every pose and step)
//   NkL.wall(L, sid, actors, o)      shadows thrown up on the wall behind by a low light in front (o.lx, o.ly, o.m enlargement)
//   NkL.filter(sid, idx, name)       put a look on an actor's body: "nkSil" backlit silhouette with a warm rim · "nkBack" rim from
//                                    behind, colours kept · "nkBack2" stronger backlight · "nkSide" key from the right, shade on the left
//   NkL.beams(tl, layer, t0, dur, o) soft shafts from a source segment to a target segment, breathing; o.motes adds dust drifting in them
//   NkL.pool(layer, x, y, rx, ry, col, op)  a pool of light on the floor (screen)
//   NkL.feet(tl, layer, t0, dur, o)  the feet of someone outside, cutting the light under the shutter, their shadows streaming in
//   NkL.lantern(tl, L, x, y, s, t0, dur)  a battery lantern on the floor, its warm pool flickering
(function () {
  const NS = "http://www.w3.org/2000/svg", f1 = (v) => (+v).toFixed(1);
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  let seq = 0;
  const nid = (p) => `${p}${seq++}`;
  const rimEdges = (d) => `<feOffset in="SourceAlpha" dx="0" dy="${d}" result="o1"/><feComposite in="SourceAlpha" in2="o1" operator="out" result="e1"/>
      <feOffset in="SourceAlpha" dx="${d}" dy="0" result="o2"/><feComposite in="SourceAlpha" in2="o2" operator="out" result="e2"/>
      <feOffset in="SourceAlpha" dx="${-d}" dy="0" result="o3"/><feComposite in="SourceAlpha" in2="o3" operator="out" result="e3"/>
      <feMerge result="rimA"><feMergeNode in="e1"/><feMergeNode in="e2"/><feMergeNode in="e3"/></feMerge>`;
  const darken = (k, kb = k + 0.04, lift = 0.02) => `<feComponentTransfer in="SourceGraphic" result="dk"><feFuncR type="linear" slope="${k}" intercept="${lift}"/><feFuncG type="linear" slope="${k}" intercept="${lift}"/><feFuncB type="linear" slope="${kb}" intercept="${lift + 0.02}"/></feComponentTransfer>`;
  Sets.DEFS += `
    <filter id="nkSh" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="sRGB">
      <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0.03  0 0 0 0 0.04  0 0 0 0 0.08  0 0 0 1 0" result="a"/><feGaussianBlur in="a" stdDeviation="5"/></filter>
    <filter id="nkSil" x="-20%" y="-10%" width="140%" height="120%" color-interpolation-filters="sRGB">${darken(0.07, 0.1, 0.01)}${rimEdges(5)}
      <feFlood flood-color="#ffd49a"/><feComposite in2="rimA" operator="in" result="rim"/><feGaussianBlur in="rim" stdDeviation="1.1" result="rimS"/>
      <feMerge><feMergeNode in="dk"/><feMergeNode in="rimS"/></feMerge></filter>
    <filter id="nkBack" x="-20%" y="-10%" width="140%" height="120%" color-interpolation-filters="sRGB">${darken(0.8, 0.84, 0)}${rimEdges(4)}
      <feFlood flood-color="#ffcf96" flood-opacity=".9"/><feComposite in2="rimA" operator="in" result="rim"/><feGaussianBlur in="rim" stdDeviation="1" result="rimS"/>
      <feMerge><feMergeNode in="dk"/><feMergeNode in="rimS"/></feMerge></filter>
    <filter id="nkBack2" x="-20%" y="-10%" width="140%" height="120%" color-interpolation-filters="sRGB">${darken(0.46, 0.52, 0.01)}${rimEdges(5)}
      <feFlood flood-color="#ffd9a6"/><feComposite in2="rimA" operator="in" result="rim"/><feGaussianBlur in="rim" stdDeviation="1.2" result="rimS"/>
      <feMerge><feMergeNode in="dk"/><feMergeNode in="rimS"/></feMerge></filter>
    <filter id="nkSide" x="-20%" y="-10%" width="140%" height="120%" color-interpolation-filters="sRGB">
      <feOffset in="SourceAlpha" dx="5" dy="1" result="o1"/><feComposite in="SourceAlpha" in2="o1" operator="out" result="rA"/>
      <feFlood flood-color="#fff0d0" flood-opacity=".75"/><feComposite in2="rA" operator="in" result="rim"/>
      <feOffset in="SourceAlpha" dx="-30" dy="-3" result="o2"/><feComposite in="SourceAlpha" in2="o2" operator="out" result="sA"/>
      <feGaussianBlur in="sA" stdDeviation="9" result="sB"/><feComposite in="sB" in2="SourceAlpha" operator="in" result="sC"/>
      <feFlood flood-color="#141a2c" flood-opacity=".42"/><feComposite in2="sC" operator="in" result="shd"/>
      <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="shd"/><feMergeNode in="rim"/></feMerge></filter>`;

  const NkL = {};
  // floor shadows: matrix flips about the ground line gy, squashes by k and shears by sh (x' = x + sh·(gy − y), y' = gy + k·(gy − y))
  NkL.cast = (L, sid, actors, o = {}) => actors.forEach((a, i) => {
    if (o.only && !o.only.includes(i)) return;
    const aid = `${sid}-a${i}`; if (!document.getElementById(aid)) return;
    const gy = a.y + (o.dy ?? 2), k = o.k ?? 0.5, sh = o.sh ?? -0.3, len = (o.len ?? 1100) * a.s * Math.max(0.4, k), mid = `${aid}-cm`;
    const g = document.createElementNS(NS, "g");
    g.innerHTML = `<defs><linearGradient id="${mid}-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#bbb"/><stop offset="1" stop-color="#000"/></linearGradient>
        <mask id="${mid}" maskUnits="userSpaceOnUse" x="-4000" y="${f1(gy - 30)}" width="9000" height="${f1(len + 60)}"><rect x="-4000" y="${f1(gy - 30)}" width="9000" height="${f1(len + 60)}" fill="url(#${mid}-g)"/></mask></defs>
      <g mask="url(#${mid})" opacity="${o.op ?? 0.5}"><use href="#${aid}" transform="matrix(1,0,${f1(-sh)},${f1(-k)},${f1(sh * gy)},${f1((1 + k) * gy)})" filter="url(#nkSh)"/></g>`;
    L.act.insertBefore(g, L.act.firstChild);
  });
  // shadows thrown on the wall behind by a low light in front at (lx, ly): an enlargement of the actor about the light
  NkL.wall = (L, sid, actors, o = {}) => actors.forEach((a, i) => {
    if (o.only && !o.only.includes(i)) return;
    const aid = `${sid}-a${i}`; if (!document.getElementById(aid)) return;
    const m = o.m ?? 1.5, lx = o.lx, ly = o.ly, g = document.createElementNS(NS, "g");
    g.innerHTML = `<g opacity="${o.op ?? 0.4}"><use href="#${aid}" transform="translate(${f1(lx)},${f1(ly)}) scale(${m}) translate(${f1(-lx)},${f1(-ly)})" filter="url(#nkSh)"/></g>`;
    L.act.insertBefore(g, L.act.firstChild);
  });
  NkL.filter = (sid, idx, name) => idx.forEach((i) => { const r = document.getElementById(`${sid}-a${i}-root`); if (r) r.setAttribute("filter", `url(#${name})`); });

  NkL.beams = (tl, layer, t0, dur, o) => {
    const r = mk(o.seed || 7), n = o.n ?? 5, id = nid("nlb"), col = o.col || "#ffd9a0";
    const [sx0, sy0, sx1, sy1] = o.src, [dx0, dy0, dx1, dy1] = o.dst;
    const at = (u, ax, ay, bx, by) => [ax + (bx - ax) * u, ay + (by - ay) * u];
    let h = `<defs><linearGradient id="${id}" gradientUnits="userSpaceOnUse" x1="${f1((sx0 + sx1) / 2)}" y1="${f1((sy0 + sy1) / 2)}" x2="${f1((dx0 + dx1) / 2)}" y2="${f1((dy0 + dy1) / 2)}">
      <stop offset="0" stop-color="${col}" stop-opacity="1"/><stop offset=".5" stop-color="${col}" stop-opacity=".5"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient></defs>`;
    const B = [];
    for (let k = 0; k < n; k++) {
      const a = (k + 0.1 + r() * 0.25) / n, b = (k + 0.55 + r() * 0.4) / n;
      const p = [at(a, sx0, sy0, sx1, sy1), at(b, sx0, sy0, sx1, sy1), at(b, dx0, dy0, dx1, dy1), at(a, dx0, dy0, dx1, dy1)];
      const op = (o.op ?? 0.3) * (0.55 + r() * 0.45);
      h += `<path id="${id}-b${k}" d="M${p.map((q) => q.map(f1).join(",")).join("L")}Z" fill="url(#${id})" opacity="${f1(op)}"/>`; B.push(op);
    }
    const g = document.createElementNS(NS, "g"); layer.appendChild(g);
    g.innerHTML = h; g.style.mixBlendMode = "screen"; g.style.filter = `blur(${o.blur ?? 10}px)`;
    B.forEach((op, k) => { const per = 1.1 + r() * 0.9, n2 = Math.max(1, Math.ceil(dur / per));
      tl.fromTo(`#${id}-b${k}`, { opacity: op * 0.55 }, { opacity: op, duration: per, repeat: n2 * 2 - 1, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + r() * 0.4); });
    if (o.motes) RabFX.motes(tl, o.motesLayer || layer, t0, dur, { box: o.motes, n: o.moteN ?? 22, seed: o.seed || 7 });
    return g;
  };
  NkL.pool = (layer, x, y, rx, ry, col = "#ffd9a0", op = 0.4) => { const gid = nid("nlp");
    layer.insertAdjacentHTML("beforeend", `<defs><radialGradient id="${gid}"><stop offset="0" stop-color="${col}" stop-opacity="1"/><stop offset=".5" stop-color="${col}" stop-opacity=".45"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></radialGradient></defs>
      <ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx)}" ry="${f1(ry)}" fill="url(#${gid})" opacity="${op}" style="mix-blend-mode:screen"/>`); };

  // the feet of someone standing outside the closed shutter: two dark shapes walk into the light strip (bottom y, door x 140–940),
  // their shadows streaming across the floor toward the camera; they shift on each knock and stay
  NkL.feet = (tl, layer, t0, dur, o = {}) => {
    const id = nid("nlf"), y = o.y ?? 1500, x = o.x ?? 540, knocks = o.knocks || [];
    const foot = (dx) => `<g transform="translate(${dx},0)"><rect x="-34" y="${y - 2}" width="68" height="30" rx="9" fill="#100a08"/>
      <path d="M-34,${y + 28}L34,${y + 28}L118,1960L-118,1960Z" fill="#05070a" opacity=".42"/></g>`;
    layer.insertAdjacentHTML("beforeend", `<g id="${id}" style="filter:blur(2.5px)"><g id="${id}-l">${foot(-52)}</g><g id="${id}-r">${foot(48)}</g></g>`);
    if (o.still) tl.set(`#${id}`, { x }, t0);
    else { const a = t0 + (o.at ?? 0.3);
      tl.fromTo(`#${id}`, { x: x + 620, opacity: 0 }, { x, opacity: 1, duration: 0.9, ease: "power2.out" }, a);
      [["l", 0], ["r", 0.22]].forEach(([s, d]) => tl.fromTo(`#${id}-${s}`, { y: 0 }, { y: -6, duration: 0.11, repeat: 5, yoyo: true, ease: "sine.inOut", immediateRender: false }, a + d)); }
    knocks.forEach((k) => tl.to(`#${id}-r`, { x: 10, duration: 0.06, yoyo: true, repeat: 1, ease: "power1.out" }, t0 + k));
    return id;
  };
  // a floor shadow for any element (a prop, the side-on cat) standing on gy
  NkL.castEl = (L, elId, gy, o = {}) => { const k = o.k ?? 0.5, sh = o.sh ?? 0, len = o.len ?? 600, mid = nid("nlc"), g = document.createElementNS(NS, "g");
    g.innerHTML = `<defs><linearGradient id="${mid}-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#bbb"/><stop offset="1" stop-color="#000"/></linearGradient>
        <mask id="${mid}" maskUnits="userSpaceOnUse" x="-4000" y="${f1(gy - 30)}" width="9000" height="${f1(len + 60)}"><rect x="-4000" y="${f1(gy - 30)}" width="9000" height="${f1(len + 60)}" fill="url(#${mid}-g)"/></mask></defs>
      <g mask="url(#${mid})" opacity="${o.op ?? 0.5}"><use href="#${elId}" transform="matrix(1,0,${f1(-sh)},${f1(-k)},${f1(sh * gy)},${f1((1 + k) * gy)})" filter="url(#nkSh)"/></g>`;
    L.act.insertBefore(g, L.act.firstChild); };
  NkL.lantern = (tl, L, x, y, s, t0, dur) => {
    const id = nid("nll");
    L.act.insertAdjacentHTML("beforeend", `<g transform="translate(${x},${y}) scale(${s})"><rect x="-26" y="-74" width="52" height="64" rx="10" fill="#2c3036"/><rect x="-18" y="-66" width="36" height="46" rx="6" fill="#fff2c8"/>
      <rect x="-30" y="-14" width="60" height="16" rx="5" fill="#3a3e46"/><path d="M-16,-74Q0,-104 16,-74" fill="none" stroke="#3a3e46" stroke-width="7"/></g>`);
    L.glow.insertAdjacentHTML("beforeend", `<defs><radialGradient id="${id}-g"><stop offset="0" stop-color="#ffe2a6" stop-opacity=".95"/><stop offset=".35" stop-color="#ffb866" stop-opacity=".42"/><stop offset="1" stop-color="#ff9a4a" stop-opacity="0"/></radialGradient></defs>
      <g id="${id}" style="mix-blend-mode:screen"><circle cx="${x}" cy="${y - 44 * s}" r="${f1(520 * s)}" fill="url(#${id}-g)"/></g>`);
    const r = mk(31); for (let t = 0; t < dur; ) { const d = 0.07 + r() * 0.12; tl.to(`#${id}`, { opacity: 0.8 + r() * 0.2, duration: d, ease: "none" }, t0 + t); t += d; }
  };
  window.NkL = NkL;
})();
