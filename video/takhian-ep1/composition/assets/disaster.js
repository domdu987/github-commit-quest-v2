// Disaster hook stills (เลน B · 1 พ.ย. 2569): two candidate stories in the 60 Seconds / Fallout vein, Thai settings.
//   Sets.dsGarage(L, o)  ไฟดับทั้งประเทศ: the front room of a Thai townhouse at night (doubles as the garage), the steel roll-up
//                        shutter pulled DOWN behind, the whole soi black through the transom; a child asleep on a floor mattress with
//                        a mosquito net; the portable generator on the tiles (o.gen {x,y,s}), its exhaust pipe breathing grey fumes
//                        (o.fume 0..1) that roll along the floor toward the mattress; o.bulb 0..1 the generator-fed work lamp.
//   Sets.dsChem(L, o)    ไซเรนโรงงานเคมี: a bedroom at night, the big window showing the village rooftops and, on the horizon, a
//                        chemical plant on fire with a yellow plume (o.plume 0..1 how far it has drifted toward the house; o.press
//                        0..1 yellow haze pressed against the glass); a split-type air conditioner over the window (o.acOn shows
//                        its green power LED); a siren tower with a red flash (o.siren 0..1).
//   Ds.remote(x,y,s,o)   the AC remote in a hand-held close-up, o.press: the thumb on the power button.
(function () {
  const INK = "#1e1a16";
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const Ds = (window.Ds = window.Ds || {});

  Sets.DEFS += `
    <linearGradient id="dsWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141a22"/><stop offset="1" stop-color="#222a34"/></linearGradient>
    <radialGradient id="dsLamp"><stop offset="0" stop-color="#ffe2a0" stop-opacity=".85"/><stop offset=".5" stop-color="#ffb04a" stop-opacity=".25"/><stop offset="1" stop-color="#ff9a3a" stop-opacity="0"/></radialGradient>
    <radialGradient id="dsFume"><stop offset="0" stop-color="#b8bcc0" stop-opacity=".6"/><stop offset=".6" stop-color="#8a9096" stop-opacity=".25"/><stop offset="1" stop-color="#7a8086" stop-opacity="0"/></radialGradient>
    <radialGradient id="dsPlume"><stop offset="0" stop-color="#f4e04a" stop-opacity=".85"/><stop offset=".55" stop-color="#c8b830" stop-opacity=".45"/><stop offset="1" stop-color="#a89a2a" stop-opacity="0"/></radialGradient>
    <radialGradient id="dsFire"><stop offset="0" stop-color="#fff2b0"/><stop offset=".4" stop-color="#ff9a2a" stop-opacity=".9"/><stop offset="1" stop-color="#ff4a1a" stop-opacity="0"/></radialGradient>
    <linearGradient id="dsSkyC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0e1424"/><stop offset=".7" stop-color="#3a2a30"/><stop offset="1" stop-color="#8a4a2a"/></linearGradient>
    <linearGradient id="dsGen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0b82a"/><stop offset="1" stop-color="#b07a12"/></linearGradient>
    <radialGradient id="dsRed"><stop offset="0" stop-color="#ff5a4a" stop-opacity=".9"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>`;

  const puffs = (r, n, x0, x1, y0, y1, s0, s1, fill, op = 1) => Array.from({ length: n }, () => { const rx = s0 + r() * (s1 - s0); return `<ellipse cx="${f1(x0 + r() * (x1 - x0))}" cy="${f1(y0 + r() * (y1 - y0))}" rx="${f1(rx)}" ry="${f1(rx * 0.5)}" fill="url(#${fill})" opacity="${f1(op * (0.6 + r() * 0.4))}"/>`; }).join("");

  // ---------------------------------------------------------------- generator
  Ds.gen = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s})">
    <ellipse cx="0" cy="10" rx="230" ry="30" fill="#000" opacity=".45"/>
    <path d="M-200,0V-200H200V0" fill="none" stroke="${INK}" stroke-width="22" stroke-linejoin="round"/><path d="M-200,0V-200H200V0" fill="none" stroke="#2a2e32" stroke-width="14" stroke-linejoin="round"/>
    <rect x="-170" y="-180" width="340" height="170" rx="18" fill="url(#dsGen)" ${OUT(5)}/>
    <rect x="-150" y="-160" width="150" height="120" rx="10" fill="#2a2a2a" ${OUT(3)}/>${[0, 1, 2, 3].map((k) => `<path d="M-140,${-145 + k * 28}H-10" stroke="#4a4a4a" stroke-width="8"/>`).join("")}
    <circle cx="80" cy="-100" r="46" fill="#3a3a3a" ${OUT(4)}/><circle cx="80" cy="-100" r="20" fill="#1a1a1a"/>
    <rect x="20" y="-170" width="120" height="26" rx="6" fill="#d8d0c0" ${OUT(3)}/><circle cx="40" cy="-157" r="7" fill="${o.on ? "#5aff6a" : "#3a4a3a"}"/>
    <g transform="translate(150,-120)"><rect x="0" y="-8" width="40" height="16" rx="4" fill="#d8d0c0" ${OUT(3)}/>${o.cord ? `<path d="M40,0 C${o.cord[0] / 2},${o.cord[1] / 2 - 40} ${o.cord[0] - 20},${o.cord[1]} ${o.cord[0]},${o.cord[1]}" stroke="${INK}" stroke-width="7" fill="none"/><path d="M40,0 C${o.cord[0] / 2},${o.cord[1] / 2 - 40} ${o.cord[0] - 20},${o.cord[1]} ${o.cord[0]},${o.cord[1]}" stroke="#e8e0d0" stroke-width="3" fill="none"/>` : ""}</g>
    <g transform="translate(-200,-70)"><rect x="-60" y="-16" width="70" height="32" rx="8" fill="#5a5a5a" ${OUT(4)}/><ellipse cx="-62" cy="0" rx="8" ry="14" fill="#111"/></g>
    <rect x="-150" y="-230" width="100" height="40" rx="8" fill="#c82a2a" ${OUT(4)}/></g>`;

  Sets.dsGarage = function (L, o = {}) {
    const r = mk(o.seed || 411), fume = o.fume ?? 0, bulb = o.bulb ?? 0;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#dsWall)"/>`);
    // back wall: plaster, a calendar, a wall clock at 01:40, a family photo, the stair going up at the right
    let f = `<rect x="-900" y="200" width="2900" height="1300" fill="#2a3240"/><path d="M-900,1300H2000" stroke="#1e242e" stroke-width="10"/>`;
    f += `<g transform="translate(160,520)"><circle r="60" fill="#e8e0cc" ${OUT(5)}/><path d="M0,0V-40M0,0L-30,18" stroke="${INK}" stroke-width="7" stroke-linecap="round"/><circle r="6" fill="${INK}"/></g>`;
    f += `<g transform="translate(470,600)"><rect x="-110" y="-80" width="220" height="160" fill="#c8b890" ${OUT(5)}/><rect x="-96" y="-66" width="192" height="132" fill="#6a7a8a"/><circle cx="-40" cy="-6" r="22" fill="#d8b890"/><circle cx="30" cy="-10" r="26" fill="#d8b890"/><circle cx="-4" cy="20" r="16" fill="#d8b890"/></g>`;
    f += `<g transform="translate(820,560)"><rect x="-70" y="-110" width="140" height="210" fill="#f0ece0" ${OUT(4)}/><rect x="-70" y="-110" width="140" height="44" fill="#c83a2a"/>${Array.from({ length: 20 }, (_, k) => `<rect x="${-58 + (k % 5) * 24}" y="${-52 + Math.floor(k / 5) * 34}" width="16" height="16" fill="#cfc8b8"/>`).join("")}</g>`;
    // stair at right
    f += `<g>${Array.from({ length: 8 }, (_, k) => `<rect x="${980 + k * 0}" y="${1300 - (k + 1) * 110}" width="${400 - k * 0}" height="110" fill="#4a3a2c" ${OUT(3)}/>`).join("")}<path d="M960,1300L960,420" stroke="#6a5240" stroke-width="18"/></g>`;
    put(L.far, f);
    // floor tiles
    let s = `<path d="M-900,1300H2000V2800H-900Z" fill="#3a3e44"/>`;
    for (let k = 0; k < 16; k++) s += `<path d="M${-900 + k * 200},1300L${-1700 + k * 300},2800" stroke="#2c3036" stroke-width="5"/>`;
    for (let k = 0; k < 7; k++) s += `<path d="M-900,${1340 + k * k * 34}H2000" stroke="#2c3036" stroke-width="5"/>`;
    // the motorbike parked at the left edge (the room is the garage)
    s += `<g transform="translate(-120,1460)"><circle cx="-90" cy="0" r="70" fill="#1a1a1a" ${OUT(5)}/><circle cx="160" cy="0" r="70" fill="#1a1a1a" ${OUT(5)}/><circle cx="-90" r="26" fill="#6a6a6a"/><circle cx="160" r="26" fill="#6a6a6a"/>
      <path d="M-90,0L0,-110H120L160,0" fill="none" stroke="#3a4a6a" stroke-width="22"/><path d="M-40,-130H110Q140,-130 130,-100H-30Z" fill="#2a3a5a" ${OUT(4)}/><path d="M160,0L190,-200" stroke="#8a8a8a" stroke-width="12"/></g>`;
    // the mattress with a mosquito net and the sleeping child (blanket lump + head on a pillow)
    const mx = o.matX ?? 560, my = o.matY ?? 1560;
    s += `<g transform="translate(${mx},${my})"><rect x="-250" y="-40" width="500" height="80" rx="20" fill="#5a7ab0" ${OUT(5)}/><rect x="-250" y="-40" width="500" height="22" rx="10" fill="#7a9ad0"/>
      <ellipse cx="-170" cy="-48" rx="70" ry="26" fill="#f0ece0" ${OUT(4)}/>
      <g transform="translate(-160,-80)"><circle r="44" fill="#c89a6a" ${OUT(4)}/><path d="M-44,-6C-48,-56 40,-62 44,-10Q20,-30 -10,-28Q-30,-26 -44,-6Z" fill="#16100c" ${OUT(3)}/><path d="M-20,8q8,6 16,0M12,8q8,6 16,0" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round"/></g>
      <path d="M-120,-40C-80,-110 140,-110 210,-40Z" fill="#e8a8b8" ${OUT(5)}/><path d="M-60,-70C0,-90 100,-90 160,-60" stroke="#f8c8d4" stroke-width="10" fill="none" opacity=".7"/>
      <path d="M-270,40L-230,-330H230L270,40" fill="#e8f0ff" fill-opacity=".1" stroke="#cfe0ff" stroke-width="3" stroke-dasharray="2 8" opacity=".9"/><path d="M-230,-330H230" stroke="#cfe0ff" stroke-width="4" opacity=".7"/></g>`;
    // the generator
    if (o.gen) s += Ds.gen(o.gen.x, o.gen.y, o.gen.s || 1, o.gen);
    put(L.set, s);
    // the closed steel roll-up shutter: the house front, seen from inside (set layer, behind the props)
    if (o.shutter !== false) {
      const sx = o.shX ?? -40, sw = o.shW ?? 560;
      put(L.far, `<g><rect x="${sx}" y="360" width="${sw}" height="950" fill="#5a646e" ${OUT(5)}/>${Array.from({ length: 24 }, (_, k) => `<path d="M${sx},${390 + k * 38}H${sx + sw}" stroke="#3a424a" stroke-width="8"/>`).join("")}<rect x="${sx}" y="330" width="${sw}" height="50" fill="#3a424a" ${OUT(4)}/><rect x="${sx + sw / 2 - 40}" y="1250" width="80" height="40" rx="6" fill="#c8a040" ${OUT(3)}/><path d="M${sx + sw / 2},1290v30" stroke="#c8a040" stroke-width="10"/></g>`);
    }
    // light: the lamp from the generator, then the fumes
    if (bulb > 0) put(L.glow, `<g><path d="M${o.lampX ?? 700},280V420" stroke="${INK}" stroke-width="5"/><circle cx="${o.lampX ?? 700}" cy="440" r="26" fill="#fff2c0" ${OUT(3)}/><circle cx="${o.lampX ?? 700}" cy="440" r="${f1(260 + 360 * bulb)}" fill="url(#dsLamp)" opacity="${f1(bulb)}"/></g>`);
    if (fume > 0 && o.gen) {
      const gx = o.gen.x - 270 * (o.gen.s || 1), gy = o.gen.y - 70 * (o.gen.s || 1), tx = mx - 120;
      put(L.glow, `<g opacity="${f1(Math.min(1, fume * 1.2))}">${puffs(r, Math.round(6 + 26 * fume), Math.min(gx, tx - 60 - 300 * fume), gx + 60, gy - 120 - 280 * fume, gy + 60, 70, 200 + 120 * fume, "dsFume")}
        ${Array.from({ length: Math.round(3 + 6 * fume) }, (_, k) => `<path d="M${f1(gx - 30 - k * 60 * fume)},${f1(gy - 10 - k * 26 * fume)}q-26,-18 -52,0t-52,0" stroke="#d8dce0" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/>`).join("")}</g>`);
    }
  };

  // ---------------------------------------------------------------- chemical plume
  Ds.remote = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s})">
    <rect x="-70" y="-190" width="140" height="380" rx="44" fill="#f4f2ec" ${OUT(5)}/><rect x="-50" y="-160" width="100" height="70" rx="10" fill="#2a3a3a" ${OUT(3)}/><text x="0" y="-112" text-anchor="middle" font-family="sans-serif" font-weight="700" font-size="40" fill="#7ae0c0">25°</text>
    <circle cx="0" cy="-40" r="30" fill="#d84a3a" ${OUT(4)}/><path d="M0,-58V-40M-12,-50A16,16 0 1 0 12,-50" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>
    ${[0, 1, 2].map((k) => `<rect x="-50" y="${10 + k * 50}" width="40" height="30" rx="8" fill="#cfcac0" ${OUT(2)}/><rect x="10" y="${10 + k * 50}" width="40" height="30" rx="8" fill="#cfcac0" ${OUT(2)}/>`).join("")}
    ${o.press ? `<circle cx="0" cy="-40" r="52" fill="#ffd84a" opacity=".3"/>` : ""}</g>`;

  Sets.dsChem = function (L, o = {}) {
    const r = mk(o.seed || 523), pl = o.plume ?? 0.2, press = o.press ?? 0, siren = o.siren ?? 1;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#141a22"/>`);
    // the view through the window (far): sky glowing orange low, the plant, flames, the plume drifting toward us over the roofs
    const wx = o.winX ?? 120, wy = o.winY ?? 300, ww = o.winW ?? 840, wh = o.winH ?? 760;
    let v = `<rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" fill="url(#dsSkyC)"/>`;
    const hz = wy + wh * 0.62;
    // the plant on the horizon: stacks, tanks, a flare
    v += `<g transform="translate(${wx + ww * 0.62},${hz})"><rect x="-150" y="-60" width="300" height="60" fill="#1a1416"/>${[-110, -60, 90].map((x, k) => `<rect x="${x}" y="${-170 - k * 20}" width="22" height="${170 + k * 20}" fill="#1a1416"/>`).join("")}<ellipse cx="20" cy="-60" rx="60" ry="40" fill="#1a1416"/>
      <ellipse cx="0" cy="-90" rx="${f1(130 + 60 * siren)}" ry="90" fill="url(#dsFire)"/><path d="M-40,-60Q-30,-140 0,-170Q10,-120 30,-150Q50,-100 40,-60Z" fill="#ffb84a"/><path d="M-14,-60Q-6,-110 8,-124Q16,-90 22,-60Z" fill="#fff2b0"/></g>`;
    // the plume: from the plant up, then leaning toward the camera-left and down over the roofs
    const px = wx + ww * 0.62, py = hz - 140;
    v += `<g>${puffs(r, 18, px - 80, px + 120, py - 260, py, 60, 140, "dsPlume", 0.9)}${puffs(r, Math.round(10 + 24 * pl), px - 420 * pl - 200, px, py - 200 + 120 * pl, hz + 80 * pl, 80, 160 + 120 * pl, "dsPlume", 0.85)}</g>`;
    // village roofs in front of the plant
    v += `<g>${Array.from({ length: 9 }, (_, k) => { const x = wx - 40 + k * 110, h = 60 + (k % 3) * 30; return `<path d="M${x},${hz + 120}V${hz + 120 - h}L${x + 55},${hz + 80 - h}L${x + 110},${hz + 120 - h}V${hz + 120}Z" fill="#0e0c10"/>`; }).join("")}<rect x="${wx}" y="${hz + 120}" width="${ww}" height="${wh}" fill="#0a0a0c"/></g>`;
    // the siren tower with the red flash
    v += `<g transform="translate(${wx + ww * 0.2},${hz + 60})"><path d="M-30,0L-8,-220H8L30,0" fill="none" stroke="#0e0c10" stroke-width="10"/><rect x="-26" y="-250" width="52" height="34" fill="#0e0c10"/><circle cy="-260" r="${f1(40 + 90 * siren)}" fill="url(#dsRed)" opacity="${f1(siren)}"/></g>`;
    // the haze pressed against the glass
    if (press > 0) v += `<g opacity="${f1(press)}">${puffs(r, 22, wx, wx + ww, wy + wh * 0.25, wy + wh, 120, 260, "dsPlume", 0.9)}</g>`;
    put(L.set, `<defs><clipPath id="dsWinClip${o.id || ""}"><rect x="${wx}" y="${wy}" width="${ww}" height="${wh}"/></clipPath></defs><g clip-path="url(#dsWinClip${o.id || ""})">${v}</g>`);
    // the room: wall, window frame with sliding panes (closed), curtains, the AC over the window, a bed, a desk lamp off
    let s = `<path d="M-900,-600H2000V2800H-900Z M${wx},${wy}h${ww}v${wh}h${-ww}Z" fill="#2a3a4a" fill-rule="evenodd"/>`;
    s += `<rect x="${wx - 20}" y="${wy - 20}" width="${ww + 40}" height="${wh + 40}" fill="none" stroke="#d8d4c8" stroke-width="26" ${""}/><rect x="${wx - 20}" y="${wy - 20}" width="${ww + 40}" height="${wh + 40}" fill="none" stroke="${INK}" stroke-width="4"/>
      <path d="M${wx + ww / 2},${wy}V${wy + wh}" stroke="#d8d4c8" stroke-width="18"/><path d="M${wx + ww / 2},${wy}V${wy + wh}" stroke="${INK}" stroke-width="3"/>
      <path d="M${wx + 30},${wy + 40}L${wx + 140},${wy + 200}" stroke="#ffffff" stroke-width="8" opacity=".12"/><path d="M${wx + ww / 2 + 40},${wy + 40}L${wx + ww / 2 + 160},${wy + 220}" stroke="#ffffff" stroke-width="8" opacity=".12"/>`;
    s += `<path d="M${wx - 120},${wy - 60}Q${wx - 40},${wy + wh / 2} ${wx - 100},${wy + wh + 120}H${wx + 10}Q${wx + 40},${wy + wh / 2} ${wx + 10},${wy - 60}Z" fill="#6a3a5a" ${OUT(4)}/><path d="M${wx + ww + 120},${wy - 60}Q${wx + ww + 40},${wy + wh / 2} ${wx + ww + 100},${wy + wh + 120}H${wx + ww - 10}Q${wx + ww - 40},${wy + wh / 2} ${wx + ww - 10},${wy - 60}Z" fill="#6a3a5a" ${OUT(4)}/>`;
    // AC
    const ax = o.acX ?? wx + ww / 2, ay = o.acY ?? wy - 150;
    s += `<g transform="translate(${ax},${ay})"><rect x="-300" y="-70" width="600" height="140" rx="30" fill="#f2f0ea" ${OUT(5)}/><path d="M-280,40H280" stroke="#cfcac0" stroke-width="6"/><rect x="-270" y="44" width="540" height="18" rx="8" fill="#a8a49a"/>
      <circle cx="230" cy="-30" r="8" fill="${o.acOn ? "#5aff7a" : "#3a4a3a"}"/>${o.acOn ? `<circle cx="230" cy="-30" r="22" fill="#5aff7a" opacity=".3"/>` : ""}<text x="-250" y="-22" font-family="sans-serif" font-size="22" fill="#a8a49a">❄</text></g>`;
    // floor + bed foot
    s += `<path d="M-900,1500H2000V2800H-900Z" fill="#3a2e28"/>${Array.from({ length: 10 }, (_, k) => `<path d="M-900,${1520 + k * 60}H2000" stroke="#2e241e" stroke-width="4"/>`).join("")}`;
    s += `<g transform="translate(${o.bedX ?? 820},1560)"><rect x="-260" y="-120" width="520" height="140" rx="16" fill="#e8e0d0" ${OUT(5)}/><rect x="-260" y="-150" width="520" height="40" rx="14" fill="#8ab0d8" ${OUT(4)}/><rect x="-270" y="20" width="540" height="40" fill="#5a3a28" ${OUT(4)}/></g>`;
    put(L.set, s);
  };
})();
