// ---------- หมาดำตาสี่: the story's own sets and on-screen graphics (house style of ผีแม่ม่าย / ทะเลลด: ink 4, flat fill, one shade, one highlight) ----------
// Everything is drawn from the world of the story: a zinc sheet nailed to the post under ยายบัว's house with chalk on it, a wooden
// "ระวังสุนัข" board on the fence, the shadow-puppet screen for the legend, and cut-away "how it gets in" pictures.
//
//   Rab.zinc(x, y, s, o)           a corrugated zinc sheet on a wire (returns SVG). o.lines [[text, size, color]…] in chalk · o.id · o.rot
//                                  o.ep "EP.1 อย่าอุ้มมัน" (a yellow chalk strip at the bottom). ids: #id (outer, translate), #id-s (swing)
//   Sets.rabTitle(L, o)            EP opener: the yard under the stilt house in morning light, the zinc title sign on the post,
//                                  ภูมิ crouched with the rice, the puppy (Dog "pup", id o.id+"-pup") at his hand. o.ep · o.time "day"|"dusk"|"night"
//   Sets.kneeIns(L, o)             insert: ภูมิ's right knee, the plaster half peeled off a red graze; the puppy's muzzle comes in
//                                  from the right and licks it. ids #id-muz (translate), #id-tng (tongue, scaleY), #id-plaster
//                                  RabUI.lick(tl, id, t0, dur) animates it
//   Sets.underHouse(L, o)          under the house at night: posts, the water jar, the rice-mill, firewood, the dark gap where the
//                                  dog lies; only its eyes (Dog glow) read. o.eyes [x, y, s] · o.lamp (a lamp lit on the stair)
//   RabUI.rules(tl, layer, t0, dur, o)  the zinc rule board: 3 chalk rules (o.active 0..2 highlighted, o.done ticked, later ones faint)
//                                       o.y · o.s · chalk writes on letter by letter (clip wipe), the tick draws, the sheet swings
//   RabUI.saliva(tl, layer, t0, dur, o) cut-away of skin: left intact skin (saliva beads off, ✓ ไม่ติด), right a graze (bullet-shaped
//                                       virus slips in, rides the nerve up toward the brain, ✗) · o.split true shows both, else the graze only
//   RabUI.pupAge(tl, layer, t0, dur, o) a growth strip of puppies 1–12 months on a calendar, 2–6 lit red, a stamp "ส่วนใหญ่"
//   RabUI.signEnd(tl, layer, t0, dur, o) end card: the wooden "ระวังสุนัข" board on the fence + a note pinned under it (o.ep, o.next)
//   RabUI.legendDog(L, id)              puppets for Sets.legend2: the four-eyed dog under a house, a spirit beside it (ids #id-dog #id-ghost)
//   RabUI.rewind(tl, layer, t0, dur, o) the tape-rewind overlay used for "ตั้งแต่วินาทีที่ N" (scan lines, ◀◀ and the time o.to)
(function () {
  const INK = "#2a1c18", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const CH = { w: "#f4f2ea", y: "#ffe27a", r: "#ff7a6a", g: "#9ae6a0" };
  Sets.DEFS += `
    <linearGradient id="rbZinc" x1="0" y1="0" x2="1" y2="0">${Array.from({ length: 13 }, (_, k) => `<stop offset="${f1(k / 12)}" stop-color="${k % 2 ? "#5e6a72" : "#7e8a92"}"/>`).join("")}</linearGradient>
    <linearGradient id="rbZincD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#1a1410" stop-opacity=".35"/></linearGradient>
    <radialGradient id="rbRust" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#a8542a" stop-opacity=".75"/><stop offset="1" stop-color="#a8542a" stop-opacity="0"/></radialGradient>
    <linearGradient id="rbBoard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8925a"/><stop offset="1" stop-color="#9a6a3a"/></linearGradient>
    <linearGradient id="rbSkin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8b48a"/><stop offset="1" stop-color="#d49a6e"/></linearGradient>
    <linearGradient id="rbMuscle" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8505a"/><stop offset="1" stop-color="#a8323e"/></linearGradient>
    <linearGradient id="rbShaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc070" stop-opacity=".5"/><stop offset="1" stop-color="#ff9a40" stop-opacity=".12"/></linearGradient>
    <radialGradient id="rbGap"><stop offset="0" stop-color="#010103" stop-opacity=".6"/><stop offset=".6" stop-color="#010103" stop-opacity=".45"/><stop offset="1" stop-color="#010103" stop-opacity="0"/></radialGradient>
    <radialGradient id="rbMorning" cx=".3" cy=".2" r=".9"><stop offset="0" stop-color="#fff2c8" stop-opacity=".6"/><stop offset="1" stop-color="#fff2c8" stop-opacity="0"/></radialGradient>`;

  const Rab = {};
  // ---------------- the zinc sheet ----------------
  Rab.zinc = (x, y, s = 1, o = {}) => {
    const id = o.id || "zn", W = o.w ?? 560, H = o.h ?? 360;
    const lines = (o.lines || []).map(([t, size, c], k, a) => {
      const yy = -H / 2 + 70 + k * ((H - 120) / Math.max(1, a.length - (o.ep ? 0 : 1))) + (o.ep ? 0 : 20);
      return `<text x="0" y="${f1(yy + size * 0.35)}" font-family="Sriracha" font-size="${size}" fill="${c || CH.w}" text-anchor="middle" opacity=".95"
        stroke="${c || CH.w}" stroke-width="1.2" stroke-opacity=".4" style="letter-spacing:1px">${t}</text>`;
    }).join("");
    const ep = o.ep ? `<g transform="translate(0,${H / 2 - 46}) rotate(-2)"><rect x="-190" y="-30" width="380" height="56" rx="6" fill="#ffd23a" opacity=".92" ${O(3)}/>
      <text x="0" y="12" font-family="Kanit" font-weight="900" font-size="34" fill="${INK}" text-anchor="middle">${o.ep}</text></g>` : "";
    return `<g id="${id}" transform="translate(${f1(x)},${f1(y)}) scale(${f1(s)})"><g id="${id}-s" transform="rotate(${o.rot ?? -2})">
      ${o.noWire ? "" : `<path d="M${-W / 2 + 30},${-H / 2}L0,${-H / 2 - 90}L${W / 2 - 30},${-H / 2}" stroke="#8a8e94" stroke-width="4" fill="none"/><circle cx="0" cy="${-H / 2 - 92}" r="9" fill="#5a5048" ${O(3)}/>`}
      <rect x="${-W / 2 + 10}" y="${-H / 2 + 12}" width="${W}" height="${H}" rx="8" fill="#000" opacity=".35"/>
      <rect x="${-W / 2}" y="${-H / 2}" width="${W}" height="${H}" rx="8" fill="url(#rbZinc)" ${O(4)}/>
      <rect x="${-W / 2}" y="${-H / 2}" width="${W}" height="${H}" rx="8" fill="url(#rbZincD)"/>
      <ellipse cx="${-W / 2 + 70}" cy="${H / 2 - 50}" rx="90" ry="50" fill="url(#rbRust)"/><ellipse cx="${W / 2 - 50}" cy="${-H / 2 + 40}" rx="60" ry="34" fill="url(#rbRust)"/>
      <rect x="${-W / 2 + 26}" y="${-H / 2 + 26}" width="${W - 52}" height="${H - 52}" rx="6" fill="#2a3034" opacity=".72"/>
      ${[[-W / 2 + 14, -H / 2 + 14], [W / 2 - 14, -H / 2 + 14], [-W / 2 + 14, H / 2 - 14], [W / 2 - 14, H / 2 - 14]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="6" fill="#c8ccd0" ${O(2)}/>`).join("")}
      <path d="M${-W / 2 + 40},${-H / 2 + 40}q40,-6 80,4" stroke="#fff" stroke-width="4" opacity=".25" fill="none"/>
      ${lines}${ep}</g></g>`;
  };

  // ---------------- EP opener: the yard under the stilt house ----------------
  Sets.rabTitle = (L, o = {}) => {
    const id = o.id || "rt", t = o.time || "day";
    Sets.village2(L, { id: id + "v", time: t, house: [-360, 1.6], tree: 1500, road: 1300, rays: t === "day", fg: false, ground: 1480 });
    // the post under the house that carries the sign, the sign, a basin and the dog's bowls
    put(L.set, `<rect x="560" y="700" width="46" height="800" fill="#5e3e28" ${O(4)}/><path d="M572,720V1490" stroke="#7a5438" stroke-width="8" opacity=".6"/>
      ${Rab.zinc(583, 980, 1, { id: id + "-zn", lines: [["หมาดำตาสี่", 92, CH.w]], ep: o.ep || "EP.1 อย่าอุ้มมัน", h: 300, w: 600, rot: -3 })}
      <g transform="translate(820,1500)"><ellipse cx="0" cy="6" rx="70" ry="14" fill="#000" opacity=".3"/><path d="M-52,-26H52L44,4H-44Z" fill="#c8402e" ${O(3)}/><path d="M-52,-26H52" stroke="#e8705a" stroke-width="5"/>
        <text x="0" y="-4" font-family="Kanit" font-weight="900" font-size="20" fill="#fff4e0" text-anchor="middle">ดำ</text></g>
      <g transform="translate(940,1506)"><ellipse cx="0" cy="4" rx="58" ry="12" fill="#000" opacity=".3"/><path d="M-44,-22H44L38,2H-38Z" fill="#3a7ab8" ${O(3)}/><path d="M-40,-18H40" stroke="#9ad0f0" stroke-width="7" opacity=".85"/></g>`);
    put(L.glow, `<rect x="-400" y="-200" width="1900" height="2400" fill="url(#rbMorning)" opacity="${t === "day" ? 0.8 : 0}" style="mix-blend-mode:screen"/>`);
  };

  // ---------------- insert: the knee ----------------
  Sets.kneeIns = (L, o = {}) => {
    const id = o.id || "ki";
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#6a8a4a"/>`);
    let s = `<g opacity=".55">${Array.from({ length: 26 }, (_, k) => `<path d="M${-200 + k * 60},${1920}q${10 + (k % 3) * 8},-${160 + (k % 5) * 40} ${30 + (k % 4) * 6},-${240 + (k % 3) * 50}" stroke="${k % 2 ? "#4a6a2e" : "#8ab05a"}" stroke-width="10" fill="none" stroke-linecap="round"/>`).join("")}</g>
      <ellipse cx="540" cy="1400" rx="900" ry="300" fill="#a8743e" opacity=".55"/>`;
    // the leg: thigh coming in from the top left, the bent knee, the shin down to the right; green shorts' hem
    s += `<path d="M-120,520C120,560 360,760 520,980C600,1090 620,1180 600,1280C580,1420 680,1640 820,1920L1180,1920C1040,1700 960,1480 960,1300C960,1120 860,920 660,720C500,560 260,380 -120,300Z" fill="url(#rbSkin)" ${O(5)}/>
      <path d="M-120,300C40,330 160,380 280,450L120,700C40,620 -40,560 -120,520Z" fill="#3e9a5a" ${O(5)}/><path d="M120,700L280,450" stroke="#2e7a44" stroke-width="10"/>
      <path d="M700,820C820,960 880,1100 880,1260" stroke="#b47a50" stroke-width="10" fill="none" opacity=".5" stroke-linecap="round"/>
      <path d="M560,1020C600,1060 640,1120 660,1190" stroke="#fff2dc" stroke-width="16" fill="none" opacity=".35" stroke-linecap="round"/>`;
    // the graze: red raw skin with scratch lines, a bead of blood; the plaster peeled half off, flapping
    s += `<g transform="translate(760,1040) rotate(28)"><ellipse id="${id}-wg" cx="0" cy="0" rx="150" ry="110" fill="url(#rbWound)" opacity=".35"/><ellipse cx="0" cy="0" rx="86" ry="58" fill="#e88a7a" ${O(3)}/><ellipse cx="-4" cy="2" rx="64" ry="40" fill="#d0504a"/>
        ${[-40, -18, 6, 28].map((x) => `<path d="M${x - 20},-26L${x + 16},24" stroke="#a8282a" stroke-width="4" stroke-linecap="round"/>`).join("")}
        <circle cx="20" cy="18" r="9" fill="#b8202a"/><circle cx="17" cy="15" r="3" fill="#fff" opacity=".6"/></g>
      <g id="${id}-plaster"><g transform="translate(700,960) rotate(28)"><path d="M-120,-46H-10L-14,46H-120Q-138,0 -120,-46Z" fill="#f2c8a0" ${O(3.5)}/><rect x="-96" y="-26" width="64" height="52" rx="6" fill="#e8b488"/>
        ${[[-104, -30], [-104, 30], [-24, -30], [-24, 30], [-64, -34]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="2.6" fill="#c89a6a"/>`).join("")}
        <path d="M-10,-46Q40,-90 70,-60Q50,-30 -14,46Z" fill="#f8dcbc" ${O(3.5)}/><path d="M-6,-40Q34,-70 56,-56" stroke="#fff" stroke-width="4" fill="none" opacity=".5"/></g></g>`;
    put(L.set, s);
    // the puppy's muzzle from the right: nose, a whisker pad, the tongue out to the graze
    put(L.act, `<g transform="translate(890,1010)"><g id="${id}-muz" transform="translate(0,0)">
      <path d="M560,-260C300,-300 120,-200 40,-80C0,-20 0,60 40,100C140,160 380,150 560,120Z" fill="#ecd2a6" ${O(5)}/>
      <path d="M560,-200C380,-210 240,-150 160,-80" stroke="#fbecd0" stroke-width="22" fill="none" opacity=".7" stroke-linecap="round"/>
      <path d="M560,40C400,70 220,80 110,60" stroke="#c8a272" stroke-width="10" fill="none" opacity=".7"/>
      <ellipse cx="40" cy="-30" rx="46" ry="38" fill="#2a1e1e" ${O(4)}/><ellipse cx="26" cy="-46" rx="14" ry="9" fill="#fff" opacity=".45"/>
      <path d="M70,40Q110,60 170,52" stroke="${INK}" stroke-width="5" fill="none"/>
      ${[[150, -20], [180, 0], [160, 20]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="4" fill="#a8825a"/>`).join("")}
      <path d="M210,-10l120,-40M214,8l130,-6M210,24l120,30" stroke="#5a4636" stroke-width="2.4" opacity=".6"/>
      <path d="M200,-60q10,-8 22,-2q-6,10 -22,2Z" fill="#a83a2a"/>
      <g transform="translate(90,70)"><g id="${id}-tng" transform="scale(1,0.2)"><path d="M0,-10Q-120,0 -150,40Q-160,90 -110,96Q-60,96 -30,60Q0,30 20,10Z" fill="#e8607a" ${O(4)}/>
        <path d="M-60,10Q-90,40 -110,70" stroke="#b83a52" stroke-width="5" fill="none"/></g></g>
      <g opacity=".85"><path d="M60,110q-4,40 4,80q8,10 12,0q4,-40 -4,-80Z" fill="#e8f4ff" ${O(2)}/></g></g></g>`);
  };
  const RabUI = {};
  RabUI.lick = (tl, id, t0, dur, n = 3) => {
    if (window.RabFX) RabFX.pulse(tl, `#${id}-wg`, t0, dur, 0.6, 0.15);
    tl.fromTo(`#${id}-muz`, { attr: { transform: "translate(420,-120)" } }, { attr: { transform: "translate(0,0)" }, duration: 0.45, ease: "power2.out", immediateRender: false }, t0);
    for (let k = 0; k < n; k++) {
      const a = t0 + 0.4 + k * ((dur - 0.6) / n);
      tl.fromTo(`#${id}-tng`, { attr: { transform: "scale(1,0.2)" } }, { attr: { transform: "scale(1,1)" }, duration: 0.16, ease: "power2.out", immediateRender: false }, a);
      tl.to(`#${id}-tng`, { attr: { transform: "scale(1,0.25)" }, duration: 0.2, ease: "power2.in" }, a + 0.2);
      tl.to(`#${id}-muz`, { attr: { transform: "translate(-30,24)" }, duration: 0.16, ease: "sine.inOut", yoyo: true, repeat: 1 }, a);
    }
  };

  // ---------------- under the house at night ----------------
  Sets.underHouse = (L, o = {}) => {
    const id = o.id || "uh";
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#06080e"/>`);
    put(L.far, `<rect x="-1300" y="700" width="3700" height="600" fill="#101a28"/><circle cx="900" cy="560" r="34" fill="#e8e2c8" opacity=".8"/>`);
    let s = `<rect x="-1300" y="-900" width="3700" height="560" fill="#1a120c"/>`;   // the floor of the house overhead
    for (let k = 0; k < 30; k++) s += `<rect x="${-1300 + k * 130}" y="-340" width="120" height="30" fill="#2a1c12" ${O(2)}/>`;
    s += `<path d="M-1300,-310H2400" stroke="#ffcf72" stroke-width="3" stroke-dasharray="40 90" opacity=".55"/>`;   // lamplight between the floorboards
    // the ground: packed earth, posts (front ones big), the water jar, firewood, the rice mill, a bicycle wheel
    s += `<rect x="-1300" y="1300" width="3700" height="1600" fill="#1e1610"/><path d="M-1300,1300H2400" stroke="#2e2218" stroke-width="10"/>`;
    [[-300, 0.7], [180, 0.85], [820, 0.85], [1300, 0.7]].forEach(([x, k]) => { s += `<rect x="${x - 26 * k}" y="-320" width="${52 * k}" height="${1640}" fill="#2e1e14" ${O(3)}/><path d="M${x - 10 * k},-300V1300" stroke="#4a3220" stroke-width="${8 * k}"/>`; });
    s += `<g transform="translate(-120,1300)"><ellipse cx="0" cy="0" rx="110" ry="20" fill="#000" opacity=".5"/><path d="M-90,0C-120,-80 -110,-200 -60,-230H60C110,-200 120,-80 90,0Z" fill="#4a2e1e" ${O(3)}/><ellipse cx="0" cy="-230" rx="60" ry="16" fill="#2a1a10" ${O(3)}/><path d="M-80,-120Q0,-100 80,-120" stroke="#6a4630" stroke-width="6" fill="none"/></g>
      <g transform="translate(1080,1300)">${Array.from({ length: 6 }, (_, k) => `<rect x="${-120 + (k % 3) * 70}" y="${-50 - Math.floor(k / 3) * 46}" width="140" height="40" rx="18" fill="#3a2616" ${O(2.4)}/>`).join("")}</g>`;
    put(L.set, s);
    if (o.lamp) put(L.glow, `<circle cx="${o.lamp}" cy="560" r="380" fill="url(#p2Lamp)" opacity=".35"/>`);
    // warm light from the house above, falling through the floorboards onto the ground round the dog's gap
    const ex = o.eyes ? o.eyes[0] : 540, ey = o.eyes ? o.eyes[1] : 1180;
    put(L.glow, `<g style="mix-blend-mode:screen"><path d="M${ex - 220},-320L${ex - 340},${ey + 160}H${ex + 260}L${ex + 150},-320Z" fill="url(#rbShaft)" opacity=".55"/>
      <ellipse cx="${ex}" cy="${ey + 140}" rx="380" ry="80" fill="#ff9a40" opacity=".22"/></g>`);
    // the gap at the back where the dog lies: deeper black, and only its eyes
    put(L.set, `<ellipse cx="${o.eyes ? o.eyes[0] : 540}" cy="${o.eyes ? o.eyes[1] + 30 : 1220}" rx="520" ry="230" fill="url(#rbGap)"/>`);
  };

  // ---------------- the rule board ----------------
  const RULES = ["ลูกหมาน่ารัก อย่าทักอย่าอุ้ม", "อย่ารอดูหมา รีบไปหาหมอ"];
  RabUI.RULES = RULES;
  RabUI.rules = (tl, layer, t0, dur, o = {}) => {
    const id = "rr" + Math.round(t0 * 100), act = o.active ?? 0, done = o.done ?? [], y = o.y ?? 640, s = o.s ?? 1;
    const rows = RULES.map((r, k) => {
      const on = k === act, d = done.includes(k), op = on || d ? 1 : 0.3, yy = -40 + k * 120;
      return `<g opacity="${op}"><text x="-232" y="${yy}" font-family="Sriracha" font-size="40" fill="${on ? CH.y : CH.w}">${k + 1}. ${r}</text>
        ${on ? `<path id="${id}-u${k}" d="M-232,${yy + 16}Q0,${yy + 26} 244,${yy + 12}" stroke="${CH.y}" stroke-width="5" fill="none" stroke-dasharray="520" stroke-dashoffset="520"/>` : ""}
        ${d ? `<path d="M-286,${yy - 14}l14,16l26,-36" stroke="${CH.g}" stroke-width="8" fill="none" stroke-linecap="round"/>` : `<circle cx="-266" cy="${yy - 12}" r="16" fill="none" stroke="${CH.w}" stroke-width="4" opacity=".7"/>`}</g>`;
    }).join("");
    put(layer, `<g id="${id}" transform="translate(540,${y}) scale(${s})" opacity="0"><g id="${id}-in">${Rab.zinc(0, 0, 1, { id: id + "-z", w: 640, h: 380, rot: 0, lines: [] })}
      <g transform="rotate(0)"><text x="0" y="-120" font-family="Kanit" font-weight="900" font-size="40" fill="${CH.y}" text-anchor="middle">กฎของยายบัว</text>${rows}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { attr: { transform: "translate(0,-700) rotate(-8)" } }, { attr: { transform: "translate(0,0) rotate(0)" }, duration: 0.6, ease: "back.out(1.6)", immediateRender: false }, t0);
    tl.to(`#${id}-z-s`, { attr: { transform: "rotate(1.5)" }, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: Math.max(0, Math.floor(dur / 1.1)) }, t0 + 0.6);
    tl.to(`#${id}-u${act}`, { attr: { "stroke-dashoffset": 0 }, duration: 0.6, ease: "power2.out" }, t0 + 0.75);
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };

  // ---------------- how it gets in: saliva on skin ----------------
  const virus = (x, y, r = 0, s = 1) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${r}) scale(${s})"><path d="M-16,-7H8Q18,-7 18,0Q18,7 8,7H-16Z" fill="#7a2a8a" ${O(2)}/>
    ${[-12, -6, 0, 6].map((a) => `<path d="M${a},-7v-4M${a},7v4" stroke="#7a2a8a" stroke-width="2"/>`).join("")}<path d="M-10,-2H8" stroke="#c88ad8" stroke-width="2.4"/></g>`;
  const skinBlock = (x, w, graze) => {
    let s = `<rect x="${x}" y="0" width="${w}" height="60" fill="#f0c4a0" ${O(3)}/><rect x="${x}" y="60" width="${w}" height="130" fill="#f8dccc" ${O(3)}/>
      <rect x="${x}" y="190" width="${w}" height="230" fill="url(#rbMuscle)" ${O(3)}/>`;
    for (let k = 0; k < 6; k++) s += `<path d="M${x + 20},${236 + k * 30}H${x + w - 20}" stroke="#8a2030" stroke-width="3" opacity=".4"/>`;
    if (graze) s += `<path d="M${x + w / 2 - 60},0L${x + w / 2 - 30},110L${x + w / 2},40L${x + w / 2 + 26},120L${x + w / 2 + 60},0Z" fill="#b8202a" ${O(3)}/>`;
    return s;
  };
  RabUI.saliva = (tl, layer, t0, dur, o = {}) => {
    const id = "rs" + Math.round(t0 * 100), y = o.y ?? 560, split = o.split !== false;
    let s = `<rect x="70" y="-60" width="940" height="${split ? 780 : 760}" rx="34" fill="#fdfaf2" ${O(5)}/><rect x="70" y="-60" width="940" height="90" rx="34" fill="#2e6a8a"/><rect x="70" y="0" width="940" height="30" fill="#2e6a8a"/>
      <text x="540" y="2" font-family="Kanit" font-weight="900" font-size="46" fill="#fff" text-anchor="middle">เชื้ออยู่ใน "น้ำลาย"</text>`;
    const panel = (x, w, graze, k) => `<g transform="translate(0,90)">${skinBlock(x, w, graze)}
      <text x="${x + w / 2}" y="470" font-family="Kanit" font-weight="900" font-size="36" fill="${graze ? "#c8282a" : "#1e7a48"}" text-anchor="middle">${graze ? "แผล / ถลอก → ติด" : "ผิวปกติ → ไม่ติด"}</text>
      <g id="${id}-drop${k}"><path d="M${x + w / 2},-120q-34,50 -34,74a34,34 0 0 0 68,0q0,-24 -34,-74Z" fill="#cfe8ff" ${O(3)}/>${virus(x + w / 2 - 6, -60, 0, 0.9)}${virus(x + w / 2 + 8, -40, 30, 0.8)}</g>
      ${graze ? `<g id="${id}-in">${virus(x + w / 2, 80, 90, 1)}${virus(x + w / 2 - 20, 150, 80, 1)}${virus(x + w / 2 + 16, 240, 100, 1)}</g>
        <path id="${id}-nerve" d="M${x + w / 2 + 20},260C${x + w / 2 + 120},250 ${x + w - 30},200 ${x + w - 10},60" stroke="#ffe27a" stroke-width="9" fill="none" stroke-dasharray="420" stroke-dashoffset="420"/>` :
        `<path id="${id}-ok" d="M${x + w / 2 - 30},-10l22,24l44,-50" stroke="#1e9a58" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="120" stroke-dashoffset="120"/>`}</g>`;
    if (split) s += panel(110, 410, false, 0) + panel(560, 410, true, 1);
    else s += panel(270, 540, true, 1);
    put(layer, `<g id="${id}" transform="translate(0,${y})" opacity="0"><g id="${id}-c">${s}</g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, t0);
    tl.fromTo(`#${id}-c`, { attr: { transform: "translate(540,300) scale(0.6) translate(-540,-300)" } }, { attr: { transform: "translate(540,300) scale(1) translate(-540,-300)" }, duration: 0.5, ease: "back.out(1.7)", immediateRender: false }, t0);
    [0, 1].forEach((k) => tl.fromTo(`#${id}-drop${k}`, { attr: { transform: "translate(0,-160)" } }, { attr: { transform: "translate(0,0)" }, duration: 0.55, ease: "bounce.out", immediateRender: false }, t0 + 0.4 + k * 0.25));
    if (split) { tl.to(`#${id}-ok`, { attr: { "stroke-dashoffset": 0 }, duration: 0.4 }, t0 + 1.0); tl.to(`#${id}-drop0`, { opacity: 0.25, duration: 0.4 }, t0 + 1.1); }
    tl.fromTo(`#${id}-in`, { opacity: 0, attr: { transform: "translate(0,-100)" } }, { opacity: 1, attr: { transform: "translate(0,0)" }, duration: 0.9, ease: "power1.inOut", immediateRender: false }, t0 + 1.0);
    tl.to(`#${id}-nerve`, { attr: { "stroke-dashoffset": 0 }, duration: 1.0, ease: "power1.inOut" }, t0 + 1.7);
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };

  // ---------------- puppies 2–6 months ----------------
  RabUI.pupAge = (tl, layer, t0, dur, o = {}) => {
    const id = "ra" + Math.round(t0 * 100), y = o.y ?? 620;
    let s = `<rect x="80" y="-40" width="920" height="560" rx="34" fill="#fdfaf2" ${O(5)}/><rect x="80" y="-40" width="920" height="100" rx="34" fill="#c8402e"/><rect x="80" y="20" width="920" height="40" fill="#c8402e"/>
      <text x="540" y="28" font-family="Kanit" font-weight="900" font-size="48" fill="#fff" text-anchor="middle">คนที่ตาย ส่วนใหญ่ถูก "ลูกหมา" กัด</text>`;
    for (let m = 1; m <= 12; m++) {
      const x = 80 + 40 + (m - 1) * 70 + 25, hot = m >= 2 && m <= 6;
      s += `<g id="${id}-m${m}"><rect x="${x - 30}" y="380" width="60" height="70" rx="10" fill="${hot ? "#ffd2c8" : "#efe8da"}" ${O(3)}/><text x="${x}" y="428" font-family="Kanit" font-weight="900" font-size="30" fill="${hot ? "#c8282a" : "#8a8070"}" text-anchor="middle">${m}</text></g>`;
    }
    s += `<text x="540" y="496" font-family="Kanit" font-weight="700" font-size="28" fill="#5a5048" text-anchor="middle">อายุ (เดือน)</text>
      <path id="${id}-br" d="M${80 + 40 + 70 + 25 - 34},372V346H${80 + 40 + 5 * 70 + 25 + 34}V372" stroke="#c8282a" stroke-width="8" fill="none" stroke-dasharray="520" stroke-dashoffset="520"/>
      <g id="${id}-lab" opacity="0"><rect x="290" y="270" width="290" height="62" rx="14" fill="#c8282a" ${O(3)}/><text x="435" y="314" font-family="Kanit" font-weight="900" font-size="36" fill="#fff" text-anchor="middle">2–6 เดือน</text></g>`;
    put(layer, `<g id="${id}" transform="translate(0,${y})" opacity="0">${s}<g id="${id}-pups"></g></g>`);
    const g = document.getElementById(id + "-pups");
    [[200, 0.55], [400, 0.7], [610, 0.85], [830, 1.0]].forEach(([x, k], i) => put(g, Dog.svg({ id: `${id}-p${i}`, kind: "pup", x, y: 250, s: k * 0.95, flip: i % 2 === 1 })));
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    [0, 1, 2, 3].forEach((i) => Dog.drive(tl, `${id}-p${i}`, t0, dur, "wag"));
    for (let m = 2; m <= 6; m++) tl.fromTo(`#${id}-m${m}`, { attr: { transform: "translate(0,0)" } }, { attr: { transform: "translate(0,-14)" }, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, t0 + 0.5 + (m - 2) * 0.1);
    tl.to(`#${id}-br`, { attr: { "stroke-dashoffset": 0 }, duration: 0.5 }, t0 + 1.0);
    tl.fromTo(`#${id}-lab`, { opacity: 0, attr: { transform: "translate(0,30)" } }, { opacity: 1, attr: { transform: "translate(0,0)" }, duration: 0.4, ease: "back.out(2)", immediateRender: false }, t0 + 1.3);
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };

  // ---------------- end card: ระวังสุนัข ----------------
  RabUI.signEnd = (tl, layer, t0, dur, o = {}) => {
    const id = "re" + Math.round(t0 * 100);
    const s = `<g transform="translate(540,760)"><g id="${id}-b"><rect x="-26" y="40" width="52" height="900" fill="#5e3e28" ${O(4)}/>
      <rect x="-330" y="-220" width="660" height="300" rx="16" fill="url(#rbBoard)" ${O(5)}/>${[-140, -60, 20].map((yy) => `<path d="M-320,${yy}H320" stroke="#7a4a24" stroke-width="3" opacity=".5"/>`).join("")}
      <text x="0" y="-60" font-family="Kanit" font-weight="900" font-size="104" fill="#c8282a" text-anchor="middle" stroke="#7a1414" stroke-width="2">ระวังสุนัข</text>
      ${Dog.svg({ id: id + "-dg", kind: "dam", x: -10, y: 66, s: 0.42, silhouette: true })}</g>
      <g id="${id}-n" transform="translate(70,180) rotate(4)"><rect x="-250" y="0" width="500" height="230" fill="#fdf6d8" ${O(3)}/><circle cx="0" cy="14" r="10" fill="#c8282a" ${O(2)}/>
        <text x="0" y="74" font-family="Mali" font-weight="700" font-size="34" fill="#2a3a8a" text-anchor="middle">${o.ep || "ตอนต่อไป"}</text>
        ${(o.next || []).map((t, k) => `<text x="0" y="${124 + k * 44}" font-family="Mali" font-weight="700" font-size="${o.size || 28}" fill="${k === (o.next.length - 1) ? "#c8282a" : "#2a2a2a"}" text-anchor="middle">${t}</text>`).join("")}</g></g>`;
    put(layer, `<g id="${id}" opacity="0">${s}</g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, t0);
    tl.fromTo(`#${id}-n`, { attr: { transform: "translate(70,700) rotate(-20)" } }, { attr: { transform: "translate(70,180) rotate(4)" }, duration: 0.7, ease: "back.out(1.5)", immediateRender: false }, t0 + 0.4);
  };

  // ---------------- the legend's puppets (for Sets.legend2) ----------------
  RabUI.legendDog = (L, id, CX = 540, CY = 820) => {
    const B = "#0a0c0b";
    put(L.glow, `<g transform="translate(${CX - 250},${CY + 420})">
        <path d="M-140,-420L60,-560L260,-420Z" fill="${B}"/><rect x="-110" y="-420" width="340" height="150" fill="${B}"/><rect x="-60" y="-380" width="70" height="60" fill="#f4c47a" opacity=".55"/>
        ${[-100, 40, 200].map((x) => `<rect x="${x}" y="-270" width="20" height="270" fill="${B}"/>`).join("")}<path d="M230,-270L300,0" stroke="${B}" stroke-width="14"/>${[0, 1, 2, 3].map((k) => `<path d="M${242 + k * 14},${-220 + k * 56}h34" stroke="${B}" stroke-width="9"/>`).join("")}
        <path d="M-200,0H420" stroke="${B}" stroke-width="10"/></g>
      ${Dog.svg({ id: id + "-dog", kind: "dam", x: CX - 160, y: CY + 410, s: 0.9, silhouette: true })}
      <g fill="#f4c47a" opacity=".9">${[[-240, 260], [-210, 262], [-180, 262], [-150, 262], [-120, 262], [-90, 260], [-60, 256]].map(([x, y]) => `<circle cx="${CX + x}" cy="${CY + y}" r="4"/>`).join("")}
        <circle cx="${CX - 21}" cy="${CY + 225}" r="5"/><circle cx="${CX - 10}" cy="${CY + 216}" r="4"/></g>
      <path d="M${CX - 150},${CY + 280}L${CX - 120},${CY + 640}M${CX + 230},${CY + 240}L${CX + 250},${CY + 640}" stroke="#0a0c0b" stroke-width="7"/>
      <g transform="translate(${CX + 230},${CY + 120})"><g id="${id}-ghost" opacity="0">
        <path d="M-30,-150C-70,-150 -80,-90 -76,-30C-74,40 -96,140 -110,290Q-60,270 -30,290Q0,270 30,290Q60,270 100,290C80,160 70,40 76,-30C80,-100 60,-150 30,-150Q0,-170 -30,-150Z" fill="${B}" opacity=".92"/>
        <path d="M-60,-40C-90,40 -100,120 -120,200M60,-40C90,40 100,120 120,180" stroke="${B}" stroke-width="10" fill="none" opacity=".8"/>
        <ellipse cx="-18" cy="-86" rx="9" ry="5" fill="#9aff5a"/><ellipse cx="18" cy="-86" rx="9" ry="5" fill="#9aff5a"/>
        <g fill="#f4c47a" opacity=".85">${[0, 1, 2, 3, 4, 5].map((k) => `<circle cx="${-30 + (k % 2) * 60}" cy="${20 + Math.floor(k / 2) * 70}" r="5"/>`).join("")}</g></g></g>`);
  };

  // ---------------- tape rewind ----------------
  RabUI.rewind = (tl, layer, t0, dur, o = {}) => {
    const id = "rw" + Math.round(t0 * 100);
    put(layer, `<g id="${id}" opacity="0"><rect width="1080" height="1920" fill="#0a1020" opacity=".25"/>${Array.from({ length: 24 }, (_, k) => `<rect y="${k * 80}" width="1080" height="3" fill="#fff" opacity=".12"/>`).join("")}
      <g transform="translate(540,300)"><rect x="-190" y="-60" width="380" height="120" rx="60" fill="#c8282a" ${O(4)}/><path d="M-130,0l50,-34v68zM-76,0l50,-34v68z" fill="#fff"/>
        <text x="60" y="22" font-family="Kanit" font-weight="900" font-size="54" fill="#fff" text-anchor="middle">ย้อน</text></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.12, immediateRender: false }, t0);
    tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + dur - 0.2);
  };

  // ---------------- the choice: two chalk boards; a dog's shadow drags the frame to o.pull ----------------
  RabUI.choice = (tl, layer, t0, dur, o = {}) => {
    const id = "rc" + Math.round(t0 * 100), Y = o.y ?? 700, at = t0 + (o.at ?? dur - 1.3), pa = o.pull === "a";
    const card = (k, c, yy) => `<g transform="translate(540,${yy})"><g id="${id}-c${k}">${Rab.zinc(0, 0, 1, { id: id + "-z" + k, w: 800, h: 210, rot: k ? 1.5 : -1.5, lines: [], noWire: true })}
      <g transform="translate(-280,0) scale(.8)">${c.icon || ""}</g><text x="-170" y="16" font-family="Sriracha" font-size="50" fill="#f4f2ea">${c.text}</text></g></g>`;
    put(layer, `<g id="${id}" opacity="0"><rect width="1080" height="1920" fill="#0a0810" opacity=".35"/>
      <text x="540" y="${Y - 230}" font-family="Kanit" font-weight="900" font-size="64" fill="#fff4dc" text-anchor="middle" stroke="#2a1c18" stroke-width="10" paint-order="stroke">${o.q || "จะทำยังไง?"}</text>
      ${card(0, o.a, Y)}${card(1, o.b, Y + 290)}
      <rect id="${id}-f" x="130" y="${Y - 120}" width="820" height="240" rx="26" fill="none" stroke="#ffd23a" stroke-width="12"/>
      <g id="${id}-sh" opacity="0"><path d="M-200,2200C100,1900 300,1700 600,1650C800,1620 1000,1700 1300,1900V2400H-200Z" fill="#05040a"/>
        <ellipse cx="560" cy="1700" rx="14" ry="9" fill="#9aff5a"/><ellipse cx="620" cy="1696" rx="14" ry="9" fill="#9aff5a"/></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    [0, 1].forEach((k) => tl.fromTo(`#${id}-c${k}`, { attr: { transform: "translate(-1200,0)" } }, { attr: { transform: "translate(0,0)" }, duration: 0.5, ease: "back.out(1.4)", immediateRender: false }, t0 + 0.1 + k * 0.15));
    tl.fromTo(`#${id}-f`, { attr: { y: Y - 120 } }, { attr: { y: Y + 170 }, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false }, t0 + 0.7);
    tl.fromTo(`#${id}-sh`, { opacity: 0, attr: { transform: "translate(0,300)" } }, { opacity: 1, attr: { transform: "translate(0,0)" }, duration: 0.5, ease: "power2.out", immediateRender: false }, at - 0.3);
    tl.to(`#${id}-f`, { attr: { y: pa ? Y - 120 : Y + 170 }, duration: 0.25, ease: "power3.in" }, at);
    tl.to(`#${id}-c${pa ? 0 : 1}`, { attr: { transform: "translate(0,0) scale(1.05)" }, duration: 0.2 }, at + 0.25);
    tl.to(`#${id}-c${pa ? 1 : 0}`, { opacity: 0.35, duration: 0.3 }, at + 0.25);
  };

  // ---------------- EP.2 cards ----------------
  // the home dog meets a dog from outside (a fight over the fence) → the bite; and the herb poultice crossed out
  RabUI.homeDog = (tl, layer, t0, dur, o = {}) => {
    const id = "rh" + Math.round(t0 * 100), y = o.y ?? 520;
    let s = `<rect x="70" y="-46" width="940" height="820" rx="34" fill="#b8a888" ${O(5)}/><rect x="70" y="-60" width="940" height="820" rx="34" fill="url(#rbSlabF)" ${O(5)}/><rect x="70" y="-60" width="940" height="90" rx="34" fill="#c8402e"/><rect x="70" y="0" width="940" height="30" fill="#c8402e"/>
      <text x="540" y="4" font-family="Kanit" font-weight="900" font-size="46" fill="#fff" text-anchor="middle">หมาเลี้ยง ก็ติดได้</text>
      <rect x="110" y="70" width="860" height="330" rx="20" fill="#e8f0d8" ${O(3)}/><path d="M540,90V380" stroke="#8a6a44" stroke-width="10" stroke-dasharray="4 26"/>
      <text x="300" y="380" font-family="Kanit" font-weight="700" font-size="28" fill="#4a6a2e" text-anchor="middle">หมาในบ้าน</text><text x="780" y="380" font-family="Kanit" font-weight="700" font-size="28" fill="#8a3a2a" text-anchor="middle">หมานอกบ้าน</text>
      <g id="${id}-bang" opacity="0"><path d="M540,180l20,-40l10,36l40,-20l-20,38l40,10l-40,16l20,36l-40,-16l-10,40l-18,-38l-38,18l16,-38l-40,-12l40,-14l-16,-38Z" fill="#ffd23a" ${O(3)}/></g>
      <g transform="translate(0,450)"><rect x="110" y="0" width="860" height="250" rx="20" fill="#f4ecd8" ${O(3)}/>
        <g transform="translate(330,130)"><ellipse rx="110" ry="80" fill="#e8b48a" ${O(3)}/><ellipse rx="70" ry="48" fill="#6a9a3a" ${O(3)}/><path d="M-50,-10q20,14 40,0q20,14 40,0" stroke="#3a6a1e" stroke-width="5" fill="none"/></g>
        <g id="${id}-x" opacity="0"><path d="M240,40L420,220M420,40L240,220" stroke="#e2382e" stroke-width="22" stroke-linecap="round"/></g>
        <text x="700" y="120" font-family="Kanit" font-weight="900" font-size="40" fill="#c8282a" text-anchor="middle">สมุนไพรพอกแผล</text><text x="700" y="176" font-family="Kanit" font-weight="900" font-size="40" fill="#c8282a" text-anchor="middle">ไม่ช่วย</text></g>`;
    put(layer, `<g id="${id}" transform="translate(0,${y})" opacity="0">${s}<g id="${id}-d"></g></g>`);
    const g = document.getElementById(id + "-d");
    put(g, Dog.svg({ id: id + "-a", kind: "dam", x: 330, y: 330, s: 0.95 }) + Dog.svg({ id: id + "-b", kind: "dam", x: 760, y: 330, s: 0.95, flip: true }));
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    Dog.drive(tl, id + "-a", t0, 0.8, "growl"); Dog.drive(tl, id + "-a", t0 + 0.8, 0.5, "lunge", { to: 420 }); Dog.drive(tl, id + "-a", t0 + 1.3, dur - 1.3, "bark");
    Dog.drive(tl, id + "-b", t0, 0.8, "growl"); Dog.drive(tl, id + "-b", t0 + 0.8, 0.5, "lunge", { to: 670 }); Dog.drive(tl, id + "-b", t0 + 1.3, dur - 1.3, "bark");
    tl.fromTo(`#${id}-bang`, { opacity: 0 }, { opacity: 1, duration: 0.1, yoyo: true, repeat: 3, immediateRender: false }, t0 + 1.2);
    tl.fromTo(`#${id}-x`, { opacity: 0, attr: { transform: "scale(1.4)" } }, { opacity: 1, attr: { transform: "scale(1)" }, duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + (o.xAt ?? 3.2));
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };
  // the race: a track from the bite to "symptoms"; the incubation can be as short as a week; the vaccine needle wins if it starts today
  RabUI.race = (tl, layer, t0, dur, o = {}) => {
    const id = "rq" + Math.round(t0 * 100), y = o.y ?? 560;
    let s = `<rect x="70" y="-46" width="940" height="620" rx="34" fill="#b8a888" ${O(5)}/><rect x="70" y="-60" width="940" height="620" rx="34" fill="url(#rbSlabF)" ${O(5)}/><rect x="70" y="-60" width="940" height="90" rx="34" fill="#2e6a8a"/><rect x="70" y="0" width="940" height="30" fill="#2e6a8a"/>
      <text x="540" y="4" font-family="Kanit" font-weight="900" font-size="46" fill="#fff" text-anchor="middle">แข่งกับเวลา</text>
      <path d="M150,230H930" stroke="#c8c0aa" stroke-width="18" stroke-linecap="round"/><path id="${id}-bar" d="M150,230H930" stroke="#e2382e" stroke-width="18" stroke-linecap="round" stroke-dasharray="780" stroke-dashoffset="780"/>
      <g transform="translate(150,230)"><circle r="34" fill="#ffd2c8" ${O(3)}/><text y="12" font-family="Kanit" font-weight="900" font-size="30" fill="#c8282a" text-anchor="middle">กัด</text></g>
      <g transform="translate(330,150)"><rect x="-120" y="-40" width="240" height="66" rx="14" fill="#ffd23a" ${O(3)}/><text y="6" font-family="Kanit" font-weight="900" font-size="30" fill="${INK}" text-anchor="middle">เร็วสุด 1 สัปดาห์</text></g>
      <path d="M330,190V215" stroke="${INK}" stroke-width="4"/>
      <g transform="translate(800,150)"><rect x="-120" y="-40" width="240" height="66" rx="14" fill="#efe8da" ${O(3)}/><text y="6" font-family="Kanit" font-weight="900" font-size="30" fill="#5a5048" text-anchor="middle">นานเกิน 1 ปี</text></g>
      <g transform="translate(930,230)"><circle r="40" fill="#2a1c18" ${O(3)}/><text y="10" font-family="Kanit" font-weight="900" font-size="24" fill="#fff" text-anchor="middle">อาการ</text></g>
      <g id="${id}-v" opacity="0" transform="translate(0,0)">${window.RabFX ? RabFX.coin("syringe", 120, 290, 0.9, id + "-cs") : ""}<g transform="translate(260,350)"><rect x="-30" y="-14" width="120" height="28" rx="8" fill="#9ad0f0" ${O(3)}/><path d="M90,0h60" stroke="${INK}" stroke-width="5"/><rect x="-60" y="-8" width="30" height="16" fill="#c8ccd2" ${O(2)}/></g>
        <text x="560" y="362" font-family="Kanit" font-weight="900" font-size="38" fill="#1e7a48">ฉีดวัคซีน วันนี้เลย</text></g>
      <g id="${id}-dead" opacity="0"><text x="540" y="480" font-family="Kanit" font-weight="900" font-size="44" fill="#c8282a" text-anchor="middle">มีอาการแล้ว = ตายเกือบทุกราย</text></g>`;
    put(layer, `<g id="${id}" transform="translate(0,${y})" opacity="0">${s}</g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    tl.to(`#${id}-bar`, { attr: { "stroke-dashoffset": 0 }, duration: 1.6, ease: "power1.in" }, t0 + 0.4);
    tl.fromTo(`#${id}-v`, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.45, ease: "back.out(2.2)", immediateRender: false }, t0 + 0.9);
    if (window.RabFX) { QkUI.iconPop(tl, document.getElementById(id + "-cs"), t0 + 0.9); RabFX.life(tl, document.getElementById(id + "-cs"), t0 + 1.6, dur); }
    tl.fromTo(`#${id}-dead`, { scale: 1 }, { scale: 1.06, transformOrigin: "50% 50%", duration: 0.4, repeat: Math.ceil(dur / 0.4), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (o.deadAt ?? 2.6) + 0.3);
    tl.fromTo(`#${id}-dead`, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, t0 + (o.deadAt ?? 2.6));
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };
  // a chain-link pen under the house (the dog kept in, watched 10 days) · Rab.pen(x, G, s, o) returns SVG; o.collar: the red collar hung on the post instead
  Rab.pen = (x, G, s = 1, o = {}) => {
    let g = `<g transform="translate(${x},${G}) scale(${s})"><rect x="-260" y="-300" width="520" height="300" fill="none" stroke="#8a9098" stroke-width="8" ${""}/>`;
    for (let k = -240; k <= 240; k += 30) g += `<path d="M${k},-300L${k + 30},0M${k + 30},-300L${k},0" stroke="#a8b0b8" stroke-width="2.4" opacity=".8"/>`;
    g += `<rect x="-270" y="-310" width="20" height="310" fill="#6a7078" ${O(2)}/><rect x="250" y="-310" width="20" height="310" fill="#6a7078" ${O(2)}/><path d="M-270,-310H270" stroke="#5a6068" stroke-width="12"/>`;
    if (o.sign) g += `<g transform="translate(0,-360) rotate(-3)"><rect x="-150" y="-36" width="300" height="72" rx="8" fill="#fdf6d8" ${O(3)}/><text y="12" font-family="Mali" font-weight="700" font-size="34" fill="#2a3a8a" text-anchor="middle">${o.sign}</text></g>`;
    return g + `</g>`;
  };
  Rab.collar = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><circle cx="0" cy="-10" r="8" fill="#8a8e94" ${O(2)}/><ellipse cx="0" cy="60" rx="46" ry="62" fill="none" stroke="#c8322a" stroke-width="16"/><ellipse cx="0" cy="60" rx="46" ry="62" fill="none" stroke="${INK}" stroke-width="2" stroke-dasharray="4 7" opacity=".6"/></g>`;
  // the series end card: the rule board with both rules ticked + "ตอนจบ" + the line to take home
  RabUI.finale = (tl, layer, t0, dur, o = {}) => {
    const id = "rf" + Math.round(t0 * 100);
    RabUI.rules(tl, layer, t0, dur, { active: -1, done: [0, 1], y: o.y ?? 640, out: false });
    put(layer, `<g id="${id}" opacity="0"><g transform="translate(540,${(o.y ?? 640) + 330}) rotate(-4)"><rect x="-150" y="-44" width="300" height="88" rx="12" fill="#c8282a" ${O(4)}/>
      <text y="18" font-family="Kanit" font-weight="900" font-size="52" fill="#fff" text-anchor="middle">ตอนจบ</text></g>
      ${o.line ? `<text x="540" y="${(o.y ?? 640) + 470}" font-family="Mali" font-weight="700" font-size="40" fill="#fff4dc" text-anchor="middle" stroke="#2a1c18" stroke-width="8" paint-order="stroke">${o.line}</text>` : ""}</g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0, attr: { transform: "translate(0,40)" } }, { opacity: 1, attr: { transform: "translate(0,0)" }, duration: 0.4, ease: "back.out(2)", immediateRender: false }, t0 + 0.8);
  };

  window.Rab = Rab; window.RabUI = RabUI;
})();
