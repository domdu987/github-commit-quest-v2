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
      chips.forEach((chip) => {
        const w = document.createElementNS(NS, "g"); chip.parentNode.insertBefore(w, chip); w.appendChild(chip);
        const bb = w.getBBox(), M = w.parentNode.getScreenCTM(); if (!M || !bb.height) return;
        const textH = Math.max(...[...chip.querySelectorAll("text")].map((t) => t.getBBox().height), 1);
        const k = TEXT_H / (textH * M.a);
        const inv = M.inverse(), p = new DOMPoint(RIGHT, BOTTOM).matrixTransform(inv);
        w.setAttribute("transform", `translate(${(p.x - (bb.x + bb.width) * k).toFixed(2)},${(p.y - (bb.y + bb.height) * k).toFixed(2)}) scale(${k.toFixed(4)})`);
        w.setAttribute("class", "srcchip");
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
