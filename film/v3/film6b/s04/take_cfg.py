"""take_cfg.py -- facts of take s04 (film 6b) for deliver.py."""
G0, G1 = 123, 314                        # plan 4.10-10.48 s; in-handle 117..122, out-handle 314..319
RANGES = {4: (117, 179), 5: (180, 227), 6: (228, 272), 7: (273, 319)}
META = {"take": "s04", "film": "6b", "shots": [4, 5, 6, 7],
        "transition_in": {"type": "cut", "frames": 0, "note": "hard cut from s01 (bakery) at g 123; in-handle g 117..122 = the crane a little higher"},
        "transition_out": {"type": "cut", "frames": 0, "note": "cut to shot 8 (bakery, Henry) at g 314; out-handle g 314..319 (push, splat drips, laugh continue)"},
        "shot_starts": {"4": 123, "5": 180, "6": 228, "7": 273},
        "events": {"crane_down": [117, 179], "beam_tips_short": [190, 200], "baker2_shocked": 194, "sign_drops_ขาดน้ำหนัก": [203, 209],
                   "pillory_push": [228, 272], "tomato_raised": [273, 283], "throw": 284, "tomato_flight": [285, 295], "splat": 296,
                   "crowd_laughs": [296, 319]},
        "set": "v3/set3d6/bakery.py: market AFTERNOON (warm sun vs blue shade); big balance keyed (0 -> -7 short, beam bounce), 12 loaves; braziers flicker keyed; Thai sign cards 'ขาดน้ำหนัก!' (on the balance) and 'ห้ามขายขาดน้ำหนัก!' (on the pillory post) in Kanit Black",
        "dof": "none (cam.data.dof.use_dof False + B.setup_dof(scene, None, None, cam=cam) before every render)",
        "light": "AFTERNOON", "narration": "film6b/audio/narration.wav at +0.10 s; captions film6b/script/captions.json",
        "cast": "v3/cast6: baker2 (at the balance; then pillory=True, card just in front of the 3D board), guard1, woman1 x2, man1 x2 (townsfolk, walks in shot 4); tomato_svg in flight (4 spins) and squash 0.55 / 1.0 splat cards"}
CUES = [
    (117, 320, "ambience", "medieval market afternoon: crowd murmur, distant hawkers, a hen, wind in the bunting"),
    (117, 179, "whoosh", "camera cranes down from the sky into the square: long airy whoosh", 150),
    (180, 180, "cut", "cut to CU baker2 at the big balance"),
    (190, 200, "prop", "the big balance tips to the weights side: wooden creak + chain rattle, low 'bonk'", 200),
    (194, 200, "accent", "baker2 shocked: sweat-drop 'plip'", 196),
    (203, 212, "prop", "the sign 'ขาดน้ำหนัก!' drops in on its cords: wooden clack + swing", 209),
    (228, 228, "cut", "cut to the pillory (low)"),
    (228, 272, "foley", "baker2 struggles in the board: wood creaks, chains"),
    (273, 273, "cut", "cut to CU baker2 in the pillory"),
    (284, 295, "whoosh", "tomato thrown: short whistle in the air", 290),
    (296, 300, "impact", "tomato SPLAT on his face: wet squelch", 296),
    (296, 320, "crowd", "townsfolk burst out laughing"),
    (314, 314, "cut", "plan: cut to shot 8 (bakery, Henry)"),
]
PAIRS = [(150, "ref/a/t0031.jpg", "ref a t0031 (high establishing city)"), (298, "ref/a/t0011.jpg", "ref a t0011 (CU, sweat, court)")]
