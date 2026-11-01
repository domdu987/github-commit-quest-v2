// Sets for เอาชีวิตรอด 99 วัน EP.7 "คนไร้ประโยชน์" (on top of estate.js): คุณวิน's office seen through its lit window from the
// first-floor walkway at night (the team photo where everyone wears the red scarf, the second radio, the desk drawn over the
// seated rig by the shot), his notebook open at ปั้น's row ("→ ภาระ"), ปั้น's drawing of เจ๊หงส์ behind bars beside a fridge,
// and the bars of the dormitory window for the first-person look across the yard. ภู with the red scarf = Rig.CAST.phuR.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const O = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);
  const T = (x, y, txt, size, col, o = {}) => `<text x="${x}" y="${y}" text-anchor="${o.anchor || "middle"}" font-family="Kanit" font-weight="${o.w || 900}" font-size="${size}" fill="${col}"${o.extra || ""}>${txt}</text>`;
  const SCARF = `<path d="M-40,-486Q0,-456 40,-486Q30,-460 0,-450Q-30,-460 -40,-486Z" fill="#c8392b" stroke="#2e2a26" stroke-width="3"/>`;
  const KNOT = `<path d="M8,-462q16,10 10,44l-12,-2q2,-24 -10,-34z" fill="#b02e22" stroke="#2e2a26" stroke-width="3"/>`;

  // ภู with the red scarf of คุณวิน's men knotted at his throat (EP.7, midnight)
  Rig.CAST.phuR = { ...Rig.CAST.phu, torsoExtra: (Rig.CAST.phu.torsoExtra || "") + SCARF + KNOT };

  Sets.DEFS += `
    <linearGradient id="oWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#363b46"/><stop offset="1" stop-color="#262a33"/></linearGradient>
    <radialGradient id="oLamp" cx=".5" cy=".3" r=".8"><stop offset="0" stop-color="#ffe9b8"/><stop offset=".55" stop-color="#e9c88c"/><stop offset="1" stop-color="#9a7a52"/></radialGradient>
    <radialGradient id="oPool"><stop offset="0" stop-color="#ffd58a" stop-opacity=".55"/><stop offset=".5" stop-color="#ffc06a" stop-opacity=".18"/><stop offset="1" stop-color="#ffc06a" stop-opacity="0"/></radialGradient>`;

  // the window of the office: x 150..930, y 520..1180 (the clip the shot puts the actors inside is `${id}-clip`)
  const WX0 = 150, WX1 = 930, WY0 = 520, WY1 = 1180;

  // the team photo on คุณวิน's wall: four of his men and him, every one with the red scarf; the second from the left is ภู
  // (cropped hair, the grey-green shirt with the reflective strip, the scar) — origin = centre of the frame, ~240 × 180
  function teamPhoto(x, y, s = 1) {
    const man = (cx, top, skin, hair, scarf = true, tie = false) => `<g transform="translate(${cx},0)"><path d="M-22,62q2,-30 22,-34q20,4 22,34z" fill="${top}" ${O(2)}/>${scarf ? `<path d="M-14,30q14,10 28,0l-4,12q-10,6 -20,0z" fill="#c8392b" ${O(1.5)}/>` : ""}${tie ? `<path d="M-3,30h6l3,22l-6,6l-6,-6z" fill="#c8392b" ${O(1.2)}/>` : ""}
      <circle cy="12" r="15" fill="${skin}" ${O(2)}/><path d="M-15,8q0,-20 15,-20q15,0 15,20q-6,-10 -15,-10q-9,0 -15,10z" fill="${hair}" ${O(1.5)}/></g>`;
    return `<g transform="translate(${x},${y}) scale(${s})"><rect x="-128" y="-96" width="256" height="192" fill="#6b4a2e" ${OUT}/><rect x="-114" y="-82" width="228" height="164" fill="#f4f2ea"/>
      <rect x="-104" y="-72" width="208" height="128" fill="#c9b48a"/><rect x="-104" y="20" width="208" height="36" fill="#8a7a5a" opacity=".6"/>
      <g transform="translate(0,-14)">${man(-76, 0, "#c48a5e", "#1c1816")}${man(-38, 0, "#c99a74", "#2a2420")}${man(0, 0, "#d9a57a", "#9aa0a6", false, true)}${man(38, 0, "#b47a50", "#1e1e1e")}${man(76, 0, "#c99064", "#2f3a52")}
        <path d="M-50,-8l6,-3" stroke="#7a4a3a" stroke-width="2"/><path d="M-60,30h44" stroke="#c9d0d4" stroke-width="3"/></g>
      ${T(0, 74, "ทีมนิคม · ปีแรก", 18, "#2e2a26", { w: 700 })}<path d="M-114,-82L114,82" stroke="#fff" stroke-opacity=".12" stroke-width="40"/></g>`;
  }

  // ======================================================================================================
  // 1. คุณวิน's office from the first-floor walkway at night: the dark outside wall, the big lit window (blinds half up), inside
  //    the warm back wall with the team photo, a calendar, the filing cabinet, the lamp and the radio on the desk; the desk's front
  //    panel is Estate7.DESK(id) put over the seated rig by the shot; the window frame and the walkway rail are in front
  // ======================================================================================================
  function officeNight(L, o = {}) {
    const id = o.id || "of", r = mk(o.seed || 81);
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#10141c"/>`);
    // the outside wall, with blocks and a drainpipe
    let w = `<rect x="-1400" y="-900" width="4000" height="3800" fill="url(#oWall)"/>${Array.from({ length: 28 }, (_, k) => `<path d="M-1400,${-900 + k * 120}H2600" stroke="#1e222a" stroke-width="3" opacity=".5"/>`).join("")}
      ${Array.from({ length: 60 }, () => `<circle cx="${f1(-600 + r() * 2300)}" cy="${f1(-200 + r() * 2400)}" r="${f1(2 + r() * 7)}" fill="#1a1d24" opacity="${f1(0.2 + r() * 0.3)}"/>`).join("")}
      <rect x="1010" y="-900" width="34" height="3800" fill="#4a505a" ${O(3)}/>${[200, 900, 1600].map((y) => `<rect x="1000" y="${y}" width="54" height="22" fill="#3a3f48" ${O(2)}/>`).join("")}`;
    put(L.far, w);
    // inside the window (clipped): back wall lit by the lamp, the photo, calendar, cabinet, the desk top with lamp, notebook, radio
    let s = `<clipPath id="${id}-clip"><rect x="${WX0}" y="${WY0}" width="${WX1 - WX0}" height="${WY1 - WY0}"/></clipPath><g clip-path="url(#${id}-clip)">
      <rect x="${WX0}" y="${WY0}" width="${WX1 - WX0}" height="${WY1 - WY0}" fill="url(#oLamp)"/><rect x="${WX0}" y="${WY1 - 120}" width="${WX1 - WX0}" height="120" fill="#7a5a3a" opacity=".55"/>
      ${teamPhoto(330, 700, 0.95)}
      <g transform="translate(620,690)"><rect x="-70" y="-90" width="140" height="170" fill="#f4f2ea" ${O(3)}/><rect x="-70" y="-90" width="140" height="34" fill="#c8392b"/>${T(0, -64, "ต.ค.", 22, "#f4f2ea")}
        ${Array.from({ length: 20 }, (_, k) => `<rect x="${-60 + (k % 5) * 25}" y="${-46 + Math.floor(k / 5) * 28}" width="18" height="18" fill="none" stroke="#9aa0a6" stroke-width="1.5"/>${k < 12 ? `<path d="M${-58 + (k % 5) * 25},${-44 + Math.floor(k / 5) * 28}l14,14M${-44 + (k % 5) * 25},${-44 + Math.floor(k / 5) * 28}l-14,14" stroke="#c8392b" stroke-width="2"/>` : ""}`).join("")}</g>
      <g transform="translate(860,1080)"><rect x="-80" y="-330" width="160" height="330" fill="#6f7880" ${OUT}/>${[0, 1, 2].map((k) => `<rect x="-66" y="${-316 + k * 106}" width="132" height="92" fill="#7d868c" ${O(2.5)}/><rect x="-20" y="${-280 + k * 106}" width="40" height="10" rx="4" fill="#3a3f45"/>`).join("")}</g>
      <rect x="${WX0}" y="1040" width="${WX1 - WX0}" height="40" fill="#5a3e24" ${O(3)}/>
      <g transform="translate(250,1040)"><path d="M-40,0h80l-10,-14h-60z" fill="#3a3f45" ${O(2)}/><path d="M0,-14L-20,-110L30,-150" stroke="#3a3f45" stroke-width="8" fill="none"/><path d="M10,-170l60,10l-20,50z" fill="#c8a85a" ${O(3)}/></g>
      <g transform="translate(470,1036) rotate(-3)"><rect x="-90" y="-26" width="180" height="26" fill="#f4ecd8" ${O(2)}/><path d="M0,-26V0" stroke="#8a7a5a" stroke-width="3"/>${[0, 1, 2].map((k) => `<path d="M${-80},${-20 + k * 6}h70M10,${-20 + k * 6}h70" stroke="#2f4a8a" stroke-width="1.5"/>`).join("")}</g>
      <g transform="translate(720,1040)"><rect x="-90" y="-100" width="180" height="100" rx="16" fill="#6b4a2e" ${OUT}/><rect x="-74" y="-84" width="90" height="50" rx="6" fill="#2a1a0a"/><g id="${id}-dialw"><rect x="-74" y="-84" width="90" height="50" rx="6" fill="#ffb35c" opacity=".75"/></g><rect x="-34" y="-80" width="3" height="42" fill="#ff3b30"/>
        <rect x="24" y="-84" width="52" height="68" rx="5" fill="#2a2420" ${O(2)}/>${Array.from({ length: 4 }, (_, k) => `<path d="M${30 + k * 12},-80v60" stroke="#c9a55a" stroke-width="3" opacity=".55"/>`).join("")}<circle cx="-50" cy="-18" r="10" fill="#c9a55a" ${O(2)}/><path d="M80,-100L130,-210" stroke="#9aa0a6" stroke-width="4"/></g>
    </g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="300" cy="920" r="460" fill="url(#oPool)"/><g id="${id}-dialg"><circle cx="700" cy="980" r="220" fill="url(#fDial)" opacity=".8"/></g>
      <path d="M${WX0},${WY1}L${WX0 - 220},2400H${WX1 + 260}L${WX1},${WY1}Z" fill="#ffd58a" opacity=".07"/>`);
    // the window frame with the blinds pulled half up and the sill (set layer, so it stays on the room); the walkway rail in front
    put(L.set, `<g><path d="M${WX0 - 40},${WY0 - 40}H${WX1 + 40}V${WY1 + 40}H${WX0 - 40}Z M${WX0},${WY0}V${WY1}H${WX1}V${WY0}Z" fill="#4a505a" fill-rule="evenodd" ${O(4)}/>
      <path d="M540,${WY0}V${WY1}" stroke="#4a505a" stroke-width="16"/><path d="M${WX0},${WY0}H${WX1}V${WY0 + 150}H${WX0}Z" fill="#d9cfb8" ${O(3)}/>${Array.from({ length: 7 }, (_, k) => `<path d="M${WX0},${WY0 + 10 + k * 21}H${WX1}" stroke="#b8ad94" stroke-width="4"/>`).join("")}
      <path d="M${WX0 + 30},${WY0 + 160}L${WX0 + 300},${WY1 - 40}" stroke="#fff" stroke-opacity=".07" stroke-width="60"/><rect x="${WX0 - 70}" y="${WY1 + 30}" width="${WX1 - WX0 + 140}" height="34" fill="#5a606a" ${O(3)}/></g>`);
    put(L.fg, `<g><path d="M-1400,1560H2600M-1400,1700H2600" stroke="#6f7880" stroke-width="18"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-1400 + k * 140},1560V1900" stroke="#5b6066" stroke-width="12"/>`).join("")}<rect x="-1400" y="1880" width="4000" height="1200" fill="#1a1d24"/></g>`);
  }
  // the desk's front panel, put over คุณวิน seated behind it (inside the window clip — the shot wraps both in `${id}-clip`)
  const DESK = (id) => `<g><rect x="${WX0 + 120}" y="1068" width="560" height="200" fill="#4e3620" ${OUT}/><rect x="${WX0 + 140}" y="1090" width="250" height="70" fill="#5a3e24" ${O(2.5)}/><rect x="${WX0 + 410}" y="1090" width="250" height="70" fill="#5a3e24" ${O(2.5)}/>
    <rect x="${WX0 + 245}" y="1120" width="40" height="10" rx="4" fill="#c9a55a"/><rect x="${WX0 + 515}" y="1120" width="40" height="10" rx="4" fill="#c9a55a"/></g>`;

  // ======================================================================================================
  // 2. คุณวิน's notebook at the register again (EP.6's page with ยายจันทร์ struck out), ปั้น's row circled and "→ ภาระ" written in
  //    red under it (#id-pun revealed by the clip rect #id-punr); everything else is Sets.notebook
  // ======================================================================================================
  function notebook7(L, o = {}) {
    const id = o.id || "nb7";
    Sets.notebook(L, { ...o, id, page: "chan", struck: true });
    const H = (x, y, txt, size = 34, col = "#2f4a8a", extra = "") => `<text x="${x}" y="${y}" font-family="Kanit" font-weight="500" font-size="${size}" fill="${col}"${extra}>${txt}</text>`;
    put(L.set, `<g transform="rotate(-4 540 1000)"><clipPath id="${id}-cp"><rect id="${id}-punr" x="220" y="${606 + 11 * 48 - 52}" width="${o.burden ? 320 : 0}" height="80"/></clipPath>
      <g id="${id}-pun" clip-path="url(#${id}-cp)">${H(236, 606 + 11 * 48 - 4, "→ ภาระ", 40, "#c8392b", ' transform="rotate(-4 236 1130)"')}<path d="M236,${606 + 11 * 48 + 8}h170" stroke="#c8392b" stroke-width="5" stroke-linecap="round"/></g>
      <ellipse id="${id}-ring" cx="370" cy="${606 + 10 * 48 - 12}" rx="118" ry="36" fill="none" stroke="#c8392b" stroke-width="6" opacity="${o.burden ? 1 : 0}"/></g>`);
  }

  // ======================================================================================================
  // 3. ปั้น's drawing that night: a room with bars, เจ๊หงส์ (pink blouse, permed hair, glasses) holding them; beside it a white
  //    fridge with a red cross; "พรุ่งนี้", "เจ๊หงส์" — the same crayon paper as drawing6
  // ======================================================================================================
  function drawing7(L, o = {}) {
    const id = o.id || "dw7";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#3a3330"/>`);
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    let s = `<g transform="rotate(1.5 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#2f6fb8" ${OUT}/>`;
    s += `<rect x="140" y="320" width="800" height="1280" fill="#2a2a3a" opacity=".22" filter="url(#fCrayon)"/>`;
    // the room with bars
    s += `<rect x="170" y="560" width="470" height="640" fill="#6f6a60" opacity=".55" filter="url(#fCrayon)"/>` + C("M170,1200V560H640V1200Z", "#3f454b", 10);
    // เจ๊หงส์ inside
    s += `<g transform="translate(400,1060)" filter="url(#fCrayon)"><path d="M-70,0q4,-150 70,-160q66,10 70,160z" fill="#e88aa8"/><circle cx="0" cy="-210" r="62" fill="#e9b48a"/><path d="M-66,-226q-4,-66 66,-70q70,4 66,70q-20,-34 -66,-36q-46,2 -66,36z" fill="#3a2a22"/>
      <circle cx="-22" cy="-210" r="16" fill="none" stroke="#2e2a26" stroke-width="5"/><circle cx="22" cy="-210" r="16" fill="none" stroke="#2e2a26" stroke-width="5"/><path d="M-6,-210h12" stroke="#2e2a26" stroke-width="4"/>
      <path d="M-18,-168q18,-10 36,0" stroke="#7a3a2a" stroke-width="6" fill="none"/><path d="M-26,-196v26M28,-196v22" stroke="#6ab0e0" stroke-width="5" stroke-linecap="round"/>
      <path d="M-70,-90l-50,-60M70,-90l50,-60" stroke="#e9b48a" stroke-width="22" stroke-linecap="round"/></g>`;
    s += C(Array.from({ length: 7 }, (_, k) => `M${215 + k * 65},575V1190`).join(""), "#2e2a26", 14);
    // the fridge with the red cross, and its cold glow
    s += `<g transform="translate(800,1200)" filter="url(#fCrayon)"><rect x="-110" y="-420" width="220" height="420" rx="18" fill="#f4f2ea" stroke="#9aa0a6" stroke-width="8"/><path d="M-110,-270H110" stroke="#9aa0a6" stroke-width="7"/><path d="M80,-380v70M80,-230v90" stroke="#9aa0a6" stroke-width="10" stroke-linecap="round"/>
      <path d="M-22,-250h44v44h44v44h-44v44h-44v-44h-44v-44h44z" fill="#d23b2e"/></g>`;
    s += C("M690,760q30,-30 60,0q30,30 60,0", "#9fd0e8", 7) + C("M700,700q30,-30 60,0q30,30 60,0", "#9fd0e8", 6);
    s += T(400, 1290, "เจ๊หงส์", 56, "#e0507a", { w: 700, extra: ' filter="url(#fCrayon)"' }) + T(540, 440, "พรุ่งนี้", 72, "#f4ecd8", { w: 700, extra: ' filter="url(#fCrayon)"' }) + T(870, 1620, "ปั้น", 34, "#c8392b", { w: 700, extra: ' filter="url(#fCrayon)"' }) + T(800, 1290, "ยา", 48, "#2f6fb8", { w: 700, extra: ' filter="url(#fCrayon)"' });
    s += `</g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }

  // the bars of the dormitory window in front of a first-person look out across the yard (L.fg of the shot)
  const BARS = () => `<g><path d="M-1400,-900H2600V2900H-1400Z M120,300V1700H960V300Z" fill="#141820" fill-rule="evenodd"/><rect x="100" y="280" width="880" height="1440" fill="none" stroke="#5b6066" stroke-width="40"/>
    ${Array.from({ length: 6 }, (_, k) => `<path d="M${200 + k * 136},300V1700" stroke="#3a3f45" stroke-width="22"/><path d="M${194 + k * 136},300V1700" stroke="#8d969d" stroke-width="5" opacity=".6"/>`).join("")}<path d="M120,1000H960" stroke="#3a3f45" stroke-width="18"/></g>`;

  window.Estate7 = { DESK, BARS, teamPhoto, WIN: { x0: WX0, x1: WX1, y0: WY0, y1: WY1 } };
  Object.assign(Sets, { officeNight, notebook7, drawing7 });
})();
