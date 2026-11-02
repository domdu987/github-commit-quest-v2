// "รูพญานาค" cards and icons, all things from the story world (no UI boxes, no ticks or crosses):
//   RupUI.leaf(tl, layer, t0, dur, o)   ยาย's rules: a bound palm-leaf book (ใบลานผูก) between two carved naga-scale cover boards, hung
//                                       on its red string. Lines are incised (จาร): a rule not yet learnt is a pale groove, this
//                                       episode's rule gets soot rubbed in as it plays (left to right, candle light passing), rules
//                                       already learnt are black with a red-white wrist thread (ด้ายผูกแขน) tied through their leaf.
//                                       o.active · o.done [..] · o.y · o.sign (the tiny "ส." initial at the end of leaf 3, EP.1 clue)
//   RupUI.lotto(tl, layer, t0, dur, o)  the opening card: the headman's hand-painted lucky-number board by the hole; the three
//                                       drums roll BACKWARD, then chalk writes o.text ("สามวันก่อน"). No real lottery logo.
//   RupUI.badge(x, y, kind, s)          a 2.5D coin icon with a naga-scale rim: "ring" (cracks in a ring) · "well" (muddy drop) ·
//                                       "far" (100 ม.) · "call" (1784). RupUI.badgeIn(tl, sel, t0) drops it in with overshoot + idle.
//   Rup.mural(L, o)                     the ฮูปแต้ม wall of the village sim: the naga coiled under the earth (coils and scales only,
//                                       one eye), villagers drilling a well above, the ground splitting in a ring. Isan folk palette.
(function () {
  const Rup = (window.Rup = window.Rup || {});
  const RupUI = (window.RupUI = window.RupUI || {});
  const f = (v) => (+v).toFixed(1);
  const LINE = "#2a1c16";
  const ln = (w = 3) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const rng = Rup.rng, mix = Rup.mix;

  Sets.DEFS += `
    <linearGradient id="ruLeaf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b88e52"/><stop offset=".08" stop-color="#d8b878"/><stop offset=".5" stop-color="#e2c88e"/><stop offset=".92" stop-color="#d0ae6c"/><stop offset="1" stop-color="#a8804a"/></linearGradient>
    <linearGradient id="ruLeafV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c8" stop-opacity=".35"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#6a4a20" stop-opacity=".28"/></linearGradient>
    <linearGradient id="ruWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a4a28"/><stop offset=".45" stop-color="#6a3418"/><stop offset="1" stop-color="#3e1c0c"/></linearGradient>
    <linearGradient id="ruGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9a0"/><stop offset=".5" stop-color="#e0a83a"/><stop offset="1" stop-color="#9a6418"/></linearGradient>
    <linearGradient id="ruBoard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c3a32"/><stop offset="1" stop-color="#1a2420"/></linearGradient>
    <linearGradient id="ruCandleBand" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd27a" stop-opacity="0"/><stop offset=".5" stop-color="#ffd27a" stop-opacity=".55"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>
    <linearGradient id="ruCoin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6e2a8"/><stop offset=".55" stop-color="#d8a84a"/><stop offset="1" stop-color="#8a5a1a"/></linearGradient>
    <linearGradient id="ruPlaster" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#efe4cc"/><stop offset="1" stop-color="#ddcca8"/></linearGradient>`;

  // naga scales: rows of overlapping arcs along a band from (x0,y) width w, scale size s
  const scales = (x0, y, w, rows, s, c, c2) => {
    let g = "";
    for (let r = 0; r < rows; r++) for (let k = 0; k < Math.ceil(w / s) + 1; k++) {
      const x = x0 + k * s + (r % 2) * s / 2, yy = y + r * s * 0.55;
      if (x > x0 + w) continue;
      g += `<path d="M${f(x - s / 2)},${f(yy)}q${f(s / 2)},${f(s * 0.75)} ${f(s)},0" fill="${r % 2 ? c2 : c}" stroke="${LINE}" stroke-width="1.6"/>`;
    }
    return g;
  };
  RupUI.scales = scales;

  // ---------------- the rules: ใบลานผูก ----------------
  RupUI.leaf = (tl, layer, t0, dur, o = {}) => {
    const id = `rul${Math.round(t0 * 100)}`, y = o.y ?? 760, done = o.done || [], act = o.active;
    const lines = o.lines || ["ดินแยกเป็นวง อย่าหลงเข้าใกล้", "น้ำบ่อขุ่นแดง แจ้งแล้วถอย", "รูยังกว้างได้ ไหว้ไกลร้อยเมตร"];
    const W = 920, H = 96;
    const cover = (yy, flip) => `<g transform="translate(0,${yy})">
      <path d="M${-W / 2 - 20},-34Q${-W / 2 - 34},0 ${-W / 2 - 20},34H${W / 2 + 20}Q${W / 2 + 34},0 ${W / 2 + 20},-34Z" fill="url(#ruWood)" ${ln(3.4)}/>
      <clipPath id="${id}-cc${flip}"><path d="M${-W / 2 - 10},-24H${W / 2 + 10}V24H${-W / 2 - 10}Z"/></clipPath>
      <g clip-path="url(#${id}-cc${flip})" opacity=".9">${scales(-W / 2 - 10, -26, W + 20, 4, 30, "url(#ruGold)", "#c88a2a")}</g>
      <path d="M${-W / 2 - 10},-24H${W / 2 + 10}M${-W / 2 - 10},24H${W / 2 + 10}" stroke="#ffe9a0" stroke-width="2" opacity=".7"/>
      <path d="M${-W / 2 - 18},${flip ? 30 : -30}H${W / 2 + 18}" stroke="#fff" stroke-width="3" opacity=".22"/></g>`;
    let g = `<g transform="translate(540,${y})"><g id="${id}">
      <path id="${id}-str" d="M-330,-360V-250M330,-360V-250" stroke="#c8302a" stroke-width="7"/>
      <path d="M-330,-250V${-128 + 3 * H - 22}M330,-250V${-128 + 3 * H - 22}" stroke="#a8241e" stroke-width="5"/>
      <g opacity=".3" transform="translate(14,22)"><rect x="${-W / 2 - 30}" y="-250" width="${W + 60}" height="${3 * H + 160}" rx="30" fill="#000" filter="url(#rpBlur16)"/></g>
      ${cover(-214, 0)}`;
    lines.forEach((t, k) => {
      const yy = -128 + k * H, st = done.includes(k) ? "done" : k === act ? "on" : "off", tilt = [-0.8, 0.6, -0.4][k], dx = st === "on" ? 0 : [6, -8, 4][k];
      const lid = `${id}-lf${k}`;
      g += `<g id="${lid}" transform="translate(${dx},${yy}) rotate(${tilt})">
        <path d="M${-W / 2 + 6},-40L${-W / 2 + 60},-44L${-W / 4},-42L0,-44L${W / 4},-41L${W / 2 - 50},-43L${W / 2 - 4},-38Q${W / 2 + 6},0 ${W / 2 - 4},38L${W / 4},41L0,40L${-W / 4},42L${-W / 2 + 40},41L${-W / 2 + 4},38Q${-W / 2 - 6},0 ${-W / 2 + 6},-40Z" fill="url(#ruLeaf)" ${ln(2.2)}/>
        <path d="M${-W / 2 + 6},-40L${W / 2 - 4},-38L${W / 2 - 4},38L${-W / 2 + 4},38Z" fill="url(#ruLeafV)"/>
        ${Array.from({ length: 16 }, (_, j) => `<path d="M${-W / 2 + 10 + (j * 37) % 30},${-36 + j * 4.6}L${W / 2 - 12 - (j * 23) % 40},${-36 + j * 4.6 + (j % 3 - 1) * 0.8}" stroke="${j % 4 ? "#b89458" : "#9a7440"}" stroke-width="${j % 4 ? 0.9 : 1.6}" opacity="${j % 4 ? 0.45 : 0.6}"/>`).join("")}
        ${Array.from({ length: 6 }, (_, j) => `<ellipse cx="${-380 + j * 150 + (j % 2) * 40}" cy="${-20 + (j * 17) % 40}" rx="${6 + j % 3 * 3}" ry="3" fill="#8a6430" opacity=".25"/>`).join("")}
        <circle cx="-330" cy="0" r="8" fill="#3a2410" stroke="#8a6430" stroke-width="2"/><circle cx="330" cy="0" r="8" fill="#3a2410" stroke="#8a6430" stroke-width="2"/>
        <text x="-298" y="16" font-family="Kanit" font-weight="700" font-size="42" fill="none" stroke="#8a6434" stroke-width="1.6" opacity=".9">${t}</text>
        <text x="-300" y="14" font-family="Kanit" font-weight="700" font-size="42" fill="#f6e6c0" opacity=".35">${t}</text>`;
      if (st !== "off") {
        g += `<clipPath id="${lid}-sc"><rect id="${lid}-sr" x="-310" y="-40" width="${st === "on" ? 0 : 640}" height="80"/></clipPath>
          <text x="-300" y="14" font-family="Kanit" font-weight="700" font-size="42" fill="#17100a" stroke="#17100a" stroke-width=".8" clip-path="url(#${lid}-sc)">${t}</text>`;
        if (st === "on") g += `<rect id="${lid}-band" x="-560" y="-52" width="260" height="104" fill="url(#ruCandleBand)" style="mix-blend-mode:screen"/>
          <g id="${lid}-sm" opacity="0"><ellipse cx="0" cy="0" rx="22" ry="12" fill="#2a1a10" opacity=".55"/><ellipse cx="-4" cy="-3" rx="10" ry="5" fill="#4a3a2a" opacity=".6"/></g>`;
      }
      if (st === "done") g += `<g transform="translate(372,-6)"><path d="M0,0q18,26 6,62M0,0q-12,30 -2,60" stroke="#d8302a" stroke-width="5" fill="none"/>
          <path d="M0,0q14,28 2,61" stroke="#f6f2ea" stroke-width="2.4" fill="none" stroke-dasharray="6 5"/><circle r="9" fill="#d8302a" ${ln(2)}/></g>`;
      if (k === 2 && o.sign) g += `<text x="${W / 2 - 46}" y="38" font-family="Kanit" font-weight="600" font-size="24" fill="#3a2414" opacity=".7">ส.</text>`;
      g += `</g>`;
    });
    g += `${cover(-128 + 3 * H - 22, 1)}
      <path d="M-330,${-128 + 3 * H}q-20,60 -60,110M-330,${-128 + 3 * H}q10,70 -10,120" stroke="#c8302a" stroke-width="6" fill="none"/>`;
    for (let k = 0; k < 10; k++) g += `<circle class="${id}-dust" cx="${f(-420 + k * 92)}" cy="${f(-260 + (k * 47) % 420)}" r="${2 + (k % 3)}" fill="#ffe6b0" opacity=".5"/>`;
    put(layer, g + `</g></g>`);
    const el = document.getElementById(id);
    tl.set(el, { opacity: 0 }, 0);
    // drop in on the string, overshoot, settle, then sway like a hung bundle
    tl.fromTo(el, { opacity: 0, y: -260, rotation: -5, svgOrigin: "540 " + (y - 360) }, { opacity: 1, y: 0, rotation: 0, svgOrigin: "540 " + (y - 360), duration: 0.6, ease: "back.out(1.9)", immediateRender: false }, t0);
    tl.fromTo(el, { rotation: -0.9, svgOrigin: "540 " + (y - 360) }, { rotation: 0.9, svgOrigin: "540 " + (y - 360), duration: 1.6, yoyo: true, repeat: Math.ceil(dur / 1.6), ease: "sine.inOut", immediateRender: false }, t0 + 0.6);
    if (act != null) {
      const lid = `${id}-lf${act}`, yy = -128 + act * H;
      // the leaf slides out of the bundle a little, soot is rubbed in left to right with the candle light passing over
      tl.fromTo(`#${lid}`, { attr: { transform: `translate(0,${yy}) rotate(0)` } }, { attr: { transform: `translate(26,${yy}) rotate(-1.2)` }, duration: 0.45, ease: "back.out(2.4)", immediateRender: false }, t0 + 0.55);
      const rub = Math.min(1.3, dur - 1.2);
      tl.fromTo(`#${lid}-sr`, { attr: { width: 0 } }, { attr: { width: 640 }, duration: rub, ease: "power1.inOut", immediateRender: false }, t0 + 0.75);
      tl.fromTo(`#${lid}-sm`, { opacity: 0, x: -300 }, { opacity: 1, x: 330, duration: rub, ease: "power1.inOut", immediateRender: false }, t0 + 0.75);
      tl.to(`#${lid}-sm`, { opacity: 0, duration: 0.2, immediateRender: false }, t0 + 0.75 + rub);
      tl.fromTo(`#${lid}-band`, { x: 0 }, { x: 1120, duration: rub + 0.4, ease: "sine.inOut", immediateRender: false }, t0 + 0.65);
    }
    tl.fromTo(`.${id}-dust`, { y: 0, opacity: 0.1 }, { y: -40, opacity: 0.6, duration: 2.2, stagger: { each: 0.18, repeat: Math.ceil(dur / 2.2), yoyo: true }, ease: "sine.inOut", immediateRender: false }, t0);
    tl.to(el, { opacity: 0, y: -40, duration: 0.3, ease: "power2.in", immediateRender: false }, t0 + dur - 0.3);
  };

  // ---------------- the opening card: the lucky-number board rolls backward ----------------
  RupUI.lotto = (tl, layer, t0, dur, o = {}) => {
    const id = `rlo${Math.round(t0 * 100)}`, nums = o.nums || [9, 2, 7], text = o.text || "สามวันก่อน", y = o.y ?? 900;
    const col = (d) => Array.from({ length: 12 }, (_, k) => `<text x="0" y="${f(54 - k * 150)}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="150" fill="#f6efe0">${(d + k) % 10}</text>`).join("");
    let g = `<g transform="translate(540,${y})"><g id="${id}">
      <path d="M-300,240L-330,640M300,240L330,640" stroke="#5a3418" stroke-width="26" stroke-linecap="round"/>
      <path d="M-300,240L-330,640M300,240L330,640" stroke="#8a5a32" stroke-width="10" stroke-linecap="round" opacity=".6"/>
      <ellipse cx="0" cy="650" rx="420" ry="34" fill="#000" opacity=".35"/>
      <rect x="-420" y="-380" width="840" height="640" rx="20" fill="url(#ruWood)" ${ln(4)}/>
      <clipPath id="${id}-fc"><rect x="-410" y="-372" width="820" height="66"/></clipPath>
      <g clip-path="url(#${id}-fc)">${scales(-410, -380, 820, 3, 34, "url(#ruGold)", "#c88a2a")}</g>
      <path d="M-420,-300H420" stroke="#2a1408" stroke-width="4"/>
      <rect x="-380" y="-284" width="760" height="510" rx="8" fill="url(#ruBoard)" ${ln(3)}/>
      ${Array.from({ length: 18 }, (_, k) => `<path d="M${-360 + (k * 97) % 700},${-260 + (k * 61) % 460}q${30 + k % 4 * 10},${-6 + k % 3 * 4} ${60 + k % 5 * 12},${2}" stroke="#f6efe0" stroke-width="3" opacity=".07" fill="none"/>`).join("")}
      <text x="0" y="-206" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="62" fill="#ffd84a" stroke="#2a1408" stroke-width="2">เลขเด็ดรูพญานาค</text>
      <path d="M-260,-186Q0,-174 260,-186" stroke="#ffd84a" stroke-width="3" fill="none" opacity=".6"/>`;
    nums.forEach((d, k) => {
      const x = -230 + k * 230;
      g += `<g transform="translate(${x},-40)"><rect x="-90" y="-100" width="180" height="200" rx="16" fill="#0e0a08" ${ln(3)}/>
        <clipPath id="${id}-dc${k}"><rect x="-84" y="-94" width="168" height="188" rx="12"/></clipPath>
        <g clip-path="url(#${id}-dc${k})"><g id="${id}-d${k}">${col(d)}</g>
          <rect x="-84" y="-94" width="168" height="40" fill="#000" opacity=".45"/><rect x="-84" y="54" width="168" height="40" fill="#000" opacity=".45"/></g>
        <path d="M-86,0H86" stroke="#000" stroke-width="3" opacity=".6"/><path d="M-80,-88H80" stroke="#fff" stroke-width="3" opacity=".18"/></g>`;
    });
    g += `<clipPath id="${id}-tc"><rect id="${id}-tr" x="-330" y="80" width="0" height="130"/></clipPath>
      <text x="0" y="176" text-anchor="middle" font-family="Mali, Kanit" font-weight="700" font-size="92" fill="#f6efe0" opacity=".92" clip-path="url(#${id}-tc)" style="filter:url(#rpBlur3) opacity(0)">${text}</text>
      <text x="0" y="176" text-anchor="middle" font-family="Mali, Kanit" font-weight="700" font-size="92" fill="#f6efe0" clip-path="url(#${id}-tc)">${text}</text>
      <g id="${id}-chalk" opacity="0"><rect x="-10" y="-30" width="20" height="58" rx="5" fill="#fbf6ea" ${ln(2)} transform="rotate(30)"/></g>
      <g transform="translate(360,240)"><rect x="-26" y="0" width="52" height="70" fill="#c8c4b8" ${ln(2.4)}/>${[-12, 0, 12].map((x, k) => `<path d="M${x},0L${x + (k - 1) * 6},-120" stroke="#a83a2a" stroke-width="3"/><circle class="${id}-ember" cx="${x + (k - 1) * 6}" cy="-120" r="4" fill="#ff7a2a"/>`).join("")}</g>
      <g transform="translate(-372,236)"><path d="M0,0q-30,-50 0,-90q30,40 0,90Z" fill="#f0a020" ${ln(2)}/><path d="M0,0q-16,-36 0,-66q16,30 0,66Z" fill="#f6d040"/></g>`;
    put(layer, g + `</g></g>`);
    const el = document.getElementById(id);
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0, scale: 0.9, svgOrigin: `540 ${y + 650}` }, { opacity: 1, scale: 1, svgOrigin: `540 ${y + 650}`, duration: 0.4, ease: "back.out(2)", immediateRender: false }, t0);
    // drums roll backward (the column moves DOWN: higher digits come in from above → counting down), staggered, each lands with a bounce
    nums.forEach((d, k) => tl.fromTo(`#${id}-d${k}`, { y: 0 }, { y: 150 * 10, duration: 1.1 + k * 0.18, ease: "back.out(1.1)", immediateRender: false }, t0 + 0.2 + k * 0.08));
    const tw = 0.9, ts = t0 + 0.5 + Math.min(1.4, dur * 0.35);
    tl.fromTo(`#${id}-tr`, { attr: { width: 0 } }, { attr: { width: 660 }, duration: tw, ease: "power1.inOut", immediateRender: false }, ts);
    tl.fromTo(`#${id}-chalk`, { opacity: 1, x: -320, y: 150 }, { x: 330, y: 150, duration: tw, ease: "power1.inOut", immediateRender: false }, ts);
    tl.fromTo(`#${id}-chalk`, { rotation: -6, transformOrigin: "50% 50%" }, { rotation: 6, transformOrigin: "50% 50%", duration: 0.09, yoyo: true, repeat: Math.ceil(tw / 0.09), ease: "sine.inOut", immediateRender: false }, ts);
    tl.to(`#${id}-chalk`, { opacity: 0, duration: 0.2, immediateRender: false }, ts + tw);
    tl.fromTo(`.${id}-ember`, { opacity: 0.5 }, { opacity: 1, duration: 0.3, stagger: { each: 0.1, repeat: Math.ceil(dur / 0.3), yoyo: true }, ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(el, { rotation: -0.4, svgOrigin: `540 ${y + 650}` }, { rotation: 0.4, svgOrigin: `540 ${y + 650}`, duration: 1.2, yoyo: true, repeat: Math.ceil(dur / 1.2), ease: "sine.inOut", immediateRender: false }, t0 + 0.4);
    tl.to(el, { opacity: 0, duration: 0.25, immediateRender: false }, t0 + dur - 0.25);
  };

  // ---------------- 2.5D coin icons with a naga-scale rim ----------------
  const glyph = {
    ring: `<ellipse cx="0" cy="8" rx="46" ry="20" fill="#1a0c06"/>${[0, 1, 2, 3, 4].map((k) => { const a = k * 1.26; return `<path d="M${f(Math.cos(a) * 60)},${f(8 + Math.sin(a) * 28)}l${f(Math.cos(a) * 14)},${f(Math.sin(a) * 6 - 4)}l${f(Math.cos(a) * 8 + 4)},${f(Math.sin(a) * 5 + 3)}" stroke="#3a2414" stroke-width="5" fill="none" stroke-linecap="round"/>`; }).join("")}`,
    well: `<path d="M0,-50Q34,-6 34,18A34,34 0 0 1 -34,18Q-34,-6 0,-50Z" fill="#a8582a" ${ln(3.4)}/><path d="M-14,4q-4,16 10,24" stroke="#ffd2a0" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/>`,
    far: `<text x="0" y="18" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#3a1c0c">100</text><text x="0" y="50" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="24" fill="#3a1c0c">เมตร</text>`,
    call: `<text x="0" y="22" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="52" fill="#3a1c0c">1784</text>`,
  };
  RupUI.badge = (x, y, kind, s = 1, bid = "") => {
    const R = 96;
    let rim = "";
    for (let k = 0; k < 28; k++) { const a = (k / 28) * Math.PI * 2, ax = Math.cos(a) * (R - 10), ay = Math.sin(a) * (R - 10);
      rim += `<path d="M${f(ax)},${f(ay)}m-9,0q9,15 18,0q-9,-6 -18,0Z" fill="${k % 2 ? "#c88a2a" : "#ffe08a"}" stroke="${LINE}" stroke-width="1.4" transform="rotate(${f(a * 180 / Math.PI + 90)} ${f(ax)} ${f(ay)})"/>`; }
    return `<g id="${bid}" transform="translate(${x},${y}) scale(${s})"><g class="rub">
      <ellipse cx="6" cy="${R + 26}" rx="${R * 0.9}" ry="16" fill="#000" opacity=".35" filter="url(#rpBlur8)"/>
      <circle cx="0" cy="14" r="${R}" fill="#6a3a12" ${ln(4)}/>
      <circle r="${R}" fill="url(#ruCoin)" ${ln(4)}/>${rim}
      <circle r="${R - 24}" fill="#f2e2b4" ${ln(3)}/><circle r="${R - 30}" fill="none" stroke="#c89a4a" stroke-width="3"/>
      ${glyph[kind] || ""}
      <path d="M${-R + 26},-30A${R - 24},${R - 24} 0 0 1 -20,${-R + 26}" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".5"/>
      <path class="glint" d="M30,-60l6,-16l6,16l16,6l-16,6l-6,16l-6,-16l-16,-6Z" fill="#fff" opacity="0"/></g></g>`;
  };
  RupUI.badgeIn = (tl, sel, t0, dur = 3) => {
    tl.fromTo(`${sel} .rub`, { scale: 0, rotation: -40, transformOrigin: "50% 50%" }, { scale: 1, rotation: 0, transformOrigin: "50% 50%", duration: 0.55, ease: "back.out(2.6)", immediateRender: false }, t0);
    tl.fromTo(`${sel} .rub`, { y: 0 }, { y: -8, duration: 0.9, yoyo: true, repeat: Math.ceil(dur / 0.9), ease: "sine.inOut", immediateRender: false }, t0 + 0.55);
    tl.fromTo(`${sel} .glint`, { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1.2, transformOrigin: "50% 50%", duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, t0 + 0.6);
  };


  // ---------------- the choice: chalked on the lucky-number board, a chalk circle pulled toward option a ----------------
  RupUI.choice = (tl, layer, t0, dur, o = {}) => {
    const id = `rch${Math.round(t0 * 100)}`, a = o.a || "นอนต่อจนเช้า", b = o.b || "พายายออกไปตอนนี้";
    let g = `<g transform="translate(540,900)"><g id="${id}"><rect x="-470" y="-330" width="940" height="560" rx="20" fill="url(#ruWood)" ${ln(4)}/>
      <clipPath id="${id}-fc"><rect x="-460" y="-322" width="920" height="54"/></clipPath><g clip-path="url(#${id}-fc)">${scales(-460, -330, 920, 3, 34, "url(#ruGold)", "#c88a2a")}</g>
      <rect x="-430" y="-250" width="860" height="440" rx="8" fill="url(#ruBoard)" ${ln(3)}/>
      <text x="0" y="-180" text-anchor="middle" font-family="Mali, Kanit" font-weight="700" font-size="54" fill="#ffd84a">ถ้าเป็นคุณ…</text>
      <g id="${id}-a"><text x="0" y="-60" text-anchor="middle" font-family="Mali, Kanit" font-weight="700" font-size="64" fill="#f6efe0">${a}</text></g>
      <text x="0" y="20" text-anchor="middle" font-family="Mali, Kanit" font-weight="700" font-size="40" fill="#f6efe0" opacity=".6">หรือ</text>
      <g id="${id}-b"><text x="0" y="110" text-anchor="middle" font-family="Mali, Kanit" font-weight="700" font-size="64" fill="#f6efe0">${b}</text></g>
      <ellipse id="${id}-ring" cx="0" cy="-80" rx="340" ry="62" fill="none" stroke="#ff6a4a" stroke-width="7" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="100" transform="rotate(-2)"/></g></g>`;
    put(layer, g);
    const el = document.getElementById(id);
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0, y: 60, scale: 0.92, transformOrigin: "50% 50%" }, { opacity: 1, y: 0, scale: 1, transformOrigin: "50% 50%", duration: 0.5, ease: "back.out(1.8)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-a`, { x: -30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power2.out", immediateRender: false }, t0 + 0.35);
    tl.fromTo(`#${id}-b`, { x: 30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power2.out", immediateRender: false }, t0 + 0.6);
    // the chalk circle hovers over b, then gets pulled up round a (the wrong pull)
    tl.fromTo(`#${id}-ring`, { attr: { "stroke-dashoffset": 100 }, y: 190 }, { attr: { "stroke-dashoffset": 0 }, y: 190, duration: 0.5, ease: "power1.inOut", immediateRender: false }, t0 + 1.1);
    tl.to(`#${id}-ring`, { y: 0, duration: 0.7, ease: "back.inOut(2)", immediateRender: false }, t0 + 1.9);
    tl.to(`#${id}-a`, { scale: 1.08, transformOrigin: "50% 50%", duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }, t0 + 2.6);
    tl.to(el, { opacity: 0, duration: 0.2, immediateRender: false }, t0 + dur - 0.2);
  };
  // ---------------- the end card: the headman's sign with a paper note ----------------
  RupUI.endCard = (tl, layer, t0, dur, o = {}) => {
    const id = `ren${Math.round(t0 * 100)}`;
    put(layer, `<rect id="${id}-bg" x="-100" y="-100" width="1300" height="2200" fill="#0c0a10" opacity=".5"/>
      <g transform="translate(540,1080)"><g id="${id}"><path d="M-14,0V-300M14,0V-300" stroke="#4a2c1a" stroke-width="22"/>
      <rect x="-330" y="-760" width="660" height="440" rx="16" fill="#e8d2a8" ${ln(5)}/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M-324,${-736 + k * 72}h648" stroke="#c8ae7a" stroke-width="3"/>`).join("")}
      <text x="0" y="-600" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="130" fill="#b8241e" transform="rotate(-2 0 -600)">รูพญานาค</text>
      <path d="M-240,-560q80,-14 160,0t160,0t160,0" stroke="#2a6a4a" stroke-width="12" fill="none" stroke-linecap="round"/>
      <g id="${id}-note" transform="translate(40,-420) rotate(4)"><rect x="-250" y="-70" width="500" height="150" fill="#fbf6ea" ${ln(3)}/><rect x="-60" y="-86" width="120" height="30" fill="#f0d878" opacity=".85"/>
        <text x="0" y="-6" text-anchor="middle" font-family="Mali, Kanit" font-weight="700" font-size="50" fill="#2a1c16">${o.ep || "ตอนที่ 2"}</text>
        <text x="0" y="56" text-anchor="middle" font-family="Mali, Kanit" font-weight="700" font-size="46" fill="#b8241e">${o.title || "น้ำบ่อขุ่นแดง"}</text></g></g></g>`);
    tl.set([`#${id}`, `#${id}-bg`], { opacity: 0 }, 0);
    tl.set(`#${id}-bg`, { opacity: 0.5 }, t0);
    tl.fromTo(`#${id}`, { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.8)", immediateRender: false }, t0 + 0.05);
    tl.fromTo(`#${id}-note`, { rotation: 4, transformOrigin: "50% 0%" }, { rotation: -3, transformOrigin: "50% 0%", duration: 0.9, yoyo: true, repeat: Math.ceil(dur / 0.9), ease: "sine.inOut", immediateRender: false }, t0 + 0.4);
  };
  // ---------------- the ฮูปแต้ม mural ----------------
  Rup.mural = (L, o = {}) => {
    const id = o.id || "rmu", r = rng(311);
    const ink = "#3a2a24", och = "#c06a32", ind = "#2e4a7a", grn = "#5a8a4a", red = "#b8402a";
    let g = `<rect x="-600" y="-200" width="2300" height="2400" fill="url(#ruPlaster)"/>`;
    for (let k = 0; k < 90; k++) g += `<ellipse cx="${f(-500 + r() * 2100)}" cy="${f(-100 + r() * 2200)}" rx="${f(10 + r() * 60)}" ry="${f(6 + r() * 30)}" fill="${r() > 0.5 ? "#d6c49c" : "#f4ead4"}" opacity=".4"/>`;
    // sky band, the village above ground: a well drill frame with two villagers, rice, a sim roof
    g += `<path d="M-600,420Q540,380 1700,430" stroke="${ink}" stroke-width="5" fill="none"/>`;
    for (let k = 0; k < 26; k++) { const x = -300 + k * 68; g += `<path d="M${x},420q-6,-50 4,-80M${x},420q10,-44 22,-66" stroke="${grn}" stroke-width="4" fill="none"/>`; }
    const folk = (x, y, s, c, pose) => `<g transform="translate(${x},${y}) scale(${s})"><circle cx="0" cy="-150" r="20" fill="#e8b88a" stroke="${ink}" stroke-width="3"/>
      <path d="M-18,-160q18,-22 36,0" fill="${ink}"/><path d="M-22,-128L22,-128L16,-60L-16,-60Z" fill="${c}" stroke="${ink}" stroke-width="3"/>
      <path d="M-16,-60L-24,0M16,-60L26,0" stroke="${ink}" stroke-width="7" stroke-linecap="round"/><path d="M-22,-60H22V-30H-22Z" fill="${red}" stroke="${ink}" stroke-width="2.6"/>
      <path d="${pose}" stroke="${ink}" stroke-width="6" fill="none" stroke-linecap="round"/></g>`;
    g += `<path d="M380,410L470,150L560,410M470,150V560" stroke="#8a5a32" stroke-width="12" fill="none"/><path d="M470,150V600" stroke="${ink}" stroke-width="6"/>`;
    g += folk(340, 410, 1.1, och, "M-20,-118L20,-170L56,-200") + folk(610, 410, 1.1, ind, "M20,-118L-30,-170L-80,-196");
    g += `<path d="M900,300L1020,220L1140,300Z" fill="${red}" stroke="${ink}" stroke-width="4"/><rect x="930" y="300" width="180" height="110" fill="#e8d8b0" stroke="${ink}" stroke-width="4"/>`;
    // the earth: bands, and the naga coiled in it — only coils, scales and one eye (barely shown)
    g += `<rect x="-600" y="430" width="2300" height="1500" fill="#b07a4a" opacity=".35"/>`;
    for (let k = 0; k < 6; k++) g += `<path d="M-600,${560 + k * 220}Q540,${520 + k * 220 + (k % 2 ? 30 : -30)} 1700,${570 + k * 220}" stroke="${ink}" stroke-width="2.4" fill="none" opacity=".5"/>`;
    const coil = (cx, cy, rx, ry) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${ink}" stroke-width="66"/><ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${grn}" stroke-width="56"/>
      <ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="#9ac87a" stroke-width="56" stroke-dasharray="14 18" opacity=".55"/><ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${ink}" stroke-width="3" stroke-dasharray="2 30"/>`;
    // the naga's body dives in and out of the soil bands (dash gaps = under the earth): only humps, scales, one eye
    const body = "M-120,1640C80,1560 160,1380 340,1440S560,1620 700,1460S760,1180 560,1150S300,1080 420,960S760,900 820,860";
    const cream = "#f2e6c8";
    const seg = (w, c, extra = "") => `<path d="${body}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-dasharray="330 140 420 120 380 110 2000" ${extra}/>`;
    // folk-mural naga: ink outline, indigo back, a cream belly line, scales as rows of cream crescents, red-earth fins along the spine
    g += `<mask id="${id}-nm" maskUnits="userSpaceOnUse" x="-600" y="-200" width="2300" height="2400"><path d="${body}" fill="none" stroke="#fff" stroke-width="90" stroke-linecap="butt" stroke-dasharray="330 140 420 120 380 110 2000"/><rect x="700" y="700" width="400" height="300" fill="#fff"/></mask>
      <g id="${id}-naga"><g mask="url(#${id}-nm)">${seg(76, ink)}${seg(64, ind)}${seg(22, cream, 'transform="translate(0,14)"')}${seg(6, och, 'transform="translate(0,14)"')}
      ${seg(40, "none", 'stroke="' + cream + '" style="stroke-dasharray:5 13" opacity=".85"')}
      ${seg(8, ink, 'transform="translate(0,-30)" style="stroke-dasharray:18 22" opacity=".9"')}
      ${seg(14, red, 'transform="translate(0,-36)" style="stroke-dasharray:14 26"')}
      </g><path d="M150,1500q60,-30 120,0M500,1580q60,-30 120,0M540,1130q60,-30 120,0" stroke="${ink}" stroke-width="3" fill="none" opacity=".5"/>
      <g transform="translate(830,850) rotate(-14) scale(.95)">
        ${[0, 1, 2, 3].map((k) => `<path d="M${-40 + k * 22},-40c-10,-30 4,-60 26,-70c-10,18 -4,30 8,34c4,-16 14,-26 28,-28c-14,22 -10,44 -22,64Z" fill="${red}" stroke="${ink}" stroke-width="3"/>`).join("")}
        <path d="M-50,26Q-40,-58 34,-54Q96,-36 84,24Q70,40 40,34L-50,26Z" fill="${ind}" stroke="${ink}" stroke-width="5"/>
        <path d="M-40,6Q10,-10 70,4" stroke="${cream}" stroke-width="5" fill="none"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M${-36 + k * 18},-24q6,8 12,0" stroke="${cream}" stroke-width="3" fill="none"/>`).join("")}
        <path d="M40,34Q74,46 96,30L84,24Z" fill="${red}" stroke="${ink}" stroke-width="3"/><path d="M60,36l4,14l4,-12M76,34l3,12l4,-12" fill="#fff" stroke="${ink}" stroke-width="2"/>
        <path d="M84,22q26,-2 40,-14" stroke="${ink}" stroke-width="3" fill="none"/>
        <ellipse id="${id}-eye" cx="44" cy="-12" rx="12" ry="9" fill="#f0d860" stroke="${ink}" stroke-width="3"/><ellipse cx="46" cy="-12" rx="3" ry="8" fill="${ink}"/></g></g>`;
    // folk frieze top and bottom (naga scales, lotus band), incense offerings kneeling at the drill site
    g += `<rect x="-600" y="-200" width="2300" height="300" fill="${red}" opacity=".85"/>` + RupUI.scales(-600, 80, 2300, 2, 40, "#e8c060", och) + `<path d="M-600,80H1700M-600,130H1700" stroke="${ink}" stroke-width="4"/>`;
    g += `<rect x="-600" y="1760" width="2300" height="400" fill="${ind}" opacity=".85"/>` + Array.from({ length: 30 }, (_, k) => `<path d="M${-560 + k * 80},1800q40,-50 80,0q-40,24 -80,0Z" fill="#e8dcc0" stroke="${ink}" stroke-width="3"/>`).join("");
    for (let k = 0; k < 3; k++) g += `<g transform="translate(${-80 + k * 120 + (k > 1 ? 800 : 0)},410)"><path d="M-20,0q0,-60 20,-80q20,20 20,80Z" fill="${k % 2 ? ind : och}" stroke="${ink}" stroke-width="3"/><circle cx="0" cy="-96" r="16" fill="#e8b88a" stroke="${ink}" stroke-width="3"/><path d="M14,-60l30,-40" stroke="${ink}" stroke-width="5"/><path d="M44,-100l4,-30" stroke="${red}" stroke-width="3"/></g>`;
    // the ground above splitting in a ring where they drill
    g += `<path id="${id}-split" d="M300,430Q470,470 640,430" stroke="${ink}" stroke-width="8" fill="none" stroke-dasharray="20 10" pathLength="100"/>`;
    // the wall's age: cracks in the plaster, a water stain
    g += `<path d="M1300,-100l-40,200l30,120l-50,180" stroke="#9a8a6a" stroke-width="3" fill="none"/><path d="M-300,1500q200,-60 380,30q160,80 380,-20" fill="#a8946a" opacity=".2"/>`;
    put(L.set, g);
  };
  Sets.rupMural = (L, o = {}) => Rup.mural(L, o);
  Rup.muralLife = (tl, id, t0, dur) => {
    tl.fromTo(`#${id}-naga`, { x: -10 }, { x: 10, duration: 2.4, yoyo: true, repeat: Math.ceil(dur / 2.4), ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-eye`, { opacity: 0.2 }, { opacity: 1, duration: 0.6, yoyo: true, repeat: Math.ceil(dur / 0.6), ease: "sine.inOut", immediateRender: false }, t0);
  };
})();
