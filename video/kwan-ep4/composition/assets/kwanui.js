// Card icons for "ควันหลง" (GameUI.ILL, 120×120): shaded fills, a highlight, a soft ground shadow and one moving part each
// (gameui.js loops: a-pulse a-bob a-bob2 a-sway a-shake a-spin a-wave[data-i] a-draw). Loaded after gameui.js and mokui.js.
// Also KwanUI.countdown(root, tl, t0, t1, from): the two-minute ring in the top corner that runs across the shots.
(function () {
  const K = "#2e2a26", O = `stroke="${K}" stroke-width="4" stroke-linejoin="round"`;
  const lg = (id, a, b, v = true) => `<linearGradient id="${id}" x1="0" y1="0" x2="${v ? 0 : 1}" y2="${v ? 1 : 0}"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient>`;
  const rg = (id, a, b, cx = 0.38, cy = 0.32) => `<radialGradient id="${id}" cx="${cx}" cy="${cy}" r=".75"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></radialGradient>`;
  const shadow = (cx = 60, cy = 108, rx = 34) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="6" fill="#000" opacity=".18"/>`;
  const shine = (d) => `<path d="${d}" fill="#fff" opacity=".38"/>`;
  const NO = `<g class="a-pulse"><circle cx="60" cy="60" r="50" fill="none" stroke="#e0362c" stroke-width="9"/><path d="M25,25L95,95" stroke="#e0362c" stroke-width="9" stroke-linecap="round"/></g>`;
  const OK = `<g class="a-pulse"><circle cx="96" cy="24" r="17" fill="#3fb86a" ${O}/><path d="M88,24l6,6l11,-12" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`;
  const DOOR = `<defs>${lg("kw-dr", "#8a5a3a", "#5a3a24", false)}</defs><rect x="30" y="10" width="60" height="96" rx="4" fill="url(#kw-dr)" ${O}/><rect x="38" y="20" width="44" height="34" rx="3" fill="none" stroke="#4a2e1c" stroke-width="4"/><rect x="38" y="62" width="44" height="36" rx="3" fill="none" stroke="#4a2e1c" stroke-width="4"/>`;
  const FLAME = (x, y, s = 1, cls = "a-pulse") => `<g class="${cls}" transform="translate(${x},${y}) scale(${s})"><path d="M0,-34C14,-18 22,-6 18,8A18,18 0 0 1 -18,8C-22,-6 -10,-14 -6,-26C-2,-16 6,-14 0,-34Z" fill="url(#kw-fl)" ${O}/><path d="M0,-10C6,-2 8,4 6,10A6,6 0 0 1 -6,10C-8,4 -4,0 0,-10Z" fill="#fff4b0"/></g>`;
  const FL = `<defs>${lg("kw-fl", "#ffd24a", "#e8461c")}</defs>`;
  const SMOKE = (x, y, s = 1, cls = "a-bob") => `<g class="${cls}" transform="translate(${x},${y}) scale(${s})"><path d="M-34,10Q-48,8 -44,-6Q-40,-20 -24,-16Q-20,-34 0,-32Q20,-34 24,-16Q44,-18 44,0Q42,14 28,12Z" fill="url(#kw-sm)" ${O}/></g>`;
  const SM = `<defs>${rg("kw-sm", "#8a8580", "#3a3632")}</defs>`;

  const ICONS = {
    clock2: `<defs>${rg("kw-ck", "#fff6e0", "#e0cfa8")}</defs>${shadow()}<circle cx="60" cy="64" r="44" fill="url(#kw-ck)" ${O}/><rect x="52" y="8" width="16" height="14" rx="3" fill="#c8392b" ${O}/>
      <path d="M60,64L60,30" stroke="${K}" stroke-width="6" stroke-linecap="round"/><g class="a-spin"><circle cx="60" cy="64" r="40" fill="none"/><path d="M60,64L84,52" stroke="#e0362c" stroke-width="5" stroke-linecap="round"/></g>
      <path d="M60,24A40,40 0 0 1 100,64" stroke="#e0362c" stroke-width="7" fill="none" opacity=".6"/><text x="60" y="94" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="18" fill="${K}">2:00</text>`,
    knob: `<defs>${rg("kw-kn", "#ffe9a0", "#b8862a")}${lg("kw-sk", "#f6d2b0", "#d79a70")}</defs>${shadow()}<rect x="10" y="20" width="56" height="88" fill="#6e4a32" ${O}/>
      <circle cx="50" cy="64" r="16" fill="url(#kw-kn)" ${O}/>${shine("M42,56q4,-6 10,-6v5q-6,0 -10,4z")}
      <g class="a-bob"><circle cx="86" cy="62" r="22" fill="url(#kw-sk)" ${O}/><path d="M74,56q12,6 24,0M74,66q12,6 24,0" stroke="#cc9a74" stroke-width="3" fill="none"/></g>
      ${[0, 1, 2].map((i) => `<path class="a-wave" data-i="${i}" d="M${36 + i * 12},28q-6,-8 0,-14q6,-6 0,-12" stroke="#e8461c" stroke-width="4" fill="none" stroke-linecap="round"/>`).join("")}`,
    doorhot: `${FL}${shadow()}${DOOR}<rect x="30" y="100" width="60" height="6" fill="#ffb04a"/>${FLAME(96, 96, 0.8)}${FLAME(22, 100, 0.6, "a-bob")}
      <circle cx="80" cy="62" r="6" fill="#c9a24a" ${O}/><g class="a-pulse"><rect x="30" y="10" width="60" height="96" rx="4" fill="#ff5a2a" opacity=".22"/></g>`,
    smokegap: `${SM}${shadow()}${DOOR}<circle cx="80" cy="62" r="6" fill="#c9a24a" ${O}/>${[0, 1, 2].map((i) => `<path class="a-wave" data-i="${i}" d="M${40 + i * 16},104q-8,-10 0,-18q8,-8 0,-16" stroke="#6a6560" stroke-width="7" fill="none" stroke-linecap="round" opacity=".85"/>`).join("")}`,
    keepshut: `${shadow()}${DOOR}<circle cx="80" cy="62" r="6" fill="#c9a24a" ${O}/><g class="a-pulse"><rect x="20" y="44" width="80" height="30" rx="8" fill="#e0362c" ${O}/><text x="60" y="66" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="20" fill="#fff">ห้ามเปิด</text></g>`,
    exit2: `<defs>${lg("kw-ex", "#3fd07a", "#1f8a4a")}</defs>${shadow()}<rect x="12" y="22" width="96" height="74" rx="10" fill="url(#kw-ex)" ${O}/>
      <g class="a-bob"><circle cx="50" cy="38" r="8" fill="#fff"/><path d="M48,48L40,66L52,72L48,86M44,60L58,58L66,66M40,66L30,74" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      <path d="M72,60H96M88,52L96,60L88,68" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>${shine("M18,28h50v6h-50z")}`,
    smokeskull: `${SM}${FL}${shadow()}${SMOKE(52, 42, 1.1, "a-bob")}<g transform="translate(52,40)"><circle cx="0" cy="-2" r="13" fill="#f4ecd8" ${O}/><circle cx="-5" cy="-3" r="3.5" fill="${K}"/><circle cx="5" cy="-3" r="3.5" fill="${K}"/><rect x="-6" y="9" width="12" height="7" fill="#f4ecd8" ${O}/></g>
      <text x="92" y="74" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="#e0362c">&gt;</text>${FLAME(96, 104, 0.55, "a-pulse")}`,
    smokeup: `${SM}${shadow()}<rect x="8" y="10" width="104" height="12" rx="3" fill="#cfc8b8" ${O}/>${SMOKE(60, 40, 1.15, "a-bob")}
      <g class="a-bob2"><path d="M60,104V64M46,78L60,62L74,78" stroke="#f2c23a" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
    crawl: `${SM}${shadow(60, 110, 44)}<rect x="6" y="14" width="108" height="34" rx="12" fill="url(#kw-sm)" opacity=".85" ${O}/><path d="M10,52H110" stroke="#e0362c" stroke-width="3" stroke-dasharray="6 5"/>
      <g class="a-sway"><circle cx="86" cy="70" r="10" fill="#f6d2b0" ${O}/><path d="M76,76L44,82L26,98M44,82L50,100M70,80L74,100" stroke="#5d6f8f" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
    closedoor: `${shadow()}<rect x="24" y="12" width="64" height="96" fill="#1e1a17" ${O}/><g class="a-sway"><path d="M26,14L74,24V100L26,108Z" fill="#8a5a3a" ${O}/><circle cx="66" cy="62" r="5" fill="#c9a24a" ${O}/></g>
      <path d="M100,40A30,30 0 0 1 100,84" stroke="#3fb86a" stroke-width="6" fill="none"/><path d="M94,80L100,90L108,80" stroke="#3fb86a" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
    cloth: `<defs>${lg("kw-tw", "#f4ead2", "#cdbb92")}</defs>${shadow(60, 110, 46)}<rect x="14" y="6" width="92" height="84" fill="#6e4a32" ${O}/>
      <g class="a-bob"><path d="M8,88Q60,78 112,88L114,106Q60,98 6,106Z" fill="url(#kw-tw)" ${O}/><path d="M20,96H100" stroke="#c9b48a" stroke-width="4"/></g>`,
    nosmoke: `${SM}${shadow()}${SMOKE(60, 62, 1.1, "a-wave")}${NO}`,
    call199: `<defs>${lg("kw-ph", "#3a4250", "#14171c")}</defs>${shadow()}<g class="a-shake"><rect x="34" y="10" width="52" height="96" rx="10" fill="url(#kw-ph)" ${O}/><rect x="40" y="20" width="40" height="70" rx="5" fill="#b8261c"/>
      <text x="60" y="62" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="20" fill="#fff">199</text><path d="M52,74h16" stroke="#fff" stroke-width="3"/></g>
      ${[0, 1].map((i) => `<path class="a-wave" data-i="${i}" d="M${94 + i * 9},${40 - i * 4}q8,10 0,22" stroke="#f2c23a" stroke-width="5" fill="none" stroke-linecap="round"/><path class="a-wave" data-i="${i}" d="M${26 - i * 9},${40 - i * 4}q-8,10 0,22" stroke="#f2c23a" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}`,
    pin: `<defs>${rg("kw-pn", "#ff8a7a", "#c8261c")}</defs>${shadow(60, 110, 24)}<g class="a-bob"><path d="M60,104C40,76 24,60 24,42A36,36 0 0 1 96,42C96,60 80,76 60,104Z" fill="url(#kw-pn)" ${O}/>
      <circle cx="60" cy="42" r="20" fill="#fff" ${O}/><text x="60" y="49" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="17" fill="${K}">714</text></g>${shine("M34,34q6,-16 22,-18q-12,8 -16,22z")}`,
    torchwave: `<defs>${lg("kw-bm", "#fff6dc", "#fff6dc", false)}${lg("kw-sk2", "#f6d2b0", "#d79a70")}</defs>${shadow()}<rect x="8" y="10" width="104" height="96" rx="6" fill="#16202e" ${O}/><path d="M60,10V106M8,58H112" stroke="#8a9296" stroke-width="5"/>
      <g class="a-sway"><path d="M60,92L22,22H46Z" fill="#fff6dc" opacity=".55"/><rect x="52" y="78" width="16" height="26" rx="4" fill="#2c3038" ${O}/><circle cx="60" cy="80" r="4" fill="#fffbe8"/><circle cx="60" cy="100" r="12" fill="url(#kw-sk2)" ${O}/></g>`,
    lightcloth: `<defs>${lg("kw-lc", "#ffffff", "#d8dde4")}</defs>${shadow()}<rect x="8" y="10" width="104" height="96" rx="6" fill="#16202e" ${O}/><path d="M24,24V100" stroke="#8a9296" stroke-width="6" stroke-linecap="round"/>
      <g class="a-wave" data-i="0"><path d="M26,28Q60,18 100,30Q86,50 100,72Q60,62 26,70Z" fill="url(#kw-lc)" ${O}/></g>`,
  };
  Object.assign(GameUI.ILL, ICONS);

  // the two-minute countdown ring (top right), running from t0 to t1 on the main timeline; hidden with KwanUI.hide(tl, a, b)
  function countdown(root, tl, t0, t1, from = 120) {
    root.insertAdjacentHTML("beforeend", `<div id="kwcd" style="position:absolute;right:34px;top:150px;z-index:57;width:190px;height:190px;opacity:0;font-family:Kanit;pointer-events:none">
      <svg width="190" height="190" viewBox="0 0 190 190" style="position:absolute;inset:0"><circle cx="95" cy="95" r="84" fill="rgba(10,8,7,.72)" stroke="rgba(244,236,216,.25)" stroke-width="3"/>
        <circle id="kwcd-ring" cx="95" cy="95" r="74" fill="none" stroke="#ff5a3a" stroke-width="12" stroke-linecap="round" transform="rotate(-90 95 95)" stroke-dasharray="465 465" stroke-dashoffset="0"/></svg>
      <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
        <b id="kwcd-t" style="font:900 52px/1 Kanit;color:#fff4ea;letter-spacing:-1px;text-shadow:0 2px 8px #000">2:00</b>
        <span style="font:700 19px/1 Kanit;color:#ffb09a;margin-top:6px;letter-spacing:1px">ก่อนอันตราย</span></div></div>`);
    const c = { s: from }, t = document.getElementById("kwcd-t"), ring = document.getElementById("kwcd-ring");
    tl.fromTo("#kwcd", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0);
    tl.fromTo(c, { s: from }, { s: 0, duration: t1 - t0, ease: "none", immediateRender: false, onUpdate: () => {
      const v = Math.max(0, Math.ceil(c.s)); t.textContent = `${Math.floor(v / 60)}:${String(v % 60).padStart(2, "0")}`;
      ring.setAttribute("stroke-dashoffset", (465 * (1 - c.s / from)).toFixed(1));
      ring.setAttribute("stroke", c.s < 30 ? "#ff2a1a" : "#ff5a3a");
    } }, t0);
    // the last 20 s: the ring pulses
    for (let u = t1 - 20 * (t1 - t0) / from; u < t1; u += 0.5) tl.fromTo("#kwcd", { scale: 1.08 }, { scale: 1, duration: 0.3, ease: "power2.out", immediateRender: false }, u);
  }
  function hide(tl, a, b) { tl.to("#kwcd", { opacity: 0, duration: 0.15 }, a); if (b !== undefined) tl.to("#kwcd", { opacity: 1, duration: 0.2 }, b); }

  window.KwanUI = { countdown, hide, ICONS };
})();
