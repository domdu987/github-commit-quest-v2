// "ต่อหัวเสือ" on-screen graphics in the channel's house style (mmui / sinkui): ink outline 4–5, flat fills + one shade + one highlight,
// soft drop shadow (#muDrop from mmui.js), Kanit; everything enters eased and staggered, then keeps a small secondary motion.
// The world's materials: a weathered teak board hung from the shrine post by a red-and-yellow cloth, a paper talisman strip, a plank sign.
// Screen space: pass L.light. Every function: (tl, layer, t0, dur, o)
//   HnUI.rules(…, { active, done: [i…], y, s })   กฎของยายบัว: the teak board, 3 rows (icon · rhyme), done rows ticked, the active row
//                                                highlighted with its rhyme words underlined, rows not reached faded
//   HnUI.tag(…, { x, y, text, c })                a name pill (ภูมิ 10 ขวบ …) that pops in
//   HnUI.still(…)                                 card: one hornet circling a calm face = ✓ stand still · a hand swatting = ✗ (stings)
//   HnUI.water(…)                                 cross-section: the pond, a swimmer under water, the swarm hovering just above the surface,
//                                                the head breaking the surface → hornets drop on it (✗)
//   HnUI.indoors(…)                               card: run → the house with its door shut ✓ · shade beats open ground
//   HnUI.kidney(…)                                card: many stings → 48-hour clock → kidney, tea-dark urine
//   HnUI.danger(…)                                card: three danger signs (breath, swollen lips, fainting) → phone 1669
//   HnUI.nextBoard(…, { l1, l2, l3 })             the end card: the plank sign "ระวัง! รังต่อ" on the shrine fence + a paper note (next episode)
//   HnUI.finale(…)                                the series end card: the board with all three rules ticked + "แชร์ให้คนที่คุณรัก…"
(function () {
  const U = { ink: "#26201c", paper: "#fdf6e6", teak: "#9a6234", teakD: "#6a3e1e", teakL: "#c8884a", red: "#d8302a", redD: "#a01e18", yellow: "#ffd23a",
    green: "#2fa864", greenD: "#1e7a48", orange: "#f08a1a", water: "#3a8ab8", waterD: "#1e5a80", sky: "#cfe6f4" };
  const SO = (w = 4) => `stroke="${U.ink}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  let seq = 0;
  const HnUI = (window.HnUI = {});
  const hornet = (x, y, s, rot = 0) => `<g transform="translate(${x},${y}) rotate(${rot})">${Hn.hornet({ s })}</g>`;
  const tick = (x, y, id) => `<g transform="translate(${x},${y})"><circle r="34" fill="${U.green}" ${SO(3.5)}/><path id="${id}" d="M-15,0l10,12l20,-23" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1"/></g>`;
  const cross = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><circle r="40" fill="${U.red}" ${SO(4)}/><path d="M-16,-16L16,16M16,-16L-16,16" stroke="#fff" stroke-width="10" stroke-linecap="round"/></g>`;
  const inOut = (tl, id, t0, dur) => {
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { y: 90, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.8)", immediateRender: false }, t0);
    tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + dur - 0.2);
  };
  const card = (id, x, y, W, H, head, hc = U.red) => `<g transform="translate(${x},${y})"><g id="${id}"><g filter="url(#muDrop)"><rect x="${-W / 2}" y="0" width="${W}" height="${H}" rx="36" fill="${U.paper}" ${SO(5)}/></g>
    <path d="M${-W / 2},36Q${-W / 2},0 ${-W / 2 + 36},0H${W / 2 - 36}Q${W / 2},0 ${W / 2},36V112H${-W / 2}Z" fill="${hc}" ${SO(5)}/><text y="78" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#fff">${head}</text>`;

  // ---------------- rule icons (100-unit, centred) ----------------
  HnUI.icon = (k, x, y, s, id) => {
    let g = "";
    if (k === 0) g = `${hornet(-18, -6, 0.62)}<g transform="translate(26,22)"><path d="M-14,30V-6Q-14,-16 -6,-16Q2,-16 2,-6V-14Q2,-22 10,-22Q18,-22 18,-12V-6Q18,-14 26,-14Q32,-14 32,-4V24Q32,40 16,40H0Q-14,40 -14,30Z" fill="#e8b48a" ${SO(3)}/></g>
      <path d="M-40,40L44,-40" stroke="${U.red}" stroke-width="9" stroke-linecap="round"/>`;
    if (k === 1) g = `<path d="M-46,30q12,-8 24,0t24,0t24,0t24,0" stroke="${U.water}" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M-46,46q12,-8 24,0t24,0t24,0t24,0" stroke="${U.water}" stroke-width="6" fill="none" opacity=".6"/>
      <g transform="translate(-6,-12)"><circle cx="0" cy="-22" r="11" fill="#e8b48a" ${SO(3)}/><path d="M0,-10l-6,22l-14,14M-6,12l10,16M-2,-4l16,6M-2,-4l-16,-2" stroke="${U.ink}" stroke-width="7" stroke-linecap="round" fill="none"/></g>
      <path d="M-44,40L44,-44" stroke="${U.red}" stroke-width="9" stroke-linecap="round"/>`;
    if (k === 2) g = `<path d="M-40,40V-6L0,-38L40,-6V40Z" fill="#fff" ${SO(3.5)}/><rect x="-8" y="-20" width="16" height="44" fill="${U.red}"/><rect x="-22" y="-6" width="44" height="16" fill="${U.red}"/>
      <g transform="translate(30,30)"><circle r="6" fill="${U.red}"/></g><g transform="translate(-30,30)"><circle r="6" fill="${U.red}"/></g>`;
    return `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}"><circle r="62" fill="#fff" ${SO(4)}/><circle r="62" fill="none" stroke="${U.orange}" stroke-width="8" opacity=".3" transform="scale(.86)"/>${g}</g></g>`;
  };
  // the rhyme of each rule: [first half, second half]; the rhyming words get the underline
  HnUI.RULES = [["ต่อบินมาวน", "อย่าลนอย่าปัด"], ["ต่อรุมให้วิ่ง", "อย่าทิ้งตัวลงน้ำ"], ["ต่อยหลายแผล อย่าแค่นอนรอ", "ต้องไปหาหมอ"]];

  HnUI.rules = (tl, layer, t0, dur, o = {}) => {
    const id = `hr${seq++}`, active = o.active ?? -1, done = o.done || [], Y = o.y ?? 420, S = o.s ?? 1, W = 920, H = 820;
    let c = `<path d="M-300,-${Y}L-260,40M300,-${Y}L260,40" stroke="${U.red}" stroke-width="22"/><path d="M-300,-${Y}L-260,40M300,-${Y}L260,40" stroke="${U.yellow}" stroke-width="6" stroke-dasharray="18 22"/>`;
    c += `<g filter="url(#muDrop)"><rect x="${-W / 2}" y="20" width="${W}" height="${H}" rx="22" fill="${U.teak}" ${SO(6)}/></g>
      ${Array.from({ length: 7 }, (_, k) => `<path d="M${-W / 2 + 20},${80 + k * 118}q${W / 2},${k % 2 ? 14 : -12} ${W - 40},0" stroke="${U.teakD}" stroke-width="3" fill="none" opacity=".55"/>`).join("")}
      <rect x="${-W / 2 + 26}" y="46" width="${W - 52}" height="${H - 52}" rx="14" fill="${U.paper}" ${SO(4)}/>
      <text y="138" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="${U.redD}">กฎของยายบัว</text>
      <path d="M-200,160q200,14 400,0" stroke="${U.orange}" stroke-width="6" fill="none" stroke-linecap="round"/>
      ${[-280, 280].map((x) => `<circle cx="${x}" cy="120" r="12" fill="${U.teakD}"/>`).join("")}`;
    HnUI.RULES.forEach(([a, b], k) => {
      const y = 290 + k * 200, st = done.includes(k) ? "done" : k === active ? "active" : active < 0 ? "all" : "next";
      c += `<g id="${id}-row${k}" opacity="${st === "next" ? 0.35 : 1}">`;
      if (st === "active") c += `<rect id="${id}-hl" x="-300" y="${y - 74}" width="700" height="150" rx="20" fill="${U.yellow}" opacity=".6"/>`;
      c += HnUI.icon(k, -340, y, 0.95, `${id}-i${k}`);
      c += `<text x="-250" y="${y - 12}" font-family="Kanit" font-weight="${st === "active" ? 900 : 800}" font-size="${a.length > 14 ? 46 : 54}" fill="${U.ink}">${a}</text>
        <text x="-250" y="${y + 56}" font-family="Kanit" font-weight="900" font-size="54" fill="${U.redD}">${b}</text>`;
      if (st === "active") c += `<path id="${id}-ul" d="M-250,${y + 72}h${b.length * 34}" stroke="${U.red}" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>`;
      if (st === "done") c += tick(380, y, `${id}-ck${k}`);
      c += `</g>`;
    });
    put(layer, `<g transform="translate(540,${Y}) scale(${S})"><g id="${id}">${c}</g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { y: -700, rotation: -4, opacity: 1, svgOrigin: "0 0" }, { y: 0, rotation: 0, svgOrigin: "0 0", duration: 0.75, ease: "bounce.out", immediateRender: false }, t0);
    tl.to(`#${id}`, { rotation: 1.6, svgOrigin: "0 0", duration: 1.1, yoyo: true, repeat: Math.ceil(dur / 1.1), ease: "sine.inOut" }, t0 + 0.75);
    done.forEach((k) => tl.fromTo(`#${id}-ck${k}`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.3, immediateRender: false }, t0 + 0.6 + k * 0.15));
    if (active >= 0) {
      tl.fromTo(`#${id}-hl`, { scaleX: 0, svgOrigin: "-300 0" }, { scaleX: 1, svgOrigin: "-300 0", duration: 0.4, ease: "power2.out", immediateRender: false }, t0 + 0.8);
      tl.fromTo(`#${id}-ul`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, immediateRender: false }, t0 + 1.2);
      tl.fromTo(`#${id}-i${active}`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.12, svgOrigin: "0 0", duration: 0.35, yoyo: true, repeat: Math.ceil(dur / 0.7), ease: "sine.inOut", immediateRender: false }, t0 + 1);
    }
    tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
    return id;
  };

  HnUI.tag = (tl, layer, t0, dur, o = {}) => {
    const id = `ht${seq++}`, text = o.text || "", w = 30 * text.length + 74;
    put(layer, `<g transform="translate(${o.x},${o.y})"><g id="${id}"><rect x="${-w / 2 + 5}" y="-28" width="${w}" height="66" rx="33" fill="#1a120c" opacity=".3"/>
      <rect x="${-w / 2}" y="-36" width="${w}" height="66" rx="33" fill="${U.paper}" ${SO(4)}/><circle cx="${-w / 2 + 34}" cy="-3" r="16" fill="${o.c || U.orange}" ${SO(3)}/>
      <text x="${-w / 2 + 60}" y="9" font-family="Kanit" font-weight="800" font-size="34" fill="#2a2018">${text}</text></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.set(`#${id}`, { opacity: 1 }, t0);
    tl.fromTo(`#${id}`, { scale: 0.3, rotation: -8, svgOrigin: "0 0" }, { scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.5, ease: "back.out(3)", immediateRender: false }, t0);
    tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + dur - 0.2);
  };

  // a simple face for the cards (rig-like), mood calm | pain
  const face = (x, y, s, mood) => `<g transform="translate(${x},${y}) scale(${s})"><circle r="70" fill="#e8b48a" ${SO(4)}/><path d="M-70,-10C-70,-80 70,-80 70,-10Q40,-50 0,-46Q-40,-50 -70,-10Z" fill="#1a1412" ${SO(3)}/>
    ${mood === "pain" ? `<path d="M-34,0l16,8M34,0l-16,8M-22,36q22,-14 44,0" stroke="${U.ink}" stroke-width="6" fill="none" stroke-linecap="round"/><circle cx="40" cy="22" r="14" fill="#ff6a5a" opacity=".7"/>`
      : `<circle cx="-24" cy="4" r="7" fill="${U.ink}"/><circle cx="24" cy="4" r="7" fill="${U.ink}"/><path d="M-16,34h32" stroke="${U.ink}" stroke-width="6" stroke-linecap="round"/>`}</g>`;

  // ✓ stand still / ✗ swatting gets you stung
  HnUI.still = (tl, layer, t0, dur, o = {}) => {
    const id = `hs${seq++}`;
    let c = card(id, 540, o.y ?? 360, 940, 760, "ต่อบินวน · ทำยังไง?", U.orange);
    c += `<g transform="translate(-230,420)"><rect x="-200" y="-260" width="400" height="460" rx="24" fill="#eaf6e8" ${SO(3)}/>${face(0, -40, 1)}<g id="${id}-h1">${hornet(0, -150, 0.9)}</g>
      <text y="160" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="50" fill="${U.greenD}">ยืนนิ่ง</text>${tick(150, -210, `${id}-ok`)}</g>
      <g transform="translate(230,420)"><rect x="-200" y="-260" width="400" height="460" rx="24" fill="#fbe6e2" ${SO(3)}/>${face(0, -40, 1, "pain")}
      <g id="${id}-hand"><path d="M-110,-20l-60,-40M-120,-10q-40,-10 -60,-40" stroke="#e8b48a" stroke-width="30" stroke-linecap="round"/></g><g id="${id}-h2">${hornet(60, -10, 0.9, 30)}</g>
      <text y="160" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="50" fill="${U.redD}">ปัด = โดนต่อย</text>${cross(150, -210, 0.85)}</g></g></g>`;
    put(layer, c);
    inOut(tl, id, t0, dur);
    tl.fromTo(`#${id}-h1`, { x: -60 }, { x: 60, duration: 0.6, yoyo: true, repeat: Math.ceil(dur / 0.6), ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-hand`, { rotation: -20, svgOrigin: "-110 -20" }, { rotation: 20, svgOrigin: "-110 -20", duration: 0.18, yoyo: true, repeat: Math.ceil(dur / 0.18), ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-ok`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.3, immediateRender: false }, t0 + 0.7);
  };

  // the pond in section: under water you hold your breath, the swarm waits over the surface; you come up → they drop
  HnUI.water = (tl, layer, t0, dur, o = {}) => {
    const id = `hw${seq++}`, Y = o.y ?? 300;
    let c = card(id, 540, Y, 960, 1000, "โดดน้ำหนี · รอดไหม?", U.waterD);
    c += `<g transform="translate(0,140)"><rect x="-440" y="0" width="880" height="320" fill="${U.sky}"/><rect x="-440" y="320" width="880" height="500" fill="${U.water}"/><rect x="-440" y="320" width="880" height="500" fill="url(#hnPond)" opacity=".7"/>
      <path d="M-440,320q55,-14 110,0t110,0t110,0t110,0t110,0t110,0t110,0t110,0" stroke="#e6f6ff" stroke-width="7" fill="none"/>
      <path d="M-440,780h880" stroke="#5a4a2a" stroke-width="40"/>
      <g id="${id}-sw"></g>
      <g id="${id}-man"><g transform="translate(-60,560)">
        <path d="M-12,40C-40,44 -46,90 -40,150L40,150C46,90 40,44 12,40Z" fill="#2a2a30" ${SO(4)}/><path d="M-6,70C-14,64 14,58 6,70C14,80 -14,82 -6,70Z" fill="#ffb4c8"/>
        <path d="M-36,60Q-90,20 -110,-30M36,60Q90,20 110,-30" stroke="#e8b48a" stroke-width="24" stroke-linecap="round" fill="none"/><path d="M-36,60Q-90,20 -110,-30M36,60Q90,20 110,-30" stroke="${U.ink}" stroke-width="3" fill="none" opacity=".5"/>
        <path d="M-24,148L-46,260M24,148L40,262" stroke="#9ec0e0" stroke-width="30" stroke-linecap="round"/><path d="M-50,262l-20,10M44,262l22,8" stroke="#f6f4ee" stroke-width="18" stroke-linecap="round"/>
        <circle r="44" fill="#e8b48a" ${SO(4)}/><path d="M-44,-6C-44,-60 44,-60 44,-6Q24,-30 0,-28Q-24,-30 -44,-6Z" fill="#1a1412" ${SO(3)}/><path d="M30,-40C70,-60 90,-30 80,10Q60,-10 40,-20Z" fill="#1a1412" ${SO(3)}/>
        <path d="M-20,4q8,-6 14,0M8,4q8,-6 14,0" stroke="${U.ink}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M-8,26q8,6 16,0" stroke="${U.ink}" stroke-width="4" fill="none"/>
        <g id="${id}-bub">${[[-10, -80, 12], [14, -126, 8], [-4, -170, 6]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="none" stroke="#e6f6ff" stroke-width="3"/>`).join("")}</g></g></g>
      <g transform="translate(250,600)"><rect x="-135" y="-50" width="270" height="100" rx="20" fill="#fff" ${SO(3)}/><text y="16" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="${U.redD}">ต้องหายใจ</text></g>
      </g></g></g>`;
    put(layer, c);
    inOut(tl, id, t0, dur);
    Hn.swarm(tl, document.getElementById(`${id}-sw`), { id: `${id}-s`, n: 18, s: 0.55, cx: 0, cy: 230, rx: 360, ry: 50, t0, dur, seed: 21 });
    // the swimmer comes up for air at ~55%; the swarm drops onto the head (the head reaches the surface)
    const up = t0 + dur * 0.55;
    tl.fromTo(`#${id}-man`, { y: 0 }, { y: -230, duration: 0.6, ease: "power2.out", immediateRender: false }, up);
    tl.to(`#${id}-bub`, { opacity: 0, duration: 0.2 }, up);
    tl.to(`#${id}-sw`, { y: 60, duration: 0.4, ease: "power2.in" }, up + 0.4);
    put(layer, `<g id="${id}-x" opacity="0">${cross(820, Y + 470, 1.2)}</g>`);
    tl.set(`#${id}-x`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}-x`, { opacity: 0, scale: 0.2, svgOrigin: `820 ${Y + 470}` }, { opacity: 1, scale: 1, svgOrigin: `820 ${Y + 470}`, duration: 0.4, ease: "back.out(3)", immediateRender: false }, up + 0.7);
    tl.to(`#${id}-x`, { opacity: 0, duration: 0.2 }, t0 + dur - 0.2);
  };

  // run, then indoors: the open field ✗ vs the house with the door shut ✓
  HnUI.indoors = (tl, layer, t0, dur, o = {}) => {
    const id = `hi${seq++}`;
    let c = card(id, 540, o.y ?? 380, 940, 720, "ถูกรุม · วิ่งไปไหน?", U.greenD);
    c += `<g transform="translate(-230,400)"><rect x="-200" y="-240" width="400" height="420" rx="24" fill="#fbe6e2" ${SO(3)}/><path d="M-200,100H200" stroke="#8aaa52" stroke-width="40"/><circle cx="110" cy="-150" r="40" fill="#ffd23a" ${SO(3)}/>
      <g transform="translate(-20,50)"><circle cy="-120" r="20" fill="#e8b48a" ${SO(3)}/><path d="M0,-100v60l-20,40M0,-40l24,36M0,-86l-30,20M0,-86l30,-14" stroke="${U.ink}" stroke-width="10" stroke-linecap="round" fill="none"/></g>
      <g id="${id}-s1"></g><text y="160" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="${U.redD}">ที่โล่ง</text>${cross(150, -190, 0.8)}</g>
      <g transform="translate(230,400)"><rect x="-200" y="-240" width="400" height="420" rx="24" fill="#eaf6e8" ${SO(3)}/><path d="M-200,100H200" stroke="#8aaa52" stroke-width="40"/>
      <path d="M-130,90V-40L0,-140L130,-40V90Z" fill="${U.teakL}" ${SO(4)}/><path d="M-150,-30L0,-160L150,-30" stroke="${U.redD}" stroke-width="18" fill="none" stroke-linecap="round"/>
      <rect id="${id}-door" x="-36" y="0" width="72" height="90" fill="${U.teakD}" ${SO(3)}/><rect x="56" y="-20" width="50" height="50" fill="#cfe6f4" ${SO(3)}/>
      <text y="160" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="${U.greenD}">เข้าบ้าน</text>${tick(150, -190, `${id}-ok`)}</g></g></g>`;
    put(layer, c);
    inOut(tl, id, t0, dur);
    Hn.swarm(tl, document.getElementById(`${id}-s1`), { id: `${id}-sw`, n: 9, s: 0.38, cx: -20, cy: -60, rx: 90, ry: 60, t0, dur, seed: 8 });
    tl.fromTo(`#${id}-ok`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.3, immediateRender: false }, t0 + 0.8);
  };

  // many stings → within 2 days → the kidneys; tea-dark urine, little of it
  HnUI.kidney = (tl, layer, t0, dur, o = {}) => {
    const id = `hk${seq++}`;
    let c = card(id, 540, o.y ?? 360, 960, 820, "พิษที่มาทีหลัง", U.redD);
    c += `<g transform="translate(-300,330)"><circle r="110" fill="#fff" ${SO(4)}/><g transform="rotate(-30)"><rect x="-80" y="-26" width="160" height="52" rx="26" fill="#e8b48a" ${SO(4)}/><path d="M80,-20q30,0 30,20q0,20 -30,20" fill="#e8b48a" ${SO(3)}/>
        ${[[-50, -6], [-20, 8], [6, -10], [30, 6], [54, -6], [-36, 14]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="10" fill="#ff7a6a" opacity=".6"/><circle cx="${x}" cy="${y}" r="3.5" fill="${U.redD}"/>`).join("")}</g>
      <text y="160" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="${U.ink}">หลายแผล</text></g>
      <path d="M-170,330h80" stroke="${U.ink}" stroke-width="8" stroke-linecap="round"/><path d="M-110,310l20,20l-20,20" stroke="${U.ink}" stroke-width="8" fill="none" stroke-linecap="round"/>
      <g transform="translate(0,330)"><circle r="110" fill="#fff" ${SO(4)}/><circle r="88" fill="none" stroke="#e8e0d0" stroke-width="10"/><path id="${id}-arc" d="M0,-88A88,88 0 1 1 -1,-88" stroke="${U.orange}" stroke-width="12" fill="none" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
        <g id="${id}-hand"><path d="M0,0V-70" stroke="${U.ink}" stroke-width="8" stroke-linecap="round"/></g><circle r="9" fill="${U.ink}"/>
        <text y="160" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="${U.ink}">ภายใน 2 วัน</text></g>
      <path d="M130,330h80" stroke="${U.ink}" stroke-width="8" stroke-linecap="round"/><path d="M190,310l20,20l-20,20" stroke="${U.ink}" stroke-width="8" fill="none" stroke-linecap="round"/>
      <g transform="translate(320,330)"><circle r="110" fill="#fff" ${SO(4)}/><g id="${id}-kid"><path d="M-40,-60C-90,-60 -90,60 -40,60C-10,60 -14,20 -2,0C-14,-20 -10,-60 -40,-60Z" fill="#c8504a" ${SO(4)}/>
        <path d="M40,-60C90,-60 90,60 40,60C10,60 14,20 2,0C14,-20 10,-60 40,-60Z" fill="#c8504a" ${SO(4)}/><path d="M-60,-30q-10,20 0,40" stroke="#f08a80" stroke-width="6" fill="none"/></g>
        <text y="160" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="${U.ink}">ไต</text></g>
      <g transform="translate(0,640)"><rect x="-380" y="-60" width="760" height="120" rx="26" fill="#fff3d6" ${SO(3)}/>
        <g transform="translate(-300,0)"><path d="M-22,-40h44l-6,80h-32Z" fill="#fff" ${SO(3)}/><path id="${id}-ur" d="M-19,10h38l-3,28h-32Z" fill="#7a4a1a"/></g>
        <text x="-240" y="16" font-family="Kanit" font-weight="900" font-size="42" fill="${U.redD}">ฉี่น้อย · สีเข้มเหมือนชา</text></g></g></g>`;
    put(layer, c);
    inOut(tl, id, t0, dur);
    tl.fromTo(`#${id}-arc`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: dur * 0.5, ease: "none", immediateRender: false }, t0 + 0.4);
    tl.fromTo(`#${id}-hand`, { rotation: 0, svgOrigin: "0 0" }, { rotation: 720, svgOrigin: "0 0", duration: dur * 0.5, ease: "none", immediateRender: false }, t0 + 0.4);
    tl.fromTo(`#${id}-kid`, { scale: 1, svgOrigin: "0 0" }, { scale: 0.9, svgOrigin: "0 0", duration: 0.4, yoyo: true, repeat: Math.ceil(dur / 0.8), ease: "sine.inOut", immediateRender: false }, t0 + dur * 0.5);
  };

  // danger signs → 1669
  HnUI.danger = (tl, layer, t0, dur, o = {}) => {
    const id = `hd${seq++}`;
    let c = card(id, 540, o.y ?? 380, 940, 760, "อาการแบบนี้ โทรทันที", U.red);
    const sign = (x, label, art, k) => `<g transform="translate(${x},330)"><g id="${id}-s${k}"><circle r="110" fill="#fff" ${SO(4)}/>${art}<text y="164" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="${U.ink}">${label}</text></g></g>`;
    c += sign(-300, "หายใจลำบาก", `<path d="M-50,-30q-30,70 10,80q30,-10 30,-60M50,-30q30,70 -10,80q-30,-10 -30,-60" fill="#f4a0a0" ${SO(3)}/><path d="M0,-70v60" stroke="${U.ink}" stroke-width="8"/>`, 0)
      + sign(0, "ปากบวม", `<circle r="70" fill="#e8b48a" ${SO(3)}/><path d="M-36,20q36,-20 72,0q-36,40 -72,0Z" fill="#e85a5a" ${SO(3)}/><circle cx="-24" cy="-20" r="7" fill="${U.ink}"/><circle cx="24" cy="-20" r="7" fill="${U.ink}"/>`, 1)
      + sign(300, "เป็นลม", `<path d="M-70,40h140" stroke="${U.ink}" stroke-width="8"/><circle cx="-50" cy="20" r="18" fill="#e8b48a" ${SO(3)}/><path d="M-30,24h80" stroke="#2a2a30" stroke-width="22" stroke-linecap="round"/><path d="M-60,-10q10,-20 24,-6" stroke="${U.ink}" stroke-width="4" fill="none"/>`, 2);
    c += `<g transform="translate(0,620)"><g id="${id}-ph"><rect x="-230" y="-70" width="460" height="140" rx="70" fill="${U.red}" ${SO(5)}/><text y="26" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="78" fill="#fff">โทร 1669</text></g></g></g></g>`;
    put(layer, c);
    inOut(tl, id, t0, dur);
    [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-s${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.45, ease: "back.out(2.4)", immediateRender: false }, t0 + 0.3 + k * 0.25));
    tl.fromTo(`#${id}-ph`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.08, svgOrigin: "0 0", duration: 0.3, yoyo: true, repeat: Math.ceil(dur / 0.6), ease: "sine.inOut", immediateRender: false }, t0 + 1.1);
  };

  // the end card: a plank sign on the shrine fence in afternoon light + a paper note naming the next episode
  HnUI.nextBoard = (tl, layer, t0, dur, o = {}) => {
    const id = `hn${seq++}`;
    put(layer, `<g id="${id}" opacity="0"><rect width="1080" height="1920" fill="url(#p2SkyDay)"/><circle cx="260" cy="320" r="520" fill="url(#p2Sun)"/>
      <path d="M0,1380Q540,1340 1080,1380V1920H0Z" fill="#7aa648"/><path d="M0,1440Q540,1400 1080,1440V1920H0Z" fill="#5e8a34"/>
      ${Array.from({ length: 9 }, (_, k) => `<rect x="${30 + k * 120}" y="1180" width="26" height="320" rx="8" fill="#b89a62" ${SO(3)}/>`).join("")}<path d="M0,1250H1080M0,1380H1080" stroke="#8a6e44" stroke-width="14"/>
      <g transform="translate(540,760)"><g id="${id}-sg"><g filter="url(#muDrop)"><path d="M-360,-230L360,-220L350,210L-350,200Z" fill="url(#hnPlank)" ${SO(6)}/></g>
        <text y="-90" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="104" fill="${U.redD}" stroke="#fff4dc" stroke-width="10" paint-order="stroke">ระวัง!</text>
        <g transform="translate(-150,40)">${Hn.nest(0, -70, 0.42, { id: `${id}-n` })}</g>
        <text x="80" y="70" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="74" fill="${U.ink}">รังต่อ</text>
        <text x="80" y="150" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="40" fill="${U.teakD}">หลังศาลตายาย</text></g></g>
      <g transform="translate(560,1060) rotate(3)"><g id="${id}-nt"><rect x="-270" y="0" width="540" height="300" fill="#f4eedc" ${SO(3.5)}/><rect x="-60" y="-18" width="120" height="40" fill="#e8dca8" opacity=".85" transform="rotate(-4)"/>
        <text y="86" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="46" fill="${U.redD}">${o.l1 || "ตอนที่ 2"}</text>
        <text y="174" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${o.l2 && o.l2.length > 12 ? 58 : 70}" fill="${U.redD}">${o.l2 || ""}</text>
        <text y="252" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="32" fill="#5a4a3a">${o.l3 || "กดติดตาม แล้ววิ่งไปด้วยกัน"}</text></g></g>
      <g id="${id}-sw"></g>
      <text x="540" y="1720" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#fff" letter-spacing="10" stroke="#2a2018" stroke-width="6" paint-order="stroke">ROD MAI CLUB</text></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.35, immediateRender: false }, t0);
    tl.fromTo(`#${id}-sg`, { y: -300, rotation: -6, svgOrigin: "0 0" }, { y: 0, rotation: 0, svgOrigin: "0 0", duration: 0.7, ease: "bounce.out", immediateRender: false }, t0 + 0.1);
    tl.fromTo(`#${id}-nt`, { scaleY: 0, svgOrigin: "0 0" }, { scaleY: 1, svgOrigin: "0 0", duration: 0.5, ease: "back.out(2)", immediateRender: false }, t0 + 0.6);
    tl.to(`#${id}-nt`, { rotation: 5, svgOrigin: "0 0", duration: 0.9, yoyo: true, repeat: Math.ceil(dur / 0.9), ease: "sine.inOut" }, t0 + 1.1);
    Hn.swarm(tl, document.getElementById(`${id}-sw`), { id: `${id}-s`, n: 6, s: 0.5, cx: 380, cy: 600, rx: 260, ry: 160, t0, dur, seed: 5 });
  };

  // the series end: every rule ticked + the share line
  HnUI.finale = (tl, layer, t0, dur, o = {}) => {
    put(layer, `<rect id="hfin-bg" width="1080" height="1920" fill="#f4e6c8" opacity="0"/>`);
    tl.set("#hfin-bg", { opacity: 0 }, 0); tl.to("#hfin-bg", { opacity: 1, duration: 0.3 }, t0);
    HnUI.rules(tl, layer, t0, dur, { done: [0, 1, 2], y: 380 });
    const id = `hf${seq++}`;
    put(layer, `<g id="${id}"><text x="540" y="1420" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="60" fill="${U.redD}">ตอนจบ</text>
      <text x="540" y="1510" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="46" fill="${U.ink}">แชร์ให้คนที่คุณรัก… ก่อนวันที่ต้องใช้</text>
      <text x="540" y="1700" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="${U.teakD}" letter-spacing="10">ROD MAI CLUB</text></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0); tl.to(`#${id}`, { opacity: 1, duration: 0.4 }, t0 + 1);
  };
})();
