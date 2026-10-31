// "รั้วสุดท้าย" on-screen graphics, in the house style of ผีแม่ม่าย / ทะเลลด (mmui.js): ink outline, flat fills, one shade + one highlight,
// eased entries (back / elastic), staggered, then a small secondary motion. Materials from the world of the story: a chalk slate hung on
// the gate, เจ๊หงส์'s ledger (lined paper, red margin, handwriting), a crayon map. All screen space: put them in L.light (y 220–1420
// keeps clear of the captions).
//   FenceUI.rules(tl, layer, t0, dur, { active, done, y })   the camp's three rules chalked on a slate hanging from a wire
//   FenceUI.ledger(tl, layer, t0, dur, { rows: [[label, value, at, mark]], day, y })   the ledger page; mark "circle" rings the value in red
//   FenceUI.card(tl, layer, t0, dur, { title, color, rows: [{ icon, text, at, mark: "x"|"ok"|"" , sub }], foot, footAt, y })
//                                             a knowledge card: paper board with a coloured header, one icon + line per row
//   FenceUI.versus(tl, layer, t0, dur, { a: {icon, text, mark}, b: {...}, title, at })  two coins side by side (wrong / right)
//   FenceUI.map(tl, layer, t0, dur, { from: [label, icon], to: [label, icon], go: [t1, t2] })  crayon map, the route drawn, a runner on it
//   FenceUI.tags(tl, layer, t0, [[x, y, name, at]])   masking-tape name labels
//   FenceUI.radio(tl, layer, t0, dur, { word, at })     the number from the radio as a big amber glowing word
//   FenceUI.rewind(tl, layer, t0, dur, label)           VHS tear + "↺ 0:05"
//   FenceUI.next(tl, layer, t0, dur, { ep, l1, l2, cta })  the ledger page "พรุ่งนี้ต้องหา" naming the next episode + the channel card
//   FenceUI.ICON[name](s)   coin glyphs (100-unit box): eye nose tongue spoon skull canB canL canF trash blur lid throat hospital
//            lung hose nofinger doctor nail scrape germ jaw cal syringe five people
(function () {
  const U = { ink: "#26201c", paper: "#fdfaf0", red: "#e2382e", redD: "#a81e18", green: "#2fa864", yellow: "#ffd23a", blue: "#2f6fd0",
    chalk: "#f2f4ee", slate: "#2a3a34", amber: "#ffb84a", wood: "#8a5a34" };
  const O = (w = 4) => `stroke="${U.ink}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  let seq = 0;
  const nid = (p) => `${p}${seq++}`;
  const FU = (window.FenceUI = window.FenceUI || {});
  Sets.DEFS += `<filter id="fuDrop" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#000" flood-opacity=".38"/></filter>
    <radialGradient id="fuAmber"><stop offset="0" stop-color="#ffe2a0" stop-opacity=".95"/><stop offset=".4" stop-color="#ffb04a" stop-opacity=".4"/><stop offset="1" stop-color="#ff9a30" stop-opacity="0"/></radialGradient>
    <linearGradient id="fuCoin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e8e2d4"/></linearGradient>
    <pattern id="fuLines" width="20" height="62" patternUnits="userSpaceOnUse"><rect width="20" height="62" fill="#fbf6e6"/><path d="M0,61H20" stroke="#9ec0e0" stroke-width="2"/></pattern>`;

  // ---------------- icons (glyphs inside a 2.5D coin) ----------------
  const I = {};
  const skin = "#e8b48a";
  I.eye = () => `<path d="M-46,0Q0,-44 46,0Q0,44 -46,0Z" fill="#fff" ${O(4)}/><circle r="18" fill="#5a3a24" ${O(3)}/><circle r="8" fill="#141414"/><circle cx="-6" cy="-6" r="4" fill="#fff"/>`;
  I.nose = () => `<path d="M-6,-46Q-14,0 -30,20Q-26,34 -8,30Q0,40 8,30Q26,34 30,20Q14,0 6,-46Z" fill="${skin}" ${O(4)}/><circle cx="-12" cy="22" r="5" fill="#8a5a3a"/><circle cx="12" cy="22" r="5" fill="#8a5a3a"/>`;
  I.tongue = () => `<path d="M-44,-20Q0,-34 44,-20Q30,10 0,10Q-30,10 -44,-20Z" fill="#c8303a" ${O(4)}/><path d="M-26,-6Q-30,44 0,48Q30,44 26,-6Z" fill="#f07a8a" ${O(4)}/><path d="M0,0V30" stroke="#c84a5a" stroke-width="4"/>`;
  I.spoon = () => `<ellipse cx="-14" cy="-14" rx="26" ry="20" fill="#d8dce0" ${O(4)} transform="rotate(-40 -14 -14)"/><path d="M4,4L44,44" stroke="#d8dce0" stroke-width="12" stroke-linecap="round"/><path d="M4,4L44,44" fill="none" ${O(3)} opacity=".0"/><ellipse cx="-16" cy="-16" rx="12" ry="8" fill="#c8a050" transform="rotate(-40 -16 -16)"/>`;
  I.skull = () => `<path d="M-38,4Q-44,-46 0,-48Q44,-46 38,4Q36,20 22,22V40H-22V22Q-36,20 -38,4Z" fill="#f4f0e4" ${O(4)}/><ellipse cx="-16" cy="-6" rx="12" ry="14" fill="${U.ink}"/><ellipse cx="16" cy="-6" rx="12" ry="14" fill="${U.ink}"/><path d="M0,10l-6,10h12Z" fill="${U.ink}"/><path d="M-12,30v10M0,30v10M12,30v10" stroke="${U.ink}" stroke-width="3"/>`;
  const canBody = (lid) => `<path d="M-34,-24V40Q0,50 34,40V-24" fill="#c8ccd2" ${O(4)}/><path d="M-34,-8Q0,2 34,-8V24Q0,34 -34,24Z" fill="${U.red}" ${O(3)}/>${lid}`;
  I.canB = () => canBody(`<path d="M-34,-24Q-34,-62 0,-64Q34,-62 34,-24Q0,-14 -34,-24Z" fill="#e8ecf0" ${O(4)}/><path d="M-16,-44Q0,-56 16,-44" stroke="#fff" stroke-width="5" fill="none"/>`);
  I.canL = () => canBody(`<ellipse cx="0" cy="-24" rx="34" ry="9" fill="#e8ecf0" ${O(4)}/>`) + `<path d="M24,0q8,20 4,40" stroke="#c8a050" stroke-width="7" fill="none" stroke-linecap="round"/><circle cx="30" cy="48" r="7" fill="#c8a050"/>`;
  I.canF = () => canBody(`<ellipse cx="0" cy="-24" rx="34" ry="9" fill="#e8ecf0" ${O(4)}/>`) + `<g fill="#f4f0e0" ${O(2.5)}><circle cx="-10" cy="-40" r="12"/><circle cx="10" cy="-50" r="14"/><circle cx="2" cy="-66" r="10"/><circle cx="-18" cy="-60" r="7"/></g>`;
  I.trash = () => `<path d="M-34,-24H34L28,46H-28Z" fill="#5a7a8a" ${O(4)}/><rect x="-42" y="-38" width="84" height="16" rx="5" fill="#7a9aaa" ${O(4)}/><path d="M-12,-46h24" stroke="${U.ink}" stroke-width="6"/><path d="M-14,-8V34M0,-8V34M14,-8V34" stroke="#3a5a6a" stroke-width="4"/>`;
  I.blur = () => `<g opacity=".55" transform="translate(-10,0)">${I.eye()}</g><g transform="translate(10,0)">${I.eye()}</g>`;
  I.lid = () => `<path d="M-46,4Q0,-40 46,4Q0,44 -46,4Z" fill="#fff" ${O(4)}/><circle cy="14" r="16" fill="#5a3a24"/><path d="M-46,4Q0,-40 46,4Q0,0 -46,4Z" fill="${skin}" ${O(4)}/><path d="M-30,-8l-6,12M-10,-12l-4,14M10,-12l4,14M30,-8l6,12" stroke="${U.ink}" stroke-width="3"/>`;
  I.throat = () => `<path d="M-30,-48Q-20,0 -26,48H26Q20,0 30,-48" fill="${skin}" ${O(4)}/><path d="M-10,-30Q0,-10 -6,10Q4,20 0,40" stroke="${U.red}" stroke-width="7" fill="none" stroke-linecap="round" stroke-dasharray="10 8"/>`;
  I.hospital = () => `<path d="M-44,46V-24L0,-48L44,-24V46Z" fill="#f4f4ee" ${O(4)}/><rect x="-14" y="-24" width="28" height="28" fill="${U.red}"/><path d="M0,-34V14M-24,-10H24" stroke="#fff" stroke-width="0"/><path d="M-6,-20h12v6h6v12h-6v6h-12v-6h-6v-12h6Z" fill="#fff"/><rect x="-12" y="20" width="24" height="26" fill="#5a8ab8" ${O(3)}/>`;
  I.lung = () => `<path d="M-6,-46V-14Q-30,-30 -42,0Q-50,40 -14,42Q-4,30 -6,-6M6,-46V-14Q30,-30 42,0Q50,40 14,42Q4,30 6,-6" fill="#f2a0a8" ${O(4)}/><path d="M-6,-14Q-20,-4 -26,10M6,-14Q20,-4 26,10" stroke="#c8606a" stroke-width="4" fill="none"/>`;
  I.hose = () => `<path d="M-40,40C-40,-10 0,-50 40,-30" stroke="#3aa86a" stroke-width="14" fill="none" stroke-linecap="round"/><circle cx="40" cy="-30" r="10" fill="#e8b42a" ${O(3)}/>`;
  I.nofinger = () => `<circle cx="-4" cy="-6" r="34" fill="${skin}" ${O(4)}/><path d="M-20,8Q-4,22 12,8" stroke="${U.ink}" stroke-width="5" fill="none"/><path d="M10,4L48,46" stroke="${skin}" stroke-width="16" stroke-linecap="round"/><path d="M10,4L48,46" fill="none" stroke="${U.ink}" stroke-width="3" opacity=".6"/>`;
  I.doctor = () => `<circle cy="-20" r="22" fill="${skin}" ${O(4)}/><path d="M-40,46Q-40,4 0,4Q40,4 40,46Z" fill="#f4f4ee" ${O(4)}/><path d="M-14,8Q-20,30 -4,36Q10,36 10,22" stroke="#3a5a8a" stroke-width="5" fill="none"/><circle cx="10" cy="20" r="6" fill="#8a9aaa" ${O(2)}/>`;
  I.nail = () => `<path d="M-6,-40L0,44L6,-40Z" fill="#9aa0a6" ${O(4)}/><ellipse cx="0" cy="-42" rx="20" ry="7" fill="#c8ccd0" ${O(4)}/><path d="M-3,-10l4,-6M-4,10l5,-6" stroke="#9a5a32" stroke-width="5"/><circle cx="0" cy="44" r="4" fill="${U.red}"/>`;
  I.scrape = () => `<path d="M-46,-30Q0,-40 46,-30V30Q0,40 -46,30Z" fill="${skin}" ${O(4)}/><path d="M-30,-6h60M-26,6h52M-20,-16h40" stroke="#e86a6a" stroke-width="5" stroke-linecap="round"/>`;
  I.germ = () => `<ellipse rx="34" ry="18" fill="#8ac06a" ${O(4)} transform="rotate(-20)"/>${[-20, 0, 20].map((x) => `<path d="M${x},-14l-4,-16M${x},14l4,16" stroke="${U.ink}" stroke-width="3"/>`).join("")}<circle cx="-10" cy="-2" r="4" fill="#3a6a2a"/><circle cx="12" cy="2" r="4" fill="#3a6a2a"/>`;
  I.soil = () => `<path d="M-46,10Q-20,-20 0,-6Q24,-30 46,6V40H-46Z" fill="#8a6a48" ${O(4)}/>${[[-20, 20], [10, 24], [26, 12], [-30, 32]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="4" fill="#5a4630"/>`).join("")}<path d="M-10,-6q-4,-20 6,-34" stroke="#4e9a3a" stroke-width="5" fill="none"/>`;
  I.jaw = () => `<path d="M-34,-40Q0,-56 34,-40V0Q34,44 0,48Q-34,44 -34,0Z" fill="${skin}" ${O(4)}/><path d="M-18,22H18" stroke="${U.ink}" stroke-width="6" stroke-linecap="round"/><path d="M-14,14v16M-4,14v16M6,14v16M14,14v16" stroke="#fff" stroke-width="3"/><path d="M-46,10l-10,-4M46,10l10,-4M-46,24l-12,2M46,24l12,2" stroke="${U.red}" stroke-width="5" stroke-linecap="round"/>`;
  I.cal = () => `<rect x="-42" y="-36" width="84" height="80" rx="8" fill="#fff" ${O(4)}/><rect x="-42" y="-36" width="84" height="22" rx="6" fill="${U.red}" ${O(4)}/><path d="M-24,-46v18M24,-46v18" stroke="${U.ink}" stroke-width="6" stroke-linecap="round"/>${Array.from({ length: 9 }, (_, k) => `<rect x="${-32 + (k % 3) * 24}" y="${-6 + Math.floor(k / 3) * 16}" width="16" height="10" fill="#d8dce0"/>`).join("")}`;
  I.syringe = () => `<g transform="rotate(-45)"><rect x="-14" y="-40" width="28" height="70" rx="4" fill="#e8f4ff" ${O(4)}/><rect x="-14" y="-6" width="28" height="36" fill="#8ac8f0"/><path d="M0,30V54" stroke="${U.ink}" stroke-width="4"/><path d="M-20,-40H20M0,-40V-56M-12,-56H12" stroke="${U.ink}" stroke-width="5" stroke-linecap="round"/></g>`;
  I.five = () => `<text y="24" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="66" fill="${U.red}">5</text><text y="46" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="20" fill="${U.ink}">ปี</text>`;
  I.people = () => [-30, -10, 10, 30].map((x, k) => `<circle cx="${x}" cy="-14" r="9" fill="${["#c8946a", "#e8b48a", "#9a6a44", "#f0c4a0"][k]}" ${O(2.5)}/><path d="M${x - 10},24V4Q${x},-4 ${x + 10},4V24Z" fill="${["#bcd8f0", "#f2c83a", "#2e3c62", "#c8303a"][k]}" ${O(2.5)}/>`).join("");
  FU.ICON = I;
  const coin = (k, s = 1, id = "") => `<g transform="scale(${s})"${id ? ` id="${id}"` : ""}><ellipse cx="0" cy="58" rx="56" ry="10" fill="#000" opacity=".2"/><circle r="62" fill="#c8c0ae" ${O(4)} transform="translate(0,8)"/><circle r="62" fill="url(#fuCoin)" ${O(4)}/><path d="M-44,-38Q-20,-60 14,-58" stroke="#fff" stroke-width="7" fill="none" opacity=".8" stroke-linecap="round"/>${(I[k] || (() => ""))()}</g>`;
  const mark = (m, id) => m === "x" ? `<g id="${id}"><circle r="30" fill="${U.red}" ${O(4)}/><path d="M-12,-12L12,12M12,-12L-12,12" stroke="#fff" stroke-width="8" stroke-linecap="round"/></g>`
    : m === "ok" ? `<g id="${id}"><circle r="30" fill="${U.green}" ${O(4)}/><path d="M-13,1l9,10l18,-20" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>` : "";
  const pop = (tl, sel, t, s0 = 0.4) => tl.fromTo(sel, { opacity: 0, scale: s0, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)", immediateRender: false }, t);
  const bob = (tl, sel, t, dur, a = 6) => tl.fromTo(sel, { y: 0 }, { y: -a, duration: 0.9, yoyo: true, repeat: Math.max(1, Math.ceil(dur / 0.9)), ease: "sine.inOut", immediateRender: false }, t);
  const hide = (tl, sel, t0) => tl.set(sel, { opacity: 0 }, t0);
  const out = (tl, sel, t) => tl.to(sel, { opacity: 0, duration: 0.18, immediateRender: false }, t);

  // ---------------- the camp's rule slate ----------------
  FU.RULES = [["ออกไป…", "ต้องกลับก่อนมืด"], ["ช่วยได้…", "แต่อย่าเชื่อ"], ["แบ่งได้…", "แต่อย่าบอกทาง"]];
  FU.rules = (tl, layer, t0, dur, o = {}) => {
    const id = nid("fr"), active = o.active ?? -1, done = o.done || [], Y = o.y ?? 360;
    let c = `<g transform="translate(540,${Y})"><g id="${id}-sw"><path d="M-330,-170L0,-250L330,-170" stroke="#9aa0a6" stroke-width="5" fill="none"/><circle cy="-250" r="12" fill="#c8ccd0" ${O(3)}/>
      <g filter="url(#fuDrop)"><rect x="-430" y="-180" width="860" height="560" rx="26" fill="${U.wood}" ${O(5)}/></g><rect x="-400" y="-150" width="800" height="500" rx="12" fill="${U.slate}"/>
      <path d="M-380,-40H380" stroke="${U.chalk}" stroke-width="3" opacity=".3"/>
      <text x="0" y="-70" text-anchor="middle" font-family="Mali" font-weight="700" font-size="60" fill="${U.yellow}">กฎของค่าย</text>`;
    FU.RULES.forEach(([a, b], k) => {
      const y = 40 + k * 110, st = done.includes(k) ? "done" : k === active ? "active" : active < 0 ? "all" : "next";
      c += `<g id="${id}-r${k}" opacity="${st === "next" ? 0.32 : 1}"><text x="-340" y="${y + 18}" font-family="Mali" font-weight="700" font-size="54" fill="${st === "active" ? U.yellow : U.chalk}">${k + 1}. ${a} <tspan fill="${st === "active" ? "#fff" : U.chalk}">${b}</tspan></text>`;
      if (st === "active") c += `<path id="${id}-ul" d="M-340,${y + 34}Q0,${y + 46} 360,${y + 30}" stroke="${U.yellow}" stroke-width="7" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>`;
      if (st === "done") c += `<path d="M330,${y}l14,16l30,-36" stroke="#8af0a0" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
      c += `</g>`;
    });
    c += `<path d="M-300,330h80" stroke="${U.chalk}" stroke-width="10" stroke-linecap="round" opacity=".8"/></g></g>`;
    put(layer, `<g id="${id}">${c}</g>`);
    hide(tl, `#${id}`, 0);
    tl.fromTo(`#${id}`, { opacity: 0, y: -500 }, { opacity: 1, y: 0, duration: 0.55, ease: "back.out(1.6)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: 6 }, { rotation: 0, svgOrigin: "0 -250", duration: 1.6, ease: "elastic.out(1,0.35)", immediateRender: false }, t0 + 0.2);
    FU.RULES.forEach((_, k) => tl.fromTo(`#${id}-r${k}`, { x: -40 }, { x: 0, duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + 0.3 + k * 0.12));
    if (active >= 0) tl.to(`#${id}-ul`, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power2.out", immediateRender: false }, t0 + 0.75);
    out(tl, `#${id}`, t0 + dur - 0.18);
  };

  // ---------------- the ledger page ----------------
  FU.ledger = (tl, layer, t0, dur, o = {}) => {
    const id = nid("fl"), Y = o.y ?? 300, rows = o.rows || [];
    let c = `<g transform="translate(540,${Y}) rotate(-3)"><g filter="url(#fuDrop)"><rect x="-400" y="0" width="800" height="${180 + rows.length * 124}" fill="url(#fuLines)" ${O(4)}/></g>
      <path d="M-300,0V${180 + rows.length * 124}" stroke="#e86a6a" stroke-width="3"/><rect x="-410" y="-24" width="820" height="40" rx="6" fill="#2a5a3a" ${O(4)}/>
      <text x="-270" y="96" font-family="Sriracha" font-size="58" fill="#2a3a8a">บัญชีของกิน · ${o.day || "วันที่ 100"}</text>`;
    rows.forEach(([label, val, at, m], k) => {
      const y = 210 + k * 124;
      c += `<g id="${id}-row${k}"><text x="-270" y="${y}" font-family="Sriracha" font-size="56" fill="#2a2a3a">${label}</text><text id="${id}-v${k}" x="300" y="${y}" text-anchor="end" font-family="Sriracha" font-size="62" fill="${m ? U.red : "#2a2a3a"}">${val}</text>
        ${m === "circle" ? `<ellipse id="${id}-c${k}" cx="200" cy="${y - 20}" rx="150" ry="52" fill="none" stroke="${U.red}" stroke-width="7" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" transform="rotate(-4 200 ${y - 20})"/>` : ""}</g>`;
    });
    c += `</g>`;
    put(layer, `<g id="${id}">${c}</g>`);
    hide(tl, `#${id}`, 0);
    tl.fromTo(`#${id}`, { opacity: 0, y: 160 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.5)", immediateRender: false }, t0);
    rows.forEach(([, , at, m], k) => {
      hide(tl, `#${id}-row${k}`, 0);
      tl.fromTo(`#${id}-row${k}`, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.3, ease: "power2.out", immediateRender: false }, t0 + (at ?? 0.3 + k * 0.3));
      if (m === "circle") tl.to(`#${id}-c${k}`, { attr: { "stroke-dashoffset": 0 }, duration: 0.45, ease: "power2.inOut", immediateRender: false }, t0 + (at ?? 0.3) + 0.35);
    });
    out(tl, `#${id}`, t0 + dur - 0.18);
  };

  // ---------------- knowledge card ----------------
  FU.card = (tl, layer, t0, dur, o = {}) => {
    const id = nid("fk"), rows = o.rows || [], Y = o.y ?? 280, col = o.color || U.red, H = 190 + rows.length * 170 + (o.foot ? 120 : 0);
    let c = `<g transform="translate(540,${Y})"><g filter="url(#fuDrop)"><rect x="-450" y="0" width="900" height="${H}" rx="34" fill="${U.paper}" ${O(5)}/></g>
      <path d="M-450,34Q-450,0 -416,0H416Q450,0 450,34V130H-450Z" fill="${col}" ${O(5)}/>
      <text x="0" y="90" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="58" fill="#fff">${o.title || ""}</text>`;
    rows.forEach((r, k) => {
      const y = 230 + k * 170;
      c += `<g id="${id}-row${k}"><g transform="translate(-330,${y})"><g id="${id}-i${k}">${coin(r.icon, 1)}</g></g>
        <text x="-235" y="${y + (r.sub ? 0 : 20)}" font-family="Kanit" font-weight="900" font-size="${r.size || 54}" fill="${U.ink}">${r.text}</text>
        ${r.sub ? `<text x="-235" y="${y + 52}" font-family="Kanit" font-weight="700" font-size="38" fill="#6a6058">${r.sub}</text>` : ""}
        <g transform="translate(370,${y})">${mark(r.mark, `${id}-m${k}`)}</g></g>`;
    });
    if (o.foot) c += `<g id="${id}-foot" transform="translate(0,${H - 70})"><rect x="-400" y="-48" width="800" height="90" rx="45" fill="${o.footColor || U.ink}"/><text y="14" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="48" fill="#fff">${o.foot}</text></g>`;
    c += `</g>`;
    put(layer, `<g id="${id}">${c}</g>`);
    hide(tl, `#${id}`, 0);
    tl.fromTo(`#${id}`, { opacity: 0, y: 120, scale: 0.9, transformOrigin: "540px 600px" }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.7)", immediateRender: false }, t0);
    rows.forEach((r, k) => {
      const at = t0 + (r.at ?? 0.25 + k * 0.35);
      hide(tl, `#${id}-row${k}`, 0);
      tl.fromTo(`#${id}-row${k}`, { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(2)", immediateRender: false }, at);
      tl.fromTo(`#${id}-i${k}`, { scale: 0.3, rotation: -30, transformOrigin: "50% 50%" }, { scale: 1, rotation: 0, duration: 0.6, ease: "elastic.out(1,0.5)", immediateRender: false }, at);
      bob(tl, `#${id}-i${k}`, at + 0.6, t0 + dur - at - 0.6, 5);
      if (r.mark) { hide(tl, `#${id}-m${k}`, 0); pop(tl, `#${id}-m${k}`, at + (r.markAt ?? 0.45), 2.4); }
    });
    if (o.foot) { hide(tl, `#${id}-foot`, 0); pop(tl, `#${id}-foot`, t0 + (o.footAt ?? 0.3 + rows.length * 0.35), 0.6); }
    out(tl, `#${id}`, t0 + dur - 0.18);
  };

  // ---------------- versus: two coins ----------------
  FU.versus = (tl, layer, t0, dur, o = {}) => {
    const id = nid("fv"), Y = o.y ?? 640;
    const side = (d, x, k) => `<g transform="translate(${x},${Y})"><g id="${id}-s${k}"><g filter="url(#fuDrop)"><rect x="-210" y="-230" width="420" height="500" rx="34" fill="${U.paper}" ${O(5)}/></g>
      <g transform="translate(0,-60)">${coin(d.icon, 1.6)}</g><text y="160" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${d.size || 50}" fill="${U.ink}">${d.text}</text>
      ${d.sub ? `<text y="214" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="36" fill="#6a6058">${d.sub}</text>` : ""}
      <g transform="translate(150,-190)">${mark(d.mark, `${id}-m${k}`)}</g></g></g>`;
    let c = (o.title ? `<g transform="translate(540,${Y - 330})"><rect x="-380" y="-50" width="760" height="100" rx="50" fill="${o.color || U.ink}" ${O(4)}/><text y="18" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="50" fill="#fff">${o.title}</text></g>` : "") + side(o.a, 300, 0) + side(o.b, 780, 1);
    put(layer, `<g id="${id}">${c}</g>`);
    hide(tl, `#${id}`, 0); tl.set(`#${id}`, { opacity: 1 }, t0);
    [0, 1].forEach((k) => { tl.fromTo(`#${id}-s${k}`, { opacity: 0, y: 140 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.8)", immediateRender: false }, t0 + k * (o.gap ?? 0.5)); hide(tl, `#${id}-m${k}`, 0); pop(tl, `#${id}-m${k}`, t0 + (o.markAt || [0.6, 1.1])[k], 2.4); });
    out(tl, `#${id}`, t0 + dur - 0.18);
  };

  // ---------------- crayon map: school → market ----------------
  FU.map = (tl, layer, t0, dur, o = {}) => {
    const id = nid("fm"), [g0, g1] = o.go || [0.4, dur - 0.6];
    const A = [270, 1180], B = [800, 520], path = `M${A[0]},${A[1]}C380,1000 300,860 470,800S760,700 ${B[0]},${B[1]}`;
    let c = `<rect width="1080" height="1920" fill="#2a2420" opacity=".55"/><g filter="url(#fuDrop)"><path d="M70,300L1010,260L1030,1380L50,1420Z" fill="#f4ecd4" ${O(5)}/></g>
      <path d="M90,320L990,282L1008,1360L70,1398Z" fill="#cfe2b0"/>${Array.from({ length: 12 }, (_, k) => `<path d="M${100 + (k % 4) * 230},${340 + Math.floor(k / 4) * 330}l200,-8l6,280l-200,8Z" fill="${k % 3 ? "#b8d890" : "#a8cc7a"}" stroke="#8aaa60" stroke-width="3"/>`).join("")}
      <path d="M70,940Q540,900 1010,960" stroke="#8a847a" stroke-width="44" fill="none"/><path d="M70,940Q540,900 1010,960" stroke="#f2ead0" stroke-width="4" stroke-dasharray="20 20" fill="none"/>
      <path d="M720,300Q640,700 760,1390" stroke="#6ab0e0" stroke-width="30" fill="none" opacity=".9"/>
      <path id="${id}-rt" d="${path}" stroke="${U.red}" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="26 18" pathLength="1"/>`;
    const pin = (x, y, label, ic, k) => `<g transform="translate(${x},${y})"><g id="${id}-p${k}"><ellipse cy="6" rx="40" ry="12" fill="#000" opacity=".25"/><path d="M0,0C-30,-40 -56,-60 -56,-100A56,56 0 1 1 56,-100C56,-60 30,-40 0,0Z" fill="${k ? U.red : U.blue}" ${O(4)}/><circle cy="-100" r="36" fill="#fff" ${O(3)}/><g transform="translate(0,-100) scale(.5)">${(I[ic] || (() => ""))()}</g>
      <g transform="translate(0,${k ? -190 : 60})"><rect x="-150" y="-36" width="300" height="70" rx="35" fill="#fff" ${O(4)}/><text y="16" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="${U.ink}">${label}</text></g></g></g>`;
    I.school = () => `<path d="M-40,40V-10L0,-40L40,-10V40Z" fill="#efdcae" ${O(4)}/><path d="M-50,-6L0,-48L50,-6" stroke="#c4532f" stroke-width="10" fill="none"/><rect x="-10" y="10" width="20" height="30" fill="#3f6f78"/>`;
    I.market = () => `<path d="M-44,-10L-30,-40H30L44,-10Z" fill="#2f7ac8" ${O(4)}/><rect x="-36" y="-10" width="72" height="50" fill="#e8d8a8" ${O(4)}/>${[-20, 0, 20].map((x) => `<rect x="${x - 7}" y="4" width="14" height="18" fill="${U.red}"/>`).join("")}`;
    c += pin(A[0], A[1], (o.from || ["โรงเรียน"])[0], (o.from || [0, "school"])[1], 0) + pin(B[0], B[1], (o.to || ["ตลาดร้าง"])[0], (o.to || [0, "market"])[1], 1);
    c += `<g id="${id}-run"><circle r="30" fill="#f2c83a" ${O(4)}/><circle cy="-6" r="10" fill="#c88a5a"/><path d="M-12,18Q0,0 12,18" stroke="#d8302a" stroke-width="6" fill="none"/></g>`;
    put(layer, `<g id="${id}">${c}</g>`);
    hide(tl, `#${id}`, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    tl.fromTo(`#${id}-p0`, { y: -300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "bounce.out", immediateRender: false }, t0 + 0.1);
    hide(tl, `#${id}-p1`, 0);
    tl.fromTo(`#${id}-p1`, { y: -300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "bounce.out", immediateRender: false }, t0 + g1);
    // the route is drawn by a mask-free trick: the dash pattern revealed with a growing clip of dashoffset on a solid copy
    tl.fromTo(`#${id}-rt`, { attr: { "stroke-dasharray": "0 1" } }, { attr: { "stroke-dasharray": "1 0" }, duration: g1 - g0, ease: "power1.inOut", immediateRender: false }, t0 + g0);
    const pe = document.getElementById(`${id}-rt`), runner = document.getElementById(`${id}-run`), c0 = { u: 0 };
    const place = (u) => { const L = pe.getTotalLength(), p = pe.getPointAtLength(L * u); runner.setAttribute("transform", `translate(${p.x.toFixed(1)},${p.y.toFixed(1)})`); };
    place(0);
    tl.to(c0, { u: 1, duration: g1 - g0, ease: "power1.inOut", immediateRender: false, onUpdate: () => place(c0.u) }, t0 + g0);
    out(tl, `#${id}`, t0 + dur - 0.18);
  };

  // ---------------- masking-tape name tags ----------------
  FU.tags = (tl, layer, t0, items, dur = 3) => items.forEach(([x, y, name, at, rot]) => {
    const id = nid("ft");
    put(layer, `<g transform="translate(${x},${y}) rotate(${rot ?? -4})"><g id="${id}"><rect x="${-name.length * 15 - 24}" y="-34" width="${name.length * 30 + 48}" height="64" fill="#f2e6c0" opacity=".96" ${O(3)}/><path d="M${-name.length * 15 - 24},-34l-8,8l8,8l-8,8l8,8l-8,8l8,8" stroke="#d8c898" stroke-width="3" fill="none"/>
      <text y="14" text-anchor="middle" font-family="Sriracha" font-size="42" fill="#2a2a3a">${name}</text></g></g>`);
    hide(tl, `#${id}`, 0); pop(tl, `#${id}`, t0 + at, 0.5); out(tl, `#${id}`, t0 + dur - 0.18);
  });

  // ---------------- the radio's number ----------------
  FU.radio = (tl, layer, t0, dur, o = {}) => {
    const id = nid("fn");
    put(layer, `<g id="${id}" transform="translate(540,${o.y ?? 640})"><circle r="360" fill="url(#fuAmber)"/><text y="70" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="230" fill="#fff4d8" stroke="#ffb04a" stroke-width="6">${o.word || "หก"}</text>
      ${Array.from({ length: 3 }, (_, k) => `<circle id="${id}-w${k}" r="200" fill="none" stroke="#ffcf80" stroke-width="5"/>`).join("")}</g>`);
    hide(tl, `#${id}`, 0);
    tl.fromTo(`#${id}`, { opacity: 0, scale: 0.6, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + (o.at || 0));
    for (let k = 0; k < 3; k++) tl.fromTo(`#${id}-w${k}`, { scale: 0.5, opacity: 0.9, transformOrigin: "50% 50%" }, { scale: 2, opacity: 0, duration: 1.1, ease: "power1.out", immediateRender: false }, t0 + (o.at || 0) + k * 0.3);
    out(tl, `#${id}`, t0 + dur - 0.2);
  };

  // ---------------- rewind ----------------
  FU.rewind = (tl, layer, t0, dur, label) => {
    const id = nid("fw");
    put(layer, `<g id="${id}"><rect width="1080" height="1920" fill="#0a0e14" opacity=".2"/>${Array.from({ length: 9 }, (_, k) => `<rect id="${id}-l${k}" x="0" y="${k * 220}" width="1080" height="${8 + (k % 3) * 6}" fill="#fff" opacity=".18"/>`).join("")}
      <g transform="translate(540,300)"><g id="${id}-b"><rect x="-190" y="-70" width="380" height="140" rx="70" fill="#ff5a3a" stroke="#fff" stroke-width="6"/>
      <text y="26" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="78" fill="#fff">↺ ${label}</text></g></g></g>`);
    hide(tl, `#${id}`, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.12, immediateRender: false }, t0);
    pop(tl, `#${id}-b`, t0 + 0.05, 0.4);
    for (let k = 0; k < 9; k++) tl.fromTo(`#${id}-l${k}`, { y: 0 }, { y: 1920, duration: 0.6, repeat: Math.ceil(dur / 0.6), ease: "none", immediateRender: false }, t0 + k * 0.05);
    out(tl, `#${id}`, t0 + dur - 0.15);
  };

  // ---------------- next episode: the ledger page "พรุ่งนี้ต้องหา" ----------------
  FU.next = (tl, layer, t0, dur, o = {}) => {
    const id = nid("fx");
    put(layer, `<g id="${id}"><rect width="1080" height="1920" fill="#0c0a0a" opacity=".86"/>
      <g transform="translate(540,560) rotate(-3)"><g id="${id}-pg"><g filter="url(#fuDrop)"><rect x="-430" y="-260" width="860" height="700" fill="url(#fuLines)" ${O(4)}/></g><path d="M-330,-260V440" stroke="#e86a6a" stroke-width="3"/>
        <rect x="-440" y="-286" width="880" height="44" rx="6" fill="#2a5a3a" ${O(4)}/>
        <text x="-300" y="-150" font-family="Sriracha" font-size="56" fill="#2a3a8a">พรุ่งนี้ต้องหา:</text>
        <text x="-300" y="-40" font-family="Sriracha" font-size="48" fill="#c8302a">ตอนที่ ${o.ep}</text>
        <text x="-300" y="80" font-family="Kanit" font-weight="900" font-size="${Math.min(54, Math.round(1180 / o.l1.length))}" fill="#2a2a3a">${o.l1}</text>
        <text x="-300" y="170" font-family="Kanit" font-weight="900" font-size="64" fill="#c8302a">${o.l2}</text>
        <path d="M-300,200Q0,214 330,196" stroke="#c8302a" stroke-width="6" fill="none"/>
        <text x="-300" y="320" font-family="Sriracha" font-size="40" fill="#5a5a6a">${o.cta || "กดติดตาม… แล้วอยู่หลังรั้วไปด้วยกัน"}</text></g></g>
      <text x="540" y="1340" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#fff" letter-spacing="10">ROD MAI CLUB</text>
      <text x="540" y="1396" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="32" fill="#8a94a0">รั้วสุดท้าย</text></g>`);
    hide(tl, `#${id}`, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, t0);
    tl.fromTo(`#${id}-pg`, { y: 200, rotation: 8, svgOrigin: "0 0" }, { y: 0, rotation: 0, svgOrigin: "0 0", duration: 0.6, ease: "back.out(1.5)", immediateRender: false }, t0 + 0.05);
  };
})();
