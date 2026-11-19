TAKE, SHOTS = "s28", [28]
SHOT_RANGES = {"28": [1805, 1894]}
FIRST, LAST = 1796, 1903
G0, G1 = 1805, 1895
TRANS_IN = dict(type="dissolve", frames=15, note="DIS from shot 27 (line_rail): 15 f smoothstep dissolve centred on g 1805, 9 handle frames rendered before it")
CUTS_QA = []
EV = dict(snap=[1868, 1883], word_postmaster_general=1874, pose_swap_keys=1875)
NOTES = dict(light="DAY", set="v3/set3d16 CHAMBER chamber_low DAY: mocker at mark mocker_post (front-row desk), runtime set_mailsacks(on) (10 oversize sacks), desk-corner inkwell FG from the preset",
             cast="v3/cast16 mocker mocker_pm_proud (sash, mail bag, key ring on the belt) -> mocker_pm_keys (dangling the key ring) on the blink at g 1874; no lip-sync",
             camera="custom 22 mm, low (1.3 D below the face), 3.9 D away, rotated 18 deg round the mocker from the preset heading to clear the sacks; push 7 %/s + slide 40 px/s + arc 6 deg/s, snap x1.5 (15 f) on 'ไปรษณีย์ใหญ่'")
CUES = [(1796, 1904, "ambience", "chamber, daytime: quiet room tone, a far door, paper rustle"),
        (1805, 1830, "accent", "pomp: short brass fanfare sting as the postmaster poses (music-box 'ta-da')"),
        (1868, 1883, "accent", "snap push whoosh"),
        (1875, 1890, "prop", "iron key ring jingles as he dangles it")]
