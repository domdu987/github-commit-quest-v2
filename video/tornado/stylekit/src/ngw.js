// นาคเล่นน้ำ (owner 4 Nov 2569: a new story about a tornado — พายุงวงช้าง). The funnel (a waterspout over the lake, a landspout
// over the field), the lake with its bank and the naga shrine, the kuti bathroom, the shadow-puppet legend, the ditch; the cast
// ฝน ปู ยายบัว ตาเทียน. Builds on takhian.js (Sets.tkScape storm world) and rupnak2.js (props).
(() => {
  const INK = "#1e1a16";
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const Ngw = (window.Ngw = window.Ngw || {});
  // a smooth path through points (Catmull-Rom as cubic Béziers)
  const smooth = (P, closed = false) => {
    const n = P.length, g = (i) => P[closed ? (i + n) % n : Math.max(0, Math.min(n - 1, i))];
    let d = `M${f1(P[0][0])},${f1(P[0][1])}`;
    for (let i = 0; i < (closed ? n : n - 1); i++) { const p0 = g(i - 1), p1 = g(i), p2 = g(i + 1), p3 = g(i + 2);
      d += `C${f1(p1[0] + (p2[0] - p0[0]) / 6)},${f1(p1[1] + (p2[1] - p0[1]) / 6)} ${f1(p2[0] - (p3[0] - p1[0]) / 6)},${f1(p2[1] - (p3[1] - p1[1]) / 6)} ${f1(p2[0])},${f1(p2[1])}`; }
    return d + (closed ? "Z" : "");
  };
  Ngw.smooth = smooth;

  Sets.DEFS += `
    <linearGradient id="ngwSpoutW" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#e6eeee"/><stop offset=".4" stop-color="#c2ccd0"/><stop offset=".82" stop-color="#8a98a0"/><stop offset="1" stop-color="#55636c"/></linearGradient>
    <linearGradient id="ngwSpoutL" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#b08e66"/><stop offset=".32" stop-color="#9a8a76"/><stop offset=".8" stop-color="#76808a"/><stop offset="1" stop-color="#4c5862"/></linearGradient>
    <linearGradient id="ngwSpoutD" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#7a6650"/><stop offset=".25" stop-color="#5a5854"/><stop offset=".65" stop-color="#46505a"/><stop offset="1" stop-color="#36404a"/></linearGradient>
    <radialGradient id="ngwBack"><stop offset="0" stop-color="#c4d0c4" stop-opacity=".95"/><stop offset=".55" stop-color="#94a8a0" stop-opacity=".6"/><stop offset="1" stop-color="#6a8080" stop-opacity="0"/></radialGradient>
    <radialGradient id="ngwSlot"><stop offset="0" stop-color="#f2e6a8" stop-opacity=".95"/><stop offset=".5" stop-color="#a8b884" stop-opacity=".55"/><stop offset="1" stop-color="#5a6a5a" stop-opacity="0"/></radialGradient>
    <radialGradient id="ngwPF"><stop offset="0" stop-color="#f0fffa" stop-opacity="1"/><stop offset=".25" stop-color="#8affd8" stop-opacity=".85"/><stop offset=".6" stop-color="#3ad0c8" stop-opacity=".35"/><stop offset="1" stop-color="#2a9ab8" stop-opacity="0"/></radialGradient>
    <linearGradient id="ngwFunR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#141a20"/><stop offset=".3" stop-color="#2a3239"/><stop offset=".62" stop-color="#434a50"/><stop offset=".88" stop-color="#4c5054"/><stop offset="1" stop-color="#5e5a52"/></linearGradient>
    <linearGradient id="ngwFunL" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#141a20"/><stop offset=".3" stop-color="#2a3239"/><stop offset=".62" stop-color="#434a50"/><stop offset=".88" stop-color="#4c5054"/><stop offset="1" stop-color="#5e5a52"/></linearGradient>
    <linearGradient id="ngwFunV" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#8a6a48" stop-opacity=".95"/><stop offset=".3" stop-color="#5e5246" stop-opacity=".55"/><stop offset=".75" stop-color="#262e36" stop-opacity=".2"/><stop offset="1" stop-color="#121820" stop-opacity=".75"/></linearGradient>
    <linearGradient id="ngwSheath" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#9a7a56" stop-opacity=".75"/><stop offset=".6" stop-color="#7a6650" stop-opacity=".35"/><stop offset="1" stop-color="#5a5048" stop-opacity="0"/></linearGradient>
    <linearGradient id="ngwTierR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#121820"/><stop offset=".45" stop-color="#26323c"/><stop offset=".78" stop-color="#56626a"/><stop offset="1" stop-color="#c2b896"/></linearGradient>
    <linearGradient id="ngwTierL" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#121820"/><stop offset=".45" stop-color="#26323c"/><stop offset=".78" stop-color="#56626a"/><stop offset="1" stop-color="#c2b896"/></linearGradient>
    <radialGradient id="ngwSun"><stop offset="0" stop-color="#fff0c0" stop-opacity="1"/><stop offset=".25" stop-color="#ffd27a" stop-opacity=".75"/><stop offset=".6" stop-color="#d89a4a" stop-opacity=".3"/><stop offset="1" stop-color="#8a5a30" stop-opacity="0"/></radialGradient>
    <linearGradient id="ngwShaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a8a94" stop-opacity=".1"/><stop offset=".5" stop-color="#9aa6ac" stop-opacity=".45"/><stop offset="1" stop-color="#c8b890" stop-opacity=".55"/></linearGradient>
    <radialGradient id="ngwBoltG"><stop offset="0" stop-color="#ffffff" stop-opacity=".9"/><stop offset=".3" stop-color="#cfe0ff" stop-opacity=".45"/><stop offset="1" stop-color="#8aa8ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="ngwLobeR" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5e6c7a"/><stop offset=".55" stop-color="#c8ccd0"/><stop offset="1" stop-color="#fff6e0"/></linearGradient>
    <linearGradient id="ngwLake" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a8e94"/><stop offset=".06" stop-color="#52666e"/><stop offset=".45" stop-color="#2e3e46"/><stop offset="1" stop-color="#1a262c"/></linearGradient>
    <radialGradient id="ngwMist"><stop offset="0" stop-color="#f2f6f6" stop-opacity=".95"/><stop offset=".55" stop-color="#d6e0e2" stop-opacity=".6"/><stop offset="1" stop-color="#c0ccd0" stop-opacity="0"/></radialGradient>
    <radialGradient id="ngwDust"><stop offset="0" stop-color="#ab8c66" stop-opacity=".95"/><stop offset=".6" stop-color="#8c7458" stop-opacity=".6"/><stop offset="1" stop-color="#6a5a48" stop-opacity="0"/></radialGradient>
    <radialGradient id="ngwCollar"><stop offset="0" stop-color="#18222a" stop-opacity=".95"/><stop offset=".65" stop-color="#202e38" stop-opacity=".75"/><stop offset="1" stop-color="#2a3a44" stop-opacity="0"/></radialGradient>
    <radialGradient id="ngwBulb"><stop offset="0" stop-color="#fff2c0" stop-opacity=".95"/><stop offset=".35" stop-color="#ffd27a" stop-opacity=".4"/><stop offset="1" stop-color="#ffb84a" stop-opacity="0"/></radialGradient>
    <linearGradient id="ngwTile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ac0a8"/><stop offset="1" stop-color="#6a9a80"/></linearGradient>
    <linearGradient id="ngwPlaster" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a7e66"/><stop offset="1" stop-color="#b8aa88"/></linearGradient>`;

  // ---------------------------------------------------------------- the funnel
  // base (x, y) on the water / ground, top (tx, ty) in the cloud base; half-width grows from wb/2 at the base to wt/2 at the top.
  // kind "water": grey-white condensation funnel, a spray mound and spray rings on the water, lotus leaves lifted;
  // kind "land": dusty brown base, a debris cloud, straw, leaves and bits of roof sheet in orbit.
  // ids: #id (whole, moves with o.dx in funnelLife), #id-sw (sways about the top), #id-hx (spiral bands), #id-base, .ngwOrb rings
  Ngw.funnel = (o = {}) => {
    const id = o.id || "nf", r = mk(o.seed || 11), land = o.kind === "land", dark = o.tone === "dark", ds = o.ds ?? 1, slope = o.slope ?? 0.3;
    const x0 = o.x ?? 540, y0 = o.y ?? 1100, x1 = o.tx ?? x0 + 60, y1 = o.ty ?? 440, H = y0 - y1;
    const wb = o.wb ?? 44, wt = o.wt ?? 280, pw = o.p ?? 2.4, bend = o.bend ?? 40, bend2 = o.bend2 ?? -14, sp = o.spray ?? wb * 2.6;
    const cx = (t) => x0 + (x1 - x0) * t + bend * Math.sin(Math.PI * t) + bend2 * Math.sin(2 * Math.PI * t), cy = (t) => y0 - H * t;
    const ph = r() * 6, hw = (t, k = 1) => k * (wb / 2 + (wt / 2 - wb / 2) * Math.pow(Math.max(0, t), pw)) * (1 + 0.07 * Math.sin(t * 19 + ph) + 0.04 * Math.sin(t * 41 + ph * 2));
    const T = Array.from({ length: 35 }, (_, i) => -0.03 + 1.16 * i / 34);
    const band = (a, b) => smooth(T.map((t) => [cx(t) + a * hw(t), cy(t)]).concat(T.slice().reverse().map((t) => [cx(t) + b * hw(t), cy(t)])), true);
    const bd = band(-1, 1), op = o.op ?? 0.96;
    // spiral bands: slanted strokes slid sideways (front face moves left → right), clipped to the body
    const S = o.stripe ?? 46, xs0 = Math.min(x0, x1) - wt - S * 2 - H * slope, xs1 = Math.max(x0, x1) + wt + S * 2 + H * slope; let hx = "";
    for (let x = xs0, k = 0; x < xs1; x += S, k++) { const d = `M${f1(x)},${f1(y0 + 30)}L${f1(x + H * slope)},${f1(y1 - 60)}`;
      hx += `<path d="${d}" stroke="${dark ? "#14181c" : land ? "#3e3a34" : "#3a4a56"}" stroke-width="${f1((k % 2 ? 6 : 11) * (dark ? 2.2 : 1))}" opacity="${dark ? 0.2 : land ? 0.32 : 0.26}"/><path d="M${f1(x + S * 0.5)},${f1(y0 + 30)}L${f1(x + S * 0.5 + H * slope)},${f1(y1 - 60)}" stroke="${dark ? "#9aa6ae" : "#f4f8f8"}" stroke-width="${dark ? 5 : 3}" opacity="${dark ? 0.1 : 0.2}"/>`; }
    let g = `<g id="${id}" class="ngwF" data-sp="${S}" data-top="${f1(x1)} ${f1(y1)}" data-base="${f1(x0)} ${f1(y0)}" opacity="${op}"><g id="${id}-sw">
      <defs><clipPath id="${id}-clip"><path d="${bd}"/></clipPath></defs>
      <path d="${bd}" fill="url(#${dark ? "ngwSpoutD" : land ? "ngwSpoutL" : "ngwSpoutW"})"/>
      <g clip-path="url(#${id}-clip)"><path d="${band(0.3, 1.25)}" fill="#18242e" opacity=".5" filter="url(#skBlur10)"/><path d="${band(-0.72, -0.08)}" fill="#f6faf8" opacity="${dark ? 0.12 : land ? 0.2 : 0.42}" filter="url(#skBlur10)"/>
        <g id="${id}-hx">${hx}</g></g>
      <path d="${bd}" fill="none" stroke="#26343e" stroke-width="2.6" opacity=".4"/>`;
    if (dark) g += `<path d="${bd}" fill="none" stroke="#12181e" stroke-width="7" opacity=".6" filter="url(#skBlur4)"/>`;
    if (dark) { let sc = ""; for (let k = 0; k < 26; k++) { const t = 0.05 + r() * 0.95, sd = k % 2 ? 1 : -1, rr = hw(t) * (0.12 + r() * 0.16); sc += `<ellipse cx="${f1(cx(t) + sd * hw(t) * (0.95 + r() * 0.1))}" cy="${f1(cy(t))}" rx="${f1(rr)}" ry="${f1(rr * 0.6)}" fill="${k % 3 ? "#2a3238" : "#3e4448"}"/>`; }
      g += `<g filter="url(#skBlur10)" opacity=".9">${sc}</g>`; }
    // ---- the base
    let b = "";
    if (!land) {
      b += `<ellipse cx="${f1(x0)}" cy="${f1(y0 + 6)}" rx="${f1(sp * 1.6)}" ry="${f1(sp * 0.2)}" fill="#101c24" opacity=".5" filter="url(#skBlur4)"/>`;
      for (let k = 0; k < 3; k++) b += `<ellipse class="ngwRing" cx="${f1(x0)}" cy="${f1(y0 + 6)}" rx="${f1(sp * (0.85 + 0.42 * k))}" ry="${f1(sp * (0.12 + 0.05 * k))}" fill="none" stroke="#dce6e8" stroke-width="${f1(3.4 - k * 0.8)}" stroke-dasharray="40 26" stroke-linecap="round" opacity="${f1(0.55 - k * 0.12)}"/>`;
      let m = ""; for (let k = 0; k < 11; k++) { const a = (k / 11) * Math.PI * 2, rr = sp * (0.26 + r() * 0.26); m += `<circle cx="${f1(x0 + Math.cos(a) * sp * 0.62)}" cy="${f1(y0 - sp * 0.2 - Math.abs(Math.sin(a)) * sp * 0.3 - r() * sp * 0.2)}" r="${f1(rr)}" fill="url(#ngwMist)"/>`; }
      m += `<ellipse cx="${f1(x0)}" cy="${f1(y0 - sp * 0.45)}" rx="${f1(sp * 0.5)}" ry="${f1(sp * 0.6)}" fill="url(#ngwMist)"/>`;
      b += `<g filter="url(#skBlur10)">${m}</g>`;
      for (let k = 0; k < 6; k++) { const sd = k % 2 ? 1 : -1, u = 0.6 + r() * 0.6; b += `<path d="M${f1(x0 + sd * sp * 0.25)},${f1(y0 - sp * 0.35)}q${f1(sd * sp * 0.7 * u)},${f1(-sp * 0.75 * u)} ${f1(sd * sp * 1.4 * u)},${f1(-sp * 0.12)}" stroke="#eef4f4" stroke-width="${f1(5 + r() * 5)}" fill="none" stroke-linecap="round" opacity=".5" filter="url(#skBlur4)"/>`; }
      for (let k = 0; k < 26; k++) { const a = r() * Math.PI * 2, rr = sp * (0.6 + r() * 0.9); b += `<circle cx="${f1(x0 + Math.cos(a) * rr)}" cy="${f1(y0 - sp * 0.2 + Math.sin(a) * rr * 0.32 - r() * sp * 0.5)}" r="${f1(1.5 + r() * 2.5)}" fill="#f2f8f8" opacity=".75"/>`; }
    } else {
      // the debris cloud: a dark skirt at the ground, a soft halo, puffy lumps lit on top, flecks of straw and mud
      b += `<ellipse cx="${f1(x0)}" cy="${f1(y0 + 8)}" rx="${f1(sp * 1.6)}" ry="${f1(sp * 0.24)}" fill="#1e1610" opacity=".55" filter="url(#skBlur4)"/>`;
      b += `<ellipse cx="${f1(x0)}" cy="${f1(y0 - sp * 0.5)}" rx="${f1(sp * 1.15)}" ry="${f1(sp * 0.55)}" fill="#8a7258" opacity=".55" filter="url(#skBlur10)"/>`;
      const dh = o.dustH ?? 1; let m = ""; for (let k = 0; k < 15; k++) { const a = (k / 15) * Math.PI * 2, rr = sp * (0.2 + r() * 0.2), px = x0 + Math.cos(a) * sp * 0.82, py = y0 - dh * (sp * 0.2 + Math.abs(Math.sin(a)) * sp * 0.36 + r() * sp * 0.22);
        m += `<circle cx="${f1(px)}" cy="${f1(py)}" r="${f1(rr)}" fill="${k % 3 ? "#6e5842" : "#836a4e"}"/><circle cx="${f1(px - rr * 0.22)}" cy="${f1(py - rr * 0.32)}" r="${f1(rr * 0.58)}" fill="#ad9068" opacity=".75"/>`; }
      m += `<ellipse cx="${f1(x0)}" cy="${f1(y0 - dh * sp * 0.42)}" rx="${f1(sp * 0.42)}" ry="${f1(dh * sp * 0.5)}" fill="#7a6248"/>`;
      b += `<g filter="url(#skBlur4)" opacity="${o.dustOp ?? 0.94}">${m}</g>`;
      for (let k = 0; k < 34; k++) { const a = r() * Math.PI * 2, rr = sp * (0.7 + r() * 1.0); b += `<circle cx="${f1(x0 + Math.cos(a) * rr)}" cy="${f1(y0 - sp * 0.3 + Math.sin(a) * rr * 0.35 - r() * sp * 0.6)}" r="${f1(1.6 + r() * 2.6)}" fill="${k % 2 ? "#3a2a1a" : "#d8c070"}" opacity=".8"/>`; }
    }
    g += `<g id="${id}-base">${b}</g>`;
    // ---- debris in orbit: rings at a few heights (outer g squashes the ring flat, inner g turns)
    const piece = (k) => { const q = r(); if (!land) return q < 0.5 ? `<ellipse rx="9" ry="7" fill="#3e7a44" stroke="${INK}" stroke-width="1.4"/><path d="M0,0L8,-3" stroke="#7ab86a" stroke-width="1.6"/>` : `<circle r="${f1(2 + r() * 2.5)}" fill="#eef6f6" opacity=".85"/>`;
      if (q < 0.3) return `<path d="M-7,0q7,-6 14,0q-7,6 -14,0z" fill="#3e6a2a" stroke="${INK}" stroke-width="1.2"/>`;
      if (q < 0.55) return `<path d="M-9,0h18" stroke="#d8c070" stroke-width="2.6" stroke-linecap="round"/>`;
      if (q < 0.75) return `<path d="M-15,-6L13,-9L15,5L-13,8Z" fill="#9aa6ac" stroke="${INK}" stroke-width="1.6"/><path d="M-9,-6L-7,7M-2,-7L0,7M5,-8L7,6" stroke="#6a767c" stroke-width="1.4"/>`;
      return `<path d="M-13,2L11,-2M2,-1l6,-7" stroke="#4a3220" stroke-width="3" stroke-linecap="round"/>`; };
    let deb = "";
    (o.rings ?? (land ? [[0.03, 1.5, 9, 0.9], [0.1, 1.25, 7, 1.2], [0.22, 1.1, 6, 1.6], [0.4, 1.0, 4, 2.1]] : [[0.05, 1.4, 6, 1.0], [0.16, 1.2, 5, 1.4]])).forEach(([t, kr, n, per], j) => {
      const R = Math.max(hw(t) * 2.2, sp * kr), yy = cy(t) - (t < 0.06 ? sp * 0.3 : 0);
      let ps = ""; for (let k = 0; k < n; k++) { const a = (360 * k) / n + r() * 30, rr = R * (0.8 + r() * 0.4); ps += `<g transform="rotate(${f1(a)}) translate(${f1(rr)},0) rotate(${f1(-a)}) scale(${f1(ds * (0.7 + r() * 0.6))},${f1(ds * 3.2 * (0.7 + r() * 0.6))})">${piece(k)}</g>`; }
      deb += `<g transform="translate(${f1(cx(t))},${f1(yy)}) scale(1,.3)"><g class="ngwOrb" data-p="${per}">${ps}</g></g>`; });
    g += `<g id="${id}-deb">${deb}</g></g>`;
    // ---- the lowered wall cloud over the top (fixed; the rope sways under it): a dark flat-bottomed mass with a bumpy underside
    const wc = o.wall ?? wt * 2.4; let under = ""; for (let k = 0; k <= 16; k++) { const u = k / 16, x = x1 - wc + 2 * wc * u, dy = 34 * Math.sin(Math.PI * u) + (r() - 0.5) * 22; under += `${k ? "L" : "M"}${f1(x)},${f1(y1 + dy)}`; }
    let col = `<path d="${under}L${f1(x1 + wc * 1.15)},${f1(y1 - 150)}Q${f1(x1)},${f1(y1 - 260)} ${f1(x1 - wc * 1.15)},${f1(y1 - 150)}Z" fill="#16202a" opacity=".96"/>`;
    for (let k = 0; k < 10; k++) { const u = (k + 0.5) / 10, rr = wt * (0.35 + r() * 0.3); col += `<ellipse cx="${f1(x1 - wc + 2 * wc * u)}" cy="${f1(y1 + 6 + 26 * Math.sin(Math.PI * u) - r() * 20)}" rx="${f1(rr)}" ry="${f1(rr * 0.36)}" fill="${k % 3 ? "#1a2630" : "#2a3a46"}"/>`; }
    col += `<path d="${under}" stroke="#7e909a" stroke-width="7" fill="none" opacity=".35" transform="translate(0,10)"/>`;
    g += `<g id="${id}-col" filter="url(#skBlur10)">${col}</g></g>`;
    return g;
  };
  // the funnel alive: bands spin, the rope sways about its top, the base breathes, rings and debris turn; o.dx moves it across
  Ngw.funnelLife = (tl, id, t0, dur, o = {}) => {
    const root = document.getElementById(id); if (!root) return;
    const q = (s) => document.getElementById(`${id}-${s}`), S = +root.dataset.sp || 46, top = root.dataset.top, base = root.dataset.base;
    const spin = o.spin ?? 0.38, n = (p) => Math.max(1, Math.ceil(dur / p));
    tl.fromTo(q("hx"), { x: 0 }, { x: S, duration: spin, ease: "none", repeat: n(spin), immediateRender: false }, t0);
    tl.fromTo(q("sw"), { skewX: -(o.sway ?? 2.2), svgOrigin: top }, { skewX: o.sway ?? 2.2, svgOrigin: top, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: n(1.4), immediateRender: false }, t0);
    tl.fromTo(q("base"), { scale: 0.96, svgOrigin: base }, { scale: 1.05, svgOrigin: base, duration: 0.55, ease: "sine.inOut", yoyo: true, repeat: n(0.55), immediateRender: false }, t0);
    root.querySelectorAll(".ngwRing").forEach((e, k) => tl.fromTo(e, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -66 }, duration: 0.5 + k * 0.2, ease: "none", repeat: n(0.5), immediateRender: false }, t0));
    root.querySelectorAll(".ngwOrb").forEach((e) => { const p = +e.dataset.p || 1; tl.fromTo(e, { rotation: 0, svgOrigin: "0 0" }, { rotation: 360, svgOrigin: "0 0", duration: p, ease: "none", repeat: n(p), immediateRender: false }, t0); });
    if (o.dx) tl.fromTo(root, { x: 0 }, { x: o.dx, duration: dur, ease: "none", immediateRender: false }, t0);
  };


  // ---------------------------------------------------------------- the big one: a supercell and its wedge tornado
  // o: x, y (base on the ground), h (funnel height), wb / wt (widths), tx (top x), plates, slotDx, flashes [[dx, dy] in base widths]
  // ids: the funnel's ids (id, id-sw, id-hx …) + #id-meso (turns), .id-pf power flashes, #id-big (big debris)
  Ngw.monster = (o = {}) => {
    const id = o.id || "mt", r = mk(o.seed || 41), x0 = o.x ?? 560, y0 = o.y ?? 1090, H = o.h ?? 470, wb = o.wb ?? 440, wt = o.wt ?? 640, x1 = o.tx ?? x0 + 30, y1 = y0 - H;
    let g = `<g id="${id}-all"><ellipse cx="${f1(x0 + 30)}" cy="${f1(y0 - H * 0.5)}" rx="${f1(wt * 1.5)}" ry="${f1(H * 0.98)}" fill="url(#ngwBack)" opacity="${o.back ?? 0.95}"/>`;
    // the clear slot: lit sky behind and to one side, so the tornado reads as a dark mass against it
    if (o.slot !== false) g += `<ellipse cx="${f1(x0 + (o.slotDx ?? 560))}" cy="${f1(y0 - H * 0.45)}" rx="${f1(wt * 0.95)}" ry="${f1(H * 0.85)}" fill="url(#ngwSlot)" opacity="${o.slot ?? 0.8}"/>`;
    // the mesocyclone: stacked plates, wider and paler up the stack, a lit rim along each underside
    const n = o.plates ?? 7, ph = o.plateH ?? 54, pw = o.plateW ?? 130; let m = "";
    for (let k = n - 1; k >= 0; k--) { const y = y1 - 40 - k * ph, rx = wt * 0.8 + k * pw, ry = 40 + k * 7, cx = x1 + k * 14 + (r() - 0.5) * 20;
      m += `<ellipse cx="${f1(cx)}" cy="${f1(y)}" rx="${f1(rx)}" ry="${f1(ry)}" fill="${k % 2 ? "#26303a" : "#323e48"}"/><path d="M${f1(cx - rx * 0.97)},${f1(y + 4)}A${f1(rx)},${f1(ry)} 0 0 0 ${f1(cx + rx * 0.97)},${f1(y + 4)}" stroke="#b4c4c6" stroke-width="${f1(8 + k * 1.6)}" fill="none" opacity="${f1(0.3 + 0.04 * k)}"/><path d="M${f1(cx - rx * 0.9)},${f1(y + ry * 0.7)}A${f1(rx * 0.92)},${f1(ry * 0.6)} 0 0 0 ${f1(cx + rx * 0.9)},${f1(y + ry * 0.7)}" stroke="#141a20" stroke-width="10" fill="none" opacity=".35"/>`; }
    g += `<g id="${id}-meso" filter="url(#skBlur4)">${m}</g>`;
    // rain and hail curtains hanging off the back of the storm
    for (let k = 0; k < 7; k++) { const x = x0 - wt * 2.2 - k * 90 + r() * 40, w = 70 + r() * 90; g += `<path d="M${f1(x)},${f1(y1 - 60)}L${f1(x - 60)},${f1(y0 + 10)}L${f1(x - 60 + w)},${f1(y0 + 10)}L${f1(x + w)},${f1(y1 - 60)}Z" fill="#8a9aa4" opacity="${f1(0.16 + r() * 0.14)}" filter="url(#skBlur10)"/>`; }
    // the funnel itself
    g += Ngw.funnel({ id, kind: "land", tone: "dark", x: x0, y: y0, tx: x1, ty: y1, wb, wt, p: o.p ?? 1.5, bend: o.bend ?? 18, bend2: o.bend2 ?? -10, spray: o.spray ?? wb * 0.62, dustH: o.dustH ?? 0.55, dustOp: o.dustOp ?? 0.86, seed: o.seed || 41, ds: o.ds ?? 2.4, wall: o.wall ?? wt * 1.35, slope: o.slope ?? 0.14, stripe: o.stripe ?? 70, rings: o.rings, op: 1 });
    // big debris: a roof sheet, planks, a tumbling car, a tree, high in the debris cloud
    let big = ""; (o.big || [[-0.55, 0.32, "sheet", 1], [0.62, 0.22, "car", 1], [0.4, 0.55, "plank", 1], [-0.35, 0.7, "sheet", 0.8], [0.15, 0.85, "plank", 0.7], [-0.75, 0.12, "tree", 1]]).forEach(([fx, fy, kind, s], k) => {
      const x = x0 + fx * wb * 1.4, y = y0 - fy * H, a = Math.round(r() * 80 - 40), sc = s * (o.bigScale ?? 1);
      const shape = kind === "car" ? `<path d="M-40,8V-6L-26,-20H18L34,-6H44V8Z" fill="#c8cfd4" stroke="${INK}" stroke-width="3"/><rect x="-20" y="-16" width="16" height="10" fill="#5a6a78"/><rect x="2" y="-16" width="16" height="10" fill="#5a6a78"/><circle cx="-24" cy="10" r="8" fill="#222" stroke="${INK}" stroke-width="2"/><circle cx="28" cy="10" r="8" fill="#222" stroke="${INK}" stroke-width="2"/>`
        : kind === "plank" ? `<rect x="-34" y="-5" width="68" height="10" fill="#8a6a44" stroke="${INK}" stroke-width="2.4"/>`
        : kind === "tree" ? `<path d="M0,30V-10" stroke="#4a3220" stroke-width="7"/><circle cx="0" cy="-22" r="22" fill="#2e4a2a" stroke="${INK}" stroke-width="2.4"/><circle cx="-14" cy="-10" r="14" fill="#2e4a2a"/><circle cx="14" cy="-12" r="15" fill="#2e4a2a"/>`
        : `<path d="M-30,-14L28,-18L32,12L-26,16Z" fill="#a8b0b4" stroke="${INK}" stroke-width="2.6"/><path d="M-20,-14L-16,15M-6,-15L-2,14M8,-16L12,13M20,-17L24,12" stroke="#78848a" stroke-width="2"/>`;
      big += `<g class="${id}-bd" transform="translate(${f1(x)},${f1(y)}) rotate(${a}) scale(${f1(sc)})">${shape}</g>`; });
    g += `<g id="${id}-big" opacity=".92">${big}</g>`;
    // power flashes: blue-green bursts where the lines and transformers go
    (o.flashes || [[-0.75, 0.02], [0.85, 0.05]]).forEach(([fx, fy], k) => { const x = x0 + fx * wb, y = y0 - fy * H;
      g += `<g class="${id}-pf" opacity="${o.flashOn === false ? 0 : 1}"><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(wb * 0.3)}" fill="url(#ngwPF)"/><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(wb * 0.04)}" fill="#f4fffc"/></g>`; });
    return g + `</g>`;
  };
  Ngw.monsterLife = (tl, id, t0, dur, o = {}) => {
    Ngw.funnelLife(tl, id, t0, dur, { spin: o.spin ?? 0.55, sway: o.sway ?? 0.8, dx: o.dx });
    const n = (p) => Math.max(1, Math.ceil(dur / p)), all = document.getElementById(`${id}-all`); if (!all) return;
    tl.fromTo(`#${id}-meso`, { x: -10 }, { x: 10, duration: 2.4, ease: "sine.inOut", yoyo: true, repeat: n(2.4), immediateRender: false }, t0);
    all.querySelectorAll(`.${id}-bd`).forEach((e, k) => { tl.to(e, { rotation: `+=${k % 2 ? 360 : -360}`, x: `+=${k % 2 ? 60 : -60}`, y: `-=${30 + k * 10}`, duration: dur, ease: "none", immediateRender: false }, t0); });
    all.querySelectorAll(`.${id}-pf`).forEach((e, k) => { const t = t0 + (o.flashAt || [0.6, 1.7])[k % 2] + k * 0.1; tl.fromTo(e, { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.04 }, { opacity: 0.3, duration: 0.06 }, { opacity: 0.9, duration: 0.05 }, { opacity: 0, duration: 0.35 }], immediateRender: false }, t); });
    if (o.dx) tl.fromTo(all, { x: 0 }, { x: o.dx, duration: dur, ease: "none", immediateRender: false }, t0);
  };
  // a Thai concrete power pole: crossarms, insulators, a transformer on some, a tangle of cables; wires run pole to pole
  Ngw.pole = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s}) rotate(${o.lean || 0})"><path d="M-9,0L-6,-440H6L9,0Z" fill="#a8a69c" ${OUT(3)}/><path d="M-60,-400H60M-46,-360H46" stroke="#5a5a56" stroke-width="8"/>
    ${[-54, -20, 20, 54].map((dx) => `<rect x="${dx - 4}" y="-418" width="8" height="18" rx="3" fill="#e8e4d8" stroke="${INK}" stroke-width="1.6"/>`).join("")}${o.tf ? `<rect x="10" y="-330" width="40" height="56" rx="6" fill="#7a8288" ${OUT(2.4)}/><path d="M18,-330v-14M42,-330v-14" stroke="#555" stroke-width="3"/>` : ""}
    <path d="M-6,-300q-30,20 -20,60q10,30 -12,50M6,-290q34,10 22,52q-10,30 14,44" stroke="#1a1a1a" stroke-width="3" fill="none"/><ellipse cx="-14" cy="-230" rx="16" ry="10" fill="none" stroke="#1a1a1a" stroke-width="3"/></g>`;
  Ngw.wires = (xs, y, s = 1, sag = 40) => { let d = ""; for (let i = 0; i < xs.length - 1; i++) [-54, -20, 20, 54].forEach((dx, k) => { const a = xs[i] + dx * s, b = xs[i + 1] + dx * s, yy = y - 410 * s; d += `M${f1(a)},${f1(yy)}Q${f1((a + b) / 2)},${f1(yy + sag * (1 + k * 0.15))} ${f1(b)},${f1(yy)}`; });
    return `<path d="${d}" stroke="#1a1a1a" stroke-width="${f1(2.4 * s + 0.6)}" fill="none"/>`; };
  // a two-lane highway across the frame: shoulders, asphalt, the centre line, a green distance sign
  Ngw.road = (o = {}) => { const y = o.y ?? 1560, h = o.h ?? 170;
    return `<rect x="-1400" y="${y - 16}" width="4000" height="16" fill="#8a8470"/><rect x="-1400" y="${y}" width="4000" height="${h}" fill="#3a3c40"/><rect x="-1400" y="${y + h}" width="4000" height="20" fill="#8a8470"/>
      <path d="M-1400,${y + h / 2}H2600" stroke="#f2c230" stroke-width="7" stroke-dasharray="70 50"/><path d="M-1400,${y + 10}H2600M-1400,${y + h - 10}H2600" stroke="#e8e4d8" stroke-width="5"/>
      ${Array.from({ length: 30 }, (_, k) => `<path d="M${-1300 + k * 140},${y + 30 + (k * 37) % (h - 50)}l${30 + (k % 3) * 10},0" stroke="#9aa4ac" stroke-width="2" opacity=".35"/>`).join("")}`; };
  Ngw.sign = (x, y, s = 1, t1 = "ตัวเมือง", t2 = "5 กม.") => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-70,0V-200M70,0V-200" stroke="#9a9a96" stroke-width="12"/><rect x="-150" y="-330" width="300" height="140" rx="12" fill="#1e7a4a" stroke="#f2f0ea" stroke-width="8"/>
    <text x="0" y="-268" text-anchor="middle" font-family="Sriracha" font-size="52" fill="#f2f0ea">${t1}</text><text x="0" y="-212" text-anchor="middle" font-family="Sriracha" font-size="40" fill="#f2f0ea">${t2}</text></g>`;

  // ---------------------------------------------------------------- damage: a house losing its roof, a ruined house, a debris field, an overpass
  // level 1: Tk.house with a hole torn in the roof, rafters showing, tiles peeling off toward the storm (dir -1 = to the left)
  // level 2: the walls broken off jagged, no roof, a heap of planks and tiles at the foot, a sheet of roofing leaning on it
  Ngw.ruin = (x, y, s = 1, o = {}) => {
    const r = mk(o.seed || 61), lv = o.level ?? 1, dir = o.dir ?? -1;
    if (lv === 1) { let g = Tk.house(x, y, s, o) + `<g transform="translate(${x},${y}) scale(${s * (o.flip ? -1 : 1)},${s})">`;
      g += `<path d="M-200,-470L-120,-560L-20,-610L60,-560L140,-520L200,-440L60,-430L-40,-450Z" fill="#1e1610" stroke="${INK}" stroke-width="6"/>`;
      g += [-150, -80, -10, 60, 130].map((rx) => `<path d="M${rx},-450L${rx + 30},-590" stroke="#8a6a44" stroke-width="12"/><path d="M${rx},-450L${rx + 30},-590" stroke="${INK}" stroke-width="3" fill="none"/>`).join("");
      // o.calm (after the storm, QA 6: "the tile streams still arcing off the roofs after the storm"): the tiles lie on the ground instead
      for (let k = 0; k < 14; k++) { if (o.calm) { const tx = -330 + r() * 660, ty = -8 - r() * 26; g += `<rect x="${f1(tx)}" y="${f1(ty)}" width="46" height="20" fill="#a8442e" stroke="${INK}" stroke-width="3" transform="rotate(${f1(r() * 50 - 25)} ${f1(tx + 23)} ${f1(ty + 10)})"/>`; continue; }
        const tx = -60 + dir * (60 + k * 50) + r() * 60, ty = -620 - k * 34 - r() * 80; g += `<rect x="${f1(tx)}" y="${f1(ty)}" width="46" height="26" fill="#a8442e" stroke="${INK}" stroke-width="3" transform="rotate(${f1(r() * 120 - 60)} ${f1(tx + 23)} ${f1(ty + 13)})"/>`; }
      return g + `</g>`; }
    let g = `<g transform="translate(${x},${y}) scale(${s * (o.flip ? -1 : 1)},${s})"><ellipse cx="0" cy="12" rx="560" ry="40" fill="#000" opacity=".35"/>`;
    let top = "M-380,0V-260"; for (let k = 1; k <= 12; k++) top += `L${-380 + k * 63},${f1(-200 - r() * 160 + (k % 3 === 0 ? 70 : 0))}`; top += "V0Z";
    g += `<path d="${top}" fill="#d8c4a0" stroke="${INK}" stroke-width="7"/><rect x="-300" y="-180" width="120" height="110" fill="#2a2018" stroke="${INK}" stroke-width="5"/><rect x="140" y="-170" width="120" height="100" fill="#2a2018" stroke="${INK}" stroke-width="5"/>`;
    g += `<path d="M-340,-240l60,30M200,-260l70,40" stroke="#5a4a38" stroke-width="5"/>`;
    for (let k = 0; k < 22; k++) { const px = -420 + r() * 840, py = -10 - r() * 90, w = 60 + r() * 120, a = r() * 50 - 25; g += `<rect x="${f1(px)}" y="${f1(py)}" width="${f1(w)}" height="14" fill="${k % 4 === 0 ? "#a8442e" : "#8a6a44"}" stroke="${INK}" stroke-width="3" transform="rotate(${f1(a)} ${f1(px + w / 2)} ${f1(py + 7)})"/>`; }
    g += `<path d="M120,-10L420,-300L460,-280L170,10Z" fill="#a8b0b4" stroke="${INK}" stroke-width="5"/><path d="M180,-60L430,-290M220,-30L445,-280" stroke="#78848a" stroke-width="4"/>`;
    return g + `</g>`;
  };
  Ngw.debris = (x0, x1, y0, y1, n = 40, seed = 71, sc = 1) => { const r = mk(seed); let g = "";
    for (let k = 0; k < n; k++) { const t = r(), x = x0 + r() * (x1 - x0), y = y0 + t * (y1 - y0), s = sc * (0.5 + t * 0.9), a = Math.round(r() * 160 - 80), q = r();
      const sh = q < 0.35 ? `<rect x="-50" y="-7" width="100" height="14" fill="#8a6a44" stroke="${INK}" stroke-width="3"/>` : q < 0.55 ? `<path d="M-46,-16L42,-22L48,14L-40,20Z" fill="#a8b0b4" stroke="${INK}" stroke-width="3"/><path d="M-30,-16L-26,18M-10,-18L-6,17M10,-19L14,16M28,-20L32,15" stroke="#78848a" stroke-width="2.4"/>`
        : q < 0.7 ? `<rect x="-22" y="-12" width="44" height="24" fill="#a8442e" stroke="${INK}" stroke-width="3"/>` : q < 0.85 ? `<path d="M-40,4L36,-4M-6,0l20,-24M10,-2l14,16" stroke="#4a3220" stroke-width="7" stroke-linecap="round"/><circle cx="20" cy="-26" r="10" fill="#2e4a2a"/>` : `<circle r="18" fill="#222" stroke="${INK}" stroke-width="3"/><circle r="8" fill="#555"/>`;
      g += `<g transform="translate(${f1(x)},${f1(y)}) rotate(${a}) scale(${f1(s)},${f1(s * 0.75)})">${sh}</g>`; }
    return g; };
  // a concrete overpass across the frame: the deck (top ty), girders under it, two piers, the abutment slope on the left where people
  // crawl up under the deck; returns { set (behind the actors), fg (the deck edge in front) }
  Ngw.overpass = (o = {}) => {
    // v2 (owner 5 Nov: "สะพาน… ยังไม่ดี"): a real highway overpass seen from the road — the near deck edge (fascia) with its concrete
    // parapet, railing, lamp posts and the route sign in front; behind the actors the underside receding in perspective (girders
    // converging), the far deck edge and far piers, a thick near pier with its cap, and the paved abutment slope people climb.
    // Clearance is set by the shot (o.y + o.h above o.ground): about three people under the deck (≈ 5 m) at the shot's actor scale.
    const ty = o.y ?? 560, dh = o.h ?? 150, gy = o.ground ?? 1560, sx = o.slopeX ?? 520, px = o.pier ?? 960, vx = o.vx ?? 540;
    const db = ty + dh, sd = o.soffit ?? 170, fb = db + sd, X0 = -1500, X1 = 2700, r = mk(o.seed || 31), G = "ov" + (Ngw._ovN = (Ngw._ovN || 0) + 1);   // gradient ids unique per drawing (68 clips share the page)
    let set = `<defs><linearGradient id="${G}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2022"/><stop offset="1" stop-color="#46494c"/></linearGradient>
      <linearGradient id="${G}p" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#bdbab0"/><stop offset=".5" stop-color="#a19e95"/><stop offset="1" stop-color="#6c6a64"/></linearGradient>
      <linearGradient id="${G}l" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8e897c"/><stop offset="1" stop-color="#b3ad9e"/></linearGradient></defs>`;
    // the underside, receding: near edge db → far edge fb, the girders converging toward vx, cross-frames between them
    set += `<path d="M${X0},${db}H${X1}V${fb}H${X0}Z" fill="url(#${G}s)"/>`;
    for (let x = X0; x <= X1; x += 170) { const x2 = vx + (x - vx) * 0.8;
      set += `<path d="M${x},${db}L${f1(x2)},${fb}" stroke="#141618" stroke-width="20"/><path d="M${x + 8},${db}L${f1(x2 + 6)},${fb}" stroke="#70747a" stroke-width="3" opacity=".75"/>`; }
    for (const t of [0.35, 0.7]) { const y = f1(db + sd * t), k = 1 - 0.2 * t; set += `<path d="M${f1(vx + (X0 - vx) * k)},${y}H${f1(vx + (X1 - vx) * k)}" stroke="#2a2c2e" stroke-width="7" opacity=".8"/>`; }
    // the far deck edge and the far row of piers (smaller, cooler: they are across the road)
    set += `<path d="M${X0},${fb}H${X1}V${fb + 52}H${X0}Z" fill="#8f8d85" stroke="${INK}" stroke-width="4"/><path d="M${X0},${fb + 40}H${X1}" stroke="#6e6c66" stroke-width="5"/>`;
    for (const fx of (o.farPiers ?? [px - 1500, px - 760, px + 760])) set += `<path d="M${fx - 48},${fb + 52}H${fx + 48}V${fb + 80}H${fx - 48}Z" fill="#7c7a73" stroke="${INK}" stroke-width="3"/><path d="M${fx - 30},${fb + 80}H${fx + 30}V${gy - 70}H${fx - 30}Z" fill="#6e6c66" stroke="${INK}" stroke-width="3"/><path d="M${fx + 12},${fb + 82}V${gy - 74}" stroke="#55534e" stroke-width="7" opacity=".6"/>`;
    // the shadow the deck throws on the road under it
    set += `<path d="M${X0},${gy - 50}H${X1}V${gy + 260}H${X0}Z" fill="#000" opacity=".2"/>`;
    // the abutment: a paved slope from the road up to the underside, its joints, its lit top edge, a ledge right under the girders
    set += `<path d="M${X0},${db}H${sx}L${sx - 640},${gy}H${X0}Z" fill="url(#${G}l)" stroke="${INK}" stroke-width="6"/>`;
    for (let k = 1; k < 10; k++) { const t = k / 10; set += `<path d="M${X0},${f1(db + t * (gy - db))}H${f1(sx - 640 * t)}" stroke="#776f62" stroke-width="4"/>`; }
    for (let x = X0 + 150; x < sx - 640; x += 190) set += `<path d="M${x},${db}V${gy}" stroke="#776f62" stroke-width="3" opacity=".7"/>`;
    set += `<path d="M${sx},${db}L${sx - 640},${gy}" stroke="#ddd8c8" stroke-width="12"/><path d="M${X0},${db + 34}H${sx - 22}" stroke="#c9c4b4" stroke-width="12"/><path d="M${X0},${db + 44}H${sx - 30}" stroke="#4e4a40" stroke-width="5" opacity=".7"/>`;
    // the near pier: a thick column with its cap and bearing pads, lit from the left, a drain pipe, rain stains
    set += `<path d="M${px - 170},${db}H${px + 170}V${db + 80}H${px - 170}Z" fill="#aaa79e" stroke="${INK}" stroke-width="6"/>${[-110, 0, 110].map((dx) => `<rect x="${px + dx - 26}" y="${db - 14}" width="52" height="14" fill="#2e2e2e"/>`).join("")}`;
    set += `<path d="M${px - 105},${db + 80}H${px + 105}V${gy + 40}H${px - 105}Z" fill="url(#${G}p)" stroke="${INK}" stroke-width="6"/><path d="M${px - 70},${db + 84}V${gy + 30}" stroke="#d2cfc6" stroke-width="6" opacity=".55"/>`;
    set += `<path d="M${px + 70},${db + 84}V${gy - 10}q0,24 -24,24" stroke="#55595c" stroke-width="13" fill="none" stroke-linecap="round"/>`;
    for (let k = 0; k < 8; k++) { const x = px - 90 + k * 24 + r() * 8; set += `<path d="M${f1(x)},${db + 84}V${f1(db + 180 + r() * 320)}" stroke="#5e5c54" stroke-width="${f1(3 + r() * 3)}" opacity=".3"/>`; }
    // in front of the actors: the near deck edge (fascia) with its drip groove, joints and stains, the parapet, the railing, lamps, the sign
    let fg = `<path d="M${X0},${ty}H${X1}V${db}H${X0}Z" fill="#b6b3a8" stroke="${INK}" stroke-width="7"/><path d="M${X0},${db - 28}H${X1}" stroke="#8c897e" stroke-width="11"/><path d="M${X0},${ty + 14}H${X1}" stroke="#d4d1c6" stroke-width="6"/>`;
    for (let x = X0 + 350; x < X1; x += 700) fg += `<path d="M${x},${ty}V${db}" stroke="#7a776c" stroke-width="6"/>`;
    for (let k = 0; k < 26; k++) { const x = X0 + 60 + k * 160 + r() * 60; fg += `<path d="M${f1(x)},${db - 22}V${f1(db - 22 + 20 + r() * 50)}" stroke="#6a675c" stroke-width="${f1(3 + r() * 4)}" opacity=".35"/>`; }
    fg += `<path d="M${X0},${ty}H${X1}V${ty - 64}H${X0}Z" fill="#cbc8bd" stroke="${INK}" stroke-width="5"/><path d="M${X0},${ty - 22}H${X1}" stroke="#a9a69b" stroke-width="5"/>`;
    for (let x = X0; x <= X1; x += 110) fg += `<path d="M${x},${ty - 64}V${ty - 118}" stroke="#6e7174" stroke-width="9"/>`;
    fg += `<path d="M${X0},${ty - 118}H${X1}M${X0},${ty - 92}H${X1}" stroke="#6e7174" stroke-width="9"/>`;
    for (let x = X0 + 300; x < X1; x += 1000) fg += `<path d="M${x},${ty - 64}V${ty - 420}q0,-26 30,-26H${x + 120}" stroke="#5e6266" stroke-width="13" fill="none"/><rect x="${x + 100}" y="${ty - 458}" width="70" height="20" rx="6" fill="#3e4246"/><path d="M${x + 106},${ty - 438}h58" stroke="#ffe9a8" stroke-width="5" opacity=".9"/>`;
    const sgx = o.signX ?? 560;
    fg += `<rect x="${sgx}" y="${ty + 22}" width="360" height="${Math.min(100, dh - 40)}" rx="10" fill="#1e7a4a" stroke="#f2f0ea" stroke-width="6"/><text x="${sgx + 205}" y="${ty + 22 + Math.min(100, dh - 40) / 2 + 15}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="40" fill="#f2f0ea">ทางหลวง 32</text>
      <path d="M${sgx + 28},${ty + 44}h44v34q-22,16 -44,0Z" fill="#f2f0ea"/><text x="${sgx + 50}" y="${ty + 72}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#1e7a4a">32</text>`;
    return { set, fg }; };
  // wind streaks rushing through a gap toward the camera (the overpass wind tunnel), with flying debris
  Ngw.streaks = (x0, x1, y0, y1, n = 26, seed = 81) => { const r = mk(seed); let g = "";   // wind rushing right → left through the gap
    for (let k = 0; k < n; k++) { const y = y0 + r() * (y1 - y0), x = x0 + r() * (x1 - x0), L0 = 160 + r() * 340; g += `<path d="M${f1(x)},${f1(y)}l${f1(-L0)},${f1(L0 * 0.06)}" stroke="#eef2f2" stroke-width="${f1(2 + r() * 4)}" stroke-linecap="round" opacity="${f1(0.22 + r() * 0.3)}"/>`; }
    return g; };

  // ---------------------------------------------------------------- the epic storm (owner: "ทำพายุให้อลังการกว่านี้")
  // A supercell and its tornado lit low from one side (o.sun: 1 = sun on the right, -1 = left). Returns { sky, mid }:
  //   sky — the sun glow, the rain and hail shafts, the mothership (striated tiers corkscrewing up into the storm body), the inflow band,
  //         the wall cloud, lightning
  //   mid — the funnel (lit rim, curved spiral bands, a dust sheath), sub-vortices at its base, the debris fountain, debris with motion
  //         streaks, ground inflow dust, power flashes
  // ids: #id (funnel root, as Ngw.funnel), #id-meso, #id-subs, .id-pf, #id-big, #id-bolts
  Ngw.epic = (o = {}) => {
    const id = o.id || "ep", r = mk(o.seed || 51), sun = o.sun ?? 1, x0 = o.x ?? 540, y0 = o.y ?? 1200, H = o.h ?? 700, wb = o.wb ?? 300, wt = o.wt ?? 620;
    const x1 = o.tx ?? x0 + 40, y1 = y0 - H, bend = o.bend ?? 30, bend2 = o.bend2 ?? -12, pw = o.p ?? 1.9;
    const cx = (t) => x0 + (x1 - x0) * t + bend * Math.sin(Math.PI * t) + bend2 * Math.sin(2 * Math.PI * t), cy = (t) => y0 - H * t;
    const ph = r() * 6, hw = (t) => (wb / 2 + (wt / 2 - wb / 2) * Math.pow(Math.max(0, t), pw)) * (1 + 0.05 * Math.sin(t * 17 + ph) + 0.03 * Math.sin(t * 39 + ph * 2));
    const T = Array.from({ length: 41 }, (_, i) => -0.03 + 1.06 * i / 40);
    const band = (a, b, t0 = -0.03, t1 = 1.03) => { const TT = T.filter((t) => t >= t0 && t <= t1); return smooth(TT.map((t) => [cx(t) + a * hw(t), cy(t)]).concat(TT.slice().reverse().map((t) => [cx(t) + b * hw(t), cy(t)])), true); };
    const SKX = (x) => x0 + (x - x0);   // (kept for readability: everything is in world px)
    // ======== sky
    let sky = "";
    // the low sun behind the storm's flank, and the lit band of sky under the storm on that side
    sky += `<ellipse cx="${f1(x0 + sun * (o.sunDx ?? 820))}" cy="${f1(y0 - 120)}" rx="900" ry="520" fill="url(#ngwSun)" opacity="${o.sunOp ?? 0.85}"/>`;
    sky += `<rect x="-1400" y="${f1(y0 - 260)}" width="4000" height="300" fill="#c8a868" opacity=".18" filter="url(#skBlur24)"/>`;
    // rain and hail shafts hanging off the rear of the storm (the side away from the sun), lit gold at their feet
    for (let k = 0; k < 9; k++) { const x = x0 - sun * (wt * 0.9 + k * 120 + r() * 60), w = 90 + r() * 120, top = y1 - 40 - r() * 80;
      sky += `<path d="M${f1(x)},${f1(top)}L${f1(x - sun * 40 - w / 2)},${f1(y0 + 20)}L${f1(x - sun * 40 + w / 2)},${f1(y0 + 20)}L${f1(x + w)},${f1(top)}Z" fill="url(#ngwShaft)" opacity="${f1(0.45 + r() * 0.35)}" filter="url(#skBlur10)"/>`; }
    // the storm body above everything, dark, its sun-side edge catching light
    const top = y1 - (o.tiers ?? 8) * (o.tierH ?? 64) - 90;
    let und = `M-1400,${f1(top + 70)}`; for (let k = 0; k <= 26; k++) { const x = -1400 + k * 155, yy = top + 40 + 50 * Math.exp(-Math.pow((x - x1) / 900, 2)) * -1 + 26 * Math.sin(k * 1.7 + ph) + Math.abs(x - x1) * 0.05; und += `Q${f1(x - 70)},${f1(yy + 46)} ${f1(x)},${f1(yy)}`; }
    sky += `<path d="${und}V-900H-1400Z" fill="#141c24" filter="url(#skBlur4)"/>`;
    sky += `<path d="M${f1(x1 + sun * 140)},${f1(top + 4)}Q${f1(x1 + sun * 800)},${f1(top + 30)} ${f1(x1 + sun * 1500)},${f1(top + 120)}" stroke="#e8d0a0" stroke-width="12" fill="none" opacity=".3" filter="url(#skBlur10)"/>`;
    // the mothership: striated tiers, wider and paler going up, each shifted a little (the corkscrew), a lit rim on each underside
    let ms = ""; const n = o.tiers ?? 8, th = o.tierH ?? 64, tg = o.tierW ?? 120;
    for (let k = n - 1; k >= 0; k--) { const yk = y1 - 70 - k * th, rx = wt * 0.66 + k * tg, ry = 46 + k * 9, ck = x1 + (k % 2 ? 1 : -1) * 22 + sun * k * 12;
      ms += `<ellipse cx="${f1(ck)}" cy="${f1(yk)}" rx="${f1(rx)}" ry="${f1(ry)}" fill="url(#${sun > 0 ? "ngwTierR" : "ngwTierL"})"/>`;
      const a0 = sun > 0 ? 0 : Math.PI, a1 = sun > 0 ? 0.62 * Math.PI : 0.38 * Math.PI, p0 = [ck + rx * Math.cos(a0), yk + ry * Math.sin(a0)], p1 = [ck + rx * Math.cos(a1), yk + ry * Math.sin(a1)];
      ms += `<path d="M${f1(p0[0])},${f1(p0[1])}A${f1(rx)},${f1(ry)} 0 0 ${sun > 0 ? 1 : 0} ${f1(p1[0])},${f1(p1[1])}" stroke="#f6e6bc" stroke-width="${f1(6 + k * 1.1)}" fill="none" opacity=".9"/>`;
      ms += `<path d="M${f1(ck - rx * 0.92)},${f1(yk - ry * 0.15)}A${f1(rx * 0.92)},${f1(ry * 0.8)} 0 0 0 ${f1(ck + rx * 0.92)},${f1(yk - ry * 0.15)}" stroke="#080b0e" stroke-width="16" fill="none" opacity=".5"/>`;
      ms += `<path d="M${f1(ck - rx * 0.7)},${f1(yk - ry * 0.3)}A${f1(rx * 0.7)},${f1(ry * 0.5)} 0 0 0 ${f1(ck + rx * 0.7)},${f1(yk - ry * 0.3)}" stroke="#9aa4a8" stroke-width="3" fill="none" opacity=".25"/>`; }
    let wc = ""; for (let k = 0; k < 9; k++) { const u = (k + 0.5) / 9, rr = wt * (0.16 + r() * 0.1); wc += `<ellipse cx="${f1(x1 - wt * 0.62 + u * wt * 1.24)}" cy="${f1(y1 - 30 + Math.sin(u * Math.PI) * 18 + r() * 12)}" rx="${f1(rr * 1.4)}" ry="${f1(rr * 0.75)}" fill="${k % 3 ? "#161e26" : "#1e2830"}"/>`; }
    wc += `<ellipse cx="${f1(x1)}" cy="${f1(y1 - 50)}" rx="${f1(wt * 0.7)}" ry="${f1(wt * 0.16)}" fill="#161e26"/>`;
    sky += `<g filter="url(#skBlur4)">${wc}</g>`;
    sky += `<g id="${id}-meso" filter="url(#skBlur4)">${ms}</g>`;
    // the inflow band (beaver tail) feeding the storm low on the sun side, and the wall cloud the funnel hangs from
    let ib = `M${f1(x1 + sun * wt * 0.45)},${f1(y1 - 36)}`; for (let k = 1; k <= 12; k++) ib += `L${f1(x1 + sun * (wt * 0.45 + k * 130))},${f1(y1 - 36 - k * 7 + (r() - 0.5) * 14)}`;
    for (let k = 12; k >= 0; k--) ib += `L${f1(x1 + sun * (wt * 0.45 + k * 130))},${f1(y1 + 6 - k * 4 + r() * 22)}`;
    sky += `<path d="${ib}Z" fill="#3e4a54" filter="url(#skBlur4)"/><path d="M${f1(x1 + sun * wt * 0.45)},${f1(y1 - 38)}L${f1(x1 + sun * (wt * 0.45 + 1560))},${f1(y1 - 122)}" stroke="#d8c8a0" stroke-width="5" opacity=".35" filter="url(#skBlur4)"/>`;
    // lightning: cloud-to-ground in the rain on the rear side
    let bolts = ""; (o.bolts ?? [[-1.35, 0.5, 3]]).forEach(([fx, fy, sd], k) => { const bx = x0 + sun * fx * wt, by = y1 - 20; bolts += `<g opacity="${o.boltOp ?? 0.85}"><circle cx="${f1(bx)}" cy="${f1(by + 80)}" r="200" fill="url(#ngwBoltG)" opacity=".55"/>${Tk.bolt(bx, by, bx - sun * 50, y0 + 10, 30 + sd, o.boltW ?? 0.32)}</g>`; });
    sky += `<g id="${id}-bolts">${bolts}</g>`;
    // ======== mid: the funnel
    let mid = `<g id="${id}" class="ngwF" data-sp="70" data-top="${f1(x1)} ${f1(y1)}" data-base="${f1(x0)} ${f1(y0)}"><g id="${id}-sw">`;
    const bd = band(-1, 1);
    mid += `<defs><clipPath id="${id}-clip"><path d="${bd}"/></clipPath></defs>`;
    // the dust sheath round the lower third, wider than the funnel, translucent
    if (!o.noFunnel) mid += `<path d="${band(-1.45, 1.45, -0.03, 0.42)}" fill="url(#ngwSheath)" filter="url(#skBlur10)"/>`;   // the dust sheath (gone with the funnel)
    if (!o.noFunnel) mid += `<path d="${bd}" fill="url(#${sun > 0 ? "ngwFunR" : "ngwFunL"})"/><path d="${bd}" fill="url(#ngwFunV)"/>`;
    // curved spiral bands, front half only (cos > 0), dark with a pale companion; a few straight streaks slid sideways (animated)
    let hel = ""; const turns = o.turns ?? 3.2, NB = o.bands ?? 9;
    for (let j = 0; j < NB; j++) { const phi = (2 * Math.PI * j) / NB; let seg = [], segs = [];
      T.forEach((t) => { const th2 = phi + 2 * Math.PI * turns * t; if (Math.cos(th2) > 0.05) seg.push([cx(t) + hw(t) * Math.sin(th2), cy(t)]); else if (seg.length) { segs.push(seg); seg = []; } }); if (seg.length) segs.push(seg);
      segs.filter((q) => q.length > 2).forEach((q) => { const d = smooth(q); hel += `<path d="${d}" stroke="#10161c" stroke-width="${f1(10 + wb * 0.03)}" fill="none" opacity=".34" stroke-linecap="round"/><path d="${d}" stroke="#c8c0a8" stroke-width="3" fill="none" opacity=".16" transform="translate(${sun * 8},0)"/>`; }); }
    let st = ""; for (let x = Math.min(x0, x1) - wt, k = 0; x < Math.max(x0, x1) + wt + H * 0.12; x += 80, k++) st += `<path d="M${f1(x)},${f1(y0 + 30)}L${f1(x + H * 0.12)},${f1(y1 - 60)}" stroke="#0e1418" stroke-width="${k % 2 ? 10 : 22}" opacity=".14"/>`;
    if (o.noFunnel) { hel = ""; st = ""; }
    if (!o.noFunnel) mid += `<g clip-path="url(#${id}-clip)">${hel}<g id="${id}-hx">${st}</g><path d="${band(-1, -0.55)}" fill="#0a0e12" opacity="${sun > 0 ? 0.35 : 0}" filter="url(#skBlur10)"/><path d="${band(0.55, 1)}" fill="#0a0e12" opacity="${sun > 0 ? 0 : 0.35}" filter="url(#skBlur10)"/></g>`;   // the funnel's shading bands (they drew a ghost of it under noFunnel)
    // the lit rim on the sun side, the ragged scud on both edges
    const rim = smooth(T.filter((t) => t > 0.05).map((t) => [cx(t) + sun * hw(t) * 0.97, cy(t)]));
    if (!o.noFunnel) mid += `<path d="${rim}" stroke="#f0d8a4" stroke-width="6" fill="none" opacity=".6" filter="url(#skBlur4)"/>`;
    let sc = ""; for (let k = 0; k < 30; k++) { const t = 0.1 + r() * 0.95, sd = k % 2 ? 1 : -1, rr = hw(t) * (0.1 + r() * 0.12); sc += `<ellipse cx="${f1(cx(t) + sd * hw(t) * (1 + r() * 0.08))}" cy="${f1(cy(t))}" rx="${f1(rr)}" ry="${f1(rr * 0.55)}" fill="${sd === sun ? "#3a4046" : "#1e252c"}"/>`; }
    if (!o.noFunnel) mid += `<g filter="url(#skBlur10)" opacity=".85">${sc}</g>`;
    // ---- the debris fountain at the base: skirt, plume, lit puffs, dark core
    const sp = o.spray ?? wb * 0.75;
    let b = `<ellipse cx="${f1(x0)}" cy="${f1(y0 + 10)}" rx="${f1(sp * 2.1)}" ry="${f1(sp * 0.26)}" fill="#120e0a" opacity=".6" filter="url(#skBlur10)"/>`;
    b += `<path d="M${f1(x0 - sp * 1.5)},${f1(y0 + 6)}Q${f1(x0 - sp * 1.2)},${f1(y0 - sp * 1.5)} ${f1(x0)},${f1(y0 - sp * 1.9)}Q${f1(x0 + sp * 1.2)},${f1(y0 - sp * 1.5)} ${f1(x0 + sp * 1.5)},${f1(y0 + 6)}Z" fill="#6e5a44" opacity=".55" filter="url(#skBlur10)"/>`;
    let pf = "", hl = ""; for (let k = 0; k < 22; k++) { const a = (k / 22) * Math.PI * 2, rr = sp * (0.18 + r() * 0.2), px = x0 + Math.cos(a) * sp * (0.7 + r() * 0.5), py = y0 - sp * 0.12 - Math.abs(Math.sin(a)) * sp * 0.5 - r() * sp * 0.5;
      pf += `<circle cx="${f1(px)}" cy="${f1(py)}" r="${f1(rr)}" fill="${k % 3 ? "#5a4836" : "#6a5440"}"/>`; hl += `<circle cx="${f1(px + sun * rr * 0.35)}" cy="${f1(py - rr * 0.35)}" r="${f1(rr * 0.6)}" fill="#b08c62" opacity=".55"/>`; }
    b += `<g filter="url(#skBlur4)">${pf}</g><g filter="url(#skBlur10)">${hl}</g>`;
    for (let k = 0; k < 60; k++) { const a = r() * Math.PI * 2, rr = sp * (0.6 + r() * 1.6); b += `<circle cx="${f1(x0 + Math.cos(a) * rr)}" cy="${f1(y0 - sp * 0.3 + Math.sin(a) * rr * 0.3 - r() * sp * 1.2)}" r="${f1(1.6 + r() * 3)}" fill="${k % 3 ? "#2a1e14" : "#d8c070"}" opacity=".85"/>`; }
    const ng = o.noGround ? ' opacity="0"' : "";   // o.noGround (with noFunnel): nothing on the ground yet — no fountain, vortices, flying debris or inflow
    mid += `<g id="${id}-base"${ng}>${b}</g>`;
    mid += `</g>`;
    let col = ""; for (let k = 0; k < 11; k++) { const u = (k + 0.5) / 11, rr = wt * (0.14 + r() * 0.08); col += `<ellipse cx="${f1(x1 - wt * 0.7 + u * wt * 1.4)}" cy="${f1(y1 - 6 + Math.sin(u * Math.PI) * 14 + r() * 10)}" rx="${f1(rr * 1.5)}" ry="${f1(rr * 0.7)}" fill="${k % 3 ? "#161e26" : "#222c34"}"/>`; }
    mid += `<g filter="url(#skBlur10)">${col}<ellipse cx="${f1(x1)}" cy="${f1(y1 - 40)}" rx="${f1(wt * 0.74)}" ry="${f1(wt * 0.12)}" fill="#161e26"/></g>`;
    mid += `<path d="M${f1(x1 + sun * wt * 0.3)},${f1(y1 + 2)}Q${f1(x1 + sun * wt * 0.6)},${f1(y1 + 8)} ${f1(x1 + sun * wt * 0.78)},${f1(y1 - 20)}" stroke="#e8d4a8" stroke-width="6" fill="none" opacity=".45" filter="url(#skBlur4)"/>`;
    mid += `</g>`;
    // ---- sub-vortices whipping round the base (multiple-vortex)
    let subs = ""; (o.subs ?? [[-1.05, 0.22], [0.95, 0.18], [-0.35, 0.14]]).forEach(([fx, fh], k) => { const bx = x0 + fx * sp * 1.2, hh = H * fh, pts = []; for (let i = 0; i <= 10; i++) { const u = i / 10; pts.push([bx + Math.sin(u * 7 + k) * 10 + (x0 - bx) * u * 0.35, y0 - u * hh]); }
      const d = smooth(pts); subs += `<g class="${id}-sub"><path d="${d}" stroke="#3e3830" stroke-width="${f1(22 - k * 4)}" fill="none" stroke-linecap="round" opacity=".85"/><path d="${d}" stroke="#a88c68" stroke-width="5" fill="none" stroke-linecap="round" opacity=".6" transform="translate(${sun * 6},0)"/><circle cx="${f1(bx)}" cy="${f1(y0 - 10)}" r="${f1(36 - k * 6)}" fill="#7a6248" opacity=".75" filter="url(#skBlur4)"/></g>`; });
    mid += `<g id="${id}-subs"${ng}>${subs}</g>`;
    // ---- debris with motion streaks (a curved tail behind each piece), big pieces high in the plume
    // QA 5 ("the same upside-down car in the same spot in five shots"): without o.big the pieces are jittered and the car moved to
    // another slot by the seed, so no two plates share their debris
    const BIG0 = [[-0.9, 0.18, "sheet", 1], [0.85, 0.3, "car", 1.1], [0.5, 0.52, "plank", 1], [-0.55, 0.62, "sheet", 0.8], [0.15, 0.82, "plank", 0.7], [-1.2, 0.08, "tree", 1.1], [1.15, 0.12, "sheet", 0.9], [-0.2, 0.42, "plank", 0.8]];
    const bigL = o.big || (() => { const rb = mk((o.seed || 41) * 13 + 7), L = BIG0.map(([fx, fy, kd, s2]) => [fx + (rb() - 0.5) * 0.45, Math.max(0.06, fy + (rb() - 0.5) * 0.18), kd, s2]);
      const kc = Math.floor(rb() * L.length); [L[1][2], L[kc][2]] = [L[kc][2], L[1][2]]; return L; })();
    let big = ""; bigL.forEach(([fx, fy, kind, s2], k) => {
      const x = x0 + fx * (wb * 1.3 + 100), y = y0 - fy * H, a = Math.round(r() * 80 - 40), scl = s2 * (o.bigScale ?? 1);
      const shape = kind === "car" ? `<path d="M-40,8V-6L-26,-20H18L34,-6H44V8Z" fill="#c8cfd4" stroke="${INK}" stroke-width="3"/><rect x="-20" y="-16" width="16" height="10" fill="#5a6a78"/><rect x="2" y="-16" width="16" height="10" fill="#5a6a78"/><circle cx="-24" cy="10" r="8" fill="#222" stroke="${INK}" stroke-width="2"/><circle cx="28" cy="10" r="8" fill="#222" stroke="${INK}" stroke-width="2"/>`
        : kind === "plank" ? `<rect x="-34" y="-5" width="68" height="10" fill="#8a6a44" stroke="${INK}" stroke-width="2.4"/>`
        : kind === "tree" ? `<path d="M0,30V-10" stroke="#4a3220" stroke-width="7"/><circle cx="0" cy="-22" r="22" fill="#2e4a2a" stroke="${INK}" stroke-width="2.4"/><circle cx="-14" cy="-10" r="14" fill="#2e4a2a"/><circle cx="14" cy="-12" r="15" fill="#2e4a2a"/>`
        : `<path d="M-30,-14L28,-18L32,12L-26,16Z" fill="#a8b0b4" stroke="${INK}" stroke-width="2.6"/><path d="M-20,-14L-16,15M-6,-15L-2,14M8,-16L12,13M20,-17L24,12" stroke="#78848a" stroke-width="2"/>`;
      const dir = fx < 0 ? 1 : -1;   // pieces left of the funnel swing right in front of it, and back
      big += `<path d="M${f1(x - dir * 120 * scl)},${f1(y + 26 * scl)}Q${f1(x - dir * 60 * scl)},${f1(y + 4)} ${f1(x - dir * 20)},${f1(y)}" stroke="#d8d0c0" stroke-width="${f1(3 * scl + 1)}" fill="none" opacity=".35" stroke-linecap="round"/>`;
      big += `<g class="${id}-bd" transform="translate(${f1(x)},${f1(y)}) rotate(${a}) scale(${f1(scl)})">${shape}</g>`; });
    mid += `<g id="${id}-big"${ng}>${big}</g>`;
    // ---- inflow dust racing along the ground into the base from both sides
    let fl = ""; for (let k = 0; k < 18; k++) { const sd = k % 2 ? 1 : -1, x = x0 + sd * (sp * 2 + 200 + r() * 1100), y = y0 + 6 + r() * 70; fl += `<path d="M${f1(x)},${f1(y)}Q${f1(x0 + sd * sp * 1.6)},${f1(y + 10)} ${f1(x0 + sd * sp * 0.9)},${f1(y0 - 6 - r() * 20)}" stroke="#9a8060" stroke-width="${f1(3 + r() * 7)}" fill="none" opacity="${f1(0.25 + r() * 0.25)}" stroke-linecap="round" filter="url(#skBlur4)"/>`; }
    mid += `<g${ng}>${fl}</g>`;
    (o.flashes || [[-1.6, 0.02], [1.8, 0.04]]).forEach(([fx, fy]) => { const x = x0 + fx * sp, y = y0 - fy * H; mid += `<g class="${id}-pf"><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(sp * 0.5)}" fill="url(#ngwPF)"/><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(sp * 0.06)}" fill="#f4fffc"/></g>`; });
    return { sky, mid };
  };
  Ngw.epicLife = (tl, id, t0, dur, o = {}) => {
    const root = document.getElementById(id); if (!root) return; const n = (p) => Math.max(1, Math.ceil(dur / p));
    const top = root.dataset.top, base = root.dataset.base;
    if (document.getElementById(`${id}-hx`)) tl.fromTo(`#${id}-hx`, { x: 0 }, { x: 160, duration: o.spin ?? 0.7, ease: "none", repeat: n(o.spin ?? 0.7), immediateRender: false }, t0);   // (no helix under noFunnel)
    tl.fromTo(`#${id}-sw`, { skewX: -1.2, svgOrigin: top }, { skewX: 1.2, svgOrigin: top, duration: 1.6, ease: "sine.inOut", yoyo: true, repeat: n(1.6), immediateRender: false }, t0);
    tl.fromTo(`#${id}-base`, { scale: 0.97, svgOrigin: base }, { scale: 1.04, svgOrigin: base, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: n(0.6), immediateRender: false }, t0);
    tl.fromTo(`#${id}-meso`, { x: -12 }, { x: 12, duration: 2.6, ease: "sine.inOut", yoyo: true, repeat: n(2.6), immediateRender: false }, t0);
    document.querySelectorAll(`.${id}-sub`).forEach((e, k) => tl.fromTo(e, { x: -30 + k * 20 }, { x: 40 - k * 20, duration: 0.5 + k * 0.15, ease: "sine.inOut", yoyo: true, repeat: n(0.5), immediateRender: false }, t0));
    document.querySelectorAll(`.${id}-bd`).forEach((e, k) => tl.to(e, { rotation: `+=${k % 2 ? 300 : -300}`, x: `+=${k % 2 ? 70 : -70}`, y: `-=${40 + k * 8}`, duration: dur, ease: "none", immediateRender: false }, t0));
    document.querySelectorAll(`.${id}-pf`).forEach((e, k) => tl.fromTo(e, { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.04 }, { opacity: 0.3, duration: 0.06 }, { opacity: 0.9, duration: 0.05 }, { opacity: 0, duration: 0.35 }], immediateRender: false }, t0 + (o.flashAt || [0.6, 1.7])[k % 2]));
    const bl = document.getElementById(`${id}-bolts`); if (bl && o.boltAt != null) { tl.set(bl, { opacity: 0 }, t0); tl.fromTo(bl, { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.03 }, { opacity: 0.2, duration: 0.05 }, { opacity: 1, duration: 0.04 }, { opacity: 0, duration: 0.3 }], immediateRender: false }, t0 + o.boltAt); }
  };

  // ---------------------------------------------------------------- title, live screen, house cutaway (the ทะเลลด extras)
  // the title painted on the highway, seen from above: elongated road-marking letters, the storm's dark swirl and dust coming over the
  // top of the frame, debris skidding across, ยายบัว's stall umbrella at the roadside
  Sets.ngwRoadTop = (L, o = {}) => {
    const r = mk(o.seed || 91), id = o.id || "rt";
    let g = `<rect x="-1400" y="-800" width="4000" height="3600" fill="#3e6a2e"/>`;
    for (let k = 0; k < 90; k++) g += `<path d="M-1400,${-800 + k * 40}H2600" stroke="${k % 2 ? "#36602a" : "#4a7a36"}" stroke-width="18" opacity=".7"/>`;
    for (let k = 0; k < 26; k++) g += `<path d="M${-1300 + k * 160},-800V2800" stroke="#5a4a32" stroke-width="10" opacity=".55"/>`;
    put(L.sky, g);
    let m = `<rect x="200" y="-800" width="680" height="3600" fill="#8a8470"/><rect x="236" y="-800" width="608" height="3600" fill="#3a3c40"/>`;
    m += `<path d="M262,-800V2800M818,-800V2800" stroke="#e8e4d8" stroke-width="10"/><path d="M540,-800V2800" stroke="#f2c230" stroke-width="12" stroke-dasharray="90 70"/>`;
    for (let k = 0; k < 60; k++) m += `<path d="M${f1(250 + r() * 580)},${f1(-700 + r() * 3300)}l${f1(20 + r() * 40)},0" stroke="#9aa4ac" stroke-width="2" opacity=".3"/>`;
    // the title in road paint, stretched along the lane like real markings
    m += `<g transform="translate(540,${o.ty ?? 1160}) scale(1,2.1)"><text text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${o.fs ?? 150}" fill="#f4f2ea" opacity=".95" letter-spacing="4">${o.title || "เสียงรถไฟ"}</text></g>`;
    m += `<g transform="translate(540,${(o.ty ?? 1160) + 260}) scale(1,1.6)"><text text-anchor="middle" font-family="Kanit" font-weight="800" font-size="58" fill="#f2c230" opacity=".95">${o.sub || "ตอนที่ 1"}</text></g>`;
    put(L.mid, m);
    // the stall umbrella from above, a motorbike, debris skidding, leaves
    let st = `<g transform="translate(980,1460)"><circle r="120" fill="#f2f0ea" stroke="#1e1a16" stroke-width="6"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M0,0L${f1(120 * Math.cos(k * Math.PI / 3))},${f1(120 * Math.sin(k * Math.PI / 3))}A120,120 0 0 1 ${f1(120 * Math.cos((k + 0.5) * Math.PI / 3))},${f1(120 * Math.sin((k + 0.5) * Math.PI / 3))}Z" fill="#2a6ad0"/>`).join("")}<circle r="10" fill="#1e1a16"/></g>`;
    st += Ngw.debris(200, 1000, 300, 1900, 26, 92, 0.9);
    put(L.set, st);
    // the storm over the top: a dark spiral and the dust coming
    let sw = `<defs><radialGradient id="${id}-dk" cx=".5" cy=".1" r=".75"><stop offset="0" stop-color="#0a0e12" stop-opacity=".95"/><stop offset=".5" stop-color="#141c22" stop-opacity=".7"/><stop offset="1" stop-color="#1a2228" stop-opacity="0"/></radialGradient></defs>`;
    sw += `<rect x="-1400" y="-800" width="4000" height="1900" fill="url(#${id}-dk)"/>`;
    for (let k = 0; k < 7; k++) sw += `<path d="M${540 + 120 * k},${-100 + 30 * k}A${300 + k * 110},${200 + k * 80} 0 0 1 ${540 - 260 - k * 90},${260 + k * 70}" stroke="#7a6a54" stroke-width="${30 - k * 3}" fill="none" opacity="${f1(0.4 - k * 0.04)}" filter="url(#skBlur10)"/>`;
    put(L.light, sw + Ngw.streaks(-200, 1400, 200, 1500, 40, 93));
  };
  // ฝน's live screen over the shot (screen space, L.light): avatar + name + LIVE, a heart button with hearts rising, comments sliding
  // up from the bottom, the comment box — no viewer numbers
  Ngw.liveUI = (o = {}) => {
    const name = o.name || "ฝนพาเที่ยว", cm = o.comments || [];
    let g = `<rect x="0" y="0" width="1080" height="260" fill="#000" opacity=".28"/>${o.noBottom ? "" : `<rect x="0" y="1380" width="1080" height="540" fill="#000" opacity=".3"/>`}`;
    g += `<g transform="translate(70,120)"><circle r="46" fill="#f2be2a" stroke="#ff3a6a" stroke-width="7"/><circle cy="-6" r="22" fill="#ebc19c"/><path d="M-26,-14Q-24,-44 2,-44Q26,-42 26,-14Q14,-30 -4,-28Q-18,-30 -26,-14Z" fill="#1e1410"/><path d="M-30,30Q0,10 30,30" stroke="#f2be2a" stroke-width="14"/></g>`;
    g += `<text x="136" y="112" font-family="Kanit" font-weight="700" font-size="40" fill="#fff">${name}</text><text x="136" y="156" font-family="Kanit" font-size="30" fill="#e8e8e8" opacity=".85">${o.title || "พายุมาแล้ววว"}</text>`;
    g += `<g transform="translate(860,104)"><rect x="-70" y="-30" width="140" height="56" rx="12" fill="#ff2a4a"/><circle cx="-42" cy="-2" r="9" fill="#fff"/><text x="12" y="12" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#fff">LIVE</text></g>`;
    g += `<g transform="translate(990,104)"><circle r="30" fill="#000" opacity=".35"/><path d="M-12,-12L12,12M12,-12L-12,12" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity="0"/></g>`;
    cm.forEach(([nm, tx, c], k) => { const y = (o.cy ?? 1340) + k * 92;
      g += `<g transform="translate(40,${y})"><rect x="0" y="-44" width="${Math.min(880, 120 + tx.length * 26 + nm.length * 22)}" height="76" rx="38" fill="#000" opacity=".35"/><circle cx="38" cy="-6" r="24" fill="${c || "#6a8ac8"}"/><text x="76" y="4" font-family="Kanit" font-weight="700" font-size="30" fill="#ffd25a">${nm}</text><text x="${84 + nm.length * 19}" y="4" font-family="Kanit" font-size="32" fill="#fff">${tx}</text></g>`; });
    g += `<g transform="translate(40,1840)"><rect x="0" y="-40" width="820" height="72" rx="36" fill="#fff" opacity=".18"/><text x="34" y="8" font-family="Kanit" font-size="30" fill="#fff" opacity=".8">แสดงความคิดเห็น...</text></g>`;
    g += `<g transform="translate(960,1800)"><circle r="44" fill="#ff3a6a"/><path d="M0,16C-24,-2 -28,-20 -14,-26C-6,-29 0,-22 0,-17C0,-22 6,-29 14,-26C28,-20 24,-2 0,16Z" fill="#fff"/></g>`;
    [[960, 1690, 1.2, "#ff4a6a"], [930, 1580, 1, "#ff9ab0"], [985, 1470, 0.9, "#ff4a6a"], [945, 1360, 0.7, "#ffd0d8"], [975, 1250, 0.55, "#ff4a6a"]].forEach(([x, y, s2, c]) => { g += `<path transform="translate(${x},${y}) scale(${s2 * 1.6})" d="M0,8C-14,-2 -18,-14 -9,-19C-4,-22 0,-17 0,-14C0,-17 4,-22 9,-19C18,-14 14,-2 0,8Z" fill="${c}" stroke="#fff" stroke-width="1.6"/>`; });
    return g;
  };
  // the cutaway house on a board: "หลบตรงไหนในบ้าน?" — the inner bathroom on the ground floor glows green (the family crouched in it),
  // the windows and the upper floor glow red, the wind and debris hit from the right
  Sets.ngwHouseCut = (L, o = {}) => {
    put(L.sky, `<rect x="-1400" y="-800" width="4000" height="3600" fill="#1a2028"/><rect x="-1400" y="-800" width="4000" height="3600" fill="url(#ngwSun)" opacity=".18"/>`);
    const X = 540, Y = 1500, I = "#1e1a16";
    let g = `<rect x="-1400" y="${Y}" width="4000" height="900" fill="#3a3226"/><path d="M-1400,${Y}H2600" stroke="#5a4a36" stroke-width="12"/>`;
    // the house: two floors, cut open; walls, slab, roof
    g += `<path d="M120,${Y}V${Y - 760}H960V${Y}Z" fill="#e8dcc0" stroke="${I}" stroke-width="8"/><path d="M120,${Y - 380}H960" stroke="${I}" stroke-width="14"/>`;
    g += `<path d="M80,${Y - 760}L540,${Y - 1060}L1000,${Y - 760}Z" fill="#a8442e" stroke="${I}" stroke-width="8"/>${[1, 2, 3, 4, 5].map((k) => `<path d="M${80 + k * 76},${Y - 760}L540,${Y - 1060}" stroke="#7a2e1e" stroke-width="3" opacity=".5"/>`).join("")}`;
    // rooms: ground floor — living room (window, left), the inner bathroom (no window, centre), kitchen (window, right); upper floor
    g += `<path d="M380,${Y}V${Y - 380}M700,${Y}V${Y - 380}" stroke="${I}" stroke-width="10"/>`;
    g += `<rect x="388" y="${Y - 372}" width="304" height="364" fill="#9ac0a8"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M388,${Y - 300 + k * 64}H692" stroke="#6a9a80" stroke-width="3"/>`).join("")}${[0, 1, 2, 3].map((k) => `<path d="M${450 + k * 64},${Y - 372}V${Y - 8}" stroke="#6a9a80" stroke-width="3"/>`).join("")}`;
    const win = (x, y) => `<g><rect x="${x}" y="${y}" width="120" height="120" fill="#9ad0f0" stroke="${I}" stroke-width="6"/><path d="M${x + 60},${y}V${y + 120}M${x},${y + 60}H${x + 120}M${x + 14},${y + 20}l40,46M${x + 80},${y + 16}l-20,34" stroke="${I}" stroke-width="3"/></g>`;
    g += win(180, Y - 300) + win(780, Y - 300) + win(220, Y - 680) + win(740, Y - 680);
    g += `<path d="M380,${Y - 380}L240,${Y}" stroke="#8a6a44" stroke-width="10"/>${[1, 2, 3, 4, 5, 6].map((k) => `<path d="M${380 - k * 20},${Y - 380 + k * 54}h40" stroke="#8a6a44" stroke-width="6"/>`).join("")}`;
    // the family crouched in the bathroom: three small figures, arms over heads
    g += [[450, 1], [540, 0.9], [625, 0.75]].map(([x, s2]) => `<g transform="translate(${x},${Y - 10}) scale(${s2})"><path d="M-34,0Q-36,-44 -10,-70L22,-64Q30,-30 34,0Z" fill="#c8483a" stroke="${I}" stroke-width="4"/><circle cx="18" cy="-78" r="20" fill="#d49c6c" stroke="${I}" stroke-width="4"/><path d="M-6,-70Q10,-112 34,-90" stroke="#d49c6c" stroke-width="12" fill="none" stroke-linecap="round"/></g>`).join("");
    // glows: green on the safe room, red on the windows and the upper floor
    g += `<rect x="388" y="${Y - 372}" width="304" height="364" fill="none" stroke="#3aff8a" stroke-width="14" opacity=".9" filter="url(#skBlur4)"/><rect x="388" y="${Y - 372}" width="304" height="364" fill="none" stroke="#c8ffd8" stroke-width="5"/>`;
    g += [[180, Y - 300], [780, Y - 300], [220, Y - 680], [740, Y - 680]].map(([x, y]) => `<rect x="${x}" y="${y}" width="120" height="120" fill="#ff3a3a" opacity=".25"/><rect x="${x - 4}" y="${y - 4}" width="128" height="128" fill="none" stroke="#ff4a4a" stroke-width="8" opacity=".85" filter="url(#skBlur4)"/>`).join("");
    g += `<rect x="128" y="${Y - 752}" width="824" height="364" fill="#ff3a3a" opacity=".1"/>`;
    // wind and debris from the right; a small tornado
    g += `<g transform="translate(1120,${Y - 520}) scale(.9)"><path d="M-80,-200H80L40,-80L50,0L20,100L0,200L-14,100L-30,0L-50,-80Z" fill="#4a5258" stroke="${I}" stroke-width="4"/></g>`;
    g += [Y - 640, Y - 500, Y - 360, Y - 220].map((y) => `<path d="M1060,${y}H990" stroke="#e8eef0" stroke-width="10" stroke-linecap="round"/><path d="M1000,${y - 16}L980,${y}L1000,${y + 16}" stroke="#e8eef0" stroke-width="8" fill="none" stroke-linecap="round"/>`).join("");
    put(L.set, g);
    // labels (in the world, on paper tags)
    const tag = (x, y, t, c, w = 360) => `<g transform="translate(${x},${y})"><rect x="${-w / 2}" y="-40" width="${w}" height="72" rx="14" fill="#fff8e8" stroke="${c}" stroke-width="6"/><text y="10" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="${c}">${t}</text></g>`;
    put(L.set, tag(540, Y + 80, "ห้องในสุด ชั้นล่าง ไม่มีหน้าต่าง", "#1a8a4a", 560) + tag(240, Y - 820, "ห่างหน้าต่าง", "#d8312a", 280) + tag(840, Y - 820, "ไม่ขึ้นชั้นบน", "#d8312a", 280));
    let lb = `<g transform="translate(540,300)"><rect x="-440" y="-80" width="880" height="140" rx="24" fill="#8a6a3e" stroke="#2a1a0c" stroke-width="7"/><text y="20" text-anchor="middle" font-family="Sriracha" font-size="78" fill="#fff6dc" stroke="#2a1a0c" stroke-width="8" paint-order="stroke">หลบตรงไหนในบ้าน?</text></g>`;
    put(L.light, lb);
  };

  // ---------------------------------------------------------------- ยายบัว's rule sign (owner: "ป้ายกฏ เอาให้เขาธีมสิ")
  // a hand-painted corrugated zinc sheet nailed to two posts by the highway: hazard stripes top and bottom, rust running from the
  // nails, a bent corner, round road-sign discs for the icons, the rules in brush lettering with the rhymes in red; it drops in,
  // rows paint on one by one, the rule of this episode gets a yellow brush swipe, the others stay faint; the sheet sways and rattles
  // in the wind, rain streaks over it. o.rules [[pictogram SVG (120 box), text with <u>rhyme</u>]…] · o.active · o.y · o.title
  Ngw.ruleBoard = (tl, layer, t0, dur, o = {}) => {
    // o.blank: one more, empty line under the rules — "4. …" with a dashed disc (QA: rule 4 had no set-up; ยายบัว's sign keeps a slot for it)
    const id = `rb${Math.round(t0 * 100)}`, I = "#1e1a16", Y0 = o.y ?? 330, X0 = 60, W = 960, rows = o.rules || [], n = rows.length, GAP = o.gap ?? 210, H = 290 + (n + (o.blank ? 1 : 0)) * GAP, act = o.active ?? 0;
    const r = mk(o.seed || 97);
    let g = `<g id="${id}"><g id="${id}-sw">`;
    // posts — or, with o.hang, two ropes up out of the frame: the sign recalled away from the stall (under the bridge, in the bathroom)
    // hangs like ทะเลลด's rope-hung boards instead of standing on posts where it could not be (QA 5)
    g += o.hang ? [X0 + 150, X0 + W - 150].map((x) => `<path d="M${x},${Y0 + 22}V${Y0 - 2600}" stroke="#3a2c1e" stroke-width="8"/><path d="M${x + 3},${Y0 + 20}V${Y0 - 2600}" stroke="#8a7050" stroke-width="2.6" stroke-dasharray="8 10" opacity=".8"/><circle cx="${x}" cy="${Y0 + 22}" r="14" fill="none" stroke="#3a2c1e" stroke-width="7"/>`).join("")
      : [X0 + 150, X0 + W - 150].map((x) => `<rect x="${x - 22}" y="${Y0 + 40}" width="44" height="${1920 - Y0}" fill="#6a4a2e" stroke="${I}" stroke-width="5"/><path d="M${x - 10},${Y0 + 60}V1920" stroke="#8a6a44" stroke-width="6" opacity=".6"/>`).join("");
    // the zinc sheet: corrugation, a dented outline, rust streaks, a bent corner
    let ol = `M${X0},${Y0 + 8}`; for (let k = 1; k <= 12; k++) ol += `L${f1(X0 + (W * k) / 12)},${f1(Y0 + (r() - 0.5) * 10)}`;
    ol += `L${X0 + W - 6},${Y0 + H}`; for (let k = 11; k >= 0; k--) ol += `L${f1(X0 + (W * k) / 12)},${f1(Y0 + H + (r() - 0.5) * 12)}`; ol += "Z";
    g += `<defs><clipPath id="${id}-cp"><path d="${ol}"/></clipPath><linearGradient id="${id}-zn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8ccc8"/><stop offset=".5" stop-color="#aeb4b2"/><stop offset="1" stop-color="#8e9694"/></linearGradient></defs>`;
    g += `<path d="${ol}" fill="#000" opacity=".35" transform="translate(10,14)"/><path d="${ol}" fill="url(#${id}-zn)" stroke="${I}" stroke-width="7" stroke-linejoin="round"/>`;
    let cor = ""; for (let x = X0; x < X0 + W; x += 44) cor += `<rect x="${x}" y="${Y0 - 20}" width="18" height="${H + 40}" fill="#e8ecea" opacity=".35"/><rect x="${x + 24}" y="${Y0 - 20}" width="10" height="${H + 40}" fill="#5a6260" opacity=".25"/>`;
    for (let k = 0; k < 14; k++) { const x = X0 + 30 + r() * (W - 60), y = Y0 + 30 + r() * (H - 120), L0 = 60 + r() * 200; cor += `<path d="M${f1(x)},${f1(y)}q${f1((r() - 0.5) * 12)},${f1(L0 / 2)} ${f1((r() - 0.5) * 10)},${f1(L0)}" stroke="#8a4a1e" stroke-width="${f1(4 + r() * 8)}" fill="none" opacity="${f1(0.15 + r() * 0.2)}" stroke-linecap="round"/>`; }
    // hazard stripes top and bottom
    const haz = (y) => { let h = `<rect x="${X0 - 10}" y="${y}" width="${W + 20}" height="46" fill="#f2c230"/>`; for (let x = X0 - 60; x < X0 + W + 40; x += 64) h += `<path d="M${x},${y + 46}L${x + 32},${y}H${x + 64}L${x + 32},${y + 46}Z" fill="#1e1a16"/>`; return h; };
    g += `<g clip-path="url(#${id}-cp)">${cor}${haz(Y0 + 6)}${haz(Y0 + H - 52)}</g>`;
    // nails with rust halos, a bent top-right corner, a leaf caught
    g += [[X0 + 30, Y0 + 80], [X0 + W - 30, Y0 + 80], [X0 + 30, Y0 + H - 80], [X0 + W - 30, Y0 + H - 80], [X0 + 150, Y0 + H / 2], [X0 + W - 150, Y0 + H / 2]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="16" fill="#8a4a1e" opacity=".35"/><circle cx="${x}" cy="${y}" r="8" fill="#6a6e70" stroke="${I}" stroke-width="2.6"/>`).join("");
    g += `<g id="${id}-flap"><path d="M${X0 + W - 120},${Y0 - 4}L${X0 + W + 4},${Y0 - 2}L${X0 + W - 2},${Y0 + 120}Z" fill="#7e8684" stroke="${I}" stroke-width="5" stroke-linejoin="round"/><path d="M${X0 + W - 110},${Y0 + 6}L${X0 + W - 10},${Y0 + 100}" stroke="#c8ccc8" stroke-width="4"/></g>`;
    g += `<path d="M${X0 + 40},${Y0 + H - 30}q30,-40 70,-20q-20,30 -70,20z" fill="#3e6a2a" stroke="${I}" stroke-width="3" transform="rotate(-20 ${X0 + 70} ${Y0 + H - 40})"/>`;
    // the title, brush-painted
    g += `<g transform="translate(540,${Y0 + 160}) rotate(-2)"><text text-anchor="middle" font-family="Sriracha" font-size="96" fill="#d8312a" stroke="#fff8ec" stroke-width="12" paint-order="stroke">${o.title || "กฎของยายบัว"}</text><path d="M-250,26Q0,46 250,22" stroke="#d8312a" stroke-width="7" fill="none" stroke-linecap="round"/></g>`;
    // rows: a road-sign disc + brush lettering; the active one on a yellow swipe
    rows.forEach(([pic, txt], k) => { const y = Y0 + 300 + k * GAP, isA = k === act;
      const t = txt.replace(/<u>(.*?)<\/u>/g, `<tspan fill="#d8312a">$1</tspan>`);
      g += `<g id="${id}-r${k}" opacity="${isA ? 0 : 0}">`;
      if (isA) g += `<path id="${id}-hl" d="M240,${y - 58}Q560,${y - 76} 1000,${y - 54}L1006,${y + 38}Q600,${y + 56} 236,${y + 34}Z" fill="#ffd23a" opacity=".85"/>`;
      g += `<g transform="translate(${X0 + 104},${y - 14})"><circle r="78" fill="#fff" stroke="#d8312a" stroke-width="14"/><circle r="78" fill="none" stroke="${I}" stroke-width="4"/><g transform="translate(-58,-62) scale(.97)">${pic}</g></g>`;
      g += `<text x="250" y="${y + 18}" font-family="Sriracha" font-size="62" fill="${I}">${t}</text></g>`; });
    if (o.blank) { const y = Y0 + 300 + n * GAP;
      g += `<g id="${id}-r${n}" opacity="0"><g transform="translate(${X0 + 104},${y - 14})"><circle r="78" fill="#fff" opacity=".55" stroke="#8a8e8c" stroke-width="8" stroke-dasharray="22 16"/><text y="30" text-anchor="middle" font-family="Sriracha" font-size="86" fill="#8a8e8c">?</text></g>
        <text x="250" y="${y + 18}" font-family="Sriracha" font-size="62" fill="#6a6e6c">${n + 1}.</text><path d="M330,${y + 12}H${X0 + W - 70}" stroke="#6a6e6c" stroke-width="6" stroke-dasharray="16 18" stroke-linecap="round"/></g>`; }
    g += `</g></g>`;
    put(layer, g);
    // animation: drop in, rows paint on, the active row's swipe, wind sway, the flapping corner, the faint later rows
    const q = (s) => document.getElementById(`${id}${s}`), n2 = (p) => Math.max(1, Math.ceil(dur / p));
    tl.fromTo(q(""), { y: -260, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.6)", immediateRender: false }, t0);
    tl.set(q(""), { opacity: 0 }, Math.max(0, t0 - 0.01));
    tl.fromTo(q("-sw"), { rotation: -1.4, svgOrigin: `540 ${Y0}` }, { rotation: 1.4, svgOrigin: `540 ${Y0}`, duration: 0.9, ease: "sine.inOut", yoyo: true, repeat: n2(0.9), immediateRender: false }, t0);
    tl.fromTo(q("-flap"), { rotation: 0, svgOrigin: `${X0 + W - 120} ${Y0}` }, { rotation: -14, svgOrigin: `${X0 + W - 120} ${Y0}`, duration: 0.12, ease: "sine.inOut", yoyo: true, repeat: n2(0.12), immediateRender: false }, t0);
    rows.forEach((_, k) => { const at = (o.at || [0.35, 0.5, 0.65])[k] ?? 0.35 + 0.15 * k, isA = k === act;
      tl.fromTo(q(`-r${k}`), { opacity: 0, x: -30 }, { opacity: isA ? 1 : (o.faint ?? 0.42), x: 0, duration: 0.3, ease: "power2.out", immediateRender: false }, t0 + at); });
    if (o.blank) tl.fromTo(q(`-r${n}`), { opacity: 0 }, { opacity: 0.8, duration: 0.3, immediateRender: false }, t0 + ((o.at || [])[n] ?? 0.35 + 0.15 * n));
    if (q("-hl")) tl.fromTo(q("-hl"), { scaleX: 0, svgOrigin: `240 0` }, { scaleX: 1, svgOrigin: `240 0`, duration: 0.35, ease: "power2.out", immediateRender: false }, t0 + 0.75);
    if (o.out != null) tl.to(q(""), { y: -300, opacity: 0, duration: 0.35, ease: "power2.in", immediateRender: false }, t0 + o.out);
  };

  // ---------------------------------------------------------------- EP.1 inserts and themed UI
  // the title painted on the highway, seen at a grazing angle in the side-view world (o.roadTitle on ngwScape)
  Ngw.roadTitle = (o = {}) => `<g transform="translate(${o.x ?? 540},${o.y ?? 1730}) scale(1,${o.k ?? 0.34})"><text text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${o.fs ?? 230}" fill="#f4f2ea" opacity=".92" letter-spacing="6">${o.text || "เสียงรถไฟ"}</text>
    <text y="${o.fs ? o.fs * 0.62 : 150}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="${(o.fs ?? 230) * 0.42}" fill="#f2c230" opacity=".95">${o.sub ?? "ตอนที่ 1"}</text></g>`;
  // a round wall clock (the stall's), ids #id-h #id-m for the hands; Ngw.clockSpin turns it from one time to another
  Ngw.clock = (id, x, y, s = 1, h = 15, m = 0) => { let g = `<g transform="translate(${x},${y}) scale(${s})"><circle r="300" fill="#2a2420" opacity=".25" transform="translate(16,20)"/><circle r="300" fill="#f2ead8" stroke="#1e1a16" stroke-width="22"/><circle r="270" fill="none" stroke="#c8402a" stroke-width="8"/>`;
    for (let k = 0; k < 12; k++) { const a = (k / 12) * Math.PI * 2; g += `<path d="M${f1(Math.sin(a) * 240)},${f1(-Math.cos(a) * 240)}L${f1(Math.sin(a) * 210)},${f1(-Math.cos(a) * 210)}" stroke="#1e1a16" stroke-width="${k % 3 ? 8 : 16}" stroke-linecap="round"/>`; }
    g += `<g id="${id}-h" transform="rotate(${((h % 12) + m / 60) * 30})"><path d="M0,30V-150" stroke="#1e1a16" stroke-width="22" stroke-linecap="round"/></g><g id="${id}-m" transform="rotate(${m * 6})"><path d="M0,40V-215" stroke="#1e1a16" stroke-width="12" stroke-linecap="round"/></g><circle r="20" fill="#c8402a" stroke="#1e1a16" stroke-width="5"/></g>`; return g; };
  Ngw.clockSpin = (tl, id, t0, dur, from, to) => {   // from/to in hours (14.5 = 2:30); the minute hand runs, the hour hand follows
    tl.fromTo(`#${id}-m`, { rotation: from * 360, svgOrigin: "0 0" }, { rotation: to * 360, svgOrigin: "0 0", duration: dur, ease: "power2.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-h`, { rotation: from * 30, svgOrigin: "0 0" }, { rotation: to * 30, svgOrigin: "0 0", duration: dur, ease: "power2.inOut", immediateRender: false }, t0); };
  // ฝน's phone filling the frame: a sound recorder showing thunder (one spike that fades) above this sound (one band that never stops)
  Ngw.phoneWave = (id) => { const I = "#1e1a16"; let g = `<rect x="-1400" y="-800" width="4000" height="3600" fill="#1a1e24"/><g transform="translate(540,960)"><rect x="-420" y="-820" width="840" height="1640" rx="90" fill="#26262e" stroke="${I}" stroke-width="10"/><rect x="-380" y="-760" width="760" height="1520" rx="50" fill="#0e1218"/>`;
    g += `<text x="0" y="-620" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="56" fill="#e8eef2">บันทึกเสียง</text><circle cx="0" cy="-520" r="16" fill="#ff3a4a"/>`;
    const lane = (y, label, c) => `<text x="-330" y="${y - 170}" font-family="Kanit" font-weight="700" font-size="52" fill="${c}">${label}</text><path d="M-330,${y}H330" stroke="#3a4048" stroke-width="3"/>`;
    g += lane(-200, "ฟ้าร้อง", "#9ab8ff") + lane(380, "เสียงนี้", "#ffb84a");
    let th = ""; for (let k = 0; k < 66; k++) { const x = -330 + k * 10, a = k > 8 && k < 20 ? 140 * Math.exp(-(k - 9) * 0.28) * (0.6 + 0.4 * Math.sin(k * 2.1)) : 4; th += `<path d="M${x},${f1(-200 - a)}V${f1(-200 + a)}" stroke="#9ab8ff" stroke-width="6" stroke-linecap="round"/>`; }
    let ro = ""; for (let k = 0; k < 66; k++) { const x = -330 + k * 10, a = 90 + 40 * Math.sin(k * 0.9) + 20 * Math.sin(k * 2.3); ro += `<path d="M${x},${f1(380 - a)}V${f1(380 + a)}" stroke="#ffb84a" stroke-width="6" stroke-linecap="round"/>`; }
    g += `<defs><clipPath id="${id}-c1"><rect id="${id}-w1" x="-330" y="-400" width="0" height="400"/></clipPath><clipPath id="${id}-c2"><rect id="${id}-w2" x="-330" y="180" width="0" height="400"/></clipPath></defs>`;
    g += `<g clip-path="url(#${id}-c1)">${th}</g><g clip-path="url(#${id}-c2)">${ro}</g>`;
    g += `<text x="0" y="40" text-anchor="middle" font-family="Kanit" font-size="40" fill="#9ab8ff" opacity=".9">ดังแล้วเงียบ</text></g>`;
    return g; };
  Ngw.phoneWaveLife = (tl, id, t0, dur, w = 660) => { tl.fromTo(`#${id}-w1`, { attr: { width: 0 } }, { attr: { width: w }, duration: Math.min(1.2, dur * 0.4), ease: "none", immediateRender: false }, t0 + 0.2);
    tl.fromTo(`#${id}-w2`, { attr: { width: 0 } }, { attr: { width: w }, duration: dur * 0.8, ease: "none", immediateRender: false }, t0 + 0.6); };
  Sets.ngwPhone = (L, o = {}) => put(L.set, o.wide ? Ngw.phoneWaveL(o.id || "pw") : Ngw.phoneWave(o.id || "pw"));
  Sets.ngwClock = (L, o = {}) => { put(L.sky, `<rect x="-1400" y="-800" width="4000" height="3600" fill="${o.bg || "#8a6a44"}"/>${Array.from({ length: 40 }, (_, k) => `<path d="M${-1400 + k * 100},-800V2800" stroke="#6a4a2e" stroke-width="8" opacity=".6"/>`).join("")}`);
    if (o.wall) put(L.set, Ngw.stallWall(o)); put(L.set, Ngw.clock(o.id || "ck", 540, 900, o.s ?? 1.2, o.h ?? 15, o.m ?? 0)); };
  // ---------------------------------------------------------------- the 16:9 film's own layouts (QA: no portrait cards left in the wide frame)
  // the stall's back wall round the clock (Sets.ngwClock o.wall): the string of bulbs, the April calendar, a marigold garland on a nail,
  // the shelf with the radio and the thermos, ยายบัว's chalk price board. o.lit: the bulbs glow (the dark afternoon)
  Ngw.stallWall = (o = {}) => { const I = "#1e1a16", lit = !!o.lit;
    let g = `<path d="M-700,330Q-90,470 540,400T1760,330" stroke="#2a2420" stroke-width="5" fill="none"/>`;
    for (let k = 0; k < 13; k++) { const x = -640 + k * 190, y = 360 + 46 * Math.sin((k / 12) * Math.PI * 2 + 0.6) * 0.6 + 40;
      g += `<path d="M${x},${f1(y - 34)}v22" stroke="#2a2420" stroke-width="5"/><circle cx="${x}" cy="${f1(y)}" r="17" fill="${lit ? "#fff2c0" : "#e8dcc0"}" ${OUT(4)}/>${lit ? `<circle cx="${x}" cy="${f1(y)}" r="90" fill="url(#ngwBulb)"/>` : ""}`; }
    // the calendar: April, the 13th ringed (สงกรานต์), the days crossed off up to today
    g += `<g transform="translate(-250,860) rotate(-2)"><path d="M0,-200v-24" stroke="${I}" stroke-width="6"/><circle cy="-226" r="9" fill="#8a8a84" ${OUT(3)}/><rect x="-150" y="-200" width="300" height="400" fill="#f4f0e4" ${OUT(6)}/><rect x="-150" y="-200" width="300" height="96" fill="#c8302a" ${OUT(6)}/>
      <text y="-138" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="54" fill="#fff6e0">เมษายน</text>`;
    for (let r = 0; r < 5; r++) for (let c = 0; c < 7; c++) { const n = r * 7 + c + 1; if (n > 30) continue; const x = -126 + c * 40, y = -64 + r * 54;
      g += `<text x="${x + 14}" y="${y + 20}" text-anchor="middle" font-family="Kanit" font-size="24" fill="${c === 0 ? "#c8302a" : "#3a3430"}">${n}</text>${n < 21 ? `<path d="M${x + 2},${y + 2}l24,24" stroke="#c8302a" stroke-width="3" opacity=".6"/>` : ""}${n === 13 ? `<circle cx="${x + 14}" cy="${y + 12}" r="20" fill="none" stroke="#c8302a" stroke-width="4"/>` : ""}`; }
    g += `</g>`;
    // a marigold garland on a nail beside the clock
    g += `<g transform="translate(905,600)"><circle r="8" fill="#8a8a84" ${OUT(3)}/>${Array.from({ length: 15 }, (_, k) => { const a = -0.15 + (k / 14) * Math.PI * 1.3, x = 70 * Math.sin(a) * 0.8, y = 30 + 130 * (1 - Math.cos(a)) * 0.6; return `<circle cx="${f1(x)}" cy="${f1(y)}" r="17" fill="${k % 4 === 3 ? "#e8e0f0" : "#f2a020"}" ${OUT(3)}/>`; }).join("")}
      <path d="M-4,190l-14,90M6,190l10,86" stroke="#e8c040" stroke-width="6"/><circle cx="0" cy="186" r="22" fill="#c8302a" ${OUT(3)}/></g>`;
    // the shelf under the clock: the transistor radio and the thermos
    g += `<rect x="190" y="1330" width="700" height="34" fill="#6a4a2e" ${OUT(6)}/><path d="M250,1364l40,80M830,1364l-40,80" stroke="${I}" stroke-width="10"/>
      <g transform="translate(400,1330)"><path d="M70,-150L150,-290" stroke="#8a8a84" stroke-width="7"/><rect x="-130" y="-160" width="260" height="160" rx="22" fill="#b0302a" ${OUT(6)}/><circle cx="-55" cy="-80" r="50" fill="#3a3430" ${OUT(4)}/>
        ${Array.from({ length: 5 }, (_, k) => `<path d="M-95,${-104 + k * 12}h80" stroke="#6a6460" stroke-width="4"/>`).join("")}<rect x="20" y="-130" width="84" height="36" rx="6" fill="#e8dcb0" ${OUT(3)}/><path d="M40,-130v36M60,-130v36M80,-130v36" stroke="#3a3430" stroke-width="2"/><circle cx="62" cy="-50" r="16" fill="#e8dcc0" ${OUT(3)}/></g>
      <g transform="translate(690,1330)"><rect x="-48" y="-230" width="96" height="230" rx="20" fill="#2a7a6a" ${OUT(6)}/><rect x="-36" y="-262" width="72" height="40" rx="10" fill="#e8e4d8" ${OUT(5)}/><path d="M48,-190q44,10 44,60t-44,60" stroke="${I}" stroke-width="12" fill="none"/><path d="M-48,-120h96" stroke="#e8e4d8" stroke-width="10"/></g>`;
    // ยายบัว's chalk price board
    g += `<g transform="translate(1340,900) rotate(2)"><path d="M-120,-260L0,-330L120,-260" stroke="${I}" stroke-width="5" fill="none"/><circle cy="-332" r="9" fill="#8a8a84" ${OUT(3)}/><rect x="-190" y="-260" width="380" height="480" rx="14" fill="#8a5a32" ${OUT(6)}/><rect x="-168" y="-238" width="336" height="436" fill="#24382c"/>
      <text y="-170" text-anchor="middle" font-family="Sriracha" font-size="50" fill="#f2c230">ไก่ย่างยายบัว</text><path d="M-140,-146h280" stroke="#e8e4d8" stroke-width="3" opacity=".6"/>
      ${[["ไก่ย่าง", "ตัวละ 150"], ["ส้มตำ", "40"], ["ข้าวเหนียว", "10"], ["น้ำแข็งใส", "15"]].map(([a, b], k) => `<text x="-146" y="${-80 + k * 74}" font-family="Sriracha" font-size="40" fill="#f2efe6">${a}</text><text x="146" y="${-80 + k * 74}" text-anchor="end" font-family="Sriracha" font-size="40" fill="#f2efe6">${b}</text>`).join("")}
      <path d="M-120,176q30,-16 60,0t60,0" stroke="#e86a6a" stroke-width="4" fill="none"/></g>`;
    return g; };
  // ฝน's recorder for the wide frame: the phone on its side filling the middle of the page, the two lanes stacked
  // (same ids as Ngw.phoneWave, so Ngw.phoneWaveLife runs it with o.w = the lane width)
  Ngw.phoneWaveL = (id) => { const I = "#1e1a16", W = 1210, X0 = -390;   // lanes in the phone's own coordinates (screen −900…900)
    let g = `<rect x="-1400" y="-800" width="4000" height="3600" fill="#1a1e24"/><rect x="-1400" y="-800" width="4000" height="3600" fill="url(#ngwBulb)" opacity=".08"/>`;
    g += `<g transform="translate(540,940)"><rect x="-960" y="-440" width="1920" height="880" rx="100" fill="#26262e" stroke="${I}" stroke-width="10"/><rect x="-900" y="-400" width="1800" height="800" rx="56" fill="#0e1218"/><circle cx="-930" cy="0" r="12" fill="#3a3a44"/>`;
    g += `<circle cx="-820" cy="-330" r="15" fill="#ff3a4a"/><text x="-790" y="-314" font-family="Kanit" font-weight="700" font-size="46" fill="#e8eef2">บันทึกเสียง</text><text x="840" y="-314" text-anchor="end" font-family="Kanit" font-size="38" fill="#9aa4ac">00:47</text>`;
    const lane = (y, label, sub, c) => `<text x="-840" y="${y + 6}" font-family="Kanit" font-weight="700" font-size="52" fill="${c}">${label}</text><text x="-840" y="${y + 56}" font-family="Kanit" font-size="34" fill="${c}" opacity=".85">${sub}</text><path d="M${X0},${y}H${X0 + W}" stroke="#3a4048" stroke-width="3"/>`;
    g += lane(-120, "ฟ้าร้อง", "ดังแล้วเงียบ", "#9ab8ff") + lane(210, "เสียงนี้", "ดังไม่หยุด", "#ffb84a");
    let th = "", ro = ""; for (let k = 0; k < 86; k++) { const x = X0 + 6 + k * 14;
      const a = k > 10 && k < 34 ? 118 * Math.exp(-(k - 11) * 0.2) * (0.6 + 0.4 * Math.sin(k * 2.1)) : 4; th += `<path d="M${x},${f1(-120 - a)}V${f1(-120 + a)}" stroke="#9ab8ff" stroke-width="7" stroke-linecap="round"/>`;
      const b = 76 + 30 * Math.sin(k * 0.9) + 16 * Math.sin(k * 2.3); ro += `<path d="M${x},${f1(210 - b)}V${f1(210 + b)}" stroke="#ffb84a" stroke-width="7" stroke-linecap="round"/>`; }
    g += `<defs><clipPath id="${id}-c1"><rect id="${id}-w1" x="${X0}" y="-260" width="0" height="280"/></clipPath><clipPath id="${id}-c2"><rect id="${id}-w2" x="${X0}" y="80" width="0" height="260"/></clipPath></defs>`;
    g += `<g clip-path="url(#${id}-c1)">${th}</g><g clip-path="url(#${id}-c2)">${ro}</g></g>`;
    return g; };
  // ฝน's live screen for the wide frame, drawn in page pixels (1920×1080) for a shot whose band starts at o.y0. It is one group as big as
  // the frame, so landscape.js leaves it full size (the portrait version shrank to a phone-wide column). The header runs across the top,
  // comments climb the left side above the captions, the hearts float up the right edge (#id-hN, Ngw.liveLifeL).
  // o.end: the "ไลฟ์จบแล้ว" card (#id-end, hidden) for ฝน ending her live; #id-on holds everything that goes when it ends.
  Ngw.liveUIL = (o = {}) => { const id = o.id || "lvl", y0 = Math.max(0, Math.min(570, o.y0 ?? 0)), name = o.name || "ฝนพาเที่ยว", cm = o.comments || [];   // landscape.js clamps the band top to 0…570
    // the invisible rect spans the whole vertical frame (2400 × 1920 after the transform), which is what makes landscape.js keep the group unscaled
    let g = `<rect x="0" y="${f1(-y0 / 1.25)}" width="1920" height="1536" fill="#000" opacity="0"/><g id="${id}-on"><rect x="0" y="0" width="1920" height="150" fill="#000" opacity=".3"/>`;
    g += `<g transform="translate(84,76)"><circle r="48" fill="#f2be2a" stroke="#ff3a6a" stroke-width="7"/><circle cy="-6" r="23" fill="#ebc19c"/><path d="M-27,-14Q-25,-46 2,-46Q27,-44 27,-14Q15,-31 -4,-29Q-19,-31 -27,-14Z" fill="#1e1410"/><path d="M-31,31Q0,10 31,31" stroke="#f2be2a" stroke-width="14"/></g>`;
    g += `<text x="152" y="68" font-family="Kanit" font-weight="700" font-size="42" fill="#fff">${name}</text><text x="152" y="112" font-family="Kanit" font-size="30" fill="#e8e8e8" opacity=".9">${o.title || "พายุมาแล้ววว"}</text>`;
    g += `<g transform="translate(1560,74)"><rect x="-74" y="-32" width="148" height="60" rx="12" fill="#ff2a4a"/><circle cx="-44" cy="-2" r="10" fill="#fff"/><text x="12" y="13" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="36" fill="#fff">LIVE</text></g>`;
    g += `<g transform="translate(1720,74)"><rect x="-66" y="-30" width="132" height="58" rx="12" fill="#000" opacity=".4"/><path d="M-46,-1q14,-16 28,0q-14,16 -28,0Z" fill="none" stroke="#fff" stroke-width="4"/><circle cx="-32" cy="-1" r="5" fill="#fff"/><text x="20" y="11" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#fff">${o.viewers || "2.4K"}</text></g>`;
    g += `<g transform="translate(1852,74)"><circle r="32" fill="#000" opacity=".4"/><path d="M-12,-12L12,12M12,-12L-12,12" stroke="#fff" stroke-width="5" stroke-linecap="round"/></g>`;
    cm.forEach(([nm, tx, c], k) => { const y = (o.cy ?? 860) - (cm.length - 1 - k) * 86;
      g += `<g id="${id}-c${k}" transform="translate(40,${y})"><rect x="0" y="-44" width="${Math.min(900, 128 + tx.length * 27 + nm.length * 23)}" height="78" rx="39" fill="#000" opacity=".42"/><circle cx="40" cy="-5" r="25" fill="${c || "#6a8ac8"}"/><text x="80" y="6" font-family="Kanit" font-weight="700" font-size="31" fill="#ffd25a">${nm}</text><text x="${90 + nm.length * 20}" y="6" font-family="Kanit" font-size="33" fill="#fff">${tx}</text></g>`; });
    g += `<g transform="translate(1840,880)"><circle r="46" fill="#ff3a6a"/><path d="M0,17C-25,-2 -29,-21 -15,-27C-6,-30 0,-23 0,-18C0,-23 6,-30 15,-27C29,-21 25,-2 0,17Z" fill="#fff"/></g>`;
    [[1836, 790, 1.2, "#ff4a6a"], [1806, 690, 1, "#ff9ab0"], [1856, 590, 0.9, "#ff4a6a"], [1820, 490, 0.7, "#ffd0d8"], [1848, 400, 0.55, "#ff4a6a"]].forEach(([x, y, s2, c], k) => {
      g += `<path id="${id}-h${k}" transform="translate(${x},${y}) scale(${s2 * 1.7})" d="M0,8C-14,-2 -18,-14 -9,-19C-4,-22 0,-17 0,-14C0,-17 4,-22 9,-19C18,-14 14,-2 0,8Z" fill="${c}" stroke="#fff" stroke-width="1.6"/>`; });
    g += `</g>`;
    if (o.end) g += `<g id="${id}-end" opacity="0"><rect x="0" y="0" width="1920" height="1080" fill="#000" opacity=".35"/><g transform="translate(960,420)"><rect x="-380" y="-170" width="760" height="320" rx="40" fill="#14181e" opacity=".92" stroke="#ff3a6a" stroke-width="5"/>
      <text y="-62" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="70" fill="#fff">ไลฟ์จบแล้ว</text><text y="6" text-anchor="middle" font-family="Kanit" font-size="36" fill="#e8e8e8">ขอบคุณที่ห่วงกันนะคะ</text>
      <g transform="translate(-120,84)"><path transform="scale(2.2)" d="M0,8C-14,-2 -18,-14 -9,-19C-4,-22 0,-17 0,-14C0,-17 4,-22 9,-19C18,-14 14,-2 0,8Z" fill="#ff3a6a"/><text x="40" y="14" font-family="Kanit" font-weight="700" font-size="40" fill="#fff">1.2 หมื่น</text></g></g></g>`;
    return `<g transform="translate(-660,${y0}) scale(1.25)">${g}</g>`; };
  // the hearts float up the right edge and fade, over and over (from t0 for dur)
  Ngw.liveLifeL = (tl, id, t0, dur) => { for (let k = 0; k < 5; k++) { const el = `#${id}-h${k}`; if (!document.querySelector(el)) return;
      tl.fromTo(el, { y: 0, opacity: 1 }, { y: -120, opacity: 0, duration: 1.4, ease: "power1.out", repeat: Math.max(0, Math.ceil(dur / 1.4) - 1), immediateRender: false }, t0 + k * 0.24); } };
  // the living room: plank walls, a family photo, the glass window with the storm outside (#id-win flashes), curtains blowing
  Sets.ngwRoom = (L, o = {}) => { const id = o.id || "rm", I = "#1e1a16", fy = 1560;
    put(L.sky, `<rect x="-1400" y="-800" width="4000" height="3600" fill="#3a2a1e"/>`);
    let w = `<rect x="-1400" y="-200" width="4000" height="${fy + 200}" fill="#8a6440"/>`; for (let x = -1400; x < 2600; x += 90) w += `<path d="M${x},-200V${fy}" stroke="#6a4a2e" stroke-width="6"/>`;
    // the window: the storm outside in it
    w += `<g><rect x="360" y="420" width="560" height="640" fill="#2a3640" stroke="${I}" stroke-width="14"/><clipPath id="${id}-wc"><rect x="360" y="420" width="560" height="640"/></clipPath>
      <g clip-path="url(#${id}-wc)"><rect x="360" y="420" width="560" height="640" fill="#36444e"/><path d="M360,820Q520,760 640,800T920,780V1060H360Z" fill="#2a3a2a"/><path d="M560,460L640,460L620,560L630,640L604,780L596,640L586,560Z" fill="#3a4248"/><ellipse cx="600" cy="790" rx="120" ry="40" fill="#7a6248" opacity=".8"/>
        ${Array.from({ length: 14 }, (_, k) => `<path d="M${380 + k * 40},${440 + (k * 53) % 600}l-30,26" stroke="#d8e0e4" stroke-width="3" opacity=".5"/>`).join("")}<rect id="${id}-win" x="360" y="420" width="560" height="640" fill="#eef4ff" opacity="0"/></g>
      <path d="M640,420V1060M360,740H920" stroke="${I}" stroke-width="12"/><rect x="340" y="1060" width="600" height="30" fill="#6a4a2e" stroke="${I}" stroke-width="6"/>
      <path d="M380,560l60,70M700,480l-40,90" stroke="#fff" stroke-width="3" opacity=".5"/></g>`;
    w += `<g id="${id}-cur"><path d="M330,400Q300,700 340,1080L380,1080Q340,700 380,400Z" fill="#c8483a" stroke="${I}" stroke-width="5"/><path d="M950,400Q990,700 940,1080L900,1080Q950,700 900,400Z" fill="#c8483a" stroke="${I}" stroke-width="5"/></g>`;
    w += `<g transform="translate(140,620)"><rect x="-90" y="-120" width="180" height="230" fill="#e8dcc0" stroke="${I}" stroke-width="8"/><rect x="-70" y="-100" width="140" height="190" fill="#9ab0c0"/><circle cx="-20" cy="-30" r="24" fill="#c8946a"/><circle cx="30" cy="-20" r="20" fill="#d49c6c"/></g>`;
    // ---- the family's things, ร้านยายพร-level detail (owner 4 Nov: "ดีเท่าทะเลลดรึยัง"): the photo wall, the Buddha shelf high up,
    // the clock, the calendar; on the floor the TV cabinet, the standing fan, the mat and a triangle cushion; a warm bulb overhead
    w += `<g transform="translate(-190,560)"><rect x="-100" y="-125" width="200" height="250" fill="#c8a050" ${OUT(6)}/><rect x="-84" y="-109" width="168" height="218" fill="#5a86b8"/>
      <path d="M-62,109Q-62,22 0,12Q62,22 62,109Z" fill="#1e1e28"/><path d="M-18,22L0,58L18,22" fill="#f4f0e8"/><circle cy="-18" r="34" fill="#d49c6c" ${OUT(2.6)}/>
      <path d="M-40,-44L0,-64L40,-44L0,-28Z" fill="#1e1e28"/><path d="M30,-44v28" stroke="#e8c040" stroke-width="3"/><path d="M-13,-16q4,3 8,0M5,-16q4,3 8,0M-6,-2q6,5 12,0" stroke="#2e2a26" stroke-width="2.4" fill="none"/>
      <path d="M-96,-122Q0,-80 96,-122" stroke="#f6f2e4" stroke-width="12" fill="none" stroke-dasharray="2 9" stroke-linecap="round"/><circle cx="0" cy="-98" r="11" fill="#d8312a" ${OUT(2)}/></g>`;
    w += `<g transform="translate(-450,650)"><rect x="-82" y="-104" width="164" height="208" fill="#5a3a22" ${OUT(6)}/><rect x="-66" y="-88" width="132" height="176" fill="#c8b08c"/>
      <circle cx="-26" cy="-22" r="22" fill="#8a7058"/><circle cx="28" cy="-26" r="22" fill="#8a7058"/><path d="M-60,88Q-56,20 -26,14Q0,16 2,40Q4,16 28,10Q58,16 60,88Z" fill="#6a5440"/><path d="M-40,-44q14,-12 28,0M14,-48q14,-12 28,0" stroke="#4a3a2a" stroke-width="6" fill="none"/></g>`;
    w += `<g transform="translate(1500,430)"><path d="M-150,0V-130Q0,-190 150,-130V0Z" fill="#8a2a1e" ${OUT(4)}/><path d="M-130,-6V-122Q0,-172 130,-122V-6" stroke="#e8b84a" stroke-width="5" fill="none"/>
      <circle cy="-72" r="70" fill="#ffe08a" opacity=".22"/><ellipse cy="-8" rx="50" ry="10" fill="#c8902a" ${OUT(2.6)}/><path d="M-42,-12Q-40,-62 0,-72Q40,-62 42,-12Z" fill="#e8b84a" ${OUT(2.6)}/>
      <circle cy="-90" r="20" fill="#e8b84a" ${OUT(2.6)}/><path d="M-7,-108q7,-16 14,0Z" fill="#e8b84a" ${OUT(2)}/>
      ${[-110, 110].map((x) => `<g transform="translate(${x},-6)"><path d="M-14,0L-18,-34H18L14,0Z" fill="#e8e0d0" ${OUT(2.4)}/>${[[-12, -52], [0, -60], [12, -52], [-6, -42], [8, -42]].map(([fx, fy2]) => `<circle cx="${fx}" cy="${fy2}" r="10" fill="#f08a1a" ${OUT(1.8)}/>`).join("")}</g>`).join("")}
      ${[-70, 70].map((x) => `<rect x="${x - 5}" y="-34" width="10" height="28" fill="#e8e0d0" ${OUT(1.8)}/><circle cx="${x}" cy="-40" r="7" fill="#ff5a3a"/><circle cx="${x}" cy="-40" r="16" fill="#ff7a4a" opacity=".3"/>`).join("")}
      <rect x="-170" y="0" width="340" height="26" fill="#a83a2a" ${OUT(4)}/><rect x="-170" y="0" width="340" height="7" fill="#e8b84a"/><path d="M-140,26L-110,26L-140,70ZM140,26L110,26L140,70Z" fill="#8a2a1e" ${OUT(3)}/>
      <path d="M-160,26Q-100,90 -40,26M40,26Q100,90 160,26" stroke="#f6f2e4" stroke-width="10" fill="none" stroke-dasharray="2 8" stroke-linecap="round"/></g>`;
    w += `<g transform="translate(1160,430)"><circle r="76" fill="#7a5232" ${OUT(6)}/><circle r="62" fill="#f6f2e8" ${OUT(3)}/>${Array.from({ length: 12 }, (_, k) => { const a = (k * Math.PI) / 6; return `<path d="M${f1(50 * Math.sin(a))},${f1(-50 * Math.cos(a))}L${f1(58 * Math.sin(a))},${f1(-58 * Math.cos(a))}" stroke="${I}" stroke-width="${k % 3 ? 3 : 6}"/>`; }).join("")}
      <path d="M0,0L24,9M0,0L-38,22" stroke="${I}" stroke-width="6" stroke-linecap="round"/><path d="M0,8L0,-50" stroke="#d8312a" stroke-width="2.4"/><circle r="6" fill="${I}"/></g>`;
    w += `<g transform="translate(1060,720)"><path d="M0,-80L-60,0M0,-80L60,0" stroke="#5a4630" stroke-width="3"/><circle cy="-80" r="6" fill="#8a8a8a" ${OUT(2)}/><rect x="-90" y="0" width="180" height="270" fill="#f6f2e8" ${OUT(5)}/>
      <rect x="-78" y="12" width="156" height="104" fill="#7ab0d8"/><path d="M-78,116V80Q-30,60 0,82Q40,58 78,76V116Z" fill="#4a9a4a"/><path d="M-20,82L0,46L20,82Z" fill="#e8b84a" ${OUT(2)}/><path d="M-12,82V64H12V82" fill="#f4f0e8"/>
      <rect x="-78" y="122" width="156" height="22" fill="#d8312a"/>${Array.from({ length: 5 }, (_, j) => Array.from({ length: 7 }, (_, i) => `<rect x="${-76 + i * 22}" y="${150 + j * 22}" width="18" height="16" fill="${i === 0 ? "#f4c8c0" : "#e8e4dc"}"/>`).join("")).join("")}
      <circle cx="${-76 + 4 * 22 + 9}" cy="${150 + 2 * 22 + 8}" r="13" fill="none" stroke="#d8312a" stroke-width="3"/></g>`;
    put(L.far, w);
    put(L.mid, `<rect x="-1400" y="${fy}" width="4000" height="1000" fill="#5a4030"/>${Array.from({ length: 10 }, (_, k) => `<path d="M-1400,${fy + 30 + k * 60}H2600" stroke="#4a3426" stroke-width="5"/>`).join("")}`);
    // the mat and the triangle cushion, the TV cabinet, the standing fan (its blades spin: #id-fan)
    let fl = `<path d="M-560,${fy + 40}H460L560,${fy + 170}H-660Z" fill="#c89a5a" ${OUT(4)}/>${Array.from({ length: 9 }, (_, k) => `<path d="M${-560 - k * 11},${fy + 54 + k * 14}H${460 + k * 11}" stroke="${["#b8382a", "#3a7a4a", "#e8b84a"][k % 3]}" stroke-width="6" opacity=".8"/>`).join("")}`;
    fl += `<g transform="translate(-440,${fy + 70})"><path d="M-110,0L-60,-120H70L110,0Z" fill="#c8302a" ${OUT(4)}/><path d="M-60,-120L-20,0M70,-120L30,0" stroke="#8a1e18" stroke-width="4"/>${[-70, -25, 20, 65].map((x) => `<path d="M${x},-60l12,-14l12,14l-12,14Z" fill="#e8b84a" ${OUT(1.6)}/>`).join("")}</g>`;
    fl += `<g transform="translate(1350,${fy + 20})"><rect x="-210" y="-300" width="420" height="300" fill="#6a4426" ${OUT(6)}/><path d="M0,-286V-14M-196,-150H196" stroke="#4a2e18" stroke-width="5"/>
      <circle cx="-22" cy="-80" r="8" fill="#e8b84a" ${OUT(2)}/><circle cx="22" cy="-80" r="8" fill="#e8b84a" ${OUT(2)}/><path d="M-200,-300Q0,-282 200,-300L190,-280Q0,-262 -190,-280Z" fill="#f4f0e8" ${OUT(2.4)}/>
      <rect x="-140" y="-520" width="280" height="220" rx="16" fill="#3a3a40" ${OUT(6)}/><rect x="-118" y="-498" width="200" height="164" rx="20" fill="#1c232a"/><path d="M-96,-480q40,-6 70,10" stroke="#8aa0b0" stroke-width="6" fill="none" opacity=".5"/>
      <circle cx="108" cy="-470" r="9" fill="#8a8a8a"/><circle cx="108" cy="-440" r="9" fill="#8a8a8a"/><path d="M-20,-520L-90,-640M20,-520L80,-650" stroke="#8a8a8a" stroke-width="5"/><circle cx="-90" cy="-640" r="6" fill="#8a8a8a"/><circle cx="80" cy="-650" r="6" fill="#8a8a8a"/></g>`;
    fl += `<g transform="translate(-280,${fy + 60})"><ellipse rx="90" ry="20" fill="#e8e4dc" ${OUT(4)}/><rect x="-8" y="-330" width="16" height="320" fill="#e8e4dc" ${OUT(3)}/>
      <g transform="translate(0,-420)"><circle r="118" fill="#d8e8f0" opacity=".25" ${OUT(4)}/><g id="${id}-fan">${[0, 120, 240].map((a) => `<path d="M0,0Q30,-50 10,-100Q-30,-90 -14,-20Z" fill="#8ac0e0" opacity=".85" ${OUT(2.4)} transform="rotate(${a})"/>`).join("")}</g>
      <circle r="18" fill="#e8e4dc" ${OUT(3)}/>${[40, 78, 112].map((rr) => `<circle r="${rr}" fill="none" stroke="#c8ccd0" stroke-width="3"/>`).join("")}${Array.from({ length: 12 }, (_, k) => `<path d="M0,0L${f1(116 * Math.cos(k * Math.PI / 6))},${f1(116 * Math.sin(k * Math.PI / 6))}" stroke="#c8ccd0" stroke-width="2.4"/>`).join("")}</g></g>`;
    put(L.mid, fl);
    // the bulb on its cord over the room (#id-bulb swings, #id-glow flickers with the storm)
    put(L.set, `<g id="${id}-bulb"><path d="M640,-400V150" stroke="${I}" stroke-width="5"/><rect x="626" y="144" width="28" height="26" rx="3" fill="#3a3a3a"/><ellipse cx="640" cy="196" rx="26" ry="32" fill="#fff4c8" ${OUT(3)}/></g>`);
    put(L.glow, `<g id="${id}-glow"><circle cx="640" cy="196" r="900" fill="url(#ngwBulb)" opacity=".6"/><circle cx="640" cy="196" r="130" fill="url(#ngwBulb)"/></g>`);
  };
  Ngw.roomLife = (tl, id, t0, dur, flashes = []) => { tl.fromTo(`#${id}-cur`, { skewX: -2, svgOrigin: "640 400" }, { skewX: 3, svgOrigin: "640 400", duration: 0.35, yoyo: true, repeat: Math.ceil(dur / 0.35), ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-fan`, { rotation: 0 }, { rotation: 360, svgOrigin: "0 0", duration: 0.7, ease: "none", repeat: Math.ceil(dur / 0.7), immediateRender: false }, t0);
    tl.fromTo(`#${id}-bulb`, { rotation: -3, svgOrigin: "640 -400" }, { rotation: 3, svgOrigin: "640 -400", duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: Math.ceil(dur / 1.1), immediateRender: false }, t0);
    tl.fromTo(`#${id}-glow`, { opacity: 1 }, { keyframes: [{ opacity: 0.7, duration: 0.08 }, { opacity: 1, duration: 0.14 }, { opacity: 0.9, duration: 0.7 }], repeat: Math.ceil(dur / 0.92), immediateRender: false }, t0);
    flashes.forEach((t) => tl.fromTo(`#${id}-win`, { opacity: 0 }, { keyframes: [{ opacity: 0.8, duration: 0.05 }, { opacity: 0.1, duration: 0.08 }, { opacity: 0.6, duration: 0.05 }, { opacity: 0, duration: 0.3 }], immediateRender: false }, t0 + t)); };
  // the choice on two zinc boards (same world as the rule sign): question plate, A / B with road-sign discs; at o.at the wind
  // "pulls" the frame onto the scary option o.pull, which shakes and glows red
  Ngw.choice = (tl, layer, t0, dur, o = {}) => { const id = `ch${Math.round(t0 * 100)}`, I = "#1e1a16", Y = [o.yA ?? 860, o.yB ?? 1160];
    const plate = (y, w, h) => `<path d="M${540 - w / 2},${y}L${540 + w / 2},${y + 4}L${540 + w / 2 - 6},${y + h}L${540 - w / 2 + 4},${y + h - 4}Z" fill="#b4bab8" stroke="${I}" stroke-width="7"/>${Array.from({ length: Math.floor(w / 44) }, (_, k) => `<rect x="${540 - w / 2 + 6 + k * 44}" y="${y + 6}" width="16" height="${h - 12}" fill="#e8ecea" opacity=".3"/>`).join("")}`;
    let g = `<g id="${id}"><rect x="-1400" y="-800" width="4000" height="3600" fill="#000" opacity=".35"/>`;
    g += `<g id="${id}-q">${plate(540, 760, 150)}<rect x="160" y="540" width="760" height="22" fill="#f2c230"/><text x="540" y="652" text-anchor="middle" font-family="Sriracha" font-size="84" fill="#d8312a" stroke="#fff8ec" stroke-width="10" paint-order="stroke">${o.q || "จะหลบที่ไหน?"}</text></g>`;
    [o.a, o.b].forEach((c, k) => { g += `<g id="${id}-c${k}"><g id="${id}-cc${k}">${plate(Y[k] - 110, 900, 220)}<g transform="translate(200,${Y[k]})"><circle r="80" fill="#fff" stroke="#d8312a" stroke-width="14"/><g transform="translate(-58,-62) scale(.97)">${c.pic || ""}</g></g>
      <text x="310" y="${Y[k] + 22}" font-family="Sriracha" font-size="70" fill="${I}">${c.text}</text><rect id="${id}-gl${k}" x="90" y="${Y[k] - 110}" width="900" height="220" fill="none" stroke="#ff3a3a" stroke-width="14" opacity="0" filter="url(#skBlur4)"/></g></g>`; });
    put(layer, g + `</g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    [0, 1].forEach((k) => tl.fromTo(`#${id}-c${k}`, { x: k ? 700 : -700 }, { x: 0, duration: 0.4, ease: "back.out(1.4)", immediateRender: false }, t0 + 0.15 + k * 0.12));
    const pk = o.pull === "b" ? 1 : 0, at = t0 + (o.at ?? dur - 1.4);
    tl.fromTo(`#${id}-gl${pk}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, at);
    tl.fromTo(`#${id}-cc${pk}`, { x: -6 }, { x: 6, duration: 0.05, yoyo: true, repeat: 15, ease: "none", immediateRender: false }, at);
    tl.to(`#${id}-c${1 - pk}`, { opacity: 0.35, duration: 0.3, immediateRender: false }, at); };
  // ยายบัว's saying as an old ink-on-paper picture (QA: ทะเลลด gave its legend an illustrated card): the paddies, palms and stilt houses,
  // a brush-drawn funnel, a ghost train of cloud running along the cloud base (the sound in the saying), "ครืนนน…" in brush letters,
  // and three villagers dropping everything and running. Ids for Ngw.sayingLife (named apart from the naga story's Sets.ngwLegend): #id-fun, #id-train, .id-run, #id-dust
  Sets.ngwSaying = (L, o = {}) => { const id = o.id || "lg", INKB = "#3a2614", r = mk(o.seed || 41), hz = 1180;
    let bg = `<rect x="-1400" y="-800" width="4000" height="3600" fill="#e6d4a8"/><rect x="-1400" y="-800" width="4000" height="3600" fill="url(#ngwSun)" opacity=".12"/>`;
    for (let k = 0; k < 70; k++) { const y = -200 + r() * 2400; bg += `<path d="M${f1(-900 + r() * 3000)},${f1(y)}l${f1(80 + r() * 260)},${f1((r() - 0.5) * 8)}" stroke="#b89c68" stroke-width="${f1(1 + r() * 2)}" opacity=".35"/>`; }
    bg += `<rect x="-560" y="330" width="2200" height="1260" fill="none" stroke="${INKB}" stroke-width="10"/><rect x="-530" y="360" width="2140" height="1200" fill="none" stroke="${INKB}" stroke-width="3"/>`;
    put(L.sky, bg);
    // sky wash and the storm: ink clouds darkening toward the funnel
    let sk = ""; for (let k = 0; k < 16; k++) { const cx = 300 + r() * 1300, cy = 520 + r() * 180, rx = 140 + r() * 220; sk += `<ellipse cx="${f1(cx)}" cy="${f1(cy)}" rx="${f1(rx)}" ry="${f1(rx * 0.38)}" fill="${INKB}" opacity="${f1(0.08 + (cx > 900 ? 0.12 : 0.03))}"/>`; }
    sk += `<path d="M700,640Q1000,560 1400,600T1660,620" stroke="${INKB}" stroke-width="7" fill="none" opacity=".55"/>`;
    // the ghost train in the cloud base: a steam engine and three cars drawn in pale strokes, smoke trailing
    const car = (x0) => `<rect x="${x0}" y="-56" width="150" height="70" rx="8" fill="none" stroke="#f6ecd2" stroke-width="5"/>${[0, 1, 2].map((k) => `<rect x="${x0 + 18 + k * 44}" y="-44" width="30" height="24" fill="none" stroke="#f6ecd2" stroke-width="3"/>`).join("")}<circle cx="${x0 + 30}" cy="22" r="14" fill="none" stroke="#f6ecd2" stroke-width="4"/><circle cx="${x0 + 120}" cy="22" r="14" fill="none" stroke="#f6ecd2" stroke-width="4"/>`;
    sk += `<g transform="translate(420,610)"><g id="${id}-train" opacity=".75"><path d="M200,-40h120v-50h50v50h40v54h-210Z" fill="none" stroke="#f6ecd2" stroke-width="5"/><path d="M330,-90v-40h26v40" stroke="#f6ecd2" stroke-width="5" fill="none"/>
      ${[0, 1, 2].map((k) => `<circle cx="${f1(300 - k * 70)}" cy="${f1(-150 - k * 26)}" r="${26 + k * 10}" fill="none" stroke="#f6ecd2" stroke-width="4" opacity="${f1(0.8 - k * 0.2)}"/>`).join("")}<circle cx="240" cy="22" r="20" fill="none" stroke="#f6ecd2" stroke-width="5"/><circle cx="350" cy="22" r="20" fill="none" stroke="#f6ecd2" stroke-width="5"/>${car(30)}${car(-140)}${car(-310)}</g></g>`;
    sk += `<text x="560" y="520" font-family="Sriracha" font-size="96" fill="${INKB}" opacity=".85" transform="rotate(-6 560 520)">ครืนนน…</text>`;
    put(L.far, sk);
    // the funnel: brush strokes from the cloud base to the ground, a dust skirt at its foot
    let fu = `<g id="${id}-fun">`; for (let k = 0; k < 9; k++) { const t = k / 8, w0 = 150 - t * 40, x1 = 1240 + (r() - 0.5) * 30;
      fu += `<path d="M${f1(x1 - w0 + k * 18)},620Q${f1(x1 - 40 + k * 6)},${f1(900)} ${f1(1180 + k * 5)},${hz}" stroke="${INKB}" stroke-width="${f1(8 + r() * 10)}" fill="none" stroke-linecap="round" opacity="${f1(0.35 + r() * 0.4)}"/>`; }
    fu += `</g><g id="${id}-dust">${Array.from({ length: 9 }, (_, k) => `<ellipse cx="${f1(1190 + (k - 4) * 46)}" cy="${f1(hz - 10 - (k % 3) * 18)}" rx="${f1(60 + (k % 4) * 14)}" ry="26" fill="${INKB}" opacity=".18"/>`).join("")}</g>`;
    // the land: horizon, paddy strokes, sugar palms, stilt houses
    let ld = `<path d="M-560,${hz}H1640" stroke="${INKB}" stroke-width="6"/>`;
    for (let k = 0; k < 140; k++) { const y = hz + 20 + r() * 300, x = -540 + r() * 2160; ld += `<path d="M${f1(x)},${f1(y)}q6,-${f1(10 + r() * 14)} 14,-${f1(18 + r() * 14)}" stroke="#6a5a2a" stroke-width="3" fill="none" opacity=".55"/>`; }
    [[-300, 1.0], [-200, 0.8], [1500, 0.9]].forEach(([x, k]) => { ld += `<path d="M${x},${hz}Q${x + 6},${hz - 160 * k} ${x - 4},${hz - 300 * k}" stroke="${INKB}" stroke-width="${f1(8 * k)}" fill="none"/>${[-2, -1, 0, 1, 2].map((j) => `<path d="M${x - 4},${f1(hz - 300 * k)}q${j * 36},${f1(-30 - Math.abs(j) * 6)} ${j * 70},${f1(10 - Math.abs(j) * 4)}" stroke="${INKB}" stroke-width="5" fill="none"/>`).join("")}`; });
    [[60, 0.9], [300, 0.7]].forEach(([x, k]) => { ld += `<g transform="translate(${x},${hz}) scale(${k})"><path d="M-90,0V-60M90,0V-60M-110,-60H110V-150H-110Z" stroke="${INKB}" stroke-width="6" fill="#d8c494"/><path d="M-140,-150L0,-240L140,-150Z" stroke="${INKB}" stroke-width="6" fill="#c8b07c"/><rect x="-30" y="-130" width="40" height="50" fill="none" stroke="${INKB}" stroke-width="4"/></g>`; });
    // three villagers dropping everything and running away (to the left), staggered; a basket spilling rice where one dropped it
    // (the moving group sits inside the placed one: GSAP's x/y on an SVG element replace its translate)
    const man = (x, y, k, carry) => `<g transform="translate(${x},${y}) scale(${k})"><g class="${id}-run"><circle cx="0" cy="-150" r="22" fill="${INKB}"/><path d="M0,-128L-10,-60M-10,-60L-40,0M-10,-60L24,-8M-4,-110L-52,-150M-4,-110L40,-140" stroke="${INKB}" stroke-width="12" fill="none" stroke-linecap="round"/>${carry ? `<circle cx="-30" cy="-118" r="18" fill="${INKB}"/>` : ""}<path d="M-8,-176q12,-16 26,-6" stroke="${INKB}" stroke-width="5" fill="none"/></g></g>`;
    ld += `<g transform="translate(860,1330)"><path d="M-40,0q40,-60 80,0Z" fill="#c8a868" stroke="${INKB}" stroke-width="5"/>${Array.from({ length: 14 }, (_, k) => `<circle cx="${f1(40 + k * 9 + (k % 3) * 4)}" cy="${f1(-4 + (k % 4) * 4)}" r="4" fill="#f6ecd2" stroke="${INKB}" stroke-width="1"/>`).join("")}</g>`;
    ld += man(560, 1350, 1.15, false) + man(250, 1316, 1.0, true) + man(-40, 1290, 0.9, false);   // above the caption line
    put(L.mid, fu); put(L.set, ld);
  };
  Ngw.sayingLife = (tl, id, t0, dur) => {
    tl.fromTo(`#${id}-train`, { x: -120 }, { x: 260, duration: dur, ease: "none", immediateRender: false }, t0);
    tl.fromTo(`#${id}-fun`, { skewX: -3, svgOrigin: "1200 1180" }, { skewX: 4, svgOrigin: "1200 1180", duration: 0.7, yoyo: true, repeat: Math.ceil(dur / 0.7), ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-dust`, { scaleX: 0.9, svgOrigin: "1190 1170" }, { scaleX: 1.15, svgOrigin: "1190 1170", duration: 0.5, yoyo: true, repeat: Math.ceil(dur / 0.5), ease: "sine.inOut", immediateRender: false }, t0);
    document.querySelectorAll(`.${id}-run`).forEach((e, k) => { tl.fromTo(e, { x: 0 }, { x: -260 - k * 40, duration: dur, ease: "none", immediateRender: false }, t0);
      tl.fromTo(e, { y: 0 }, { y: -14, duration: 0.18, yoyo: true, repeat: Math.ceil(dur / 0.18), ease: "sine.inOut", immediateRender: false }, t0 + k * 0.06); }); };
  // the choice for the wide frame (QA: the last phone-style stack): question plate on top, the two answers side by side, drawn in page pixels
  // for a band starting at o.y0 (kept full size by the frame-tall invisible rect, like Ngw.liveUIL); the pull and the dimming as Ngw.choice
  Ngw.choiceL = (tl, layer, t0, dur, o = {}) => { const id = `cl${Math.round(t0 * 100)}`, I = "#1e1a16", y0 = Math.max(0, Math.min(570, o.y0 ?? 0));
    const plate = (x, y, w, h) => `<path d="M${x - w / 2},${y}L${x + w / 2},${y + 4}L${x + w / 2 - 6},${y + h}L${x - w / 2 + 4},${y + h - 4}Z" fill="#b4bab8" stroke="${I}" stroke-width="6"/>${Array.from({ length: Math.floor(w / 40) }, (_, k) => `<rect x="${x - w / 2 + 6 + k * 40}" y="${y + 6}" width="14" height="${h - 12}" fill="#e8ecea" opacity=".3"/>`).join("")}`;
    let g = `<rect x="0" y="${f1(-y0 / 1.25)}" width="1920" height="1536" fill="#000" opacity="0"/><rect x="0" y="0" width="1920" height="1080" fill="#000" opacity=".35"/>`;
    g += `<g id="${id}-q">${plate(960, 120, 760, 130)}<rect x="580" y="120" width="760" height="20" fill="#f2c230"/><text x="960" y="218" text-anchor="middle" font-family="Sriracha" font-size="76" fill="#d8312a" stroke="#fff8ec" stroke-width="9" paint-order="stroke">${o.q || "จะหลบที่ไหน?"}</text></g>`;
    const X = [520, 1400];
    [o.a, o.b].forEach((c, k) => { g += `<g id="${id}-c${k}"><g id="${id}-cc${k}">${plate(X[k], 330, 780, 300)}<g transform="translate(${X[k]},440)"><circle r="78" fill="#fff" stroke="#d8312a" stroke-width="13"/><g transform="translate(-57,-60) scale(.95)">${c.pic || ""}</g></g>
      <text x="${X[k]}" y="590" text-anchor="middle" font-family="Sriracha" font-size="64" fill="${I}">${c.text}</text><rect id="${id}-gl${k}" x="${X[k] - 390}" y="330" width="780" height="300" fill="none" stroke="#ff3a3a" stroke-width="13" opacity="0" filter="url(#skBlur4)"/></g></g>`; });
    put(layer, `<g id="${id}" transform="translate(-660,${y0}) scale(1.25)">${g}</g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    [0, 1].forEach((k) => tl.fromTo(`#${id}-c${k}`, { y: 500 }, { y: 0, duration: 0.4, ease: "back.out(1.4)", immediateRender: false }, t0 + 0.15 + k * 0.12));
    const pk = o.pull === "b" ? 1 : 0, at = t0 + (o.at ?? dur - 1.4);
    tl.fromTo(`#${id}-gl${pk}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, at);
    tl.fromTo(`#${id}-cc${pk}`, { x: -6 }, { x: 6, duration: 0.05, yoyo: true, repeat: 15, ease: "none", immediateRender: false }, at);
    tl.to(`#${id}-c${1 - pk}`, { opacity: 0.35, duration: 0.3, immediateRender: false }, at); };
  // QA (third review): the "scream" D-mouth with its top teeth read as laughing, the "worry" brows (inner ends down) as anger. Added to
  // every actor after the build (call Ngw.addFaces(root) from Engine.build): mouth "shout" — wide open, corners pulled down, the lower
  // teeth; mouth "fear" — a tall oval; eyes "fear" — the wide eyes with the inner ends of the brows lifted
  Ngw.addFaces = (root) => { const LN = "#1e1a16", inner = "#5a1e1e", tongue = "#d86a6a", EY = -548;
    const SHOUT = `<path d="M-11,-519Q4,-529 19,-519L17,-499Q4,-492 -9,-499Z" fill="${inner}" stroke="${LN}" stroke-width="2.6" stroke-linejoin="round"/><path d="M-7,-501Q4,-496 15,-501L14,-505Q4,-501 -6,-505Z" fill="#f4eee2"/><path d="M-3,-509q7,-5 14,0q-7,4 -14,0z" fill="${tongue}"/>`;
    const FEAR = `<path d="M-3,-523Q4,-528 11,-523Q14,-507 4,-502Q-6,-507 -3,-523Z" fill="${inner}" stroke="${LN}" stroke-width="2.4"/><path d="M0,-507q4,-3 8,0q-4,3 -8,0z" fill="${tongue}"/>`;
    root.querySelectorAll('g[id$="-mouth"]').forEach((m) => { if (!m.querySelector(".mouth-smile") || m.querySelector(".mouth-shout")) return;
      m.insertAdjacentHTML("beforeend", `<g class="mouth-shout" display="none">${SHOUT}</g><g class="mouth-fear" display="none">${FEAR}</g>`); });
    const B = [`M-28,${EY - 21}Q-17,${EY - 29} -6,${EY - 32}`, `M8,${EY - 32}Q19,${EY - 29} 30,${EY - 21}`];
    root.querySelectorAll('g[id$="-eyes"]').forEach((e) => { const w = e.querySelector(":scope > .eye-wide"); if (!w || e.querySelector(":scope > .eye-fear")) return;
      const f = w.cloneNode(true); f.setAttribute("class", "eye-fear"); f.setAttribute("display", "none");
      [...f.querySelectorAll("path")].filter((q) => q.getAttribute("stroke-width") === "4.6").forEach((q, i) => q.setAttribute("d", B[i] || B[1]));
      e.appendChild(f); }); };
  // a hand holding a phone up in the foreground (over ฝน's shoulder): the screen shows o.screen = "funnel" (the live picture of the storm,
  // LIVE badge, timer, hearts) or "comments" (the live's comment list, o.comments). Drawn for L.glow, sharp in front of everything
  Ngw.phoneOTS = (o = {}) => { const I = "#1e1a16", x = o.x ?? 200, y = o.y ?? 1900, s = o.s ?? 1, rot = o.rot ?? -6, id = o.id || "ots";
    let scr = `<rect x="-130" y="-520" width="260" height="470" rx="18" fill="#0e1218"/><clipPath id="${id}-sc"><rect x="-130" y="-520" width="260" height="470" rx="18"/></clipPath><g clip-path="url(#${id}-sc)">`;
    if ((o.screen || "funnel") === "funnel") {
      scr += `<rect x="-130" y="-520" width="260" height="470" fill="#3a4a52"/><rect x="-130" y="-300" width="260" height="120" fill="#c8a868" opacity=".35"/><rect x="-130" y="-180" width="260" height="130" fill="#3e5a32"/>
        <path d="M-130,-330Q0,-380 130,-340V-520H-130Z" fill="#1e262c"/><path id="${id}-fn" d="M-40,-345Q20,-350 40,-340Q10,-300 18,-250Q8,-215 4,-180H-6Q-10,-220 -18,-252Q-26,-300 -40,-345Z" fill="#4a3e34"/>
        <ellipse cx="0" cy="-182" rx="46" ry="12" fill="#8a7458" opacity=".7"/><path d="M-130,-180H130" stroke="#d8c8a0" stroke-width="2" opacity=".6"/>`;
    } else {
      scr += `<rect x="-130" y="-520" width="260" height="470" fill="#2a3640"/>` + (o.comments || []).map(([nm, tx, c], k) => `<g transform="translate(-118,${-330 + k * 62})"><rect width="236" height="50" rx="25" fill="#000" opacity=".45"/><circle cx="24" cy="25" r="15" fill="${c}"/><text x="46" y="21" font-family="Kanit" font-weight="700" font-size="15" fill="#ffd25a">${nm}</text><text x="46" y="40" font-family="Kanit" font-size="15" fill="#fff">${tx}</text></g>`).join("");
    }
    scr += `<rect x="-130" y="-520" width="260" height="56" fill="#000" opacity=".35"/><circle cx="-104" cy="-492" r="15" fill="#f2be2a" stroke="#ff3a6a" stroke-width="4"/><rect x="40" y="-506" width="56" height="26" rx="6" fill="#ff2a4a"/><text x="68" y="-487" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="17" fill="#fff">LIVE</text>
      <text x="-82" y="-486" font-family="Kanit" font-weight="700" font-size="17" fill="#fff">ฝนพาเที่ยว</text><path d="M96,-110c-10,-8 -12,-16 -6,-19c3,-2 6,0 6,2c0,-2 3,-4 6,-2c6,3 4,11 -6,19z" fill="#ff4a6a" transform="scale(1.6) translate(-36,40)"/></g>`;
    scr += `<path d="M-130,-520L-40,-520L-130,-300Z" fill="#fff" opacity=".07"/>`;
    const arm = `<path d="M-60,40L-40,-80L60,-90L90,60Z" fill="#e8b830" stroke="${I}" stroke-width="6"/><path d="M-44,-70L56,-80" stroke="#c4931c" stroke-width="10"/>`;
    const hand = `<path d="M-150,-170Q-170,-120 -150,-60Q-110,-30 -40,-60L60,-90Q90,-120 70,-160L-60,-150Z" fill="#ebbd95" stroke="${I}" stroke-width="5"/>${[0, 1, 2, 3].map((k) => `<path d="M${-146 + k * 6},${-170 + k * 30}q-40,0 -32,22q8,10 36,4" fill="#ebbd95" stroke="${I}" stroke-width="4"/>`).join("")}<path d="M150,-200q30,10 22,48q-10,26 -40,16" fill="#ebbd95" stroke="${I}" stroke-width="4"/>`;
    return `<g transform="translate(${x},${y}) rotate(${rot}) scale(${s})">${arm}<rect x="-150" y="-545" width="300" height="520" rx="34" fill="#1a1a1e" stroke="${I}" stroke-width="7"/>${scr}${hand}</g>`; };
  // ยายบัว's grill stall after the storm (the payoff of "ไก่ย่างทั้งร้าน… ทิ้งไว้ตรงนั้น"): the cart tipped on its side, the umbrella torn
  // inside out, skewers and the price board in the mud, a stool upside down
  Ngw.stallWreck = (x, y, s = 1) => { const I = "#1e1a16";
    let g = `<g transform="rotate(-24 ${x} ${y})">${Rup2.stall(x, y, s)}</g>`;
    g += `<g transform="translate(${x + 320 * s},${y - 10 * s}) rotate(28) scale(${s})"><path d="M0,0L-30,-220" stroke="#8a8a84" stroke-width="10"/><path d="M-30,-220L-200,-150L-150,-260L-40,-300L60,-250L120,-170Z" fill="#e8eef2" stroke="${I}" stroke-width="5"/><path d="M-30,-220L-150,-260M-30,-220L60,-250" stroke="#3a6ac8" stroke-width="12"/><path d="M-120,-200l40,-30" stroke="${I}" stroke-width="4"/></g>`;
    for (let k = 0; k < 9; k++) g += `<path d="M${x - 260 * s + k * 52 * s},${y + (k % 3) * 8 * s}l${(30 + k * 7) * s},${-(6 + k % 4 * 4) * s}" stroke="#8a6a44" stroke-width="${5 * s}" stroke-linecap="round"/>`;
    g += `<g transform="translate(${x - 420 * s},${y + 10 * s}) rotate(-78) scale(${0.55 * s})"><rect x="-190" y="-260" width="380" height="480" rx="14" fill="#8a5a32" stroke="${I}" stroke-width="8"/><rect x="-168" y="-238" width="336" height="436" fill="#24382c"/><text y="-170" text-anchor="middle" font-family="Sriracha" font-size="50" fill="#f2c230">ไก่ย่างยายบัว</text></g>`;
    g += `<g transform="translate(${x + 520 * s},${y}) rotate(180) scale(${s})"><rect x="-60" y="0" width="120" height="20" fill="#3a6ac8" stroke="${I}" stroke-width="4"/><path d="M-50,20V90M50,20V90" stroke="#3a6ac8" stroke-width="10"/></g>`;
    return `<g>${g}</g>`; };
  // the end card: a green highway sign on its pole in the storm: o.l1 "ตอนที่ 2", o.l2 "ใต้สะพาน"
  Sets.ngwEndSign = (L, o = {}) => { if (o.cta) return Sets.ngwEndCta(L, o); put(L.sky, `<rect x="-1400" y="-800" width="4000" height="3600" fill="#141a20"/><rect x="-1400" y="700" width="4000" height="700" fill="#3a4a50" opacity=".5" filter="url(#skBlur24)"/>
      <path d="M760,420H1000L930,560L950,700L900,860L880,1000L860,860L840,700L800,560Z" fill="#20282e" opacity=".9" filter="url(#skBlur4)"/><ellipse cx="880" cy="1010" rx="160" ry="40" fill="#3a3028" opacity=".8" filter="url(#skBlur10)"/>
      <rect x="-1400" y="1000" width="4000" height="1600" fill="#1a221c"/>${Array.from({ length: 60 }, (_, k) => `<path d="M${(k * 97) % 1400 - 160},${(k * 211) % 1900}l-24,90" stroke="#9aa8b0" stroke-width="3" opacity=".35"/>`).join("")}`);
    put(L.set, `<g transform="translate(540,1040)"><path d="M-14,0V880M14,0V880" stroke="#8a8a84" stroke-width="22"/><g id="${o.id || "es"}"><rect x="-430" y="-330" width="860" height="420" rx="26" fill="#1e7a4a" stroke="#f2f0ea" stroke-width="12"/>
      <text y="-150" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="110" fill="#f2f0ea">${o.l1 || "ตอนที่ 2"}</text><text y="10" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="96" fill="#f2c230">${o.l2 || "ใต้สะพาน"}</text></g></g>`); };
  // the short's last card (owner 4 Nov 2569: the short carries EP.1 only, then "กดติดตาม แล้วดูเรื่องเต็มได้ที่ช่อง YouTube"):
  // a highway guide sign in the storm with the tornado behind it; "YouTube" as plain lettering, never its logo (another app's mark cuts reach on IG)
  Sets.ngwEndCta = (L, o = {}) => {
    const id = o.id || "es", r = mk(o.seed || 31);
    let wall = "";
    for (let k = 0; k < 9; k++) wall += `<ellipse cx="${f1(-200 + k * 190 + r() * 80)}" cy="${f1(250 + r() * 120)}" rx="${f1(260 + r() * 160)}" ry="${f1(90 + r() * 60)}" fill="${k % 2 ? "#1b2329" : "#222b32"}" opacity=".95" filter="url(#skBlur24)"/>`;
    put(L.sky, `<rect x="-1400" y="-800" width="4000" height="3600" fill="#141a20"/><rect x="-1400" y="880" width="4000" height="560" fill="#3a4a50" opacity=".45" filter="url(#skBlur24)"/>${wall}
      <g id="${id}Fun"><path d="M620,300C700,340 990,340 1080,300L1000,520L966,760L934,990L914,1190L900,1262L884,1190L852,990L806,760L740,520Z" fill="#1c242a" filter="url(#skBlur4)"/>
        <path d="M620,300L740,520L806,760L852,990L884,1190" fill="none" stroke="#4e5c66" stroke-width="7" opacity=".55" filter="url(#skBlur4)"/></g>
      <rect x="-1400" y="1250" width="4000" height="1400" fill="#1a221c"/><ellipse id="${id}Dust" cx="900" cy="1262" rx="200" ry="48" fill="#3a3028" opacity=".85" filter="url(#skBlur10)"/>
      ${Array.from({ length: 70 }, (_, k) => `<path d="M${(k * 97) % 1400 - 160},${(k * 211) % 1900}l-24,90" stroke="#9aa8b0" stroke-width="3" opacity=".3"/>`).join("")}`);
    put(L.set, Ngw.ctaSign(o));
  };
  // the sign alone (any scene can carry it as props): o.y = where the board's posts meet its bottom edge minus 90 (default 1040)
  Ngw.ctaSign = (o = {}) => {
    const id = o.id || "es";
    const T = (k, y, fs, fw, fill, txt, ls) => `<text id="${id}R${k}" y="${y}" text-anchor="middle" font-family="Kanit" font-weight="${fw}" font-size="${fs}" fill="${fill}"${ls ? ` letter-spacing="${ls}"` : ""} opacity=".14">${txt}</text>`;
    return `<defs><clipPath id="${id}Clip"><rect x="-460" y="-480" width="920" height="570" rx="30"/></clipPath>
      <linearGradient id="${id}GlintG" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
      <g transform="translate(540,${o.y ?? 1040})"><path d="M-300,60V900M300,60V900" stroke="#6e706c" stroke-width="28"/><path d="M-310,60V900M290,60V900" stroke="#a4a69e" stroke-width="6" opacity=".5"/>
        <g id="${id}"><rect x="-460" y="-480" width="920" height="570" rx="30" fill="#1e7a4a" stroke="#f2f0ea" stroke-width="12"/>
          <rect x="-436" y="-456" width="872" height="522" rx="20" fill="none" stroke="#f2f0ea" stroke-width="3" opacity=".3"/>
          ${T(1, -352, 104, 800, "#f2c230", o.l1 || "ปูจะรอดไหม?")}<path id="${id}Rule" d="M-380,-304H380" stroke="#f2f0ea" stroke-width="4" opacity=".14"/>
          ${T(2, -206, 84, 700, "#f2f0ea", o.l2 || "ดูเรื่องเต็มได้ที่")}${T(3, -78, 112, 800, "#f2f0ea", o.l3 || "ช่อง YouTube")}${T(4, 28, 60, 600, "#f2f0ea", o.l4 || "Rod Mai Club", 4)}
          <g clip-path="url(#${id}Clip)"><g id="${id}Glint" opacity="0"><rect x="-90" y="-520" width="180" height="660" fill="url(#${id}GlintG)" transform="skewX(-18)"/></g></g></g>
        <g transform="translate(0,90)"><g id="${id}Plate" opacity="0"><path d="M-200,0V60M200,0V60" stroke="#a4a69e" stroke-width="7" stroke-dasharray="10 6"/>
          <rect x="-260" y="60" width="520" height="150" rx="18" fill="#f2c230" stroke="#1a1a1a" stroke-width="8"/>
          <text y="170" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="96" fill="#1a1a1a">${o.plate || "กดติดตาม"}</text></g></g></g>`;
  };
  // the short's early follow tag (owner 4 Nov 2569: "หาจังหวะใส่ให้คนเห็น"): a small highway sign that drops on chains into the top of the
  // frame at a calm beat soon after the hook, while most viewers are still watching (FB: avg watch 36–50 s, ~30% left at 1:00), swings,
  // catches a glint and is pulled back up. Screen space (layer = L.light). Skipped in the 16:9 YouTube build: "the full story is on
  // YouTube" makes no sense there.
  Ngw.ctaTag = (tl, layer, t0, dur, o = {}) => {
    if (window.LANDSCAPE) return;
    const id = o.id || `ct${Math.round(t0 * 100)}`, y = o.y ?? 250, w = o.w ?? 700, h = 196, up = -(y + h + 80);
    put(layer, `<defs><clipPath id="${id}C"><rect x="${-w / 2}" y="0" width="${w}" height="${h}" rx="24"/></clipPath>
      <linearGradient id="${id}GG" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
      <g transform="translate(540,${y})"><g id="${id}" opacity="0">
        <path d="M${-w / 2 + 80},${-y - 40}V8M${w / 2 - 80},${-y - 40}V8" stroke="#a4a69e" stroke-width="8" stroke-dasharray="12 7"/>
        <rect x="${-w / 2}" y="0" width="${w}" height="${h}" rx="24" fill="#1e7a4a" stroke="#f2f0ea" stroke-width="10"/>
        <rect x="${-w / 2 + 18}" y="18" width="${w - 36}" height="${h - 36}" rx="14" fill="none" stroke="#f2f0ea" stroke-width="3" opacity=".3"/>
        <text y="92" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="84" fill="#f2c230">${o.l1 || "กดติดตาม"}</text>
        <text y="160" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="50" fill="#f2f0ea">${o.l2 || "ดูเรื่องเต็มที่ช่อง YouTube"}</text>
        <g clip-path="url(#${id}C)"><g id="${id}G" opacity="0"><rect x="-70" y="-40" width="140" height="${h + 80}" fill="url(#${id}GG)" transform="skewX(-18)"/></g></g></g></g>`);
    const sel = `#${id}`;
    tl.set(sel, { opacity: 1 }, t0);
    tl.fromTo(sel, { y: up, rotation: -4, transformOrigin: "50% 0%" }, { y: 0, rotation: 0, duration: 0.5, ease: "bounce.out", immediateRender: false }, t0);
    tl.to(sel, { keyframes: [{ rotation: 3, duration: 0.3, ease: "sine.out" }, { rotation: -2, duration: 0.36, ease: "sine.inOut" }, { rotation: 1, duration: 0.36, ease: "sine.inOut" }, { rotation: 0, duration: 0.4, ease: "sine.in" }], transformOrigin: "50% 0%" }, t0 + 0.45);
    tl.set(`#${id}G`, { opacity: 1 }, t0 + 1.3);
    tl.fromTo(`#${id}G`, { x: -w / 2 - 120 }, { x: w / 2 + 120, duration: 0.7, ease: "power2.inOut", immediateRender: false }, t0 + 1.3);
    tl.set(`#${id}G`, { opacity: 0 }, t0 + 2.0);
    tl.to(sel, { y: up, duration: 0.35, ease: "power2.in" }, t0 + dur - 0.35);
  };
  // ================= เสียงรถไฟ ตอนจบ (full 16:9 story, owner 4 Nov 2569: "ทำรวมเป็นเรื่องเดียว ขนาด 16:9") =================
  // Knowledge cards in the channel's graphic language (ผีแม่ม่าย mmui.js): an illustrated paper card, ink outlines, flat fills with one
  // shade and one highlight, soft drop shadow, Kanit labels; everything enters eased and staggered, then keeps a small secondary motion.
  // Drawn in world space for the 16:9 window (x −660…1740 around the centre 540), not in the vertical light layer.
  Sets.DEFS += `<linearGradient id="ngwPaper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf6"/><stop offset="1" stop-color="#efe7d2"/></linearGradient>
    <linearGradient id="ngwSkyCard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bcdcf2"/><stop offset="1" stop-color="#f4f0e2"/></linearGradient>
    <linearGradient id="ngwConc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8d6ce"/><stop offset="1" stop-color="#a4a29a"/></linearGradient>
    <linearGradient id="ngwFunCard" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#46525c"/><stop offset=".45" stop-color="#76828c"/><stop offset="1" stop-color="#364048"/></linearGradient>
    <radialGradient id="ngwSparkG"><stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="#e2f8ff" stop-opacity=".95"/><stop offset="1" stop-color="#6ad0ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="ngwPoleG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7e7c74"/><stop offset=".4" stop-color="#dcdad2"/><stop offset="1" stop-color="#6e6c64"/></linearGradient>
    <linearGradient id="ngwBeam" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#fff2c8" stop-opacity=".75"/><stop offset="1" stop-color="#fff2c8" stop-opacity="0"/></linearGradient>
    <linearGradient id="ngwZinc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8ccc8"/><stop offset=".5" stop-color="#aeb4b2"/><stop offset="1" stop-color="#8e9694"/></linearGradient>`;
  const CARD = (x, y, w, h) => `<rect x="${x + 18}" y="${y + 22}" width="${w}" height="${h}" rx="44" fill="#000" opacity=".3"/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="44" fill="url(#ngwPaper)" ${OUT(7)}/>`;
  const LBL = (x, y, t, fs, c) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="${fs}" fill="${c}" stroke="#fffdf6" stroke-width="14" paint-order="stroke">${t}</text>`;
  const FIG = (x, y, s, shirt) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse cy="4" rx="36" ry="9" fill="#000" opacity=".18"/><path d="M-16,0L-11,-70H11L16,0Z" fill="#3a4a6a" ${OUT(4)}/>
    <path d="M-23,-70Q-25,-132 0,-136Q25,-132 23,-70Z" fill="${shirt}" ${OUT(4)}/><path d="M-12,-126Q-6,-110 -8,-76" stroke="#fff" stroke-width="5" opacity=".35" fill="none"/><circle cy="-160" r="25" fill="#e6ae80" ${OUT(4)}/><path d="M-25,-168Q-21,-190 0,-188Q23,-188 25,-166" fill="#2a221c"/></g>`;
  const ZFRAME = (id, X, Y, W, H) => { const b = 50, x0 = X - b, y0 = Y - b, w = W + 2 * b, h = H + 2 * b;
    let g = [X + 150, X + W - 150].map((x) => `<path d="M${x},${y0 + 10}L${x + (x < 540 ? -60 : 60)},-1400" stroke="#5a4630" stroke-width="12"/><path d="M${x},${y0 + 10}L${x + (x < 540 ? -60 : 60)},-1400" stroke="#a8875a" stroke-width="6" stroke-dasharray="14 10"/>`).join("");
    g += `<rect x="${x0 + 18}" y="${y0 + 26}" width="${w}" height="${h}" rx="20" fill="#000" opacity=".38"/><clipPath id="${id}-zc"><rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="20"/></clipPath>`;
    g += `<rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="20" fill="url(#ngwZinc)"/><g clip-path="url(#${id}-zc)">`;
    for (let x = x0; x < x0 + w; x += 44) g += `<rect x="${x}" y="${y0}" width="18" height="${h}" fill="#e8ecea" opacity=".32"/><rect x="${x + 24}" y="${y0}" width="10" height="${h}" fill="#5a6260" opacity=".24"/>`;
    const haz = (y) => { let q = `<rect x="${x0}" y="${y}" width="${w}" height="30" fill="#f2c230"/>`; for (let x = x0 - 40; x < x0 + w + 40; x += 52) q += `<path d="M${x},${y + 30}L${x + 26},${y}H${x + 52}L${x + 26},${y + 30}Z" fill="#1e1a16"/>`; return q; };
    g += haz(y0 + 8) + haz(y0 + h - 38) + `</g><rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="20" fill="none" ${OUT(7)}/>`;
    g += [[x0 + 24, y0 + 24], [x0 + w - 24, y0 + 24], [x0 + 24, y0 + h - 24], [x0 + w - 24, y0 + h - 24], [X + 150, y0 + 24], [X + W - 150, y0 + 24]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="15" fill="#8a4a1e" opacity=".35"/><circle cx="${x}" cy="${y}" r="8" fill="#6a6e70" ${OUT(2.6)}/>`).join("");
    return g; };
  const CARDBG = (id, X, Y, W, H, gy, world) => `${world ? "" : `<rect x="-1400" y="-800" width="4000" height="3600" fill="#26303a"/>`}<g id="${id}-card">${world ? ZFRAME(id, X, Y, W, H) : ""}${CARD(X, Y, W, H)}
    <clipPath id="${id}-cp"><rect x="${X + 14}" y="${Y + 14}" width="${W - 28}" height="${H - 28}" rx="34"/></clipPath><g clip-path="url(#${id}-cp)">
    <rect x="${X}" y="${Y}" width="${W}" height="${gy - Y}" fill="url(#ngwSkyCard)"/><rect x="${X}" y="${gy}" width="${W}" height="${Y + H - gy}" fill="#7aa85a"/><rect x="${X}" y="${gy}" width="${W}" height="22" fill="#5a8a42"/>`;
  // the overpass wind tunnel (NWS: "Overpasses can concentrate the tornado winds, causing them to be significantly stronger.")
  const HUNG = (id, g, o) => o.world ? `<g id="${id}" transform="translate(540 ${o.cy ?? 900}) scale(${o.k ?? 0.8}) translate(-540 -960)"><g id="${id}-sway">${g}</g></g>` : `<g id="${id}">${g}</g>`;
  // a hung board drops in on its ropes and sways a little in the wind (world mode); the slate card rises in (o.world false)
  const HANGLIFE = (tl, id, t0, dur) => { const w = document.getElementById(`${id}-sway`);
    tl.fromTo(`#${id}-card`, w ? { y: -900, opacity: 1 } : { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: w ? 0.55 : 0.45, ease: w ? "back.out(1.2)" : "back.out(1.6)", immediateRender: false }, t0);
    if (w) tl.fromTo(w, { rotation: -0.7, svgOrigin: "540 -1400" }, { rotation: 0.7, svgOrigin: "540 -1400", duration: 1.7, ease: "sine.inOut", yoyo: true, repeat: Math.max(1, Math.ceil(dur / 1.7)), immediateRender: false }, t0 + 0.4); };
  Ngw.bridgeWind = (o = {}) => { const id = o.id || "bw", X = -560, Y = 380, W = 2200, H = 1160, gy = 1380;
    let g = CARDBG(id, X, Y, W, H, gy, o.world);
    g += `<g id="${id}-tor"><path d="M-470,${Y + 70}H-40L-150,${Y + 360}L-210,${gy - 260}L-250,${gy}H-310L-360,${gy - 260}L-410,${Y + 360}Z" fill="url(#ngwFunCard)" ${OUT(6)}/>`;
    for (let k = 0; k < 6; k++) { const y = Y + 120 + k * 150, w = 200 - k * 26; g += `<path class="${id}-band" d="M${-255 - w},${y}Q-255,${y + 30} ${-255 + w},${y}" stroke="#d4dce2" stroke-width="6" fill="none" opacity=".75"/>`; }
    g += `<ellipse cx="-280" cy="${gy}" rx="160" ry="34" fill="#8a7a5a" opacity=".75"/></g>`;
    const dx = 330, dw = 1000, dy = 830, dh = 80;
    g += `<path d="M${dx - 260},${gy}L${dx},${dy + dh}H${dx + 40}V${gy}Z" fill="#b8b6ae" ${OUT(5)}/><path d="M${dx + dw + 260},${gy}L${dx + dw},${dy + dh}H${dx + dw - 40}V${gy}Z" fill="#a8a69e" ${OUT(5)}/>`;
    g += `<rect x="${dx + 40}" y="${dy + dh}" width="${dw - 80}" height="${gy - dy - dh}" fill="#3a4450" opacity=".2"/>`;
    g += `<path d="M${dx},${dy}L${dx + 40},${dy - 34}H${dx + dw + 40}L${dx + dw},${dy}Z" fill="#e6e4dc" ${OUT(5)}/><rect x="${dx}" y="${dy}" width="${dw}" height="${dh}" fill="url(#ngwConc)" ${OUT(6)}/><path d="M${dx + 14},${dy + 14}H${dx + dw - 14}" stroke="#fff" stroke-width="5" opacity=".45"/>`;
    for (let x = dx + 20; x < dx + dw; x += 60) g += `<path d="M${x + 20},${dy - 34}V${dy - 72}" stroke="#7a786e" stroke-width="7"/>`;
    g += `<path d="M${dx + 20},${dy - 72}H${dx + dw + 30}" stroke="#7a786e" stroke-width="8"/>`;
    g += `<rect id="${id}-zone" x="${dx + 40}" y="${dy + dh}" width="${dw - 80}" height="${gy - dy - dh}" fill="#ff3a2a" opacity="0"/>`;
    const rib = (x0, x1, y, w, c, cls) => `<path class="${cls}" d="M${x0},${y}H${x1}" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-dasharray="${w * 3} ${w * 1.6}" opacity=".92"/><path d="M${x1 - 6},${y - w}L${x1 + w * 1.6},${y}L${x1 - 6},${y + w}Z" fill="${c}" ${OUT(3)}/>`;
    g += `<g id="${id}-out">` + [1010, 1120, 1230, 1330].map((y) => rib(-150, 170, y, 30, "#3a8ad8", `${id}-o`)).join("") + `</g>`;
    g += `<g id="${id}-jet" opacity="0">` + [970, 1050, 1130, 1210, 1290].map((y, k) => rib(380, 1250, y, 13, k % 2 ? "#ff6a2a" : "#e2382e", `${id}-i`)).join("");
    for (let k = 0; k < 16; k++) g += `<path d="M${400 + (k * 61) % 820},${960 + (k * 47) % 330}h${-50 - (k % 4) * 26}" stroke="#ff8a3a" stroke-width="4" stroke-linecap="round" opacity=".7"/>`;
    g += `</g><g id="${id}-ppl">${FIG(640, gy, 1.0, "#e2382e")}${FIG(800, gy, 0.95, "#2f6fd0")}${FIG(960, gy, 1.05, "#2fa864")}</g></g></g>`;
    g += `<g id="${id}-lbl1" opacity="0">${LBL(10, 960, "ลมข้างนอก", 60, "#2f6fd0")}</g><g id="${id}-lbl2" opacity="0">${LBL(830, 700, "ใต้สะพาน: ลมถูกบีบ แรงขึ้น", 68, "#e2382e")}</g>`;
    return HUNG(id, g, o); };
  Ngw.bridgeWindLife = (tl, id, t0, dur, at = []) => { const n = (p) => Math.max(1, Math.ceil(dur / p)), a0 = at[0] ?? t0 + 1.2;
    const pop = (sel, t, d = 0.35) => tl.fromTo(sel, { opacity: 0, scale: 0.7, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: d, ease: "back.out(2)", immediateRender: false }, t);
    HANGLIFE(tl, id, t0, dur);
    tl.fromTo(`#${id}-out`, { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.35, ease: "power2.out", immediateRender: false }, t0 + 0.35);
    tl.fromTo(`.${id}-o`, { strokeDashoffset: 0 }, { strokeDashoffset: -138, duration: 1.0, ease: "none", repeat: n(1.0), immediateRender: false }, t0);
    tl.fromTo(`.${id}-i`, { strokeDashoffset: 0 }, { strokeDashoffset: -60, duration: 0.25, ease: "none", repeat: n(0.25), immediateRender: false }, t0);
    tl.fromTo(`.${id}-band`, { x: -24 }, { x: 24, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: n(0.45), immediateRender: false }, t0);
    pop(`#${id}-lbl1`, t0 + 0.55);
    tl.fromTo(`#${id}-jet`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, a0);
    pop(`#${id}-lbl2`, a0 + 0.15, 0.4);
    tl.fromTo(`#${id}-ppl`, { x: 0 }, { x: 46, duration: 0.2, ease: "sine.inOut", yoyo: true, repeat: n(0.4), immediateRender: false }, a0);
    tl.fromTo(`#${id}-zone`, { opacity: 0 }, { keyframes: [{ opacity: 0.32, duration: 0.3 }, { opacity: 0.16, duration: 0.4 }, { opacity: 0.32, duration: 0.4 }, { opacity: 0.22, duration: 0.5 }], immediateRender: false }, at[1] ?? t0 + 3.5);
  };
  // the downed line (กรมอุตุนิยมวิทยา: "ถ้ามีเสาไฟฟ้าล้ม สายไฟขาดอย่าเข้าใกล้หรือแตะต้องเป็นอันขาด" · "อย่าแตะโลหะที่เป็นสื่อไฟฟ้า" ·
  // NWS: "Contact local authorities if you see power lines down.")
  const ARC = (s, k) => [0, 1, 2, 3].map((j) => { const a = k + j * 1.6; return `<path d="M0,0l${f1(28 * s * Math.cos(a))},${f1(28 * s * Math.sin(a) - 8 * s)}l${f1(-12 * s)},${f1(12 * s)}l${f1(34 * s * Math.cos(a + 0.4))},${f1(34 * s * Math.sin(a + 0.4))}" stroke="#ffffff" stroke-width="${f1(4.6 * s)}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`; }).join("");
  Ngw.LDGY = 1280;   // the board's ground line (QA "the top half is empty": raised from 1380, and the sky above dressed)
  Ngw.lineDanger = (o = {}) => { const id = o.id || "ld", X = -560, Y = 380, W = 2200, H = 1160, gy = Ngw.LDGY;
    let g = CARDBG(id, X, Y, W, H, gy, o.world);
    // the sky over the scene: the storm moving off to the right (rain still trailing under it), the sun back on the left
    g += `<g opacity=".9"><circle cx="-330" cy="700" r="120" fill="#ffe08a" opacity=".55"/><circle cx="-330" cy="700" r="70" fill="#fff2c0"/>${[0, 1, 2, 3, 4, 5, 6, 7].map((k) => { const a = (k / 8) * Math.PI * 2; return `<path d="M${f1(-330 + Math.cos(a) * 96)},${f1(700 + Math.sin(a) * 96)}L${f1(-330 + Math.cos(a) * 150)},${f1(700 + Math.sin(a) * 150)}" stroke="#ffd25a" stroke-width="10" stroke-linecap="round"/>`; }).join("")}
      ${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path d="M${1080 + k * 70},880l-30,${150 + (k % 3) * 40}" stroke="#7a8a98" stroke-width="6" stroke-linecap="round" opacity=".5"/>`).join("")}
      <path d="M940,880Q930,800 1010,780Q1040,700 1140,712Q1210,640 1320,690Q1420,650 1480,730Q1580,740 1570,830Q1600,880 1540,890H960Z" fill="#4a5664" ${OUT(5)}/><path d="M1000,850Q1100,830 1200,850T1420,846" stroke="#6a7888" stroke-width="8" fill="none" opacity=".7"/>
      <path d="M1600,760l40,-6M1610,800l46,0" stroke="#4a5664" stroke-width="8" stroke-linecap="round"/></g>`;
    g += `<g id="${id}-zone" opacity="0"><ellipse cx="560" cy="${gy + 40}" rx="840" ry="120" fill="#ffb42a" opacity=".35"/><ellipse cx="560" cy="${gy + 40}" rx="840" ry="120" fill="none" stroke="#e08a10" stroke-width="8" stroke-dasharray="36 22"/></g>`;
    g += `<path d="M-330,${gy}V${gy - 90}L-312,${gy - 122}L-292,${gy - 94}L-274,${gy - 118}V${gy}Z" fill="url(#ngwPoleG)" ${OUT(5)}/>`;
    g += `<g id="${id}-pole"><g transform="translate(-302,${gy - 70}) rotate(-12)"><rect x="0" y="-22" width="760" height="44" rx="10" fill="url(#ngwPoleG)" ${OUT(5)}/><path d="M680,-92V92M630,-72V72" stroke="#5a5e60" stroke-width="12"/><circle cx="680" cy="-90" r="10" fill="#e8e4dc" ${OUT(3)}/></g></g>`;
    g += `<g id="${id}-truck"><ellipse cx="760" cy="${gy + 6}" rx="300" ry="20" fill="#000" opacity=".2"/><path d="M500,${gy - 40}V${gy - 170}H700L760,${gy - 260}H900L960,${gy - 170}H1030V${gy - 40}Z" fill="#e8e4dc" ${OUT(6)}/><path d="M500,${gy - 110}H1030" stroke="#c8c2b4" stroke-width="10"/><path d="M712,${gy - 172}L762,${gy - 244}H888L930,${gy - 172}Z" fill="#9ad0f0" ${OUT(4)}/><path d="M520,${gy - 150}H690" stroke="#fff" stroke-width="6" opacity=".5"/>${[600, 940].map((x) => `<circle cx="${x}" cy="${gy - 34}" r="48" fill="#2a2e34" ${OUT(5)}/><circle cx="${x}" cy="${gy - 34}" r="20" fill="#8a8e94"/>`).join("")}</g>`;
    g += `<path id="${id}-hot" d="M500,${gy - 40}V${gy - 170}H700L760,${gy - 260}H900L960,${gy - 170}H1030V${gy - 40}Z" fill="#ffb42a" opacity="0"/>`;
    const wire = `M372,${gy - 240}Q600,${gy - 330} 830,${gy - 262}Q1010,${gy - 220} 1080,${gy - 120}Q1140,${gy - 20} 1220,${gy}`;
    g += `<path d="${wire}" stroke="${INK}" stroke-width="12" fill="none" stroke-linecap="round"/><path d="${wire}" stroke="#5a5e64" stroke-width="5" fill="none"/>`;
    const spark = (x, y, k) => `<g class="${id}-sp" opacity="0" transform="translate(${x},${y})"><circle r="78" fill="url(#ngwSparkG)"/>${ARC(1.3, k)}</g>`;
    g += spark(830, gy - 262, 0.4) + spark(1220, gy, 1.3);
    g += `<g id="${id}-call" opacity="0">${FIG(1440, gy, 1.25, "#2fa864")}<rect x="1454" y="${gy - 216}" width="24" height="42" rx="6" fill="#ffd23a" ${OUT(3)}/>${[0, 1, 2].map((k) => `<path class="${id}-wave" d="M${1494 + k * 22},${gy - 228}q${18 + k * 8},${22 + k * 6} 0,${46 + k * 14}" stroke="#1e7a48" stroke-width="6" fill="none" stroke-linecap="round"/>`).join("")}</g></g></g>`;
    g += `<g id="${id}-l0" opacity="0">${LBL(540, 560, "เสาไฟล้ม สายไฟขาด", 84, "#2a2622")}</g><g id="${id}-l1" opacity="0">${LBL(-70, gy + 122, "อย่าเข้าใกล้", 68, "#d07a08")}</g><g id="${id}-l2" opacity="0">${LBL(760, gy - 330, "อย่าแตะ", 66, "#e2382e")}</g><g id="${id}-l3" opacity="0">${LBL(1420, gy - 300, "แจ้งเจ้าหน้าที่", 58, "#1e7a48")}</g>`;
    return HUNG(id, g, o); };
  Ngw.lineDangerLife = (tl, id, t0, dur, at = []) => { const n = (p) => Math.max(1, Math.ceil(dur / p));
    const pop = (sel, t, d = 0.35) => tl.fromTo(sel, { opacity: 0, scale: 0.7, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: d, ease: "back.out(2)", immediateRender: false }, t);
    HANGLIFE(tl, id, t0, dur);
    const po = `-302 ${Ngw.LDGY - 70}`;
    tl.fromTo(`#${id}-pole`, { rotation: -70, svgOrigin: po }, { rotation: 0, svgOrigin: po, duration: 0.55, ease: "bounce.out", immediateRender: false }, (at[0] ?? t0) + 0.1);
    pop(`#${id}-l0`, (at[0] ?? t0) + 0.25, 0.4);
    tl.fromTo(`.${id}-sp`, { opacity: 0.3, scale: 0.8 }, { keyframes: [{ opacity: 1, scale: 1.2, duration: 0.06 }, { opacity: 0.5, scale: 0.9, duration: 0.12 }, { opacity: 0.3, scale: 0.8, duration: 0.2 }, { opacity: 0.3, duration: 0.42 }], repeat: n(0.8), immediateRender: false }, (at[0] ?? t0) + 0.6);
    tl.fromTo(`#${id}-zone`, { opacity: 0, scale: 0.7, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)", immediateRender: false }, at[1] ?? t0 + 1.5);
    pop(`#${id}-l1`, (at[1] ?? t0 + 1.5) + 0.1);
    tl.fromTo(`#${id}-hot`, { opacity: 0 }, { keyframes: [{ opacity: 0.45, duration: 0.25 }, { opacity: 0.22, duration: 0.35 }, { opacity: 0.45, duration: 0.35 }, { opacity: 0.3, duration: 0.4 }], immediateRender: false }, at[2] ?? t0 + 4);
    pop(`#${id}-l2`, (at[2] ?? t0 + 4) + 0.1);
    tl.fromTo(`#${id}-call`, { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)", immediateRender: false }, at[3] ?? t0 + 6);
    pop(`#${id}-l3`, (at[3] ?? t0 + 6) + 0.15);
    tl.fromTo(`.${id}-wave`, { opacity: 0.2 }, { opacity: 1, duration: 0.3, yoyo: true, repeat: n(0.6), stagger: 0.1, immediateRender: false }, at[3] ?? t0 + 6);
  };
  // lying face down, side view (SPC: lie flat face-down in a ditch, protect the back of your head with your arms): the rig can only
  // lie on its side with the chest and face to the camera (reads as lying on the back), so the two ditch shots use this drawing —
  // the back, the back of the head (ปู's hat, ตาเทียน's white fringe), the near forearm over the side of the head, hands locked
  // on the nape, toes dug in. (x, y) = the shoulder on the ground; the head points right (o.flip: left). who "pu" | "taTian"
  Ngw.prone = (x, y, s = 1, who = "pu", o = {}) => {
    const K = who === "pu", id = o.id || "pr", dk = (c, a = 0.25) => { const n = parseInt(c.slice(1), 16); return "#" + [16, 8, 0].map((b) => Math.round(((n >> b) & 255) * (1 - a)).toString(16).padStart(2, "0")).join(""); };
    const C = K ? { skin: "#d49c6c", top: "#d8382a", bot: "#b8a070", shin: "#d49c6c", foot: "#3a6ad0" } : { skin: "#8a5a3a", top: "#b09a68", bot: "#34363e", shin: "#34363e", foot: "#5a3a22" };
    const hr = K ? 54 : 44, hx = K ? 136 : 128, hy = -hr - 2;   // ปู's head is bigger for his size
    const limb = (pts, w, c) => `<path d="M${pts.map((q) => q.join(",")).join("L")}" stroke="${INK}" stroke-width="${w + 7}" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M${pts.map((q) => q.join(",")).join("L")}" stroke="${c}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
    const foot = (fx, c) => `<path d="M${fx + 6},-36L${fx - 30},-44L${fx - 40},-30L${fx - 16},0L${fx + 4},-2Z" fill="${c}" ${OUT(4)}/><path d="M${fx - 30},-40L${fx - 10},-6" stroke="${dk(c, 0.35)}" stroke-width="5"/>`;
    let g = "";
    // far leg and foot (behind, in shadow), then the near leg; ปู: khaki shorts to the knee, bare shins
    g += limb([[-170, -30], [-440, -20]], 40, dk(K ? C.shin : C.bot, 0.3)) + foot(-446, dk(C.foot, 0.3));
    if (K) g += limb([[-170, -36], [-262, -32]], 46, dk(C.bot, 0.3));
    g += limb([[-160, -26], [-430, -14]], 42, C.shin) + foot(-434, C.foot);
    if (K) g += limb([[-160, -30], [-268, -26]], 48, C.bot) + `<path d="M-268,-52V-2" stroke="${dk(C.bot, 0.35)}" stroke-width="5"/>`;
    // seat and back: the shirt's back, a shade strip along the ground, ปู's stripes run across his back; ตาเทียน's shirt seam
    g += `<path d="M-214,-4Q-218,-70 -160,-74Q-130,-74 -110,-66L-110,-4Z" fill="${C.bot}" ${OUT(5)}/>`;
    g += `<path id="${id}-back" d="M-150,-66Q-60,-96 40,-88Q74,-84 84,-60L88,-4H-150Z" fill="${C.top}" ${OUT(5)}/>`;
    if (K) g += [-120, -80, -40, 0, 40].map((sx) => `<path d="M${sx},${sx > 20 ? -84 : -86 + Math.abs(sx + 40) * 0.08}Q${sx - 6},-46 ${sx},-6" stroke="#f6f2ea" stroke-width="13" fill="none"/>`).join("");
    else g += `<path d="M-60,-86Q-56,-46 -60,-6" stroke="${dk(C.top, 0.25)}" stroke-width="4" fill="none"/><path d="M60,-80Q76,-60 70,-36" stroke="${dk(C.top, 0.3)}" stroke-width="4" fill="none"/>`;
    g += `<path d="M-150,-20H86" stroke="${dk(C.top, 0.35)}" stroke-width="16" opacity=".55"/>`;
    // ตาเทียน's ผ้าขาวม้า over the shoulder, its end flapping in the wind
    if (!K) g += `<path d="M30,-90Q58,-96 76,-74L64,-62Q46,-80 26,-76Z" fill="#c8483a" ${OUT(3)}/><g class="${id}-flap"><path d="M30,-88Q-10,-104 -46,-96L-40,-82Q-6,-90 28,-76Z" fill="#c8483a" ${OUT(3)}/><path d="M24,-84Q-8,-94 -40,-88" stroke="#f2e6d8" stroke-width="2.4" stroke-dasharray="5 5" fill="none"/></g>`;
    // far arm behind the head (elbow forward by the ground, forearm up to the nape)
    g += limb([[54, -72], [hx + 70, -34], [hx - 22, hy - hr * 0.62]], 24, dk(C.skin, 0.32));
    // neck and head: the back of the head toward us, face pressed to the ground
    g += `<path d="M70,-76Q90,-82 100,-66L102,-24L74,-22Z" fill="${dk(C.skin, 0.1)}" ${OUT(4)}/>`;
    g += `<circle cx="${hx}" cy="${hy}" r="${hr}" fill="${C.skin}" ${OUT(5)}/>`;
    if (K) {   // black hair at the back, the green bucket hat crown pointing ahead along the ground, the brim a ring round the head
      g += `<path d="M${hx - hr * 0.9},${hy + hr * 0.4}Q${hx - hr * 1.02},${hy - hr * 0.7} ${hx - hr * 0.2},${hy - hr * 0.98}L${hx - hr * 0.1},${hy + hr * 0.7}Z" fill="#2a1e18"/>`;
      g += `<g class="${id}-flap"><path d="M${hx - 12},${hy - hr - 14}Q${hx + hr + 30},${hy - hr - 16} ${hx + hr + 26},${hy}Q${hx + hr + 30},${hy + hr + 8} ${hx - 6},${hy + hr + 6}Z" fill="#4a8a5a" ${OUT(5)}/></g>`;
      g += `<ellipse cx="${hx - 8}" cy="${hy}" rx="16" ry="${hr + 22}" fill="#3a7a4a" ${OUT(5)}/><path d="M${hx + 20},${hy - hr + 4}Q${hx + hr},${hy - hr * 0.4} ${hx + hr + 4},${hy + 6}" stroke="#6aa87a" stroke-width="6" fill="none" opacity=".7"/>`;
    } else {   // bald crown with a shine, the white fringe round the back, an ear
      g += `<path d="M${hx - hr * 0.86},${hy + hr * 0.5}Q${hx - hr * 1.05},${hy - hr * 0.1} ${hx - hr * 0.62},${hy - hr * 0.78}L${hx - hr * 0.42},${hy - hr * 0.5}Q${hx - hr * 0.7},${hy} ${hx - hr * 0.5},${hy + hr * 0.62}Z" fill="#f2f0ea" ${OUT(2.4)}/>`;
      g += `<ellipse cx="${hx + 10}" cy="${hy - hr * 0.5}" rx="${hr * 0.42}" ry="${hr * 0.2}" fill="#fff" opacity=".22" transform="rotate(-30 ${hx + 10} ${hy - hr * 0.5})"/>`;
    }
    g += `<path d="M${hx - 4},${hy + 4}q-12,-2 -12,12q0,14 12,12" fill="${dk(C.skin, 0.12)}" ${OUT(3)}/>`;
    // near arm: short sleeve on the upper arm, elbow down in front of the face, forearm over the side of the head, hands on the nape
    const ex = hx + hr + 26, ey = -18, nx = hx - 26, ny = hy - hr * 0.55;
    g += limb([[50, -60], [ex, ey]], 30, C.skin) + limb([[50, -60], [50 + (ex - 50) * 0.36, -60 + (ey + 60) * 0.36]], 40, C.top);
    if (K) g += `<path d="M${50 + (ex - 50) * 0.2},-70v26" stroke="#f6f2ea" stroke-width="9"/>`;
    g += limb([[ex, ey], [nx, ny]], 27, C.skin);
    g += `<g transform="translate(${nx},${ny}) rotate(-34)"><ellipse rx="24" ry="17" fill="${C.skin}" ${OUT(4)}/><path d="M-12,-12v22M-2,-14v26M8,-12v22" stroke="${dk(C.skin, 0.4)}" stroke-width="3" stroke-linecap="round"/></g>`;
    // the ground contact shadow
    const sh = `<ellipse cx="-160" cy="2" rx="${K ? 330 : 360}" ry="12" fill="#000" opacity=".28"/>`;
    return `<g id="${id}" transform="translate(${x},${y}) scale(${o.flip ? -s : s},${s})">${sh}<g class="${id}-body">${K ? `<g transform="scale(0.82)">${g}</g>` : g}</g></g>`;
  };
  // wind on someone lying flat: a shiver through the body, the hat brim / the scarf end flapping
  Ngw.proneLife = (tl, id, t0, dur) => {
    tl.fromTo(`#${id} .${id}-body`, { x: -1.2 }, { x: 1.2, duration: 0.09, ease: "sine.inOut", yoyo: true, repeat: Math.ceil(dur / 0.09), immediateRender: false }, t0);
    tl.fromTo(`#${id} .${id}-flap`, { rotation: -3, transformOrigin: "20% 80%" }, { rotation: 6, duration: 0.13, ease: "sine.inOut", yoyo: true, repeat: Math.ceil(dur / 0.13), immediateRender: false }, t0);
  };
  // the insert at "ตา! ลงคูเร็ว!" — ported from ทะเลลด EP.2's wrist grab (tide2.js herArm / hisArm) and recoloured: ตาเทียน's old
  // forearm comes up from the bottom (khaki short sleeve, dark weathered skin, veins, age spots, white hairs), the back of his hand to us,
  // fingers open; ปู's young arm comes down from the top left (red-and-white tee sleeve) and his hand clamps ตาเทียน's wrist.
  // Drawn with the grip at (0, 0), placed at (o.x, o.y) × o.s. ids: #id-ta (ตาเทียน's arm), #id-tf (his fingers), #id-pu (ปู's arm),
  // #id-popen / #id-pshut (ปู's hand reaching / closed), #id-pk (knuckles whitening), #id-hit, #id-spd
  Ngw.wristGrab = (o = {}) => {
    const id = o.id || "wg", P2 = (q) => `${f1(q[0])},${f1(q[1])}`, ln = (w = 3) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
    const cap = (A, B, wa, wb) => { const dx = B[0] - A[0], dy = B[1] - A[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l;
      const a1 = [A[0] + (nx * wa) / 2, A[1] + (ny * wa) / 2], a2 = [A[0] - (nx * wa) / 2, A[1] - (ny * wa) / 2], b1 = [B[0] + (nx * wb) / 2, B[1] + (ny * wb) / 2], b2 = [B[0] - (nx * wb) / 2, B[1] - (ny * wb) / 2];
      return `M${P2(a1)}L${P2(b1)}A${f1(wb / 2)},${f1(wb / 2)} 0 0 0 ${P2(b2)}L${P2(a2)}A${f1(wa / 2)},${f1(wa / 2)} 0 0 0 ${P2(a1)}Z`; };
    const r = mk(o.seed || 77);
    // ---- ตาเทียน (the forearm up from the bottom, the wrist at (0, 0), the hand up)
    const T = { sk: "#8a5a3a", skD: "#5a3620", skL: "#b48460", vein: "#5e3420", nail: "#d8c2a8", ...(o.T || {}) },   // o.T / o.ST: the held arm's skin and sleeve
      ST = { c: "#b09a68", d: "#8e7a4c", l: "#e8dcc0", e1: "#6e5e3a", e2: "#4a3e26", cuff: "#c8b484", cuffL: "#f0e6cc", ...(o.ST || {}) };
    let ta = `<path d="M-128,384Q0,356 134,386L196,1700H-176Z" fill="${ST.c}" ${ln(3.2)}/>
      <path d="M-96,470Q-84,900 -120,1500M36,450Q52,900 44,1600M110,470Q140,800 150,1300" stroke="${ST.d}" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/>
      <path d="M-50,480Q-30,900 -40,1500" stroke="${ST.l}" stroke-width="10" fill="none" opacity=".3" stroke-linecap="round"/><ellipse cx="4" cy="394" rx="122" ry="34" fill="${ST.e1}" ${ln(2.6)}/><ellipse cx="4" cy="402" rx="104" ry="22" fill="${ST.e2}"/>`;
    ta += `<path d="${cap([0, 0], [6, 352], 100, 128)}" fill="${T.sk}" ${ln(3)}/><path d="M26,40Q36,200 38,380" stroke="${T.skD}" stroke-width="14" fill="none" opacity=".4" stroke-linecap="round"/>
      <path d="M-24,60Q-30,220 -22,370" stroke="${T.skL}" stroke-width="10" fill="none" opacity=".45" stroke-linecap="round"/>
      <path d="M-10,40Q20,150 -6,240Q-20,300 6,370" stroke="${T.vein}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-12,38Q18,150 -8,240" stroke="${T.skL}" stroke-width="2.4" fill="none" opacity=".6"/>`;
    for (let k = 0; k < 22; k++) { const x = -40 + r() * 80, y = 60 + r() * 300; ta += `<path d="M${f1(x)},${f1(y)}l${f1(-6 - r() * 5)},${f1(-2 - r() * 3)}" stroke="#ece6dc" stroke-width="1.4" opacity=".55"/>`; }
    for (let k = 0; k < 6; k++) ta += `<ellipse cx="${f1(-36 + r() * 72)}" cy="${f1(60 + r() * 280)}" rx="${f1(3 + r() * 4)}" ry="${f1(2 + r() * 3)}" fill="${T.skD}" opacity=".5"/>`;
    ta += `<path d="M-126,396Q4,446 132,396Q130,418 4,462Q-122,420 -126,396Z" fill="${ST.cuff}" ${ln(2.8)}/><path d="M-100,412Q4,446 108,412" stroke="${ST.cuffL}" stroke-width="4" fill="none" opacity=".6" stroke-linecap="round"/>`;
    let th = `<path d="M-54,-40Q-66,-110 -64,-178Q-32,-198 8,-198Q50,-196 70,-172Q78,-110 58,-40Q32,-20 0,-22Q-32,-22 -54,-40Z" fill="${T.sk}" ${ln(3)}/>
      <path d="M-34,-56Q-36,-120 -40,-168M-10,-56Q-10,-120 -14,-176M14,-56Q16,-120 14,-178M36,-60Q42,-118 42,-168" stroke="${T.skD}" stroke-width="3.4" fill="none" opacity=".5" stroke-linecap="round"/>
      <path d="M-24,-60Q-24,-120 -28,-170" stroke="${T.skL}" stroke-width="7" fill="none" opacity=".45" stroke-linecap="round"/><path d="M20,-50Q30,-90 10,-130" stroke="${T.vein}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
    th += [[-30, -100, 6], [24, -140, 5], [40, -80, 4], [-10, -160, 4]].map(([x, y, rr]) => `<ellipse cx="${x}" cy="${y}" rx="${rr}" ry="${f1(rr * 0.8)}" fill="${T.skD}" opacity=".5"/>`).join("");
    const F = [[-46, -178, -24, 100, 27], [-16, -192, -8, 128, 31], [14, -194, 4, 136, 32], [44, -182, 16, 120, 30]];
    let tf = "";
    F.forEach(([x, y, a, l, w]) => { const rr = (a * Math.PI) / 180, B = [x + Math.sin(rr) * l, y - Math.cos(rr) * l], M2 = [x + Math.sin(rr) * l * 0.5, y - Math.cos(rr) * l * 0.5], N = [x + Math.sin(rr) * (l - 10), y - Math.cos(rr) * (l - 10)];
      tf += `<path d="${cap([x, y], B, w, w * 0.84)}" fill="${T.sk}" ${ln(2.8)}/><path d="M${f1(M2[0] - w * 0.3)},${f1(M2[1])}q${f1(w * 0.3)},4 ${f1(w * 0.6)},0" stroke="${T.skD}" stroke-width="2.4" fill="none"/>`;
      tf += `<ellipse cx="${f1(N[0])}" cy="${f1(N[1])}" rx="${f1(w * 0.3)}" ry="${f1(w * 0.36)}" fill="${T.nail}" stroke="${T.skD}" stroke-width="1.4" transform="rotate(${a} ${f1(N[0])} ${f1(N[1])})"/><circle cx="${f1(x)}" cy="${f1(y + 6)}" r="${f1(w * 0.22)}" fill="${T.skL}" opacity=".6"/>`; });
    tf += `<path d="M56,-60Q100,-84 122,-140Q130,-160 116,-166Q102,-168 96,-150Q80,-112 52,-100Z" fill="${T.sk}" ${ln(2.8)}/><ellipse cx="115" cy="-153" rx="7" ry="9" fill="${T.nail}" stroke="${T.skD}" stroke-width="1.4" transform="rotate(30 115 -153)"/>`;
    const beads = (pts) => pts.map(([x, y, rr]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="#fff" opacity=".5"/><circle cx="${f1(x - rr * 0.3)}" cy="${f1(y - rr * 0.3)}" r="${f1(rr * 0.35)}" fill="#fff"/>`).join("");
    let g = `<g id="${id}-ta">${ta}<g id="${id}-tf">${tf}</g>${th}${beads([[-30, 200, 5], [20, 260, 4], [-12, 320, 6], [30, -120, 4], [-30, -150, 3.5]])}</g>`;
    // ---- ปู (the grip at (0, 0): the back of his right hand over ตาเทียน's wrist, the forearm up to the top left, the red tee sleeve)
    const U = { sk: "#d49c6c", skD: "#a8704a", skL: "#f2c89e", nail: "#f6d8c6", ...(o.U || {}) },   // o.U / o.SU: the gripping hand's skin and sleeve (SU.stripe "" = plain, SU.dots = a print)
      SU = { c: "#d8382a", stripe: "#f6f2ea", cuff: "#a82218", dots: "", ...(o.SU || {}) };
    const W0 = [-140, -6], dir = [-0.8, -0.6], at = (d) => [W0[0] + dir[0] * d, W0[1] + dir[1] * d], nrm = [-dir[1], dir[0]];
    let pu = `<g id="${id}-spd" opacity="0">${[-120, -40, 40, 120].map((o2) => `<path d="M${P2([at(700)[0] + nrm[0] * o2, at(700)[1] + nrm[1] * o2])}L${P2([at(1300)[0] + nrm[0] * o2, at(1300)[1] + nrm[1] * o2])}" stroke="#f2f4f6" stroke-width="8" stroke-linecap="round" opacity=".7"/>`).join("")}</g>`;
    pu += `<path d="${cap(W0, at(900), 112, 136)}" fill="${U.sk}" ${ln(3.2)}/><path d="M${P2(at(60))}L${P2(at(560))}" stroke="${U.skD}" stroke-width="22" opacity=".25" transform="translate(-22,26)" stroke-linecap="round"/>`;
    pu += `<path d="M${P2([at(80)[0] + 18, at(80)[1] - 28])}L${P2([at(520)[0] + 22, at(520)[1] - 36])}" stroke="${U.skL}" stroke-width="12" opacity=".45" stroke-linecap="round"/>`;
    const c0 = at(600);
    { const e1 = at(1500), q = (P, w) => [[P[0] + nrm[0] * w, P[1] + nrm[1] * w], [P[0] - nrm[0] * w, P[1] - nrm[1] * w]], [a1, a2] = q(c0, 98), [b1, b2] = q(e1, 118);
      pu += `<path d="M${P2(a1)}L${P2(b1)}L${P2(b2)}L${P2(a2)}Z" fill="${SU.c}" ${ln(3.2)}/>`; }
    for (let k = 0; SU.stripe && k < 6; k++) { const q = at(660 + k * 120); pu += `<path d="M${P2([q[0] + nrm[0] * 110, q[1] + nrm[1] * 110])}L${P2([q[0] - nrm[0] * 110, q[1] - nrm[1] * 110])}" stroke="${SU.stripe}" stroke-width="30"/>`; }
    for (let k = 0; SU.dots && k < 9; k++) { const q = at(680 + (k % 3) * 230 + (k > 5 ? 60 : 0)), w = [-58, 4, 62][Math.floor(k / 3)]; pu += `<g transform="translate(${f1(q[0] + nrm[0] * w)},${f1(q[1] + nrm[1] * w)})">${[0, 72, 144, 216, 288].map((d) => `<circle cx="${f1(9 * Math.cos((d * Math.PI) / 180))}" cy="${f1(9 * Math.sin((d * Math.PI) / 180))}" r="7" fill="${SU.dots}"/>`).join("")}<circle r="4" fill="#f2c230"/></g>`; }
    pu += `<path d="M${P2([c0[0] + nrm[0] * 92, c0[1] + nrm[1] * 92])}L${P2([c0[0] - nrm[0] * 92, c0[1] - nrm[1] * 92])}" stroke="${SU.cuff}" stroke-width="16" stroke-linecap="round"/><path d="M${P2([c0[0] - 90 * nrm[0], c0[1] - 90 * nrm[1]])}L${P2([at(1400)[0] - 90 * nrm[0], at(1400)[1] - 90 * nrm[1]])}" stroke="#8a1e18" stroke-width="10" opacity=".35"/>`;
    const back = `M-182,-44Q-160,-88 -72,-88Q-28,-86 -16,-70Q-8,-20 -12,60Q-20,84 -64,88Q-122,92 -170,60Q-196,10 -182,-44Z`;
    pu += `<path d="${back}" fill="${U.sk}" ${ln(3)}/><path d="M-176,-40q10,-18 30,-14" stroke="${U.skL}" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>`;
    pu += `<path d="M-140,-20Q-80,-40 -30,-60M-140,-6Q-80,-14 -28,-22M-140,8Q-80,14 -28,16M-140,22Q-84,40 -32,54" stroke="${U.skL}" stroke-width="4" fill="none" opacity=".5" stroke-linecap="round"/>`;
    const FY = [[-58, 28], [-22, 32], [16, 34], [52, 32]];
    let shut = "";
    FY.forEach(([y, w]) => { shut += `<path d="${cap([-30, y], [44, y + 4], w, w * 0.94)}" fill="${U.sk}" ${ln(2.8)}/>`;
      shut += `<path d="M-6,${f1(y - w * 0.32)}q4,${f1(w * 0.32)} 0,${f1(w * 0.64)}M30,${f1(y - w * 0.3)}q-4,${f1(w * 0.3)} 0,${f1(w * 0.6)}" stroke="${U.skD}" stroke-width="2.4" fill="none"/>`;
      shut += `<path d="M52,${f1(y + 4 - w * 0.44)}A${f1(w * 0.47)},${f1(w * 0.47)} 0 0 1 52,${f1(y + 4 + w * 0.44)}" stroke="${U.skD}" stroke-width="6" fill="none" opacity=".5" stroke-linecap="round"/>`; });
    shut += `<g id="${id}-pk" opacity=".15">${FY.map(([y, w]) => `<ellipse cx="-24" cy="${y}" rx="${f1(w * 0.38)}" ry="${f1(w * 0.42)}" fill="#fbe2c8"/><ellipse cx="46" cy="${y + 4}" rx="${f1(w * 0.26)}" ry="${f1(w * 0.3)}" fill="#fbe2c8"/>`).join("")}</g>`;
    shut += FY.map(([y, w]) => `<path d="M-30,${f1(y - w * 0.36)}q-8,${f1(w * 0.36)} 0,${f1(w * 0.72)}" stroke="${U.skD}" stroke-width="2.4" fill="none" opacity=".8"/>`).join("");
    const thumb = `<path d="M-120,64Q-96,104 -54,108Q-36,108 -40,92Q-50,78 -78,70Q-100,58 -116,46Z" fill="${U.sk}" ${ln(2.8)}/><ellipse cx="-48" cy="99" rx="7" ry="5" fill="${U.nail}" stroke="${U.skD}" stroke-width="1.4"/>`;
    let open = "";
    FY.forEach(([y, w], i) => { const L0 = 128 + [0, 14, 20, 10][i], sp = [-12, -4, 4, 12][i];
      open += `<path d="${cap([-30, y], [-30 + L0, y + sp], w, w * 0.84)}" fill="${U.sk}" ${ln(2.8)}/><ellipse cx="${f1(-30 + L0 - 9)}" cy="${f1(y + sp * 0.93)}" rx="${f1(w * 0.3)}" ry="${f1(w * 0.26)}" fill="${U.nail}" stroke="${U.skD}" stroke-width="1.4"/>`; });
    g += `<g id="${id}-pu">${pu}${thumb}<g id="${id}-popen" opacity="0">${open}</g><g id="${id}-pshut">${shut}</g></g>`;
    g += `<g id="${id}-hit" opacity="0">${[[-1, -0.5], [-0.3, -1], [0.5, -0.9], [1, -0.2], [0.9, 0.6], [-1, 0.5]].map(([dx, dy]) => `<path d="M${f1(dx * 170)},${f1(dy * 150)}l${f1(dx * 70)},${f1(dy * 70)}" stroke="#fff" stroke-width="10" stroke-linecap="round"/>`).join("")}</g>`;
    // o.rot turns the whole insert (QA 5: ตาเทียน's arm straight up from the bottom edge read as being pulled out of a hole)
    return `<g transform="translate(${o.x ?? 640},${o.y ?? 1230}) rotate(${o.rot ?? 0}) scale(${(o.flip ? -1 : 1) * (o.s ?? 1)},${o.s ?? 1})"><g id="${id}">${g}</g></g>`; };
  // ปู's hand flies in along his arm and clamps at `at` (on "ตา!"): squash, ตาเทียน's fingers splay, the knuckles whiten as the grip
  // tightens; the tug at `tug` ("ลงคูเร็ว!") hauls both down and to the left, then a strained tremble to the end
  Ngw.wristGrabLife = (tl, id, t0, dur, at = 0.3, tug = 0.8) => { const q = (s) => `#${id}${s}`;
    tl.set(q("-pu"), { x: 760, y: 570, opacity: 0 }, t0); tl.set(q("-popen"), { opacity: 1 }, t0); tl.set(q("-pshut"), { opacity: 0 }, t0);
    tl.fromTo(q("-pu"), { x: -760, y: -570, opacity: 1 }, { x: 0, y: 0, opacity: 1, duration: 0.2, ease: "power2.in", immediateRender: false }, t0 + at - 0.2);
    tl.fromTo(q("-spd"), { opacity: 0.9 }, { opacity: 0, duration: 0.3, immediateRender: false }, t0 + at - 0.14);
    tl.set(q("-popen"), { opacity: 0 }, t0 + at); tl.set(q("-pshut"), { opacity: 1 }, t0 + at);
    tl.fromTo(q("-pu"), { scaleX: 1 }, { keyframes: [{ scaleX: 0.94, scaleY: 1.04, duration: 0.05 }, { scaleX: 1, scaleY: 1, duration: 0.12 }], svgOrigin: "0 0", immediateRender: false }, t0 + at);
    tl.fromTo(q("-hit"), { opacity: 1, scale: 0.7, svgOrigin: "0 0" }, { opacity: 0, scale: 1.35, svgOrigin: "0 0", duration: 0.3, ease: "power2.out", immediateRender: false }, t0 + at);
    tl.fromTo(q("-tf"), { scale: 1, svgOrigin: "0 -180" }, { keyframes: [{ scale: 1.14, duration: 0.08 }, { scale: 1.05, duration: 0.3 }], svgOrigin: "0 -180", immediateRender: false }, t0 + at + 0.02);
    tl.fromTo(q("-pk"), { opacity: 0.15 }, { opacity: 0.85, duration: 0.6, immediateRender: false }, t0 + at + 0.1);
    tl.fromTo(q(""), { x: 0, y: 0 }, { x: -110, y: 50, duration: 0.34, ease: "power2.inOut", immediateRender: false }, t0 + tug);
    tl.fromTo(q("-ta"), { rotation: 0, svgOrigin: "0 1600" }, { rotation: -3, svgOrigin: "0 1600", duration: 0.34, ease: "power2.inOut", immediateRender: false }, t0 + tug);
    tl.fromTo(q("-tf"), { rotation: -2, svgOrigin: "0 -180" }, { rotation: 2, svgOrigin: "0 -180", duration: 0.06, yoyo: true, repeat: Math.max(1, Math.ceil(dur / 0.06)), immediateRender: false }, t0 + at + 0.4);
  };
  // "ที่มา: …" chip (owner's standard, as in ทะเลลด): a pill with a small funnel badge, page-positioned at the bottom right of the clip
  Ngw.srcChip = (tl, clipId, t0, text, o = {}) => { const clip = document.getElementById(clipId); if (!clip) return;
    const d = document.createElement("div"); d.className = "srcchip";
    Object.assign(d.style, { position: "absolute", right: (o.right ?? 36) + "px", bottom: (o.bottom ?? 40) + "px", zIndex: 57, display: "flex", alignItems: "center", gap: "10px", padding: "7px 18px 7px 7px",
      borderRadius: "999px", background: "rgba(220,230,232,.94)", border: "3px solid #1e2a2c", boxShadow: "0 5px 0 #2d6a6e", font: "600 28px/1 Kanit", color: "#1e2a2c", opacity: 0, whiteSpace: "nowrap" });
    d.innerHTML = `<span style="width:34px;height:34px;border-radius:50%;background:#2d8a8e;border:3px solid #1e2a2c;display:inline-flex;align-items:center;justify-content:center"><svg width="20" height="20" viewBox="0 0 20 20"><path d="M2,3H18L13,8L11,12L10,18L9,12L7,8Z" fill="#fff"/></svg></span>ที่มา: ${text}`;
    // 16:9 (QA 5: the lowered captions covered it): page-positioned in the bottom-right corner, clear of the centred caption box
    if (window.LANDSCAPE) { d.classList.add("pagepos"); Object.assign(d.style, { right: "44px", bottom: "36px", fontSize: "26px" }); }
    clip.appendChild(d); tl.fromTo(d, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out", immediateRender: false }, t0 + (o.at ?? 0.4)); };
  // a power pole knocked flat at (x, y), its line draped to (wx, wy) on whatever it fell across and on to the ground at (ex, ey)
  Ngw.fallenPole = (x, y, s = 1, o = {}) => { const id = o.id || "fp", lean = o.lean ?? -70, a = (lean * Math.PI) / 180;
    const tx = x + 440 * s * Math.sin(-a) * -1, ty = y - 440 * s * Math.cos(a);   // the pole top after the lean
    const wx = o.wx ?? x + 500, wy = o.wy ?? y - 120, ex = o.ex ?? wx + 260, ey = o.ey ?? y;
    let g = Ngw.pole(x, y, s, { lean });
    g += `<path d="M${f1(x - 20 * s)},${y}l${f1(10 * s)},${f1(-30 * s)}l${f1(14 * s)},${f1(22 * s)}l${f1(12 * s)},${f1(-18 * s)}" stroke="#5a5a56" stroke-width="${f1(8 * s)}" fill="none"/>`;
    const d = `M${f1(tx)},${f1(ty)}Q${f1((tx + wx) / 2)},${f1(Math.max(ty, wy) + 60)} ${f1(wx)},${f1(wy)}Q${f1((wx + ex) / 2)},${f1(wy + 20)} ${f1(ex)},${f1(ey)}`;
    g += `<path d="${d}" stroke="#1e1a16" stroke-width="${f1(7 * s)}" fill="none"/>`;
    // the live end (QA: "a thin live wire"): a scorch where it lies, a smoke wisp always rising (#id-sm, puffs .id-smp), and the arc (#id-sp):
    // jagged bolts with a cyan glow and a white core, spark beads thrown up and out — popped by Ngw.sparkLife, one pop a period (V1b)
    const rr = mk(Math.round(wx * 7 + wy * 3) % 997 + 11), bolt = (a, L0) => { let x = 0, y = 0, d = "M0,0"; for (let k = 0; k < 6; k++) { const aa = a + (rr() - 0.5) * 1.3, l = L0 * (0.14 + rr() * 0.1); x += Math.cos(aa) * l; y += Math.sin(aa) * l; d += `L${f1(x)},${f1(y)}`; } return d; };
    const bl = [-2.2, -1.5, -0.9, -0.2, 0.5].map((a) => bolt(a + (rr() - 0.5) * 0.4, (110 + rr() * 70) * s));
    g += `<ellipse cx="${f1(wx)}" cy="${f1(wy + 6 * s)}" rx="${f1(52 * s)}" ry="${f1(13 * s)}" fill="#14100c" opacity=".5"/>`;
    g += `<g id="${id}-sm" transform="translate(${f1(wx)},${f1(wy)})">${[0, 1, 2].map((k) => `<circle class="${id}-smp" cx="${f1((k - 1) * 12 * s)}" cy="${f1(-16 * s)}" r="${f1((18 + k * 7) * s)}" fill="#9a9c9a" opacity="0" filter="url(#skBlur4)"/>`).join("")}</g>`;
    g += `<g id="${id}-sp" transform="translate(${f1(wx)},${f1(wy)})"><circle r="${f1(96 * s)}" fill="url(#ngwSparkG)"/>`
      + bl.map((d) => `<path d="${d}" stroke="#6ad0ff" stroke-width="${f1(11 * s)}" fill="none" stroke-linejoin="round" stroke-linecap="round" opacity=".55"/><path d="${d}" stroke="#ffffff" stroke-width="${f1(3.6 * s)}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`).join("")
      + Array.from({ length: 12 }, () => { const a = -Math.PI * (0.1 + rr() * 0.8), d = (40 + rr() * 90) * s; return `<circle cx="${f1(Math.cos(a) * d)}" cy="${f1(Math.sin(a) * d)}" r="${f1((2.4 + rr() * 2.6) * s)}" fill="${rr() > 0.4 ? "#fffbe8" : "#ffd25a"}"/>`; }).join("") + `</g>`;
    return g; };
  Ngw.sparkLife = (tl, sel, t0, dur, period = 0.8) => { const n = Math.max(1, Math.ceil(dur / period));   // one bright pop per period (V1b: ≤ 3 a second)
    tl.fromTo(sel, { opacity: 0.32, scale: 0.7 }, { keyframes: [{ opacity: 1, scale: 1.25, duration: 0.06 }, { opacity: 0.55, scale: 0.95, duration: 0.12 }, { opacity: 0.32, scale: 0.7, duration: 0.2 }, { opacity: 0.32, duration: Math.max(0.05, period - 0.38) }], repeat: n, immediateRender: false }, t0);   // a dim crackle stays on between pops
    // the smoke off a downed line's live end (#x-sm next to #x-sp): three puffs rising and spreading, one after another, the whole time
    const sm = sel.replace(/-sp$/, "-sm"); if (sm !== sel && document.querySelector(sm)) document.querySelectorAll(`.${sm.slice(1)}p`).forEach((e, k) =>
      tl.fromTo(e, { y: 0, x: 0, opacity: 0.5, scale: 0.6, transformOrigin: "50% 50%" }, { y: -150, x: 30, opacity: 0, scale: 1.9, duration: 1.8, ease: "sine.out", repeat: Math.ceil(dur / 1.8), immediateRender: false }, t0 + k * 0.6)); };
  // ปู's little camera
  Ngw.cam = (x, y, s = 1, rot = 0) => `<g transform="translate(${x},${y}) rotate(${rot}) scale(${s})"><rect x="-44" y="-30" width="88" height="58" rx="10" fill="#2a2e34" stroke="#1e1a16" stroke-width="5"/><circle r="19" fill="#4a6a8a" stroke="#1e1a16" stroke-width="5"/><circle r="9" fill="#9ad0f0"/><rect x="18" y="-42" width="20" height="12" fill="#2a2e34" stroke="#1e1a16" stroke-width="3"/><circle cx="-28" cy="-16" r="5" fill="#d8312a"/></g>`;
  // glass bursting out of a window rect toward the camera (one small flash on the pane, never a full-screen flash: V1b)
  Ngw.shatter = (tl, layer, t0, o = {}) => { const id = o.id || `sh${Math.round(t0 * 100)}`, x = o.x ?? 360, y = o.y ?? 420, w = o.w ?? 560, h = o.h ?? 640, n = o.n ?? 46, r = mk(o.seed || 17);
    const cx = x + w / 2, cy = y + h / 2; let g = `<g id="${id}"><rect id="${id}-fl" x="${x}" y="${y}" width="${w}" height="${h}" fill="#eaf6ff" opacity="0"/>`;
    const sh = [];
    for (let k = 0; k < n; k++) { const px = x + r() * w, py = y + r() * h, sz = 14 + r() * 34;
      g += `<path id="${id}-s${k}" d="M${f1(px)},${f1(py - sz)}L${f1(px + sz * 0.7)},${f1(py + sz * 0.5)}L${f1(px - sz * 0.6)},${f1(py + sz * 0.3)}Z" fill="#d8eef8" stroke="#ffffff" stroke-width="2" opacity="0"/>`;
      sh.push([k, px - cx, py - cy, r()]); }
    if (o.hole) { let e = ""; const edge = (ax, ay, bx, by, k) => { const m = 5; for (let j = 0; j < m; j++) { const t0 = j / m, t1 = (j + 1) / m, d = 30 + r() * 70;
        const p0 = [ax + (bx - ax) * t0, ay + (by - ay) * t0], p1 = [ax + (bx - ax) * t1, ay + (by - ay) * t1], nx = k[0] * d, ny = k[1] * d;
        e += `<path d="M${f1(p0[0])},${f1(p0[1])}L${f1((p0[0] + p1[0]) / 2 + nx)},${f1((p0[1] + p1[1]) / 2 + ny)}L${f1(p1[0])},${f1(p1[1])}Z" fill="#d8eef8" stroke="#ffffff" stroke-width="2" opacity=".75"/>`; } };
      edge(x, y, x + w, y, [0, 1]); edge(x, y + h, x + w, y + h, [0, -1]); edge(x, y, x, y + h, [1, 0]); edge(x + w, y, x + w, y + h, [-1, 0]);
      for (let k = 0; k < 26; k++) { const px = x + r() * w, py = y + r() * h; e += `<path d="M${f1(px)},${f1(py)}l${f1(-60 - r() * 80)},${f1(90 + r() * 60)}" stroke="#cfe6f2" stroke-width="3" opacity=".55"/>`; }
      g += `<g id="${id}-hole" opacity="0">${e}</g>`; }
    put(layer, g + `</g>`);
    if (o.hole) tl.set(`#${id}-hole`, { opacity: 1 }, t0 + 0.02);
    tl.fromTo(`#${id}-fl`, { opacity: 0 }, { keyframes: [{ opacity: 0.7, duration: 0.04 }, { opacity: 0, duration: 0.2 }], immediateRender: false }, t0);
    sh.forEach(([k, dx, dy, q]) => { const f = 1.6 + q * 1.8;
      tl.fromTo(`#${id}-s${k}`, { opacity: 1, x: 0, y: 0, rotation: 0, scale: 1, transformOrigin: "50% 50%" }, { opacity: 0, x: dx * f + (q - 0.5) * 300, y: dy * f + 260 + q * 300, rotation: (q - 0.5) * 720, scale: 2 + q * 2.5, duration: 0.7 + q * 0.5, ease: "power2.out", immediateRender: false }, t0 + q * 0.06); });
  };
  // QA ("a weak window blast"): what comes in behind the glass — wet leaves, twigs, a torn paper, then a sheet of rain spraying across the
  // room; everything flies from the hole toward the camera and the floor, growing as it nears (one burst at t, the rain on to t + dur)
  Ngw.blastIn = (tl, layer, t, o = {}) => { const id = o.id || "bi", x = o.x ?? 360, y = o.y ?? 420, w = o.w ?? 560, h = o.h ?? 640, r = mk(o.seed || 29), cx = x + w / 2, cy = y + h / 2, dur = o.dur ?? 1.6;
    let g = `<g id="${id}">`; const P = [];
    for (let k = 0; k < 34; k++) { const px = cx + (r() - 0.5) * w * 0.7, py = cy + (r() - 0.5) * h * 0.6, kind = k % 5, sz = 0.8 + r() * 0.9;
      const shape = kind === 0 ? `<path d="M0,-16Q14,-4 0,16Q-14,-4 0,-16Z" fill="#4a7a34" stroke="#1e1a16" stroke-width="2.4"/><path d="M0,-14V14" stroke="#2e4a22" stroke-width="2"/>`
        : kind === 1 ? `<path d="M-22,2L22,-2" stroke="#6a4a2a" stroke-width="5" stroke-linecap="round"/><path d="M4,0l10,-10" stroke="#6a4a2a" stroke-width="3" stroke-linecap="round"/>`
        : kind === 2 ? `<path d="M-14,-12L16,-9L12,14L-16,10Z" fill="#e8e2d0" stroke="#1e1a16" stroke-width="2"/><path d="M-8,-4h16M-8,3h12" stroke="#8a8478" stroke-width="2"/>`
        : kind === 3 ? `<path d="M0,-12Q12,0 0,12Q-12,0 0,-12Z" fill="#6a9a40" stroke="#1e1a16" stroke-width="2"/>`
        : `<circle r="5" fill="#cfe6f2" opacity=".8"/>`;
      g += `<g id="${id}-p${k}" transform="translate(${f1(px)},${f1(py)})" opacity="0"><g transform="scale(${f1(sz)})">${shape}</g></g>`; P.push([k, px - cx, py - cy, r()]); }
    g += `<g id="${id}-rain" opacity="0">${Array.from({ length: 30 }, () => { const sx = cx + (r() - 0.5) * w * 0.8, sy = cy + (r() - 0.5) * h * 0.7, L0 = 260 + r() * 420, a = 0.25 + r() * 0.5;
      return `<path d="M${f1(sx)},${f1(sy)}l${f1(Math.cos(a) * L0 * (r() > 0.5 ? 1 : -1))},${f1(Math.sin(a) * L0)}" stroke="#e6f2f8" stroke-width="${f1(2 + r() * 3)}" stroke-linecap="round" opacity="${f1(0.3 + r() * 0.4)}"/>`; }).join("")}</g>`;
    put(layer, g + `</g>`);
    P.forEach(([k, dx, dy, q]) => { const f = 2.2 + q * 2.4;
      tl.fromTo(`#${id}-p${k}`, { opacity: 1, x: 0, y: 0, rotation: 0, scale: 0.6 }, { opacity: 0.9, x: dx * f + (q - 0.5) * 900, y: dy * f + 420 + q * 520, rotation: (q - 0.5) * 900, scale: 2.6 + q * 3, duration: 0.6 + q * 0.7, ease: "power1.in", immediateRender: false }, t + 0.02 + q * 0.25);
      tl.to(`#${id}-p${k}`, { opacity: 0, duration: 0.15, immediateRender: false }, t + 0.62 + q * 0.95); });
    tl.fromTo(`#${id}-rain`, { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.12 }, { opacity: 0.85, duration: Math.max(0.2, dur - 0.5) }, { opacity: 0, duration: 0.38 }], immediateRender: false }, t + 0.08);
    tl.fromTo(`#${id}-rain`, { x: 0, y: 0 }, { x: -40, y: 120, duration: dur, ease: "none", immediateRender: false }, t + 0.08); };
  // the CTA sign lights row by row on the narrator's beats (at = ปูจะรอดไหม, กดติดตาม, แล้วไปดูเรื่องเต็ม, ได้ที่ช่อง YouTube);
  // the plate drops on "กดติดตาม" and swings to rest, a headlight glint sweeps the sign on "YouTube", the funnel drifts behind it
  Ngw.endCtaLife = (tl, id, t0, dur, at) => {
    const lit = (sel, t) => tl.fromTo(sel, { opacity: 0.14 }, { opacity: 1, duration: 0.35, ease: "power2.out", immediateRender: false }, t);
    lit(`#${id}R1`, at[0] - 0.05); lit(`#${id}Rule`, at[0] + 0.2); lit(`#${id}R2`, at[2] - 0.05); lit(`#${id}R3`, at[3] - 0.05); lit(`#${id}R4`, at[3] + 0.3);
    tl.set(`#${id}Plate`, { opacity: 1 }, at[1] - 0.12);
    tl.fromTo(`#${id}Plate`, { y: -150, rotation: -8, transformOrigin: "50% 0%" }, { y: 0, rotation: 0, duration: 0.4, ease: "bounce.out", immediateRender: false }, at[1] - 0.12);
    tl.to(`#${id}Plate`, { keyframes: [{ rotation: 4.5, duration: 0.3, ease: "sine.out" }, { rotation: -3, duration: 0.36, ease: "sine.inOut" }, { rotation: 1.5, duration: 0.36, ease: "sine.inOut" }, { rotation: 0, duration: 0.4, ease: "sine.in" }], transformOrigin: "50% 0%" }, at[1] + 0.28);
    tl.set(`#${id}Glint`, { opacity: 1 }, at[3] - 0.05);
    tl.fromTo(`#${id}Glint`, { x: -640 }, { x: 640, duration: 0.8, ease: "power2.inOut", immediateRender: false }, at[3] - 0.05);
    tl.set(`#${id}Glint`, { opacity: 0 }, at[3] + 0.78);
    if (document.getElementById(`${id}Fun`)) {   // the plain night sky of Sets.ngwEndCta (a scene with Ngw.epic animates its own storm)
      tl.fromTo(`#${id}Fun`, { x: -12 }, { x: 16, duration: dur, ease: "sine.inOut", immediateRender: false }, t0);
      tl.fromTo(`#${id}Dust`, { scale: 0.9, transformOrigin: "50% 50%" }, { scale: 1.15, duration: dur, ease: "sine.inOut", immediateRender: false }, t0); }
  };
  // ---------------------------------------------------------------- the lake, its bank, the shrine
  Ngw.lake = (o = {}) => {   // from the horizon hz down to the near shore y1, in perspective: swell bands, wind streaks, whitecaps
    const hz = o.hz ?? 900, y1 = o.y1 ?? 1480, r = mk(o.seed || 5), D = y1 - hz;
    let g = `<rect x="-1400" y="${hz}" width="4000" height="${D + 60}" fill="url(#ngwLake)"/>`;
    for (let k = 0; k < 20; k++) { const t = Math.pow(k / 20, 1.8), y = hz + t * D, amp = 2 + t * 22, ph = r() * 6; let d = `M-1400,${f1(y)}`;
      for (let x = -1400; x <= 2600; x += 80) d += `L${x},${f1(y + amp * Math.sin(x * (0.004 + 0.002 * (1 - t)) + ph))}`;
      g += `<path d="${d}V${f1(y + 14 + t * 60)}H-1400Z" fill="${k % 2 ? "#3e525a" : "#16222a"}" opacity="${f1(0.18 + 0.2 * t)}"/>`; }
    g += `<path d="M-1400,${hz + 2}H2600" stroke="#b4c6c8" stroke-width="3" opacity=".6"/>`;
    for (let k = 0; k < 80; k++) { const t = Math.pow(r(), 1.7), y = hz + 6 + t * (D - 10), L0 = 40 + t * 360 * (0.5 + r()), x = -1300 + r() * 3700;
      g += `<path d="M${f1(x)},${f1(y)}h${f1(L0)}" stroke="#a6babe" stroke-width="${f1(1 + t * 2.6)}" opacity="${f1(0.1 + 0.16 * r())}"/>`; }
    for (let k = 0; k < 110; k++) { const t = Math.pow(r(), 1.25), y = hz + 8 + t * (D - 14), w = 5 + t * 40, x = -1300 + r() * 3700;
      g += `<path d="M${f1(x)},${f1(y)}l${f1(w)},${f1(-1 - t * 2)}" stroke="#eaf2f2" stroke-width="${f1(1.2 + t * 3)}" stroke-linecap="round" opacity="${f1(0.22 + 0.4 * r())}"/>`; }
    return g;
  };
  // the near bank: the waterline with foam, lotus leaves in the shallows, the muddy edge, grass, reeds bending in the wind
  Ngw.bank = (o = {}) => {
    const y1 = o.y1 ?? 1480, r = mk(o.seed || 8), wind = o.wind ?? 1;
    const edge = (y, amp, ph) => { let d = ""; for (let x = -1400; x <= 2600; x += 60) d += `${x === -1400 ? "M" : "L"}${x},${f1(y + amp * Math.sin(x * 0.006 + ph) + amp * 0.5 * Math.sin(x * 0.017 + ph * 2))}`; return d; };
    let g = "";
    // lotus leaves and buds in the shallows just off the shore
    for (let k = 0; k < 26; k++) { const x = -1200 + r() * 3600, t = r(), y = y1 - 70 + t * 70, s = 0.5 + t * 0.9;
      g += `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(s)},${f1(s * 0.42)})"><path d="M0,0L-26,-8A30,30 0 1 0 -8,-26Z" fill="#2e5a34" stroke="${INK}" stroke-width="3"/><path d="M0,0L-20,22M0,0L18,18M0,0L24,-6" stroke="#5a8a54" stroke-width="2.4"/></g>`;
      if (k % 5 === 0) g += `<g transform="translate(${f1(x + 30 * s)},${f1(y - 4)}) scale(${f1(s * 0.8)})"><path d="M0,0V-40" stroke="#3e6a3a" stroke-width="4"/><path d="M0,-38Q-14,-56 0,-76Q14,-56 0,-38Z" fill="#e88aa8" stroke="${INK}" stroke-width="2.4"/><path d="M0,-40Q-6,-56 0,-70" stroke="#f8c8d8" stroke-width="2" fill="none"/></g>`; }
    g += `<path d="${edge(y1 + 4, 6, 1)}" stroke="#e2ecec" stroke-width="5" fill="none" opacity=".55"/>`;
    g += `<path d="${edge(y1, 10, 2)}V2600H-1400Z" fill="#3a3222"/><path d="${edge(y1 + 26, 14, 3)}V2600H-1400Z" fill="#2c3a24"/>`;
    g += `<path d="${edge(y1 + 120, 20, 4)}V2600H-1400Z" fill="#22301e"/>`;
    // grass blades along the bank top and reeds (cattails) in clumps
    let gr = ""; for (let x = -1400; x < 2600; x += 9 + r() * 10) { const y = y1 + 26 + 14 * Math.sin(x * 0.006 + 3), h = 16 + r() * 30, l = wind * (6 + r() * 12); gr += `M${f1(x)},${f1(y + 4)}q${f1(l * 0.4)},${f1(-h * 0.6)} ${f1(l)},${f1(-h)}`; }
    g += `<path d="${gr}" stroke="#4a6a3a" stroke-width="3" fill="none" stroke-linecap="round" opacity=".9"/>`;
    (o.reeds || [-900, -520, -150, 1180, 1500, 1900]).forEach((x0) => { let rd = ""; for (let k = 0; k < 9; k++) { const x = x0 + (r() - 0.5) * 120, h = 160 + r() * 160, l = wind * (30 + r() * 50), y = y1 + 30;
      rd += `<path d="M${f1(x)},${y}q${f1(l * 0.3)},${f1(-h * 0.6)} ${f1(l)},${f1(-h)}" stroke="#3e5a2e" stroke-width="5" fill="none" stroke-linecap="round"/>`;
      if (k % 2) rd += `<path d="M${f1(x + l * 0.85)},${f1(y - h * 0.86)}l${f1(l * 0.1)},${f1(-h * 0.14)}" stroke="#6a4a2a" stroke-width="13" stroke-linecap="round"/>`; } g += rd; });
    return g;
  };
  // a naga statue at the lake's edge: concrete plinth, two coils, the hooded head with its crest, a marigold garland, incense smoke
  Ngw.naga = (x, y, s = 1, o = {}) => {
    const G = o.c || "#3e8a5a", Gd = "#24583a", Gh = "#86c896", Au = "#e8b830";
    let g = `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="8" rx="170" ry="22" fill="#000" opacity=".35"/>`;
    g += `<path d="M-150,0V-44H150V0Z" fill="#a8a294" ${OUT(4)}/><path d="M-150,-44H150" stroke="#cec8ba" stroke-width="6"/><path d="M-120,-20h60M20,-24h80" stroke="#8a8476" stroke-width="3"/>`;
    const coil = (cx, w, h) => `<path d="M${cx - w},-44Q${cx - w},${-44 - h} ${cx},${-44 - h}Q${cx + w},${-44 - h} ${cx + w},-44Z" fill="${G}" ${OUT(4)}/><path d="M${cx - w * 0.7},-50Q${cx - w * 0.7},${-40 - h * 0.86} ${cx},${-40 - h * 0.86}" stroke="${Gh}" stroke-width="6" fill="none" opacity=".7"/>
      <path d="M${cx - w * 0.8},-60Q${cx},${-30 - h} ${cx + w * 0.8},-60" stroke="${Gd}" stroke-width="4" fill="none" stroke-dasharray="8 10" opacity=".8"/>`;
    g += coil(70, 60, 74) + coil(-90, 44, 56);
    // the neck rising from the front coil and arching over; scales as rows of arcs; the pale belly plates on its front edge
    const neck = "M-30,-44C-40,-150 40,-200 10,-300C0,-330 -20,-344 -36,-350L-6,-372C30,-350 64,-300 50,-220C40,-150 20,-120 34,-44Z";
    g += `<path d="${neck}" fill="${G}" ${OUT(4.5)}/><path d="M-26,-60C-34,-150 34,-196 6,-290" stroke="#e8d8a0" stroke-width="10" fill="none" stroke-dasharray="10 6" opacity=".85"/>`;
    for (let k = 0; k < 7; k++) g += `<path d="M${f1(4 + 6 * Math.sin(k))},${-80 - k * 34}q14,-10 26,0" stroke="${Gd}" stroke-width="3.4" fill="none" opacity=".75"/>`;
    // the head: hood and crest flames (gold), the snout to the left, a red eye, the mouth with fangs
    g += `<g transform="translate(-20,-370)"><path d="M-10,0Q-30,-40 -6,-80Q10,-108 40,-110Q30,-90 44,-80Q26,-60 40,-40Q20,-30 30,-6Z" fill="${Au}" ${OUT(3.4)}/>
      <path d="M8,-90q8,-20 26,-24M10,-60q12,-14 28,-14M8,-30q12,-6 22,0" stroke="#b8862a" stroke-width="3" fill="none"/>
      <path d="M30,0C10,-20 -30,-30 -64,-24Q-80,-20 -78,-8L-60,-2Q-70,6 -60,14Q-30,22 0,18Q24,16 30,0Z" fill="${G}" ${OUT(4)}/>
      <path d="M-62,-2Q-36,4 -6,2" stroke="${INK}" stroke-width="3" fill="none"/><path d="M-50,-1l3,10l4,-9M-30,1l3,9l3,-9" fill="#f6f2e4" stroke="${INK}" stroke-width="1.6"/>
      <ellipse cx="-30" cy="-14" rx="7" ry="5" fill="#d8302a" stroke="${INK}" stroke-width="2"/><circle cx="-28" cy="-15" r="1.8" fill="#fff"/>
      <path d="M-70,-20q-4,-4 -2,-8" stroke="${INK}" stroke-width="2.4" fill="none"/></g>`;
    // the garland (marigolds) round the neck, and a pot of incense on the plinth with smoke curling off in the wind
    let gl = ""; for (let k = 0; k <= 12; k++) { const a = Math.PI * k / 12, bx = -6 - 34 * Math.cos(a), by = -170 + 26 * Math.sin(a); gl += `<circle cx="${f1(bx)}" cy="${f1(by)}" r="7" fill="${k % 3 ? "#f29a1a" : "#e8402a"}" stroke="#7a3a10" stroke-width="1.4"/>`; }
    g += gl + `<path d="M-40,-160q-6,30 -2,60" stroke="#f29a1a" stroke-width="5" stroke-dasharray="6 4"/>`;
    g += `<g transform="translate(-110,-44)"><path d="M-22,0L-18,-26H18L22,0Z" fill="#8a6a3a" ${OUT(2.6)}/>${[-8, 0, 8].map((dx, k) => `<path d="M${dx},-26l${-3 + k * 3},-46" stroke="#a83a2a" stroke-width="3"/><circle cx="${dx - 3 + k * 3}" cy="${-72}" r="2.6" fill="#ffb84a"/><path d="M${dx - 3 + k * 3},-74q${16 + k * 6},-24 ${30 + k * 10},-36t${30 + k * 14},-40" stroke="#e8e4dc" stroke-width="${3 - k * 0.6}" fill="none" opacity=".45"/>`).join("")}</g>`;
    return g + `</g>`;
  };
  // small far villagers on the bank holding phones up (silhouette-ish, flat colours), each [x, y, s, shirt]
  Ngw.crowd = (list) => list.map(([x, y, s, c, phone = 1]) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse cy="2" rx="22" ry="5" fill="#000" opacity=".35"/>
    <path d="M-12,0L-10,-50H10L12,0Z" fill="#2a2e38"/><path d="M-18,-50L-14,-104Q0,-112 14,-104L18,-50Z" fill="${c}" ${OUT(2.4)}/><circle cy="-124" r="17" fill="#c8946a" ${OUT(2.4)}/><path d="M-17,-128Q-14,-148 0,-148Q16,-148 17,-128Q8,-136 -2,-134Q-10,-138 -17,-128Z" fill="#1a1410"/>
    ${phone ? `<path d="M10,-98L28,-150" stroke="${c}" stroke-width="9" stroke-linecap="round"/><rect x="20" y="-176" width="16" height="26" rx="3" fill="#1e1e26" stroke="${INK}" stroke-width="1.6"/><rect x="22" y="-173" width="12" height="18" fill="#bfe8ff" opacity=".9"/>` : `<path d="M14,-98L22,-60M-14,-98L-22,-60" stroke="${c}" stroke-width="9" stroke-linecap="round"/>`}</g>`).join("");

  // ---------------------------------------------------------------- the village: the temple (โบสถ์ + เจดีย์), a school, a far strip of lake
  Ngw.wat = (x, y, s = 1, o = {}) => {
    const R = o.roof || "#b8402a", Gr = "#2e7a4a", Au = "#e2b034", W = "#f0eadc";
    let g = `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="60" cy="10" rx="520" ry="34" fill="#000" opacity=".3"/>`;
    // the chedi beside it (right, behind)
    g += `<g transform="translate(330,0)"><path d="M-90,0V-40H90V0ZM-70,-40V-70H70V-40Z" fill="${W}" ${OUT(4)}/><path d="M-62,-70Q-70,-150 0,-190Q70,-150 62,-70Z" fill="${W}" ${OUT(4)}/>
      ${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${-18 + k * 3},${-196 - k * 22}H${18 - k * 3}" stroke="${INK}" stroke-width="4"/><path d="M${-16 + k * 3},${-196 - k * 22}L${-12 + k * 2},${-214 - k * 22}H${12 - k * 2}L${16 - k * 3},${-196 - k * 22}Z" fill="${W}" stroke="${INK}" stroke-width="2.4"/>`).join("")}
      <path d="M0,-330V-380" stroke="${Au}" stroke-width="8" stroke-linecap="round"/><path d="M-40,-120Q0,-100 40,-120" stroke="#c8beaa" stroke-width="4" fill="none"/></g>`;
    // the hall: platform, white walls with columns, red-gold door and windows
    g += `<path d="M-300,0V-44H300V0Z" fill="#d8d0c0" ${OUT(5)}/><path d="M-240,-44V-250H240V-44Z" fill="${W}" ${OUT(5)}/>`;
    [-200, -110, 110, 200].forEach((cx) => { g += `<path d="M${cx},-46V-250" stroke="#c8bea8" stroke-width="14"/>`; });
    g += `<path d="M-46,-46V-170Q0,-200 46,-170V-46Z" fill="#a8302a" ${OUT(4)}/><path d="M0,-50V-178" stroke="${Au}" stroke-width="4"/>`;
    [-155, 155].forEach((cx) => { g += `<rect x="${cx - 24}" y="-200" width="48" height="80" fill="#a8302a" ${OUT(3)}/><path d="M${cx},-200V-120" stroke="${Au}" stroke-width="3"/>`; });
    // three stacked gables with tiled slopes, green edges, gold chofa and hang-hong curls
    const tier = (y0, hw, apex) => `<path d="M${-hw - 40},${y0}L0,${apex}L${hw + 40},${y0}L${hw + 10},${y0 + 16}L0,${apex + 30}L${-hw - 10},${y0 + 16}Z" fill="${R}" ${OUT(4)}/>
      <path d="M${-hw - 40},${y0}L0,${apex}L${hw + 40},${y0}" stroke="${Gr}" stroke-width="12" fill="none" stroke-linejoin="round"/><path d="M${-hw - 40},${y0}L0,${apex}L${hw + 40},${y0}" stroke="${Au}" stroke-width="3.4" fill="none" stroke-dasharray="10 8"/>
      <path d="M0,${apex}q-10,-24 6,-44q12,-14 0,-30" stroke="${Au}" stroke-width="9" fill="none" stroke-linecap="round"/>
      <path d="M${-hw - 40},${y0}q-24,-2 -26,-26M${hw + 40},${y0}q24,-2 26,-26" stroke="${Au}" stroke-width="7" fill="none" stroke-linecap="round"/>`;
    g += tier(-410, 150, -640) + tier(-330, 210, -560);
    g += `<path d="M-300,-240L0,-470L300,-240L270,-226L0,-430L-270,-226Z" fill="${R}" ${OUT(4)}/>`;
    g += `<path d="M-190,-252L0,-420L190,-252Z" fill="${Au}" ${OUT(4)}/><path d="M-120,-262L0,-370L120,-262" stroke="#a8781e" stroke-width="5" fill="none"/><circle cx="0" cy="-310" r="24" fill="none" stroke="#a8781e" stroke-width="5"/>`;
    g += tier(-240, 260, -470).replace(/^<path[^>]*\/>/, "");
    return g + `</g>`;
  };
  Ngw.school = (x, y, s = 1) => {
    let g = `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="8" rx="460" ry="26" fill="#000" opacity=".3"/>`;
    g += `<path d="M-420,0V-330H420V0Z" fill="#e8dcc0" ${OUT(5)}/><path d="M-440,-330L-400,-400H400L440,-330Z" fill="#a84a2e" ${OUT(5)}/><path d="M-420,-170H420" stroke="#c8b898" stroke-width="10"/>`;
    for (let r0 = 0; r0 < 2; r0++) for (let k = 0; k < 7; k++) g += `<rect x="${-380 + k * 110}" y="${-300 + r0 * 150}" width="70" height="90" fill="#4a7ab0" ${OUT(3)}/><path d="M${-345 + k * 110},${-300 + r0 * 150}v90" stroke="#2a4a7a" stroke-width="3"/>`;
    g += `<path d="M500,0V-560" stroke="#b8b8b8" stroke-width="10"/><circle cx="500" cy="-566" r="10" fill="#e2b034"/>`;
    return g + `</g>`;
  };
  // the kuti bathroom: green tiles to the shoulder, damp plaster, a breeze-block vent (the only "window", high up), a plank door with a
  // bolt, a tiled water tank with a floating ขัน, a saffron robe on a line, a bare bulb on its cord (#id-bulb swings, #id-glow flickers)
  Sets.ngwKuti = function (L, o = {}) {
    const id = o.id || "ku", fy = o.floor ?? 1500, ty = fy - 640, r = mk(o.seed || 21);
    put(L.sky, `<rect x="-1400" y="-800" width="4000" height="3600" fill="#2a2620"/>`);
    let w = `<rect x="-1400" y="-300" width="4000" height="${fy + 300}" fill="url(#ngwPlaster)"/>`;
    for (let k = 0; k < 9; k++) { const x = -900 + r() * 2900, y = ty - 40 - r() * 380; w += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(60 + r() * 140)}" ry="${f1(40 + r() * 90)}" fill="#5a5038" opacity=".2" filter="url(#skBlur10)"/>`; }
    w += `<rect x="-1400" y="${ty}" width="4000" height="${fy - ty}" fill="url(#ngwTile)"/>`;
    for (let x = -1400; x <= 2600; x += 64) w += `<path d="M${x},${ty}V${fy}" stroke="#4a7a62" stroke-width="3" opacity=".75"/>`;
    for (let y = ty; y <= fy; y += 64) w += `<path d="M-1400,${y}H2600" stroke="#4a7a62" stroke-width="3" opacity=".75"/>`;
    w += `<rect x="-1400" y="${ty - 16}" width="4000" height="16" fill="#5a8a72" stroke="${INK}" stroke-width="3"/>`;
    // the vent: 3×2 breeze blocks (the cross pattern), lit from behind by the storm (#id-vent flashes)
    const vx = o.ventX ?? 250, vy = 300; w += `<rect x="${vx - 10}" y="${vy - 10}" width="${3 * 90 + 20}" height="${2 * 90 + 20}" fill="#6a6250" ${OUT(4)}/>`;
    for (let i = 0; i < 3; i++) for (let j = 0; j < 2; j++) { const bx = vx + i * 90, by = vy + j * 90; w += `<rect x="${bx}" y="${by}" width="90" height="90" fill="#c8bfa8" stroke="${INK}" stroke-width="3"/><g class="${id}-hole">${[[16, 16], [52, 16], [16, 52], [52, 52]].map(([dx, dy]) => `<rect x="${bx + dx}" y="${by + dy}" width="22" height="22" rx="4" fill="#4a5a6a"/>`).join("")}</g>`; }
    w += `<g id="${id}-vent" opacity="0">${Array.from({ length: 6 }, (_, k) => { const bx = vx + (k % 3) * 90, by = vy + Math.floor(k / 3) * 90; return [[16, 16], [52, 16], [16, 52], [52, 52]].map(([dx, dy]) => `<rect x="${bx + dx}" y="${by + dy}" width="22" height="22" rx="4" fill="#eaf2ff"/>`).join(""); }).join("")}</g>`;
    // the door (right): planks, a bolt, light along its gap
    const dx = o.doorX ?? 760; w += `<g id="${id}-door"><rect x="${dx}" y="${fy - 900}" width="300" height="900" fill="#6a4a2e" ${OUT(6)}/>${[1, 2, 3, 4].map((k) => `<path d="M${dx + k * 60},${fy - 896}V${fy - 4}" stroke="#4a3220" stroke-width="4"/>`).join("")}
      <path d="M${dx + 20},${fy - 700}H${dx + 280}M${dx + 20},${fy - 260}H${dx + 280}" stroke="#4a3220" stroke-width="16"/><rect x="${dx + 30}" y="${fy - 470}" width="70" height="20" rx="4" fill="#9a9a9a" ${OUT(2.4)}/><circle cx="${dx + 104}" cy="${fy - 460}" r="9" fill="#9a9a9a" ${OUT(2)}/>
      <path d="M${dx - 4},${fy - 900}V${fy}" stroke="#d8e4f0" stroke-width="5" opacity=".5"/></g>`;
    // the robe on a line, the shelf with soap and a cup
    w += `<path d="M-200,${ty - 160}Q300,${ty - 120} 760,${ty - 170}" stroke="#d8d0b8" stroke-width="4" fill="none"/><g transform="translate(-400,-30)"><path d="M380,${ty - 136}Q370,${ty + 40} 400,${ty + 160}L560,${ty + 150}Q540,${ty + 20} 560,${ty - 142}Z" fill="${o.robeC || "#d8781e"}" ${OUT(4)}/>
      <path d="M420,${ty - 120}Q412,${ty + 40} 430,${ty + 140}M480,${ty - 130}Q474,${ty + 30} 490,${ty + 150}" stroke="${o.robeS || "#b85a14"}" stroke-width="5" fill="none"/></g>`;
    w += `<rect x="560" y="${ty + 120}" width="150" height="16" fill="#8a6a4a" ${OUT(3)}/><rect x="580" y="${ty + 92}" width="40" height="28" rx="6" fill="#e8e0d0" ${OUT(2.4)}/><path d="M650,${ty + 120}l8,-48h30l8,48Z" fill="#4a9ad0" ${OUT(2.4)}/><path d="M666,${ty + 74}l-6,-30" stroke="#e84a6a" stroke-width="5"/>`;
    // more of a family bathroom (owner 4 Nov: "ดีเท่าทะเลลดรึยัง"): a round mirror over the shelf, shampoo bottles, a towel rail with two
    // towels on the right wall (#id-tw sways in the draught), a calendar-free tile wall stays clean
    w += `<g transform="translate(635,${ty - 60})"><circle r="62" fill="#c8ccc4" ${OUT(5)}/><circle r="50" fill="#dfe8ea"/><path d="M-30,-14q20,-26 46,-24" stroke="#fff" stroke-width="7" fill="none" opacity=".8" stroke-linecap="round"/></g>`;
    w += `<path d="M700,${ty + 120}l6,-46h22l6,46Z" fill="#f0a8c8" ${OUT(2.4)}/><rect x="709" y="${ty + 62}" width="16" height="14" fill="#e8e4dc" ${OUT(1.8)}/><path d="M566,${ty + 120}l4,-36h18l4,36Z" fill="#7ac0a0" ${OUT(2.2)}/>`;
    w += `<path d="M1140,${ty + 140}H1480" stroke="#c8ccd0" stroke-width="12" stroke-linecap="round"/><path d="M1140,${ty + 140}H1480" stroke="#f4f6f8" stroke-width="4" stroke-linecap="round"/>
      <g id="${id}-tw"><path d="M1170,${ty + 140}Q1160,${ty + 300} 1176,${ty + 420}H1290Q1300,${ty + 300} 1290,${ty + 140}Z" fill="#f08aa8" ${OUT(3.4)}/><path d="M1180,${ty + 380}H1286M1180,${ty + 396}H1286" stroke="#fff" stroke-width="5"/>
      <path d="M1316,${ty + 140}Q1306,${ty + 260} 1320,${ty + 350}H1450Q1462,${ty + 260} 1450,${ty + 140}Z" fill="#f2d24a" ${OUT(3.4)}/><path d="M1326,${ty + 316}H1446" stroke="#fff" stroke-width="5"/></g>`;
    put(L.far, w);
    // the floor: wet tiles in perspective
    let f = `<rect x="-1400" y="${fy}" width="4000" height="1200" fill="#4a6a5a"/>`;
    for (let k = 1; k < 9; k++) { const y = fy + Math.pow(k / 9, 1.6) * 700; f += `<path d="M-1400,${f1(y)}H2600" stroke="#2e4a3e" stroke-width="${f1(2 + k * 0.6)}"/>`; }
    for (let k = -14; k <= 14; k++) f += `<path d="M${540 + k * 70},${fy}L${540 + k * 260},${fy + 900}" stroke="#2e4a3e" stroke-width="3"/>`;
    f += `<ellipse cx="540" cy="${fy + 220}" rx="520" ry="80" fill="#c8e0d4" opacity=".14" filter="url(#skBlur24)"/>`;
    put(L.mid, f);
    // the water tank (left) with the ขัน floating on it
    put(L.set, `<g><path d="M-260,${fy + 40}V${fy - 330}H140V${fy + 40}Z" fill="#8ab49c" ${OUT(6)}/>${[0, 1, 2, 3, 4].map((k) => `<path d="M-260,${fy - 330 + k * 74}H140" stroke="#4a7a62" stroke-width="3"/>`).join("")}${[-200, -120, -40, 40, 120].map((x) => `<path d="M${x},${fy - 330}V${fy + 40}" stroke="#4a7a62" stroke-width="3"/>`).join("")}
      <rect x="-276" y="${fy - 350}" width="432" height="26" fill="#6a9a80" ${OUT(4)}/><ellipse cx="-30" cy="${fy - 338}" rx="170" ry="9" fill="#2a4a5a"/>
      <g transform="translate(20,${fy - 352}) rotate(-8)"><path d="M-44,0Q-40,26 0,28Q40,26 44,0Z" fill="#f08a2a" ${OUT(3)}/><path d="M-46,0H46" stroke="${INK}" stroke-width="3"/><path d="M-30,6Q0,12 30,6" stroke="#ffc07a" stroke-width="4" fill="none"/></g>
      <path d="M-120,${fy - 420}V${fy - 380}H-90" stroke="#9a9a9a" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M-120,${fy - 420}V${fy - 380}H-90" stroke="#d8d8d8" stroke-width="4" fill="none"/></g>`);
    // a red bucket with a dipper and a blue plastic stool on the floor, a scrub brush against the wall
    put(L.set, `<g transform="translate(1300,${fy + 50})"><path d="M-90,0L-104,-150H104L90,0Z" fill="#d8382a" ${OUT(5)}/><path d="M-104,-150H104" stroke="#a82218" stroke-width="10"/><ellipse cy="-150" rx="104" ry="16" fill="#3a5a6a" ${OUT(3)}/>
        <path d="M-96,-150Q0,-260 96,-150" stroke="#d8d8d8" stroke-width="6" fill="none"/><g transform="translate(30,-166) rotate(-14)"><path d="M-40,0Q-36,24 0,26Q36,24 40,0Z" fill="#4a9ad0" ${OUT(2.6)}/><rect x="36" y="-6" width="70" height="12" rx="6" fill="#4a9ad0" ${OUT(2.2)}/></g></g>
      <g transform="translate(330,${fy + 40})"><path d="M-80,0L-64,-110H64L80,0" fill="none" stroke="#3a7ad8" stroke-width="16"/><rect x="-86" y="-130" width="172" height="26" rx="10" fill="#4a8ae8" ${OUT(3.4)}/><circle cy="-117" r="14" fill="#2a5aa8"/></g>
      <g transform="translate(1530,${fy + 10}) rotate(12)"><rect x="-8" y="-300" width="16" height="230" rx="6" fill="#c8a060" ${OUT(2.4)}/><rect x="-40" y="-80" width="80" height="60" rx="10" fill="#e8e4dc" ${OUT(2.8)}/><path d="M-34,-20V0M-20,-20V0M-6,-20V0M8,-20V0M22,-20V0M34,-20V0" stroke="#3a7a4a" stroke-width="5"/></g>`);
    // the bulb on its cord (swings from the ceiling), its glow
    put(L.set, `<g id="${id}-bulb"><path d="M540,-300V${o.bulbY ?? 240}" stroke="#1e1a16" stroke-width="5"/><rect x="526" y="${(o.bulbY ?? 240) - 6}" width="28" height="26" rx="3" fill="#3a3a3a"/><ellipse cx="540" cy="${(o.bulbY ?? 240) + 46}" rx="26" ry="32" fill="#fff4c8" stroke="${INK}" stroke-width="3"/></g>`);
    put(L.glow, `<g id="${id}-glow"><circle cx="540" cy="${(o.bulbY ?? 240) + 46}" r="760" fill="url(#ngwBulb)" opacity=".75"/><circle cx="540" cy="${(o.bulbY ?? 240) + 46}" r="120" fill="url(#ngwBulb)"/></g>`);
  };
  Ngw.kutiLife = (tl, id, t0, dur, flashes = []) => {
    tl.fromTo(`#${id}-bulb`, { rotation: -4, svgOrigin: "540 -300" }, { rotation: 4, svgOrigin: "540 -300", duration: 0.9, ease: "sine.inOut", yoyo: true, repeat: Math.ceil(dur / 0.9), immediateRender: false }, t0);
    tl.fromTo(`#${id}-glow`, { opacity: 1 }, { keyframes: [{ opacity: 0.55, duration: 0.06 }, { opacity: 1, duration: 0.1 }, { opacity: 0.8, duration: 0.5 }, { opacity: 0.4, duration: 0.05 }, { opacity: 1, duration: 0.12 }], repeat: Math.ceil(dur / 0.83), immediateRender: false }, t0);
    tl.fromTo(`#${id}-door`, { x: 0 }, { x: 5, duration: 0.07, ease: "none", yoyo: true, repeat: Math.ceil(dur / 0.07), immediateRender: false }, t0);
    tl.fromTo(`#${id}-tw`, { skewX: -1.5, svgOrigin: "1300 0" }, { skewX: 2, svgOrigin: "1300 0", duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: Math.ceil(dur / 0.6), immediateRender: false }, t0);
    flashes.forEach((t) => tl.fromTo(`#${id}-vent`, { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.05 }, { opacity: 0.2, duration: 0.08 }, { opacity: 0.8, duration: 0.05 }, { opacity: 0, duration: 0.3 }], immediateRender: false }, t0 + t));
  };
  // the legend on the shadow-puppet screen: the lake, the naga rising out of it as a twisting column into the cloud (eyes lit), the
  // villagers on the bank waiing it, a little house on the far bank. Ids: #id-naga #id-eyes #id-cloud #id-people
  Sets.ngwLegend = (L, o = {}) => {
    const id = o.id || "nl";
    Sets.legend3(L, { id, shirt: false });
    ["widow", "man"].forEach((p) => { const n = document.getElementById(`${id}-${p}`); if (n) n.setAttribute("opacity", "0"); });
    const clip = document.querySelector(`[clip-path="url(#${id}-clip)"]`), B = "#050404", Hs = "url(#mmScreen)";
    let g = `<rect id="${id}-dim" x="0" y="0" width="1080" height="1920" fill="#000" opacity="0"/>`;
    // the cloud band at the top, punched swirls
    g += `<g id="${id}-cloud"><path d="M60,250H1020V360Q960,420 900,380Q840,440 760,392Q690,450 610,400Q540,470 460,404Q380,450 310,396Q230,446 170,390Q110,420 60,380Z" fill="${B}"/>
      ${[[200, 330], [420, 350], [640, 345], [860, 330]].map(([x, y]) => `<path d="M${x - 40},${y}q20,-26 46,-8q22,16 0,30q-14,8 -22,-4" stroke="${Hs}" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
    // the naga: a column twisting up out of the lake into the cloud, the scales punched as rows of crescents; the head breaking out of
    // the cloud, crest flames, mouth open, eyes lit
    const pts = []; for (let k = 0; k <= 20; k++) { const t = k / 20; pts.push([540 + 90 * Math.sin(t * Math.PI * 2.2) * (1 - t * 0.5), 1230 - t * 640]); }
    const wv = (t) => 84 - 40 * t;
    const Lp = pts.map(([x, y], k) => [x - wv(k / 20), y]), Rp = pts.map(([x, y], k) => [x + wv(k / 20), y]).reverse();
    let sc = ""; pts.forEach(([x, y], k) => { if (k % 2 || k > 18) return; const w = wv(k / 20); sc += `<path d="M${f1(x - w * 0.7)},${f1(y)}q${f1(w * 0.7)},${f1(-w * 0.45)} ${f1(w * 1.4)},0" stroke="${Hs}" stroke-width="5" fill="none"/>`; });
    g += `<g id="${id}-naga"><path d="${smooth(Lp.concat(Rp), true)}" fill="${B}"/>${sc}
      <g transform="translate(${f1(pts[20][0])},${f1(pts[20][1] + 6)}) scale(1.7)"><path d="M-40,20Q-60,-40 -20,-90Q10,-120 40,-110Q24,-90 50,-74Q24,-60 46,-40Q20,-30 36,0Z" fill="${B}"/>
        <path d="M-10,-20Q-60,-50 -120,-40Q-140,-34 -136,-18L-110,-10Q-126,4 -108,14Q-60,26 -10,20Z" fill="${B}"/>
        <path d="M-118,-8l6,12l6,-11M-90,-4l5,11l5,-10" fill="${Hs}"/>
        <g id="${id}-eyes"><ellipse cx="-64" cy="-28" rx="9" ry="6" fill="#ffd25a"/><circle cx="-64" cy="-28" r="36" fill="#ffb84a" opacity=".5" filter="url(#tkGhostGlow2)"/></g></g></g>`;
    // the lake: a black band with scalloped crests and punched wave lines; the bank (left) with the people waiing; a house far right
    g += `<path d="M60,1230Q120,1200 180,1230T300,1230T420,1230T540,1230T660,1230T780,1230T900,1230T1020,1230V1400H60Z" fill="${B}"/>`;
    g += [1270, 1310, 1350].map((y, k) => `<path d="M${100 + k * 30},${y}q30,-12 60,0t60,0M${420 + k * 40},${y}q30,-12 60,0t60,0M${760 - k * 20},${y}q30,-12 60,0t60,0" stroke="${Hs}" stroke-width="5" fill="none"/>`).join("");
    g += `<path d="M60,1200Q160,1170 300,1196L330,1240H60Z" fill="${B}"/>`;
    g += `<g>${[-1, 1].map((sd) => [0, 1, 2].map((k) => `<path d="M${540 + sd * (40 + k * 30)},1230q${sd * (40 + k * 20)},${-60 - k * 30} ${sd * (110 + k * 40)},${-20 - k * 10}l${sd * 10},18q${-sd * 50},${-30 + k * 6} ${-sd * (110 + k * 40)},${10 + k * 10}Z" fill="${B}"/>`).join("")).join("")}
      ${Array.from({ length: 14 }, (_, k) => `<circle cx="${f1(400 + k * 21 + (k % 3) * 6)}" cy="${f1(1120 - (k % 4) * 26 - (k % 5) * 8)}" r="${4 + (k % 3) * 2}" fill="${B}"/>`).join("")}</g>`;
    g += `<g id="${id}-people">${[[110, 1.0], [170, 0.9], [230, 0.95]].map(([x, s]) => `<g transform="translate(${x},1196) scale(${s})"><path d="M-30,0Q-34,-26 -16,-52L12,-56Q20,-30 30,0Z" fill="${B}"/><circle cx="8" cy="-74" r="17" fill="${B}"/><path d="M10,-48L32,-58L30,-80" stroke="${B}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/></g>`).join("")}</g>`;
    g += `<g transform="translate(900,1222)"><path d="M-50,0V-50H50V0Z" fill="${B}"/><path d="M-66,-48L0,-100L66,-48Z" fill="${B}"/><rect x="-14" y="-36" width="28" height="36" fill="${Hs}"/></g>`;
    clip.insertAdjacentHTML("beforeend", `<defs><filter id="tkGhostGlow2" x="-2" y="-2" width="5" height="5"><feGaussianBlur stdDeviation="10"/></filter></defs>` + g);
  };
  // the ditch beside the paddy, low camera: the far bank, the muddy water, the near bank in the foreground (L.fg) over the actor's legs
  Ngw.ditch = (o = {}) => {
    const y0 = o.y ?? 1420, nb = o.near ?? 150, r = mk(o.seed || 31);   // o.near: how far below the waterline the near bank (fg) starts
    const edge = (y, amp, ph) => { let d = ""; for (let x = -1400; x <= 2600; x += 50) d += `${x === -1400 ? "M" : "L"}${x},${f1(y + amp * Math.sin(x * 0.007 + ph) + amp * 0.4 * Math.sin(x * 0.019 + ph))}`; return d; };
    let s = `<path d="${edge(y0 - 90, 10, 1)}V${y0 + 30}H-1400Z" fill="#4a3e2a"/><path d="${edge(y0 - 90, 10, 1)}" stroke="#2c3a22" stroke-width="10" fill="none"/>`;
    let gr = ""; for (let x = -1400; x < 2600; x += 8 + r() * 9) { const y = y0 - 92 + 10 * Math.sin(x * 0.007 + 1), h = 20 + r() * 40, l = 10 + r() * 20; gr += `M${f1(x)},${f1(y)}q${f1(l * 0.4)},${f1(-h * 0.6)} ${f1(l)},${f1(-h)}`; }
    s += `<path d="${gr}" stroke="#3e5a2e" stroke-width="3.4" fill="none" stroke-linecap="round"/>`;
    s += `<path d="${edge(y0 - 30, 8, 1.5)}V${y0 + 4}H-1400Z" fill="#6a5638"/>`;
    s += `<path d="${edge(y0, 6, 2)}V${y0 + 260}H-1400Z" fill="#262c2a"/><path d="${edge(y0 + 18, 6, 2)}" stroke="#8a9a98" stroke-width="10" fill="none" opacity=".25"/><path d="${edge(y0, 6, 2)}" stroke="#a8b8b6" stroke-width="4" fill="none" opacity=".55"/>`;
    for (let k = 0; k < 40; k++) { const x = -1300 + r() * 3700, y = y0 + 10 + r() * 140; s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(8 + r() * 22)}" ry="${f1(2 + r() * 4)}" fill="none" stroke="#9aaab0" stroke-width="2" opacity=".4"/>`; }
    let fg = `<path d="${edge(y0 + nb, 18, 3)}V2600H-1400Z" fill="#2e2a1e"/>`, g2 = "";
    for (let x = -1400; x < 2600; x += 10 + r() * 12) { const y = y0 + nb + 18 * Math.sin(x * 0.007 + 3), h = 40 + r() * 90, l = 16 + r() * 30; g2 += `M${f1(x)},${f1(y + 6)}q${f1(l * 0.4)},${f1(-h * 0.6)} ${f1(l)},${f1(-h)}`; }
    fg += `<path d="${g2}" stroke="#2a3e22" stroke-width="7" fill="none" stroke-linecap="round"/>`;
    return { set: s, fg };
  };
  // ---------------------------------------------------------------- the world: Sets.tkScape storm + the lake / spouts / bank / shrine
  // QA ("one house design repeated"): five looks for the village — wall and roof colours, and one thing each house owns: water jars,
  // a laundry line, a banana clump, a zinc porch, a mango tree (drawn in the house's own coordinates, so they scale with it)
  Ngw.houseV = (x, y, s, o = {}) => { const k = ((o.k ?? 0) % 5 + 5) % 5, I = "#1e1a16";
    const P = [["#d8c4a0", "#a8442e", "#5a2a1e"], ["#ece4cc", "#3a6a8a", "#24445a"], ["#c8d8c0", "#8a4a2e", "#4a2a1a"], ["#e8d0b0", "#5a7a4a", "#2e4a26"], ["#b08454", "#8a8e8c", "#4a4e4c"]][k];
    let g = Tk.house(x, y, s, o).replace(/#d8c4a0/g, P[0]).replace(/#a8442e/g, P[1]).replace(/#5a2a1e/g, P[2]);
    const ex = [
      `<g transform="translate(-520,0)">${[0, 120].map((dx) => `<ellipse cx="${dx}" cy="-70" rx="58" ry="72" fill="#5a3422" stroke="${I}" stroke-width="5"/><ellipse cx="${dx}" cy="-138" rx="40" ry="10" fill="#3a2418" stroke="${I}" stroke-width="4"/><path d="M${dx - 40},-90q40,-14 80,0" stroke="#e8c070" stroke-width="5" fill="none"/>`).join("")}</g>`,
      `<path d="M640,0V-300M1000,0V-300M640,-280Q820,-250 1000,-280" stroke="${I}" stroke-width="6" fill="none"/>${[[690, "#e85a4a"], [770, "#4a8ae0"], [850, "#f2c230"], [925, "#f4f0e8"]].map(([cx, c]) => `<path d="M${cx - 30},-266h60v90l-30,14l-30,-14Z" fill="${c}" stroke="${I}" stroke-width="4"/>`).join("")}`,
      `<g transform="translate(-560,0)"><path d="M0,0V-360" stroke="#5a7a3a" stroke-width="26"/>${[[-1, -340], [1, -320], [-1, -260], [1, -230]].map(([d, yy]) => `<path d="M0,${yy}q${d * 120},-90 ${d * 230},-10q${d * -110},-20 ${d * -230},10Z" fill="#5a9a40" stroke="${I}" stroke-width="4"/>`).join("")}</g>`,
      `<path d="M-160,-300L220,-300L260,-250H-200Z" fill="#a8b0b0" stroke="${I}" stroke-width="5"/>${[-150, 0, 150, 250].map((px) => `<path d="M${px},-250V0" stroke="#6a5a44" stroke-width="10"/>`).join("")}`,
      `<g transform="translate(720,0)"><path d="M0,0V-260" stroke="#5a3a22" stroke-width="30"/><circle cx="-60" cy="-330" r="120" fill="#3e6a32" stroke="${I}" stroke-width="5"/><circle cx="70" cy="-360" r="130" fill="#4a7a3a" stroke="${I}" stroke-width="5"/><circle cx="10" cy="-450" r="110" fill="#558a42" stroke="${I}" stroke-width="5"/></g>`][k];
    const i = g.lastIndexOf("</g>"); return g.slice(0, i) + ex + g.slice(i); };
  // a towering storm cloud far off on the horizon (the hot afternoon's cumulonimbus): a cauliflower column lit from the sun's side, an anvil
  // sheared to the right at the top, the dark base and (o.dark) a rain shaft under it; o.h grows shot by shot (QA: the old flat cloud read as a hill)
  Ngw.cbTower = (o = {}) => { const x = o.x ?? 1350, hz = o.hz ?? 1160, h = o.h ?? 420, w = o.w ?? h * 0.62, d = o.dark ?? 0, r = mk(o.seed || 23), id = o.id || "cbt";
    const mix = (a, b, t) => "#" + [0, 2, 4].map((j) => Math.round(parseInt(a.substr(1 + j, 2), 16) * (1 - t) + parseInt(b.substr(1 + j, 2), 16) * t).toString(16).padStart(2, "0")).join("");
    const LIT = mix("#fff8ec", "#c8ccd4", d * 0.6), MID = mix("#dcdee4", "#7a8494", d), SH = mix("#9aa4b4", "#3a4452", d), BASE = mix("#6a7686", "#262e38", d);
    let g = `<g id="${id}">`;
    if (d > 0.2) g += `<path d="M${x - w * 0.42},${hz - 40}L${x - w * 0.52},${hz + 4}H${x + w * 0.38}L${x + w * 0.3},${hz - 40}Z" fill="${BASE}" opacity="${f1(0.3 + d * 0.4)}" filter="url(#skBlur10)"/>`;
    // the column: many overlapping lobes of different sizes, jittered, wider and brighter toward the top; three passes (shade, body, sunlit
    // tops) so lobes merge into one mass instead of a stack of balls; the whole tower softened with a light blur
    const N = 16, L0 = []; for (let i = 0; i < N; i++) { const u = i / (N - 1), yy = hz - 60 - u * h * 0.8, rw = w * (0.3 + 0.16 * u) * (0.85 + r() * 0.3);
      for (let j = 0; j < 3; j++) L0.push([x + (r() - 0.5) * rw * 1.1 + u * w * 0.1, yy + (r() - 0.5) * h * 0.05, rw * (0.34 + r() * 0.26)]); }
    let lobes = L0.map(([cx, cy, R]) => `<circle cx="${f1(cx + R * 0.18)}" cy="${f1(cy + R * 0.22)}" r="${f1(R)}" fill="${SH}"/>`).join("")
      + L0.map(([cx, cy, R]) => `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(R * 0.9)}" fill="${MID}"/>`).join("")
      + L0.map(([cx, cy, R]) => `<circle cx="${f1(cx - R * 0.3)}" cy="${f1(cy - R * 0.34)}" r="${f1(R * 0.5)}" fill="${LIT}" opacity=".85"/>`).join("");
    const top = hz - 50 - h * 0.86, aw = w * 2.3;   // the anvil: wide, flat, sheared downwind
    g += `<path d="M${f1(x - aw * 0.32)},${f1(top + 30)}Q${f1(x - aw * 0.2)},${f1(top - 60)} ${f1(x + aw * 0.1)},${f1(top - 50)}Q${f1(x + aw * 0.5)},${f1(top - 46)} ${f1(x + aw * 0.78)},${f1(top + 6)}Q${f1(x + aw * 0.46)},${f1(top + 30)} ${f1(x + aw * 0.12)},${f1(top + 50)}Z" fill="${MID}"/><path d="M${f1(x - aw * 0.3)},${f1(top + 20)}Q${f1(x - aw * 0.18)},${f1(top - 58)} ${f1(x + aw * 0.1)},${f1(top - 48)}Q${f1(x + aw * 0.5)},${f1(top - 44)} ${f1(x + aw * 0.76)},${f1(top + 4)}" stroke="${LIT}" stroke-width="16" fill="none" stroke-linecap="round"/>`;
    g += `<g filter="url(#skBlur4)">${lobes}</g><path d="M${f1(x - w * 0.5)},${hz - 50}Q${x},${hz - 74} ${f1(x + w * 0.5)},${hz - 50}L${f1(x + w * 0.46)},${hz - 30}H${f1(x - w * 0.46)}Z" fill="${BASE}" filter="url(#skBlur4)"/>`;
    if (d > 0.3) g += `${[0, 1, 2, 3].map((k) => `<path d="M${f1(x - w * 0.3 + k * w * 0.16)},${hz - 34}l-26,${f1(40 + d * 30)}" stroke="${BASE}" stroke-width="10" opacity="${f1(0.25 + d * 0.3)}"/>`).join("")}`;
    return g + `</g>`; };
  Sets.ngwScape = function (L, o = {}) {
    Sets.tkScape(L, { ...o, fgRice: o.lake ? false : o.fgRice });
    const hz = o.horizon ?? 1000;
    // before the storm (QA: "a rainbow on the hottest day, one hour before"): no rainbow, a sun-bleached haze on the horizon, the growing tower
    if (o.noRainbow) [...L.sky.querySelectorAll("g")].forEach((g) => { if (g.querySelector('path[stroke="#ff5a5a"]')) g.remove(); });
    if (o.haze) put(L.sky, `<rect x="-1400" y="${hz - 340}" width="4000" height="360" fill="#fff2d8" opacity=".32" filter="url(#skBlur24)"/>`);
    if (o.tower) put(L.sky, Ngw.cbTower({ hz, ...o.tower }));
    if (o.lake) { put(L.mid, Ngw.lake({ hz, ...o.lake })); put(L.mid, `<rect x="-1400" y="${hz - 110}" width="4000" height="210" fill="#8a9aa0" opacity=".16" filter="url(#skBlur24)"/>`); }
    (o.spouts || []).forEach((sp) => put(L[sp.layer || "mid"], Ngw.funnel(sp)));
    if (o.monster) put(L[o.monster.layer || "mid"], Ngw.monster(o.monster));
    if (o.epic) { const e = Ngw.epic({ ...o.epic, y: o.epic.y ?? hz + 6 }); put(L.sky, e.sky); put(L.mid, e.mid); }
    if (o.lake && o.bank !== false) put(L.set, Ngw.bank({ y1: o.lake.y1, ...(o.bankOpts || {}) }));
    if (o.crowd) put(L.set, Ngw.crowd(o.crowd));
    if (o.shrine) put(L.set, Rup2.shrine(o.shrine.x, o.shrine.y, o.shrine.s || 1));
    if (o.naga) put(L.set, Ngw.naga(o.naga.x, o.naga.y, o.naga.s || 1, o.naga));
    if (o.farLake) { const [a, b] = o.farLake; put(L.mid, `<path d="M${a},${hz}H${b}L${b - 160},${hz + 34}H${a}Z" fill="url(#ngwLake)"/><path d="M${a},${hz + 1}H${b}" stroke="#b4c6c8" stroke-width="3" opacity=".6"/>`); }
    if (o.village) put(L.mid, o.village.map((v, i) => v.kind === "wat" ? Ngw.wat(v.x, v.y, v.s) : v.kind === "school" ? Ngw.school(v.x, v.y, v.s) : Ngw.houseV(v.x, v.y, v.s, { ...v, k: v.k ?? i })).join(""));
    if (o.ditch) { const d = Ngw.ditch(o.ditch); put(L.set, d.set); put(L.fg, d.fg); }
    if (o.far) put(L.mid, typeof o.far === "function" ? o.far() : o.far);
    if (o.road) put(L.set, Ngw.road(o.road));
    if (o.roadTitle) put(L.set, Ngw.roadTitle(o.roadTitle));
    if (o.ruins) { const PAL = [["#d8c4a0", "#a8442e"], ["#ece4cc", "#3a6a8a"], ["#c8d8c0", "#8a4a2e"], ["#e8d0b0", "#5a7a4a"], ["#b08454", "#8a8e8c"]];
      put(L[o.ruinsLayer || "mid"], o.ruins.map((v, i) => { const P = PAL[(v.k ?? i + 1) % 5]; return Ngw.ruin(v.x, v.y, v.s, v).replace(/#d8c4a0/g, P[0]).replace(/#a8442e/g, P[1]); }).join("")); }
    if (o.overpass) { const ov = Ngw.overpass(o.overpass); put(L.set, ov.set); put(L.fg, ov.fg); }
    if (o.poles) { const { xs, y = 1540, s: ps = 1, tf = [] } = o.poles; put(L.set, xs.map((x, k) => Ngw.pole(x, y, ps, { tf: tf.includes(k), lean: (o.poles.lean || [])[k] || 0 })).join("") + Ngw.wires(xs, y, ps, o.poles.sag ?? 40)); }
    if (o.props) put(L.set, typeof o.props === "function" ? o.props() : o.props);
    if (o.fgProps) put(L.fg, typeof o.fgProps === "function" ? o.fgProps() : o.fgProps);
    if (o.glowProps) put(L.glow, typeof o.glowProps === "function" ? o.glowProps() : o.glowProps);   // in front of the actors, sharp (fg is depth-blurred)
  };

  // ---------------------------------------------------------------- cast
  const { LINE } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const base = (k) => (C[k] && C[k].v2) || {};
  // ฝน (16): high ponytail with a yellow scrunchie, side-swept fringe, a yellow raincoat over a white tee, denim shorts, sneakers
  const fonFront = (h) => `<path d="M-54,-534C-66,-604 -30,-640 6,-640C44,-640 66,-606 58,-536Q54,-570 40,-584Q20,-574 0,-592Q-16,-566 -40,-570Q-50,-556 -54,-534Z" fill="${h.c}" ${ln()}/>
    <path d="M-40,-570Q-20,-596 4,-614M0,-592Q24,-610 44,-596" stroke="${h.sh}" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>`;
  const fonTail = (h) => `<path d="M24,-630Q84,-660 104,-596Q120,-530 90,-454Q88,-520 70,-560Q52,-600 24,-610Z" fill="${h.c}" ${ln()}/><path d="M64,-610Q92,-570 90,-500" stroke="${h.sh}" stroke-width="4" fill="none" opacity=".5"/>
    <ellipse cx="34" cy="-628" rx="13" ry="10" fill="#f2c230" ${ln(2)}/>`;
  C.fon = { v2: { ...base("june"), hair: { c: "#1e1410", s: "#0a0604", sh: "#6a5446", front: (x) => fonFront(x.hair), back: (x) => fonTail(x.hair) },
    top: { kind: "coat", c: "#f2be2a", sleeve: "long" }, print: `<path d="M-14,-490L0,-440L14,-490" fill="#f6f4ee" stroke="${LINE}" stroke-width="2"/>`,
    bottom: { kind: "shorts", c: "#4a6a9a" }, feet: { kind: "sneaker", c: "#f2f0ea" }, wristband: "#ff5a8a", face: "" } };
  const phone = `<g transform="translate(0,118) rotate(-10)"><rect x="-14" y="-28" width="28" height="48" rx="5" fill="#26262e" ${ln(2)}/><rect x="-11" y="-24" width="22" height="38" rx="2" fill="#bfe8ff"/><circle cx="-5" cy="-18" r="3" fill="#ff3a4a"/></g>`;
  C.fonPhone = { ...C.fon, hand: phone, keep: "F" };
  // ปู (9): green bucket hat, red-and-white striped tee, a little camera on a strap, khaki shorts, blue sandals
  const hat = `<g><path d="M-48,-588Q-46,-646 2,-650Q50,-646 52,-588Z" fill="#4a8a5a" ${ln()}/><path d="M-70,-584Q0,-604 72,-584L80,-566Q0,-584 -78,-566Z" fill="#3a7a4a" ${ln()}/>
    <path d="M-40,-604Q2,-616 44,-604" stroke="#2e6a3e" stroke-width="4" fill="none"/><path d="M-30,-636Q-4,-646 20,-640" stroke="#7ab88a" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/></g>`;
  const stripes = `<g>${[-470, -440, -410, -380, -350].map((y) => `<path d="M-50,${y}Q0,${y + 6} 50,${y}" stroke="#f6f2ea" stroke-width="12" fill="none"/>`).join("")}</g>
    <path d="M-34,-490L0,-414L34,-490" stroke="#2a2a2a" stroke-width="4" fill="none"/><rect x="-22" y="-426" width="44" height="30" rx="5" fill="#2e2e34" ${ln(2)}/><circle cx="4" cy="-411" r="10" fill="#4a5a6a" stroke="#111" stroke-width="2"/><circle cx="4" cy="-411" r="4" fill="#9ad0ff"/>`;
  C.pu = { v2: { ...base("tang"), top: { kind: "tee", c: "#d8382a", sleeve: "short" }, print: stripes, bottom: { kind: "shorts", c: "#b8a070" }, feet: { kind: "sandal", c: "#3a6ad0" }, faceTop: hat, face: "" } };
  // ปู after he left his camera in ตาเทียน's truck bed (the ending): the stripes without the strap and the camera
  C.puNoCam = { v2: { ...C.pu.v2, print: stripes.replace(/<path d="M-34,-490L0,-414L34,-490"[\s\S]*$/, "") } };
  const camera = `<g transform="translate(0,116)"><rect x="-22" y="-16" width="44" height="30" rx="5" fill="#2e2e34" ${ln(2)}/><circle cx="6" cy="-1" r="10" fill="#4a5a6a" stroke="#111" stroke-width="2"/><circle cx="6" cy="-1" r="4" fill="#9ad0ff"/><rect x="-18" y="-22" width="12" height="6" rx="2" fill="#2e2e34"/></g>`;
  C.puCam = { ...C.pu, hand: camera, keep: "F" };
  // ยายบัว: grey bun, pale lotus-pink lace blouse with small lotus prints, dark green sarong, no apron
  const lotus = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M0,0Q-10,-8 -4,-16Q0,-10 0,-18Q0,-10 4,-16Q10,-8 0,0Z" fill="#e86a90"/><path d="M-8,2h16" stroke="#3e7a4a" stroke-width="2.4"/></g>`;
  C.yaiBua = { v2: { ...base("yaiTide"), top: { kind: "blouse", c: "#f2dce2", sleeve: "elbow", lace: true, trim: "#d8a8b8" },
    print: `<g>${[[-34, -446], [24, -424], [-10, -384], [38, -350], [-40, -336]].map(([x, y]) => lotus(x, y, 1.2)).join("")}</g>`,
    bottom: { kind: "sarong", c: "#2e5a3e", band: "#1e4a2e", band2: "#1e4a2e" }, skirt: null, extra: "" } };
  // ตาเทียน: ex-headman — white hair, white moustache, khaki short-sleeve shirt with shoulder straps and a pen, an old red-check
  // ผ้าขาวม้า over the shoulder (the clue: a name stitched in its corner), dark trousers
  const tash = `<path d="M-26,-522Q-12,-532 4,-524Q20,-532 34,-522Q22,-512 4,-518Q-12,-512 -26,-522Z" fill="#f2f0ea" ${ln(1.6)}/>`;
  const khaki = `<path d="M-62,-486L-30,-492L-28,-478L-60,-472Z" fill="#8e7a4c" ${ln(2)}/><path d="M62,-486L30,-492L28,-478L60,-472Z" fill="#8e7a4c" ${ln(2)}/>
    <rect x="16" y="-452" width="30" height="34" rx="3" fill="#a08c5c" ${ln(1.8)}/><path d="M22,-458v20" stroke="#2a4aa8" stroke-width="4" stroke-linecap="round"/>`;
  const cloth = `<g><path d="M-46,-492Q0,-466 46,-492L50,-476Q0,-446 -50,-476Z" fill="#c8483a" ${ln(2.2)}/><path d="M-42,-486Q0,-462 44,-486M-46,-480Q0,-456 48,-480" stroke="#f2e6d8" stroke-width="2.4" fill="none" stroke-dasharray="6 6"/>
    <path d="M32,-486Q44,-440 38,-392L58,-392Q62,-442 50,-488Z" fill="#c8483a" ${ln(2.2)}/><path d="M38,-470h16M38,-450h18M40,-430h18M40,-410h18" stroke="#f2e6d8" stroke-width="2.4" stroke-dasharray="5 5"/>
    <path d="M38,-392h20" stroke="#f2e6d8" stroke-width="3" stroke-dasharray="3 3"/></g>`;
  C.taTian = { v2: { ...base("taJun"), brow: "#f2f0ea", top: { kind: "shirt", c: "#b09a68", sleeve: "short", neck: "collar", collar: "#9a8656", button: "#e8dcc0" }, print: khaki,
    bottom: { kind: "jeans", c: "#34363e" }, feet: { kind: "sandal", c: "#5a3a22" }, legs: undefined, extra: cloth, face: (base("taJun").face || "") + tash } };
  C.taTianWai = C.taTian;
  const tears = `<g><path d="M-29,-537q12,6 24,0M7,-537q12,6 24,0" stroke="#bfe6f2" stroke-width="3.4" fill="none" opacity=".95"/>
    <path d="M-25,-533c-4,9 -5,15 0,19c5,-4 4,-10 0,-19z" fill="#d4f0fa" stroke="${INK}" stroke-width="1.6"/><path d="M26,-531c-3,8 -4,13 0,16c4,-3 3,-8 0,-16z" fill="#d4f0fa" stroke="${INK}" stroke-width="1.6"/>
    <circle cx="-26" cy="-524" r="1.8" fill="#fff"/><circle cx="25" cy="-523" r="1.5" fill="#fff"/></g>`;
  C.taTianCry = { v2: { ...C.taTian.v2, face: C.taTian.v2.face + tears } };
  C.yaiBuaCry = { v2: { ...C.yaiBua.v2, face: (C.yaiBua.v2.face || "") + tears } };
})();
