// ---------- หมาดำตาสี่ (พิษสุนัขบ้า): the cast, drawn with rig v2 — load after tidecast.js (borrows its bodies) ----------
//   Rig.CAST.phum      ภูมิ 9: buzz-cut, sky-blue tee with a bone print, green shorts, sandals (the plaster is on the right knee: seen in inserts)
//   Rig.CAST.prae      แพร 16: dark ponytail, mustard hoodie, jeans, white sneakers
//   Rig.CAST.yaiBua    ยายบัว 68: grey bun, cream lace blouse with a ผ้าขาวม้า over the shoulder, a mudmee sarong, sandals
//   Rig.CAST.yaiBuaHerb  the same, her left hand bound in a green herb poultice wrapped in cloth (EP.2–3)
//   Rig.CAST.khiao     ลุงเขียว 55: green volunteer vest with a patch "อาสาปศุสัตว์", khaki shirt, a cap, long trousers, boots
//   Rig.CAST.khiaoBox  ลุงเขียว carrying the vaccine cool box (hand F)
//   Rig.CAST.phumRice  ภูมิ holding out a ball of sticky rice (hand F)
(function () {
  const { LINE, dk, hi } = Rig2;
  const C = Rig.CAST;
  // ภูมิ holds the rice out to the puppy, bent forward a little; a scared step back
  Rig.MODES.offer = (u, o) => ({ ...Rig.MODES.idle(u, o), torso: 10, head: 8, uaF: -28 + 3 * Math.sin(u * 3), faF: -40, uaB: 8, faB: 10 });
  Rig.MODES.recoil = (u, o) => ({ ...Rig.MODES.idle(u, o), torso: -8, head: -6, uaF: -40, faF: -60, uaB: 30, faB: 50 });
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round"`;

  // ---------------- ภูมิ ----------------
  const buzz = (h) => `
    <path d="M-46,-552C-50,-606 -18,-626 4,-624C30,-623 53,-604 49,-552Q46,-572 40,-580Q30,-588 16,-584Q4,-592 -10,-586Q-26,-590 -38,-580Q-44,-570 -46,-552Z" fill="${h.c}" ${ln()}/>
    <path d="M-44,-556v14M48,-556v12" stroke="${h.c}" stroke-width="5" stroke-linecap="round"/>
    <g fill="${h.sh}" opacity=".5">${[[-30, -606], [-16, -612], [0, -614], [16, -612], [30, -604], [-22, -596], [-6, -600], [10, -600], [24, -594], [38, -590], [-36, -590]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="1.7"/>`).join("")}</g>
    <path d="M-30,-608Q2,-624 34,-606" stroke="${h.sh}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".4"/>`;
  const bones = `<g transform="translate(0,-400)">${[[-26, -18, -20], [22, 14, 24], [-10, 34, -8]].map(([x, y, r]) => `<g transform="translate(${x},${y}) rotate(${r})">
      <path d="M-14,-3H14M-14,3H14" stroke="#fffbf0" stroke-width="5"/><circle cx="-15" cy="-4" r="4.4" fill="#fffbf0"/><circle cx="-15" cy="4" r="4.4" fill="#fffbf0"/><circle cx="15" cy="-4" r="4.4" fill="#fffbf0"/><circle cx="15" cy="4" r="4.4" fill="#fffbf0"/>
      <path d="M-18,-8Q-22,0 -18,8M18,-8Q22,0 18,8" stroke="${LINE}" stroke-width="1.6" fill="none" opacity=".6"/></g>`).join("")}
    <path d="M-30,-48q6,-8 12,0q6,-8 12,0" stroke="#2e6aa8" stroke-width="3" fill="none"/><text x="2" y="-40" font-family="Kanit" font-weight="900" font-size="16" fill="#2e6aa8" text-anchor="middle">WOOF</text></g>`;
  const phumV2 = {
    skin: "#d4a074", iris: "#2e1c12", blush: 0.7, headScale: 1.2, w: 0.9, limb: 0.9,
    hair: { c: "#17100c", s: "#060404", sh: "#5a4a40", front: (x) => buzz(x.hair) },
    top: { kind: "tee", c: "#7cc4ec", sleeve: "short", trim: "#5aa8d4" },
    print: bones,
    bottom: { kind: "shorts", c: "#3e9a5a" }, feet: { kind: "sandal", c: "#e2483c" },
  };
  C.phum = { v2: phumV2 };

  // ---------------- แพร ----------------
  const ponyFront = (h) => `
    <path d="M-50,-546C-58,-610 -18,-632 6,-630C36,-628 60,-606 52,-546Q48,-574 30,-590Q12,-582 -6,-590Q-26,-584 -40,-570Q-47,-560 -50,-546Z" fill="${h.c}" ${ln()}/>
    <path d="M-20,-622Q-28,-600 -38,-578M8,-628Q4,-604 -4,-588M30,-620Q36,-602 32,-590" stroke="${h.s}" stroke-width="2.4" fill="none" opacity=".7"/>
    <path d="M-34,-606Q0,-626 38,-606" stroke="${h.sh}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".5"/>
    <path d="M-50,-560C-56,-536 -54,-512 -48,-496Q-44,-520 -44,-548Z" fill="${h.c}" ${ln(2.2)}/>`;
  const ponyBack = (h) => `<path d="M-30,-612C-70,-618 -86,-570 -80,-516C-76,-480 -86,-450 -96,-430Q-70,-436 -62,-470C-54,-500 -56,-540 -40,-574Z" fill="${dk(h.c, 0.1)}" ${ln()}/>
    <path d="M-36,-604Q-30,-618 -18,-616" stroke="#e2483c" stroke-width="7" stroke-linecap="round"/><path d="M-74,-540Q-80,-490 -88,-450" stroke="${h.s}" stroke-width="2.4" fill="none" opacity=".7"/>`;
  const hoodie = `<path d="M-40,-492Q-56,-500 -60,-474Q-50,-460 -30,-470ZM40,-492Q56,-500 60,-474Q50,-460 30,-470Z" fill="#d89a22" ${ln(2.2)}/>
    <path d="M-50,-488Q0,-454 50,-488" stroke="#c4861a" stroke-width="8" fill="none" stroke-linecap="round"/>
    <path d="M-10,-470v54M10,-470v50" stroke="#fff4dc" stroke-width="3" stroke-linecap="round"/><circle cx="-10" cy="-414" r="3.4" fill="#fff4dc"/><circle cx="10" cy="-418" r="3.4" fill="#fff4dc"/>
    <path d="M-40,-330Q0,-318 40,-330L36,-290Q0,-280 -36,-290Z" fill="#d89a22" ${ln(2.2)}/><path d="M0,-326v40" stroke="#b47812" stroke-width="2"/>`;
  C.prae = { v2: {
    skin: "#ebc19c", iris: "#3a2016", lash: true, blush: 0.6, lip: "#c8606a", w: 1.04,
    hair: { c: "#24170f", s: "#0c070a", sh: "#7a5a4a", front: (x) => ponyFront(x.hair), back: (x) => ponyBack(x.hair) },
    top: { kind: "tee", c: "#e8ac2e", sleeve: "long", trim: "#c4861a" },
    print: hoodie,
    bottom: { kind: "jeans", c: "#4a6a98" }, feet: { kind: "sneaker", c: "#f4f2ec", sole: "#d8d2c4", lace: "#b8b2a6" },
  } };

  // ---------------- ยายบัว ----------------
  const yt = C.yaiTide.v2;
  const pakaoma = `<path d="M-46,-492Q-20,-470 20,-470L44,-490L56,-470Q20,-440 -20,-448L-50,-468Z" fill="url(#rbCheck)" ${ln(2.2)}/>
    <path d="M40,-480Q58,-420 50,-340L68,-344Q72,-430 54,-486Z" fill="url(#rbCheck)" ${ln(2.2)}/><path d="M50,-342h18" stroke="#f4e6c8" stroke-width="3" stroke-dasharray="3 3"/>`;
  Sets.DEFS += `<pattern id="rbCheck" width="18" height="18" patternUnits="userSpaceOnUse"><rect width="18" height="18" fill="#3a7ab8"/><path d="M0,4h18M0,13h18" stroke="#e2483c" stroke-width="3" opacity=".8"/>
      <path d="M4,0v18M13,0v18" stroke="#f4e6c8" stroke-width="2.4" opacity=".7"/></pattern>
    <pattern id="rbMudmee" width="40" height="34" patternUnits="userSpaceOnUse"><rect width="40" height="34" fill="#4a2a5a"/>
      <path d="M0,17L10,7L20,17L10,27ZM20,17L30,7L40,17L30,27Z" fill="#a8507a" opacity=".85"/><path d="M10,12L15,17L10,22L5,17ZM30,12L35,17L30,22L25,17Z" fill="#f0c860" opacity=".8"/>
      <path d="M0,0h40M0,34h40" stroke="#2a1838" stroke-width="3"/></pattern>`;
  const mudmee = `<path d="M-57,-336Q-62,-250 -55,-150L-50,-38Q-26,-31 0,-34Q26,-31 50,-38L55,-150Q62,-250 57,-336Z" fill="url(#rbMudmee)" ${ln(2.6)}/>
    <path d="M-55,-60Q0,-50 55,-60L52,-38Q0,-30 -52,-38Z" fill="#c8963a" ${ln(2)}/><path d="M16,-336L24,-30" stroke="${LINE}" stroke-width="2.2"/>
    <path d="M-57,-336Q-62,-250 -55,-150L-50,-38Q-26,-31 0,-34Q26,-31 50,-38L55,-150Q62,-250 57,-336Z" fill="url(#r2Cyl)"/>`;
  const yaiV2 = { ...yt, top: { kind: "blouse", c: "#f4ead6", sleeve: "elbow", lace: true, trim: "#d8c8a4" }, print: "", skirt: mudmee,
    bottom: { kind: "sarong", c: "#4a2a5a", band: "#c8963a", band2: "#2a1838" }, extra: pakaoma };
  C.yaiBua = { v2: yaiV2 };

  // ---------------- ลุงเขียว ----------------
  const jv = C.taJun.v2;
  const cap = (h) => `<path d="M-50,-560C-54,-616 -18,-636 6,-634C36,-632 58,-612 52,-560Q20,-572 -50,-560Z" fill="#2e7a4a" ${ln()}/>
    <path d="M30,-566Q70,-570 86,-556Q66,-548 30,-554Z" fill="#256640" ${ln(2.4)}/><path d="M-40,-604Q0,-626 40,-606" stroke="#5aa874" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/>
    <circle cx="4" cy="-634" r="5" fill="#256640" ${ln(1.8)}/><path d="M-46,-560v18M48,-560v16" stroke="#cfc8bc" stroke-width="5" stroke-linecap="round"/>`;
  const vestG = `
    <path d="M-52,-488L-22,-484L-14,-430L-18,-306Q-44,-300 -70,-306L-68,-448Q-66,-476 -52,-488Z" fill="#2f8a52" ${ln(2.8)}/>
    <path d="M52,-488L22,-484L14,-430L18,-306Q44,-300 70,-306L68,-448Q66,-476 52,-488Z" fill="#2f8a52" ${ln(2.8)}/>
    <path d="M-60,-460Q-54,-400 -60,-330M58,-460Q54,-400 60,-330" stroke="#1e6a3a" stroke-width="2.6" fill="none" opacity=".6"/>
    <rect x="22" y="-452" width="40" height="22" rx="4" fill="#fff8e0" ${ln(1.8)}/><text x="42" y="-437" font-family="Kanit" font-weight="700" font-size="9" fill="#1e6a3a" text-anchor="middle">อาสาปศุสัตว์</text>
    <path d="M-62,-380h40v26h-40z" fill="#26784a" ${ln(2)}/><path d="M-62,-372h40" stroke="#1e6a3a" stroke-width="2"/><path d="M-36,-392v14" stroke="#2a3a8a" stroke-width="4" stroke-linecap="round"/>`;
  C.khiao = { v2: { ...jv, hair: { ...jv.hair, front: (x) => cap(x.hair) }, top: { kind: "shirt", c: "#c8b88a", sleeve: "long", neck: "collar", collar: "#b0a072", button: "#8a7a5a", trim: "#b0a072" },
    bottom: { kind: "trousers", c: "#4a4a40" }, feet: { kind: "boot", c: "#2a2a2a" }, legs: undefined, extra: vestG } };

  // ---------------- props ----------------
  const rice = () => `<g transform="translate(0,118)"><path d="M-4,-12Q16,-22 30,-8Q36,8 18,14Q-2,16 -8,2Q-10,-6 -4,-12Z" fill="#fbf6e8" ${ln(2)}/>
    <g fill="#e8dcc0">${[[4, -6], [14, -10], [22, -2], [8, 4], [18, 6]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="2.6" ry="1.4"/>`).join("")}</g></g>`;
  const coolbox = () => `<g transform="translate(0,118)"><path d="M-6,-6v-10q0,-8 8,-8h20q8,0 8,8v10" stroke="${LINE}" stroke-width="4" fill="none"/>
    <rect x="-30" y="-6" width="84" height="56" rx="6" fill="#f4f6f8" ${ln(2.6)}/><rect x="-30" y="-6" width="84" height="14" rx="5" fill="#2f8acc" ${ln(2.2)}/>
    <path d="M6,20h12M12,14v12" stroke="#e2483c" stroke-width="5"/><path d="M-24,40h72" stroke="#c8ccd2" stroke-width="3"/></g>`;
  const herb = `<g transform="translate(0,118)"><ellipse cx="0" cy="4" rx="20" ry="16" fill="#e8e2cc" ${ln(2)}/><path d="M-14,-4q14,10 28,0M-16,8q16,8 32,0" stroke="#c8bea0" stroke-width="2" fill="none"/>
    <path d="M-10,-2q4,4 10,2q6,4 10,0" stroke="#5a8a3a" stroke-width="4" fill="none" opacity=".9"/></g>`;
  C.phumRice = { v2: phumV2, hand: rice(), keep: "F" };
  C.khiaoBox = { v2: C.khiao.v2, hand: coolbox(), keep: "F" };
  C.yaiBuaHerb = { v2: yaiV2, hand: herb, keep: "B" };
})();
