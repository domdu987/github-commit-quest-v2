"""take_info.py -- the take-specific data deliver.py / qa.py read (film 9, take s08 = shots 8-9)."""
TAKE = "s08"
SHOTS = [8, 9]
G0, G1 = 507, 697                      # plan 16.90 s .. 23.24 s; g1 = first frame of shot 10 (next take)
FIRST_G, LAST_G = 501, 702             # 6 handle frames each side, rendered in 3D
RANGES = {8: (501, 614), 9: (615, 702)}
SHOT_RANGES = {8: (507, 614), 9: (615, 696)}
CUTS = [(614, 615)]
TRANSITION_IN = {"type": "cut", "frames": 0, "note": "in-handle g 501..506 = shot 8 set-up continued backwards"}
TRANSITION_OUT = {"type": "cut", "frames": 0, "note": "out-handle g 697..702 = shot 9 set-up continued (lin keeps stirring)"}
TRANSITIONS = [{"at": 507, "type": "in", "handle": [501, 506]}, {"at": 615, "type": "cut", "note": "plan cut shot 8 -> 9 at 20.50 s: DAY -> DAWN (two builds)"},
               {"at": 697, "type": "out", "handle": [697, 702]}]
SETUPS = {
    "8": {"g": [501, 614], "set": "two_sections area, DAY; closer, lower camera than the preset so the figures read: (0.3, 17.8, 4.2) -> (0.6, 16.9, 4.1) look (0..0.2, 5, 2.9), 20 mm; the general's grey plain-mortar section screen-left, lin's creamy rice-mortar section screen-right, meeting at x 0 in the middle of the frame"},
    "9": {"g": [615, 702], "set": "cauldron area, DAWN; (-12.0, 21.8, 6.6) -> (-12.5, 20.4, 6.2) look (-13.6..-14, 12.5, 3.5), 24 mm: lin on his platform stirring, the steaming wok, his section + scaffold behind in pink-gold dawn light"},
}
EVENTS = {"general_chops_the_seam": [520, 549], "general_points_at_his_grey_section": [561, 571], "general_akimbo": [602, 612],
          "worker_carries_bricks": [501, 614], "cut_to_dawn": 615, "lin_stirs": [615, 702], "lin_content_smile": [662, 702]}
SET_NOTE = ("heights lin 16 / general 16 keyed every frame (the wall just split: both level; month 1 = 18 / 21 in shot 10), "
            "set_cauldron_steam 1.0 and set_flames keyed every frame; shot 8 light DAY, shot 9 light DAWN (separate build); no set edits")
CAST_NOTE = ("general (smug, chop gesture down the seam, then mirrored to point at his own section, akimbo), lin (shot 8: lin_calm arms folded, "
             "mirrored to watch the general; shot 9: lin_stir on the lin_stir platform, mirrored, determined -> content smile), "
             "worker_b carrying a brick stack (workers_carry_b + walk cycle) behind the general")
MOUTH_NOTE = "no quote in shots 8-9: static mouths only (general smug, lin smile, worker carry pose)."
CUES = [
    (501, 615, "busy site by day: masons tapping, bricks clacking, a distant hoist pulley creaking", "ambience", {}),
    (520, 549, "the general's arm swish down the seam: a whoosh + a firm 'chop' woodblock hit", "accent", {"peak_frame": 540}),
    (561, 571, "armour clink as he turns and points proudly at his grey section", "foley", {"peak_frame": 566}),
    (501, 614, "the worker's footsteps and the bricks clinking in his arms", "foley", {"peak_frame": 590}),
    (615, 615, "cut to dawn: quiet morning, birds chirping, a rooster far off", "cut", {}),
    (615, 702, "the cauldron simmering and bubbling, fire crackling, the paddle scraping round the wok in a slow rhythm", "ambience", {"peak_frame": 650}),
]
