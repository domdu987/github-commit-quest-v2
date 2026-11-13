#!/usr/bin/env python3
"""deliver.py -- take s23 (shot 23): python3 deliver.py  (see deliver_lib.py)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deliver_lib
CUTS = [1887, 1916]
NAMES = ["23a walk", "23b hood", "23c royal"]
cfg = dict(
    take="s23", id=23, shots=[23], range=(1841, 1940), g0=1847, g1=1935, cuts=CUTS,
    transition_in={"type": "cut", "frames": 0, "note": "plan: cut from shot 22 (bakery); 6 in-handle frames g 1841..1846 rendered in 3D"},
    transition_out={"type": "cut", "frames": 0, "note": "plan: shot 24 (big_scale_insert) follows at g 1935; 6 out-handle frames g 1935..1940 (royal reveal continues)"},
    shot_ranges={"23": [1847, 1934]},
    events={"23a_walk_crowd_parts": [1841, 1886], "parting": {"man1b": 1846, "man1": 1853, "woman1": 1856, "woman1b": 1866},
            "stops_centre": 1890, "hood_back_1_to_0.15": [1898, 1911], "blink": [1913, 1915], "hard_cut_to_inspector_royal": 1916},
    set="v3/set3d6/bakery.py: market AFTERNOON; 3 custom cameras (eye level 24 mm in the square looking north, low 24 mm medium, lower/closer 26 mm for the reveal); braziers flicker keyed per frame",
    light="AFTERNOON",
    cast="v3/cast6: inspector (hooded walk cycle -> inspector_hood_drop, hood 1 -> 0.15), inspector_royal (inspector_reveal: tabard with three lions, chain of office) after the hard cut; townsfolk woman1 x2, man1 x2 (part with walk cycles, then stunned)",
    label_of=lambda g: NAMES[sum(g >= c for c in CUTS)],
    cues=[(1841, 1941, "market square: crowd murmur that drops to a hush as he passes", "ambience", {}),
          (1841, 1890, "the stranger's measured footsteps on cobbles, cloak swish", "foley", {}),
          (1846, 1878, "townsfolk shuffle aside (4 quick step-scuffles + a gasp)", "foley", {}),
          (1887, 1887, "cut: low angle (drum hit)", "cut", {}),
          (1898, 1911, "he throws back the hood: big cloth whoosh", "gesture", {"peak_frame": 1904}),
          (1916, 1940, "HARD CUT reveal: royal fanfare stab + chain jingle; crowd gasp", "accent", {"peak_frame": 1916}),
          (1935, 1935, "plan: shot 24 (big scale insert)", "cut", {})],
    compare=[(1870, "a/t0062.jpg"), (1925, "a/t0051.jpg")],
    hue_rows=[("s23 shot 23 (g 1847-1934)", (1847, 1934)), ("s23 23a walk (g 1841-1886)", (1841, 1886)), ("s23 23b-c reveal (g 1887-1940)", (1887, 1940))],
    hue_refs=[("ref a t0062 t0072", ["a/t0062.jpg", "a/t0072.jpg"])],
)
deliver_lib.run(HERE, cfg)
