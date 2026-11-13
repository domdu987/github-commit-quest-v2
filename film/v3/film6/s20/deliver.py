#!/usr/bin/env python3
"""deliver.py -- take s20 (shot 20): python3 deliver.py  (see deliver_lib.py)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deliver_lib
CUT = 1606
cfg = dict(
    take="s20", id=20, shots=[20], range=(1572, 1644), g0=1578, g1=1639, cuts=[CUT],
    transition_in={"type": "cut", "frames": 0, "note": "plan: cut from shot 19 (bakery small_scale_insert); 6 in-handle frames g 1572..1577 rendered in 3D"},
    transition_out={"type": "cut", "frames": 0, "note": "plan: cut to shot 21 (bakery counter, AFTERNOON) at g 1639; 6 out-handle frames g 1639..1644 (push continues)"},
    shot_ranges={"20": [1578, 1638]},
    events={"20a_empty_pillory_long_shadows": [1572, 1605], "20b_kit_reverse": [1606, 1644], "eyes_widen": 1614, "turn_to_lens": [1616, 1622]},
    set="v3/set3d6/bakery.py: market AFTERNOON (low warm sun 26 deg from the WSW: long shadows); 20a near the pillory_low preset (lifted to 1.5-1.75 D to see the shadows on the planks / cobbles), 20b custom reverse with the pillory behind kit; braziers flicker keyed per frame",
    light="AFTERNOON",
    cast="v3/cast6: kit (flour boy) in 20b only: kit_think (hand on chin) -> stunned -> shocked, hands open",
    label_of=lambda g: "20a pillory" if g < CUT else "20b kit",
    cues=[(1572, 1645, "market square in the afternoon, quiet: distant market murmur, a crow caws once, a creak of the empty pillory board", "ambience", {}),
          (1606, 1606, "cut: reverse on kit (tiny whoosh)", "cut", {}),
          (1614, 1620, "kit's eyes go wide: realisation sting (bright 'ding!' + string stab)", "accent", {"peak_frame": 1614}),
          (1616, 1622, "head snaps round to the lens (cloth swish)", "gesture", {"peak_frame": 1618}),
          (1639, 1639, "plan: cut to shot 21 (bakery counter, the hooded stranger)", "cut", {})],
    compare=[(1600, "a/t0062.jpg"), (1630, "a/t0001.jpg")],
    hue_rows=[("s20 shot 20 (g 1578-1638)", (1578, 1638)), ("s20 20a pillory (g 1572-1605)", (1572, 1605)), ("s20 20b kit (g 1606-1644)", (1606, 1644))],
    hue_refs=[("ref a t0062 t0072", ["a/t0062.jpg", "a/t0072.jpg"])],
)
deliver_lib.run(HERE, cfg)
