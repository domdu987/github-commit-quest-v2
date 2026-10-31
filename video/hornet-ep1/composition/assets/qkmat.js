// "ตึกโยก" material kit, shared by quake.js / quake2.js / quakemap.js / quakeui.js (load right after pop2.js, before quake.js).
// The look (skill rule V10): every object has a lit face, a shade face, an edge highlight and a soft contact shadow; light has a source
// (the window / the sun on the right, ceiling lamps from above); surfaces read as a material (wood grain, brushed steel, glass streaks,
// fabric folds). Gradients only — no SVG filters in the sets (they are slow to paint at 1080×1920).
//   Qk.tone(hex, k)                  lighten (k > 0, toward white) or darken (k < 0, toward black) a colour, k in −1…1
//   Qk.cs(cx, cy, rx, ry, op)        a soft contact shadow (radial gradient ellipse) — put one under everything that stands
//   Qk.glowE(cx, cy, rx, ry, col, op) a soft light pool (radial gradient ellipse in col)
//   Qk.poly(pts, attrs)              a closed path through [[x, y]…]
//   Qk.pbox(x0, y0, x1, y1, o)       a box in one-point perspective: the front face x0…x1 × y0…y1, the back face = the front scaled by
//                                    o.k (default 0.9) toward o.vp (default the room's vanishing point 1050, 860); draws the visible side
//                                    face (o.side), the top or bottom face (o.top / o.bottom), then the front (o.front) — each a fill
//                                    string; o.out an outline attr string; o.edge true adds a highlight along the front's top edge
//   Qk.grain(x, y, w, h, seed, o)    wood grain over a rect: long wavy lines and a few knots (o.col, o.op, o.dir "h" | "v")
//   Qk.brushed(x, y, w, h, seed, o)  brushed-metal streaks over a rect (o.dir "v" default | "h")
//   Qk.streaks(x, y, w, h, o)        glass reflection streaks (two diagonal bands) over a rect
//   Qk.folds(x0, x1, y0, y1, n, seed, o)  fabric folds: n vertical light/shade bands between x0 and x1 (curtains, cloth)
//   Qk.knob(x, y, r, col)            a round knob / button with highlight and shadow
//   Qk.handle(x, y, len, o)          a bar handle (o.dir "h" | "v"), brushed with a highlight
(function () {
  const Qk = (window.Qk = window.Qk || {});
  const f1 = (v) => (+v).toFixed(1);
  const mk = (seed) => () => { seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  Qk.mk = mk;
  Qk.f1 = f1;

  Sets.DEFS += `
    <radialGradient id="qkCS"><stop offset="0" stop-color="#140c06" stop-opacity=".5"/><stop offset=".55" stop-color="#140c06" stop-opacity=".2"/><stop offset="1" stop-color="#140c06" stop-opacity="0"/></radialGradient>
    <radialGradient id="qkPoolW"><stop offset="0" stop-color="#fff6dc" stop-opacity=".9"/><stop offset=".45" stop-color="#fff0c8" stop-opacity=".35"/><stop offset="1" stop-color="#fff0c8" stop-opacity="0"/></radialGradient>
    <linearGradient id="qkAOup" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#1e140a" stop-opacity=".32"/><stop offset="1" stop-color="#1e140a" stop-opacity="0"/></linearGradient>
    <linearGradient id="qkAOdn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e140a" stop-opacity=".28"/><stop offset="1" stop-color="#1e140a" stop-opacity="0"/></linearGradient>
    <linearGradient id="qkAOlt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1e140a" stop-opacity=".28"/><stop offset="1" stop-color="#1e140a" stop-opacity="0"/></linearGradient>
    <linearGradient id="qkAOrt" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#1e140a" stop-opacity=".28"/><stop offset="1" stop-color="#1e140a" stop-opacity="0"/></linearGradient>
    <linearGradient id="qkSheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".0"/><stop offset=".42" stop-color="#fff" stop-opacity=".0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset=".58" stop-color="#fff" stop-opacity=".0"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="qkTopLit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".3"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="qkSideDk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient>`;

  const hex = (h) => { h = h.replace("#", ""); if (h.length === 3) h = h.split("").map((c) => c + c).join(""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); };
  Qk.tone = (h, k) => {
    const c = hex(h), t = k >= 0 ? 255 : 0, a = Math.abs(k);
    return "#" + c.map((v) => Math.round(v + (t - v) * a).toString(16).padStart(2, "0")).join("");
  };
  Qk.cs = (cx, cy, rx, ry, op = 1) => `<ellipse cx="${f1(cx)}" cy="${f1(cy)}" rx="${f1(rx)}" ry="${f1(ry)}" fill="url(#qkCS)" opacity="${op}"/>`;
  Qk.glowE = (cx, cy, rx, ry, col = "url(#qkPoolW)", op = 1) => `<ellipse cx="${f1(cx)}" cy="${f1(cy)}" rx="${f1(rx)}" ry="${f1(ry)}" fill="${col}" opacity="${op}"/>`;
  Qk.poly = (pts, attrs = "") => `<path d="M${pts.map((p) => `${f1(p[0])},${f1(p[1])}`).join("L")}Z" ${attrs}/>`;

  Qk.pbox = (x0, y0, x1, y1, o = {}) => {
    const [vx, vy] = o.vp || [1050, 860], k = o.k ?? 0.9, out = o.out || "";
    const B = (x, y) => [vx + (x - vx) * k, vy + (y - vy) * k];
    const [bx0, by0] = B(x0, y0), [bx1, by1] = B(x1, y1);
    let s = "";
    if (x1 < vx && o.side) s += Qk.poly([[x1, y0], [bx1, by0], [bx1, by1], [x1, y1]], `fill="${o.side}" ${out}`);
    if (x0 > vx && o.side) s += Qk.poly([[x0, y0], [bx0, by0], [bx0, by1], [x0, y1]], `fill="${o.side}" ${out}`);
    if (y0 > vy && o.top) s += Qk.poly([[x0, y0], [x1, y0], [bx1, by0], [bx0, by0]], `fill="${o.top}" ${out}`);
    if (y1 < vy && o.bottom) s += Qk.poly([[x0, y1], [x1, y1], [bx1, by1], [bx0, by1]], `fill="${o.bottom}" ${out}`);
    if (o.front !== false) s += `<rect x="${f1(x0)}" y="${f1(y0)}" width="${f1(x1 - x0)}" height="${f1(y1 - y0)}" fill="${o.front || "#ccc"}" ${out}/>`;
    if (o.edge) s += `<path d="M${f1(x0 + 4)},${f1(y0 + 3)}H${f1(x1 - 4)}" stroke="#fff" stroke-width="3" opacity=".45" stroke-linecap="round"/>`;
    return s;
  };

  Qk.grain = (x, y, w, h, seed = 1, o = {}) => {
    const r = mk(seed), col = o.col || "#5a3618", op = o.op ?? 0.22, v = o.dir === "v";
    let s = "";
    const n = Math.max(3, Math.round((v ? w : h) / (o.gap || 14)));
    for (let i = 0; i < n; i++) {
      const t = (i + 0.3 + r() * 0.4) / n, amp = 2 + r() * 5, ph = r() * 6, fr = 0.008 + r() * 0.012;
      let d = "";
      if (v) { const x0 = x + t * w; for (let yy = y; yy <= y + h; yy += 16) d += `${d ? "L" : "M"}${f1(x0 + Math.sin(yy * fr + ph) * amp)},${f1(yy)}`; }
      else { const y0 = y + t * h; for (let xx = x; xx <= x + w; xx += 16) d += `${d ? "L" : "M"}${f1(xx)},${f1(y0 + Math.sin(xx * fr + ph) * amp)}`; }
      s += `<path d="${d}" stroke="${col}" stroke-width="${f1(1 + r() * 1.6)}" fill="none" opacity="${f1(op * (0.5 + r() * 0.7))}"/>`;
    }
    const knots = o.knots ?? Math.round((w * h) / 60000);
    for (let i = 0; i < knots; i++) { const kx = x + w * (0.1 + r() * 0.8), ky = y + h * (0.15 + r() * 0.7); s += `<ellipse cx="${f1(kx)}" cy="${f1(ky)}" rx="${f1(v ? 5 : 12)}" ry="${f1(v ? 12 : 5)}" fill="none" stroke="${col}" stroke-width="1.6" opacity="${f1(op * 1.2)}"/>`; }
    return s;
  };

  Qk.brushed = (x, y, w, h, seed = 1, o = {}) => {
    const r = mk(seed), v = o.dir !== "h";
    let s = "";
    const n = Math.round((v ? w : h) / 6);
    for (let i = 0; i < n; i++) {
      const t = (v ? x : y) + (i / n) * (v ? w : h) + r() * 3, c = r() < 0.5 ? "#fff" : "#2a3238", op = 0.05 + r() * 0.12;
      s += v ? `<path d="M${f1(t)},${f1(y + r() * h * 0.1)}V${f1(y + h - r() * h * 0.1)}" stroke="${c}" stroke-width="${f1(0.8 + r() * 1.4)}" opacity="${f1(op)}"/>`
        : `<path d="M${f1(x + r() * w * 0.1)},${f1(t)}H${f1(x + w - r() * w * 0.1)}" stroke="${c}" stroke-width="${f1(0.8 + r() * 1.4)}" opacity="${f1(op)}"/>`;
    }
    return s;
  };

  Qk.streaks = (x, y, w, h, o = {}) => {
    const op = o.op ?? 0.22, a = Math.min(w, h);
    return `<path d="M${f1(x + w * 0.12)},${f1(y + h)}L${f1(x + w * 0.12 + a * 0.5)},${f1(y)}H${f1(x + w * 0.12 + a * 0.72)}L${f1(x + w * 0.12 + a * 0.22)},${f1(y + h)}Z" fill="#fff" opacity="${op}"/>
      <path d="M${f1(x + w * 0.5)},${f1(y + h)}L${f1(x + w * 0.5 + a * 0.4)},${f1(y)}H${f1(x + w * 0.5 + a * 0.47)}L${f1(x + w * 0.5 + a * 0.07)},${f1(y + h)}Z" fill="#fff" opacity="${f1(op * 0.7)}"/>`;
  };

  Qk.folds = (x0, x1, y0, y1, n, seed = 1, o = {}) => {
    const r = mk(seed), w = (x1 - x0) / n, lit = o.lit || "#fff", dk = o.dk || "#3a2a1a";
    let s = "";
    for (let i = 0; i < n; i++) {
      const x = x0 + i * w, wob = (r() - 0.5) * w * 0.3;
      s += `<path d="M${f1(x + w * 0.15)},${f1(y0)}C${f1(x + w * 0.1 + wob)},${f1(y0 + (y1 - y0) * 0.4)} ${f1(x + w * 0.2 - wob)},${f1(y0 + (y1 - y0) * 0.7)} ${f1(x + w * 0.1)},${f1(y1)}H${f1(x + w * 0.45)}C${f1(x + w * 0.55 - wob)},${f1(y0 + (y1 - y0) * 0.7)} ${f1(x + w * 0.45 + wob)},${f1(y0 + (y1 - y0) * 0.4)} ${f1(x + w * 0.5)},${f1(y0)}Z" fill="${lit}" opacity="${f1(o.litOp ?? 0.28)}"/>`;
      s += `<path d="M${f1(x + w * 0.62)},${f1(y0)}C${f1(x + w * 0.6 - wob)},${f1(y0 + (y1 - y0) * 0.5)} ${f1(x + w * 0.7 + wob)},${f1(y0 + (y1 - y0) * 0.8)} ${f1(x + w * 0.66)},${f1(y1)}H${f1(x + w * 0.92)}C${f1(x + w * 0.95 + wob)},${f1(y0 + (y1 - y0) * 0.8)} ${f1(x + w * 0.88 - wob)},${f1(y0 + (y1 - y0) * 0.5)} ${f1(x + w * 0.9)},${f1(y0)}Z" fill="${dk}" opacity="${f1(o.dkOp ?? 0.16)}"/>`;
    }
    return s;
  };

  Qk.knob = (x, y, r, col = "#c8ccce") => `<circle cx="${f1(x)}" cy="${f1(y + r * 0.25)}" r="${f1(r)}" fill="#000" opacity=".18"/><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(r)}" fill="${col}" stroke="${Qk.tone(col, -0.55)}" stroke-width="${f1(Math.max(1.5, r * 0.18))}"/><circle cx="${f1(x - r * 0.3)}" cy="${f1(y - r * 0.32)}" r="${f1(r * 0.35)}" fill="#fff" opacity=".6"/>`;

  Qk.handle = (x, y, len, o = {}) => {
    const h = o.dir === "h", t = o.t ?? 12, col = o.col || "#b8bec2";
    return h ? `<rect x="${f1(x)}" y="${f1(y + 3)}" width="${f1(len)}" height="${f1(t)}" rx="${f1(t / 2)}" fill="#000" opacity=".2"/><rect x="${f1(x)}" y="${f1(y)}" width="${f1(len)}" height="${f1(t)}" rx="${f1(t / 2)}" fill="${col}" stroke="${Qk.tone(col, -0.5)}" stroke-width="2"/><path d="M${f1(x + t / 2)},${f1(y + t * 0.32)}H${f1(x + len - t / 2)}" stroke="#fff" stroke-width="${f1(t * 0.22)}" opacity=".65" stroke-linecap="round"/>`
      : `<rect x="${f1(x + 3)}" y="${f1(y)}" width="${f1(t)}" height="${f1(len)}" rx="${f1(t / 2)}" fill="#000" opacity=".2"/><rect x="${f1(x)}" y="${f1(y)}" width="${f1(t)}" height="${f1(len)}" rx="${f1(t / 2)}" fill="${col}" stroke="${Qk.tone(col, -0.5)}" stroke-width="2"/><path d="M${f1(x + t * 0.32)},${f1(y + t / 2)}V${f1(y + len - t / 2)}" stroke="#fff" stroke-width="${f1(t * 0.22)}" opacity=".65" stroke-linecap="round"/>`;
  };
})();
