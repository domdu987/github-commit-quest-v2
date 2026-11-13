"""take_cfg.py -- the numbers of take s07 for deliver.py."""
TAKE = "s07"
SHOTS = [7]
G0, G1 = 354, 480                       # [g0, g1): shot 7 = 11.81 .. 16.00 s
FIRST_G, LAST_G = 347, 479              # 7-frame in-handle for the dissolve from s06; hard cut out to s08
PARTS = {1: (347, 401), 2: (402, 441), 3: (442, 479)}
PART_NOTES = {1: "7A medium: kenta on a scaffold deck at the top storey's level pays out the hoist chain; the top storey hangs on four ropes and comes down 1.6 -> 0.2 D; orbit",
              2: "7B insert raking over the third roof: a bare dowel peg, the top storey's deck settles over it, touch-down g 417 + loose wobble, no nail",
              3: "7C medium from the other side: ropes gone, storey sits loose and wobbles; kenta shows both open hands on 'mai tok loei' (g 460)"}
CUTS = [(401, 402), (441, 442)]
TRANS_IN = {"type": "dissolve", "frames": 10, "from": "s06", "mixed": [349, 358],
            "note": "in-handle g 347..353 rendered in 3D (7A camera already orbiting); s06 has its out-handle g 354..360"}
TRANS_OUT = {"type": "cut", "frames": 0, "to": "s08", "note": "hard cut on the new sentence (master laughs, 16.0 s); no out-handle"}
TRANSITIONS = [{"at": 354, "type": "dissolve_in", "frames": 10, "handle": [347, 353]},
               {"at": 402, "type": "cut", "from_part": 1, "to_part": 2},
               {"at": 442, "type": "cut", "from_part": 2, "to_part": 3},
               {"at": 480, "type": "cut_out"}]
SHOT_RANGES = {"7": [354, 479]}
SET_NOTE = "v3/set3d4/pagoda.py v2 DAY; shot.py adds a scaffold on the pagoda's south side (deck z 13.95), dowel pegs on storey 3's roof ring, peg holes under storey 4 and four hoist ropes on storey 4 (7A/7B); storey_4 pivot keyed (lowering 1.6 D, touch g 417, wobble)"
DOF = {"7A": "kenta card, f 3.5", "7B": "(-1.0, -2.08, 14.6), f 4.5", "7C": "kenta card, f 3.5"}
CAST = "v3/cast4: kenta (7A kenta_hang_chain paying out; 7C kenta_determined -> open palms)"
COMPARE = [("7A", 380, 17), ("7B", 417, 23), ("7C", 466, 25)]
CUES = [
    (347, 402, "high on the pagoda scaffold: wind, the hoist chain rattling link by link through kenta's hands, rope creak", "ambience", {}),
    (349, 358, "dissolve in from the tower (s06)", "dissolve", {}),
    (354, 400, "the hanging top storey: slow wooden creaks as it sways on its ropes", "foley", {}),
    (402, 402, "hard cut to the dowel on the roof ring", "cut", {}),
    (402, 442, "close: wind over the tiles, wooden creak", "ambience", {}),
    (414, 419, "soft wooden 'thunk' as the storey settles over the peg (plan 13.8 s), no nail, no hammer", "impact", {"peak_frame": 417}),
    (419, 440, "loose joint: a gentle knocking wobble, wood on wood (tok... tok)", "foley", {}),
    (442, 442, "hard cut to kenta, the storey sitting loose behind him", "cut", {}),
    (442, 480, "wind, distant town; the storey's faint creak as it rocks", "ambience", {}),
    (454, 462, "kenta lifts both open hands (cloth whip of the happi sleeves) on 'mai tok loei'", "gesture", {"peak_frame": 460}),
]
