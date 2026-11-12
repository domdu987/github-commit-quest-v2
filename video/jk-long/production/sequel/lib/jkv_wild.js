// สกิลจอมโกหก ภาค 2 "อัศวินถังไม้" · detailed hand-drawn sets for the sequel (owner 12 Nov: "ทำฉากให้ละเอียดกว่านี้"). Ground for people: y 1400.
// Everything is SVG: gradients for light (key light from the upper left), patterns for texture, far things paler and bluer. No fal images.
//   Sets.jkForest(L, o)  the old forest on the way to the mountain: misty trunk rows, mossy trunks with bark and shelf fungus, ferns, red mushrooms,
//                        a dirt path with leaf litter and roots, a signpost "ภูเขามังกร" (x 1560), god rays and sun flecks.
//                        o.dim: deeper in, cooler and darker · o.prints: the dragon's footprints along the path · o.trap: x of a rope snare on the path
//                        o.canopy: a big tree crown over x (for the giant stuck in the treetop: branches in front of y 300…700)
//   Sets.jkCave(L, o)    the cave mouth on the mountain top: a sea of clouds below, snowy ranges, rock spires, the cliff face with strata, a huge arch
//                        (mouth centre o.mx ?? 1250, width 980, top y 520), stalactite teeth, claw gouges, scorch marks, bones, a gold hoard glinting inside.
//                        o.dragon {x, y, s, flip}: the dragon awake in front of the mouth (behind the cast) · o.dusk: evening light
//   Sets.jkTownNight(L, o) the town at night: jkTown at dusk, then a night sky (stars, moon) over it
//   JKW.swarm(tl, layer, t0, dur, o)  a flock of dragon silhouettes crossing the sky (o.n, o.x0, o.y0, o.toward [x, y])
//   JKD.dress.jkForest / jkCave: life (motes, falling leaves, breathing rays, drifting cloud banks, glinting hoard)
(function () {
  if (window.JKW) return;
  const f = (v) => (+v).toFixed(1);
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const NS = "http://www.w3.org/2000/svg";
  const T = (x, y, size, text, o = {}) => `<text x="${f(x)}" y="${f(y)}" text-anchor="${o.anchor || "middle"}" font-family="Kanit" font-weight="${o.w || 800}" font-size="${size}" fill="${o.fill || "#222"}"${o.op ? ` opacity="${o.op}"` : ""}>${text}</text>`;

  Sets.DEFS += `
    <linearGradient id="jw_skyF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9cc49a"/><stop offset=".45" stop-color="#d6e6b4"/><stop offset=".8" stop-color="#f6eec4"/><stop offset="1" stop-color="#e8e0b0"/></linearGradient>
    <linearGradient id="jw_skyFd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e4a44"/><stop offset=".5" stop-color="#5a7a62"/><stop offset="1" stop-color="#8aa078"/></linearGradient>
    <linearGradient id="jw_hazeF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef2d4" stop-opacity="0"/><stop offset=".6" stop-color="#eef2d4" stop-opacity=".7"/><stop offset="1" stop-color="#eef2d4" stop-opacity=".2"/></linearGradient>
    <linearGradient id="jw_bark" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a6a4c"/><stop offset=".35" stop-color="#6e5038"/><stop offset=".75" stop-color="#4a3424"/><stop offset="1" stop-color="#2e2016"/></linearGradient>
    <linearGradient id="jw_barkM" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a7058"/><stop offset=".4" stop-color="#5e5442"/><stop offset="1" stop-color="#3a3428"/></linearGradient>
    <linearGradient id="jw_leafG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ab85a"/><stop offset=".5" stop-color="#4e8a3e"/><stop offset="1" stop-color="#2a5a2e"/></linearGradient>
    <linearGradient id="jw_floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a9a5a"/><stop offset=".3" stop-color="#6e7e44"/><stop offset="1" stop-color="#3e4a26"/></linearGradient>
    <linearGradient id="jw_path" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8c094"/><stop offset=".5" stop-color="#c0a272"/><stop offset="1" stop-color="#9a7c52"/></linearGradient>
    <linearGradient id="jw_ray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff8d0" stop-opacity=".75"/><stop offset="1" stop-color="#fff8d0" stop-opacity="0"/></linearGradient>
    <radialGradient id="jw_fleck"><stop offset="0" stop-color="#fff6c0" stop-opacity=".75"/><stop offset=".6" stop-color="#fff0a0" stop-opacity=".25"/><stop offset="1" stop-color="#fff0a0" stop-opacity="0"/></radialGradient>
    <radialGradient id="jw_moss"><stop offset="0" stop-color="#8ab84a"/><stop offset="1" stop-color="#5a8a34" stop-opacity="0"/></radialGradient>
    <pattern id="jw_litter" width="120" height="60" patternUnits="userSpaceOnUse"><rect width="120" height="60" fill="none"/>
      <path d="M10,12q8,-8 16,0q-8,6 -16,0Z" fill="#b8843a" opacity=".55"/><path d="M60,8q7,-9 14,1q-8,5 -14,-1Z" fill="#9a6a2e" opacity=".5"/><path d="M92,30q9,-6 15,2q-9,4 -15,-2Z" fill="#c89a48" opacity=".5"/>
      <path d="M30,40q8,-7 14,1q-7,5 -14,-1Z" fill="#7a8a3a" opacity=".5"/><path d="M78,50q7,-8 13,0q-7,5 -13,0Z" fill="#a8742e" opacity=".45"/><circle cx="48" cy="26" r="2.4" fill="#6a5a3a" opacity=".5"/><circle cx="108" cy="12" r="2" fill="#5a4a2e" opacity=".5"/>
      <path d="M4,52l6,-8M20,26l5,-7M100,44l4,-7" stroke="#5a6a2e" stroke-width="2" opacity=".5"/></pattern>
    <pattern id="jw_barkT" width="40" height="90" patternUnits="userSpaceOnUse"><path d="M6,0q4,22 0,45t2,45M22,0q-3,30 2,50t-2,40M34,0q3,20 -1,44t3,46" stroke="#2a1a10" stroke-width="2.4" fill="none" opacity=".45"/>
      <path d="M12,10q3,14 0,26M28,50q2,12 0,24" stroke="#c09a70" stroke-width="1.6" fill="none" opacity=".35"/></pattern>
    <linearGradient id="jw_skyM" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a8ad0"/><stop offset=".45" stop-color="#9cc0ea"/><stop offset=".8" stop-color="#ffe0b8"/><stop offset="1" stop-color="#ffc898"/></linearGradient>
    <linearGradient id="jw_skyMd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a7a"/><stop offset=".45" stop-color="#9a6a9a"/><stop offset=".8" stop-color="#ffa070"/><stop offset="1" stop-color="#ff8a5a"/></linearGradient>
    <linearGradient id="jw_rock" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b8a48c"/><stop offset=".5" stop-color="#8e7c68"/><stop offset="1" stop-color="#5a4c40"/></linearGradient>
    <linearGradient id="jw_rockD" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a8874"/><stop offset=".6" stop-color="#6e5e50"/><stop offset="1" stop-color="#4a3e36"/></linearGradient>
    <linearGradient id="jw_ledge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b4a084"/><stop offset=".35" stop-color="#94806a"/><stop offset="1" stop-color="#5a4a3c"/></linearGradient>
    <radialGradient id="jw_mouth" cx=".5" cy=".75" r=".75"><stop offset="0" stop-color="#3a1a0e"/><stop offset=".55" stop-color="#1a0c08"/><stop offset="1" stop-color="#0a0606"/></radialGradient>
    <radialGradient id="jw_hoard"><stop offset="0" stop-color="#ffd860" stop-opacity=".9"/><stop offset=".5" stop-color="#ff9a30" stop-opacity=".35"/><stop offset="1" stop-color="#ff7a20" stop-opacity="0"/></radialGradient>
    <radialGradient id="jw_scorch"><stop offset="0" stop-color="#1a1210" stop-opacity=".7"/><stop offset=".6" stop-color="#2a1a14" stop-opacity=".3"/><stop offset="1" stop-color="#2a1a14" stop-opacity="0"/></radialGradient>
    <linearGradient id="jw_cloudB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#f4eef2"/><stop offset="1" stop-color="#d8d0e4"/></linearGradient>
    <linearGradient id="jw_snow" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#eef2fa"/><stop offset="1" stop-color="#b8c4dc"/></linearGradient>
    <linearGradient id="jw_nightSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1030"/><stop offset=".55" stop-color="#1e2858"/><stop offset=".85" stop-color="#3a3a6a"/><stop offset="1" stop-color="#6a4a6a"/></linearGradient>
    <radialGradient id="jw_moonG"><stop offset="0" stop-color="#fff8dc" stop-opacity=".7"/><stop offset=".4" stop-color="#d8e0ff" stop-opacity=".18"/><stop offset="1" stop-color="#d8e0ff" stop-opacity="0"/></radialGradient>`;

  // ---------------- forest pieces ----------------
  const fern = (x, y, s, c = "#3e7a34", hi = "#7ab84e", flip = 1) => { let h = ""; for (let k = 0; k < 7; k++) { const a = -80 + k * 26, L = 120 - Math.abs(k - 3) * 14;
      const ex = Math.cos((a - 90) * Math.PI / 180) * L, ey = Math.sin((a - 90) * Math.PI / 180) * L;
      h += `<path d="M0,0Q${f(ex * 0.3)},${f(ey * 0.8)} ${f(ex)},${f(ey)}" stroke="${c}" stroke-width="6" fill="none" stroke-linecap="round"/>`;
      for (let j = 1; j < 7; j++) { const u = j / 7, px = ex * u * 0.9 + ex * 0.1 * u * u, py = ey * u * (0.9 + 0.1 * u) + ey * 0.0, w = 20 * (1 - u * 0.7);
        h += `<path d="M${f(px)},${f(py)}l${f(-ey / L * w)},${f(ex / L * w - 6)}M${f(px)},${f(py)}l${f(ey / L * w)},${f(-ex / L * w - 6)}" stroke="${j % 2 ? c : hi}" stroke-width="5" stroke-linecap="round"/>`; } }
    return `<g transform="translate(${f(x)},${f(y)}) scale(${f(s * flip)},${f(s)})">${h}</g>`; };
  const shroom = (x, y, s, c = "#d83a2e") => `<g transform="translate(${f(x)},${f(y)}) scale(${f(s)})"><ellipse cx="0" cy="2" rx="26" ry="5" fill="#000" opacity=".25"/><path d="M-7,0Q-9,-26 -5,-34H5Q9,-26 7,0Z" fill="#f4ead6"/><path d="M2,-34Q8,-20 7,0" stroke="#c8b898" stroke-width="3" fill="none"/>
    <path d="M-26,-30Q-24,-62 0,-64Q24,-62 26,-30Q0,-38 -26,-30Z" fill="${c}"/><path d="M-20,-40Q-14,-56 0,-58" stroke="#fff" stroke-width="4" fill="none" opacity=".35" stroke-linecap="round"/>
    <circle cx="-11" cy="-48" r="4.5" fill="#fff6e8"/><circle cx="7" cy="-54" r="3.6" fill="#fff6e8"/><circle cx="14" cy="-40" r="3" fill="#fff6e8"/><circle cx="-2" cy="-40" r="2.6" fill="#fff6e8"/></g>`;
  const tuft = (x, y, s, c = "#5a8a34") => `<g transform="translate(${f(x)},${f(y)}) scale(${f(s)})"><path d="M-16,0Q-20,-30 -26,-44Q-10,-26 -6,0ZM-4,0Q-4,-40 2,-58Q6,-30 6,0ZM6,0Q14,-28 26,-40Q16,-16 14,0Z" fill="${c}"/><path d="M-2,-4Q0,-36 2,-54" stroke="#a8d070" stroke-width="2" fill="none" opacity=".6"/></g>`;
  const flower = (x, y, c) => `<g transform="translate(${f(x)},${f(y)})"><path d="M0,0V-20" stroke="#4a7a2e" stroke-width="3"/>${[0, 72, 144, 216, 288].map((a) => `<ellipse cx="0" cy="-27" rx="4" ry="7" fill="${c}" transform="rotate(${a} 0 -20)"/>`).join("")}<circle cy="-20" r="3.5" fill="#f6d36a"/></g>`;
  const stone = (x, y, w, h) => `<g transform="translate(${f(x)},${f(y)})"><ellipse cx="4" cy="3" rx="${f(w * 0.55)}" ry="${f(h * 0.22)}" fill="#000" opacity=".25"/><path d="M${f(-w / 2)},0Q${f(-w / 2)},${f(-h)} 0,${f(-h)}Q${f(w / 2)},${f(-h)} ${f(w / 2)},0Z" fill="#9a9488"/>
    <path d="M${f(-w / 2 + 6)},${f(-h * 0.35)}Q${f(-w / 3)},${f(-h * 0.92)} ${f(w * 0.05)},${f(-h * 0.95)}" stroke="#d8d2c4" stroke-width="4" fill="none" opacity=".7" stroke-linecap="round"/><path d="M${f(-w / 2)},0Q${f(-w / 2)},${f(-h * 0.5)} ${f(-w * 0.2)},${f(-h * 0.8)}" fill="none"/>
    <ellipse cx="${f(-w * 0.1)}" cy="${f(-h * 0.92)}" rx="${f(w * 0.3)}" ry="${f(h * 0.14)}" fill="#6a9a3a" opacity=".85"/></g>`;
  // a big trunk: bark gradient + texture, root flare, moss, a knot, shelf fungus
  const trunk = (x, top, w, o = {}) => { const b = 1420 + (o.dy || 0), g = o.grad || "jw_bark";
    return `<g transform="translate(${f(x)},0)"><path d="M${f(-w / 2)},${top}L${f(-w / 2 - 6)},${b - 160}Q${f(-w / 2 - 40)},${b - 30} ${f(-w / 2 - 110)},${b}H${f(w / 2 + 110)}Q${f(w / 2 + 40)},${b - 30} ${f(w / 2 + 6)},${b - 160}L${f(w / 2)},${top}Z" fill="url(#${g})"/>
      <path d="M${f(-w / 2)},${top}L${f(-w / 2 - 6)},${b - 160}Q${f(-w / 2 - 40)},${b - 30} ${f(-w / 2 - 110)},${b}H${f(w / 2 + 110)}Q${f(w / 2 + 40)},${b - 30} ${f(w / 2 + 6)},${b - 160}L${f(w / 2)},${top}Z" fill="url(#jw_barkT)"/>
      <path d="M${f(-w / 2 + 8)},${top}V${b - 170}" stroke="#c8a47a" stroke-width="5" opacity=".35"/>
      <path d="M${f(-w / 2 - 70)},${b}Q${f(-w / 2 - 20)},${b - 60} ${f(-w * 0.1)},${b - 40}" stroke="#3a2818" stroke-width="10" fill="none" opacity=".5"/><path d="M${f(w / 2 + 80)},${b}Q${f(w / 2)},${b - 70} ${f(w * 0.15)},${b - 50}" stroke="#2a1a10" stroke-width="10" fill="none" opacity=".5"/>
      <ellipse cx="${f(-w * 0.18)}" cy="${b - 120}" rx="${f(w * 0.42)}" ry="70" fill="url(#jw_moss)" opacity=".8"/><ellipse cx="${f(-w * 0.3)}" cy="${b - 300}" rx="${f(w * 0.2)}" ry="90" fill="url(#jw_moss)" opacity=".55"/>
      ${o.knot !== false ? `<ellipse cx="${f(w * 0.12)}" cy="${b - 520}" rx="${f(w * 0.12)}" ry="${f(w * 0.17)}" fill="#2a1a10"/><ellipse cx="${f(w * 0.12)}" cy="${b - 520}" rx="${f(w * 0.16)}" ry="${f(w * 0.22)}" fill="none" stroke="#9a7650" stroke-width="5" opacity=".6"/>` : ""}
      ${o.fungus !== false ? [[w / 2 - 6, b - 380, 1], [w / 2 - 4, b - 330, 0.75], [-w / 2 + 4, b - 640, -0.9]].map(([fx, fy, sc]) => `<g transform="translate(${f(fx)},${fy}) scale(${sc},${Math.abs(sc)})"><path d="M0,0Q40,-18 64,0Q40,10 0,8Z" fill="#e8c890"/><path d="M4,2Q36,-10 58,0" stroke="#fff4d8" stroke-width="3" fill="none" opacity=".7"/><path d="M2,8Q36,12 60,2" stroke="#9a7444" stroke-width="3" fill="none"/></g>`).join("") : ""}
      ${o.vine ? `<path d="M${f(-w * 0.3)},${top}Q${f(w * 0.4)},${top + 300} ${f(-w * 0.2)},${top + 620}T${f(w * 0.1)},${b - 200}" stroke="#4a7a30" stroke-width="7" fill="none"/>${[0.2, 0.35, 0.5, 0.65, 0.8].map((u, k) => `<ellipse cx="${f(-w * 0.2 + (k % 2 ? 26 : -20))}" cy="${f(top + (b - 200 - top) * u)}" rx="14" ry="8" fill="#6aa040" transform="rotate(${k % 2 ? 30 : -30} ${f(-w * 0.2 + (k % 2 ? 26 : -20))} ${f(top + (b - 200 - top) * u)})"/>`).join("")}` : ""}</g>`; };
  // a crown of leaves (clusters with lit tops and shaded bellies)
  const crown = (cx, cy, rx, ry, r, dark = false) => { let h = ""; for (let k = 0; k < 16; k++) { const a = r() * Math.PI * 2, d = Math.sqrt(r()), x = cx + Math.cos(a) * rx * d, y = cy + Math.sin(a) * ry * d * 0.8, s = 70 + r() * 70;
      h += `<g transform="translate(${f(x)},${f(y)})"><ellipse rx="${f(s)}" ry="${f(s * 0.72)}" fill="${dark ? "#1e3a22" : "#2e5a2e"}"/><ellipse cy="${f(-s * 0.2)}" rx="${f(s * 0.82)}" ry="${f(s * 0.5)}" fill="${dark ? "#2a4a2a" : "#4a7e3a"}"/><ellipse cx="${f(-s * 0.2)}" cy="${f(-s * 0.36)}" rx="${f(s * 0.45)}" ry="${f(s * 0.24)}" fill="${dark ? "#3a5a34" : "#7aae4e"}" opacity=".8"/>${[...Array(9)].map((_, j) => { const a2 = j * 0.7 + r(), d2 = 0.35 + r() * 0.55; return `<path d="M${f(Math.cos(a2) * s * d2)},${f(Math.sin(a2) * s * d2 * 0.7)}q8,-12 18,-2q-8,10 -18,2Z" fill="${j % 2 ? (dark ? "#2a4a2a" : "#5a9a42") : (dark ? "#16301c" : "#24502a")}"/>`; }).join("")}</g>`; }
    return h; };

  Sets.jkForest = (L, o = {}) => {
    const id = o.id || "jf", r = mk(o.seed || 23), dim = !!o.dim;
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="${dim ? "#4a6a5a" : "#e8ecc0"}"/><rect x="-3000" y="-900" width="8000" height="2300" fill="url(#${dim ? "jw_skyFd" : "jw_skyF"})"/>
      <circle cx="700" cy="120" r="420" fill="#fffbe0" opacity="${dim ? 0.18 : 0.55}"/>`);
    // far: two rows of misty trunks with crowns, haze between
    let far = "";
    for (let row = 0; row < 2; row++) { const col = row ? (dim ? "#3a5e52" : "#6e9a7e") : (dim ? "#4a6e62" : "#8eb494"), cc = row ? (dim ? "#2e5246" : "#5e8e6a") : (dim ? "#3e6252" : "#7eaa82");
      for (let x = -2600 + row * 90; x < 3800; x += 150 + r() * 120) { const w = 26 + r() * 30 + row * 14;
        far += `<rect x="${f(x)}" y="-400" width="${f(w)}" height="${f(1600 + row * 40)}" fill="${col}"/><path d="M${f(x + w * .3)},-300V1150M${f(x + w * .7)},-200V1120" stroke="${cc}" stroke-width="3" opacity=".6"/>`;
        far += `<ellipse cx="${f(x + w / 2)}" cy="${f(-120 + r() * 260)}" rx="${f(150 + r() * 90)}" ry="${f(120 + r() * 70)}" fill="${cc}"/>`; }
      far += `<rect x="-3000" y="${row ? 700 : 500}" width="8000" height="${row ? 700 : 900}" fill="url(#jw_hazeF)" opacity="${dim ? 0.22 : 0.45}"/>`; }
    put(L.far, far + `<rect x="-3000" y="1150" width="8000" height="300" fill="${dim ? "#4e6a48" : "#9aae78"}"/>`);
    // mid: trunks with crowns, ferns and a fallen log
    let mid = "";
    for (let x = -2300; x < 3600; x += 330 + r() * 220) { if (x > 300 && x < 1100) continue; const w = 60 + r() * 40;
      mid += trunk(x, -500, w, { dy: -170, grad: "jw_barkM", knot: r() > 0.6, fungus: r() > 0.6, vine: r() > 0.7 }); mid += crown(x, -260, 260, 160, r, dim); }
    mid += `<g transform="translate(-520,1230)"><path d="M-260,0Q-250,-60 -180,-66L220,-58Q270,-50 268,0Z" fill="url(#jw_barkM)"/><ellipse cx="240" cy="-30" rx="28" ry="32" fill="#c8a478"/><ellipse cx="240" cy="-30" rx="18" ry="22" fill="none" stroke="#8a6a44" stroke-width="3"/>
      <ellipse cx="-40" cy="-64" rx="190" ry="16" fill="#6a9a3a"/>${shroom(-120, -60, 0.55, "#e8b040")}${shroom(-80, -62, 0.4, "#e8b040")}</g>`;
    for (let k = 0; k < 14; k++) { const x = -2200 + k * 420 + r() * 120; if (x > 380 && x < 1050) continue; mid += fern(x, 1215, 0.7 + r() * 0.3, dim ? "#2e5a2a" : "#4a7e38", dim ? "#4a7a3a" : "#8ac05a", r() > 0.5 ? 1 : -1); }
    put(L.mid, mid);
    // set: the floor, the path, the big near trunks, details
    let s = `<rect x="-3000" y="1190" width="8000" height="1600" fill="url(#jw_floor)"/><rect x="-3000" y="1190" width="8000" height="1600" fill="url(#jw_litter)"/>
      <path d="M560,1190Q700,1188 840,1190Q1100,1400 1560,1700Q1800,1860 2100,2400H-700Q-200,1900 120,1680Q420,1460 560,1190Z" fill="url(#jw_path)"/>
      <path d="M560,1190Q700,1188 840,1190Q1100,1400 1560,1700Q1800,1860 2100,2400H-700Q-200,1900 120,1680Q420,1460 560,1190Z" fill="url(#jw_litter)" opacity=".55"/>
      <path d="M600,1200Q450,1460 140,1690M800,1200Q1080,1420 1540,1710" stroke="#7a6a3a" stroke-width="6" fill="none" opacity=".35"/>`;
    // roots crossing the path, wheel-rut lines, pebbles
    for (let k = 0; k < 6; k++) { const y = 1260 + k * 90, x = 300 + r() * 600; s += `<path d="M${f(x - 260)},${y}Q${f(x)},${y - 26} ${f(x + 280)},${y + 10}" stroke="#6a4a2c" stroke-width="${9 + k * 2}" fill="none" stroke-linecap="round" opacity=".75"/><path d="M${f(x - 200)},${y - 5}Q${f(x)},${y - 30} ${f(x + 200)},${y + 2}" stroke="#a8845a" stroke-width="3" fill="none" opacity=".5"/>`; }
    for (let k = 0; k < 40; k++) { const x = -600 + r() * 2600, y = 1210 + r() * 700; s += stone(x, y, 18 + r() * 30, 10 + r() * 16); }
    for (let k = 0; k < 46; k++) { const x = -2400 + r() * 5600, y = 1200 + r() * 600; if (x > 200 && x < 1500 && y > 1300) continue; s += tuft(x, y, 0.8 + r() * 0.8, r() > 0.5 ? "#5a8a34" : "#6e9a3e"); }
    for (let k = 0; k < 18; k++) { const x = -1800 + r() * 4800, y = 1220 + r() * 420; if (x > 300 && x < 1400) continue; s += flower(x, y, ["#f4f0ff", "#f6d36a", "#d888c8", "#9ac8f4"][k % 4]); }
    for (let k = 0; k < 9; k++) { const x = [-900, -760, 1700, 1820, 2300, -1400, 2600, -300, 1500][k], y = 1230 + (k % 3) * 40; s += shroom(x, y, 0.7 + (k % 3) * 0.25); }
    // near trunks framing the path (far left and far right of the wide frame)
    s += trunk(-1050, -800, 210, { vine: true }) + trunk(2250, -800, 240, { knot: true }) + trunk(-1700, -800, 160, { fungus: false });
    s += crown(-1050, -560, 420, 260, r, dim) + crown(2250, -560, 460, 260, r, dim);
    // the signpost
    s += `<g transform="translate(1560,1300)"><ellipse cx="6" cy="4" rx="40" ry="8" fill="#000" opacity=".3"/><rect x="-9" y="-300" width="18" height="300" fill="url(#jw_bark)"/>
      <g transform="translate(10,-250) rotate(-4)"><path d="M-10,-34H200L236,0L200,34H-10Z" fill="#b88a52"/><path d="M-10,-34H200L236,0L200,34H-10Z" fill="url(#jkv_wood)" opacity=".5"/><path d="M-10,-34H200L236,0" stroke="#e8c890" stroke-width="3" fill="none" opacity=".7"/>
        ${T(108, 13, 34, "ภูเขามังกร", { fill: "#3a2410", w: 900 })}</g><g transform="translate(-10,-170) rotate(6)"><path d="M10,-26H-150L-176,0L-150,26H10Z" fill="#a87a48"/>${T(-82, 10, 26, "เมือง", { fill: "#3a2410", w: 900 })}</g>
      <path d="M-30,-60q30,-20 60,0" stroke="#6a9a3a" stroke-width="8" fill="none"/></g>`;
    if (o.prints) for (let k = 0; k < 6; k++) { const x = 620 + k * 150 - (k % 2) * 60, y = 1240 + k * 90, sc = 0.5 + k * 0.17;
      s += `<g transform="translate(${f(x)},${f(y)}) scale(${f(sc)},${f(sc * 0.45)}) rotate(${k % 2 ? -12 : 12})"><ellipse rx="70" ry="90" fill="#6a5434" opacity=".7"/><ellipse rx="56" ry="74" fill="#5a4428" opacity=".6"/>${[-46, 0, 46].map((dx) => `<path d="M${dx},-86l${dx / 4},-56l14,48Z" fill="#4a3620" opacity=".8"/>`).join("")}</g>`; }
    if (o.trap !== undefined) s += `<g id="${id}-trap" transform="translate(${o.trap},1420)"><ellipse rx="150" ry="26" fill="none" stroke="#c8a46a" stroke-width="9"/><ellipse rx="150" ry="26" fill="none" stroke="#8a6a3a" stroke-width="3" stroke-dasharray="8 10"/>
      <path d="M150,0Q260,-120 300,-420" stroke="#c8a46a" stroke-width="8" fill="none"/><path d="M300,-420Q330,-560 260,-700" stroke="#6a4a2c" stroke-width="16" fill="none" stroke-linecap="round"/>${[[-60, 4], [40, -6], [100, 8]].map(([lx, ly]) => `<path d="M${lx},${ly}q10,-14 22,0q-12,8 -22,0Z" fill="#b8843a"/>`).join("")}</g>`;
    // undergrowth band at the foot of the trees (bushes with berries), stumps with rings, a log, more mushrooms and stones
    const bush = (x, y, sc, c1, c2, berry) => { let h = `<g transform="translate(${f(x)},${f(y)}) scale(${f(sc)})">`; for (let k = 0; k < 6; k++) { const bx = -90 + k * 36 + r() * 20, by = -40 - r() * 50, rr = 42 + r() * 26;
        h += `<circle cx="${f(bx)}" cy="${f(by)}" r="${f(rr)}" fill="${c1}"/><circle cx="${f(bx - rr * .25)}" cy="${f(by - rr * .3)}" r="${f(rr * .55)}" fill="${c2}"/>`; }
      if (berry) for (let k = 0; k < 7; k++) h += `<circle cx="${f(-80 + r() * 170)}" cy="${f(-30 - r() * 80)}" r="7" fill="${berry}"/>`; return h + `</g>`; };
    for (let x = -2300; x < 3500; x += 170 + r() * 120) { if (x > 380 && x < 1150) continue; s = bush(x, 1215, 0.8 + r() * 0.5, dim ? "#1e4a2a" : "#2e6a34", dim ? "#2e6a3a" : "#5a9a44", r() > 0.6 ? "#d8443a" : (r() > 0.7 ? "#7a4ac8" : null)) + s; }
    const stump = (x, y, sc) => `<g transform="translate(${f(x)},${f(y)}) scale(${f(sc)})"><path d="M-70,0L-60,-120H60L70,0Z" fill="url(#jw_bark)"/><path d="M-90,0Q-70,-20 -60,-30M90,0Q70,-20 60,-30" stroke="#4a3424" stroke-width="16" fill="none"/>
      <ellipse cy="-120" rx="60" ry="18" fill="#c89a62"/>${[44, 30, 16].map((rr) => `<ellipse cy="-120" rx="${rr}" ry="${rr * .3}" fill="none" stroke="#9a6a3a" stroke-width="3"/>`).join("")}<ellipse cx="-30" cy="-60" rx="30" ry="40" fill="url(#jw_moss)"/>${shroom(40, -4, 0.5, "#e8b040")}</g>`;
    s += stump(-640, 1330, 1) + stump(1880, 1300, 0.85) + stump(2480, 1350, 1.1);
    s += `<g transform="translate(1340,1520) rotate(-4)"><path d="M-300,0Q-290,-70 -220,-74L260,-64Q320,-56 318,0Z" fill="url(#jw_bark)"/><path d="M-300,0Q-290,-70 -220,-74L260,-64Q320,-56 318,0Z" fill="url(#jw_barkT)"/><ellipse cx="290" cy="-32" rx="30" ry="34" fill="#c8a478"/>
      ${[24, 14].map((rr) => `<ellipse cx="290" cy="-32" rx="${rr}" ry="${rr * 1.1}" fill="none" stroke="#8a6a44" stroke-width="3"/>`).join("")}<ellipse cx="-20" cy="-72" rx="220" ry="16" fill="#5a9a3a"/>${shroom(-150, -70, 0.6)}${shroom(-100, -72, 0.45)}${fern(120, -64, 0.5)}</g>`;
    for (let k = 0; k < 14; k++) { const x = -1400 + r() * 4200, y = 1250 + r() * 600; if (x > 300 && x < 1500 && y > 1300) continue; s += shroom(x, y, 0.35 + r() * 0.4, ["#d83a2e", "#e8b040", "#c86ab0"][k % 3]); }
    put(L.set, `<g id="${id}-world">${s}</g>`);
    // fg: hanging leaves at the top corners, dark ferns low at the edges (outside the wide frame's centre)
    let fg = "";
    [[-900, -60, 1], [1950, -40, -1]].forEach(([x, y, d]) => { for (let k = 0; k < 9; k++) fg += `<path d="M${f(x + k * 50 * d)},${f(y)}q${f(10 * d)},${f(140 + k * 22)} ${f(-6 * d)},${f(240 + (k % 3) * 70)}" stroke="#1e3a1e" stroke-width="5" fill="none"/><ellipse cx="${f(x + k * 50 * d - 6 * d)}" cy="${f(y + 240 + (k % 3) * 70)}" rx="16" ry="28" fill="#2a4a24"/>`; });
    fg += fern(-760, 1760, 2.2, "#14281a", "#20402a") + fern(1880, 1780, 2.4, "#14281a", "#20402a", -1);
    let top = `<rect x="-3000" y="-1400" width="8000" height="1560" fill="${dim ? "#0a1610" : "#13261a"}"/>`; for (let x = -2600; x < 3800; x += 120 + r() * 80) { const y = 120 + r() * 160, rr = 110 + r() * 90; top += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rr)}" ry="${f(rr * .7)}" fill="${dim ? "#0a1610" : "#13261a"}"/><ellipse cx="${f(x - 20)}" cy="${f(y + rr * .45)}" rx="${f(rr * .5)}" ry="${f(rr * .25)}" fill="${dim ? "#14261a" : "#1f3a24"}"/>`; }
    for (let k = 0; k < 26; k++) { const x = -2400 + r() * 6000, l = 120 + r() * 260; top += `<path d="M${f(x)},${f(160)}q${f(-10 + r() * 20)},${f(l / 2)} ${f(-6 + r() * 12)},${f(l)}" stroke="${dim ? "#14261a" : "#1f3a24"}" stroke-width="6" fill="none"/><ellipse cx="${f(x)}" cy="${f(160 + l)}" rx="10" ry="16" fill="${dim ? "#1e3a24" : "#2e5a30"}"/>`; }
    fg += `<g class="jwTop">${top}</g>`;
    put(L.fg, `<g class="jwFg">${fg}</g>`);
    // glow: god rays and sun flecks
    const rays = [[260, 0.5], [520, 0.35], [860, 0.45], [1180, 0.3], [-200, 0.3], [1600, 0.25]].map(([x, op], k) => `<path class="jwRay" d="M${x},-300H${x + 110}L${x + 520},1500H${x + 230}Z" fill="url(#jw_ray)" opacity="${f(op * (dim ? 0.5 : 1))}"/>`).join("");
    let fl = ""; for (let k = 0; k < 22; k++) { const x = -800 + r() * 2900, y = 1230 + r() * 560; fl += `<ellipse class="jwFleck" cx="${f(x)}" cy="${f(y)}" rx="${f(40 + r() * 70)}" ry="${f(10 + r() * 14)}" fill="url(#jw_fleck)" opacity="${f(dim ? 0.4 : 0.85)}"/>`; }
    put(L.glow, `<g style="mix-blend-mode:screen">${rays}${fl}</g>`);
    let motes = ""; for (let k = 0; k < 26; k++) motes += `<circle cx="${f(-400 + r() * 2400)}" cy="${f(300 + r() * 1100)}" r="${f(2 + r() * 3.5)}" fill="#fffbd8" opacity="${f(0.4 + r() * 0.5)}"/>`;
    let leaves = ""; for (let k = 0; k < 7; k++) leaves += `<g transform="translate(${f(-200 + k * 300 + r() * 100)},${f(-100 - r() * 300)})"><g class="jwLeaf"><path d="M0,0q10,-14 22,0q-12,8 -22,0Z" fill="${["#c89a3a", "#8ab84a", "#d8763a"][k % 3]}"/></g></g>`;
    put(L.fg, `<g class="jwMotes">${motes}</g>${leaves}`);
    if (o.canopy !== undefined) put(L.fg, `<g id="${id}-canopy">${crown(o.canopy, 320, 360, 200, mk(91), false)}<path d="M${o.canopy - 420},560Q${o.canopy - 100},430 ${o.canopy + 380},520" stroke="#4a3220" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M${o.canopy - 300},380Q${o.canopy},300 ${o.canopy + 300},420" stroke="#5a3e26" stroke-width="26" fill="none" stroke-linecap="round"/></g>`);
  };

  // ---------------- the mountain top and the cave ----------------
  const puffRow = (y, x0, x1, h, r, c1 = "#ffffff", c2 = "#e6dcea") => { let s = ""; for (let x = x0; x < x1; x += 160 + r() * 140) { const w = 220 + r() * 220, hh = h * (0.6 + r() * 0.6);
      s += `<g class="jwPuff"><ellipse cx="${f(x)}" cy="${f(y + hh * 0.1)}" rx="${f(w * 0.6)}" ry="${f(hh * 0.5)}" fill="${c2}"/><ellipse cx="${f(x - w * 0.08)}" cy="${f(y - hh * 0.12)}" rx="${f(w * 0.5)}" ry="${f(hh * 0.5)}" fill="${c1}"/></g>`; } return s; };
  const peak = (x, base, w, h, c, snow = true) => `<g transform="translate(${f(x)},${f(base)})"><path d="M${f(-w / 2)},0L${f(-w * 0.08)},${f(-h)}L${f(w * 0.06)},${f(-h * 0.94)}L${f(w / 2)},0Z" fill="${c}"/><path d="M${f(-w * 0.08)},${f(-h)}L${f(w * 0.06)},${f(-h * 0.94)}L${f(w / 2)},0H${f(w * 0.05)}Z" fill="#000" opacity=".16"/>
    ${snow ? `<path d="M${f(-w * 0.08)},${f(-h)}L${f(-w * 0.2)},${f(-h * 0.7)}L${f(-w * 0.12)},${f(-h * 0.74)}L${f(-w * 0.05)},${f(-h * 0.64)}L${f(0)},${f(-h * 0.76)}L${f(w * 0.1)},${f(-h * 0.68)}L${f(w * 0.06)},${f(-h * 0.94)}Z" fill="url(#jw_snow)"/>` : ""}</g>`;
  Sets.jkCave = (L, o = {}) => {
    const id = o.id || "jc", r = mk(o.seed || 31), dusk = !!o.dusk, mx = o.mx ?? 1250;
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="${dusk ? "#ff9a6a" : "#ffe6c4"}"/><rect x="-3000" y="-1400" width="8000" height="2700" fill="url(#${dusk ? "jw_skyMd" : "jw_skyM"})"/>
      <circle cx="-300" cy="${dusk ? 980 : 260}" r="${dusk ? 150 : 110}" fill="#fff4d0"/><circle cx="-300" cy="${dusk ? 980 : 260}" r="420" fill="#fff0c0" opacity=".3"/>
      ${[[-1200, 120, 520], [400, 40, 700], [1900, 180, 600]].map(([x, y, w]) => `<path d="M${x - w / 2},${y}q${w / 4},-26 ${w / 2},-6t${w / 2},4" stroke="#fff" stroke-width="16" fill="none" opacity=".5" stroke-linecap="round"/>`).join("")}
      ${[[-900, 360, 1.3], [700, 240, 1.0], [2300, 380, 1.4], [-2200, 280, 1.1]].map(([x, y, sc]) => `<g transform="translate(${x},${y}) scale(${sc})"><ellipse cx="0" cy="0" rx="260" ry="80" fill="#b8a8d8"/><ellipse cx="-90" cy="-40" rx="130" ry="80" fill="#c8b8e4"/><ellipse cx="80" cy="-30" rx="150" ry="90" fill="#c4b4e0"/><ellipse cx="0" cy="30" rx="250" ry="40" fill="#fff0d8"/><ellipse cx="-60" cy="22" rx="120" ry="24" fill="#ffe4c0"/></g>`).join("")}`);
    let far = peak(-1600, 1120, 1300, 560, "#8a9ac8") + peak(-500, 1120, 1100, 470, "#7e90c0") + peak(2600, 1120, 1500, 600, "#8a98c4") + peak(3600, 1120, 1100, 420, "#90a0ca");
    far += `<g opacity=".85">${puffRow(1080, -2600, 4000, 160, r)}</g><g transform="translate(-900,1010)" opacity=".55"><path d="M-80,0V-60H-50V-90H-30V-60H30V-100H50V-60H80V0Z" fill="#6a78a8"/><path d="M-50,-90l10,-20l10,20ZM30,-100l10,-24l10,24Z" fill="#6a78a8"/></g>`;
    far += `<g opacity=".95">${puffRow(1180, -2800, 4200, 200, r, "#fffaf6", "#e8dce8")}</g>`;
    put(L.far, far);
    // mid: rock spires on the left, a dead tree, a pine or two
    let mid = "";
    [[-1300, 380, 360], [-900, 560, 260], [-1700, 640, 300]].forEach(([x, top, w]) => { mid += `<path d="M${x - w / 2},1300L${x - w * 0.3},${top + 120}L${x - w * 0.1},${top}L${x + w * 0.15},${top + 40}L${x + w * 0.32},${top + 180}L${x + w / 2},1300Z" fill="url(#jw_rockD)"/>
      ${[0.3, 0.5, 0.7].map((u) => `<path d="M${f(x - w * 0.4)},${f(top + (1300 - top) * u)}q${f(w * 0.4)},-14 ${f(w * 0.8)},6" stroke="#4a3e34" stroke-width="5" fill="none" opacity=".45"/>`).join("")}
      <path d="M${x - w * 0.1},${top}L${x - w * 0.28},${top + 140}" stroke="#d8c8b0" stroke-width="6" opacity=".5"/>`; });
    mid += `<g transform="translate(-700,1200)"><path d="M0,0Q-6,-120 10,-220Q-40,-280 -90,-300M8,-180Q60,-240 110,-250M10,-220Q20,-300 0,-360" stroke="#4a3626" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M-60,-290l-30,-20M90,-246l26,-12" stroke="#4a3626" stroke-width="8" stroke-linecap="round"/></g>`;
    [[-1050, 1250, 1], [-420, 1270, 0.8]].forEach(([x, y, s]) => { mid += `<g transform="translate(${x},${y}) scale(${s})"><rect x="-8" y="-40" width="16" height="40" fill="#4a3420"/>${[0, 1, 2, 3].map((k) => `<path d="M${-70 + k * 12},${-30 - k * 60}L0,${-110 - k * 60}L${70 - k * 12},${-30 - k * 60}Z" fill="${k % 2 ? "#2e5a3a" : "#3a6a44"}"/>`).join("")}</g>`; });
    put(L.mid, mid);
    // set: the cliff face and the arch, the ledge floor
    let s = `<path d="M${mx - 980},1420L${mx - 900},700Q${mx - 860},300 ${mx - 600},120Q${mx - 300},-160 ${mx + 100},-260Q${mx + 600},-300 ${mx + 1100},-140Q${mx + 1700},20 ${mx + 2600},-80V1420Z" fill="url(#jw_rock)"/>`;
    s += `<defs><clipPath id="${id}-cliff"><path d="M${mx - 980},1420L${mx - 900},700Q${mx - 860},300 ${mx - 600},120Q${mx - 300},-160 ${mx + 100},-260Q${mx + 600},-300 ${mx + 1100},-140Q${mx + 1700},20 ${mx + 2600},-80V1420Z"/></clipPath></defs><g clip-path="url(#${id}-cliff)">`;
    for (let gy = -320; gy < 1420; gy += 90) for (let gx = mx - 1000; gx < mx + 2620; gx += 110) { const jx = gx + (r() - 0.5) * 50, jy = gy + (r() - 0.5) * 40, t = r();
      s += `<path d="M${f(jx)},${f(jy)}l${f(110 + r() * 30)},${f(-10 + r() * 20)}l${f(-40 + r() * 30)},${f(90 + r() * 20)}Z" fill="${t < 0.35 ? "#c4b098" : t < 0.7 ? "#9e8a74" : "#7a6858"}" opacity=".55"/>`; }
    s += `</g>`;
    for (let k = 0; k < 9; k++) { const y = -100 + k * 160; s += `<path d="M${f(mx - 920 + k * 20)},${f(y + 200)}Q${f(mx + 300)},${f(y + 150 - r() * 60)} ${f(mx + 2600)},${f(y + 120)}" stroke="#5a4a3c" stroke-width="${f(4 + r() * 4)}" fill="none" opacity=".4"/><path d="M${f(mx - 900 + k * 20)},${f(y + 190)}Q${f(mx + 300)},${f(y + 140 - r() * 60)} ${f(mx + 2600)},${f(y + 112)}" stroke="#d8c8ae" stroke-width="2.5" fill="none" opacity=".35"/>`; }
    for (let k = 0; k < 7; k++) { const x = mx - 800 + r() * 2800, y = -100 + r() * 1100; s += `<path d="M${f(x)},${f(y)}l${f(-20 + r() * 40)},${f(60 + r() * 40)}l${f(-16 + r() * 32)},${f(50 + r() * 40)}" stroke="#3a2e26" stroke-width="4" fill="none" opacity=".6"/>`; }
    for (let k = 0; k < 6; k++) { const x = mx - 850 + r() * 2600, y = 0 + r() * 900; s += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(50 + r() * 60)}" ry="${f(14 + r() * 10)}" fill="#6a8a44" opacity=".6"/>`; }
    // scorch marks around the mouth and claw gouges beside it
    s += `<ellipse cx="${mx}" cy="560" rx="760" ry="340" fill="url(#jw_scorch)"/><ellipse cx="${mx - 420}" cy="1000" rx="300" ry="240" fill="url(#jw_scorch)" opacity=".7"/>`;
    s += `<g transform="translate(${mx + 640},760) rotate(-18)">${[0, 34, 68].map((dx) => `<path d="M${dx},0Q${dx + 10},120 ${dx - 6},260" stroke="#2a1e18" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M${dx + 6},10Q${dx + 16},120 ${dx},250" stroke="#d8c4a4" stroke-width="3" fill="none" opacity=".5"/>`).join("")}</g>`;
    // the arch: dark mouth, a lit rim, stalactite teeth, the hoard glinting deep inside
    s += `<g id="${id}-mouth"><path d="M${mx - 490},1420Q${mx - 520},780 ${mx - 260},600Q${mx},480 ${mx + 260},600Q${mx + 520},780 ${mx + 490},1420Z" fill="url(#jw_mouth)"/>
      <ellipse cx="${mx + 40}" cy="1270" rx="300" ry="70" fill="url(#jw_hoard)"/>
      ${[...Array(26)].map((_, k) => { const x = mx - 230 + (k * 37) % 520, y = 1240 + (k * 13) % 50; return `<ellipse class="jwCoin" cx="${x}" cy="${y}" rx="15" ry="7" fill="${k % 3 ? "#f6c84a" : "#ffe48a"}" stroke="#8a5a10" stroke-width="2"/>`; }).join("")}
      <path d="M${mx - 120},1252l14,-60l18,58ZM${mx + 150},1250l10,-40l14,38Z" fill="#d8a83a"/><circle cx="${mx + 160}" cy="1214" r="6" fill="#fff" class="jwGlint"/><circle cx="${mx - 100}" cy="1200" r="5" fill="#fff" class="jwGlint"/>
      <path d="M${mx - 490},1420Q${mx - 520},780 ${mx - 260},600Q${mx},480 ${mx + 260},600Q${mx + 520},780 ${mx + 490},1420" stroke="#d8c4a4" stroke-width="10" fill="none" opacity=".55"/>
      <path d="M${mx - 470},1420Q${mx - 500},800 ${mx - 250},626Q${mx},510 ${mx + 250},626" stroke="#2a1e18" stroke-width="20" fill="none" opacity=".5"/>
      ${[[-300, 650, 80], [-200, 590, 110], [-90, 556, 70], [20, 548, 130], [130, 566, 90], [240, 610, 110], [330, 680, 70]].map(([dx, y, h]) => `<path d="M${mx + dx - 28},${y - 10}L${mx + dx},${y + h}L${mx + dx + 28},${y - 10}Z" fill="#7a6a58"/><path d="M${mx + dx - 22},${y - 6}L${mx + dx - 2},${y + h - 16}" stroke="#d8c4a4" stroke-width="3" opacity=".5"/>`).join("")}</g>`;
    // the ledge floor: rock with cracks and pebbles, bones, boulders
    s += `<path d="M-3000,1380Q-1200,1350 0,1370Q1200,1390 3600,1360V2600H-3000Z" fill="url(#jw_ledge)"/>`;
    for (let k = 0; k < 9; k++) { const x = -1500 + r() * 4200, y = 1420 + r() * 500; s += `<path d="M${f(x)},${f(y)}l${f(60 + r() * 60)},${f(10 + r() * 20)}l${f(40 + r() * 50)},${f(-14 + r() * 20)}l${f(30 + r() * 40)},${f(16)}" stroke="#4a3c30" stroke-width="4" fill="none" opacity=".6"/>`; }
    for (let k = 0; k < 260; k++) { const x = -1600 + r() * 4800, y = 1400 + r() * 700, rr = 3 + r() * 7; s += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rr * 1.4)}" ry="${f(rr)}" fill="${r() > 0.5 ? "#6a5a4a" : "#c8b498"}"/>`; }
    for (let k = 0; k < 34; k++) s += stone(-1600 + r() * 4600, 1400 + r() * 600, 16 + r() * 28, 9 + r() * 14).replace("#6a9a3a", "#8a7a5a");
    s += `<g transform="translate(${mx - 640},1460)"><ellipse cx="0" cy="8" rx="80" ry="12" fill="#000" opacity=".25"/><path d="M-50,0Q-60,-46 -14,-56Q30,-60 46,-30Q56,-6 40,0Z" fill="#efe6d2"/><circle cx="-12" cy="-30" r="10" fill="#3a2e26"/><circle cx="18" cy="-30" r="10" fill="#3a2e26"/><path d="M-56,-40q-40,-30 -30,-70M42,-44q40,-30 34,-70" stroke="#efe6d2" stroke-width="12" fill="none" stroke-linecap="round"/></g>
      <g transform="translate(${mx + 760},1500) rotate(-8)">${[0, 1, 2, 3, 4].map((k) => `<path d="M${k * 34},0q-30,-50 6,-96" stroke="#efe6d2" stroke-width="11" fill="none" stroke-linecap="round"/>`).join("")}<path d="M-10,-4H150" stroke="#e2d8c2" stroke-width="12" stroke-linecap="round"/></g>`;
    s += `<g transform="translate(${mx - 1150},1420)"><path d="M-140,0Q-150,-130 -40,-160Q90,-170 130,-70Q150,-20 140,0Z" fill="url(#jw_rock)"/><path d="M-120,-60Q-100,-140 -30,-150" stroke="#e8dcc4" stroke-width="6" fill="none" opacity=".6"/><ellipse cx="-20" cy="-150" rx="70" ry="14" fill="#7a9a4a" opacity=".7"/></g>
      <g transform="translate(${mx + 1300},1440)"><path d="M-180,0Q-170,-170 -20,-200Q140,-200 180,-60L170,0Z" fill="url(#jw_rock)"/><path d="M-150,-80Q-130,-170 -30,-188" stroke="#e8dcc4" stroke-width="6" fill="none" opacity=".6"/></g>`;
    const torchPole = (x) => `<g transform="translate(${x},1420)"><rect x="-8" y="-300" width="16" height="300" fill="url(#jw_bark)"/><path d="M-22,-300h44l-8,-30h-28z" fill="#4a3a2a"/><g class="jwFlame"><path d="M0,-420Q-34,-360 -18,-332Q0,-318 18,-332Q34,-360 0,-420Z" fill="#ff7a22"/><path d="M0,-392Q-16,-358 -8,-340Q0,-334 8,-340Q16,-358 0,-392Z" fill="#ffe08a"/></g></g>`;
    s += torchPole(mx - 560) + torchPole(mx + 560);
    s += `<g transform="translate(${mx - 860},1470)"><path d="M-70,0Q-60,-40 -10,-44Q40,-46 60,-10L56,0Z" fill="#9aa2ac"/><path d="M-40,-30h60" stroke="#5a626c" stroke-width="5"/><path d="M-14,-44v-24l10,-8l10,8v24" fill="#8a929c"/>
        <ellipse cx="90" cy="-20" rx="50" ry="40" fill="#a8302a"/><ellipse cx="90" cy="-20" rx="36" ry="28" fill="none" stroke="#e8c048" stroke-width="6"/><path d="M90,-46v52M64,-20h52" stroke="#e8c048" stroke-width="5"/>
        <path d="M-150,0L-120,-160" stroke="#c8ccd4" stroke-width="10"/><path d="M-132,-60h-34" stroke="#8a6a3a" stroke-width="9"/><path d="M180,0L196,-120" stroke="#c8ccd4" stroke-width="9"/><path d="M178,-40h30" stroke="#8a6a3a" stroke-width="8"/></g>`;
    const crystal = (x, y, sc, c) => `<g transform="translate(${x},${y}) scale(${sc})">${[[-30, 60, -14], [0, 100, 4], [26, 70, 16], [50, 40, 26]].map(([dx, h, a]) => `<path d="M${dx - 12},0L${dx - 8},${-h}L${dx},${-h - 18}L${dx + 8},${-h}L${dx + 12},0Z" fill="${c}" transform="rotate(${a} ${dx} 0)"/><path d="M${dx - 4},-6L${dx - 2},${-h + 4}" stroke="#fff" stroke-width="3" opacity=".6" transform="rotate(${a} ${dx} 0)"/>`).join("")}</g>`;
    s += crystal(mx - 380, 1400, 1, "#7ac8e8") + crystal(mx + 420, 1395, 0.8, "#b88ae8") + crystal(mx + 1040, 1440, 1.1, "#7ac8e8");
    s += `<g transform="translate(${mx - 1250},1420)"><rect x="-8" y="-260" width="16" height="260" fill="url(#jw_bark)"/><g transform="rotate(-6 0 -200)"><rect x="-150" y="-280" width="300" height="130" rx="8" fill="#c8a06a"/><rect x="-150" y="-280" width="300" height="130" rx="8" fill="url(#jkv_wood)" opacity=".5"/>
        ${T(0, -230, 40, "ระวังมังกร!", { fill: "#a8241c", w: 900 })}${T(0, -180, 28, "ห้ามโม้ใกล้ถ้ำ", { fill: "#3a2410", w: 800 })}<path d="M120,-268l14,10M-132,-268l14,10" stroke="#5a3a1a" stroke-width="5"/></g></g>`;
    for (let k = 0; k < 18; k++) { const x = mx - 420 + r() * 900, y = 1430 + r() * 160; s += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="13" ry="6" fill="${k % 3 ? "#f6c84a" : "#ffe48a"}" stroke="#8a5a10" stroke-width="2"/>`; }
    s += `<g transform="translate(${mx + 300},1480)"><path d="M-24,0L-30,-46H30L24,0Z" fill="#e8b830"/><ellipse cy="-46" rx="30" ry="8" fill="#ffe48a"/><path d="M-30,-40q-20,6 -18,24" stroke="#e8b830" stroke-width="6" fill="none"/></g>`;
    if (o.dragon) { const d = o.dragon; s += `<g id="${id}-dragon" transform="translate(${d.x ?? mx},${d.y ?? 1380}) scale(${d.flip ? -(d.s ?? 3) : (d.s ?? 3)},${d.s ?? 3})">${JK.dragon(d.fill || "#4f8a5e", { heads: `${id}-dg` })}</g>`; }
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `<g class="jwTop"><path d="M-2600,-1200H700Q600,-100 200,80Q-200,240 -700,200Q-1200,160 -1500,380Q-1900,560 -2600,500Z" fill="#241c26"/><path d="M-1500,-300Q-1300,-380 -1000,-420" stroke="#4a3a40" stroke-width="10" fill="none"/>
      ${[-1300, -900, -500, -100].map((x, k) => `<path d="M${x},${300 - k * 40}l18,${90 + k * 14}l18,${-90 - k * 14}Z" fill="#241c26"/>`).join("")}</g>`);
    
    let wisps = ""; for (let k = 0; k < 4; k++) wisps += `<g class="jwWisp" opacity=".35"><ellipse cx="${-1200 + k * 1100}" cy="${1500 + (k % 2) * 160}" rx="420" ry="60" fill="#ffffff"/></g>`;
    
    put(L.glow, `<g style="mix-blend-mode:screen"><ellipse class="jwHoardGlow" cx="${mx + 40}" cy="1250" rx="420" ry="160" fill="url(#jw_hoard)" opacity=".6"/><circle cx="-300" cy="${dusk ? 980 : 260}" r="700" fill="#fff0c0" opacity=".18"/></g>`);
  };

  // ---------------- the town at night ----------------
  Sets.jkTownNight = (L, o = {}) => {
    Sets.jkTown(L, { ...o, dusk: true });
    const r = mk(o.seed || 47);
    let st = ""; for (let k = 0; k < 90; k++) st += `<circle cx="${f(-2400 + r() * 6000)}" cy="${f(-1200 + r() * 1900)}" r="${f(1.2 + r() * 2.6)}" fill="#fffbe8" opacity="${f(0.4 + r() * 0.6)}" class="jwStar"/>`;
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#0c1030" opacity=".9"/><rect x="-3000" y="-1400" width="8000" height="2600" fill="url(#jw_nightSky)" opacity=".95"/>${st}
      <circle cx="${o.moonX ?? 1500}" cy="${o.moonY ?? 160}" r="520" fill="url(#jw_moonG)"/><circle cx="${o.moonX ?? 1500}" cy="${o.moonY ?? 160}" r="96" fill="#fff6d8"/><circle cx="${(o.moonX ?? 1500) - 26}" cy="${(o.moonY ?? 160) - 18}" r="16" fill="#e8dcb8" opacity=".6"/><circle cx="${(o.moonX ?? 1500) + 30}" cy="${(o.moonY ?? 160) + 24}" r="11" fill="#e8dcb8" opacity=".6"/>`);
    put(L.far, `<rect x="-3000" y="-1400" width="8000" height="3000" fill="#141a44" opacity=".45"/>`);
    put(L.mid, `<rect x="-3000" y="-1400" width="8000" height="3000" fill="#141a44" opacity=".3"/>`);
  };

  // ---------------- a flock of dragon silhouettes ----------------
  const JKW = window.JKW = {};
  JKW.swarm = (tl, layer, t0, dur, o = {}) => { const n = o.n ?? 100, r = mk(o.seed || 5), g = document.createElementNS(NS, "g"); layer.appendChild(g);
    const sym = `jwDrg${o.seed || 5}`; let h = `<defs><g id="${sym}">${JK.dragon("#000", { stroke: o.rim || "#b8c4f4", sw: 16 })}${JK.dragon(o.fill || "#07040e", { detail: false })}</g></defs>`;
    for (let k = 0; k < n; k++) { const d = Math.pow(r(), 1.6), x = (o.x0 ?? 540) + (r() - 0.5) * (o.w ?? 2600) * (0.3 + d), y = (o.y0 ?? 200) + (r() - 0.5) * (o.h ?? 500) * (0.4 + d), s = (o.s ?? 0.16) * (0.35 + d * 1.3);
      h += `<g transform="translate(${f(x)},${f(y)})"><g class="jwFly"><g class="jwFlap"><use href="#${sym}" transform="scale(${f(-s)},${f(s)})" opacity="${f(0.55 + d * 0.45)}"/></g></g></g>`; }
    g.innerHTML = h; g.style.opacity = 0; tl.fromTo(g, { opacity: 0 }, { opacity: 1, duration: 0.6, immediateRender: false }, t0);
    [...g.querySelectorAll(".jwFly")].forEach((el, k) => { tl.fromTo(el, { x: 0, y: 0 }, { x: (o.dx ?? -260) * (0.6 + (k % 5) * 0.12), y: (o.dy ?? 40) + Math.sin(k) * 20, duration: dur, ease: "none", immediateRender: false }, t0);
      tl.fromTo(el.firstChild, { scaleY: 1, svgOrigin: "0 0" }, { scaleY: 0.8, svgOrigin: "0 0", duration: 0.3 + (k % 4) * 0.05, repeat: Math.ceil(dur / 0.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0); });
    return g; };

  // ---------------- life ----------------
  window.JKD = window.JKD || { dress: {} }; JKD.dress = JKD.dress || {};
  const reps = (dur, p) => Math.ceil(dur / p) + 1;
  JKD.dress.jkForest = (L, tl, sh, id) => { const t0 = sh.start, dur = sh.dur;
    [...L.fg.querySelectorAll(".jwMotes circle")].forEach((el, i) => { const p = 4 + (i % 5) * 0.8; tl.fromTo(el, { x: 0, y: 0 }, { x: (i % 2 ? 1 : -1) * (20 + (i % 3) * 10), y: -50 - (i % 4) * 16, duration: p, repeat: reps(dur, p), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0); });
    [...L.fg.querySelectorAll(".jwLeaf")].forEach((el, i) => { const p = 5 + (i % 3); tl.fromTo(el, { y: 0, x: 0, rotation: 0 }, { y: 1900, x: (i % 2 ? 160 : -140), rotation: 540 * (i % 2 ? 1 : -1), duration: p, repeat: reps(dur, p), ease: "none", immediateRender: false }, t0 - (i * 1.3) % p); });
    [...L.glow.querySelectorAll(".jwRay")].forEach((el, i) => { const op = +el.getAttribute("opacity"); tl.fromTo(el, { opacity: op }, { opacity: op * 0.45, duration: 2.2 + (i % 3) * 0.5, repeat: reps(dur, 2.2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0); });
    [...L.glow.querySelectorAll(".jwFleck")].forEach((el, i) => { const op = +el.getAttribute("opacity"); tl.fromTo(el, { opacity: op }, { opacity: op * 0.3, duration: 1.6 + (i % 4) * 0.4, repeat: reps(dur, 1.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 - (i % 5) * 0.3); }); };
  JKD.dress.jkCave = (L, tl, sh, id) => { const t0 = sh.start, dur = sh.dur;
    ["far", "fg"].forEach((n) => [...L[n].querySelectorAll(".jwPuff, .jwWisp")].forEach((el, i) => tl.fromTo(el, { x: 0 }, { x: (i % 2 ? 1 : -1) * (40 + (i % 4) * 14), duration: 7 + (i % 4), repeat: reps(dur, 7), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 - (i % 5) * 0.7)));
    [...L.set.querySelectorAll(".jwGlint")].forEach((el, i) => tl.fromTo(el, { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1.4, transformOrigin: "50% 50%", duration: 0.5, repeat: reps(dur, 1.3), repeatDelay: 0.8, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.6));
    [...L.set.querySelectorAll(".jwFlame")].forEach((el, i) => tl.fromTo(el, { scaleY: 0.9, scaleX: 1.08, transformOrigin: "50% 100%" }, { scaleY: 1.14, scaleX: 0.9, transformOrigin: "50% 100%", duration: 0.16 + i * 0.03, repeat: reps(dur, 0.16), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    [...L.glow.querySelectorAll(".jwHoardGlow")].forEach((el) => tl.fromTo(el, { opacity: 0.6 }, { opacity: 0.35, duration: 1.4, repeat: reps(dur, 1.4), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0)); };
  JKD.dress.jkTownNight = (L, tl, sh, id, o) => { if (JKD.dress.jkTown) JKD.dress.jkTown(L, tl, sh, id, { ...o, dusk: true });
    [...L.sky.querySelectorAll(".jwStar")].forEach((el, i) => { if (i % 3) return; tl.fromTo(el, { opacity: 1 }, { opacity: 0.25, duration: 0.8 + (i % 5) * 0.3, repeat: reps(sh.dur, 0.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, sh.start); }); };
})();
