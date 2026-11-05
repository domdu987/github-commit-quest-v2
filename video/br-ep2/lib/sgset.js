// Rod Mai Club · new-look sets (owner 4 Nov 2026: the reference series' depth, light and colour + the นิวเคลียร์ลงกรุงเทพฯ night).
// Painted for both frames: every layer runs x −1800…3000 and well below the ground, so a 9:16 or a 16:9 camera never finds an edge.
//   Sets.sgSoi(L, o)   ซอยตีสอง: the far-side shophouse row with shutters down (mid), condo towers in haze (far), a wet road,
//                      ยายจันทร์'s cart (x 290…690, counter top 1090, glass case left, pot right at 588, bulb at 540,790; the cart stands in FRONT of anyone behind it),
//                      a folding table under a printed cloth (x 760…990, top 1178), red stools (seat 1265 at x 1066, an empty one
//                      at 698 with a cat asleep on it), the chalkboard (x 1236), a sodium street lamp (head at 1060,300).
//                      Ground: near things stand on y 1400 (you, the stool, the table), the cart on 1386.
//                      o.id (unique per shot) · o.rows (chalkboard lines) · o.noCat · o.cloth:false
//                      ids: #id-steam (pot steam, glow), #id-bowl (the steam over the bowl), #id-moths, #id-bulb
//   Sgs.steam(tl, sid, t0, dur)   keeps both plumes of steam rising and fading for the length of a shot
(function () {
  const f = (v) => (+v).toFixed(1);
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const T = (x, y, size, text, o = {}) => `<text x="${f(x)}" y="${f(y)}" text-anchor="${o.anchor || "middle"}" font-family="${o.font || "Kanit"}" font-weight="${o.w || 800}" font-size="${size}" fill="${o.fill || "#222"}"${o.op ? ` opacity="${o.op}"` : ""}${o.ls ? ` letter-spacing="${o.ls}"` : ""}>${text}</text>`;

  Sets.DEFS += `
    <linearGradient id="sgNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060a1a"/><stop offset=".38" stop-color="#101838"/><stop offset=".62" stop-color="#262a4c"/><stop offset=".74" stop-color="#3c3350"/><stop offset="1" stop-color="#2a2338"/></linearGradient>
    <linearGradient id="sgHaze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a4a68" stop-opacity="0"/><stop offset="1" stop-color="#8a6a6a" stop-opacity=".55"/></linearGradient>
    <linearGradient id="sgSteel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a929a"/><stop offset=".22" stop-color="#c4cbd2"/><stop offset=".5" stop-color="#9aa2aa"/><stop offset=".8" stop-color="#b4bcc4"/><stop offset="1" stop-color="#7c848c"/></linearGradient>
    <linearGradient id="sgPot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7c8288"/><stop offset=".3" stop-color="#d6dce0"/><stop offset=".55" stop-color="#a2a8ae"/><stop offset="1" stop-color="#6c7278"/></linearGradient>
    <linearGradient id="sgGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8eef6" stop-opacity=".42"/><stop offset=".5" stop-color="#a8c8d8" stop-opacity=".16"/><stop offset="1" stop-color="#d8eef6" stop-opacity=".34"/></linearGradient>
    <linearGradient id="sgCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc47a" stop-opacity=".5"/><stop offset=".55" stop-color="#ffab5a" stop-opacity=".16"/><stop offset="1" stop-color="#ff9a4a" stop-opacity="0"/></linearGradient>
    <linearGradient id="sgStreak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffbf73" stop-opacity=".55"/><stop offset="1" stop-color="#ffbf73" stop-opacity="0"/></linearGradient>
    <linearGradient id="sgStreakW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe6b0" stop-opacity=".5"/><stop offset="1" stop-color="#ffe6b0" stop-opacity="0"/></linearGradient>
    <radialGradient id="sgLamp"><stop offset="0" stop-color="#fff2d0" stop-opacity="1"/><stop offset=".12" stop-color="#ffcf8a" stop-opacity=".85"/><stop offset=".45" stop-color="#ffa858" stop-opacity=".22"/><stop offset="1" stop-color="#ff9a4a" stop-opacity="0"/></radialGradient>
    <radialGradient id="sgBulb"><stop offset="0" stop-color="#fffbe8" stop-opacity="1"/><stop offset=".14" stop-color="#ffe6ac" stop-opacity=".8"/><stop offset=".5" stop-color="#ffc77a" stop-opacity=".2"/><stop offset="1" stop-color="#ffb05a" stop-opacity="0"/></radialGradient>
    <radialGradient id="sgPool"><stop offset="0" stop-color="#ffb867" stop-opacity=".75"/><stop offset=".55" stop-color="#ffa050" stop-opacity=".25"/><stop offset="1" stop-color="#ff9a4a" stop-opacity="0"/></radialGradient>
    <radialGradient id="sgPoolW"><stop offset="0" stop-color="#ffe2a8" stop-opacity=".7"/><stop offset=".55" stop-color="#ffd08a" stop-opacity=".22"/><stop offset="1" stop-color="#ffc070" stop-opacity="0"/></radialGradient>
    <radialGradient id="sgStore"><stop offset="0" stop-color="#d8fff0" stop-opacity=".8"/><stop offset=".4" stop-color="#9ae8d0" stop-opacity=".25"/><stop offset="1" stop-color="#7ad8c0" stop-opacity="0"/></radialGradient>
    <radialGradient id="sgWin"><stop offset="0" stop-color="#ffcf8a" stop-opacity=".55"/><stop offset="1" stop-color="#ffcf8a" stop-opacity="0"/></radialGradient>`;

  // ---------------- far: condo towers in the city haze ----------------
  function towers(r) {
    let s = "";
    const cols = ["#161c38", "#1a2140", "#1d2444", "#141a32"];
    for (let x = -1900; x < 3200; ) {
      const w = 120 + r() * 170, h = 360 + r() * 620, top = 1180 - h, c = cols[Math.floor(r() * cols.length)];
      s += `<rect x="${f(x)}" y="${f(top)}" width="${f(w)}" height="${f(h + 1500)}" fill="${c}"/>`;
      if (r() < 0.4) s += `<rect x="${f(x + w * 0.3)}" y="${f(top - 26)}" width="${f(w * 0.4)}" height="28" fill="${c}"/>`;
      for (let yy = top + 26; yy < 1120; yy += 30) for (let xx = x + 14; xx < x + w - 18; xx += 26)
        if (r() < 0.07) s += `<rect x="${f(xx)}" y="${f(yy)}" width="12" height="15" fill="${r() < 0.7 ? "#e8b870" : "#a8c8e8"}" opacity="${f(0.35 + r() * 0.45)}"/>`;
      if (h > 820) s += `<circle cx="${f(x + w / 2)}" cy="${f(top - 4)}" r="5" fill="#ff4a3a"/><circle cx="${f(x + w / 2)}" cy="${f(top - 4)}" r="16" fill="#ff4a3a" opacity=".25"/>`;
      x += w + 10 + r() * 60;
    }
    return s;
  }

  // ---------------- mid: the far-side shophouse row, shutters down ----------------
  const SIGNS = [["ซ่อมมือถือ", "#2a6a9a"], ["ร้านตัดผม", "#9a3a3a"], ["เจริญพาณิชย์", "#b8862e"], ["ข้าวมันไก่", "#3a7a5a"], ["วัสดุก่อสร้าง", "#6a4a8a"], ["ร้านยา", "#2a7a7a"], ["โชห่วย", "#a85a2a"]];
  function shophouses(r) {
    let s = "", k = 0;
    const walls = ["#3a3d54", "#423c52", "#3a4552", "#4a4248", "#363c4e"];
    for (let x = -1900; x < 3100; x += 300, k++) {
      const w = 300, top = 300 + Math.floor(r() * 3) * 34, wall = walls[k % walls.length], G = 1160;
      if (x > 2050 && x < 2400) { // the one shop still open: a minimart's cool spill
        s += `<rect x="${x}" y="${top}" width="${w}" height="${G - top}" fill="${wall}"/>
          <rect x="${x + 16}" y="${G - 290}" width="${w - 32}" height="290" fill="#cfeee4"/>
          ${[0, 1, 2, 3].map((i) => `<rect x="${x + 36 + i * 62}" y="${G - 250}" width="40" height="230" fill="#7aa89a" opacity=".55"/>`).join("")}
          <rect x="${x + 6}" y="${G - 352}" width="${w - 12}" height="56" fill="#1f6a5e"/>${T(x + w / 2, G - 312, 34, "มินิมาร์ท 24 ชม.", { fill: "#e8fff6", w: 800 })}`;
      } else {
        s += `<rect x="${x}" y="${top}" width="${w}" height="${G - top}" fill="${wall}"/>
          <rect x="${x + 18}" y="${G - 300}" width="${w - 36}" height="300" fill="#4c5262"/>
          ${[...Array(28)].map((_, i) => `<path d="M${x + 18},${G - 296 + i * 10.6}H${x + w - 18}" stroke="#5e6474" stroke-width="3"/>`).join("")}
          <rect x="${x + 18}" y="${G - 22}" width="${w - 36}" height="22" fill="#3a3e4c"/><rect x="${x + w / 2 - 22}" y="${G - 26}" width="44" height="12" rx="3" fill="#2e323e"/>`;
        const [txt, sc] = SIGNS[k % SIGNS.length];
        s += `<rect x="${x + 10}" y="${G - 362}" width="${w - 20}" height="54" rx="4" fill="${sc}" opacity=".85"/>${T(x + w / 2, G - 323, 30, txt, { fill: "#efe6d2", w: 800, op: 0.8 })}`;
      }
      // upper floors: windows (some lit, curtains), an AC unit, a balcony grille, plants, laundry
      [G - 600, G - 860].forEach((wy, fl) => {
        if (wy < top + 40) return;
        const lit = r() < 0.32, wc = lit ? "#e8b26a" : "#232838";
        s += `<rect x="${x + 40}" y="${wy}" width="${w - 80}" height="170" fill="${wc}"/>`;
        if (lit) s += `<path d="M${x + 40},${wy}h${(w - 80) * 0.36}q-10,90 6,170h-${(w - 80) * 0.36 + 6}z" fill="#b8604a" opacity=".85"/><rect x="${x + 20}" y="${wy - 30}" width="${w - 40}" height="230" fill="url(#sgWin)"/>`;
        s += [...Array(9)].map((_, i) => `<path d="M${x + 52 + i * ((w - 104) / 8)},${wy}V${wy + 170}" stroke="#2a2e3a" stroke-width="4"/>`).join("");
        s += `<rect x="${x + 34}" y="${wy + 170}" width="${w - 68}" height="12" fill="#2e3242"/>`;
        if (r() < 0.6) s += `<g transform="translate(${x + w - 96},${wy + 186})"><rect width="70" height="50" rx="4" fill="#9aa0a8"/><circle cx="24" cy="25" r="17" fill="#7a8088"/><circle cx="24" cy="25" r="5" fill="#5a6068"/><rect x="48" y="10" width="14" height="30" fill="#868c94"/></g>`;
        if (r() < 0.5) s += [0, 1, 2].map((i) => `<g transform="translate(${x + 60 + i * 30},${wy + 170})"><rect x="-10" y="-22" width="20" height="22" rx="3" fill="#7a4a3a"/><path d="M0,-22q-16,-24 -4,-40M0,-22q14,-26 6,-44M0,-22q2,-30 -2,-36" stroke="#3a6a4a" stroke-width="6" fill="none" stroke-linecap="round"/></g>`).join("");
        if (fl === 0 && r() < 0.4) s += `<path d="M${x + 44},${wy - 14}Q${x + w / 2},${wy - 2} ${x + w - 44},${wy - 14}" stroke="#2a2e3a" stroke-width="2" fill="none"/>${[0, 1, 2].map((i) => `<rect x="${x + 70 + i * 60}" y="${wy - 12}" width="34" height="${30 + i * 6}" fill="${["#c8a86a", "#6a8aa8", "#a86a6a"][i]}" opacity=".75"/>`).join("")}`;
      });
      s += `<rect x="${x - 6}" y="${top - 16}" width="${w + 12}" height="20" fill="#2a2e3e"/><rect x="${x - 4}" y="${top}" width="14" height="${G - top}" fill="#2e3242"/>`;
      if (r() < 0.35) s += `<g transform="translate(${x + 200},${top - 16})"><rect x="-34" y="-70" width="68" height="70" rx="8" fill="#5a6a7a"/><rect x="-30" y="-2" width="60" height="6" fill="#3a4250"/><path d="M-26,0v-6M26,0v-6" stroke="#3a4250" stroke-width="5"/></g>`;
    }
    // far sidewalk, curb, the power poles and their cables
    s += `<rect x="-2200" y="1158" width="5600" height="40" fill="#5a5a68"/><rect x="-2200" y="1194" width="5600" height="12" fill="#6e6e7c"/><rect x="-2200" y="1204" width="5600" height="1500" fill="#2a2934"/>`;
    [-1050, 120, 1350, 2560].forEach((px) => {
      s += `<rect x="${px - 9}" y="140" width="18" height="1050" fill="#4a4a54"/><rect x="${px - 70}" y="200" width="140" height="10" fill="#3a3a44"/><rect x="${px - 50}" y="250" width="100" height="8" fill="#3a3a44"/>
        <g transform="translate(${px + 14},300)"><rect width="40" height="64" rx="6" fill="#5c6470"/><rect x="6" y="-8" width="28" height="10" fill="#4a5260"/></g>`;
    });
    for (let i = 0; i < 6; i++) {
      const y0 = 200 + i * 16 + (i % 2) * 40, sag = 60 + i * 18;
      s += `<path d="M-2200,${y0}${[-1050, 120, 1350, 2560, 3700].map((px, j, a) => { const x0 = j ? a[j - 1] : -2200; return `Q${(x0 + px) / 2},${y0 + sag} ${px},${y0}`; }).join("")}" stroke="#141620" stroke-width="${i < 2 ? 3.4 : 2.4}" fill="none"/>`;
    }
    s += `<path d="M90,232q-30,40 -10,80q14,30 -16,60" stroke="#141620" stroke-width="2.4" fill="none"/>`;
    return s;
  }

  // ---------------- set pieces ----------------
  function cart(id) {
    const W = (cx) => `<g transform="translate(${cx},1338)"><circle r="48" fill="#22252c"/><circle r="40" fill="#3a3e46"/>${[...Array(12)].map((_, i) => `<path d="M0,0L${f(38 * Math.cos(i * Math.PI / 6))},${f(38 * Math.sin(i * Math.PI / 6))}" stroke="#9aa0a8" stroke-width="1.6"/>`).join("")}<circle r="8" fill="#9aa0a8"/><path d="M-40,0A40,40 0 0,1 0,-40" stroke="#5a5e66" stroke-width="3" fill="none"/></g>`;
    return `<g id="${id}-cart" class="act-front">
      <rect x="452" y="1262" width="74" height="124" rx="26" fill="#3a6aa8"/><rect x="452" y="1262" width="22" height="124" rx="11" fill="#2a4a80"/><rect x="474" y="1244" width="30" height="22" rx="5" fill="#6a7078"/>
      ${W(352)}${W(628)}
      <rect x="300" y="1100" width="380" height="198" fill="url(#sgSteel)"/>
      <path d="M300,1100H680V1118H300Z" fill="#6a7178"/><path d="M490,1118V1298" stroke="#6f767e" stroke-width="3"/>
      <rect x="318" y="1136" width="154" height="140" rx="6" fill="#aab2ba" opacity=".55"/><rect x="508" y="1136" width="154" height="140" rx="6" fill="#aab2ba" opacity=".55"/>
      <rect x="456" y="1196" width="10" height="34" rx="4" fill="#5a6168"/><rect x="514" y="1196" width="10" height="34" rx="4" fill="#5a6168"/>
      <rect x="286" y="1086" width="408" height="18" rx="4" fill="#d4dade"/><rect x="286" y="1100" width="408" height="5" fill="#8a9298"/>
      <path d="M300,1086V930H436V1086" fill="url(#sgGlass)"/><path d="M300,1086V930H436V1086" stroke="#c8d0d6" stroke-width="7" fill="none"/>
      <path d="M300,1006H436" stroke="#c8d0d6" stroke-width="5"/>
      ${[0, 1, 2].map((i) => `<ellipse cx="${334 + i * 6}" cy="${1076 - i * 14}" rx="30" ry="9" fill="#f2efe8"/><path d="M${306 + i * 10},${1076 - i * 14}q30,16 60,0" fill="#e6e2da"/>`).join("")}
      <ellipse cx="400" cy="1074" rx="30" ry="10" fill="#c87a4a"/><ellipse cx="394" cy="1069" rx="11" ry="5" fill="#e8c46a"/>
      <ellipse cx="340" cy="994" rx="28" ry="9" fill="#f2efe8"/><ellipse cx="402" cy="996" rx="24" ry="8" fill="#d8b070"/>
      ${T(368, 976, 38, "ข้าวต้ม", { fill: "#d8352a", w: 900 })}${T(368, 1054, 18, "ตีหนึ่ง – ตีสี่", { fill: "#d8352a", w: 800, op: 0.85 })}
      <path d="M512,962Q510,1084 522,1088H654Q666,1084 664,962Z" fill="url(#sgPot)"/><ellipse cx="588" cy="962" rx="80" ry="14" fill="#5e646a"/><ellipse cx="588" cy="960" rx="72" ry="10" fill="#efe6d2"/>
      <path d="M510,1000H666M510,1040H666" stroke="#8a9096" stroke-width="2.4" opacity=".7"/><rect x="498" y="990" width="16" height="12" rx="5" fill="#5e646a"/><rect x="662" y="990" width="16" height="12" rx="5" fill="#5e646a"/>
      <path d="M296,1100V712Q296,694 314,694H540" stroke="#5a5e66" stroke-width="10" fill="none" stroke-linecap="round"/>
      <path d="M540,694V758" stroke="#2a2a30" stroke-width="3"/><rect x="532" y="752" width="16" height="16" rx="3" fill="#3a3a40"/>
      <g id="${id}-bulb"><ellipse cx="540" cy="790" rx="17" ry="22" fill="#fff7dc"/><path d="M532,786q8,-10 16,0" stroke="#e8a040" stroke-width="2.4" fill="none"/></g>
      <g transform="translate(296,840)"><path d="M0,0q-12,4 -14,24q10,22 28,0q-2,-20 -14,-24z" fill="#e88aa8" opacity=".9"/><path d="M0,0v-6" stroke="#ccc" stroke-width="2"/></g>
      </g>`;
  }
  function table(id, o) {
    const cl = o.cloth === false ? "#cfd6da" : "url(#sgCloth)";
    return `<g id="${id}-table" class="act-front">
      <path d="M786,1236L776,1400M966,1236L978,1400M790,1240L956,1240" stroke="#9aa0a6" stroke-width="7" stroke-linecap="round"/>
      <path d="M754,1170H994L1000,1244Q984,1252 968,1244Q952,1254 936,1244Q920,1254 904,1244Q888,1254 872,1244Q856,1254 840,1244Q824,1254 808,1244Q792,1254 776,1244Q760,1252 748,1244Z" fill="${cl}"/>
      <path d="M754,1170H994L1000,1244Q984,1252 968,1244Q952,1254 936,1244Q920,1254 904,1244Q888,1254 872,1244Q856,1254 840,1244Q824,1254 808,1244Q792,1254 776,1244Q760,1252 748,1244Z" fill="#1c2030" opacity=".16"/>
      <rect x="752" y="1164" width="244" height="12" rx="4" fill="#efeae0"/>
      <g transform="translate(796,1164)"><rect x="-26" y="-40" width="52" height="40" rx="5" fill="#f0a2b6"/><rect x="-26" y="-40" width="14" height="40" fill="#d8869c"/><path d="M-6,-40q6,-16 14,-4q-4,6 -14,4z" fill="#fff"/></g>
      <g transform="translate(952,1164)"><rect x="-40" y="-8" width="80" height="8" rx="3" fill="#b8bec4"/><path d="M-36,-8V-56M36,-8V-56M-36,-50H36" stroke="#b8bec4" stroke-width="4"/>
        ${[["#c8352a", -26], ["#efe8da", -9], ["#8a5a2a", 8], ["#d8c86a", 25]].map(([c, x]) => `<rect x="${x - 7}" y="-40" width="14" height="32" rx="4" fill="#e8eef0" opacity=".85"/><rect x="${x - 6}" y="-28" width="12" height="20" rx="3" fill="${c}"/>`).join("")}</g>
      <g transform="translate(880,1164)"><path d="M-46,-30Q-44,0 0,2Q44,0 46,-30Z" fill="#f4f1ea"/><path d="M-46,-30Q-44,0 0,2Q-30,-6 -32,-30Z" fill="#1c2030" opacity=".12"/>
        <ellipse cx="0" cy="-30" rx="46" ry="9" fill="#f7f2e6"/><ellipse cx="0" cy="-30" rx="40" ry="6.4" fill="#e9dcc0"/>
        <path d="M-20,-31q4,-3 8,0M4,-32q4,-3 8,0M-6,-28q4,-3 8,0" stroke="#5a9a4a" stroke-width="3" fill="none" stroke-linecap="round"/><ellipse cx="18" cy="-30" rx="9" ry="4" fill="#c88a5a"/>
        <g transform="translate(30,-34) rotate(28)"><ellipse cx="0" cy="-6" rx="7" ry="10" fill="#e0e4e8"/><rect x="-2.4" y="2" width="4.8" height="40" rx="2" fill="#c3c8cd"/></g></g>
      </g>`;
  }
  const stool = (x, gy, id = "") => `<g${id ? ` id="${id}"` : ""} transform="translate(${x},${gy})">
      <path d="M-40,-132L-52,0H-36L-28,-118H28L36,0H52L40,-132Z" fill="#b82e2a"/><path d="M-40,-132L-52,0H-36L-30,-124Z" fill="#8e1e1c"/>
      <path d="M-22,-96h44M-26,-60h52M-30,-24h60" stroke="#8e1e1c" stroke-width="7" stroke-linecap="round"/>
      <ellipse cx="0" cy="-134" rx="50" ry="11" fill="#d8403a"/><ellipse cx="0" cy="-136" rx="40" ry="6" fill="#e86a5e"/>
      ${[-24, -8, 8, 24].map((dx) => `<ellipse cx="${dx}" cy="-135" rx="4" ry="2" fill="#8e1e1c"/>`).join("")}</g>`;
  const catAsleep = (x, y) => `<g transform="translate(${x},${y})"><path d="M-44,0Q-50,-38 -6,-42Q40,-44 46,-8Q46,2 30,2H-34Q-44,2 -44,0Z" fill="#cf8448"/>
      <path d="M-44,0Q-50,-38 -6,-42Q-30,-30 -30,0Z" fill="#a8642e" opacity=".55"/><path d="M30,-6Q60,-6 52,-30" stroke="#a8642e" stroke-width="10" fill="none" stroke-linecap="round"/>
      <ellipse cx="-30" cy="-22" rx="20" ry="17" fill="#cf8448"/><path d="M-46,-30L-44,-50L-32,-36ZM-24,-36L-14,-50L-14,-30Z" fill="#cf8448"/>
      <path d="M-40,-22q4,3 8,0M-26,-22q4,3 8,0" stroke="#211714" stroke-width="2.4" fill="none" stroke-linecap="round"/><path d="M-30,-14l2,2l2,-2" fill="#a85848"/></g>`;
  function board(id, rows) {
    return `<g id="${id}-board" transform="translate(1236,1398)">
      <path d="M-70,-40L-96,0M70,-40L96,0M-60,-330L-84,0M60,-330L84,0" stroke="#6a4424" stroke-width="10" stroke-linecap="round"/>
      <rect x="-118" y="-420" width="236" height="270" rx="8" fill="#8a5a32"/><rect x="-118" y="-420" width="236" height="16" fill="#a8743e"/><rect x="-106" y="-408" width="212" height="246" rx="4" fill="#2c3832"/>
      <path d="M-96,-300q40,8 96,0" stroke="#e8e4d8" stroke-width="2" opacity=".18" fill="none"/>
      ${T(0, -370, 30, "กฎของร้าน", { font: "Sriracha", w: 400, fill: "#f6d36a" })}
      ${rows.map((t, k) => T(-94, -326 + k * 52, 21, `${k + 1}. ${t}`, { anchor: "start", font: "Sriracha", w: 400, fill: "#f2efe6", op: 0.92 })).join("")}</g>`;
  }
  function lamp() {
    return `<g><rect x="1320" y="236" width="20" height="1166" fill="#3a3c46"/><rect x="1310" y="1360" width="40" height="42" rx="4" fill="#2e3038"/>
      <path d="M1330,286Q1330,252 1296,252H1098" stroke="#3a3c46" stroke-width="14" fill="none" stroke-linecap="round"/>
      <path d="M1000,286H1124L1110,312H1014Z" fill="#4a4c58"/><path d="M1004,286H1120L1116,294H1008Z" fill="#5c5e6a"/>
      <rect x="1350" y="760" width="18" height="120" rx="4" fill="#2e3038"/><path d="M1340,820h18" stroke="#2e3038" stroke-width="6"/>
      <g transform="translate(1302,620)"><rect x="-58" y="0" width="58" height="96" rx="4" fill="#efe6d2" opacity=".9"/><rect x="-54" y="6" width="50" height="22" fill="#d8352a"/>
        ${T(-29, 22, 15, "ห้ามจอด", { fill: "#fff", w: 800 })}${T(-29, 56, 14, "ประกาศ", { fill: "#3a3a40", w: 700, op: 0.7 })}<path d="M-50,66h42M-50,78h36" stroke="#9a9488" stroke-width="3"/></g></g>`;
  }
  function road() {
    return `<rect x="-2200" y="1200" width="5600" height="1500" fill="#23222c"/>
      <rect x="-2200" y="1200" width="5600" height="26" fill="#1c1b24"/>
      <path d="M-2200,1612H3400" stroke="#8a7a4a" stroke-width="7" stroke-dasharray="90 110" opacity=".35"/>
      ${[[-420, 1500, 240], [180, 1680, 320], [760, 1520, 200], [1480, 1590, 260], [2100, 1460, 220]].map(([x, y, w]) => `<path d="M${x},${y}h${w}l-30,26h-${w - 60}z" fill="#2a2934" opacity=".9"/>`).join("")}
      <path d="M560,1460l40,10l30,-6l50,14M1180,1640l30,-8l40,12" stroke="#17161e" stroke-width="3" fill="none"/>
      <g transform="translate(1520,1540)"><ellipse rx="96" ry="16" fill="#3a3a44"/><ellipse rx="86" ry="12" fill="#2c2c36"/>${[-60, -30, 0, 30, 60].map((d) => `<path d="M${d - 10},-8L${d + 10},8" stroke="#3e3e48" stroke-width="3"/>`).join("")}</g>
      <rect x="-300" y="1212" width="120" height="16" rx="3" fill="#15141b"/>${[...Array(7)].map((_, i) => `<path d="M${-292 + i * 16},1214v12" stroke="#33323c" stroke-width="3"/>`).join("")}
      ${[[880, 1500, 170, 16], [330, 1450, 120, 11], [1180, 1700, 220, 20], [-80, 1590, 160, 14]].map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#171822"/><ellipse cx="${x - rx * 0.2}" cy="${y - ry * 0.3}" rx="${rx * 0.5}" ry="${ry * 0.35}" fill="#2e3448" opacity=".7"/>`).join("")}`;
  }

  Sets.sgSoi = (L, o = {}) => {
    const id = o.id || "sgs", r = mk(o.seed || 11);
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#2a2338"/><rect x="-3000" y="-1200" width="8000" height="2600" fill="url(#sgNight)"/>
      ${[...Array(60)].map(() => `<circle cx="${f(-1800 + r() * 4800)}" cy="${f(-400 + r() * 900)}" r="${f(0.8 + r() * 1.6)}" fill="#e8ecff" opacity="${f(0.25 + r() * 0.5)}"/>`).join("")}`);
    put(L.far, `<g id="${id}-far">${towers(mk(5))}</g><rect x="-2400" y="600" width="6200" height="700" fill="url(#sgHaze)"/><rect x="-2400" y="1290" width="6200" height="1600" fill="#1e1d28"/>`);
    put(L.mid, `<g id="${id}-row">${shophouses(mk(23))}</g><rect x="-2400" y="820" width="6200" height="400" fill="url(#sgHaze)" opacity=".55"/>`);
    let s = road() + lamp() + board(id, o.rows || ["กินให้อิ่มก่อน แล้วค่อยคิด", "ห้ามตัดสินใจตอนตีสอง", "นับสิ่งที่ทำได้แล้ว"]);
    s += stool(698, 1396) + (o.noCat ? "" : catAsleep(706, 1258)) + table(id, o) + stool(1066, 1400, `${id}-stool`) + cart(id);
    put(L.set, `<g id="${id}-world">${s}</g>`);
    // foreground: the tail of a parked scooter (left), a potted plant (right), cables across the top
    put(L.fg, `<g opacity=".95"><path d="M-520,1500Q-520,1300 -360,1240H-120Q-40,1250 -20,1330L0,1520Q-60,1640 -260,1640H-460Z" fill="#14161e"/>
        <rect x="-60" y="1300" width="44" height="26" rx="6" fill="#ff4a3a"/><circle cx="-180" cy="1640" r="120" fill="#0c0d12"/></g>
      <g transform="translate(1540,1760)">${[[-60, -460, -40], [10, -560, 10], [70, -420, 40], [-120, -330, -70], [120, -300, 70]].map(([dx, dy, rot]) => `<path d="M0,0Q${dx - 60},${dy * 0.5} ${dx},${dy}Q${dx + 70},${dy * 0.55} 0,0Z" fill="#1c3a2c" transform="rotate(${rot * 0.2})"/>`).join("")}
        <rect x="-90" y="-20" width="180" height="200" rx="16" fill="#3a2a24"/></g>
      <path d="M-900,120Q600,260 2400,90M-900,170Q500,330 2400,150" stroke="#08090d" stroke-width="7" fill="none"/>`);
    // light: the sodium lamp (lens, cone, pools, wet streaks), the cart's bulb, the minimart down the road, moths
    put(L.glow, `<g style="mix-blend-mode:screen">
      <path d="M1012,300H1112L1560,1470H560Z" fill="url(#sgCone)" style="filter:blur(14px)"/>
      <circle cx="1062" cy="306" r="300" fill="url(#sgLamp)"/><ellipse cx="1062" cy="300" rx="56" ry="10" fill="#fff4d8"/>
      <ellipse cx="1060" cy="1440" rx="620" ry="150" fill="url(#sgPool)" opacity=".85"/>
      <path d="M1036,1430H1088L1106,1880H1018Z" fill="url(#sgStreak)" style="filter:blur(8px)"/><path d="M856,1488H904L912,1620H848Z" fill="url(#sgStreak)" style="filter:blur(5px)" opacity=".8"/>
      <circle cx="540" cy="790" r="250" fill="url(#sgBulb)"/><ellipse cx="560" cy="1092" rx="250" ry="34" fill="url(#sgPoolW)"/><ellipse cx="560" cy="1420" rx="330" ry="70" fill="url(#sgPoolW)" opacity=".7"/>
      <path d="M520,1416H562L576,1640H508Z" fill="url(#sgStreakW)" style="filter:blur(6px)"/>
      <ellipse cx="2240" cy="1180" rx="520" ry="200" fill="url(#sgStore)" opacity=".7"/>
      <g id="${id}-moths">${[...Array(14)].map(() => { const a = r() * 6.28, d = 30 + r() * 150; return `<circle cx="${f(1062 + Math.cos(a) * d)}" cy="${f(330 + Math.sin(a) * d * 0.6)}" r="${f(1.6 + r() * 1.8)}" fill="#fff0d0" opacity="${f(0.5 + r() * 0.5)}"/>`; }).join("")}</g>
      <g id="${id}-steam" style="filter:blur(3px)">${[0, 1, 2, 3].map((k) => `<path id="${id}-st${k}" d="M${552 + k * 22},950q-26,-40 0,-80t0,-80t0,-80" stroke="#fff6e8" stroke-width="${16 - k * 2}" fill="none" stroke-linecap="round" opacity=".5"/>`).join("")}</g>
      <g id="${id}-bowl" style="filter:blur(2.5px)">${[0, 1].map((k) => `<path id="${id}-bw${k}" d="M${870 + k * 22},1126q-14,-24 0,-48t0,-48" stroke="#fff6e8" stroke-width="8" fill="none" stroke-linecap="round" opacity=".45"/>`).join("")}</g></g>`);
  };

  const Sgs = {};
  Sgs.steam = (tl, sid, t0, dur) => {
    [0, 1, 2, 3].forEach((k) => tl.fromTo(`#${sid}-st${k}`, { y: 0, opacity: 0.55 }, { y: -90, opacity: 0, duration: 1.6, repeat: Math.ceil(dur / 1.6), ease: "none", immediateRender: false }, t0 + k * 0.4));
    [0, 1].forEach((k) => tl.fromTo(`#${sid}-bw${k}`, { y: 0, opacity: 0.5 }, { y: -50, opacity: 0, duration: 1.3, repeat: Math.ceil(dur / 1.3), ease: "none", immediateRender: false }, t0 + k * 0.6));
  };
  window.Sgs = Sgs;
})();
