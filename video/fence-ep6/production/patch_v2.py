# patch_v2.py : shots.part for the tightened EP.6 (2:36) — lines removed/merged, new fragment indices, the merged chapter,
# and the key-moment acting pass (gas inserts and reactions, the turn + hand-in-hand exit, reaction cuts in the talk scenes)
import re
p = "shots.part"; s = open(p).read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:90])
    s = s.replace(old, new)
def block(start, end):
    a = s.index(start); b = s.index(end, a)
    return a, b

# ---- 1. hook: push in on the two labels at "มีน้ำยาอยู่สองขวด" ----
rep('cam: { keys: [{ t: 0, ...fr(540, 1180, 1.0, 540, 960), drift: { s: 0.01 } }, { t: vo("hook", 2) - 0.05, glide: 0.4, ...fr(540, 1380, 1.2, 540, 1000), drift: { s: 0.02 } }] },',
    'cam: { keys: [{ t: 0, ...fr(540, 1180, 1.0, 540, 960), drift: { s: 0.01 } }, { t: vo("hook", 1) - 0.05, ...fr(540, 1150, 1.28, 540, 1000), drift: { s: 0.015 } }, { t: vo("hook", 2) - 0.05, glide: 0.4, ...fr(540, 1380, 1.2, 540, 1000), drift: { s: 0.02 } }] },')

# ---- 2+3. the chapter takes over the road shot (the far shot and its two lines are gone) ----
a, _ = block('      // ---------- 2. chapter:', 'add("chapter", {')
b = s.index('      // ---------- 4. the gate:')
s = s[:a] + '''      // ---------- 2. chapter: the board over the road at dawn; the six walk up behind the guard; the camera reaches the lit fence ----------
      add("chapter", {
        set: "estateFar", setOpts: { id: "ch", time: "morning" }, dark: 0.12, blur: { far: 3 },
        cam: { keys: [{ t: 0, ...fr(540, 1520, 0.82, 540, 1180), drift: { s: 0.012 } }, { t: F("chapter", 0, 2) - 0.05, glide: 0.9, ...fr(540, 1180, 1.55, 540, 1150), drift: { s: 0.02 } }] },
        captions: caps("chapter"),
        ui: [{ type: "board", t: 0.05, day: "94", ep: "ตอนที่ 6 · นิคม", top: 300 }],
        fx(tl, id, t0, L) {
          // the six of them on the verge, small against the paddies, the guard in front with his rifle
          [["guard", 600, 0.36, "rifle"], ["phu", 480, 0.36], ["pim", 380, 0.36], ["pun", 310, 0.22], ["kong", 220, 0.36, "spear1"], ["hong", 120, 0.35]].forEach(([w, x, s, prop], k) => {
            const aid = `ch-w${k}`; rigIn(tl, L.act, aid, w, x, 1830, s, t0, D("chapter"), [{ t: 0, mode: "walk", eyes: "squint", mouth: "flat", opts: { period: 1.05 } }], false, prop);
            routeS(tl, aid, t0, [{ t: 0, x, y: 1830, s }, { t: D("chapter"), x: x + 430, y: 1810, s: s * 0.97 }]);
          });
          // the lamps along the fence breathe
          tl.fromTo(`#${id}-glow`, { opacity: 0.8 }, { opacity: 1, duration: 0.8, repeat: Math.ceil(D("chapter") / 0.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
          Fx.heart(tl, t0 + 0.6, D("chapter") - 0.6, 0.7, 0.3); Fx.punch(tl, `#${id} .stage`, t0 + F("chapter", 0, 2) + 0.2, 1.05, 0.3);
        },
      });

''' + s[b:]

# ---- 4. gate: "หันมามองภู" is now the line's second fragment ----
rep('FA("gate", vo("gate", 1) - 0.1, 1, 2)', 'FA("gate", vo("gate", 1) - 0.1, 1, 1)', 2)

# ---- 5. win: no narrator line; the skill card rides the welcome, ปั้น's line is index 1 ----
a, b = block('      add("win", {', '      // ---------- 6. the offer')
w = s[a:b]
w = w.replace('{ t: vo("win", 2) - 0.05, ...fr(470, 1300, 1.25, 540, 960)', '{ t: vo("win", 1) - 0.05, ...fr(470, 1300, 1.25, 540, 960)')
w = w.replace('{ t: vo("win", 1), mode: "idle", eyes: "normal", mouth: "smile" }', '{ t: voEnd("win", 0) + 0.2, mode: "idle", eyes: "normal", mouth: "smile" }')
w = w.replace('{ t: vo("win", 2), mode: "idle", eyes: "wide", mouth: "o" }', '{ t: vo("win", 1), mode: "idle", eyes: "wide", mouth: "o" }')
w = w.replace('{ t: vo("win", 2) - 0.2, mode: "point", eyes: "wide", mouth: "o" }', '{ t: vo("win", 1) - 0.2, mode: "point", eyes: "wide", mouth: "o" }')
w = w.replace('        captions: caps("win", [1]),\n', '')
w = w.replace('bub("win", 2, 560, 1060, 520, { br: true })', 'bub("win", 1, 560, 1060, 520, { br: true })')
w = w.replace('{ type: "skill", t: vo("win", 1) + 0.1, end: vo("win", 2) - 0.1, x: 40, y: 900,', '{ type: "skill", t: 1.0, end: vo("win", 1) + 0.3, x: 560, y: 1260,')
w = w.replace('const P = t0 + vo("win", 2) + 0.15;', 'const P = t0 + vo("win", 1) + 0.15;')
assert 'vo("win", 2)' not in w and 'caps("win"' not in w, w
s = s[:a] + w + s[b:]

# ---- 6. offer: reaction cuts — ก้อง lights up at "ไฟฟ้า น้ำประปา", ครูพิม wary at "แลกกับอย่างเดียว…" ----
rep('''        ui: [{ type: "signs", t: 0.1, items: ["ห้องนอน",''', '''        react: [{ a: 3, t: F("offer", 0, 2) - 0.05, dur: 1.1, fast: true }, { a: 2, t: vo("offer", 1) + 0.15, dur: F("offer", 1, 1) - vo("offer", 1) - 0.5, fast: true }],
        ui: [{ type: "signs", t: 0.1, items: ["ห้องนอน",''')
rep('KO(1080, 1560, 0.9, [{ t: 0, mode: "idle", eyes: "wide", mouth: "smileOpen" }], { flip: true, prop: "spear1" })],\n        react:',
    'KO(1080, 1560, 0.9, [{ t: 0, mode: "idle", eyes: "normal", mouth: "smile" }, { t: F("offer", 0, 2) - 0.1, mode: "idle", eyes: "wide", mouth: "smileOpen" }], { flip: true, prop: "spear1" })],\n        react:')

# ---- 7. register: no narrator line (w04 is 0, d02 is 1); a beat on ปั้น's face at the stamp ----
a, b = block('      add("register", {', '      // ---------- 8. he already knows')
w = s[a:b]
w = w.replace('vo("register", 1)', 'vo("register", 0)').replace('vo("register", 2)', 'vo("register", 1)').replace('voEnd("register", 2)', 'voEnd("register", 1)')
w = w.replace('        captions: caps("register", [0]),\n', '')
w = w.replace('bubbles: [bub("register", 1, 160, 760, 220), bub("register", 2, 480, 760, 260)],',
              'bubbles: [bub("register", 0, 160, 760, 220), bub("register", 1, 480, 760, 260)],\n        react: [{ a: 2, t: voEnd("register", 1) + 0.45, dur: D("register") - voEnd("register", 1) - 0.55, fast: true }],   // "รอดู": ปั้น')
assert 'caps("register"' not in w and 'register", 2' not in w
s = s[:a] + w + s[b:]

# ---- 8. knows C: the shortened line has two fragments — the reveal is index 1 ----
rep('react: [{ a: 2, t: FA("knows", vo("knows", 2) - 0.1, 2, 3) - 0.12, dur: 1.5, fast: true }],', 'react: [{ a: 2, t: FA("knows", vo("knows", 2) - 0.1, 2, 1) - 0.12, dur: 1.5, fast: true }],')
rep('at: [0.05, 0.25, FA("knows", vo("knows", 2) - 0.1, 2, 1) - 0.2], top: 230 }],', 'at: [0.05, 0.2, 0.4], top: 230 }],')
rep('const A = vo("knows", 2) - 0.1, H = t0 + FA("knows", A, 2, 3);', 'const A = vo("knows", 2) - 0.1, H = t0 + FA("knows", A, 2, 1);')

# ---- 9. workshop: the recipe runs on fixed beats (collar, rubber, build — mix.py uses the same three); ครูพิม answers with her face ----
rep('      split("workshop", vo("workshop", 1) - 0.35, {', '      const WP1 = F("workshop", 0, 1), WP2 = WP1 + 0.75, WB = WP2 + 1.1;   // collar, rubber, build\n      split("workshop", vo("workshop", 1) - 0.35, {')
rep('parts: [{ icon: "spear", label: "หอกมีด +1", at: F("workshop", 0, 0) + 0.25 }, { icon: "pipe", label: "ปลอกเหล็ก", at: F("workshop", 0, 1) }, { icon: "tape", label: "ยางพันด้าม", at: F("workshop", 0, 2) }],',
    'parts: [{ icon: "spear", label: "หอกมีด +1", at: F("workshop", 0, 0) + 0.25 }, { icon: "pipe", label: "ปลอกเหล็ก", at: WP1 }, { icon: "tape", label: "ยางพันด้าม", at: WP2 }],')
rep('build: voEnd("workshop", 0) + 0.35, result:', 'build: WB, result:')
rep('{ type: "callback", t: voEnd("workshop", 0) + 1.3, end: vo("workshop", 1) - 0.45,', '{ type: "callback", t: WB + 0.5, end: vo("workshop", 1) - 0.4,')
rep('const P1 = F("workshop", 0, 1), P2 = F("workshop", 0, 2), B = voEnd("workshop", 0) + 0.35 + 0.55;', 'const P1 = WP1, P2 = WP2, B = WB + 0.55;')
rep('tl.fromTo(w, { opacity: 0, scaleY: 0.3 }, { opacity: 1, scaleY: 1, transformOrigin: "50% 50%", duration: 0.1, immediateRender: false }, t0 + P2 + 0.05 + k * 0.11));',
    'tl.fromTo(w, { opacity: 0, scaleY: 0.3 }, { opacity: 1, scaleY: 1, transformOrigin: "50% 50%", duration: 0.08, immediateRender: false }, t0 + P2 + 0.05 + k * 0.075));')
rep('tl.to(c, { k: 1, duration: 1.3, ease: "none", immediateRender: false,', 'tl.to(c, { k: 1, duration: 0.9, ease: "none", immediateRender: false,')
rep('A("#ws-hm", "translate(410,1490) rotate(-100) scale(0.6,0.6)", "translate(1700,1700) rotate(-90) scale(0.6,0.6)", P2 + 1.45, 0.5, "power2.in");',
    'A("#ws-hm", "translate(410,1490) rotate(-100) scale(0.6,0.6)", "translate(1700,1700) rotate(-90) scale(0.6,0.6)", P2 + 1.0, 0.45, "power2.in");')
rep('PI(1200, 1560, 0.9, [{ t: 0, mode: "idle", eyes: "normal", mouth: "flat" }, { t: VA("workshop", vo("workshop", 1) - 0.35, 2) - 0.2, mode: "think", eyes: "worry", mouth: "frown" }]),',
    'PI(1200, 1560, 0.9, [{ t: 0, mode: "idle", eyes: "normal", mouth: "flat" }, { t: voEnd("workshop", 1) - (vo("workshop", 1) - 0.35) + 0.05, mode: "think", eyes: "worry", mouth: "frown" }]),')
rep('bubbles: [bubAt(bub("workshop", 1, 330, 520, 210), vo("workshop", 1) - 0.35, D("workshop")), bubAt(bub("workshop", 2, 320, 440, 220), vo("workshop", 1) - 0.35, D("workshop"))],   // both lines play in the speaker close-up (face at ~540, 860): the bubble sits over the head',
    'bubbles: [bubAt(bub("workshop", 1, 330, 520, 210), vo("workshop", 1) - 0.35, D("workshop"))],   // the line plays in the speaker close-up (face at ~540, 860): the bubble sits over the head\n        react: [{ a: 1, t: voEnd("workshop", 1) - (vo("workshop", 1) - 0.35) + 0.1, dur: D("workshop") - voEnd("workshop", 1) - 0.3, fast: true }],   // ครูพิม doesn\'t answer')

# ---- 12. mix: an insert on the pour and the labels while the narrator names them; back out for the gas ----
rep('cam: { keys: [{ t: 0, ...fr(760, 1370, 1.35, 540, 1000), drift: { s: 0.015 } }, { t: vo("mix", 1) - 0.05, glide: 0.5, ...fr(700, 1300, 1.0, 540, 1100), drift: { s: 0.015 } }] },',
    'cam: { keys: [{ t: 0, ...fr(760, 1370, 1.35, 540, 1000), drift: { s: 0.015 } }, { t: vo("mix", 1) - 0.05, ...fr(850, 1500, 2.1, 540, 1080), drift: { s: 0.02 } }, { t: vo("mix", 2) - 0.25, glide: 0.4, ...fr(700, 1300, 1.0, 540, 1100), drift: { s: 0.015 } }] },')
rep('actors: [YA(640, 1590, 0.9, [{ t: 0, mode: "pourKneel", eyes: "normal", mouth: "flat" }, { t: vo("mix", 1) + 0.6, mode: "scrub", eyes: "normal", mouth: "flat" }], { prop: "acidPour" })],',
    'actors: [YA(640, 1590, 0.9, [{ t: 0, mode: "pourKneel", eyes: "normal", mouth: "flat" }, { t: vo("mix", 2) - 0.3, mode: "scrub", eyes: "normal", mouth: "flat" }], { prop: "acidPour" })],')
rep('tl.set("#mx-pour", { opacity: 1 }, t0 + 0.4); tl.set("#mx-pour", { opacity: 0 }, t0 + vo("mix", 1) + 0.55);',
    'tl.set("#mx-pour", { opacity: 1 }, t0 + 0.4); tl.set("#mx-pour", { opacity: 0 }, t0 + vo("mix", 2) - 0.35);')
rep('repeat: Math.ceil(vo("mix", 1) / 0.5) + 1, ease: "none", immediateRender: false }, t0 + 0.4);', 'repeat: Math.ceil(vo("mix", 2) / 0.5) + 1, ease: "none", immediateRender: false }, t0 + 0.4);')

# ---- 14. signs: cuts on the beats — ยาย's eyes, เจ๊หงส์ fighting for breath, ยาย at "ถึงตายได้" ----
rep('HO(220, 1590, 0.9, [{ t: 0, mode: "cough", eyes: "pain", mouth: "o" }, { t: 2.0, mode: "wipeEyes", eyes: "closed", mouth: "frown" }, { t: 4.2, mode: "cough", eyes: "pain", mouth: "o" }])],\n        captions: caps("signs"),',
    'HO(220, 1590, 0.9, [{ t: 0, mode: "cough", eyes: "pain", mouth: "o" }, { t: 1.0, mode: "wipeEyes", eyes: "closed", mouth: "frown" }, { t: 2.8, mode: "cough", eyes: "pain", mouth: "o" }])],\n        captions: caps("signs"),\n        react: [{ a: 0, t: F("signs", 0, 1) - 0.05, dur: 1.2, fast: true }, { a: 1, t: F("signs", 0, 2) - 0.05, dur: 1.1, fast: true }, { a: 0, t: F("signs", 1, 3) - 0.1, dur: D("signs") - F("signs", 1, 3) - 0.1, fast: true }],')

# ---- 15. out: ครูพิม runs in, turns for the door (a quick squash through edge-on) and leads ยาย out by the hand; ภู has one line ----
rep('actors: [PI(-300, 1590, 0.9, [{ t: 0, mode: "run", eyes: "wide", mouth: "scream" }, { t: 0.9, mode: "leadHand", eyes: "squint", mouth: "grit" }], { moveTo: { x: 500, dur: 0.9, ease: "power1.out" } }),',
    'actors: [PI(-300, 1590, 0.9, [{ t: 0, mode: "run", eyes: "wide", mouth: "scream" }, { t: 0.9, mode: "leadHand", eyes: "squint", mouth: "grit" }], { moveTo: { x: 290, dur: 0.9, ease: "power1.out" } }),')
rep('{ t: 1.05, mode: "coughLed", eyes: "closed", mouth: "o" }], { flip: true, moveTo: { x: 520, dur: vo("out", 1) - 1.15, at: 1.05 } }),',
    '{ t: 1.05, mode: "coughLed", eyes: "closed", mouth: "o" }], { flip: true, moveTo: { x: 490, dur: vo("out", 1) - 0.1 - 1.06, at: 1.06 } }),')
rep('route(tl, `${id}-a0`, t0, [{ t: 1.0, x: 500, y: 1590 }, { t: vo("out", 1) - 0.1, x: 230, y: 1590 }], 0.9, true);   // ครูพิม turns for the door and leads her out',
    '''const pg = document.getElementById(`${id}-a0`), turn = { k: 0 };   // ครูพิม turns for the door: squash through edge-on, then she faces left
          tl.to(turn, { k: 1, duration: 0.12, ease: "power1.inOut", immediateRender: false, onUpdate: () => pg.setAttribute("transform", `translate(290,${(1590 - 10 * Math.sin(turn.k * Math.PI)).toFixed(1)}) scale(${(0.9 * (1 - 2 * turn.k)).toFixed(3)},0.9)`) }, t0 + 0.93);
          route(tl, `${id}-a0`, t0, [{ t: 1.06, x: 290, y: 1590 }, { t: vo("out", 1) - 0.1, x: 140, y: 1590 }], 0.9, true);   // and leads ยาย out by the hand, a constant arm's length (350) ahead of her''')
rep('bubbles: [bubAt(bub("out", 1, 120, 640, 300, { br: true }), vo("out", 1) - 0.1, D("out")), bubAt(bub("out", 2, 120, 640, 300, { br: true }), vo("out", 1) - 0.1, D("out"))],',
    'bubbles: [bubAt(bub("out", 1, 120, 560, 300, { br: true }), vo("out", 1) - 0.1, D("out"))],')
rep('end: VA("out", vo("out", 1) - 0.1, 2) - 0.1, x: 600, y: 1180, name: "ภู",', 'end: FA("out", vo("out", 1) - 0.1, 1, 1) - 0.1, x: 600, y: 1180, name: "ภู",')
rep('{ type: "tip", t: VA("out", vo("out", 1) - 0.1, 2), end: D("out") - (vo("out", 1) - 0.1) - 0.05, ill: "airout",', '{ type: "tip", t: FA("out", vo("out", 1) - 0.1, 1, 1), end: D("out") - (vo("out", 1) - 0.1) - 0.05, ill: "airout",')

# ---- 16. real: one line — the first card to "หายใจลำบาก…", the ambulance card after ----
rep('{ type: "tip", t: F("real", 0, 1) - 0.1, end: vo("real", 1) - 0.1, ill: "nomix",', '{ type: "tip", t: F("real", 0, 1) - 0.1, end: F("real", 0, 2) - 0.1, ill: "nomix",')
rep('{ type: "tip", t: vo("real", 1) + 0.1, end: D("real") - 0.05, ill: "amb",', '{ type: "tip", t: F("real", 0, 2), end: D("real") - 0.05, ill: "amb",')
rep('Fx.punch(tl, `#${id} .stage`, t0 + F("real", 1, 3), 1.05, 0.3);', 'Fx.punch(tl, `#${id} .stage`, t0 + F("real", 0, 3), 1.05, 0.3);')

# ---- 18. dinner: คุณวิน presides without a word; เจ๊หงส์'s whisper is the only line; ครูพิม's face after it ----
a, b = block('      add("dinner", {', '      // ---------- 19. sig')
w = s[a:b]
w = w.replace('cam: { keys: [{ t: 0, ...fr(520, 1240, 0.86, 540, 960), drift: { s: 0.012 } }, { t: vo("dinner", 1) - 0.1, glide: 0.5, ...fr(470, 1260, 1.35, 540, 960), drift: { s: 0.02 } }] },',
              'cam: { keys: [{ t: 0, ...fr(440, 1240, 0.82, 540, 960), drift: { s: 0.012 } }, { t: vo("dinner", 0) - 0.15, glide: 0.4, ...fr(470, 1260, 1.35, 540, 960), drift: { s: 0.02 } }] },')
w = w.replace('WI(-250, 1560, 0.9, [{ t: 0, mode: "present", eyes: "normal", mouth: "smile" }, { t: F("dinner", 0, 2) - 0.1, mode: "idle", eyes: "squint", mouth: "flat" }], { prop: "cup" }),',
              'WI(-120, 1560, 0.9, [{ t: 0, mode: "present", eyes: "normal", mouth: "smile" }, { t: 0.8, mode: "idle", eyes: "squint", mouth: "smile" }], { prop: "cup" }),')
w = w.replace('{ t: vo("dinner", 1) + 1.0, mode: "sitTable", eyes: "wide", mouth: "o", look: 8 }', '{ t: vo("dinner", 0) + 1.0, mode: "sitTable", eyes: "wide", mouth: "o", look: 8 }')
w = w.replace('{ t: vo("dinner", 1) - 0.2, mode: "lean", eyes: "worry", mouth: "frown" }', '{ t: vo("dinner", 0) - 0.2, mode: "lean", eyes: "worry", mouth: "frown" }')
w = w.replace('bubbles: [bub("dinner", 0, 80, 640, 200, { br: true }), bub("dinner", 1, 380, 640, 240, { br: true })],',
              'bubbles: [bub("dinner", 0, 380, 640, 240, { br: true })],\n        react: [{ a: 2, t: voEnd("dinner", 0) + 0.05, dur: D("dinner") - voEnd("dinner", 0) - 0.1, fast: true }],   // ครูพิม')
w = w.replace('Fx.punch(tl, `#${id} .stage`, t0 + F("dinner", 1, 1), 1.06, 0.4); red(tl, t0 + F("dinner", 1, 1), 0.4, 0.5);', 'Fx.punch(tl, `#${id} .stage`, t0 + F("dinner", 0, 1), 1.06, 0.4); red(tl, t0 + F("dinner", 0, 1), 0.4, 0.5);')
assert 'dinner", 1' not in w and 'dinner", 0, 2' not in w, w
s = s[:a] + w + s[b:]

# ---- 21. night B: cut in on the gate as it rolls shut on her ----
rep('cam: { keys: [{ t: 0, ...fr(560, 1220, 0.78, 540, 960), drift: { s: 0.02 } }] },\n        captions: capsFrom("night", NB, [1])',
    'cam: { keys: [{ t: 0, ...fr(560, 1220, 0.78, 540, 960), drift: { s: 0.02 } }, { t: FA("night", NB, 1, 2) - 0.35, ...fr(560, 1330, 1.3, 540, 1000), drift: { s: 0.03 } }] },\n        captions: capsFrom("night", NB, [1])')

# ---- the look: the chapter has the road's grass in front; no far shot ----
rep('hook: () => {}, chapter: (L) => { MORN(L); }, far: (L) => { MORN(L); Fence.depth(L, "grass", { op: 0.9 }); },', 'hook: () => {}, chapter: (L) => { MORN(L); Fence.depth(L, "grass", { op: 0.9 }); },')

open(p, "w").write(s)
# every F/FA/vo/voEnd/bub index must exist in the new schedule
import json
sch = {x["key"]: x for x in json.load(open("schedule.json"))["shots"]}
bad = []
for m in re.finditer(r'\b(F|FA|vo|voEnd|VA|bub|caps|capsFrom|capsAt)\("(\w+)"(?:,\s*([^,()]+(?:\([^()]*\))?[^,()]*))?(?:,\s*(\d+))?(?:,\s*(\d+))?', s):
    fn, k = m.group(1), m.group(2)
    if k not in sch: bad.append((fn, k, "no shot")); continue
    vos = sch[k]["vo"]
    args = [x for x in (m.group(3), m.group(4), m.group(5)) if x is not None]
    if fn in ("F",):
        i = int(args[0]) if args and args[0].strip().isdigit() else 0
        j = int(args[1]) if len(args) > 1 else 0
        if i >= len(vos) or j >= len(vos[i]["frags"]): bad.append((fn, k, i, j))
    elif fn == "FA":
        i = int(m.group(4)) if m.group(4) else 0; j = int(m.group(5)) if m.group(5) else 0
        if i >= len(vos) or j >= len(vos[i]["frags"]): bad.append((fn, k, i, j))
    elif fn in ("vo", "voEnd", "VA"):
        i = int(args[0]) if args and args[0].strip().isdigit() else (int(m.group(4)) if fn == "VA" and m.group(4) else 0)
        if i >= len(vos): bad.append((fn, k, i))
    elif fn == "bub":
        i = int(args[0]) if args and args[0].strip().isdigit() else 0
        if i >= len(vos): bad.append((fn, k, i))
print("patched; bad refs:", bad)
