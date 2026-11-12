// สกิลจอมโกหก v2 long cut · extra coin glyphs in the jkicons line style (ink lines, paper fills, one accent colour). Load after jkicons.js.
//   book (พูดให้คนเชื่อใน 7 วัน, pages flip) · flame (ไฟเบรกระเบิด) · chain (โซ่หนาม) · shield (เกราะสะท้อน) · gsword (ดาบทอง) · paper (ใบประกัน 112)
//   club (กระบองหิน) · coins (ทองร้อยเหรียญ) · rank0 (อันดับ 0) · sales (ยอดขาย) · mark (ตราจอมมาร) · moon (คืนนั้น)
(function () {
  const { C, INK } = NkV;
  const L5 = `fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"`;
  const O4 = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const T = (x, y, s, t, fill = INK) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${s}" fill="${fill}">${t}</text>`;
  const G = JKI.GLY;
  G.book = (id) => `<path d="M-30,-22Q-14,-30 0,-20Q14,-30 30,-22V24Q14,16 0,26Q-14,16 -30,24Z" fill="${C.red}" ${O4}/><path d="M0,-20V26" ${L5}/>
    <g id="${id}-pg"><path d="M2,-18Q14,-26 26,-20V20Q14,14 2,22Z" fill="${C.paper}" ${O4}/></g>${T(-15, 8, 24, "7", C.yellow)}`;
  G.flame = (id) => `<g id="${id}-fl2"><path d="M0,30Q-28,24 -26,-2Q-24,-20 -8,-34Q-10,-14 2,-10Q2,-26 14,-36Q30,-14 26,6Q22,28 0,30Z" fill="${C.red}" ${O4}/>
    <path d="M0,24Q-12,18 -10,4Q-6,-6 2,-10Q4,2 10,4Q16,16 0,24Z" fill="${C.yellow}"/></g>`;
  G.chain = (id) => `<g id="${id}-ch">${[[-22, -16], [-6, -2], [10, 12], [26, 26]].map(([x, y], k) => `<ellipse cx="${x}" cy="${y}" rx="12" ry="8" transform="rotate(${k % 2 ? -45 : 45} ${x} ${y})" fill="none" stroke="#8a8f98" stroke-width="7"/><ellipse cx="${x}" cy="${y}" rx="12" ry="8" transform="rotate(${k % 2 ? -45 : 45} ${x} ${y})" ${L5} stroke-width="3"/>`).join("")}
    <path d="M-34,-30l-6,-6M-14,-18l2,-8M2,4l8,-4M18,20l-6,6" ${L5} stroke-width="3"/></g>`;
  G.shield = (id) => `<g id="${id}-sd"><path d="M0,-32L26,-22Q26,14 0,32Q-26,14 -26,-22Z" fill="${C.yellow}" ${O4}/><path d="M0,-22V22M-14,-6h28" ${L5}/></g>
    <g id="${id}-rf"><path d="M-40,-8l-10,-6M-40,8l-10,6M40,-8l10,-6M40,8l10,6" ${L5}/></g>`;
  G.gsword = (id) => `<g id="${id}-gs" transform="rotate(-35)"><path d="M-5,-36H5V18H-5Z" fill="${C.yellow}" ${O4}/><path d="M-5,-36L0,-44L5,-36" fill="${C.yellow}" ${O4}/><path d="M-16,18H16" ${L5}/><path d="M0,20V36" ${L5} stroke-width="7"/></g>`;
  G.paper = (id) => `<g id="${id}-pp" transform="rotate(-8)"><rect x="-22" y="-30" width="44" height="58" rx="3" fill="${C.paper}" ${O4}/><rect x="-22" y="-30" width="44" height="13" fill="${C.blue}" ${O4}/>
    <path d="M-14,-6h28M-14,4h22M-14,14h26" ${L5} stroke-width="3.5"/>${T(8, 26, 12, "112")}</g>`;
  G.club = (id) => `<g id="${id}-cl" transform="rotate(30)"><path d="M-4,20V40" ${L5} stroke-width="8"/><path d="M-14,22Q-20,-10 -12,-36Q0,-44 12,-36Q20,-10 14,22Z" fill="#a8a49c" ${O4}/><circle cx="2" cy="-14" r="4" fill="${INK}"/><circle cx="-4" cy="4" r="3" fill="${INK}"/></g>`;
  G.coins = (id) => `<g id="${id}-cn">${[[-14, 12], [12, 12], [0, -4], [-10, -18], [14, -16]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="15" ry="9" fill="${C.yellow}" ${O4}/><path d="M${x - 6},${y}h12" ${L5} stroke-width="3"/>`).join("")}</g>`;
  G.rank0 = (id) => `<g id="${id}-r0">${T(0, 18, 54, "0")}<path d="M-30,-30L-20,-14M30,-30L20,-14M0,-40V-24" ${L5}/></g>`;
  G.sales = (id) => `<g id="${id}-sl"><path d="M-30,24V-4M-14,24V-14M2,24V-22M18,24V-34" ${L5} stroke-width="9"/><path d="M-30,-10L-14,-20L2,-28L26,-40" ${L5}/><path d="M16,-42l10,2l-2,10" ${L5}/></g>`;
  G.mark = (id) => `<circle r="22" ${L5}/><path d="M-8,-6v3M8,-6v3" ${L5}/><path d="M-8,10q8,-6 16,0" ${L5}/>
    <g id="${id}-mk"><path d="M0,-34l6,10h-12z" fill="${C.red}" ${O4}/><path d="M-16,-20Q-26,-34 -18,-46Q-18,-34 -10,-24Z" fill="#3a1a24" ${O4}/><path d="M16,-20Q26,-34 18,-46Q18,-34 10,-24Z" fill="#3a1a24" ${O4}/></g>`;
  G.moon = (id) => `<g id="${id}-mn"><path d="M8,-30A30,30 0 1 0 30,8A24,24 0 1 1 8,-30Z" fill="${C.yellow}" ${O4}/></g><g id="${id}-zz">${T(-20, -16, 16, "z")}${T(-30, -30, 12, "z")}</g>`;
})();
