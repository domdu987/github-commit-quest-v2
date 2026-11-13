// สกิลจอมโกหก · v3 eyes (the EP.1/EP.2 look-V clips): big round whites, round pupils with a catch-light, thick curved brows, open mouths; the hero's glasses fit them.
(function () {
  if (window.LTEYES_DONE) return; window.LTEYES_DONE = 1;
      // ---------- v3 faces (owner, 11 Nov): big round whites with round pupils and a catch-light, thick curved brows, open mouths with a dark red inside ----------
      const EX = [-8, 21], EY = -549, INK3 = "#211714";
      Sets.DEFS += `<radialGradient id="v3Shade" cx=".34" cy=".3" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset=".8" stop-color="#5a2038" stop-opacity=".16"/><stop offset="1" stop-color="#3a1028" stop-opacity=".38"/></radialGradient>`;
      const SHADE = `<ellipse cx="5" cy="-547" rx="39.5" ry="43.6" fill="url(#v3Shade)"/><path d="M40,-578Q50,-547 38,-512" stroke="#ffd8b8" stroke-width="3.5" fill="none" opacity=".55" stroke-linecap="round"/><ellipse cx="-14" cy="-560" rx="12" ry="18" fill="#fff" opacity=".10" transform="rotate(-20 -14 -560)"/>`;
      const bigFaces = (o = {}) => (x, browC, base) => {
        const b = base(browC), bw = o.browW ?? 5.2, R = o.r ?? 9.4;
        const white = (cx, cy, r = R, ry) => `<ellipse cx="${cx}" cy="${cy}" rx="${r}" ry="${ry ?? r}" fill="#fffaf4"/><ellipse cx="${cx}" cy="${(cy + (ry ?? r) * 0.35).toFixed(1)}" rx="${(r * 0.9).toFixed(1)}" ry="${((ry ?? r) * 0.55).toFixed(1)}" fill="#e8d4cc" opacity=".35"/>`;
        const pupil = (cx, cy, pr = 4.4) => `<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${pr}" fill="${INK3}"/><circle cx="${(cx + pr * 0.4).toFixed(1)}" cy="${(cy - pr * 0.45).toFixed(1)}" r="${Math.max(1.2, pr * 0.36).toFixed(1)}" fill="#fff" opacity=".95"/>`;
        const brows = (dy = 0, tilt = 0) => EX.map((ex, i) => { const inner = ex + (i ? -8 : 8), outer = ex + (i ? 9.5 : -9.5);
          return `<path d="M${outer},${EY - 17 + dy}Q${(inner + outer) / 2},${EY - 21 + dy + tilt / 2} ${inner},${EY - 17 + dy + tilt}" stroke="${browC}" stroke-width="${bw}" fill="none" stroke-linecap="round"/>`; }).join("");
        const eyes = (q = {}) => EX.map((ex, i) => white(ex, EY, q.r ?? R, q.ry) + pupil(ex + (q.dx ?? 0) + (q.inward ? (i ? -1 : 1) * q.inward : 0), EY + (q.dy ?? 0), q.pr ?? 4.4)).join("") + brows(q.bdy ?? 0, q.tilt ?? 0);
        const closed = EX.map((ex) => `<path d="M${ex - 8},${EY - 0.5}q8,7 16,0" stroke="${INK3}" stroke-width="3.4" fill="none" stroke-linecap="round"/>`).join("") + brows(2);
        const happy = EX.map((ex) => `<path d="M${ex - 8.5},${EY + 2}q8.5,-11 17,0" stroke="${INK3}" stroke-width="3.6" fill="none" stroke-linecap="round"/>`).join("") + brows(-2);
        const tired = EX.map((ex) => white(ex, EY) + pupil(ex, EY + 1.5, 4.2) + `<path d="M${ex - 9.6},${EY}A9.6,9.6 0 0,1 ${ex + 9.6},${EY}Z" fill="${x.skin}"/><path d="M${ex - 9.6},${EY}H${ex + 9.6}" stroke="${INK3}" stroke-width="2.6" stroke-linecap="round"/>`).join("") + brows(3, 2);
        const squint = EX.map((ex) => white(ex, EY, R, 4.6) + `<ellipse cx="${ex}" cy="${EY}" rx="4.2" ry="3" fill="${INK3}"/>`).join("") + brows(1, 3);
        const E = { ...b.eyes, normal: eyes({ pr: 4.6 }), side: eyes({ dx: 4.2, pr: 4.4 }), worry: eyes({ pr: 4.2, bdy: -4, tilt: -6 }), angry: eyes({ pr: 4.8, bdy: 4, tilt: 9 }), wide: eyes({ r: R + 1, pr: 3.9, inward: 0.8, bdy: -8, tilt: -1 }), sad: eyes({ pr: 4.4, dy: 1.5, bdy: -1, tilt: 7 }), squint, happy, tired, closed };
        return { eyes: Object.fromEntries(Object.entries(E).map(([k, v]) => [k, SHADE + v])),
          mouths: { ...b.mouths, o: `<ellipse cx="9" cy="-519" rx="6.2" ry="8" fill="#5a2622"/><ellipse cx="9" cy="-515" rx="4" ry="3.2" fill="#c8605a"/>`, scream: `<ellipse cx="9" cy="-516" rx="9" ry="12.5" fill="#5a2622"/><ellipse cx="9" cy="-508" rx="5.5" ry="4" fill="#c8605a"/><path d="M2,-526h14" stroke="#f4ecd8" stroke-width="2.6" stroke-linecap="round"/>` } };
      };
      Object.keys(Flat.SPEC).filter((k) => /^(jk|lt)/.test(k) && Flat.SPEC[k].faces).forEach((k) => { Flat.SPEC[k].faces = bigFaces({ browW: k === "jkYou" || k === "jkKen" ? 5.4 : 5.0 }); });
      // the hero: thick round glasses drawn over the big eyes (with a lens glint), a warmer peach skin like the owner's picture
      { const earSvg = Flat.SPEC.jkYou.headTop ? Flat.SPEC.jkYou.headTop() : ""; Flat.SPEC.jkYou.glasses = false;
        Flat.SPEC.jkYou.headTop = () => earSvg + `<g fill="none" stroke="#1e1a1c" stroke-width="3.4"><circle cx="-8" cy="-549" r="11.6"/><circle cx="21" cy="-549" r="11.6"/><path d="M3.6,-549H9.4"/><path d="M-19.6,-551l-7,-3"/></g><path d="M-15,-556q4,-5 9,-5M14,-556q4,-5 9,-5" stroke="#fff" stroke-width="2" fill="none" opacity=".45" stroke-linecap="round"/>`;
        Rig.CAST.jkYou.v2.skin = "#e8a070"; Flat.SPEC.jkYou.blush = 0.3; }

})();
