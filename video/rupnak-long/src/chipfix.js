// Long-form 16:9 (also: any light-layer group with data-page="cx,cy,h" is placed centred at those page pixels, h px tall): the "ที่มา: …" source chips drawn in a shot's L.light land under the captions after landscape.js fits the light
// layer into the band (and come out ~22 px tall). Load after landscape.js: once the clips are laid out, every light-layer group whose
// text starts with "ที่มา" is wrapped and placed bottom right of the page (right edge 1880, bottom 1046, text ~34 px tall), clear of
// the centred captions and the badge on the left. The chip's own tweens (fade, slide) still drive it inside the wrapper.
(function () {
  const RIGHT = 1880, BOTTOM = 1046, TEXT_H = 34;
  const build0 = Engine.build;
  Engine.build = (root, tl, shots) => {
    const r = build0(root, tl, shots);
    const NS = "http://www.w3.org/2000/svg";
    document.querySelectorAll('[id$="-light"]').forEach((light) => {
      const chips = new Set();
      light.querySelectorAll("text").forEach((t) => {
        if (!/^\s*ที่มา/.test(t.textContent || "")) return;
        let g = t; while (g.parentNode && g.parentNode !== light && !(g.parentNode.parentNode === light && !g.parentNode.id)) g = g.parentNode;
        chips.add(g);
      });
      // groups marked data-page="cx,cy,h" go to page pixels too: centred on (cx, cy), h px tall
      const marked = [...light.querySelectorAll("[data-page]")];
      if (!chips.size && !marked.length) return;
      const clip = light.closest(".clip"), vis = clip.style.visibility, disp = clip.style.display;
      clip.style.visibility = "visible"; clip.style.display = "";
      // fit shots (the whole vertical frame in a centre panel): keep the chip inside the panel's right edge (review r2 B1: e3_week)
      const R = clip.dataset.land === "fit" || clip.classList.contains("lfit") ? 1600 : RIGHT;
      chips.forEach((chip) => {
        const w = document.createElementNS(NS, "g"); chip.parentNode.insertBefore(w, chip); w.appendChild(chip);
        const bb = w.getBBox(), M = w.parentNode.getScreenCTM(); if (!M || !bb.height) return;
        const textH = Math.max(...[...chip.querySelectorAll("text")].map((t) => t.getBBox().height), 1);
        const k = TEXT_H / (textH * M.a);
        const inv = M.inverse(), p = new DOMPoint(R, BOTTOM).matrixTransform(inv);
        w.setAttribute("transform", `translate(${(p.x - (bb.x + bb.width) * k).toFixed(2)},${(p.y - (bb.y + bb.height) * k).toFixed(2)}) scale(${k.toFixed(4)})`);
        w.setAttribute("class", "srcchip");
        // never under a caption: if the chip's page box meets any caption box of this shot, lift it to sit just above the captions
        const cr = w.getBoundingClientRect(), caps = [...clip.querySelectorAll(".capbox")].map((c) => c.getBoundingClientRect()).filter((r) => r.width > 0);
        const hit = caps.some((r) => cr.left < r.right + 24 && cr.right > r.left - 24 && cr.top < r.bottom && cr.bottom > r.top);
        if (hit) {
          const top = Math.min(...caps.map((r) => r.top)) - 14, q = new DOMPoint(R, top).matrixTransform(inv);
          w.setAttribute("transform", `translate(${(q.x - (bb.x + bb.width) * k).toFixed(2)},${(q.y - (bb.y + bb.height) * k).toFixed(2)}) scale(${k.toFixed(4)})`);
        }
      });
      marked.forEach((g) => {
        const [cx, cy, h] = g.getAttribute("data-page").split(",").map(Number);
        const w = document.createElementNS(NS, "g"); g.parentNode.insertBefore(w, g); w.appendChild(g);
        const bb = w.getBBox(), M = w.parentNode.getScreenCTM(); if (!M || !bb.height) return;
        const k = h / (bb.height * M.a), p = new DOMPoint(cx, cy).matrixTransform(M.inverse());
        w.setAttribute("transform", `translate(${(p.x - (bb.x + bb.width / 2) * k).toFixed(2)},${(p.y - (bb.y + bb.height / 2) * k).toFixed(2)}) scale(${k.toFixed(4)})`);
      });
      clip.style.visibility = vis; clip.style.display = disp;
    });
    return r;
  };
})();
