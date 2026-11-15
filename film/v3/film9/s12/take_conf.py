"""take s12 numbers for deliver.py / qa.py (shots 12 + 13)."""
TAKE, SHOTS, LIGHT = "s12", [12, 13], "RAIN"
G0, G_CUT, G1 = 887, 960, 1041
FIRST, LAST = 881, 1046
SETUPS = {1: dict(name="shot12_lin_rain", set="wall_site two_sections build, RAIN, lin 20 / general 26; custom medium camera from the site on Lin at the foot of his rice section (z 4.5 -> 4.3, 24 mm), slow push 1.8 D; set_mortar_wet 0.55 -> 1.0 over g 881..941"),
          2: dict(name="shot13_wall_top_rain", set="wall_site, RAIN, lin 20 / general 26; wall_top-like camera along the general's top (x 15.6 -> 13.6, z 16.4 -> 16.1, 20 mm), slow push 2.1 D")}
EVENTS = {"mortar_softens": [881, 941], "lin_looks_at_soft_mortar": [881, 911], "lin_looks_up_worried": [912, 926],
          "cut_to_wall_top": 960, "general_shouts_lipsync": [963, 1039], "quote_text_in_narration": [993, 1043]}
SET = ("v3/set3d9/wall.py wall_site (two_sections build), RAIN light: set_rain(1) (compositor streaks), set_mortar_wet (0.55 -> 1.0 in shot 12, "
       "1.0 in shot 13), set_flames, set_cauldron_steam(1), set_wall_height lin 20 / general 26, all keyed on every frame. No runtime set changes.")
CAST = ("v3/cast9: shot 12 lin (lin_rain, wet=1: first looks down at the soft mortar beside him, then up into the rain worried, palm out); "
        "shot 13 general on his top (general_rain_shout, wet=1, pointing down at the site, fist up, body shake)")
MOUTHS = ("only the general's quote moves the mouth: cast9.talk_mouth on g 963..1039 (~32.0-34.5 s, as the worker brief's 32.0-34.6); "
          "g 960..962 and 1040..1046 hold the open shout shape still; Lin's worried mouth is static")
CUES = [
    (881, 1046, "ambience", "steady rain on bricks, roof tiles and puddles, gurgling run-off, a low rumble of thunder far off", None),
    (887, 887, "cut", "cut in to Lin in the rain (first rain): a thunder roll", 887),
    (887, 941, "foley", "soft wet squelch / drip of milky mortar running down the joints", 910),
    (912, 926, "accent", "Lin looks up worried: a small uneasy descending woodwind figure", 920),
    (960, 960, "cut", "cut to the general on his wall in the rain: wind and rain gust up high", None),
    (963, 1039, "voice", "the general shouts and laughs in the rain (his quote 'เห็นมั้ย ขนมเปียกฝนก็เละ!'; lip-sync window)", 1000),
    (1041, 1041, "cut", "plan: cut to shot 14 (enemy army, cannon line, BATTLE): war drums", None),
]
