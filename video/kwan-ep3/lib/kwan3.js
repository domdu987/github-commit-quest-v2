// Sets for "ควันหลง" EP.3 ลิฟต์มารับ (loaded after kwan2.js):
//   Sets.liftFloor    your eyes looking down: your bare foot over the lift's threshold, ดาว's burnt feet in the light inside
//   Sets.liftPanel    the floor display over the lift (#id-n1 … #id-n7, one shown at a time) and the down arrow
//   Sets.stairwell    the fire stairs side on: switchback flights between landings (floor 7 at y 0, 6 at 900, 5 at 1800,
//                     4 at 2700), a floor sign and a fire door on each landing, smoke; #id-tile is the burning ceiling panel
//   Sets.stairwellUp  your torch up the stairwell well: railings receding up, ดาว hanging upside down at the top (#id-dao)
//   Sets.landing      a landing wall: the big floor number (#id-s4 … #id-s7, o.show), the fire door with a small window
//                     (#id-win eyes), the 714 key on a hook (#id-key, swings), the knob (#id-knob)
// Card icons for EP.3: stairs, nolift, firefighter, stopnow, dropdown, coverface, rollover.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const LAVA = "#ff6a1a", CH = "#1b1512";

  // ---------------- your foot over the threshold ----------------
  Sets.liftFloor = function (L, o) {
    const id = o.id || "lf";
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#090a0a"/>`);
    let s = `<rect x="-600" y="1100" width="2300" height="1400" fill="url(#k2Floor)"/><rect x="-600" y="-400" width="2300" height="1520" fill="#f2deb0"/>
      <path d="M-600,1080H1700V1130H-600Z" fill="url(#k2Steel)" ${OUT3}/>${[0, 1, 2, 3, 4, 5, 6, 7].map((k) => `<path d="M${-500 + k * 300},1086V1124" stroke="#6a7076" stroke-width="5"/>`).join("")}
      <path d="M-600,-400H1700V1080H-600Z" fill="#fff4d8" opacity=".35"/>`;
    // ดาว's burnt feet inside, just past the threshold
    s += `<g transform="translate(560,700)"><path d="M-70,-600L-62,-40M70,-600L62,-40" stroke="${CH}" stroke-width="44" stroke-linecap="round"/><path class="flk" d="M-66,-400l8,30l-6,24M66,-300l-8,30" stroke="${LAVA}" stroke-width="5" fill="none"/>
        <path d="M-110,-30Q-70,-60 -30,-30L-20,10H-120Z" fill="${CH}"/><path d="M30,-30Q70,-60 110,-30L120,10H20Z" fill="${CH}"/>${[-112, -96, -80, 26, 42, 58].map((x) => `<circle cx="${x + 14}" cy="10" r="7" fill="${CH}"/>`).join("")}</g>`;
    put(L.set, s);
    // your foot and shin from the bottom (pyjama hem, bare foot), stepping over the steel strip
    put(L.act, `<g id="${id}-foot" transform="translate(0,0)"><path d="M380,2400L420,1500" stroke="${INK}" stroke-width="230" stroke-linecap="round"/><path d="M380,2400L420,1500" stroke="#5d6f8f" stroke-width="218" stroke-linecap="round"/>
        <rect x="300" y="1440" width="240" height="70" rx="20" fill="#7f91b2" ${OUT}/><path d="M340,1500C330,1300 360,1150 470,1100C560,1060 640,1090 640,1150C640,1230 560,1300 520,1500Z" fill="#ecc19a" ${OUT}/>
        ${[0, 1, 2, 3, 4].map((k) => `<ellipse cx="${500 + k * 26}" cy="${1090 - (k === 0 ? 6 : 0) + k * 6}" rx="${k === 0 ? 20 : 13}" ry="${k === 0 ? 24 : 16}" fill="#ecc19a" ${OUT3}/>`).join("")}</g>`);
    put(L.glow, `<circle cx="560" cy="600" r="900" fill="url(#k2Warm)" opacity=".6"/>`);
  };

  // ---------------- the floor display ----------------
  Sets.liftPanel = function (L, o) {
    const id = o.id || "lp";
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#0c0e0e"/>`);
    let s = `<rect x="-600" y="-400" width="2300" height="2800" fill="url(#k2Wall)"/><rect x="-600" y="1300" width="2300" height="1200" fill="url(#k2Steel)"/><path d="M540,1300V2500" stroke="#3a3e42" stroke-width="10"/>
      <rect x="140" y="560" width="800" height="560" rx="40" fill="#140a08" ${OUT}/><rect x="180" y="600" width="720" height="480" rx="24" fill="#0a0504"/>`;
    for (let n = 1; n <= 7; n++) s += `<text id="${id}-n${n}" x="640" y="1010" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="420" fill="#ff4a2a" opacity="${n === (o.n ?? 7) ? 1 : 0}">${n}</text>`;
    s += `<g id="${id}-dn"><path d="M300,760L380,880L460,760Z" fill="#ff4a2a"/></g><g id="${id}-up" opacity="0"><path d="M300,900L380,780L460,900Z" fill="#ff4a2a"/></g>`;
    put(L.set, s + Pov.smoke(mk(3), { x0: -800, x1: 1900, y0: -900, y1: 420, n: 10, op: 0.85 }));
    put(L.glow, `<circle cx="540" cy="840" r="600" fill="url(#k2Red)" opacity=".5"/>`);
  };

  // ---------------- the fire stairs, side on ----------------
  const LY = [0, 900, 1800, 2700]; // landings of floors 7, 6, 5, 4
  Sets.stairwell = function (L, o) {
    const id = o.id || "sw", r = mk(o.seed || 61);
    put(L.sky, `<rect x="-1500" y="-2000" width="4100" height="7000" fill="#0d0f0f"/>`);
    let s = `<rect x="-800" y="-1500" width="2700" height="5600" fill="#2c3332"/>`;
    for (let y = -1400; y < 4000; y += 120) s += `<path d="M-800,${y}H1900" stroke="#262c2b" stroke-width="4"/>`;
    LY.forEach((y, k) => {
      const fl = 7 - k;
      // the landing (left) with its fire door and floor number; the half landing on the right (760…1660, room to lie down and roll)
      s += `<rect x="-300" y="${y}" width="620" height="60" fill="#5a5e5c" ${OUT}/><rect x="-200" y="${y - 760}" width="300" height="760" fill="#3a4a42" ${OUT}/><rect x="-170" y="${y - 700}" width="100" height="140" fill="#7a9a8a" opacity=".45"/>
        <text x="230" y="${y - 420}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="220" fill="#d8d0b8" opacity=".85">${fl}</text>
        <rect x="760" y="${y + 450}" width="900" height="50" fill="#5a5e5c" ${OUT}/>`;
      // flight down to the right half landing, then back down to the left
      const steps = (x0, y0, x1, y1) => { let p = `M${x0},${y0}`; const n = 9, dx = (x1 - x0) / n, dy = (y1 - y0) / n; for (let j = 0; j < n; j++) p += `h${f1(dx)}v${f1(dy)}`; return `<path d="${p}V${y1 + 80}L${x0},${y0 + 80}Z" fill="#4a4e4c" ${OUT3}/>`; };
      if (k < LY.length - 1) {
        s += steps(320, y, 760, y + 450) + steps(760, y + 450, 320, y + 900).replace("#4a4e4c", "#3e4240");
        s += `<path d="M320,${y - 120}L760,${y + 330}" stroke="#8a6a3a" stroke-width="12"/><path d="M760,${y + 330}L320,${y + 780}" stroke="#7a5a32" stroke-width="12" opacity=".7"/>`;
      }
    });
    s += `<g id="${id}-tile" opacity="0" transform="translate(0,0)"><rect x="380" y="560" width="220" height="40" fill="#5a4a3a" ${OUT3}/>${[0, 1, 2].map((k) => `<path class="flk" d="M${400 + k * 70},560q20,-50 6,-90q30,40 14,90z" fill="#ff9a3a"/>`).join("")}</g>`;
    put(L.set, s + Pov.smoke(r, { x0: -900, x1: 2000, y0: -1600, y1: o.smokeY ?? -300, n: 20, op: 0.85 }) + Pov.embers(r, { n: 14, x0: 0, x1: 1200, y0: 0, y1: 1800 }));
    put(L.glow, LY.map((y) => `<circle cx="-50" cy="${y - 820}" r="160" fill="url(#k2Exit)"/>`).join(""));
  };

  // ---------------- up the stairwell well ----------------
  Sets.stairwellUp = function (L, o) {
    const id = o.id || "su";
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#050606"/>`);
    let s = "";
    for (let k = 9; k >= 1; k--) {
      const w = 1100 / k, h = 1500 / k, x = 540 - w / 2, y = 900 - h / 2;
      s += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h)}" fill="none" stroke="${k % 2 ? "#4a4e4c" : "#3a3e3c"}" stroke-width="${f1(70 / k)}"/>
        <rect x="${f1(x - 30 / k)}" y="${f1(y - 30 / k)}" width="${f1(w + 60 / k)}" height="${f1(h + 60 / k)}" fill="none" stroke="#8a6a3a" stroke-width="${f1(14 / k)}" opacity=".7"/>`;
    }
    s += `<g id="${id}-dao" transform="translate(540,640) scale(-0.5,-0.5)">${Kwan.daoStand(`${id}-d`)}</g>`;
    put(L.set, s + Pov.smoke(mk(9), { x0: -800, x1: 1900, y0: -900, y1: 500, n: 12, op: 0.6 }));
  };

  // ---------------- a landing ----------------
  Sets.landing = function (L, o) {
    const id = o.id || "ld", r = mk(o.seed || 71);
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#0d0f0f"/>`);
    let s = `<rect x="-600" y="-400" width="2300" height="2000" fill="#2c3332"/><rect x="-600" y="1560" width="2300" height="900" fill="#3a3e3c"/><rect x="-600" y="1530" width="2300" height="40" fill="#1e2423"/>`;
    for (let y = -300; y < 1560; y += 120) s += `<path d="M-600,${y}H1700" stroke="#262c2b" stroke-width="4"/>`;
    // the fire door and its little window
    s += `<rect x="460" y="560" width="440" height="1000" fill="#3a4a42" ${OUT}/><rect x="520" y="640" width="150" height="200" fill="#0a0c0c" ${OUT3}/><g id="${id}-win" opacity="0"><ellipse cx="575" cy="730" rx="12" ry="5" fill="#ffd27a"/><ellipse cx="615" cy="732" rx="12" ry="5" fill="#ffd27a"/><circle cx="595" cy="731" r="44" fill="${LAVA}" opacity=".2"/></g>
      <rect x="490" y="1050" width="380" height="50" rx="10" fill="#8a9096" ${OUT3}/><circle id="${id}-knob" cx="840" cy="1180" r="0" fill="none"/>`;
    // the big floor number on the wall (one shown)
    [4, 5, 6, 7].forEach((n) => (s += `<g id="${id}-s${n}" opacity="${(o.show ?? 7) === n ? 1 : 0}"><text x="220" y="1040" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="460" fill="#d8d0b8" opacity=".9">${n}</text><text x="220" y="1180" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="90" fill="#d8d0b8" opacity=".75">ชั้น ${n}</text></g>`));
    // the 714 key on a hook by the door
    if (o.key) s += `<path d="M980,820v30" stroke="#8a9096" stroke-width="8"/><g id="${id}-key" transform="rotate(0 980 850)"><circle cx="980" cy="870" r="18" fill="none" stroke="#c9a24a" stroke-width="7"/>
        <path d="M980,888l-50,70l50,110l50,-110Z" fill="#c8392b" ${OUT}/><text x="980" y="990" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#fff4ea" transform="rotate(-8 980 980)">714</text></g>`;
    put(L.set, s + Pov.smoke(r, { x0: -800, x1: 1900, y0: -900, y1: o.smokeY ?? 260, n: 12, op: 0.85 }));
    put(L.glow, `<circle cx="680" cy="420" r="300" fill="url(#k2Exit)"/><g id="${id}-under" opacity="${o.under ?? 0}"><rect x="470" y="1548" width="420" height="12" fill="#ffb04a"/><ellipse cx="680" cy="1580" rx="320" ry="60" fill="url(#kwGapPool)"/></g>`);
  };

  // ---------------- a source footnote under a knowledge card (GameUI.C.src) ----------------
  if (window.GameUI && !GameUI.C.src) {
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

  // ---------------- card icons for EP.3 ----------------
  if (window.GameUI) {
    const K = INK, O = `stroke="${K}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"`;
    const SH = `<ellipse cx="60" cy="108" rx="34" ry="6" fill="#000" opacity=".18"/>`;
    const NO = `<g class="a-pulse"><circle cx="60" cy="60" r="50" fill="none" stroke="#e0362c" stroke-width="9"/><path d="M25,25L95,95" stroke="#e0362c" stroke-width="9" stroke-linecap="round"/></g>`;
    Object.assign(GameUI.ILL, {
      stairs: `${SH}<path d="M14,100H40V78H62V56H84V34H106V100Z" fill="#3fb86a" ${O}/><g class="a-bob"><circle cx="30" cy="40" r="9" fill="${K}"/><path d="M30,50L26,70M26,70L38,78M26,70L18,82M28,56L40,52M28,56L18,62" stroke="${K}" stroke-width="6" fill="none" stroke-linecap="round"/></g>`,
      nolift: `${SH}<rect x="26" y="14" width="68" height="90" rx="6" fill="#b8bec4" ${O}/><path d="M60,14V104" stroke="${K}" stroke-width="4"/><path d="M44,30l8,-10l8,10M44,36l8,10l8,-10" stroke="${K}" stroke-width="3" fill="none" transform="translate(8,0)"/>${NO}`,
      firefighter: `${SH}<path d="M18,70Q20,28 60,26Q100,28 102,70Z" fill="#e8b830" ${O}/><path d="M10,70H110L104,82H16Z" fill="#c4931c" ${O}/><rect x="48" y="38" width="24" height="22" rx="4" fill="#c8392b" ${O}/><g class="a-pulse"><path d="M60,92v14" stroke="#3fb86a" stroke-width="6" stroke-linecap="round"/></g>`,
      stopnow: `${SH}<g class="a-pulse"><path d="M40,14H80L106,40V80L80,106H40L14,80V40Z" fill="#e0362c" ${O}/><text x="60" y="72" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="28" fill="#fff">หยุด</text></g>`,
      dropdown: `${SH}<g class="a-bob"><circle cx="24" cy="84" r="10" fill="#e9bc93" ${O}/><path d="M34,88H96" stroke="#7fb3a0" stroke-width="18" stroke-linecap="round"/></g><path d="M70,20V52M58,40L70,54L82,40" stroke="#3fb86a" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
      coverface: `${SH}<circle cx="60" cy="60" r="34" fill="#e9bc93" ${O}/><g class="a-bob"><path d="M28,70C26,40 40,30 52,36L54,76Z" fill="#e9bc93" ${O}/><path d="M92,70C94,40 80,30 68,36L66,76Z" fill="#e9bc93" ${O}/></g>`,
      rollover: `${SH}<g class="a-spin"><circle cx="60" cy="60" r="30" fill="none" stroke="#7fb3a0" stroke-width="10" stroke-dasharray="60 30"/></g><circle cx="60" cy="60" r="12" fill="#e9bc93" ${O}/><path d="M86,30l10,-4l-2,12" stroke="#3fb86a" stroke-width="5" fill="none" stroke-linecap="round"/>`,
    });
  }
})();
