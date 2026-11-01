// Hook stills (เลน B · 1 พ.ย. 2569): two candidate stories, three frames each, for the owner to choose before any script.
//   Sets.hkKitchen(L, o)  แก๊สรั่ว: a dark kitchen at night seen from the front door; cold moonlight through the window, a warm spill from
//                         the open door behind the camera, the LPG cylinder under the counter, its hose split and hissing; the leaked gas
//                         as a sickly yellow-green haze rolling along the floor and up the walls (o.gas 0..1); the wall switch by the door
//                         (o.sw x,y,s). Lt-style ink outlines.
//   Hk.switchBig(x, y, s, o) the wall switch plate in close-up (o.spark: a tiny arc inside the rocker)
//   Sets.hkFlood(L, o)    จระเข้บุกบ้าน: a living room at night, flood water to the knee, the front door open on the storm, lightning
//                         (o.flash 0..1), the stairs on the right rising out of the water, floating sandals and a plastic chair;
//                         o.croc { x, y, s, open, body } the crocodile gliding in (eyeshine, scutes, wake)
//   Hk.croc(x, y, s, o)   the crocodile, facing the camera at an angle: snout, eyes with eyeshine, scutes trailing back, the wake V
(function () {
  const INK = "#1e1a16";
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const Hk = (window.Hk = window.Hk || {});

  Sets.DEFS += `
    <linearGradient id="hkWallN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1218"/><stop offset=".6" stop-color="#18232c"/><stop offset="1" stop-color="#202c34"/></linearGradient>
    <linearGradient id="hkMoon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ec8ff" stop-opacity=".55"/><stop offset="1" stop-color="#9ec8ff" stop-opacity="0"/></linearGradient>
    <radialGradient id="hkGas"><stop offset="0" stop-color="#e8f06a" stop-opacity=".55"/><stop offset=".55" stop-color="#b8d24a" stop-opacity=".28"/><stop offset="1" stop-color="#a8c040" stop-opacity="0"/></radialGradient>
    <radialGradient id="hkWarm"><stop offset="0" stop-color="#ffcf8a" stop-opacity=".75"/><stop offset=".6" stop-color="#ff9a4a" stop-opacity=".25"/><stop offset="1" stop-color="#ff9a4a" stop-opacity="0"/></radialGradient>
    <linearGradient id="hkCyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a5a4a"/><stop offset=".35" stop-color="#7aa88a"/><stop offset=".6" stop-color="#4e7a62"/><stop offset="1" stop-color="#22382c"/></linearGradient>
    <linearGradient id="hkCounter" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a6670"/><stop offset="1" stop-color="#2a3238"/></linearGradient>
    <linearGradient id="hkWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a4a32"/><stop offset="1" stop-color="#3a2618"/></linearGradient>
    <linearGradient id="hkWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e4a4a"/><stop offset=".4" stop-color="#1a2e30"/><stop offset="1" stop-color="#0a1416"/></linearGradient>
    <linearGradient id="hkStorm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2234"/><stop offset="1" stop-color="#2e3a4e"/></linearGradient>
    <linearGradient id="hkCroc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a6a3a"/><stop offset=".6" stop-color="#3a4626"/><stop offset="1" stop-color="#1e2614"/></linearGradient>
    <radialGradient id="hkEye"><stop offset="0" stop-color="#fff6a0"/><stop offset=".45" stop-color="#ffb21a" stop-opacity=".9"/><stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="hkFlash" cx=".3" cy=".25" r=".9"><stop offset="0" stop-color="#e8f0ff" stop-opacity=".9"/><stop offset="1" stop-color="#9ab0e8" stop-opacity=".25"/></radialGradient>`;

  // ---------------------------------------------------------------- แก๊สรั่ว
  const gasCloud = (r, n, x0, x1, y0, y1, s0 = 160, s1 = 360, op = 1) => Array.from({ length: n }, () => `<g class="gasW" data-d="${f1(10 + r() * 30)}"><ellipse cx="${f1(x0 + r() * (x1 - x0))}" cy="${f1(y0 + r() * (y1 - y0))}" rx="${f1(s0 + r() * (s1 - s0))}" ry="${f1((s0 + r() * (s1 - s0)) * 0.45)}" fill="url(#hkGas)" opacity="${f1(op * (0.6 + r() * 0.4))}"/></g>`).join("");
  // wavy heat-shimmer lines (the gas you can't see, drawn so you can)
  const shimmer = (r, n, x0, x1, y0, y1) => Array.from({ length: n }, () => { const x = x0 + r() * (x1 - x0), y = y0 + r() * (y1 - y0), w = 80 + r() * 160; return `<path d="M${f1(x)},${f1(y)}q${f1(w / 4)},-14 ${f1(w / 2)},0t${f1(w / 2)},0" stroke="#e4f07a" stroke-width="4" fill="none" opacity=".55" stroke-linecap="round"/>`; }).join("");
  Hk.switchBig = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s})">
    <rect x="-96" y="-150" width="192" height="300" rx="22" fill="#000" opacity=".35" transform="translate(10,14)"/>
    <rect x="-96" y="-150" width="192" height="300" rx="22" fill="#e8e4d8" ${OUT(5)}/><rect x="-84" y="-138" width="168" height="40" rx="12" fill="#fff" opacity=".5"/>
    <rect x="-44" y="-86" width="88" height="172" rx="14" fill="#d4cfc0" ${OUT(4)}/><path d="M-44,0H44" stroke="#a8a294" stroke-width="5"/><rect x="-38" y="-80" width="76" height="76" rx="10" fill="#f4f0e6"/>
    <circle cx="-70" cy="-120" r="6" fill="#a8a294"/><circle cx="70" cy="120" r="6" fill="#a8a294"/>
    ${o.spark ? `<g class="spk"><circle cx="0" cy="30" r="46" fill="#7ad0ff" opacity=".35"/><path d="M-14,10l12,14l-8,4l18,22" stroke="#e8f8ff" stroke-width="6" fill="none" stroke-linecap="round"/></g>` : ""}</g>`;
  Sets.hkKitchen = function (L, o = {}) {
    const id = o.id || "kg", r = mk(o.seed || 301), gas = o.gas ?? 0.6;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#hkWallN)"/>`);
    // back wall: tiles to shoulder height, the window with moonlight, a wall clock at 02:14, cupboards
    let f = `<rect x="-900" y="700" width="2900" height="560" fill="#1c2a30"/>`;
    for (let x = -900; x < 2000; x += 70) f += `<path d="M${x},700V1260" stroke="#26363e" stroke-width="3"/>`;
    for (let y = 700; y < 1260; y += 70) f += `<path d="M-900,${y}H2000" stroke="#26363e" stroke-width="3"/>`;
    f += `<g><rect x="600" y="260" width="420" height="380" fill="#26405e" ${OUT(6)}/><rect x="616" y="276" width="388" height="348" fill="#3a6a9a"/><circle cx="900" cy="370" r="54" fill="#e8f2ff"/><circle cx="900" cy="370" r="120" fill="#cfe2ff" opacity=".25"/>
      <path d="M810,276V624M616,450H1004" stroke="#1a2a3a" stroke-width="12"/><path d="M600,250Q640,420 590,650" stroke="#4a3a5a" stroke-width="40" fill="none" opacity=".9"/></g>`;
    f += `<g transform="translate(300,420)"><circle r="62" fill="#e8e0cc" ${OUT(5)}/><path d="M0,0V-40M0,0L26,10" stroke="${INK}" stroke-width="7" stroke-linecap="round"/><circle r="6" fill="${INK}"/></g>`;
    f += `<rect x="-900" y="120" width="1360" height="300" fill="#2a2420" ${OUT(5)}/>${[-700, -400, -100, 200].map((x) => `<rect x="${x}" y="140" width="260" height="260" rx="8" fill="#342c26" ${OUT(3)}/><circle cx="${x + 230}" cy="270" r="8" fill="#8a7a62"/>`).join("")}`;
    put(L.far, f);
    // the counter, the stove, the cylinder in the open cabinet, the split hose
    let s = `<rect x="-900" y="1160" width="2900" height="34" fill="url(#hkCounter)" ${OUT(5)}/><rect x="-900" y="1194" width="2900" height="420" fill="#2c2620" ${OUT(5)}/>`;
    s += [-700, -380, 1060].map((x) => `<rect x="${x}" y="1220" width="290" height="360" rx="8" fill="#3a3028" ${OUT(3)}/><rect x="${x + 250}" y="1380" width="16" height="60" rx="6" fill="#8a7a62"/>`).join("");
    s += `<g transform="translate(860,1160)"><rect x="-210" y="-50" width="420" height="50" rx="8" fill="#5a6066" ${OUT(4)}/>${[-100, 100].map((x) => `<ellipse cx="${x}" cy="-52" rx="70" ry="14" fill="#2a2e32" ${OUT(3)}/><ellipse cx="${x}" cy="-56" rx="34" ry="7" fill="#1a1c1e"/>`).join("")}${[-150, -60, 60, 150].map((x) => `<circle cx="${x}" cy="-22" r="10" fill="#1a1c1e"/>`).join("")}</g>`;
    // open cabinet with the cylinder
    s += `<rect x="520" y="1220" width="560" height="380" fill="#0e0c0a" ${OUT(4)}/><path d="M1080,1220L1220,1250V1620L1080,1600Z" fill="#4a3c30" ${OUT(4)}/>`;
    s += `<g transform="translate(760,1600)"><ellipse cx="0" cy="0" rx="150" ry="22" fill="#000" opacity=".5"/><path d="M-120,0V-250Q-120,-300 -60,-310H60Q120,-300 120,-250V0Z" fill="url(#hkCyl)" ${OUT(5)}/>
      <path d="M-120,-180H120M-120,-80H120" stroke="#1e3428" stroke-width="6"/><rect x="-40" y="-370" width="80" height="60" rx="10" fill="url(#hkCyl)" ${OUT(4)}/><path d="M-60,-370Q0,-410 60,-370" stroke="#8a9aa2" stroke-width="14" fill="none"/>
      <g transform="translate(0,-380)"><rect x="-30" y="-36" width="60" height="40" rx="8" fill="#b8bec4" ${OUT(4)}/><circle cx="0" cy="-16" r="13" fill="#d8302a" ${OUT(3)}/></g></g>`;
    // the hose: orange, from the regulator up behind the counter; split at (420,1340)
    s += `<path d="M760,1250C820,1250 860,1330 940,1340C990,1346 990,1260 1010,1210" stroke="${INK}" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M760,1250C820,1250 860,1330 940,1340C990,1346 990,1260 1010,1210" stroke="#e8701a" stroke-width="20" fill="none" stroke-linecap="round"/>
      <path d="M928,1330l20,20" stroke="#1a0e06" stroke-width="10" stroke-linecap="round"/>`;
    // floor
    s += `<path d="M-900,1600H2000V2800H-900Z" fill="#1a2024"/>`;
    for (let k = 0; k < 14; k++) s += `<path d="M${-900 + k * 230},1600L${-1600 + k * 330},2800" stroke="#242c32" stroke-width="5"/>`;
    for (let k = 0; k < 6; k++) s += `<path d="M-900,${1660 + k * k * 40}H2000" stroke="#242c32" stroke-width="5"/>`;
    // the door frame on the left with the switch
    const SW = o.sw || { x: 110, y: 1000, s: 0.55 };
    s += `<rect x="-900" y="0" width="980" height="2800" fill="#141a1e" ${OUT(5)}/><rect x="40" y="0" width="60" height="2800" fill="#3a2e26" ${OUT(4)}/>`;
    s += Hk.switchBig(SW.x, SW.y, SW.s, { spark: o.spark });
    s += `<g opacity="${gas}">${gasCloud(r, 18, -300, 1400, 1250, 1900, 200, 460, 1.3)}${gasCloud(r, 12, 400, 1300, 800, 1350, 140, 300, 1.2)}${shimmer(r, 26, 400, 1300, 850, 1800)}
      <g transform="translate(940,1340)"><ellipse cx="-40" cy="-200" rx="260" ry="200" fill="url(#hkGas)"/><path d="M0,0Q60,-40 40,-120Q20,-200 90,-260" stroke="#e8f07a" stroke-width="10" fill="none" opacity=".6" stroke-linecap="round"/><path d="M0,0Q-50,-60 -20,-150" stroke="#e8f07a" stroke-width="8" fill="none" opacity=".5" stroke-linecap="round"/></g></g>`;
    put(L.set, s);
    // the light: moonbeam, the warm spill from the door behind the camera, the gas haze rolling
    put(L.glow, `<path d="M616,276L1004,276L1100,1700L500,1700Z" fill="url(#hkMoon)" opacity=".28"/>
      <ellipse cx="200" cy="1900" rx="900" ry="340" fill="url(#hkWarm)" opacity=".8"/>
      <g id="${id}-gasf" opacity="${gas}">${gasCloud(mk(9), 8, -300, 1400, 1850, 2100, 220, 420, 1.1)}</g>
      <g id="${id}-gas" opacity="0">
        <g transform="translate(940,1340)"><ellipse cx="-40" cy="-200" rx="260" ry="200" fill="url(#hkGas)"/><path d="M0,0Q60,-40 40,-120Q20,-200 90,-260" stroke="#e8f07a" stroke-width="10" fill="none" opacity=".55" stroke-linecap="round"/><path d="M0,0Q-50,-60 -20,-150" stroke="#e8f07a" stroke-width="8" fill="none" opacity=".45" stroke-linecap="round"/><ellipse cx="20" cy="-60" rx="120" ry="70" fill="url(#hkGas)"/></g></g>`);
  };

  // ---------------------------------------------------------------- จระเข้บุกบ้าน
  Hk.croc = (x, y, s = 1, o = {}) => (o.open ? lunge(x, y, s, o) : lurk(x, y, s, o));
  const eye = (cx, cy, r, sh = 1) => `<g transform="translate(${cx},${cy})"><circle r="${r * 2.2}" fill="url(#hkEye)" opacity="${sh}"/><ellipse rx="${r * 1.35}" ry="${r}" fill="#4a5630" ${OUT(3)}/><path d="M${-r},${-r * 0.1}Q0,${-r * 0.8} ${r},${-r * 0.1}Q0,${r * 0.5} ${-r},${-r * 0.1}Z" fill="#ffcf2a" ${OUT(2.5)}/><ellipse cy="${-r * 0.1}" rx="${r * 0.16}" ry="${r * 0.58}" fill="#0a0806"/><circle cx="${-r * 0.35}" cy="${-r * 0.35}" r="${r * 0.18}" fill="#fff"/></g>`;
  function lurk(x, y, s, o) {
    let g = `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">`;
    g += `${[1, 2, 3, 4].map((k) => `<ellipse cx="0" cy="${10 + k * 10}" rx="${120 + k * 110}" ry="${18 + k * 12}" fill="none" stroke="#9ab8b8" stroke-width="5" opacity="${(0.55 - k * 0.11).toFixed(2)}"/>`).join("")}`;
    g += `<path d="M-40,20L-460,140M40,20L460,140" stroke="#a8c8c8" stroke-width="8" opacity=".45" stroke-linecap="round"/>`;
    // scutes behind, receding (smaller, higher)
    for (let k = 1; k < 6; k++) { const yy = -30 - k * 34, sc = 1 - k * 0.13; g += `<g transform="translate(${f1(Math.sin(k) * 10)},${f1(yy)}) scale(${f1(sc)})">${[-36, -12, 12, 36].map((sx) => `<path d="M${sx - 10},10L${sx},-14L${sx + 10},10Z" fill="#3e4a26" ${OUT(2.5)}/>`).join("")}</g>`; }
    // the head low in the water, seen from just above the surface: a flat skull, a LONG tapering snout running at the lens,
    // the nostril knob at the tip, bony brow ridges with slit-pupil eyes, rough osteoderms
    g += `<path d="M-110,-40Q-118,-92 -60,-110Q0,-120 60,-110Q118,-92 110,-40L70,0Q0,12 -70,0Z" fill="url(#hkCroc)" ${OUT(4)}/>`;
    g += `<path d="M-70,0Q-60,90 -34,170Q0,200 34,170Q60,90 70,0Q0,14 -70,0Z" fill="#4e5c2e" ${OUT(4)}/><path d="M0,10V160" stroke="#3a4422" stroke-width="6" opacity=".7"/>`;
    g += Array.from({ length: 7 }, (_, k) => `<path d="M${-58 + k * 6},${20 + k * 22}h${116 - k * 12}" stroke="#3a4422" stroke-width="3" opacity=".55"/>`).join("");
    g += `<ellipse cx="0" cy="172" rx="34" ry="18" fill="#3a4422" ${OUT(3)}/><circle cx="-12" cy="168" r="5" fill="#0a0806"/><circle cx="12" cy="168" r="5" fill="#0a0806"/>`;
    g += Array.from({ length: 10 }, (_, k) => `<path d="M${-90 + k * 20},${-62 + (k % 2) * 12}l6,-10l6,10z" fill="#2e3a1a" opacity=".85"/>`).join("");
    g += [-1, 1].map((sd) => `<path d="M${sd * 30},-104Q${sd * 62},-150 ${sd * 96},-106" fill="#3e4a26" ${OUT(3)}/>`).join("");
    g += eye(-62, -104, 15, o.shine ?? 1) + eye(62, -104, 15, o.shine ?? 1);
    g += `<path d="M-200,4Q0,40 200,4" stroke="#2e4a4a" stroke-width="22" fill="none" opacity=".8"/><path d="M-170,0Q0,26 170,0" stroke="#8ab0b0" stroke-width="4" fill="none" opacity=".6"/></g>`;
    return g;
  }
  function lunge(x, y, s, o) {
    // 3/4 profile facing right, bursting up out of the water; jaw angle ~30°
    let g = `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">`;
    g += Array.from({ length: 16 }, (_, k) => { const a = -2.6 + k * 0.17, rr = 180 + (k % 3) * 60; return `<path d="M${f1(Math.cos(a) * 60)},${f1(Math.sin(a) * 30)}L${f1(Math.cos(a) * rr)},${f1(Math.sin(a) * rr * 0.9)}" stroke="#cfe6ea" stroke-width="${7 - (k % 3) * 2}" opacity=".7" stroke-linecap="round"/>`; }).join("");
    g += `<g transform="rotate(-18)">`;
    // neck and skull
    g += `<path d="M-320,90Q-300,-60 -150,-90Q-40,-110 40,-70L60,40Q-100,110 -320,90Z" fill="url(#hkCroc)" ${OUT(5)}/>`;
    g += Array.from({ length: 5 }, (_, k) => `<path d="M${-290 + k * 50},${-40 + k * 4}l14,-30l14,30z" fill="#3e4a26" ${OUT(2.5)}/>`).join("");
    // upper jaw: long, tapered, slightly lifted; lower jaw dropped open; the mouth inside
    g += `<path d="M20,-70L420,-150Q450,-150 448,-128L60,20Z" fill="#8a2a22" ${OUT(3)}/>`;
    g += `<path d="M20,-70Q200,-130 420,-152Q456,-150 450,-124Q260,-80 60,-20Z" fill="url(#hkCroc)" ${OUT(5)}/>`;
    g += `<path d="M60,40Q240,120 400,150Q436,152 432,124Q240,70 60,10Z" fill="#c8b07a" ${OUT(5)}/>`;
    g += Array.from({ length: 11 }, (_, k) => { const tx = 80 + k * 32, ty = -40 - k * 9.5; return `<path d="M${tx},${f1(ty)}l7,26l9,-25z" fill="#f4eed8" ${OUT(1.5)}/>`; }).join("");
    g += Array.from({ length: 10 }, (_, k) => { const tx = 90 + k * 32, ty = 38 + k * 10; return `<path d="M${tx},${f1(ty)}l7,-26l9,25z" fill="#f4eed8" ${OUT(1.5)}/>`; }).join("");
    g += `<ellipse cx="430" cy="-150" rx="22" ry="14" fill="#3e4a26" ${OUT(3)}/><circle cx="436" cy="-156" r="4" fill="#0a0806"/>`;
    g += eye(-40, -110, 24, o.shine ?? 1);
    g += `</g><path d="M-420,120Q0,170 420,110" stroke="#2e4a4a" stroke-width="40" fill="none" opacity=".85"/><path d="M-380,100Q0,150 380,92" stroke="#9ac0c0" stroke-width="6" fill="none" opacity=".7"/></g>`;
    return g;
  }
  Sets.hkFlood = function (L, o = {}) {
    const id = o.id || "kf", r = mk(o.seed || 311), W = o.water ?? 1340, fl = o.flash ?? 0;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#0c1016"/>`);
    // back wall with family photos, the front door open on the storm
    let f = `<rect x="-900" y="0" width="2900" height="1500" fill="#1e2830"/><path d="M-900,980H2000" stroke="#2e3a42" stroke-width="10"/>`;
    f += `<g><rect x="80" y="520" width="440" height="${W - 520}" fill="url(#hkStorm)"/>${Array.from({ length: 30 }, () => `<path d="M${f1(90 + r() * 420)},${f1(530 + r() * 700)}l-14,60" stroke="#8aa0c8" stroke-width="3" opacity=".6"/>`).join("")}
      <path d="M380,520L330,640L370,650L300,820" stroke="#e8f0ff" stroke-width="${fl > 0 ? 9 : 0}" fill="none" stroke-linejoin="round"/>
      <rect x="60" y="500" width="480" height="${W - 500 + 10}" fill="none" stroke="#3a2a1e" stroke-width="40"/><path d="M540,520L700,560V${W}L540,${W}Z" fill="#5a3e28" ${OUT(4)}/></g>`;
    f += [[-500, 640], [-260, 700], [820, 620]].map(([x, y]) => `<g><rect x="${x}" y="${y}" width="150" height="190" fill="#5a4a3a" ${OUT(4)}/><rect x="${x + 14}" y="${y + 14}" width="122" height="162" fill="#8aa0b0"/><circle cx="${x + 75}" cy="${y + 80}" r="30" fill="#c89a78"/></g>`).join("");
    put(L.far, f);
    // the water: dark, with the room's things floating, reflections of the door's storm light
    let s = `<rect x="-900" y="${W}" width="2900" height="1500" fill="url(#hkWater)"/><path d="M-900,${W}H2000" stroke="#6a9090" stroke-width="6" opacity=".6"/>`;
    s += `<path d="M100,${W + 10}L520,${W + 10}L700,${W + 700}L-100,${W + 700}Z" fill="#4a6a8a" opacity=".22"/>`;
    for (let k = 0; k < 26; k++) s += `<path class="rip" d="M${f1(-800 + r() * 2700)},${f1(W + 30 + r() * 900)}q30,-8 60,0t60,0" stroke="#7aa0a0" stroke-width="4" fill="none" opacity="${(0.25 + r() * 0.3).toFixed(2)}"/>`;
    s += `<g transform="translate(-260,${W + 60}) rotate(-12)"><rect x="-90" y="-20" width="180" height="26" rx="8" fill="#2a8ac8" ${OUT(3)}/><path d="M-80,-20V-110H80V-20" stroke="#2a8ac8" stroke-width="16" fill="none"/></g>`;
    s += `<ellipse cx="760" cy="${W + 120}" rx="40" ry="14" fill="#e8c030" ${OUT(2.5)}/><ellipse cx="-560" cy="${W + 220}" rx="44" ry="15" fill="#e85a3a" ${OUT(2.5)}/>`;
    put(L.set, s);
    // the croc
    if (o.croc) put(L.set, `<g id="${id}-croc">${Hk.croc(o.croc.x, o.croc.y, o.croc.s, o.croc)}</g>`);
    // the stairs on the right rising out of the water, the banister
    let st = "";
    for (let k = 0; k < 9; k++) { const sx = 640 + k * 70, sy = W + 180 - k * 120; st += `<path d="M${sx},${sy}H2000V${sy + 120}H${sx}Z" fill="url(#hkWood)" ${OUT(4)}/><path d="M${sx},${sy}H2000" stroke="#9a7a5a" stroke-width="6"/>`; }
    st += `<path d="M620,${W + 120}L1260,${W - 960}" stroke="${INK}" stroke-width="30" stroke-linecap="round"/><path d="M620,${W + 120}L1260,${W - 960}" stroke="#7a5236" stroke-width="20" stroke-linecap="round"/>`;
    for (let k = 0; k < 7; k++) { const px = 650 + k * 92, py = W + 70 - k * 155; st += `<rect x="${px - 8}" y="${py}" width="16" height="${f1(160 + k * 0)}" fill="#6a4a30" ${OUT(2.5)}/>`; }
    put(L.mid, "");
    put(L.act, st);
    // the front water over the actors' legs (fg), rain on the lens, lightning wash
    put(L.fg, `<rect x="640" y="${W + 40}" width="1400" height="1600" fill="url(#hkWater)" opacity=".72"/><path d="M640,${W + 40}H2000" stroke="#8ab0b0" stroke-width="5" opacity=".5"/>
      ${Array.from({ length: 12 }, () => `<path d="M${f1(-800 + r() * 2700)},${f1(W + 60 + r() * 300)}q40,-10 80,0t80,0" stroke="#9ac0c0" stroke-width="4" fill="none" opacity=".4"/>`).join("")}`);
    put(L.glow, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#hkFlash)" opacity="${f1(fl * 0.28)}"/>`);
  };
})();
