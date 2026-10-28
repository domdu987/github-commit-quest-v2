// "เห็ดปอบ" v2 — on-screen graphics in the story's own hand: Yai Kham's rules on a taped notebook page with drawn icons,
// the source chip, and the drawn icons themselves. Everything is SVG in screen space (put it in L.light).
//   PopUI.rule(tl, layer, t0, dur, o)   o.active 0..2 (the line this episode teaches), o.y (card centre), o.done [i…] (lines ticked)
//   PopUI.source(tl, layer, t0, dur, o) o.text, o.y
//   PopUI.ICON.{mushQ, hospital, belly, skull, check, cross, clock, spoon, rice, shallot, fire}(x, y, s)  drawn icons, 100-unit box
(function () {
  const f1 = (v) => (+v).toFixed(1);
  const INK = "#3a2a22", PAPER = "#f6eedb";
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  let seq = 0;

  Sets.DEFS += `
    <linearGradient id="uiPaper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf4e2"/><stop offset="1" stop-color="#efe2c4"/></linearGradient>
    <linearGradient id="uiTape" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#efe2b8" stop-opacity=".82"/><stop offset="1" stop-color="#e2d2a2" stop-opacity=".82"/></linearGradient>
    <filter id="uiShadow" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="14"/><feOffset dx="0" dy="18"/><feComponentTransfer><feFuncA type="linear" slope=".55"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="uiRough" x="-5%" y="-20%" width="110%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".04" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="6"/></filter>`;

  // ---------------- drawn icons (ink outline, flat fills, a highlight) in a 100-unit box centred on (x, y) ----------------
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const at = (x, y, s, g) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">${g}</g>`;
  const ICON = {
    mush: (x, y, s = 1) => at(x, y, s, `<path d="M-8,40Q-12,10 -6,-6H6Q12,10 8,40Z" fill="#fffaf0" ${O()}/><path d="M-12,4q12,10 24,0" fill="#fffaf0" ${O(3)}/><path d="M-40,-4Q-38,-40 0,-44Q38,-40 40,-4Q0,6 -40,-4Z" fill="#fffaf0" ${O()}/><path d="M-26,-28q12,-10 26,-8" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M-16,40h32" ${O()}/>`),
    mushQ: (x, y, s = 1) => at(x, y, s, ICON.mush(-10, 8, 0.9) + `<circle cx="30" cy="-30" r="20" fill="#ffd84a" ${O(3.5)}/><text x="30" y="-21" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="28" fill="${INK}">?</text>`),
    basketX: (x, y, s = 1) => at(x, y, s, `<path d="M-30,-20Q-36,30 0,40Q36,30 30,-20Z" fill="#d8a85a" ${O()}/><path d="M-32,-4Q0,6 32,-4M-30,14Q0,24 30,14" stroke="#9a6a30" stroke-width="3" fill="none"/><path d="M-34,-20Q0,-30 34,-20" ${O()} fill="none"/>
      <path d="M-40,-40L40,40M40,-40L-40,40" stroke="#e8433a" stroke-width="9" stroke-linecap="round"/>`),
    hospital: (x, y, s = 1) => at(x, y, s, `<path d="M-40,40V-20L0,-44L40,-20V40Z" fill="#f4f6f8" ${O()}/><rect x="-14" y="-22" width="28" height="28" rx="4" fill="#e8433a"/><path d="M0,-18V2M-10,-8H10" stroke="#fff" stroke-width="6" stroke-linecap="round"/><path d="M-12,40V18H12V40" fill="#9ab4d0" ${O(3)}/>`),
    belly: (x, y, s = 1) => at(x, y, s, `<path d="M-24,-34Q-4,-44 6,-28Q30,-30 36,-6Q42,26 14,38Q-14,46 -30,26Q-40,8 -26,-6Q-36,-24 -24,-34Z" fill="#f4a0a0" ${O()}/><path d="M-10,-12q10,10 22,4M-6,14q12,6 22,-4" stroke="#c86a6a" stroke-width="3.5" fill="none" stroke-linecap="round"/>
      <path d="M26,-40l18,32h-36z" fill="#ffd84a" ${O(3)}/><path d="M26,-30v10M26,-14v1" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>`),
    skull: (x, y, s = 1) => at(x, y, s, `<path d="M-32,4Q-36,-40 0,-42Q36,-40 32,4Q30,18 18,20V34H-18V20Q-30,18 -32,4Z" fill="#f4f0e6" ${O()}/><circle cx="-13" cy="-6" r="9" fill="${INK}"/><circle cx="13" cy="-6" r="9" fill="${INK}"/><path d="M0,6l-5,9h10z" fill="${INK}"/><path d="M-8,26v8M0,26v8M8,26v8" stroke="${INK}" stroke-width="3"/>`),
    check: (x, y, s = 1) => at(x, y, s, `<circle r="40" fill="#5ab86a" ${O()}/><path d="M-18,0l12,13l24,-26" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`),
    cross: (x, y, s = 1) => at(x, y, s, `<circle r="40" fill="#e8433a" ${O()}/><path d="M-15,-15L15,15M15,-15L-15,15" stroke="#fff" stroke-width="10" stroke-linecap="round"/>`),
    clock: (x, y, s = 1) => at(x, y, s, `<circle r="40" fill="#fffaf0" ${O()}/><path d="M0,-24V0L16,10" stroke="${INK}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>${[0, 90, 180, 270].map((a) => `<path d="M0,-34v6" stroke="${INK}" stroke-width="4" transform="rotate(${a})"/>`).join("")}`),
    spoon: (x, y, s = 1) => at(x, y, s, `<ellipse cx="0" cy="-22" rx="16" ry="22" fill="#dfe4ea" ${O()}/><path d="M0,0V44" stroke="${INK}" stroke-width="12" stroke-linecap="round"/><path d="M0,0V44" stroke="#dfe4ea" stroke-width="5" stroke-linecap="round"/><path d="M-6,-32q2,-8 8,-8" stroke="#fff" stroke-width="4" fill="none"/>`),
    rice: (x, y, s = 1) => at(x, y, s, [[-14, 8, 30], [6, -8, -20], [18, 14, 60], [-4, -26, 10], [-24, -14, -40], [10, 30, 0]].map(([gx, gy, a]) => `<ellipse cx="${gx}" cy="${gy}" rx="8" ry="15" transform="rotate(${a} ${gx} ${gy})" fill="#fffaf0" ${O(3)}/>`).join("")),
    shallot: (x, y, s = 1) => at(x, y, s, `<path d="M0,-44Q6,-20 24,-4Q36,20 18,38Q0,46 -18,38Q-36,20 -24,-4Q-6,-20 0,-44Z" fill="#c8607a" ${O()}/><path d="M0,-30Q-10,6 -6,40M0,-30Q12,6 8,40" stroke="#9a3a56" stroke-width="3" fill="none"/>`),
    fire: (x, y, s = 1) => at(x, y, s, `<path d="M0,44Q-34,40 -34,10Q-34,-14 -12,-30Q-14,-10 0,-6Q-4,-30 12,-46Q18,-22 30,-8Q38,6 34,20Q30,42 0,44Z" fill="#ff8a3a" ${O()}/><path d="M0,40Q-14,36 -14,20Q-14,8 0,-2Q2,10 10,14Q16,24 10,32Q6,40 0,40Z" fill="#ffd84a"/>`),
    palette: (x, y, s = 1) => at(x, y, s, `<path d="M-6,-40Q-44,-38 -42,0Q-40,36 -4,40Q14,40 10,26Q6,14 20,14Q42,14 42,-6Q40,-40 -6,-40Z" fill="#f2dfb4" ${O()}/><circle cx="-20" cy="-14" r="8" fill="#e8433a"/><circle cx="2" cy="-24" r="8" fill="#ffd84a"/><circle cx="24" cy="-12" r="8" fill="#4a9ae8"/><circle cx="-18" cy="16" r="8" fill="#5ab86a"/>`),
    nose: (x, y, s = 1) => at(x, y, s, `<path d="M-30,-40Q-10,-10 -6,18Q-4,32 -20,32Q-34,30 -30,20" fill="none" ${O(6)}/><path d="M6,-20q16,6 8,20q-8,14 6,22M22,-30q16,8 8,22q-8,14 6,24" stroke="#5ab86a" stroke-width="5" fill="none" stroke-linecap="round"/>`),
    shape: (x, y, s = 1) => at(x, y, s, `<path d="M-30,6Q-28,-34 0,-36Q28,-34 30,6Z" fill="none" stroke="${INK}" stroke-width="5" stroke-dasharray="8 6"/><path d="M-6,6V38H6V6" fill="none" stroke="${INK}" stroke-width="5" stroke-dasharray="6 5"/><path d="M-40,42H40" ${O(4)}/>${[-32, -16, 0, 16, 32].map((tx) => `<path d="M${tx},42v-8" stroke="${INK}" stroke-width="3"/>`).join("")}`),
    pot: (x, y, s = 1) => at(x, y, s, `<path d="M-40,-10Q-42,30 -30,38H30Q42,30 40,-10Z" fill="#b8bcc0" ${O()}/><path d="M-46,-12H46" ${O()}/><path d="M-50,-4h8M42,-4h8" ${O(6)}/><path d="M-20,-30q6,-10 0,-18M0,-30q6,-10 0,-18M20,-30q6,-10 0,-18" stroke="#9aa0a6" stroke-width="4" fill="none" stroke-linecap="round"/>`),
  };

  // ---------------- Yai Kham's rules: a notebook page taped up, her three rhyming lines with drawn icons ----------------
  const RULES = ["เห็ดไม่รู้จัก อย่าหักใส่ข้อง", "กินแล้วเมา เอาเห็ดไปหาหมอ", "ท้องหายปวด อย่าอวดว่าหาย"];
  const RICON = [(x, y) => ICON.mushQ(x, y, 1.05), (x, y) => ICON.hospital(x, y, 1.05), (x, y) => ICON.belly(x, y, 1.05)];
  const BADGE = ["#e4f2d4", "#dcecf8", "#fbe0e0"];
  function rule(tl, layer, t0, dur, o = {}) {
    const id = `ui${++seq}`, A = o.active ?? 0, W = 900, H = 700, cx = 540, cy = o.y ?? 900;
    let g = `<g id="${id}" opacity="0"><g transform="translate(${cx},${cy}) rotate(-1.6)"><g id="${id}-card"><g filter="url(#uiShadow)">`;
    // the page: ruled lines, a red margin, a torn top edge, tape on the corners
    const torn = Array.from({ length: 31 }, (_, k) => `${f1(-W / 2 + k * (W / 30))},${f1(-H / 2 + (k % 2 ? 7 : -3) + Math.sin(k * 2.1) * 4)}`).join(" L");
    g += `<path d="M${torn} L${W / 2},${H / 2} L${-W / 2},${H / 2} Z" fill="url(#uiPaper)"/>`;
    for (let k = 0; k < 11; k++) g += `<path d="M${-W / 2 + 10},${-H / 2 + 120 + k * 52}H${W / 2 - 10}" stroke="#9ab8d8" stroke-width="2" opacity=".45"/>`;
    g += `<path d="M${-W / 2 + 90},${-H / 2 + 10}V${H / 2}" stroke="#e88a8a" stroke-width="3" opacity=".6"/></g>`;
    g += `<rect x="${-W / 2 - 40}" y="${-H / 2 - 26}" width="170" height="54" fill="url(#uiTape)" transform="rotate(-24 ${-W / 2 + 40} ${-H / 2})"/><rect x="${W / 2 - 130}" y="${-H / 2 - 26}" width="170" height="54" fill="url(#uiTape)" transform="rotate(22 ${W / 2 - 40} ${-H / 2})"/>`;
    // title in her hand, underlined
    g += `<text x="0" y="${-H / 2 + 96}" text-anchor="middle" font-family="Mali" font-weight="700" font-size="62" fill="#7a3a22">กฎของยายคำ</text>
      <path id="${id}-ul" d="M-190,${-H / 2 + 118}Q0,${-H / 2 + 104} 200,${-H / 2 + 120}" stroke="#7a3a22" stroke-width="5" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>`;
    RULES.forEach((txt, i) => {
      const ry = -H / 2 + 230 + i * 160, on = i === A, done = (o.done || []).includes(i);
      g += `<g id="${id}-r${i}" opacity="0">`;
      if (on) g += `<g filter="url(#uiRough)"><path id="${id}-hl" d="M-200,${ry - 34}L${W / 2 - 34},${ry - 40}L${W / 2 - 38},${ry + 22}L-202,${ry + 26}Z" fill="#ffe066" opacity=".75"/></g>`;
      g += `<g transform="translate(${-W / 2 + 170},${ry - 8})"><g id="${id}-i${i}"><circle r="66" fill="${BADGE[i]}" stroke="${INK}" stroke-width="4"/>${RICON[i](0, 0)}</g></g>`;
      g += `<text x="-188" y="${ry + 14}" font-family="Mali" font-weight="${on ? 700 : 600}" font-size="${on ? 47 : 43}" fill="${INK}">${txt}</text>`;
      if (done) g += `<path d="M${W / 2 - 70},${ry - 20}l14,16l26,-30" stroke="#3a9a4a" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
      g += `</g>`;
    });
    g += `<text x="${W / 2 - 60}" y="${H / 2 - 30}" text-anchor="end" font-family="Mali" font-weight="600" font-size="30" fill="#8a6a50">— ยายคำ</text></g></g></g>`;
    put(layer, g);
    const card = `#${id}-card`;
    tl.set(`#${id}`, { opacity: 1 }, t0);
    tl.fromTo(card, { y: 140, rotation: -7, opacity: 0, transformOrigin: "50% 50%" }, { y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(1.6)", immediateRender: false }, t0);
    tl.to(`#${id}-ul`, { strokeDashoffset: 0, duration: 0.45, ease: "power2.out" }, t0 + 0.35);
    RULES.forEach((_, i) => tl.to(`#${id}-r${i}`, { opacity: i === A ? 1 : 0.38, duration: 0.3 }, t0 + 0.45 + i * 0.14));
    tl.fromTo(`#${id}-hl`, { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.5, ease: "power2.inOut" }, t0 + 1.0);
    tl.fromTo(`#${id}-i${A}`, { scale: 1 }, { scale: 1.16, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 50%", immediateRender: false }, t0 + 1.05);
    tl.to(`#${id}-i${A}`, { rotation: 8, duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut", transformOrigin: "50% 50%" }, t0 + 1.45);
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
    return id;
  }

  // ---------------- the source chip: a small pill bottom-centre with a document glyph ----------------
  function source(tl, layer, t0, dur, o = {}) {
    const id = `ui${++seq}`, y = o.y ?? 1660, txt = o.text || "", w = Math.min(980, 120 + txt.length * 17.5);
    put(layer, `<g transform="translate(540,0)"><g id="${id}" opacity="0"><rect x="${-w / 2}" y="-34" width="${w}" height="68" rx="34" fill="#0c1014" opacity=".78"/><rect x="${-w / 2}" y="-34" width="${w}" height="68" rx="34" fill="none" stroke="#f4ecd8" stroke-opacity=".28" stroke-width="2"/>
      <g transform="translate(${-w / 2 + 44},0)"><path d="M-14,-20H6L16,-10V20H-14Z" fill="#f4ecd8"/><path d="M6,-20V-10H16" fill="#c8bca0"/><path d="M-8,-4h16M-8,4h16M-8,12h10" stroke="#5a5040" stroke-width="2.6"/></g>
      <text x="${-w / 2 + 76}" y="10" font-family="Kanit" font-weight="400" font-size="28" fill="#f4ecd8">${txt}</text></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, y: y + 16 }, { opacity: 1, y, duration: 0.35, ease: "power2.out", immediateRender: false }, t0);
    tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
    return id;
  }

  // ---------------- a phone held up in the hand, filling the lower frame ----------------
  //   o.mode "nosignal" (no bars, a video stuck loading) | "camera" (a viewfinder over the scene, focus box, shutter; o.flashAt)
  function phone(tl, layer, t0, dur, o = {}) {
    const id = `ui${++seq}`, X = o.x ?? 540, Y = o.y ?? 1080, W = 560, H = 1060, sk = o.skin || "#efc6a0", skS = Rig2.shade(sk, 0.22);
    let scr = "";
    if (o.mode === "camera") {
      scr = `<rect x="${-W / 2 + 22}" y="${-H / 2 + 60}" width="${W - 44}" height="${H - 160}" rx="20" fill="#000" opacity=".08"/>
        ${[1, 2].map((k) => `<path d="M${-W / 2 + 22 + k * (W - 44) / 3},${-H / 2 + 60}v${H - 160}M${-W / 2 + 22},${-H / 2 + 60 + k * (H - 160) / 3}h${W - 44}" stroke="#fff" stroke-width="2" opacity=".5"/>`).join("")}
        <g id="${id}-focus"><path d="M-80,-60v-30h30M50,-90h30v30M80,40v30h-30M-50,70h-30v-30" stroke="#ffd84a" stroke-width="5" fill="none"/></g>
        <rect x="${-W / 2}" y="${H / 2 - 110}" width="${W}" height="110" rx="0" fill="#0c0c10" opacity=".85"/><circle cy="${H / 2 - 56}" r="38" fill="#fff" stroke="#9a9aa0" stroke-width="6"/>
        <text x="0" y="${-H / 2 + 46}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#ffd84a" letter-spacing="3">PHOTO</text>`;
    } else {
      scr = `<rect x="${-W / 2 + 22}" y="${-H / 2 + 22}" width="${W - 44}" height="${H - 44}" rx="30" fill="#14161c"/>
        <g transform="translate(${-W / 2 + 60},${-H / 2 + 52})">${[0, 1, 2, 3].map((k) => `<rect x="${k * 12}" y="${-k * 6}" width="8" height="${10 + k * 6}" fill="#4a4e58"/>`).join("")}<path d="M-4,-24L48,8M48,-24L-4,8" stroke="#e8433a" stroke-width="5"/></g>
        <text x="${W / 2 - 60}" y="${-H / 2 + 62}" text-anchor="end" font-family="Kanit" font-weight="700" font-size="24" fill="#c8ccd4">ไม่มีบริการ</text>
        <rect x="${-W / 2 + 50}" y="${-H / 2 + 130}" width="${W - 100}" height="340" rx="18" fill="#22262e"/>
        <g id="${id}-spin" transform="translate(0,${-H / 2 + 300})"><g id="${id}-spinr">${Array.from({ length: 8 }, (_, k) => `<rect x="-5" y="-46" width="10" height="24" rx="5" fill="#fff" opacity="${(0.2 + k * 0.1).toFixed(2)}" transform="rotate(${k * 45})"/>`).join("")}</g></g>
        <g transform="translate(0,${H / 2 - 360})"><circle r="70" fill="#2a2e38"/><path d="M-36,-10Q0,-46 36,-10M-22,8Q0,-14 22,8" stroke="#8a8e98" stroke-width="8" fill="none" stroke-linecap="round"/><circle cy="26" r="8" fill="#8a8e98"/><path d="M-60,-60L60,60" stroke="#e8433a" stroke-width="9" stroke-linecap="round"/></g>
        <text x="0" y="${H / 2 - 230}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="#f4ecd8">ไม่มีการเชื่อมต่อ</text><text x="0" y="${H / 2 - 186}" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="26" fill="#9a9ea8">ลองใหม่อีกครั้ง</text>`;
    }
    const fin = (x0, y0, x1, y1, w, nail) => `<path d="M${x0},${y0}L${x1},${y1}" stroke="${LN2}" stroke-width="${w + 8}" stroke-linecap="round"/><path d="M${x0},${y0}L${x1},${y1}" stroke="${sk}" stroke-width="${w}" stroke-linecap="round"/>` +
      (nail ? `<ellipse cx="${x1 + (x1 < x0 ? 10 : -10)}" cy="${y1}" rx="12" ry="${w * 0.32}" fill="#f6dcc8"/>` : "");
    const palm = `<path d="M${-W / 2 - 50},${H / 2 - 190}C${-W / 2 - 100},${H / 2 + 40} ${-W / 2 - 40},${H / 2 + 300} ${-W / 2 + 30},${H / 2 + 520}H${W / 2 + 40}C${W / 2 + 100},${H / 2 + 300} ${W / 2 + 90},${H / 2 + 20} ${W / 2 + 46},${H / 2 - 230}Z" fill="${sk}" stroke="${LN2}" stroke-width="4"/>
      <path d="M${-W / 2 - 50},${H / 2 - 190}C${-W / 2 - 100},${H / 2 + 40} ${-W / 2 - 40},${H / 2 + 300} ${-W / 2 + 30},${H / 2 + 520}H${W / 2 + 40}C${W / 2 + 100},${H / 2 + 300} ${W / 2 + 90},${H / 2 + 20} ${W / 2 + 46},${H / 2 - 230}Z" fill="url(#r2Cyl)"/>
      <path d="M${-W / 2 - 40},${H / 2 - 120}C${-W / 2 + 60},${H / 2 - 40} ${-W / 2 + 80},${H / 2 + 160} ${-W / 2 + 10},${H / 2 + 330}" stroke="${skS}" stroke-width="7" fill="none" opacity=".55" stroke-linecap="round"/>
      <path d="M${-W / 2 - 40},${H / 2 - 150}C${-W / 2 + 20},${H / 2 - 60} ${-W / 2 + 30},${H / 2 + 80} ${-W / 2 - 20},${H / 2 + 200}" stroke="#fff" stroke-width="10" fill="none" opacity=".18" stroke-linecap="round"/>
      <path d="M${-W / 2 + 120},${H / 2 + 10}Q0,${H / 2 + 60} ${W / 2 - 40},${H / 2 - 10}" stroke="${skS}" stroke-width="5" fill="none" opacity=".45"/>
      <rect x="${-W / 2 - 20}" y="${H / 2 - 24}" width="${W + 40}" height="60" fill="#1c1030" opacity=".18"/>`;
    const grip = fin(W / 2 + 70, H / 2 - 430, W / 2 - 24, H / 2 - 410, 50, true) + fin(W / 2 + 76, H / 2 - 340, W / 2 - 30, H / 2 - 322, 54, true) + fin(W / 2 + 70, H / 2 - 252, W / 2 - 26, H / 2 - 236, 52, true) +
      fin(-W / 2 - 80, H / 2 - 210, -W / 2 + 44, H / 2 - 290, 62, true);
    put(layer, `<g id="${id}" opacity="0"><g transform="translate(${X},${Y}) rotate(${o.rot ?? -4})"><g id="${id}-ph">${palm}
      <rect x="${-W / 2 - 14}" y="${-H / 2 - 14}" width="${W + 28}" height="${H + 28}" rx="70" fill="${o.mode === "camera" ? "none" : "#1a1c22"}" stroke="#1a1c22" stroke-width="${o.mode === "camera" ? 30 : 4}"/>
      ${o.mode === "camera" ? `<rect x="${-W / 2}" y="${-H / 2}" width="${W}" height="${H}" rx="58" fill="none" stroke="#000" stroke-width="24"/>` : `<rect x="${-W / 2}" y="${-H / 2}" width="${W}" height="${H}" rx="58" fill="#0e1014"/>`}${scr}
      <rect x="-60" y="${-H / 2 + 6}" width="120" height="30" rx="15" fill="#000"/>${grip}
    </g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, t0);
    tl.fromTo(`#${id}-ph`, { y: 500 }, { y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }, t0);
    if (o.mode !== "camera") tl.fromTo(`#${id}-spinr`, { rotation: 0, svgOrigin: "0 0" }, { rotation: 360 * Math.ceil(dur), duration: dur, ease: "none", immediateRender: false }, t0);
    else { tl.fromTo(`#${id}-focus`, { scale: 1.5, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, t0 + 0.3); }
    if (o.shake) tl.to(`#${id}-ph`, { x: 10, duration: 0.06, repeat: Math.floor(dur / 0.06) - 2, yoyo: true, ease: "none" }, t0 + 0.4);
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + dur - 0.2);
    return id;
  }
  const LN2 = "#3a2622";

  // ---------------- a paper label on a bamboo pick, stuck into the ground (world space) ----------------
  function tag(x, y, text, o = {}) {
    const w = o.w || 360, ic = o.icon ? ICON[o.icon](-w / 2 + 52, -2, 0.62) : "", rot = o.rot ?? -3;
    return `<g ${o.id ? `id="${o.id}"` : ""}><g transform="translate(${f1(x)},${f1(y)})"><path d="M0,0V${o.stick ?? 220}" stroke="#b89a5a" stroke-width="8" stroke-linecap="round"/><path d="M0,0V${o.stick ?? 220}" stroke="#7a5a2a" stroke-width="2" opacity=".6"/>
      <g transform="rotate(${rot})"><rect x="${-w / 2 + 6}" y="-50" width="${w}" height="104" rx="10" fill="#000" opacity=".3"/><rect x="${-w / 2}" y="-56" width="${w}" height="104" rx="10" fill="url(#uiPaper)" stroke="${INK}" stroke-width="3"/><circle cx="0" cy="-42" r="7" fill="#b89a5a" stroke="${INK}" stroke-width="2"/>
      ${ic}<text x="${o.icon ? 30 : 0}" y="14" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${o.size || 40}" fill="${o.color || INK}">${text}</text></g></g></g>`;
  }

  // ---------------- a drawn sound word ----------------
  function sfx(tl, layer, t0, dur, text, x, y, o = {}) {
    const id = `ui${++seq}`;
    put(layer, `<g transform="translate(${x},${y}) rotate(${o.rot ?? -6})"><g id="${id}" opacity="0"><text x="0" y="0" text-anchor="middle" font-family="Sriracha" font-size="${o.size || 92}" fill="${o.color || "#f4ecd8"}" stroke="#14100c" stroke-width="14" paint-order="stroke" stroke-linejoin="round">${text}</text></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, scale: 0.6, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.18, ease: "back.out(3)", immediateRender: false }, t0);
    tl.to(`#${id}`, { y: -20, duration: dur, ease: "none" }, t0);
    tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
    return id;
  }

  // ---------------- the delay of the poison: eaten → 4–6 hours → the belly ----------------
  function timeline(tl, layer, t0, dur, o = {}) {
    const id = `ui${++seq}`, y = o.y ?? 560;
    put(layer, `<g id="${id}" opacity="0"><g transform="translate(540,${y})"><rect x="-470" y="-150" width="940" height="300" rx="34" fill="#0c1014" opacity=".82"/><rect x="-470" y="-150" width="940" height="300" rx="34" fill="none" stroke="#f4ecd8" stroke-opacity=".25" stroke-width="2"/>
      <g transform="translate(-350,-20)"><circle r="70" fill="#fdf2d8" stroke="${INK}" stroke-width="4"/>${ICON.mush(0, 4, 0.9)}</g><text x="-350" y="110" text-anchor="middle" font-family="Mali" font-weight="700" font-size="34" fill="#f4ecd8">กินตอนค่ำ</text>
      <path d="M-260,-20H250" stroke="#4a4e56" stroke-width="16" stroke-linecap="round"/><path id="${id}-bar" d="M-260,-20H250" stroke="#ffd84a" stroke-width="16" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
      <g transform="translate(0,-20)"><g id="${id}-clk">${ICON.clock(0, 0, 0.9)}</g></g><text x="0" y="80" text-anchor="middle" font-family="Mali" font-weight="700" font-size="44" fill="#ffd84a">4 – 6 ชั่วโมง</text>
      <g transform="translate(350,-20)"><g id="${id}-belly"><circle r="70" fill="#fbe0e0" stroke="${INK}" stroke-width="4"/>${ICON.belly(0, 4, 0.9)}</g></g><text x="350" y="110" text-anchor="middle" font-family="Mali" font-weight="700" font-size="34" fill="#f4ecd8">อาการมาทีหลัง</text></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.3, immediateRender: false }, t0);
    tl.to(`#${id}-bar`, { strokeDashoffset: 0, duration: Math.min(1.8, dur * 0.5), ease: "power1.inOut" }, t0 + 0.4);
    tl.fromTo(`#${id}-clk`, { rotation: 0, svgOrigin: "0 0" }, { rotation: 360, duration: Math.min(1.8, dur * 0.5), ease: "power1.inOut", immediateRender: false }, t0 + 0.4);
    tl.fromTo(`#${id}-belly`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.18, duration: 0.18, yoyo: true, repeat: 3, immediateRender: false }, t0 + 0.4 + Math.min(1.8, dur * 0.5));
    tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
    return id;
  }

  // ---------------- the end-of-episode choice: two drawn cards, a draining ring; o.possessed takes over one side ----------------
  function choice(tl, layer, t0, dur, o = {}) {
    const id = `ui${++seq}`, y = o.y ?? 760, secs = o.secs || 3, RC = 2 * Math.PI * 56;
    const card = (side, label, icon, x) => `<g transform="translate(${x},0)"><g id="${id}-${side}"><rect x="-230" y="-170" width="460" height="340" rx="30" fill="#0c1014" opacity=".9"/><rect x="-230" y="-170" width="460" height="340" rx="30" fill="none" stroke="#f4ecd8" stroke-opacity=".35" stroke-width="3"/>
      <circle cy="-50" r="84" fill="${side === "A" ? "#dcecf8" : "#2a2a3a"}" stroke="${INK}" stroke-width="4"/>${icon}
      <text y="110" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#f4ecd8"><tspan id="${id}-${side}t">${label}</tspan></text>
      ${o.possessed && o.possessed.side.toUpperCase() === side ? `<text id="${id}-${side}g" y="110" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#ff5a5a" opacity="0">${o.possessed.glitch}</text>` : ""}</g></g>`;
    const moon = `<g transform="translate(0,-50)"><path d="M18,-50A54,54 0 1 0 50,30A44,44 0 1 1 18,-50Z" fill="#f2dfb4" stroke="${INK}" stroke-width="4"/><text x="34" y="-30" font-family="Kanit" font-weight="900" font-size="30" fill="#f2dfb4">z</text></g>`;
    put(layer, `<g id="${id}" opacity="0"><g transform="translate(540,${y})">
      <g transform="translate(0,-280)"><rect x="-230" y="-48" width="460" height="92" rx="46" fill="#0c1014" opacity=".86"/><text y="18" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#f4ecd8">${o.q || ""}</text></g>
      ${card("A", o.a, ICON.hospital(0, -50, 1.25), -250)}${card("B", o.b, moon, 250)}
      <g transform="translate(0,230)"><circle r="56" fill="#0c1014" stroke="#f4ecd8" stroke-opacity=".25" stroke-width="10"/><circle id="${id}-ring" r="56" fill="none" stroke="#f2c55c" stroke-width="10" stroke-linecap="round" stroke-dasharray="${RC.toFixed(1)}" stroke-dashoffset="0" transform="rotate(-90)"/>
        ${Array.from({ length: secs + 1 }, (_, n) => `<text id="${id}-n${n}" y="18" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#f4ecd8" opacity="0">${n}</text>`).join("")}</g>
      ${o.possessed ? `<text id="${id}-who" y="400" text-anchor="middle" font-family="Sriracha" font-size="54" fill="#ff6a6a" stroke="#14100c" stroke-width="10" paint-order="stroke" opacity="0">${o.possessed.who}</text>` : ""}</g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    tl.fromTo(`#${id}-A`, { x: -80, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "back.out(2)", immediateRender: false }, t0 + 0.1);
    tl.fromTo(`#${id}-B`, { x: 80, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "back.out(2)", immediateRender: false }, t0 + 0.1);
    tl.fromTo(`#${id}-ring`, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": RC }, duration: dur - 0.3, ease: "none", immediateRender: false }, t0);
    for (let n = secs; n >= 0; n--) { const at = t0 + ((secs - n) * (dur - 0.3)) / secs; tl.set(`#${id} [id^="${id}-n"]`, { opacity: 0 }, at); tl.set(`#${id}-n${n}`, { opacity: 1 }, at); }
    if (o.possessed) {
      const pa = t0 + o.possessed.at, S = o.possessed.side.toUpperCase(), OT = S === "A" ? "B" : "A";
      tl.to(`#${id}-${S}`, { x: 8, duration: 0.05, repeat: Math.floor((dur - o.possessed.at) / 0.05) - 1, yoyo: true, ease: "none" }, pa);
      tl.to(`#${id}-${S}`, { scale: 1.12, svgOrigin: "0 0", duration: 0.9, ease: "power2.in" }, pa);
      tl.to(`#${id}-${OT}`, { opacity: 0.3, duration: 0.5 }, pa + 0.2);
      [0.15, 0.4, 0.62, 0.8, 0.95].forEach((k, i) => { tl.set(`#${id}-${S}t`, { opacity: i % 2 ? 1 : 0 }, pa + k); tl.set(`#${id}-${S}g`, { opacity: i % 2 ? 0 : 1 }, pa + k); });
      tl.fromTo(`#${id}-who`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, pa + 0.5);
    }
    return id;
  }

  window.PopUI = { rule, source, phone, tag, sfx, timeline, choice, ICON, RULES };
})();
