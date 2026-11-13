#!/usr/bin/env python3
"""deliver.py -- s21 (shots 21-22): raw/s1..s5 -> frames/, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv, work/qa.txt."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from t5deliver import deliver
S = {1: (2038, 2091, "A high wide over the reopening-day queue, the empty wall"), 2: (2092, 2135, "B reverse from the wall: faces of the queue"),
     3: (2136, 2169, "C ECU the four hooks, push in"), 4: (2170, 2207, "D two-shot at the rope: lady gasps, gentleman doffs his bowler"),
     5: (2208, 2241, "E the hooks again, low and wider, push in (out-handle 2236-2241)")}
cues = [(2038, 2136, "the Salon Carre reopened: a big murmuring crowd, shuffling feet on parquet, echo under the skylight", "ambience"),
        (2044, 2044, "dissolve in from shot 20 (the closet office)", "cut"),
        (2092, 2092, "cut: reverse on the faces of the queue", "cut"),
        (2136, 2136, "cut to the four hooks: the murmur drops to a hush (one cough)", "cut"),
        (2136, 2170, "a single held low note on the bare wall", "accent"),
        (2170, 2242, "hushed crowd, a few whispers", "ambience"),
        (2174, 2180, "the lady gasps behind her gloved hand", "gesture"),
        (2182, 2200, "the gentleman lifts his bowler off (cloth brush), holds it to his chest", "gesture"),
        (2208, 2208, "cut back to the hooks", "cut"), (2225, 2228, "soft 'ting' on 'four hooks' (74.07 s)", "accent")]
deliver(dict(here=HERE, take="s21", shots=[21, 22], g0=2044, g1=2236, handle=6, setups=S,
             transition_in={"type": "dissolve", "frames": 10, "note": "plan: dissolves 9-12 f between locations (closet office -> gallery); in-handle g 2038-2043 rendered in 3D"},
             transition_out={"type": "dissolve", "frames": 10, "note": "next take s23 is paris (kiosk); out-handle g 2236-2241 rendered in 3D"},
             shot_ranges={"21": [2044, 2135], "22": [2136, 2235]},
             events={"cut_B": 2092, "shot22_hooks": 2136, "lady_gasp": [2174, 2178], "bowler_doff": [2182, 2200], "four_hooks_word": 2225},
             cues=cues, compare=[(2060, "a", 40), (2190, "a", 48), (2150, "a", 30)],
             set="v3/set3d7/louvre.py louvre empty_wall_queue (Mona gone + queue ropes keyed per frame, set_flames keyed per frame), 5 custom cameras 18-30 mm",
             light="GALLERY_DAY",
             cast="v3/cast7 crowd: lady, gentleman, newsboy, guard + runtime colour variants lady_b/c/d, gentleman_b/c (s21/t5lib.py, cast files untouched); "
                  "gentleman's bowler taken off via a runtime hat_off pose key + the derby drawn in his hand as a sprite overlay"))
