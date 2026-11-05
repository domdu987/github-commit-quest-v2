// "เห็ดปอบ" v2 — EP.3 pieces: the doctor's whiteboard with the course of the poisoning drawn in marker, ยายคำ seen from behind at
// the bedside, and her feet on the ward floor.
//   Sets.board2(L, o)       the ward wall with a whiteboard: the symptom curve #id-sick (dash-drawn), the liver curve #id-liver,
//                           labels #id-l1 "ดีขึ้นชั่วคราว" #id-l2 "ตับแย่ลง" #id-l3 "แม้กินดอกเดียว", stage marks; o.time
//   Pop2.yaiBack(x, y, s, id)   ยาย sitting on a stool, back to camera: grey bun with its pin, lace blouse, sash, purple sarong; #id-head
//   Sets.feet2(L, o)        the ward floor at night, close: her bare feet muddy to the ankle, toes far too long (#id-toes curl)
(function () {
  const { mk, f1, put, blob } = Pop2;
  const LN = "#3a2622";

  Sets.DEFS += `
    <linearGradient id="bdBoard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbfcfa"/><stop offset="1" stop-color="#e6ebe8"/></linearGradient>
    <linearGradient id="ftFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4a48"/><stop offset="1" stop-color="#1e2826"/></linearGradient>
    <radialGradient id="ftMoon" cx=".6" cy=".3" r=".8"><stop offset="0" stop-color="#a8c4ff" stop-opacity=".35"/><stop offset="1" stop-color="#a8c4ff" stop-opacity="0"/></radialGradient>`;

  // ---------------- the whiteboard ----------------
  function board2(L, o = {}) {
    const id = o.id || "bd", r = mk(o.seed || 5), dawn = o.time !== "night";
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#${dawn ? "wdWallD" : "wdWallN"})"/>`);
    let s = `<rect x="-1300" y="1560" width="3700" height="1600" fill="url(#wdFloor)"/>`;
    // the board on the wall, aluminium frame, a marker tray
    s += `<g transform="translate(540,880)"><rect x="-470" y="-560" width="940" height="1120" rx="10" fill="#000" opacity=".25" transform="translate(12,18)"/><rect x="-470" y="-560" width="940" height="1120" rx="10" fill="#c8ccd0" stroke="#8a8e92" stroke-width="6"/>
      <rect x="-446" y="-536" width="892" height="1072" fill="url(#bdBoard)"/><path d="M-440,-500L-200,-520L300,-480" stroke="#e0e6e4" stroke-width="40" opacity=".5"/>
      <rect x="-300" y="560" width="600" height="30" rx="6" fill="#a8acb0"/><rect x="-220" y="540" width="90" height="22" rx="8" fill="#2a6ad8"/><rect x="-100" y="540" width="90" height="22" rx="8" fill="#e8302a"/>
      <text x="0" y="-440" text-anchor="middle" font-family="Mali" font-weight="700" font-size="56" fill="#1a3a8a">พิษเห็ดระโงก</text>
      <path d="M-380,300V-340M-380,300H400" stroke="#2a2a2a" stroke-width="6" stroke-linecap="round"/><path d="M-392,-320l12,-24l12,24M384,288l24,12l-24,12" stroke="#2a2a2a" stroke-width="6" fill="none" stroke-linecap="round"/>
      <text x="-370" y="350" font-family="Mali" font-weight="600" font-size="34" fill="#3a3a3a">กิน</text><text x="-120" y="350" font-family="Mali" font-weight="600" font-size="34" fill="#3a3a3a">6 ชม.</text><text x="120" y="350" font-family="Mali" font-weight="600" font-size="34" fill="#3a3a3a">1 วัน</text><text x="300" y="350" font-family="Mali" font-weight="600" font-size="34" fill="#3a3a3a">2–3 วัน</text>
      <path d="M-140,300V-300M100,300V-300" stroke="#9aa0a4" stroke-width="3" stroke-dasharray="14 12"/>
      <text x="-260" y="-290" text-anchor="middle" font-family="Mali" font-weight="600" font-size="30" fill="#6a6a6a">ระยะ 1</text><text x="-20" y="-290" text-anchor="middle" font-family="Mali" font-weight="600" font-size="30" fill="#6a6a6a">ระยะ 2 (18–36 ชม.)</text><text x="250" y="-290" text-anchor="middle" font-family="Mali" font-weight="600" font-size="30" fill="#6a6a6a">ระยะ 3</text>
      <path id="${id}-sick" d="M-380,280C-320,280 -300,-160 -230,-170C-160,-180 -150,120 -60,150C20,170 60,40 120,-60C180,-160 240,-240 380,-250" stroke="#e8302a" stroke-width="12" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
      <path id="${id}-liver" d="M-380,290C-200,290 -120,280 -40,240C40,190 120,40 200,-80C260,-170 320,-220 390,-240" stroke="#a84a3a" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="20 14" opacity="0"/>
      <g id="${id}-l1" opacity="0"><path d="M-36,8L-56,118M-70,98l14,22l10,-25" stroke="#1a3a8a" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><rect x="-132" y="-54" width="206" height="60" rx="12" fill="#e4f2d4" stroke="#1a3a8a" stroke-width="4"/><text x="-29" y="-12" text-anchor="middle" font-family="Mali" font-weight="700" font-size="32" fill="#1a3a8a">ดีขึ้นชั่วคราว</text></g>
      <g id="${id}-l2" opacity="0"><rect x="120" y="-200" width="270" height="140" rx="14" fill="#fbe0e0" stroke="#a8302a" stroke-width="4"/>${PopUI.ICON.liver(175, -130, 0.8)}<text x="290" y="-112" text-anchor="middle" font-family="Mali" font-weight="700" font-size="38" fill="#a8302a">ตับแย่ลง</text></g>
      <g id="${id}-l3" opacity="0"><rect x="-300" y="-230" width="420" height="80" rx="14" fill="#ffe066" stroke="#3a2a22" stroke-width="4" transform="rotate(-3)"/><text x="-90" y="-176" text-anchor="middle" font-family="Mali" font-weight="700" font-size="40" fill="#3a2a22" transform="rotate(-3)">แม้กินแค่ดอกเดียว!</text></g>
    </g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="200" r="1000" fill="url(#wdTube)" opacity=".6" style="mix-blend-mode:screen"/>`);
  }

  // ---------------- ยายคำ from behind, sitting at the bedside ----------------
  function yaiBack(x, y, s, id) {
    const skin = "#c99a74", hair = "#c2bdb4", hairS = "#8f8a84";
    let g = `<ellipse cx="0" cy="6" rx="120" ry="16" fill="#000" opacity=".3"/>`;
    // the stool
    g += `<path d="M-60,0L-50,-170M60,0L50,-170M-70,-90H70" stroke="#5a6a72" stroke-width="12" fill="none"/><rect x="-80" y="-186" width="160" height="22" rx="8" fill="#7a8a92" stroke="${LN}" stroke-width="3"/>`;
    // sarong over the knees, feet tucked under
    g += `<path d="M-74,-180Q-90,-120 -80,-30H80Q90,-120 74,-180Z" fill="#6a2f62" stroke="${LN}" stroke-width="3"/><path d="M-82,-60H82" stroke="#d8a83a" stroke-width="8"/><path d="M-80,-44H80" stroke="#a8342a" stroke-width="4"/>
      <path d="M-40,-170V-40M0,-176V-36M40,-170V-40" stroke="#52244c" stroke-width="3" opacity=".6"/>`;
    // the back: lace blouse, the sash across, arms down to the lap
    g += `<path d="M-62,-470Q-76,-420 -72,-190H72Q76,-420 62,-470Q0,-492 -62,-470Z" fill="#f2ece0" stroke="${LN}" stroke-width="3"/><path d="M-62,-470Q-76,-420 -72,-190H72Q76,-420 62,-470Q0,-492 -62,-470Z" fill="url(#r2Cyl)"/>
      <path d="M-30,-460q4,6 8,0q4,6 8,0q4,6 8,0q4,6 8,0q4,6 8,0q4,6 8,0q4,6 8,0" stroke="#d8cfbd" stroke-width="2.4" fill="none"/>
      <path d="M52,-478Q10,-380 -56,-200" stroke="#d8a83a" stroke-width="24" fill="none"/><path d="M52,-478Q10,-380 -56,-200" stroke="#a8342a" stroke-width="4" stroke-dasharray="9 9" fill="none"/>
      ${[-1, 1].map((k) => `<path d="M${k * 60},-460Q${k * 86},-380 ${k * 74},-250" stroke="${LN}" stroke-width="34" fill="none" stroke-linecap="round"/><path d="M${k * 60},-460Q${k * 86},-380 ${k * 74},-250" stroke="#f2ece0" stroke-width="28" fill="none" stroke-linecap="round"/>
        <path d="M${k * 74},-250Q${k * 60},-210 ${k * 40},-200" stroke="${LN}" stroke-width="26" fill="none" stroke-linecap="round"/><path d="M${k * 74},-250Q${k * 60},-210 ${k * 40},-200" stroke="${skin}" stroke-width="20" fill="none" stroke-linecap="round"/>`).join("")}`;
    // the head from behind: neck, ears, grey hair pulled back to a bun with a gold pin
    g += `<g id="${id}-head"><path d="M-16,-500V-470Q0,-462 16,-470V-500Z" fill="${Rig2.shade(skin, 0.2)}" stroke="${LN}" stroke-width="2.4"/>
      <path d="M-50,-560q-14,-4 -14,12q0,16 12,18M50,-560q14,-4 14,12q0,16 -12,18" fill="${skin}" stroke="${LN}" stroke-width="2.4"/>
      <ellipse cx="0" cy="-556" rx="50" ry="58" fill="${hair}" stroke="${LN}" stroke-width="2.6"/><path d="M-30,-604Q-24,-560 -30,-508M0,-614V-500M30,-604Q24,-560 30,-508M-44,-580Q-40,-540 -44,-512M44,-580Q40,-540 44,-512" stroke="${hairS}" stroke-width="2.4" fill="none"/>
      <circle cx="0" cy="-574" r="26" fill="${Rig2.dk(hair, 0.06)}" stroke="${LN}" stroke-width="2.6"/><path d="M-14,-586q14,-10 28,0M-18,-572q18,-6 36,0" stroke="${hairS}" stroke-width="2.4" fill="none"/>
      <path d="M-40,-596L40,-552" stroke="#d8a83a" stroke-width="5" stroke-linecap="round"/><circle cx="-40" cy="-596" r="6" fill="#d8a83a" stroke="${LN}" stroke-width="2"/></g>`;
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><g id="${id}">${g}</g></g>`;
  }

  // ---------------- her feet on the ward floor ----------------
  function feet2(L, o = {}) {
    const id = o.id || "ft", r = mk(o.seed || 23), skin = "#c99a74", skinS = Rig2.shade(skin, 0.22), mud = "#5a3a22";
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#0a0e10"/>`);
    let s = `<rect x="-1300" y="600" width="3700" height="2600" fill="url(#ftFloor)"/>${Array.from({ length: 10 }, (_, k) => `<path d="M-1300,${700 + Math.pow(k / 9, 1.4) * 1400}H2400" stroke="#14201e" stroke-width="3" opacity=".7"/>`).join("")}`;
    s += `<rect x="-1300" y="-900" width="3700" height="1500" fill="#1e2a28"/><rect x="-1300" y="560" width="3700" height="40" fill="#2a3634"/>`;
    // the bed's legs and the sheet hanging at the top of frame
    s += `<path d="M-200,-900V700M1300,-900V700" stroke="#6a6e72" stroke-width="30"/><path d="M-400,-900H1500V180Q540,240 -400,180Z" fill="#c8ccd0" opacity=".85"/><path d="M-400,170Q540,230 1500,170" stroke="#9aa0a4" stroke-width="6" fill="none"/>`;
    // the sarong's hem and the ankles; mud caked to the ankle; dirt trailing behind on the floor
    for (let k = 0; k < 24; k++) s += `<ellipse cx="${f1(200 + r() * 700)}" cy="${f1(1500 + r() * 400)}" rx="${f1(6 + r() * 18)}" ry="${f1(3 + r() * 8)}" fill="${mud}" opacity="${f1(0.4 + r() * 0.4)}"/>`;
    const foot = (fx, flip) => {
      const m = flip ? -1 : 1;
      let g = `<path d="M-60,-700V-120Q-70,-60 -50,0H70Q60,-80 60,-140V-700Z" fill="${skin}" stroke="${LN}" stroke-width="4"/><path d="M-60,-700V-120Q-70,-60 -50,0H70Q60,-80 60,-140V-700Z" fill="url(#r2Cyl)"/>
        <path d="M30,-640Q44,-400 30,-200" stroke="${skinS}" stroke-width="5" fill="none" opacity=".5"/><ellipse cx="50" cy="-110" rx="12" ry="20" fill="${skinS}" opacity=".6"/>`;
      g += `<path d="M-64,-300Q0,-260 64,-300V-120Q60,-60 70,0H-50Q-70,-60 -64,-120Z" fill="${mud}" opacity=".75"/>`;
      g += `<path d="M-60,-40Q-80,60 -40,120Q20,150 120,130Q200,110 230,60Q200,-10 120,-30Q60,-40 40,-10Z" fill="${skin}" stroke="${LN}" stroke-width="4"/>`;
      g += `<path d="M-60,-40Q-80,60 -40,120Q20,150 120,130Q200,110 230,60" fill="none" stroke="${mud}" stroke-width="30" opacity=".6"/>`;
      // the toes — long, jointed, mud under the nails
      g += `<g id="${id}-toes${flip ? "L" : "R"}">${[[200, 40, 150, 22], [210, 70, 170, 20], [205, 98, 160, 18], [190, 120, 140, 16], [160, 134, 110, 14]].map(([tx, ty, len, w], k) => {
        const a = (-8 + k * 10) * Math.PI / 180, mx = tx + Math.cos(a) * len * 0.55, my = ty + Math.sin(a) * len * 0.55 - 10, ex = tx + Math.cos(a) * len, ey = ty + Math.sin(a) * len + 16;
        return `<path d="M${tx},${ty}Q${f1(mx)},${f1(my)} ${f1(ex)},${f1(ey)}" stroke="${LN}" stroke-width="${w + 8}" fill="none" stroke-linecap="round"/><path d="M${tx},${ty}Q${f1(mx)},${f1(my)} ${f1(ex)},${f1(ey)}" stroke="${skin}" stroke-width="${w}" fill="none" stroke-linecap="round"/>
          <path d="M${f1(mx - 6)},${f1(my - 2)}q6,${w * 0.4} 12,0" stroke="${skinS}" stroke-width="3" fill="none"/><ellipse cx="${f1(ex - 4)}" cy="${f1(ey - 2)}" rx="${f1(w * 0.42)}" ry="${f1(w * 0.3)}" fill="#3a2414"/>`; }).join("")}</g>`;
      g += `<path d="M-50,-700V-120" stroke="#fff" stroke-width="10" opacity=".12"/>`;
      return `<g transform="translate(${fx},1560) scale(${m},1)">${g}</g>`;
    };
    s += foot(360, true) + foot(720, false);
    s += `<path d="M-200,880Q540,960 1300,880L1300,600Q540,700 -200,600Z" fill="#6a2f62" stroke="${LN}" stroke-width="4"/><path d="M-200,860Q540,940 1300,860" stroke="#d8a83a" stroke-width="12" fill="none"/><path d="M-200,880Q540,960 1300,880" stroke="#a8342a" stroke-width="6" fill="none"/>`;
    put(L.set, s);
    put(L.glow, `<rect x="-200" y="-200" width="1500" height="2400" fill="url(#ftMoon)" style="mix-blend-mode:screen"/>`);
  }

  Object.assign(Sets, { board2, feet2 });
  Object.assign(Pop2, { yaiBack });
})();
