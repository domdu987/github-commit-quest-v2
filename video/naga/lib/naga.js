// "ถ้ำพญานาค หน้าฝน" pre-production (lane C, 1 Nov). A made-up cave "ถ้ำผาเกล็ดนาค" in a made-up village by the Mekong.
//   Sets.nagaMouth(L, o)  the cave mouth in heavy rain: limestone cliff, jungle, a naga balustrade stair (two naga heads),
//                         offerings and a garland, a rope across the mouth with a "ปิดช่วงฤดูฝน" board, a muddy stream already
//                         running out of the mouth. o.rain 0..1
//   Sets.nagaCave(L, o)   inside: a lit limestone chamber with depth (near pillar, mid chamber, far passage in haze), the
//                         "เกล็ดนาค" wall — scale-like rock that is really old flood lines (#id-scl), a dry ledge above the top
//                         line, the low exit passage on the left drowning (o.wl water level, #id-wtr), headlamp beams o.beams.
//                         Brighter than the hook test: o.amb lifts the shadows (default 0.42 darkness)
//   NagaUI.rules(tl, layer, t0, dur, o)  ยายบัวคำ's carved wooden board hung at the cave mouth: naga-scale border, a naga head
//                         curling over the top, three rhyming rules brushed on, the spoken one highlighted with a yellow brush
//   cast: petch (เพชร 17, vlogger, phone + one headlamp) · puifai (ปุยฝ้าย 12, his sister, rain poncho, glow bracelet)
//         yai (ยายบัวคำ 68, white blouse, sabai) · saeng (ลุงแสง 55, local guide, khaki, the "crazy" one)
(function () {
  const { f1, put, mk } = Pop2;
  const INK = "#1e2228";
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  Sets.DEFS += `
    <linearGradient id="ngLime" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8b0a0"/><stop offset=".6" stop-color="#8a8274"/><stop offset="1" stop-color="#5a5248"/></linearGradient>
    <linearGradient id="ngLime2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6a6254"/><stop offset=".45" stop-color="#a89e8c"/><stop offset="1" stop-color="#5a5246"/></linearGradient>
    <linearGradient id="ngCaveBg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a463e"/><stop offset="1" stop-color="#2a2622"/></linearGradient>
    <linearGradient id="ngWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a7a52" stop-opacity=".78"/><stop offset=".35" stop-color="#6a5a3a" stop-opacity=".9"/><stop offset="1" stop-color="#2a2418" stop-opacity=".97"/></linearGradient>
    <linearGradient id="ngRainSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a6a72"/><stop offset="1" stop-color="#a8b4b0"/></linearGradient>
    <linearGradient id="ngGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset=".5" stop-color="#d8a43a"/><stop offset="1" stop-color="#8a5a1a"/></linearGradient>
    <linearGradient id="ngBoard" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b07e4a"/><stop offset=".5" stop-color="#9a6a3a"/><stop offset="1" stop-color="#7a5028"/></linearGradient>
    <radialGradient id="ngHaze"><stop offset="0" stop-color="#d8d0b8" stop-opacity=".55"/><stop offset="1" stop-color="#d8d0b8" stop-opacity="0"/></radialGradient>
    <radialGradient id="ngLamp"><stop offset="0" stop-color="#fffbe8"/><stop offset=".3" stop-color="#fff0b0" stop-opacity=".8"/><stop offset="1" stop-color="#ffe080" stop-opacity="0"/></radialGradient>`;

  // naga-scale rows (arched scales) inside a band, as old flood lines: lighter stone, a dark tide line under each row
  const scales = (x0, x1, y, rows, sz, op = 0.75) => {
    let s = "";
    for (let r = 0; r < rows; r++) {
      const yy = y + r * sz * 0.62, off = (r % 2) * sz * 0.5;
      s += `<path d="M${x0},${f1(yy + sz * 0.5)}H${x1}" stroke="#3a3428" stroke-width="${f1(sz * 0.12)}" opacity=".55"/>`;
      for (let x = x0 + off; x < x1; x += sz) s += `<path d="M${f1(x)},${f1(yy + sz * 0.5)}q${f1(sz * 0.5)},${f1(-sz * 0.9)} ${f1(sz)},0" fill="#c8bea8" stroke="#6a604e" stroke-width="2.4" opacity="${op}"/>`;
    }
    return s;
  };
  const nagaHead = (x, y, s, flip = 1, id = "") => `<g ${id ? `id="${id}"` : ""} transform="translate(${x},${y}) scale(${s * flip},${s})">
    <path d="M-10,220C-20,140 -10,80 30,40L80,60C60,100 50,160 60,220Z" fill="url(#ngGold)" ${O(5)}/>
    ${[0, 1, 2, 3].map((k) => `<path d="M${2 + k * 6},${200 - k * 40}q24,-16 48,0" fill="none" stroke="#8a5a1a" stroke-width="3"/>`).join("")}
    <path d="M40,-10C0,-60 -6,-130 18,-170C28,-120 48,-108 62,-116C50,-170 72,-226 116,-250C104,-196 114,-160 136,-150C146,-196 178,-216 214,-214C190,-170 186,-126 180,-60Z" fill="url(#ngGold)" ${O(5)}/>
    <path d="M40,-40C30,-90 34,-130 50,-150M90,-70C88,-130 100,-180 120,-210M150,-80C156,-130 170,-170 196,-196" stroke="#8a5a1a" stroke-width="3" fill="none" opacity=".7"/>
    <path d="M20,50C26,-26 90,-60 164,-52C210,-46 246,-28 262,-6L196,12L250,36C228,70 176,88 124,78C82,72 44,82 20,50Z" fill="url(#ngGold)" ${O(5)}/>
    <path d="M200,10L210,28L220,12ZM226,16L234,32L242,18Z" fill="#fffaf0" ${O(1.6)}/><path d="M196,12L250,36" stroke="#7a1a10" stroke-width="6"/>
    <ellipse cx="150" cy="-22" rx="16" ry="12" fill="#fffaf0" ${O(3)}/><circle cx="154" cy="-22" r="7" fill="#c8302a"/>
    <path d="M110,-44q30,-20 70,-10M60,30q40,14 90,6" stroke="#8a5a1a" stroke-width="3" fill="none"/><circle cx="240" cy="-8" r="4" fill="${INK}"/></g>`;

  function nagaMouth(L, o = {}) {
    const id = o.id || "nm", G = 1500, r = mk(o.seed || 41);
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="3200" fill="url(#ngRainSky)"/>`);
    put(L.far, `<path d="M-1400,600Q-800,300 -200,520T1100,420T2500,560V1600H-1400Z" fill="#5a7a6a" opacity=".7"/><path d="M-1400,800Q-600,600 200,760T1700,700T2500,820V1600H-1400Z" fill="#4a6a58" opacity=".8"/>`);
    // the cliff with the mouth
    let s = `<path d="M-1400,-900H2500V${G}H-1400Z" fill="url(#ngLime)"/>
      ${Array.from({ length: 16 }, (_, k) => `<path d="M${-1400 + k * 260 + r() * 80},-900q${f1(30 - r() * 60)},${f1(800 + r() * 900)} ${f1(-20 + r() * 40)},${f1(1500 + r() * 400)}" stroke="#6a6254" stroke-width="${f1(3 + r() * 5)}" opacity=".35" fill="none"/>`).join("")}
      <path d="M140,${G}Q120,${G - 700} 540,${G - 820}Q960,${G - 700} 940,${G}Z" fill="#141210" ${O(6)}/>
      <path d="M200,${G}Q190,${G - 620} 540,${G - 740}Q890,${G - 620} 880,${G}" fill="none" stroke="#3a342c" stroke-width="30"/>
      ${[[260, G - 640, 120, 30], [420, G - 760, 180, 34], [640, G - 770, 150, 28], [820, G - 640, 110, 24]].map(([x, y, h, w]) => `<path d="M${x - w},${y}Q${x - w * 0.2},${y + h * 0.7} ${x},${y + h}Q${x + w * 0.2},${y + h * 0.7} ${x + w},${y}Z" fill="url(#ngLime2)" ${O(3)}/>`).join("")}
      <g opacity=".5">${scales(-200, 120, G - 520, 5, 46, 0.6)}${scales(960, 1300, G - 480, 5, 46, 0.6)}</g>
      ${Array.from({ length: 22 }, (_, k) => { const x = -1300 + ((k * 197) % 3600), y = -700 + ((k * 131) % 900); return `<path d="M${x},${y}q-30,80 10,180q40,90 -10,200" stroke="#3a6a3a" stroke-width="8" fill="none"/>${Array.from({ length: 5 }, (_, j) => `<ellipse cx="${x + (j % 2 ? 16 : -16)}" cy="${y + 40 + j * 70}" rx="20" ry="9" fill="#4a8a4a" transform="rotate(${j % 2 ? 30 : -30} ${x} ${y + 40 + j * 70})"/>`).join("")}`; }).join("")}`;
    // the ground, the muddy stream out of the mouth, the naga stair
    s += `<path d="M-1400,${G}H2500V2600H-1400Z" fill="#6a5a44"/><path d="M380,${G}Q420,${G + 300} 260,${G + 1100}H900Q700,${G + 300} 700,${G}Z" fill="#9a8058" opacity=".9"/>
      ${Array.from({ length: 10 }, (_, k) => `<path d="M${420 + (k % 3) * 80},${G + 60 + k * 90}q40,-10 80,0" stroke="#e8d8b0" stroke-width="4" opacity=".6"/>`).join("")}
      ${[0, 1, 2, 3, 4].map((k) => `<rect x="${-120 - k * 40}" y="${G + 140 + k * 110}" width="${1320 + k * 80}" height="40" fill="#8a8274" ${O(3)} opacity=".9" transform="translate(${k * 0},0)"/>`).join("")}`;
    put(L.set, s);
    // naga balustrades on the stair sides, offerings, the rope and the closure board
    put(L.act, `<path d="M-160,${G + 700}Q-120,${G + 400} 40,${G + 180}" stroke="url(#ngGold)" stroke-width="70" fill="none" stroke-linecap="round"/><path d="M-160,${G + 700}Q-120,${G + 400} 40,${G + 180}" stroke="${INK}" stroke-width="4" fill="none" stroke-dasharray="18 30"/>
      ${nagaHead(-10, G - 40, 1.0, 1, `${id}-nl`)}
      <path d="M1240,${G + 700}Q1200,${G + 400} 1040,${G + 180}" stroke="url(#ngGold)" stroke-width="70" fill="none" stroke-linecap="round"/>
      ${nagaHead(1090, G - 40, 1.0, -1, `${id}-nr`)}
      <g transform="translate(150,${G + 120})"><path d="M-40,0h80l-10,-40h-60z" fill="#c8302a" ${O(3)}/><circle cx="0" cy="-56" r="18" fill="#f4e8a8" ${O(2)}/><path d="M-20,-60q20,-50 40,0" stroke="#e8e0c8" stroke-width="3" fill="none"/>${[-50, -30, -10, 10, 30].map((d) => `<circle cx="${d + 10}" cy="-${70 + (d % 3) * 4}" r="6" fill="#f4f4f0"/>`).join("")}</g>
      <g id="${id}-rope"><path d="M120,${G - 220}Q540,${G - 120} 960,${G - 220}" stroke="#d8c8a0" stroke-width="10" fill="none"/>
        <g transform="translate(540,${G - 160})"><path d="M-40,-10L-140,40M40,-10L140,40" stroke="#d8c8a0" stroke-width="5"/><rect x="-170" y="40" width="340" height="110" rx="8" fill="#f4f0e4" ${O(4)}/><text y="88" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#c8302a">ปิดช่วงฤดูฝน</text><text y="132" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#2a2a2a">ห้ามเข้าถ้ำ</text></g></g>`);
    // rain over everything
    put(L.glow, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#3a4a52" opacity="${f1(0.18 * (o.rain ?? 1))}"/>`);
  }

  function nagaCave(L, o = {}) {
    const id = o.id || "nc", WL = o.wl ?? 1320, r = mk(o.seed || 43);
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#1a1814"/>`);
    // far: the passage running back into haze (depth), a pale glow where the chamber opens
    put(L.far, `<rect x="-1400" y="-900" width="3900" height="3200" fill="url(#ngCaveBg)"/><ellipse cx="760" cy="${WL - 380}" rx="520" ry="360" fill="url(#ngHaze)"/>
      <path d="M420,${WL}Q430,${WL - 520} 760,${WL - 600}Q1090,${WL - 520} 1100,${WL}Z" fill="#6a6252" opacity=".55"/><path d="M560,${WL}Q570,${WL - 330} 760,${WL - 380}Q950,${WL - 330} 960,${WL}Z" fill="#8a8270" opacity=".45"/>`);
    // mid: the chamber walls with texture, stalactites, the เกล็ดนาค flood-line wall on the right with a ledge above it
    const stal = (x, y, h, w) => `<path d="M${x - w},${y}Q${x - w * 0.3},${y + h * 0.6} ${x},${y + h}Q${x + w * 0.3},${y + h * 0.6} ${x + w},${y}Z" fill="url(#ngLime2)" ${O(3)}/><path d="M${x - w * 0.4},${y + 10}Q${x - w * 0.1},${y + h * 0.5} ${x},${y + h - 6}" stroke="#e8e0cc" stroke-width="4" opacity=".45" fill="none"/>`;
    let mid = `<path d="M-1400,-900H2500V${WL - 760}Q1900,${WL - 860} 1500,${WL - 800}Q1100,${WL - 740} 900,${WL - 820}Q560,${WL - 940} 180,${WL - 820}Q-200,${WL - 720} -600,${WL - 800}Q-1000,${WL - 880} -1400,${WL - 760}Z" fill="url(#ngLime)" ${O(5)}/>
      ${Array.from({ length: 30 }, (_, k) => `<path d="M${-1400 + k * 130 + r() * 40},${-900 + r() * 200}q${f1(r() * 30 - 15)},${f1(300 + r() * 500)} ${f1(r() * 20 - 10)},${f1(700 + r() * 300)}" stroke="#5a5246" stroke-width="${f1(2 + r() * 4)}" opacity=".3" fill="none"/>`).join("")}
      ${[[-300, WL - 800, 230, 40], [-60, WL - 760, 170, 26], [330, WL - 880, 280, 48], [640, WL - 900, 200, 30], [1180, WL - 780, 250, 42], [1420, WL - 810, 160, 26], [-720, WL - 790, 210, 34], [900, WL - 840, 140, 22]].map(([x, y, h, w]) => stal(x, y, h, w)).join("")}
      <path d="M-1400,${WL - 760}Q-900,${WL - 560} -720,${WL - 240}L-660,${WL + 600}H-1400Z" fill="url(#ngLime2)" ${O(5)}/>
      <path d="M2500,${WL - 760}Q1900,${WL - 600} 1640,${WL - 520}L1600,${WL + 600}H2500Z" fill="url(#ngLime2)" ${O(5)}/>
      <g id="${id}-scl">${scales(1180, 1640, WL - 480, 7, 54, 0.85)}</g>
      <path d="M1160,${WL - 520}Q1400,${WL - 570} 1660,${WL - 530}L1660,${WL - 480}H1150Z" fill="url(#ngLime)" ${O(4)}/><path d="M1180,${WL - 525}Q1400,${WL - 565} 1640,${WL - 530}" stroke="#f4ecd8" stroke-width="5" opacity=".6" fill="none"/>
      <path d="M-1000,${WL - 400}q60,40 40,120M1880,${WL - 360}q-50,50 -20,140M-400,${WL - 700}q40,30 20,90" stroke="#f4ecd8" stroke-width="5" opacity=".35" fill="none"/>`;
    put(L.mid, mid);
    // set: the low exit passage on the left (half drowned), a near pillar for foreground depth
    put(L.set, `<path d="M-700,${WL + 40}Q-690,${WL - 260} -460,${WL - 300}Q-230,${WL - 260} -220,${WL + 40}Z" fill="#0e0c0a" ${O(5)}/><path d="M-660,${WL}Q-650,${WL - 220} -460,${WL - 250}Q-270,${WL - 220} -260,${WL}" stroke="#4a4236" stroke-width="16" fill="none"/>`);
    if (o.pillar !== false) put(L.fg, `<path d="M${o.pillar ?? 1900},-1000Q${(o.pillar ?? 1900) - 120},${WL - 300} ${(o.pillar ?? 1900) - 40},${WL + 900}H${(o.pillar ?? 1900) + 600}V-1000Z" fill="#3a342c" ${O(6)}/><path d="M${(o.pillar ?? 1900) - 70},-800Q${(o.pillar ?? 1900) - 150},${WL - 300} ${(o.pillar ?? 1900) - 60},${WL + 800}" stroke="#8a8270" stroke-width="10" opacity=".5" fill="none"/>`);
    // the flood (above the actors)
    const rip = (o.ripples || []).map(([x, rr]) => `<ellipse cx="${x}" cy="${WL + 6}" rx="${rr}" ry="${f1(rr * 0.16)}" fill="none" stroke="#f4ecd0" stroke-width="4" opacity=".6"/><ellipse cx="${x}" cy="${WL + 10}" rx="${rr * 1.5}" ry="${f1(rr * 0.22)}" fill="none" stroke="#f4ecd0" stroke-width="3" opacity=".3"/>`).join("");
    put(L.glow, `<g id="${id}-wtr"><rect x="-1400" y="${WL}" width="3900" height="2400" fill="url(#ngWater)"/>
      <path d="M-1400,${WL}Q-1000,${WL - 8} -600,${WL}T200,${WL}T1000,${WL}T1800,${WL}T2600,${WL}" stroke="#f4ecd0" stroke-width="5" fill="none" opacity=".7"/>
      <ellipse cx="-460" cy="${WL + 8}" rx="260" ry="40" fill="#f4ecd0" opacity=".25"/>${Array.from({ length: 8 }, (_, k) => `<path d="M${-640 + k * 40},${WL + 4}q20,-14 40,0" stroke="#fff" stroke-width="3" opacity=".6" fill="none"/>`).join("")}
      ${rip}<g opacity=".25">${Array.from({ length: 14 }, (_, k) => `<path d="M${-1300 + k * 270},${WL + 40 + (k % 3) * 60}h${80 + (k % 4) * 30}" stroke="#f4ecd0" stroke-width="3"/>`).join("")}</g></g>`);
    // light: an ambient lift so the rock reads (brighter than the hook test), headlamp beams on top
    const beams = o.beams || [];
    const cone = ([x, y, d, len], w = 0.42) => { const a = (d * Math.PI) / 180, l = len || 1600, e1 = [x + Math.cos(a - w) * l, y + Math.sin(a - w) * l], e2 = [x + Math.cos(a + w) * l, y + Math.sin(a + w) * l];
      return `M${x},${y}L${f1(e1[0])},${f1(e1[1])}Q${f1(x + Math.cos(a) * l * 1.15)},${f1(y + Math.sin(a) * l * 1.15)} ${f1(e2[0])},${f1(e2[1])}Z`; };
    put(L.glow, `<mask id="${id}-mk"><rect x="-1400" y="-900" width="3900" height="3200" fill="#fff"/>${beams.map((b) => `<path d="${cone(b, 0.32)}" fill="#000" opacity=".8" filter="url(#p2Soft)"/><circle cx="${b[0]}" cy="${b[1]}" r="280" fill="#000" opacity=".7" filter="url(#p2Soft)"/>`).join("")}</mask>
      <rect id="${id}-dark" x="-1400" y="-900" width="3900" height="3200" fill="#0a0806" opacity="${o.amb ?? 0.42}" mask="url(#${id}-mk)"/>
      <g style="mix-blend-mode:screen">${beams.map((b, k) => `<g id="${id}-b${k}"><path d="${cone(b, 0.26)}" fill="#ffe8a8" opacity=".14"/><path d="${cone(b, 0.11)}" fill="#fff6d8" opacity=".14"/><circle cx="${b[0]}" cy="${b[1]}" r="44" fill="url(#ngLamp)"/></g>`).join("")}</g>`);
  }
  Object.assign(Sets, { nagaMouth, nagaCave });

  // ---------------- ยายบัวคำ's rules board ----------------
  const NagaUI = (window.NagaUI = {});
  let seq = 0;
  NagaUI.RULES = [["ฝนลง<u>หนัก</u> อย่า<u>พัก</u>ในถ้ำ"], ["น้ำปิดทาง อย่าดำ<u>ฝ่า</u> ขึ้นหา<u>ผา</u>"], ["ไฟเหลือ<u>น้อย</u> อย่า<u>ปล่อย</u>มือ"]];
  NagaUI.rules = (tl, layer, t0, dur, o = {}) => {
    const id = `ng${seq++}`, act = o.active ?? 0, Y = o.y ?? 260, H = 640, X = 80, Wd = 920;
    const rowY = (k) => Y + 250 + k * 150;
    let rows = "";
    NagaUI.RULES.forEach(([t], k) => {
      const st = k === act ? "act" : k < act ? "done" : "later", y = rowY(k), plain = t.replace(/<\/?u>/g, "");
      const tw = Math.min(760, plain.length * 34 + 20);
      const tt = t.replace(/<u>(.*?)<\/u>/g, `<tspan fill="${st === "later" ? "#8a7f70" : "#c8302a"}">$1</tspan>`);
      rows += `<g id="${id}-r${k}" opacity="${st === "later" ? 0.45 : 1}">
        ${st === "act" ? `<path id="${id}-hl" d="M${X + 90},${y - 52}Q${X + 300},${y - 68} ${X + 110 + tw},${y - 54}L${X + 114 + tw},${y + 36}Q${X + 300},${y + 50} ${X + 84},${y + 32}Z" fill="#ffd23a" opacity=".55"/>` : ""}
        <text x="${X + 60}" y="${y + 22}" font-family="Sriracha" font-size="58" fill="#fffaf0" stroke="#fffaf0" stroke-width="10" stroke-linejoin="round" opacity=".5">${k + 1}. ${plain}</text>
        <text x="${X + 60}" y="${y + 22}" font-family="Sriracha" font-size="58" fill="${st === "later" ? "#8a7f70" : "#2a1a10"}">${k + 1}. ${tt}</text></g>`;
    });
    // the scale border: rows of small arches along the frame
    const border = (() => { let s = ""; for (let x = X + 20; x < X + Wd - 20; x += 34) { s += `<path d="M${x},${Y + 30}q17,-26 34,0" fill="none" stroke="#5a3a1a" stroke-width="3"/><path d="M${x},${Y + H - 20}q17,-26 34,0" fill="none" stroke="#5a3a1a" stroke-width="3"/>`; } return s; })();
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-m"><g id="${id}-sw">
      <path d="M${X + 160},-60V${Y + 20}M${X + Wd - 160},-60V${Y + 20}" stroke="#4a3a20" stroke-width="12"/><path d="M${X + 160},-60V${Y + 20}M${X + Wd - 160},-60V${Y + 20}" stroke="#c8a870" stroke-width="7" stroke-dasharray="10 8"/>
      <rect x="${X}" y="${Y + 16}" width="${Wd}" height="${H}" rx="24" fill="#5a3a1a" ${O(5)}/>
      <rect x="${X}" y="${Y}" width="${Wd}" height="${H}" rx="24" fill="url(#ngBoard)" ${O(5)}/>
      ${Array.from({ length: 12 }, (_, k) => `<path d="M${X + 20},${Y + 60 + k * 48}Q${X + Wd / 2},${Y + 50 + k * 48 + (k % 3) * 8} ${X + Wd - 20},${Y + 62 + k * 48}" stroke="#7a5028" stroke-width="2" opacity=".5" fill="none"/>`).join("")}
      ${border}
      <text x="${X + Wd / 2}" y="${Y + 150}" text-anchor="middle" font-family="Sriracha" font-size="78" fill="#fffaf0" stroke="#fffaf0" stroke-width="12" stroke-linejoin="round" opacity=".55">กฎของยายบัวคำ</text>
      <text x="${X + Wd / 2}" y="${Y + 150}" text-anchor="middle" font-family="Sriracha" font-size="78" fill="#7a1a10">กฎของยายบัวคำ</text>
      ${rows}
      <g id="${id}-nh">${nagaHead(X - 30, Y - 120, 0.75, 1)}</g>
      <g transform="translate(${X + Wd - 90},${Y + H - 10})"><g id="${id}-gl">${[0, 1, 2, 3, 4].map((k) => `<circle cx="0" cy="${k * 26}" r="13" fill="${k % 2 ? "#fff4d8" : "#f8d040"}" ${O(2)}/>`).join("")}<path d="M-10,140l10,30l10,-30z" fill="#c8302a"/></g></g>
      </g></g></g>`);
    tl.set(`#${id}`, { opacity: 1 }, t0);
    tl.fromTo(`#${id}-m`, { y: -1100 }, { y: 0, duration: 0.5, ease: "power3.out", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: 5, svgOrigin: `540 -60` }, { rotation: 0, svgOrigin: `540 -60`, duration: 1.5, ease: "elastic.out(1, 0.32)", immediateRender: false }, t0 + 0.35);
    tl.fromTo(`#${id}-sw`, { rotation: 0, svgOrigin: `540 -60` }, { rotation: 0.7, svgOrigin: `540 -60`, duration: 1.3, repeat: Math.ceil(dur / 1.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 1.85);
    tl.fromTo(`#${id}-gl`, { rotation: -10, svgOrigin: "0 0" }, { rotation: 10, svgOrigin: "0 0", duration: 0.8, repeat: Math.ceil(dur / 0.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.4);
    if (document.getElementById(`${id}-hl`)) tl.fromTo(`#${id}-hl`, { scaleX: 0, svgOrigin: `${X + 84} ${rowY(act)}` }, { scaleX: 1, svgOrigin: `${X + 84} ${rowY(act)}`, duration: 0.5, ease: "power2.inOut", immediateRender: false }, t0 + (o.at ?? 0.7));
    tl.to(`#${id}-m`, { y: -900, duration: 0.3, ease: "power2.in", immediateRender: false }, t0 + dur - 0.3);
  };

  // ---------------- cast ----------------
  const { LINE, dk } = Rig2;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const lampBand = `<path d="M-60,-588Q0,-604 60,-588" stroke="#2a2a30" stroke-width="10" fill="none"/><rect x="-20" y="-616" width="40" height="28" rx="8" fill="#2a2a30" ${ln(2.4)}/><circle cx="0" cy="-602" r="10" fill="#fffbe8"/>`;
  const spiky = (c) => `<path d="M-48,-552C-58,-600 -40,-624 -22,-626L-36,-644L-10,-632L-4,-658L12,-632L28,-654L32,-628Q58,-620 52,-552Q46,-576 30,-586Q12,-592 -6,-586Q-26,-590 -38,-576Q-46,-564 -48,-552Z" fill="${c}" ${ln()}/>`;
  const petch = { skin: "#c88a5a", iris: "#2a1a10", blush: 0.4, hair: { c: "#1a1410", s: "#000", sh: "#5a4a40", front: (x) => spiky("#1a1410") + lampBand },
    top: { kind: "shirt", c: "#2a2a30", sleeve: "short", neck: "crew", trim: "#1a1a20" }, print: `<path d="M-30,-450h60" stroke="#e8c84a" stroke-width="8"/>`, bottom: { kind: "shorts", c: "#6a6a54" }, feet: { kind: "sneaker", c: "#e8e8e8", sole: "#aaa" } };
  const puifai = { skin: "#e8b890", iris: "#2a1a10", lash: true, blush: 0.7, lip: "#d0645a",
    hair: { c: "#1e140f", s: "#0a0604", sh: "#5a4034", front: (x) => `<path d="M-50,-552C-58,-616 -16,-632 6,-630C36,-628 58,-606 52,-552Q46,-584 22,-594Q0,-602 -22,-592Q-42,-580 -50,-552Z" fill="#1e140f" ${ln()}/><circle cx="-56" cy="-560" r="20" fill="#1e140f" ${ln()}/><circle cx="58" cy="-560" r="20" fill="#1e140f" ${ln()}/>` },
    top: { kind: "coat", c: "#f0c83a", sleeve: "long", trim: "#c8a02a" }, print: `<path d="M-50,-480q50,30 100,0" stroke="#c8a02a" stroke-width="6" fill="none"/>`, bottom: { kind: "shorts", c: "#3a5a8a" }, feet: { kind: "sandal", c: "#e85a8a" },
    extra: `<circle cx="70" cy="-330" r="6" fill="#7aff9a" opacity=".9"/>` };
  const yai = { skin: "#c89a72", iris: "#3a2418", lash: true, blush: 0.3, lip: "#a84a4a",
    hair: { c: "#d8d4cc", s: "#9a968e", sh: "#fff", front: (x) => `<path d="M-48,-552C-54,-610 -16,-626 4,-626C30,-624 52,-606 48,-552Q42,-578 26,-588Q8,-596 -12,-588Q-34,-580 -48,-552Z" fill="#d8d4cc" ${ln()}/>`, back: (x) => `<circle cx="30" cy="-596" r="26" fill="#c8c4bc" ${ln()}/>` },
    top: { kind: "blouse", c: "#f4f0e4", sleeve: "elbow", trim: "#d8d0c0" }, print: `<path d="M-60,-490L50,-380" stroke="#c8902a" stroke-width="18"/>`, bottom: { kind: "sarong", c: "#7a3a5a", band: "#c8902a", band2: "#c8902a" }, feet: { kind: "sandal", c: "#5a3a2a" } };
  const saeng = { skin: "#9a6a44", iris: "#2a1a10", blush: 0.2, hair: { c: "#3a3430", s: "#1a1814", sh: "#7a7068", front: (x) => `<path d="M-54,-560C-60,-620 -20,-640 0,-640C40,-640 64,-616 56,-560L74,-560Q70,-596 0,-600Q-70,-596 -74,-560Z" fill="#6a6a4a" ${ln()}/>` },
    top: { kind: "shirt", c: "#8a8a5a", sleeve: "long", neck: "collar", collar: "#7a7a4a", button: "#4a4a2a", trim: "#6a6a40" }, bottom: { kind: "jeans", c: "#4a4a3a" }, feet: { kind: "boot", c: "#2a2018" },
    face: `<path d="M-30,-500q30,14 60,0" stroke="#8a8a8a" stroke-width="5" fill="none"/>` };
  Object.assign(Rig.CAST, { petch: { v2: petch }, puifai: { v2: puifai }, yai: { v2: yai }, saeng: { v2: saeng },
    petchPhone: { v2: petch, hand: `<g transform="translate(0,118) rotate(-10)"><rect x="-20" y="-40" width="40" height="76" rx="7" fill="#1a1c22" ${ln(2.2)}/><rect x="-15" y="-34" width="30" height="62" rx="4" fill="#5a7080"/><circle cx="0" cy="20" r="5" fill="#e2382e"/></g>`, keep: "F" } });
  const M = Rig.MODES;
  M.wade = M.wade || ((u) => ({ ...M.idle(u, {}), uaF: -60, faF: -70, uaB: -50, faB: -60 }));
  M.breath = (u) => { const k = Math.min(1, u / 0.5); return { ...M.idle(u, {}), uaF: -40 - 60 * k, faF: -40, uaB: -30 - 50 * k, faB: -40, torso: -8 * k + 14 * Math.max(0, u - 0.6), head: -14 * k + 20 * Math.max(0, Math.min(1, u - 0.6)), bodyY: 10 * Math.max(0, u - 0.6) * 20 }; };
  M.tug = (u) => { const j = Math.sin(u * 23) * 2; return { ...M.idle(u, {}), uaF: -96 + j, faF: -6, uaB: -86 - j, faB: -10, torso: -18 + j * 0.4, head: -6, thF: -30, shF: 30, bodyY: 16 }; };
  M.filmUp = (u) => ({ ...M.idle(u, {}), uaF: -150 + 3 * Math.sin(u * 2), faF: -20, head: -14, torso: -4 });
})();
