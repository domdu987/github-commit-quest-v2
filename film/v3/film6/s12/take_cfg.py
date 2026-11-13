"""take_cfg.py -- per-take settings read by deliver.py (s12)."""
TAKE = "s12"
SHOTS = [12, 13, 14, 15]
G0, G1 = 933, 1239                     # shots 12..15 = g 933..1238 (plan 31.09-41.29 s)
G_FIRST, G_LAST = 927, 1244
SIDS = {1: (927, 968), 2: (969, 1004), 3: (1005, 1043), 4: (1044, 1079), 5: (1080, 1115), 6: (1116, 1151), 7: (1152, 1197), 8: (1198, 1244)}
SID_NOTES = {1: "shot 12a square MORNING, 28 mm two-shot: woman1 + man1 laugh (mouths move: allowed in 12) and point screen-right; slow push",
             2: "shot 12b kit walks past with the basket of 13 (walk cycle), glances back at the laughers and grins; pan with him",
             3: "shot 13a pillory AFTERNOON, week 1: one head (baker2), frontal-low 24 mm, crow on the post",
             4: "shot 13b punch-in on baker2 (30 mm): a long sigh, head droops",
             5: "shot 14a week 2: two heads (baker2 + baker3), frontal-low",
             6: "shot 14b closer two-shot from the right (28 mm): they look at each other",
             7: "shot 15a week 3: four heads in a row (baker2..baker5) all shaking their heads",
             8: "shot 15b track along the row from left to right (30 mm), heads shaking out of phase, crow caws"}
SHOT_RANGES = {12: [933, 1004], 13: [1005, 1079], 14: [1080, 1151], 15: [1152, 1238]}
TRANSITION_IN = {"type": "dissolve", "frames": 10, "note": "plan: dissolve from shot 11 (bakery counter) into the market; in-handle g 927..932 rendered in 3D"}
TRANSITION_OUT = {"type": "cut", "frames": 0, "note": "plan: cut to shot 16 (bakery, Henry laughs) at g 1239; out-handle g 1239..1244 rendered in 3D"}
EVENTS = {"laugh_mouths": [927, 1004], "cut_12b": 969, "kit_glances_back": [978, 994], "week1": 1005, "sigh": [1050, 1072],
          "week2": 1080, "look_at_each_other": [1122, 1146], "week3": 1152, "heads_shake": [1152, 1244], "crow_caws": [[1212, 1219], [1232, 1238]]}
SET = "v3/set3d6/bakery.py: market MORNING (shot 12) and AFTERNOON (shots 13-15: the busts under the afternoon sun); the set's pillory board cut away at runtime (cast6 pillory boards on the bakers); sky redrawn sharp"
CAST = "v3/cast6: woman1, man1 (laughing, mouths alternate in shot 12 only), kit (walk cycle with the 13-loaf basket), baker2 + baker3/4/5 (runtime copies of baker2 with other tunics, caps, hair, moustache / beard: mk.register_bakers, cast6 not edited) in the pillory pose key; crow = mk.crow_svg card"
CUES = [
    (927, 1005, "morning market, townsfolk laughing out loud ('ha-ha-ha', mouths on screen g 927-1004)", "ambience", None),
    (969, 1004, "kit's light footsteps, basket creak", "sfx", None),
    (1005, 1245, "afternoon square around the pillory: murmur, wood creak", "ambience", None),
    (1005, 1005, "week 1: a single low 'dong' sting", "accent", 1005),
    (1050, 1072, "baker2 sighs (breathy, no lip-sync)", "accent", 1058),
    (1080, 1080, "week 2: 'dong dong'", "accent", 1080),
    (1152, 1152, "week 3: 'dong dong dong dong'", "accent", 1152),
    (1152, 1244, "four heads shaking: rattling pillory boards, mumbled protests (no lip-sync)", "sfx", None),
    (1212, 1219, "crow CAW", "sfx", 1212),
    (1232, 1238, "crow CAW", "sfx", 1232),
    (1239, 1239, "plan: cut to shot 16 (bakery, Henry laughs)", "cut", None),
]
COMPARE = [(950, "a/t0014.jpg", "(laughing)"), (1170, "b/t0094.jpg", "(row of heads)")]
HUE_ROWS = [("s12 shot 12 (MORNING)", 933, 1004), ("s12 shots 13-15 (AFTERNOON)", 1005, 1238)]
HUE_REFS = [("ref a t0034 t0074 t0094 (exteriors)", ["a/t0034.jpg", "a/t0074.jpg", "a/t0094.jpg"])]
