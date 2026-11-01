// "ห้องสอบ" cast (rig v2 · load after tidecast.js for v2.skirt / keep, and after fencecast.js for its poses)
//   fon     ฝน 15 (ม.3): a long ponytail with a navy ribbon, white school blouse with a navy bow and the school emblem, a navy
//           pleated skirt, white socks + black shoes · fonPhone (her phone in the hand)
//   beam    บีม 15 (ม.3): messy spiky hair, white school shirt untucked, khaki shorts, white socks + black shoes · beamPhone (filming)
//   orn     ครูอร 40: hair in a low bun, glasses, a lilac blouse with a teacher's lanyard, a long dark-green skirt, flat shoes
//   st1 st2 st3   classmates (boy, girl, boy) for the rows
//   zs1 zs2       ผีห่า… no: the infected students (boy / girl): grey-green skin, milky glowing eyes ("glow"), torn uniform, no blood
(function () {
  const { LINE, dk, hi } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const emblem = `<circle cx="-30" cy="-430" r="11" fill="#2c5a8a" ${ln(1.8)}/><path d="M-30,-436v12M-36,-430h12" stroke="#ffd23a" stroke-width="2.5"/><text x="-18" y="-404" font-family="Kanit" font-weight="800" font-size="12" fill="#2c5a8a">น.ส.</text>`;
  const bow = `<path d="M0,-484l-24,-12v24ZM0,-484l24,-12v24Z" fill="#1e2a5a" ${ln(2)}/><circle cx="0" cy="-484" r="5" fill="#1e2a5a" ${ln(1.8)}/><path d="M-6,-478l-8,30M6,-478l8,30" stroke="#1e2a5a" stroke-width="6" stroke-linecap="round"/>`;
  const pleat = (c) => `<g><path d="M-62,-336Q-70,-260 -78,-200H78Q70,-260 62,-336Z" fill="${c}" ${ln(2.6)}/>${[-50, -26, 0, 26, 50].map((x) => `<path d="M${x * 0.8},-332L${x * 1.2},-202" stroke="${dk(c, 0.35)}" stroke-width="2.4"/>`).join("")}<path d="M-62,-336H62" stroke="${dk(c, 0.3)}" stroke-width="6"/></g>`;
  const fonFront = (h) => `<path d="M-48,-550C-56,-610 -18,-630 6,-628C34,-628 58,-606 51,-550Q44,-574 30,-584Q12,-596 -8,-590Q-24,-586 -36,-574Q-44,-562 -48,-550Z" fill="${h.c}" ${ln()}/>
    <path d="M-8,-626Q-40,-610 -44,-566" stroke="${h.s}" stroke-width="2.4" fill="none"/><path d="M-26,-614Q4,-628 30,-614" stroke="${h.sh}" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>`;
  const fonBack = (h) => `<path d="M14,-626Q66,-650 74,-600Q84,-540 70,-470Q64,-430 74,-400Q50,-410 48,-460Q52,-540 30,-608Z" fill="${h.c}" ${ln()}/><path d="M44,-628q14,-14 28,0q-14,14 -28,0z" fill="#1e2a5a" ${ln(2)}/>`;
  const spiky = (h) => `<path d="M-48,-552C-58,-600 -40,-624 -22,-626L-36,-644L-10,-632L-4,-658L12,-632L28,-654L32,-628Q58,-620 52,-552Q46,-576 30,-586Q12,-592 -6,-586Q-26,-590 -38,-576Q-46,-564 -48,-552Z" fill="${h.c}" ${ln()}/>`;
  const bun = (h) => `<path d="M-46,-550C-52,-606 -16,-624 4,-624C30,-623 54,-604 49,-550Q46,-572 34,-586Q18,-594 4,-588Q-12,-596 -28,-588Q-42,-576 -46,-550Z" fill="${h.c}" ${ln()}/>`;
  const bunBack = (h) => `<circle cx="30" cy="-590" r="24" fill="${dk(h.c, 0.06)}" ${ln()}/>`;
  const glasses = `<g fill="none" stroke="#3a2a2a" stroke-width="3"><rect x="-38" y="-566" width="30" height="24" rx="8"/><rect x="12" y="-566" width="30" height="24" rx="8"/><path d="M-8,-556h20"/></g>`;
  const lanyard = `<path d="M-24,-490L-6,-400M24,-490L6,-400" stroke="#2c5a8a" stroke-width="5"/><rect x="-18" y="-402" width="36" height="46" rx="4" fill="#fbfaf4" ${ln(2)}/><rect x="-12" y="-394" width="24" height="16" fill="#9ab8d8"/>`;
  const socks = (side) => ({ shin: `<path d="M-16,96H16V132H-16Z" fill="#f4f4f0" ${ln(2)}/>` });
  const tear = `<path d="M-50,-360l12,-16l10,18l12,-14l10,16" fill="none" stroke="${LINE}" stroke-width="2.2"/><path d="M-40,-440q10,30 -4,60M30,-400q14,20 0,50" stroke="#6a6a5a" stroke-width="10" opacity=".25" fill="none" stroke-linecap="round"/>`;
  const zFace = `<path d="M-40,-560q10,-6 22,-2M20,-562q12,-4 22,2" stroke="#2a3020" stroke-width="3" fill="none"/><path d="M-30,-520q6,8 0,18M30,-518q-4,10 2,18" stroke="#4a5a3a" stroke-width="3" fill="none" opacity=".6"/>`;
  const shirt = (c = "#f8f8f4") => ({ kind: "shirt", c, sleeve: "short", neck: "collar", collar: "#ffffff", button: "#e8e8e8", trim: "#e0e0dc" });

  const fon = { skin: "#e8b890", iris: "#3a2418", lash: true, blush: 0.6, lip: "#d0645a",
    hair: { c: "#1e140f", s: "#0a0604", sh: "#5a4034", front: (x) => fonFront(x.hair), back: (x) => fonBack(x.hair) },
    top: { kind: "blouse", c: "#f8f8f4", sleeve: "short" }, print: bow + emblem, bottom: { kind: "shorts", c: "#22306a" },
    feet: { kind: "sneaker", c: "#1e1e24", sole: "#f4f4f4" }, skirt: pleat("#22306a"), legs: socks };
  const beam = { skin: "#c88a5a", iris: "#2a1a10", blush: 0.4,
    hair: { c: "#1a1410", s: "#000", sh: "#5a4a40", front: (x) => spiky(x.hair) },
    top: shirt(), print: emblem, bottom: { kind: "shorts", c: "#a8946a" }, feet: { kind: "sneaker", c: "#1e1e24", sole: "#f4f4f4" }, legs: socks };
  const orn = { skin: "#d8a47a", iris: "#3a2418", lash: true, blush: 0.4, lip: "#b84a4a",
    hair: { c: "#2a1a14", s: "#140c08", sh: "#6a4a3a", front: (x) => bun(x.hair), back: (x) => bunBack(x.hair) },
    top: { kind: "blouse", c: "#c8b4e0", sleeve: "elbow", trim: "#a890c8" }, bottom: { kind: "sarong", c: "#2a4a3a", band: "#2a4a3a", band2: "#2a4a3a" },
    feet: { kind: "sandal", c: "#3a2a20" }, extra: lanyard, face: glasses };
  const st = (skin, hair, girl) => ({ skin, iris: "#2a1a10", blush: 0.4, lash: girl,
    hair: { c: hair, s: dk(hair, 0.4), sh: hi(hair, 0.3), front: (x) => (girl ? bun(x.hair) : spiky(x.hair)) },
    top: girl ? { kind: "blouse", c: "#f8f8f4", sleeve: "short" } : shirt(), print: girl ? bow + emblem : emblem,
    bottom: { kind: "shorts", c: girl ? "#22306a" : "#a8946a" }, feet: { kind: "sneaker", c: "#1e1e24" }, ...(girl ? { skirt: pleat("#22306a") } : {}), legs: socks });
  const zs = (girl) => ({ ...st("#8e9e80", "#2a2420", girl), iris: "#e8f0d8", blush: 0, bags: true, print: (girl ? bow : "") + tear, face: zFace,
    top: girl ? { kind: "blouse", c: "#dcdcd0", sleeve: "short" } : shirt("#dcdcd0") });
  Object.assign(C, {
    fon: { v2: fon }, beam: { v2: beam }, orn: { v2: orn },
    st1: { v2: st("#d8a070", "#1a1410", false) }, st2: { v2: st("#f0c4a0", "#2a1a14", true) }, st3: { v2: st("#b8804e", "#120c08", false) },
    zs1: { v2: zs(false) }, zs2: { v2: zs(true) },
    beamPhone: { v2: beam, hand: `<g transform="translate(0,118) rotate(-10)"><rect x="-20" y="-40" width="40" height="76" rx="7" fill="#1a1c22" ${ln(2.2)}/><rect x="-15" y="-34" width="30" height="62" rx="4" fill="#5a7080"/><circle cx="0" cy="20" r="5" fill="#e2382e"/></g>`, keep: "F" },
    fonPhone: { v2: fon, hand: `<g transform="translate(0,118) rotate(-10)"><rect x="-20" y="-40" width="40" height="76" rx="7" fill="#1a1c22" ${ln(2.2)}/><rect x="-15" y="-34" width="30" height="62" rx="4" fill="#1e3a5a"/></g>`, keep: "F" },
  });
  const M = Rig.MODES;
  M.film = M.film || ((u, o) => ({ ...M.idle(u, o), uaF: -80, faF: -60, head: 4 }));
  M.drag = (u, o) => ({ ...M.idle(u, o), uaF: -70, faF: -10, uaB: -64, faB: -8, torso: -16 + 3 * Math.sin(u * 8), head: -6, thF: -20, shF: 30, thB: 24, shB: 10, bodyY: 18 });
  M.crouchHide = (u, o) => ({ ...M.crouch(u, o), uaF: -100, faF: -150, head: 6 });

  // บีม's fall (stagger back 0–0.3 s → butt hits the floor 0.3–0.55 → scoots away on hands and heels, never still)
  const sm = (x) => { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); }, lp = (a, b, k) => a + (b - a) * k;
  M.fallBack = (u, o) => {
    const k1 = sm(u / 0.3), k2 = sm((u - 0.3) / 0.25), sc = Math.max(0, u - 0.55), w = Math.sin(sc * 13), pw = Math.max(0, w);
    const st = { thF: lp(0, -10, k1), shF: lp(0, 20, k1), thB: lp(0, 26, k1), shB: lp(0, 30, k1), torso: lp(0, -24, k1), head: lp(0, -14, k1), uaF: lp(0, -130, k1), faF: lp(0, -70, k1), uaB: lp(0, -110, k1), faB: lp(0, -60, k1), bodyY: lp(0, 20, k1), rootX: lp(0, -60, k1) };
    const sit = { thF: -84 + 10 * w, shF: 14 + 34 * pw, thB: -82 - 10 * w, shB: 18 + 34 * Math.max(0, -w), torso: -16 + 3 * w, head: -6 + 4 * Math.sin(u * 19), uaF: 46, faF: -14, uaB: 56, faB: -10, bodyY: 290 - 8 * pw, rootX: -120 - 150 * sc - 10 * pw };
    const r = {}; Object.keys(sit).forEach((j) => (r[j] = lp(st[j], sit[j], k2))); return { ...M.idle(u, o), ...r, hair: 6 * Math.sin(u * 17) };
  };
  // pulling a heavy desk backwards: leaning far back, front leg braced, feet slipping every ~0.7 s, arms straight out
  M.dragHard = (u, o) => {
    const ph = (u % 0.7) / 0.7, slip = ph < 0.18 ? Math.sin((ph / 0.18) * Math.PI) : 0, j = Math.sin(u * 23);
    return { ...M.idle(u, o), torso: -26 + 4 * Math.sin(u * 7) - 6 * slip, head: -12 + 3 * j, uaF: -84 + 4 * j, faF: -14, uaB: -78 - 4 * j, faB: -10,
      thF: -42 - 16 * slip, shF: 18 + 10 * slip, thB: 26, shB: 34, bodyY: 36 + 5 * Math.sin(u * 7) + 16 * slip, rootX: -18 * slip, rootR: -4 - 3 * slip, hair: -8 + 4 * j };
  };
  // shoving from behind: leaning hard in, little steps
  M.shove = (u, o) => { const j = Math.sin(u * 9); return { ...M.idle(u, o), torso: 24 + 3 * j, head: 8, uaF: -96, faF: -8, uaB: -90, faB: -6, thF: -30 + 18 * j, shF: 30, thB: 30 - 18 * j, shB: 24, bodyY: 26 + 4 * Math.abs(j) }; };
  // hiding, trembling, breath held (never quite still)
  M.hideShake = (u, o) => { const t = Math.sin(u * 31) * 0.8 + Math.sin(u * 17) * 0.6; return { ...M.crouchHide(u, o), head: 6 + t, uaF: -100 + t, torso: 22 + 0.6 * t, bodyY: 115 + 0.8 * Math.sin(u * 2.2) }; };
})();
