// ช่างเชื่อมสายฟ้า remake · character look pass (owner 13 Nov: "ทำตัวละครให้ดีกว่านี้ สี ลายเส้น เงา")
//   colour: warmer, more saturated skin and clothes, each character on its own hue so they read apart in a busy 3D set
//   line:   a warm dark ink outline on every body shape (non-scaling, paint-order stroke) so the flat cast sits on top of the set
//   shade:  a stronger directional shade on torso/limbs/head + a rim light on the key side + a contact shadow under the feet
// Exposes LTINK(aid) to run after Rig.build (called from the sprite job's "extra").
(function () {
  if (window.LTSTYLE_DONE) return; window.LTSTYLE_DONE = 1;
  const INK = "#2b1a16";

  // ---------- 1. colour ----------
  const C = Rig.CAST;
  const set = (k, v) => { if (C[k]) Object.assign(C[k].v2, v); };
  const skin = (k, s) => { if (C[k]) C[k].v2.skin = s; };
  // the welder: warmer skin, a deeper denim tee, a richer leather apron tone comes from the acc art
  ["ltYou", "ltYouWeld", "ltYouWeldOn", "ltYouBolt", "ltYouBoltWeld"].forEach((k) => {
    skin(k, "#d89158"); set(k, { top: { kind: "tee", c: "#2d5f8f", sleeve: "short" }, bottom: { kind: "jeans", c: "#30406e" }, feet: { kind: "boot", c: "#4a3122" } });
  });
  skin("ltYouGown", "#d89158");
  if (C.ltYouGown) Object.assign(C.ltYouGown.v2, { top: { kind: "tee", c: "#8fd6e8", sleeve: "short" }, bottom: { kind: "trousers", c: "#8fd6e8" } });
  // เจ๊หงส์: hotter magenta blouse, warmer skin
  ["ltHong", "ltHongCalc", "ltHongCash"].forEach((k) => { skin(k, "#e8b184"); set(k, { top: { kind: "tee", c: "#d62f6e", sleeve: "elbow" }, bottom: { kind: "trousers", c: "#36364e" } }); });
  // เฮียกิม: olive skin, cream singlet, khaki shorts
  ["ltKim", "ltKimDriver"].forEach((k) => { skin(k, "#d8a97e"); set(k, { top: { kind: "singlet", c: "#f4efe2" }, bottom: { kind: "shorts", c: "#7f6b44" } }); });
  // the alley: push each one to a clearly different hue
  const ALLEY = { ltMan1: ["#caa06a", "#e8d88a"], ltMan2: ["#d8a278", "#3f7fd6"], ltWom1: ["#e8bc92", "#f2c838"], ltWom2: ["#dca888", "#ea5f84"] };
  Object.entries(ALLEY).forEach(([k, [sk, tc]]) => { skin(k, sk); if (C[k]) C[k].v2.top.c = tc; });
  if (C.ltNurse) C.ltNurse.v2.skin = "#eac29c";
  if (C.ltNurseBolt) C.ltNurseBolt.v2.skin = "#eac29c";

  // ---------- 2. shade: stronger gradients (every body shape already paints url(#flV) / url(#flLimb) over itself) ----------
  const stops = (id, list) => document.querySelectorAll('[id="' + id + '"]').forEach((g) => {
    g.innerHTML = list.map(([o, c, op]) => `<stop offset="${o}" stop-color="${c}" stop-opacity="${op}"/>`).join("");
  });
  // key from the upper left in the sprite's own frame: light on top-left, deep shade bottom-right
  stops("flV", [[0, "#ffe9c8", 0.3], [0.38, "#fff", 0.04], [0.72, "#2a1c44", 0.16], [1, "#1a1036", 0.38]]);
  stops("flLimb", [[0, "#ffe9c8", 0.26], [0.42, "#fff", 0.03], [1, "#1a1036", 0.3]]);
  document.querySelectorAll('[id="flV"],[id="flLimb"]').forEach((g) => { if (g.id === "flV") { g.setAttribute("x1", "0.15"); g.setAttribute("x2", "0.85"); g.setAttribute("y1", "0"); g.setAttribute("y2", "1"); } });

  // ---------- 3. the pass that runs on a built character ----------
  window.LTINK = function (aid, o) {
    o = o || {};
    const root = document.getElementById(aid + "-root") || document.querySelector("#spr");
    if (!root) return;
    const W = o.w || 3.4, OP = o.op || 0.92;
    root.querySelectorAll("path,rect,ellipse,circle,polygon").forEach((el) => {
      const fl = el.getAttribute("fill");
      if (!fl || fl === "none" || fl.startsWith("url")) return;
      const st = el.getAttribute("stroke"); if (st && st !== "none") return;
      if (el.getAttribute("filter")) return;
      let op = 1; for (let n = el; n && n !== root; n = n.parentNode) { if (n.getAttribute) op *= +(n.getAttribute("opacity") ?? 1); }
      if (op * +(el.getAttribute("fill-opacity") ?? 1) < 0.75) return;
      let bb; try { bb = el.getBBox(); } catch (e) { return; }
      if (bb.width * bb.height < 26) return;                       // skip catch-lights, stitches, tiny marks
      if (bb.width > 1400 || bb.height > 1400) return;
      // limb bars are thin rounded rects: a thinner line keeps the elbow / knee overlaps from reading as cuts
      const thin = el.tagName === "rect" && Math.min(bb.width, bb.height) < 42;
      el.setAttribute("stroke", INK); el.setAttribute("stroke-width", thin ? W * 0.72 : W); el.setAttribute("stroke-opacity", thin ? OP * 0.8 : OP);
      el.setAttribute("vector-effect", "non-scaling-stroke"); el.setAttribute("stroke-linejoin", "round"); el.setAttribute("paint-order", "stroke");
    });
    // rim light on the key side of the head and a contact shadow under the feet
    const head = document.getElementById(aid + "-head");
    if (head && !head.querySelector(".ltRim")) {
      head.insertAdjacentHTML("beforeend", `<g class="ltRim" style="pointer-events:none"><path d="M-33,-575Q-44,-546 -34,-516" stroke="#ffe3b0" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/></g>`);
    }
    if (!root.querySelector(".ltFloor")) {
      root.insertAdjacentHTML("afterbegin", `<ellipse class="ltFloor" cx="6" cy="6" rx="52" ry="13" fill="#17102c" opacity=".3" filter="url(#flSoft)"/>`);
    }
  };
})();
