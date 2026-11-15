"""take s10 numbers for deliver.py / qa.py (shots 10 + 11)."""
TAKE, SHOTS, LIGHT = "s10", [10, 11], "DAY"
G0, G_CUT, G1 = 697, 792, 887
FIRST, LAST = 691, 892
SETUPS = {1: dict(name="shot10_two_sections", set="wall_site two_sections build, DAY; custom low camera from the site looking at the seam of both inner faces (24 -> 20.6 D out, z 5.9 -> 5.6, pitch -11, 20 mm), slow push 1.6 D + small drift; lin 18 / general 18 -> 21 courses"),
          2: dict(name="shot11_wall_top", set="wall_site, DAY, lin 20 / general 26; wall_top-like camera along the general's top (x 17.6 -> 14.9, z 16.7 -> 16.1, 20 mm), slow push 2.7 D")}
EVENTS = {"month1_both_18": [691, 738], "general_course_19": 739, "general_course_20": 747, "general_course_21": 758,
          "general_looks_up_at_his_wall": [733, 769], "general_puffs_up_smug": [764, 791], "cut_to_wall_top": 792,
          "general_laughs_on_top_akimbo": [792, 892]}
SET = ("v3/set3d9/wall.py wall_site (two_sections build), DAY: set_flames + set_cauldron_steam(1) + set_wall_height keyed on every frame "
       "(shot 10: lin 18, general 18 -> 19 -> 20 -> 21 at g 739 / 747 / 758, constant keys; shot 11: lin 20 / general 26). No runtime set changes.")
CAST = ("v3/cast9: shot 10 lin (lin_calm mirrored, arms folded, watching the general's section rise), general (general_stand akimbo -> looks up "
        "at his section, happy -> smug puff), worker_a / worker_b (workers_carry with brick stacks, idle sway); shot 11 general on his top "
        "(general_wall_laugh, belly-laugh squash shake, static laughing mouth), worker_c with bricks behind him")
MOUTHS = "no quote in shots 10-11: no lip-sync; fixed expression mouths (laughing mouth shape held, not animated)"
CUES = [
    (691, 892, "ambience", "Ming construction site by day: mallets on brick, trowels scraping, distant shouts of workers, the cauldron fire crackling, banners flapping in the wind", None),
    (697, 697, "cut", "cut in to the two sections (month 1)", None),
    (739, 739, "accent", "a brick course thunks into place on the general's section (wooden 'tok')", 739),
    (747, 747, "accent", "second course thunks into place, a little higher pitch", 747),
    (758, 758, "accent", "third course thunks into place: a proud brass 'ta-da' sting on 'สามชั้น'", 758),
    (764, 791, "foley", "the general's armour clinks as he puffs up; a smug 'hmph'", 768),
    (792, 792, "cut", "cut to the top of the general's wall (month 2): wind gust up high", None),
    (792, 886, "foley", "the general's big booming belly laugh, armour plates rattling with each shake", 830),
    (887, 887, "cut", "plan: cut to shot 12 (rain): thunder roll and rain start", None),
]
