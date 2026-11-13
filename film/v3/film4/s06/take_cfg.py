"""take_cfg.py -- the numbers of take s06 for deliver.py."""
TAKE = "s06"
SHOTS = [6]
G0, G1 = 256, 354                       # [g0, g1): shot 6 = 8.53 .. 11.81 s
FIRST_G, LAST_G = 249, 360              # with the 7-frame handles (dissolve in from s01, dissolve out to s07)
PARTS = {1: (249, 299), 2: (300, 327), 3: (328, 360)}
PART_NOTES = {1: "6A low angle: the master on his tower's scaffold hammering the big joint (strikes g 270, 286)",
              2: "6B ECU insert: the iron joint plate, a 3D mallet drives the long nail home (strikes g 306, 321)",
              3: "6C low wide from the courtyard up the rigid tower + scaffold, crane up; strike g 343; out-handle g 354..360"}
CUTS = [(299, 300), (327, 328)]
TRANS_IN = {"type": "dissolve", "frames": 10, "from": "s01", "mixed": [251, 260],
            "note": "in-handle g 249..255 rendered in 3D (6A camera); s01 has its out-handle g 256..262; smoothstep mix by the editor"}
TRANS_OUT = {"type": "dissolve", "frames": 10, "to": "s07", "mixed": [349, 358],
             "note": "out-handle g 354..360 rendered in 3D (6C crane continues); s07 has its in-handle g 347..353"}
TRANSITIONS = [{"at": 256, "type": "dissolve_in", "frames": 10, "handle": [249, 255]},
               {"at": 300, "type": "cut", "from_part": 1, "to_part": 2},
               {"at": 328, "type": "cut", "from_part": 2, "to_part": 3},
               {"at": 354, "type": "dissolve_out", "frames": 10, "handle": [354, 360]}]
SHOT_RANGES = {"6": [256, 353]}
SET_NOTE = "v3/set3d4/pagoda.py v2 DAY; shot.py adds a scaffold on the tower's south face (decks z 4.6 / 9.0), an iron joint plate with nails at G.JOINT, the keyed hero nail and a 3D mallet (insert only)"
DOF = {"6A": "master card, f 3.5", "6B": "(13.7, -2.8, 11.3), f 4.0", "6C": "off"}
CAST = "v3/cast4: master (6A, 6C; master_plaster pose with a mallet, mallet head pinned to the nail on each blow)"
COMPARE = [("6A", 286, 13), ("6A", 270, 45), ("6B", 312, 3), ("6C", 345, 31)]
CUES = [
    (249, 300, "high on the tower scaffold: wind, creak of bamboo poles and rope lashings", "ambience", {}),
    (256, 256, "dissolve in from the town wide (s01)", "dissolve", {}),
    (267, 271, "mallet blow on iron: heavy wooden 'tok' on the nail plate", "impact", {"peak_frame": 270}),
    (283, 287, "mallet blow on iron (on 'sang ho thi')", "impact", {"peak_frame": 286}),
    (300, 300, "hard cut to the ECU of the iron joint plate", "cut", {}),
    (300, 328, "close: quiet wood room tone, the mallet's whoosh before each blow", "ambience", {}),
    (303, 307, "the long nail is driven: metallic CLANG + wood crunch (plan 10.1 s)", "impact", {"peak_frame": 306}),
    (318, 322, "second blow on 'naen' (tight): nail goes flush, a ringing clank", "impact", {"peak_frame": 321}),
    (328, 328, "hard cut to the low wide of the rigid tower", "cut", {}),
    (328, 361, "courtyard ambience, wind; a deep wooden boom accent under 'khaeng muean kon hin' (hard as rock)", "ambience", {}),
    (340, 344, "distant mallet blow from up the scaffold", "impact", {"peak_frame": 343}),
    (349, 358, "dissolve to kenta and the pagoda (s07)", "dissolve", {}),
]
