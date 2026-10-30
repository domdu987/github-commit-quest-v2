// Round cartoon hands for close-ups, in the house style (the rigs' hands are plain circles; the เสียงกอย torch hand is a round fist):
// a flat skin circle with the ink outline, a soft shade on the lower side, the fold of the curled fingers and three short finger lines.
//   Hands.fist(o)  — a fist centred at (0, 0), radius o.r (default 80); the finger lines face -y (rotate the group to turn it).
//   Hands.poke(o)  — a fist with one short round finger out, the fingertip at (0, 0); the fist and the arm run toward +x.
//   o.skin, o.shade = colours; o.sleeve = colour for the arm (poke only: drawn from the fist along +x for o.sleeveLen, with a lighter cuff).
(function () {
  const f1 = (v) => v.toFixed(1);
  const INK = "#2e2a26", OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const SKIN = "#ecbf98", SHADE = "#cc9a74";

  function fist(o = {}) {
    const r = o.r ?? 80, sk = o.skin || SKIN, sh = o.shade || SHADE;
    const pt = (a, rr) => [rr * Math.cos(a * Math.PI / 180), rr * Math.sin(a * Math.PI / 180)];
    const [ax, ay] = pt(-10, r), [bx, by] = pt(150, r);
    let g = `<circle r="${r}" fill="${sk}" ${OUT}/>`;
    g += `<path d="M${f1(ax)},${f1(ay)}A${r},${r} 0 0 1 ${f1(bx)},${f1(by)}A${f1(r * 1.25)},${f1(r * 1.25)} 0 0 0 ${f1(ax)},${f1(ay)}Z" fill="${sh}" opacity=".45"/>`;
    g += `<ellipse cx="${f1(-r * 0.32)}" cy="${f1(-r * 0.38)}" rx="${f1(r * 0.3)}" ry="${f1(r * 0.2)}" fill="#fff" opacity=".18"/>`;
    // the fold where the curled fingers meet the palm, and the lines between the fingers above it
    g += `<path d="M${f1(-r * 0.62)},${f1(r * 0.12)}Q0,${f1(r * 0.3)} ${f1(r * 0.62)},${f1(r * 0.12)}" stroke="${sh}" stroke-width="${f1(Math.max(3, r * 0.06))}" stroke-linecap="round" fill="none"/>`;
    [-0.3, 0, 0.3].forEach((k) => {
      const x = k * r, y0 = -r * 0.5, y1 = r * 0.14 + (0.3 - Math.abs(k)) * r * 0.25;
      g += `<path d="M${f1(x)},${f1(y0)}L${f1(x)},${f1(y1 - r * 0.12)}" stroke="${sh}" stroke-width="${f1(Math.max(2.5, r * 0.045))}" stroke-linecap="round"/>`;
    });
    return g;
  }

  function poke(o = {}) {
    const r = o.r ?? 70, w = r * 0.5, sk = o.skin || SKIN, sh = o.shade || SHADE;
    const cx = r * 1.7, cy = r * 0.3;
    let g = "";
    if (o.sleeve) {
      const L = o.sleeveLen ?? 900, cw = r * 1.45;
      g += `<path d="M${f1(cx)},${f1(cy)}H${f1(cx + L)}" stroke="${INK}" stroke-width="${f1(cw + 10)}" stroke-linecap="round"/><path d="M${f1(cx)},${f1(cy)}H${f1(cx + L)}" stroke="${o.sleeve}" stroke-width="${f1(cw)}" stroke-linecap="round"/>`;
      g += `<rect x="${f1(cx + r * 0.6)}" y="${f1(cy - cw / 2)}" width="${f1(r * 0.5)}" height="${f1(cw)}" fill="${o.cuff || "#efc256"}" ${OUT}/>`;
    }
    g += `<rect x="0" y="${f1(-w / 2)}" width="${f1(cx)}" height="${f1(w)}" rx="${f1(w / 2)}" fill="${sk}" ${OUT}/>`;
    g += `<path d="M${f1(w * 0.55)},${f1(w * 0.3)}q${f1(w * 0.2)},${f1(-w * 0.12)} ${f1(w * 0.4)},0" stroke="${sh}" stroke-width="3" fill="none" stroke-linecap="round"/>`;
    g += `<g transform="translate(${f1(cx)},${f1(cy)}) rotate(-90)">${fist({ r, skin: sk, shade: sh })}</g>`;
    return g;
  }

  window.Hands = { fist, poke, SKIN };
})();
