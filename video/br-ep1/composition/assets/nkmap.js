// นิวเคลียร์ลงกรุงเทพ v4 · the maps and the car drawn as part of the world, not stickers: flat shapes in the episode's muted palette,
// soft shadows thrown away from the blast, thin UI on top (dashed routes, leader lines, small cream labels), and motion that belongs
// to the place (the jam crawling, tail lights pouring out of the city, fallout drifting straight through the car).
//   NkM.drone(tl, layer, t0, dur, o)   s05: the expressway and the concrete tower from a drone; the route from Keng's car to the car park
//   NkM.night(tl, layer, t0, dur, o)   s09: the city at night from high up; every road out clogs with tail lights, Keng stuck in one
//   NkM.carCut(tl, layer, t0, dur, o)  s10: the family's car side on; fallout drifts through glass and thin steel and reaches them
// All tweens sit on the shot clock (tl, absolute seconds) so any frame can be seeked.
(function () {
  const f1 = (v) => (+v).toFixed(1), put = (el, h) => el.insertAdjacentHTML("beforeend", h);
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  let seq = 0;
  const nid = (p) => `${p}${seq++}`;
  const INK = "#2e2a26", CREAM = "#f4ecd8";
  // a small cream label on a thin leader: tip (x, y) → label centred at (lx, ly)
  const tag = (id, x, y, lx, ly, txt, o = {}) => { const size = o.size ?? 36, w = o.w ?? 44 + txt.length * size * 0.56;
    return `<g id="${id}"><path id="${id}-l" d="M${f1(x)},${f1(y)}L${f1(lx)},${f1(ly)}" stroke="${o.line || CREAM}" stroke-width="3" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
      <circle id="${id}-d" cx="${f1(x)}" cy="${f1(y)}" r="8" fill="${o.line || CREAM}" stroke="${INK}" stroke-width="3"/>
      <g transform="translate(${f1(lx)},${f1(ly)})"><g id="${id}-p"><rect x="${f1(-w / 2)}" y="-27" width="${f1(w)}" height="54" rx="27" fill="${o.fill || CREAM}" stroke="${INK}" stroke-width="3"/>
      <text y="13" font-family="Kanit" font-weight="800" font-size="${size}" fill="${o.ink || INK}" text-anchor="middle">${txt}</text></g></g></g>`; };
  const tagIn = (tl, id, at, x, y) => {
    tl.fromTo(`#${id}-d`, { scale: 0, svgOrigin: `${f1(x)} ${f1(y)}` }, { scale: 1, svgOrigin: `${f1(x)} ${f1(y)}`, duration: 0.25, ease: "back.out(3)" }, at);
    tl.to(`#${id}-l`, { attr: { "stroke-dashoffset": 0 }, duration: 0.28, ease: "power2.out" }, at + 0.05);
    tl.fromTo(`#${id}-p`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.4, ease: "back.out(2.4)" }, at + 0.2);
  };
  const hide = (tl, id, t0) => tl.set(`#${id}-p`, { scale: 0, svgOrigin: "0 0" }, t0);
  const loop = (tl, sel, from, to, period, t0, dur, yoyo = true, ease) => { if (dur <= 0.1) return; const n = Math.max(1, Math.round(dur / period));
    tl.fromTo(sel, from, { ...to, duration: yoyo ? period / 2 : period, repeat: yoyo ? n * 2 - 1 : n - 1, yoyo, ease: ease || (yoyo ? "sine.inOut" : "none"), immediateRender: false }, t0); };

  // ---------------- s05 · the drone: the jammed expressway, the concrete tower beside it, the way down to its car park ----------------
  function drone(tl, layer, t0, dur, o = {}) {
    const id = nid("nmd"), r = mk(41), AT = o.routeAt ?? 1.6;
    // the expressway: a band tilted 12°, centred on x 380 at y 960 (local: vertical, 340 wide)
    const X0 = 380, Y0 = 960, ANG = -12, W = 340;
    let g = `<defs><radialGradient id="${id}-glow" cx="1" cy="0" r="1.1"><stop offset="0" stop-color="#ffb070" stop-opacity=".75"/><stop offset=".45" stop-color="#ff8a4a" stop-opacity=".22"/><stop offset="1" stop-color="#ff8a4a" stop-opacity="0"/></radialGradient>
      <filter id="${id}-sh" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter>
      <radialGradient id="${id}-vig" cx=".5" cy=".46" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient></defs>`;
    // ground: streets and blocks
    let ground = `<rect x="-400" y="-400" width="1880" height="2720" fill="#3b3540"/>`;
    const blocks = [], trees = [];
    for (let by = -300; by < 2300; by += 290) for (let bx = -300; bx < 1400; bx += 260) {
      const x = bx + r() * 20, y = by + r() * 20, w = 210 + r() * 20, h = 240 + r() * 20;
      if (x + w > 600 && x < 1040 && y + h > 640 && y < 1260) continue;   // the tower's block
      ground += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h)}" rx="10" fill="#4a434c"/>`;
      // two to four buildings per block
      let cx = x + 14; while (cx < x + w - 50) { const bw = 60 + r() * 90, bh = 80 + r() * (h - 110), byy = y + 14 + r() * (h - bh - 28), hgt = 0.5 + r() * 1.6;
        blocks.push({ x: cx, y: byy, w: Math.min(bw, x + w - 14 - cx), h: bh, hgt, col: ["#8a8490", "#9a8f86", "#7a7482", "#a59a8c", "#6e6878"][Math.floor(r() * 5)] }); cx += bw + 12; }
      for (let k = 0; k < 3; k++) trees.push([x - 6 + r() * (w + 12), y - 8 + (r() < 0.5 ? 0 : h + 16), 14 + r() * 12]);
    }
    let shadows = "", roofs = "";
    blocks.forEach((b) => { const d = 22 * b.hgt;
      shadows += `<rect x="${f1(b.x - d)}" y="${f1(b.y + d)}" width="${f1(b.w)}" height="${f1(b.h)}" fill="#120e16" opacity=".55"/>`;
      roofs += `<rect x="${f1(b.x)}" y="${f1(b.y)}" width="${f1(b.w)}" height="${f1(b.h)}" fill="${b.col}"/><rect x="${f1(b.x + 6)}" y="${f1(b.y + 6)}" width="${f1(b.w - 12)}" height="${f1(b.h - 12)}" fill="#fff" opacity=".07"/>`;
      if (b.w > 70 && b.h > 70) roofs += `<rect x="${f1(b.x + b.w * 0.2)}" y="${f1(b.y + b.h * 0.25)}" width="18" height="14" fill="#5a5560"/><rect x="${f1(b.x + b.w * 0.55)}" y="${f1(b.y + b.h * 0.55)}" width="16" height="12" fill="#5a5560"/>`; });
    let tr = ""; trees.forEach(([x, y, rr]) => (tr += `<circle cx="${f1(x - 6)}" cy="${f1(y + 6)}" r="${f1(rr)}" fill="#120e16" opacity=".45"/><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(rr)}" fill="#55684f"/><circle cx="${f1(x + rr * 0.25)}" cy="${f1(y - rr * 0.25)}" r="${f1(rr * 0.55)}" fill="#6c8062"/>`));
    // the tower: concrete roof, parapet, core, tank, AC units; its long shadow; the ramp mouth on the street side with the P sign
    const TX = 640, TY = 700, TW = 380, TH = 470, TD = 90;
    const tower = `<rect x="${TX - TD}" y="${TY + TD}" width="${TW}" height="${TH}" fill="#120e16" opacity=".6" filter="url(#${id}-sh)"/>
      <g id="${id}-tw"><rect x="${TX}" y="${TY}" width="${TW}" height="${TH}" fill="#bdb6a9"/><rect x="${TX + 16}" y="${TY + 16}" width="${TW - 32}" height="${TH - 32}" fill="#aaa397"/>
      <rect x="${TX + 150}" y="${TY + 170}" width="90" height="120" fill="#968f84"/><rect x="${TX + 158}" y="${TY + 178}" width="74" height="104" fill="#a39c90"/>
      <circle cx="${TX + 300}" cy="${TY + 90}" r="38" fill="#8f897f"/><circle cx="${TX + 300}" cy="${TY + 90}" r="26" fill="#a39c90"/>
      ${[0, 1, 2, 3].map((k) => `<rect x="${TX + 50 + k * 34}" y="${TY + 360}" width="24" height="24" fill="#8a8479"/><circle cx="${TX + 62 + k * 34}" cy="${TY + 372}" r="7" fill="#6f695f"/>`).join("")}
      <path d="M${TX + 30},${TY + 60}h70M${TX + 30},${TY + 80}h70" stroke="#968f84" stroke-width="6"/></g>
      <rect x="${TX - 64}" y="${TY + 330}" width="64" height="96" fill="#1c1a20"/><path d="M${TX - 64},${TY + 330}h64M${TX - 64},${TY + 426}h64" stroke="#e8c03a" stroke-width="5" stroke-dasharray="10 8"/>
      <circle cx="${TX - 32}" cy="${TY + 300}" r="22" fill="#3f6fb6" stroke="${CREAM}" stroke-width="4"/><text x="${TX - 32}" y="${TY + 310}" font-family="Kanit" font-weight="900" font-size="28" fill="${CREAM}" text-anchor="middle">P</text>`;
    // the expressway, elevated: its shadow on the streets, deck, barriers, lanes and the jam (outbound lanes packed, brake lights on)
    let xw = `<g transform="rotate(${ANG} ${X0} ${Y0})"><rect x="${X0 - W / 2 - 60}" y="-700" width="${W}" height="3400" fill="#120e16" opacity=".55" filter="url(#${id}-sh)"/>
      <rect x="${X0 - W / 2}" y="-700" width="${W}" height="3400" fill="#5a5560"/><rect x="${X0 - W / 2}" y="-700" width="14" height="3400" fill="#8a8590"/><rect x="${X0 + W / 2 - 14}" y="-700" width="14" height="3400" fill="#8a8590"/>
      <rect x="${X0 - 8}" y="-700" width="16" height="3400" fill="#8a8590"/>`;
    for (const lx of [-110, -55, 55, 110]) xw += `<path d="M${X0 + lx},-700V2700" stroke="#d8d2c4" stroke-width="3" stroke-dasharray="26 30" opacity=".55"/>`;
    const CARC = ["#c9c4bc", "#8a3a34", "#3e4a5c", "#d8d2c8", "#5c6066", "#b8a46a", "#2e3238"];
    const car = (cx, cy, col, hi) => `<g transform="translate(${f1(cx)},${f1(cy)})"><rect x="-17" y="-32" width="34" height="64" rx="9" fill="${col}"${hi ? ` stroke="${CREAM}" stroke-width="3"` : ""}/>
      <rect x="-13" y="-20" width="26" height="15" rx="4" fill="#20242c" opacity=".85"/><rect x="-13" y="10" width="26" height="10" rx="3" fill="#20242c" opacity=".7"/>
      <circle cx="-11" cy="29" r="4" fill="#ff4a36"/><circle cx="11" cy="29" r="4" fill="#ff4a36"/></g>`;
    let lanes = "", glowL = "";
    const lanesX = [-137, -82, -27, 27, 82, 137], KX = X0 + 137, KY = 1020;
    lanesX.forEach((lx, li) => { const out = li >= 3; let cars = "", y = -680 + r() * 40;
      while (y < 2650) { if (li === 5 && Math.abs(y - KY) < 76) { y += 80; continue; }   // leave Keng's slot free
        cars += car(X0 + lx + (r() - 0.5) * 4, y, CARC[Math.floor(r() * CARC.length)], false);
        if (out) glowL += `<circle cx="${f1(X0 + lx - 11)}" cy="${f1(y + 29)}" r="12" fill="#ff4a36" opacity=".35"/><circle cx="${f1(X0 + lx + 11)}" cy="${f1(y + 29)}" r="12" fill="#ff4a36" opacity=".35"/>`;
        y += out ? 74 + r() * 10 : 150 + r() * 260; }
      lanes += `<g id="${id}-ln${li}">${cars}</g>`; });
    // Keng's car: outbound, nearest the emergency stair
    lanes += `<g id="${id}-me"><circle cx="${KX}" cy="${KY}" r="46" fill="none" stroke="${CREAM}" stroke-width="4" id="${id}-ring"/>${car(KX, KY, "#f2efe8", true)}</g>`;
    xw += lanes + `<g style="mix-blend-mode:screen;filter:blur(3px)">${glowL}</g>`;
    // the emergency stair on the deck's edge, down to the street
    xw += `<g transform="translate(${X0 + W / 2 + 6},${KY + 60})"><rect x="0" y="-36" width="56" height="88" fill="#d8b54a"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M4,${-30 + k * 14}H52" stroke="#7a6420" stroke-width="4"/>`).join("")}</g></g>`;
    // the route: from the car, through the barrier to the stair, down, across the street into the ramp
    const rot = (x, y) => { const a = (ANG * Math.PI) / 180, dx = x - X0, dy = y - Y0; return [X0 + dx * Math.cos(a) - dy * Math.sin(a), Y0 + dx * Math.sin(a) + dy * Math.cos(a)]; };
    const [ax, ay] = rot(KX, KY), [bx, by] = rot(X0 + W / 2 + 34, KY + 60), [cx2, cy2] = [TX - 120, TY + 380], [dx2, dy2] = [TX - 40, TY + 378];
    const RP = `M${f1(ax)},${f1(ay)}L${f1(bx)},${f1(by)}Q${f1(bx + 30)},${f1(by + 120)} ${f1(cx2)},${f1(cy2)}L${f1(dx2)},${f1(dy2)}`;
    const route = `<mask id="${id}-rm"><path id="${id}-rmp" d="${RP}" stroke="#fff" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></mask>
      <g mask="url(#${id}-rm)"><path d="${RP}" stroke="#14110f" stroke-width="15" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>
        <path id="${id}-rt" d="${RP}" stroke="${CREAM}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="18 14"/></g>
      <g id="${id}-arr" opacity="0"><path d="M${f1(dx2 - 22)},${f1(dy2 - 14)}L${f1(dx2 + 2)},${f1(dy2)}L${f1(dx2 - 22)},${f1(dy2 + 14)}" stroke="${CREAM}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`;
    // the shelter: a green ring that breathes around the tower
    const safe = `<g id="${id}-safe" opacity="0"><rect x="${TX - 24}" y="${TY - 24}" width="${TW + 48}" height="${TH + 48}" rx="20" fill="#3a9c66" opacity=".16"/>
      <rect x="${TX - 24}" y="${TY - 24}" width="${TW + 48}" height="${TH + 48}" rx="20" fill="none" stroke="#7ee0a6" stroke-width="6" stroke-dasharray="22 14"/></g>`;
    // scale bar
    const scale = `<g id="${id}-sc" opacity="0" transform="translate(70,1520)"><path d="M0,0H120M0,-12V12M120,-12V12" stroke="${CREAM}" stroke-width="5" stroke-linecap="round"/>
      <text x="60" y="-22" font-family="Kanit" font-weight="800" font-size="30" fill="${CREAM}" text-anchor="middle">50 ม.</text></g>`;
    const [lkx, lky] = rot(KX, KY);
    const tags = tag(`${id}-t1`, lkx - 24, lky - 30, 200, 820, "รถเก่ง", { w: 160 }) + tag(`${id}-t2`, TX + 240, TY + 120, 760, 470, "ตึกคอนกรีต", { w: 250 })
      + tag(`${id}-t3`, TX - 40, TY + 430, 790, 1420, "ลานจอดใต้ดิน", { w: 300, fill: "#dcefdf" });
    g += `<g id="${id}-cam">${ground}${shadows}${tr}${roofs}${tower}${xw}${route}${safe}<rect x="-400" y="-400" width="1880" height="2720" fill="url(#${id}-glow)" style="mix-blend-mode:screen"/>${tags}</g>
      <rect width="1080" height="1920" fill="url(#${id}-vig)"/>${scale}`;
    put(layer, `<g id="${id}">${g}</g>`);
    ["t1", "t2", "t3"].forEach((k) => hide(tl, `${id}-${k}`, t0));
    tl.fromTo(`#${id}-cam`, { scale: 1.0, rotation: -3, svgOrigin: "540 1000" }, { scale: 1.13, rotation: 0, svgOrigin: "540 1000", duration: dur, ease: "sine.inOut" }, t0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t0);
    lanesX.forEach((_, li) => tl.fromTo(`#${id}-ln${li}`, { y: 0 }, { y: li >= 3 ? -22 : -60, duration: dur, ease: li >= 3 ? "steps(4)" : "none" }, t0));
    loop(tl, `#${id}-ring`, { scale: 0.7, opacity: 1, svgOrigin: `${KX} ${KY}` }, { scale: 1.5, opacity: 0, svgOrigin: `${KX} ${KY}` }, 0.8, t0 + 0.2, dur - 0.2, false, "power1.out");
    tagIn(tl, `${id}-t1`, t0 + 0.35, lkx - 24, lky - 30);
    tagIn(tl, `${id}-t2`, t0 + 0.8, TX + 240, TY + 120);
    tl.to(`#${id}-rmp`, { attr: { "stroke-dashoffset": 0 }, duration: 0.95, ease: "power1.inOut" }, t0 + AT);
    tl.to(`#${id}-arr`, { opacity: 1, duration: 0.1 }, t0 + AT + 0.9);
    loop(tl, `#${id}-rt`, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -64 } }, 0.5, t0 + AT, dur - AT, false);
    tl.to(`#${id}-safe`, { opacity: 1, duration: 0.3 }, t0 + AT + 0.85);
    loop(tl, `#${id}-safe`, { opacity: 1 }, { opacity: 0.45 }, 0.9, t0 + AT + 1.15, dur - AT - 1.15);
    tagIn(tl, `${id}-t3`, t0 + AT + 0.95, TX - 40, TY + 430);
    tl.to(`#${id}-sc`, { opacity: 1, duration: 0.3 }, t0 + 0.6);
  }

  // ---------------- s09 · the city at night from high up: every road out clogs with tail lights ----------------
  function night(tl, layer, t0, dur, o = {}) {
    const id = nid("nmn"), r = mk(23), CX = 540, CY = 860;
    let g = `<defs><radialGradient id="${id}-bg" cx=".5" cy=".45" r=".75"><stop offset="0" stop-color="#142030"/><stop offset="1" stop-color="#04070b"/></radialGradient>
      <radialGradient id="${id}-hot"><stop offset="0" stop-color="#fff4dc" stop-opacity="1"/><stop offset=".25" stop-color="#ffb070" stop-opacity=".7"/><stop offset="1" stop-color="#ff6a3a" stop-opacity="0"/></radialGradient>
      <filter id="${id}-bl" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="7"/></filter>
      <mask id="${id}-m"><circle id="${id}-mc" cx="${CX}" cy="${CY}" r="60" fill="#fff"/></mask></defs>
      <rect x="-300" y="-300" width="1680" height="2520" fill="url(#${id}-bg)"/>`;
    // the street grid, turned a little; the city's lights
    let grid = `<g transform="rotate(14 ${CX} ${CY})" stroke="#1b2737" stroke-width="2" opacity=".9">`;
    for (let k = -22; k <= 22; k++) grid += `<path d="M${CX - 1300},${CY + k * 62}H${CX + 1300}M${CX + k * 62},${CY - 1500}V${CY + 1500}"/>`;
    grid += `</g>`;
    let lights = ""; for (let k = 0; k < 700; k++) { const a = r() * Math.PI * 2, d = Math.pow(r(), 0.7) * 1250, x = CX + Math.cos(a) * d, y = CY + Math.sin(a) * d * 1.25;
      lights += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(1.2 + r() * 1.8)}" fill="#ffd9a0" opacity="${f1(0.08 + 0.32 * (1 - d / 1250) * r())}"/>`; }
    // the river, an S through the city
    const RV = `M150,-200C260,300 560,520 520,860S300,1300 640,1640S880,2000 820,2300`;
    g += grid + lights + `<path d="${RV}" stroke="#16222f" stroke-width="50" fill="none"/><path d="${RV}" stroke="#070b11" stroke-width="38" fill="none"/>`;
    // the roads out: quadratic curves from the centre; each split at u = 0.4 into the moving inner part and the packed outer part
    const roads = [-98, -52, -12, 30, 74, 118, 160, 205, 250].map((deg, k) => { const a = (deg * Math.PI) / 180, L = 1450 + r() * 250, bend = (r() - 0.5) * 260;
      const ex = CX + Math.cos(a) * L, ey = CY + Math.sin(a) * L * 1.15, mx = (CX + ex) / 2 - Math.sin(a) * bend, my = (CY + ey) / 2 + Math.cos(a) * bend;
      return { p0: [CX, CY], p1: [mx, my], p2: [ex, ey] }; });
    const split = (R, u) => { const L = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
      const a = L(R.p0, R.p1, u), b = L(R.p1, R.p2, u), m = L(a, b, u); return [{ p0: R.p0, p1: a, p2: m }, { p0: m, p1: b, p2: R.p2 }]; };
    const D = (R) => `M${R.p0.map(f1).join(",")}Q${R.p1.map(f1).join(",")} ${R.p2.map(f1).join(",")}`;
    let base = "", flow = "", jam = "", glow = "";
    roads.forEach((R, k) => { const [inn, out] = split(R, 0.36);
      base += `<path d="${D(R)}" stroke="#263243" stroke-width="18" fill="none" stroke-linecap="round"/><path d="${D(R)}" stroke="#30405a" stroke-width="5" fill="none" stroke-dasharray="20 18"/>`;
      flow += `<path class="${id}-fl" d="${D(inn)}" stroke="#ff5a40" stroke-width="7" fill="none" stroke-linecap="round" stroke-dasharray="2 24"/>`;
      jam += [-7, 7].map((o2) => `<g transform="translate(${o2},${-o2 * 0.6})"><path class="${id}-jm" d="${D(out)}" stroke="#ff4430" stroke-width="8" fill="none" stroke-linecap="round" stroke-dasharray="2 9"/></g>`).join("")
        + `<path class="${id}-jm2" d="${D(out)}" stroke="#ffb090" stroke-width="3" fill="none" stroke-linecap="round" stroke-dasharray="1 23"/>`;
      glow += `<path d="${D(out)}" stroke="#ff3a2a" stroke-width="30" fill="none" stroke-linecap="round" opacity=".45"/>`; });
    g += base + `<g mask="url(#${id}-m)"><g filter="url(#${id}-bl)" style="mix-blend-mode:screen">${glow}</g>${flow}${jam}</g>`;
    // the blast: a hot glow and rings; Keng, a green dot stuck in one of the red rivers, 8 km out
    g += `<circle cx="${CX}" cy="${CY}" r="230" fill="url(#${id}-hot)" style="mix-blend-mode:screen"/><g id="${id}-rg"><circle cx="${CX}" cy="${CY}" r="60" fill="none" stroke="#ffc890" stroke-width="4"/></g>
      <circle cx="${CX}" cy="${CY}" r="16" fill="#fff8ec"/>`;
    const KR = split(roads[6], 0.3)[0].p2, kx = KR[0], ky = KR[1];
    g += `<path id="${id}-kl" d="M${CX},${CY}L${f1(kx)},${f1(ky)}" stroke="${CREAM}" stroke-width="3" stroke-dasharray="10 10" opacity=".85"/>
      <circle cx="${f1(kx)}" cy="${f1(ky)}" r="34" fill="#5ae08a" opacity=".25" id="${id}-kg"/><circle cx="${f1(kx)}" cy="${f1(ky)}" r="13" fill="#5ae08a" stroke="#0b2a18" stroke-width="3"/>`;
    const midx = (CX + kx) / 2, midy = (CY + ky) / 2;
    g += `<g transform="translate(${f1(midx)},${f1(midy)})"><g id="${id}-km"><rect x="-62" y="-24" width="124" height="48" rx="24" fill="${CREAM}" stroke="${INK}" stroke-width="3"/><text y="12" font-family="Kanit" font-weight="800" font-size="32" fill="${INK}" text-anchor="middle">8 กม.</text></g></g>`
      + tag(`${id}-t1`, kx + 8, ky - 14, kx + 90, ky - 130, "เก่ง", { w: 110 })
      + `<g transform="translate(${CX},${CY + 92})"><g id="${id}-bp"><rect x="-96" y="-25" width="192" height="50" rx="25" fill="#d8463c" stroke="${INK}" stroke-width="3"/><text y="12" font-family="Kanit" font-weight="800" font-size="30" fill="#fff" text-anchor="middle">จุดระเบิด</text></g></g>`;
    put(layer, `<g id="${id}"><g id="${id}-cam">${g}</g></g>`);
    hide(tl, `${id}-t1`, t0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25 }, t0);
    tl.fromTo(`#${id}-cam`, { scale: 1.22, svgOrigin: `${CX} ${CY}` }, { scale: 1.0, svgOrigin: `${CX} ${CY}`, duration: dur, ease: "power2.out" }, t0);
    tl.to(`#${id}-mc`, { attr: { r: 1700 }, duration: Math.min(1.9, dur - 0.3), ease: "power1.in" }, t0 + 0.15);
    loop(tl, `.${id}-fl`, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -52 } }, 0.35, t0, dur, false);
    loop(tl, `.${id}-jm`, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -11 } }, 0.9, t0, dur, false);
    loop(tl, `.${id}-jm2`, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -24 } }, 1.4, t0, dur, false);
    loop(tl, `#${id}-rg`, { scale: 0.7, opacity: 1, svgOrigin: `${CX} ${CY}` }, { scale: 4, opacity: 0, svgOrigin: `${CX} ${CY}` }, 0.9, t0, dur, false, "power1.out");
    loop(tl, `#${id}-kg`, { scale: 0.8, svgOrigin: `${f1(kx)} ${f1(ky)}` }, { scale: 1.5, svgOrigin: `${f1(kx)} ${f1(ky)}` }, 0.7, t0 + 0.3, dur - 0.3);
    tl.fromTo(`#${id}-bp`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.35, ease: "back.out(2.4)" }, t0 + 0.2);
    tl.fromTo(`#${id}-km`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.35, ease: "back.out(2.4)" }, t0 + 0.75);
    tagIn(tl, `${id}-t1`, t0 + 0.5, kx + 8, ky - 14);
  }

  // ---------------- s10 · the family's car side on: fallout drifts through glass and thin steel and reaches them ----------------
  function carCut(tl, layer, t0, dur, o = {}) {
    const id = nid("nmc"), r = mk(57), AT = o.at ?? 2.27;
    const BODY = `M95,1150L95,1082Q100,1042 160,1032L332,1012Q362,1006 384,990L472,902Q492,882 522,880L722,880Q762,882 782,902L862,990Q882,1006 912,1010L960,1020Q985,1030 985,1070L985,1150Q985,1172 963,1174L118,1174Q95,1172 95,1150Z`;
    const WIN1 = `M398,996L484,908Q494,900 506,900L606,900L606,996Z`, WIN2 = `M620,996L620,900L714,900Q734,902 748,918L800,996Z`;
    let g = `<defs><linearGradient id="${id}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c1828"/><stop offset=".55" stop-color="#3e2a38"/><stop offset="1" stop-color="#241e26"/></linearGradient>
      <radialGradient id="${id}-hot" cx="1" cy="0" r="1"><stop offset="0" stop-color="#ffb070" stop-opacity=".6"/><stop offset="1" stop-color="#ff8a4a" stop-opacity="0"/></radialGradient>
      <linearGradient id="${id}-body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2ddd4"/><stop offset=".55" stop-color="#cfc9bf"/><stop offset=".56" stop-color="#b3ada3"/><stop offset="1" stop-color="#9f998f"/></linearGradient>
      <linearGradient id="${id}-gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a4a5c"/><stop offset="1" stop-color="#1e2632"/></linearGradient>
      <radialGradient id="${id}-in"><stop offset="0" stop-color="#d8ff7a" stop-opacity=".9"/><stop offset="1" stop-color="#a8e04a" stop-opacity="0"/></radialGradient>
      <clipPath id="${id}-wc"><path d="${WIN1}"/><path d="${WIN2}"/></clipPath><filter id="${id}-b6"><feGaussianBlur stdDeviation="6"/></filter></defs>
      <rect width="1080" height="1920" fill="url(#${id}-sky)"/><rect width="1080" height="1920" fill="url(#${id}-hot)" style="mix-blend-mode:screen"/>`;
    // the city behind, the deck, the jam's lights out of focus
    let sky = ""; for (let k = 0; k < 14; k++) { const x = -40 + k * 84 + r() * 30, h = 120 + r() * 300; sky += `<rect x="${f1(x)}" y="${f1(1150 - h)}" width="${f1(60 + r() * 50)}" height="${f1(h)}" fill="#2a2234" opacity=".9"/>`; }
    g += `<g transform="translate(0,-190)">` + sky + `<rect x="0" y="1150" width="1080" height="960" fill="#2e282e"/><rect x="0" y="1150" width="1080" height="10" fill="#4a4248"/><path d="M0,1330H1080" stroke="#d8d2c4" stroke-width="5" stroke-dasharray="44 36" opacity=".35"/>`;
    let bok = ""; for (let k = 0; k < 16; k++) bok += `<circle cx="${f1(r() * 1080)}" cy="${f1(1030 + r() * 140)}" r="${f1(14 + r() * 22)}" fill="${r() < 0.75 ? "#ff4a36" : "#ffd9a0"}" opacity="${f1(0.25 + r() * 0.3)}"/>`;
    g += `<g filter="url(#${id}-b6)">${bok}</g>`;
    // the car: shadow, body, glass, the family inside, doors, wheels, lights
    g += `<ellipse cx="540" cy="1192" rx="470" ry="26" fill="#0c0a0e" opacity=".6"/>
      <g id="${id}-car"><path d="${BODY}" fill="url(#${id}-body)"/><path d="M110,1104H972" stroke="#8f897f" stroke-width="4"/>
      <path d="${WIN1}" fill="url(#${id}-gl)"/><path d="${WIN2}" fill="url(#${id}-gl)"/>
      <g clip-path="url(#${id}-wc)"><path d="M486,996Q486,930 528,930Q570,930 570,996Z" fill="#0c0b10"/><circle cx="528" cy="934" r="28" fill="#0c0b10"/><rect x="560" y="906" width="40" height="70" rx="12" fill="#121118"/>
        <path d="M664,996Q664,950 696,950Q728,950 728,996Z" fill="#0c0b10"/><circle cx="696" cy="952" r="22" fill="#0c0b10"/>
        <rect id="${id}-inglow" x="380" y="880" width="440" height="130" fill="url(#${id}-in)" opacity="0" style="mix-blend-mode:screen"/>
        <path d="M430,996L520,900H560L470,996Z" fill="#fff" opacity=".12"/><path d="M650,996L720,900H740L670,996Z" fill="#fff" opacity=".1"/></g>
      <path d="M612,900V1160M394,994V1160M806,996L812,1120" stroke="#8f897f" stroke-width="4"/><rect x="560" y="1030" width="34" height="9" rx="4" fill="#8f897f"/><rect x="760" y="1030" width="34" height="9" rx="4" fill="#8f897f"/>
      <path d="M372,990L398,976L404,996Z" fill="#b3ada3"/>
      <path d="M100,1052L150,1044L152,1074L104,1078Z" fill="#fff4cf"/><path d="M962,1034L984,1040L985,1078L960,1078Z" fill="#ff4a36"/>
      ${[260, 820].map((x) => `<circle cx="${x}" cy="1172" r="92" fill="#1e1c22"/><circle cx="${x}" cy="1176" r="76" fill="#17161a"/><circle cx="${x}" cy="1176" r="44" fill="#8a8c90"/><circle cx="${x}" cy="1176" r="14" fill="#5a5c60"/>`).join("")}</g>`;
    // inside the cabin: grains that got in, glowing on the family
    let ins = ""; for (let k = 0; k < 26; k++) ins += `<circle cx="${f1(400 + r() * 400)}" cy="${f1(905 + r() * 90)}" r="${f1(2.5 + r() * 3)}" fill="#e4ff8a"/>`;
    g += `<g clip-path="url(#${id}-wc)"><g id="${id}-ins" opacity="0">${ins}</g></g></g>`;
    // fallout: grains drifting down-left from the blast, over everything, two copies for a seamless loop; streaks on some
    let dust = ""; for (let k = 0; k < 120; k++) { const x = r() * 1500 - 100, y = r() * 1700 - 300, rr = 2.5 + r() * 4;
      dust += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(rr)}" fill="#c2e24a" opacity="${f1(0.55 + r() * 0.45)}"/>`; if (k % 4 === 0) dust += `<path d="M${f1(x)},${f1(y)}l${f1(14 + rr * 2)},${f1(-30 - rr * 4)}" stroke="#c2e24a" stroke-width="2" opacity=".35"/>`; }
    g += `<g id="${id}-d1">${dust}</g><g id="${id}-d2" transform="translate(360,-1200)">${dust}</g>`;
    // labels on leaders, and the protection meter on the beat of "แทบไม่ได้"
    g += tag(`${id}-t1`, 540, 760, 250, 590, "กระจก", { w: 170 }) + tag(`${id}-t2`, 720, 870, 850, 590, "เหล็กบาง", { w: 200 });
    g += `<g transform="translate(540,410)"><g id="${id}-mt"><rect x="-300" y="-56" width="600" height="112" rx="28" fill="${CREAM}" stroke="${INK}" stroke-width="4"/>
      <text x="-268" y="-6" font-family="Kanit" font-weight="800" font-size="34" fill="${INK}">กันรังสี</text>
      <rect x="-268" y="12" width="536" height="26" rx="13" fill="#e3d8c0" stroke="${INK}" stroke-width="3"/><rect id="${id}-mf" x="-266" y="14" width="0" height="22" rx="11" fill="#d8463c"/>
      <text x="268" y="-6" font-family="Kanit" font-weight="800" font-size="34" fill="#d8463c" text-anchor="end">แทบไม่ได้</text></g></g>`;
    put(layer, `<g id="${id}"><g id="${id}-cam">${g}</g></g>`);
    ["t1", "t2"].forEach((k) => hide(tl, `${id}-${k}`, t0));
    tl.fromTo(`#${id}-cam`, { scale: 1.0, svgOrigin: "540 850" }, { scale: 1.07, svgOrigin: "540 850", duration: dur, ease: "sine.inOut" }, t0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t0);
    loop(tl, `#${id}-d1`, { x: 0, y: 0 }, { x: -360, y: 1200 }, 3.2, t0, dur, false);
    loop(tl, `#${id}-d2`, { x: 0, y: 0 }, { x: -360, y: 1200 }, 3.2, t0, dur, false);
    tl.fromTo(`#${id}-car`, { y: 0 }, { y: 2, duration: 0.5, repeat: Math.ceil(dur / 0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
    tagIn(tl, `${id}-t1`, t0 + 0.5, 540, 760);
    tagIn(tl, `${id}-t2`, t0 + 1.15, 720, 870);
    tl.to(`#${id}-ins`, { opacity: 1, duration: 0.8 }, t0 + 0.9);
    loop(tl, `#${id}-ins`, { y: -4 }, { y: 6 }, 0.9, t0 + 0.9, dur - 0.9);
    tl.to(`#${id}-inglow`, { opacity: 0.35, duration: 1.2 }, t0 + 0.9); tl.to(`#${id}-inglow`, { opacity: 0.75, duration: 0.4 }, t0 + AT);
    tl.fromTo(`#${id}-mt`, { scale: 0, rotation: -6, svgOrigin: "0 0" }, { scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.45, ease: "back.out(2)" }, t0 + AT - 0.3);
    tl.to(`#${id}-mf`, { attr: { width: 40 }, duration: 0.5, ease: "power2.out" }, t0 + AT);
    tl.to(`#${id}-mf`, { attr: { width: 26 }, duration: 0.3, ease: "power1.inOut", yoyo: true, repeat: 3 }, t0 + AT + 0.5);
  }

  // ---------------- s13 · car ✗ → building ✓ → underground ✓: round cream tiles with plain line glyphs, thin arrows, marks ----------------
  const GLYPH = {
    car: `<path d="M-30,10V0Q-30,-6 -24,-8L-14,-22Q-11,-26 -6,-26H8Q13,-26 16,-22L26,-8Q32,-6 32,0V10Z" fill="none" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
      <path d="M-12,-22V-9M2,-22V-9" stroke="${INK}" stroke-width="4"/><circle cx="-16" cy="12" r="7" fill="${CREAM}" stroke="${INK}" stroke-width="5"/><circle cx="18" cy="12" r="7" fill="${CREAM}" stroke="${INK}" stroke-width="5"/>`,
    building: `<rect x="-18" y="-30" width="36" height="58" fill="none" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
      ${[-20, -8, 4].map((y) => `<path d="M-9,${y}h6M3,${y}h6" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`).join("")}<path d="M-4,28V18h8V28" fill="none" stroke="${INK}" stroke-width="4"/>`,
    under: `<path d="M-32,-4H32" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><rect x="-12" y="-30" width="24" height="26" fill="none" stroke="${INK}" stroke-width="5"/>
      <rect x="-24" y="4" width="48" height="24" rx="4" fill="#3a9c66" opacity=".25"/><rect x="-24" y="4" width="48" height="24" rx="4" fill="none" stroke="${INK}" stroke-width="5"/><path d="M0,8V22M-6,16l6,6l6,-6" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
  };
  function ladder(tl, layer, t0, dur, items, o = {}) {
    const id = nid("nml"), y = o.y ?? 300, gap = o.gap ?? 300, n = items.length, x0 = 540 - ((n - 1) * gap) / 2;
    let g = "";
    items.forEach((it, k) => { const x = x0 + k * gap, ok = it.ok, ring = ok ? "#3a9c66" : "#d8463c";
      if (k < n - 1) g += `<path id="${id}-a${k}" d="M${x + 76},${y}H${x + gap - 82}" stroke="${CREAM}" stroke-width="5" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
        <path id="${id}-h${k}" d="M${x + gap - 98},${y - 14}L${x + gap - 82},${y}L${x + gap - 98},${y + 14}" stroke="${CREAM}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0"/>`;
      g += `<g transform="translate(${x},${y})"><g id="${id}-i${k}"><circle r="62" fill="#000" opacity=".35" cy="6"/><circle r="60" fill="${CREAM}" stroke="${ring}" stroke-width="7"/>${GLYPH[it.icon]}
        <g transform="translate(44,-44)"><g id="${id}-m${k}"><circle r="20" fill="${ring}" stroke="${CREAM}" stroke-width="4"/>${ok ? `<path d="M-8,0l5,6l11,-12" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>` : `<path d="M-7,-7L7,7M7,-7L-7,7" stroke="#fff" stroke-width="5" stroke-linecap="round"/>`}</g></g></g></g>
        <g transform="translate(${x},${y + 98})"><g id="${id}-l${k}"><rect x="-80" y="-26" width="160" height="52" rx="26" fill="${CREAM}" stroke="${INK}" stroke-width="3"/><text y="13" font-family="Kanit" font-weight="800" font-size="36" fill="${INK}" text-anchor="middle">${it.label}</text></g></g>`; });
    put(layer, `<g id="${id}">${g}</g>`);
    items.forEach((it, k) => { const a = t0 + (o.at ?? 0.1) + k * (o.step ?? 0.45);
      tl.fromTo(`#${id}-i${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.42, ease: "back.out(2.2)" }, a);
      tl.fromTo(`#${id}-l${k}`, { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.25 }, a + 0.15);
      tl.fromTo(`#${id}-m${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.3, ease: "back.out(3)" }, a + 0.35);
      if (!it.ok) tl.fromTo(`#${id}-i${k}`, { x: -5 }, { x: 5, duration: 0.06, repeat: 5, yoyo: true, ease: "sine.inOut", immediateRender: false }, a + 0.5);
      if (k < n - 1) { tl.to(`#${id}-a${k}`, { attr: { "stroke-dashoffset": 0 }, duration: 0.3, ease: "power2.out" }, a + 0.3); tl.to(`#${id}-h${k}`, { opacity: 1, duration: 0.08 }, a + 0.56); } });
  }

  // ---------------- story UI: a name on a leader for a character, a red stamp that slams on ----------------
  function nameTag(tl, layer, t0, at, x, y, lx, ly, txt, o = {}) { const id = nid("nmt"); put(layer, tag(id, x, y, lx, ly, txt, o)); hide(tl, id, t0); tagIn(tl, id, at, x, y); }
  function stamp(tl, layer, at, x, y, txt, o = {}) { const id = nid("nms"), w = o.w ?? 70 + txt.length * 30;
    put(layer, `<g transform="translate(${f1(x)},${f1(y)}) rotate(${o.rot ?? -8})"><g id="${id}" opacity="0"><rect x="${f1(-w / 2)}" y="-38" width="${f1(w)}" height="76" rx="12" fill="none" stroke="#d8463c" stroke-width="7"/>
      <rect x="${f1(-w / 2 + 9)}" y="-29" width="${f1(w - 18)}" height="58" rx="7" fill="#d8463c" opacity=".94"/><text y="16" font-family="Kanit" font-weight="900" font-size="46" fill="#fff" text-anchor="middle">${txt}</text></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, scale: 1.9, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.2, ease: "power3.in" }, at);
    tl.fromTo(`#${id}`, { x: -5 }, { x: 5, duration: 0.05, repeat: 3, yoyo: true, ease: "none", immediateRender: false }, at + 0.2);
    tl.to(`#${id}`, { x: 0, duration: 0.05 }, at + 0.42); }

  // ---------------- s23 · the supplies laid out on a tarp, seen from above; a hand counts them as the clipboard fills ----------------
  function supplies(tl, layer, t0, dur, o = {}) {
    const id = nid("nmy"), r = mk(71), times = o.times || [0.5, 0.75, 1.0, 1.25, 1.5];
    let g = `<defs><radialGradient id="${id}-lamp" cx=".18" cy=".62" r=".8"><stop offset="0" stop-color="#ffcf8a" stop-opacity=".55"/><stop offset=".5" stop-color="#ffb066" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
      <radialGradient id="${id}-vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
      <filter id="${id}-sh" x="-20%" y="-20%" width="140%" height="160%"><feGaussianBlur stdDeviation="5"/></filter></defs>
      <rect width="1080" height="1920" fill="#2c2e30"/><rect x="30" y="-40" width="1020" height="2000" fill="#3c5a7c"/>
      ${[260, 640, 1020, 1400, 1780].map((y) => `<path d="M30,${y}L1050,${y + 40}" stroke="#4d6d92" stroke-width="10" opacity=".7"/>`).join("")}
      ${[[60, 60], [1020, 60], [60, 1880], [1020, 1880]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="10" fill="#c8ccd2" stroke="#2c2e30" stroke-width="4"/>`).join("")}`;
    const sh = (inner, dx = 10, dy = 14) => `<g transform="translate(${dx},${dy})" filter="url(#${id}-sh)" opacity=".45">${inner.replace(/fill="[^"]*"/g, 'fill="#0c1118"').replace(/stroke="[^"]*"/g, 'stroke="#0c1118"')}</g>${inner}`;
    let it = "";
    // water: a case of bottles seen from above
    let wb = ""; for (let i = 0; i < 3; i++) for (let j = 0; j < 4; j++) { const x = 140 + j * 58, y = 1010 + i * 58;
      wb += `<circle cx="${x}" cy="${y}" r="26" fill="#a8d4ef" opacity=".92"/><circle cx="${x}" cy="${y}" r="26" fill="none" stroke="#6aa8d4" stroke-width="3"/><circle cx="${x - 7}" cy="${y - 7}" r="7" fill="#fff" opacity=".55"/><circle cx="${x}" cy="${y}" r="9" fill="#2f6fd0"/>`; }
    it += sh(wb);
    // snacks: packets dropped in a heap
    let sn = ""; for (let k = 0; k < 7; k++) { const x = 420 + r() * 150, y = 940 + r() * 130, a = -30 + r() * 60, col = ["#e2b04a", "#d8463c", "#3a9c66", "#e8e0c8", "#f08a2a"][k % 5];
      sn += `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(a)})"><rect x="-34" y="-48" width="68" height="96" rx="8" fill="${col}"/><rect x="-34" y="-48" width="68" height="14" fill="#fff" opacity=".35"/><circle cy="6" r="14" fill="#fff" opacity=".5"/></g>`; }
    it += sh(sn);
    // the radio, the torches, the first-aid box — open and empty
    it += sh(`<g transform="translate(760,1060) rotate(6)"><rect x="-84" y="-52" width="168" height="104" rx="14" fill="#c8302a"/><rect x="-66" y="-36" width="70" height="72" rx="8" fill="#5a2a2a"/>
      ${[0, 1, 2, 3, 4].map((k) => `<path d="M-60,${-26 + k * 13}h58" stroke="#3a1a1a" stroke-width="5"/>`).join("")}<rect x="16" y="-34" width="54" height="26" rx="5" fill="#b9e8a8"/><circle cx="43" cy="18" r="16" fill="#e9e4cf"/></g>`);
    let tc = ""; [[860, 1250, -20], [905, 1310, -14], [840, 1370, -26]].forEach(([x, y, a]) => (tc += `<g transform="translate(${x},${y}) rotate(${a})"><rect x="-62" y="-15" width="96" height="30" rx="8" fill="#2e3238"/><path d="M34,-22h28v44h-28z" fill="#8a8f98"/><circle cx="62" cy="0" r="16" fill="#fff4cf"/><rect x="-40" y="-6" width="18" height="12" rx="3" fill="#d8463c"/></g>`));
    it += sh(tc);
    it += sh(`<g transform="translate(470,1480)"><rect x="-130" y="-30" width="260" height="170" rx="14" fill="#efe9dc"/><rect x="-116" y="-16" width="232" height="142" rx="8" fill="#cfc7b6"/>
      <path d="M-100,110l30,-10M60,90l14,8M-20,40l10,4" stroke="#b8ae9a" stroke-width="5" stroke-linecap="round"/>
      <g transform="translate(0,-110) rotate(-8)"><rect x="-130" y="-70" width="260" height="76" rx="14" fill="#f6f1e6"/><path d="M-14,-58h28v20h20v28h-20v20h-28v-20h-20v-28h20z" fill="#d8463c" transform="translate(0,4) scale(.8)"/></g></g>`);
    g += it + `<rect width="1080" height="1920" fill="url(#${id}-lamp)" style="mix-blend-mode:screen"/><rect width="1080" height="1920" fill="url(#${id}-vig)"/>`;
    // the hand: sleeve from the bottom edge, palm, the pointing finger; it visits each item on the beat of the clipboard's rows
    const hand = `<g id="${id}-h"><g transform="rotate(-12)"><path d="M-40,40L-56,520H56L40,40Z" fill="#3a4a62"/><path d="M-44,60H44" stroke="#2a3446" stroke-width="10"/>
      <ellipse cx="0" cy="20" rx="46" ry="54" fill="#d8a070"/><rect x="-12" y="-110" width="26" height="110" rx="13" fill="#d8a070"/><path d="M-40,8Q-62,-6 -54,-34" stroke="#d8a070" stroke-width="22" fill="none" stroke-linecap="round"/>
      <path d="M-8,-104h18" stroke="#b47e52" stroke-width="5" stroke-linecap="round"/></g></g>`;
    g += hand;
    put(layer, `<g id="${id}">${g}</g>`);
    const spots = [[236, 1075], [495, 1010], [760, 1060], [880, 1300], [470, 1470]];
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t0);
    tl.set(`#${id}-h`, { x: 600, y: 2200 }, t0);
    spots.forEach(([x, y], k) => { tl.to(`#${id}-h`, { x: x + 4, y: y + 112, duration: 0.2, ease: "power2.out" }, t0 + times[k] - 0.18);
      tl.to(`#${id}-h`, { y: y + 104, duration: 0.07, yoyo: true, repeat: 1, ease: "power1.inOut" }, t0 + times[k] + 0.02); });
    tl.to(`#${id}-h`, { y: 2200, duration: 0.35, ease: "power2.in" }, t0 + times[4] + 0.45);
  }

  window.NkM = { drone, night, carCut, ladder, nameTag, stamp, supplies };
})();
