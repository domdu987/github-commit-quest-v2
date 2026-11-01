// @_helpers
      // ---- v5: inserts are drawn at the identity camera (world = screen), the set behind thrown out of focus ----
      const ID = fr(540, 960, 1.0, 540, 960);
      const INS = (base, d, push = 0.04) => ({ ...base, blur: { far: 8, mid: 8, set: 9, fg: 14 }, cam: { keys: [{ t: 0, ...ID }, { t: d, glide: d, ...fr(540, 960, 1 + push, 540, 960) }] } });
      Rig.MODES.cup = (u, o) => ({ ...Rig.MODES.kneel(u, o), torso: 34, head: 6, uaF: -54, faF: -48, uaB: -44, faB: -56 });
      Rig.MODES.sitFire = (u, o) => ({ ...Rig.MODES.kneel(u, o), torso: 18, head: -4 + 2 * Math.sin(u * 1.2), uaF: -60, faF: -30, uaB: -20, faB: -60 });
      Rig.MODES.throwF = (u, o) => { const k = Math.min(1, u / 0.35); return { ...Rig.MODES.idle(u, o), torso: 10 * k - 6, head: -4, uaF: 40 - 150 * k, faF: -60 + 50 * k, uaB: 10, faB: -20 }; };
      const DAYR = (id, extra = {}) => ISLE(id, "day", "rocks", extra);
// @bottle
      // the clock: half a bottle of water in his hand
      add("bottle", { ...INS(ROCKS("bo", { fg: false }), D("bottle")), captions: caps("bottle"),
        fx(tl, id, t0, L) { life(tl, t0, D("bottle")); put(L.act, `<g transform="translate(560,1330) scale(1.7) rotate(-6)">${Isle.bottle("bo1", 0.5)}</g>${Isle.hand([470, 1180], 84, 2.2, { hand: { curl: [0.8, 0.85, 0.85, 0.9], thumb: 0.2 } })}`);
          tl.fromTo("#bo1-w", { y: 0 }, { y: 4, duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }, t0); } });
// @sun
      // the sun on the rocks all day: white heat, shimmer, him small and squinting
      add("sun", { ...DAYR("su", { tail: [460, 1500, 1.0], grey: true }), dark: 0, cam: { keys: [{ t: 0, ...fr(540, 1100, 1.05, 540, 1000) }, { t: D("sun"), glide: D("sun"), ...fr(540, 1080, 1.15, 540, 1000) }] }, captions: caps("sun"),
        actors: [A("kiw", 820, 1820, 1.2, [T("idle", "worry", "frown")], { flip: true })],
        fx(tl, id, t0, L) { life(tl, t0, D("sun")); put(L.light, `<rect id="su-h" width="1080" height="1920" fill="#fff6d8" opacity=".25" style="mix-blend-mode:screen"/>`);
          tl.fromTo("#su-h", { opacity: 0.1 }, { opacity: 0.35, duration: 0.4, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }, t0); } });
// @empty1
      // the last drop
      add("empty1", { ...INS(DAYR("e1", { fg: false }), D("empty1")), captions: caps("empty1"),
        fx(tl, id, t0, L) { life(tl, t0, D("empty1")); put(L.act, `<g transform="translate(560,620) scale(1.8) rotate(160)">${Isle.bottle("bo2", 0.03)}</g>`);
          tl.fromTo("#bo2-d", { opacity: 1, attr: { cy: -330 } }, { opacity: 1, attr: { cy: -560 }, duration: 0.6, ease: "power2.in", immediateRender: false }, t0 + 0.3); tl.to("#bo2-d", { opacity: 0, duration: 0.1 }, t0 + 0.9); } });
// @thirst
      // cracked lips (≥ 1/3) → he kneels at the water's edge and cups the sea in both hands
      seg("thirst", [
        [0, CU(DAYR("th1"), "kiw", 360, [T("idle", "worry", "frown")], { dx: 50 })],
        [C("thirst", 0, 1), (d) => ({ ...DAYR("th2", { fg: false }), cam: { keys: [{ t: 0, ...fr(560, 1380, 1.25, 540, 1100) }, { t: d, glide: d, ...fr(560, 1400, 1.35, 540, 1100) }] },
          actors: [A("kiw", 520, 1560, 1.3, [T("kneel", "wide", "o"), T("cup", "wide", "o", 0.35)])], fx(tl, id, t0) { life(tl, t0, d); } })],
      ]);
// @nosea
      // the cupped seawater stops at his mouth
      add("nosea", { ...INS(DAYR("ns", { fg: false }), D("nosea"), 0.08), captions: caps("nosea"), shake: (t) => ({ x: t < 0.2 ? 6 * Math.sin(t * 70) : 0, y: 0, r: 0 }),
        fx(tl, id, t0, L) { life(tl, t0, D("nosea")); put(L.act, `<g id="ns-h">${Isle.hand([470, 1120], 18, 2.4, { hand: { curl: [0.25, 0.25, 0.25, 0.3], thumb: 0.6 } })}${Isle.hand([610, 1120], -18, 2.4, { mirror: true, hand: { curl: [0.25, 0.25, 0.25, 0.3], thumb: 0.6 } })}<ellipse cx="540" cy="1000" rx="120" ry="34" fill="#5ab0d8" opacity=".85"/><path d="M450,990q90,-20 180,0" stroke="#fff" stroke-width="6" opacity=".7" fill="none"/></g>`);
          tl.fromTo("#ns-h", { y: 160 }, { y: 0, duration: 0.25, ease: "power3.out", immediateRender: false }, t0); } });
// @salt
      // the water runs out between his fingers onto the rock; the salt crust left where the sea dried
      add("salt", { ...INS(DAYR("sl", { fg: false }), D("salt")), captions: caps("salt"),
        fx(tl, id, t0, L) { life(tl, t0, D("salt")); const r = Pop2.mk(4);
          put(L.act, `<path d="M-200,1500Q300,1440 1300,1520V2200H-200Z" fill="#4a4a54"/>${Array.from({ length: 26 }, () => `<ellipse cx="${f1(r() * 1080)}" cy="${f1(1540 + r() * 300)}" rx="${f1(20 + r() * 60)}" ry="${f1(6 + r() * 14)}" fill="#f4f2ee" opacity="${f1(0.5 + r() * 0.4)}"/>`).join("")}
            ${Isle.hand([500, 1050], 0, 2.4, { hand: { curl: [0, 0, 0, 0], thumb: 0 } })}<g id="sl-dr">${Array.from({ length: 8 }, (_, k) => `<circle cx="${440 + k * 18}" cy="${980}" r="${6 + (k % 3) * 2}" fill="#7ac8f0"/>`).join("")}</g>`);
          tl.fromTo("#sl-dr", { y: 0, opacity: 1 }, { y: 560, opacity: 0.2, duration: 0.6, repeat: 3, ease: "power2.in", immediateRender: false }, t0); } });
// @look
      // he looks up: green coconuts high in the only palm
      add("look", { ...DAYR("lk", { fg: false }), cam: { keys: [{ t: 0, ...fr(480, 1200, 0.95, 540, 1000) }, { t: D("look"), glide: D("look"), ...fr(460, 1000, 1.05, 540, 1000) }] }, captions: caps("look"),
        actors: [A("kiw", 330, 1820, 1.3, [T("lookUp", "wide", "o")])],
        fx(tl, id, t0, L) { life(tl, t0, D("look")); put(L.act, `<g>${Tide.coco(760, 1850, 1.3, -0.12, 41, { pal: ["#2f6e3a", "#4f9a44", "#9ccc6a"] })}</g>`); } });
// @coco
      // he knocks one down and opens it on the wreck's torn metal: the water inside · the brown, ripe one beside it
      add("coco", { ...INS(DAYR("cc", { fg: false }), D("coco")), captions: caps("coco"),
        cam: { keys: [{ t: 0, ...fr(420, 1100, 1.15, 540, 960) }, { t: C("coco", 0, 2), ...fr(440, 1100, 1.2, 540, 960) }, { t: C("coco", 0, 2) + 0.35, ...fr(800, 1180, 1.3, 540, 960) }, { t: D("coco"), glide: D("coco") - C("coco", 0, 2) - 0.35, ...fr(810, 1180, 1.36, 540, 960) }] },
        fx(tl, id, t0, L) { life(tl, t0, D("coco")); put(L.act, `<path d="M-300,1400Q500,1340 1500,1420V2400H-300Z" fill="#6a6a74"/><g transform="translate(400,1060)">${Isle.coconut("open", { s: 2.1 })}</g>${Isle.hand([250, 1210], 60, 2.0, { hand: { curl: [0.6, 0.7, 0.7, 0.75], thumb: 0.3 } })}
            <g transform="translate(820,1320)">${Isle.coconut("brown", { s: 1.7 })}</g>`); } });
// @onetree
      // wide: the whole rock and its one palm
      add("onetree", { ...DAYR("ot", { tail: [460, 1500, 1.0], grey: true, palms: 1 }), cam: { keys: [{ t: 0, ...fr(300, 1200, 0.62, 540, 960) }, { t: D("onetree"), glide: D("onetree"), ...fr(300, 1200, 0.56, 540, 960) }] }, captions: caps("onetree"),
        actors: [A("kiw", -560, 1460, 0.9, [T("idle", "worry", "frown")])], fx(tl, id, t0) { life(tl, t0, D("onetree")); } });
// @rain
      // night rain: the plastic sheet from the wreck tied between rocks, its belly filling, dripping into the bottle
      add("rain", { ...ISLE("rn", "night", "rocks", { tail: [-200, 1420, 1.0] }), cam: { keys: [{ t: 0, ...fr(560, 1400, 1.2, 540, 1000) }, { t: D("rain"), glide: D("rain"), ...fr(560, 1420, 1.3, 540, 1000) }] }, captions: caps("rain"),
        actors: [A("kiwHidden", 200, 1760, 1.2, [T("crouch", "normal", "smile")])],
        fx(tl, id, t0, L) { life(tl, t0, D("rain")); Isle.life3(tl, t0, D("rain")); put(L.act, `${Isle.sheet("rs", 620, 1420, 560)}<g transform="translate(620,1760) scale(.8)">${Isle.bottle("rb", 0.1)}</g>`); Isle.rainOver(L, "rn");
          tl.fromTo("#rb-w", { scaleY: 1, svgOrigin: "0 0" }, { scaleY: 6, svgOrigin: "0 0", duration: D("rain"), ease: "none", immediateRender: false }, t0);
          tl.fromTo("#rs-pool", { attr: { rx: 40 } }, { attr: { rx: 110 }, duration: D("rain"), ease: "none", immediateRender: false }, t0); } });
// @glow
      seg("glow", [
        [0, (d) => ({ ...ISLE("gl", "night", "rocks", { fire: [900, 900], tail: [-300, 1400, 1.0] }), cam: { keys: [{ t: 0, ...fr(760, 960, 1.4, 540, 960) }, { t: d, glide: d, ...fr(860, 920, 1.7, 540, 960) }] },
          fx(tl, id, t0) { tl.fromTo("#gl-fire", { opacity: 1 }, { opacity: 0.4, duration: 0.15, yoyo: true, repeat: 9, ease: "steps(1)", immediateRender: false }, t0); life(tl, t0, d); } })],
        // his face lit orange; the fire across the bay out of focus over his shoulder
        [C("glow", 0, 0) + 1.0, CU(ISLE("gl2", "night", "rocks", {}), "kiwHidden", 360, [T("idle", "wide", "o")], { dx: 50,
          fx(tl, id, t0, L, d) { warmFace(L, "gl2", "right", "#ff9a40", 0.7);
            put(L.light, `<g id="gl2-bk" filter="url(#plBlur6)"><circle cx="880" cy="560" r="150" fill="url(#isFireG)" opacity=".9"/><circle cx="880" cy="560" r="34" fill="#fff0c0"/><path d="M780,640h200l160,500h-520z" fill="#ffb060" opacity=".22"/></g>`);
            tl.fromTo("#gl2-bk", { opacity: 1 }, { opacity: 0.55, duration: 0.15, yoyo: true, repeat: 9, ease: "steps(1)", immediateRender: false }, t0); } })],
      ]);
// @tide
      // morning, low tide: limpets on the wet rock | a bush of bright red fruit, his hand reaching for it
      seg("tide", [
        [0, (d) => ({ ...INS(ISLE("td1", "dawn", "rocks", { fg: false }), d), fx(tl, id, t0, L) { life(tl, t0, d);
          put(L.act, `<path d="M-300,1250Q500,1180 1400,1260V2400H-300Z" fill="#4a4456"/><path d="M-300,1250Q500,1180 1400,1260V1420Q500,1360 -300,1420Z" fill="#6a6474"/><path d="M-300,1420Q500,1360 1400,1420" stroke="#2a2836" stroke-width="10" fill="none"/>${Isle.limpets(540, 1560, 14, 3)}${Isle.limpets(300, 1760, 8, 4)}${Isle.limpets(800, 1720, 8, 6)}`); } })],
        [C("tide", 0, 2), (d) => ({ ...INS(ISLE("td2", "dawn", "rocks", { fg: false }), d), fx(tl, id, t0, L) { life(tl, t0, d); Isle.life3(tl, t0, d);
          put(L.act, `${Isle.redBush("rbs", 420, 1500, 2.2)}<g id="td2h">${Isle.hand([900, 1080], -62, 2.2, { hand: { curl: [0.1, 0.15, 0.2, 0.25], thumb: 0.2 } })}</g>`);
          tl.fromTo("#td2h", { x: 400, y: 120 }, { x: 0, y: 0, duration: d, ease: "power1.out", immediateRender: false }, t0); } })],
      ]);
// @nofruit
      // his fingers stop a hair from the fruit
      add("nofruit", { ...INS(ISLE("nf", "dawn", "rocks", { fg: false }), D("nofruit"), 0.1), captions: caps("nofruit"), shake: (t) => ({ x: t < 0.18 ? 5 * Math.sin(t * 80) : 0, y: 0, r: 0 }),
        fx(tl, id, t0, L) { life(tl, t0, D("nofruit")); Isle.life3(tl, t0, D("nofruit")); put(L.act, `${Isle.redBush("rbn", 420, 1500, 2.2)}<g id="nfh">${Isle.hand([900, 1080], -62, 2.2, { hand: { curl: [0.1, 0.15, 0.2, 0.25], thumb: 0.2 } })}</g>`);
          tl.fromTo("#nfh", { x: 0 }, { x: 60, duration: 0.25, ease: "back.out(3)", immediateRender: false }, t0 + 0.05); } });
// @shell
      // only the shells the sea covers at high tide: the dark wet band under the waterline; he prises one off
      add("shell", { ...INS(ISLE("sh", "dawn", "rocks", { fg: false }), D("shell")), captions: caps("shell"),
        fx(tl, id, t0, L) { life(tl, t0, D("shell"));
          put(L.act, `<path d="M-300,900Q500,860 1400,920V2400H-300Z" fill="#8a8494"/><path d="M-300,1300Q500,1250 1400,1310V2400H-300Z" fill="#4a4456"/><path d="M-300,1300Q500,1250 1400,1310" stroke="#c8e4f0" stroke-width="8" stroke-dasharray="22 14" fill="none"/>
            ${Isle.limpets(540, 1520, 14, 7)}<g id="shh">${Isle.hand([640, 1400], -20, 2.2, { hand: { curl: [0.5, 0.6, 0.7, 0.75], thumb: 0.5 } })}</g>`);
          tl.fromTo("#shh", { x: 120, y: 80 }, { x: 0, y: 0, duration: 0.5, ease: "power2.out", immediateRender: false }, t0); tl.to("#shh", { y: -60, duration: 0.3, ease: "power2.in", immediateRender: false }, t0 + D("shell") - 0.5); } });
// @cook
      add("cook", { ...INS(ISLE("ck", "dawn", "rocks", { fg: false }), D("cook"), 0.06), captions: caps("cook"),
        fx(tl, id, t0, L) { life(tl, t0, D("cook")); put(L.act, `${Isle.firePit("ckf", 540, 1400, 2.4, { shells: true, smoke: "thin" })}`); life(tl, t0, D("cook")); } });
// @fire
      // the lighter from a passenger's bag; the fire catches; pull back: him crouched by it, thin smoke
      seg("fire", [
        [0, (d) => ({ ...INS(ISLE("fi1", "dawn", "rocks", { fg: false }), d, 0.06), fx(tl, id, t0, L) { life(tl, t0, d);
          put(L.act, `<g transform="translate(560,1060) scale(2.4)">${Isle.lighter("lt")}</g>${Isle.hand([500, 1420], 10, 2.2, { hand: { curl: [0.85, 0.85, 0.85, 0.9], thumb: 0.1 } })}`);
          tl.fromTo("#lt-f", { scale: 0, svgOrigin: "0 -46" }, { scale: 1, svgOrigin: "0 -46", duration: 0.2, ease: "back.out(3)", immediateRender: false }, t0 + 0.4); } })],
        [C("fire", 0, 1), (d) => ({ ...ISLE("fi2", "dawn", "rocks", { tail: [-300, 1420, 1.0] }), cam: { keys: [{ t: 0, ...fr(560, 1400, 1.1, 540, 1000) }, { t: d, glide: d, ...fr(560, 1380, 1.0, 540, 1000) }] },
          actors: [A("kiw", 300, 1760, 1.2, [T("sitFire", "normal", "smile")])], fx(tl, id, t0, L) { life(tl, t0, d); put(L.act, Isle.firePit("fif", 680, 1720, 1.0, { smoke: "thin" })); life(tl, t0, d); } })],
      ]);
// @rotor
      add("rotor", { ...ISLE("ro", "day", "rocks", { tail: [-300, 1420, 1.0] }), cam: { keys: [{ t: 0, ...fr(480, 1280, 1.35, 540, 1000) }, { t: D("rotor"), glide: D("rotor"), ...fr(480, 1240, 1.45, 540, 1000) }] }, captions: caps("rotor"),
        actors: [A("kiw", 360, 1760, 1.2, [T("sitFire", "normal", "smile"), T("lookUp", "wide", "o", 0.25)])], fx(tl, id, t0, L) { life(tl, t0, D("rotor")); put(L.act, Isle.firePit("rof", 720, 1720, 1.0, { smoke: "thin" })); life(tl, t0, D("rotor")); } });
// @bright
      // the safety card: his marker list (≥ half the screen) → the vest spread on the wreck
      seg("bright", [
        [0, (d) => ({ ...DAYR("br1", { tail: [460, 1500, 1.0], antenna: [700, 1260] }), blur: { far: 6, mid: 6, set: 6, fg: 10 }, cam: { keys: [{ t: 0, ...fr(560, 1100, 1.1, 540, 1000) }, { t: d, glide: d, ...fr(560, 1100, 1.14, 540, 1000) }] },
          fx(tl, id, t0, L) { life(tl, t0, d); Isle.card(tl, L.light, t0 + 0.02, d + 0.2, { id: "rc", title: "ทำให้ซากเด่น", y: 200, active: 0, done: [], at: [0.15],
            rows: [{ text: "วาง<u>ของสีสด</u>บนซาก", icon: "vest" }, { text: "<u>แผ่นโลหะ</u>สะท้อนแดด", icon: "mirror" }, { text: "<u>ใบไม้สด</u>ลงกองไฟ", icon: "leaf" }] }); } })],
        [C("bright", 0, 1), (d) => ({ ...DAYR("br2", { tail: [460, 1500, 1.0], vest: true, blanket: true }), cam: { keys: [{ t: 0, ...fr(560, 1100, 1.05, 540, 1000) }, { t: d, glide: d, ...fr(560, 1120, 1.12, 540, 1000) }] },
          actors: [A("kiw", 900, 1860, 1.3, [T("pointBack", "normal", "smile")], { flip: true })], fx(tl, id, t0) { life(tl, t0, d); } })],
      ]);
// @flash
      add("flash", { ...DAYR("fl", { tail: [460, 1500, 1.0], vest: true, blanket: true, panel: true }), cam: { keys: [{ t: 0, ...fr(260, 1180, 1.5, 540, 960) }, { t: D("flash"), glide: D("flash"), ...fr(260, 1180, 1.62, 540, 960) }] }, captions: caps("flash"),
        fx(tl, id, t0) { life(tl, t0, D("flash")); tl.fromTo("#fl-flash", { opacity: 0 }, { opacity: 1, duration: 0.1, yoyo: true, repeat: 7, immediateRender: false }, t0 + 0.3); } });
// @leaves
      // green leaves on the fire: thick white smoke climbs against the dark rock
      add("leaves", { ...ISLE("lv", "dusk", "rocks", { tail: [-300, 1420, 1.0], vest: true }), cam: { keys: [{ t: 0, ...fr(600, 1300, 1.0, 540, 1100) }, { t: D("leaves"), glide: D("leaves"), ...fr(620, 1100, 0.8, 540, 1100) }] }, captions: caps("leaves"),
        actors: [A("kiw", 380, 1780, 1.3, [T("throwF", "wide", "o")])],
        fx(tl, id, t0, L) { life(tl, t0, D("leaves")); put(L.act, `${Isle.firePit("lvf", 720, 1740, 1.0, { smoke: "white" })}<g id="lvl" transform="translate(560,1560)">${Array.from({ length: 5 }, (_, k) => `<path d="M0,0q30,-40 70,-10q-30,30 -70,10z" fill="#3a8a3a" transform="rotate(${k * 30 - 60})" stroke="#1a3a1a" stroke-width="2"/>`).join("")}</g>`);
          tl.fromTo("#lvl", { x: 0, y: 0, rotation: 0, svgOrigin: "560 1560" }, { x: 160, y: 120, rotation: 120, svgOrigin: "560 1560", duration: 0.5, ease: "power1.in", immediateRender: false }, t0 + 0.2); tl.to("#lvl", { opacity: 0, duration: 0.1 }, t0 + 0.7);
          tl.fromTo("#lvf-ws", { scaleY: 0.2, opacity: 0.3, svgOrigin: "0 -180" }, { scaleY: 1, opacity: 1, svgOrigin: "0 -180", duration: 1.6, ease: "power2.out", immediateRender: false }, t0 + 0.6); life(tl, t0, D("leaves")); } });
// @back
      add("back", { ...DAYR("bk", { tail: [460, 1500, 1.0], vest: true, blanket: true, panel: true }), cam: { keys: [{ t: 0, ...fr(520, 1000, 0.9, 540, 1000) }] }, captions: caps("back"),
        actors: [A("kiw", 880, 1860, 1.2, [T("wave2", "wide", "laugh")], { flip: true })],
        fx(tl, id, t0, L) { life(tl, t0, D("back")); tl.set("#bk-flash", { opacity: 1 }, t0); put(L.set, Isle.firePit("bkf", -80, 1700, 0.9, { smoke: "white" })); put(L.mid, `<g id="bkhl" transform="translate(1500,420) scale(-1.6,1.6)">${Isle.heliBig("hlb")}</g>`); Isle.heliShake(tl, "hlb", t0, D("back")); tl.to("#bkhl", { x: -760, y: 60, duration: D("back"), ease: "power2.out", immediateRender: false }, t0); life(tl, t0, D("back")); } });
// @end
      add("end", { ...DAYR("en", { tail: [460, 1500, 1.0], vest: true, antenna: [700, 1260] }), blur: { far: 6, mid: 6, set: 6, fg: 10 },
        cam: { keys: [{ t: 0, ...still(fr(540, 1100, 0.9, 540, 1000)) }] },
        fx(tl, id, t0, L) { life(tl, t0, D("end")); Isle.card(tl, L.light, t0 + 0.02, D("end"), { id: "ec", title: "รอดคนเดียว · 3 กฎ", y: 200, h: 1220, active: -1, done: [0, 1, 2], at: [0.15, 0.45, 0.75],
          rows: [{ text: "<u>อยู่กับซาก</u> อย่าเดินไป", icon: "stay", fs: 66 }, { text: "<u>อย่าดื่ม</u>น้ำทะเล", icon: "sea", fs: 66 }, { text: "<u>อย่ากิน</u>ของที่ไม่รู้จัก", icon: "fruit", fs: 66 }] }); } });
