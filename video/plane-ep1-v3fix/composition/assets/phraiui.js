// UI for "มือพราย": the source footnote under a knowledge card (GameUI.C.src, same as kwan3.js) and the card icons
// (120×120, ink outline, an animated part each: a-bob / a-pulse / a-wave / a-spin from gameui.js):
//   nopick (a hand over a krathong with coins, crossed out), nobend (someone bending over the water, crossed out),
//   shout (a mouth calling, sound arcs), throw (a gallon flying in an arc), reach (a long pole held out low), crouch (knees bent)
(function () {
  if (!window.GameUI) return;
  if (!GameUI.C.src) {
    if (typeof document !== "undefined" && !document.getElementById("zsrc-css")) document.head.insertAdjacentHTML("beforeend", `<style id="zsrc-css">
      .zsrc { position: absolute; left: 60px; right: 60px; z-index: 52; display: flex; justify-content: center; opacity: 0; }
      .zsrc span { display: inline-flex; gap: 12px; align-items: center; padding: 9px 20px 11px; border-radius: 16px; background: rgba(8,12,14,.86); border: 2px solid rgba(143,195,214,.5); color: #d8e8ee; font: 700 27px/1.25 Kanit; box-shadow: 0 10px 24px rgba(0,0,0,.45); }
      .zsrc b { flex: none; width: 34px; height: 34px; border-radius: 50%; background: #8fc3d6; color: #0d171b; font: 900 24px/34px Kanit; text-align: center; }
      .zsrc em { font-style: normal; color: #8fc3d6; font-weight: 900; }</style>`);
    GameUI.C.src = {
      html: (id, o) => `<div id="${id}" class="zsrc" style="top:${o.top}px"><span><b>i</b><div>${o.text}</div></span></div>`,
      anim(tl, id, t0, o) {
        tl.fromTo(`#${id}`, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out", immediateRender: false }, t0);
        if (o.end !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.15 }, o.t0abs + o.end);
      },
    };
  }
  const K = "#2e2a26", O = `stroke="${K}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"`;
  const SH = `<ellipse cx="60" cy="108" rx="34" ry="6" fill="#000" opacity=".18"/>`;
  const NO = `<g class="a-pulse"><circle cx="60" cy="60" r="50" fill="none" stroke="#e0362c" stroke-width="9"/><path d="M25,25L95,95" stroke="#e0362c" stroke-width="9" stroke-linecap="round"/></g>`;
  const WATER = `<path d="M8,86q13,-8 26,0t26,0t26,0t26,0V110H8Z" fill="#4f8fbf" ${O}/>`;
  Object.assign(GameUI.ILL, {
    nopick: `${WATER}<path d="M30,80Q60,60 90,80" fill="#5c9a4a" ${O}/><path d="M44,76Q48,52 60,48Q72,52 76,76Z" fill="#6aa856" ${O}/><circle cx="60" cy="44" r="5" fill="#ffd36a"/>
      <g class="a-bob"><ellipse cx="50" cy="76" rx="7" ry="3.5" fill="#f2d16a" ${O}/><ellipse cx="70" cy="77" rx="7" ry="3.5" fill="#f2d16a" ${O}/></g>
      <path d="M74,18q-8,20 -6,34q4,6 10,2l2,-14q6,4 12,0" fill="#efc6a0" ${O}/>${NO}`,
    nobend: `${WATER}<path d="M14,86H54" stroke="#8a5f3c" stroke-width="10"/><g class="a-bob"><circle cx="66" cy="54" r="11" fill="#efc6a0" ${O}/><path d="M30,82L36,58Q46,44 62,62" stroke="${K}" stroke-width="13" fill="none"/><path d="M30,82L36,58Q46,44 62,62" stroke="#d8443a" stroke-width="7" fill="none"/></g>${NO}`,
    shout: `${SH}<circle cx="44" cy="58" r="30" fill="#efc6a0" ${O}/><ellipse cx="58" cy="66" rx="10" ry="12" fill="#5a1f1a" ${O}/><circle cx="40" cy="48" r="4" fill="${K}"/>
      ${[0, 1, 2].map((i) => `<path class="a-wave" data-i="${i}" d="M${80 + i * 10},${46 - i * 6}q${10 + i * 4},${20 + i * 6} 0,${40 + i * 12}" fill="none" stroke="#e0362c" stroke-width="6" stroke-linecap="round"/>`).join("")}`,
    throw: `${WATER}<path d="M16,70Q50,0 92,60" stroke="#f4ecd8" stroke-width="5" stroke-dasharray="8 8" fill="none"/>
      <g class="a-bob"><path d="M76,36h22q6,0 6,6v26q0,6 -6,6h-22q-6,0 -6,-6v-26q0,-6 6,-6z" fill="#e9eef0" ${O}/><path d="M70,56h34v12q0,6 -6,6h-22q-6,0 -6,-6z" fill="#7fb3c9"/><path d="M80,36v-8h12v8" fill="#e04a3a" ${O}/></g>`,
    reach: `${WATER}<path d="M10,82H40" stroke="#8a5f3c" stroke-width="10"/><g class="a-pulse"><path d="M22,64L104,92" stroke="${K}" stroke-width="13" stroke-linecap="round"/><path d="M22,64L104,92" stroke="#c9b26a" stroke-width="7" stroke-linecap="round"/></g>
      <circle cx="104" cy="86" r="9" fill="#efc6a0" ${O}/><circle cx="24" cy="44" r="10" fill="#efc6a0" ${O}/>`,
    crouch: `${SH}<g class="a-bob"><circle cx="54" cy="30" r="12" fill="#efc6a0" ${O}/><path d="M50,44L44,70L66,78L58,102" stroke="${K}" stroke-width="13" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M50,44L44,70L66,78L58,102" stroke="#2b3d5e" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M52,52L86,62" stroke="${K}" stroke-width="10" stroke-linecap="round"/></g>
      <path d="M96,30v34M86,54l10,12l10,-12" stroke="#3fb86a" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
    nocarry: `${SH}<g class="a-bob"><circle cx="58" cy="26" r="11" fill="#efc6a0" ${O}/><path d="M50,38L46,74L40,104M58,40L64,74L70,104" stroke="${K}" stroke-width="9" fill="none" stroke-linecap="round"/>
      <path d="M30,40Q60,30 92,44L86,58Q60,48 34,54Z" fill="#d8443a" ${O}/><circle cx="96" cy="50" r="9" fill="#efc6a0" ${O}/></g>${NO}`,
    call1669: `${SH}<rect x="34" y="12" width="52" height="92" rx="10" fill="#2e3440" ${O}/><rect x="40" y="24" width="40" height="64" rx="4" fill="#9fd6ff"/>
      <g class="a-pulse"><text x="60" y="64" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="19" fill="#c8261c">1669</text></g>
      ${[0, 1].map((i) => `<path class="a-wave" data-i="${i}" d="M${94 + i * 8},${36 - i * 5}q${8 + i * 3},${14 + i * 4} 0,${28 + i * 9}" fill="none" stroke="#3fb86a" stroke-width="5" stroke-linecap="round"/>`).join("")}`,
    flatground: `<path d="M8,92H112" stroke="#8a5f3c" stroke-width="10" stroke-linecap="round"/><g class="a-bob"><circle cx="24" cy="74" r="11" fill="#efc6a0" ${O}/><path d="M36,78H96" stroke="${K}" stroke-width="15" stroke-linecap="round"/><path d="M36,78H96" stroke="#d8443a" stroke-width="9" stroke-linecap="round"/></g>
      <path d="M20,104h80" stroke="#3fb86a" stroke-width="5" stroke-dasharray="10 8"/>`,
    shake: `${SH}<circle cx="60" cy="44" r="18" fill="#efc6a0" ${O}/><path d="M30,104Q30,66 60,66Q90,66 90,104Z" fill="#d8443a" ${O}/>
      <g class="a-bob"><path d="M14,72l18,-6M106,72l-18,-6" stroke="${K}" stroke-width="10" stroke-linecap="round"/><path d="M8,56l-6,-6M8,88l-6,6M112,56l6,-6M112,88l6,6" stroke="#f2c55c" stroke-width="5" stroke-linecap="round"/></g>`,
    airway: `${SH}<g class="a-bob"><path d="M20,80Q20,40 60,36Q96,36 100,70" fill="#efc6a0" ${O}/><path d="M74,72q10,10 22,2" stroke="${K}" stroke-width="4" fill="none"/><path d="M28,46Q20,30 40,28" fill="#2a2220" ${O}/></g>
      <path d="M40,22l14,-10M96,92l12,8" stroke="#3fb86a" stroke-width="7" stroke-linecap="round"/><path d="M8,96H112" stroke="#8a5f3c" stroke-width="8"/>`,
    breath2: `${SH}<circle cx="46" cy="60" r="32" fill="#efc6a0" ${O}/><ellipse cx="62" cy="72" rx="9" ry="6" fill="#7a3a2a"/>
      <g class="a-pulse">${[0, 1].map((i) => `<circle cx="${86 + i * 16}" cy="${58 - i * 10}" r="${9 + i * 3}" fill="#bfe6ff" ${O}/>`).join("")}</g><text x="96" y="104" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="24" fill="${K}">×2</text>`,
    press30: `${SH}<path d="M14,100Q60,70 106,100" fill="#d8443a" ${O}/><g class="a-bob"><ellipse cx="60" cy="66" rx="26" ry="16" fill="#e8b48a" ${O}/><ellipse cx="60" cy="56" rx="26" ry="16" fill="#efc6a0" ${O}/><path d="M60,40V12" stroke="#f2f0ea" stroke-width="16"/></g>
      <path d="M88,24v24M80,40l8,10l8,-10" stroke="#3fb86a" stroke-width="5" fill="none" stroke-linecap="round"/><text x="26" y="34" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="${K}">30</text>`,
    sideLie: `<path d="M8,96H112" stroke="#8a5f3c" stroke-width="8"/><g class="a-bob"><circle cx="26" cy="70" r="12" fill="#efc6a0" ${O}/><path d="M40,74Q70,58 96,80L92,92Q66,80 42,88Z" fill="#d8443a" ${O}/><path d="M62,76L56,96M90,86L104,94" stroke="${K}" stroke-width="7" stroke-linecap="round"/></g>`,
    blanket: `<path d="M8,96H112" stroke="#8a5f3c" stroke-width="8"/><circle cx="24" cy="72" r="12" fill="#efc6a0" ${O}/><g class="a-bob"><path d="M34,62Q70,48 106,66L104,92H36Z" fill="#8a6a5a" ${O}/>${[50, 66, 82].map((x) => `<path d="M${x},58V90" stroke="#6a4e40" stroke-width="4"/>`).join("")}</g>`,
    nofood: `${SH}<path d="M38,30h44l-6,72h-32z" fill="#bfe6ff" ${O}/><path d="M40,50h40" stroke="#4f8fbf" stroke-width="5"/><path d="M84,40q16,14 0,30" stroke="${K}" stroke-width="5" fill="none"/>${NO}`,
  });
})();
