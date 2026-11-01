p = "mix.py"; s = open(p).read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:100]); s = s.replace(old, new)
# chapter now carries the road: steps of the six, the hum of power as the camera reaches the lit fence
rep('''    *bed("wind", T("chapter", 0), T("far", -0.1), 0.22, 3.2), *bed("crickets", T("chapter", 0), T("far", -0.1), 0.12, 4.0),
    # the estate from the road: their steps on the verge; the hum of power as the camera reaches the lit fence
    *[("far", 0.3 + k * 0.6, "steps", 0.3) for k in range(12)], ("far", vo_t("far", 1) - 0.3, "riser", 0.4), *bed("hum", T("far", vo_t("far", 1)), T("far", -0.1), 0.35, 3.0), ("far", frag("far", 1, 1), "sting", 0.6), ("far", frag("far", 1, 1), "buzz", 0.3),''',
    '''    *bed("wind", T("chapter", 0), T("chapter", -0.1), 0.22, 3.2), *bed("crickets", T("chapter", 0), T("chapter", -0.1), 0.12, 4.0),
    # the six on the verge; the hum of power as the camera reaches the lit fence
    *[("chapter", 0.3 + k * 0.6, "steps", 0.25) for k in range(8)], ("chapter", frag("chapter", 0, 2) - 0.35, "riser", 0.4), *bed("hum", T("chapter", frag("chapter", 0, 2)), T("chapter", -0.1), 0.35, 3.0), ("chapter", frag("chapter", 0, 2) + 0.25, "buzz", 0.3),''')
# gate: "หันมามองภู" is fragment 1 now
rep('frag("gate", 1, 2)', 'frag("gate", 1, 1)', 3)
# win: the skill card at 1.0 (no narrator line); ปั้น's polaroid on her line (index 1)
rep('''    *[("win", 0.1 + k * 0.45, "steps", 0.35) for k in range(4)], ("win", vo_t("win", 1) + 0.1, "page", 0.5), ("win", vo_t("win", 1) + 0.35, "slam", 0.5), ("win", vo_t("win", 1) + 0.45, "pop", 0.4), ("win", frag("win", 1, 1), "sting", 0.6),
    ("win", vo_t("win", 2) + 0.15, "whoosh", 0.4), ("win", vo_t("win", 2) + 0.45, "page", 0.6), ("win", vo_t("win", 2) + 0.45, "sting", 0.7), *beats("win", vo_t("win", 2), D["win"] - vo_t("win", 2), 0.6, 0.45),''',
    '''    *[("win", 0.1 + k * 0.45, "steps", 0.35) for k in range(4)], ("win", 1.0, "page", 0.5), ("win", 1.25, "slam", 0.5), ("win", 1.35, "pop", 0.4),
    ("win", vo_t("win", 1) + 0.15, "whoosh", 0.4), ("win", vo_t("win", 1) + 0.45, "page", 0.6), ("win", vo_t("win", 1) + 0.45, "sting", 0.7), *beats("win", vo_t("win", 1), D["win"] - vo_t("win", 1), 0.6, 0.45),''')
# register: w04 is 0, d02 is 1
rep('''    ("register", vo_end("register", 2) + 0.2, "pen", 0.6), ("register", vo_end("register", 2) + 0.55, "slam", 0.8), ("register", vo_end("register", 2) + 0.55, "sting", 0.7), *beats("register", vo_t("register", 1), D["register"] - vo_t("register", 1), 0.6, 0.45),''',
    '''    ("register", vo_end("register", 1) + 0.2, "pen", 0.6), ("register", vo_end("register", 1) + 0.55, "slam", 0.8), ("register", vo_end("register", 1) + 0.55, "sting", 0.7), *beats("register", vo_t("register", 0), D["register"] - vo_t("register", 0), 0.6, 0.45),''')
# knows: the reveal is fragment 1 of the short line
rep('''    ("knows", frag("knows", 2, 3), "sting", 1.0), ("knows", frag("knows", 2, 3), "boom", 0.6), ("knows", frag("knows", 2, 3), "glitch", 0.5),''',
    '''    ("knows", frag("knows", 2, 1), "sting", 1.0), ("knows", frag("knows", 2, 1), "boom", 0.6), ("knows", frag("knows", 2, 1), "glitch", 0.5),''')
rep('("knows", frag("knows", 2, 1) + 0.6, "chalk", 0.6),\n', '\n')
# workshop: collar / rubber / build on the same beats as shots.part (WP1, WP2, WB); ครูพิม's silence after ก้อง's plea
rep('''    ("workshop", 0.2, "page", 0.8), ("workshop", 0.5, "slam", 0.45), *[("workshop", o, "pop", 0.5) for o in (frag("workshop", 0, 0) + 0.25, frag("workshop", 0, 1), frag("workshop", 0, 2))],
    ("workshop", frag("workshop", 0, 1) + 0.1, "clang", 0.7), ("workshop", frag("workshop", 0, 1) + 0.3, "latch", 0.5), *[("workshop", frag("workshop", 0, 2) + 0.1 + k * 0.22, "squish", 0.35) for k in range(6)],
    ("workshop", vo_end("workshop", 0) + 0.3, "saw", 0.7), ("workshop", vo_end("workshop", 0) + 0.4, "sparks", 0.8), ("workshop", vo_end("workshop", 0) + 0.85, "riser", 0.5), ("workshop", vo_end("workshop", 0) + 0.9, "slam", 0.9),
    ("workshop", vo_end("workshop", 0) + 0.9, "sting", 0.7), ("workshop", vo_end("workshop", 0) + 1.2, "ding", 0.5), ("workshop", vo_end("workshop", 0) + 1.3, "ching", 0.5), *beats("workshop", 0.0, vo_t("workshop", 1), 0.6, 0.35),
    *bed("hum", T("workshop", vo_t("workshop", 1) - 0.3), T("calm", -0.1), 0.2, 3.0), ("workshop", vo_t("workshop", 2) + 0.4, "sting", 0.4),''',
    '''    ("workshop", 0.2, "page", 0.8), ("workshop", 0.5, "slam", 0.45), *[("workshop", o, "pop", 0.5) for o in (frag("workshop", 0, 0) + 0.25, WP1, WP2)],
    ("workshop", WP1 + 0.1, "clang", 0.7), ("workshop", WP1 + 0.3, "latch", 0.5), *[("workshop", WP2 + 0.1 + k * 0.15, "squish", 0.35) for k in range(6)],
    ("workshop", WB - 0.05, "saw", 0.7), ("workshop", WB + 0.05, "sparks", 0.8), ("workshop", WB + 0.5, "riser", 0.5), ("workshop", WB + 0.55, "slam", 0.9),
    ("workshop", WB + 0.55, "sting", 0.7), ("workshop", WB + 0.85, "ding", 0.5), ("workshop", WB + 0.95, "ching", 0.5), *beats("workshop", 0.0, vo_t("workshop", 1), 0.6, 0.35),
    *bed("hum", T("workshop", vo_t("workshop", 1) - 0.3), T("calm", -0.1), 0.2, 3.0), ("workshop", vo_end("workshop", 1) + 0.15, "sting", 0.4),''')
rep('''def frag(k, i=0, j=0):
    return SH[k]["vo"][i]["t"] + SH[k]["vo"][i]["frags"][j]
''', '''def frag(k, i=0, j=0):
    return SH[k]["vo"][i]["t"] + SH[k]["vo"][i]["frags"][j]


WP1 = frag("workshop", 0, 1); WP2 = WP1 + 0.75; WB = WP2 + 1.1   # the recipe's collar, rubber and build (shots.part uses the same three)
''')
rep('for a0, a1 in ((T("out", 0), T("out", vo_t("out", 1))), (T("workshop", vo_end("workshop", 0) + 0.4), T("workshop", vo_end("workshop", 0) + 2.0))):',
    'for a0, a1 in ((T("out", 0), T("out", vo_t("out", 1))), (T("workshop", WB + 0.05), T("workshop", WB + 1.65))):')
# mix: the pour now runs through the insert
rep('    ("mix", 0.35, "stream", 0.8), ("mix", 1.2, "stream", 0.5), *[("mix", 0.5 + k * 0.4, "drip", 0.35) for k in range(5)],',
    '    ("mix", 0.35, "stream", 0.8), ("mix", 1.2, "stream", 0.5), ("mix", vo_t("mix", 1) - 0.1, "stream", 0.7), ("mix", vo_t("mix", 1) + 1.0, "stream", 0.5), *[("mix", 0.5 + k * 0.4, "drip", 0.35) for k in range(9)],')
# out: ภู's single line — the tip card lands on "อย่าเพิ่งกลับเข้าไป"
rep('''    *[("out", vo_t("out", 1) + 1.2 + k * 1.3, "cough", 0.25) for k in range(4)], ("out", vo_t("out", 2), "page", 0.5), ("out", vo_t("out", 2) + 0.3, "slam", 0.45), *beats("out", 0.0, vo_t("out", 1), 0.36, 0.8),''',
    '''    *[("out", vo_t("out", 1) + 1.2 + k * 1.3, "cough", 0.25) for k in range(3)], ("out", frag("out", 1, 1), "page", 0.5), ("out", frag("out", 1, 1) + 0.3, "slam", 0.45), *beats("out", 0.0, vo_t("out", 1), 0.36, 0.8),''')
# real: one line
rep('''    ("real", frag("real", 0, 1) - 0.1, "page", 0.6), ("real", frag("real", 0, 1) + 0.2, "slam", 0.5), ("real", vo_t("real", 1) + 0.1, "page", 0.6), ("real", vo_t("real", 1) + 0.4, "slam", 0.5), ("real", frag("real", 1, 3), "ding", 0.5), ("real", frag("real", 1, 3), "pop", 0.5),''',
    '''    ("real", frag("real", 0, 1) - 0.1, "page", 0.6), ("real", frag("real", 0, 1) + 0.2, "slam", 0.5), ("real", frag("real", 0, 2), "page", 0.6), ("real", frag("real", 0, 2) + 0.3, "slam", 0.5), ("real", frag("real", 0, 3), "ding", 0.5), ("real", frag("real", 0, 3), "pop", 0.5),''')
# dinner: เจ๊หงส์'s whisper is line 0
rep('''    *bed("hum", T("dinner", 0), T("sig", -0.1), 0.3, 3.0), *bed("fan", T("dinner", 0), T("dinner", -0.1), 0.15, 4.0), *[("dinner", 0.4 + k * 0.8, "ching", 0.12) for k in range(12)],
    ("dinner", frag("dinner", 0, 2), "sting", 0.5), ("dinner", vo_t("dinner", 1) - 0.1, "whoosh", 0.3), ("dinner", frag("dinner", 1, 1), "sting", 0.8), ("dinner", frag("dinner", 1, 1), "boom", 0.4), *beats("dinner", vo_t("dinner", 1), D["dinner"] - vo_t("dinner", 1), 0.55, 0.55),''',
    '''    *bed("hum", T("dinner", 0), T("sig", -0.1), 0.3, 3.0), *bed("fan", T("dinner", 0), T("dinner", -0.1), 0.15, 4.0), *[("dinner", 0.2 + k * 0.8, "ching", 0.12) for k in range(5)],
    ("dinner", vo_t("dinner", 0) - 0.1, "whoosh", 0.3), ("dinner", frag("dinner", 0, 1), "sting", 0.8), ("dinner", frag("dinner", 0, 1), "boom", 0.4), *beats("dinner", vo_t("dinner", 0), D["dinner"] - vo_t("dinner", 0), 0.55, 0.55),''')
# signs: the cuts land on the beats — a slam on each
rep('''    ("signs", frag("signs", 1, 3), "sting", 1.0),''', '''    ("signs", frag("signs", 0, 1) - 0.05, "whoosh", 0.3), ("signs", frag("signs", 0, 2) - 0.05, "whoosh", 0.3),
    ("signs", frag("signs", 1, 3), "sting", 1.0),''')
# night: the cut in on the closing gate
rep('''    ("night", frag("night", 1, 2) - 0.2, "gate", 0.9),''', '''    ("night", frag("night", 1, 2) - 0.35, "whoosh", 0.35), ("night", frag("night", 1, 2) - 0.2, "gate", 0.9),''')
open(p, "w").write(s); print("mix patched")
