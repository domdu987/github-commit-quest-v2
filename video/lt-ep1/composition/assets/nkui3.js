// นิวเคลียร์ลงกรุงเทพ v2 · the channel's own motion graphics, not the reference series' cream cards:
// ink outline 4–6, flat fills with one shade and one highlight, soft drop shadows, Kanit (Mali for handwriting); icons are little
// scenes inside 2.5D coin badges; everything enters with back / elastic easing, staggered, squashes on landing, then keeps a
// secondary motion while on screen (rays flowing, shields pulsing, arrows bobbing, numbers rolling, ticks drawing).
// All tweens sit on the shot clock (tl, absolute seconds), so any frame can be seeked.
//   NkV.coin(kind, x, y, s, id, tone)  an icon badge · NkV.enter(tl, sel, at) its pop · NkV.idle(tl, id, kind, t0, dur)
//   NkV.title / isoMap / cityMap / rule / section / chain / counter / chip / big / clipboard / chalkEnd (tl, layer, t0, dur, o)
(function () {
  const f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const INK = "#26201c";
  const C0 = { red: "#e2382e", redD: "#a81e18", redL: "#ffd8d2", green: "#2fa864", greenD: "#1e7a48", greenL: "#dff5e6", yellow: "#ffd23a", yellowD: "#d8a410",
    yellowL: "#fff1b0", paper: "#fdfaf2", paperD: "#ece3cf", blue: "#2f6fd0", blueL: "#d6e6fb", sky: "#9fd2f2", slate: "#26303c", grey: "#c9ced4", greyD: "#8a9098",
    concrete: "#bdb7ab", concreteD: "#938c80", skin: "#e6ae80", cat: "#ec9248", catD: "#b8642a", ray: "#c8f03a", orange: "#f08a2a", night: "#16222e" };
  const C = Object.assign({}, C0, window.NK_PALETTE || {});   // an episode can mute the palette to sit in its world (set before this file loads)
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const T = (x, y, size, txt, o = {}) => `<text${o.id ? ` id="${o.id}"` : ""} x="${f1(x)}" y="${f1(y)}" font-family="${o.font || "Kanit"}" font-weight="${o.w || 900}" font-size="${size}" fill="${o.fill || INK}" text-anchor="${o.anchor || "middle"}"${o.stroke ? ` stroke="${o.stroke}" stroke-width="${o.sw || 8}" paint-order="stroke" stroke-linejoin="round"` : ""}${o.op != null ? ` opacity="${o.op}"` : ""}>${txt}</text>`;
  let seq = 0;
  const nid = (p = "nv") => `${p}${seq++}`;
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  Sets.DEFS += `<filter id="nvDrop" x="-40%" y="-40%" width="180%" height="190%"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-color="#000" flood-opacity=".42"/></filter>
    <radialGradient id="nvGlow"><stop offset="0" stop-color="#fff6c8" stop-opacity=".95"/><stop offset=".5" stop-color="#ffb04a" stop-opacity=".45"/><stop offset="1" stop-color="#ff7a2a" stop-opacity="0"/></radialGradient>
    <linearGradient id="nvSign" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#23915a"/><stop offset="1" stop-color="#17703f"/></linearGradient>
    <linearGradient id="nvMapBg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#132232"/><stop offset="1" stop-color="#0b141e"/></linearGradient>`;

  // ---------------- icons: ~100-unit scenes centred on 0,0, drawn to sit inside a badge face of radius 54 ----------------
  const trefoil = (r0, r1) => [90, 210, 330].map((a) => { const A = (d) => ((a + d) * Math.PI) / 180, p = (r, d) => `${f1(Math.cos(A(d)) * r)},${f1(-Math.sin(A(d)) * r)}`;
    return `M${p(r0, -30)}L${p(r1, -30)}A${r1},${r1} 0 0 0 ${p(r1, 30)}L${p(r0, 30)}A${r0},${r0} 0 0 1 ${p(r0, -30)}Z`; }).join("");
  const arrowDown = (x, y, len, col = C.yellow) => `<path d="M${x},${y}V${y + len}M${x - 11},${y + len - 11}l11,11l11,-11" stroke="${INK}" stroke-width="15" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M${x},${y}V${y + len}M${x - 11},${y + len - 11}l11,11l11,-11" stroke="${col}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
  const ICON = {
    // radiation rays pass straight through a car
    car: (p) => `<g id="${p}-car"><path d="M-46,14V0Q-46,-10 -36,-12L-24,-30Q-20,-36 -12,-36H14Q22,-36 28,-30L40,-12Q50,-10 50,0V14Z" fill="${C.red}" ${O(4)}/>
        <path d="M-18,-30H-2V-14H-30ZM4,-30H14Q20,-30 24,-24L32,-14H4Z" fill="${C.sky}" ${O(3)}/><path d="M-40,2H44" stroke="${C.redD}" stroke-width="4"/>
        <circle cx="-26" cy="16" r="11" fill="${C.slate}" ${O(4)}/><circle cx="28" cy="16" r="11" fill="${C.slate}" ${O(4)}/><circle cx="-26" cy="16" r="4" fill="${C.grey}"/><circle cx="28" cy="16" r="4" fill="${C.grey}"/></g>
      <g id="${p}-rays">${[-30, -8, 14].map((y) => `<path d="M-96,${y}q8,-7 16,0t16,0t16,0t16,0t16,0t16,0t16,0t16,0t16,0t16,0t16,0t16,0" stroke="${C.ray}" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}</g>`,
    // concrete stops the rays; the shield says safe
    building: (p) => `<path d="M-60,44H60" stroke="${C.greyD}" stroke-width="5" stroke-linecap="round"/>
      <rect x="-30" y="-48" width="50" height="92" fill="${C.concrete}" ${O(4)}/><rect x="6" y="-48" width="14" height="92" fill="${C.concreteD}"/>
      ${[-36, -16, 4, 24].map((y) => `<rect x="-22" y="${y}" width="10" height="10" fill="${C.sky}"/><rect x="-6" y="${y}" width="10" height="10" fill="${C.sky}"/>`).join("")}
      <rect x="-30" y="-48" width="50" height="92" fill="none" ${O(4)}/>
      <g id="${p}-rays">${[-26, 2].map((y) => `<path d="M-84,${y}q6,-6 12,0t12,0t12,0t12,0" stroke="${C.ray}" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}</g>
      <g id="${p}-sh"><path d="M36,-26Q46,-20 54,-20V-2Q54,14 36,24Q18,14 18,-2V-20Q26,-20 36,-26Z" fill="${C.green}" ${O(4)}/><path d="M28,-2l6,6l11,-12" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
    // the level under the ground: people and the P sign below the line
    under: (p) => `<rect x="-60" y="0" width="120" height="70" fill="#7a6250"/><path d="M-60,0H60" stroke="${INK}" stroke-width="4"/>
      <rect x="-22" y="-46" width="44" height="46" fill="${C.concrete}" ${O(4)}/><path d="M-12,-36h8v8h-8zM4,-36h8v8h-8zM-12,-20h8v8h-8zM4,-20h8v8h-8z" fill="${C.sky}"/>
      <rect x="-40" y="8" width="80" height="36" rx="4" fill="${C.concreteD}" ${O(4)}/>
      <circle cx="-20" cy="26" r="11" fill="${C.blue}" ${O(3)}/>${T(-20, 32, 16, "P", { fill: "#fff" })}
      ${[[6, 34], [22, 34]].map(([x, y]) => `<g transform="translate(${x},${y})"><circle cy="-12" r="5" fill="${C.skin}" ${O(2.5)}/><path d="M-6,4Q-6,-5 0,-5Q6,-5 6,4Z" fill="${C.green}" ${O(2.5)}/></g>`).join("")}
      <g id="${p}-arr">${arrowDown(38, -48, 34)}</g>`,
    radio: (p) => `<path d="M-34,-20L-16,-48" ${O(4)} fill="none"/><circle cx="-16" cy="-48" r="4" fill="${INK}"/>
      <rect x="-46" y="-20" width="80" height="54" rx="10" fill="${C.red}" ${O(4)}/><circle cx="-22" cy="7" r="14" fill="${C.slate}" ${O(3)}/>
      ${[-30, -22, -14].map((x) => `<path d="M${x},-2v18" stroke="#5a6470" stroke-width="2.5"/>`).join("")}
      <rect x="0" y="-10" width="26" height="13" rx="3" fill="${C.yellowL}" ${O(3)}/><path d="M8,-10v13" stroke="${C.red}" stroke-width="2.5"/><circle cx="13" cy="20" r="7" fill="${C.paper}" ${O(3)}/>
      <g id="${p}-w"><path d="M42,-6q7,9 0,18M50,-14q12,17 0,34" stroke="${C.blue}" stroke-width="4.5" fill="none" stroke-linecap="round"/></g>`,
    water: (p) => { const B = "M-14,-40H14V-34Q22,-26 22,-14V40Q22,48 14,48H-14Q-22,48 -22,40V-14Q-22,-26 -14,-34Z";
      return `<path d="${B}" fill="#eef8ff"/><clipPath id="${p}-bc"><path d="${B}"/></clipPath><g clip-path="url(#${p}-bc)"><g id="${p}-wl"><path d="M-46,-2q9,-6 18,0t18,0t18,0t18,0t18,0V60H-46Z" fill="#5ab4ec"/></g></g>
        <path d="${B}" fill="none" ${O(4)}/><rect x="-11" y="-52" width="22" height="13" rx="3" fill="${C.blue}" ${O(4)}/><path d="M-8,-20V30" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".7"/>`; },
    person: (p) => `<g transform="translate(-28,10) scale(.72)" opacity=".9"><circle cy="-18" r="17" fill="#d89a6a" ${O(4)}/><path d="M-30,44Q-30,4 0,4Q30,4 30,44Z" fill="${C.green}" ${O(4)}/></g>
      <g transform="translate(28,10) scale(.72)" opacity=".9"><circle cy="-18" r="17" fill="#c88a5e" ${O(4)}/><path d="M-30,44Q-30,4 0,4Q30,4 30,44Z" fill="${C.yellowD}" ${O(4)}/></g>
      <g id="${p}-p"><circle cy="-14" r="18" fill="${C.skin}" ${O(4)}/><path d="M-18,-20Q-14,-36 0,-34Q14,-36 18,-20Q8,-28 0,-26Q-8,-28 -18,-20Z" fill="#2a1e18"/>
        <path d="M-32,52Q-32,10 0,10Q32,10 32,52Z" fill="${C.blue}" ${O(4)}/></g>`,
    cat: (p) => `<g id="${p}-c"><path d="M-34,-8L-31,-46L-8,-26ZM34,-8L31,-46L8,-26Z" fill="${C.cat}" ${O(4)}/><path d="M-28,-16L-27,-38L-14,-27ZM28,-16L27,-38L14,-27Z" fill="#f4b8a0"/>
      <ellipse cy="6" rx="38" ry="32" fill="${C.cat}" ${O(4)}/><path d="M-10,-24l4,9l4,-9M-22,-18l6,8M22,-18l-6,8" stroke="${C.catD}" stroke-width="4" fill="none" stroke-linecap="round"/>
      <ellipse cy="18" rx="14" ry="10" fill="#fff4e4"/><ellipse cx="-14" cy="2" rx="4.5" ry="6" fill="${INK}"/><ellipse cx="14" cy="2" rx="4.5" ry="6" fill="${INK}"/>
      <circle cx="-12.5" cy="-0.5" r="1.6" fill="#fff"/><circle cx="15.5" cy="-0.5" r="1.6" fill="#fff"/><path d="M-3,12h6l-3,4z" fill="#c8605a"/></g>`,
    // the outer layer goes into a sealed bag
    shirt: (p) => `<path d="M-34,46Q-42,14 -24,0L-10,-6H10L24,0Q42,14 34,46Z" fill="#2a2e34" ${O(4)}/><path d="M-10,-6L-18,-16M10,-6L18,-16" ${O(4)} fill="none"/>
      <path d="M-20,20Q0,28 20,20" stroke="#4a505a" stroke-width="4" fill="none"/>
      <g id="${p}-sh"><path d="M-30,-40L-14,-50H14L30,-40L22,-28L14,-32V-8H-14V-32L-22,-28Z" fill="${C.yellow}" ${O(4)}/><path d="M-8,-50Q0,-42 8,-50" fill="none" ${O(3)}/>
        <circle cx="-6" cy="-24" r="3" fill="#a8c83a"/><circle cx="6" cy="-18" r="2.5" fill="#a8c83a"/><circle cx="2" cy="-30" r="2" fill="#a8c83a"/></g>`,
    warn: (p) => `<g id="${p}-t"><path d="M0,-46L46,36H-46Z" fill="${C.yellow}" ${O(5)}/><path d="M0,-16V8" stroke="${INK}" stroke-width="9" stroke-linecap="round"/><circle cx="0" cy="22" r="5.5" fill="${INK}"/></g>`,
    pill: (p) => `<g id="${p}-pl"><g transform="rotate(-35)"><rect x="-40" y="-16" width="80" height="32" rx="16" fill="#fff" ${O(4)}/><path d="M0,-16H-24Q-40,-16 -40,0Q-40,16 -24,16H0Z" fill="${C.red}" ${O(4)}/>
      <path d="M8,-8H28" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".8"/></g></g>`,
    torch: (p) => `<g id="${p}-b"><path d="M8,-10L58,-38V36L8,8Z" fill="${C.yellowL}" opacity=".9"/></g>
      <rect x="-46" y="-11" width="46" height="20" rx="6" fill="${C.slate}" ${O(4)}/><path d="M0,-16H12V14H0Z" fill="${C.greyD}" ${O(4)}/><rect x="-32" y="-4" width="10" height="5" rx="2" fill="${C.red}"/>`,
    food: (p) => `<g id="${p}-st">${[-12, 0, 12].map((x) => `<path d="M${x},-28q-6,-7 0,-14t0,-14" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>`).join("")}</g>
      <path d="M-32,-20H32L24,36Q22,44 14,44H-14Q-22,44 -24,36Z" fill="${C.paper}" ${O(4)}/><path d="M-30,-6H30L28,8H-28Z" fill="${C.red}"/><path d="M-32,-20H32" ${O(5)}/>
      <path d="M-30,-6H30M-28,8H28" stroke="${INK}" stroke-width="3"/>`,
    clock: (p) => `<circle r="42" fill="${C.paper}" ${O(5)}/>${Array.from({ length: 12 }, (_, k) => { const a = (k * Math.PI) / 6; return `<path d="M${f1(Math.sin(a) * 33)},${f1(-Math.cos(a) * 33)}L${f1(Math.sin(a) * 38)},${f1(-Math.cos(a) * 38)}" stroke="${INK}" stroke-width="${k % 3 ? 2.5 : 4}"/>`; }).join("")}
      <g id="${p}-h"><path d="M0,0V-28" stroke="${INK}" stroke-width="5" stroke-linecap="round"/></g><path d="M0,0L16,9" stroke="${C.red}" stroke-width="6" stroke-linecap="round"/><circle r="5" fill="${INK}"/>`,
    // stay in: the roof over a person
    home: (p) => `<path d="M-40,44V-4L0,-38L40,-4V44Z" fill="${C.paperD}" ${O(4)}/><path d="M-50,2L0,-46L50,2" fill="none" stroke="${INK}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M-50,2L0,-46L50,2" fill="none" stroke="${C.red}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
      <g id="${p}-p"><circle cy="4" r="11" fill="${C.skin}" ${O(3)}/><path d="M-16,44Q-16,18 0,18Q16,18 16,44Z" fill="${C.blue}" ${O(3)}/></g>`,
    nuke: (p) => `<g id="${p}-n"><path d="${trefoil(13, 44)}" fill="${INK}"/><circle r="8" fill="${INK}"/></g>`,
    mush: (p) => `<g id="${p}-m"><path d="M-8,40Q-10,10 -6,-4H6Q10,10 8,40Z" fill="#f0a060" ${O(4)}/>
      <path d="M-40,-10Q-46,-34 -22,-42Q-12,-58 8,-52Q30,-58 40,-38Q52,-24 36,-8Q20,0 0,-4Q-24,4 -40,-10Z" fill="#f6b46a" ${O(4)}/>
      <path d="M-30,-18Q-20,-30 -4,-28M8,-40Q22,-44 30,-32" stroke="#fff4d8" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/><path d="M-26,40H26" stroke="${INK}" stroke-width="5" stroke-linecap="round"/></g>`,
  };

  const RING = { yellow: [C.yellowL, C.yellow], green: [C.greenL, C.green], red: [C.redL, C.red], blue: [C.blueL, C.blue], white: ["#ffffff", C.paperD], dark: ["#2c3a4a", "#18222c"] };
  // glyph mode (window.NK_GLYPHS, set by the episode before this file loads): plain line glyphs on a cream tile with a coloured ring —
  // they stay readable at phone size where the little scenes turn to mush
  const L5 = `fill="none" stroke="${INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"`;
  const GLY = {
    nuke: `<path d="${trefoil(9, 30)}" fill="${INK}"/><circle r="6" fill="${INK}"/>`,
    building: `<rect x="-17" y="-30" width="34" height="58" ${L5}/>${[-19, -7, 5].map((y) => `<path d="M-8,${y}h5M4,${y}h5" ${L5}/>`).join("")}<path d="M-4,28V18h8V28" ${L5}/>`,
    home: `<path d="M-30,-2L0,-28L30,-2" ${L5}/><path d="M-21,-9V26H21V-9" ${L5}/><circle cy="4" r="6" ${L5}/><path d="M-10,24Q-10,14 0,14Q10,14 10,24" ${L5}/>`,
    radio: `<path d="M-22,-12L-8,-30" ${L5}/><rect x="-30" y="-12" width="54" height="36" rx="6" ${L5}/><circle cx="-14" cy="6" r="8" ${L5}/><path d="M4,-2h12M4,8h12" ${L5}/><path d="M32,-2q6,8 0,16" ${L5}/>`,
    water: `<path d="M-7,-30h14v8q10,6 10,16v34q0,6 -6,6h-22q-6,0 -6,-6v-34q0,-10 10,-16z" ${L5}/><path d="M-12,6q6,-5 12,0t12,0" ${L5}/>`,
    food: `<path d="M-24,-10h48l-6,36h-36z" ${L5}/><path d="M-26,-10h52" ${L5}/><path d="M-8,-18q-5,-6 0,-12M8,-18q-5,-6 0,-12" ${L5}/>`,
    torch: `<rect x="-30" y="-8" width="32" height="16" rx="4" ${L5}/><path d="M2,-12h8v24h-8z" ${L5}/><path d="M16,-12L30,-20M18,0H32M16,12L30,20" ${L5}/>`,
    pill: `<g transform="rotate(-35)"><rect x="-28" y="-11" width="56" height="22" rx="11" ${L5}/><path d="M0,-11V11" ${L5}/></g>`,
    person: `<circle cx="-11" cy="-12" r="8" ${L5}/><path d="M-26,20Q-26,2 -11,2Q4,2 4,20" ${L5}/><circle cx="13" cy="-6" r="7" ${L5}/><path d="M2,24Q4,9 13,9Q26,9 26,24" ${L5}/>`,
    cat: `<path d="M-22,-4L-24,-28L-8,-18Q0,-21 8,-18L24,-28L22,-4Q26,22 0,24Q-26,22 -22,-4Z" ${L5}/><circle cx="-9" cy="2" r="3" fill="${INK}"/><circle cx="9" cy="2" r="3" fill="${INK}"/><path d="M-3,11l3,3l3,-3" ${L5}/>`,
    warn: `<path d="M0,-28L28,22H-28Z" ${L5}/><path d="M0,-10V6" ${L5}/><circle cy="14" r="3" fill="${INK}"/>`,
    shirt: `<path d="M-24,-20L-9,-26H9L24,-20L30,-6L20,-2V24H-20V-2L-30,-6Z" ${L5}/><path d="M-9,-26Q0,-18 9,-26" ${L5}/>`,
    car: `<path d="M-30,10V0Q-30,-6 -24,-8L-14,-22Q-11,-26 -6,-26H8Q13,-26 16,-22L26,-8Q32,-6 32,0V10Z" ${L5}/><circle cx="-16" cy="12" r="7" fill="${C.paper}" ${L5}/><circle cx="18" cy="12" r="7" fill="${C.paper}" ${L5}/>`,
    under: `<path d="M-32,-4H32" ${L5}/><rect x="-11" y="-30" width="22" height="26" ${L5}/><rect x="-24" y="4" width="48" height="24" rx="4" fill="${C.greenL}"/><rect x="-24" y="4" width="48" height="24" rx="4" ${L5}/><path d="M0,8V22M-6,16l6,6l6,-6" ${L5}/>`,
  };
  // EP.2: the washing chant (ถอดเสื้อ · ใส่ถุง · ล้างตัว · ค่อยกอด) and EP.3's (อยู่นิ่ง · ฟังข่าว · รอสั่ง · ค่อยออก)
  Object.assign(GLY, {
    bag: `<path d="M-22,-14Q-30,6 -24,26H24Q30,6 22,-14Z" ${L5}/><path d="M-12,-14L-6,-24M12,-14L6,-24" ${L5}/><path d="M-8,-26Q0,-32 8,-26" ${L5}/><path d="M-10,4h20" ${L5}/>`,
    wash: `<circle cy="2" r="11" ${L5}/><path d="M-20,28Q-20,14 0,14Q20,14 20,28" ${L5}/><path d="M-22,-30h44" ${L5}/><path d="M-14,-24v6M0,-24v8M14,-24v6" ${L5}/>`,
    hug: `<circle cx="-10" cy="-14" r="8" ${L5}/><circle cx="12" cy="-12" r="8" ${L5}/><path d="M-26,24Q-26,2 -10,2Q2,2 4,10Q8,2 14,2Q28,2 28,24" ${L5}/><path d="M-4,-30q4,-6 8,0q4,-6 8,0q0,6 -8,12q-8,-6 -8,-12z" ${L5}/>`,
    still: `<circle cy="-16" r="9" ${L5}/><path d="M-14,24V6Q-14,-4 0,-4Q14,-4 14,6V24" ${L5}/><path d="M-26,24H26" ${L5}/>`,
    wait: `<circle r="26" ${L5}/><path d="M0,-14V0L10,8" ${L5}/>`,
    exit: `<path d="M-18,-26H14V26H-18Z" ${L5}/><path d="M-2,0H28M18,-10L28,0L18,10" ${L5}/>`,
  });
  // ถูกหวยทั้งบ้าน: ป้าแจ๋ว's three rules
  Object.assign(GLY, {
    nosmile: `<circle r="24" ${L5}/><path d="M-9,-8v3M9,-8v3" ${L5}/><path d="M-11,11H11" ${L5}/>`,
    shush: `<circle r="24" ${L5}/><path d="M-9,-8v3M9,-8v3" ${L5}/><path d="M-11,11H11" ${L5}/><path d="M0,30V-2" ${L5}/>`,
    eaten: `<path d="M-26,-20H26V10H2L-12,24V10H-26Z" ${L5}/><path d="M-13,-5h1M0,-5h1M13,-5h1" ${L5}/>`,
    ticket: `<path d="M-28,-18H28V-6A6,6 0 0 0 28,6V18H-28V6A6,6 0 0 0 -28,-6Z" ${L5}/><path d="M-12,-14V14" ${L5} stroke-dasharray="3 6"/><path d="M-2,-5H18M-2,6H12" ${L5}/>`,
  });
  const GRING = { yellow: C.yellowD, green: C.green, red: C.red, blue: C.blue, white: "#8a8f98", dark: "#2e3440" };
  const coin = (kind, x, y, s, id, tone = "yellow") => { if (window.NK_GLYPHS && GLY[kind])
      return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><g id="${id}"><circle r="62" cy="7" fill="#000" opacity=".28"/>
        <circle r="58" fill="${C.paper}" stroke="${GRING[tone] || GRING.yellow}" stroke-width="8"/><g transform="scale(1.3)">${GLY[kind]}</g></g></g>`;
    const [face, rim] = RING[tone];
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><g id="${id}">
      <circle r="64" cy="9" fill="#000" opacity=".3"/><circle r="64" fill="${rim}" ${O(5)}/><circle r="54" fill="${face}"/>
      <defs><clipPath id="${id}-cl"><circle r="54"/></clipPath></defs><g clip-path="url(#${id}-cl)">${ICON[kind](id)}</g>
      <circle r="54" fill="none" stroke="${INK}" stroke-width="3.5"/><path d="M-46,-28Q-32,-52 -6,-58" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".6"/></g></g>`; };
  const mark = (ok, x, y, id) => `<g transform="translate(${f1(x)},${f1(y)})"><g id="${id}"><circle r="25" fill="${ok ? C.green : C.red}" ${O(4)}/>${ok
    ? `<path id="${id}-p" d="M-11,0l7,8l14,-15" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>`
    : `<path id="${id}-p" d="M-9,-9L9,9" stroke="#fff" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/><path id="${id}-q" d="M9,-9L-9,9" stroke="#fff" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>`}</g></g>`;
  const pillLabel = (txt, id, o = {}) => { const w = o.w ?? 34 + txt.length * 26;
    return `<g id="${id}"><rect x="${f1(-w / 2)}" y="-24" width="${f1(w)}" height="48" rx="24" fill="${o.fill || C.paper}" ${O(4)}/>${T(0, 12, o.size || 32, txt, { fill: o.ink || INK, w: 800 })}</g>`; };

  // ---------------- motion ----------------
  const enter = (tl, sel, at, o = {}) => {
    const d = o.dur ?? 0.5;
    tl.fromTo(sel, { scale: 0, rotation: o.rot ?? -30, svgOrigin: "0 0" }, { scale: 1, rotation: 0, svgOrigin: "0 0", duration: d, ease: "back.out(2.6)" }, at);
    tl.to(sel, { scaleX: 1.12, scaleY: 0.88, svgOrigin: "0 0", duration: 0.07, ease: "power1.out" }, at + d);
    tl.to(sel, { scaleX: 1, scaleY: 1, svgOrigin: "0 0", duration: 0.4, ease: "elastic.out(1, 0.45)" }, at + d + 0.07);
  };
  const loop = (tl, sel, from, to, period, t0, dur, o = {}) => { if (dur <= 0.1) return; const n = Math.max(1, Math.round(dur / period));
    tl.fromTo(sel, from, { ...to, duration: o.yoyo === false ? period : period / 2, repeat: o.yoyo === false ? n - 1 : n * 2 - 1, yoyo: o.yoyo !== false, ease: o.ease || (o.yoyo === false ? "none" : "sine.inOut"), immediateRender: false }, t0); };
  const draw = (tl, sel, at, d = 0.3) => tl.to(sel, { attr: { "stroke-dashoffset": 0 }, duration: d, ease: "power2.out" }, at);
  // each icon keeps moving while it is on screen
  function idle(tl, id, kind, t0, dur) {
    const q = (s) => `#${id}-${s}`;
    if (!document.querySelector(`#${id}`) || dur <= 0.2 || (window.NK_GLYPHS && GLY[kind])) return;   // glyph tiles hold still after their pop
    if (kind === "car") { loop(tl, q("rays"), { x: 0 }, { x: 32 }, 0.42, t0, dur, { yoyo: false }); loop(tl, q("car"), { y: 0 }, { y: -2 }, 0.3, t0, dur); }
    if (kind === "building") { loop(tl, q("rays"), { x: -14 }, { x: 0 }, 0.5, t0, dur, { yoyo: false, ease: "power2.in" }); loop(tl, q("sh"), { scale: 1, svgOrigin: "36 0" }, { scale: 1.14, svgOrigin: "36 0" }, 0.9, t0, dur); }
    if (kind === "under") loop(tl, q("arr"), { y: 0 }, { y: 8 }, 0.7, t0, dur);
    if (kind === "radio") loop(tl, q("w"), { opacity: 0.15 }, { opacity: 1 }, 0.5, t0, dur);
    if (kind === "water") loop(tl, q("wl"), { x: -8 }, { x: 8 }, 1.0, t0, dur);
    if (kind === "person" || kind === "home") loop(tl, q("p"), { y: 0 }, { y: -4 }, 0.8, t0, dur);
    if (kind === "cat") loop(tl, q("c"), { rotation: -5, svgOrigin: "0 30" }, { rotation: 5, svgOrigin: "0 30" }, 1.1, t0, dur);
    if (kind === "shirt") loop(tl, q("sh"), { y: -10 }, { y: 10 }, 1.2, t0, dur);
    if (kind === "warn") loop(tl, q("t"), { rotation: -7, svgOrigin: "0 30" }, { rotation: 7, svgOrigin: "0 30" }, 0.22, t0, dur);
    if (kind === "pill") loop(tl, q("pl"), { rotation: -12, svgOrigin: "0 0" }, { rotation: 12, svgOrigin: "0 0" }, 0.5, t0, dur);
    if (kind === "torch") loop(tl, q("b"), { opacity: 0.35 }, { opacity: 1 }, 0.3, t0, dur);
    if (kind === "food") loop(tl, q("st"), { y: 6, opacity: 1 }, { y: -8, opacity: 0.1 }, 0.9, t0, dur, { yoyo: false, ease: "power1.out" });
    if (kind === "clock") loop(tl, q("h"), { rotation: 0, svgOrigin: "0 0" }, { rotation: 360, svgOrigin: "0 0" }, 3, t0, dur, { yoyo: false });
    if (kind === "nuke") loop(tl, q("n"), { rotation: 0, svgOrigin: "0 0" }, { rotation: 120, svgOrigin: "0 0" }, 2.4, t0, dur, { yoyo: false });
    if (kind === "mush") loop(tl, q("m"), { scale: 1, svgOrigin: "0 40" }, { scale: 1.08, svgOrigin: "0 40" }, 0.8, t0, dur);
  }
  const sparkle = (tl, layer, x, y, at, col = C.yellow) => { const g = document.createElementNS("http://www.w3.org/2000/svg", "g"); layer.appendChild(g);
    put(g, `<g transform="translate(${f1(x)},${f1(y)})">${[0, 60, 120, 180, 240, 300].map((a) => `<path d="M0,-30V-48" stroke="${col}" stroke-width="6" stroke-linecap="round" transform="rotate(${a})"/>`).join("")}</g>`);
    tl.fromTo(g, { opacity: 0, scale: 0.5, svgOrigin: `${f1(x)} ${f1(y)}` }, { opacity: 1, scale: 1.1, svgOrigin: `${f1(x)} ${f1(y)}`, duration: 0.18, ease: "power2.out" }, at);
    tl.to(g, { opacity: 0, scale: 1.4, svgOrigin: `${f1(x)} ${f1(y)}`, duration: 0.3, ease: "power1.in" }, at + 0.18); };

  // ---------------- the episode card: a green expressway sign on its gantry ----------------
  function title(tl, layer, t0, dur, o = {}) {
    const id = nid("nvt"), y = o.y ?? 170, W = 860, H = 380;
    put(layer, `<g id="${id}-g"><rect x="-40" y="${y - 70}" width="1160" height="40" fill="#3a4048" ${O(5)}/><rect x="-40" y="${y - 70}" width="1160" height="12" fill="#5a626c"/>
      <g id="${id}" filter="url(#nvDrop)"><path d="M${540 - 250},${y - 32}V${y + 10}M${540 + 250},${y - 32}V${y + 10}" stroke="${INK}" stroke-width="14"/>
        <rect x="${540 - W / 2}" y="${y}" width="${W}" height="${H}" rx="26" fill="url(#nvSign)" ${O(6)}/><rect x="${540 - W / 2 + 16}" y="${y + 16}" width="${W - 32}" height="${H - 32}" rx="16" fill="none" stroke="#fff" stroke-width="6"/>
        <g transform="translate(${540 - W / 2 + 92},${y + 92})">${coin("nuke", 0, 0, 0.62, `${id}-c`, "yellow")}</g>
        ${T(590, y + 128, 74, o.tag || "นิวเคลียร์ลงกรุงเทพ", { fill: "#fff" })}
        ${T(540, y + 214, 48, o.sub || "ตอนที่ 1 · วันที่ 1", { fill: "#e8ffe8", w: 800 })}
        <g transform="translate(540,${y + 296})"><rect x="-120" y="-44" width="240" height="78" rx="14" fill="#101418" ${O(5)}/>
          ${T(-40, 18, 58, (o.time || "17:42").split(":")[0], { fill: "#ffcf3a" })}<g id="${id}-col">${T(0, 14, 58, ":", { fill: "#ffcf3a" })}</g>${T(42, 18, 58, (o.time || "17:42").split(":")[1], { fill: "#ffcf3a" })}</g></g></g>`);
    tl.fromTo(`#${id}-g`, { y: -620 }, { y: 0, duration: 0.5, ease: "power3.out" }, t0);
    tl.fromTo(`#${id}`, { rotation: 7, svgOrigin: `540 ${y - 32}` }, { rotation: 0, svgOrigin: `540 ${y - 32}`, duration: 1.6, ease: "elastic.out(1, 0.28)" }, t0 + 0.3);
    enter(tl, `#${id}-c`, t0 + 0.45);
    idle(tl, `${id}-c`, "nuke", t0 + 1.0, dur - 1.0);
    loop(tl, `#${id}-col`, { opacity: 1 }, { opacity: 0.1 }, 1.0, t0 + 0.5, dur - 0.5, { ease: "steps(1)" });
  }

  // ---------------- 2.5D map of the block: a slab with depth, blocks that grow, the route to the car park, a dropping pin ----------------
  function isoMap(tl, layer, t0, dur, o = {}) {
    const id = nid("nvm"), cx = o.cx ?? 540, cy = o.cy ?? 820, S = o.s ?? 330, r = mk(17);
    const P = (x, y, z = 0) => [cx + (x - y) * S * 0.866, cy + (x + y) * S * 0.5 - z * S];
    const pt = (x, y, z) => P(x, y, z).map(f1).join(",");
    const poly = (pts, fill, extra = "") => `<path d="M${pts.join("L")}Z" fill="${fill}" ${O(4)} ${extra}/>`;
    const box = (x, y, w, d, h, col, bid) => { const top = poly([pt(x, y, h), pt(x + w, y, h), pt(x + w, y + d, h), pt(x, y + d, h)], col);
      const right = poly([pt(x + w, y, 0), pt(x + w, y + d, 0), pt(x + w, y + d, h), pt(x + w, y, h)], Rig2.dk(col, 0.18));
      const front = poly([pt(x, y + d, 0), pt(x + w, y + d, 0), pt(x + w, y + d, h), pt(x, y + d, h)], Rig2.dk(col, 0.32));
      const [bx, by] = P(x + w / 2, y + d / 2, 0);
      return { html: `<g id="${bid}">${front}${right}${top}</g>`, origin: `${f1(bx)} ${f1(by)}`, key: x + y };
    };
    const TH = 0.1;
    let g = `<g id="${id}-slab">${poly([pt(-1, 1, 0), pt(1, 1, 0), pt(1, 1, -TH), pt(-1, 1, -TH)], "#6e8a5a")}${poly([pt(1, -1, 0), pt(1, 1, 0), pt(1, 1, -TH), pt(1, -1, -TH)], "#5a7448")}
      ${poly([pt(-1, -1, 0), pt(1, -1, 0), pt(1, 1, 0), pt(-1, 1, 0)], "#cfe3b4")}
      ${poly([pt(-1, 0.18, 0), pt(1, 0.18, 0), pt(1, 0.46, 0), pt(-1, 0.46, 0)], "#6a6e76")}
      <path d="M${pt(-1, 0.32, 0)}L${pt(1, 0.32, 0)}" stroke="#f4f2ea" stroke-width="4" stroke-dasharray="14 12"/></g>`;
    const cars = [];
    for (let k = 0; k < 9; k++) { const x = -0.92 + k * 0.2 + r() * 0.04, lane = k % 2 ? 0.22 : 0.36; cars.push(box(x, lane, 0.1, 0.07, 0.04, ["#e2382e", "#f4f2ea", "#2f6fd0", "#ffd23a", "#8a9098"][k % 5], `${id}-car${k}`)); }
    const blocks = [];
    const spots = [[-0.9, -0.9, 0.3, 0.3], [-0.5, -0.9, 0.28, 0.32], [-0.9, -0.5, 0.3, 0.26], [-0.45, -0.45, 0.24, 0.24], [0.1, -0.9, 0.3, 0.28], [-0.9, 0.6, 0.3, 0.3], [-0.45, 0.62, 0.3, 0.28], [0.05, 0.6, 0.3, 0.3], [0.5, 0.62, 0.38, 0.3], [-0.05, -0.4, 0.22, 0.26]];
    spots.forEach(([x, y, w, d], k) => blocks.push(box(x, y, w, d, 0.1 + r() * 0.16, ["#e8dcc4", "#c9c2b4", "#b8c4cc", "#d8cbb0"][k % 4], `${id}-b${k}`)));
    const tower = box(0.45, -0.85, 0.42, 0.5, 0.62, "#eef0f2", `${id}-tw`);
    const all = [...blocks, tower, ...cars].sort((a, b) => a.key - b.key);
    g += all.map((b) => b.html).join("");
    // the P sign on the tower's front face and the ramp mouth
    const [px, py] = P(0.66, -0.35, 0.36), [rx, ry] = P(0.66, -0.35, 0.06);
    g += `<g transform="translate(${f1(px)},${f1(py)})"><circle r="26" fill="${C.blue}" ${O(4)}/>${T(0, 11, 32, "P", { fill: "#fff" })}</g><ellipse cx="${f1(rx)}" cy="${f1(ry)}" rx="34" ry="16" fill="#1a1c20" ${O(3)}/>`;
    // the route: from the family's car on the expressway into the ramp
    const [ax, ay] = P(-0.42, 0.29, 0.06), [bx2, by2] = P(0.3, 0.12, 0.02), [cx2, cy2] = P(0.62, -0.3, 0.02);
    g += `<path id="${id}-rt" d="M${f1(ax)},${f1(ay)}Q${f1(bx2)},${f1(by2)} ${f1(cx2)},${f1(cy2)}" stroke="${INK}" stroke-width="14" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
      <path id="${id}-rt2" d="M${f1(ax)},${f1(ay)}Q${f1(bx2)},${f1(by2)} ${f1(cx2)},${f1(cy2)}" stroke="${C.yellow}" stroke-width="7" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
      <g transform="translate(${f1(ax)},${f1(ay - 10)})"><g id="${id}-me"><circle r="16" fill="${C.green}" ${O(4)}/><circle r="6" fill="#fff"/></g></g>`;
    // the pin over the tower
    const [tx, ty] = P(0.66, -0.6, 0.62);
    g += `<g transform="translate(${f1(tx)},${f1(ty)})"><ellipse id="${id}-ps" rx="26" ry="10" fill="#000" opacity=".3"/><g id="${id}-pin"><path d="M0,0C-30,-36 -34,-62 -22,-80C-12,-96 12,-96 22,-80C34,-62 30,-36 0,0Z" fill="${C.red}" ${O(5)}/><circle cy="-66" r="12" fill="#fff" ${O(3)}/></g></g>`;
    // tokens around the slab, each on a short leader
    const tok = [["building", cx - 360, cy - 380, "ตึก", 120], ["under", cx + 360, cy - 380, "ลานจอดใต้ดิน", 290], ["radio", cx - 360, cy + 330, "วิทยุ", 140], ["water", cx + 360, cy + 330, "น้ำ", 100]];
    tok.forEach(([kind, x, y, lab, lw], k) => { g += coin(kind, x, y, 0.8, `${id}-k${k}`, "yellow") + `<g transform="translate(${x},${y + 86})">${pillLabel(lab, `${id}-kl${k}`, { size: 34, w: lw })}</g>`; });
    put(layer, `<g id="${id}" filter="url(#nvDrop)">${g}</g>`);
    // in: the slab rises, blocks grow from the ground, cars drop in, the route draws, the pin drops, tokens pop
    tl.fromTo(`#${id}`, { opacity: 0, y: 90 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.6)" }, t0);
    [...blocks, tower].forEach((b, k) => tl.fromTo(`#${b.html.match(/id="([^"]+)"/)[1]}`, { scaleY: 0, svgOrigin: b.origin }, { scaleY: 1, svgOrigin: b.origin, duration: 0.45, ease: "back.out(2.2)" }, t0 + 0.2 + k * 0.05));
    cars.forEach((c, k) => tl.fromTo(`#${id}-car${k}`, { y: -40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "bounce.out" }, t0 + 0.4 + k * 0.03));
    draw(tl, `#${id}-rt`, t0 + 0.9, 0.7); draw(tl, `#${id}-rt2`, t0 + 0.9, 0.7);
    tl.fromTo(`#${id}-pin`, { y: -260 }, { y: 0, duration: 0.6, ease: "bounce.out" }, t0 + 1.2);
    tl.fromTo(`#${id}-ps`, { scale: 0.2, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.6, ease: "bounce.out" }, t0 + 1.2);
    loop(tl, `#${id}-me`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.25, svgOrigin: "0 0" }, 0.6, t0 + 0.9, dur - 0.9);
    tok.forEach(([kind], k) => { enter(tl, `#${id}-k${k}`, t0 + 0.5 + k * 0.18); tl.fromTo(`#${id}-kl${k}`, { opacity: 0, y: -8 }, { opacity: 1, y: 0, duration: 0.25 }, t0 + 0.75 + k * 0.18);
      idle(tl, `${id}-k${k}`, kind, t0 + 1.3 + k * 0.18, dur - 1.3 - k * 0.18); });
  }

  // ---------------- the city map: every road out of the city fills with cars, the blast pulses ----------------
  function cityMap(tl, layer, t0, dur, o = {}) {
    const id = nid("nvy"), cx = o.cx ?? 540, cy = o.cy ?? 760, done = !!o.done, r = mk(23), N = 8;
    let g = `<rect width="1080" height="1920" fill="url(#nvMapBg)"/>`;
    for (let k = 0; k < 28; k++) g += `<path d="M${k * 40},0V1920M0,${k * 70}H1080" stroke="#1c3040" stroke-width="2"/>`;
    [280, 560].forEach((R, k) => (g += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="#2c4a5c" stroke-width="${10 - k * 3}" stroke-dasharray="${k ? "22 16" : "none"}"/>`));
    for (let k = 0; k < N; k++) { const a = (k / N) * Math.PI * 2 + 0.2, ex = cx + Math.cos(a) * 1250, ey = cy + Math.sin(a) * 1250, d = `M${cx},${cy}L${f1(ex)},${f1(ey)}`;
      g += `<path d="${d}" stroke="${INK}" stroke-width="30" stroke-linecap="round"/><path d="${d}" stroke="#4a6878" stroke-width="20" stroke-linecap="round"/>
        <path id="${id}-j${k}" d="${d}" stroke="#ff4a3a" stroke-width="20" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="${done ? 0 : 1}"/>
        <path id="${id}-f${k}" d="${d}" stroke="#ffd8c8" stroke-width="6" stroke-linecap="round" stroke-dasharray="10 26" opacity=".85"/>`; }
    // the blast in its red coin, its rings
    g += `<g id="${id}-rg"><circle cx="${cx}" cy="${cy}" r="120" fill="url(#nvGlow)"/></g>` + coin("mush", cx, cy, 0.95, `${id}-bl`, "red");
    g += `<g transform="translate(${cx},${cy + 110})">${pillLabel("จุดระเบิด", `${id}-bll`, { fill: C.red, ink: "#fff", size: 30 })}</g>`;
    // Keng, 8 km out on one of the roads
    const ka = (5 / N) * Math.PI * 2 + 0.2 - 0.3, kx = cx + Math.cos(ka) * 420, ky = cy + Math.sin(ka) * 420;
    g += `<path id="${id}-dl" d="M${cx},${cy}L${f1(kx)},${f1(ky)}" stroke="#f4ecd8" stroke-width="5" stroke-dasharray="14 12" opacity=".9"/>
      <g transform="translate(${f1((cx + kx) / 2)},${f1((cy + ky) / 2)})">${pillLabel("8 กม.", `${id}-km`, { size: 28 })}</g>
      <g transform="translate(${f1(kx)},${f1(ky)})"><ellipse rx="22" ry="8" fill="#000" opacity=".35"/><g id="${id}-pin"><path d="M0,0C-28,-34 -32,-58 -20,-75C-10,-90 10,-90 20,-75C32,-58 28,-34 0,0Z" fill="${C.green}" ${O(5)}/><circle cy="-60" r="11" fill="#fff" ${O(3)}/></g>
        <g transform="translate(0,46)">${pillLabel("เก่ง", `${id}-kl`, { size: 28 })}</g></g>`;
    put(layer, `<g id="${id}">${g}</g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25 }, t0);
    for (let k = 0; k < N; k++) {
      if (!done) tl.to(`#${id}-j${k}`, { attr: { "stroke-dashoffset": 0 }, duration: 1.5, ease: "power1.in" }, t0 + 0.2 + k * 0.06);
      loop(tl, `#${id}-f${k}`, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -36 } }, 0.5, t0, dur, { yoyo: false });
    }
    enter(tl, `#${id}-bl`, t0 + 0.1); idle(tl, `${id}-bl`, "mush", t0 + 0.7, dur - 0.7);
    loop(tl, `#${id}-rg`, { scale: 0.8, opacity: 1, svgOrigin: `${cx} ${cy}` }, { scale: 2.6, opacity: 0, svgOrigin: `${cx} ${cy}` }, 0.9, t0 + 0.3, dur - 0.3, { yoyo: false, ease: "power1.out" });
    tl.fromTo(`#${id}-pin`, { y: -200 }, { y: 0, duration: 0.55, ease: "bounce.out" }, t0 + 0.35);
    tl.fromTo(`#${id}-km`, { opacity: 0, scale: 0.6, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.3, ease: "back.out(2)" }, t0 + 0.6);
    tl.fromTo(`#${id}-kl`, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t0 + 0.7);
  }

  // ---------------- rule 1: a radiation-yellow sign on two chains; each line ticks as it lands ----------------
  function rule(tl, layer, t0, dur, o = {}) {
    const id = nid("nvr"), top = o.y ?? 150, W = 860, x0 = 540 - W / 2, rows = o.rows || [["building", "เข้าตึก"], ["home", "อยู่ในตึก"], ["radio", "ฟังข่าว"]];
    const H = Math.max(600, 236 + rows.length * 116), ticks = o.ticks || rows.map(() => true);
    let g = `<path d="M${540 - 300},-40L${540 - 300},${top + 20}M${540 + 300},-40L${540 + 300},${top + 20}" stroke="#8a9098" stroke-width="10" stroke-dasharray="16 8"/>
      <g id="${id}" filter="url(#nvDrop)"><rect x="${x0}" y="${top}" width="${W}" height="${H}" rx="30" fill="${C.yellow}" ${O(6)}/>
      <rect x="${x0 + 18}" y="${top + 18}" width="${W - 36}" height="${H - 36}" rx="20" fill="none" stroke="${INK}" stroke-width="4" stroke-dasharray="26 14"/>
      ${coin(o.icon || "nuke", x0 + 104, top + 104, 0.66, `${id}-c`, "white")}
      ${T(x0 + 190, top + 124, 70, o.tag || "กฎข้อ 1", { anchor: "start" })}${T(x0 + W - 50, top + 122, 30, o.sub || "ฝุ่นรังสีมา", { anchor: "end", w: 800, fill: C.redD })}
      <path d="M${x0 + 40},${top + 176}H${x0 + W - 40}" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    rows.forEach(([kind, txt], k) => { const y = top + 262 + k * 116;
      g += `<g id="${id}-r${k}">${coin(kind, x0 + 110, y, 0.62, `${id}-i${k}`, "white")}${T(x0 + 196, y + 22, 66, txt, { anchor: "start" })}
        <circle cx="${x0 + W - 90}" cy="${y}" r="25" fill="none" stroke="${INK}" stroke-width="4" stroke-dasharray="7 6" opacity=".45"/>${ticks[k] ? mark(true, x0 + W - 90, y, `${id}-m${k}`) : ""}</g>`; });
    const sc = o.s ?? 1;
    put(layer, `<g transform="translate(${f1(540 * (1 - sc))},${f1(o.dy ?? 0)}) scale(${sc})"><g id="${id}-g">${g}</g></g></g>`);
    tl.fromTo(`#${id}-g`, { y: -900 }, { y: 0, duration: 0.5, ease: "power3.out" }, t0);
    tl.fromTo(`#${id}`, { rotation: -6, svgOrigin: `540 ${top}` }, { rotation: 0, svgOrigin: `540 ${top}`, duration: 1.6, ease: "elastic.out(1, 0.3)" }, t0 + 0.3);
    enter(tl, `#${id}-c`, t0 + 0.4); idle(tl, `${id}-c`, o.icon || "nuke", t0 + 1.0, dur - 1.0);
    rows.forEach(([kind], k) => { const a = o.rowTimes ? t0 + o.rowTimes[k] : t0 + (o.rowAt ?? 0.55) + k * (o.rowStep ?? 0.32), m = o.tickAt ? t0 + o.tickAt[k] : a + 0.3;
      tl.fromTo(`#${id}-r${k}`, { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }, a);
      enter(tl, `#${id}-i${k}`, a + 0.05);
      if (ticks[k]) { tl.fromTo(`#${id}-m${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.35, ease: "back.out(3)" }, m);
        draw(tl, `#${id}-m${k}-p`, m + 0.1, 0.25);
        if (o.tickAt) tl.fromTo(`#${id}-r${k}`, { x: 0 }, { x: 14, duration: 0.09, yoyo: true, repeat: 1, ease: "power1.out", immediateRender: false }, m); }
      idle(tl, `${id}-i${k}`, kind, a + 0.8, t0 + dur - a - 0.8); });
  }

  // ---------------- the cut-away: fallout drifts down and settles on the roof, rays from the sides stop at the outer walls,
  // the people deep inside and below ground glow safe ----------------
  function section(tl, layer, t0, dur, o = {}) {
    const id = nid("nvs"), r = mk(29), L0 = 250, R0 = 830, top = 300, ground = 900, base = 1150, fl = 6, fh = (ground - top - 34) / fl;
    const wave = (x, y, dir, n) => `M${x},${y}` + `q${12 * dir},-10 ${24 * dir},0` + `t${24 * dir},0`.repeat(n - 1);
    let g = `<rect width="1080" height="1920" fill="url(#nvMapBg)"/>`;
    let dust = "";
    for (let k = 0; k < 80; k++) { const x = 30 + r() * 1020; if (x > L0 - 20 && x < R0 + 20) continue; dust += `<circle cx="${f1(x)}" cy="${f1(-200 + r() * 1500)}" r="${f1(4 + r() * 5)}" fill="${C.ray}" opacity="${f1(0.5 + r() * 0.5)}"/>`; }
    let roof = ""; for (let k = 0; k < 30; k++) roof += `<circle cx="${f1(L0 + 16 + r() * (R0 - L0 - 32))}" cy="${f1(top - 7 - r() * 12)}" r="${f1(4 + r() * 4)}" fill="${C.ray}"/>`;
    g += `<g id="${id}-d1">${dust}</g><g id="${id}-d2" transform="translate(0,-1400)">${dust}</g>`;
    // rays from the sides that end at the walls (the walls are drawn over their tips)
    g += `<g id="${id}-rl">${[420, 560, 700].map((y) => `<path d="${wave(-96, y, 1, 14)}" stroke="${C.ray}" stroke-width="7" fill="none" stroke-linecap="round" opacity=".9"/>`).join("")}</g>`;
    g += `<g id="${id}-rr">${[480, 620, 760].map((y) => `<path d="${wave(1176, y, -1, 14)}" stroke="${C.ray}" stroke-width="7" fill="none" stroke-linecap="round" opacity=".9"/>`).join("")}</g>`;
    // ground, the building, its floors, the basement
    g += `<rect x="-20" y="${ground}" width="1120" height="1100" fill="#3c3430"/><path d="M-20,${ground}H1100" stroke="#7a6a5a" stroke-width="10"/>`;
    for (let k = 0; k < 40; k++) g += `<circle cx="${f1(r() * 1080)}" cy="${f1(ground + 40 + r() * 900)}" r="${f1(3 + r() * 6)}" fill="#4c423c"/>`;
    g += `<rect x="${L0}" y="${top}" width="${R0 - L0}" height="${ground - top}" fill="${C.concrete}" ${O(6)}/><rect x="${L0 + 34}" y="${top + 34}" width="${R0 - L0 - 68}" height="${ground - top - 34}" fill="#ece8e0"/>`;
    for (let k = 1; k < fl; k++) g += `<path d="M${L0 + 34},${f1(top + 34 + k * fh)}H${R0 - 34}" stroke="${C.concreteD}" stroke-width="9"/>`;
    for (let k = 0; k < fl; k++) { const y = top + 34 + k * fh; g += `<rect x="${L0 + 6}" y="${f1(y + 22)}" width="22" height="${f1(fh - 44)}" fill="${C.sky}" opacity=".8"/><rect x="${R0 - 28}" y="${f1(y + 22)}" width="22" height="${f1(fh - 44)}" fill="${C.sky}" opacity=".8"/>`; }
    g += `<rect x="${L0}" y="${ground}" width="${R0 - L0}" height="${base - ground}" fill="${C.concreteD}" ${O(6)}/><rect x="${L0 + 34}" y="${ground + 22}" width="${R0 - L0 - 68}" height="${base - ground - 56}" fill="#d8d2c6"/>`;
    // the safe zones: the core of the middle floors and the basement
    const cy0 = top + 34 + 2 * fh, cH = 2 * fh;
    g += `<g id="${id}-safe" opacity="0"><rect x="${L0 + 34}" y="${ground + 22}" width="${R0 - L0 - 68}" height="${base - ground - 56}" fill="${C.green}" opacity=".38"/><rect x="${L0 + 140}" y="${f1(cy0)}" width="${R0 - L0 - 280}" height="${f1(cH)}" fill="${C.green}" opacity=".32"/></g>`;
    const person = (x, y, col, s = 1) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><circle cy="-30" r="14" fill="${C.skin}" ${O(3)}/><path d="M-20,20Q-20,-12 0,-12Q20,-12 20,20Z" fill="${col}" ${O(3)}/></g>`;
    [0, 1].forEach((f) => [-60, 0, 60].forEach((dx, k) => (g += person(540 + dx, cy0 + (f + 1) * fh - 26, [C.blue, C.yellow, C.red][(k + f) % 3], 0.9))));
    for (let k = 0; k < 6; k++) g += person(L0 + 110 + k * 72, base - 60, [C.blue, C.yellow, C.green, C.red, C.blue, C.yellowD][k]);
    g += `<g id="${id}-roof">${roof}</g>`;
    const labs = [[140, top - 20, "หลังคา", false, 170, L0 + 10, top - 14], [140, 560, "ผนังนอก", false, 190, L0 + 4, 560], [945, cy0 + fh, "กลางตึก", true, 190, R0 - 150, cy0 + fh], [945, ground + 120, "ใต้ดิน", true, 160, R0 - 40, ground + 120]];
    labs.forEach(([x, y, txt, ok, w, ex, ey], k) => {
      g += `<path id="${id}-ld${k}" d="M${x + (x < 540 ? w / 2 : -w / 2)},${f1(y)}L${f1(ex)},${f1(ey)}" stroke="${ok ? C.green : C.paper}" stroke-width="5" stroke-dasharray="8 7" opacity=".9"/>`;
      g += `<g transform="translate(${x},${f1(y)})">${pillLabel(txt, `${id}-l${k}`, { size: 36, w, fill: ok ? C.greenL : C.paper })}</g>`; if (ok) g += mark(true, x + w / 2 - 6, y - 34, `${id}-m${k}`); });
    put(layer, `<g id="${id}">${g}</g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.3 }, t0);
    loop(tl, `#${id}-d1`, { y: 0 }, { y: 1400 }, 2.2, t0, dur, { yoyo: false });
    loop(tl, `#${id}-d2`, { y: 0 }, { y: 1400 }, 2.2, t0, dur, { yoyo: false });
    loop(tl, `#${id}-rl`, { x: 0 }, { x: 48 }, 0.5, t0, dur, { yoyo: false });
    loop(tl, `#${id}-rr`, { x: 0 }, { x: -48 }, 0.5, t0, dur, { yoyo: false });
    tl.fromTo(`#${id}-roof`, { opacity: 0 }, { opacity: 1, duration: 0.6 }, t0 + 0.2);
    labs.forEach(([, , , ok], k) => { const a = t0 + 0.3 + k * 0.22;
      tl.fromTo(`#${id}-ld${k}`, { opacity: 0 }, { opacity: 0.9, duration: 0.2 }, a);
      enter(tl, `#${id}-l${k}`, a, { dur: 0.4, rot: k % 2 ? 14 : -14 });
      if (ok) { tl.fromTo(`#${id}-m${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.35, ease: "back.out(3)" }, a + 0.2); draw(tl, `#${id}-m${k}-p`, a + 0.3, 0.25); } });
    loop(tl, `#${id}-safe`, { opacity: 0.45 }, { opacity: 1 }, 0.9, t0 + 0.9, dur - 0.9);
  }

  // ---------------- the chain of coins with arrows drawing between them ----------------
  function chain(tl, layer, t0, dur, items, o = {}) {
    const id = nid("nvc"), y = o.y ?? 230, gap = o.gap ?? 300, n = items.length, x0 = 540 - ((n - 1) * gap) / 2, s = o.s ?? 0.95;
    let g = "";
    items.forEach((it, k) => { const x = x0 + k * gap;
      if (k < n - 1) { const a = x + 78 * s, b = x + gap - 80 * s;
        g += `<path id="${id}-a${k}" d="M${f1(a)},${y}H${f1(b)}" stroke="${INK}" stroke-width="16" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
          <path id="${id}-b${k}" d="M${f1(a)},${y}H${f1(b)}" stroke="#fff" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
          <g id="${id}-h${k}" opacity="0"><path d="M${f1(b - 18)},${y - 16}L${f1(b)},${y}L${f1(b - 18)},${y + 16}" stroke="${INK}" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M${f1(b - 18)},${y - 16}L${f1(b)},${y}L${f1(b - 18)},${y + 16}" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`; }
      g += coin(it.icon, x, y, s, `${id}-i${k}`, it.ok === false ? "red" : it.ok ? "green" : "yellow");
      g += `<g transform="translate(${x},${y + 96 * s})">${pillLabel(it.label, `${id}-l${k}`, { size: o.labelSize ?? 30 })}</g>` + (it.ok == null ? "" : mark(it.ok, x + 50 * s, y - 50 * s, `${id}-m${k}`));
    });
    put(layer, `<g id="${id}" filter="url(#nvDrop)">${g}</g>`);
    items.forEach((it, k) => { const a = t0 + (o.at ?? 0.1) + k * (o.step ?? 0.42);
      enter(tl, `#${id}-i${k}`, a);
      tl.fromTo(`#${id}-l${k}`, { opacity: 0, y: -12 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, a + 0.2);
      if (it.ok != null) { tl.fromTo(`#${id}-m${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.35, ease: "back.out(3)" }, a + 0.35);
        draw(tl, `#${id}-m${k}-p`, a + 0.45, 0.2); if (!it.ok) { draw(tl, `#${id}-m${k}-q`, a + 0.6, 0.2); loop(tl, `#${id}-i${k}`, { x: -5 }, { x: 5 }, 0.12, a + 0.8, 0.5); }
        else sparkle(tl, layer, x0 + k * gap + 50 * s, y - 50 * s, a + 0.55); }
      if (k < n - 1) { draw(tl, `#${id}-a${k}`, a + 0.3, 0.3); draw(tl, `#${id}-b${k}`, a + 0.3, 0.3); tl.fromTo(`#${id}-h${k}`, { opacity: 0 }, { opacity: 1, duration: 0.08 }, a + 0.58); }
      idle(tl, `${id}-i${k}`, it.icon, a + 0.95, t0 + dur - a - 0.95);
    });
  }

  // ---------------- a counter sticker: the coin, a number that rolls up, its unit ----------------
  function counter(tl, layer, t0, dur, o = {}) {
    const id = nid("nvn"), x = o.x ?? 44, y = o.y ?? 84, w = o.w ?? 330, from = o.from ?? 0, to = o.to;
    put(layer, `<g transform="translate(${x},${y}) rotate(-3)"><g id="${id}" filter="url(#nvDrop)">
      <rect x="0" y="0" width="${w}" height="104" rx="52" fill="${C.paper}" ${O(5)}/>
      ${coin(o.icon, 52, 52, 0.66, `${id}-c`, o.tone || "yellow")}
      ${T(w - 104, 76, 70, String(from), { id: `${id}-v`, anchor: "end" })}<g id="${id}-pl" opacity="0">${T(w - 100, 70, 52, "+", { anchor: "start", fill: C.red })}</g>
      ${T(w - 26, 74, 34, o.unit || "", { anchor: "end", w: 800 })}</g></g>`);
    const a = t0 + (o.at ?? 0), ra = t0 + (o.rollAt ?? (o.at ?? 0) + 0.3), cnt = o.count ?? 0.9;
    if (!o.still) { tl.fromTo(`#${id}`, { x: -140, opacity: 0, rotation: -8, svgOrigin: "0 52" }, { x: 0, opacity: 1, rotation: 0, svgOrigin: "0 52", duration: 0.5, ease: "back.out(1.8)" }, a);
      enter(tl, `#${id}-c`, a + 0.15); }
    const c = { v: from }, el = () => document.getElementById(`${id}-v`);
    if (to !== from) { tl.fromTo(c, { v: from }, { v: to, duration: cnt, ease: "power2.out", onUpdate: () => { const e = el(); if (e) e.textContent = String(Math.round(c.v)); } }, ra);
      tl.fromTo(`#${id}-v`, { scale: 1.3, svgOrigin: `${w - 140} 52` }, { scale: 1, svgOrigin: `${w - 140} 52`, duration: 0.4, ease: "elastic.out(1, 0.4)" }, ra + cnt); }
    if (o.plus) tl.fromTo(`#${id}-pl`, { opacity: 0, scale: 0, svgOrigin: `${w - 86} 52` }, { opacity: 1, scale: 1, svgOrigin: `${w - 86} 52`, duration: 0.35, ease: "back.out(3)" }, ra + 0.05 + cnt);
    idle(tl, `${id}-c`, o.icon, a + 0.8, dur - (o.at ?? 0) - 0.8);
  }

  // ---------------- an info sticker: coloured header band with the headline, a body line, the coin on its corner ----------------
  function chip(tl, layer, t0, dur, o = {}) {
    const id = nid("nvp"), w = o.w ?? 820, x = o.x ?? (1080 - w) / 2, y = o.y ?? 90, lines = o.lines, band = { red: C.red, green: C.green, blue: C.blue, yellow: C.yellowD }[o.tone || "blue"];
    const h = 96 + (lines.length - 1) * 50;
    let body = lines.slice(1).map((ln, k) => `<g id="${id}-t${k}">${T(150, 136 + k * 50, 34, ln, { anchor: "start", w: 700 })}</g>`).join("");
    put(layer, `<g transform="translate(${x},${y})"><g id="${id}" filter="url(#nvDrop)">
      <rect x="0" y="0" width="${w}" height="${h + 18}" rx="28" fill="${C.paper}" ${O(5)}/>
      <path d="M0,28Q0,0 28,0H${w - 28}Q${w},0 ${w},28V70H0Z" fill="${band}" ${O(5)}/>${T(150, 50, 40, lines[0], { anchor: "start", fill: "#fff" })}${body}
      ${coin(o.icon, 70, 62, 0.82, `${id}-c`, o.ctone || "yellow")}</g></g>`);
    const a = t0 + (o.at ?? 0);
    tl.fromTo(`#${id}`, { y: -60, opacity: 0, rotation: -5, svgOrigin: `${w / 2} 0` }, { y: 0, opacity: 1, rotation: -1.5, svgOrigin: `${w / 2} 0`, duration: 0.55, ease: "back.out(2)" }, a);
    enter(tl, `#${id}-c`, a + 0.15);
    lines.slice(1).forEach((_, k) => tl.fromTo(`#${id}-t${k}`, { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }, a + 0.35 + k * 0.15));
    idle(tl, `${id}-c`, o.icon, a + 0.8, dur - (o.at ?? 0) - 0.8);
  }

  // ---------------- a big number badge (−90%) with squash and a bouncing arrow ----------------
  function big(tl, layer, t0, dur, o = {}) {
    const id = nid("nvb"), x = o.x ?? 860, y = o.y ?? 190;
    put(layer, `<g transform="translate(${x},${y})"><g id="${id}" filter="url(#nvDrop)"><circle r="96" fill="${C.red}" ${O(6)}/><circle r="80" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="10 8" opacity=".7"/>
      ${T(0, 18, 64, o.text || "−90%", { fill: "#fff" })}<g id="${id}-ar" transform="translate(0,62)"><path d="M0,-12V10M-12,0l12,12l12,-12" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      <path d="M-70,-40Q-50,-74 -14,-80" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" opacity=".45"/></g></g>`);
    enter(tl, `#${id}`, t0, { rot: 20, dur: 0.55 });
    sparkle(tl, layer, x - 70, y - 70, t0 + 0.4); sparkle(tl, layer, x + 80, y + 50, t0 + 0.5);
    loop(tl, `#${id}-ar`, { y: 0 }, { y: 8 }, 0.5, t0 + 0.6, dur - 0.6);
  }

  // ---------------- the supplies sheet on a clipboard, written row by row (Mali, a pencil running along) ----------------
  function clipboard(tl, layer, t0, dur, rows, o = {}) {
    const id = nid("nvk"), x = o.x ?? 120, y = o.y ?? 130, w = o.w ?? 840, h = 190 + rows.length * 112;
    let g = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="30" fill="#b98a52" ${O(6)}/><rect x="${x + 26}" y="${y + 40}" width="${w - 52}" height="${h - 66}" rx="10" fill="#fffdf6" ${O(4)}/>
      <rect x="${x + w / 2 - 110}" y="${y - 22}" width="220" height="74" rx="16" fill="#a8aeb6" ${O(5)}/><rect x="${x + w / 2 - 70}" y="${y - 6}" width="140" height="22" rx="8" fill="#6a7078" ${O(3)}/>
      ${T(x + 60, y + 124, 52, o.title || "เสบียง · วันที่ 1 · 40 คน", { anchor: "start", font: "Mali", w: 700 })}<path d="M${x + 60},${y + 146}H${x + w - 60}" stroke="${C.red}" stroke-width="5" stroke-linecap="round"/>`;
    rows.forEach((rw, k) => { const ry = y + 230 + k * 112, bad = rw.bad;
      g += `<defs><clipPath id="${id}-c${k}"><rect id="${id}-cr${k}" x="${x + 30}" y="${ry - 56}" width="0" height="104"/></clipPath></defs>
        <g clip-path="url(#${id}-c${k})">${T(x + 160, ry + 16, 46, rw.label, { anchor: "start", font: "Mali", w: 600 })}${T(x + w - 150, ry + 16, 48, rw.val, { anchor: "end", font: "Mali", w: 700, fill: bad ? C.red : INK })}
        <path d="M${x + 60},${ry + 42}H${x + w - 60}" stroke="#c8d8e8" stroke-width="3"/></g>
        ${coin(rw.icon, x + 100, ry, 0.5, `${id}-i${k}`, bad ? "red" : "yellow")}${bad ? `<ellipse id="${id}-o${k}" cx="${x + w - 190}" cy="${ry + 2}" rx="64" ry="40" fill="none" stroke="${C.red}" stroke-width="6" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>` : mark(true, x + w - 92, ry, `${id}-m${k}`)}`; });
    g += `<g id="${id}-pen"><path d="M0,0L-14,-46L60,-150L84,-132L10,-28Z" fill="${C.yellow}" ${O(4)}/><path d="M0,0L-14,-46L-2,-38Z" fill="${INK}"/><path d="M60,-150L84,-132L94,-146L70,-164Z" fill="#f4a0a8" ${O(4)}/></g>`;
    put(layer, `<g id="${id}" filter="url(#nvDrop)">${g}</g>`);
    tl.fromTo(`#${id}`, { y: 900, rotation: 6, svgOrigin: "540 900" }, { y: 0, rotation: 0, svgOrigin: "540 900", duration: 0.55, ease: "back.out(1.4)" }, t0);
    const step = Math.min(0.42, (dur - 1.2) / rows.length);
    rows.forEach((rw, k) => { const a = t0 + 0.5 + k * step, ry = y + 230 + k * 112;
      enter(tl, `#${id}-i${k}`, a, { dur: 0.35 });
      tl.to(`#${id}-cr${k}`, { attr: { width: w - 60 }, duration: step * 0.9, ease: "power1.inOut" }, a + 0.05);
      tl.fromTo(`#${id}-pen`, { x: x + 150, y: ry + 20 }, { x: x + w - 140, y: ry + 20, duration: step * 0.9, ease: "power1.inOut", immediateRender: k === 0 }, a + 0.05);
      if (rw.bad) { draw(tl, `#${id}-o${k}`, a + step * 0.9, 0.4); loop(tl, `#${id}-i${k}`, { x: -4 }, { x: 4 }, 0.12, a + step, 0.6); }
      else { tl.fromTo(`#${id}-m${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.3, ease: "back.out(3)" }, a + step * 0.8); draw(tl, `#${id}-m${k}-p`, a + step * 0.85, 0.2); } });
    tl.to(`#${id}-pen`, { x: x + w - 60, y: y + h + 60, opacity: 0, duration: 0.4, ease: "power2.in" }, t0 + 0.55 + rows.length * step);
  }

  // ---------------- the next-episode card written in chalk on the closed steel door ----------------
  function chalkEnd(tl, layer, t0, dur, o = {}) {
    const id = nid("nve");
    put(layer, `<g id="${id}"><defs><clipPath id="${id}-c1"><rect id="${id}-r1" x="150" y="560" width="0" height="260"/></clipPath><clipPath id="${id}-c2"><rect id="${id}-r2" x="150" y="840" width="0" height="200"/></clipPath>
        <filter id="${id}-ch" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="4" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.0 1.42" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in"/></filter></defs>
      <radialGradient id="${id}-sm"><stop offset="0" stop-color="#06080a" stop-opacity=".7"/><stop offset=".7" stop-color="#06080a" stop-opacity=".35"/><stop offset="1" stop-color="#06080a" stop-opacity="0"/></radialGradient>
      <ellipse cx="540" cy="840" rx="470" ry="300" fill="url(#${id}-sm)"/>
      <g filter="url(#${id}-ch)"><g clip-path="url(#${id}-c1)">${T(540, 760, 176, o.big || "ตอนที่ 2", { font: "Sriracha", w: 400, fill: "#ffffff" })}</g>
        <g clip-path="url(#${id}-c2)">${T(540, 962, 104, o.q || "ใครเคาะ?", { font: "Sriracha", w: 400, fill: "#ffd24a" })}</g>
        <path id="${id}-u" d="M340,1000Q540,1030 740,996" stroke="${C.red}" stroke-width="10" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></g>
      <g transform="translate(540,1240)"><g id="${id}-f">${pillLabel(o.foot || "กดติดตาม แล้วมารอดไปด้วยกัน", `${id}-fp`, { size: 32, w: 560 })}</g></g>
      <g transform="translate(540,470) rotate(-4)"><g id="${id}-tag"><rect x="-130" y="-34" width="260" height="68" rx="34" fill="${C.red}" ${O(5)}/><circle cx="-92" cy="0" r="9" fill="#fff"/>${T(14, 12, 34, o.tag || "ตอนต่อไป", { fill: "#fff" })}</g></g></g>`);
    tl.fromTo(`#${id}-tag`, { scale: 0, rotation: -20, svgOrigin: "0 0" }, { scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.45, ease: "back.out(2.6)" }, t0 + 0.05);
    tl.to(`#${id}-r1`, { attr: { width: 780 }, duration: 0.6, ease: "power1.inOut" }, t0 + 0.15);
    tl.to(`#${id}-r2`, { attr: { width: 780 }, duration: 0.45, ease: "power1.inOut" }, t0 + 0.75);
    draw(tl, `#${id}-u`, t0 + 1.2, 0.3);
    tl.fromTo(`#${id}-f`, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, t0 + 1.3);
  }

  window.NkV = { coin, mark, pillLabel, enter, idle, loop, draw, sparkle, T, title, isoMap, cityMap, rule, section, chain, counter, chip, big, clipboard, chalkEnd, ICON, C, INK };
})();
