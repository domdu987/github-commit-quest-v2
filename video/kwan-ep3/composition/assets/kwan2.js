// Sets for "ควันหลง" EP.2 ทางเดินมืด (loaded after kwan.js; EP.1's room, peephole and phone stay in kwan.js).
// The seventh-floor corridor of the old dorm at 2 a.m., lights out, smoke under the ceiling, the floor wet from the hoses:
//   Sets.escapePlan   the fire-escape plan on the back of the door: rooms 701–716, stairs at both ends, the lift, "you are here"
//   Sets.corridor     looking down the corridor (one-point perspective, vanishing at 540,900): doors both sides, the lift on the
//                     left, the red fire-alarm station on the right, the exit sign over the stairwell door at the far end;
//                     o.open (every door swung open, eyes in the dark rooms), o.smoke 0..1, o.strobe (alarm strobes), o.liftLit
//   Sets.corridorSide the corridor side on (a long wall of doors, x 0–4200): for crawling shots and for door 714 from outside
//   Sets.doorGap      your door open a hand's width: the corridor's smoke and แพร's face in the gap
//   Sets.alarmClose   the fire-alarm pull station, close (#id-lever, strobe)
//   Sets.handsClose   your hand on the floor in the torch light and the hand that holds it (#id-other: dark; #id-burnt: ดาว's)
//   Sets.liftOpen     the lift: doors slide apart (#id-dl, #id-dr), warm light floods out, ดาว standing inside (#id-dao)
// Also Kwan.daoStand (ดาว standing, same burnt look as EP.1's daoSit), Rig.CAST.prae (แพร) and card icons for EP.2.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const LAVA = "#ff6a1a", CH = "#1b1512";

  Sets.DEFS += `
    <linearGradient id="k2Wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4442"/><stop offset=".6" stop-color="#323b39"/><stop offset="1" stop-color="#262d2c"/></linearGradient>
    <linearGradient id="k2Floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e2a26"/><stop offset="1" stop-color="#46403a"/></linearGradient>
    <linearGradient id="k2Door" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a3e2a"/><stop offset="1" stop-color="#432d1e"/></linearGradient>
    <radialGradient id="k2Exit"><stop offset="0" stop-color="#7affa8" stop-opacity=".75"/><stop offset=".4" stop-color="#3fd07a" stop-opacity=".25"/><stop offset="1" stop-color="#3fd07a" stop-opacity="0"/></radialGradient>
    <radialGradient id="k2Red"><stop offset="0" stop-color="#ff4a3a" stop-opacity=".85"/><stop offset=".45" stop-color="#ff2a1a" stop-opacity=".3"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="k2Warm"><stop offset="0" stop-color="#fff6dc" stop-opacity=".95"/><stop offset=".5" stop-color="#ffe2a8" stop-opacity=".45"/><stop offset="1" stop-color="#ffd38a" stop-opacity="0"/></radialGradient>
    <linearGradient id="k2Steel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a9096"/><stop offset=".5" stop-color="#b8bec4"/><stop offset="1" stop-color="#7a8086"/></linearGradient>
    <linearGradient id="k2Wet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ec3ff" stop-opacity=".0"/><stop offset=".5" stop-color="#9ec3ff" stop-opacity=".18"/><stop offset="1" stop-color="#9ec3ff" stop-opacity="0"/></linearGradient>
    <linearGradient id="k2Plan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2ecd8"/><stop offset="1" stop-color="#d8cca8"/></linearGradient>`;

  // ---------------- people ----------------
  // ดาว standing (the same burnt girl as EP.1's daoSit): charcoal skin cracked like cooling embers (class flk glows),
  // ember slits for eyes, a glowing split for a mouth (#id-smile turns it up), frizzled smoking hair, the scorched student
  // blouse and dark skirt, the 714 name tag. Origin at the feet, ~760 px tall at s = 1. Parts: #id-head, #id-armR (raises)
  function daoStand(id, o = {}) {
    const crack = (d, w = 3.5) => `<path class="flk" d="${d}" stroke="${LAVA}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>`;
    const frizz = [-50, -36, -22, -8, 6, 20, 34, 48].map((x, k) => `<path d="M${x},-52q${k % 2 ? 8 : -8},-16 ${k % 2 ? -2 : 4},-30q${k % 2 ? -6 : 6},-10 ${k % 2 ? 4 : -2},-20" stroke="#120d0b" stroke-width="9" fill="none" stroke-linecap="round"/>`).join("");
    const RIM = `stroke="#3a2a22" stroke-width="3" stroke-linejoin="round"`;
    const arm = (sx, extra = "") => `<path d="M0,0C${sx * 10},90 ${sx * 14},170 ${sx * 10},250" stroke="${CH}" stroke-width="20" fill="none" stroke-linecap="round"/>${crack(`M${sx * 4},50l${sx * 8},24l${sx * -4},22M${sx * 10},170l${sx * 4},26`, 3)}
        ${[-6, 3, 12, 20].map((dx, k) => `<path d="M${sx * 10 + dx * 0.4},252l${dx * 0.3},${46 + (k % 2) * 8}" stroke="${CH}" stroke-width="7" stroke-linecap="round"/>`).join("")}${extra}`;
    return `<g id="${id}" transform="translate(${o.x || 0},${o.y || 0}) scale(${o.s || 1})">
      <ellipse cx="0" cy="6" rx="80" ry="14" fill="#000" opacity=".5"/>
      <path d="M-22,-250L-26,-10M22,-250L26,-10" stroke="${CH}" stroke-width="26" stroke-linecap="round"/>${crack("M-24,-160l6,20l-4,18M24,-120l-6,18", 3)}
      <path d="M-36,-14h22v14h-28zM14,-14h22l6,14h-28z" fill="#0f0b09"/>
      <path d="M-70,-250L-58,-420H58L70,-250Z" fill="#1e1a24" ${RIM}/><path d="M-60,-300L-30,-262M40,-330L60,-290" stroke="#2c2632" stroke-width="5"/>
      <path d="M-58,-420C-64,-500 -56,-570 -40,-630C-30,-660 30,-662 42,-632C58,-570 64,-500 58,-420Z" fill="#cfc8b8" ${RIM}/>
      <path d="M-58,-440C-46,-500 -16,-470 -10,-530C-4,-580 34,-560 46,-610L52,-520C36,-500 16,-470 -6,-450Z" fill="#2a221d"/>
      ${[[-30, -560, 16], [26, -470, 20], [-14, -600, 12], [34, -590, 10]].map(([x, y, r]) => `<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${r * 0.8}" fill="${CH}"/><ellipse cx="${x}" cy="${y}" rx="${r * 0.55}" ry="${r * 0.4}" fill="${LAVA}" opacity=".5" class="flk"/>`).join("")}
      <path d="M-34,-630Q0,-606 34,-630L26,-616Q0,-598 -26,-616Z" fill="#2a221d"/><rect x="-16" y="-598" width="32" height="15" rx="2" fill="#8a8478" opacity=".6"/><text x="0" y="-586" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="11" fill="#1a1612">714</text>
      <g transform="translate(-56,-600)">${arm(-1)}</g><g id="${id}-armR" transform="translate(56,-600) rotate(0)">${arm(1)}</g>
      <g id="${id}-head" transform="translate(0,-660) rotate(0)">
        <path d="M-14,40V20M14,40V20" stroke="${CH}" stroke-width="16"/>
        <ellipse cx="0" cy="-4" rx="50" ry="58" fill="${CH}" ${RIM}/>${frizz}
        ${crack("M-40,-30l14,10l-6,16l12,12M30,-40l-8,16l10,10M-6,30l6,12l-8,8M40,10l-10,4", 3)}
        <g><path d="M-30,-6Q-18,-14 -6,-6Q-18,0 -30,-6Z" fill="#ffd27a"/><path d="M8,-4Q20,-12 32,-4Q20,2 8,-4Z" fill="#ffd27a"/>
          <ellipse cx="-18" cy="-6" rx="20" ry="11" fill="${LAVA}" opacity=".35"/><ellipse cx="20" cy="-4" rx="20" ry="11" fill="${LAVA}" opacity=".35"/></g>
        <g id="${id}-flat">${crack("M-18,24l6,-4l6,6l6,-6l6,4l6,-4", 4)}</g>
        <g id="${id}-smile" opacity="0">${crack("M-24,18Q0,40 26,16", 4.5)}</g>
        <g class="smk" data-d="6">${[0, 1, 2].map((k) => `<path d="M${-30 + k * 26},-80C${-40 + k * 26},-120 ${-10 + k * 26},-150 ${-24 + k * 26},-200" stroke="#5a5550" stroke-width="${8 - k * 2}" fill="none" opacity="${0.45 - k * 0.1}" stroke-linecap="round"/>`).join("")}</g></g></g>`;
  }
  // แพร (19), your roommate: mint pyjamas, long dark hair tied low, a cloth pressed over her mouth
  if (window.Rig) Rig.CAST.prae = {
    skin: "#e8b98f", skinS: "#c8946c", top: "#7fb3a0", topS: "#5f9482", sleeve: "#7fb3a0", sleeveS: "#5f9482", forearm: "#7fb3a0", forearmS: "#5f9482",
    pants: "#7fb3a0", pantsS: "#5f9482", shoe: "#e8b98f", belt: "#5f9482",
    torsoExtra: `<path d="M-30,-484L0,-456L30,-484" fill="#a8d4c2" ${OUT3}/>${[[-30, -430], [24, -400], [-22, -360], [32, -340]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="5" fill="#f2efe6" opacity=".8"/>`).join("")}`,
    hair: `<path d="M-50,-540Q-58,-610 0,-612Q58,-610 50,-540Q48,-520 40,-512Q36,-566 2,-576Q-34,-566 -40,-512Q-50,-520 -50,-540Z" fill="#1f1816" ${OUT3}/>
      <path d="M40,-540Q70,-500 56,-430Q48,-400 60,-370" stroke="#1f1816" stroke-width="20" fill="none" stroke-linecap="round"/><circle cx="46" cy="-528" r="7" fill="#e07a8a"/>`,
    face: `<path d="M-30,-530H34V-506Q2,-492 -30,-506Z" fill="#f2efe6" ${OUT3}/><path d="M-24,-520h50M-24,-512h48" stroke="#cfc8b8" stroke-width="3"/>`,
  };

  // ---------------- the fire-escape plan ----------------
  Sets.escapePlan = function (L, o) {
    const id = o.id || "ep";
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#2a2016"/>`);
    let s = `<rect x="-600" y="-400" width="2300" height="2800" fill="url(#kwWoodV)"/>`;
    for (let k = 0; k < 12; k++) s += `<path d="M${-600 + k * 200},-400V2400" stroke="#3e2a1c" stroke-width="5" opacity=".5"/>`;
    s += `<g transform="translate(90,420)"><rect x="-10" y="-10" width="920" height="1120" fill="#000" opacity=".3"/><rect width="900" height="1100" fill="url(#k2Plan)" ${OUT}/>
      <rect x="0" y="0" width="900" height="120" fill="#2f8a52"/><text x="450" y="80" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="56" fill="#fff">แผนผังหนีไฟ · ชั้น 7</text>`;
    // the corridor down the middle, rooms both sides, stairs at both ends, the lift
    s += `<rect x="90" y="520" width="720" height="110" fill="#e9e2c8" stroke="#3a3a3a" stroke-width="5"/>`;
    for (let k = 0; k < 8; k++) {
      const x = 90 + k * 90;
      s += `<rect x="${x}" y="300" width="90" height="220" fill="#f6f1de" stroke="#3a3a3a" stroke-width="4"/><text x="${x + 45}" y="420" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="24" fill="#3a3a3a">${701 + k * 2}</text>`;
      const n = 702 + k * 2, me = n === 714;
      s += `<rect x="${x}" y="630" width="90" height="220" fill="${me ? "#ffe2a0" : "#f6f1de"}" stroke="#3a3a3a" stroke-width="4"/><text x="${x + 45}" y="740" text-anchor="middle" font-family="Kanit" font-weight="${me ? 900 : 700}" font-size="24" fill="${me ? "#c8392b" : "#3a3a3a"}">${n}</text>`;
    }
    s += `<rect x="20" y="480" width="70" height="190" fill="#3fd07a" stroke="#2a6a42" stroke-width="4"/><text x="55" y="590" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="20" fill="#fff" transform="rotate(-90 55 575)">บันได</text>
      <rect x="810" y="480" width="70" height="190" fill="#3fd07a" stroke="#2a6a42" stroke-width="4"/><text x="845" y="590" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="20" fill="#fff" transform="rotate(90 845 575)">บันได</text>
      <rect x="400" y="250" width="100" height="50" fill="#b8bec4" stroke="#3a3a3a" stroke-width="4"/><text x="450" y="284" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="#3a3a3a">ลิฟต์</text>
      <g id="${id}-route"><path d="M630,575H110" stroke="#2f8a52" stroke-width="12" stroke-dasharray="26 18" fill="none"/><path d="M130,555L100,575L130,595" stroke="#2f8a52" stroke-width="12" fill="none" stroke-linejoin="round"/>
        <path d="M640,575H790" stroke="#2f8a52" stroke-width="12" stroke-dasharray="26 18" fill="none"/><path d="M770,555L800,575L770,595" stroke="#2f8a52" stroke-width="12" fill="none" stroke-linejoin="round"/></g>
      <g id="${id}-here"><circle cx="585" cy="700" r="34" fill="#e0362c" opacity=".35"/><circle cx="585" cy="700" r="18" fill="#e0362c" ${OUT3}/></g>
      <rect x="430" y="900" width="420" height="80" rx="12" fill="#e0362c"/><text x="640" y="954" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#fff">● คุณอยู่ที่นี่</text>
      <text x="60" y="1060" font-family="Kanit" font-weight="700" font-size="30" fill="#5a5040">เกิดเพลิงไหม้ ใช้บันได ห้ามใช้ลิฟต์</text>
      <path d="M440,240L460,200" stroke="#c8392b" stroke-width="6"/><path d="M430,232q40,-20 60,6" stroke="#c8392b" stroke-width="5" fill="none" opacity=".0"/></g>`;
    put(L.set, s);
  };

  // ---------------- the corridor (one-point perspective) ----------------
  const VX = 540, VY = 900, HW = 640, FL = 860, CE = 760, DH = 1220;
  const xl = (z) => VX - HW / z, xr = (z) => VX + HW / z, yf = (z) => VY + FL / z, yc = (z) => VY - CE / z;
  // one door on a side wall between depths z1 < z2: its frame quad, and the leaf (opacity tweened to open it)
  function doorQuad(side, z1, z2, h = DH) {
    const x1 = side < 0 ? xl(z1) : xr(z1), x2 = side < 0 ? xl(z2) : xr(z2);
    return [[x1, yf(z1)], [x2, yf(z2)], [x2, yf(z2) - h / z2], [x1, yf(z1) - h / z1]];
  }
  const poly = (q) => q.map((p) => `${f1(p[0])},${f1(p[1])}`).join(" ");
  const lerp2 = (a, b, k) => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k];
  Sets.corridor = function (L, o) {
    const id = o.id || "cd", r = mk(o.seed || 7), Z = 9.5;
    put(L.sky, `<rect x="-1500" y="-1500" width="4100" height="5000" fill="#0b0d0d"/>`);
    let s = "";
    // ceiling, floor, walls, the end wall
    s += `<polygon points="${poly([[xl(1) - 900, yc(1) - 600], [xr(1) + 900, yc(1) - 600], [xr(Z), yc(Z)], [xl(Z), yc(Z)]])}" fill="#1c2120"/>`;
    s += `<polygon points="${poly([[xl(1) - 900, yf(1) + 900], [xr(1) + 900, yf(1) + 900], [xr(Z), yf(Z)], [xl(Z), yf(Z)]])}" fill="url(#k2Floor)"/>`;
    s += `<polygon points="${poly([[xl(1) - 900, yc(1) - 600], [xl(Z), yc(Z)], [xl(Z), yf(Z)], [xl(1) - 900, yf(1) + 900]])}" fill="url(#k2Wall)"/>`;
    s += `<polygon points="${poly([[xr(1) + 900, yc(1) - 600], [xr(Z), yc(Z)], [xr(Z), yf(Z)], [xr(1) + 900, yf(1) + 900]])}" fill="url(#k2Wall)"/>`;
    s += `<rect x="${f1(xl(Z))}" y="${f1(yc(Z))}" width="${f1(xr(Z) - xl(Z))}" height="${f1(yf(Z) - yc(Z))}" fill="#2a3230"/>`;
    // floor tiles converging, the wet sheen of the hoses, skirting lines
    for (let k = -8; k <= 8; k++) s += `<path d="M${VX + k * 30 / Z * 9},${f1(yf(Z))}L${VX + k * 260},${yf(1) + 900}" stroke="#25211d" stroke-width="3" opacity=".7"/>`;
    for (let z = 1.2; z < Z; z *= 1.32) s += `<path d="M${f1(xl(z))},${f1(yf(z))}H${f1(xr(z))}" stroke="#25211d" stroke-width="${f1(4 / Math.sqrt(z))}" opacity=".7"/>`;
    s += `<polygon points="${poly([[VX - 180, yf(1.3)], [VX + 220, yf(1.3)], [VX + 30, yf(6)], [VX - 10, yf(6)]])}" fill="url(#k2Wet)"/>`;
    [-1, 1].forEach((sd) => (s += `<polygon points="${poly([[sd < 0 ? xl(1) - 900 : xr(1) + 900, yf(1) + 900 - 60], [sd < 0 ? xl(Z) : xr(Z), yf(Z) - 60 / Z], [sd < 0 ? xl(Z) : xr(Z), yf(Z)], [sd < 0 ? xl(1) - 900 : xr(1) + 900, yf(1) + 900]])}" fill="#1e2423"/>`));
    // dead tube lights on the ceiling
    for (let z = 1.5; z < Z; z *= 1.45) s += `<rect x="${f1(VX - 120 / z)}" y="${f1(yc(z) + 10 / z)}" width="${f1(240 / z)}" height="${f1(22 / z)}" rx="${f1(8 / z)}" fill="#4a5250" opacity=".8"/>`;
    // doors: odd numbers on the left, even on the right; 714 is the near right one
    const D = [[1.15, 1.75], [2.1, 2.7], [3.2, 3.75], [4.6, 5.2], [6.4, 7.0], [8.2, 8.8]];
    const nums = { "-1": [703, 705, 707, 709, 711, 713], "1": [714, 712, 710, 708, 706, 704] };
    let leaves = "", eyes = "";
    [-1, 1].forEach((sd) => D.forEach(([z1, z2], k) => {
      if (sd < 0 && k === 3) return; // the lift sits there
      const q = doorQuad(sd, z1, z2), num = nums[sd][k];
      s += `<polygon points="${poly(q)}" fill="#050505"/>`; // the dark room behind the door
      // eyes in the dark room (shown when the doors swing open)
      const c = lerp2(lerp2(q[0], q[1], 0.5), lerp2(q[3], q[2], 0.5), 0.62), sc = 1 / ((z1 + z2) / 2);
      eyes += `<g class="flk" opacity=".95"><circle cx="${f1(c[0])}" cy="${f1(c[1])}" r="${f1(70 * sc * 2)}" fill="${LAVA}" opacity=".12"/><ellipse cx="${f1(c[0] - 14 * sc * 2)}" cy="${f1(c[1])}" rx="${f1(16 * sc * 2)}" ry="${f1(6 * sc * 2)}" fill="${LAVA}" opacity=".35"/><ellipse cx="${f1(c[0] + 14 * sc * 2)}" cy="${f1(c[1] + 2 * sc)}" rx="${f1(16 * sc * 2)}" ry="${f1(6 * sc * 2)}" fill="${LAVA}" opacity=".35"/>
        <path d="M${f1(c[0] - 22 * sc * 2)},${f1(c[1])}q${f1(8 * sc * 2)},${f1(-5 * sc * 2)} ${f1(16 * sc * 2)},0M${f1(c[0] + 6 * sc * 2)},${f1(c[1] + 2 * sc)}q${f1(8 * sc * 2)},${f1(-5 * sc * 2)} ${f1(16 * sc * 2)},0" stroke="#ffd27a" stroke-width="${f1(Math.max(2, 5 * sc * 2))}" stroke-linecap="round"/></g>`;
      const plate = lerp2(q[3], q[2], 0.5);
      leaves += `<g class="leaf" id="${id}-door${num}"><polygon points="${poly(q)}" fill="url(#k2Door)" ${OUT3}/>
        <polygon points="${poly([lerp2(q[0], q[1], 0.12), lerp2(q[0], q[1], 0.88), lerp2(q[3], q[2], 0.88), lerp2(q[3], q[2], 0.12)].map((p, j) => [p[0], p[1] + (j > 1 ? 30 / ((z1 + z2) / 2) : -20 / ((z1 + z2) / 2))]))}" fill="none" stroke="#3a2618" stroke-width="${f1(4 / Math.sqrt(z1))}"/>
        <rect x="${f1(plate[0] - 26 / z1)}" y="${f1(plate[1] + 70 / z1)}" width="${f1(52 / z1)}" height="${f1(24 / z1)}" fill="#c9a24a" opacity=".85"/><text x="${f1(plate[0])}" y="${f1(plate[1] + 89 / z1)}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${f1(20 / z1)}" fill="#2a1e10">${num}</text>
        <circle cx="${f1(lerp2(q[0], q[1], sd < 0 ? 0.85 : 0.15)[0])}" cy="${f1(yf((z1 + z2) / 2) - 600 / ((z1 + z2) / 2))}" r="${f1(14 / z1)}" fill="#c9a24a"/></g>`;
    }));
    // the lift on the left wall
    const lq = doorQuad(-1, 4.5, 5.3, 1150);
    s += `<polygon points="${poly(lq)}" fill="#1a1d20"/><g id="${id}-lift"><polygon points="${poly([lq[0], lerp2(lq[0], lq[1], 0.5), lerp2(lq[3], lq[2], 0.5), lq[3]])}" fill="url(#k2Steel)" ${OUT3}/>
      <polygon points="${poly([lerp2(lq[0], lq[1], 0.5), lq[1], lq[2], lerp2(lq[3], lq[2], 0.5)])}" fill="url(#k2Steel)" ${OUT3}/></g>
      <rect x="${f1(lerp2(lq[3], lq[2], 0.5)[0] - 22)}" y="${f1(lerp2(lq[3], lq[2], 0.5)[1] - 50)}" width="44" height="30" fill="#140a08"/><text id="${id}-floor" x="${f1(lerp2(lq[3], lq[2], 0.5)[0])}" y="${f1(lerp2(lq[3], lq[2], 0.5)[1] - 26)}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="24" fill="#ff5a3a">7</text>`;
    // the fire-alarm station on the right wall, near
    const ax = xr(1.9) - 6, ay = yf(1.9) - 640 / 1.9;
    s += `<g id="${id}-alarmbox"><rect x="${f1(ax - 30)}" y="${f1(ay - 40)}" width="60" height="80" rx="6" fill="#c8261c" ${OUT3}/><rect x="${f1(ax - 18)}" y="${f1(ay - 14)}" width="36" height="22" rx="3" fill="#f2efe6"/><circle cx="${f1(ax)}" cy="${f1(ay - 70)}" r="14" fill="#c8261c" ${OUT3}/></g>`;
    // the stairwell door at the far end under the exit sign
    s += `<rect x="${f1(VX - 70)}" y="${f1(yf(Z) - DH / Z)}" width="140" height="${f1(DH / Z)}" fill="#3a4a42" ${OUT3}/><rect x="${f1(VX - 50)}" y="${f1(yf(Z) - DH / Z + 20)}" width="40" height="50" fill="#7a9a8a" opacity=".6"/>
      <rect x="${f1(VX - 64)}" y="${f1(yf(Z) - DH / Z - 54)}" width="128" height="40" rx="5" fill="#2f8a52" ${OUT3}/><text x="${f1(VX)}" y="${f1(yf(Z) - DH / Z - 26)}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="#eaffe8">ทางหนีไฟ</text>`;
    put(L.set, s + `<g id="${id}-leaves" opacity="${o.open ? 0 : 1}">${leaves}</g>`);
    put(L.glow, `<g id="${id}-eyes" opacity="${o.open ? 1 : 0}">${eyes}</g>`);
    // light: the exit sign's green, the alarm strobes, the warm lift when it is lit, smoke under the ceiling
    let g = `<circle cx="${VX}" cy="${f1(yf(Z) - DH / Z - 34)}" r="260" fill="url(#k2Exit)"/>`;
    g += `<g class="strobe" opacity="${o.strobe ? 1 : 0}"><circle cx="${f1(ax)}" cy="${f1(ay - 70)}" r="520" fill="url(#k2Red)"/><circle cx="${f1(xl(3.5))}" cy="${f1(yc(3.5) + 40)}" r="380" fill="url(#k2Red)"/><circle cx="${f1(xr(6))}" cy="${f1(yc(6) + 30)}" r="260" fill="url(#k2Red)"/></g>`;
    if (o.liftLit) g += `<polygon points="${poly(lq)}" fill="#fff4d8" opacity=".9"/><circle cx="${f1((lq[0][0] + lq[1][0]) / 2)}" cy="${f1((lq[0][1] + lq[3][1]) / 2)}" r="500" fill="url(#k2Warm)"/>`;
    put(L.glow, g);
    const sm = o.smoke ?? 0.5;
    put(L.set, Pov.smoke(r, { x0: -800, x1: 1900, y0: -900, y1: 300 + 500 * sm, n: 18, op: 0.85 }) + Pov.embers(r, { n: 10, y0: 200, y1: 1100 }));
  };

  // ---------------- the corridor side on ----------------
  // a long wall of doors x 0–4200 (714 at x 600–1000), floor below y 1520, smoke ceiling (o.smokeY), the exit sign at x 3900
  // #id-d714 is door 714's leaf (attr transform to swing it; the knob #id-k714); o.ajar leaves it open on the dark room
  Sets.corridorSide = function (L, o) {
    const id = o.id || "cs", r = mk(o.seed || 9), FLOOR = 1520, CEIL = 420;
    put(L.sky, `<rect x="-1500" y="-1500" width="7500" height="5000" fill="#0b0d0d"/>`);
    let s = `<rect x="-800" y="${CEIL}" width="5800" height="${FLOOR - CEIL}" fill="url(#k2Wall)"/><rect x="-800" y="-900" width="5800" height="${CEIL + 900}" fill="#1c2120"/>
      <rect x="-800" y="${FLOOR}" width="5800" height="1400" fill="url(#k2Floor)"/><rect x="-800" y="${FLOOR - 36}" width="5800" height="36" fill="#1e2423"/>`;
    for (let x = -800; x < 5000; x += 180) s += `<path d="M${x},${FLOOR}L${x + (x - 2000) * 0.6},${FLOOR + 1400}" stroke="#25211d" stroke-width="3" opacity=".7"/>`;
    for (let k = 1; k < 8; k++) s += `<path d="M-800,${f1(FLOOR + Math.pow(k / 8, 1.6) * 1400)}H5000" stroke="#25211d" stroke-width="3" opacity=".6"/>`;
    for (let k = 0; k < 6; k++) s += `<ellipse cx="${f1(-200 + k * 900 + r() * 200)}" cy="${f1(FLOOR + 160 + r() * 300)}" rx="${f1(260 + r() * 200)}" ry="${f1(26 + r() * 20)}" fill="#9ec3ff" opacity=".12"/>`;
    const doors = [[-500, 715], [600, 714], [1700, 713], [2800, 712]];
    doors.forEach(([x, n]) => {
      s += `<rect x="${x - 20}" y="${FLOOR - 1000}" width="440" height="1000" fill="#1f1712" ${OUT}/><rect x="${x}" y="${FLOOR - 980}" width="400" height="980" fill="#050505"/>`;
      s += `<g id="${id}-d${n}" transform="translate(0,0)"><rect x="${x}" y="${FLOOR - 980}" width="400" height="980" fill="url(#k2Door)" ${OUT}/><rect x="${x + 40}" y="${FLOOR - 920}" width="320" height="380" fill="none" stroke="#3a2618" stroke-width="6"/><rect x="${x + 40}" y="${FLOOR - 480}" width="320" height="400" fill="none" stroke="#3a2618" stroke-width="6"/>
        <rect x="${x + 150}" y="${FLOOR - 860}" width="100" height="44" rx="4" fill="#c9a24a" ${OUT3}/><text x="${x + 200}" y="${FLOOR - 826}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#2a1e10">${n}</text>
        <circle id="${id}-k${n}" cx="${x + 350}" cy="${FLOOR - 470}" r="22" fill="#c9a24a" ${OUT3}/></g>`;
    });
    // the exit sign and the stairwell door at the far right; the alarm station between the doors
    s += `<rect x="3700" y="${FLOOR - 1000}" width="420" height="1000" fill="#3a4a42" ${OUT}/><rect x="3740" y="${FLOOR - 940}" width="140" height="180" fill="#7a9a8a" opacity=".5"/>
      <rect x="3720" y="${FLOOR - 1130}" width="380" height="110" rx="12" fill="#2f8a52" ${OUT}/><text x="3910" y="${FLOOR - 1056}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#eaffe8">ทางหนีไฟ</text>
      <g transform="translate(1350,${FLOOR - 700})"><rect x="-40" y="-55" width="80" height="110" rx="8" fill="#c8261c" ${OUT3}/><rect x="-24" y="-20" width="48" height="30" rx="4" fill="#f2efe6"/></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="3910" cy="${FLOOR - 1075}" r="700" fill="url(#k2Exit)"/><g class="strobe" opacity="${o.strobe ? 1 : 0}"><circle cx="1350" cy="${FLOOR - 800}" r="900" fill="url(#k2Red)"/></g>`);
    put(L.set, Pov.smoke(r, { x0: -900, x1: 5200, y0: -900, y1: o.smokeY ?? 760, n: 30, op: 0.9 }));
  };

  // ---------------- through the gap: แพร in the smoky corridor ----------------
  Sets.doorGap = function (L, o) {
    const id = o.id || "dg", r = mk(o.seed || 21);
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#070808"/>`);
    put(L.set, `<rect x="330" y="-200" width="420" height="2400" fill="#1d2120"/>${Pov.smoke(r, { x0: 300, x1: 800, y0: -200, y1: 1100, n: 8, op: 0.9 })}
      <g transform="translate(560,980) scale(1.25)" id="${id}-prae">${Kwan.praeFace(`${id}-pf`)}</g>`);
    put(L.fg, `<rect x="-600" y="-400" width="960" height="2800" fill="url(#k2Door)"/><rect x="330" y="-400" width="40" height="2800" fill="#2a1d14"/>
      <rect x="760" y="-400" width="900" height="2800" fill="#2f3a38"/><rect x="740" y="-400" width="40" height="2800" fill="#1f1712"/>`);
    put(L.glow, `<ellipse cx="560" cy="980" rx="260" ry="360" fill="url(#pvPoolLit)" opacity=".9"/>`);
  };

  // ---------------- the fire-alarm station, close ----------------
  Sets.alarmClose = function (L, o) {
    const id = o.id || "ac", r = mk(o.seed || 31);
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#262d2c"/>`);
    let s = `<rect x="-600" y="-400" width="2300" height="2800" fill="url(#k2Wall)"/>`;
    for (let k = 0; k < 14; k++) s += `<path d="M-600,${-300 + k * 200}H1700" stroke="#2c3433" stroke-width="4"/>`;
    s += `<g transform="translate(540,900)"><rect x="-240" y="-330" width="480" height="660" rx="40" fill="#c8261c" ${OUT}/><rect x="-200" y="-290" width="400" height="120" rx="14" fill="#a01a12"/>
      <text x="0" y="-210" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="62" fill="#fff">ไฟไหม้</text>
      <rect x="-150" y="-120" width="300" height="230" rx="20" fill="#f2efe6" ${OUT}/><text x="0" y="-60" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#c8261c">ดึงลง</text>
      <g id="${id}-lever" transform="translate(0,0)"><rect x="-100" y="-30" width="200" height="70" rx="16" fill="#c8261c" ${OUT}/><path d="M-60,5H60" stroke="#fff" stroke-width="10" stroke-linecap="round"/></g>
      <path d="M-40,180L0,230L40,180" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      <g transform="translate(540,350)"><rect x="-90" y="-60" width="180" height="120" rx="20" fill="#d8d0c0" ${OUT}/><circle id="${id}-strobe" cx="0" cy="0" r="44" fill="#ff5a4a" opacity=".35"/></g>`;
    put(L.set, s + Pov.smoke(r, { x0: -800, x1: 1900, y0: -900, y1: 120, n: 10, op: 0.8 }));
    put(L.glow, `<g class="strobe" opacity="${o.strobe ? 1 : 0}"><circle cx="540" cy="350" r="900" fill="url(#k2Red)"/></g>`);
  };

  // ---------------- hands on the floor ----------------
  // your hand (blue sleeve) in the torch light and the hand that holds it: #id-other (a dark shape reaching out of the
  // black) and #id-burnt (ดาว's: charcoal, glowing cracks, smoke), opacity 0 until revealed
  Sets.handsClose = function (L, o) {
    const id = o.id || "hc", r = mk(o.seed || 41);
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#060707"/>`);
    let s = `<rect x="-600" y="-400" width="2300" height="2800" fill="url(#k2Floor)"/>`;
    for (let k = 0; k < 12; k++) s += `<path d="M${-600 + k * 220},-400L${-900 + k * 300},2400" stroke="#25211d" stroke-width="5" opacity=".6"/>`;
    for (let k = 0; k < 5; k++) s += `<ellipse cx="${f1(200 + r() * 700)}" cy="${f1(700 + r() * 900)}" rx="${f1(160 + r() * 200)}" ry="${f1(30 + r() * 30)}" fill="#9ec3ff" opacity=".12"/>`;
    const fingers = (col, w = 30) => [[-46, -64, -70], [-16, -84, -90], [16, -82, -88], [44, -66, -70]].map(([x, y, l]) => `<path d="M${x},${y + 30}q${x * 0.1},${l * 0.5} ${x * 0.15},${l}" stroke="${INK}" stroke-width="${w + 8}" stroke-linecap="round" fill="none"/><path d="M${x},${y + 30}q${x * 0.1},${l * 0.5} ${x * 0.15},${l}" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`).join("");
    // your hand from the bottom left, palm down, reaching up-right
    s += `<g transform="translate(470,1150) rotate(30)"><path d="M0,120L0,900" stroke="${INK}" stroke-width="190" stroke-linecap="round"/><path d="M0,120L0,900" stroke="#5d6f8f" stroke-width="178" stroke-linecap="round"/>
        <rect x="-96" y="140" width="192" height="60" fill="#7f91b2" ${OUT}/><ellipse cx="0" cy="40" rx="80" ry="96" fill="#ecc19a" ${OUT}/>${fingers("#ecc19a")}</g>`;
    // the other hand comes down from the top right and closes over yours
    const other = (col, extra) => `<g transform="translate(640,880) rotate(200)"><path d="M0,120L0,1000" stroke="${INK}" stroke-width="170" stroke-linecap="round"/><path d="M0,120L0,1000" stroke="${col}" stroke-width="158" stroke-linecap="round"/>
        <ellipse cx="0" cy="40" rx="76" ry="92" fill="${col}" ${OUT}/>${fingers(col, 26)}${extra || ""}</g>`;
    s += `<g id="${id}-other" opacity="0">${other("#151413")}</g>`;
    s += `<g id="${id}-burnt" opacity="0">${other(CH, `<path class="flk" d="M-40,0l20,30l-10,40l24,30M30,-20l-14,40l20,30M-10,300l20,60l-14,50M20,500l-16,60" stroke="${LAVA}" stroke-width="7" fill="none" stroke-linecap="round" opacity=".9"/>
        <ellipse cx="10" cy="260" rx="40" ry="26" fill="${LAVA}" opacity=".45" class="flk"/><g class="smk" data-d="6"><path d="M-20,400C-60,460 0,520 -40,600" stroke="#5a5550" stroke-width="10" fill="none" opacity=".4"/></g>`)}</g>`;
    put(L.set, s);
  };

  // ---------------- the lift ----------------
  Sets.liftOpen = function (L, o) {
    const id = o.id || "lo", r = mk(o.seed || 51);
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#0b0d0d"/>`);
    let s = `<rect x="-600" y="-400" width="2300" height="2800" fill="url(#k2Wall)"/><rect x="-600" y="1560" width="2300" height="900" fill="url(#k2Floor)"/>`;
    // inside the car: warm light, steel walls, a handrail, a mirror; ดาว standing in it
    s += `<rect x="190" y="480" width="700" height="1080" fill="#f6e6c0"/><polygon points="190,480 300,560 300,1480 190,1560" fill="#d8c49a"/><polygon points="890,480 780,560 780,1480 890,1560" fill="#d8c49a"/>
      <rect x="300" y="560" width="480" height="920" fill="#efdcb2"/><path d="M300,1120H780" stroke="#b8a070" stroke-width="12"/><rect x="380" y="620" width="320" height="380" fill="#cfd8dc" opacity=".55"/>
      <rect x="300" y="1480" width="480" height="80" fill="#c8b48a"/>`;
    s += Kwan.daoStand(`${id}-dao`, { x: 540, y: 1470, s: 1.05 });
    // the doors (slide apart), the frame, the floor indicator and the call buttons
    s += `<g id="${id}-dl" transform="translate(0,0)"><rect x="190" y="480" width="350" height="1080" fill="url(#k2Steel)" ${OUT}/><path d="M220,520V1520" stroke="#a8aeb4" stroke-width="6"/></g>
      <g id="${id}-dr" transform="translate(0,0)"><rect x="540" y="480" width="350" height="1080" fill="url(#k2Steel)" ${OUT}/><path d="M860,520V1520" stroke="#a8aeb4" stroke-width="6"/></g>
      <path d="M150,1560V440H930V1560" fill="none" stroke="#5a6064" stroke-width="40"/><rect x="430" y="300" width="220" height="100" rx="12" fill="#140a08" ${OUT3}/>
      <text x="540" y="372" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="72" fill="#ff5a3a">▼7</text>
      <rect x="980" y="900" width="70" height="170" rx="12" fill="#8a9096" ${OUT3}/><circle cx="1015" cy="950" r="20" fill="#3a3e42"/><circle id="${id}-btn" cx="1015" cy="1020" r="20" fill="#ffd27a"/>`;
    put(L.set, s + Pov.smoke(r, { x0: -800, x1: 1900, y0: -900, y1: 360, n: 10, op: 0.85 }));
    put(L.glow, `<g id="${id}-light" opacity="${o.lit ?? 0}"><rect x="190" y="480" width="700" height="1080" fill="#fff6dc" opacity=".08"/><circle cx="540" cy="1100" r="760" fill="url(#k2Warm)" opacity=".55"/>
      <polygon points="190,1560 890,1560 1300,2400 -220,2400" fill="#fff0c8" opacity=".22"/></g>`);
  };

  // ---------------- card icons for EP.2 ----------------
  if (window.GameUI) {
    const K = INK, O = `stroke="${K}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"`;
    Object.assign(GameUI.ILL, {
      doorslow: `<ellipse cx="60" cy="108" rx="34" ry="6" fill="#000" opacity=".18"/><rect x="24" y="10" width="64" height="96" fill="#2a1d14" ${O}/><g class="a-flapL"><path d="M24,10L64,22V100L24,106Z" fill="#8a5a3a" ${O}/></g>
        <g class="a-bob"><path d="M74,40q16,0 22,10" stroke="#3fb86a" stroke-width="5" fill="none"/><text x="92" y="36" font-family="Kanit" font-weight="900" font-size="18" fill="#3fb86a">ช้าๆ</text></g>`,
      firedark: `<rect x="10" y="10" width="100" height="100" rx="16" fill="#141414" ${O}/><g class="a-bob"><path d="M26,60Q20,40 40,38Q44,20 64,24Q86,20 88,40Q104,42 98,60Z" fill="#3a3632"/></g>
        <circle class="a-pulse" cx="60" cy="88" r="10" fill="#ff8a3a" opacity=".5"/><text x="60" y="106" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="15" fill="#f4ecd8">มืด</text>`,
      shutbehind: `<ellipse cx="60" cy="108" rx="34" ry="6" fill="#000" opacity=".18"/><rect x="34" y="12" width="60" height="94" fill="#8a5a3a" ${O}/><circle cx="84" cy="62" r="5" fill="#c9a24a"/><rect x="48" y="24" width="32" height="14" rx="2" fill="#c9a24a"/><text x="64" y="35" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="11" fill="${K}">714</text>
        <g class="a-look"><path d="M28,62H8M16,52L6,62L16,72" stroke="#3fb86a" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
      pullalarm: `<rect x="28" y="8" width="64" height="98" rx="10" fill="#c8261c" ${O}/><rect x="38" y="40" width="44" height="30" rx="5" fill="#f2efe6"/><g class="a-bob"><rect x="44" y="48" width="32" height="14" rx="4" fill="#c8261c" ${O}/></g>
        ${[0, 1, 2].map((i) => `<path class="a-wave" data-i="${i}" d="M${96 + i * 7},${30 - i * 4}q${8 + i * 3},${14} 0,${28 + i * 6}" stroke="#ffb04a" stroke-width="4" fill="none" stroke-linecap="round"/>`).join("")}`,
      people: `<g class="a-bob"><circle cx="38" cy="40" r="14" fill="#efc6a0" ${O}/><path d="M16,100q0,-40 22,-40t22,40z" fill="#7fb3a0" ${O}/></g><g class="a-bob2"><circle cx="82" cy="40" r="14" fill="#e9bc93" ${O}/><path d="M60,100q0,-40 22,-40t22,40z" fill="#5d6f8f" ${O}/></g>
        <g class="a-pulse"><circle cx="60" cy="18" r="12" fill="#ffd27a" ${O}/><text x="60" y="24" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="16" fill="${K}">!</text></g>`,
    });
  }

  Object.assign(window.Kwan, { daoStand, corridorZ: { VX, VY, xl, xr, yf, yc } });
})();
