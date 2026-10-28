// "ผีแม่ม่าย" EP.2 motion graphics, in the design language of mmui.js (ink outline 4–5, flat fills, one shade and one highlight,
// soft drop shadows, Kanit; everything enters eased and staggered, then keeps a small secondary motion).
//   MmUI.phone(tl, layer, t0, dur, o)  the phone to camera: 1669 ringing → connected (the call timer runs), speaker on (waves);
//                      the checklist card beside it ticks its rows at o.rows (s after t0): ขอเครื่อง AED / ที่อยู่ / อาการ / เบอร์โทรกลับ
//   MmUI.eta(tl, layer, t0, dur, o)    the ambulance chip: icon, "รถกู้ชีพ อีก", mm:ss running from o.from to o.to (seconds) over the
//                      shot (a time-lapse), a bar that drains; o.big pops it at the centre first and flies it to the corner at o.fly
//   MmUI.cpr(tl, layer, t0, dur, o)    the compression meter over a live shot: the depth ruler (the plate dips to 5 cm on every
//                      push), the rate pill "100–120 ครั้ง/นาที" with a beating dot and the count · o.x, o.y, o.bpm (110)
//   Sets.chestTop(L, o)  Keng on the planks from straight above, head at the top. o.bare: the singlet cut away (skin, collarbones).
//                      Ids: #id-xr (x-ray ribs + breastbone), #id-low (its lower half), #id-lowl (label), #id-arms (Fon's forearms + hands,
//                      #id-h1 the lower hand, #id-h2 the upper, #id-lock the locked fingers), #id-pad0 #id-pad1, #id-cab0 #id-cab1,
//                      #id-pl0 #id-pl1 (pad labels); o.fon: Fon's head from above by his mouth (#id-fon) with #id-br (breath wisps),
//                      #id-brx, #id-ar (chest arrows), #id-arx (the crosses)
//   MmUI.handsAnim(tl, id, t0, o)  x-ray in → the lower half pulses + label → hand 1 slides in (o.h1) → hand 2 lands (o.h2) →
//                      fingers lock → pushes at 110/min to o.end
//   MmUI.padsAnim(tl, id, t0, o)   pad 0 (o.p0) under the right collarbone, pad 1 (o.p1) on the left ribs; cables draw; labels
//   MmUI.breathAnim(tl, id, t0, o) the check: wisps and chest arrows draw, then each is crossed out (o.x0, o.x1)
//   Sets.aedClose(L, o)  the AED on the planks, close: lid #id-lid, power #id-pwr, screen states #id-s0..3 (off, pads, analysing
//                      with #id-ecg / #id-sw and the hands-off sign #id-warn, shock), shock button #id-shock (+ #id-sglow), speaker
//                      waves #id-w0..2, the pads pack and the orange cable
//   MmUI.aedOn / aedTalk / aedState / aedShock (tl, id, t0, …)  its moments
//   Mm.aedKit(x, G, s, o)  the same AED small, on the floor of a wide shot (lid up, screen glowing #id-kscr), its cable to the chest
//   Mm.ghostArm(x, y, s, o)  a long coal-black arm reaching in from the right (the wrist at the origin, the hand towards -x):
//                      #id (an untransformed wrapper to move), #id-open / #id-shut (the fingers spread or closed round an ankle)
(function () {
  const f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const { mk } = Pop2;
  const INK = "#26201c";
  const C = { red: "#e2382e", redD: "#a81e18", green: "#2fa864", greenD: "#1e7a48", greenL: "#e4f6ea", yellow: "#ffd23a", orange: "#ff8a1a",
    orangeD: "#c85a0a", paper: "#fdfaf2", slate: "#1e2630", muted: "#8a8f98", blue: "#2f6fd0", skinK: "#b47448", skinKS: "#94582e", skinF: "#e6b48a",
    skinFS: "#c88e62", tee: "#e2a92e", teeS: "#b8821a", singlet: "#eef0f0" };
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const Mm = (window.Mm = window.Mm || {});
  let seq = 0;

  Sets.DEFS += `
    <linearGradient id="mu2Scr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c3644"/><stop offset="1" stop-color="#121820"/></linearGradient>
    <linearGradient id="mu2Card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf8"/><stop offset="1" stop-color="#f4eee0"/></linearGradient>
    <linearGradient id="mu2Plank" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a2e1e"/><stop offset=".5" stop-color="#5a3a26"/><stop offset="1" stop-color="#46301e"/></linearGradient>
    <radialGradient id="mu2Pool" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="#ffd8a0" stop-opacity=".42"/><stop offset=".55" stop-color="#ffb870" stop-opacity=".12"/><stop offset="1" stop-color="#ffb870" stop-opacity="0"/></radialGradient>
    <radialGradient id="mu2Vig" cx=".5" cy=".46" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".62"/></radialGradient>
    <linearGradient id="mu2SkinK" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a66a40"/><stop offset=".45" stop-color="#bc7c50"/><stop offset="1" stop-color="#8e5430"/></linearGradient>
    <linearGradient id="mu2Sing" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#dfe2e2"/><stop offset=".45" stop-color="#f4f6f6"/><stop offset="1" stop-color="#cfd3d4"/></linearGradient>
    <linearGradient id="mu2Aed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3cc078"/><stop offset="1" stop-color="#249a58"/></linearGradient>
    <radialGradient id="mu2XR"><stop offset="0" stop-color="#9ff0ff" stop-opacity=".85"/><stop offset="1" stop-color="#2ab8e8" stop-opacity="0"/></radialGradient>
    <radialGradient id="mu2Phone"><stop offset="0" stop-color="#cfeaff" stop-opacity=".55"/><stop offset=".45" stop-color="#9ccfff" stop-opacity=".16"/><stop offset="1" stop-color="#9ccfff" stop-opacity="0"/></radialGradient>
    <radialGradient id="mu2Glow"><stop offset="0" stop-color="#ffd23a" stop-opacity=".9"/><stop offset=".5" stop-color="#ff8a1a" stop-opacity=".35"/><stop offset="1" stop-color="#ff8a1a" stop-opacity="0"/></radialGradient>`;

  const pillT = (text, px = 34) => Math.round(text.length * px * 0.55 + 56);
  const label = (x, y, text, id, o = {}) => { const px = o.px || 34, w = pillT(text, px), fill = o.fill || "#fffaf0", col = o.col || INK;
    return `<g transform="translate(${x},${y})"><g id="${id}"><rect x="${-w / 2}" y="${-px * 0.95}" width="${w}" height="${px * 1.9}" rx="${px * 0.95}" fill="${fill}" ${O(4)}/><text y="${f1(px * 0.36)}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="${px}" fill="${col}">${text}</text></g></g>`; };
  const mmss = (s) => { s = Math.max(0, Math.round(s)); return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`; };

  // ---------------- small icons (centred, ~60 units) ----------------
  const IC = {
    aed: `<path d="M0,22C-22,4 -38,-14 -34,-30C-30,-46 -10,-48 0,-32C10,-48 30,-46 34,-30C38,-14 22,4 0,22Z" fill="${C.green}" ${O(3.5)}/><path d="M3,-36l-11,20h10l-7,16l17,-24h-10l7,-12z" fill="#fff"/>`,
    pin: `<path d="M0,30C-6,14 -26,0 -26,-14A26,26 0 1 1 26,-14C26,0 6,14 0,30Z" fill="${C.red}" ${O(3.5)}/><circle cy="-14" r="10" fill="#fff"/>`,
    man: `<circle cy="-20" r="14" fill="#f2c094" ${O(3.5)}/><path d="M-28,30Q-28,0 0,0Q28,0 28,30Z" fill="#5a86c8" ${O(3.5)}/><path d="M18,-34l6,-8M24,-24l9,-3M-18,-34l-6,-8" stroke="${C.red}" stroke-width="3.5" stroke-linecap="round"/>`,
    phone: `<rect x="-17" y="-30" width="34" height="60" rx="8" fill="#2a2e34" ${O(3.5)}/><rect x="-12" y="-22" width="24" height="40" rx="3" fill="#bfe6ff"/><path d="M-32,-8q-6,8 0,16M32,-8q6,8 0,16" stroke="${C.blue}" stroke-width="4" fill="none" stroke-linecap="round"/>`,
    amb: `<path d="M-40,14V-18H14L26,-6L40,-2V14Z" fill="#fbfbfb" ${O(3.5)}/><path d="M-40,2H40" stroke="${C.red}" stroke-width="6"/><path d="M-20,-14v12M-26,-8h12" stroke="${C.red}" stroke-width="5"/><rect x="-14" y="-26" width="16" height="8" rx="2" fill="${C.red}" ${O(2.5)}/><circle cx="-22" cy="16" r="8" fill="#1e1e22" ${O(2.5)}/><circle cx="24" cy="16" r="8" fill="#1e1e22" ${O(2.5)}/>`,
  };

  // ---------------- the phone and the checklist ----------------
  function phone(tl, layer, t0, dur, o = {}) {
    const id = `mph${seq++}`, X = o.x ?? 320, Y = o.y ?? 760, W = 430, H = 860, rows = o.rows || [0.8, 1.6, 2.4, 3.2], con = o.connect ?? 0.7;
    let p = `<g transform="translate(${X},${Y}) rotate(-5)"><g id="${id}-ph"><g filter="url(#muDrop)">
      <rect x="${-W / 2}" y="${-H / 2}" width="${W}" height="${H}" rx="64" fill="#1b1f26" ${O(5)}/><rect x="${-W / 2 + 14}" y="${-H / 2 + 14}" width="${W - 28}" height="${H - 28}" rx="52" fill="url(#mu2Scr)"/></g>
      <rect x="-56" y="${-H / 2 + 28}" width="112" height="24" rx="12" fill="#07090c"/>
      <text x="${-W / 2 + 50}" y="${-H / 2 + 50}" font-family="Kanit" font-weight="600" font-size="24" fill="#e8ecf2">03:14</text>
      ${[0, 1, 2, 3].map((k) => `<rect x="${W / 2 - 112 + k * 9}" y="${-H / 2 + 50 - 6 - k * 4}" width="6" height="${6 + k * 4}" rx="1.5" fill="#e8ecf2"/>`).join("")}
      <rect x="${W / 2 - 66}" y="${-H / 2 + 34}" width="30" height="16" rx="4" fill="none" stroke="#e8ecf2" stroke-width="2.5"/><rect x="${W / 2 - 63}" y="${-H / 2 + 37}" width="10" height="10" rx="2" fill="#e8705a"/>
      <g transform="translate(0,${-H / 2 + 230})">${[0, 1, 2].map((k) => `<circle id="${id}-rg${k}" r="92" fill="none" stroke="#ff8a7a" stroke-width="5" opacity="0"/>`).join("")}
        <circle r="92" fill="${C.red}" ${O(4)}/><circle r="92" fill="none" stroke="#fff" stroke-width="6" opacity=".35" transform="scale(.88)"/><path d="M0,-42V42M-42,0H42" stroke="#fff" stroke-width="26" stroke-linecap="round"/></g>
      <text y="${-H / 2 + 410}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="78" fill="#fff" letter-spacing="2">1669</text>
      <text y="${-H / 2 + 456}" text-anchor="middle" font-family="Kanit" font-weight="500" font-size="27" fill="#aab4c2">สายด่วนการแพทย์ฉุกเฉิน</text>
      <g id="${id}-st0"><text y="${-H / 2 + 512}" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="32" fill="#7fd8a0">กำลังโทร…</text></g>
      <g id="${id}-st1" opacity="0"><text id="${id}-tm" y="${-H / 2 + 512}" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="34" fill="#7fd8a0">00:00</text></g>
      <g transform="translate(0,${H / 2 - 250})">${[["#3a4452", -120], ["#3a4452", 0], ["#f4f6f8", 120]].map(([c, x], k) => `<circle cx="${x}" r="46" fill="${c}"/>`).join("")}
        <path d="M-136,-14v28M-104,-14v28M-128,-6l16,-12v36l-16,-12" stroke="#e8ecf2" stroke-width="5" fill="none" stroke-linecap="round" opacity="0"/>
        <g transform="translate(-120,0)"><rect x="-10" y="-20" width="20" height="30" rx="10" fill="none" stroke="#e8ecf2" stroke-width="5"/><path d="M-16,4q16,20 32,0M0,18v8" stroke="#e8ecf2" stroke-width="5" fill="none" stroke-linecap="round"/></g>
        ${[[-14, -14], [0, -14], [14, -14], [-14, 0], [0, 0], [14, 0], [-14, 14], [0, 14], [14, 14]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="4.5" fill="#e8ecf2"/>`).join("")}
        <g transform="translate(120,0)"><path d="M-22,-10h10l14,-12v44l-14,-12h-10z" fill="${C.blue}"/><g id="${id}-sw">${[0, 1, 2].map((k) => `<path id="${id}-w${k}" d="M${10 + k * 9},${-12 - k * 5}q${8 + k * 3},${12 + k * 5} 0,${24 + k * 10}" stroke="${C.blue}" stroke-width="4.5" fill="none" stroke-linecap="round"/>`).join("")}</g></g>
        <text x="120" y="78" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="22" fill="#e8ecf2">ลำโพง</text>
        <circle cy="140" r="52" fill="${C.red}"/><path d="M-24,148q24,-22 48,0" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/></g>
      <path d="M${-W / 2 + 40},${-H / 2 + 90}Q0,${-H / 2 + 70} ${W / 2 - 40},${-H / 2 + 90}" stroke="#fff" stroke-width="4" opacity=".08" fill="none"/></g></g>`;
    // the checklist: what to tell them
    const CW = 430, CH = 720, CX = o.cx ?? 790, CY = o.cy ?? 780;
    const ROWS = o.items || [["ขอเครื่อง AED", IC.aed], ["บอกที่อยู่", IC.pin], ["บอกอาการ", IC.man], ["เบอร์โทรกลับ", IC.phone]];
    let c = `<g transform="translate(${CX},${CY}) rotate(3)"><g id="${id}-card"><g filter="url(#muDrop)"><rect x="${-CW / 2}" y="${-CH / 2}" width="${CW}" height="${CH}" rx="38" fill="url(#mu2Card)" ${O(5)}/></g>
      <path d="M${-CW / 2},${-CH / 2 + 104}V${-CH / 2 + 38}Q${-CW / 2},${-CH / 2} ${-CW / 2 + 38},${-CH / 2}H${CW / 2 - 38}Q${CW / 2},${-CH / 2} ${CW / 2},${-CH / 2 + 38}V${-CH / 2 + 104}Z" fill="url(#muHead)" ${O(5)}/>
      <text y="${-CH / 2 + 68}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="40" fill="#fff">บอกให้ครบ</text>`;
    ROWS.forEach(([t, ic], k) => { const y = -CH / 2 + 190 + k * 146;
      c += `<g transform="translate(0,${y})"><g id="${id}-r${k}" opacity=".3"><circle cx="${-CW / 2 + 70}" r="48" fill="#f2efe6" ${O(3.5)}/><g transform="translate(${-CW / 2 + 70},0) scale(.9)">${ic}</g>
        <text x="${-CW / 2 + 134}" y="12" font-family="Kanit" font-weight="800" font-size="${t.length > 10 ? 33 : 36}" fill="${INK}">${t}</text>
        <rect x="${CW / 2 - 76}" y="-24" width="48" height="48" rx="12" fill="#fff" ${O(3.5)}/><rect id="${id}-cf${k}" x="${CW / 2 - 76}" y="-24" width="48" height="48" rx="12" fill="${C.green}" opacity="0"/>
        <path id="${id}-ck${k}" d="M${CW / 2 - 64},0l10,11l18,-21" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></g></g>`;
      if (k < ROWS.length - 1) c += `<path d="M${-CW / 2 + 30},${y + 73}H${CW / 2 - 30}" stroke="#e2dccc" stroke-width="2.5"/>`; });
    c += `</g></g>`;
    put(layer, `<g id="${id}">${p}${c}</g>`);
    // in: the phone rises, the card slides in
    tl.fromTo(`#${id}-ph`, { y: 260, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "back.out(1.6)", immediateRender: false }, t0);
    tl.set(`#${id}-card`, { opacity: 0 }, t0);
    tl.fromTo(`#${id}-card`, { x: 300, opacity: 0, rotation: 8, svgOrigin: "0 0" }, { x: 0, opacity: 1, rotation: 0, svgOrigin: "0 0", duration: 0.6, ease: "back.out(1.4)", immediateRender: false }, t0 + (o.cardAt ?? 0.35));
    // ringing, then connected: the timer runs
    for (let t = 0; t < con; t += 0.35) [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-rg${k}`, { opacity: 0.8, scale: 1, svgOrigin: "0 0" }, { opacity: 0, scale: 1.6, svgOrigin: "0 0", duration: 0.7, ease: "power1.out", immediateRender: false }, t0 + t + k * 0.12));
    tl.set(`#${id}-st0`, { opacity: 0 }, t0 + con); tl.set(`#${id}-st1`, { opacity: 1 }, t0 + con);
    const clk = { v: 0 }, tm = document.getElementById(`${id}-tm`);
    tl.fromTo(clk, { v: o.timer0 ?? 0 }, { v: (o.timer0 ?? 0) + dur - con, duration: dur - con, ease: "none", immediateRender: false, onUpdate: () => { tm.textContent = mmss(clk.v); } }, t0 + con);
    for (let t = t0 + con; t < t0 + dur - 0.2; t += 0.45) [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-w${k}`, { opacity: 0.25 }, { opacity: 1, duration: 0.15, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }, t + k * 0.08));
    // the rows tick on the words
    rows.forEach((tr, k) => {
      tl.to(`#${id}-r${k}`, { opacity: 1, duration: 0.2 }, t0 + tr);
      tl.fromTo(`#${id}-r${k}`, { scale: 1.1, svgOrigin: `${-CW / 2 + 70} 0` }, { scale: 1, svgOrigin: `${-CW / 2 + 70} 0`, duration: 0.4, ease: "back.out(3)", immediateRender: false }, t0 + tr);
      tl.to(`#${id}-cf${k}`, { opacity: 1, duration: 0.15 }, t0 + tr + 0.1);
      tl.fromTo(`#${id}-ck${k}`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.3, ease: "power2.out", immediateRender: false }, t0 + tr + 0.12);
    });
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
    return id;
  }

  // ---------------- the ambulance countdown chip ----------------
  function eta(tl, layer, t0, dur, o = {}) {
    const id = `met${seq++}`, X = o.x ?? 790, Y = o.y ?? 200, from = o.from ?? 720, to = o.to ?? from - 20, total = o.total ?? 720;
    const W = 470, H = 124;
    put(layer, `<g transform="translate(${X},${Y})"><g id="${id}"><g id="${id}-in"><g filter="url(#muDrop)"><rect x="${-W / 2}" y="${-H / 2}" width="${W}" height="${H}" rx="${H / 2}" fill="#14181e" opacity=".9" ${O(4)}/></g>
      <circle cx="${-W / 2 + 64}" r="46" fill="#fffaf2" ${O(3.5)}/><g transform="translate(${-W / 2 + 64},2) scale(.9)"><g id="${id}-amb">${IC.amb}</g></g>
      <g id="${id}-lite"><circle cx="${-W / 2 + 57}" cy="-22" r="10" fill="${C.red}" opacity=".0"/></g>
      <text x="${-W / 2 + 128}" y="-12" font-family="Kanit" font-weight="700" font-size="28" fill="#f2c55c" letter-spacing="1">รถกู้ชีพ อีก</text>
      <text id="${id}-t" x="${-W / 2 + 128}" y="40" font-family="Kanit" font-weight="900" font-size="56" fill="#fff" letter-spacing="2">${mmss(from)}</text>
      <text x="${W / 2 - 36}" y="40" text-anchor="end" font-family="Kanit" font-weight="600" font-size="26" fill="#aab4c2">นาที</text>
      <rect x="${-W / 2 + 128}" y="50" width="${W - 170}" height="8" rx="4" fill="#3a424e"/><rect id="${id}-bar" x="${-W / 2 + 128}" y="50" width="${f1((W - 170) * from / total)}" height="8" rx="4" fill="#ff6a5a"/></g></g></g>`);
    const tx = document.getElementById(`${id}-t`), bar = document.getElementById(`${id}-bar`), v = { s: from };
    if (o.big) { // x/y on the outer group, scale on the inner one (mixing them with svgOrigin on one element throws the chip off screen)
      const fly = t0 + (o.fly ?? 1.6);
      document.getElementById(id).setAttribute("opacity", "0");
      tl.fromTo(`#${id}`, { x: 540 - X, y: 860 - Y, opacity: 0 }, { x: 540 - X, y: 860 - Y, opacity: 1, duration: 0.15, immediateRender: false }, t0);
      tl.fromTo(`#${id}-in`, { scale: 0.2, svgOrigin: "0 0" }, { scale: 1.7, svgOrigin: "0 0", duration: 0.55, ease: "back.out(2)", immediateRender: false }, t0);
      tl.to(`#${id}`, { x: 0, y: 0, duration: 0.6, ease: "power3.inOut" }, fly);
      tl.to(`#${id}-in`, { scale: 1, svgOrigin: "0 0", duration: 0.6, ease: "power3.inOut" }, fly);
    } else tl.fromTo(`#${id}`, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, t0);
    tl.fromTo(v, { s: from }, { s: to, duration: Math.max(0.1, dur - (o.hold ?? 0.2)), ease: o.ease || "none", immediateRender: false,
      onUpdate: () => { tx.textContent = mmss(v.s); bar.setAttribute("width", f1(Math.max(0, (W - 170) * v.s / total))); } }, t0 + (o.big ? (o.fly ?? 1.6) : 0.1));
    for (let t = t0; t < t0 + dur - 0.2; t += 0.5) tl.fromTo(`#${id}-lite circle`, { opacity: 0.95 }, { opacity: 0, duration: 0.25, immediateRender: false }, t);
    if (o.out) tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
    return id;
  }

  // ---------------- the compression meter (over a live shot) ----------------
  function cpr(tl, layer, t0, dur, o = {}) {
    const id = `mcp${seq++}`, X = o.x ?? 880, Y = o.y ?? 640, bpm = o.bpm ?? 110, P = 60 / bpm, CM = 46; // 46 units a centimetre
    let g = `<g transform="translate(${X},${Y})"><g id="${id}"><g filter="url(#muDrop)"><rect x="-120" y="-250" width="240" height="560" rx="40" fill="#14181e" opacity=".88" ${O(4)}/></g>
      <text y="-200" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="28" fill="#f2c55c">ความลึก</text>
      <g transform="translate(-20,-160)"><rect x="-26" y="0" width="52" height="${6 * CM}" rx="10" fill="#2a323c" stroke="#5a6472" stroke-width="3"/>
        <rect x="-26" y="${5 * CM}" width="52" height="${CM}" rx="6" fill="${C.green}" opacity=".85"/>
        ${Array.from({ length: 7 }, (_, k) => `<path d="M26,${k * CM}h16" stroke="#cfd6de" stroke-width="3"/><text x="50" y="${k * CM + 8}" font-family="Kanit" font-weight="600" font-size="22" fill="#cfd6de">${k}</text>`).join("")}
        <g id="${id}-pl"><path d="M-40,-4H40" stroke="#fff" stroke-width="8" stroke-linecap="round"/><path d="M-34,-24l14,14l14,-14" stroke="#ffd23a" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></g>
      <text y="${-160 + 6 * CM + 46}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#fff">≥ 5 ซม.</text>
      <g transform="translate(0,${-160 + 6 * CM + 104})"><rect x="-108" y="-36" width="216" height="72" rx="36" fill="${C.red}" ${O(3.5)}/><g id="${id}-dot"><circle cx="-76" r="13" fill="#fff"/></g>
        <text x="16" y="13" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="36" fill="#fff">100–120</text></g>
      <text y="${-160 + 6 * CM + 172}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="26" fill="#f4f0e6">ครั้ง/นาที</text>
      <text id="${id}-n" y="-226" x="96" text-anchor="end" font-family="Kanit" font-weight="900" font-size="1" fill="#fff"></text></g></g>`;
    put(layer, g);
    tl.fromTo(`#${id}`, { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.45, ease: "back.out(1.6)", immediateRender: false }, t0);
    const t1 = t0 + (o.start ?? 0.1);
    for (let t = t1; t < t0 + dur - 0.2; t += P) {
      tl.to(`#${id}-pl`, { y: 5 * CM, duration: P * 0.42, ease: "power2.in" }, t);
      tl.to(`#${id}-pl`, { y: 0, duration: P * 0.5, ease: "power2.out" }, t + P * 0.45);
      tl.fromTo(`#${id}-dot`, { scale: 1.6, svgOrigin: "-76 0" }, { scale: 1, svgOrigin: "-76 0", duration: P * 0.8, ease: "power2.out", immediateRender: false }, t + P * 0.42);
    }
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
    return id;
  }

  // ---------------- two cards side by side: the wrong one crossed, the right one ticked ----------------
  //   MmUI.versus(tl, layer, t0, dur, o)  o.a / o.b labels, o.ia / o.ib icons (SVG, ~120 units), o.at [ta, tb] (s after t0), o.y
  const ICON_BED = `<path d="M-70,30V-6Q-70,-20 -56,-20H56Q70,-20 70,-6V30Z" fill="#e2d8ec" ${O(4)}/><path d="M-70,8Q0,26 70,8" stroke="#b8acc8" stroke-width="5" fill="none"/><path d="M-62,-20Q-62,-44 -40,-44H-12Q4,-44 4,-20Z" fill="#fff" ${O(3.5)}/>
    ${[-46, -16, 14, 44].map((x) => `<path d="M${x},30q6,10 0,20" stroke="#b8acc8" stroke-width="4" fill="none" stroke-linecap="round"/>`).join("")}`;
  const ICON_FLOOR = `${[-60, -20, 20, 60].map((x, k) => `<rect x="${x - 19}" y="-6" width="38" height="44" rx="3" fill="${["#9c6a46", "#8a5a3a", "#a87650", "#8e5e3c"][k]}" ${O(3.5)}/>`).join("")}
    <path d="M-70,-12H70" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><circle cx="-30" cy="-34" r="14" fill="${C.skinK}" ${O(3)}/><path d="M-14,-30H56Q64,-30 64,-22V-12H-14Z" fill="${C.singlet}" ${O(3)}/>`;
  function versus(tl, layer, t0, dur, o = {}) {
    const id = `mvs${seq++}`, Y = o.y ?? 420, at = o.at || [0.3, 1.0];
    const card = (x, art, text, ok, k) => `<g transform="translate(${x},${Y})"><g id="${id}-c${k}" opacity="0"><g filter="url(#muDrop)"><rect x="-210" y="-170" width="420" height="340" rx="36" fill="#fffaf2" ${O(5)}/></g>
      <g transform="translate(0,-40) scale(1.5)">${art}</g><text y="122" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="44" fill="${INK}">${text}</text>
      <g transform="translate(150,-130)"><g id="${id}-m${k}"><circle r="46" fill="${ok ? C.green : C.red}" ${O(4)}/>${ok ? `<path d="M-20,0l14,15l26,-30" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>` : `<path d="M-17,-17l34,34M17,-17l-34,34" stroke="#fff" stroke-width="10" stroke-linecap="round"/>`}</g></g>
      ${ok ? "" : `<path d="M-170,-120L170,110" stroke="${C.red}" stroke-width="12" stroke-linecap="round" opacity=".8"/>`}</g></g>`;
    put(layer, `<g id="${id}">${card(300, o.ia || ICON_BED, o.a || "ที่นอนนุ่ม", false, 0)}${card(780, o.ib || ICON_FLOOR, o.b || "พื้นแข็ง", true, 1)}</g>`);
    [0, 1].forEach((k) => {
      tl.fromTo(`#${id}-c${k}`, { opacity: 0, y: 60, rotation: k ? 6 : -6, svgOrigin: "0 0" }, { opacity: 1, y: 0, rotation: k ? 2 : -2, svgOrigin: "0 0", duration: 0.5, ease: "back.out(1.8)", immediateRender: false }, t0 + at[k]);
      tl.fromTo(`#${id}-m${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.4, ease: "back.out(3)", immediateRender: false }, t0 + at[k] + 0.3);
    });
    tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
  }

  // ---------------- Keng from above, on the planks ----------------
  function chestTop(L, o = {}) {
    const id = o.id || "ct", r = mk(o.seed || 77), bare = !!o.bare;
    // the floor: planks along the frame, dark gaps, grain; the bulb's warm pool and a vignette (in glow, so the set's darkness can sit under them)
    let s = `<rect x="-600" y="-600" width="2300" height="3200" fill="#2a1a10"/>`;
    for (let k = 0; k < 18; k++) { const x = -600 + k * 132;
      s += `<rect x="${x}" y="-600" width="128" height="3200" fill="url(#mu2Plank)" opacity="${f1(0.85 + r() * 0.15)}"/>`;
      for (let j = 0; j < 4; j++) { const gx = x + 16 + r() * 96; s += `<path d="M${f1(gx)},-600C${f1(gx + 10)},400 ${f1(gx - 10)},1200 ${f1(gx + 6)},2600" stroke="#2e1c12" stroke-width="${f1(1.5 + r() * 2)}" fill="none" opacity=".5"/>`; }
      if (r() > 0.4) { const ny = 200 + r() * 1500; s += `<path d="M${x},${f1(ny)}h128" stroke="#1a100a" stroke-width="5"/>`; } }
    put(L.set, s);
    // Keng: arms at his sides, the singlet (or bare skin), the face turned up to us, eyes shut
    const SK = "url(#mu2SkinK)";
    let b = `<g id="${id}-keng">`;
    b += `<path d="M330,520C270,560 250,700 262,820C270,940 280,1060 300,1150" stroke="${C.skinKS}" stroke-width="86" fill="none" stroke-linecap="round"/><path d="M330,520C270,560 250,700 262,820C270,940 280,1060 300,1150" stroke="${C.skinK}" stroke-width="70" fill="none" stroke-linecap="round"/>`;
    b += `<path d="M750,520C810,560 830,700 818,820C810,940 800,1060 780,1150" stroke="${C.skinKS}" stroke-width="86" fill="none" stroke-linecap="round"/><path d="M750,520C810,560 830,700 818,820C810,940 800,1060 780,1150" stroke="${C.skinK}" stroke-width="70" fill="none" stroke-linecap="round"/>`;
    b += `<ellipse cx="300" cy="1180" rx="40" ry="52" fill="${C.skinK}" ${O(4)}/><ellipse cx="780" cy="1180" rx="40" ry="52" fill="${C.skinK}" ${O(4)}/>`;
    const TORSO = "M372,462C420,440 660,440 708,462C760,486 776,560 770,680C764,820 740,1000 728,1240H352C340,1000 316,820 310,680C304,560 320,486 372,462Z";
    b += `<path d="${TORSO}" fill="${SK}" ${O(5)}/>`;
    if (!bare) b += `<path d="M410,470Q540,620 670,470L700,476C730,560 746,700 740,820C734,960 722,1100 716,1240H364C358,1100 346,960 340,820C334,700 350,560 380,476Z" fill="url(#mu2Sing)" ${O(4)}/>
      <path d="M410,470Q540,620 670,470" stroke="#c8ccce" stroke-width="6" fill="none"/>`;
    else b += `<path d="M420,520Q480,552 530,540M660,520Q600,552 550,540" stroke="${C.skinKS}" stroke-width="7" fill="none" stroke-linecap="round"/>
      <path d="M440,700Q540,740 640,700M470,860Q540,880 610,860" stroke="${C.skinKS}" stroke-width="4" fill="none" opacity=".45"/><path d="M540,560V900" stroke="${C.skinKS}" stroke-width="4" opacity=".4"/>`;
    b += `<path d="M352,1240H728V1320H352Z" fill="#3a4a6a" ${O(4)}/>`;
    b += `<rect x="500" y="400" width="80" height="80" fill="${C.skinKS}" ${O(4)}/>`;
    b += `<ellipse cx="540" cy="300" rx="96" ry="116" fill="${C.skinK}" ${O(5)}/><path d="M450,250C460,170 620,170 630,250C640,210 620,160 540,154C460,160 440,210 450,250Z" fill="#1a1412" ${O(4)}/>`;
    b += `<ellipse cx="444" cy="310" rx="14" ry="24" fill="${C.skinK}" ${O(3.5)}/><ellipse cx="636" cy="310" rx="14" ry="24" fill="${C.skinK}" ${O(3.5)}/>`;
    b += `<path d="M492,292q16,8 32,0M556,292q16,8 32,0" stroke="${INK}" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M490,268q18,-8 36,-2M554,266q18,-6 36,2" stroke="#1a1412" stroke-width="6" fill="none" stroke-linecap="round"/>`;
    b += `<path d="M534,300q-6,26 6,32" stroke="${C.skinKS}" stroke-width="5" fill="none" stroke-linecap="round"/><ellipse cx="540" cy="362" rx="18" ry="9" fill="#5a2a22" ${O(3)}/>`;
    b += `</g>`;
    put(L.act, b);
    // the x-ray: ribs, the breastbone, its lower half
    let x = `<g id="${id}-xr" opacity="0" style="mix-blend-mode:screen">`;
    for (let k = 0; k < 6; k++) { const y = 560 + k * 58, w = 150 + k * 14 - (k > 3 ? (k - 3) * 22 : 0);
      x += `<path d="M528,${y}C${528 - w * 0.6},${y - 10} ${528 - w},${y + 30} ${528 - w - 10},${y + 70}M552,${y}C${552 + w * 0.6},${y - 10} ${552 + w},${y + 30} ${552 + w + 10},${y + 70}" stroke="#8fe8ff" stroke-width="9" fill="none" stroke-linecap="round" opacity=".7"/>`; }
    x += `<path d="M420,540Q480,560 526,548M660,540Q600,560 554,548" stroke="#8fe8ff" stroke-width="10" fill="none" stroke-linecap="round" opacity=".8"/>`;
    x += `<rect x="522" y="530" width="36" height="370" rx="16" fill="#bff4ff" opacity=".8"/><path d="M540,900l-12,24h24z" fill="#bff4ff" opacity=".8"/></g>`;
    x += `<g id="${id}-low" opacity="0"><circle cx="540" cy="810" r="120" fill="url(#mu2XR)"/><rect x="518" y="716" width="44" height="190" rx="18" fill="#fff36a" stroke="#ffb020" stroke-width="5"/></g>`;
    put(L.glow, x);
    // the label for the lower half, on a leader (shown by handsAnim)
    put(L.light, `<g id="${id}-lowl" opacity="0"><path d="M576,808L700,640H760" stroke="#fffaf0" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="576" cy="808" r="9" fill="#fffaf0"/>${label(818, 640, "ครึ่งล่างกระดูกหน้าอก", `${id}-lowp`, { px: 32, fill: "#fff36a" })}</g>`);
    // Fon's forearms from the left (she kneels at his right side) and her hands, the heel on the breastbone
    const HC = C.skinF, HS = C.skinFS;
    let h = `<g id="${id}-arms"><g id="${id}-h1"><path d="M-80,1010L470,820" stroke="${C.teeS}" stroke-width="104" stroke-linecap="round"/><path d="M-80,1010L470,820" stroke="${HS}" stroke-width="88" stroke-linecap="round"/><path d="M-80,1000L470,812" stroke="${HC}" stroke-width="72" stroke-linecap="round"/>
        <path d="M-140,1060L60,990" stroke="${C.tee}" stroke-width="150" stroke-linecap="round"/>
        <ellipse cx="545" cy="808" rx="82" ry="64" fill="${HC}" ${O(4.5)}/>${[0, 1, 2, 3].map((k) => `<path d="M600,${770 + k * 26}q44,${-4 + k * 2} 70,${4 + k * 3}" stroke="${INK}" stroke-width="31" fill="none" stroke-linecap="round"/><path d="M600,${770 + k * 26}q44,${-4 + k * 2} 70,${4 + k * 3}" stroke="${HC}" stroke-width="23" fill="none" stroke-linecap="round"/>`).join("")}</g>
      <g id="${id}-h2"><path d="M-60,920L470,770" stroke="${C.teeS}" stroke-width="104" stroke-linecap="round"/><path d="M-60,920L470,770" stroke="${HS}" stroke-width="88" stroke-linecap="round"/><path d="M-60,912L470,762" stroke="${HC}" stroke-width="72" stroke-linecap="round"/>
        <path d="M-120,960L80,900" stroke="${C.tee}" stroke-width="150" stroke-linecap="round"/>
        <ellipse cx="540" cy="790" rx="80" ry="60" fill="${HC}" ${O(4.5)}/><path d="M500,780q30,-16 70,-8" stroke="${HS}" stroke-width="6" fill="none" stroke-linecap="round"/></g>
      <g id="${id}-lock">${[0, 1, 2, 3].map((k) => `<path d="M596,${756 + k * 26}q30,10 22,${30}" stroke="${INK}" stroke-width="28" fill="none" stroke-linecap="round"/><path d="M596,${756 + k * 26}q30,10 22,${30}" stroke="${HC}" stroke-width="20" fill="none" stroke-linecap="round"/>`).join("")}</g></g>`;
    put(L.glow, h);
    // the pads, their cables to the AED off the top right, their labels
    if (o.pads) {
      const pad = (k, x0, y0, a) => `<g transform="translate(${x0},${y0}) rotate(${a})"><g id="${id}-pad${k}"><rect x="-74" y="-96" width="148" height="192" rx="26" fill="#fbfbf6" ${O(4.5)}/><rect x="-60" y="-82" width="120" height="164" rx="18" fill="none" stroke="#c8ccd0" stroke-width="3"/>
        <g transform="translate(0,-10) scale(.8)"><circle cy="-40" r="14" fill="#9aa4b0"/><path d="M-30,40V-14Q-30,-24 -20,-24H20Q30,-24 30,-14V40Z" fill="#9aa4b0"/><rect x="${k ? 6 : -24}" y="${k ? 8 : -18}" width="18" height="22" rx="4" fill="${C.orange}"/></g>
        <path d="M-40,70h80" stroke="${C.orange}" stroke-width="8" stroke-linecap="round"/></g></g>`;
      let pd = `<path id="${id}-cab0" d="M430,520C440,380 620,260 760,-60" stroke="${C.orange}" stroke-width="14" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
        <path id="${id}-cab1" d="M716,860C860,700 880,300 820,-60" stroke="${C.orange}" stroke-width="14" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>`;
      pd += pad(0, 432, 600, -8) + pad(1, 712, 934, 28);
      pd += label(240, 450, "ใต้ไหปลาร้าขวา", `${id}-pl0`, { px: 36 }) + label(780, 1150, "ชายโครงซ้าย", `${id}-pl1`, { px: 36 });
      put(L.glow, pd);
    }
    // the check: Fon's head bent to his mouth, the breath that isn't there, the chest that doesn't rise
    if (o.fon) {
      put(L.glow, `<g id="${id}-fon"><ellipse cx="760" cy="250" rx="118" ry="104" fill="#1a1412" ${O(4)}/><path d="M680,200Q760,150 850,210" stroke="#3a2a22" stroke-width="6" fill="none"/>
        <ellipse cx="672" cy="300" rx="22" ry="30" fill="${C.skinF}" ${O(3.5)}/><path d="M860,240q70,10 110,-30" stroke="#1a1412" stroke-width="48" fill="none" stroke-linecap="round"/><circle cx="866" cy="238" r="20" fill="${C.red}" ${O(3)}/>
        <path d="M640,350Q700,380 760,350" stroke="#2a2e34" stroke-width="7" fill="none"/></g>
        <g id="${id}-br">${[0, 1, 2].map((k) => `<path d="M${560 + k * 18},${376 + k * 4}q20,20 6,40t8,38" stroke="#bfe6ff" stroke-width="6" fill="none" stroke-linecap="round" stroke-dasharray="10 10"/>`).join("")}</g>
        <g id="${id}-brx"><circle cx="590" cy="420" r="58" fill="none" stroke="${C.red}" stroke-width="10"/><path d="M549,461l82,-82" stroke="${C.red}" stroke-width="10" stroke-linecap="round"/></g>
        <g id="${id}-ar"><path d="M430,700v-90M410,630l20,-20l20,20M650,700v-90M630,630l20,-20l20,20" stroke="#bfe6ff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
        <g id="${id}-arx"><circle cx="540" cy="660" r="150" fill="none" stroke="${C.red}" stroke-width="12"/><path d="M434,766l212,-212" stroke="${C.red}" stroke-width="12" stroke-linecap="round"/></g>`);
    }
    put(L.glow, `<rect x="-600" y="-600" width="2300" height="3200" fill="url(#mu2Pool)" style="mix-blend-mode:screen"/><rect x="-200" y="-200" width="1480" height="2320" fill="url(#mu2Vig)"/>`);
  }

  function handsAnim(tl, id, t0, o = {}) {
    const h1 = t0 + (o.h1 ?? 1.2), h2 = t0 + (o.h2 ?? 2.0), end = t0 + (o.end ?? 4.4), P = 60 / (o.bpm ?? 110);
    tl.set([`#${id}-h1`, `#${id}-h2`, `#${id}-lock`], { opacity: 0 }, t0);
    tl.set(`#${id}-low`, { opacity: 0 }, t0);
    tl.to(`#${id}-xr`, { opacity: 0.9, duration: 0.45 }, t0 + 0.1);
    tl.to(`#${id}-low`, { opacity: 1, duration: 0.3 }, t0 + 0.55);
    tl.set(`#${id}-lowl`, { opacity: 0 }, t0);
    tl.fromTo(`#${id}-lowl`, { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(2)", immediateRender: false }, t0 + (o.lab ?? 0.7));
    for (let t = t0 + 0.6; t < h1; t += 0.6) tl.fromTo(`#${id}-low`, { scale: 1.12, svgOrigin: "540 810" }, { scale: 1, svgOrigin: "540 810", duration: 0.5, ease: "power2.out", immediateRender: false }, t);
    tl.fromTo(`#${id}-h1`, { x: -620, opacity: 1 }, { x: 0, opacity: 1, duration: 0.55, ease: "power3.out", immediateRender: false }, h1);
    tl.fromTo(`#${id}-h2`, { y: -160, x: -60, opacity: 0 }, { y: 0, x: 0, opacity: 1, duration: 0.4, ease: "back.out(2)", immediateRender: false }, h2);
    tl.to(`#${id}-lock`, { opacity: 1, duration: 0.2 }, h2 + 0.3);
    tl.to(`#${id}-xr`, { opacity: 0.45, duration: 0.4 }, h2);
    for (let t = h2 + 0.6; t < end - 0.1; t += P) {
      tl.to(`#${id}-arms`, { scale: 0.965, svgOrigin: "540 800", duration: P * 0.42, ease: "power2.in" }, t);
      tl.to(`#${id}-arms`, { scale: 1, svgOrigin: "540 800", duration: P * 0.5, ease: "power2.out" }, t + P * 0.45);
      tl.to(`#${id}-keng`, { scaleY: 0.985, svgOrigin: "540 1240", duration: P * 0.42, ease: "power2.in" }, t);
      tl.to(`#${id}-keng`, { scaleY: 1, svgOrigin: "540 1240", duration: P * 0.5, ease: "power2.out" }, t + P * 0.45);
    }
  }

  function padsAnim(tl, id, t0, o = {}) {
    const p0 = t0 + (o.p0 ?? 0.5), p1 = t0 + (o.p1 ?? 2.0);
    tl.set([`#${id}-pad0`, `#${id}-pad1`, `#${id}-pl0`, `#${id}-pl1`], { opacity: 0 }, t0);
    [[p0, 0], [p1, 1]].forEach(([t, k]) => {
      tl.fromTo(`#${id}-pad${k}`, { opacity: 0, scale: 1.8, rotation: k ? 30 : -30, svgOrigin: "0 0" }, { opacity: 1, scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.5, ease: "back.out(1.8)", immediateRender: false }, t);
      tl.fromTo(`#${id}-cab${k}`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.6, ease: "power2.out", immediateRender: false }, t + 0.25);
      tl.fromTo(`#${id}-pl${k}`, { opacity: 0, scale: 0, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.45, ease: "back.out(2.6)", immediateRender: false }, t + 0.3);
    });
  }

  function breathAnim(tl, id, t0, o = {}) {
    const a = t0 + (o.x0 ?? 0.9), b = t0 + (o.x1 ?? 1.7);
    tl.set([`#${id}-brx`, `#${id}-arx`], { opacity: 0 }, t0);
    tl.fromTo(`#${id}-fon`, { x: 160, y: -120 }, { x: 0, y: 0, duration: 0.5, ease: "power2.out", immediateRender: false }, t0);
    tl.fromTo(`#${id}-br`, { opacity: 0 }, { opacity: 0.9, duration: 0.3, immediateRender: false }, t0 + 0.3);
    tl.fromTo(`#${id}-ar`, { opacity: 0 }, { opacity: 0.9, duration: 0.3, immediateRender: false }, t0 + 0.45);
    tl.fromTo(`#${id}-brx`, { opacity: 0, scale: 1.6, svgOrigin: "590 420" }, { opacity: 1, scale: 1, svgOrigin: "590 420", duration: 0.35, ease: "back.out(2.4)", immediateRender: false }, a);
    tl.to(`#${id}-br`, { opacity: 0.25, duration: 0.3 }, a + 0.2);
    tl.fromTo(`#${id}-arx`, { opacity: 0, scale: 1.6, svgOrigin: "540 660" }, { opacity: 1, scale: 1, svgOrigin: "540 660", duration: 0.35, ease: "back.out(2.4)", immediateRender: false }, b);
    tl.to(`#${id}-ar`, { opacity: 0.25, duration: 0.3 }, b + 0.2);
  }

  // ---------------- the AED, close ----------------
  const vfTrace = (W, H, seed) => { const r = mk(seed), c = H / 2; let d = `M0,${c}`;
    for (let x = 5; x <= W; x += 5) { const a = 0.2 + 0.2 * Math.abs(Math.sin(x / 60)); d += `L${x},${f1(c + Math.sin(x / 8 + Math.sin(x / 21) * 2) * H * a + (r() - 0.5) * H * 0.1)}`; } return d; };
  const torsoPict = (k) => `<circle cy="-62" r="20" fill="#e8ecf2"/><path d="M-46,70V-22Q-46,-38 -30,-38H30Q46,-38 46,-22V70Z" fill="#e8ecf2"/>
    <rect id="${k}a" x="-36" y="-30" width="26" height="32" rx="5" fill="${C.orange}"/><rect id="${k}b" x="14" y="16" width="26" height="32" rx="5" fill="${C.orange}" transform="rotate(20 27 32)"/>`;
  function aedClose(L, o = {}) {
    const id = o.id || "ad", r = mk(o.seed || 31);
    let s = `<rect x="-600" y="-600" width="2300" height="3200" fill="#2a1a10"/>`;
    for (let k = 0; k < 18; k++) { const x = -600 + k * 132; s += `<rect x="${x}" y="-600" width="128" height="3200" fill="url(#mu2Plank)" opacity="${f1(0.85 + r() * 0.15)}"/>`;
      for (let j = 0; j < 3; j++) { const gx = x + 16 + r() * 96; s += `<path d="M${f1(gx)},-600C${f1(gx + 10)},400 ${f1(gx - 10)},1200 ${f1(gx + 6)},2600" stroke="#2e1c12" stroke-width="2" fill="none" opacity=".5"/>`; } }
    // Keng's arm and the edge of the singlet at the left, so we know where we are
    s += `<path d="M-120,1500C80,1460 160,1520 260,1700" stroke="${C.skinKS}" stroke-width="96" fill="none" stroke-linecap="round"/><path d="M-120,1500C80,1460 160,1520 260,1700" stroke="${C.skinK}" stroke-width="80" fill="none" stroke-linecap="round"/>`;
    put(L.set, s);
    const X = 560, Y = 980, W = 760, H = 560;
    let a = `<g id="${id}-dev">`;
    // the lid, hinged along the top edge and flipped up behind (its inside: the steps printed)
    a += `<g transform="translate(${X},${Y - H / 2})"><g id="${id}-lid"><rect x="${-W / 2 + 10}" y="-330" width="${W - 20}" height="320" rx="44" fill="#1e7a48" ${O(5)}/><rect x="${-W / 2 + 40}" y="-300" width="${W - 80}" height="260" rx="26" fill="#e8f6ee" ${O(3.5)}/>
      ${["1 เปิดเครื่อง", "2 ติดแผ่น", "3 ช็อก"].map((t, k) => `<g transform="translate(${-W / 2 + 90 + k * 210},-170)"><circle r="40" fill="${[C.green, C.blue, C.orange][k]}" ${O(3)}/><text y="12" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#fff">${k + 1}</text><text y="80" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="26" fill="${INK}">${t.slice(2)}</text></g>`).join("")}</g></g>`;
    // the body: a soft shadow, the green shell with its depth, the white face
    a += `<rect x="${X - W / 2 + 14}" y="${Y - H / 2 + 34}" width="${W}" height="${H}" rx="70" fill="#000" opacity=".4"/>`;
    a += `<rect x="${X - W / 2}" y="${Y - H / 2 + 20}" width="${W}" height="${H}" rx="70" fill="#167040" ${O(5)}/><rect x="${X - W / 2}" y="${Y - H / 2}" width="${W}" height="${H}" rx="70" fill="url(#mu2Aed)" ${O(5)}/>`;
    a += `<rect x="${X - W / 2 + 40}" y="${Y - H / 2 + 40}" width="${W - 80}" height="${H - 80}" rx="44" fill="#fbfbf6" ${O(4)}/>`;
    a += `<path d="M${X - W / 2 + 70},${Y - H / 2 + 60}H${X + W / 2 - 70}" stroke="#fff" stroke-width="10" opacity=".7" stroke-linecap="round"/>`;
    // power (1)
    a += `<g transform="translate(${X - 230},${Y - 120})"><g id="${id}-pring" opacity="0"><circle r="74" fill="none" stroke="${C.green}" stroke-width="10"/></g><g id="${id}-pwr"><circle r="56" fill="${C.green}" ${O(4)}/><path d="M-20,-14A26,26 0 1 0 20,-14" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M0,-32V0" stroke="#fff" stroke-width="9" stroke-linecap="round"/></g>
      <text y="104" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="${INK}">เปิด</text></g>`;
    // the screen and its states
    const SX = X + 120, SY = Y - 200, SW = 300, SH = 220;
    a += `<g transform="translate(${SX},${SY})"><rect x="-14" y="-14" width="${SW + 28}" height="${SH + 28}" rx="24" fill="#2a2e34" ${O(4)}/><rect width="${SW}" height="${SH}" rx="14" fill="#0e1418"/>
      <g id="${id}-s1" opacity="0"><g transform="translate(${SW / 2},${SH / 2 + 4}) scale(1.05)">${torsoPict(`${id}-pk`)}</g></g>
      <g id="${id}-s2" opacity="0"><defs><clipPath id="${id}-sc"><rect id="${id}-sw" x="0" y="0" width="0" height="${SH}"/></clipPath></defs><g clip-path="url(#${id}-sc)"><path d="${vfTrace(SW, 120, 9)}" transform="translate(0,20)" stroke="#7aff9a" stroke-width="4" fill="none"/></g>
        <text x="${SW / 2}" y="${SH - 54}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="28" fill="#7aff9a">กำลังวิเคราะห์</text>
        <g id="${id}-warn"><rect x="40" y="${SH - 40}" width="${SW - 80}" height="34" rx="17" fill="${C.red}"/><text x="${SW / 2}" y="${SH - 14}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="24" fill="#fff">ห้ามสัมผัสผู้ป่วย</text></g></g>
      <g id="${id}-s3" opacity="0"><path d="M${SW / 2 + 16},28l-46,84h40l-28,76l74,-104h-42l30,-56z" fill="${C.orange}" stroke="#fff3c0" stroke-width="5" stroke-linejoin="round"/>
        <text x="${SW / 2}" y="${SH - 14}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="#ffd23a">กดปุ่มช็อก</text></g>
      <path d="M10,10Q${SW / 2},0 ${SW - 10},10" stroke="#fff" stroke-width="3" opacity=".12" fill="none"/></g>`;
    // shock (3)
    a += `<g transform="translate(${X},${Y + 130})"><g id="${id}-sglow" opacity="0"><circle r="150" fill="url(#mu2Glow)"/></g><g id="${id}-shock"><circle r="78" fill="${C.orange}" ${O(5)}/><circle r="78" fill="none" stroke="#fff" stroke-width="6" opacity=".4" transform="scale(.86)"/>
      <path d="M10,-48l-30,54h26l-18,46l48,-64h-28l20,-36z" fill="#fff" ${O(3)}/></g><text y="122" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="${INK}">ช็อก</text></g>`;
    // speaker grille and its waves
    a += `<g transform="translate(${X + 250},${Y + 120})">${[-24, -8, 8, 24].map((dy) => `<path d="M-30,${dy}h60" stroke="#9aa4b0" stroke-width="7" stroke-linecap="round"/>`).join("")}
      ${[0, 1, 2].map((k) => `<path id="${id}-w${k}" d="M${48 + k * 18},${-30 - k * 10}q${14 + k * 4},${30 + k * 10} 0,${60 + k * 20}" stroke="${C.green}" stroke-width="7" fill="none" stroke-linecap="round" opacity="0"/>`).join("")}</g>`;
    // the socket, the orange cable and the pads pack
    a += `<path d="M${X - W / 2 + 60},${Y + 180}C${X - W / 2 - 60},${Y + 260} ${X - 520},${Y + 300} ${X - 520},${Y + 470}" stroke="${C.orangeD}" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M${X - W / 2 + 60},${Y + 180}C${X - W / 2 - 60},${Y + 260} ${X - 520},${Y + 300} ${X - 520},${Y + 470}" stroke="${C.orange}" stroke-width="14" fill="none" stroke-linecap="round"/>`;
    a += `</g>`;
    put(L.act, a);
  }
  function aedOn(tl, id, t0) {
    tl.set([`#${id}-s1`, `#${id}-s2`, `#${id}-s3`], { opacity: 0 }, t0);
    tl.fromTo(`#${id}-lid`, { scaleY: 0.08, svgOrigin: "0 0" }, { scaleY: 1, svgOrigin: "0 0", duration: 0.55, ease: "back.out(1.6)", immediateRender: false }, t0 + 0.1);
    tl.to(`#${id}-pwr`, { scale: 0.86, svgOrigin: "0 0", duration: 0.1, ease: "power2.in" }, t0 + 0.75);
    tl.to(`#${id}-pwr`, { scale: 1, svgOrigin: "0 0", duration: 0.3, ease: "back.out(3)" }, t0 + 0.85);
    tl.fromTo(`#${id}-pring`, { opacity: 1, scale: 0.8, svgOrigin: "0 0" }, { opacity: 0, scale: 1.6, svgOrigin: "0 0", duration: 0.6, ease: "power2.out", immediateRender: false }, t0 + 0.85);
    aedState(tl, id, t0 + 0.95, 1);
  }
  function aedState(tl, id, t, k) {
    [1, 2, 3].forEach((j) => tl.set(`#${id}-s${j}`, { opacity: j === k ? 1 : 0 }, t));
  }
  function aedTalk(tl, id, t0, dur) {
    for (let t = t0; t < t0 + dur - 0.15; t += 0.36) [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-w${k}`, { opacity: 0 }, { opacity: 1, duration: 0.12, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }, t + k * 0.07));
  }
  function aedPads(tl, id, t0, dur) { // the pads on the screen blink in turn
    for (let t = t0; t < t0 + dur - 0.2; t += 0.8) { tl.fromTo(`#${id}-pka`, { opacity: 0.2 }, { opacity: 1, duration: 0.2, immediateRender: false }, t); tl.fromTo(`#${id}-pkb`, { opacity: 0.2 }, { opacity: 1, duration: 0.2, immediateRender: false }, t + 0.4); }
  }
  function aedAnalyze(tl, id, t0, dur) {
    aedState(tl, id, t0, 2);
    tl.fromTo(`#${id}-sw`, { attr: { width: 0 } }, { attr: { width: 300 }, duration: Math.min(2.2, dur), ease: "none", immediateRender: false }, t0);
    for (let t = t0 + 0.2; t < t0 + dur - 0.2; t += 0.5) tl.fromTo(`#${id}-warn`, { opacity: 1 }, { opacity: 0.35, duration: 0.25, yoyo: true, repeat: 1, immediateRender: false }, t);
  }
  function aedShock(tl, id, t0, at) {
    aedState(tl, id, t0, 3);
    for (let t = t0; t < t0 + at; t += 0.3) tl.fromTo(`#${id}-sglow`, { opacity: 0.95, scale: 0.9, svgOrigin: "0 0" }, { opacity: 0.2, scale: 1.15, svgOrigin: "0 0", duration: 0.28, ease: "sine.out", immediateRender: false }, t);
    tl.to(`#${id}-shock`, { scale: 0.86, svgOrigin: "0 0", duration: 0.08, ease: "power2.in" }, t0 + at);
    tl.to(`#${id}-shock`, { scale: 1, svgOrigin: "0 0", duration: 0.3, ease: "back.out(3)" }, t0 + at + 0.1);
    tl.set(`#${id}-sglow`, { opacity: 0 }, t0 + at + 0.12);
  }

  // ---------------- the AED small, in a wide shot ----------------
  Mm.aedKit = (x, G, s, o = {}) => {
    const id = o.id || "ak";
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})"><g id="${id}">
      <path d="M-70,-8L-62,-150L62,-158L70,-12Z" fill="#1e7a48" ${O(4)}/><path d="M-50,-30L-46,-130L46,-136L50,-34Z" fill="#e8f6ee" ${O(3)}/>
      <rect x="-80" y="-34" width="160" height="40" rx="14" fill="#2fa864" ${O(4)}/><rect x="-58" y="-28" width="116" height="24" rx="8" fill="#fbfbf6"/>
      <g id="${id}-kscr"><rect x="4" y="-26" width="44" height="20" rx="4" fill="#7aff9a" opacity=".85"/></g><circle cx="-40" cy="-16" r="9" fill="${C.green}"/><circle cx="-14" cy="-16" r="9" fill="${C.orange}"/>
      ${o.cable ? `<path d="M80,-14C130,-20 ${o.cable[0] - x},${o.cable[1] - G + 40} ${o.cable[0] - x},${o.cable[1] - G}" stroke="${C.orange}" stroke-width="8" fill="none" stroke-linecap="round"/>` : ""}</g></g>`;
  };

  // ---------------- the widow's arm out of the dark ----------------
  Mm.ghostArm = (x, y, s, o = {}) => {
    const id = o.id || "garm", BL = "#050607", RIM = "#7a9ac8";
    const arm = `<path d="M720,-160C560,-120 420,-60 300,-50C200,-40 100,-20 10,-6" stroke="${BL}" stroke-width="34" fill="none" stroke-linecap="round"/>
      <path d="M720,-178C560,-140 420,-80 300,-70C200,-60 100,-36 14,-22" stroke="${RIM}" stroke-width="5" fill="none" opacity=".9"/>
      <ellipse cx="-14" cy="0" rx="44" ry="30" fill="${BL}"/>`;
    const open = [-26, -10, 6, 22].map((d, i) => `<path d="M-40,${d}q${-50 - i * 6},${-8 + i * 6} ${-110 - i * 12},${4 + i * 10}" stroke="${BL}" stroke-width="10" fill="none" stroke-linecap="round"/>`).join("") + `<path d="M-20,-24q-20,-30 -60,-44" stroke="${BL}" stroke-width="11" fill="none" stroke-linecap="round"/>`;
    const shut = [-26, -10, 6, 22].map((d, i) => `<path d="M-40,${d}q${-46 - i * 4},${-6 + i * 4} ${-60 - i * 4},${36 + i * 6}q-6,30 30,${40 - i * 4}" stroke="${BL}" stroke-width="10" fill="none" stroke-linecap="round"/>`).join("") + `<path d="M-20,-24q-30,-10 -44,20" stroke="${BL}" stroke-width="11" fill="none" stroke-linecap="round"/>`;
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><g id="${id}">${arm}<g id="${id}-open">${open}</g><g id="${id}-shut" opacity="0">${shut}</g></g></g>`;
  };

  Object.assign(Sets, { chestTop, aedClose });
  Object.assign(window.MmUI, { phone, eta, cpr, versus, handsAnim, padsAnim, breathAnim, aedOn, aedState, aedTalk, aedPads, aedAnalyze, aedShock, IC });
})();
