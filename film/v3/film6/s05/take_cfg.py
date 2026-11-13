"""take_cfg.py -- per-take settings read by deliver.py (s05)."""
TAKE = "s05"
SHOTS = [5, 6]
G0, G1 = 259, 460                      # shot 5 = g 259..359, shot 6 = g 360..459 (plan 8.62-15.34 s)
G_FIRST, G_LAST = 253, 465
SIDS = {1: (253, 312), 2: (313, 359), 3: (360, 414), 4: (415, 465)}
SID_NOTES = {1: "shot 5a market_wide MORNING: high establishing, slow crane down + push; strolling crowd (walk cycles) and groups",
             2: "shot 5b eye level in the square MORNING (square_eye family): townsfolk cross, guard by the big balance, lateral drift",
             3: "shot 6a pillory AFTERNOON, medium slightly low (26 mm): baker2 in the pillory, a rotten tomato flies in and splats beside his head, he flinches",
             4: "shot 6b wider from behind two townsfolk (24 mm): woman1 laughs and points, man1 raises a rotten cabbage, throws, it splats, baker2 flinches, man1 laughs"}
SHOT_RANGES = {5: [259, 359], 6: [360, 459]}
TRANSITION_IN = {"type": "dissolve", "frames": 10, "note": "plan: dissolve from shot 4 (bakery counter) into the market establishing; in-handle g 253..258 rendered in 3D (the crane starts there)"}
TRANSITION_OUT = {"type": "cut", "frames": 0, "note": "plan: cut to shot 7 (bakery, Henry low angle) at g 460; out-handle g 460..465 rendered in 3D"}
EVENTS = {"cut_5b": 313, "cut_6a": 360, "tomato_flies": [383, 391], "tomato_splat": 392, "cut_6b": 415,
          "cabbage_raised": [415, 432], "cabbage_throw": [433, 436], "cabbage_splat": 446}
SET = "v3/set3d6/bakery.py: market MORNING (shot 5) and AFTERNOON (shot 6: the busts happen under the afternoon sun, shot 20); the set's pillory board is cut away at runtime in shot 6 (cast6 pillory board drawn on baker2); sky redrawn sharp; braziers flicker keyed per frame"
CAST = "v3/cast6: shot 5 crowd = woman1 / man1 copies (walk cycles + town_point / town_laugh), guard1, guard2; shot 6 baker2 (pillory pose key), woman1, man1; flying veg = cast6.tomato_svg / cabbage_svg cards, splats = mk.splat_svg cards"
CUES = [
    (253, 360, "busy medieval market square in the morning: crowd murmur, footsteps on cobbles, a hawker's call, bunting flapping, a cart wheel", "ambience", None),
    (313, 313, "framing change (cut to eye level), same ambience", "cut", None),
    (360, 466, "the pillory in the afternoon: crowd jeering and laughing, wood creak", "ambience", None),
    (383, 392, "tomato whoosh then a wet cartoon SPLAT on the board", "sfx", 392),
    (392, 401, "baker2 flinches: comic 'oof' squeak / wobble sting", "accent", 393),
    (415, 415, "cut to the throwers", "cut", None),
    (433, 446, "cabbage throw: arm swish + whoosh", "sfx", 434),
    (446, 448, "cabbage hits: soft cartoon SPLOTCH", "sfx", 446),
    (437, 466, "townsfolk laughter (the crowd laughs; no lip-sync)", "accent", 437),
    (460, 460, "plan: cut to shot 7 (bakery)", "cut", None),
]
COMPARE = [(300, "a/t0034.jpg", "(establishing)"), (440, "a/t0014.jpg", "(laughing crowd)")]
HUE_ROWS = [("s05 shot 5 (g 259-359, MORNING)", 259, 359), ("s05 shot 6 (g 360-459, AFTERNOON)", 360, 459)]
HUE_REFS = [("ref a t0034 t0074 t0094 (exteriors)", ["a/t0034.jpg", "a/t0074.jpg", "a/t0094.jpg"])]
