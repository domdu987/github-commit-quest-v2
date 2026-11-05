// Rod Mai Club · the channel's own cast look (owner 4 Nov 2026: "ทำตัวละครเราใหม่ ทำให้ดี ให้เป็นเอกลักษณ์"), built on flat.js:
// slender, no outlines, one shade panel, printed cloth, and almond eyes with a lid line instead of dots. Every pose mode still works.
//   Rig.CAST.sgYou     คุณ, the channel's recurring "you": messy hair with one cowlick, round glasses, a mustard hoodie (the brand
//                      yellow) with the hood down, joggers, blue flip-flops · story 6: a pencil behind the ear
//                      variants: sgYouPen, sgYouSpoon, sgYouPhone (prop in the near hand)
//   Rig.CAST.sgYai     ยายจันทร์: white bun with a wooden pin, a cream floral blouse, an indigo sarong, a cream apron, a checked
//                      pha-khao-ma over the shoulder, smile creases · sgYaiLadle, sgYaiPhone
//   eye states (besides flat.js's): "tired" (half-lidded) · patterns: sgFloral, sgPlaid, sgCloth (table cloth)
// Load after flat.js; set Rig.FLAT = true on the page.
(function () {
  const { mix, dk, hi } = Rig2;
  const INK = Flat.INK;
  const f = (v) => (+v).toFixed(1);
  const EX = [-8, 21], EY = -549;

  Sets.DEFS += `
    <pattern id="sgFloral" width="34" height="34" patternUnits="userSpaceOnUse">
      <rect width="34" height="34" fill="#efe2cc"/>
      <g fill="#d86a78"><circle cx="8" cy="6" r="3.2"/><circle cx="12.5" cy="9" r="3.2"/><circle cx="11" cy="14" r="3.2"/><circle cx="5.5" cy="14" r="3.2"/><circle cx="3.8" cy="9" r="3.2"/></g>
      <circle cx="8" cy="10.5" r="2.4" fill="#f6d36a"/>
      <g fill="#c24a5a"><circle cx="25" cy="23" r="2.6"/><circle cx="28.6" cy="25.6" r="2.6"/><circle cx="27.4" cy="29.4" r="2.6"/><circle cx="23" cy="29.4" r="2.6"/><circle cx="21.6" cy="25.6" r="2.6"/></g>
      <circle cx="25" cy="26.8" r="1.9" fill="#f6d36a"/>
      <path d="M17,8q5,-4 9,0q-5,3 -9,0zM4,25q4,-4 8,0q-4,3 -8,0z" fill="#6a9a6a"/></pattern>
    <pattern id="sgPlaid" width="22" height="22" patternUnits="userSpaceOnUse">
      <rect width="22" height="22" fill="#e8e2d6"/><path d="M0,5.5h22M0,16.5h22" stroke="#3a6aa8" stroke-width="5" opacity=".85"/>
      <path d="M5.5,0v22M16.5,0v22" stroke="#c8443a" stroke-width="4" opacity=".75"/></pattern>
    <pattern id="sgCloth" width="60" height="60" patternUnits="userSpaceOnUse">
      <rect width="60" height="60" fill="#e9e4d8"/><path d="M0,15h60M0,45h60M15,0v60M45,0v60" stroke="#c8d8e0" stroke-width="10" opacity=".7"/>
      <g fill="#e07a68" opacity=".85"><circle cx="15" cy="15" r="5"/><circle cx="45" cy="45" r="5"/></g><g fill="#7aa86a" opacity=".8"><circle cx="45" cy="15" r="3.4"/><circle cx="15" cy="45" r="3.4"/></g></pattern>`;

  // ---------------- hair ----------------
  Flat.HAIR.messy = (c) => `<path d="M-42,-530C-48,-578 -26,-601 -2,-603C27,-605 51,-590 47,-558Q42,-572 32,-571L36,-586Q22,-574 10,-578L12,-593Q-1,-579 -13,-581L-14,-595Q-25,-581 -30,-569Q-33,-552 -34,-530Z" fill="${c}"/>
    <path d="M-3,-601Q-13,-630 9,-640Q1,-624 7,-603Z" fill="${c}"/>
    <path d="M-24,-593Q0,-607 30,-597" stroke="${hi(c, 0.28)}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".55"/>`;
  Flat.HAIR.bunPin = (c) => `<path d="M-42,-532C-48,-586 -16,-601 4,-601C33,-601 51,-587 47,-561Q33,-577 10,-578Q-14,-577 -28,-562Q-34,-550 -34,-532Z" fill="${c}"/>
    <circle cx="-30" cy="-597" r="20" fill="${dk(c, 0.07)}"/><path d="M-44,-604Q-30,-614 -16,-600" stroke="${dk(c, 0.16)}" stroke-width="2.4" fill="none"/>
    <path d="M-60,-614L-4,-584" stroke="#8a5a32" stroke-width="4.4" stroke-linecap="round"/><circle cx="-60" cy="-614" r="4.6" fill="#c8963a"/>
    <path d="M-20,-591Q4,-598 30,-589M-26,-580Q-6,-588 16,-584" stroke="${dk(c, 0.13)}" stroke-width="2" fill="none" stroke-linecap="round"/>`;

  // ---------------- faces: almond eyes with a lid line (o.bags: tired rings · o.crinkle: smile creases · o.k: eye height) ----------------
  function sigFaces(o = {}) {
    return (x, browC, base) => {
      const b = base(browC), k0 = o.k ?? 1, bw = o.browW ?? 4.4;
      const almond = (cx, cy, k) => `<path d="M${f(cx - 6.6)},${f(cy + 0.6)}Q${f(cx - 0.4)},${f(cy - 7.6 * k)} ${f(cx + 6.6)},${f(cy - 0.6)}Q${f(cx + 0.4)},${f(cy + 5.6 * k)} ${f(cx - 6.6)},${f(cy + 0.6)}Z" fill="${INK}"/><circle cx="${f(cx + 1.9)}" cy="${f(cy - 1.9 * k)}" r="1.6" fill="#fff" opacity=".9"/>`;
      const lid = (cx, cy, k) => `<path d="M${f(cx - 8.4)},${f(cy - 0.2)}Q${f(cx - 1)},${f(cy - 9.6 * k)} ${f(cx + 8.8)},${f(cy - 2.2)}" stroke="${INK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>`;
      const bags = (cx, cy) => (o.bags ? `<path d="M${f(cx - 5.5)},${f(cy + 8.5)}q5.5,3.2 11,0" stroke="${x.skinS}" stroke-width="2.4" fill="none" stroke-linecap="round"/>` : "");
      const crinkle = (cx, cy, i) => (o.crinkle ? `<path d="M${f(cx + (i ? 10 : -10))},${f(cy - 2.5)}l${i ? 5 : -5},-2.5M${f(cx + (i ? 10 : -10))},${f(cy + 2)}l${i ? 5 : -5},2.5" stroke="${x.skinS}" stroke-width="2" stroke-linecap="round"/>` : "");
      const brows = (dy = 0, tilt = 0) => EX.map((ex, i) => {
        const inner = ex + (i ? -7 : 7), outer = ex + (i ? 8.5 : -8.5);
        return `<path d="M${f(outer)},${f(EY - 16 + dy)}Q${f((inner + outer) / 2)},${f(EY - 19.5 + dy + tilt / 2)} ${f(inner)},${f(EY - 16 + dy + tilt)}" stroke="${browC}" stroke-width="${bw}" fill="none" stroke-linecap="round"/>`;
      }).join("");
      const set = (dx = 0, k = k0, dy = 0, tilt = 0) => EX.map((ex, i) => almond(ex + dx, EY, k) + lid(ex + dx, EY, k) + bags(ex + dx, EY) + crinkle(ex + dx, EY, i)).join("") + brows(dy, tilt);
      // half-lidded: the upper half of the eye under a skin-coloured lid, the lid line lower and flatter
      const tired = EX.map((ex, i) => `${almond(ex, EY + 1, k0)}<path d="M${f(ex - 8)},${f(EY - 9)}H${f(ex + 8.5)}V${f(EY + 0.5)}Q${f(ex)},${f(EY - 2.5)} ${f(ex - 8)},${f(EY + 1.2)}Z" fill="${x.skin}"/>
        <path d="M${f(ex - 8.4)},${f(EY + 1.2)}Q${f(ex)},${f(EY - 3)} ${f(ex + 8.8)},${f(EY + 0.2)}" stroke="${INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>${bags(ex, EY)}${crinkle(ex, EY, i)}`).join("") + brows(3, 2);
      const closed = EX.map((ex, i) => `<path d="M${f(ex - 7)},${f(EY - 0.5)}q7,6 14,0" stroke="${INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>${crinkle(ex, EY, i)}`).join("") + brows(2);
      const happy = EX.map((ex, i) => `<path d="M${f(ex - 7.5)},${f(EY + 2)}q7.5,-10 15,0" stroke="${INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>${crinkle(ex, EY, i)}`).join("") + brows(-2, 0);
      return { eyes: { ...b.eyes, normal: set(), side: set(4, k0, 1), worry: set(0, k0, -4, -6), angry: set(0, k0 * 0.8, 3, 7), wide: set(0, k0 * 1.25, -7, -1), sad: set(0, k0 * 0.95, -1, 7), squint: set(0, k0 * 0.45, 1, 3), happy, tired, closed }, mouths: b.mouths };
    };
  }

  // ---------------- props in the near hand (flat: the hand is at 0,112 in the forearm) ----------------
  const PROP = {
    pen: `<g transform="translate(0,112) rotate(-28)"><rect x="-3.6" y="-48" width="7.2" height="62" rx="3" fill="#2a4a8a"/><path d="M-3.6,14L0,25L3.6,14Z" fill="#e8d0a8"/><path d="M-1.4,21L0,25L1.4,21Z" fill="#2a2220"/></g>`,
    spoon: `<g transform="translate(0,112) rotate(-24)"><ellipse cx="0" cy="-36" rx="11" ry="15" fill="#dfe4e8"/><ellipse cx="-3" cy="-40" rx="4" ry="6" fill="#fff" opacity=".7"/><rect x="-3" y="-22" width="6" height="52" rx="3" fill="#c3c8cd"/></g>`,
    phone: `<g transform="translate(0,112) rotate(-12)"><rect x="-19" y="-36" width="38" height="70" rx="7" fill="#1c2026"/><rect x="-15.5" y="-31" width="31" height="58" rx="4" fill="#a8d8f4"/><path d="M-12,-25L8,4M-5,-28L13,-3" stroke="#fff" stroke-width="1.6" opacity=".7"/></g>`,
    ladle: `<g transform="translate(0,112) rotate(-10)"><rect x="-3.4" y="-84" width="6.8" height="100" rx="3" fill="#aab0b6"/><path d="M-21,16Q-21,41 0,41Q21,41 21,16Z" fill="#c9cfd5"/><path d="M-21,16Q0,25 21,16" stroke="#8c9298" stroke-width="2.4" fill="none"/></g>`,
  };

  // ---------------- per-character specs ----------------
  const hood = (x) => { const c = dk(x.top, 0.2); return `<path d="M-47,-486Q-55,-522 -27,-528Q2,-505 31,-528Q57,-522 47,-486Q0,-470 -47,-486Z" fill="${c}"/>
    <path d="M-27,-528Q2,-505 31,-528" stroke="${dk(x.top, 0.32)}" stroke-width="3" fill="none"/>
    <path d="M-9,-478V-428M9,-478V-434" stroke="#f2ead8" stroke-width="3.2" stroke-linecap="round"/><circle cx="-9" cy="-426" r="3" fill="#f2ead8"/><circle cx="9" cy="-432" r="3" fill="#f2ead8"/>
    <path d="M-31,-372H31L37,-322H-37Z" fill="${dk(x.top, 0.1)}"/><path d="M-31,-372L-37,-322M31,-372L37,-322" stroke="${dk(x.top, 0.22)}" stroke-width="2.4"/>`; };
  const pencilEar = `<g transform="translate(-38,-556) rotate(-14)"><rect x="-3.4" y="-26" width="6.8" height="40" fill="#f2c230"/><rect x="-3.4" y="-26" width="2.2" height="40" fill="#d8a420"/>
    <path d="M-3.4,14L0,22L3.4,14Z" fill="#ead2ac"/><path d="M-1.3,18.5L0,22L1.3,18.5Z" fill="#2a2220"/><rect x="-3.4" y="-32" width="6.8" height="6" rx="2" fill="#e08a96"/></g>`;
  const apron = `<path d="M-41,-438H41L49,-206Q0,-194 -49,-206Z" fill="#f3ede2"/><path d="M-41,-438H-24L-28,-204Q-40,-204 -49,-206Z" fill="#1c2030" opacity=".1"/>
    <path d="M-38,-438L-26,-488M38,-438L26,-488" stroke="#f3ede2" stroke-width="7" stroke-linecap="round"/>
    <path d="M-24,-330h42v34h-42z" fill="#e6dccb"/><path d="M-4,-342v14" stroke="#3a6aa8" stroke-width="4" stroke-linecap="round"/>`;
  const towel = `<path d="M20,-494Q36,-498 46,-488L42,-372Q34,-366 24,-372Z" fill="url(#sgPlaid)"/><path d="M20,-494Q36,-498 46,-488L42,-372Q34,-366 24,-372Z" fill="#1c2030" opacity=".08"/>
    <path d="M25,-372l-1,9M30,-370l-1,10M35,-370l0,10M40,-372l1,9" stroke="#e8e2d6" stroke-width="2.4" stroke-linecap="round"/>`;
  Flat.SPEC.sgYou = { hair: "messy", glasses: "round", faces: sigFaces({ bags: true, browW: 4.8 }), acc: hood, headTop: () => pencilEar };
  Flat.SPEC.sgYai = { hair: "bunPin", faces: sigFaces({ crinkle: true, k: 0.82, browW: 3.4 }), acc: () => apron + towel,
    headTop: () => `<ellipse cx="31" cy="-530" rx="8.5" ry="5" fill="#e0705e" opacity=".26"/><ellipse cx="-17" cy="-530" rx="7" ry="4.6" fill="#e0705e" opacity=".2"/>` };

  // ---------------- cast entries (v2 data; FLAT builds them through the specs above) ----------------
  const C = Rig.CAST;
  C.sgYou = { v2: { skin: "#c68b60", hair: { c: "#1f1813" }, top: { kind: "tee", c: "#d9a43a", sleeve: "long" }, bottom: { kind: "trousers", c: "#2f3441" },
    feet: { kind: "sandal", c: "#2a5aa8" }, w: 1.04 } };
  C.sgYouPen = { v2: C.sgYou.v2, hand: PROP.pen, keep: "F" };
  C.sgYouSpoon = { v2: C.sgYou.v2, hand: PROP.spoon, keep: "F" };
  C.sgYouPhone = { v2: C.sgYou.v2, hand: PROP.phone, keep: "F" };
  C.sgYai = { v2: { skin: "#b47c55", hair: { c: "#e4e0d8" }, top: { kind: "tee", c: "#efe2cc", sleeve: "elbow", pat: "sgFloral" },
    bottom: { kind: "sarong", c: "#2e3458", band: "#c8963a" }, feet: { kind: "sandal", c: "#7a4a2a" }, w: 1.1, limb: 0.96 } };
  C.sgYaiLadle = { v2: C.sgYai.v2, hand: PROP.ladle, keep: "F" };
  C.sgYaiPhone = { v2: C.sgYai.v2, hand: PROP.phone, keep: "F" };
  window.Sig = { PROP, sigFaces };
})();
