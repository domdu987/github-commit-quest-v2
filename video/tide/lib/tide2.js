// "ทะเลลด" EP.2 sets — the close-ups and the places EP.1 did not need. Same look and contract as tide.js (layers sky / far / mid / set /
// act / fg, glow above the darkness; ink #2e2a26; gradients only, no SVG filters; seeded RNG; everything that moves is redrawn from the
// timeline clock by one proxy tween per call, so any seek gives the same frame). Load after tide.js (shares Tide._st); uses Rig2 and
// TideCast at build time only. Set coordinates are screen coordinates at the identity camera fr(540, 960, 1).
//
//   Sets.tideGrab(L, o)    the insert on the wet concrete evacuation steps (eerie light, seen steeply from above, the flight going down
//                          toward the bottom of the frame): a handrail post's foot bolted to a tread, a red sea-almond leaf stuck to the
//                          wet concrete, puddles holding the pale sky. จูน's left forearm comes up from the bottom of the frame (the lilac
//                          oversized sleeve, the pink scrunchie on her wrist), her hand straining open, while she lunges down the steps;
//                          ตาจุ่น's old left hand (dark weathered skin, big knuckles, raised veins, age spots, a faded rope-burn scar
//                          across the back of the hand, the rolled cuff of his teal work shirt and the edge of his orange life vest) is
//                          off frame until it shoots in from the top left and clamps her wrist. One of her pink flip-flops skids on the
//                          wet tread, tips over the step's edge and drops to the step below.
//                          o.grip [x, y] where the clamp happens (560, 760); everything is drawn 1.45× round it (a close-up at the
//                          identity camera) · o.sandal false leaves the flip-flop out · o.seed
//                          ids (redrawn): #id-her (her arm; #id-hf her fingers), #id-his (his arm; #id-hopen / #id-hshut the open and the
//                          closed hand, #id-hk the knuckles' pressure), #id-shd (both arms' shadows on the steps), #id-sq (her wrist's
//                          skin squeezed between his fingers), #id-spd (speed lines), #id-hit (the clamp's impact marks), #id-drops
//                          (water flung off her fingers), #id-flop (the flip-flop) + #id-skid (its wet trail) + #id-spray
//   Tide.grab(tl, id, t0, dur, o)      runs it: her wrist is carried down toward the bottom of the frame by her lunge, his hand shoots in
//                          and clamps it exactly o.at seconds into the call (0.5; put it on the narrator's
//                          "อย่า"; it comes in over the last 0.22 s, fastest at the end): squash on contact, her hand jerks and splays, flinging water, the momentum carries both down a little
//                          and he hauls her back up and holds — his knuckles pale as the grip tightens, both arms trembling with the
//                          strain; the flip-flop skids from o.at + 0.04. o.hold false: he never comes (her arm only)
(function () {
  const { mk, f1, put, crown, blob } = Pop2;
  const T = Qk.tone;
  const INK = "#2e2a26";
  const Tide = (window.Tide = window.Tide || {});
  const ST = (Tide._st = Tide._st || {});
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const sm = (a, b, x) => { const k = clamp((x - a) / (b - a), 0, 1); return k * k * (3 - 2 * k); };
  const lerp = (a, b, k) => a + (b - a) * k;
  const el = (id) => document.getElementById(id);
  const P2 = (p) => `${f1(p[0])},${f1(p[1])}`;
  const ln = (w = 3) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  // a tapered capsule from A (width wa) to B (width wb): fingers, forearms, posts
  const cap = (A, B, wa, wb) => {
    const dx = B[0] - A[0], dy = B[1] - A[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l;
    const a1 = [A[0] + (nx * wa) / 2, A[1] + (ny * wa) / 2], a2 = [A[0] - (nx * wa) / 2, A[1] - (ny * wa) / 2], b1 = [B[0] + (nx * wb) / 2, B[1] + (ny * wb) / 2], b2 = [B[0] - (nx * wb) / 2, B[1] - (ny * wb) / 2];
    return `M${P2(a1)}L${P2(b1)}A${f1(wb / 2)},${f1(wb / 2)} 0 0 0 ${P2(b2)}L${P2(a2)}A${f1(wa / 2)},${f1(wa / 2)} 0 0 0 ${P2(a1)}Z`;
  };
  // SVG that must stand in front of the cast: appended to L.act and moved after the actors once the shot is built (as tide.js does)
  const front = (L, id, svg) => {
    L.act.insertAdjacentHTML("beforeend", `<g id="${id}">${svg}</g>`);
    const g = el(id);
    queueMicrotask(() => { if (g && g.parentNode) g.parentNode.appendChild(g); });
  };

  Sets.DEFS += `
    <linearGradient id="t2Tread" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b4b0a4"/><stop offset=".55" stop-color="#9c988c"/><stop offset="1" stop-color="#86827a"/></linearGradient>
    <linearGradient id="t2Riser" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5e5a52"/><stop offset="1" stop-color="#77736a"/></linearGradient>
    <linearGradient id="t2Sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e8e6d8" stop-opacity="0"/><stop offset=".55" stop-color="#eeead8" stop-opacity=".1"/><stop offset=".8" stop-color="#f4eed8" stop-opacity=".34"/><stop offset="1" stop-color="#f4eed8" stop-opacity=".1"/></linearGradient>
    <linearGradient id="t2Pud" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e6e2cc"/><stop offset=".5" stop-color="#c8ccc0"/><stop offset="1" stop-color="#9aa8aa"/></linearGradient>
    <linearGradient id="t2Steel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8e969a"/><stop offset=".45" stop-color="#e8ecec"/><stop offset="1" stop-color="#9aa2a6"/></linearGradient>
    <linearGradient id="t2Leaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0a040"/><stop offset=".5" stop-color="#d8562a"/><stop offset="1" stop-color="#a8301a"/></linearGradient>
    <linearGradient id="t2Lilac" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9c86d8"/><stop offset=".45" stop-color="#c2b0f0"/><stop offset="1" stop-color="#a08ae0"/></linearGradient>
    <linearGradient id="t2Teal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fa0a2"/><stop offset=".6" stop-color="#6f8e90"/><stop offset="1" stop-color="#55706f"/></linearGradient>
    <radialGradient id="t2Flop" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#ff9cc6"/><stop offset=".7" stop-color="#ec6aa0"/><stop offset="1" stop-color="#c84a80"/></radialGradient>
    <radialGradient id="t2Shd"><stop offset="0" stop-color="#14120e" stop-opacity=".5"/><stop offset="1" stop-color="#14120e" stop-opacity="0"/></radialGradient>`;

  // =====================================================================================================================================
  // the wrist grab
  // =====================================================================================================================================
  // her arm, drawn with the middle of her wrist at (0, 0): the forearm goes down (+y) to the oversized lilac sleeve, the hand up (−y),
  // the back of her left hand to us (thumb on the right), the fingers splayed and trembling (#id-hf, scaled by the redraw)
  const JN = { sk: "#ebc19c", skD: "#c8916c", skL: "#f8dcc0", nail: "#f6d2cc" };
  function herArm(id) {
    const { sk, skD, skL, nail } = JN;
    // the oversized lilac sleeve: a loose tube from the frame's bottom up to its hem at y ≈ 390, the dark inside of the opening, then the
    // forearm coming out of it (96 wide at the wrist, 124 where it leaves the sleeve), then the near lip of the hem over it
    let g = `<path d="M-128,384Q0,356 134,386L196,1700H-176Z" fill="url(#t2Lilac)" ${ln(3.2)}/>
      <path d="M-96,470Q-84,900 -120,1500M36,450Q52,900 44,1600M110,470Q140,800 150,1300" stroke="#8a74c8" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/>
      <path d="M-50,480Q-30,900 -40,1500" stroke="#e4dcff" stroke-width="10" fill="none" opacity=".35" stroke-linecap="round"/>
      <ellipse cx="4" cy="394" rx="122" ry="34" fill="#5a4892" ${ln(2.6)}/><ellipse cx="4" cy="402" rx="104" ry="22" fill="#3e306a"/>`;
    g += `<path d="${cap([0, 0], [6, 352], 92, 122)}" fill="${sk}" ${ln(3)}/><path d="M26,40Q36,200 38,380" stroke="${skD}" stroke-width="14" fill="none" opacity=".35" stroke-linecap="round"/>
      <path d="M-24,60Q-30,220 -22,370" stroke="${skL}" stroke-width="10" fill="none" opacity=".45" stroke-linecap="round"/><path d="M-8,150q10,30 6,70" stroke="${skD}" stroke-width="2.4" fill="none" opacity=".5"/>
      <path d="M-126,396Q4,446 132,396Q130,418 4,462Q-122,420 -126,396Z" fill="#cdbff4" ${ln(2.8)}/><path d="M-100,412Q4,446 108,412" stroke="#f0eaff" stroke-width="4" fill="none" opacity=".7" stroke-linecap="round"/>`;
    // the scrunchie: a ruffled pink ring round the wrist below his grip
    let ruf = "";
    for (let k = 0; k <= 10; k++) { const x = -60 + k * 12.4, y = 100 + 6 * Math.sin(k * 1.9); ruf += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="9" ry="22" fill="${k % 2 ? "#ff8ec0" : "#f06aa4"}" ${ln(2)}/>`; }
    g += `<path d="M-62,88Q0,74 64,88L66,118Q0,132 -64,118Z" fill="#e85a98" ${ln(2.6)}/>${ruf}<path d="M-50,92Q0,80 52,92" stroke="#ffd0e4" stroke-width="4" fill="none" opacity=".7" stroke-linecap="round"/>`;
    // the hand: the back of the palm, tendons, knuckle dimples
    let h = `<path d="M-50,-40Q-62,-110 -60,-176Q-30,-196 8,-196Q48,-194 66,-170Q74,-110 54,-40Q30,-20 0,-22Q-30,-22 -50,-40Z" fill="${sk}" ${ln(3)}/>
      <path d="M-34,-56Q-36,-120 -40,-168M-10,-56Q-10,-120 -14,-176M14,-56Q16,-120 14,-178M36,-60Q42,-118 42,-168" stroke="${skD}" stroke-width="3" fill="none" opacity=".4" stroke-linecap="round"/>
      <path d="M-24,-60Q-24,-120 -28,-170" stroke="${skL}" stroke-width="7" fill="none" opacity=".5" stroke-linecap="round"/>`;
    // fingers (pinky … index, left to right) and the thumb on the right: splayed, the tips a little bent back
    const F = [[-44, -176, -22, 96, 25], [-16, -190, -8, 124, 29], [14, -192, 4, 134, 30], [42, -180, 16, 118, 29]];
    let fi = "";
    F.forEach(([x, y, a, l, w]) => {
      const r = (a * Math.PI) / 180, B = [x + Math.sin(r) * l, y - Math.cos(r) * l], M2 = [x + Math.sin(r) * l * 0.5, y - Math.cos(r) * l * 0.5];
      fi += `<path d="${cap([x, y], B, w, w * 0.84)}" fill="${sk}" ${ln(2.8)}/>`;
      fi += `<path d="M${f1(M2[0] - w * 0.3)},${f1(M2[1])}q${f1(w * 0.3)},4 ${f1(w * 0.6)},0" stroke="${skD}" stroke-width="2" fill="none"/>`;
      const N = [x + Math.sin(r) * (l - 10), y - Math.cos(r) * (l - 10)];
      fi += `<ellipse cx="${f1(N[0])}" cy="${f1(N[1])}" rx="${f1(w * 0.3)}" ry="${f1(w * 0.36)}" fill="${nail}" stroke="${skD}" stroke-width="1.4" transform="rotate(${a} ${f1(N[0])} ${f1(N[1])})"/>`;
      fi += `<circle cx="${f1(x)}" cy="${f1(y + 6)}" r="${f1(w * 0.22)}" fill="${skL}" opacity=".7"/>`;
    });
    fi += `<path d="M52,-60Q96,-84 118,-140Q126,-160 112,-166Q98,-168 92,-150Q76,-112 48,-100Z" fill="${sk}" ${ln(2.8)}/><ellipse cx="111" cy="-153" rx="7" ry="9" fill="${nail}" stroke="${skD}" stroke-width="1.4" transform="rotate(30 111 -153)"/>`;
    // water beads on the skin
    const beads = [[-30, 200, 5], [20, 260, 4], [-12, 320, 6], [30, -120, 4], [-30, -150, 3.5], [8, -90, 4]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" opacity=".55"/><circle cx="${x - r * 0.3}" cy="${y - r * 0.3}" r="${f1(r * 0.35)}" fill="#fff"/>`).join("");
    return `<g id="${id}-her">${g}<g id="${id}-hf">${fi}</g>${h}${beads}</g>`;
  }
  // his arm, drawn with the grip (the middle of her wrist) at (0, 0): the back of his left hand over her wrist, the fingers across it
  // toward +x curling down behind its far edge, the thumb tucked under on the near side, the wrist and forearm going up to the top left
  const TJ = { sk: "#7a4a2e", skD: "#4e2c18", skL: "#a8744e", vein: "#5e3420", scar: "#b8876a", nail: "#cdb49a" };
  function hisArm(id) {
    const { sk, skD, skL, vein, scar, nail } = TJ;
    // the forearm from his wrist (−140, −10) up and away to the corner; the rolled teal cuff; the orange vest's edge at the very end
    const W0 = [-140, -6], dir = [-0.8, -0.6], at = (d) => [W0[0] + dir[0] * d, W0[1] + dir[1] * d];
    let g = `<path d="${cap(W0, at(900), 118, 150)}" fill="${sk}" ${ln(3.2)}/>`;
    g += `<path d="M${P2(at(60))}L${P2(at(560))}" stroke="${skD}" stroke-width="24" opacity=".25" transform="translate(-22,26)" stroke-linecap="round"/>`;
    g += `<path d="M${P2([at(80)[0] + 18, at(80)[1] - 28])}L${P2([at(520)[0] + 22, at(520)[1] - 36])}" stroke="${skL}" stroke-width="12" opacity=".35" stroke-linecap="round"/>`;
    // old veins winding up the forearm, white hairs, a few age spots
    g += `<path d="M${P2(at(40))}Q${P2([at(200)[0] + 30, at(200)[1] - 10])} ${P2([at(340)[0] + 6, at(340)[1] + 18])}" stroke="${vein}" stroke-width="7" fill="none" stroke-linecap="round"/>`;
    g += `<path d="M${P2(at(40))}Q${P2([at(200)[0] + 30, at(200)[1] - 10])} ${P2([at(340)[0] + 6, at(340)[1] + 18])}" stroke="${skL}" stroke-width="2.4" fill="none" opacity=".6" transform="translate(-2,-3)"/>`;
    const r = mk(77);
    for (let k = 0; k < 26; k++) { const d = 90 + r() * 220, o = (r() - 0.5) * 90, p = at(d), q = [p[0] + dir[1] * o, p[1] - dir[0] * o]; g += `<path d="M${P2(q)}l${f1(-8 - r() * 6)},${f1(-2 - r() * 4)}" stroke="#e8e0d4" stroke-width="1.4" opacity=".5"/>`; }
    for (let k = 0; k < 7; k++) { const p = at(80 + r() * 220), o = (r() - 0.5) * 70; g += `<ellipse cx="${f1(p[0] + dir[1] * o)}" cy="${f1(p[1] - dir[0] * o)}" rx="${f1(3 + r() * 4)}" ry="${f1(2 + r() * 3)}" fill="${skD}" opacity=".45"/>`; }
    // the rolled-up teal sleeve (two folds) and the vest's orange edge beyond it
    const c0 = at(330), c1 = at(410);
    g += `<path d="${cap(c0, at(980), 176, 210)}" fill="url(#t2Teal)" ${ln(3.2)}/><path d="${cap(c0, c1, 172, 180)}" fill="#86a6a8" ${ln(3)}/>`;
    g += `<path d="M${P2([c0[0] - 70 * dir[1], c0[1] + 70 * dir[0]])}L${P2([c1[0] - 70 * dir[1], c1[1] + 70 * dir[0]])}" stroke="#56706f" stroke-width="4" opacity=".7"/>`;
    g += `<path d="M${P2([c0[0] + 60 * dir[1], c0[1] - 60 * dir[0]])}Q${P2(at(600))} ${P2([c1[0] - 50 * dir[1], c1[1] + 50 * dir[0]])}" stroke="#b8d0d0" stroke-width="5" fill="none" opacity=".5"/>`;
    g += `<path d="${cap(at(600), at(1100), 230, 260)}" fill="#e8863c" ${ln(3.2)}/><path d="M${P2(at(640))}L${P2(at(1000))}" stroke="#d8d4c8" stroke-width="22" opacity=".7" transform="translate(-60,60)"/>`;
    // the back of the hand: from the wrist to the knuckle row at x ≈ −26, the four fingers stacked top (little) to bottom (index)
    const back = `M-182,-44Q-160,-88 -72,-88Q-28,-86 -16,-70Q-8,-20 -12,60Q-20,84 -64,88Q-122,92 -170,60Q-196,10 -182,-44Z`;
    g += `<path d="${back}" fill="${sk}" ${ln(3)}/><path d="M-176,-40q10,-18 30,-14" stroke="${skL}" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/>
      <path d="M-158,-58q-4,10 4,18" stroke="${skD}" stroke-width="2.2" fill="none" opacity=".6"/>`;
    // tendons fanning to the knuckles, a raised vein, the faded rope-burn scar across the back of the hand, age spots
    g += `<path d="M-140,-20Q-80,-40 -30,-60M-140,-6Q-80,-14 -28,-22M-140,8Q-80,14 -28,16M-140,22Q-84,40 -32,54" stroke="${skL}" stroke-width="4" fill="none" opacity=".45" stroke-linecap="round"/>`;
    g += `<path d="M-150,-40Q-118,-30 -100,-46Q-80,-62 -54,-50M-150,30Q-120,40 -96,22" stroke="${vein}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M-148,-43Q-118,-34 -100,-50" stroke="${skL}" stroke-width="2" fill="none" opacity=".6"/>`;
    g += `<path d="M-148,-58Q-110,-20 -64,48L-56,40Q-100,-24 -136,-66Z" fill="${scar}" opacity=".75"/><path d="M-140,-56Q-106,-20 -66,40" stroke="#d8a888" stroke-width="2.4" fill="none" opacity=".8" stroke-dasharray="7 4 3 5"/>
      <path d="M-146,-62Q-110,-26 -60,46" stroke="${skD}" stroke-width="1.6" fill="none" opacity=".45" stroke-dasharray="3 6"/>`;
    g += [[-92, 12, 5], [-70, -30, 4], [-118, 50, 6], [-40, 20, 3.5]].map(([x, y, rr]) => `<ellipse cx="${x}" cy="${y}" rx="${rr}" ry="${f1(rr * 0.8)}" fill="${skD}" opacity=".5"/>`).join("");
    // the closed hand: the fingers across her wrist to its far edge, where the middle joints bulge and the rest curls behind it
    const FY = [[-58, 26], [-22, 31], [16, 33], [52, 32]];
    let shut = "";
    FY.forEach(([y, w], i) => {
      shut += `<path d="${cap([-30, y], [44, y + 4], w, w * 0.94)}" fill="${sk}" ${ln(2.8)}/>`;
      shut += `<path d="M${-6},${y - w * 0.32}q4,${f1(w * 0.32)} 0,${f1(w * 0.64)}M30,${y - w * 0.3}q-4,${f1(w * 0.3)} 0,${f1(w * 0.6)}" stroke="${skD}" stroke-width="2.4" fill="none"/>`;
      shut += `<path d="M52,${f1(y + 4 - w * 0.44)}A${f1(w * 0.47)},${f1(w * 0.47)} 0 0 1 52,${f1(y + 4 + w * 0.44)}" stroke="${skD}" stroke-width="6" fill="none" opacity=".55" stroke-linecap="round"/>
        <path d="M40,${f1(y - w * 0.22)}q7,3 8,12" stroke="${skL}" stroke-width="3" fill="none" opacity=".6" stroke-linecap="round"/>`;
    });
    // the knuckle row (whitening as the grip tightens: #id-hk)
    shut += `<g id="${id}-hk" opacity=".2">${FY.map(([y, w]) => `<ellipse cx="-24" cy="${y}" rx="${f1(w * 0.38)}" ry="${f1(w * 0.42)}" fill="#e8c8a8"/><ellipse cx="46" cy="${y + 4}" rx="${f1(w * 0.26)}" ry="${f1(w * 0.3)}" fill="#e8c8a8"/>`).join("")}</g>`;
    shut += FY.map(([y, w]) => `<path d="M-30,${f1(y - w * 0.36)}q-8,${f1(w * 0.36)} 0,${f1(w * 0.72)}" stroke="${skD}" stroke-width="2.4" fill="none" opacity=".8"/>`).join("");
    // the thumb, tucked round the near side of her wrist and under it
    const thumb = `<path d="M-120,64Q-96,104 -54,108Q-36,108 -40,92Q-50,78 -78,70Q-100,58 -116,46Z" fill="${sk}" ${ln(2.8)}/><path d="M-58,92q6,6 14,4" stroke="${skD}" stroke-width="2" fill="none"/><ellipse cx="-48" cy="99" rx="7" ry="5" fill="${nail}" stroke="${skD}" stroke-width="1.4"/>`;
    // the open hand on its way in: the fingers reaching out flat past where her wrist will be, the thumb spread
    let open = "";
    FY.forEach(([y, w], i) => {
      const L0 = 128 + [0, 14, 20, 10][i], sp = [-12, -4, 4, 12][i];
      open += `<path d="${cap([-30, y], [-30 + L0, y + sp], w, w * 0.84)}" fill="${sk}" ${ln(2.8)}/>`;
      open += `<path d="M${f1(-30 + L0 * 0.45)},${f1(y + sp * 0.45 - w * 0.34)}q4,${f1(w * 0.34)} 0,${f1(w * 0.68)}M${f1(-30 + L0 * 0.75)},${f1(y + sp * 0.75 - w * 0.3)}q4,${f1(w * 0.3)} 0,${f1(w * 0.6)}" stroke="${skD}" stroke-width="2.2" fill="none"/>`;
      open += `<ellipse cx="${f1(-30 + L0 - 9)}" cy="${f1(y + sp * 0.93)}" rx="${f1(w * 0.3)}" ry="${f1(w * 0.26)}" fill="${nail}" stroke="${skD}" stroke-width="1.4"/>`;
    });
    open += `<path d="M-116,48Q-80,110 -26,124Q-6,126 -10,108Q-20,96 -56,84Q-86,70 -104,40Z" fill="${sk}" ${ln(2.8)}/><ellipse cx="-18" cy="114" rx="8" ry="6" fill="${nail}" stroke="${skD}" stroke-width="1.4"/>`;
    return `<g id="${id}-his">${g}<g id="${id}-hthumb">${thumb}</g><g id="${id}-hopen" opacity="0">${open}</g><g id="${id}-hshut">${shut}</g></g>`;
  }
  // a flip-flop seen from above (toe end toward −y): the pink sole, the thong, its wet sheen; origin at the middle of the sole
  const flipflop = () => `<path d="M-38,-96Q-46,-120 -20,-128Q14,-132 30,-110Q40,-80 36,-30Q34,20 40,70Q42,112 4,118Q-34,120 -40,80Q-46,30 -40,-20Q-34,-60 -38,-96Z" fill="#c84a80" transform="translate(5,7)"/>
    <path d="M-38,-96Q-46,-120 -20,-128Q14,-132 30,-110Q40,-80 36,-30Q34,20 40,70Q42,112 4,118Q-34,120 -40,80Q-46,30 -40,-20Q-34,-60 -38,-96Z" fill="url(#t2Flop)" ${ln(3)}/>
    <path d="M-26,-90Q-30,-112 -10,-116Q12,-116 20,-100Q28,-70 24,-30Q22,20 28,64Q28,96 4,100Q-22,100 -26,70Q-30,30 -26,-20Z" fill="#f48cb8" opacity=".6"/>
    <path d="M-2,-92Q-30,-70 -40,-36M-2,-92Q26,-72 38,-36" stroke="#fff4f8" stroke-width="11" fill="none" stroke-linecap="round"/><path d="M-2,-92Q-30,-70 -40,-36M-2,-92Q26,-72 38,-36" stroke="#e85a98" stroke-width="7" fill="none" stroke-linecap="round"/>
    <circle cx="-2" cy="-93" r="6" fill="#e85a98" ${ln(2)}/><path d="M-14,40Q0,48 14,40M-16,70Q0,78 16,70" stroke="#c84a80" stroke-width="2" fill="none" opacity=".6"/>
    <path d="M-24,-10Q-26,30 -22,70" stroke="#fff" stroke-width="5" fill="none" opacity=".45" stroke-linecap="round"/>`;

  function tideGrab(L, o = {}) {
    const id = o.id || "gr", r = mk(o.seed || 21), G = o.grip || [560, 760];
    // far: past the top of the flight the steps run on into the jungle gloom (only seen if the camera pulls back)
    put(L.far, `<rect x="-600" y="-900" width="2300" height="3800" fill="#3e4a3a"/>`);
    // set: the flight, seen steeply from above, going down toward the bottom of the frame — each step a riser (its face toward us,
    // darker) under a lit nosing and a deep wet tread, smaller toward the top; tilted a little (a dutch angle)
    const Z = `translate(${G[0]},${G[1]}) scale(1.45) translate(${-G[0]},${-G[1]})`;
    let s = `<g transform="${Z}"><g transform="rotate(-5 540 960)">`;
    s += `<rect x="-500" y="-600" width="2100" height="3200" fill="#4c5440"/>`;
    const steps = [];
    let y = 2260, k = 0;
    while (y > -500 && k < 14) {
      const sc = Math.pow(0.9, k), Td = 250 * sc, Rd = 82 * sc, xl = lerp(90, 250, clamp((2260 - y) / 2600, 0, 1)), xr = lerp(960, 820, clamp((2260 - y) / 2600, 0, 1));
      steps.push({ k, yN: y, yB: y - Td, xl, xr, sc });
      y = y - Td - Rd; k++;
    }
    steps.forEach((q, i) => {
      const nx = steps[i + 1], yR = nx ? nx.yN : q.yB - 82 * q.sc;
      // the riser above this tread (the next step's face), then the tread, then the nosing's lit edge and its chipped lip
      s += `<path d="M${f1(q.xl - 40)},${f1(yR)}H${f1(q.xr + 40)}V${f1(q.yB)}H${f1(q.xl - 40)}Z" fill="url(#t2Riser)"/>`;
      for (let j = 0; j < 4; j++) { const x = q.xl + r() * (q.xr - q.xl); s += `<path d="M${f1(x)},${f1(yR + 2)}q${f1(-3 + r() * 6)},${f1((q.yB - yR) * 0.5)} ${f1(-2 + r() * 4)},${f1(q.yB - yR - 2)}" stroke="#3a3830" stroke-width="${f1(3 + r() * 6)}" opacity=".3" fill="none"/>`; }
      s += `<path d="M${f1(q.xl - 40)},${f1(q.yB)}H${f1(q.xr + 40)}V${f1(q.yN)}H${f1(q.xl - 40)}Z" fill="url(#t2Tread)"/><path d="M${f1(q.xl - 40)},${f1(q.yB)}H${f1(q.xr + 40)}V${f1(q.yN)}H${f1(q.xl - 40)}Z" fill="url(#t2Sheen)"/>`;
      // the shadow the nosing above throws on the back of the tread, the wet dark band where water pools against the riser
      s += `<rect x="${f1(q.xl - 40)}" y="${f1(q.yB)}" width="${f1(q.xr - q.xl + 80)}" height="${f1(26 * q.sc)}" fill="#3e3c34" opacity=".35"/>`;
      s += `<path d="M${f1(q.xl - 40)},${f1(q.yN - 3)}H${f1(q.xr + 40)}" stroke="#e8e4d6" stroke-width="${f1(7 * q.sc)}"/><path d="M${f1(q.xl - 40)},${f1(q.yN + 2)}H${f1(q.xr + 40)}" stroke="#4a463e" stroke-width="${f1(4 * q.sc)}" opacity=".6"/>`;
      for (let j = 0; j < 3; j++) { const x = q.xl + r() * (q.xr - q.xl), w = (12 + r() * 30) * q.sc; s += `<path d="M${f1(x)},${f1(q.yN - 4)}l${f1(w * 0.3)},${f1(5 * q.sc)}l${f1(w * 0.5)},${f1(-2 * q.sc)}l${f1(w * 0.2)},${f1(-3 * q.sc)}" fill="#6a665c" opacity=".8"/>`; }
      // puddles along the back of the tread holding the pale sky, rings from drips; grit, moss in the corners
      for (let j = 0; j < 2; j++) { const px = q.xl + 60 + r() * (q.xr - q.xl - 120), pw = (90 + r() * 160) * q.sc, ph = (16 + r() * 16) * q.sc, py = q.yB + 30 * q.sc + ph;
        s += `<path d="${blob(px, py, pw / 2, r, 9)}" fill="url(#t2Pud)" opacity=".85" transform="translate(${f1(px)},${f1(py)}) scale(1,${f1(ph / pw * 2)}) translate(${f1(-px)},${f1(-py)})"/>`;
        s += `<ellipse cx="${f1(px + pw * 0.1)}" cy="${f1(py)}" rx="${f1(pw * 0.18)}" ry="${f1(ph * 0.28)}" fill="none" stroke="#fff" stroke-width="1.6" opacity=".6"/>`; }
      for (let j = 0; j < 22; j++) { const x = q.xl + r() * (q.xr - q.xl), yy = q.yB + r() * (q.yN - q.yB); s += `<circle cx="${f1(x)}" cy="${f1(yy)}" r="${f1((1 + r() * 2.4) * q.sc)}" fill="${r() < 0.5 ? "#6e6a60" : "#d8d4c6"}" opacity=".7"/>`; }
      [q.xl, q.xr].forEach((ex, side) => { for (let j = 0; j < 5; j++) s += `<circle cx="${f1(ex + (side ? -1 : 1) * r() * 50 * q.sc)}" cy="${f1(q.yB + r() * (q.yN - q.yB))}" r="${f1((8 + r() * 16) * q.sc)}" fill="${["#3e5a2e", "#4e6e36", "#2e4626"][j % 3]}" opacity=".8"/>`; });
    });
    // the jungle spilling over the left edge, the handrail along the right: posts on base plates bolted to the treads, the top rail
    for (let j = 0; j < 26; j++) { const yy = -400 + r() * 2700, x = 40 + r() * 140, R = 50 + r() * 90; s += crown(x, yy, R, r, ["#22361e", "#33502a", "#4e6e36", "#6e8e4a"], 8); }
    for (let j = 0; j < 16; j++) { const yy = -400 + r() * 2700, x = 980 + r() * 160, R = 60 + r() * 90; s += crown(x, yy, R, r, ["#22361e", "#33502a", "#4e6e36", "#6e8e4a"], 8); }
    const posts = steps.filter((q, i) => i % 2 === 0).map((q) => { const bx = q.xr - 34 * q.sc, by = q.yB + (q.yN - q.yB) * 0.55, h = 150 * q.sc, tx = bx + 0.12 * h, ty = by - h; return { bx, by, tx, ty, sc: q.sc }; });
    s += `<path d="M${posts.map((p) => P2([p.tx + 40, p.ty + 60])).join("L")}" stroke="#14120e" stroke-width="16" opacity=".25" fill="none"/>`;
    posts.forEach((p) => {
      s += `<path d="M${f1(p.bx + 18 * p.sc)},${f1(p.by + 10 * p.sc)}l${f1(70 * p.sc)},${f1(60 * p.sc)}" stroke="#14120e" stroke-width="${f1(20 * p.sc)}" opacity=".22" stroke-linecap="round"/>`;
      s += `<path d="M${f1(p.bx - 30 * p.sc)},${f1(p.by - 12 * p.sc)}h${f1(60 * p.sc)}l${f1(10 * p.sc)},${f1(24 * p.sc)}h${f1(-80 * p.sc)}Z" fill="#8a9296" ${ln(2)}/>`;
      [[-20, 0], [20, 0], [-24, 14], [24, 14]].forEach(([dx, dy]) => { s += `<circle cx="${f1(p.bx + dx * p.sc)}" cy="${f1(p.by + dy * p.sc - 4 * p.sc)}" r="${f1(4 * p.sc)}" fill="#5a6266" stroke="#2e3236" stroke-width="1"/>`; });
      s += `<path d="${cap([p.bx, p.by], [p.tx, p.ty], 24 * p.sc, 22 * p.sc)}" fill="url(#t2Steel)" ${ln(2.4)}/><path d="M${f1(p.bx)},${f1(p.by + 2)}c${f1(-6 * p.sc)},${f1(8 * p.sc)} ${f1(10 * p.sc)},${f1(14 * p.sc)} ${f1(18 * p.sc)},${f1(10 * p.sc)}" stroke="#7a5a3a" stroke-width="${f1(5 * p.sc)}" fill="none" opacity=".6"/>`;
    });
    s += `<path d="M${posts.map((p) => P2([p.tx, p.ty])).join("L")}" stroke="${INK}" stroke-width="20" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M${posts.map((p) => P2([p.tx, p.ty])).join("L")}" stroke="url(#t2Steel)" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M${posts.map((p) => P2([p.tx - 3, p.ty - 3])).join("L")}" stroke="#fff" stroke-width="3" fill="none" opacity=".75"/>`;
    // the leaf: a fallen sea-almond leaf (ใบหูกวาง) stuck flat to the wet concrete, red with a yellow heart, beaded with water
    s += `<g transform="translate(820,1140) rotate(28) scale(1.1)"><path d="M0,-96Q58,-86 62,-20Q60,48 4,84Q-52,48 -56,-20Q-56,-84 0,-96Z" fill="#2a1408" opacity=".25" transform="translate(-8,10)"/>
      <path d="M0,-96Q58,-86 62,-20Q60,48 4,84Q-52,48 -56,-20Q-56,-84 0,-96Z" fill="url(#t2Leaf)" ${ln(2.6)}/><path d="M2,-90Q4,0 4,96" stroke="#8a2a14" stroke-width="4" fill="none"/>
      ${[-60, -30, 0, 28].map((yy) => `<path d="M3,${yy}Q30,${yy - 10} 52,${yy - 30}M3,${yy}Q-24,${yy - 10} -48,${yy - 30}" stroke="#8a2a14" stroke-width="2.4" fill="none" opacity=".8"/>`).join("")}
      <path d="M-30,-60Q-10,-40 -4,0Q-30,-10 -40,-40Z" fill="#f2c040" opacity=".45"/>${[[20, -40, 6], [-22, 10, 5], [30, 20, 4]].map(([x, yy, rr]) => `<circle cx="${x}" cy="${yy}" r="${rr}" fill="#fff" opacity=".6"/><circle cx="${x - 2}" cy="${yy - 2}" r="2" fill="#fff"/>`).join("")}</g>`;
    s += `</g></g>`;
    put(L.set, s);
    // act: the arms' shadows on the steps, the flip-flop and its trail, her arm, the squeezed skin, his arm, the marks and the drops
    let a = `<g transform="${Z}"><g id="${id}-shd" opacity=".3"><path id="${id}-shH" d="" fill="#14120e"/><path id="${id}-shJ" d="" fill="#14120e"/></g>`;
    if (o.sandal !== false) a += `<path id="${id}-skid" d="" stroke="#5a564c" stroke-width="44" fill="none" stroke-linecap="round" opacity="0"/><g id="${id}-flopS" opacity=".3"><ellipse id="${id}-flopSE" cx="0" cy="0" rx="60" ry="120" fill="url(#t2Shd)"/></g>
      <g id="${id}-flop"><g id="${id}-flopR">${flipflop()}</g></g><g id="${id}-spray">${Array.from({ length: 14 }, (_, j) => `<circle id="${id}-sp${j}" r="1" fill="#eef2ec" opacity="0"/>`).join("")}</g>`;
    a += `<g id="${id}-spd" opacity="0">${Array.from({ length: 6 }, (_, j) => `<path id="${id}-sl${j}" d="" stroke="#f4f0e2" stroke-width="${8 - j}" stroke-linecap="round" opacity=".7"/>`).join("")}</g>`;
    a += `<g id="${id}-herT">${herArm(id)}</g>`;
    a += `<g id="${id}-sq" opacity="0">${[[-48, -56], [-48, -18], [-48, 20], [-48, 54], [48, -50], [48, -12], [48, 26]].map(([x, yy]) => `<path d="M${x},${yy}q${x < 0 ? -9 : 9},8 0,16" fill="${JN.sk}" ${ln(2.4)}/>`).join("")}</g>`;
    a += `<g id="${id}-hisT">${hisArm(id)}</g>`;
    a += `<g id="${id}-hit" opacity="0">${Array.from({ length: 8 }, (_, j) => { const an = (j / 8) * Math.PI * 2 + 0.3; return `<path d="M${f1(Math.cos(an) * 150)},${f1(Math.sin(an) * 150)}L${f1(Math.cos(an) * 215)},${f1(Math.sin(an) * 215)}" stroke="#fffbea" stroke-width="9" stroke-linecap="round"/>`; }).join("")}</g>`;
    a += `<g id="${id}-drops">${Array.from({ length: 12 }, (_, j) => `<g id="${id}-dr${j}" opacity="0"><ellipse rx="7" ry="10" fill="#e8f0f0" stroke="#7a8a8a" stroke-width="1.5"/><circle cx="-2" cy="-3" r="2.4" fill="#fff"/></g>`).join("")}</g>`;
    put(L.act, a + `</g>`);
    // fg: wet fern fronds hanging into the top left corner (blur fg)
    let fg = "";
    for (let j = 0; j < 3; j++) { const bx = -80 + j * 70, by = -60 + j * 40; let fr = `M${bx},${by}`; const pts = []; for (let u = 0; u <= 1.001; u += 0.1) pts.push([bx + 360 * u + 30 * Math.sin(u * 3 + j), by + 260 * u * u + 40 * u]);
      fg += `<path d="M${pts.map(P2).join("L")}" stroke="#1e3018" stroke-width="10" fill="none"/>`;
      pts.forEach(([x, yy], i) => { if (i % 1 === 0 && i > 0) { const L0 = 70 * (1 - i / 12); fg += `<path d="M${f1(x)},${f1(yy)}q${f1(-10)},${f1(L0 * 0.6)} ${f1(-L0 * 0.4)},${f1(L0)}M${f1(x)},${f1(yy)}q${f1(L0 * 0.5)},${f1(L0 * 0.2)} ${f1(L0 * 0.7)},${f1(L0 * 0.8)}" stroke="#2a4422" stroke-width="${f1(14 * (1 - i / 14))}" fill="none" stroke-linecap="round"/>`; } }); }
    put(L.fg, fg);
    ST[id] = { kind: "grab", G, sandal: o.sandal !== false, flop0: [292, 1000], flop1: [322, 1092], drop: [350, 1222] };
    grabDraw(id, 0, { at: 0.5, hold: true });
  }

  // the arms' silhouettes (for the shadows): her forearm and hand as capsules, his forearm and hand
  const herSil = (W, ph) => { const R = (p) => { const c = Math.cos(ph), s = Math.sin(ph); return [W[0] + p[0] * c - p[1] * s, W[1] + p[0] * s + p[1] * c]; };
    return `${cap(R([0, 0]), R([10, 900]), 92, 220)}${cap(R([0, -20]), R([4, -190]), 110, 120)}${cap(R([4, -190]), R([0, -320]), 100, 40)}`; };
  const hisSil = (H, ps, closed) => { const R = (p) => { const c = Math.cos(ps), s = Math.sin(ps); return [H[0] + p[0] * c - p[1] * s, H[1] + p[0] * s + p[1] * c]; };
    return `${cap(R([-140, -6]), R([-140 - 0.8 * 1100, -6 - 0.6 * 1100]), 118, 200)}${cap(R([-150, 0]), R([closed ? 50 : 100, 0]), 160, 120)}`; };

  function grabDraw(id, t, o) {
    const S = ST[id], at = o.at ?? 0.5, u = t - at, G = S.G;
    // her wrist: carried down toward the bottom of the frame by her lunge (accelerating), then — once he has it — the momentum takes both on
    // a little, he hauls it back up and holds, both trembling with the strain
    const e = clamp((t - (at - 0.6)) / 0.6, 0, 1), pre = 1 - e * e;
    let wx = G[0] - 34 * pre, wy = G[1] - 230 * pre, ph = (-6 + 10 * (1 - pre)) * Math.PI / 180;
    const held = o.hold !== false;
    if (u > 0) {
      if (held) {
        const over = Math.sin(clamp(u / 0.1, 0, 1) * Math.PI / 2) * Math.exp(-Math.max(0, u - 0.1) / 0.13), back = sm(0.1, 0.45, u);
        const tr = sm(0.2, 0.5, u) * (2.2 * Math.sin(t * 41) + 1.4 * Math.sin(t * 29 + 1));
        wx = G[0] + 10 * over - 6 * back + tr; wy = G[1] + 44 * over - 22 * back + tr * 0.6;
        ph = (4 + 16 * Math.sin(clamp(u / 0.16, 0, 1) * Math.PI) * Math.exp(-u / 0.25) - 4 * back) * Math.PI / 180;
      } else { wx = G[0] + 30 * u; wy = G[1] + 600 * u; }
    }
    el(`${id}-herT`).setAttribute("transform", `translate(${f1(wx)},${f1(wy)}) rotate(${f1((ph * 180) / Math.PI)})`);
    // her fingers: straining open and shaking; at the clamp they splay wide, then claw at the air
    const spread = 1 + (held && u > 0 ? 0.16 * Math.sin(clamp(u / 0.14, 0, 1) * Math.PI) - 0.08 * sm(0.15, 0.5, u) : 0), sh = 1.5 * Math.sin(t * 37);
    el(`${id}-hf`).setAttribute("transform", `translate(0,-180) scale(${f1(spread)},${f1(1 - (spread - 1) * 0.4)}) rotate(${f1(sh)}) translate(0,180)`);
    // his hand: off frame until 0.16 s before the clamp, then in along his arm, fastest at the end; squash on contact; then it rides with her
    // wrist; the closed hand replaces the open one over two frames; the knuckles pale as the grip tightens
    const k = clamp((t - (at - 0.22)) / 0.22, 0, 1), inK = 1 - k * k * k, ps = (8 * Math.PI) / 180;
    const hx = (u > 0 ? wx : G[0]) - 430 * inK, hy = (u > 0 ? wy : G[1]) - 330 * inK;
    const sq = u > 0 ? Math.sin(clamp(u / 0.12, 0, 1) * Math.PI) * Math.exp(-u / 0.2) : 0;
    const show = held && k > 0;
    el(`${id}-hisT`).setAttribute("transform", `translate(${f1(hx)},${f1(hy)}) rotate(${f1((ps * 180) / Math.PI)}) scale(${f1(1 + 0.12 * sq)},${f1(1 - 0.1 * sq)})`);
    el(`${id}-hisT`).setAttribute("opacity", show ? "1" : "0");
    const c = sm(-0.03, 0.03, u);
    el(`${id}-hopen`).setAttribute("opacity", f1(1 - c));
    el(`${id}-hshut`).setAttribute("opacity", f1(c));
    el(`${id}-hthumb`).setAttribute("opacity", f1(c));
    el(`${id}-hk`).setAttribute("opacity", f1(0.15 + 0.6 * sm(0.1, 0.8, u)));
    el(`${id}-sq`).setAttribute("opacity", held ? f1(sm(0.02, 0.2, u)) : "0");
    el(`${id}-sq`).setAttribute("transform", `translate(${f1(wx)},${f1(wy)}) rotate(${f1((ph * 180) / Math.PI)})`);
    // the shadows on the steps (the light is up to the right): long and soft, offset down to the left
    el(`${id}-shH`).setAttribute("d", show ? hisSil([hx - 70, hy + 64], ps, c > 0.5) : "");
    el(`${id}-shJ`).setAttribute("d", herSil([wx - 70, wy + 64], ph));
    // speed lines behind his hand while it shoots in; the impact marks at the clamp
    const sp = held ? sm(-0.2, -0.12, u) * (1 - sm(0.0, 0.08, u)) : 0;
    el(`${id}-spd`).setAttribute("opacity", f1(sp));
    for (let j = 0; j < 6; j++) { const off = (j - 2.5) * 36, len = 220 + 60 * Math.sin(j * 2.1); const x0 = hx - 160 + off * 0.6, y0 = hy - 20 - off * 0.8;
      el(`${id}-sl${j}`).setAttribute("d", `M${f1(x0 - 0.8 * len)},${f1(y0 - 0.6 * len)}L${f1(x0)},${f1(y0)}`); }
    const hit = held && u > 0 ? Math.exp(-u / 0.12) : 0;
    el(`${id}-hit`).setAttribute("opacity", f1(hit));
    el(`${id}-hit`).setAttribute("transform", `translate(${f1(wx)},${f1(wy)}) scale(${f1(0.8 + 0.6 * (1 - hit))})`);
    // water flung off her fingertips by the jerk
    for (let j = 0; j < 12; j++) {
      const d = el(`${id}-dr${j}`), u2 = u - 0.03 * (j % 3);
      if (!held || u2 < 0 || u2 > 0.7) { d.setAttribute("opacity", "0"); continue; }
      const an = (-60 - 70 * ((j * 0.37) % 1) + (j % 2 ? 20 : -10)) * Math.PI / 180, v = 900 + 500 * ((j * 0.61) % 1), x = wx + 30 * Math.cos(an) * 6 + Math.cos(an) * v * u2, yy = wy - 230 + Math.sin(an) * v * u2 + 1600 * u2 * u2;
      d.setAttribute("opacity", f1(1 - u2 / 0.7));
      d.setAttribute("transform", `translate(${f1(x)},${f1(yy)}) rotate(${f1((an * 180) / Math.PI + 90)}) scale(${f1(0.6 + 0.5 * ((j * 0.43) % 1))})`);
    }
    // the flip-flop: skids down the wet tread from o.at + 0.04, tips over the step's edge and drops to the tread below, settles
    if (S.sandal) {
      const u3 = u - 0.04, A0 = S.flop0, A1 = S.flop1, B = S.drop;
      let fx = A0[0], fy = A0[1], rot = -52, tip = 0, lift = 0;
      if (u3 > 0) {
        const sk = 1 - Math.pow(1 - clamp(u3 / 0.42, 0, 1), 2);
        fx = lerp(A0[0], A1[0], sk); fy = lerp(A0[1], A1[1], sk); rot = -52 + 22 * sk;
        if (u3 > 0.32) { const d = clamp((u3 - 0.32) / 0.3, 0, 1), dd = d * d; fx = lerp(A1[0], B[0], d); fy = lerp(A1[1], B[1], dd); tip = 70 * Math.sin(Math.min(1, d * 1.4) * Math.PI) * (1 - d * 0.5); lift = 30 * Math.sin(d * Math.PI); }
        if (u3 > 0.62) { const b = u3 - 0.62; fy = B[1] - 14 * Math.abs(Math.sin(b * 18)) * Math.exp(-b * 9); rot = -24 + 3 * Math.exp(-b * 6) * Math.sin(b * 20); tip = 0; }
      }
      el(`${id}-flop`).setAttribute("transform", `translate(${f1(fx)},${f1(fy - lift)}) rotate(${f1(rot)}) scale(.78)`);
      el(`${id}-flopR`).setAttribute("transform", `scale(1,${f1(Math.cos((tip * Math.PI) / 180))})`);
      el(`${id}-flopS`).setAttribute("transform", `translate(${f1(fx - 12 + lift * 0.6)},${f1(fy + 18)}) rotate(${f1(rot)}) scale(.78)`);
      const tr0 = u3 > 0 ? clamp(u3 / 0.3, 0, 1) : 0;
      el(`${id}-skid`).setAttribute("d", tr0 > 0 ? `M${P2(A0)}L${P2([lerp(A0[0], fx, 1), Math.min(fy, A1[1])])}` : "");
      el(`${id}-skid`).setAttribute("opacity", f1(0.32 * tr0 * (1 - sm(0.8, 1.6, u3))));
      for (let j = 0; j < 14; j++) {
        const c2 = el(`${id}-sp${j}`), u4 = u3 - 0.02 * (j % 5);
        if (u4 < 0 || u4 > 0.45) { c2.setAttribute("opacity", "0"); continue; }
        const an = ((j % 2 ? 30 : 150) + 40 * ((j * 0.37) % 1)) * Math.PI / 180, v = 300 + 300 * ((j * 0.53) % 1), base = [fx, fy + 100];
        c2.setAttribute("cx", f1(base[0] + Math.cos(an) * v * u4)); c2.setAttribute("cy", f1(base[1] - Math.abs(Math.sin(an)) * v * u4 * 0.6 + 900 * u4 * u4));
        c2.setAttribute("r", f1(3 + 4 * ((j * 0.71) % 1))); c2.setAttribute("opacity", f1(0.85 * (1 - u4 / 0.45)));
      }
    }
  }
  Tide.grab = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, oo = { at: o.at ?? 0.5, hold: o.hold !== false };
    grabDraw(id, 0, oo);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => grabDraw(id, c.t, oo) }, t0);
  };


  // =====================================================================================================================================
  // the raft
  // =====================================================================================================================================
  // palettes (the same values as tide.js) and a sky like tide.js's
  const PAL = {
    eerie: { sky: ["#6a8697", "#9cb0b4", "#cfd2c0", "#f0e2bc"], cloud: "tdCloudE", cl: ["#f4f0e2", "#9a9c94"], sun: 0.35, haze: "#e9dfc2",
      green: ["#365c3a", "#557a4a", "#86a266"], leaf: ["#34583a", "#567c48", "#94b070"], sand: ["#f0e4ca", "#e0cea8", "#ceb890"], bed: ["#a2916e", "#887b5e", "#6e664f"],
      sea: ["#c4cfc4", "#88a6a6", "#4b7b8c", "#4e8a90", "#7cb2aa", "#a8d0c2"], rock: "#bab09f" },
    squall: { sky: ["#3c4854", "#62707a", "#949ea2", "#b6bab2"], cloud: "tdCloudS", cl: ["#a8b0ae", "#3a444a"], sun: 0, haze: "#9aa09a",
      green: ["#22382a", "#344e34", "#4e6846"], leaf: ["#26402a", "#3a5c38", "#6a8a56"], sand: ["#d6caae", "#c4b696", "#ae9e7e"], bed: ["#867658", "#6e624a", "#5a523e"],
      sea: ["#8a968e", "#53666a", "#344f5a", "#3c5a60", "#5a7a76", "#7a968c"], rock: "#8a8074" },
  };
  function sky(L, id, P, hz, seed) {
    const r = mk(seed);
    let g = `<defs><linearGradient id="${id}-skyG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(hz - 1900)}" x2="0" y2="${f1(hz + 30)}"><stop offset="0" stop-color="${P.sky[0]}"/><stop offset=".5" stop-color="${P.sky[1]}"/><stop offset=".84" stop-color="${P.sky[2]}"/><stop offset="1" stop-color="${P.sky[3]}"/></linearGradient></defs>`;
    g += `<rect x="-3000" y="${f1(hz - 4200)}" width="8000" height="6400" fill="url(#${id}-skyG)"/>`;
    if (P.sun) g += `<circle cx="1480" cy="${f1(hz - 1350)}" r="820" fill="url(#qkSun)" opacity="${P.sun}"/>`;
    for (let k = 0; k < 6; k++) g += Pop2.cloud2(-760 + k * 640 + r() * 220, hz - 820 - r() * 700, 300 + r() * 320, 96 + r() * 60, r, P.cloud, P.cl[0], P.cl[1]);
    if (!P.sun) for (let k = 0; k < 6; k++) g += Pop2.cloud2(-900 + k * 560 + r() * 200, hz - 1300 + r() * 900, 900 + r() * 500, 300 + r() * 160, r, P.cloud, "#7a8482", "#1e262c");
    put(L.sky, g);
  }
  // the hotel's front (โรงแรมแหลมหอย, the same design as tide.js): origin the ground under the middle, W 560, a storey FH 104, the outside
  // stair tower on the right, the flat roof with its railing, tank and sign
  function hotelArt(id) {
    const W = 560, FH = 104, NF = 5, top = -NF * FH, SW = 112, X0 = -W / 2, X1 = W / 2 - SW, O2 = `stroke="${INK}" stroke-width="2" stroke-linejoin="round"`, O3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
    let g = `<path d="M${X0},${top - 30}L${X0 - 70},${top - 4}V-6L${X0},0Z" fill="#cbbfa8" ${O3}/>`;
    for (let n = 1; n < NF; n++) g += `<path d="M${X0},${-n * FH}L${X0 - 70},${-n * FH + 22}" stroke="#a89c86" stroke-width="5"/>`;
    for (let n = 1; n <= NF; n++) {
      const y0 = -n * FH, y1 = y0 + FH, bw = (X1 - X0) / 4;
      let f = `<rect x="${X0}" y="${y0}" width="${X1 - X0}" height="${FH}" fill="#f4f0e6"/>`;
      if (n === 1) {
        f += `<rect x="${X0 + 20}" y="${y0 + 22}" width="${X1 - X0 - 40}" height="${FH - 22}" fill="#9ccbd8" ${O2}/>`;
        for (let k = 1; k < 6; k++) f += `<path d="M${X0 + 20 + (k * (X1 - X0 - 40)) / 6},${y0 + 22}V${y1}" stroke="#5a7a86" stroke-width="3"/>`;
        f += `<path d="M${X0 + 120},${y0 + 14}H${X0 + 330}L${X0 + 344},${y0 + 34}H${X0 + 106}Z" fill="#8a6a4a" ${O2}/>`;
      } else for (let k = 0; k < 4; k++) {
        const bx = X0 + k * bw;
        f += `<rect x="${bx + 8}" y="${y0 + 10}" width="${bw - 16}" height="${FH - 14}" fill="#c6c0b2"/><rect x="${bx + 18}" y="${y0 + 18}" width="${bw - 36}" height="${FH - 24}" fill="#7fb2c4" ${O2}/><path d="M${bx + bw / 2},${y0 + 18}V${y1 - 6}" stroke="#4a6a78" stroke-width="3"/>`;
        f += `<path d="M${bx + 22},${y0 + 20}H${bx + 44}V${y1 - 8}H${bx + 22}Z" fill="${["#f2e6c8", "#e8d0c0", "#d8e4e8", "#f0e0b8"][(k + n) % 4]}" opacity=".9"/>`;
        f += `<rect x="${bx + 6}" y="${y1 - 40}" width="${bw - 12}" height="38" fill="#bfe4ea" opacity=".45"/><path d="M${bx + 6},${y1 - 40}H${bx + bw - 6}" stroke="#d8dcdc" stroke-width="5"/>`;
        if ((k + n) % 3 === 0) f += `<rect x="${bx + bw - 60}" y="${y1 - 32}" width="36" height="26" fill="#d8dcdc" ${O2}/><circle cx="${bx + bw - 42}" cy="${y1 - 19}" r="8" fill="#9aa0a2"/>`;
        if ((k * 3 + n) % 5 === 1) f += `<path d="M${bx + 30},${y1 - 42}h28v24h-28z" fill="${["#e84a3a", "#2a8ad0", "#f2c030"][(k + n) % 3]}" ${O2}/>`;
      }
      f += `<rect x="${X0 - 6}" y="${y1 - 7}" width="${X1 - X0 + 12}" height="10" fill="#e4dccc" ${O2}/>`;
      g += `<g id="${id}-f${n}">${f}</g>`;
    }
    let st = `<rect x="${X1}" y="${top - 40}" width="${SW}" height="${-top + 40}" fill="#ebe4d6" ${O3}/>`;
    for (let n = 1; n <= NF; n++) { const y0 = -n * FH; st += `<rect x="${X1 + 22}" y="${y0 + 14}" width="${SW - 44}" height="${FH - 24}" fill="#4e6a74" ${O2}/><path d="M${X1 + 26},${y0 + FH - 14}L${X1 + SW - 26},${y0 + 22}" stroke="#d8d0c0" stroke-width="9"/><path d="M${X1 + 26},${y0 + FH - 34}L${X1 + SW - 26},${y0 + 4}" stroke="#f4f0e6" stroke-width="2.5"/>`; }
    st += `<rect x="${X1 + 30}" y="${top - 30}" width="${SW - 60}" height="18" fill="#2e8a4a" ${O2}/>`;
    g += `<g id="${id}-stair">${st}</g>`;
    let rf = `<rect x="${X0 - 8}" y="${top - 10}" width="${X1 - X0 + 16}" height="14" fill="#e4dccc" ${O2}/><rect x="${X0}" y="${top - 34}" width="${X1 - X0}" height="24" fill="#f2ede2" ${O2}/>`;
    rf += `<path d="M${X0},${top - 78}H${X1}" stroke="#c8ccce" stroke-width="7"/>`;
    for (let k = 0; k <= 12; k++) rf += `<path d="M${X0 + (k * (X1 - X0)) / 12},${top - 34}V${top - 78}" stroke="#a8aeb0" stroke-width="4"/>`;
    rf += `<g transform="translate(${X0 + 90},${top - 34})"><rect x="-34" y="-82" width="68" height="70" rx="8" fill="#5a8ad0" ${O2}/><path d="M-26,-12V0M26,-12V0" stroke="#8a9296" stroke-width="6"/></g>`;
    rf += `<g id="${id}-hsign"><rect x="${X0 + 170}" y="${top - 112}" width="290" height="58" rx="6" fill="#1e3a5a" ${O2}/><text x="${X0 + 315}" y="${top - 74}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#f4e6b8">โรงแรมแหลมหอย</text><path d="M${X0 + 200},${top - 54}V${top - 34}M${X0 + 430},${top - 54}V${top - 34}" stroke="#5a6266" stroke-width="5"/></g>`;
    g += `<g id="${id}-roof">${rf}</g>`;
    return g;
  }
  Tide.hotelArt = hotelArt;

  // debris riding the flood (drawn about 1 m long at scale 1, centred, the waterline at y 0: the part below is drawn darker, as seen through
  // muddy water): a plank, a red plastic chair on its side, a palm frond, a lost flip-flop, a foam box, a bottle, a coconut, a basket
  const DEB = [
    `<path d="M-60,-6L58,-10L62,4L-58,8Z" fill="#a8845a" ${ln(2.4)}/><path d="M-50,-2H50" stroke="#7a5a3a" stroke-width="2"/><circle cx="-44" cy="0" r="2.4" fill="#5a5a5a"/><circle cx="46" cy="-3" r="2.4" fill="#5a5a5a"/>`,
    `<g transform="rotate(-30)"><path d="M-34,-40H30V-4H-34Z" fill="#d8402e" ${ln(2.6)}/><path d="M-30,-36H26M-30,-24H26M-30,-12H26" stroke="#a82a1e" stroke-width="3"/><path d="M-34,-4L-40,30M30,-4L36,30" stroke="#c8382a" stroke-width="7" stroke-linecap="round"/><path d="M-38,-6H34V6H-38Z" fill="#e8503a" ${ln(2.4)}/></g>`,
    `<path d="M-70,0Q0,-14 70,-4" stroke="#6a7a3a" stroke-width="5" fill="none"/>${Array.from({ length: 12 }, (_, k) => `<path d="M${-62 + k * 11},${-4 - k * 0.6}l${-6 + (k % 2) * 12},${k % 2 ? 22 : -22}" stroke="${k % 3 ? "#5e8a3a" : "#7a9a4a"}" stroke-width="5" stroke-linecap="round"/>`).join("")}`,
    `<path d="M-30,-8Q-32,-20 -14,-20Q30,-22 34,-6Q36,8 14,10Q-26,12 -30,-8Z" fill="#2a8ad0" ${ln(2.4)}/><path d="M18,-14Q4,-4 -10,-16M18,-14Q8,0 -6,6" stroke="#ffd43a" stroke-width="4" fill="none"/>`,
    `<path d="M-40,-24H40V10H-40Z" fill="#f4f4ee" ${ln(2.4)}/><path d="M-40,-24L-30,-34H48L40,-24Z" fill="#e2e4dc" ${ln(2)}/><path d="M40,-24L48,-34V2L40,10Z" fill="#d0d2ca" ${ln(2)}/>`,
    `<g transform="rotate(-70)"><path d="M-10,-30Q-12,-40 -6,-44V-50H6V-44Q12,-40 10,-30V24Q10,30 0,30Q-10,30 -10,24Z" fill="#cfe8f0" fill-opacity=".85" ${ln(2)}/><rect x="-6" y="-56" width="12" height="7" fill="#2a8ad0"/><rect x="-10" y="-6" width="20" height="16" fill="#e84a3a"/></g>`,
    `<circle r="22" fill="#7a5a34" ${ln(2.4)}/><path d="M-12,-12Q0,-20 12,-10" stroke="#a88a5a" stroke-width="4" fill="none"/><circle cx="-6" cy="-4" r="3" fill="#3a2a1a"/><circle cx="4" cy="-6" r="3" fill="#3a2a1a"/>`,
    `<path d="M-36,-14Q0,-24 36,-14L30,12Q0,18 -30,12Z" fill="#c8a060" ${ln(2.4)}/><path d="M-32,-6Q0,-14 32,-6M-30,4Q0,-4 30,4" stroke="#8a6a3a" stroke-width="2.4" fill="none"/>${Array.from({ length: 8 }, (_, k) => `<path d="M${-28 + k * 8},-18V12" stroke="#8a6a3a" stroke-width="1.6"/>`).join("")}`,
  ];
  // how long each piece is in metres, and in its drawing's units
  const DEBM = [1.2, 0.6, 1.6, 0.26, 0.6, 0.3, 0.25, 0.5], DEBU = [124, 76, 140, 64, 88, 86, 44, 72];
  // the white ice cooler (from ยาย's shop: "น้ำแข็ง" in blue on its side) in the clinging tourist's own units: the lid's top at y −425, the
  // box down to −270, 300 wide; it goes inside the rig between his torso and his arms (Tide.raft puts it there)
  const coolerArt = () => `<g>
    <path d="M-150,-420H150L146,-266Q0,-256 -146,-266Z" fill="#f2f4f0" ${ln(3)}/><path d="M-150,-420H150L146,-266Q0,-256 -146,-266Z" fill="url(#r2Cyl)"/>
    <path d="M-140,-400H140M-142,-300Q0,-292 142,-300" stroke="#c8ccc8" stroke-width="3" fill="none"/>
    <rect x="-124" y="-408" width="248" height="36" rx="6" fill="#2a8ad0" ${ln(2)}/><text x="0" y="-380" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="28" fill="#ffffff">น้ำแข็ง</text>
    <text x="0" y="-322" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="40" fill="#2a6ab8" opacity=".8">ร้านยายพร</text>
    <path d="M-150,-386h-14v40h14M150,-386h14v40h-14" fill="#dfe4e2" ${ln(2.4)}/><circle cx="118" cy="-290" r="7" fill="#9aa4a8" ${ln(1.6)}/>
    <path d="M-120,-356l18,8M96,-372l14,-6M-60,-300l24,-4" stroke="#a8a49a" stroke-width="2.2" opacity=".7"/>
    <path d="M-158,-424Q0,-446 158,-424L156,-412Q0,-428 -156,-412Z" fill="#e4e8e4" ${ln(2.8)}/><path d="M-158,-424Q0,-446 158,-424" stroke="#ffffff" stroke-width="3" fill="none" opacity=".8"/>
    <path d="M-150,-420Q-40,-432 40,-430" stroke="#fff" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/></g>`;

  function tideRaft(L, o = {}) {
    const id = o.id || "rf", P = PAL[o.time || "squall"], r = mk(o.seed || 31), HZ = o.hz ?? 980, F = 1100, HC = 0.7, dT = o.dist ?? 1.7;
    const yAt = (d) => HZ + (F * HC) / d, yT = yAt(dT);
    sky(L, id, P, HZ, (o.seed || 31) + 1);
    // far: the jungle hill behind the village, the warning tower on its shoulder (its beacon blinks), the flood out to the foot of the hill
    let f = `<path d="M-800,${HZ + 4}L-800,560Q-300,380 200,420Q600,300 980,380Q1400,460 1900,600V${HZ + 4}Z" fill="${P.green[0]}"/>`;
    for (let k = 0; k < 50; k++) { const x = -700 + r() * 2500, y = 460 + r() * (HZ - 520); f += crown(x, y, 50 + r() * 50, r, [T(P.green[0], -0.1), P.green[1], P.green[2], T(P.green[2], 0.2)], 7); }
    f += `<rect x="-800" y="360" width="2700" height="${HZ - 356}" fill="${P.haze}" opacity=".35"/>` + Tide.tower(-120, HZ - 60, 0.34, id);
    // roofs of the village just showing above the flood, far away
    for (let k = 0; k < 9; k++) { const x = -600 + k * 300 + r() * 120, w = 70 + r() * 60; f += `<path d="M${f1(x - w / 2)},${HZ + 2}L${f1(x - w / 2 + 12)},${HZ - 22}H${f1(x + w / 2 - 12)}L${f1(x + w / 2)},${HZ + 2}Z" fill="${r() < 0.5 ? "#8a9294" : "#9a5a3a"}" opacity=".8"/>`; }
    put(L.far, f);
    // mid: the hotel standing in the flood (its foot under ~o.level storeys of water), palms standing in the water, the far water to the hotel
    const dH = o.hotelDist ?? 25, sH = (F / dH) * 3 / 104, gH = HZ + (F * (HC + 3 * (o.level ?? 1.3))) / dH;
    let m = `<g id="${id}-hot" data-d="${dH}"><g transform="translate(${o.hotelX ?? 300},${f1(gH)}) scale(${f1(sH)})">${hotelArt(id + "h")}</g></g>`;
    const PALMS = (o.palms || [[930, 16, 0.08], [60, 21, -0.06]]).map(([x, d, lean], k) => ({ x, d, lean, k }));
    PALMS.forEach((p) => { const s0 = (F / p.d) * 7 / 900; m += `<g id="${id}-pm${p.k}" data-d="${p.d}"><g transform="translate(${p.x},${f1(yAt(p.d) + 4)})">${Tide.coco(0, 0, s0, p.lean, 70 + p.k, { pal: P.leaf, q: 0.6 })}<path d="M${f1(-60 * s0)},2Q0,-8 ${f1(60 * s0)},2" stroke="#e8e6da" stroke-width="${f1(Math.max(2, 10 * s0))}" fill="none" opacity=".7" stroke-linecap="round"/></g></g>`; });
    // the far water: muddy, the sky's grey in it, bands of foam and flow lines (each depth band slides with the current: #id-wb0 …)
    const WG = `<defs><linearGradient id="${id}-wG" gradientUnits="userSpaceOnUse" x1="0" y1="${HZ}" x2="0" y2="1920"><stop offset="0" stop-color="#8a9088"/><stop offset=".08" stop-color="#727260"/><stop offset=".3" stop-color="#666048"/><stop offset=".6" stop-color="#5a5036"/><stop offset="1" stop-color="#4c4028"/></linearGradient></defs>`;
    const bands = [];
    const D = [60, 30, 16, 9, 5.5, 3.6, 2.4, dT, 1.35, 1.1, 0.9, 0.75];
    for (let i = 0; i + 1 < D.length; i++) bands.push({ i, d0: D[i], d1: D[i + 1], y0: yAt(D[i]), y1: yAt(D[i + 1]), d: Math.sqrt(D[i] * D[i + 1]) });
    const bandArt = (b) => {
      const pxm = F / b.d, h = b.y1 - b.y0, n = Math.round(clamp(6 + 260 / b.d, 6, 44)); let g = "";
      for (let k = 0; k < n; k++) { const x = r() * 1200, y = b.y0 + r() * h, w = Math.min(420, (0.3 + r() * 1.2) * pxm); g += `<path d="M${f1(x)},${f1(y)}q${f1(w / 2)},${f1(-Math.min(6, 0.02 * pxm) * (0.5 + r()))} ${f1(w)},0" stroke="#d8d6c4" stroke-width="${f1(clamp(0.01 * pxm, 1, 4))}" fill="none" opacity="${f1(0.12 + r() * 0.2)}" stroke-linecap="round"/>`; }
      for (let k = 0; k < Math.round(n / 3); k++) { const x = r() * 1200, y = b.y0 + r() * h, w = Math.min(560, (1 + r() * 3) * pxm); g += `<path d="M${f1(x)},${f1(y)}h${f1(w)}" stroke="#ece8d8" stroke-width="${f1(clamp(0.008 * pxm, 1, 3.2))}" opacity="${f1(0.2 + r() * 0.25)}" stroke-linecap="round" stroke-dasharray="${f1(Math.min(60, 0.2 * pxm))} ${f1(Math.min(24, 0.08 * pxm))}"/>`; }
      for (let k = 0; k < Math.round(n / 7); k++) { const x = r() * 1200, y = b.y0 + r() * h, R = Math.min(0.5 * h + 6, (0.06 + r() * 0.12) * pxm); g += `<path d="${blob(x, y, R, r, 7)}" fill="#efeee2" opacity="${f1(0.22 + r() * 0.22)}" transform="translate(${f1(x)},${f1(y)}) scale(2.2,.2) translate(${f1(-x)},${f1(-y)})"/>`; }
      for (let k = 0; k < Math.round(n / 2); k++) { const x = r() * 1200, y = b.y0 + r() * h, w = Math.min(150, (0.12 + r() * 0.24) * pxm), a = Math.min(10, 0.03 * pxm); g += `<path d="M${f1(x)},${f1(y)}q${f1(w / 2)},${f1(-a)} ${f1(w)},0" stroke="#2e2818" stroke-width="${f1(clamp(0.008 * pxm, 1, 3))}" fill="none" opacity=".22" transform="translate(0,${f1(a * 0.5)})"/><path d="M${f1(x)},${f1(y)}q${f1(w / 2)},${f1(-a)} ${f1(w)},0" stroke="#c8c6b2" stroke-width="${f1(clamp(0.008 * pxm, 1, 3))}" fill="none" opacity=".3"/>`; }
      for (let k = 0; k < Math.round(n / 10); k++) { const x = r() * 1200, y = b.y0 + r() * h, R = Math.min(1.2 * h, (0.25 + r() * 0.35) * pxm); g += `<path d="M${f1(x - R)},${f1(y)}A${f1(R)},${f1(R * 0.26)} 0 0 1 ${f1(x + R * 0.8)},${f1(y - R * 0.1)}" stroke="#3e3420" stroke-width="${f1(clamp(0.01 * pxm, 1, 4))}" fill="none" opacity=".25"/>`; }
      return `<g id="${id}-wb${b.i}" data-d="${f1(b.d)}"><g id="${id}-wt${b.i}">${g}</g><use href="#${id}-wt${b.i}" x="-1200"/><use href="#${id}-wt${b.i}" x="1200"/></g>`;
    };
    m += WG + `<path d="M-1200,${HZ}H2400V1960H-1200Z" fill="url(#${id}-wG)"/>`;
    bands.filter((b) => b.d0 > 5.5).forEach((b) => { m += bandArt(b); });
    // the water piling against the hotel's front and the palms
    m += `<path d="M${f1((o.hotelX ?? 300) - 300 * sH)},${f1(yAt(dH))}H${f1((o.hotelX ?? 300) + 240 * sH)}" stroke="#ecead8" stroke-width="5" opacity=".6" stroke-dasharray="20 8 6 8"/>`;
    put(L.mid, m);
    // set: the flow over the water between the far bands and the tourist (the water itself is the mid layer's, which runs to the bottom)
    let sw = "";
    bands.filter((b) => b.d0 <= 5.5 && b.d1 >= dT - 1e-6).forEach((b) => { sw += bandArt(b); });
    // debris riding the current behind the tourist (#id-db0 …)
    const DB = (o.debris || [[0, 9, 140], [2, 5, 840], [1, 7, 620], [6, 4.4, 980], [3, 2.6, 300], [5, 3.0, 760], [7, 6.5, -100], [4, 14, 1010], [3, 1.45, 900], [6, 1.3, -80]]).map(([kind, d, x], k) => ({ kind, d, x, k, ph: r() * 6, rot: (r() - 0.5) * 40 }));
    const dbArt = (q) => { const s0 = (DEBM[q.kind] * F) / q.d / DEBU[q.kind]; return `<g id="${id}-db${q.k}"><g transform="scale(${f1(s0)})">${DEB[q.kind]}<path d="M-70,8Q0,20 70,8" stroke="#efeee2" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/></g></g>`; };
    DB.filter((q) => q.d > dT).forEach((q) => { sw += dbArt(q); });
    put(L.set, sw);
    // in front of the tourist: the water nearer than him (its top edge is his waterline), its bands, the foam ring round him, the rings
    // spreading from his bobbing, debris nearer than him
    let fw = `<path id="${id}-wl" d="" fill="url(#${id}-wG)"/>`;
    fw += `<g id="${id}-near">${bands.filter((b) => b.d0 <= dT + 1e-6).map(bandArt).join("")}</g>`;
    fw += `<g id="${id}-rings">${[0, 1, 2].map((k) => `<ellipse id="${id}-rg${k}" rx="1" ry="1" fill="none" stroke="#e8e6d8" stroke-width="3" opacity="0"/>`).join("")}</g>`;
    fw += `<g id="${id}-foam"><path id="${id}-fo1" d="" fill="#efeee4" opacity=".9"/><path id="${id}-fo2" d="" fill="none" stroke="#ffffff" stroke-width="4" opacity=".8" stroke-linecap="round"/>${Array.from({ length: 16 }, (_, k) => `<circle id="${id}-fb${k}" r="3" fill="#ffffff" opacity=".8"/>`).join("")}</g>`;
    DB.filter((q) => q.d <= dT).forEach((q) => { fw += dbArt(q); });
    front(L, `${id}-front`, fw);
    // fg: the rain in the squall (streaks)
    if (o.rain !== false) { let rn = ""; for (let k = 0; k < 90; k++) { const x = -300 + r() * 1700, y = -200 + r() * 2300, l = 40 + r() * 80; rn += `<path d="M${f1(x)},${f1(y)}l${f1(-l * 0.18)},${f1(l)}" stroke="#d8dee0" stroke-width="${f1(1.5 + r() * 1.5)}" opacity="${f1(0.15 + r() * 0.2)}"/>`; } put(L.fg, `<g id="${id}-rain">${rn}</g>`); }
    ST[id] = { kind: "raft", HZ, F, HC, dT, yT, yAt, bands, DB, PALMS, dH, rain: o.rain !== false };
    raftDraw(id, 0, { speed: 1.2, follow: 0.9, dir: 1 });
  }
  // the drift: the current V (m/s, o.dir 1 = toward the right) carries the tourist and everything loose; the camera follows him at o.follow
  // of the current, so what stands still (the hotel, the palms) slides the other way, faster the nearer it is
  function raftDraw(id, t, o) {
    const S = ST[id], V = o.speed * o.dir, Vc = V * o.follow, rel = (d) => ((V - Vc) * S.F) / d, cam = (d) => (-Vc * S.F) / d;
    const wrap = (x, w) => ((x % w) + w) % w;
    S.bands.forEach((b) => { const g = el(`${id}-wb${b.i}`); if (g) g.setAttribute("transform", `translate(${f1(wrap(rel(b.d) * t + 1.2 * Math.sin(t * 1.3 + b.i), 1200) - 1200)},${f1(2 * Math.sin(t * 2.1 + b.i * 1.7))})`); });
    el(`${id}-hot`).setAttribute("transform", `translate(${f1(cam(S.dH) * t)},0)`);
    S.PALMS.forEach((p) => { el(`${id}-pm${p.k}`).setAttribute("transform", `translate(${f1(cam(p.d) * t)},0)`); });
    S.DB.forEach((q) => {
      const x = q.x + rel(q.d) * t + 0.3 * S.F / q.d * Math.sin(t * 0.7 + q.ph) * 0.1, y = S.yAt(q.d) + 0.05 * (S.F / q.d) * Math.sin(t * 2.2 + q.ph);
      el(`${id}-db${q.k}`).setAttribute("transform", `translate(${f1(x)},${f1(y)}) rotate(${f1(q.rot + 6 * Math.sin(t * 1.7 + q.ph))})`);
    });
    if (S.rain) el(`${id}-rain`).setAttribute("transform", `translate(${f1(wrap(-260 * t, 300) - 150)},${f1(wrap(1500 * t, 600) - 300)})`);
    const bc = el(`${id}-beacon`); if (bc) bc.setAttribute("opacity", f1(Math.max(0, Math.sin(t * 9))));
  }
  // where the tourist floats: x on screen and how far his chest rides up and down
  function raftActor(id, t, o) {
    const S = ST[id], A = S.actor; if (!A) return;
    const V = o.speed * o.dir, Vc = V * o.follow, x = A.x + ((V - Vc) * S.F / S.dT) * t + (o.drift ?? 0) * t;
    const bob = 9 * Math.sin(t * 2.6) + 4 * Math.sin(t * 4.3 + 1), rock = 2.4 * Math.sin(t * 1.9 + 0.5) + 1.2 * Math.sin(t * 3.7);
    // the water line on him: local y −372 (his chest, just under the cooler's lid) sits on the surface at yT
    const y = S.yT + 372 * A.s + bob;
    el(A.id).setAttribute("transform", `translate(${f1(x)},${f1(y)}) rotate(${f1(rock)} 0 ${f1(-372 * A.s)}) scale(${A.flip ? -A.s : A.s},${A.s})`);
    // the near water's top edge rides the surface's chop; the foam ring hugs the cooler at his x
    const yT = S.yT, wv = (xx) => yT + 3 * Math.sin(xx * 0.012 + t * 3.1) + 2 * Math.sin(xx * 0.031 - t * 2.3);
    let d = `M-1200,${f1(wv(-1200))}`; for (let xx = -1150; xx <= 2400; xx += 50) d += `L${xx},${f1(wv(xx))}`;
    el(`${id}-wl`).setAttribute("d", d + "V1960H-1200Z");
    const hw = 175 * A.s, cx = x;
    let fo = `M${f1(cx - hw - 30)},${f1(yT)}`; for (let k = 0; k <= 14; k++) { const u = k / 14, xx = cx - hw - 30 + u * (2 * hw + 60), yy = yT + 4 + 10 * Math.sin(Math.PI * u) + 4 * Math.sin(k * 2.7 + t * 9); fo += `L${f1(xx)},${f1(yy)}`; }
    for (let k = 14; k >= 0; k--) { const u = k / 14, xx = cx - hw - 30 + u * (2 * hw + 60), yy = yT - 4 + 3 * Math.sin(k * 1.9 + t * 7); fo += `L${f1(xx)},${f1(yy)}`; }
    el(`${id}-fo1`).setAttribute("d", fo + "Z");
    el(`${id}-fo2`).setAttribute("d", `M${f1(cx - hw - 20)},${f1(yT + 6)}Q${f1(cx)},${f1(yT + 26 + 4 * Math.sin(t * 5))} ${f1(cx + hw + 20)},${f1(yT + 6)}`);
    for (let k = 0; k < 16; k++) { const u = ((k * 0.618) % 1), xx = cx - hw - 40 + u * (2 * hw + 80), yy = yT + 6 + 12 * Math.sin(Math.PI * u) + 5 * Math.sin(t * 6 + k), c = el(`${id}-fb${k}`); c.setAttribute("cx", f1(xx)); c.setAttribute("cy", f1(yy)); c.setAttribute("r", f1(2 + 3 * Math.abs(Math.sin(t * 3 + k)))); }
    // rings spreading from his bobbing
    for (let k = 0; k < 3; k++) { const ph = wrapT(t + k * 0.6, 1.8), R = hw + 40 + 260 * ph, e = el(`${id}-rg${k}`); e.setAttribute("cx", f1(cx)); e.setAttribute("cy", f1(yT + 6)); e.setAttribute("rx", f1(R)); e.setAttribute("ry", f1(R * 0.1)); e.setAttribute("opacity", f1(0.35 * (1 - ph / 1.8))); }
  }
  const wrapT = (x, w) => ((x % w) + w) % w;
  // Tide.raft(tl, id, t0, dur, o) runs the raft shot: o.actor the tourist's element id (the engine names actors `${shotId}-a${k}`: pass
  // `${id}-a0` from the shot's fx) — he must be the "tourist" cast in the "cling" pose; his white cooler is put inside his rig between his
  // torso and his arms (both arms then lie over its lid), and from then on this call places him: drifting with the current, bobbing and
  // rocking with his chest at the waterline. o.speed (1.2 m/s), o.dir (1 the current runs to the right, −1 left), o.follow (0.85 of the
  // current the camera keeps up with: he creeps across the frame while the hotel and the palms slide the other way), o.drift extra px/s
  Tide.raft = (tl, id, t0, dur, o = {}) => {
    const S = ST[id], oo = { speed: o.speed ?? 1.2, dir: o.dir ?? 1, follow: o.follow ?? 0.9, drift: o.drift ?? 0 };
    if (o.actor) {
      const a = el(o.actor), m = (a.getAttribute("transform") || "").match(/translate\(([-\d.]+)[ ,]([-\d.]+)\)\s*scale\(([-\d.]+)/);
      const sc = m ? +m[3] : 1;
      S.actor = { id: o.actor, x: o.x ?? (m ? +m[1] : 540), s: Math.abs(sc), flip: sc < 0 };
      const ua = el(`${o.actor}-uaF`), ub = el(`${o.actor}-uaB`);
      if (ua && ub && !el(`${o.actor}-cooler`)) {
        const fa = ua.parentNode, fb = ub.parentNode;
        fa.insertAdjacentHTML("beforebegin", `<g id="${o.actor}-cooler">${coolerArt()}</g>`);
        fa.parentNode.insertBefore(fb, fa);
      }
    }
    raftDraw(id, 0, oo); raftActor(id, 0, oo);
    const c = { t: 0 };
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => { raftDraw(id, c.t, oo); raftActor(id, c.t, oo); } }, t0);
  };

  // =====================================================================================================================================
  // the shop front and the hotel
  // =====================================================================================================================================
  // a small perspective camera: eye E, looking at T, focal length F px, the image centre (cx, cy); world metres, Y up
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]], dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const nrm = (a) => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
  function cam3(E, T, F, cx = 540, cy = 960) {
    const f = nrm(sub(T, E)), r = nrm(cross(f, [0, 1, 0])), u = cross(r, f);
    const P = (X) => { const v = sub(X, E), z = Math.max(0.05, dot(v, f)); return [cx + (F * dot(v, r)) / z, cy - (F * dot(v, u)) / z, z]; };
    P.E = E; P.F = F; P.f = f;
    return P;
  }
  const Q = (P, pts) => `M${pts.map((X) => P2(P(X))).join("L")}Z`;
  // a flat elevation drawing (its own units, +y down) laid on a vertical plane: art point (x, y) → world O + x·ux + y·uy. Drawn in
  // horizontal bands, each clipped to its exact perspective outline and mapped by the affine fit at its middle (a camera that looks
  // square at the plane makes every row exact; the bands take up the keystone)
  function onPlane(P, key, artId, O, ux, uy, xa, xb, bands) {
    const W = (x, y) => [O[0] + x * ux[0] + y * uy[0], O[1] + x * ux[1] + y * uy[1], O[2] + x * ux[2] + y * uy[2]];
    let g = "";
    bands.forEach(([y0, y1], i) => {
      const cid = `${key}-c${i}`, xm = (xa + xb) / 2, ym = (y0 + y1) / 2, h = 20;
      const s0 = P(W(xm, ym)), sx = P(W(xm + h, ym)), sy = P(W(xm, ym + h));
      const a = (sx[0] - s0[0]) / h, b = (sx[1] - s0[1]) / h, c = (sy[0] - s0[0]) / h, d = (sy[1] - s0[1]) / h;
      const e = s0[0] - a * xm - c * ym, ff = s0[1] - b * xm - d * ym;
      g += `<clipPath id="${cid}"><path d="${Q(P, [W(xa, y0 - 0.5), W(xb, y0 - 0.5), W(xb, y1 + 0.5), W(xa, y1 + 0.5)])}"/></clipPath>`;
      g += `<g clip-path="url(#${cid})"><use href="#${artId}" transform="matrix(${[a, b, c, d, e, ff].map((v) => v.toFixed(4)).join(",")})"/></g>`;
    });
    return g;
  }
  // ยาย's shop front as an elevation in centimetres: the origin on the sand at the left end, x along the front, y down (the deck at −50,
  // the eave at −270, the sign board up to −390). The folding doors stand open on the left two bays (the dark shop behind: the clock,
  // the clipping, the pale patch where the photo hung); the right bay is shut. Posts, the menu sheet, a shell chime, stumps under the deck.
  function shopArt(artId, o = {}) {
    const O2 = `stroke="${INK}" stroke-width="2.4" stroke-linejoin="round"`, YD = -50, YE = -270, leafC = "#4f948e";
    let g = `<rect x="-20" y="${YD}" width="740" height="50" fill="#1a1410" opacity=".55"/>`;
    [14, 236, 476, 690].forEach((x) => { g += `<rect x="${x - 9}" y="${YD}" width="18" height="50" fill="#bcb6aa" ${O2}/>`; });
    // the dark inside behind the open bays
    g += `<rect x="0" y="${YE}" width="480" height="${YD - YE}" fill="#16201e"/><rect x="40" y="${YE + 30}" width="400" height="140" fill="#2e4a46" opacity=".5"/>`;
    for (let k = 0; k < 9; k++) g += `<path d="M${40 + k * 50},${YE + 30}V${YE + 170}" stroke="#1a2a28" stroke-width="2" opacity=".6"/>`;
    g += `<rect x="196" y="${YE + 60}" width="44" height="34" fill="#4a6a64" opacity=".85"/><circle cx="218" cy="${YE + 50}" r="2" fill="#8a8a86"/>`;
    g += `<g opacity=".8">${TideCast.clipping(282, YE + 76, 0.1, { rot: -4 })}</g><circle cx="360" cy="${YE + 56}" r="18" fill="#3a5450" stroke="#1a2a28" stroke-width="2"/><path d="M360,${YE + 56}v-12M360,${YE + 56}l8,4" stroke="#1a2a28" stroke-width="2.4"/>`;
    g += `<path d="M30,${YD}L60,${YD - 50}H420L450,${YD}Z" fill="#e8dcb8" opacity=".1"/><rect x="60" y="${YE + 160}" width="320" height="${YD - YE - 160}" fill="#101614" opacity=".6"/>`;
    // folding doors: folded back against the posts on the open bays, the right bay shut (four leaves)
    const leaf = (x, w, c = leafC) => `<rect x="${f1(x)}" y="${YE}" width="${f1(w)}" height="${YD - YE}" fill="${c}" ${O2}/><rect x="${f1(x + w * 0.16)}" y="${YE + 18}" width="${f1(w * 0.68)}" height="88" fill="none" stroke="#2e6a64" stroke-width="2.4"/><rect x="${f1(x + w * 0.16)}" y="${YE + 118}" width="${f1(w * 0.68)}" height="88" fill="none" stroke="#2e6a64" stroke-width="2.4"/><path d="M${f1(x + w * 0.2)},${YE + 20}V${YE + 104}" stroke="#a8d8d0" stroke-width="2.4" opacity=".4"/>`;
    g += leaf(10, 16) + leaf(26, 14, "#478a84") + leaf(452, 14, "#478a84") + leaf(466, 16);
    for (let k = 0; k < 4; k++) g += leaf(486 + k * 51, 51);
    // posts, the eave beam, the roof's front edge, the sign board
    [0, 240, 480, 700].forEach((x) => { g += `<rect x="${x - 11}" y="${YE - 20}" width="22" height="${YD - YE + 20}" fill="url(#tdWoodH)" ${O2}/>`; });
    g += `<rect x="-30" y="${YE - 16}" width="760" height="16" fill="#8a5a32" ${O2}/><path d="M-40,${YE - 16}L-20,${YE - 34}H720L740,${YE - 16}Z" fill="url(#tdTin)" ${O2}/>`;
    g += `<rect x="70" y="-392" width="560" height="96" rx="8" fill="#f8f4ea" stroke="#1e4e94" stroke-width="7"/><path d="M110,-296V-286M590,-296V-286" stroke="#6a5a4a" stroke-width="8"/>
      <text x="350" y="-340" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="56" fill="#d8302a" stroke="#7a1410" stroke-width="1.5">ร้านยายพร</text>
      <text x="350" y="-308" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#1e4e94">อาหารทะเลสด · ปลาเผา หมึกย่าง</text>
      <g transform="translate(112,-344)"><path d="M-22,0C-10,-14 12,-14 20,-4L32,-12L30,0L32,12L20,4C12,14 -10,14 -22,0Z" fill="#3a8ad0" ${O2}/><circle cx="-12" cy="-2" r="2.5" fill="${INK}"/></g>
      <g transform="translate(590,-344)"><ellipse rx="18" ry="12" fill="#e8582a" ${O2}/><path d="M-16,-8l-10,-12M16,-8l10,-12M-14,8l-10,8M14,8l10,8" stroke="#e8582a" stroke-width="4"/></g>`;
    // the menu sheet taped to the middle post, the shell chime under the eave, the deck's front edge
    g += `<g transform="translate(248,${YE + 90}) rotate(-6)"><path d="M0,0H56V76H0Z" fill="#fbf8f0" ${O2}/>${["ปลาเผา", "หมึกย่าง", "ข้าวผัด"].map((t, i) => `<text x="6" y="${20 + i * 20}" font-family="Mali" font-weight="700" font-size="11" fill="#2e2a26">${t}</text>`).join("")}</g>`;
    g += `<g transform="translate(130,${YE})"><path d="M-10,0V40M0,0V54M10,0V34" stroke="#6a5a4a" stroke-width="1.6"/>${[[-10, 46], [0, 60], [10, 40]].map(([x, y]) => `<path d="M${x},${y + 7}c-6,-2 -7,-9 -4,-14q4,-3 8,0c4,5 3,12 -4,14z" fill="#f6e4d4" stroke="${INK}" stroke-width="1.4"/>`).join("")}</g>`;
    g += `<rect x="-20" y="${YD - 12}" width="740" height="12" fill="#c89464" ${O2}/><rect x="-20" y="${YD}" width="740" height="14" fill="#a8743e" ${O2}/>`;
    return `<g id="${artId}">${g}</g>`;
  }
  // world layout (metres; X along the beach, + to the right seen from the sea; Z toward the sea; Y up): the shop's front at Z 0 from X 0 to 7
  // (the deck 0.5 up, 1.4 deep, its steps at X 1.3 … 2.7 down to the sand at Z 2.3); the hotel beside it, its front at Z −3.5 from
  // X −16.3 to −1.3 (the stair tower on the shop's side); the sea's usual edge 45 m out
  const SF = { deck: 0.5, deckZ: 1.4, stepX: [1.3, 2.7], hotelZ: -3.5, hotelX: [-16.3, -1.3] };
  const SFV = {
    // a low camera on the sand at the foot of the steps, looking square at the shop and up: the hotel climbs out of the top at the left
    front: { E: [1.0, 0.62, 6.6], T: [1.0, 3.2, -3.4], F: 820 },
    // high on the beach, square to the hotel: the whole hotel, the shop beside it, someone at the shop's steps small at its foot
    side: { E: [-3.0, 7.0, 24.0], T: [-3.0, 5.6, -3.5], F: 900 },
    // from the hotel's outside stair (third-floor landing) looking down past the shop's roof to the sand and out over the bare seabed
    out: { E: [-2.2, 8.6, -2.6], T: [3.6, 0.2, 9.0], F: 760 },
  };
  function tideShopFront(L, o = {}) {
    const id = o.id || "sf", view = o.view || "front", P0 = PAL[o.time || "eerie"], r = mk(o.seed || 47), V = SFV[view], P = cam3(V.E, V.T, V.F);
    // the horizon (a far point straight ahead at eye height)
    const HZp = P([V.E[0] + (V.T[0] - V.E[0]) * 200, V.E[1], V.E[2] + (V.T[2] - V.E[2]) * 200])[1];
    sky(L, id, P0, HZp, (o.seed || 47) + 1);
    let f = "", m = "", s = "";
    // ---- far: the bay out to the horizon (high view: the sea drawn back to a band under the karsts, the white line), the hill (front view)
    const sea = o.sea ?? 1.6;
    if (view === "out") {
      const yS = (d) => P([V.E[0] + (V.T[0] - V.E[0]) / Math.hypot(V.T[0] - V.E[0], V.T[2] - V.E[2]) * d, 0, V.E[2] + (V.T[2] - V.E[2]) / Math.hypot(V.T[0] - V.E[0], V.T[2] - V.E[2]) * d])[1];
      const edge = yS(45 + 260 * Math.min(sea, 1.7)), beach = yS(45), sand = yS(14);
      f += `<rect x="-2000" y="${f1(HZp)}" width="5000" height="${f1(edge - HZp + 2)}" fill="${P0.sea[2]}"/><rect x="-2000" y="${f1(HZp)}" width="5000" height="12" fill="${P0.haze}" opacity=".6"/>`;
      [[-120, 120, 0.7], [380, 160, 0.82], [880, 110, 0.75]].forEach(([x, w, v], k) => { const hh = w * 1.3; f += `<path d="M${x - w / 2},${f1(HZp + 2)}Q${x - w / 2 - 8},${f1(HZp - hh * 0.6)} ${x - w * 0.3},${f1(HZp - hh)}Q${x},${f1(HZp - hh * 1.12)} ${x + w * 0.32},${f1(HZp - hh * 0.98)}Q${x + w / 2 + 6},${f1(HZp - hh * 0.5)} ${x + w / 2},${f1(HZp + 2)}Z" fill="${mixC(P0.rock, P0.haze, v * 0.7)}"/><path d="M${x - w * 0.34},${f1(HZp - hh * 0.96)}Q${x},${f1(HZp - hh * 1.18)} ${x + w * 0.34},${f1(HZp - hh * 0.96)}" stroke="${mixC(P0.green[1], P0.haze, v * 0.6)}" stroke-width="${f1(w * 0.16)}" fill="none" stroke-linecap="round"/>`; });
      // the white line far out (o.line 0 … 1)
      const wl = o.line ?? 1;
      if (wl > 0) f += `<path d="M-2000,${f1(HZp + 3)}H3000" stroke="#ffffff" stroke-width="${f1(3 + 5 * wl)}" opacity="${f1(0.5 + 0.4 * wl)}"/><path d="M-2000,${f1(HZp + 9)}H3000" stroke="${T(P0.sea[2], -0.4)}" stroke-width="${f1(4 * wl)}" opacity=".7"/>`;
      // the bare seabed: mud and sand ripples, pools holding the sky, rocks; then the beach
      f += `<path d="M-2000,${f1(edge)}H3000V${f1(beach)}H-2000Z" fill="${P0.bed[1]}"/><path d="M-2000,${f1(edge)}H3000" stroke="#ffffff" stroke-width="3" opacity=".7"/>`;
      for (let k = 0; k < 60; k++) { const y = edge + Math.pow(r(), 0.7) * (beach - edge), x = -300 + r() * 1700, w = 20 + r() * 90 * ((y - edge) / (beach - edge) + 0.3); f += `<path d="M${f1(x)},${f1(y)}q${f1(w / 2)},-3 ${f1(w)},0" stroke="${T(P0.bed[2], -0.25)}" stroke-width="1.6" fill="none" opacity=".45"/>`; }
      for (let k = 0; k < 14; k++) { const y = edge + r() * (beach - edge), x = -200 + r() * 1500, w = 14 + r() * 60 * ((y - edge) / (beach - edge) + 0.3); f += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w)}" ry="${f1(w * 0.16)}" fill="${P0.sky[2]}" opacity=".75"/>`; }
      for (let k = 0; k < 20; k++) { const y = edge + r() * (beach - edge), x = -200 + r() * 1500, w = 4 + r() * 16 * ((y - edge) / (beach - edge) + 0.3); f += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w)}" ry="${f1(w * 0.4)}" fill="${T(P0.bed[2], -0.3)}"/>`; }
      f += `<path d="M-2000,${f1(beach)}H3000V2600H-2000Z" fill="${P0.sand[1]}"/><path d="M-2000,${f1(beach)}H3000" stroke="${P0.wet ? P0.wet[0] : "#b9a482"}" stroke-width="14" opacity=".6"/>`;
      for (let k = 0; k < 40; k++) { const y = beach + Math.pow(r(), 0.8) * (2000 - beach), x = -200 + r() * 1500, w = 30 + r() * 120 * ((y - beach) / 900 + 0.3); f += `<path d="M${f1(x)},${f1(y)}q${f1(w / 2)},-3 ${f1(w)},0" stroke="#fff" stroke-width="2" fill="none" opacity=".3"/>`; }
      void sand;
    } else {
      // the jungle hill behind the village, the tower on its shoulder (beacon), haze
      f += `<path d="M-600,${f1(HZp + 40)}L-600,${f1(HZp - 520)}Q-200,${f1(HZp - 760)} 300,${f1(HZp - 700)}Q760,${f1(HZp - 820)} 1100,${f1(HZp - 640)}Q1500,${f1(HZp - 520)} 1700,${f1(HZp - 400)}V${f1(HZp + 40)}Z" fill="${P0.green[0]}"/>`;
      for (let k = 0; k < 40; k++) { const x = -500 + r() * 2100, y = HZp - 700 + r() * 680; f += crown(x, y, 46 + r() * 50, r, [T(P0.green[0], -0.1), P0.green[1], P0.green[2], T(P0.green[2], 0.2)], 7); }
      f += `<rect x="-600" y="${f1(HZp - 800)}" width="2300" height="840" fill="${P0.haze}" opacity=".3"/>` + Tide.tower(880, HZp - 380, 0.38, id);
    }
    put(L.far, f);
    // ---- mid: the hotel (its front in bands, the stair tower's side toward the shop with its windows and green exit sign), palms
    const hotO = [(SF.hotelX[0] + SF.hotelX[1]) / 2, 0, SF.hotelZ], uH = 15 / 560, artH = `${id}-hart`;
    let defs = `<defs><g id="${artH}">${hotelArt(id + "h")}</g>${shopArt(`${id}-sart`)}</defs>`;
    const HB = [[-680, -520], [-520, -416], [-416, -312], [-312, -208], [-208, -104], [-104, 0]];
    let hot = view === "out" ? "" : onPlane(P, `${id}-hb`, artH, hotO, [uH, 0, 0], [0, -uH, 0], -360, 290, HB);
    // the stair tower's side face (X −1.3), toward the shop: shaded concrete, a column of windows with the flights behind, the exit sign
    const sx = SF.hotelX[1], hz0 = SF.hotelZ, hz1 = SF.hotelZ - 3.2, Ht = 15.6;
    if (view !== "out" && P.E[0] > sx) {
      hot += `<path d="${Q(P, [[sx, 0, hz0], [sx, Ht, hz0], [sx, Ht, hz1], [sx, 0, hz1]])}" fill="#d8cfbe" ${ln(2.6)}/>`;
      for (let n = 0; n < 5; n++) { const y0 = n * 2.79 + 0.5, y1 = y0 + 1.9; hot += `<path d="${Q(P, [[sx, y0, hz0 - 0.6], [sx, y1, hz0 - 0.6], [sx, y1, hz1 + 0.6], [sx, y0, hz1 + 0.6]])}" fill="#4e6a74" ${ln(2)}/><path d="M${P2(P([sx, y0 + 0.2, hz0 - 0.8]))}L${P2(P([sx, y1 - 0.3, hz1 + 0.8]))}" stroke="#d8d0c0" stroke-width="5"/>`; }
      hot += `<path d="${Q(P, [[sx, 2.2, hz0 - 0.9], [sx, 2.6, hz0 - 0.9], [sx, 2.6, hz0 - 2.2], [sx, 2.2, hz0 - 2.2]])}" fill="#2e8a4a" ${ln(1.6)}/>`;
      // the outside stair's open landing on this side: a door at the foot, the first flight's rail climbing
      hot += `<path d="${Q(P, [[sx, 0, hz0 - 0.9], [sx, 2.1, hz0 - 0.9], [sx, 2.1, hz0 - 2.0], [sx, 0, hz0 - 2.0]])}" fill="#3e4a4e" ${ln(2)}/>`;
    }
    m += defs + `<g id="${id}-hotel">${hot}</g>`;
    // palms between the shop and the hotel, behind
    const palm = (X, Z, h, lean, seed) => { const b = P([X, 0, Z]), t = P([X, h, Z]); return Tide.coco(b[0], b[1], (b[1] - t[1]) / 900, lean, seed, { pal: P0.leaf, q: 0.7 }); };
    if (view !== "out") m += palm(-0.2, -6, 9, 0.05, 81) + palm(8.5, -5, 8, -0.06, 82);
    put(L.mid, m);
    // ---- set: the ground (sand, ยาย's prints toward the hotel), the shop (its front in bands, the deck, the steps, the awning over them)
    const sand0 = P([V.E[0], 0, -60])[1];
    if (view !== "out") {
      s += `<path d="M-1000,${f1(Math.min(HZp + 20, sand0))}H2200V2400H-1000Z" fill="${P0.sand[1]}"/>`;
      for (let k = 0; k < 30; k++) { const X = -6 + r() * 16, Z = -3 + r() * 9, a = P([X, 0, Z]), w = 0.3 + r() * 0.8, b = P([X + w, 0, Z]); s += `<path d="M${P2(a)}L${P2(b)}" stroke="#fff" stroke-width="2.2" opacity=".3" stroke-linecap="round"/>`; }
    }
    const steps = [];
    for (let k = 0; k < 3; k++) { const yT = SF.deck - (k + 1) * (SF.deck / 3), z0 = SF.deckZ + k * 0.3, z1 = z0 + 0.3; steps.push({ yT, z0, z1 }); }
    // ยาย's prints on the sand: from the foot of the steps off toward the hotel's stair
    const dent = T(P0.sand[2], -0.32);
    for (let k = 0; k < 7; k++) { const X = SF.stepX[0] + 0.3 - k * 0.55, Z = 2.6 - k * 0.32 + (k % 2) * 0.12, c = P([X, 0, Z]), c2 = P([X - 0.26, 0, Z]), w = Math.hypot(c2[0] - c[0], c2[1] - c[1]); s += `<ellipse cx="${f1(c[0])}" cy="${f1(c[1])}" rx="${f1(w * 0.5)}" ry="${f1(Math.max(1.5, w * 0.16))}" fill="${dent}" opacity=".7"/>`; }
    // the shop: its front (bands: under the deck, the wall, the roof and sign), the side wall at X 0, the tin roof seen from the high view
    const shO = [0, 0, 0], uS = 0.01;
    let sh = "";
    if (view === "out") {
      // from above: the tin roof falling to the front, the awning, the deck and the steps
      sh += `<path d="${Q(P, [[-0.3, 3.0, 0.1], [7.3, 3.0, 0.1], [7.3, 3.9, -4.2], [-0.3, 3.9, -4.2]])}" fill="url(#tdTin)" ${ln(2.6)}/>`;
      for (let k = 1; k < 16; k++) { const X = -0.3 + k * 0.5; sh += `<path d="M${P2(P([X, 3.0, 0.1]))}L${P2(P([X, 3.9, -4.2]))}" stroke="#7a8488" stroke-width="2" opacity=".7"/>`; }
      [[1.2, 1.4], [4.6, 2.0]].forEach(([X, w]) => { sh += `<path d="M${P2(P([X, 3.05, -0.4]))}L${P2(P([X + w * 0.1, 3.4, -2]))}" stroke="#b0643a" stroke-width="6" opacity=".5"/>`; });
      sh += `<path d="${Q(P, [[-0.4, 2.62, 0.05], [7.4, 2.62, 0.05], [7.4, 2.25, 1.55], [-0.4, 2.25, 1.55]])}" fill="url(#tdTarp)" ${ln(2.4)}/>`;
      sh += `<path d="${Q(P, [[-0.2, SF.deck, 0], [7.2, SF.deck, 0], [7.2, SF.deck, SF.deckZ], [-0.2, SF.deck, SF.deckZ]])}" fill="#c89464" ${ln(2.2)}/>`;
    } else {
      sh += onPlane(P, `${id}-sb`, `${id}-sart`, shO, [uS, 0, 0], [0, -uS, 0], -40, 740, [[-400, -290], [-290, -50], [-50, 0]]);
      // the deck's top (a sliver from this low eye), its front edge and stumps are in the front's bottom band; the awning over the deck
      sh += `<path d="${Q(P, [[-0.2, SF.deck, 0], [7.2, SF.deck, 0], [7.2, SF.deck, SF.deckZ], [-0.2, SF.deck, SF.deckZ]])}" fill="#c89464" ${ln(2)}/>`;
      sh += `<path d="${Q(P, [[-0.2, SF.deck - 0.14, SF.deckZ], [7.2, SF.deck - 0.14, SF.deckZ], [7.2, SF.deck, SF.deckZ], [-0.2, SF.deck, SF.deckZ]])}" fill="#a8743e" ${ln(2)}/>`;
      // the ice cooler on the deck by the shut bay ("น้ำแข็ง"), its lid open
      const c0 = P([5.2, SF.deck, 0.6]), c1 = P([6.2, SF.deck + 0.55, 0.6]), cw = c1[0] - c0[0], chh = c0[1] - c1[1];
      sh += `<g transform="translate(${f1(c0[0])},${f1(c0[1])})"><rect x="0" y="${f1(-chh)}" width="${f1(cw)}" height="${f1(chh)}" rx="5" fill="#f4f6f4" ${ln(2.2)}/><path d="M0,${f1(-chh)}L${f1(-cw * 0.12)},${f1(-chh * 1.9)}L${f1(cw * 0.92)},${f1(-chh * 1.8)}L${f1(cw)},${f1(-chh)}Z" fill="#dfe6e8" ${ln(2)}/><text x="${f1(cw / 2)}" y="${f1(-chh * 0.35)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${f1(chh * 0.32)}" fill="#2a6ab8">น้ำแข็ง</text></g>`;
    }
    // the steps: three wooden treads down from the deck to the sand
    steps.forEach((q) => {
      const [x0, x1] = SF.stepX;
      sh += `<path d="${Q(P, [[x0, q.yT, q.z0], [x1, q.yT, q.z0], [x1, q.yT, q.z1], [x0, q.yT, q.z1]])}" fill="#d8a46c" ${ln(2)}/>`;
      sh += `<path d="${Q(P, [[x0, q.yT, q.z1], [x1, q.yT, q.z1], [x1, Math.max(0, q.yT - SF.deck / 3), q.z1], [x0, Math.max(0, q.yT - SF.deck / 3), q.z1]])}" fill="#a8743e" ${ln(2.2)}/>`;
    });
    // one of ยาย's brown sandals left on the middle step (as EP.1 left it) — o.slipper false
    if (o.slipper !== false) { const a = P([1.75, steps[1].yT, steps[1].z0 + 0.15]), b = P([2.02, steps[1].yT, steps[1].z0 + 0.15]), w = b[0] - a[0];
      sh += `<g transform="translate(${f1(a[0])},${f1(a[1])}) rotate(-8) scale(${f1(w / 110)},${f1(w / 160)})"><path d="M-58,4C-60,-14 -40,-24 -14,-22C8,-20 20,-26 40,-24C60,-22 64,-6 62,4C60,16 44,22 24,20C6,18 -6,22 -24,24C-46,26 -56,18 -58,4Z" fill="#3a2414" ${ln(3)}/><path d="M14,-26C10,-4 12,10 18,24L38,22C34,8 34,-8 38,-26Z" fill="#5a3a22" ${ln(2.8)}/></g>`; }
    s += sh;
    put(L.set, s);
    // ---- the awning in front of the cast in the low view (it hangs over the steps, between the camera and the shop): redrawn hem
    if (view !== "out") {
      const aw0 = [-0.4, 2.62, 0.05], aw1 = [7.4, 2.62, 0.05], hemY = 2.2, hemZ = 1.6;
      const awn = `<path d="${Q(P, [aw0, aw1, [7.4, hemY, hemZ], [-0.4, hemY, hemZ]])}" fill="url(#tdTarp)" ${ln(2.6)}/><path d="M${P2(P([-0.4, hemY + 0.05, hemZ - 0.05]))}L${P2(P([7.4, hemY + 0.05, hemZ - 0.05]))}" stroke="#7ab8f0" stroke-width="4" opacity=".6"/><path id="${id}-hem" d="" fill="url(#tdTarp)" ${ln(2.2)}/>`;
      put(L.set, awn);
    }
    // fg: a palm frond hanging into the top right (low view) / the hotel stair's railing across the bottom left (high view)
    if (view === "out") {
      const rail = (a, b) => `<path d="M${P2(P(a))}L${P2(P(b))}" stroke="${INK}" stroke-width="16" stroke-linecap="round"/><path d="M${P2(P(a))}L${P2(P(b))}" stroke="url(#t2Steel)" stroke-width="11" stroke-linecap="round"/>`;
      let fr = "";
      const x0 = SF.hotelX[1] + 0.25, zA = -2.0, zB = 0.4;
      [0, 0.5, 1].forEach((k) => { const z = lerp(zA, zB, k); fr += rail([x0, 7.6, z], [x0, 8.6, z]); });
      fr += rail([x0, 8.6, zA], [x0, 8.6, zB]) + rail([x0, 8.1, zA], [x0, 8.1, zB]);
      fr += `<path d="${Q(P, [[x0 - 0.2, 7.6, zA - 0.4], [x0 - 0.2, 7.6, zB + 0.4], [x0 - 1.4, 7.6, zB + 0.4], [x0 - 1.4, 7.6, zA - 0.4]])}" fill="#d8d0c0" ${ln(2.4)}/>`;
      put(L.fg, fr);
    } else put(L.fg, `<g transform="translate(1140,-40) rotate(28)">${Tide.coco(0, 0, 1.15, 0, 63, { trunk: false, pal: [T(P0.leaf[0], -0.3), T(P0.leaf[1], -0.25), P0.leaf[1]] })}</g>`);
    ST[id] = { kind: "shopFront", view, P, hemY: 2.2, hemZ: 1.6 };
    shopFrontDraw(id, 0, 1, true);
  }
  const mixC = (a, b, k) => { const A = [1, 3, 5].map((i) => parseInt(a.substr(i, 2), 16)), B = [1, 3, 5].map((i) => parseInt(b.substr(i, 2), 16)); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, "0")).join(""); };
  function shopFrontDraw(id, t, amp, siren) {
    const S = ST[id], P = S.P, hem = el(`${id}-hem`);
    if (hem) {
      let d = "";
      for (let X = -0.4, i = 0; X <= 7.401; X += 0.4, i++) {
        const w = 0.04 * amp * Math.sin(X * 2 + t * 6), a = P([X, S.hemY, S.hemZ]), b = P([Math.min(7.4, X + 0.2), S.hemY - 0.16 + w, S.hemZ + 0.02]), c = P([Math.min(7.4, X + 0.4), S.hemY, S.hemZ]);
        d += `${i ? "" : `M${P2(a)}`}Q${P2(b)} ${P2(c)}`;
      }
      d += `L${P2(P([7.4, S.hemY + 0.06, S.hemZ]))}L${P2(P([-0.4, S.hemY + 0.06, S.hemZ]))}Z`;
      hem.setAttribute("d", d);
    }
    const bc = el(`${id}-beacon`); if (bc) bc.setAttribute("opacity", siren ? f1(Math.max(0, Math.sin(t * 9))) : "0");
  }
  // where to stand someone in the shop-front views: world X (along the beach), Z (toward the sea), standing on the sand (or o.y metres
  // up) → { x, y, s } the feet on screen and the rig scale for an adult 1.6 m tall (a child × 0.76)
  Tide.shopFrontPos = (id, X, Z, Y = 0, h = 1.6) => { const P = ST[id].P, a = P([X, Y, Z]), b = P([X, Y + h, Z]); return { x: Math.round(a[0]), y: Math.round(a[1]), s: +((a[1] - b[1]) / 620).toFixed(3) }; };
  // the wind in the low view: the awning's hem ripples; o.siren (true) blinks the tower's beacon
  Tide.shopFront = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, amp = o.amp ?? 1, siren = o.siren !== false;
    shopFrontDraw(id, 0, amp, siren);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => shopFrontDraw(id, c.t, amp, siren) }, t0);
  };

  Object.assign(Sets, { tideGrab, tideRaft, tideShopFront });
})();
