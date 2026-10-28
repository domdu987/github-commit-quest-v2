// "ผีแม่ม่าย" EP.3 motion graphics (same language as mmui.js / mmui2.js): the family tree that carries the gene, the ECG strip that
// prints for every age, the implanted defibrillator from above, the medicine warning, and the small props for the village class.
//   MmUI.famTree(tl, layer, t0, dur, o)  three generations: ปู่ → พ่อ (black ribbon, died asleep at 35) + แม่, อา → เก่ง ฝน · บอส.
//                      The gene (a red helix) runs down the blood lines; rings: เก่ง เสี่ยง, ฝน and บอส ต้องตรวจ; the count "ไม่ต่ำกว่า 20 ยีน".
//                      o.at = { genes, count, rings } seconds after t0
//   MmUI.ecgPrint(tl, layer, t0, dur, o)  the ECG paper feeding out of the machine with its trace, then three age chips (เด็ก วัยรุ่น
//                      ผู้ใหญ่) under "ตรวจได้ทุกช่วงอายุ" · o.ages (s after t0)
//   Sets.icdTop(L, o)  chestTop (bare) with the implanted defibrillator under the left collarbone, its lead into the heart (x-ray)
//   MmUI.icdAnim(tl, id, t0, o)  x-ray in → the device slides under the skin → the lead draws into the heart → the label → a quiver on the
//                      little monitor, the device fires (bolt) and the rhythm comes back · o.dev, o.fire (s after t0)
//   MmUI.pills(tl, layer, t0, dur, o)    two cards (ยานอนหลับ / ยาสลบ) stamped "อาจกระตุ้นได้", then the banner "บอกหมอทุกครั้ง" (o.at [a, b, banner])
//   Mm.manikin(x, G, s, o)  a CPR training torso on a mat, side view, head to the left (chest top at about (0, -60)·s)
//   Mm.electrodes(x, y, s, id)  ECG stickers with leads, for a chest seen side-on
(function () {
  const f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const INK = "#26201c";
  const C = { red: "#e2382e", redD: "#a81e18", green: "#2fa864", greenD: "#1e7a48", yellow: "#ffd23a", orange: "#ff8a1a", paper: "#fdfaf2", grid: "#f4b8b0",
    skinK: "#b47448", skinF: "#e6b48a", skinB: "#d8a078", skinM: "#c08a62", skinU: "#a87048", skinG: "#c48c62" };
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const Mm = (window.Mm = window.Mm || {});
  let seq = 0;

  Sets.DEFS += `
    <linearGradient id="mu3Card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf8"/><stop offset="1" stop-color="#f2ecdc"/></linearGradient>
    <linearGradient id="mu3Metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eef2f6"/><stop offset=".5" stop-color="#b8c2cc"/><stop offset="1" stop-color="#8a96a2"/></linearGradient>
    <radialGradient id="mu3Helix"><stop offset="0" stop-color="#ff8a7a" stop-opacity=".9"/><stop offset="1" stop-color="#ff4a3a" stop-opacity="0"/></radialGradient>
    <pattern id="mu3Grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M0,0H20M0,0V20" stroke="#f0a8a0" stroke-width="1"/><path d="M0,10H20M10,0V20" stroke="#f8d0cc" stroke-width=".6"/></pattern>`;

  // a person as a portrait badge: shirt, neck, head, hair, face; o.kind picks the look
  const LOOK = {
    pu: { skin: "#c08a62", shirt: "#e8e2d4", hair: `<path d="M-30,-36Q0,-58 30,-36Q26,-46 0,-50Q-26,-46 -30,-36Z" fill="#e8e8e8"/>`, extra: `<path d="M-14,-6q14,8 28,0" stroke="#e8e8e8" stroke-width="5" fill="none"/>` },
    pho: { skin: "#a87048", shirt: "#56677a", hair: `<path d="M-32,-30Q-30,-58 0,-58Q30,-58 32,-30Q22,-44 0,-44Q-22,-44 -32,-30Z" fill="#1a1412"/>` },
    mae: { skin: "#c08a62", shirt: "#56677a", hair: `<path d="M-34,-24Q-36,-60 0,-60Q36,-60 34,-24L30,6Q24,-30 0,-34Q-24,-30 -30,6Z" fill="#2a1e18"/>` },
    a: { skin: "#a87048", shirt: "#b39a62", hair: `<path d="M-32,-32Q-28,-56 0,-56Q28,-56 32,-32Q18,-42 0,-42Q-18,-42 -32,-32Z" fill="#1a1412"/>` },
    keng: { skin: "#b47448", shirt: "#eef0f0", hair: `<path d="M-32,-30Q-30,-60 0,-60Q30,-60 32,-30L26,-40Q0,-50 -26,-40Z" fill="#1a1412"/>` },
    fon: { skin: "#e6b48a", shirt: "#e2a92e", hair: `<path d="M-34,-20Q-38,-62 0,-62Q38,-62 34,-20Q26,-44 0,-46Q-26,-44 -34,-20Z" fill="#1a1412"/><circle cx="30" cy="-48" r="9" fill="${C.red}" ${O(2.5)}/>`,
      extra: `<circle cx="-12" cy="-16" r="10" fill="none" stroke="${INK}" stroke-width="3"/><circle cx="12" cy="-16" r="10" fill="none" stroke="${INK}" stroke-width="3"/><path d="M-2,-16h4" stroke="${INK}" stroke-width="3"/>` },
    boss: { skin: "#d8a078", shirt: "#4a9a5a", s: 0.86, hair: `<path d="M-32,-28Q-30,-58 0,-58Q30,-58 32,-28Q16,-40 0,-40Q-16,-40 -32,-28Z" fill="#2a1e18"/>` },
  };
  const person = (kind, x, y, s, id, o = {}) => { const P = LOOK[kind], k = s * (P.s || 1);
    return `<g transform="translate(${x},${y}) scale(${f1(k)})"><g id="${id}"><circle r="70" fill="${o.bg || "#f2efe6"}" ${O(4)}/>
      <defs><clipPath id="${id}-cl"><circle r="66"/></clipPath></defs><g clip-path="url(#${id}-cl)">
        <path d="M-50,80Q-50,26 0,26Q50,26 50,80Z" fill="${P.shirt}" ${O(3.5)}/><rect x="-11" y="4" width="22" height="26" fill="${P.skin}"/>
        <ellipse cx="0" cy="-16" rx="30" ry="34" fill="${P.skin}" ${O(3.5)}/>${P.hair}<path d="M-12,-12h4M8,-12h4" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>
        <path d="M-8,6q8,5 16,0" stroke="${INK}" stroke-width="3" fill="none" stroke-linecap="round"/>${P.extra || ""}</g>
      ${o.ribbon ? `<path d="M40,-58l18,-6l6,18l-12,10z" fill="#111" ${O(2)}/><path d="M-66,0A66,66 0 0 0 66,0" stroke="#111" stroke-width="7" fill="none" opacity=".0"/>` : ""}
      ${o.gray ? `<circle r="66" fill="#fff" opacity=".35"/>` : ""}</g></g>`; };
  const helix = (x, y, s, id) => `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}"><circle r="30" fill="url(#mu3Helix)"/>
    <path d="M-10,-22C10,-14 10,-6 -10,2S10,18 -10,24M10,-22C-10,-14 -10,-6 10,2S-10,18 10,24" stroke="${C.red}" stroke-width="5" fill="none" stroke-linecap="round"/>
    ${[-16, -6, 4, 14].map((yy) => `<path d="M-7,${yy}H7" stroke="#ffb0a6" stroke-width="3"/>`).join("")}</g></g>`;

  // ---------------- the family tree ----------------
  function famTree(tl, layer, t0, dur, o = {}) {
    const id = `mft${seq++}`, at = o.at || {}, tG = t0 + (at.genes ?? 1.2), tC = t0 + (at.count ?? 2.6), tR = t0 + (at.rings ?? 3.4);
    const P = { pu: [540, 330], pho: [330, 610], mae: [130, 610], a: [770, 610], keng: [240, 900], fon: [450, 900], boss: [770, 900] };
    const lines = [["pu", "pho"], ["pu", "a"], ["pho", "keng"], ["pho", "fon"], ["a", "boss"]];
    let g = `<g transform="translate(0,0)"><g id="${id}-card" filter="url(#muDrop)"><rect x="40" y="150" width="1000" height="1010" rx="44" fill="url(#mu3Card)" ${O(5)}/></g>
      <text x="540" y="226" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="${INK}">ครอบครัวนี้</text></g>`;
    // marriage line, blood lines (drawn on), the gene dots that travel them
    g += `<path d="M200,610H262" stroke="#b8b0a0" stroke-width="7" stroke-dasharray="10 8"/>`;
    lines.forEach(([a, b], k) => { const [x0, y0] = P[a], [x1, y1] = P[b], my = (y0 + y1) / 2;
      const d = `M${x0},${y0 + 70}V${my}H${x1}V${y1 - 70}`;
      g += `<path id="${id}-l${k}" d="${d}" stroke="#c8beac" stroke-width="8" fill="none" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
        <path id="${id}-r${k}" d="${d}" stroke="${C.red}" stroke-width="8" fill="none" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" opacity=".85"/>`; });
    const names = { pu: "ปู่", pho: "พ่อ", mae: "แม่", a: "อา", keng: "เก่ง", fon: "ฝน", boss: "บอส" };
    Object.entries(P).forEach(([k, [x, y]]) => {
      g += person(k, x, y, 1, `${id}-p${k}`, { ribbon: k === "pho", gray: k === "mae" });
      g += `<text x="${x}" y="${y + 106}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="${INK}">${names[k]}</text>`;
    });
    g += `<g transform="translate(330,500)"><g id="${id}-died"><rect x="-120" y="-24" width="240" height="48" rx="24" fill="#2a2e34"/><text y="10" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="26" fill="#fff">ตายตอนหลับ อายุ 35</text></g></g>`;
    // rings and their tags
    [["keng", "เสี่ยง", C.red], ["fon", "ต้องตรวจ", C.orange], ["boss", "ต้องตรวจ", C.orange]].forEach(([k, t, col]) => { const [x, y] = P[k];
      g += `<g transform="translate(${x},${y})"><g id="${id}-ring-${k}" opacity="0"><circle r="84" fill="none" stroke="${col}" stroke-width="9"/><g transform="translate(0,-104)"><rect x="-74" y="-24" width="148" height="48" rx="24" fill="${col}" ${O(3)}/><text y="10" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="28" fill="#fff">${t}</text></g></g></g>`; });
    // the helix that rides each blood line, the count
    lines.forEach((_, k) => (g += `<g id="${id}-h${k}" opacity="0">${helix(0, 0, 0.9, `${id}-hx${k}`)}</g>`));
    g += `<g transform="translate(540,1086)"><g id="${id}-cnt" opacity="0"><rect x="-300" y="-46" width="600" height="92" rx="46" fill="${C.red}" ${O(4)}/>${helix(-240, 0, 0.9, `${id}-cx`)}
      <text x="24" y="16" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#fff">ไม่ต่ำกว่า <tspan id="${id}-n">0</tspan> ยีน</text></g></g>`;
    put(layer, `<g id="${id}">${g}</g>`);
    tl.fromTo(`#${id}`, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out", immediateRender: false }, t0);
    Object.keys(P).forEach((k, i) => tl.fromTo(`#${id}-p${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.45, ease: "back.out(2.4)", immediateRender: false }, t0 + 0.15 + [0, 1, 1, 1, 2, 2, 2][i] * 0.22 + i * 0.03));
    tl.fromTo(`#${id}-died`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.4, ease: "back.out(2.6)", immediateRender: false }, t0 + 0.7);
    lines.forEach((_, k) => tl.fromTo(`#${id}-l${k}`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power1.inOut", immediateRender: false }, t0 + 0.3 + (k < 2 ? 0 : 0.3)));
    // the gene: red flows down the lines, a helix riding the head of each
    lines.forEach((_, k) => { const tt = tG + (k < 2 ? 0 : 0.55), path = document.getElementById(`${id}-r${k}`), hx = document.getElementById(`${id}-h${k}`), len = path.getTotalLength(), pr = { p: 0 };
      tl.fromTo(`#${id}-r${k}`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.55, ease: "power1.in", immediateRender: false }, tt);
      tl.set(hx, { opacity: 1 }, tt); tl.set(hx, { opacity: 0 }, tt + 0.6);
      tl.fromTo(pr, { p: 0 }, { p: 1, duration: 0.55, ease: "power1.in", immediateRender: false, onUpdate: () => { const q = path.getPointAtLength(pr.p * len); hx.setAttribute("transform", `translate(${f1(q.x)},${f1(q.y)})`); } }, tt); });
    // the count runs up to 20
    tl.fromTo(`#${id}-cnt`, { opacity: 0, scale: 0.4, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.45, ease: "back.out(2.2)", immediateRender: false }, tC);
    const nEl = document.getElementById(`${id}-n`), cnt = { v: 0 };
    tl.fromTo(cnt, { v: 0 }, { v: 20, duration: 0.8, ease: "power2.out", immediateRender: false, onUpdate: () => { nEl.textContent = String(Math.round(cnt.v)); } }, tC + 0.2);
    ["keng", "fon", "boss"].forEach((k, i) => { tl.fromTo(`#${id}-ring-${k}`, { opacity: 0, scale: 1.5, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.4, ease: "back.out(2.6)", immediateRender: false }, tR + i * 0.18);
      for (let t = tR + 0.6 + i * 0.18; t < t0 + dur - 0.3; t += 0.8) { tl.to(`#${id}-ring-${k}`, { scale: 1.08, svgOrigin: "0 0", duration: 0.2, ease: "power2.out" }, t); tl.to(`#${id}-ring-${k}`, { scale: 1, svgOrigin: "0 0", duration: 0.35, ease: "power2.inOut" }, t + 0.2); } });
    tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
  }

  // ---------------- the ECG strip and the ages ----------------
  const sinus = (W, H, step) => { const c = H / 2; let d = `M0,${c}`; for (let bx = 60; bx < W; bx += step) d += `L${bx - 40},${c}Q${bx - 32},${c - 10} ${bx - 24},${c}L${bx - 8},${c}L${bx - 4},${c + 10}L${bx},${c - H * 0.4}L${bx + 6},${c + H * 0.2}L${bx + 11},${c}L${bx + 30},${c}Q${bx + 44},${c - 14} ${bx + 58},${c}`; return d + `L${W},${c}`; };
  function ecgPrint(tl, layer, t0, dur, o = {}) {
    const id = `mep${seq++}`, Y = o.y ?? 520, ages = o.ages || [1.6, 1.9, 2.2], W = 860, H = 230;
    let g = `<g transform="translate(110,${Y})"><g id="${id}-m" filter="url(#muDrop)"><rect x="-20" y="-120" width="${W + 40}" height="120" rx="22" fill="#2a2e34" ${O(4)}/><rect x="20" y="-92" width="220" height="64" rx="10" fill="#0e1418"/>
        <path d="M30,-60h40l8,-20l8,34l8,-24l6,10h40l8,-20l8,34l8,-24l6,10h40" stroke="#7aff9a" stroke-width="3" fill="none"/><circle cx="${W - 60}" cy="-60" r="16" fill="${C.green}"/><rect x="300" y="-40" width="${W - 420}" height="14" rx="7" fill="#111"/></g>
      <defs><clipPath id="${id}-cp"><rect id="${id}-feed" x="0" y="0" width="${W}" height="0"/></clipPath></defs>
      <g clip-path="url(#${id}-cp)"><rect x="0" y="0" width="${W}" height="${H}" fill="#fff6f4"/><rect x="0" y="0" width="${W}" height="${H}" fill="url(#mu3Grid)"/>
        <path d="${sinus(W, H, 150)}" stroke="#1a1412" stroke-width="4" fill="none" stroke-linejoin="round"/><text x="16" y="34" font-family="Kanit" font-weight="700" font-size="24" fill="#a84a3a">คลื่นไฟฟ้าหัวใจ</text></g></g>`;
    g += `<g transform="translate(540,${Y + H + 110})"><g id="${id}-t" opacity="0"><text text-anchor="middle" font-family="Kanit" font-weight="900" font-size="50" fill="#fff" stroke="#140c0a" stroke-width="9" paint-order="stroke">ตรวจได้ทุกช่วงอายุ</text></g></g>`;
    const AG = [["เด็ก", "boss"], ["วัยรุ่น", "fon"], ["ผู้ใหญ่", "keng"]];
    AG.forEach(([t, k], i) => { const x = 230 + i * 310;
      g += `<g transform="translate(${x},${Y + H + 300})"><g id="${id}-a${i}" opacity="0">${person(k, 0, 0, 1.05, `${id}-ap${i}`)}<g transform="translate(0,104)"><rect x="-80" y="-26" width="160" height="52" rx="26" fill="${C.green}" ${O(3.5)}/><text y="11" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="32" fill="#fff">${t}</text></g></g></g>`; });
    put(layer, `<g id="${id}">${g}</g>`);
    tl.fromTo(`#${id}-m`, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.6)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-feed`, { attr: { height: 0 } }, { attr: { height: H }, duration: Math.min(1.6, dur * 0.5), ease: "none", immediateRender: false }, t0 + 0.3);
    tl.fromTo(`#${id}-t`, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out", immediateRender: false }, t0 + ages[0] - 0.2);
    ages.forEach((ta, i) => tl.fromTo(`#${id}-a${i}`, { opacity: 0, scale: 0.3, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.45, ease: "back.out(2.6)", immediateRender: false }, t0 + ta));
    tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
  }

  // ---------------- the implanted defibrillator, from above ----------------
  function icdTop(L, o = {}) {
    const id = o.id || "ic";
    Sets.chestTop(L, { ...o, id, bare: true });
    // the bump under the skin (in the act layer, on the chest), the x-ray: heart, the device, its lead; the little monitor; labels
    put(L.act, `<g id="${id}-bump" opacity="0"><rect x="600" y="540" width="120" height="96" rx="34" fill="#c48a5e" stroke="#8e5430" stroke-width="4"/><path d="M612,552q50,-10 96,0" stroke="#e0a878" stroke-width="5" fill="none" opacity=".7"/></g>`);
    put(L.glow, `<g id="${id}-xh" opacity="0" style="mix-blend-mode:screen"><path d="M520,700C470,690 440,740 452,790C466,850 520,880 560,900C600,870 640,830 640,780C640,730 600,700 570,712C556,700 540,698 520,700Z" fill="#ff8a7a" opacity=".35" stroke="#ffb0a6" stroke-width="6"/></g>
      <g id="${id}-dev" opacity="0"><rect x="604" y="544" width="112" height="88" rx="30" fill="url(#mu3Metal)" stroke="#5a6672" stroke-width="5"/><rect x="624" y="560" width="72" height="20" rx="8" fill="#7a8692"/><circle cx="660" cy="606" r="9" fill="#4ad0ff"/></g>
      <path id="${id}-lead" d="M610,590C560,600 540,640 548,700C556,760 560,820 556,880" stroke="#dfe8f0" stroke-width="9" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
      <g id="${id}-zap" opacity="0"><path d="M640,640l-40,70h34l-26,64l66,-90h-36l26,-44z" fill="${C.yellow}" stroke="#fff3c0" stroke-width="4"/></g>`);
    put(L.light, `<g id="${id}-lab" opacity="0"><path d="M720,590L800,520H850" stroke="#fffaf0" stroke-width="5" fill="none"/><g transform="translate(880,470)"><rect x="-150" y="-30" width="300" height="60" rx="30" fill="#4ad0ff" ${O(4)}/><text y="11" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="${INK}">เครื่องกระตุกหัวใจ</text></g>
      <g transform="translate(880,540)"><text text-anchor="middle" font-family="Kanit" font-weight="700" font-size="28" fill="#fff" stroke="#140c0a" stroke-width="7" paint-order="stroke">ฝังใต้ผิวหนังหน้าอก</text></g></g>
      <g id="${id}-mon" opacity="0"><g transform="translate(180,1160)"><rect x="-150" y="-70" width="300" height="140" rx="20" fill="#14181e" ${O(4)}/>
        <defs><clipPath id="${id}-mc"><rect id="${id}-ms" x="-130" y="-56" width="0" height="112"/></clipPath></defs><g clip-path="url(#${id}-mc)">
        <path d="M-130,0${Array.from({ length: 16 }, (_, k) => `L${-130 + (k + 1) * 6},${(k % 2 ? 22 : -22) * (0.6 + 0.4 * Math.sin(k))}`).join("")}L-34,0L-24,0L-18,-40L-12,24L-6,0H20L26,-40L32,24L38,0H64L70,-40L76,24L82,0H130" stroke="#7aff9a" stroke-width="4" fill="none" stroke-linejoin="round"/></g>
        <path d="M-40,-50v100" stroke="${C.yellow}" stroke-width="4" stroke-dasharray="6 6"/></g></g>`);
  }
  function icdAnim(tl, id, t0, o = {}) {
    const dev = t0 + (o.dev ?? 0.6), fire = t0 + (o.fire ?? 2.6);
    tl.set([`#${id}-arms`, `#${id}-xr`, `#${id}-low`, `#${id}-lowl`], { opacity: 0 }, t0);
    tl.to(`#${id}-xh`, { opacity: 1, duration: 0.4 }, t0 + 0.1);
    for (let t = t0 + 0.3; t < t0 + (o.end ?? 4.5) - 0.2; t += 0.85) { tl.to(`#${id}-xh`, { scale: 1.06, svgOrigin: "546 800", duration: 0.12, ease: "power2.out" }, t); tl.to(`#${id}-xh`, { scale: 1, svgOrigin: "546 800", duration: 0.35, ease: "power2.inOut" }, t + 0.12); }
    tl.fromTo(`#${id}-dev`, { opacity: 0, x: 120, y: -80, scale: 1.4, svgOrigin: "660 588" }, { opacity: 1, x: 0, y: 0, scale: 1, svgOrigin: "660 588", duration: 0.5, ease: "back.out(1.8)", immediateRender: false }, dev);
    tl.to(`#${id}-bump`, { opacity: 1, duration: 0.3 }, dev + 0.3);
    tl.fromTo(`#${id}-lead`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.6, ease: "power1.inOut", immediateRender: false }, dev + 0.4);
    tl.fromTo(`#${id}-lab`, { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(2)", immediateRender: false }, dev + 0.6);
    tl.to(`#${id}-mon`, { opacity: 1, duration: 0.3 }, fire - 0.9);
    tl.fromTo(`#${id}-ms`, { attr: { width: 0 } }, { attr: { width: 260 }, duration: 1.6, ease: "none", immediateRender: false }, fire - 0.9);
    tl.fromTo(`#${id}-zap`, { opacity: 1, scale: 0.6, svgOrigin: "620 700" }, { opacity: 0, scale: 1.3, svgOrigin: "620 700", duration: 0.35, ease: "power2.out", immediateRender: false }, fire);
    tl.fromTo(`#${id}-dev`, { filter: "brightness(1.8)" }, { filter: "brightness(1)", duration: 0.3, immediateRender: false }, fire);
  }

  // ---------------- the medicine warning ----------------
  function pills(tl, layer, t0, dur, o = {}) {
    const id = `mpl${seq++}`, at = o.at || [0.2, 0.7, 2.2], Y = o.y ?? 470;
    const BOTTLE = `<rect x="-34" y="-30" width="68" height="84" rx="12" fill="#f4f0e6" ${O(4)}/><rect x="-38" y="-52" width="76" height="26" rx="8" fill="#4a7ad8" ${O(4)}/><rect x="-26" y="-6" width="52" height="40" rx="6" fill="#dfe8f8"/>
      <path d="M8,2a14,14 0 1 0 0,26a10,10 0 1 1 0,-26z" fill="#2a3a7a"/><circle cx="-12" cy="10" r="3" fill="#2a3a7a"/>`;
    const MASK = `<path d="M-40,10Q-40,-30 0,-34Q40,-30 40,10Q40,40 0,44Q-40,40 -40,10Z" fill="#cfe8f4" ${O(4)}/><path d="M-26,8Q0,-10 26,8" stroke="#8ab0c8" stroke-width="4" fill="none"/>
      <path d="M0,44V70Q0,84 20,84H50" stroke="#6a8aa0" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M-40,0L-62,-14M40,0L62,-14" stroke="${INK}" stroke-width="4"/>`;
    const card = (x, art, t, k) => `<g transform="translate(${x},${Y})"><g id="${id}-c${k}" opacity="0"><g filter="url(#muDrop)"><rect x="-200" y="-190" width="400" height="380" rx="36" fill="#fffaf2" ${O(5)}/></g>
      <g transform="translate(0,-50) scale(1.6)">${art}</g><text y="110" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="46" fill="${INK}">${t}</text>
      <g transform="translate(0,160) rotate(-6)"><g id="${id}-s${k}"><rect x="-150" y="-30" width="300" height="60" rx="12" fill="none" stroke="${C.red}" stroke-width="7"/><text y="12" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="32" fill="${C.red}">อาจกระตุ้นได้</text></g></g></g></g>`;
    let g = card(300, BOTTLE, "ยานอนหลับ", 0) + card(780, MASK, "ยาสลบ", 1);
    g += `<g transform="translate(540,${Y + 330})"><g id="${id}-b" opacity="0"><rect x="-330" y="-50" width="660" height="100" rx="50" fill="${C.green}" ${O(5)}/>
      <g transform="translate(-270,0) scale(.7)"><circle r="40" fill="#fff"/><path d="M-14,-24v18a14,14 0 0 0 28,0v-18M0,8v14q0,16 18,16" stroke="${INK}" stroke-width="6" fill="none"/><circle cx="18" cy="40" r="8" fill="${INK}"/></g>
      <text x="30" y="16" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#fff">บอกหมอทุกครั้ง</text></g></g>`;
    put(layer, `<g id="${id}">${g}</g>`);
    [0, 1].forEach((k) => { tl.fromTo(`#${id}-c${k}`, { opacity: 0, y: 60, rotation: k ? 6 : -6, svgOrigin: "0 0" }, { opacity: 1, y: 0, rotation: k ? 2 : -2, svgOrigin: "0 0", duration: 0.5, ease: "back.out(1.8)", immediateRender: false }, t0 + at[k]);
      tl.fromTo(`#${id}-s${k}`, { opacity: 0, scale: 2.2, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.22, ease: "power4.in", immediateRender: false }, t0 + at[k] + 0.6); });
    tl.fromTo(`#${id}-b`, { opacity: 0, scale: 0.5, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.5, ease: "back.out(2.2)", immediateRender: false }, t0 + at[2]);
    tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
  }

  // ---------------- props ----------------
  Mm.manikin = (x, G, s = 1, o = {}) => `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})"><g id="${o.id || "mk"}"><rect x="-150" y="-14" width="300" height="20" rx="8" fill="#3a6ad8" ${O(3)}/>
    <circle cx="-118" cy="-52" r="36" fill="#f0d2b0" ${O(4)}/><path d="M-86,-90H96Q120,-90 120,-66V-14H-86Z" fill="#f0d2b0" ${O(4)}/><path d="M-60,-84Q20,-104 100,-84" stroke="#d8b090" stroke-width="5" fill="none"/>
    <circle cx="10" cy="-70" r="10" fill="#e2382e" opacity=".7"/></g></g>`;
  Mm.electrodes = (x, y, s, id) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><g id="${id}">${[[-60, 0], [-20, -8], [20, -10], [60, -6], [100, 0]].map(([dx, dy]) => `<circle cx="${dx}" cy="${dy}" r="11" fill="#fbfbf8" stroke="#8a96a2" stroke-width="3"/><circle cx="${dx}" cy="${dy}" r="4" fill="#c8ccd0"/>`).join("")}
    ${[[-60, 0], [-20, -8], [20, -10], [60, -6], [100, 0]].map(([dx, dy], k) => `<path d="M${dx},${dy - 10}C${dx + 20},${dy - 80} ${160 + k * 10},-120 ${240 + k * 6},-60" stroke="${["#e2382e", "#ffd23a", "#2fa864", "#2f6fd0", "#8a5ad8"][k]}" stroke-width="3" fill="none"/>`).join("")}</g></g>`;

  Object.assign(Sets, { icdTop });
  Object.assign(window.MmUI, { famTree, ecgPrint, icdAnim, pills });
})();
