// "ตึกโยก" on-screen graphics (screen space: put them in L.light unless noted). Motion-graphics standard of the channel (mmui.js):
// ink outlines, 3–4 flat colours + one shade + one highlight, entries with back/elastic easing staggered 0.12–0.15 s, and a secondary
// motion that keeps running until the shot ends.
//   QkUI.title(tl, layer, t0, dur, o)    the EP.1 opener title: ROD MAI CLUB · "ตึกโยก" swaying like the tower on a seismograph line ·
//                                        o.ep "EP.1 · หมอบ ป้อง เกาะ"
//   QkUI.app(tl, layer, t0, dur, o)      your left hand holding the phone with the rider app: the route map to เดอะสกาย 32, the order
//                                        (ห้อง 2714 · มิว · ก๋วยเตี๋ยวต้มยำ "ไม่ใส่ผัก!!"), the clock (o.clock "13:18") and the countdown
//                                        o.eta [from, to] seconds over the shot
//   QkUI.eta(tl, layer, t0, dur, o)      the HUD chip top-left: scooter, ห้อง 2714, the countdown o.eta [from, to] (00:00 → "ถึงแล้ว")
//   QkUI.choice(tl, layer, t0, dur, o)   the first-person choice: o.q, o.a / o.b { text, icon }, a 3-2-1 ring (o.secs), the cursor
//                                        hesitating then picking o.pick at o.pickAt; o.mark { at, wrong, right } stamps ✗ / ✓;
//                                        o.pull: the cursor drifts to o.pick as the ring runs out (the end-of-episode question)
//   QkUI.rewind(tl, layer, t0, dur, o)   VHS rewind over the shot: tracking bars, ◀◀, a clock running back (o.from → o.to text)
//   QkUI.note(tl, layer, t0, dur, o)     แม่'s note on the fridge = the rule card: 3 rhyming rules with stickers; o.active (1–3) gets a
//                                        highlighter swipe and its sticker animates, o.done ticks, later rules are faint pencil;
//                                        o.at [t…] (seconds into the shot) when each row lands · o.out
//   QkUI.labels(tl, layer, t0, o)        telestrator call-outs: o.items [{ x, y, lx, ly, text, icon, at }] — a pulsing dot on the body,
//                                        a line that draws to a pill with a moving icon
//   QkUI.seismo(tl, layer, t0, dur, o)   a seismogram drawing itself: the main shock, then smaller aftershocks with pills, and "หลบซ้ำ"
//   QkUI.quakeMap(tl, L, sid, t0, o)     on Sets.mapTH (id o.map): hides its route bits, an epicentre burst in Myanmar with rings that
//                                        sweep over Bangkok, the Bangkok pin with a swaying tower and a counter "โยกนานกว่า 20 วินาที"
//                                        (o.count [start, end]), the date chip (o.chipAt)
//   QkUI.call(tl, layer, t0, dur, o)     a phone close in a hand calling "แม่ ♥": rings, then "ไม่มีผู้รับสาย" (o.failAt)
//   QkUI.endCard(tl, layer, t0, dur, o)  the end card: มิว's orange whistle on its lanyard with a paper tag (o.l1 "ตอนที่ 2", o.l2 "ลงบันได")
//   QkUI.ICON.<name>(s)                  pictograms in a 120-unit circle: duck cover hold table lift stairs whistle candle torch
(function () {
  const INK = "#2a2420", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  let seq = 0;
  const nid = () => `qu${++seq}`;
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mmss = (s) => { s = Math.max(0, Math.round(s)); return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`; };

  Sets.DEFS += `
    <linearGradient id="quPanel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16201f" stop-opacity=".94"/><stop offset="1" stop-color="#0b1112" stop-opacity=".94"/></linearGradient>
    <linearGradient id="quNote" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf4"/><stop offset="1" stop-color="#f6efdc"/></linearGradient>
    <linearGradient id="quHi" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffe45a" stop-opacity=".75"/><stop offset="1" stop-color="#ffd23a" stop-opacity=".6"/></linearGradient>
    <radialGradient id="quBurst"><stop offset="0" stop-color="#fff2b0"/><stop offset=".35" stop-color="#ff8a3a" stop-opacity=".85"/><stop offset="1" stop-color="#e8382a" stop-opacity="0"/></radialGradient>
    <linearGradient id="quTag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8f0dc"/><stop offset="1" stop-color="#e6d8b8"/></linearGradient>
    <filter id="quDrop" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur in="SourceAlpha" stdDeviation="9"/><feOffset dy="12"/><feComponentTransfer><feFuncA type="linear" slope=".45"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>`;

  // ---------------- pictograms (120-unit circle, centre 60,60) ----------------
  const disc = (bg = "#f6efdc") => `<circle cx="60" cy="60" r="56" fill="${bg}" ${OUT(5)}/><path d="M22,40A44,44 0 0 1 60,16" stroke="#fff" stroke-width="7" fill="none" opacity=".6" stroke-linecap="round"/>`;
  const person = (x, y, s = 1, c = "#2a2420") => `<g transform="translate(${x},${y}) scale(${s})" fill="${c}">`;
  const ICON = {
    // หมอบ: a figure dropping low, the arrow pushing down
    duck: () => `${disc("#fbe7a8")}<g class="quAn" data-a="duck"><circle cx="60" cy="52" r="9" fill="${INK}"/><path d="M60,62Q48,70 46,84H74Q72,70 60,62Z" fill="#2fa45a" ${OUT(3)}/><path d="M46,84L38,94M74,84L82,94" ${OUT(6)}/></g>
      <g class="quArr"><path d="M60,18V34" stroke="#d8312a" stroke-width="7" stroke-linecap="round"/><path d="M50,28L60,40L70,28" stroke="#d8312a" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      <path d="M26,98H94" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`,
    // ป้อง: a head with both arms over it, bits bouncing off
    cover: () => `${disc("#cfe8f4")}<circle cx="60" cy="70" r="16" fill="#e8b88e" ${OUT(4)}/><path d="M34,78Q34,50 60,48Q86,50 86,78" fill="none" stroke="#2fa45a" stroke-width="12" stroke-linecap="round"/><path d="M34,78Q34,50 60,48Q86,50 86,78" fill="none" ${OUT(3)}/>
      <path d="M42,96Q60,88 78,96" stroke="${INK}" stroke-width="6" fill="none" stroke-linecap="round"/>
      <g class="quBits"><rect x="46" y="18" width="10" height="10" fill="#8a7a6a" ${OUT(2)} transform="rotate(20 51 23)"/><rect x="66" y="24" width="8" height="8" fill="#8a7a6a" ${OUT(2)} transform="rotate(-15 70 28)"/></g>`,
    // เกาะ: a hand gripping a table leg
    hold: () => `${disc("#f4d8c8")}<g class="quTbl"><path d="M20,40H100" stroke="#8a5a36" stroke-width="12" stroke-linecap="round"/><path d="M34,40V100M86,40V100" stroke="#8a5a36" stroke-width="10" stroke-linecap="round"/></g>
      <g class="quGrip"><path d="M70,66Q92,60 96,76Q98,90 84,92L72,90" fill="#e8b88e" ${OUT(4)}/><path d="M78,68V88M86,70V90" stroke="#9a6a48" stroke-width="3"/><path d="M96,78H112" stroke="#2fa45a" stroke-width="16" stroke-linecap="round"/></g>`,
    // หมอบใต้โต๊ะ: the whole drill, a figure crouched under a table with hands on the head
    table: () => `${disc("#e2f2d8")}<g class="quTbl"><path d="M14,46H106" stroke="#8a5a36" stroke-width="10" stroke-linecap="round"/><path d="M24,46V98M96,46V98" stroke="#8a5a36" stroke-width="8" stroke-linecap="round"/></g>
      <g class="quAn" data-a="duck"><circle cx="60" cy="70" r="9" fill="${INK}"/><path d="M48,66Q60,56 72,66" stroke="#2fa45a" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M60,80Q46,84 44,96H76Q74,84 60,80Z" fill="#2fa45a" ${OUT(3)}/></g>
      <path d="M14,100H106" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><g class="quBits"><rect x="56" y="16" width="10" height="10" fill="#8a7a6a" ${OUT(2)}/></g>`,
    // วิ่งไปลิฟต์: lift doors with the arrows, a running figure
    lift: () => `${disc("#dfe4e8")}<rect x="36" y="28" width="48" height="70" fill="#b8c0c6" ${OUT(4)}/><path d="M60,28V98" ${OUT(3)}/><path d="M48,20l6,-8l6,8zM66,12l6,8l6,-8z" fill="#d8312a"/>
      <g class="quRun"><circle cx="30" cy="54" r="7" fill="${INK}"/><path d="M28,62L22,80M22,80L30,92M22,80L12,88M26,66L36,72M26,66L16,70" ${OUT(5)} fill="none"/></g>`,
    // ลงบันได ไม่ใช่ลิฟต์ (rule 2)
    stairs: () => `${disc("#e2f2d8")}<path d="M18,96H40V80H58V64H76V48H98" fill="none" stroke="#8a5a36" stroke-width="8" stroke-linejoin="round"/><g class="quAn" data-a="walk"><circle cx="44" cy="52" r="7" fill="${INK}"/><path d="M44,60L46,72M46,72L40,80M46,72L52,78M44,62L52,66" ${OUT(5)} fill="none"/></g>
      <g transform="translate(86,26)"><circle r="16" fill="#fff" stroke="#d8312a" stroke-width="5"/><rect x="-7" y="-9" width="14" height="18" fill="#b8c0c6"/><path d="M-11,11L11,-11" stroke="#d8312a" stroke-width="5"/></g>`,
    // ติดใต้ซาก: whistle with sound waves (rule 3)
    whistle: () => `${disc("#fde2c8")}<g transform="translate(50,66) rotate(-10)"><path d="M-22,-10H12Q28,-10 28,8Q28,26 8,26Q-8,26 -10,12H-22Z" fill="#f47b20" ${OUT(4)}/><rect x="-36" y="-10" width="16" height="12" rx="3" fill="#f47b20" ${OUT(3)}/><circle cx="8" cy="8" r="6" fill="#b8500e"/></g>
      <g class="quWave">${[0, 1, 2].map((k) => `<path d="M${84 + k * 9},${44 - k * 6}q${8},${16 + k * 6} 0,${32 + k * 12}" stroke="#d8312a" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}</g>`,
    candle: () => `${disc("#fde8c8")}<rect x="50" y="48" width="20" height="52" rx="3" fill="#f6f0e2" ${OUT(4)}/><path class="quFlame" d="M60,22Q72,36 66,44Q60,50 54,44Q48,36 60,22Z" fill="#ffb03a" ${OUT(3)}/>`,
    torch: () => `${disc("#e0ecf8")}<g transform="rotate(-30 60 60)"><rect x="50" y="56" width="20" height="44" rx="4" fill="#2a2a2c" ${OUT(4)}/><rect x="46" y="44" width="28" height="14" rx="3" fill="#f2c230" ${OUT(3)}/><path class="quBeam" d="M50,44L36,10H84L70,44Z" fill="#fff6c8" opacity=".85"/></g>`,
  };
  const icon = (name, x, y, s = 1, id = "") => `<g transform="translate(${x},${y}) scale(${s})"><g ${id ? `id="${id}"` : ""}><defs><clipPath id="${id || nid()}c"><circle cx="60" cy="60" r="54"/></clipPath></defs>${ICON[name]()}</g></g>`;
  // secondary motion inside an icon, run from t until t + dur
  function iconLife(tl, root, t, dur) {
    const q = (s) => root.querySelectorAll(s), n = Math.max(1, Math.round(dur / 0.5));
    q(".quArr").forEach((e) => tl.fromTo(e, { y: -4 }, { y: 6, duration: 0.25, repeat: n * 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".quBits").forEach((e) => tl.fromTo(e, { y: -10, opacity: 0 }, { y: 18, opacity: 1, duration: 0.5, repeat: n, ease: "bounce.out", immediateRender: false }, t));
    q(".quTbl").forEach((e) => tl.fromTo(e, { x: -3 }, { x: 3, duration: 0.09, repeat: n * 5, yoyo: true, ease: "none", immediateRender: false }, t));
    q(".quGrip").forEach((e) => tl.fromTo(e, { x: 2 }, { x: -2, duration: 0.09, repeat: n * 5, yoyo: true, ease: "none", immediateRender: false }, t));
    q(".quRun").forEach((e) => tl.fromTo(e, { x: -6 }, { x: 8, duration: 0.3, repeat: n * 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".quWave").forEach((e) => tl.fromTo(e, { opacity: 0.2 }, { opacity: 1, duration: 0.2, repeat: n * 2, yoyo: true, immediateRender: false }, t));
    q(".quFlame").forEach((e) => tl.fromTo(e, { scaleY: 0.9, svgOrigin: "60 44" }, { scaleY: 1.12, svgOrigin: "60 44", duration: 0.12, repeat: n * 4, yoyo: true, immediateRender: false }, t));
    q('.quAn[data-a="duck"]').forEach((e) => tl.fromTo(e, { y: -6 }, { y: 2, duration: 0.4, repeat: n, yoyo: true, ease: "power2.inOut", immediateRender: false }, t));
    q('.quAn[data-a="walk"]').forEach((e) => tl.fromTo(e, { x: -6, y: -8 }, { x: 8, y: 8, duration: 0.8, repeat: Math.ceil(n / 2), ease: "none", immediateRender: false }, t));
  }

  // ---------------- the opener title ----------------
  function title(tl, layer, t0, dur, o = {}) {
    const id = nid();
    // a seismograph trace: flat, then the swing
    let tr = "M90,0";
    for (let x = 90; x <= 990; x += 6) { const k = (x - 90) / 900, a = k < 0.25 ? 3 : 70 * Math.sin(Math.PI * Math.min(1, (k - 0.25) / 0.6)) * (k < 0.85 ? 1 : 0.4); tr += `L${x},${f1(Math.sin(x * 0.23) * a + Math.sin(x * 0.61) * a * 0.35)}`; }
    put(layer, `<g id="${id}" opacity="0"><rect x="0" y="120" width="1080" height="640" fill="url(#${id}g)"/>
      <defs><linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05090c" stop-opacity=".75"/><stop offset=".7" stop-color="#05090c" stop-opacity=".45"/><stop offset="1" stop-color="#05090c" stop-opacity="0"/></linearGradient></defs>
      <text x="540" y="268" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" letter-spacing="16" fill="#f4ecd8" opacity=".85">ROD MAI CLUB</text>
      <g id="${id}-t"><text x="540" y="470" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="210" fill="#f6efe0" stroke="#140e0a" stroke-width="12" paint-order="stroke">ตึกโยก</text>
        <path d="M640,300l-20,60l26,22l-30,52l18,30" stroke="#140e0a" stroke-width="9" fill="none" stroke-linejoin="round"/><path d="M640,300l-20,60l26,22l-30,52l18,30" stroke="#ff6a3a" stroke-width="3" fill="none" stroke-linejoin="round"/></g>
      <g transform="translate(0,560)"><path id="${id}-tr" d="${tr}" stroke="#ff4a3a" stroke-width="6" fill="none" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></g>
      <g transform="translate(540,660)"><g id="${id}-ep"><rect x="-250" y="-44" width="500" height="80" rx="40" fill="#d8312a" stroke="#140e0a" stroke-width="6"/>
        <text x="0" y="14" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#fff6ea">${o.ep || "EP.1 · หมอบ ป้อง เกาะ"}</text></g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, t0);
    tl.fromTo(`#${id}-t`, { scale: 1.6, opacity: 0, svgOrigin: "540 470" }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.2)", immediateRender: false }, t0 + 0.05);
    tl.fromTo(`#${id}-t`, { rotation: -3.5, svgOrigin: "540 480" }, { rotation: 3.5, svgOrigin: "540 480", duration: 0.55, repeat: Math.ceil(dur / 0.55), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.4);
    tl.fromTo(`#${id}-tr`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 1.5, ease: "power1.inOut", immediateRender: false }, t0 + 0.3);
    tl.fromTo(`#${id}-ep`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.45, ease: "back.out(2.6)", immediateRender: false }, t0 + 0.75);
    tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
  }

  // ---------------- the rider app in your hand ----------------
  function app(tl, layer, t0, dur, o = {}) {
    const id = nid(), X = 540, Y = o.y ?? 1180, W = 560, H = 1040, [e0, e1] = o.eta || [120, 110];
    put(layer, `<g id="${id}" transform="translate(${X},${Y})" opacity="0"><g id="${id}-in">
      <path d="M-330,520Q-360,300 -300,180L-250,120L-200,560Z" fill="#2fa45a" ${OUT(5)}/><path d="M-340,420H-210" stroke="#e8f0e8" stroke-width="16" opacity=".85"/>
      <rect x="${-W / 2}" y="${-H / 2}" width="${W}" height="${H}" rx="56" fill="#1e2228" ${OUT(5)}/><rect x="${-W / 2 + 18}" y="${-H / 2 + 18}" width="${W - 36}" height="${H - 36}" rx="42" fill="#f4f6f4"/>
      <rect x="${-W / 2 + 18}" y="${-H / 2 + 18}" width="${W - 36}" height="150" rx="42" fill="#2fa45a"/><rect x="${-W / 2 + 18}" y="${-H / 2 + 120}" width="${W - 36}" height="48" fill="#2fa45a"/>
      <text x="${-W / 2 + 60}" y="${-H / 2 + 62}" font-family="Kanit" font-weight="700" font-size="28" fill="#e8f6ec">${o.clock || "13:18"}</text>
      <g transform="translate(${-W / 2 + 96},${-H / 2 + 118})"><circle r="30" fill="#fff4dc" ${OUT(3)}/><path d="M-17,-2h34q-2,17 -17,19q-15,-2 -17,-19z" fill="#e2a92e" ${OUT(2)}/></g>
      <text x="${-W / 2 + 140}" y="${-H / 2 + 130}" font-family="Kanit" font-weight="800" font-size="40" fill="#fff">อิ่มด่วน · ไรเดอร์</text>
      <g transform="translate(0,${-H / 2 + 330})"><rect x="-240" y="-140" width="480" height="280" rx="18" fill="#e4eee4"/>
        <path d="M-240,-40H240M-100,-140V140M120,-140V140M-240,80L240,10" stroke="#fff" stroke-width="14"/><path d="M-240,-40H240M-100,-140V140M120,-140V140M-240,80L240,10" stroke="#cfd8cf" stroke-width="2"/>
        <path id="${id}-route" d="M-200,110L-100,96L-100,-40L120,-40L150,-90" stroke="#2fa45a" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
        <circle cx="-200" cy="110" r="14" fill="#2a5cb8" stroke="#fff" stroke-width="4"/><g transform="translate(150,-90)"><path d="M0,0C-22,-24 -26,-40 -26,-50A26,26 0 0 1 26,-50C26,-40 22,-24 0,0Z" fill="#d8312a" ${OUT(3)}/><circle cy="-50" r="9" fill="#fff"/></g>
        <text x="150" y="-150" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="26" fill="#2a3a2a">เดอะสกาย 32</text></g>
      <g transform="translate(0,${-H / 2 + 560})"><text x="-220" y="0" font-family="Kanit" font-weight="800" font-size="46" fill="#1e2228">ห้อง 2714 · มิว</text>
        <text x="-220" y="56" font-family="Kanit" font-weight="400" font-size="32" fill="#3a4a3a">ก๋วยเตี๋ยวต้มยำ x1</text>
        <g id="${id}-noteg"><rect x="-226" y="78" width="452" height="64" rx="14" fill="#fff1c8" stroke="#e2a92e" stroke-width="3"/><text x="0" y="122" text-anchor="middle" font-family="Mali" font-weight="700" font-size="34" fill="#c8281e">"ไม่ใส่ผัก!! ไม่ใส่ผัก!!"</text></g></g>
      <g transform="translate(0,${H / 2 - 150})"><rect x="-240" y="-60" width="480" height="120" rx="30" fill="#1e2228"/><text x="-200" y="14" font-family="Kanit" font-weight="700" font-size="32" fill="#cfe8d4">ส่งภายใน</text>
        <text id="${id}-eta" x="200" y="22" text-anchor="end" font-family="Kanit" font-weight="900" font-size="66" fill="#ffd23a">${mmss(e0)}</text></g>
      <path d="M${W / 2 - 20},-120Q${W / 2 + 40},-110 ${W / 2 + 46},-40Q${W / 2 + 48},0 ${W / 2 - 10},10" fill="#c99068" ${OUT(4)}/>
      <path d="M-${W / 2 + 10},-60Q-${W / 2 + 60},-40 -${W / 2 + 56},40Q-${W / 2 + 50},80 -${W / 2 - 14},80" fill="#c99068" ${OUT(4)}/></g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { y: 700, rotation: 8, svgOrigin: "0 0" }, { y: 0, rotation: -3, svgOrigin: "0 0", duration: 0.55, ease: "back.out(1.4)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-route`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 1.2, ease: "power2.inOut", immediateRender: false }, t0 + 0.4);
    tl.fromTo(`#${id}-noteg`, { scale: 0, svgOrigin: "0 110" }, { scale: 1, svgOrigin: "0 110", duration: 0.4, ease: "back.out(3)", immediateRender: false }, t0 + 0.9);
    tl.fromTo(`#${id}-noteg`, { rotation: -2, svgOrigin: "0 110" }, { rotation: 2, svgOrigin: "0 110", duration: 0.18, repeat: Math.ceil(dur / 0.18), yoyo: true, immediateRender: false }, t0 + 1.3);
    const el = document.getElementById(`${id}-eta`), c = { v: e0 };
    tl.fromTo(c, { v: e0 }, { v: e1, duration: dur, ease: "none", immediateRender: false, onUpdate: () => { el.textContent = mmss(c.v); } }, t0);
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + dur - 0.2);
  }

  // ---------------- the HUD chip ----------------
  function eta(tl, layer, t0, dur, o = {}) {
    const id = nid(), [e0, e1] = o.eta || [100, 80];
    put(layer, `<g id="${id}" transform="translate(${o.x ?? 40},${o.y ?? 150})" opacity="0"><rect width="${o.w ?? 400}" height="96" rx="48" fill="#0c1412" opacity=".82"/><rect width="${o.w ?? 400}" height="96" rx="48" fill="none" stroke="#2fa45a" stroke-width="4"/>
      <g transform="translate(52,48)"><circle r="34" fill="#2fa45a"/><path d="M-20,8L-6,-12H10L20,8M-6,-12L-10,-20" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="-20" cy="10" r="7" fill="#fff"/><circle cx="20" cy="10" r="7" fill="#fff"/></g>
      <text x="100" y="40" font-family="Kanit" font-weight="700" font-size="26" fill="#cfe8d4">ห้อง 2714</text>
      <text id="${id}-v" x="100" y="80" font-family="Kanit" font-weight="900" font-size="40" fill="#ffd23a">ส่งภายใน ${mmss(e0)}</text></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, x: (o.x ?? 40) - 60 }, { opacity: 1, x: o.x ?? 40, duration: o.pop === false ? 0.01 : 0.3, ease: "back.out(2)", immediateRender: false }, t0);
    const el = document.getElementById(`${id}-v`), c = { v: e0 };
    tl.fromTo(c, { v: e0 }, { v: e1, duration: dur, ease: "none", immediateRender: false, onUpdate: () => { el.textContent = c.v <= 0.5 ? "ถึงแล้ว!" : `ส่งภายใน ${mmss(c.v)}`; el.setAttribute("fill", c.v <= 10.5 ? "#ff6a4a" : "#ffd23a"); } }, t0);
    if (e1 <= 0.5) tl.fromTo(`#${id}`, { scale: 1, svgOrigin: "200 48" }, { scale: 1.12, svgOrigin: "200 48", duration: 0.15, repeat: 5, yoyo: true, immediateRender: false }, t0 + dur * (e0 / Math.max(0.01, e0 - e1)) - 0.1);
    if (o.out) tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + o.out);
  }

  // ---------------- the first-person choice ----------------
  function choice(tl, layer, t0, dur, o = {}) {
    const id = nid(), secs = o.secs ?? 3, A = o.a, B = o.b, Y = [o.yA ?? 880, o.yB ?? 1190];
    const card = (k, c) => `<g transform="translate(540,${Y[k]})"><g id="${id}-c${k}"><rect x="-430" y="-130" width="860" height="260" rx="34" fill="url(#quPanel)" stroke="#f4ecd8" stroke-opacity=".35" stroke-width="4"/>
        <rect id="${id}-f${k}" x="-436" y="-136" width="872" height="272" rx="38" fill="none" stroke="#ffd23a" stroke-width="9" opacity="0"/>
        <text x="-370" y="-76" font-family="Kanit" font-weight="900" font-size="34" fill="#ffd23a">${k ? "B" : "A"}</text>
        ${icon(c.icon, -330, -96, 1.6, `${id}-i${k}`)}<text x="-110" y="24" font-family="Kanit" font-weight="900" font-size="74" fill="#f6efe0">${c.text}</text>
        <g id="${id}-x${k}" opacity="0"><circle cx="340" cy="0" r="66" fill="#d8312a" stroke="#fff" stroke-width="7"/><path d="M314,-26L366,26M366,-26L314,26" stroke="#fff" stroke-width="14" stroke-linecap="round"/></g>
        <g id="${id}-v${k}" opacity="0"><circle cx="340" cy="0" r="66" fill="#1e9a50" stroke="#fff" stroke-width="7"/><path d="M308,0l22,24l40,-46" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></g></g>`;
    put(layer, `<g id="${id}" opacity="0"><rect width="1080" height="1920" fill="#05090c" opacity=".42"/>
      <g transform="translate(540,560)"><rect x="-400" y="-70" width="800" height="140" rx="70" fill="#f6efe0" stroke="#140e0a" stroke-width="6"/><text x="-40" y="22" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="58" fill="#1e1a16">${o.q || "คุณจะทำยังไง?"}</text>
        <g transform="translate(300,0)"><circle r="52" fill="#1e1a16"/><circle id="${id}-ring" r="42" fill="none" stroke="#ffd23a" stroke-width="10" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0" transform="rotate(-90)"/>
          <text id="${id}-n" y="20" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="56" fill="#fff">${secs}</text></g></g>
      ${card(0, A)}${card(1, B)}</g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.18, immediateRender: false }, t0);
    [0, 1].forEach((k) => {
      tl.fromTo(`#${id}-c${k}`, { scale: 0.6, opacity: 0, svgOrigin: "0 0" }, { scale: 1, opacity: 1, svgOrigin: "0 0", duration: 0.4, ease: "back.out(2)", immediateRender: false }, t0 + 0.12 + k * 0.14);
      iconLife(tl, document.getElementById(`${id}-i${k}`), t0 + 0.5, dur);
    });
    const ring = { k: 0 }, n = document.getElementById(`${id}-n`), ringEl = document.getElementById(`${id}-ring`), T = o.pickAt ?? secs;
    tl.fromTo(ring, { k: 0 }, { k: 1, duration: T, ease: "none", immediateRender: false, onUpdate: () => { ringEl.setAttribute("stroke-dashoffset", f1(ring.k)); n.textContent = String(Math.max(0, Math.ceil(secs * (1 - ring.k) - 0.001))); } }, t0);
    // the cursor: hovers A, B, A… then lands on the pick
    const hov = o.hover || [[0.4, 0], [1.0, 1], [1.6, 0]], pick = o.pick === "b" ? 1 : 0;
    hov.forEach(([t, k]) => { tl.set(`#${id}-f${k}`, { opacity: 1 }, t0 + t); tl.set(`#${id}-f${1 - k}`, { opacity: 0 }, t0 + t); });
    tl.set(`#${id}-f${pick}`, { opacity: 1 }, t0 + T); tl.set(`#${id}-f${1 - pick}`, { opacity: 0 }, t0 + T);
    tl.fromTo(`#${id}-c${pick}`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.07, svgOrigin: "0 0", duration: 0.12, yoyo: true, repeat: 1, immediateRender: false }, t0 + T);
    tl.to(`#${id}-c${1 - pick}`, { opacity: 0.35, duration: 0.15 }, t0 + T);
    if (o.mark) {
      const { at, wrong = "a" } = o.mark, w = wrong === "a" ? 0 : 1;
      tl.fromTo(`#${id}-x${w}`, { opacity: 0, scale: 2.4, svgOrigin: "340 0" }, { opacity: 1, scale: 1, svgOrigin: "340 0", duration: 0.25, ease: "back.out(3)", immediateRender: false }, t0 + at);
      tl.to(`#${id}-c${w}`, { opacity: 0.45, duration: 0.2 }, t0 + at + 0.2);
      tl.to(`#${id}-c${1 - w}`, { opacity: 1, duration: 0.1 }, t0 + at + 0.25);
      tl.set(`#${id}-f${1 - w}`, { opacity: 1 }, t0 + at + 0.25); tl.set(`#${id}-f${w}`, { opacity: 0 }, t0 + at + 0.25);
      tl.fromTo(`#${id}-v${1 - w}`, { opacity: 0, scale: 2.4, svgOrigin: "340 0" }, { opacity: 1, scale: 1, svgOrigin: "340 0", duration: 0.3, ease: "back.out(3)", immediateRender: false }, t0 + at + 0.4);
      tl.fromTo(`#${id}-c${1 - w}`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.08, svgOrigin: "0 0", duration: 0.16, yoyo: true, repeat: 1, immediateRender: false }, t0 + at + 0.4);
    }
    if (o.out !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.15 }, t0 + o.out);
    return id;
  }

  // ---------------- VHS rewind ----------------
  function rewind(tl, layer, t0, dur, o = {}) {
    const id = nid();
    const bars = [0, 1, 2].map((k) => `<rect id="${id}-b${k}" x="0" y="0" width="1080" height="${60 + k * 30}" fill="#fff" opacity=".22"/>`).join("");
    let lines = ""; for (let y = 0; y < 1920; y += 8) lines += `<path d="M0,${y}H1080" stroke="#000" stroke-width="3" opacity=".18"/>`;
    put(layer, `<g id="${id}" opacity="0"><rect width="1080" height="1920" fill="#2a3a6a" opacity=".22"/>${lines}${bars}
      <g transform="translate(70,190)"><path d="M60,0L0,40L60,80ZM130,0L70,40L130,80Z" fill="#fff"/><text x="160" y="64" font-family="Kanit" font-weight="900" font-size="64" fill="#fff" letter-spacing="4">ย้อนกลับ</text></g>
      ${o.from ? `<text id="${id}-tc" x="1010" y="254" text-anchor="end" font-family="Kanit" font-weight="700" font-size="56" fill="#fff">${o.from}</text>` : ""}</g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.08, immediateRender: false }, t0);
    [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-b${k}`, { y: 1920 * (k / 3) }, { y: -400, duration: 0.45 + k * 0.1, repeat: Math.ceil(dur / 0.45), ease: "none", immediateRender: false }, t0));
    if (o.from && o.to) { const tc = document.getElementById(`${id}-tc`), [h0, m0] = o.from.split(":").map(Number), [h1, m1] = o.to.split(":").map(Number), c = { v: h0 * 60 + m0 };
      tl.fromTo(c, { v: h0 * 60 + m0 }, { v: h1 * 60 + m1, duration: dur * 0.8, ease: "power2.inOut", immediateRender: false, onUpdate: () => { const v = Math.round(c.v); tc.textContent = `${Math.floor(v / 60)}:${String(v % 60).padStart(2, "0")}`; } }, t0); }
    tl.to(`#${id}`, { opacity: 0, duration: 0.12 }, t0 + dur - 0.12);
  }

  // ---------------- แม่'s note on the fridge: the rule card ----------------
  const RULES = [
    ["duck", "ตึกโยก อย่า<u>วิ่ง</u>", "หมอบ ป้อง เกาะ อย่า<u>ทิ้ง</u>"],
    ["stairs", "หยุดสั่นแล้ว<u>ไป</u>", "ลงบัน<u>ได</u> ไม่ใช่ลิฟต์"],
    ["whistle", "ติดใต้<u>ซาก</u> อย่าอ้า<u>ปาก</u>ตะโกน", "เคาะท่อ เป่านกหวีด"],
  ];
  function note(tl, layer, t0, dur, o = {}) {
    const id = nid(), act = o.active ?? 1, done = o.done || [], at = o.at || [0.6, 1.4, 2.2], Y0 = o.y ?? 250;
    const row = (k) => {
      const [ic, l1, l2] = RULES[k], st = k + 1 === act ? "act" : done.includes(k + 1) ? "done" : "later", y = 300 + k * 300;
      const col = st === "later" ? "#8a8478" : "#2a2420", u = (s) => s.replace(/<u>(.*?)<\/u>/g, `<tspan class="quU" fill="${st === "later" ? "#8a8478" : "#c8281e"}">$1</tspan>`);
      return `<g id="${id}-r${k}" opacity="${st === "later" ? 0.38 : 1}">
        ${st === "act" ? `<rect id="${id}-hl" x="250" y="${y - 96}" width="610" height="180" rx="16" fill="url(#quHi)"/>` : ""}
        <g transform="translate(70,${y - 100})"><g id="${id}-s${k}"${st === "later" ? ` filter="url(#quGray)"` : ""}>${icon(ic, 0, 0, 1.5, `${id}-ic${k}`)}</g></g>
        <text x="270" y="${y - 22}" font-family="Mali" font-weight="700" font-size="${l1.replace(/<[^>]+>/g, "").length > 20 ? 50 : 60}" fill="${col}">${u(l1)}</text>
        <text x="270" y="${y + 58}" font-family="Mali" font-weight="700" font-size="${l2.length > 22 ? 50 : 56}" fill="${col}">${u(l2)}</text>
        ${st === "done" ? `<g id="${id}-tk${k}"><path d="M74,${y - 10}l40,40l80,-90" stroke="#1e9a50" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>` : ""}
        ${k < 2 ? `<path d="M60,${y + 130}H960" stroke="#c8dce8" stroke-width="3" stroke-dasharray="4 10"/>` : ""}</g>`;
    };
    put(layer, `<defs><filter id="quGray"><feColorMatrix type="saturate" values="0"/></filter></defs>
      <g id="${id}" transform="translate(40,${Y0})" opacity="0"><g id="${id}-m"><g id="${id}-s"><g id="${id}-w"><g id="${id}-p" filter="url(#quDrop)">
      <path d="M0,20Q0,0 20,0H980Q1000,0 1000,20V1180Q1000,1200 980,1200H20Q0,1200 0,1180Z" fill="url(#quNote)" stroke="#d8ccb0" stroke-width="3"/>
      ${Array.from({ length: 11 }, (_, k) => `<path d="M40,${180 + k * 96}H960" stroke="#bcd4e6" stroke-width="2" opacity=".7"/>`).join("")}<path d="M150,40V1160" stroke="#f0a8a8" stroke-width="3"/>
      <text x="500" y="118" text-anchor="middle" font-family="Mali" font-weight="700" font-size="58" fill="#c8281e">ถ้าตึกโยก… จำไว้นะลูก</text>
      ${[0, 1, 2].map(row).join("")}
      <text x="930" y="1160" text-anchor="end" font-family="Mali" font-weight="700" font-size="48" fill="#c8281e">♥ แม่</text>
      <circle cx="120" cy="30" r="34" fill="#3aa0e8" stroke="#1e5a8a" stroke-width="4"/><circle cx="110" cy="20" r="10" fill="#fff" opacity=".5"/>
      <circle cx="880" cy="30" r="34" fill="#f2c230" stroke="#8a6a10" stroke-width="4"/><circle cx="870" cy="20" r="10" fill="#fff" opacity=".5"/></g></g></g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, t0);
    tl.fromTo(`#${id}-m`, { x: -120, y: 220 }, { x: 0, y: 0, duration: 0.6, ease: "back.out(1.4)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-s`, { scale: 0.35, rotation: -9, svgOrigin: "500 600" }, { scale: 1, rotation: -1.5, svgOrigin: "500 600", duration: 0.6, ease: "back.out(1.4)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-w`, { rotation: -1, svgOrigin: "500 0" }, { rotation: 1, svgOrigin: "500 0", duration: 1.6, repeat: Math.ceil(dur / 1.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.6);
    [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-r${k}`, { x: -30 }, { x: 0, duration: 0.35, ease: "power2.out", immediateRender: false }, t0 + at[k]));
    const a = act - 1;
    if (a >= 0 && a < 3) {
      tl.fromTo(`#${id}-hl`, { scaleX: 0, svgOrigin: "250 0" }, { scaleX: 1, svgOrigin: "250 0", duration: 0.5, ease: "power2.inOut", immediateRender: false }, t0 + at[a] + 0.2);
      tl.fromTo(`#${id}-s${a}`, { scale: 0, rotation: -40, svgOrigin: "90 90" }, { scale: 1, rotation: 0, svgOrigin: "90 90", duration: 0.5, ease: "back.out(2.6)", immediateRender: false }, t0 + at[a]);
      iconLife(tl, document.getElementById(`${id}-ic${a}`), t0 + at[a] + 0.5, dur);
      document.getElementById(`${id}-r${a}`).querySelectorAll(".quU").forEach((u, j) => tl.fromTo(u, { attr: { "font-size": 60 } }, { attr: { "font-size": 72 }, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, t0 + at[a] + 0.7 + j * 0.25));
    }
    done.forEach((d) => { const el = document.getElementById(`${id}-tk${d - 1}`); if (el) tl.fromTo(el, { opacity: 0, scale: 2, svgOrigin: `130 ${300 + (d - 1) * 300}` }, { opacity: 1, scale: 1, svgOrigin: `130 ${300 + (d - 1) * 300}`, duration: 0.3, ease: "back.out(3)", immediateRender: false }, t0 + at[d - 1] + 0.3); });
    if (o.out !== undefined) { tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + o.out); tl.to(`#${id}-m`, { y: -40, duration: 0.25 }, t0 + o.out); }
  }

  // ---------------- call-outs on the bodies ----------------
  function labels(tl, layer, t0, o = {}) {
    (o.items || []).forEach((it) => {
      const id = nid(), at = t0 + (it.at ?? 0), w = 90 + it.text.length * 42;
      put(layer, `<g id="${id}" opacity="0"><circle cx="${it.x}" cy="${it.y}" r="16" fill="#ffd23a" stroke="#140e0a" stroke-width="5"/><circle id="${id}-pu" cx="${it.x}" cy="${it.y}" r="16" fill="none" stroke="#ffd23a" stroke-width="6"/>
        <path id="${id}-ln" d="M${it.x},${it.y}L${it.lx},${it.ly}" stroke="#ffd23a" stroke-width="8" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
        <g transform="translate(${it.lx},${it.ly})"><g id="${id}-pl"><rect x="-70" y="-62" width="${w + 70}" height="124" rx="62" fill="#140e0a" stroke="#ffd23a" stroke-width="6"/>
          ${icon(it.icon, -64, -56, 0.94, `${id}-ic`)}<text x="${62}" y="24" font-family="Kanit" font-weight="900" font-size="72" fill="#ffd23a">${it.text}</text></g></g></g>`);
      tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.1, immediateRender: false }, at);
      tl.fromTo(`#${id}-ln`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.25, ease: "power2.out", immediateRender: false }, at);
      tl.fromTo(`#${id}-pl`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.4, ease: "back.out(2.6)", immediateRender: false }, at + 0.15);
      tl.fromTo(`#${id}-pu`, { attr: { r: 16 }, opacity: 1 }, { attr: { r: 60 }, opacity: 0, duration: 0.8, repeat: 4, ease: "power2.out", immediateRender: false }, at);
      iconLife(tl, document.getElementById(`${id}-ic`), at + 0.4, it.dur ?? 3);
      if (it.end !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + it.end);
    });
  }

  // ---------------- the seismogram ----------------
  function seismo(tl, layer, t0, dur, o = {}) {
    const id = nid(), X0 = 110, X1 = 970, Y = o.y ?? 860, draw = o.draw ?? 2.6;
    const amp = (k) => (k < 0.08 ? 4 : k < 0.42 ? 230 * Math.sin(Math.PI * (k - 0.08) / 0.34) : 0) + [[0.58, 0.05, 80], [0.72, 0.04, 60], [0.86, 0.035, 46]].reduce((s, [c, w, a]) => s + (Math.abs(k - c) < w ? a * Math.sin(Math.PI * (k - c + w) / (2 * w)) : 0), 0);
    let d = `M${X0},0`;
    for (let x = X0; x <= X1; x += 4) { const k = (x - X0) / (X1 - X0), a = amp(k); d += `L${x},${f1(Math.sin(x * 0.42) * a * (0.6 + 0.4 * Math.sin(x * 0.09)) + Math.sin(x * 1.3) * 3)}`; }
    const pill = (x, y, t, c, k) => `<g transform="translate(${x},${y})"><g id="${id}-p${k}"><rect x="${-(28 + t.length * 15)}" y="-30" width="${56 + t.length * 30}" height="60" rx="30" fill="${c}" stroke="#140e0a" stroke-width="4"/><text y="12" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#fff">${t}</text></g></g>`;
    put(layer, `<g id="${id}" opacity="0"><rect x="60" y="${Y - 420}" width="960" height="840" rx="40" fill="url(#quPanel)" stroke="#f4ecd8" stroke-opacity=".3" stroke-width="4"/>
      <text x="110" y="${Y - 340}" font-family="Kanit" font-weight="800" font-size="44" fill="#f4ecd8">คลื่นแผ่นดินไหว</text>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M${X0},${Y - 260 + k * 65}H${X1}" stroke="#f4ecd8" stroke-width="1.5" opacity=".12"/>`).join("")}
      <defs><clipPath id="${id}-cl"><rect id="${id}-cr" x="${X0 - 10}" y="${Y - 300}" width="0" height="600"/></clipPath></defs>
      <g clip-path="url(#${id}-cl)"><path d="${d}" transform="translate(0,${Y})" stroke="#ff5a46" stroke-width="5" fill="none" stroke-linejoin="round"/></g>
      <circle id="${id}-pen" cx="${X0}" cy="${Y}" r="12" fill="#fff" stroke="#ff5a46" stroke-width="5"/>
      <text x="${X1}" y="${Y + 360}" text-anchor="end" font-family="Kanit" font-weight="600" font-size="30" fill="#f4ecd8" opacity=".7">เวลา →</text>
      ${pill(X0 + (X1 - X0) * 0.25, Y + 265, "แผ่นดินไหวหลัก", "#d8312a", 0)}${pill(X0 + (X1 - X0) * 0.72, Y + 170, "อาฟเตอร์ช็อก", "#e8822a", 1)}
      <g transform="translate(${X1 - 110},${Y - 330})"><g id="${id}-dk">${icon("table", -64, -64, 1.07, `${id}-tb`)}</g></g>
      <g transform="translate(${X1 - 110},${Y - 170})"><g id="${id}-dl"><rect x="-100" y="-30" width="200" height="60" rx="30" fill="#1e9a50" stroke="#140e0a" stroke-width="4"/><text y="12" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#fff">หลบซ้ำ</text></g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out", immediateRender: false }, t0);
    tl.fromTo(`#${id}-cr`, { attr: { width: 0 } }, { attr: { width: X1 - X0 + 20 }, duration: draw, ease: "none", immediateRender: false }, t0 + 0.25);
    const pen = document.getElementById(`${id}-pen`), c = { k: 0 };
    tl.fromTo(c, { k: 0 }, { k: 1, duration: draw, ease: "none", immediateRender: false, onUpdate: () => { const x = X0 + (X1 - X0) * c.k, a = amp(c.k); pen.setAttribute("cx", f1(x)); pen.setAttribute("cy", f1(Y + Math.sin(x * 0.42) * a * (0.6 + 0.4 * Math.sin(x * 0.09)))); } }, t0 + 0.25);
    [[0, 0.2], [1, 0.62]].forEach(([k, f]) => tl.fromTo(`#${id}-p${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.35, ease: "back.out(2.6)", immediateRender: false }, t0 + 0.25 + draw * f));
    tl.fromTo([`#${id}-dk`, `#${id}-dl`], { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.45, stagger: 0.12, ease: "back.out(2.6)", immediateRender: false }, t0 + 0.25 + draw * 0.75);
    iconLife(tl, document.getElementById(`${id}-tb`), t0 + 0.25 + draw * 0.8, dur);
    if (o.out !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + o.out);
  }

  // ---------------- the real quake on the map (draws into the map's set layer) ----------------
  function quakeMap(tl, L, sid, t0, o = {}) {
    const mp = o.map || "mq", X = o.x ?? 90, Y = o.y ?? 300, S = o.s ?? 1, W = (lon, lat) => { const [px, py] = Maps.P(lon, lat); return [X + px * S, Y + py * S]; };
    const [ex, ey] = W(95.9, 22.0), [bx, by] = W(100.5, 13.75), id = `${sid}-qm`;
    ["pin0", "pin1", "sh0", "sh1", "lab0", "lab1", "car", "rip"].forEach((p) => { if (document.getElementById(`${mp}-${p}`)) tl.set(`#${mp}-${p}`, { opacity: 0 }, t0); });
    if (document.getElementById(`${mp}-reveal`)) tl.set(`#${mp}-reveal`, { attr: { "stroke-dashoffset": 1 } }, t0);
    put(L.glow, `<g id="${id}">${[0, 1, 2, 3].map((k) => `<circle id="${id}-r${k}" cx="${f1(ex)}" cy="${f1(ey)}" r="10" fill="none" stroke="#e8382a" stroke-width="7" opacity="0"/>`).join("")}
      <g id="${id}-ep"><circle cx="${f1(ex)}" cy="${f1(ey)}" r="90" fill="url(#quBurst)"/><path d="M${f1(ex)},${f1(ey - 34)}l10,22l24,-6l-14,20l18,16l-24,2l-2,24l-12,-20l-12,20l-2,-24l-24,-2l18,-16l-14,-20l24,6z" fill="#ffd23a" stroke="#140e0a" stroke-width="4"/></g>
      <g transform="translate(${f1(ex + 40)},${f1(ey + 90)})"><g id="${id}-el"><rect x="-10" y="-40" width="330" height="80" rx="40" fill="#140e0a"/><text x="155" y="14" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="38" fill="#ffd23a">เมียนมา · ขนาด 8.2</text></g></g>
      <g transform="translate(${f1(bx)},${f1(by)})"><g id="${id}-bk"><path d="M0,0C-30,-34 -36,-56 -36,-70A36,36 0 0 1 36,-70C36,-56 30,-34 0,0Z" fill="#d8312a" stroke="#140e0a" stroke-width="4"/><circle cy="-70" r="14" fill="#fff"/></g></g>
      <g transform="translate(${f1(bx + 50)},${f1(by - 40)})"><g id="${id}-bl"><rect x="0" y="-40" width="230" height="80" rx="40" fill="#fffaf0" stroke="#140e0a" stroke-width="4"/><text x="115" y="14" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="40" fill="#140e0a">กรุงเทพฯ</text></g></g>
      <g transform="translate(${f1(bx - 150)},${f1(by + 210)})"><g id="${id}-tw" opacity="0"><g id="${id}-tws"><rect x="-30" y="-180" width="60" height="180" fill="#5f8fb0" stroke="#140e0a" stroke-width="4"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M-22,${-160 + k * 28}H22" stroke="#cfe6f2" stroke-width="5"/>`).join("")}</g>
        <rect x="40" y="-120" width="360" height="110" rx="24" fill="#140e0a" stroke="#ffd23a" stroke-width="5"/><text x="220" y="-78" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#f4ecd8">ตึกสูงโยกนานกว่า</text>
        <text id="${id}-cnt" x="220" y="-26" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#ffd23a">0 วินาที</text></g></g></g>`);
    put(L.light, `<g id="${id}-chip" opacity="0" transform="translate(540,200)"><rect x="-420" y="-56" width="840" height="112" rx="56" fill="#140e0a" stroke="#ffd23a" stroke-width="5"/>
      <text y="16" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="46" fill="#fff">28 มี.ค. 2568 · 13:20 น.</text></g>`);
    tl.fromTo(`#${id}-ep`, { scale: 0, svgOrigin: `${f1(ex)} ${f1(ey)}` }, { scale: 1, svgOrigin: `${f1(ex)} ${f1(ey)}`, duration: 0.5, ease: "back.out(3)", immediateRender: false }, t0 + 0.1);
    tl.fromTo(`#${id}-ep`, { rotation: -8, svgOrigin: `${f1(ex)} ${f1(ey)}` }, { rotation: 8, svgOrigin: `${f1(ex)} ${f1(ey)}`, duration: 0.12, repeat: 60, yoyo: true, immediateRender: false }, t0 + 0.6);
    const reach = Math.hypot(bx - ex, by - ey) + 160;
    [0, 1, 2, 3].forEach((k) => tl.fromTo(`#${id}-r${k}`, { attr: { r: 10 }, opacity: 0.9 }, { attr: { r: reach }, opacity: 0, duration: 2.2, repeat: 3, ease: "power1.out", immediateRender: false }, t0 + 0.3 + k * 0.55));
    tl.fromTo(`#${id}-el`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.4, ease: "back.out(2.6)", immediateRender: false }, t0 + (o.labelAt ?? 1.4));
    tl.fromTo(`#${id}-chip`, { opacity: 0, y: 160 }, { opacity: 1, y: 200, duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + (o.chipAt ?? 0.3));
    tl.fromTo(`#${id}-bk`, { y: -160, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "bounce.out", immediateRender: false }, t0 + (o.bkkAt ?? 2.8));
    tl.fromTo(`#${id}-bl`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.4, ease: "back.out(2.6)", immediateRender: false }, t0 + (o.bkkAt ?? 2.8) + 0.4);
    const [c0, c1] = o.count || [5.9, 8.2], cnt = document.getElementById(`${id}-cnt`), cc = { v: 0 };
    tl.to(`#${id}-el`, { opacity: 0, duration: 0.3 }, t0 + c0 - 0.6);
    tl.fromTo(`#${id}-tw`, { opacity: 0, scale: 0.6, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + c0);
    tl.fromTo(`#${id}-tws`, { rotation: -4, svgOrigin: "0 0" }, { rotation: 4, svgOrigin: "0 0", duration: 0.6, repeat: Math.ceil((c1 - c0) / 0.6) + 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + c0);
    tl.fromTo(cc, { v: 0 }, { v: 20, duration: c1 - c0 - 0.3, ease: "power1.in", immediateRender: false, onUpdate: () => { cnt.textContent = `${Math.round(cc.v)}${cc.v >= 19.5 ? "+" : ""} วินาที`; } }, t0 + c0 + 0.2);
    if (o.out !== undefined) tl.to(`#${id}-chip`, { opacity: 0, duration: 0.2 }, t0 + o.out);
  }

  // ---------------- calling แม่ ----------------
  function call(tl, layer, t0, dur, o = {}) {
    const id = nid(), X = o.x ?? 640, Y = o.y ?? 1240;
    put(layer, `<g id="${id}" transform="translate(${X},${Y}) rotate(${o.rot ?? 6})" opacity="0"><rect x="-200" y="-380" width="400" height="760" rx="48" fill="#1e2228" ${OUT(5)}/><rect x="-184" y="-364" width="368" height="728" rx="36" fill="#2a3a5a"/>
      <circle cy="-180" r="80" fill="#f4c8d8" ${OUT(4)}/><text y="-150" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="80" fill="#c8281e">♥</text>
      <text y="-40" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="60" fill="#fff">แม่</text>
      <text id="${id}-s" y="20" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="36" fill="#cfd8e8">กำลังโทร…</text>
      <text id="${id}-f" y="20" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="40" fill="#ff8a7a" opacity="0">ไม่มีผู้รับสาย</text>
      ${[0, 1, 2].map((k) => `<circle id="${id}-w${k}" cy="-180" r="80" fill="none" stroke="#fff" stroke-width="4" opacity="0"/>`).join("")}
      <circle cy="250" r="56" fill="#e8443a"/><path d="M-26,250h52" stroke="#fff" stroke-width="12" stroke-linecap="round"/>
      <path d="M-200,120Q-260,140 -250,260Q-240,380 -120,400" fill="#e8b88e" ${OUT(4)}/></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, y: Y + 300 }, { opacity: 1, y: Y, duration: 0.4, ease: "back.out(1.6)", immediateRender: false }, t0);
    [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-w${k}`, { attr: { r: 80 }, opacity: 0.8 }, { attr: { r: 170 }, opacity: 0, duration: 1, repeat: 3, ease: "power1.out", immediateRender: false }, t0 + 0.3 + k * 0.33));
    const f = t0 + (o.failAt ?? dur - 1);
    tl.to(`#${id}-s`, { opacity: 0, duration: 0.1 }, f);
    tl.fromTo(`#${id}-f`, { opacity: 0, scale: 1.5, svgOrigin: "0 10" }, { opacity: 1, scale: 1, svgOrigin: "0 10", duration: 0.3, ease: "back.out(3)", immediateRender: false }, f);
    [0, 1, 2].forEach((k) => tl.set(`#${id}-w${k}`, { opacity: 0 }, f));
  }

  // ---------------- the end card: the orange whistle and its tag ----------------
  function endCard(tl, layer, t0, dur, o = {}) {
    const id = nid();
    put(layer, `<g id="${id}" opacity="0"><rect width="1080" height="1920" fill="#120e0c"/><rect width="1080" height="1920" fill="url(#${id}v)"/>
      <defs><radialGradient id="${id}v" cx=".5" cy=".42" r=".7"><stop offset="0" stop-color="#3a2a22"/><stop offset="1" stop-color="#0a0706"/></radialGradient></defs>
      <g transform="translate(540,0) scale(1.3) translate(-540,0)"><g id="${id}-sw"><path d="M540,-20V560" stroke="#e8682a" stroke-width="10"/><path d="M548,-20V560" stroke="#ff9a5a" stroke-width="3" opacity=".6"/>
        <g transform="translate(540,640) rotate(-8)"><path d="M-110,-60H70Q150,-60 150,30Q150,120 50,120Q-30,120 -40,50H-110Z" fill="#f47b20" stroke="#140e0a" stroke-width="8"/>
          <rect x="-190" y="-60" width="90" height="70" rx="14" fill="#f47b20" stroke="#140e0a" stroke-width="7"/><circle cx="50" cy="30" r="34" fill="#b8500e" stroke="#140e0a" stroke-width="5"/><path d="M-90,-40H60" stroke="#ffd0a8" stroke-width="12" opacity=".7" stroke-linecap="round"/>
          <circle cx="-160" cy="-60" r="18" fill="none" stroke="#9aa0a4" stroke-width="7"/></g>
        <g transform="translate(540,900) rotate(4)"><path d="M0,-170V-60" stroke="#c8b08a" stroke-width="5"/><g filter="url(#quDrop)"><path d="M-230,-60H230V210H-230Z" fill="url(#quTag)" stroke="#8a7a5a" stroke-width="4"/><circle cy="-30" r="14" fill="#120e0c"/>
          <text y="60" text-anchor="middle" font-family="Mali" font-weight="700" font-size="54" fill="#8a6a3a">${o.l1 || "ตอนที่ 2"}</text>
          <text y="150" text-anchor="middle" font-family="Mali" font-weight="700" font-size="76" fill="#c8281e">${o.l2 || "ลงบันได"}</text></g></g></g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: 7, svgOrigin: "540 -20" }, { rotation: -4, svgOrigin: "540 -20", duration: 1.1, ease: "elastic.out(1, 0.4)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: -4, svgOrigin: "540 -20" }, { rotation: 2, svgOrigin: "540 -20", duration: 1.4, repeat: 3, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 1.1);
  }

  window.QkUI = { title, app, eta, choice, rewind, note, labels, seismo, quakeMap, call, endCard, ICON, icon, iconLife, RULES, mmss };
})();
