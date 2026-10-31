// Card icons for "หมอกลง" (GameUI.ILL, 120×120): shaded fills, a highlight, a soft ground shadow and one moving part each
// (gameui.js loops(): a-pulse a-bob a-bob2 a-sway a-shake a-spin a-wave[data-i] a-draw). Loaded after gameui.js; the episode
// templates no longer define their own copies. Also restyles the step badges for the series (glossy, coloured ring).
(function () {
  const K = "#2e2a26", O = `stroke="${K}" stroke-width="4" stroke-linejoin="round"`;
  const lg = (id, a, b, v = true) => `<linearGradient id="${id}" x1="0" y1="0" x2="${v ? 0 : 1}" y2="${v ? 1 : 0}"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient>`;
  const rg = (id, a, b, cx = 0.38, cy = 0.32) => `<radialGradient id="${id}" cx="${cx}" cy="${cy}" r=".75"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></radialGradient>`;
  const shadow = (cx = 60, cy = 108, rx = 34) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="6" fill="#000" opacity=".18"/>`;
  const shine = (d) => `<path d="${d}" fill="#fff" opacity=".38"/>`;
  const NO = `<g class="a-pulse"><circle cx="60" cy="60" r="50" fill="none" stroke="#e0362c" stroke-width="9"/><path d="M25,25L95,95" stroke="#e0362c" stroke-width="9" stroke-linecap="round"/></g>`;
  const face = (id, a, b) => `<defs>${rg(id, a, b)}</defs>${shadow(60, 110, 30)}<circle cx="60" cy="66" r="36" fill="url(#${id})" ${O}/>${shine("M38,48q8,-14 24,-16q-14,8 -18,20z")}`;
  const wheel = (cx, cy, r) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="url(#mi-wh)" stroke-width="11"/><circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${K}" stroke-width="2.5" opacity=".6"/>
      <path d="M${cx - r},${cy}H${cx + r}M${cx},${cy}V${cy + r}" stroke="url(#mi-wh)" stroke-width="9"/><circle cx="${cx}" cy="${cy}" r="11" fill="#3a3f47" ${O}/>`;
  const WH = `<defs>${lg("mi-wh", "#6b717a", "#2a2d33")}</defs>`;

  const ICONS = {
    // ---------------- EP.1: driving in fog ----------------
    lowbeam: `<defs>${lg("mi-lb", "#8a929c", "#3a3f47")}${rg("mi-lbl", "#fffbe6", "#e0a43a")}${lg("mi-ray", "#ffe7a0", "#ffe7a0", false)}</defs>${shadow(50, 106, 26)}
      <path d="M20,38Q20,22 38,22H56V98H38Q20,98 20,82Z" fill="url(#mi-lb)" ${O}/><ellipse cx="46" cy="60" rx="9" ry="28" fill="url(#mi-lbl)"/>${shine("M26,34q4,-8 14,-8v10q-8,0 -14,6z")}
      ${[0, 1, 2].map((i) => `<path class="a-wave" data-i="${i}" d="M64,${46 + i * 14}L106,${62 + i * 16}" stroke="#f2c23a" stroke-width="8" stroke-linecap="round"/>`).join("")}`,
    slow: `<defs>${rg("mi-sl", "#3a4656", "#141a22")}</defs>${shadow()}<circle cx="60" cy="66" r="44" fill="url(#mi-sl)" ${O}/>
      <path d="M26,80A36,36 0 0 1 36,40" stroke="#3fb86a" stroke-width="9" fill="none"/><path d="M38,38A36,36 0 0 1 82,38" stroke="#f2c23a" stroke-width="9" fill="none"/><path d="M84,40A36,36 0 0 1 94,80" stroke="#e0362c" stroke-width="9" fill="none"/>
      <g class="a-sway"><circle cx="60" cy="72" r="34" fill="none"/><path d="M60,72L34,58" stroke="#fff" stroke-width="6" stroke-linecap="round"/></g><circle cx="60" cy="72" r="8" fill="#e0362c" ${O}/>
      <text x="60" y="100" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="15" fill="#cfe8ff">km/h</text>${shine("M30,48q14,-22 40,-24q-24,10 -34,30z")}`,
    lines: `<defs>${lg("mi-rd", "#4a525c", "#1e2329")}</defs>${shadow(60, 110, 40)}<path d="M44,10H76L108,108H12Z" fill="url(#mi-rd)" ${O}/>
      <path d="M44,12L16,106M76,12L104,106" stroke="#f4f0e4" stroke-width="5"/><g class="a-bob">${[[60, 20, 4, 10], [60, 42, 6, 16], [60, 72, 9, 24]].map(([x, y, w, h]) => `<rect x="${x - w / 2}" y="${y}" width="${w}" height="${h}" rx="2" fill="#f2c23a"/>`).join("")}</g>
      <rect x="44" y="92" width="32" height="16" rx="5" fill="#d9dde2" ${O}/><circle cx="48" cy="100" r="3.5" fill="#ff4a3a"/><circle cx="72" cy="100" r="3.5" fill="#ff4a3a"/>`,
    hazard: `<defs>${lg("mi-hz", "#ff6a52", "#b81e14")}</defs>${shadow()}<g class="a-pulse"><path d="M60,14L108,98H12Z" fill="url(#mi-hz)" ${O}/><path d="M60,44L82,84H38Z" fill="none" stroke="#fff" stroke-width="7" stroke-linejoin="round"/></g>${shine("M60,20L38,58l8,2z")}`,
    lightsoff: `<defs>${lg("mi-lo", "#8a929c", "#3a3f47")}</defs>${shadow(50, 106, 26)}<path d="M20,38Q20,22 38,22H56V98H38Q20,98 20,82Z" fill="url(#mi-lo)" ${O}/><ellipse cx="46" cy="60" rx="9" ry="28" fill="#5a636e"/>
      ${[0, 1, 2].map((i) => `<path d="M64,${46 + i * 14}L100,${62 + i * 16}" stroke="#8a929c" stroke-width="7" stroke-linecap="round" opacity=".5"/>`).join("")}${NO}`,
    handbrake: `<defs>${lg("mi-hb", "#5a616b", "#22262c")}${lg("mi-hbg", "#ff6a52", "#b81e14")}</defs>${shadow()}<rect x="18" y="94" width="70" height="14" rx="6" fill="#3a3f47" ${O}/>
      <g class="a-bob"><path d="M30,96L86,34" stroke="url(#mi-hb)" stroke-width="16" stroke-linecap="round"/><rect x="74" y="16" width="30" height="30" rx="9" fill="url(#mi-hbg)" ${O}/>${shine("M78,20h18v6h-18z")}</g>
      <path d="M100,70V96M92,78L100,68L108,78" stroke="#3fb86a" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
    footoff: `<defs>${lg("mi-pd", "#4a525c", "#1e2329")}${lg("mi-sh", "#f4f0e4", "#c9c1ae")}</defs>${shadow(84, 110, 22)}<rect x="62" y="66" width="44" height="40" rx="8" fill="url(#mi-pd)" ${O}/>
      <path d="M68,76H100M68,86H100M68,96H100" stroke="#6b737d" stroke-width="3"/>
      <g class="a-bob"><path d="M22,58C16,38 24,18 42,14L56,16C62,30 60,46 50,58Z" fill="url(#mi-sh)" ${O}/><path d="M22,58H52" stroke="${K}" stroke-width="5"/></g>
      <path d="M36,92V66M28,74L36,64L44,74" stroke="#3fb86a" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,

    // ---------------- EP.2: carbon monoxide ----------------
    headache: `${face("mi-hd", "#f6d2b0", "#d79a70")}<path d="M44,66l10,4M76,66l-10,4M48,86q12,-7 24,0" stroke="${K}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <g class="a-shake"><path d="M20,14l12,15l-9,5l12,16" stroke="#e0362c" stroke-width="6" fill="none" stroke-linejoin="round" stroke-linecap="round"/><path d="M100,14l-12,15l9,5l-12,16" stroke="#e0362c" stroke-width="6" fill="none" stroke-linejoin="round" stroke-linecap="round"/></g>`,
    dizzy: `${face("mi-dz", "#f6d2b0", "#d79a70")}${[47, 73].map((x) => `<path d="M${x},64m-8,0a8,8 0 1 1 8,8a5,5 0 1 1 -4,-5" stroke="${K}" stroke-width="4" fill="none"/>`).join("")}<path d="M50,88q10,6 20,0" stroke="${K}" stroke-width="5" fill="none"/>
      <g class="a-spin"><circle cx="60" cy="26" r="44" fill="none"/>${[0, 120, 240].map((a) => `<path transform="rotate(${a} 60 26) translate(60,-8)" d="M0,-8L2.4,-2.4L8,0L2.4,2.4L0,8L-2.4,2.4L-8,0L-2.4,-2.4Z" fill="#f2c23a" stroke="${K}" stroke-width="1.5"/>`).join("")}</g>`,
    nausea: `${face("mi-ns", "#d6efb4", "#8fbf6a")}<path d="M44,60l9,3M76,60l-9,3" stroke="${K}" stroke-width="5" stroke-linecap="round"/><path d="M40,84q5,-6 10,0t10,0t10,0t10,0" stroke="${K}" stroke-width="5" fill="none"/>
      <g class="a-bob"><path d="M92,36q8,12 0,16q-8,-4 0,-16z" fill="#7fd1ff" ${O}/></g>`,
    inroom: `<defs>${lg("mi-hw", "#f1e6cc", "#cdb88a")}${lg("mi-rf", "#8a4a32", "#5a2e20")}</defs>${shadow()}<path d="M22,58V104H98V58Z" fill="url(#mi-hw)" ${O}/><path d="M12,62L60,22L108,62Z" fill="url(#mi-rf)" ${O}/>
      ${[[40, 72], [56, 88], [76, 74], [84, 94]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="4.5" fill="#9b8ccf" opacity=".8"/>`).join("")}
      <g class="a-bob"><path d="M60,50V92M44,76L60,92L76,76" stroke="#e0362c" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
    outside: `<defs>${rg("mi-sky", "#e8f6ff", "#9ad0f0")}</defs>${shadow()}<circle cx="60" cy="60" r="46" fill="url(#mi-sky)" ${O}/>
      ${[0, 1, 2].map((i) => `<path class="a-wave" data-i="${i}" d="M${24 + i * 6},${36 + i * 16}q14,-8 28,0t28,0" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}
      <g class="a-bob"><path d="M60,98V48M42,64L60,46L78,64" stroke="#2f9e5a" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
    co: `<defs>${rg("mi-co", "#e6e0ff", "#9b8ccf")}</defs>${shadow()}<g class="a-bob"><path d="M28,80Q10,78 14,60Q16,44 34,46Q38,24 60,26Q82,24 86,44Q106,44 106,62Q106,80 88,80Z" fill="url(#mi-co)" ${O}/>
      <text x="60" y="72" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="${K}">CO</text></g>${[[30, 96], [52, 102], [80, 98]].map(([x, y], i) => `<circle class="a-wave" data-i="${i}" cx="${x}" cy="${y}" r="4" fill="#9b8ccf"/>`).join("")}`,
    noeye: `<defs>${rg("mi-ey", "#ffffff", "#d6dde4", 0.5, 0.4)}${rg("mi-ir", "#8fd0ff", "#2a6fb0", 0.4, 0.35)}</defs>${shadow()}<path d="M12,60Q60,12 108,60Q60,108 12,60Z" fill="url(#mi-ey)" ${O}/>
      <circle cx="60" cy="60" r="18" fill="url(#mi-ir)" ${O}/><circle cx="60" cy="60" r="7" fill="${K}"/><circle cx="54" cy="54" r="4" fill="#fff"/>${NO}`,
    nonose: `<defs>${rg("mi-ns2", "#f6d2b0", "#d79a70")}</defs>${shadow()}<path d="M58,16C54,46 38,70 34,84Q44,96 58,90Q72,96 82,84C78,70 62,46 58,16Z" fill="url(#mi-ns2)" ${O}/>
      <path d="M46,86q4,-6 8,0M62,86q4,-6 8,0" stroke="${K}" stroke-width="4" fill="none"/>${[0, 1].map((i) => `<path class="a-wave" data-i="${i}" d="M${90 + i * 8},${30 + i * 12}q8,8 0,16" stroke="#9b8ccf" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}${NO}`,
    build: `<defs>${lg("mi-bw", "#f1e6cc", "#cdb88a")}${lg("mi-gas", "#c9bcff", "#8a7ab4")}</defs>${shadow()}<rect x="16" y="22" width="88" height="84" rx="8" fill="url(#mi-bw)" ${O}/>
      <rect class="a-bob" x="20" y="52" width="80" height="50" rx="4" fill="url(#mi-gas)" opacity=".75"/>
      ${[[32, 66], [50, 80], [70, 62], [86, 84], [42, 92], [64, 90]].map(([x, y], i) => `<circle class="a-wave" data-i="${i % 3}" cx="${x}" cy="${y}" r="4" fill="#fff" opacity=".8"/>`).join("")}<path d="M16,22H104" stroke="${K}" stroke-width="6"/>`,
    skull: `<defs>${rg("mi-sk", "#ffffff", "#d8d2c4")}</defs>${shadow()}<g class="a-shake"><path d="M24,56Q24,16 60,16Q96,16 96,56Q96,72 84,78V98H36V78Q24,72 24,56Z" fill="url(#mi-sk)" ${O}/>
      <circle cx="45" cy="56" r="11" fill="${K}"/><circle cx="75" cy="56" r="11" fill="${K}"/><path d="M60,68l-6,10h12z" fill="${K}"/><path d="M48,98V88M60,98V88M72,98V88" stroke="${K}" stroke-width="4"/>${shine("M32,40q6,-16 22,-20q-14,10 -16,24z")}</g>`,
    stovex: `<defs>${lg("mi-st", "#d06a46", "#8a3a22")}${rg("mi-em", "#ffd27a", "#e0582a", 0.5, 0.5)}</defs>${shadow()}<path d="M28,46L40,104H80L92,46Z" fill="url(#mi-st)" ${O}/><path d="M24,42H96" stroke="${K}" stroke-width="8"/>
      <ellipse class="a-pulse" cx="60" cy="38" rx="30" ry="8" fill="url(#mi-em)"/><path d="M52,104V86Q60,78 68,86V104" fill="#2a1a12"/>
      <g class="a-pulse"><path d="M26,14L94,82M94,14L26,82" stroke="#e0362c" stroke-width="10" stroke-linecap="round"/></g>`,
    goout: `<defs>${lg("mi-dr", "#6b5236", "#3a2c22")}${lg("mi-lt", "#fff3c8", "#ffd27a", false)}</defs>${shadow()}<rect x="14" y="16" width="54" height="90" fill="#1b1714" ${O}/><path d="M18,20H50V102H18Z" fill="url(#mi-lt)" opacity=".85"/>
      <path d="M50,18L66,26V98L50,104Z" fill="url(#mi-dr)" ${O}/><g class="a-bob"><path d="M58,62H106M90,46L106,62L90,78" stroke="#2f9e5a" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,

    // ---------------- EP.3: after the gas ----------------
    doctor: `<defs>${lg("mi-dc", "#ffffff", "#e3e8ee")}${lg("mi-cr", "#ff6a52", "#c42418")}</defs>${shadow()}<rect x="16" y="16" width="88" height="88" rx="22" fill="url(#mi-dc)" ${O}/>
      <path class="a-pulse" d="M50,30H70V50H90V70H70V90H50V70H30V50H50Z" fill="url(#mi-cr)" ${O}/>${shine("M24,30q4,-10 16,-10v8q-10,0 -16,8z")}`,
    noback: `<defs>${lg("mi-nh", "#f1e6cc", "#cdb88a")}${lg("mi-nr", "#8a4a32", "#5a2e20")}</defs>${shadow()}<path d="M26,62V104H94V62Z" fill="url(#mi-nh)" ${O}/><path d="M16,66L60,28L104,66Z" fill="url(#mi-nr)" ${O}/>
      <rect x="50" y="74" width="20" height="30" fill="#1b1714"/><path d="M14,88H46M34,78L46,88L34,98" stroke="#3a5a8a" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>${NO}`,
    breath: `<defs>${rg("mi-lu", "#ffc2c2", "#d8585a")}</defs>${shadow()}<path d="M56,22V56M64,22V56M56,52L44,60M64,52L76,60" stroke="${K}" stroke-width="6" stroke-linecap="round" fill="none"/>
      <g class="a-pulse"><path d="M52,50Q28,40 20,74Q18,100 50,98Q56,80 52,50Z" fill="url(#mi-lu)" ${O}/><path d="M68,50Q92,40 100,74Q102,100 70,98Q64,80 68,50Z" fill="url(#mi-lu)" ${O}/></g>
      <path d="M92,20l10,-8M100,30l14,-4" stroke="#e0362c" stroke-width="5" stroke-linecap="round"/>`,
    confused: `${face("mi-cf", "#f6d2b0", "#d79a70")}<path d="M44,64h8M66,62l8,4M48,86q8,-5 16,0" stroke="${K}" stroke-width="5" stroke-linecap="round" fill="none"/>
      <g class="a-bob"><text x="98" y="40" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#e0362c" stroke="${K}" stroke-width="1.5">?</text></g><g class="a-bob2"><text x="22" y="34" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="26" fill="#f2c23a" stroke="${K}" stroke-width="1.5">?</text></g>`,
    faint: `<defs>${rg("mi-ft", "#f6d2b0", "#d79a70")}${lg("mi-fb", "#f2c23a", "#c48a1a")}</defs>${shadow(60, 100, 46)}<path d="M10,96H110" stroke="${K}" stroke-width="5"/>
      <circle cx="28" cy="78" r="15" fill="url(#mi-ft)" ${O}/><path d="M42,72H100V90H42Z" fill="url(#mi-fb)" ${O}/><path d="M22,76l6,4M30,76l-6,4" stroke="${K}" stroke-width="3"/>
      ${[0, 1, 2].map((i) => `<text class="a-wave" data-i="${i}" x="${54 + i * 16}" y="${56 - i * 14}" font-family="Kanit" font-weight="900" font-size="${18 + i * 5}" fill="#2f7fbf">z</text>`).join("")}`,
    call1669: `<defs>${lg("mi-ph", "#3a3f47", "#14171b")}${lg("mi-sc", "#ffffff", "#dfe8f0")}</defs>${shadow()}<g class="a-shake"><rect x="34" y="12" width="52" height="96" rx="12" fill="url(#mi-ph)" ${O}/>
      <rect x="40" y="24" width="40" height="64" rx="4" fill="url(#mi-sc)"/><text x="60" y="62" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="18" fill="#e0362c">1669</text><circle cx="60" cy="98" r="5" fill="#fff"/></g>
      ${[0, 1].map((i) => `<path class="a-wave" data-i="${i}" d="M${94 + i * 8},${40 - i * 6}q${8 + i * 3},${16 + i * 4} 0,${32 + i * 10}M${26 - i * 8},${40 - i * 6}q${-8 - i * 3},${16 + i * 4} 0,${32 + i * 10}" stroke="#2f9e5a" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}`,
    nodrive: `${WH}${shadow()}${wheel(60, 60, 34)}${NO}`,
    otherdrive: `${WH}${shadow()}${wheel(54, 64, 32)}<g class="a-pulse"><circle cx="92" cy="30" r="20" fill="#2f9e5a" ${O}/><path d="M82,30l7,7l13,-14" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
    ambulance: `<defs>${lg("mi-am", "#ffffff", "#d8dee6")}</defs>${shadow(60, 104, 44)}<g class="a-bob"><path d="M8,42H72V88H8Z" fill="url(#mi-am)" ${O}/><path d="M72,54H96L112,72V88H72Z" fill="url(#mi-am)" ${O}/>
      <path d="M78,58H94L104,72H78Z" fill="#9fd0f0" ${O}/><path d="M40,52V80M26,66H54" stroke="#e0362c" stroke-width="9"/><path d="M8,80H112" stroke="#e0362c" stroke-width="4"/>
      <circle cx="28" cy="92" r="10" fill="${K}"/><circle cx="92" cy="92" r="10" fill="${K}"/><circle cx="28" cy="92" r="4" fill="#9aa2aa"/><circle cx="92" cy="92" r="4" fill="#9aa2aa"/>
      <g class="a-pulse"><rect x="30" y="30" width="20" height="12" rx="4" fill="#2f7fbf"/><circle cx="40" cy="30" r="12" fill="#7fd1ff" opacity=".45"/></g></g>`,
  };
  Object.assign(GameUI.ILL, ICONS);

  // glossy step badges with a coloured rim per step and a light sweep across each (GSAP-driven so renders are frame-exact)
  document.head.insertAdjacentHTML("beforeend", `<style>
    .steps .ic { background: radial-gradient(circle at 34% 28%, #ffffff 0%, #f6efdd 38%, #dccba2 100%); border: 4px solid ${K};
      box-shadow: 0 0 0 5px #f2c23a, 0 0 22px rgba(242,194,58,.55), inset 0 -8px 14px rgba(120,90,40,.28), 0 10px 18px rgba(0,0,0,.5); position: relative; overflow: hidden; }
    .steps .st:nth-child(3) .ic { box-shadow: 0 0 0 5px #7fd1ff, 0 0 22px rgba(127,209,255,.5), inset 0 -8px 14px rgba(120,90,40,.28), 0 10px 18px rgba(0,0,0,.5); }
    .steps .st:nth-child(5) .ic { box-shadow: 0 0 0 5px #ff8a7a, 0 0 22px rgba(255,138,122,.5), inset 0 -8px 14px rgba(120,90,40,.28), 0 10px 18px rgba(0,0,0,.5); }
    .steps .st:nth-child(7) .ic { box-shadow: 0 0 0 5px #9be0a8, 0 0 22px rgba(155,224,168,.5), inset 0 -8px 14px rgba(120,90,40,.28), 0 10px 18px rgba(0,0,0,.5); }
    .steps .ic .shn { position: absolute; left: -30%; top: -30%; width: 160%; height: 160%; pointer-events: none;
      background: linear-gradient(115deg, transparent 42%, rgba(255,255,255,.7) 50%, transparent 58%); transform: translateX(-160%); }
    .steps .ic svg { position: relative; }
  </style>`);
  const S0 = GameUI.C.steps;
  GameUI.C.steps = {
    html: (id, o) => S0.html(id, o).replace(/<div class="ic">/g, '<div class="ic"><i class="shn"></i>'),
    anim(tl, id, t0, o) {
      S0.anim(tl, id, t0, o);
      const end = o.t0abs + (o.end ?? o.t + 3.5), n = Math.max(1, Math.ceil((end - t0) / 2.4));
      document.querySelectorAll(`#${id} .shn`).forEach((el, i) => tl.fromTo(el, { xPercent: -160 }, { xPercent: 160, duration: 0.9, repeat: n, repeatDelay: 1.5, ease: "power1.inOut", immediateRender: false }, t0 + 0.6 + i * 0.25));
    },
  };
})();
