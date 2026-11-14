"""take_cfg.py -- facts of take s01 (film 6b) for deliver.py."""
G0, G1 = 0, 123                          # plan 0.00-4.10 s; out-handle 123..128
RANGES = {1: (0, 47), 2: (48, 71), 3: (72, 128)}
META = {"take": "s01", "film": "6b", "shots": [1, 2, 3],
        "transition_in": {"type": "cut", "frames": 0, "note": "film opening (first frame of the film)"},
        "transition_out": {"type": "cut", "frames": 0, "note": "cut to shot 4 (market crane) at g 123; out-handle g 123..128 rendered in 3D (push + grin continue)"},
        "shot_starts": {"1": 0, "2": 48, "3": 72},
        "events": {"glance_left": [6, 16], "glance_right": [18, 28], "pale_loaf_up_on_palm": 30, "smirk": 38,
                   "loaf_leaves_hand": 53, "loaf13_lands": 56, "steam_puff": [56, 71], "customer_walks_off": [84, 112],
                   "wink": [98, 104], "grin": 105},
        "set": "v3/set3d6/bakery.py: bakery MORNING, steam 0.35, oven flicker keyed per frame; extra blue area light L_cool_window (cool counter-colour, formula rule 7); Thai fascia sign 'ร้านลุงเฮนรี่' card over the painted HENRY · BAKER fascia",
        "dof": "none (cam.data.dof.use_dof False + B.setup_dof(scene, None, None, cam=cam) before every render)",
        "light": "MORNING", "narration": "film6b/audio/narration.wav at +0.10 s; captions film6b/script/captions.json",
        "cast": "v3/cast6: kit (hidden stool behind the counter), woman1 = the customer with the basket of 13; basket_svg(12) PropCard x1.4 on the counter; pale 13th loaf = loaf_svg lightened (lib6b.pale_png) on a PropCard; steam puff cards (lib6b.puff_svg)"}
CUES = [
    (0, 129, "ambience", "bakery morning inside: oven fire crackle, soft street murmur through the counter opening"),
    (6, 16, "gesture", "kit's sneaky glance screen-left: tiny 'tik' / pizzicato", 7),
    (18, 28, "gesture", "glance screen-right: second 'tik'", 19),
    (26, 32, "prop", "the pale 13th loaf comes up on his palm: soft cloth swish", 30),
    (38, 42, "accent", "deadpan turns into a smirk: sly little sting", 38),
    (48, 48, "cut", "cut to ECU of the basket"),
    (53, 56, "prop", "the 13th loaf drops onto the pile: crusty thump + wicker creak", 56),
    (56, 70, "prop", "white steam puff off the landed loaf: soft whoosh", 57),
    (72, 72, "cut", "cut to the street over the counter"),
    (84, 112, "foley", "the customer walks off screen-left with the basket: footsteps on cobbles, wicker creak"),
    (98, 104, "accent", "kit winks at the camera: bright 'ting' / sparkle", 98),
    (105, 129, "accent", "kit grins at us (cheeky musical sting)", 105),
    (123, 123, "cut", "plan: cut to shot 4 (market, crane down)"),
]
PAIRS = [(40, "ref/a/t0001.jpg", "ref a t0001 (CU character + prop)"), (100, "ref/a/t0046.jpg", "ref a t0046 (people behind a laden table)")]
