import re, sys
W = "/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8").write(s)
def rep1(s, old, new, label=""):
    if s.count(old) == 0 and new in s: return s          # already applied on an earlier run
    assert s.count(old) == 1, f"{label}: {s.count(old)} matches for {old[:70]!r}"
    return s.replace(old, new)

# ---------------------------------------------------------------- isle.js: the cloth in the POV set, the draped blanket prop
p = f"{W}/hf/lib/isle.js"; s = rd(p)
old = '''      <g id="${id}-blur" opacity="0"><rect x="-1400" y="-900" width="4000" height="3800" fill="#9fb8d8" opacity=".18"/></g>`);
  }'''
new = '''      <g id="${id}-blur" opacity="0"><rect x="-1400" y="-900" width="4000" height="3800" fill="#9fb8d8" opacity=".18"/></g>`);
    // the blanket she pulls over his face, seen from under it: the shot tweens #id-clothg's y from 0 to 2100 so the hem slides down over
    // the whole view; once it has settled a little firelight (#id-leak) and the weave show through
    put(L.fg, `<g id="${id}-cloth" opacity="0"><g id="${id}-clothg"><rect x="-1400" y="-2800" width="4000" height="2800" fill="#2a2236"/>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M${-1300 + k * 440},-2800q${(k % 2 ? 90 : -70)},900 ${(k % 2 ? -40 : 60)},2790" stroke="#3b3050" stroke-width="${26 + (k % 3) * 10}" fill="none" opacity=".7"/>`).join("")}
      <path d="M-1400,0q200,-70 400,0t400,0t400,0t400,0t400,0t400,0t400,0t400,0V-120H-1400Z" fill="#2a2236"/>
      <path d="M-1400,-40q200,-70 400,0t400,0t400,0t400,0t400,0t400,0t400,0t400,0" stroke="#4a3d60" stroke-width="10" fill="none" opacity=".8"/>
      <g id="${id}-leak" opacity=".12"><circle cx="1500" cy="-900" r="900" fill="url(#iLampG)"/></g>
      ${Array.from({ length: 70 }, (_, k) => `<path d="M-1400,${-2780 + k * 40}H2600" stroke="#000" stroke-width="2" opacity=".12"/>`).join("")}</g></g>`);
  }'''
s = rep1(s, old, new, "lieDown cloth")
old = "  const STICKFISH = (x, y, s = 1, rot = -60) =>"
new = '''  // the purple blanket from the boat, draped over the boy's head on the sand (still#2 draws it up, rule#1 pulls it away)
  const CLOTH = (x, y, s = 1, rot = 0) => `<g transform="translate(${x},${y}) rotate(${rot}) scale(${s})"><path d="M-150,40Q-170,-30 -100,-70Q-30,-105 60,-85Q150,-60 160,20Q165,75 100,85Q0,95 -100,85Q-150,75 -150,40Z" fill="#8a6a9a" stroke="#2e2a26" stroke-width="4"/><path d="M-120,-10q70,30 140,0M-100,36q60,26 120,0" stroke="#6a4a7a" stroke-width="5" fill="none"/></g>`;
  const STICKFISH = (x, y, s = 1, rot = -60) =>'''
s = rep1(s, old, new, "CLOTH prop")
s = rep1(s, "window.Isle = { PALM, BOULDER, SHRINE, LAMP, FIRE, LONGTAIL, PUFFER, COCONUT, STICKFISH,", "window.Isle = { PALM, BOULDER, SHRINE, LAMP, FIRE, LONGTAIL, PUFFER, COCONUT, STICKFISH, CLOTH,", "export")
wr(p, s)

# ---------------------------------------------------------------- sys.part: the memory caption style
p = f"{W}/isle1/sys.part"; s = rd(p)
i = s.index('document.head.insertAdjacentHTML("beforeend", `<style>.capbox.inner')
j = s.index("\n", i)
if ".capbox.mem" not in s: s = s[:j + 1] + '      document.head.insertAdjacentHTML("beforeend", `<style>.capbox.mem { color: #f6dfb4; font-style: italic; letter-spacing: 1px; text-shadow: 0 0 18px rgba(255,200,120,.55), 0 2px 6px #000; }</style>`);   // ยาย\'s words heard again in memory\n' + s[j + 1:]
wr(p, s)

# ---------------------------------------------------------------- foot.part: the badge
p = f"{W}/isle1/foot.part"; s = rd(p)
s = rep1(s, "ติดเกาะร้าง · EP.1 ผีอำ", "ติดเกาะร้าง · EP.1 ปลาลูกโป่ง", "badge"); wr(p, s)

# ---------------------------------------------------------------- head.part: a static "sat up, weak" pose for the framings after the first stir
p = f"{W}/isle1/head.part"; s = rd(p)
old = "      Rig.MODES.sitUpWeak = (u, o) =>"
new = "      Rig.MODES.sitWeak = (u, o) => Rig.MODES.sitUpWeak(u + 1.2, o);   // already sat up (the later dawn framings start here, so he does not rise twice)\n      Rig.MODES.sitUpWeak = (u, o) =>"
s = rep1(s, old, new, "sitWeak"); wr(p, s)

# (shots.part and timing.py were rewritten on the previous run)
# ---------------------------------------------------------------- mix.py
p = f"{W}/isle1/mix.py"; s = rd(p)
s = rep1(s, 'PA2 = vo_t("phiam", 1) - 0.25\nLP2 = vo_t("lamp", 1) - 0.4\nDW2 = vo_t("dawn", 1) - 0.4; DW3 = vo_t("dawn", 2) - 0.25',
            'ST2 = vo_t("still", 1) - 0.25; ST3 = vo_t("still", 4) - 0.45\nRU2 = vo_t("rule", 2) - 0.5; RU3 = vo_t("rule", 3) - 0.3\nDW2 = vo_t("dawn", 1) - 0.4; DW3 = vo_t("dawn", 2) - 0.3', "mix consts")
s = rep1(s, 'LINE_GAIN = {"i01": -2, "i02": -2, "t10": 1, "t11": 1, "t12": 0, "p07": -1.5, "p09": -1.5, "m01": -1, "m02": -1, "m03": -1, "s01": 0}',
            'LINE_GAIN = {"i01": -2, "i02": -2, "i03": -2, "t10": 1, "t11": 1, "t12": 0, "p07": -1.5, "p11": -1, "y05": -3, "y06": -3, "p10": 0.5, "s01": 0}', "line gain")
a = s.index('    # ผีอำ: he goes down'); b = s.index('    # the safety card')
new = '''    # still: he goes down; the cut inside his head — the world muffled; her tears; she says it; the blanket drawn over his face
    ("still", 0.1, "thud", 0.8), ("still", 0.12, "rustle", 0.5), ("still", 0.1, "boom", 0.4), ("still", ST2, "whoosh", 0.4), ("still", ST2 + 0.05, "boom", 0.5),
    ("still", frag("still", 2, 3), "sting", 1.0), ("still", frag("still", 2, 3), "boom", 0.6), ("still", frag("still", 2, 3), "glitch", 0.4),
    *[("still", vo_t("still", 3) + o + 0.5, "drip", 0.6) for o in (0.2, 1.1, 2.0)],
    ("still", ST3, "whoosh", 0.3), ("still", frag("still", 4, 1), "sting", 0.8), ("still", frag("still", 4, 1), "boom", 0.5), ("still", vo_end("still", 4) + 1.15, "rustle", 0.8),
    *beats("still", 0.0, D["still"], 0.5, 0.85),
    # the cloth: from inside — the rustle over the ears, the heart louder, the world gone
    ("cloth", 0.1, "rustle", 0.9), ("cloth", 0.95, "boom", 0.5), ("cloth", 1.0, "sting", 0.5), *beats("cloth", 0.0, D["cloth"], 0.45, 1.0),
    # the rule: her grandmother's words; the blanket pulled back; the tear; the breath that stops; the first breaths she gives
    ("rule", vo_t("rule", 0) - 0.15, "whoosh", 0.35), ("rule", vo_t("rule", 0) - 0.1, "sting", 0.5), ("rule", frag("rule", 1, 1), "sting", 0.6),
    ("rule", RU2 + 0.15, "rustle", 0.7), ("rule", RU2 + 1.0, "drip", 0.5), ("rule", vo_t("rule", 2) - 0.1, "sting", 0.5),
    ("rule", RU3 + 0.3, "breath", 0.6), ("rule", frag("rule", 3, 0) - 0.3, "sting", 0.9), ("rule", frag("rule", 3, 0) - 0.3, "boom", 0.5), ("rule", frag("rule", 3, 0) - 0.3, "glitch", 0.3),
    ("rule", frag("rule", 3, 2) + 0.3, "breath", 0.9), ("rule", frag("rule", 3, 2) + 1.9, "breath", 0.9), *beats("rule", 0.0, D["rule"], 0.55, 0.65),
'''
s = s[:a] + new + s[b:]
a = s.index('    # dawn: gulls'); b = s.index('    # the boat home')
new = '''    # dawn: gulls, the first breath, the longtail coming in, feet on sand; what he sees; her answer; the stick by the fire
    *bed("waves", T("dawn", 0), T("dawn", -0.1), 0.26, 4.6), ("dawn", 0.3, "gull", 0.35), ("dawn", 2.2, "gull", 0.3), ("dawn", 0.9, "gasp", 0.7), ("dawn", 1.3, "cough", 0.4), ("dawn", vo_t("dawn", 0) - 0.1, "sting", 0.4),
    *bed("longtail", T("dawn", DW2 - 0.6), T("dawn", DW3 + 0.5), 0.35, 4.2), *[("dawn", DW2 + 0.2 + k * 0.3, "steps", 0.4) for k in range(5)],
    ("dawn", DW2 + 1.4, "breath", 0.6), ("dawn", frag("dawn", 1, 1), "sting", 0.7), ("dawn", frag("dawn", 1, 1), "boom", 0.4), ("dawn", DW2 + 1.9, "wash", 0.5),
    ("dawn", DW3, "whoosh", 0.35), ("dawn", frag("dawn", 2, 1), "sting", 0.9), ("dawn", frag("dawn", 2, 1), "boom", 0.5), ("dawn", vo_end("dawn", 2) + 1.7, "whoosh", 0.3),
    *beats("dawn", DW2, D["dawn"] - DW2, 0.55, 0.55),
'''
s = s[:a] + new + s[b:]
s = rep1(s, 'dip(T("phiam", 0), T("phiam", -0.05), 0.12)                          # the world drops away while he cannot move\ndip(T("lamp", 0), T("lamp", vo_t("lamp", 0) + 0.4), 0.2)\ndip(T("lamp", vo_t("lamp", 1) - 0.2), T("lamp", -0.05), 0.3)',
            'dip(T("still", 0), T("still", -0.05), 0.12)                          # the world drops away while he cannot move\ndip(T("cloth", 0), T("cloth", -0.05), 0.08)\ndip(T("rule", 0), T("rule", RU2), 0.3)', "dips")
for w in ('"phiam"', 'T("lamp"', '("lamp",', 'D["lamp"]', 'vo_t("lamp"', "LP2", "PA2", '"m01"'):
    assert w not in s, f"mix.py still has {w!r}"
s = s.replace("the dying fire, the lamp; the moon", "the dying fire; the moon").replace("the empty beach; the lamp smoking on the shrine", "what he sees; her answer")
wr(p, s)
print("all edits applied")
