// "ท่อนซุงลงเขา" cast (rig v2), built on the channel's adult v2 bodies with this story's own hair and clothes:
//   jeng      เจ๋ง 28, the driver: short side-parted hair, a denim shirt with the sleeves rolled to the elbow over a white tee, dark jeans
//   ning      หนิง 31, his older sister: black hair in a high top-knot, sunglasses pushed up on her head, a mustard tee, light jeans
//             · ningPhone (phone in the front fist; poses phoneLook / raise)
// Scene: Sets.ltCabin(L, o) — the two-shot through the windscreen from the bonnet: rear window behind them (o.rear "grille" = the big
//   chrome grille glued to the back window, o.beam the high beams), headrests, dashboard, the wheel in front of เจ๋ง (screen left,
//   right-hand drive), A-pillars, sliding tree reflections on the glass. Actors go in by the engine: เจ๋ง x≈330, หนิง x≈760, y 1560, s 1.
(function () {
  const { LINE } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const base = (k) => (C[k] && C[k].v2) || {};

  const sidePart = (h) => `<path d="M-50,-548C-56,-606 -20,-628 6,-628C36,-627 58,-606 52,-548Q44,-580 30,-590Q-6,-596 -36,-574Q-44,-562 -50,-548Z" fill="${h.c}" ${ln()}/>
    <path d="M-30,-596Q4,-618 40,-598" stroke="${h.sh}" stroke-width="6" fill="none" opacity=".7" stroke-linecap="round"/><path d="M-8,-626Q-14,-604 -36,-578" stroke="${h.s}" stroke-width="3" fill="none"/>`;
  const knotFront = (h) => `<path d="M-50,-540C-58,-604 -22,-630 4,-630C34,-629 60,-604 52,-540Q48,-574 34,-586Q0,-578 -34,-586Q-46,-570 -50,-540Z" fill="${h.c}" ${ln()}/>
    <path d="M-26,-606Q4,-620 34,-604" stroke="${h.sh}" stroke-width="6" fill="none" opacity=".7" stroke-linecap="round"/>`;
  const knotBack = (h) => `<g><circle cx="2" cy="-648" r="28" fill="${h.c}" ${ln()}/><path d="M-12,-662Q2,-672 16,-660" stroke="${h.sh}" stroke-width="5" fill="none" opacity=".7"/><path d="M-22,-628Q2,-618 26,-628" stroke="#d8302a" stroke-width="7" stroke-linecap="round"/></g>`;
  const shades = `<g transform="translate(0,-604)"><path d="M-44,0Q-46,-14 -30,-16H-8Q2,-14 0,0Q-4,12 -22,12Q-40,12 -44,0Z" fill="#1e2228" ${ln(2)}/><path d="M44,0Q46,-14 30,-16H8Q-2,-14 0,0Q4,12 22,12Q40,12 44,0Z" fill="#1e2228" ${ln(2)}/>
    <path d="M-34,-8l10,-4M16,-8l10,-4" stroke="#fff" stroke-width="3" opacity=".5" stroke-linecap="round"/></g>`;
  const tee = `<path d="M-20,-486Q0,-470 20,-486" stroke="#f4f2ee" stroke-width="9" fill="none"/>`;

  const km = base("keng");
  C.jeng = { v2: { ...km, skin: "#c8905e", w: 1.02, hair: { c: "#1a1410", s: "#000", sh: "#5a4a40", front: (x) => sidePart(x.hair) }, faceTop: "",
    top: { kind: "shirt", c: "#4a78a8", sleeve: "elbow", neck: "collar", collar: "#3e6890", button: "#e8e4d8" }, print: tee, extra: "",
    bottom: { kind: "jeans", c: "#2a3446" }, feet: { kind: "sneaker", c: "#e8e4dc", mark: "#4a78a8" } } };
  const mv = base("mint");
  C.ning = { v2: { ...mv, skin: "#e2b088", hair: { c: "#16100c", s: "#000", sh: "#5a4434", front: (x) => knotFront(x.hair), back: (x) => knotBack(x.hair) }, faceTop: shades,
    top: { kind: "tee", c: "#d8a62a", sleeve: "short" }, print: `<path d="M-30,-420h60" stroke="#fff4d8" stroke-width="6" opacity=".7"/><path d="M-22,-404h44" stroke="#fff4d8" stroke-width="6" opacity=".5"/>`,
    bottom: { kind: "jeans", c: "#9ab8d8" }, feet: { kind: "sneaker", c: "#f6f4ee", mark: "#d8a62a" } } };
  const phone = () => `<g transform="translate(0,118) rotate(-10)"><rect x="-13" y="-26" width="26" height="46" rx="5" fill="#2a2a32" ${ln(2)}/><rect x="-10" y="-22" width="20" height="36" rx="2" fill="#8ac8f0"/></g>`;
  C.ningPhone = { ...C.ning, hand: phone(), keep: "F" };

  // ---------------------------------------------------------------- the two-shot through the windscreen
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const f1 = (v) => (+v).toFixed(1);
  Sets.ltCabin = function (L, o = {}) {
    const id = o.id || "lc", r = mk(o.seed || 233), INK = "#2e2a26";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#1e1b18"/>`);
    // the rear window: sky, the road dropping behind, the follower (grille) and its beams
    let rw = `<clipPath id="${id}-rw"><path d="M120,640Q540,560 960,640L1000,960H80Z"/></clipPath><g clip-path="url(#${id}-rw)"><rect x="0" y="540" width="1080" height="440" fill="url(#ltSky)"/>
      <path d="M0,820L300,760L600,800L1080,740V980H0Z" fill="url(#ltRidge2)"/><path d="M380,980L520,810H560L700,980Z" fill="#6a6e74"/>`;
    if (o.rear === "grille") rw += `<g id="${id}-fol" transform="translate(540,${o.folY ?? 1180}) scale(${o.folS ?? 0.62})">${Lt.tankerFront(`${id}-tk`, 0, 0, 1, { plate: false, beam: o.beam ?? 0 })}</g>`;
    rw += `<rect x="0" y="540" width="1080" height="440" fill="#d8e4ec" opacity=".18"/></g><path d="M120,640Q540,560 960,640L1000,960H80Z" fill="none" stroke="#0e0c0a" stroke-width="18"/>`;
    put(L.far, `<rect x="-900" y="-600" width="2900" height="3400" fill="#2a2622"/><path d="M-900,420Q540,330 2000,420V1100H-900Z" fill="#33302b"/>` + rw);
    // headrests and seat backs
    put(L.mid, [320, 770].map((x) => `<g><rect x="${x - 110}" y="840" width="220" height="180" rx="40" fill="#3e3a34" stroke="#1a1816" stroke-width="5"/><rect x="${x - 10}" y="996" width="8" height="40" fill="#8a8e94"/><rect x="${x + 4}" y="996" width="8" height="40" fill="#8a8e94"/>
      <path d="M${x - 170},1040Q${x},1000 ${x + 170},1040V1700H${x - 170}Z" fill="#4a453e" stroke="#1a1816" stroke-width="6"/><path d="M${x - 130},1080V1640M${x + 130},1080V1640" stroke="#3a362f" stroke-width="10"/></g>`).join(""));
    // dashboard, wheel, windscreen frame, glass reflections (fg: in front of the actors)
    let fg = `<path d="M-900,1300Q540,1220 2000,1300V2800H-900Z" fill="url(#ltDash)"/><path d="M-900,1300Q540,1220 2000,1300" stroke="#4a443c" stroke-width="10" fill="none"/>`;
    fg += `<g transform="translate(320,1340)"><ellipse rx="300" ry="90" fill="none" stroke="#0e0d0c" stroke-width="34"/><ellipse rx="300" ry="90" fill="none" stroke="#2c2926" stroke-width="22"/><path d="M0,70V0" stroke="#1c1a18" stroke-width="40"/></g>`;
    fg += `<path d="M380,1290h120v40h-120z" fill="#0b0d10"/><text x="440" y="1320" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="26" fill="#7fd1ff">${o.clock || "14:20"}</text>`;
    // the bonnet edge and wipers at the very bottom, the pillars and roof outside the glass
    fg += `<path d="M-900,1720Q540,1640 2000,1720V2800H-900Z" fill="url(#ltMint)" stroke="${INK}" stroke-width="6"/><path d="M60,1700L420,1640M640,1640L1000,1690" stroke="#141210" stroke-width="12" stroke-linecap="round"/>`;
    fg += `<path d="M-900,-600H2000V560Q1500,500 1060,470L960,560Q540,520 120,560L20,470Q-420,500 -900,560Z" fill="url(#ltMint)" stroke="${INK}" stroke-width="6"/>`;
    fg += `<path d="M20,470L120,560L-60,1720H-900V560Q-420,500 20,470Z" fill="#5ea88e" stroke="${INK}" stroke-width="6"/><path d="M1060,470L960,560L1140,1720H2000V560Q1500,500 1060,470Z" fill="#5ea88e" stroke="${INK}" stroke-width="6"/>`;
    // reflections sliding over the glass (class dap — Lt.life slides them): sky streaks and tree shadows
    fg += `<g opacity=".9">${Array.from({ length: 5 }, (_, k) => `<path class="dap" d="M${f1(-200 + k * 300)},560L${f1(40 + k * 300)},560L${f1(-180 + k * 300)},1700L${f1(-420 + k * 300)},1700Z" fill="${k % 2 ? "#ffffff" : "#1e3a2a"}" opacity="${k % 2 ? 0.08 : 0.12}"/>`).join("")}</g>`;
    put(L.fg, fg);
    put(L.glow, `<g id="${id}-hibeam" opacity="${o.beam ?? 0}"><ellipse cx="540" cy="780" rx="620" ry="260" fill="url(#ltHead)" opacity=".8"/></g>`);
  };
})();
