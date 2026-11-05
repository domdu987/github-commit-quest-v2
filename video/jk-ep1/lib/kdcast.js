// ---------- ข้าวต้มตีสอง: the cast, the poses and the story's UI (load after rig2.js, mmcast.js, rabcast.js, lotcast.js) ----------
//   Rig.CAST.kdYou       you, the cartoonist: grey hoodie (hood down), round glasses, dark sweatpants · kdYouPen (a pen in hand)
//   Rig.CAST.kdYai       ยายจันทร์: hair bun, pale blue blouse, white apron · kdYaiLadle · kdYaiPhone
//   Rig.MODES            slump (tired at the desk) · type (both hands on the keyboard) · stir (ladle in the pot) · write (pen on paper)
//   KD.page(o)           the comic page on a 272×540 phone/laptop screen: ตอนที่ 214, ♥ 12, a red "ลบเพจ" button (o.id → #id-del, #id-heart)
//   KD.board(x,y,s,o)    the chalkboard by the pot: o.rows [text…] (o.id → #id-r0…), o.back → the back side with rule 4
//   KD.paper(x,y,s,o)    a sheet of paper with handwritten lines (o.id → #id-l0…)
//   KD.steam(x,y,s,id)   three wisps of steam (#id-s0…2)
(function () {
  const C = Rig.CAST, LINE = Rig2.LINE, INK = "#2e2a26", M = Rig.MODES;
  const f1 = (v) => (+v).toFixed(1);
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"`;
  const T = (x, y, size, text, o = {}) => `<text x="${x}" y="${y}" text-anchor="${o.anchor || "middle"}" font-family="${o.font || "Kanit"}" font-weight="${o.w || 900}" font-size="${size}" fill="${o.fill || INK}"${o.op ? ` opacity="${o.op}"` : ""}>${text}</text>`;
  const at = (x, y, s, svg, rot = 0) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${s})">${svg}</g>`;

  // ---------------- people ----------------
  const GLASSES = `<g fill="none" stroke="#2a2a2a" stroke-width="3.4"><circle cx="-16" cy="-549" r="13"/><circle cx="20" cy="-549" r="13"/><path d="M-3,-550h10M-29,-552l-14,-4M33,-552l12,-4"/></g>`;
  const HOOD = `<path d="M-52,-484Q-62,-522 -34,-530Q0,-502 34,-530Q62,-522 52,-484Q0,-468 -52,-484Z" fill="#5a6270" stroke="${LINE}" stroke-width="2.4"/>
    <path d="M-10,-470V-418M10,-470V-422" stroke="#e8eef4" stroke-width="3" stroke-linecap="round"/>`;
  const PEN_H = `<g transform="translate(4,146) rotate(-30)"><rect x="-4" y="-46" width="8" height="64" rx="3" fill="#2a4a8a" stroke="${LINE}" stroke-width="2"/><path d="M-4,18L0,30L4,18Z" fill="#2e2a26"/></g>`;
  const LADLE_H = `<g transform="translate(4,146) rotate(-10)"><rect x="-3.5" y="-80" width="7" height="96" rx="3" fill="#b8bcc2" stroke="${LINE}" stroke-width="2"/><path d="M-20,16Q-20,40 0,40Q20,40 20,16Z" fill="#c8ccd2" stroke="${LINE}" stroke-width="2.2"/></g>`;
  const PHONE_H = `<g transform="translate(4,146) rotate(-12)"><rect x="-21" y="-38" width="42" height="76" rx="8" fill="#1c2026" stroke="${LINE}" stroke-width="2.6"/>
    <rect x="-17" y="-32" width="34" height="62" rx="5" fill="#a8d8f4"/><path d="M-14,-26L8,6M-6,-30L14,-2" stroke="#fff" stroke-width="1.6" opacity=".8"/></g>`;
  C.kdYou = { v2: { ...C.keng.v2, extra: HOOD, top: { kind: "tee", c: "#6b7380", sleeve: "long" }, print: `<path d="M-30,-384h60v34h-60z" fill="#5a6270" opacity=".55"/>`,
    bottom: { kind: "jeans", c: "#353a44" }, faceTop: GLASSES } };
  C.kdYouPen = { v2: C.kdYou.v2, hand: PEN_H, keep: "F" };
  const SPOON_H = `<g transform="translate(4,146) rotate(-20)"><ellipse cx="0" cy="-36" rx="12" ry="16" fill="#dfe3e6" stroke="${LINE}" stroke-width="2.2"/><rect x="-3.5" y="-22" width="7" height="58" rx="3" fill="#c8ccd0" stroke="${LINE}" stroke-width="2"/></g>`;
  C.kdYouSpoon = { v2: C.kdYou.v2, hand: SPOON_H, keep: "F" };
  const APRON = `<path d="M-42,-420H42L50,-300Q0,-292 -50,-300Z" fill="#f6f2ea" stroke="${LINE}" stroke-width="2.4"/><path d="M-24,-380h48v28h-48z" fill="none" stroke="#c8c0b0" stroke-width="2.4"/>
    <path d="M-40,-420L-30,-482M40,-420L30,-482" stroke="#f6f2ea" stroke-width="7"/>`;
  C.kdYai = { v2: { ...C.yaiBua.v2, top: { kind: "blouse", c: "#bcd8e6", sleeve: "elbow", trim: "#8ab0c4" }, extra: APRON } };
  C.kdYaiLadle = { v2: C.kdYai.v2, hand: LADLE_H, keep: "F" };
  C.kdYaiPhone = { v2: C.kdYai.v2, hand: PHONE_H, keep: "F" };

  // ---------------- poses ----------------
  M.slump = (u, o) => ({ ...M.sitChair(u, o), torso: 10 + Math.sin(u * 1.2), head: 16, uaF: -30, faF: -60, uaB: -24, faB: -56 });
  M.type = (u, o) => { const j = Math.sin(u * 18) * 3; return { ...M.sitChair(u, o), torso: 6, head: 8, uaF: -48 + j, faF: -46, uaB: -44 - j, faB: -48 }; };
  M.stir = (u, o) => { const c = Math.sin((2 * Math.PI * u) / 1.4); return { ...M.idle(u, o), uaF: -40 + 10 * c, faF: -40 - 8 * c, torso: 4, head: 8 }; };
  M.write = (u, o) => { const j = Math.sin(u * 14) * 2.5; return { ...M.sitChair(u, o), torso: 8, head: 14, uaF: -44 + j, faF: -52 - j, uaB: -30, faB: -40 }; };

  // ---------------- UI ----------------
  const page = (o = {}) => { const id = o.id || "kp";
    return `<rect width="272" height="540" fill="#f4f2ee"/><rect width="272" height="70" fill="#3a5a9a"/>${T(18, 44, 22, "การ์ตูนวันละตอน", { anchor: "start", fill: "#fff" })}
      <rect x="16" y="86" width="240" height="250" rx="10" fill="#fff" ${O(3)}/><path d="M28,98h104v110h-104zM140,98h104v110h-104zM28,216h216v108h-216z" fill="#e8eef6" ${O(2.5)}/>
      <circle cx="80" cy="150" r="22" fill="#f2d6b4" ${O(2.5)}/><circle cx="192" cy="156" r="22" fill="#f2d6b4" ${O(2.5)}/><path d="M60,270q40,-30 80,0t80,0" stroke="#3a5a9a" stroke-width="5" fill="none"/>
      ${T(18, 370, 24, "ตอนที่ 214", { anchor: "start", w: 800 })}
      <g id="${id}-heart"><path d="M30,396C22,388 24,378 32,378C36,378 38,381 40,384C42,381 44,378 48,378C56,378 58,388 50,396L40,406Z" fill="#e05a6a"/>${T(64, 404, 24, "12", { anchor: "start", w: 800, fill: "#e05a6a" })}</g>
      <g id="${id}-del"><rect x="40" y="446" width="192" height="58" rx="29" fill="#d8443a" ${O(3)}/>${T(136, 484, 26, "ลบเพจ", { fill: "#fff" })}</g>`; };
  const chalk = (x, y, size, text) => T(x, y, size, text, { anchor: "start", font: "Sriracha", w: 400, fill: "#f4f2ea" });
  const board = (x, y, s, o = {}) => { const id = o.id || "kb", rows = o.rows || [];
    const face = o.back ? `${T(0, -150, 40, "ด้านหลัง", { font: "Sriracha", w: 400, fill: "#f6d36a" })}<g id="${id}-r0">${chalk(-150, -40, 52, "พักได้…")}${chalk(-150, 40, 52, "แต่อย่าลบ")}</g>`
      : `${T(0, -170, 40, "กฎของร้าน", { font: "Sriracha", w: 400, fill: "#f6d36a" })}${rows.map((r, k) => `<g id="${id}-r${k}">${chalk(-172, -90 + k * 92, 31, `${k + 1}. ${r}`)}</g>`).join("")}`;
    return at(x, y, s, `<path d="M-150,230L-180,330M150,230L180,330" stroke="#5a3a1a" stroke-width="12" stroke-linecap="round"/>
      <rect x="-210" y="-230" width="420" height="460" rx="12" fill="#8a5a32" ${O(5)}/><rect x="-192" y="-212" width="384" height="424" rx="6" fill="#2e3a34"/>${face}`, o.rot || 0); };
  const paper = (x, y, s, o = {}) => { const id = o.id || "kq";
    return at(x, y, s, `<rect x="-200" y="-260" width="400" height="520" rx="6" fill="#fbf8f0" ${O(4)}/>${[...Array(9)].map((_, k) => `<path d="M-176,${-190 + k * 52}H176" stroke="#c8d4e4" stroke-width="2.5"/>`).join("")}
      ${(o.lines || []).map((l, k) => `<g id="${id}-l${k}">${T(-170, -200 + k * 52, 30, l, { anchor: "start", font: "Sriracha", w: 400, fill: "#2a4a8a" })}</g>`).join("")}`, o.rot || 0); };
  const steam = (x, y, s, id) => at(x, y, s, [0, 1, 2].map((k) => `<path id="${id}-s${k}" d="M${-40 + k * 40},0q-16,-30 0,-60t0,-60" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" opacity=".55"/>`).join(""));
  // the laptop seen close: the page in landscape, ♥ 12, the red delete button, a cursor (o.id → #id-heart, #id-del, #id-cur)
  const laptop = (x, y, s, o = {}) => { const id = o.id || "kl";
    return at(x, y, s, `<rect x="-330" y="-220" width="660" height="430" rx="22" fill="#2a2e34" ${O(6)}/><rect x="-306" y="-198" width="612" height="384" rx="6" fill="#f4f2ee"/>
      <rect x="-306" y="-198" width="612" height="56" fill="#3a5a9a"/>${T(-288, -160, 26, "การ์ตูนวันละตอน", { anchor: "start", fill: "#fff" })}
      <rect x="-286" y="-128" width="260" height="210" rx="8" fill="#e8eef6" ${O(3)}/><circle cx="-200" cy="-60" r="30" fill="#f2d6b4" ${O(3)}/><circle cx="-110" cy="-50" r="30" fill="#f2d6b4" ${O(3)}/>
      <path d="M-260,40q50,-30 100,0t100,0" stroke="#3a5a9a" stroke-width="6" fill="none"/>
      ${T(0, -96, 34, "ตอนที่ 214", { anchor: "start", w: 800 })}
      <g id="${id}-heart"><path d="M14,-34C2,-46 6,-62 18,-62C24,-62 27,-58 30,-54C33,-58 36,-62 42,-62C54,-62 58,-46 46,-34L30,-18Z" fill="#e05a6a"/>${T(64, -24, 44, "12", { anchor: "start", w: 900, fill: "#e05a6a" })}</g>
      <g id="${id}-del"><rect x="20" y="40" width="250" height="74" rx="37" fill="#d8443a" ${O(4)}/>${T(145, 90, 36, "ลบเพจ", { fill: "#fff" })}</g>
      <g id="${id}-cur"><path d="M236,82L236,136L250,122L262,148L274,142L262,117L282,116Z" fill="#fff" ${O(3)}/></g>
      <path d="M-360,210H360L380,240H-380Z" fill="#9aa2ac" ${O(5)}/>`); };
  window.KD = { page, board, paper, steam, chalk, laptop, T, at, O, INK };
})();
