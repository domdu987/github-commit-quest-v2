// Landscape (16:9, 1920×1080) layout of a vertical (1080×1920) episode — the YouTube long cut
// (owner 4 Nov 2569: "คลิปสั้น ig Facebook · คลิปยาว YouTube" → "แนวนอน 16:9").
// Load after engine.js and set window.LANDSCAPE = {} before Engine.build runs. Nothing in the episode changes: every clip the
// engine built is re-laid out for a 1920×1080 page:
//   .vf   the whole vertical frame (stage SVG + speech bubbles + SFX words), scaled 0.8 and slid up so the band of the frame where
//         the action is fills the page; the stage SVG is widened to x −660…1740 so the world goes on past the old left/right edges
//   .vui  game UI and HTML cards, fitted to the page height (scale .5625) in the centre column, never cut
//   captions stay where the vertical layout had them, mapped like the fitted UI (top × .5625), so source chips under them stay clear
//   L.light (screen-space SVG cards: rule cards, chips, end cards) is fitted into the visible band the same way; full-frame washes in
//   it are kept full width
// Per shot (optional): sh.land = { y0 }  top of the band in vertical px (0…570), or { fit: true } the whole vertical frame centred
// (used automatically when the set does not reach past the old frame, e.g. puppet screens, maps, notebooks).
(() => {
  const LS = window.LANDSCAPE;
  if (!LS || !window.Engine) return;
  const SC = 0.8, BAND = 1080 / SC, EXTRA = 660, FIT = 1080 / 1920; // band = 1350 vertical px; 660 × 0.8 = 528 px each side
  const build0 = Engine.build;

  const rectIn = (el, svg, vb) => { // an element's box in the stage's viewBox units (via client rects; the stage maps linearly)
    const r = el.getBoundingClientRect(), s = svg.getBoundingClientRect();
    if (!r.width && !r.height) return null;
    const kx = vb[2] / s.width, ky = vb[3] / s.height;
    return [vb[0] + (r.left - s.left) * kx, vb[1] + (r.top - s.top) * ky, vb[0] + (r.right - s.left) * kx, vb[1] + (r.bottom - s.top) * ky];
  };
  const union = (bs) => bs.filter(Boolean).reduce((u, b) => (u ? [Math.min(u[0], b[0]), Math.min(u[1], b[1]), Math.max(u[2], b[2]), Math.max(u[3], b[3])] : b), null);

  function reflow(clip, sh) {
    const id = clip.id, svg = clip.querySelector("svg.stage");
    if (!svg) return;
    const vb = [-EXTRA, 0, 1080 + 2 * EXTRA, 1920];
    // the stage, widened
    svg.setAttribute("width", vb[2]); svg.setAttribute("height", vb[3]); svg.setAttribute("viewBox", vb.join(" "));
    Object.assign(svg.style, { position: "absolute", left: `${-EXTRA}px`, top: "0px", right: "auto", bottom: "auto", width: `${vb[2]}px`, height: `${vb[3]}px` });
    // screen-space washes cover the wider stage
    [["dark", -EXTRA, vb[2]], ["fog", -EXTRA - 200, vb[2] + 400], ["grade", -EXTRA, vb[2]], ["vig", -EXTRA, vb[2]], ["grain", -EXTRA - 256, vb[2] + 512]].forEach(([k, x, w]) => {
      const r = document.getElementById(`${id}-${k}`); if (r) { r.setAttribute("x", x); r.setAttribute("width", w); } });
    // containers
    const vf = document.createElement("div"); vf.className = "vf";
    Object.assign(vf.style, { position: "absolute", left: "0px", top: "0px", width: "1080px", height: "1920px", transformOrigin: "0 0", overflow: "visible" });
    const vui = document.createElement("div"); vui.className = "vui";
    Object.assign(vui.style, { position: "absolute", left: "0px", top: "0px", width: "1080px", height: "1920px", transformOrigin: "0 0", pointerEvents: "none",
      transform: `translate(${(1920 - 1080 * FIT) / 2}px, 0px) scale(${FIT})` });
    // captions keep their place relative to the vertical layout (above source chips and HUD), mapped like the fitted UI
    const cw = clip.querySelector(".capwrap");
    if (cw) { const top = parseFloat(getComputedStyle(cw).top) || 1630; cw.style.top = `${Math.min(1000, top * FIT).toFixed(0)}px`; }
    const kids = [...clip.children];
    clip.appendChild(vf); clip.appendChild(vui);
    kids.forEach((n) => {
      if (n === svg || n.classList.contains("bubble") || n.classList.contains("sfxw")) vf.appendChild(n);
      else if (n.classList.contains("capwrap") || n.classList.contains("pagepos")) clip.appendChild(n); // stays on top, page-positioned (.pagepos: opt-in for UI drawn in page pixels)
      else vui.appendChild(n);
    });
    clip.appendChild(clip.querySelector(".capwrap") || document.createElement("i"));
    // measure with a neutral placement: the whole frame at scale .8, top at 0
    vf.style.transform = `translate(${(1920 - 1080 * SC) / 2}px, 0px) scale(${SC})`;
    const L = (k) => document.getElementById(`${id}-${k}`);
    const world = union(["sky", "far", "mid", "set"].map((k) => L(k) && rectIn(L(k), svg, vb)));
    const acts = union([...(L("act") ? L("act").children : [])].map((a) => rectIn(a, svg, vb)));
    const o = sh.land || {};
    const fit = o.fit ?? (!world || (world[0] > -160 && world[2] < 1240));
    let y0;
    if (fit) {
      vf.style.transform = `translate(${(1920 - 1080 * FIT) / 2}px, 0px) scale(${FIT})`;
      clip.classList.add("lfit");
    } else {
      if (o.y0 != null) y0 = o.y0;
      else if (acts && acts[3] > acts[1]) {
        const top = Math.max(0, acts[1]), bot = Math.min(1920, acts[3]);
        y0 = bot - top <= BAND - 260 ? Math.max(top - 110, bot - (BAND - 190)) : top - 70; // feet clear of the captions; else keep the heads
      } else y0 = (1920 - BAND) / 2;
      y0 = Math.max(0, Math.min(1920 - BAND, y0));
      vf.style.transform = `translate(${(1920 - 1080 * SC) / 2}px, ${-y0 * SC}px) scale(${SC})`;
      // screen-space SVG cards fitted into the visible band; full-frame washes stay full width
      const light = L("light");
      if (light) {
        const wide = document.createElementNS("http://www.w3.org/2000/svg", "g"); wide.setAttribute("id", `${id}-lightwide`);
        light.parentNode.insertBefore(wide, light);
        [...light.children].forEach((n) => { const b = rectIn(n, svg, vb); if (b && b[2] - b[0] >= 1000 && b[3] - b[1] >= 1700) wide.appendChild(n); });
        // a wash drawn for the old 1080 width (dim behind a choice, a gradient under the live comments) is stretched to the new width
        const widen = (r) => { const w = +r.getAttribute("width"); if (w >= 1000 && !/%/.test(r.getAttribute("width") || "")) { const x = +(r.getAttribute("x") || 0); r.setAttribute("x", x - EXTRA); r.setAttribute("width", w + 2 * EXTRA); } };
        [...wide.querySelectorAll("rect")].concat(wide.tagName === "rect" ? [wide] : []).forEach(widen);
        [...light.querySelectorAll("rect")].forEach((r) => { const w = +r.getAttribute("width"); if (w >= 1000) { const k = BAND / 1920, x = +(r.getAttribute("x") || 0);
          // inside the fitted group: stretch so it still reaches the page edges after the group's scale
          const L0 = 540 - (540 + EXTRA) / k, L1 = 540 + (540 + EXTRA) / k; r.setAttribute("x", Math.min(x, L0).toFixed(1)); r.setAttribute("width", (Math.max(x + w, L1) - Math.min(x, L0)).toFixed(1)); } });
        const k = BAND / 1920;
        light.setAttribute("transform", `translate(540 ${y0.toFixed(1)}) scale(${k.toFixed(4)}) translate(-540 0)`);
      }
    }
    clip.dataset.land = fit ? "fit" : `y0=${Math.round(y0)}`;
    // source chips (K3, SVG groups id src<N>) go to the page's bottom-right corner, clear of the captions and the badge (review M6)
    // at their 9:16 size (one unit = one page pixel), not shrunk with a fitted card (review r2 item 5)
    clip.querySelectorAll('g[id^="src"]').forEach((g) => {
      const w = document.createElementNS("http://www.w3.org/2000/svg", "g"); g.parentNode.insertBefore(w, g); w.appendChild(g);
      const r = w.getBoundingClientRect(), bb = w.getBBox(); if (!r.width || !bb.width) return;
      const k = r.width / bb.width, m = 1 / k, bx = bb.x + bb.width, by = bb.y + bb.height;
      const dx = (1890 - r.right) / k, dy = (1052 - r.bottom) / k;
      w.setAttribute("transform", `translate(${(bx + dx).toFixed(1)} ${(by + dy).toFixed(1)}) scale(${m.toFixed(4)}) translate(${(-bx).toFixed(1)} ${(-by).toFixed(1)})`);
    });
    clip.dataset.world = world ? world.map((v) => Math.round(v)).join(",") : "";
    // a set drawn only for the 9:16 frame (a card, a diagram, the shadow screen, a map) leaves the widened sides empty: fill them with a
    // blurred, dimmed blow-up of the shot itself (window.LANDBG: shot key -> image, made by fitbg.cjs), never plain black
    const bg = (window.LANDBG || {})[sh.key];
    if (bg) Object.assign(clip.style, { backgroundImage: `url(${bg})`, backgroundSize: "cover", backgroundPosition: "center" });
  }

  Engine.build = (root, tl, shots) => {
    build0(root, tl, shots);
    [...root.querySelectorAll(".clip")].forEach((clip) => { const i = +clip.id.slice(1); if (shots[i]) reflow(clip, shots[i]); });
    // things made for the Shorts only (the "watch the full story" sign, the repeated HG7 card): never in the long
    (LS.hide || []).forEach((sel) => root.querySelectorAll(sel).forEach((e) => { e.style.display = "none"; }));
  };
  window.Landscape = { reflow, SC, EXTRA, FIT };
})();
