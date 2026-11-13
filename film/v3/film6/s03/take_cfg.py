"""take_cfg.py -- per-take settings read by deliver.py (s03)."""
TAKE = "s03"
SHOTS = [3]
G0, G1 = 108, 180                      # shot 3 = g 108..179 (plan 3.60-6.00 s)
G_FIRST, G_LAST = 102, 185             # 6 handle frames each side
SIDS = {1: (102, 143), 2: (144, 185)}
SID_NOTES = {1: "low, up at the empty pillory (pillory_low family, 24 mm), slow push; crows on the post / board ends, one crosses the sky",
             2: "punch-in at g 144 (1.2 s into the shot): closer along the board from the right (26 mm), slow push; crow hops to the neck hole, crow on the post takes off"}
SHOT_RANGES = {3: [108, 179]}
TRANSITION_IN = {"type": "cut", "frames": 0, "note": "plan: hard cut from shot 2 (bakery table_insert); in-handle g 102..107 rendered in 3D"}
TRANSITION_OUT = {"type": "cut", "frames": 0, "note": "plan: cut to shot 4 (bakery counter) at g 180; out-handle g 180..185 rendered in 3D"}
EVENTS = {"crow_C_caws": [118, 125], "punch_in": 144, "crow_B_hops_to_neck_hole": [150, 157], "crow_C_caws_again": [160, 166],
          "crow_A_takes_off": 168}
SET = "v3/set3d6/bakery.py: market AFTERNOON (sun from the WSW, long shadows); the set's 3D pillory kept whole (empty); oven / brazier flicker keyed per frame; sky redrawn sharp"
CAST = "no people (empty pillory). 3-4 cartoon crows = mk.crow_svg drawings on common.PropCard cards (x1.15, cast shadows), the pose variant switched per frame"
CUES = [
    (102, 186, "market square in the afternoon, near-empty: distant market murmur, wind flapping the bunting, wooden creak of the pillory", "ambience", None),
    (102, 144, "a crow flaps across the sky behind the pillory (wing beats)", "sfx", None),
    (118, 125, "crow on the right end of the board: CAW! (short, comic)", "sfx", 118),
    (144, 144, "framing change (punch-in), same sound", "cut", None),
    (150, 157, "crow hops along the board: two little wooden taps", "sfx", 157),
    (158, 180, "pecking at a dried splat: tock-tock-tock", "sfx", 160),
    (160, 166, "second CAW", "sfx", 160),
    (168, 182, "crow takes off from the post top: wing flaps whoosh", "sfx", 168),
    (180, 180, "plan: cut to shot 4 (bakery counter)", "cut", None),
]
COMPARE = [(130, "a/t0094.jpg", "(exterior, day)"), (170, "a/t0034.jpg", "(exterior, sky)")]
HUE_ROWS = [("s03 shot 3 (g 108-179)", 108, 179), ("s03 all (g 102-185)", 102, 185)]
HUE_REFS = [("ref a t0034 t0074 t0094 (exteriors)", ["a/t0034.jpg", "a/t0074.jpg", "a/t0094.jpg"])]
