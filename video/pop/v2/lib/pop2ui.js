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

  window.PopUI = { rule, source, ICON, RULES };
})();
