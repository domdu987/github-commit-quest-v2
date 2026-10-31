// ---------- หมาเฝ้าบ้าน (พิษสุนัขบ้า): the dogs — a side-view dog rig in the house style (ink line, flat fill, one shade, one highlight) ----------
// Dog.svg(o) returns the markup of one dog; put it in any layer (usually L.act or L.set). Dog.drive(tl, id, t0, dur, mode, o) poses it over time
// (a proxy tween whose onUpdate writes the joints from the timeline time, so any seek is exact).
//
//   o.id     ids: <id> root (translate/scale written by drive) · <id>-body · <id>-head · <id>-jaw · <id>-tail · <id>-leg{0..3} / -knee{0..3}
//            <id>-eye (normal eye) · <id>-glow (green eye shine, hidden unless o.glow / pose glow) · <id>-tongue · <id>-drool · <id>-lip (snarl)
//   o.kind   "dam"  ไอ้ดำ: grown black Thai dog, prick ears, tan "four eyes" spots over the eyes, tan chest and socks, red rope collar
//            "pup"  the stray puppy: cream with a brown saddle and one brown ear, big head, short legs, thin (ribs), a scab on the muzzle
//            "pupS" the same puppy sick: dull coat, head low, drool by default
//   o.x o.y  the paws' ground point · o.s scale (dam: 1 ≈ 0.5 m at the shoulder next to rig2 people at s 1; pup at 1 ≈ 0.22 m)
//   o.flip   face left · o.glow true: eye shine on from the start (night)
//
// Dog.drive modes (u = seconds into the pose):
//   idle (breathing, slow tail) · wag (fast tail, happy head bob) · walk / trot (o.to: target x, legs cycle, body bobs) · sniff (head down, bobbing)
//   lick (head down, tongue flicks: o.rate per second) · growl (head low, lip up, tremble, tail low) · bark (jaw snaps on o.beats)
//   howl (sits back, head up, jaw open, ears back) · sick (head low and swaying, drool, wobble) · cower (crouched low, tail tucked)
//   lunge (springs forward o.to, jaw snaps) · sit · lie (on its belly, head on paws)
//   o.glow: eye shine on/off during the pose · o.to: walk target x · o.ease
(function () {
  const INK = "#2a1c18";
  const f = (v) => (+v).toFixed(1);
  const ln = (w = 3) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const PAL = {
    dam: { coat: "#24212a", coatL: "#3e3a4a", coatD: "#121016", tan: "#c98a4c", tanL: "#e2aa6a", nose: "#141014", inner: "#6a4048", collar: "#c8322a" },
    pup: { coat: "#ecd2a6", coatL: "#fbecd0", coatD: "#c8a272", tan: "#9a5a32", tanL: "#b8784a", nose: "#2a1e1e", inner: "#e0909a", collar: null },
    pupS: { coat: "#d2bc94", coatL: "#e4d2b0", coatD: "#a8906a", tan: "#80502e", tanL: "#9a6a44", nose: "#2a1e1e", inner: "#c88088", collar: null },
  };
  Sets.DEFS += `
    <radialGradient id="dgGlow"><stop offset="0" stop-color="#e8ffb0" stop-opacity="1"/><stop offset=".3" stop-color="#8dff5a" stop-opacity=".75"/><stop offset="1" stop-color="#5aff4a" stop-opacity="0"/></radialGradient>
    <radialGradient id="dgShadow"><stop offset="0" stop-color="#0a0608" stop-opacity=".5"/><stop offset=".65" stop-color="#0a0608" stop-opacity=".2"/><stop offset="1" stop-color="#0a0608" stop-opacity="0"/></radialGradient>`;

  // body plan per kind (dog units, ground y 0, nose to +x)
  const PLAN = {
    dam: { hipF: [62, -150], hipB: [-78, -146], up: 66, lo: 76, paw: 14, legW: 22, neck: [86, -176], headS: 1, tail: [-104, -164], belly: -96 },
    pup: { hipF: [40, -80], hipB: [-44, -80], up: 32, lo: 40, paw: 10, legW: 18, neck: [50, -92], headS: 0.84, tail: [-62, -92], belly: -50 },
  };
  PLAN.pupS = PLAN.pup;

  const legSvg = (id, k, P, c, far) => {
    const fill = far ? c.coatD : c.coat, w = P.legW, back = k % 2 === 1, lw = w * 0.4;
    const sockC = c === PAL.dam ? (far ? "#8a5a32" : c.tan) : (far ? c.coatD : c.coatL);
    // upper: front = a tapered capsule, back = a thick thigh; both with rounded ends that overlap the body and the joint (no seam lines)
    const up = back
      ? `M${-w * 0.95},-14C${-w * 1.2},${P.up * 0.45} ${-w * 0.5},${P.up + w * 0.5} ${0},${P.up + lw}C${lw * 1.6},${P.up + lw} ${w * 0.8},${P.up * 0.5} ${w * 0.75},-10C${w * 0.6},-24 ${-w * 0.7},-26 ${-w * 0.95},-14Z`
      : `M${-w * 0.55},-12C${-w * 0.62},${P.up * 0.5} ${-lw * 1.1},${P.up} ${-lw},${P.up}C${-lw},${P.up + lw * 1.2} ${lw},${P.up + lw * 1.2} ${lw},${P.up}C${lw * 1.1},${P.up * 0.6} ${w * 0.62},${P.up * 0.3} ${w * 0.55},-12C${w * 0.4},-22 ${-w * 0.4},-22 ${-w * 0.55},-12Z`;
    const lo = `M${-lw},0C${-lw},${-lw * 1.1} ${lw},${-lw * 1.1} ${lw},0L${lw * 0.85},${P.lo - 6}L${-lw * 0.85},${P.lo - 6}Z`;
    const paw = `M${-lw * 1.1},${P.lo - 7}Q${-lw * 1.3},${P.lo + 3} ${-lw * 0.5},${P.lo + 3}L${lw * 2.1},${P.lo + 3}Q${lw * 2.9},${P.lo + 2} ${lw * 2.3},${P.lo - 6}Q${lw * 1.2},${P.lo - 11} ${-lw * 1.1},${P.lo - 7}Z`;
    const toes = `<path d="M${f(lw * 0.7)},${f(P.lo - 1)}v4M${f(lw * 1.5)},${f(P.lo - 2)}v5" stroke="${INK}" stroke-width="1.6" opacity=".55"/>`;
    return `<g id="${id}-leg${k}" transform="rotate(0)">
      <g transform="translate(0,${P.up})"><g id="${id}-knee${k}" transform="rotate(0)">
        <path d="${lo}" fill="${fill}" ${ln(2.4)}/>
        <path d="M${-lw * 0.9},${P.lo * 0.6}L${lw * 0.9},${P.lo * 0.6}L${lw * 0.86},${P.lo - 6}L${-lw * 0.86},${P.lo - 6}Z" fill="${sockC}"/>
        <path d="${paw}" fill="${sockC}" ${ln(2.4)}/>${toes}
      </g></g>
      <path d="${up}" fill="${fill}" ${ln(2.6)}/>
      ${!far ? `<path d="M${-w * 0.25},2Q${-w * 0.3},${P.up * 0.55} ${-lw * 0.3},${P.up - 2}" stroke="${c.coatL}" stroke-width="3.4" fill="none" stroke-linecap="round" opacity=".45"/>` : ""}</g>`;
  };

  const headSvg = (id, kind, c, o) => {
    const pup = kind !== "dam";
    // head drawn around the neck pivot (0,0): skull up-right, snout to +x
    const skull = pup
      ? `M-14,-6C-26,-40 -6,-74 26,-78C58,-80 78,-56 80,-34C96,-30 110,-22 112,-10C112,2 100,8 84,8C70,14 50,18 30,16C6,14 -8,8 -14,-6Z`
      : `M-18,-4C-26,-36 -4,-62 26,-66C54,-68 70,-54 76,-40C96,-36 122,-28 128,-16C132,-4 122,4 104,6C84,12 58,16 32,14C6,12 -12,8 -18,-4Z`;
    const snoutHi = pup ? `M60,-30Q86,-32 104,-20` : `M64,-36Q98,-34 120,-22`;
    const nose = pup ? `<ellipse cx="108" cy="-14" rx="8" ry="6.5" fill="${c.nose}" ${ln(2)}/><circle cx="106" cy="-17" r="2" fill="#fff" opacity=".5"/>`
      : `<ellipse cx="126" cy="-18" rx="9" ry="7.5" fill="${c.nose}" ${ln(2)}/><circle cx="123" cy="-21" r="2.4" fill="#fff" opacity=".45"/>`;
    const eyeX = pup ? 46 : 52, eyeY = pup ? -40 : -40, er = pup ? 9 : 7;
    const eye = `<g id="${id}-eye"><ellipse cx="${eyeX}" cy="${eyeY}" rx="${er}" ry="${er * 0.85}" fill="#2a160e" ${ln(2)}/>
      <circle cx="${eyeX + er * 0.3}" cy="${eyeY - er * 0.3}" r="${er * 0.38}" fill="#fff"/><circle cx="${eyeX - er * 0.35}" cy="${eyeY + er * 0.3}" r="${er * 0.16}" fill="#fff" opacity=".7"/>
      <path d="M${eyeX - er - 2},${eyeY - er + 1}Q${eyeX},${eyeY - er - 5} ${eyeX + er + 3},${eyeY - er + 2}" stroke="${INK}" stroke-width="2.2" fill="none"/></g>`;
    const glow = `<g id="${id}-glow" opacity="${o.glow ? 1 : 0}"><circle cx="${eyeX}" cy="${eyeY}" r="${er * 3.4}" fill="url(#dgGlow)" opacity=".55"/>
      <ellipse cx="${eyeX}" cy="${eyeY}" rx="${er * 0.95}" ry="${er * 0.8}" fill="#b6ff6a"/><ellipse cx="${eyeX + 1}" cy="${eyeY}" rx="${er * 0.3}" ry="${er * 0.7}" fill="#1a3a0a"/>
      <circle cx="${eyeX + er * 0.35}" cy="${eyeY - er * 0.3}" r="${er * 0.25}" fill="#fff"/></g>`;
    const spots = kind === "dam" ? `<ellipse cx="${eyeX - 2}" cy="${eyeY - 15}" rx="6.5" ry="4.5" fill="${c.tan}" ${ln(1.6)}/><path d="M${eyeX - 6},${eyeY - 17}q4,-2 8,0" stroke="${c.tanL}" stroke-width="2" fill="none"/>` : "";
    const muzzle = kind === "dam" ? `<path d="M76,-8Q100,-2 124,-8Q120,4 104,6C84,12 64,12 52,8Q62,-4 76,-8Z" fill="${c.tan}" opacity=".95"/>`
      : `<path d="M58,-6Q84,-2 106,-6Q102,6 84,8C70,12 54,14 42,10Q48,0 58,-6Z" fill="${c.coatL}"/>`;
    const scab = kind !== "dam" ? `<path d="M72,-26q4,-3 8,0q-2,4 -8,0Z" fill="#a83a2a" opacity=".85"/>` : "";
    const earB = pup
      ? `<path d="M6,-56C-4,-80 6,-96 18,-98C30,-92 30,-74 22,-60Z" fill="${kind === "pup" ? c.tan : c.coatD}" ${ln(2.4)}/>`
      : `<path d="M8,-54L4,-104Q12,-108 20,-100L34,-58Z" fill="${c.coatD}" ${ln(2.4)}/>`;
    const earF = pup
      ? `<g id="${id}-ear"><path d="M22,-62C18,-92 32,-104 46,-100C56,-90 52,-70 40,-58C48,-50 46,-40 40,-40C32,-44 26,-52 22,-62Z" fill="${kind === "pup" ? c.tan : c.coatD}" ${ln(2.6)}/>
          <path d="M30,-70C30,-86 38,-94 44,-92" stroke="${c.inner}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/></g>`
      : `<g id="${id}-ear"><path d="M18,-56L18,-112Q26,-118 34,-110L48,-58Z" fill="${c.coat}" ${ln(2.6)}/><path d="M26,-62L26,-100Q30,-104 34,-98L40,-62Z" fill="${c.inner}" opacity=".85"/>
          ${o.earWound ? `<path d="M38,-92L30,-86L40,-80Z" fill="#7a1018" stroke="${INK}" stroke-width="1.6"/><path d="M36,-96L28,-88M38,-78L30,-72" stroke="#d8303a" stroke-width="3" stroke-linecap="round"/>
            <path d="M33,-84q-2,8 0,14" stroke="#b81e2a" stroke-width="3.4" fill="none" stroke-linecap="round"/><circle cx="33" cy="-68" r="3" fill="#b81e2a"/>` : ""}</g>`;
    const jaw = pup
      ? `<g transform="translate(36,4)"><g id="${id}-jaw" transform="rotate(0)"><path d="M-8,-2Q24,10 64,2Q70,10 60,16Q30,22 -6,12Z" fill="${c.coat}" ${ln(2.4)}/>
          <g id="${id}-tongue" opacity="0"><path d="M30,8Q48,12 62,8Q72,22 60,34Q48,40 42,28Q38,18 30,14Z" fill="#e8607a" ${ln(2)}/><path d="M50,14q2,10 0,18" stroke="#b83a52" stroke-width="2" fill="none"/></g></g></g>`
      : `<g transform="translate(40,6)"><g id="${id}-jaw" transform="rotate(0)"><path d="M-10,-2Q30,10 80,2Q86,10 76,16Q36,22 -8,12Z" fill="${c.tan}" ${ln(2.4)}/>
          <path d="M60,4l3,7l3,-7M44,6l3,7l3,-7" fill="#fff" stroke="${INK}" stroke-width="1.4"/>
          <g id="${id}-tongue" opacity="0"><path d="M40,8Q60,12 76,8Q86,24 74,38Q60,44 54,32Q50,20 40,14Z" fill="#d8506a" ${ln(2)}/><path d="M62,14q2,12 0,22" stroke="#a83048" stroke-width="2" fill="none"/></g></g></g>`;
    const lip = kind === "dam"
      ? `<g id="${id}-lip" opacity="0"><path d="M72,-6Q92,-18 120,-10" stroke="${INK}" stroke-width="3" fill="none"/><path d="M76,-4L80,10L86,-4ZM92,-8L95,4L99,-8ZM104,-9L107,2L110,-9Z" fill="#fff" stroke="${INK}" stroke-width="1.6"/>
          <path d="M70,-24q10,6 20,2M80,-30q10,6 20,2" stroke="${c.coatL}" stroke-width="2.2" fill="none"/></g>` : `<g id="${id}-lip" opacity="0"><path d="M60,-4Q78,-14 100,-6" stroke="${INK}" stroke-width="2.6" fill="none"/><path d="M64,-2L67,8L70,-2ZM78,-6L81,4L84,-6Z" fill="#fff" stroke="${INK}" stroke-width="1.4"/></g>`;
    const drool = `<g id="${id}-drool" opacity="${kind === "pupS" ? 1 : 0}"><path d="M${pup ? 70 : 84},${pup ? 18 : 20}q-3,14 1,30q4,8 6,0q2,-14 -1,-30Z" fill="#e8f4ff" opacity=".85" ${ln(1.4)}/><circle cx="${pup ? 74 : 88}" cy="${pup ? 50 : 52}" r="3.2" fill="#e8f4ff" ${ln(1.2)}/>
      <path d="M${pup ? 98 : 112},${pup ? 10 : 12}q-2,10 1,18" stroke="#e8f4ff" stroke-width="3" fill="none" opacity=".8"/></g>`;
    const collar = c.collar ? `<path d="M-14,-24Q-4,-8 6,10" stroke="${c.collar}" stroke-width="10" stroke-linecap="round" fill="none"/><path d="M-14,-24Q-4,-8 6,10" stroke="${INK}" stroke-width="2" stroke-dasharray="3 5" fill="none" opacity=".6"/>` : "";
    return `${earB}${jaw}<path d="${skull}" fill="${c.coat}" ${ln(3)}/>${muzzle}<path d="${skull}" fill="none" ${ln(3)}/>
      <path d="${snoutHi}" stroke="${c.coatL}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".55"/>
      <path d="M2,-30Q10,-58 34,-64" stroke="${c.coatL}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".45"/>
      ${spots}${scab}${eye}${glow}${nose}${lip}${drool}${earF}${collar}`;
  };

  const bodySvg = (id, kind, c, P) => {
    const pup = kind !== "dam";
    const torso = pup
      ? `M-66,-90C-76,-70 -62,-50 -40,-52C-14,-48 14,-46 38,-54C60,-58 72,-76 66,-98C60,-116 34,-114 6,-110C-24,-110 -58,-112 -66,-90Z`
      : `M-112,-168C-124,-140 -112,-108 -84,-104C-50,-94 10,-94 60,-104C90,-110 104,-136 98,-164C92,-196 54,-196 10,-188C-30,-182 -98,-196 -112,-168Z`;
    const chest = kind === "dam" ? `<path d="M64,-108C86,-112 100,-130 98,-156Q84,-128 58,-120Z" fill="${c.tan}"/>` : "";
    const saddle = kind !== "dam" ? `<path d="M-40,-104C-30,-114 10,-114 26,-104C22,-90 -26,-88 -40,-104Z" fill="${c.tan}" opacity=".9"/>` : "";
    const ribs = kind === "pupS" ? `<path d="M-14,-70q6,10 0,20M-2,-72q6,10 0,20M10,-72q6,10 0,20" stroke="${c.coatD}" stroke-width="2.4" fill="none" opacity=".8"/>` : (kind === "pup" ? `<path d="M-8,-70q5,9 0,17M4,-71q5,9 0,17" stroke="${c.coatD}" stroke-width="2" fill="none" opacity=".55"/>` : "");
    const sheen = pup ? `<path d="M-50,-98Q0,-112 50,-96" stroke="${c.coatL}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".55"/>`
      : `<path d="M-96,-176Q-30,-196 60,-178" stroke="${c.coatL}" stroke-width="9" fill="none" stroke-linecap="round" opacity=".5"/><path d="M-60,-110Q0,-100 50,-110" stroke="${c.coatD}" stroke-width="7" fill="none" opacity=".6"/>`;
    return `<path d="${torso}" fill="${c.coat}" ${ln(3)}/>${chest}${saddle}${ribs}${sheen}`;
  };

  const tailSvg = (id, kind, c) => kind === "dam"
    ? `<g id="${id}-tail" transform="rotate(0)"><path d="M0,0C-24,-10 -40,-36 -38,-70Q-30,-80 -24,-70C-26,-44 -14,-22 6,-12Z" fill="${c.coat}" ${ln(2.6)}/><path d="M-36,-66Q-32,-76 -26,-70" stroke="${c.tan}" stroke-width="4" fill="none"/></g>`
    : `<g id="${id}-tail" transform="rotate(0)"><path d="M0,0C-14,-6 -24,-22 -22,-42Q-16,-48 -12,-42C-14,-26 -6,-14 4,-8Z" fill="${kind === "pup" ? c.tan : c.coatD}" ${ln(2.2)}/></g>`;

  const Dog = {};
  const POS = {}, DK = {};   // where each dog stands, in build order: Dog.svg sets it, each drive moves it on (so seeking back is exact)
  Dog.svg = (o = {}) => {
    const id = o.id || "dg", kind = o.kind || "dam", c = PAL[kind], P = PLAN[kind], s = o.s ?? 1, sx = o.flip ? -s : s;
    POS[id] = [o.x ?? 540, o.y ?? 1400, sx, s]; DK[id] = kind;
    const only = o.eyesOnly ? `<style>#${id} *{fill-opacity:0;stroke-opacity:0}#${id}-glow,#${id}-glow *{fill-opacity:1;stroke-opacity:1}</style>` : "";
    const sil = o.silhouette ? ` style="filter:brightness(0)"` : "";
    return `${only}<g id="${id}"${sil} transform="translate(${f(o.x ?? 540)},${f(o.y ?? 1400)}) scale(${f(sx)},${f(s)})">
      <ellipse cx="-6" cy="2" rx="${kind === "dam" ? 150 : 82}" ry="${kind === "dam" ? 16 : 10}" fill="url(#dgShadow)"/>
      <g id="${id}-body" transform="translate(0,0) rotate(0)">
        <g transform="translate(${P.hipF[0] - 14},${P.hipF[1]})">${legSvg(id, 2, P, c, true)}</g>
        <g transform="translate(${P.hipB[0] + 14},${P.hipB[1]})">${legSvg(id, 3, P, c, true)}</g>
        <g transform="translate(${P.tail[0]},${P.tail[1]})">${tailSvg(id, kind, c)}</g>
        ${bodySvg(id, kind, c, P)}
        <g transform="translate(${P.hipF[0]},${P.hipF[1]})">${legSvg(id, 0, P, c, false)}</g>
        <g transform="translate(${P.hipB[0]},${P.hipB[1]})">${legSvg(id, 1, P, c, false)}</g>
        <g transform="translate(${P.neck[0]},${P.neck[1]}) scale(${P.headS})"><g id="${id}-head" transform="rotate(0)">${headSvg(id, kind, c, o)}</g></g>
      </g></g>`;
  };

  // ---------------- poses ----------------
  const S = Math.sin, PI = Math.PI;
  const rest = () => ({ pv: 0, dy: 0, rot: 0, legs: [[0, 0], [0, 0], [0, 0], [0, 0]], head: 0, jaw: 0, tail: 0, ear: 0, tongue: 0, lip: 0, drool: null, glow: null, dx: 0 });
  const walkLegs = (ph, a = 22, k = 30) => [0, PI, PI, 0].map((o, i) => {
    const p = ph + o + (i % 2 ? 0.6 : 0), h = a * S(p), kn = Math.max(0, S(p + PI / 2)) * k;
    return i % 2 ? [h, -kn * 0.9] : [h, kn];
  });
  const MODES = {
    idle: (u) => ({ ...rest(), dy: 1.5 * S(u * 3), head: 2 * S(u * 1.3), tail: 10 * S(u * 2.2) - 10 }),
    wag: (u) => ({ ...rest(), dy: 3 * Math.abs(S(u * 7)), head: -6 + 5 * S(u * 7), tail: 28 * S(u * 16) - 22, tongue: 1, jaw: 10 }),
    walk: (u) => ({ ...rest(), dy: 3 * Math.abs(S(u * 6)), legs: walkLegs(u * 6), head: 3 * S(u * 6), tail: 8 * S(u * 6) - 14 }),
    trot: (u) => ({ ...rest(), dy: 5 * Math.abs(S(u * 10)), legs: walkLegs(u * 10, 30, 40), head: 4 * S(u * 10), tail: 14 * S(u * 10) - 24, tongue: 1, jaw: 12 }),
    sniff: (u) => ({ ...rest(), head: 34 + 6 * S(u * 9), legs: [[-6, 6], [4, 0], [-6, 6], [4, 0]], tail: 6 * S(u * 3) - 8 }),
    lick: (u, o) => { const r = o.rate || 2.4, k = Math.max(0, S(u * r * 2 * PI)); return { ...rest(), head: 30 + 4 * k, jaw: 14 * k, tongue: k, tail: 18 * S(u * 9) - 18, legs: [[-6, 6], [4, 0], [-6, 6], [4, 0]] }; },
    growl: (u) => { const j = 1.4 * S(u * 31); return { ...rest(), head: 16 + j, rot: 3, dy: 8, lip: 1, jaw: 4 + 2 * S(u * 23), tail: -36 + j, ear: -14, legs: [[-10, 10], [8, -6], [-10, 10], [8, -6]] }; },
    bark: (u, o) => { const b = (o.beats || [0.2, 0.7, 1.1]).reduce((m, t) => Math.max(m, Math.exp(-((u - t) ** 2) / 0.006)), 0); return { ...rest(), head: -8 * b, jaw: 30 * b, lip: 0.6, dy: -4 * b, tail: -20, legs: [[-6 * b, 4], [4, 0], [-6 * b, 4], [4, 0]] }; },
    howl: (u) => ({ ...rest(), pv: 1, rot: -40, dy: 4, head: -30 + 3 * S(u * 2), jaw: 26 + 6 * S(u * 3.5), ear: -18, tail: 40, legs: [[40, 0], [-50, 120], [40, 0], [-50, 120]] }),
    sick: (u) => ({ ...rest(), head: 30 + 8 * S(u * 1.6), rot: 2 * S(u * 1.1), dy: 4 + 3 * S(u * 1.1), drool: 1, tail: -40, ear: 10, legs: [[4 * S(u * 1.1), 4], [-4 * S(u * 1.1), 0], [-4, 6], [4, 0]] }),
    cower: (u) => ({ ...rest(), dy: 34 + 2 * S(u * 9), rot: 4, head: 24, tail: -70, ear: 16, legs: [[-30, 60], [-40, 80], [-30, 60], [-40, 80]] }),
    lunge: (u) => { const k = Math.min(1, u / 0.25); return { ...rest(), dy: -18 * S(k * PI), rot: -8 * S(k * PI), head: -6, jaw: u > 0.12 && u < 0.4 ? 30 : 4, lip: 1, tail: -10, legs: walkLegs(u * 16, 40, 50) }; },
    sit: (u) => ({ ...rest(), pv: 1, rot: -40, dy: 4, head: 30 + 2 * S(u * 1.3), tail: 10 * S(u * 2) + 40, legs: [[40, 0], [-50, 120], [40, 0], [-50, 120]] }),
    lie: (u) => ({ ...rest(), dy: 70, head: 22 + 2 * S(u * 1.1), tail: -70, legs: [[-80, -10], [-60, 140], [-80, -10], [-60, 140]] }),
  };
  const lerp = (a, b, k) => a + (b - a) * k;
  const blend = (A, B, k) => ({
    pv: B.pv || A.pv, dy: lerp(A.dy, B.dy, k), rot: lerp(A.rot, B.rot, k), head: lerp(A.head, B.head, k), jaw: lerp(A.jaw, B.jaw, k), tail: lerp(A.tail, B.tail, k),
    ear: lerp(A.ear, B.ear, k), tongue: lerp(A.tongue, B.tongue, k), lip: lerp(A.lip, B.lip, k), drool: B.drool ?? A.drool, glow: B.glow ?? A.glow,
    legs: A.legs.map((l, i) => [lerp(l[0], B.legs[i][0], k), lerp(l[1], B.legs[i][1], k)]),
  });
  const last = {};   // the pose each dog ended its previous drive in (to blend into the next one)
  Dog.drive = (tl, id, t0, dur, mode, o = {}) => {
    const fn = MODES[mode] || MODES.idle;
    const root = () => document.getElementById(id);
    const base = o.at ? [o.at[0], o.at[1], o.at[2] ?? 1, o.at[3] ?? Math.abs(o.at[2] ?? 1)] : (POS[id] || [540, 1400, 1, 1]).slice();
    const fl = o.flip == null ? Math.sign(base[2]) : (o.flip ? -1 : 1);
    POS[id] = [o.to ?? base[0], o.toY ?? base[1], fl * (o.toS ?? Math.abs(base[3])), o.toS ?? Math.abs(base[3])];
    let els = null;
    const PV = (DK[id] && PLAN[DK[id]].hipF) || [0, 0];   // sit / howl turn the body about the front hip
    const prev = last[id] || rest();
    const proxy = { u: 0 };
    tl.to(proxy, {
      u: dur, duration: dur, ease: "none", immediateRender: false,
      onUpdate() {
        if (!els) {
          els = {}; ["body", "head", "jaw", "tail", "eye", "glow", "tongue", "drool", "lip", "ear"].forEach((k) => (els[k] = document.getElementById(id + "-" + k)));
          for (let i = 0; i < 4; i++) { els["l" + i] = document.getElementById(id + "-leg" + i); els["k" + i] = document.getElementById(id + "-knee" + i); }
        }
        if (!root()) return;
        const u = proxy.u, k = Math.min(1, u / (o.blend ?? 0.22));
        let P = fn(u, o); P = k < 1 ? blend(prev, P, k * k * (3 - 2 * k)) : P;
        const ez = o.ease || ((v) => v);
        const mx = o.to != null ? lerp(base[0], o.to, ez(Math.min(1, u / (o.moveDur || dur)))) : base[0];
        const my = o.toY != null ? lerp(base[1], o.toY, ez(Math.min(1, u / (o.moveDur || dur)))) : base[1];
        const ms = o.toS != null ? lerp(Math.abs(base[3]), o.toS, ez(Math.min(1, u / (o.moveDur || dur)))) : Math.abs(base[3]);
        const sx = fl * ms;
        root().setAttribute("transform", `translate(${f(mx)},${f(my)}) scale(${f(sx)},${f(ms)})`);
        els.body && els.body.setAttribute("transform", `translate(0,${f(P.dy)}) rotate(${f(P.rot)},${f(PV[0] * (P.pv || 0))},${f(PV[1] * (P.pv || 0))})`);
        els.head && els.head.setAttribute("transform", `rotate(${f(P.head)})`);
        els.jaw && els.jaw.setAttribute("transform", `rotate(${f(P.jaw)})`);
        els.tail && els.tail.setAttribute("transform", `rotate(${f(P.tail)})`);
        els.ear && els.ear.setAttribute("transform", `rotate(${f(P.ear)},30,-60)`);
        els.tongue && els.tongue.setAttribute("opacity", f(P.tongue));
        els.lip && els.lip.setAttribute("opacity", f(P.lip));
        if (P.drool != null && els.drool) els.drool.setAttribute("opacity", f(P.drool));
        const g = o.glow != null ? (o.glow ? 1 : 0) : P.glow;
        if (g != null && els.glow) { els.glow.setAttribute("opacity", f(g)); els.eye && els.eye.setAttribute("opacity", f(1 - g)); }
        for (let i = 0; i < 4; i++) { const L = P.legs[i]; els["l" + i] && els["l" + i].setAttribute("transform", `rotate(${f(L[0])})`); els["k" + i] && els["k" + i].setAttribute("transform", `rotate(${f(L[1])})`); }
      },
    }, t0);
    last[id] = fn(dur, o);
  };
  Dog.MODES = MODES;
  window.Dog = Dog;
})();
