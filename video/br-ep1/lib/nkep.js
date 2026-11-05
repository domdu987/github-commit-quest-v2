// นิวเคลียร์ลงกรุงเทพ EP.2–3: the family's mother and what happens at the door.
//   Rig.CAST.mae / maeBag     แม่ ~48: short perm, rose blouse, dark slacks, sandals · maeBag holds her shoulder bag in the front hand
//   NkE.bucket(x, y, s)       a blue plastic bucket of water with a dipper        NkE.bottle(x, y, s, kind)  "shampoo" | "cond" (pink, ครีมนวด)
//   NkE.soap(x, y, s)         a bar on its dish                                   NkE.towel(x, y, s)          a folded towel
//   NkE.salt(x, y, s)         a pack of iodised salt                              NkE.iodine(x, y, s)         a small brown antiseptic bottle (no brand)
//   NkE.sheet(x, y, w, h)     the plastic sheet of the washing corner             NkE.ban(x, y, s)            a red "no" ring with its bar
//   NkE.paws(pts, s, col)     a cat's paw prints along [[x, y, rot]…]             NkE.handbag(x, y, s)        her bag
// Everything is flat: ink outline, 2–3 tones, one highlight — the look of the EP.1 props.
(function () {
  const INK = "#14181a", f1 = (v) => (+v).toFixed(1);
  const O = (w = 4, c = INK) => `stroke="${c}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const T = (x, y, size, txt, o = {}) => `<text x="${x}" y="${y}" font-family="Kanit" font-weight="${o.w || 800}" font-size="${size}" fill="${o.fill || INK}" text-anchor="middle">${txt}</text>`;
  const at = (x, y, s, body) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">${body}</g>`;

  const handbag = (x, y, s) => at(x, y, s, `<path d="M-46,-118Q0,-196 46,-118" stroke="#5a3a2a" stroke-width="10" fill="none" stroke-linecap="round"/>
    <path d="M-70,-112H70L82,10Q82,24 66,24H-66Q-82,24 -82,10Z" fill="#8a4a3a" ${O(5)}/><path d="M-70,-112H70L74,-70Q0,-50 -74,-70Z" fill="#a85a46"/>
    <rect x="-12" y="-80" width="24" height="16" rx="4" fill="#e8c860" ${O(3)}/><path d="M-60,-96Q0,-104 60,-96" stroke="#fff" stroke-width="4" opacity=".3" fill="none"/>`);
  const C = Rig.CAST;
  C.mae = { v2: { ...C.bua.v2, skin: "#d6a27a", lip: "#b04a50", top: { kind: "blouse", c: "#c9607c", sleeve: "elbow", trim: "#f2d4dc" }, extra: "",
    bottom: { kind: "trousers", c: "#33364a" }, feet: { kind: "sandal", c: "#5a3a2a" }, face: "" } };
  C.maeBag = { v2: C.mae.v2, hand: handbag(0, 168, 0.48), keep: "F" };
  if (window.Flat) Flat.SPEC.mae = { hair: "perm",
    print: () => [[-24, -440], [12, -452], [30, -404], [-8, -392], [-30, -350], [20, -346]].map(([x, y]) =>
      `<g transform="translate(${x},${y})"><circle r="6" fill="#f6dce4"/><circle r="2.4" fill="#e8b84a"/></g>`).join("") };

  const bucket = (x, y, s) => at(x, y, s, `<ellipse cx="0" cy="4" rx="96" ry="14" fill="#000" opacity=".25"/>
    <path d="M-80,-150L-64,0H64L80,-150Z" fill="#2f78c8" ${O(5)}/><path d="M-80,-150L-74,-96H74L80,-150Z" fill="#3a8ad8"/><path d="M-50,-140L-40,-14" stroke="#fff" stroke-width="7" opacity=".25" stroke-linecap="round"/>
    <ellipse cx="0" cy="-150" rx="80" ry="18" fill="#9ad0ec" ${O(5)}/><ellipse cx="-10" cy="-152" rx="40" ry="6" fill="#fff" opacity=".45"/>
    <path d="M-80,-150Q0,-260 80,-150" stroke="#1e4a80" stroke-width="7" fill="none"/>
    <g transform="translate(46,-170) rotate(24)"><ellipse rx="30" ry="12" fill="#f2c230" ${O(4)}/><rect x="26" y="-6" width="70" height="12" rx="6" fill="#f2c230" ${O(4)}/></g>`);
  const bottle = (x, y, s, kind = "shampoo") => { const c = kind === "cond" ? "#f2a8c4" : "#f4f2ea", lb = kind === "cond" ? "#d8507e" : "#3a9a5a";
    return at(x, y, s, `<ellipse cx="0" cy="4" rx="44" ry="8" fill="#000" opacity=".25"/>
      <path d="M-34,0V-120Q-34,-150 -14,-156V-176H14V-156Q34,-150 34,-120V0Z" fill="${c}" ${O(5)}/><rect x="-20" y="-196" width="40" height="22" rx="5" fill="${lb}" ${O(4)}/>
      <rect x="-28" y="-104" width="56" height="64" rx="6" fill="${lb}"/>${T(0, -66, 19, kind === "cond" ? "ครีม" : "แชมพู", { fill: "#fff" })}${T(0, -46, 15, kind === "cond" ? "นวดผม" : "", { fill: "#fff" })}
      <path d="M-24,-130V-20" stroke="#fff" stroke-width="6" opacity=".35" stroke-linecap="round"/>`); };
  const soap = (x, y, s) => at(x, y, s, `<ellipse cx="0" cy="2" rx="70" ry="16" fill="#cfd8dc" ${O(4)}/><rect x="-44" y="-40" width="88" height="36" rx="16" fill="#9fd8c8" ${O(4)}/>
    <path d="M-30,-30h40" stroke="#fff" stroke-width="5" opacity=".5" stroke-linecap="round"/><circle cx="34" cy="-52" r="9" fill="#fff" opacity=".8" ${O(2)}/><circle cx="50" cy="-66" r="6" fill="#fff" opacity=".8" ${O(2)}/>`);
  const towel = (x, y, s) => at(x, y, s, `<ellipse cx="0" cy="4" rx="96" ry="12" fill="#000" opacity=".22"/><rect x="-90" y="-46" width="180" height="46" rx="10" fill="#f2d24a" ${O(5)}/>
    <rect x="-90" y="-82" width="180" height="40" rx="10" fill="#f6dc6a" ${O(5)}/><path d="M-90,-62h180M-90,-24h180" stroke="#d8b030" stroke-width="5"/>`);
  const salt = (x, y, s) => at(x, y, s, `<ellipse cx="0" cy="4" rx="64" ry="10" fill="#000" opacity=".25"/>
    <path d="M-56,0L-60,-150Q-60,-166 -44,-168H44Q60,-166 60,-150L56,0Z" fill="#f4f6f8" ${O(5)}/><path d="M-60,-150H60" stroke="${INK}" stroke-width="4"/>
    <rect x="-46" y="-130" width="92" height="74" rx="8" fill="#2a64b0"/>${T(0, -96, 26, "เกลือ", { fill: "#fff" })}${T(0, -66, 17, "ไอโอดีน", { fill: "#cfe4ff", w: 700 })}
    <path d="M-40,-40h80M-40,-24h60" stroke="#c8ccd2" stroke-width="5" stroke-linecap="round"/>`);
  const iodine = (x, y, s) => at(x, y, s, `<ellipse cx="0" cy="4" rx="40" ry="8" fill="#000" opacity=".25"/>
    <path d="M-32,0V-92Q-32,-112 -14,-116V-130H14V-116Q32,-112 32,-92V0Z" fill="#7a3a1a" ${O(5)}/><rect x="-16" y="-160" width="32" height="32" rx="6" fill="#f4f2ea" ${O(4)}/>
    <rect x="-24" y="-82" width="48" height="54" rx="5" fill="#f4f2ea"/>${T(0, -56, 15, "ยาใส่", { w: 700 })}${T(0, -38, 15, "แผล", { w: 700 })}
    <path d="M-22,-100V-12" stroke="#c8784a" stroke-width="6" opacity=".6" stroke-linecap="round"/>`);
  const sheet = (x, y, w, h) => `<g><path d="M${f1(x - w / 2)},${f1(y)}L${f1(x + w / 2)},${f1(y)}L${f1(x + w / 2 + 40)},${f1(y + h)}L${f1(x - w / 2 - 40)},${f1(y + h)}Z" fill="#9ab8c8" opacity=".55" ${O(3, "#5a7484")}/>
    <path d="M${f1(x - w / 4)},${f1(y + 4)}L${f1(x - w / 4 - 20)},${f1(y + h - 4)}M${f1(x + w / 5)},${f1(y + 4)}L${f1(x + w / 5 + 18)},${f1(y + h - 4)}" stroke="#fff" stroke-width="4" opacity=".35"/></g>`;
  const ban = (x, y, s) => at(x, y, s, `<circle r="74" fill="none" stroke="#d8443a" stroke-width="18"/><path d="M-52,-52L52,52" stroke="#d8443a" stroke-width="18" stroke-linecap="round"/>`);
  // a cat's paw: the pad and four toes, rotated to the way it walked
  const paw = (x, y, rot, s, col) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(rot)}) scale(${s})" fill="${col}"><ellipse cx="0" cy="6" rx="13" ry="11"/>
    <ellipse cx="-14" cy="-10" rx="5" ry="6.5"/><ellipse cx="-5" cy="-17" rx="5" ry="6.5"/><ellipse cx="5" cy="-17" rx="5" ry="6.5"/><ellipse cx="14" cy="-10" rx="5" ry="6.5"/></g>`;
  const paws = (pts, s = 1, col = "#cfc8b8") => pts.map(([x, y, rot], i) => paw(x + (i % 2 ? 12 : -12) * s, y, rot, s * (0.7 + 0.3 * (y / 1900)), col)).join("");

  C.maeTank = { v2: { ...C.mae.v2, top: { kind: "singlet", c: "#efe8dc" } } };   // her outer blouse off: the vest underneath
  C.maeTowel = { v2: { ...C.mae.v2, top: { kind: "singlet", c: "#efe8dc" } }, hand: `<g transform="translate(0,150) scale(.4)"><rect x="-90" y="-40" width="180" height="80" rx="12" fill="#f6dc6a" stroke="${INK}" stroke-width="5"/></g>`, keep: "F" };

  // falling fallout: grey grains drifting down across a box, looping on the shot clock (layer = a world layer)
  function fall(tl, layer, t0, dur, o = {}) {
    const [bx, by, bw, bh] = o.box || [-100, -200, 1280, 2200], n = o.n ?? 70, r = ((s) => () => (s = (s * 16807) % 2147483647) / 2147483647)(o.seed || 5);
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g"); layer.appendChild(g);
    let h = "";
    for (let k = 0; k < n; k++) { const x = bx + r() * bw, y = by + r() * bh, rr = (o.r ?? 3) * (0.6 + r() * 0.9);
      h += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(rr)}" fill="${o.col || "#d8d0c0"}" opacity="${f1(0.45 + r() * 0.5)}"/>`; }
    g.innerHTML = `<g>${h}</g><g transform="translate(0,${-bh})">${h}</g>`;
    const sp = o.speed ?? 160;   // px per second; two copies stacked so the loop never shows a seam
    tl.fromTo(g, { y: 0, x: 0 }, { y: sp * dur, x: (o.drift ?? 18) * dur, duration: dur, ease: "none" }, t0);
    return g;
  }

  // the car-park mouth from outside at dusk, fallout coming down: concrete face, the closed shutter, the ramp, a lamp, the street
  Sets.nkDoorOut = (L, o = {}) => {
    const sh = o.shutter ?? 1, bottom = 1460 - 520 * (1 - sh);
    L.sky.insertAdjacentHTML("beforeend", `<defs><linearGradient id="nkdoSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3040"/><stop offset=".55" stop-color="#9a6050"/><stop offset="1" stop-color="#e0a070"/></linearGradient></defs>
      <rect x="-1300" y="-900" width="3700" height="3900" fill="url(#nkdoSky)"/>`);
    let far = "";
    [[-120, 380], [60, 260], [210, 420], [380, 300], [560, 460], [740, 280], [900, 380], [1060, 320]].forEach(([x, h], k) =>
      far += `<rect x="${x}" y="${720 - h}" width="${150 + (k % 3) * 20}" height="${h + 40}" fill="#6a4a54" opacity=".75"/>`);
    L.far.insertAdjacentHTML("beforeend", far);
    let s = `<rect x="-900" y="700" width="2900" height="900" fill="url(#n2Conc)"/><rect x="-900" y="690" width="2900" height="26" fill="#7a7068"/>
      <rect x="200" y="860" width="680" height="${f1(bottom - 860 + 20)}" fill="#3a3c40"/>
      <rect x="220" y="880" width="640" height="${f1(bottom - 880)}" fill="#a8acb2" stroke="${INK}" stroke-width="5"/>`;
    for (let y = 905; y < bottom - 10; y += 34) s += `<path d="M224,${y}H856" stroke="#7a7e86" stroke-width="8"/><path d="M224,${y + 6}H856" stroke="#d4d8de" stroke-width="3"/>`;
    s += `<rect x="220" y="${f1(bottom - 28)}" width="640" height="28" fill="#6a6e76" stroke="${INK}" stroke-width="4"/>
      <g transform="translate(540,800)"><rect x="-150" y="-40" width="300" height="80" rx="10" fill="#1e5a9a" stroke="${INK}" stroke-width="4"/>${T(0, 16, 40, "P ที่จอดรถ B1", { fill: "#fff" })}</g>
      <path d="M-900,1460H2000V2600H-900Z" fill="#7a746c"/><path d="M200,1460L-200,1920M880,1460L1280,1920" stroke="#5a5650" stroke-width="10"/>
      <path d="M-900,1470H2000" stroke="#c8c0b0" stroke-width="14" opacity=".7"/>
      <rect x="-900" y="1480" width="2900" height="440" fill="#c8c0b0" opacity=".28"/>
      <path d="M980,1460V820M980,820h60" stroke="#4a4644" stroke-width="12"/><circle cx="1046" cy="826" r="13" fill="#fff2c8"/>`;
    L.set.insertAdjacentHTML("beforeend", `<g id="${o.id || "ndo"}-deck">${s}</g>`);
    L.glow.insertAdjacentHTML("beforeend", `<circle cx="1046" cy="826" r="120" fill="url(#nkBloom)" opacity=".35"/>`);
  };

  // the knowledge card: grey grains settle on the person's hair, shoulders and clothes; water runs over them and they fall away
  function washCard(tl, layer, t0, dur, o = {}) {
    const id = `nkw${Math.floor(Math.random() * 1e9)}`, y0 = o.y ?? 230;
    const r = ((s) => () => (s = (s * 16807) % 2147483647) / 2147483647)(9);
    let grains = "";
    [[540, y0 + 170, 70, 26], [440, y0 + 390, 60, 14], [640, y0 + 390, 60, 14], [540, y0 + 520, 110, 30]].forEach(([cx, cy, w, n]) => {
      for (let k = 0; k < n; k++) grains += `<circle cx="${f1(cx + (r() - 0.5) * w * 2)}" cy="${f1(cy + (r() - 0.5) * 50)}" r="${f1(4 + r() * 5)}" fill="#8a8478"/>`; });
    let water = ""; for (let k = 0; k < 14; k++) water += `<path d="M${380 + k * 24},${y0 + 60}v${60 + (k % 4) * 30}" stroke="#7ac8f0" stroke-width="7" stroke-linecap="round"/>`;
    layer.insertAdjacentHTML("beforeend", `<g id="${id}"><rect x="140" y="${y0}" width="800" height="${o.h ?? 760}" rx="34" fill="#f4efe2" stroke="${INK}" stroke-width="6"/>
      <g id="${id}-p"><circle cx="540" cy="${y0 + 220}" r="78" fill="#e8c09a" stroke="${INK}" stroke-width="6"/><path d="M462,${y0 + 200}Q470,${y0 + 120} 540,${y0 + 118}Q610,${y0 + 120} 618,${y0 + 200}Q590,${y0 + 160} 540,${y0 + 162}Q490,${y0 + 160} 462,${y0 + 200}Z" fill="#3a2a22"/>
        <path d="M380,${y0 + 640}Q380,${y0 + 360} 540,${y0 + 350}Q700,${y0 + 360} 700,${y0 + 640}Z" fill="#c9607c" stroke="${INK}" stroke-width="6"/></g>
      <g id="${id}-w" opacity="0">${water}</g><g id="${id}-g">${grains}</g>
      ${(o.labels || [["ผม", 760, y0 + 170], ["ไหล่", 760, y0 + 390], ["เสื้อ", 760, y0 + 540]]).map(([t, x, y]) => `<g class="lb"><path d="M${x - 60},${y}H${x - 140}" stroke="${INK}" stroke-width="4"/>${T(x, y + 14, 40, t)}</g>`).join("")}
      <g id="${id}-ok" opacity="0"><circle cx="400" cy="${y0 + (o.h ?? 760) - 62}" r="40" fill="#2f9a5a" stroke="${INK}" stroke-width="5"/><path d="M380,${y0 + (o.h ?? 760) - 62}l14,14l24,-26" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        ${T(580, y0 + (o.h ?? 760) - 46, 46, o.ok || "ล้างออกได้")}</g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, t0);
    tl.fromTo(`#${id}-g circle`, { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.006, ease: "power2.in" }, t0 + 0.2);
    const wa = t0 + (o.washAt ?? dur * 0.5);
    tl.fromTo(`#${id}-w`, { opacity: 0, y: -30 }, { opacity: 1, y: 30, duration: 0.5, ease: "none" }, wa);
    tl.to(`#${id}-w`, { opacity: 0, duration: 0.3 }, wa + 0.9);
    tl.to(`#${id}-g circle`, { y: 520, opacity: 0, duration: 0.8, stagger: 0.004, ease: "power2.in" }, wa + 0.15);
    tl.fromTo(`#${id}-ok`, { opacity: 0, scale: 0.6, svgOrigin: `400 ${y0 + (o.h ?? 760) - 62}` }, { opacity: 1, scale: 1, svgOrigin: `400 ${y0 + (o.h ?? 760) - 62}`, duration: 0.35, ease: "back.out(3)" }, wa + 0.7);
    return id;
  }

  // EP.3 · a phone held up (screen content in phone coords, 0..260 × 0..520), a torch, two cells, the school card
  const phone = (x, y, s, screen = "", o = {}) => at(x, y, s, `<rect x="-150" y="-300" width="300" height="600" rx="40" fill="#14181a"/>
    <rect x="-136" y="-270" width="272" height="540" rx="24" fill="${o.bg || "#20283a"}"/><rect x="-40" y="-288" width="80" height="12" rx="6" fill="#2e3440"/>
    <g transform="translate(-136,-270)">${screen}</g>`);
  const bars = (n) => [0, 1, 2, 3].map((k) => `<rect x="${222 + k * 10}" y="${22 - k * 5}" width="7" height="${8 + k * 5}" rx="2" fill="${k < n ? "#f4f2ea" : "#5a6070"}"/>`).join("");
  const torch = (x, y, s, rot = 0) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${s})"><rect x="-90" y="-26" width="140" height="52" rx="10" fill="#2a2e34" ${O(5)}/>
    <path d="M50,-36H96Q104,-36 104,-28V28Q104,36 96,36H50Z" fill="#c8ccd2" ${O(5)}/><circle cx="104" cy="0" r="26" fill="#fff4c8" opacity=".25"/>
    <rect x="-40" y="-36" width="36" height="12" rx="4" fill="#d8443a" ${O(3)}/><path d="M-80,-14H30" stroke="#fff" stroke-width="5" opacity=".2" stroke-linecap="round"/></g>`;
  const cell = (x, y, s, rot = 0) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${s})"><rect x="-22" y="-60" width="44" height="120" rx="8" fill="#2f78c8" ${O(4)}/>
    <rect x="-22" y="-60" width="44" height="34" rx="8" fill="#e8c840" ${O(4)}/><rect x="-8" y="-72" width="16" height="12" rx="3" fill="#c8ccd2" ${O(3)}/>${T(0, 22, 26, "AA", { fill: "#fff" })}</g>`;
  // the card: the school's basement (the child stays) · the road between, grey with fallout (the parent does not go)
  function schoolCard(tl, layer, t0, dur, o = {}) {
    const id = `nks${Math.floor(Math.random() * 1e9)}`, y0 = o.y ?? 240;
    layer.insertAdjacentHTML("beforeend", `<g id="${id}"><rect x="110" y="${y0}" width="860" height="700" rx="34" fill="#f4efe2" stroke="${INK}" stroke-width="6"/>
      <g transform="translate(330,${y0 + 360})"><rect x="-150" y="-200" width="300" height="200" fill="#d8c8a8" stroke="${INK}" stroke-width="5"/><path d="M-170,-200L0,-290L170,-200Z" fill="#c85a3a" stroke="${INK}" stroke-width="5"/>
        ${[-90, -30, 30, 90].map((x) => `<rect x="${x - 18}" y="-170" width="36" height="40" fill="#7ac0e8" stroke="${INK}" stroke-width="3"/>`).join("")}
        <path d="M-180,0H180" stroke="${INK}" stroke-width="6"/><rect x="-150" y="0" width="300" height="130" fill="#8a7a6a" stroke="${INK}" stroke-width="5"/>
        <g id="${id}-kid"><circle cx="-30" cy="60" r="18" fill="#e8c09a" stroke="${INK}" stroke-width="4"/><path d="M-52,118Q-52,84 -30,84Q-8,84 -8,118Z" fill="#f4f2ea" stroke="${INK}" stroke-width="4"/>
          <circle cx="30" cy="62" r="16" fill="#e8c09a" stroke="${INK}" stroke-width="4"/><path d="M10,118Q10,86 30,86Q50,86 50,118Z" fill="#2a64b0" stroke="${INK}" stroke-width="4"/></g>
        ${T(0, 190, 40, o.inLabel || "อยู่ที่นั่น")}</g>
      <g transform="translate(760,${y0 + 360})"><rect x="-130" y="-200" width="260" height="330" rx="16" fill="#c8c0b0" opacity=".6"/>
        ${Array.from({ length: 22 }, (_, k) => `<circle cx="${-110 + ((k * 53) % 220)}" cy="${-180 + ((k * 89) % 300)}" r="${4 + (k % 3) * 2}" fill="#8a8478"/>`).join("")}
        <circle cx="0" cy="-60" r="26" fill="#e8c09a" stroke="${INK}" stroke-width="4"/><path d="M-36,40Q-36,-24 0,-24Q36,-24 36,40Z" fill="#9ab4cc" stroke="${INK}" stroke-width="4"/>
        <path d="M-20,40L-30,110M20,40L30,110" stroke="${INK}" stroke-width="10" stroke-linecap="round"/>
        <g id="${id}-x"><circle cx="0" cy="-20" r="110" fill="none" stroke="#d8443a" stroke-width="16"/><path d="M-78,-98L78,58" stroke="#d8443a" stroke-width="16" stroke-linecap="round"/></g>
        ${T(0, 190, 40, o.outLabel || "ออกไปรับ")}</g>
      <path d="M560,${y0 + 360}h40" stroke="${INK}" stroke-width="5"/></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, t0);
    tl.fromTo(`#${id}-x`, { scale: 0, svgOrigin: `0 -20` }, { scale: 1, svgOrigin: `0 -20`, duration: 0.35, ease: "back.out(3)" }, t0 + (o.xAt ?? dur * 0.55));
    return id;
  }
  window.NkE = { handbag, bucket, bottle, soap, towel, salt, iodine, sheet, ban, paws, fall, washCard, phone, bars, torch, cell, schoolCard };
})();
