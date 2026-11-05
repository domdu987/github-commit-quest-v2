// Sets, props, cast and the ghost for "เห็ดปอบ": an Isan village at the first rains, the dry dipterocarp forest (ป่าโคก) where the
// white mushrooms come up by the termite mounds, the kitchen under the stilt house, and a ปอบ that is almost never seen. Same layer
// contract as sets.js (sky / far / mid / set / act / fg, glow above the darkness); seeded RNG only.
//   Rig.CAST: mint (มิ้นท์ 17, from Bangkok) · ton (ต้น 11, her cousin) · yai (ยายคำ 70) · thong (ลุงทองดี 62, the loner next door)
//   Pop.ghost(x, y, s, o)  the ปอบ: a coal-black, thin, hunched figure in one piece, long tangled hair, long nails, green eyes (o.eat: hands at the mouth)
//   Pop.lurk(x, y, s, o)   only its shape against the dark and the two green eyes (#id-eyes); Pop.eyes(x, y, s, id) the eyes alone
//   Pop.mush(x, y, s, o)   a white mushroom (o.cup = the cup at the foot, o.ring, o.egg = still closed, o.lines = lines at the cap's edge)
//   Pop.basket / pot / bowl / stove / lamp / kratip  props
//   Sets.isanVillage   wide: paddies with the first rain in them, stilt houses, a tamarind tree, the road (o.time day | dusk | night)
//   Sets.dryForest     ป่าโคก: straight trunks, small high crowns, red earth, leaf litter, a termite mound (o.mound), mushrooms (o.mush)
//   Sets.underHouse    the kitchen under the house: posts, the floor overhead, a bamboo platform, the clay stove (#id-fire) and the pot (#id-steam)
//   Sets.mushClose     close on the forest floor: mushrooms by the mound, a hand reaching (#id-hand)
//   Sets.mushSection   koi-style diagrams on slate: o.v 1 the two white mushrooms side by side · 2 the folk tests crossed out · 3 boiling does not help
//   Sets.clockCard     chapter card: the kitchen clock, its hands running backwards (#id-hh #id-mm)
//   Sets.popLegend     the legend as an Isan shadow-puppet screen, four panels (y 0/1000/2000/3000)
//   Sets.forestSign    end card: the community-forest sign on a tree with a note pinned to it
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  // the channel's ghosts: coal-black with green eyes
  const PBL = "#0a0c0b", PBL2 = "#171b19", PEYE = ["#7dff6a", "#bfff96", "#f2ffe4"];

  Sets.DEFS += `
    <linearGradient id="ppDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fb4cf"/><stop offset=".6" stop-color="#c8d8de"/><stop offset="1" stop-color="#e6e2cf"/></linearGradient>
    <linearGradient id="ppDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c2d52"/><stop offset=".5" stop-color="#7a5470"/><stop offset=".85" stop-color="#e08a5c"/><stop offset="1" stop-color="#f4bd7a"/></linearGradient>
    <linearGradient id="ppNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070c"/><stop offset=".6" stop-color="#0e1424"/><stop offset="1" stop-color="#1c2232"/></linearGradient>
    <linearGradient id="ppEarth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b0683e"/><stop offset="1" stop-color="#7a4426"/></linearGradient>
    <linearGradient id="ppPaddy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fbcc4"/><stop offset="1" stop-color="#6f9c8a"/></linearGradient>
    <linearGradient id="ppSlate" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3a32"/><stop offset="1" stop-color="#1c2822"/></linearGradient>
    <radialGradient id="ppFire"><stop offset="0" stop-color="#ffe6a0" stop-opacity=".95"/><stop offset=".35" stop-color="#ff9a3a" stop-opacity=".45"/><stop offset="1" stop-color="#ff7a2a" stop-opacity="0"/></radialGradient>
    <radialGradient id="ppLamp"><stop offset="0" stop-color="#ffe2a0" stop-opacity=".85"/><stop offset=".4" stop-color="#ffc06a" stop-opacity=".22"/><stop offset="1" stop-color="#ffc06a" stop-opacity="0"/></radialGradient>
    <radialGradient id="ppGlow"><stop offset="0" stop-color="#7dff6a" stop-opacity=".5"/><stop offset=".4" stop-color="#3dbf5a" stop-opacity=".16"/><stop offset="1" stop-color="#3dbf5a" stop-opacity="0"/></radialGradient>
    <radialGradient id="ppScreen"><stop offset="0" stop-color="#ffe0a8"/><stop offset=".7" stop-color="#e9a457"/><stop offset="1" stop-color="#b8743a"/></radialGradient>
    <linearGradient id="ppCap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbfaf4"/><stop offset="1" stop-color="#e2ddcc"/></linearGradient>`;

  // ---------------- cast ----------------
  Object.assign(Rig.CAST, {
    mint: { // มิ้นท์: 17, up from Bangkok — oversized lilac tee with a heart, light jeans, white sneakers, long hair with bangs and a scrunchie
      skin: "#ecc29c", skinS: "#cfa078", top: "#c8b4e6", topS: "#a894c8", sleeve: "#c8b4e6", sleeveS: "#a894c8", forearm: "#ecc29c", forearmS: "#cfa078",
      pants: "#8fb3d9", pantsS: "#6f93b9", shoe: "#f4f4f0", belt: "#8fb3d9",
      torsoExtra: `<path d="M-8,-420c-10,-14 -30,-2 -16,14l16,14l16,-14c14,-16 -6,-28 -16,-14z" fill="#e85a7a"/>`,
      hair: `<path d="M-52,-560Q-58,-620 0,-622Q58,-620 52,-560Q62,-500 58,-420Q42,-470 42,-540Q40,-560 30,-574Q0,-560 -30,-574Q-40,-560 -42,-540Q-42,-470 -58,-420Q-62,-500 -52,-560Z" fill="#4a2e22" ${OUT}/>
        <path d="M-40,-574Q-10,-556 4,-578Q20,-556 40,-574" stroke="#4a2e22" stroke-width="16" fill="none"/><rect x="34" y="-606" width="20" height="14" rx="6" fill="#e85a7a"/>`,
      face: `<g fill="#e88a8a" opacity=".55"><ellipse cx="-24" cy="-526" rx="8" ry="4"/><ellipse cx="30" cy="-526" rx="8" ry="4"/></g>`,
    },
    ton: { // ต้น: 11, the village's self-declared mushroom expert — red tank top, a woven bag across the chest, khaki shorts, rubber boots, buzz cut
      skin: "#c98e5e", skinS: "#a87048", top: "#d8443a", topS: "#b4342c", sleeve: "#c98e5e", sleeveS: "#a87048", forearm: "#c98e5e", forearmS: "#a87048",
      pants: "#a8946a", pantsS: "#8a7852", shoe: "#2f5a3a", belt: "#a8946a",
      torsoExtra: `<path d="M-40,-468L34,-330" stroke="#3a6a8a" stroke-width="12"/><path d="M-40,-468L34,-330" stroke="#e8d8a8" stroke-width="4" stroke-dasharray="8 8"/>`,
      hair: `<path d="M-48,-556Q-50,-612 0,-614Q50,-612 48,-556Q40,-586 0,-588Q-40,-586 -48,-556Z" fill="#1e1814" ${OUT}/>`,
      face: `<path d="M18,-500l14,-4" stroke="#a87048" stroke-width="3"/>`,
    },
    yai: { // ยายคำ: 70, white lace blouse, a purple woven sarong, a sash over one shoulder, grey bun, lips red from betel
      skin: "#c99a74", skinS: "#a87c58", top: "#efe6d6", topS: "#d2c6b0", sleeve: "#efe6d6", sleeveS: "#d2c6b0", forearm: "#c99a74", forearmS: "#a87c58",
      pants: "#6a2f62", pantsS: "#52244c", shoe: "#c99a74", belt: "#d8a83a",
      torsoExtra: `<path d="M-50,-470L40,-300" stroke="#d8a83a" stroke-width="18"/><path d="M-50,-470L40,-300" stroke="#a8342a" stroke-width="4" stroke-dasharray="10 10"/>`,
      hair: `<circle cx="0" cy="-616" r="26" fill="#b8b4ac" ${OUT}/><path d="M-48,-546Q-52,-610 0,-612Q50,-610 48,-548Q40,-582 0,-586Q-38,-582 -48,-546Z" fill="#b8b4ac" ${OUT}/>`,
      face: `<path d="M-30,-562q8,-3 14,0M14,-562q8,-3 14,0" stroke="#8a6a50" stroke-width="2.5" fill="none"/><path d="M-36,-520q6,8 0,14M40,-520q-6,8 0,14" stroke="#a87c58" stroke-width="2" fill="none"/>
        <path d="M-6,-498h14" stroke="#a8342a" stroke-width="5" stroke-linecap="round"/>`,
    },
    thong: { // ลุงทองดี: 62, lives alone at the forest edge — thin, a faded brown shirt, a checked loincloth at the waist, a woven hat, sunken eyes
      skin: "#a87048", skinS: "#875634", top: "#7a6a50", topS: "#5f523c", sleeve: "#7a6a50", sleeveS: "#5f523c", forearm: "#7a6a50", forearmS: "#5f523c",
      pants: "#2a2a2c", pantsS: "#1c1c1e", shoe: "#a87048", belt: "#c8342a",
      torsoExtra: `<path d="M-46,-312h92" stroke="#e8e0d0" stroke-width="10" stroke-dasharray="12 12"/>`,
      // the woven hat sits down on the head: a low crown just wider than the skull, the brim at the brows, a shadow on the forehead
      hair: `<path d="M-40,-566Q0,-552 40,-566V-580H-40Z" fill="#000" opacity=".16"/>
        <path d="M-52,-578Q-56,-634 0,-637Q56,-634 52,-578Z" fill="#c8a868" ${OUT}/>
        <path d="M-30,-626Q-26,-600 -28,-582M0,-636V-582M30,-626Q26,-600 28,-582" stroke="#a8884a" stroke-width="3" fill="none" opacity=".7"/>
        <path d="M-53,-592Q0,-582 53,-592" stroke="#8a6a38" stroke-width="7" fill="none"/>
        <path d="M-104,-572Q-60,-594 0,-593Q60,-594 104,-572Q60,-562 0,-563Q-60,-562 -104,-572Z" fill="#d4b676" ${OUT}/>`,
      face: `<g fill="#6a4228" opacity=".55"><ellipse cx="-20" cy="-540" rx="14" ry="10"/><ellipse cx="22" cy="-540" rx="14" ry="10"/></g><path d="M-6,-520v12" stroke="#875634" stroke-width="3"/>`,
    },
    boon: { // ป้าบุญ: 50, the neighbour who knows everything — orange blouse, a loincloth on the head, chequered sarong
      skin: "#b88058", skinS: "#98643e", top: "#e88a3a", topS: "#c46e28", sleeve: "#e88a3a", sleeveS: "#c46e28", forearm: "#b88058", forearmS: "#98643e",
      pants: "#3a5a8a", pantsS: "#2c466c", shoe: "#b88058", belt: "#3a5a8a",
      hair: `<path d="M-50,-560Q-50,-616 0,-618Q50,-616 50,-560Z" fill="#2a2420" ${OUT}/><path d="M-54,-580Q0,-640 54,-580Q30,-570 0,-572Q-30,-570 -54,-580Z" fill="#c8342a" ${OUT3}/>`,
      face: `<g fill="#98643e" opacity=".4"><ellipse cx="-24" cy="-526" rx="8" ry="4"/><ellipse cx="30" cy="-526" rx="8" ry="4"/></g>`,
    },
    khem: { // ลุงเข็ม: 60, a neighbour with a torch — white singlet, fisherman trousers, a towel round the neck
      skin: "#a87048", skinS: "#875634", top: "#efe9dc", topS: "#d0c8b8", sleeve: "#a87048", sleeveS: "#875634", forearm: "#a87048", forearmS: "#875634",
      pants: "#4a6a4a", pantsS: "#3a523a", shoe: "#a87048", belt: "#4a6a4a",
      torsoExtra: `<path d="M-40,-470Q0,-430 40,-470V-420" stroke="#8ab4d8" stroke-width="12" fill="none"/>`,
      hair: `<path d="M-48,-556Q-50,-612 0,-614Q50,-612 48,-556Q40,-586 0,-588Q-40,-586 -48,-556Z" fill="#8a8680" ${OUT}/>`,
      face: `<path d="M-30,-562q8,-3 14,0M14,-562q8,-3 14,0" stroke="#6a4228" stroke-width="2.5" fill="none"/>`,
    },
    doc: { // หมอเวรดึก: white coat over green scrubs, stethoscope, hair tied back, glasses
      skin: "#e2b28c", skinS: "#c29470", top: "#f6f6f2", topS: "#d8d8d2", sleeve: "#f6f6f2", sleeveS: "#d8d8d2", forearm: "#f6f6f2", forearmS: "#d8d8d2",
      pants: "#4a9a8a", pantsS: "#3a7a6c", shoe: "#f4f4f0", belt: "#4a9a8a",
      torsoExtra: `<path d="M-14,-470V-330M14,-470V-330" stroke="#4a9a8a" stroke-width="18"/><path d="M-30,-460Q-40,-380 0,-370Q40,-380 30,-460" stroke="#3a3a3a" stroke-width="5" fill="none"/><circle cx="0" cy="-368" r="9" fill="#9aa4a8"/>`,
      hair: `<path d="M-50,-556Q-54,-614 0,-616Q54,-614 50,-556Q44,-584 0,-588Q-44,-584 -50,-556Z" fill="#1e1814" ${OUT}/><circle cx="52" cy="-590" r="16" fill="#1e1814"/>`,
      face: `<g fill="none" stroke="#2a2a2a" stroke-width="4"><rect x="-38" y="-560" width="30" height="22" rx="6"/><rect x="8" y="-560" width="30" height="22" rx="6"/><path d="M-8,-550h16"/></g>`,
    },
  });

  // ---------------- the ปอบ ----------------
  const eyes = (x, y, s, id = "") => `<g ${id ? `id="${id}"` : ""} class="peye" transform="translate(${f1(x)},${f1(y)}) scale(${s})">${[-22, 22].map((cx) => `<circle cx="${cx}" cy="0" r="22" fill="${PEYE[0]}" opacity=".3"/>
    <path d="M${cx - 13},0Q${cx},-10 ${cx + 13},0Q${cx},6 ${cx - 13},0Z" fill="${PEYE[0]}"/><ellipse cx="${cx}" cy="0" rx="4.5" ry="4" fill="${PEYE[2]}"/>`).join("")}</g>`;
  function ghost(x, y, s, o = {}) {
    // crouched on its heels, spine curved, the head low and forward; arms long, fingers longer, nails like thorns
    const hair = Array.from({ length: 11 }, (_, i) => { const dx = -60 + i * 12, len = 140 + (i % 3) * 40;
      return `<path class="phair" d="M${dx},-250C${dx * 1.3},${-250 + len * 0.4} ${dx * 1.5 + (i % 2 ? 14 : -14)},${-250 + len * 0.8} ${dx * 1.4},${-250 + len}" stroke="${PBL}" stroke-width="${12 - (i % 3) * 3}" fill="none" stroke-linecap="round"/>`; }).join("");
    const arm = (sx, hx, hy) => `<path d="M${sx},-200Q${(sx + hx) / 2 + (sx < 0 ? -60 : 60)},${(hy - 200) / 2 + 40} ${hx},${hy}" stroke="${PBL}" stroke-width="22" fill="none" stroke-linecap="round"/>
      ${[-16, -6, 4, 14].map((d) => `<path d="M${hx},${hy}l${d * 1.4},${34 + Math.abs(d)}l${d * 0.4},18" stroke="${PBL}" stroke-width="6" fill="none" stroke-linecap="round"/>`).join("")}`;
    const hands = o.eat ? arm(-40, -30, -250) + arm(40, 30, -240) : arm(-40, -120, -10) + arm(40, 110, -20);
    return `<g ${o.id ? `id="${o.id}"` : ""} class="pbob" transform="translate(${f1(x)},${f1(y)}) scale(${s})" opacity="${o.op ?? 1}">
      <ellipse cx="0" cy="6" rx="150" ry="18" fill="#000" opacity=".35"/>
      <path d="M-90,0Q-120,-60 -70,-110Q-110,-150 -60,-200Q-20,-260 40,-240Q110,-210 100,-130Q130,-70 90,0Z" fill="${PBL}"/>
      <path d="M-40,-10q-30,-60 10,-90M50,-10q30,-50 0,-90" stroke="${PBL2}" stroke-width="6" fill="none"/>
      <ellipse cx="0" cy="-262" rx="54" ry="60" fill="${PBL}"/>${hair}${hands}
      ${eyes(0, -270, 1)}
    </g>`;
  }
  function lurk(x, y, s, o = {}) {
    return `<g ${o.id ? `id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})" opacity="${o.op ?? 1}">
      <path d="M-120,180Q-130,40 -70,-10Q-90,-90 0,-100Q90,-90 70,-10Q130,40 120,180Z" fill="${PBL}" opacity=".92"/>
      ${Array.from({ length: 9 }, (_, i) => `<path d="M${-56 + i * 14},-80q${(i - 4) * 6},70 ${(i - 4) * 10},140" stroke="${PBL}" stroke-width="10" fill="none" stroke-linecap="round"/>`).join("")}
      ${eyes(0, -40, 1, o.id ? `${o.id}-eyes` : "")}</g>`;
  }

  // ---------------- props ----------------
  // a white amanita-type mushroom: cap, gills, stem, ring, the cup at the foot. Origin at its foot.
  function mush(x, y, s, o = {}) {
    const k = o.tilt || 0;
    if (o.egg) return `<g ${o.id ? `id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s}) rotate(${k})"><ellipse cx="0" cy="-46" rx="40" ry="50" fill="url(#ppCap)" ${OUT3}/>
      <path d="M-30,-60q30,-34 60,0" fill="#f8f6ee" stroke="#cfc8b4" stroke-width="3"/><path d="M-40,-30q40,20 80,0" stroke="#cfc8b4" stroke-width="3" fill="none"/></g>`;
    const cup = o.cup === false ? "" : `<path d="M-34,0q-8,-40 6,-56q22,10 44,0q14,16 6,56z" fill="#f2efe4" ${OUT3}/><path d="M-26,-50q4,24 0,44M24,-50q-4,24 0,44" stroke="#cfc8b4" stroke-width="2.5" fill="none"/>`;
    const ring = o.ring === false ? "" : `<path d="M-26,-168q26,26 52,0q-4,18 -26,22q-22,-4 -26,-22z" fill="#f8f6ee" ${OUT3}/>`;
    const lines = o.lines ? Array.from({ length: 9 }, (_, i) => `<path d="M${-96 + i * 24},${-224 + Math.abs(i - 4) * 4}l${(i - 4) * 2},-18" stroke="#c8c0aa" stroke-width="3"/>`).join("") : "";
    return `<g ${o.id ? `id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s}) rotate(${k})">
      <path d="M-18,-40Q-24,-130 -16,-220H16Q24,-130 18,-40Z" fill="#f6f3ea" ${OUT3}/>${ring}${cup}
      <path d="M-110,-222Q-100,-300 0,-312Q100,-300 110,-222Q60,-208 0,-206Q-60,-208 -110,-222Z" fill="url(#ppCap)" ${OUT}/>
      <path d="M-104,-222Q0,-200 104,-222" stroke="#cfc8b4" stroke-width="5" fill="none"/>${lines}
      ${o.bite ? `<path d="M60,-300q24,10 30,40q-20,-6 -34,4z" fill="#f2e6c8" ${OUT3}/>` : ""}</g>`;
  }
  const basket = (x, y, s, o = {}) => `<g ${o.id ? `id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M-110,-150Q-120,-10 -80,0H80Q120,-10 110,-150Z" fill="#c8a066" ${OUT}/>
    ${[0, 1, 2, 3].map((k) => `<path d="M-112,${-130 + k * 34}Q0,${-112 + k * 34} 112,${-130 + k * 34}" stroke="#9a7444" stroke-width="5" fill="none"/>`).join("")}${Array.from({ length: 8 }, (_, k) => `<path d="M${-96 + k * 27},-150V-6" stroke="#9a7444" stroke-width="3"/>`).join("")}
    ${o.full ? `<g>${[-60, -10, 40, 80].map((dx, i) => `<ellipse cx="${dx}" cy="-160" rx="40" ry="26" fill="url(#ppCap)" ${OUT3} transform="rotate(${(i - 1.5) * 14} ${dx} -160)"/>`).join("")}</g>` : ""}
    <path d="M-110,-150Q0,-330 110,-150" stroke="#8a6438" stroke-width="10" fill="none"/></g>`;
  const pot = (x, y, s, o = {}) => `<g ${o.id ? `id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M-130,-150Q-150,-10 -90,0H90Q150,-10 130,-150Z" fill="${o.clay ? "#a8583a" : "#9aa4a8"}" ${OUT}/>
    <ellipse cx="0" cy="-150" rx="136" ry="26" fill="${o.clay ? "#8a4228" : "#7f8a8e"}" ${OUT}/><ellipse cx="0" cy="-150" rx="114" ry="18" fill="${o.curry || "#c8a03a"}"/>
    ${o.curry !== false ? [-50, 0, 46].map((dx) => `<ellipse cx="${dx}" cy="-152" rx="22" ry="8" fill="#f2efe4" ${OUT3}/>`).join("") : ""}
    <path d="M-136,-130h-30M136,-130h30" stroke="${INK}" stroke-width="12" stroke-linecap="round"/></g>`;
  const bowl = (x, y, s, o = {}) => `<g ${o.id ? `id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M-80,-60Q-70,0 0,4Q70,0 80,-60Z" fill="${o.col || "#f2efe4"}" ${OUT}/>
    <ellipse cx="0" cy="-60" rx="80" ry="14" fill="${o.empty ? "#d8d0c0" : "#c8a03a"}" ${OUT3}/>${o.empty ? "" : `<ellipse cx="-16" cy="-62" rx="16" ry="6" fill="#f2efe4"/><ellipse cx="24" cy="-60" rx="14" ry="5" fill="#f2efe4"/>`}</g>`;
  const stove = (x, y, s, o = {}) => `<g ${o.id ? `id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M-110,-180H110L90,0H-90Z" fill="#b8683a" ${OUT}/><rect x="-118" y="-196" width="236" height="22" rx="6" fill="#8a4a28" ${OUT3}/>
    <path d="M-50,-20v-70h100v70z" fill="#2a160c" ${OUT3}/><g class="pfire">${[-24, 0, 24].map((dx, i) => `<path d="M${dx},-24q-18,-30 0,-60q${i % 2 ? 14 : -14},26 0,60z" fill="${i === 1 ? "#ffd46a" : "#ff8a3a"}"/>`).join("")}</g></g>`;
  const kratip = (x, y, s) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M-50,0Q-60,-90 -40,-130H40Q60,-90 50,0Z" fill="#d8b878" ${OUT3}/><path d="M-44,-130Q0,-170 44,-130" fill="#c8a868" ${OUT3}/>
    ${[0, 1, 2].map((k) => `<path d="M-52,${-30 - k * 34}h104" stroke="#a88848" stroke-width="3"/>`).join("")}<path d="M-40,-130Q-70,-190 0,-200Q70,-190 40,-130" stroke="#8a6438" stroke-width="5" fill="none"/></g>`;
  const lamp = (x, y, s) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M0,-200V-60" stroke="#3a2a20" stroke-width="4"/><path d="M-30,-60h60l-8,70h-44z" fill="#d8c8a0" ${OUT3}/><ellipse cx="0" cy="-20" rx="12" ry="18" fill="#ffe6a0"/></g>`;

  // ---------------- skies and ground ----------------
  function sky(L, o, r) {
    const t = o.time || "day";
    let s = `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#${t === "dusk" ? "ppDusk" : t === "night" ? "ppNight" : "ppDay"})"/>`;
    if (t === "night") {
      for (let i = 0; i < 50; i++) s += `<circle cx="${f1(-900 + r() * 2900)}" cy="${f1(-600 + r() * 1200)}" r="${f1(1 + r() * 2)}" fill="#e8ecff" opacity="${(0.25 + r() * 0.5).toFixed(2)}"/>`;
      if (o.moon !== false) s += `<circle cx="${o.moonX ?? 820}" cy="240" r="260" fill="#9fb0d8" opacity=".07"/><circle cx="${o.moonX ?? 820}" cy="240" r="50" fill="#e8e2c0"/>`;
    }
    // rain clouds of the first rains, heavy and low
    const cc = t === "night" ? "#1a2030" : t === "dusk" ? "#5a4060" : "#aab8c4";
    s += `<g class="pcloud">${[[-500, 220, 900], [300, 120, 1000], [1100, 260, 800], [0, 420, 1200]].map(([x, y, w]) => `<path d="M${x},${y}q${w * 0.2},-80 ${w * 0.45},-30q${w * 0.25},-90 ${w * 0.55},10q-${w * 0.4},70 -${w},20z" fill="${cc}" opacity=".9"/>`).join("")}</g>`;
    put(L.sky, s);
  }
  function hills(L, y, o = {}) {
    const t = o.time || "day", c = t === "night" ? "#0a0f16" : t === "dusk" ? "#4a3a52" : "#7f9aa0";
    put(L.far, `<path d="M-1200,${y}Q-700,${y - 260} -200,${y - 120}T800,${y - 200}T1800,${y - 90}T2400,${y}V${y + 400}H-1200Z" fill="${c}"/>`);
  }
  // an Isan stilt house: tall posts, the open space under it, a gable roof, wooden walls, shutters; origin at the ground, centre
  function stiltHouse(x, G, s, o = {}) {
    const lit = !!o.lit;
    return `<g transform="translate(${f1(x)},${G}) scale(${s})">
      ${[-260, -100, 60, 220].map((px) => `<rect x="${px}" y="-420" width="26" height="420" fill="#4a3424" ${OUT3}/>`).join("")}
      <rect x="-300" y="-440" width="560" height="36" fill="#5a4030" ${OUT3}/><path d="M-290,-440V-760H250V-440Z" fill="#7a5a3c" ${OUT}/>
      ${Array.from({ length: 13 }, (_, k) => `<path d="M${-290 + k * 42},-760V-440" stroke="#5a4030" stroke-width="4"/>`).join("")}
      <rect x="-220" y="-700" width="120" height="150" fill="${lit ? "#ffd38a" : "#2a1f18"}" ${OUT3}/><rect x="60" y="-700" width="120" height="150" fill="${lit ? "#ffcf7a" : "#2a1f18"}" ${OUT3}/>
      <path d="M-350,-760L-20,-980L310,-760Z" fill="#5a3a2a" ${OUT}/><path d="M-20,-980v-40" stroke="#5a3a2a" stroke-width="10"/>
      <path d="M260,-440L380,0" stroke="#5a4030" stroke-width="12"/>${[1, 2, 3, 4, 5].map((k) => `<path d="M${260 + k * 20},${-440 + k * 73}h40" stroke="#5a4030" stroke-width="8"/>`).join("")}</g>`;
  }
  const houseGlow = (x, G, s) => `<circle cx="${f1(x - 160 * s)}" cy="${f1(G - 625 * s)}" r="${f1(240 * s)}" fill="url(#ppLamp)"/><circle cx="${f1(x + 120 * s)}" cy="${f1(G - 625 * s)}" r="${f1(220 * s)}" fill="url(#ppLamp)"/>`;
  function tamarind(x, G, s, t) {
    const c = t === "night" ? "#0c1410" : t === "dusk" ? "#2a3a2a" : "#4a7a4a";
    return `<g transform="translate(${f1(x)},${G}) scale(${s})"><path d="M-30,0Q-40,-200 -10,-380L10,-380Q30,-200 40,0Z" fill="${t === "night" ? "#0a0c0a" : "#4a3424"}"/>
      ${[[-160, -460, 200], [80, -520, 230], [-40, -620, 220], [200, -400, 160], [-240, -360, 150]].map(([cx, cy, r]) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${c}"/>`).join("")}</g>`;
  }

  // ---------------- wide: the village at the first rains ----------------
  function isanVillage(L, o = {}) {
    const id = o.id || "iv", r = mk(o.seed || 311), G = o.ground ?? 1300, t = o.time || "day";
    sky(L, o, r);
    hills(L, G - 120, o);
    const dark = t === "night";
    // paddies: flooded squares with the sky in them, bunds between, young rice in rows
    let m = `<rect x="-1200" y="${G - 140}" width="3500" height="1200" fill="${dark ? "#0c1418" : "url(#ppPaddy)"}"/>`;
    for (let k = 0; k < 5; k++) m += `<path d="M-1200,${G - 120 + k * 60}H2300" stroke="${dark ? "#1a2420" : "#7a6a48"}" stroke-width="${8 + k * 3}"/>`;
    for (let k = 0; k < 90; k++) m += `<path d="M${f1(-1100 + r() * 3300)},${f1(G - 110 + r() * 260)}v-${f1(10 + r() * 16)}" stroke="${dark ? "#1e3024" : "#5f9a52"}" stroke-width="4" stroke-linecap="round"/>`;
    put(L.mid, m);
    let s = "", g = "";
    (o.houses || [[-120, 0.9, { lit: dark }], [900, 0.7, { lit: dark }]]).forEach(([x, k, ho]) => { s += stiltHouse(x, G, k, ho || {}); if (ho && ho.lit) g += houseGlow(x, G, k); });
    if (o.tree !== false) s += tamarind(o.treeX ?? 420, G, 1.1, t);
    if (o.fence) s += `<g>${Array.from({ length: 16 }, (_, k) => `<rect x="${o.fence[0] + k * 70}" y="${G - 240 + (k % 3) * 8}" width="16" height="${250 - (k % 3) * 8}" fill="${dark ? "#1a1410" : "#9a8458"}" ${dark ? "" : OUT3}/>`).join("")}
      <path d="M${o.fence[0] - 20},${G - 190}H${o.fence[0] + 1120}M${o.fence[0] - 20},${G - 90}H${o.fence[0] + 1120}" stroke="${dark ? "#1a1410" : "#7a6440"}" stroke-width="10"/></g>`;
    // the red dirt road running into the paddies
    const RX = o.roadX ?? 560;
    if (o.road !== false) s += `<path d="M${RX - 260},${G + 900}L${RX - 40},${G - 120}H${RX + 40}L${RX + 380},${G + 900}Z" fill="${dark ? "#1a1410" : "#a8643a"}"/><path d="M${RX - 160},${G + 900}L${RX - 14},${G - 120}M${RX + 280},${G + 900}L${RX + 14},${G - 120}" stroke="${dark ? "#120e0a" : "#8a4a2a"}" stroke-width="5" opacity=".6"/>`;
    put(L.set, s);
    put(L.glow, g);
    if (o.rain) put(L.fg, `<g class="prain">${Array.from({ length: 80 }, () => `<path d="M${f1(-200 + r() * 1500)},${f1(-200 + r() * 2200)}l-14,60" stroke="#c8d8e8" stroke-width="3" opacity=".45"/>`).join("")}</g>`);
  }

  // ---------------- ป่าโคก: the dry dipterocarp forest after rain ----------------
  function dryForest(L, o = {}) {
    const id = o.id || "df", r = mk(o.seed || 331), G = o.ground ?? 1400, t = o.time || "day", dark = t === "night";
    sky(L, { ...o, moon: o.moon ?? false }, r);
    put(L.far, `<rect x="-1200" y="${G - 700}" width="3500" height="800" fill="${dark ? "#0a0f0c" : t === "dusk" ? "#4a4a3a" : "#9aa88a"}" opacity=".85"/>
      ${Array.from({ length: 26 }, () => { const x = -1100 + r() * 3300; return `<path d="M${f1(x)},${G - 40}V${f1(G - 700 - r() * 300)}" stroke="${dark ? "#0e1410" : "#7f8a70"}" stroke-width="${f1(10 + r() * 10)}"/>`; }).join("")}`);
    // mid trees: straight trunks with flaky bark, small crowns high up
    let m = "";
    for (let k = 0; k < 9; k++) {
      const x = -1000 + k * 380 + r() * 120, w = 26 + r() * 14, top = G - 1500 - r() * 400;
      m += `<g><path d="M${f1(x - w)},${G}L${f1(x - w * 0.6)},${f1(top)}H${f1(x + w * 0.6)}L${f1(x + w)},${G}Z" fill="${dark ? "#120f0c" : "#6a5440"}" ${dark ? "" : OUT3}/>
        ${dark ? "" : Array.from({ length: 6 }, (_, j) => `<path d="M${f1(x - w * 0.7)},${f1(G - 120 - j * 220)}l${f1(w * 1.2)},${f1(-20 + r() * 40)}" stroke="#4a3a2a" stroke-width="4"/>`).join("")}
        ${[[-120, -40, 150], [90, -90, 130], [0, -180, 140]].map(([dx, dy, rr]) => `<circle cx="${f1(x + dx)}" cy="${f1(top + dy)}" r="${rr}" fill="${dark ? "#0c120e" : t === "dusk" ? "#3a4a30" : "#6a8a4a"}"/>`).join("")}</g>`;
    }
    put(L.mid, m);
    // red earth, leaf litter, the termite mound, mushrooms
    let s = `<rect x="-1200" y="${G}" width="3500" height="1400" fill="${dark ? "#1a120c" : "url(#ppEarth)"}"/>`;
    for (let k = 0; k < 140; k++) s += `<ellipse cx="${f1(-1100 + r() * 3300)}" cy="${f1(G + 10 + r() * 700)}" rx="${f1(14 + r() * 16)}" ry="${f1(5 + r() * 5)}" fill="${dark ? "#2a1c12" : ["#8a5a2a", "#a8742e", "#6a4424"][k % 3]}" transform="rotate(${f1(r() * 180)})" opacity=".9"/>`;
    const MX = o.mound ?? 300;
    if (MX !== false) s += `<path d="M${MX - 260},${G + 20}Q${MX - 200},${G - 200} ${MX - 60},${G - 420}Q${MX},${G - 470} ${MX + 50},${G - 400}Q${MX + 200},${G - 180} ${MX + 270},${G + 20}Z" fill="${dark ? "#2a1a10" : "#b8703a"}" ${dark ? "" : OUT}/>
      ${dark ? "" : `<path d="M${MX - 120},${G - 200}q40,-30 60,10M${MX + 40},${G - 300}q30,20 10,60M${MX + 100},${G - 120}q-30,-20 -60,0" stroke="#8a4a24" stroke-width="5" fill="none"/>`}`;
    put(L.set, s);
    let a = "";
    (o.mush || []).forEach(([x, k, mo], i) => { a += mush(x, G + 10, k, { ...(mo || {}), id: `${id}-m${i}` }); });
    put(L.act, a);
    if (o.mist) put(L.fg, `<rect x="-1200" y="${G - 260}" width="3500" height="320" fill="${dark ? "#2a3440" : "#e8ecea"}" opacity=".22"/>`);
  }

  // ---------------- the kitchen under the stilt house ----------------
  function underHouse(L, o = {}) {
    const id = o.id || "uh", r = mk(o.seed || 341), G = o.ground ?? 1480, t = o.time || "night", dark = t === "night";
    sky(L, { ...o, time: t }, r);
    hills(L, G - 300, { time: t });
    put(L.mid, `<rect x="-1200" y="${G - 320}" width="3500" height="400" fill="${dark ? "#0c1418" : "url(#ppPaddy)"}"/>`);
    // the house floor overhead with its joists, the posts, the ladder up, a bamboo platform, the stove and the pot
    const SX = o.stoveX ?? 260;
    let s = `<rect x="-1200" y="${G - 1700}" width="3500" height="520" fill="#4a3424"/>${Array.from({ length: 20 }, (_, k) => `<rect x="${-1200 + k * 180}" y="${G - 1200}" width="40" height="40" fill="#3a2818"/>`).join("")}
      <rect x="-1200" y="${G - 1220}" width="3500" height="40" fill="#5a4030" ${OUT3}/>
      ${[-700, -150, 560, 1160].map((px) => `<rect x="${px}" y="${G - 1200}" width="44" height="1220" fill="#5a4030" ${OUT3}/>`).join("")}
      <rect x="-1200" y="${G}" width="3500" height="1200" fill="${dark ? "#5a4632" : "#a07850"}"/>${Array.from({ length: 30 }, () => `<ellipse cx="${f1(-1100 + r() * 3300)}" cy="${f1(G + 20 + r() * 500)}" rx="${f1(30 + r() * 60)}" ry="${f1(6 + r() * 8)}" fill="#6a4a30" opacity=".5"/>`).join("")}
      <g><rect x="-560" y="${G - 300}" width="620" height="40" fill="#c8a066" ${OUT3}/>${Array.from({ length: 12 }, (_, k) => `<path d="M${-550 + k * 50},${G - 300}v40" stroke="#9a7444" stroke-width="4"/>`).join("")}
        ${[-540, 30].map((px) => `<rect x="${px}" y="${G - 260}" width="20" height="260" fill="#9a7444" ${OUT3}/>`).join("")}</g>
      <path d="M1300,${G - 1200}L1500,${G}M1420,${G - 1200}L1620,${G}" stroke="#5a4030" stroke-width="14"/>${[1, 2, 3, 4, 5, 6, 7].map((k) => `<path d="M${1300 + k * 25},${G - 1200 + k * 150}h120" stroke="#5a4030" stroke-width="12"/>`).join("")}
      ${stove(SX, G, 1.0)}${pot(SX, G - 196, 0.95, { id: `${id}-pot`, clay: o.clay, curry: o.curry })}
      ${kratip(-380, G - 300, 0.9)}${bowl(-200, G - 300, 0.8, { id: `${id}-bowl`, empty: o.bowlEmpty })}${bowl(-90, G - 300, 0.7, { empty: true, col: "#e8e0d0" })}
      ${o.basket !== false ? basket(o.basketX ?? 760, G, 0.9, { id: `${id}-basket`, full: o.basketFull !== false }) : ""}
      ${lamp(-260, G - 1180, 1.2)}`;
    put(L.set, s);
    if (o.prints) {
      // bare feet with toes too long, from the pot out toward the forest edge (right)
      const foot = (x, y, k, fl) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${fl ? 8 : -8}) scale(${k * 1.4})"><ellipse cx="0" cy="0" rx="24" ry="14" fill="#9a7a5a" opacity=".6"/><ellipse cx="0" cy="0" rx="22" ry="12" fill="#1a100a" opacity=".9"/><ellipse cx="34" cy="${fl ? 4 : -4}" rx="16" ry="11" fill="#1a100a" opacity=".9"/>
        ${[-14, -5, 4, 13].map((d, j) => `<path d="M48,${(fl ? 1 : -1) * d * 0.6}l${30 + j * 4},${(fl ? 1 : -1) * d}" stroke="#1a100a" stroke-width="7" stroke-linecap="round" opacity=".9"/>`).join("")}</g>`;
      put(L.set, `<g id="${id}-prints">${Array.from({ length: 7 }, (_, k) => foot(SX + 200 + k * 190, G + 60 + (k % 2 ? 40 : -10) + k * 18, 1 + k * 0.1, k % 2)).join("")}</g>`);
    }
    if (o.beam) put(L.glow, `<g id="${id}-beam"><path d="M${o.beam[0]},${o.beam[1]}L${o.beam[2] - 360},${o.beam[3] + 120}L${o.beam[2] + 360},${o.beam[3] + 140}Z" fill="#fff2c8" opacity=".18"/><ellipse cx="${o.beam[2]}" cy="${o.beam[3] + 130}" rx="380" ry="110" fill="url(#ppLamp)"/></g>`);
    put(L.act, `<g id="${id}-steam" class="psteam">${[0, 1, 2].map((k) => `<path d="M${SX - 50 + k * 50},${G - 360}c-30,-60 30,-100 0,-170c-24,-50 20,-80 10,-120" stroke="#e8e4dc" stroke-width="${18 - k * 3}" fill="none" stroke-linecap="round" opacity=".35"/>`).join("")}</g>`);
    put(L.glow, `<g id="${id}-fire"><circle cx="${SX}" cy="${G - 60}" r="420" fill="url(#ppFire)" opacity=".8"/></g><circle cx="-260" cy="${G - 1200}" r="520" fill="url(#ppLamp)" opacity="${dark ? 0.9 : 0.4}"/>`);
  }

  // ---------------- upstairs at night: the sleeping mat, the mosquito net, the floorboards with gaps (ember light from below) ----------------
  function bedNet(L, o = {}) {
    const id = o.id || "bn", G = o.ground ?? 1480;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#0e0c0a"/>`);
    let s = `<rect x="-1200" y="-800" width="3500" height="${G + 800}" fill="#2a2018"/>${Array.from({ length: 22 }, (_, k) => `<path d="M${-1200 + k * 160},-800V${G}" stroke="#1e1610" stroke-width="8"/>`).join("")}
      <rect x="-1200" y="${G}" width="3500" height="1200" fill="#3a2a1c"/>${Array.from({ length: 14 }, (_, k) => `<path d="M-1200,${G + 30 + k * 70}H2300" stroke="#120c08" stroke-width="${k % 2 ? 6 : 10}"/>`).join("")}
      <rect x="-200" y="${G - 40}" width="1500" height="60" fill="#8a7a50" ${OUT3}/>${Array.from({ length: 12 }, (_, k) => `<path d="M${-200 + k * 125},${G - 40}v60" stroke="#6a5a38" stroke-width="4"/>`).join("")}`;
    put(L.set, s);
    put(L.glow, `<g id="${id}-ember">${Array.from({ length: 6 }, (_, k) => `<path d="M-1200,${G + 30 + k * 140}H2300" stroke="#ff9a3a" stroke-width="4" opacity="${0.25 - k * 0.03}"/>`).join("")}</g>`);
    put(L.fg, `<g id="${id}-net" opacity=".5"><path d="M-260,${G - 1100}H1360V${G + 40}H-260Z" fill="#e8e4dc" opacity=".14"/>${Array.from({ length: 40 }, (_, k) => `<path d="M${-260 + k * 42},${G - 1100}V${G + 40}" stroke="#e8e4dc" stroke-width="1.5" opacity=".35"/>`).join("")}
      ${Array.from({ length: 28 }, (_, k) => `<path d="M-260,${G - 1100 + k * 42}H1360" stroke="#e8e4dc" stroke-width="1.5" opacity=".3"/>`).join("")}</g>`);
  }
  // ---------------- top-down: through the gaps between the floorboards, the kitchen below in ember light ----------------
  function floorGap(L, o = {}) {
    const id = o.id || "fg";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#050403"/>`);
    // below: the ground, the stove's embers, the pot, a shape crouched beside it (only its eyes will show)
    let b = `<rect x="-200" y="200" width="1500" height="1500" fill="#1a120c"/><circle cx="420" cy="960" r="330" fill="url(#ppFire)" opacity=".55"/>
      <g transform="translate(420,960)"><circle r="120" fill="#2a160c"/><circle r="96" fill="#7a5a2a"/><ellipse cx="-30" cy="-10" rx="24" ry="10" fill="#e8e0cc"/><ellipse cx="30" cy="16" rx="20" ry="9" fill="#e8e0cc"/></g>`;
    if (o.ghost !== false) b += `<g id="${id}-ghost" opacity="${o.ghostOp ?? 0.9}"><ellipse cx="690" cy="1000" rx="150" ry="120" fill="${PBL}"/><circle cx="628" cy="900" r="70" fill="${PBL}"/>${Array.from({ length: 8 }, (_, k) => `<path d="M${588 + k * 12},880q${(k - 4) * 8},50 ${(k - 4) * 14},90" stroke="${PBL}" stroke-width="9" fill="none"/>`).join("")}
      <path d="M560,960q-40,10 -60,-20" stroke="${PBL}" stroke-width="18" fill="none" stroke-linecap="round"/></g>${eyes(628, 890, 1.0, `${id}-eyes`)}`;
    put(L.mid, b);
    // the boards: wide planks with narrow gaps
    let s = "";
    for (let k = 0; k < 9; k++) { const x = -260 + k * 200; if (k === 4) continue; s += `<rect x="${x}" y="-800" width="176" height="3600" fill="${k % 2 ? "#4a3424" : "#3e2c1e"}"/><path d="M${x + 30},-800V2800M${x + 120},-800V2800" stroke="#2e2014" stroke-width="3" opacity=".6"/>`; }
    put(L.set, s);
  }

  // ---------------- an old pickup on the dirt road at night, headlights on (side view); o.lit cab light ----------------
  const pickup = (x, y, s, o = {}) => `<g ${o.id ? `id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${o.flip ? -s : s},${s})">
    <path d="M-420,-120V-250H-120L-60,-380H140L220,-250H360Q400,-250 400,-200V-120Z" fill="#5a7a8a" ${OUT}/><path d="M-50,-360H120L180,-260H-90Z" fill="${o.lit ? "#ffe2a0" : "#2a3a44"}" ${OUT3}/>
    <rect x="-420" y="-260" width="290" height="20" fill="#4a6a7a" ${OUT3}/><path d="M360,-230h40v40h-40z" fill="#fff6c8"/>
    ${[-260, 230].map((cx) => `<g><circle cx="${cx}" cy="-120" r="70" fill="#1c1c1e" ${OUT}/><circle cx="${cx}" cy="-120" r="30" fill="#9aa4a8"/></g>`).join("")}</g>`;
  function nightRoad(L, o = {}) {
    const id = o.id || "nr", r = mk(o.seed || 371), G = o.ground ?? 1400;
    sky(L, { time: "night", moonX: o.moonX ?? 300 }, r);
    hills(L, G - 200, { time: "night" });
    put(L.mid, `<g id="${id}-scroll"><rect x="-1200" y="${G - 220}" width="4500" height="300" fill="#0c1418"/>${Array.from({ length: 60 }, () => `<path d="M${f1(-1100 + r() * 4300)},${f1(G - 200 + r() * 160)}v-14" stroke="#1e3024" stroke-width="4"/>`).join("")}</g>`);
    put(L.set, `<rect x="-1200" y="${G - 40}" width="4500" height="1400" fill="#2a1c12"/><path d="M-1200,${G + 40}H3300" stroke="#3a2818" stroke-width="10"/><g id="${id}-posts">${Array.from({ length: 11 }, (_, k) => `<rect x="${-1000 + k * 420}" y="${G - 700}" width="22" height="660" fill="#141210"/>`).join("")}</g>`);
    put(L.act, pickup(o.x ?? 540, G + 60, o.s ?? 1.1, { id: `${id}-truck`, lit: true, flip: o.flip }));
    put(L.glow, `<g id="${id}-beam"><path d="M${(o.x ?? 540) + 440 * (o.s ?? 1.1)},${G - 140}L2400,${G - 420}L2400,${G + 260}Z" fill="#fff2c8" opacity=".22"/></g>`);
  }
  // ---------------- a district hospital at night: the emergency entrance, its sign and light ----------------
  function erFront(L, o = {}) {
    const id = o.id || "er", r = mk(o.seed || 381), G = o.ground ?? 1400;
    sky(L, { time: o.time || "night", moon: false }, r);
    let s = `<rect x="-600" y="${G - 900}" width="2200" height="900" fill="#e8e4d8" ${OUT}/><rect x="-600" y="${G - 960}" width="2200" height="70" fill="#4a7a6a" ${OUT3}/>
      ${Array.from({ length: 8 }, (_, k) => `<rect x="${-500 + k * 260}" y="${G - 820}" width="150" height="180" fill="#ffe8b0" ${OUT3}/>`).join("")}
      <rect x="260" y="${G - 520}" width="560" height="520" fill="#9ac8c0" ${OUT}/><path d="M540,${G - 520}V${G}" stroke="${INK}" stroke-width="5"/>
      <rect x="200" y="${G - 640}" width="680" height="100" rx="12" fill="#c8342a" ${OUT}/><text x="540" y="${G - 572}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="56" fill="#fff">ห้องฉุกเฉิน</text>
      <rect x="-1200" y="${G}" width="3500" height="1200" fill="#4a4a48"/><path d="M-1200,${G + 200}H2300" stroke="#f2c84a" stroke-width="10" stroke-dasharray="60 40"/>`;
    put(L.set, s);
    if (o.truck !== false) put(L.act, pickup(o.truckX ?? -200, G + 260, 1.0, { id: `${id}-truck`, lit: true }));
    put(L.glow, `<circle cx="540" cy="${G - 590}" r="420" fill="url(#ppLamp)" opacity=".7"/><circle cx="540" cy="${G - 200}" r="520" fill="url(#ppLamp)" opacity=".45"/>`);
  }
  // ---------------- the ward: a bed, a drip stand, the window (o.time night | dawn), a curtain ----------------
  function ward(L, o = {}) {
    const id = o.id || "wd", G = o.ground ?? 1480, dawn = o.time === "dawn";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#cfe0dc"/>`);
    let s = `<rect x="-1200" y="-800" width="3500" height="${G + 800}" fill="#dfe8e4"/><rect x="-1200" y="${G - 220}" width="3500" height="220" fill="#b8ccc6"/>
      <g id="${id}-window"><rect x="560" y="${G - 1220}" width="520" height="560" fill="${dawn ? "#c8b8d8" : "#0e1424"}" ${OUT}/>${dawn ? `<rect x="560" y="${G - 860}" width="520" height="200" fill="#f2c08a" opacity=".8"/>` : ""}
        <path d="M820,${G - 1220}V${G - 660}M560,${G - 940}H1080" stroke="#9aa4a8" stroke-width="12"/></g>
      <path d="M-200,${G - 1400}V${G - 260}" stroke="#9aa4a8" stroke-width="6"/>${Array.from({ length: 10 }, (_, k) => `<path d="M${-200 + k * 2},${G - 1400}q40,${300 + k * 80} -10,${1100}" stroke="#a8c8d8" stroke-width="40" fill="none" opacity=".5"/>`).join("")}
      <rect x="-1200" y="${G}" width="3500" height="1200" fill="#9aa8a4"/>${Array.from({ length: 10 }, (_, k) => `<path d="M-1200,${G + 40 + k * 90}H2300" stroke="#8a9894" stroke-width="3"/>`).join("")}
      <g><rect x="-120" y="${G - 360}" width="760" height="70" rx="12" fill="#f4f4f0" ${OUT}/><rect x="-120" y="${G - 300}" width="760" height="40" fill="#9aa4a8" ${OUT3}/>
        ${[-100, 600].map((x) => `<path d="M${x},${G - 260}V${G}" stroke="#7a8488" stroke-width="12"/>`).join("")}<rect x="-140" y="${G - 520}" width="30" height="230" fill="#9aa4a8" ${OUT3}/></g>
      <g><path d="M720,${G}V${G - 1000}M680,${G - 1000}h80" stroke="#7a8488" stroke-width="10"/><rect x="660" y="${G - 1000}" width="70" height="120" rx="14" fill="#e8f4f8" ${OUT3}/><path d="M695,${G - 880}Q680,${G - 600} 520,${G - 400}" stroke="#bcd8e0" stroke-width="5" fill="none"/></g>`;
    put(L.set, s);
    if (o.print) put(L.set, `<g id="${id}-print" opacity="${o.printOp ?? 1}" transform="translate(720,${G - 1060})"><path d="M0,0q-30,40 -10,90q30,30 80,10q30,-30 10,-90z" fill="#3a3020" opacity=".35"/>
      ${[[-30, -10, -60, -120], [0, -20, -10, -150], [30, -20, 40, -150], [56, -6, 90, -110], [-40, 50, -110, 20]].map(([x0, y0, x1, y1]) => `<path d="M${x0},${y0}L${x1},${y1}" stroke="#3a3020" stroke-width="16" stroke-linecap="round" opacity=".35"/>`).join("")}</g>`);
    if (o.eyes) put(L.glow, eyes(950, G - 1080, 0.8, `${id}-eyes`));
  }

  // ---------------- close on the floor: ยาย's feet under the sarong hem — muddy, the toes too long ----------------
  function feetClose(L, o = {}) {
    const id = o.id || "fc", G = o.ground ?? 1300;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#1a1c1c"/>`);
    put(L.set, `<rect x="-1200" y="${G - 40}" width="3500" height="1400" fill="#7a8884"/>${Array.from({ length: 10 }, (_, k) => `<path d="M-1200,${G + k * 120}H2300" stroke="#6a7874" stroke-width="4"/>`).join("")}
      <path d="M-1200,${G - 900}H2300V${G - 40}H-1200Z" fill="#2a2c2c"/>`);
    const foot = (x, fl) => `<g transform="translate(${x},${G}) scale(${fl ? -1 : 1},1)"><path d="M-60,-260Q-70,-120 -80,-40Q-90,10 -20,20H60Q80,10 60,-30Q40,-120 40,-260Z" fill="#c99a74" ${OUT}/>
      ${[0, 1, 2, 3, 4].map((k) => `<path d="M${-60 + k * 26},10q${4 + k},${60 + k * 10} ${-6 + k * 2},${110 + k * 16}" stroke="${INK}" stroke-width="26" fill="none" stroke-linecap="round"/><path d="M${-60 + k * 26},10q${4 + k},${60 + k * 10} ${-6 + k * 2},${110 + k * 16}" stroke="#c99a74" stroke-width="18" fill="none" stroke-linecap="round"/>`).join("")}
      <path d="M-80,-40Q-10,-10 60,-30L60,20H-20Q-90,10 -80,-40Z" fill="#5a3a20" opacity=".6"/>${[0, 1, 2].map((k) => `<ellipse cx="${-50 + k * 40}" cy="${60 + k * 30}" rx="12" ry="8" fill="#5a3a20" opacity=".7"/>`).join("")}</g>`;
    put(L.act, foot(400, false) + foot(680, true) + `<path d="M150,${G - 900}H930L960,${G - 230}Q540,${G - 180} 120,${G - 230}Z" fill="#6a2f62" ${OUT}/>${Array.from({ length: 6 }, (_, k) => `<path d="M${180 + k * 130},${G - 880}l-20,640" stroke="#52244c" stroke-width="10"/>`).join("")}`);
  }

  // ---------------- close on the forest floor ----------------
  function mushClose(L, o = {}) {
    const id = o.id || "mc", r = mk(o.seed || 351), G = o.ground ?? 1300;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="${o.dusk ? "#3a2a22" : "#8a6a4a"}"/>`);
    let s = `<path d="M-400,${G - 200}Q-200,${G - 900} 200,${G - 1200}Q420,${G - 1300} 600,${G - 1100}Q1000,${G - 700} 1400,${G - 200}V${G + 900}H-400Z" fill="${o.dusk ? "#6a3a20" : "#b8703a"}" ${OUT}/>
      <path d="M100,${G - 900}q60,-40 100,20M500,${G - 1000}q40,40 0,100M800,${G - 600}q-60,-20 -100,30" stroke="#8a4a24" stroke-width="8" fill="none"/>
      <rect x="-1200" y="${G}" width="3500" height="1200" fill="${o.dusk ? "#4a2a18" : "#8a5228"}"/>`;
    for (let k = 0; k < 80; k++) s += `<ellipse cx="${f1(-200 + r() * 1500)}" cy="${f1(G - 20 + r() * 700)}" rx="${f1(30 + r() * 30)}" ry="${f1(10 + r() * 8)}" fill="${["#a8742e", "#7a5228", "#c8944a"][k % 3]}" transform="rotate(${f1(-30 + r() * 60)} 0 0)" opacity=".95"/>`;
    put(L.set, s);
    let a = "";
    (o.mush || [[380, 1.6, { cup: true }], [700, 1.3, { cup: true, tilt: 8 }], [560, 1.0, { egg: true }]]).forEach(([x, k, mo], i) => { a += mush(x, G + 40, k, { ...(mo || {}), id: `${id}-m${i}` }); });
    put(L.act, a);
    if (o.hand !== false) put(L.fg, `<g id="${id}-hand" transform="translate(0,0)"><path d="M1400,${G - 600}L760,${G - 300}" stroke="${INK}" stroke-width="150" stroke-linecap="round"/><path d="M1400,${G - 600}L760,${G - 300}" stroke="${o.sleeve || "#d8443a"}" stroke-width="136" stroke-linecap="round"/>
      <path d="M800,${G - 320}L600,${G - 240}" stroke="${INK}" stroke-width="110" stroke-linecap="round"/><path d="M800,${G - 320}L600,${G - 240}" stroke="${o.skin || "#c98e5e"}" stroke-width="96" stroke-linecap="round"/>
      ${[-30, 0, 30].map((d) => `<path d="M${560 + d * 0.3},${G - 250 + d}q-50,10 -60,50" stroke="${INK}" stroke-width="34" fill="none" stroke-linecap="round"/><path d="M${560 + d * 0.3},${G - 250 + d}q-50,10 -60,50" stroke="${o.skin || "#c98e5e"}" stroke-width="22" fill="none" stroke-linecap="round"/>`).join("")}</g>`);
  }

  // ---------------- knowledge, drawn: the mushrooms on slate ----------------
  function mushSection(L, o = {}) {
    const id = o.id || "ms", v = o.v || 1, F = 1300;
    const T = (x, y, t, c = "#f4ecd8", sz = 40, i = "") => `<text ${i ? `id="${i}"` : ""} x="${x}" y="${y}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${sz}" fill="${c}" stroke="#1c2822" stroke-width="8" paint-order="stroke" ${i ? 'opacity="0"' : ""}>${t}</text>`;
    const X = (x, y, i, r = 70) => `<g id="${i}" opacity="0" transform="translate(${x},${y})"><circle r="${r}" fill="none" stroke="#e0362c" stroke-width="12"/><path d="M${-r * 0.7},${-r * 0.7}L${r * 0.7},${r * 0.7}" stroke="#e0362c" stroke-width="12" stroke-linecap="round"/></g>`;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#ppSlate)"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-1100 + k * 100},-800V2800M-1200,${-700 + k * 100}H2300" stroke="#2f4038" stroke-width="2"/>`).join("")}`);
    let s = `<path d="M-600,${F}H1700" stroke="#7a5a3a" stroke-width="14"/>`, a = "";
    if (v === 1) {
      // edible and deadly, side by side: white cap, gills, ring, the cup at the foot — the same shape
      a += `<g id="${id}-a">${mush(300, F, 1.6, { lines: o.lines })}${T(300, F + 80, o.la || "กินได้", "#9ae68a", 44)}</g>
        <g id="${id}-b">${mush(780, F, 1.6, {})}${T(780, F + 80, o.lb || "พิษถึงตาย", "#ff8a7a", 44)}</g>
        <g id="${id}-q" opacity="0">${T(540, 560, "?", "#ffe08a", 200)}</g>
        <g id="${id}-eye" opacity="0" transform="translate(540,760)"><path d="M-90,0Q0,-70 90,0Q0,70 -90,0Z" fill="#f4ecd8" ${OUT}/><circle r="30" fill="#2a3a4a"/><path d="M-110,60L110,-60" stroke="#e0362c" stroke-width="12" stroke-linecap="round"/></g>`;
      if (o.parts) a += `<g id="${id}-parts" opacity="0">${T(470, F - 520, "หมวก", "#f4ecd8", 32)}${T(470, F - 300, "วงแหวน", "#f4ecd8", 32)}${T(470, F - 30, "ถ้วยหุ้มโคน", "#f4ecd8", 32)}
          <path d="M420,${F - 530}H360M420,${F - 310}H350M405,${F - 40}H360" stroke="#f4ecd8" stroke-width="4"/></g>`;
    } else if (v === 2) {
      // the folk tests: rice in the pot, a silver spoon, an onion — none of them tells
      a += `<g id="${id}-t0">${pot(220, F, 1.0, { curry: "#e8e0cc" })}${Array.from({ length: 14 }, (_, k) => `<ellipse cx="${160 + (k % 7) * 20}" cy="${F - 150 - Math.floor(k / 7) * 10}" rx="7" ry="4" fill="#fffef4"/>`).join("")}${T(220, F + 70, "ต้มกับข้าวสาร", "#f4ecd8", 36)}${X(220, F - 220, `${id}-x0`)}</g>
        <g id="${id}-t1"><path d="M480,${F - 60}L640,${F - 420}" stroke="#d8dce0" stroke-width="22" stroke-linecap="round"/><ellipse cx="660" cy="${F - 470}" rx="44" ry="64" fill="#e8ecf0" ${OUT} transform="rotate(24 660 ${F - 470})"/>${T(560, F + 70, "ช้อนเงิน", "#f4ecd8", 36)}${X(580, F - 260, `${id}-x1`)}</g>
        <g id="${id}-t2"><ellipse cx="880" cy="${F - 90}" rx="80" ry="90" fill="#b84a6a" ${OUT}/><path d="M880,${F - 180}q-10,-60 10,-90" stroke="#6a9a4a" stroke-width="10" fill="none"/>${T(880, F + 70, "หอมแดง", "#f4ecd8", 36)}${X(880, F - 120, `${id}-x2`)}</g>`;
    } else if (v === 4) {
      // don't make them vomit: a finger down the throat, salt water, a raw egg — each crossed out; the lungs: choking
      a += `<g id="${id}-t0"><circle cx="220" cy="${F - 420}" r="90" fill="#e9bc93" ${OUT}/><path d="M220,${F - 380}q-30,30 0,50" stroke="${INK}" stroke-width="5" fill="none"/><path d="M300,${F - 300}L240,${F - 380}" stroke="#e9bc93" stroke-width="36" stroke-linecap="round"/><path d="M300,${F - 300}L240,${F - 380}" stroke="${INK}" stroke-width="4" fill="none"/>${T(220, F + 70, "ล้วงคอ", "#f4ecd8", 36)}${X(220, F - 380, `${id}-x0`, 120)}</g>
        <g id="${id}-t1"><path d="M480,${F - 300}h140l-14,300h-112z" fill="#cfe6ee" opacity=".7" ${OUT}/><path d="M486,${F - 200}h128" stroke="#9ac8d8" stroke-width="6"/>${Array.from({ length: 8 }, (_, k) => `<circle cx="${500 + (k % 4) * 30}" cy="${F - 120 - Math.floor(k / 4) * 30}" r="5" fill="#fff"/>`).join("")}${T(550, F + 70, "น้ำเกลือ", "#f4ecd8", 36)}${X(550, F - 160, `${id}-x1`, 110)}</g>
        <g id="${id}-t2"><ellipse cx="860" cy="${F - 80}" rx="80" ry="64" fill="#f4f0e4" ${OUT}/><ellipse cx="860" cy="${F - 86}" rx="34" ry="28" fill="#f2c84a"/>${T(860, F + 70, "ไข่ขาวดิบ", "#f4ecd8", 36)}${X(860, F - 90, `${id}-x2`, 100)}</g>
        <g id="${id}-lung" opacity="0" transform="translate(800,${F - 760})"><path d="M-20,-80V0M20,-80V0" stroke="#f4ecd8" stroke-width="14"/><path d="M-20,-10Q-140,-20 -130,100Q-120,180 -30,150Q-10,80 -20,-10Z" fill="#e88a8a" ${OUT}/><path d="M20,-10Q140,-20 130,100Q120,180 30,150Q10,80 20,-10Z" fill="#e88a8a" ${OUT}/>${T(0, 230, "สำลัก", "#ff8a7a", 40)}</g>`;
    } else if (v === 5) {
      // to the hospital now, with the leftover mushrooms and a photo
      a += `<g id="${id}-h" transform="translate(760,${F})"><rect x="-200" y="-420" width="400" height="420" fill="#e8e4d8" ${OUT}/><rect x="-60" y="-180" width="120" height="180" fill="#9ac8c0" ${OUT3}/><rect x="-40" y="-380" width="80" height="80" fill="#c8342a"/><path d="M0,-370v60M-30,-340h60" stroke="#fff" stroke-width="16"/>${T(0, 70, "โรงพยาบาล", "#f4ecd8", 36)}</g>
        <g id="${id}-bag" transform="translate(260,${F})"><path d="M-110,-240h220l-20,240h-180z" fill="#e8ecf0" opacity=".85" ${OUT}/>${mush(-20, -20, 0.55, {})}${T(0, 70, "เห็ดที่เหลือ", "#f4ecd8", 36)}</g>
        <g id="${id}-ph" opacity="0" transform="translate(300,${F - 640})"><rect x="-90" y="-150" width="180" height="300" rx="24" fill="#1d1f22" ${OUT}/><rect x="-74" y="-126" width="148" height="240" rx="8" fill="#e8e0cc"/>${mush(0, 90, 0.5, {})}${T(0, 220, "รูปถ่าย", "#f4ecd8", 32)}</g>
        <path id="${id}-arrow" d="M400,${F - 220}H520" stroke="#9ae68a" stroke-width="16" stroke-linecap="round" opacity="0"/><path id="${id}-arrowh" d="M510,${F - 250}l40,30l-40,30" stroke="#9ae68a" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0"/>`;
    } else if (v === 6) {
      // everyone who ate from the pot goes to be checked, symptoms or not
      const fig = (x, c, sick) => `<g transform="translate(${x},${F})"><circle cx="0" cy="-260" r="46" fill="#e9bc93" ${OUT3}/><path d="M-60,-200h120l20,200h-160z" fill="${c}" ${OUT3}/>${sick ? `<path d="M-16,-250l8,-8M8,-250l8,8" stroke="${INK}" stroke-width="5"/>` : `<circle cx="-14" cy="-262" r="5" fill="${INK}"/><circle cx="14" cy="-262" r="5" fill="${INK}"/>`}</g>`;
      a += `<g>${pot(540, F - 640, 0.9, {})}</g><g id="${id}-who">${fig(260, "#d8443a", true)}${fig(540, "#efe6d6", false)}${fig(820, "#c8b4e6", false)}</g>
        ${[260, 540].map((x, i) => `<path d="M540,${F - 600}L${x},${F - 330}" stroke="#f4ecd8" stroke-width="6" stroke-dasharray="14 12"/>`).join("")}
        <g id="${id}-ok" opacity="0">${[260, 540].map((x) => `<g transform="translate(${x},${F - 400})"><circle r="40" fill="#3fb86a" ${OUT3}/><path d="M-18,0l12,14l24,-28" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round"/></g>`).join("")}</g>
        ${T(820, F + 70, "ไม่ได้กิน", "#c8c0b0", 32)}${T(400, F + 70, "กินด้วยกัน = ไปตรวจด้วย", "#9ae68a", 38)}`;
    } else if (v === 8) {
      // the three stages of amatoxin poisoning (DDC handbook, table 2): sick → seems better → the liver gets worse
      const X0 = 120, X1 = 980, Y0 = F - 180, Y1 = F - 760;
      a += `<g><path d="M${X0},${Y1 - 40}V${Y0}H${X1 + 20}" stroke="#f4ecd8" stroke-width="6" fill="none"/>
        ${[[X0 + 140, "4–24 ชม."], [X0 + 430, "18–36 ชม."], [X0 + 720, "2–4 วัน"]].map(([x, t]) => `${T(x, Y0 + 60, t, "#c8c0b0", 30)}<path d="M${x},${Y0}v14" stroke="#f4ecd8" stroke-width="5"/>`).join("")}
        <path id="${id}-sick" d="M${X0},${Y0 - 20}C${X0 + 80},${Y0 - 40} ${X0 + 120},${Y1 + 60} ${X0 + 180},${Y1 + 70}C${X0 + 260},${Y1 + 80} ${X0 + 320},${Y0 - 100} ${X0 + 430},${Y0 - 120}C${X0 + 540},${Y0 - 130} ${X0 + 620},${Y1 + 40} ${X1},${Y1}" stroke="#ff8a7a" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="1600" stroke-dashoffset="1600"/>
        <path id="${id}-liver" d="M${X0},${Y0 - 10}C${X0 + 300},${Y0 - 20} ${X0 + 450},${Y0 - 140} ${X0 + 600},${Y0 - 320}S${X1 - 60},${Y1 - 20} ${X1},${Y1 - 30}" stroke="#c87ae8" stroke-width="10" fill="none" stroke-dasharray="1400" stroke-dashoffset="1400"/>
        ${T(X0 + 180, Y1 + 10, "อาเจียน", "#ff8a7a", 34)}${T(X0 + 430, Y0 - 160, "ดูเหมือนดีขึ้น", "#9ae68a", 34, `${id}-l1`)}${T(X1 - 120, Y1 - 70, "ตับแย่ลง", "#c87ae8", 36, `${id}-l2`)}
        <g transform="translate(${X1 - 90},${Y1 + 120})"><path d="M-70,0Q-80,-60 -20,-70Q40,-80 70,-40Q80,10 30,30Q-40,50 -70,0Z" fill="#a83a4a" ${OUT3}/></g>
        <g><circle cx="${X0 + 60}" cy="${Y1 - 10}" r="12" fill="#ff8a7a"/>${T(X0 + 140, Y1, "อาการ", "#ff8a7a", 30)}<circle cx="${X0 + 60}" cy="${Y1 + 40}" r="12" fill="#c87ae8"/>${T(X0 + 150, Y1 + 50, "ค่าตับ", "#c87ae8", 30)}</g></g>`;
    } else if (v === 7) {
      // tell the doctor everything: what, when, how many — a clipboard filling in
      a += `<g transform="translate(540,${F - 560})"><rect x="-300" y="-420" width="600" height="800" rx="20" fill="#c8a066" ${OUT}/><rect x="-260" y="-370" width="520" height="720" fill="#fbfaf4" ${OUT3}/><rect x="-90" y="-450" width="180" height="70" rx="14" fill="#9aa4a8" ${OUT3}/>
        ${[["กินอะไร", "เห็ดระโงก (มีรูป)"], ["กินกี่โมง", "หนึ่งทุ่ม"], ["อาการเริ่ม", "ตีสอง"], ["กินกี่คน", "2 คน"]].map(([q, aa], k) => `<g id="${id}-r${k}" opacity="0"><text x="-220" y="${-250 + k * 160}" font-family="Kanit" font-weight="700" font-size="40" fill="#5a4a3a">${q}</text><text x="-220" y="${-190 + k * 160}" font-family="Kanit" font-weight="800" font-size="46" fill="#c8342a">${aa}</text></g>`).join("")}</g>`;
    } else {
      // boiling: the pot on the fire a long time, the poison still there
      a += `<g>${stove(540, F, 1.4)}${pot(540, F - 274, 1.3, {})}</g>
        <g id="${id}-tox">${[[440, F - 500], [540, F - 540], [640, F - 500], [490, F - 590], [600, F - 600]].map(([x, y]) => `<g transform="translate(${x},${y})"><circle r="26" fill="#7a2a8a" ${OUT3}/><path d="M-8,-6h4M4,-6h4M-8,8q8,-6 16,0" stroke="#f4ecd8" stroke-width="4" fill="none"/></g>`).join("")}</g>
        <g id="${id}-clock" opacity="0" transform="translate(880,560)"><circle r="80" fill="#f4ecd8" ${OUT}/><path id="${id}-hand" d="M0,0V-60" stroke="${INK}" stroke-width="8" stroke-linecap="round"/><circle r="8" fill="${INK}"/></g>
        ${X(540, F - 560, `${id}-x0`, 140)}`;
    }
    put(L.set, s);
    put(L.act, a);
    put(L.glow, v === 3 ? `<circle cx="540" cy="${F - 60}" r="420" fill="url(#ppFire)" opacity=".7"/>` : "");
  }

  // ---------------- chapter card: the kitchen clock running backwards ----------------
  function clockCard(L, o = {}) {
    const id = o.id || "cc";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#6a4a32"/>${Array.from({ length: 20 }, (_, k) => `<path d="M${-1200 + k * 180},-800V2800" stroke="#5a3e28" stroke-width="6"/>`).join("")}`);
    put(L.set, `<g transform="translate(540,900)"><path d="M0,-420V-330" stroke="#3a2a20" stroke-width="6"/><circle r="330" fill="#f4ecd8" ${OUT}/><circle r="300" fill="none" stroke="#c8342a" stroke-width="10"/>
      ${Array.from({ length: 12 }, (_, k) => `<path d="M0,-270V-236" stroke="${INK}" stroke-width="${k % 3 ? 6 : 12}" transform="rotate(${k * 30})"/>`).join("")}
      <g id="${id}-hh"><path d="M0,0V-150" stroke="${INK}" stroke-width="18" stroke-linecap="round"/></g><g id="${id}-mm"><path d="M0,0V-230" stroke="${INK}" stroke-width="10" stroke-linecap="round"/></g><circle r="18" fill="#c8342a"/>
      <text y="120" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="#8a7a6a">ร้านทองหนองคาย</text></g>
      <g transform="translate(860,1300)"><path d="M0,0q40,-30 80,0q-10,24 -40,24q-30,0 -40,-24z" fill="#6a8a5a" ${OUT3}/><circle cx="62" cy="-6" r="5" fill="${INK}"/><path d="M0,0q-60,20 -90,-10" stroke="#6a8a5a" stroke-width="12" fill="none" stroke-linecap="round"/></g>`);
  }

  // ---------------- the legend: an Isan shadow-puppet screen, four panels ----------------
  function popLegend(L, o = {}) {
    const P = "#170d06";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="4600" fill="#1c1009"/>`);
    let s = "";
    const screen = (y0) => `<rect x="-40" y="${y0}" width="1160" height="900" fill="url(#ppScreen)"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-40 + k * 40},${y0}V${y0 + 900}" stroke="#c98a44" stroke-width="1.5" opacity=".25"/>`).join("")}`;
    const person = (x, y, s2, pose = "stand") => pose === "lie"
      ? `<g transform="translate(${x},${y}) scale(${s2})" fill="${P}"><rect x="-260" y="-6" width="520" height="16" rx="4"/><circle cx="-190" cy="-52" r="42"/><path d="M-150,-90Q-40,-110 80,-86L200,-70Q230,-50 200,-26L-150,-12Q-170,-50 -150,-90Z"/></g>`
      : `<g transform="translate(${x},${y}) scale(${s2})" fill="${P}"><circle cx="0" cy="-300" r="44"/><circle cx="0" cy="-350" r="22"/><path d="M-50,-250H50L70,0H-70Z"/><path d="M-50,-230L-110,-120M50,-230L110,-130" stroke="${P}" stroke-width="22" stroke-linecap="round"/></g>`;
    const house = (x, y) => `<g fill="${P}"><path d="M${x - 220},${y - 300}L${x},${y - 460}L${x + 220},${y - 300}Z"/><rect x="${x - 190}" y="${y - 300}" width="380" height="160"/>${[-170, -60, 60, 170].map((d) => `<rect x="${x + d - 8}" y="${y - 140}" width="16" height="140"/>`).join("")}</g>`;
    // 1: an ordinary woman by her house, by day
    s += screen(0) + house(700, 800) + person(300, 820, 1.2);
    // 2: at night, a black shape slipping into a sleeper
    s += screen(1000) + `<rect x="-40" y="1000" width="1160" height="900" fill="#0a0604" opacity=".35"/>` + person(560, 1700, 1.4, "lie") + `<path d="M520,1180Q420,1400 300,1600" stroke="${P}" stroke-width="34" fill="none" stroke-linecap="round"/><ellipse cx="540" cy="1170" rx="60" ry="74" fill="${P}"/>${[-14, 14].map((d) => `<circle cx="${540 + d}" cy="1160" r="7" fill="#7dff6a"/>`).join("")}`;
    // 3: it eats from the inside — the sleeper thin, a black knot in the belly
    s += screen(2000) + person(560, 2700, 1.4, "lie") + `<ellipse cx="580" cy="2588" rx="120" ry="34" fill="url(#ppScreen)"/><path d="M490,2590q30,-30 60,0t60,0t50,-6" stroke="${P}" stroke-width="16" fill="none" stroke-linecap="round"/><circle cx="660" cy="2582" r="14" fill="${P}"/>`;
    // 4: and then that person dies — a body under a cloth, two candles
    s += screen(3000) + `<rect x="300" y="3730" width="520" height="16" rx="4" fill="${P}"/><path d="M330,3730Q560,3600 800,3730Z" fill="${P}"/>${[270, 850].map((x) => `<rect x="${x - 10}" y="3560" width="20" height="160" fill="${P}"/><path d="M${x},3560q-16,-30 0,-56q16,26 0,56z" fill="#fff3c8"/>`).join("")}`;
    put(L.set, s);
  }

  // ---------------- end card: the community-forest sign ----------------
  function forestSign(L, o = {}) {
    const id = o.id || "fs", r = mk(o.seed || 361);
    sky(L, { time: "dusk" }, r);
    put(L.mid, `<rect x="-1200" y="1500" width="3500" height="1200" fill="#6a3a20"/>`);
    let s = `<rect x="420" y="-800" width="240" height="3400" fill="#5a4030" ${OUT}/>${Array.from({ length: 14 }, (_, k) => `<path d="M430,${-700 + k * 220}l220,${-10 + (k % 3) * 10}" stroke="#3a2818" stroke-width="5"/>`).join("")}`;
    s += `<g id="${id}-sign" transform="rotate(-2 540 900)"><rect x="170" y="560" width="740" height="560" rx="18" fill="#c8a066" ${OUT}/><rect x="200" y="590" width="680" height="500" rx="10" fill="none" stroke="#8a6438" stroke-width="8"/>
      <text x="540" y="680" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="56" fill="#3a2414">ป่าชุมชนบ้านโคกเห็ด</text>
      <text x="540" y="750" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="38" fill="#5a3a20">ไม่รู้จัก… ไม่เก็บ</text>
      ${mush(330, 1030, 0.7, {})}
      <g transform="rotate(4 600 920)"><rect x="420" y="800" width="400" height="240" fill="#f4ecd8" ${OUT3}/><circle cx="620" cy="808" r="12" fill="#c8342a"/>
        <text x="620" y="880" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="36" fill="#c8342a">${o.ep || "ตอนที่ 2"}</text>
        <text x="620" y="950" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="50" fill="${INK}">${o.title || ""}</text>
        <text x="760" y="1016" text-anchor="end" font-family="Kanit" font-weight="500" font-size="24" fill="#5a4a3a">— ยายคำ</text></g></g>`;
    put(L.set, s);
  }

  // ---------------- motion ----------------
  function life(tl, scope, t0, dur) {
    const q = (c) => Array.from(document.querySelectorAll(`${scope} ${c}`));
    q(".psteam").forEach((el, i) => tl.fromTo(el, { y: 0, opacity: 0.8 }, { y: -40, opacity: 0.5, duration: 1.6, repeat: Math.ceil(dur / 1.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.2));
    q(".pfire").forEach((el) => tl.fromTo(el, { scaleY: 1, svgOrigin: "0 -24" }, { scaleY: 1.18, svgOrigin: "0 -24", duration: 0.18, repeat: Math.ceil(dur / 0.18), yoyo: true, ease: "none", immediateRender: false }, t0));
    q(".pcloud").forEach((el) => tl.fromTo(el, { x: 0 }, { x: 60, duration: dur, ease: "none", immediateRender: false }, t0));
    q(".prain").forEach((el) => tl.fromTo(el, { y: -200 }, { y: 0, duration: 0.35, repeat: Math.ceil(dur / 0.35), ease: "none", immediateRender: false }, t0));
    q(".pbob").forEach((el) => tl.fromTo(el, { y: 0 }, { y: -8, duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
  }

  Object.assign(Sets, { isanVillage, dryForest, underHouse, bedNet, floorGap, nightRoad, erFront, ward, feetClose, mushClose, mushSection, clockCard, popLegend, forestSign });
  window.Pop = { ghost, lurk, eyes, mush, pickup, basket, pot, bowl, stove, kratip, lamp, stiltHouse, life, PBL, PEYE };
})();
