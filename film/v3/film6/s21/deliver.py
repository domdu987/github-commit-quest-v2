#!/usr/bin/env python3
"""deliver.py -- take s21 (shots 21-22): python3 deliver.py  (see deliver_lib.py)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deliver_lib
CUTS = [1694, 1740, 1802, 1830]
NAMES = ["21a street", "21b hood low", "22a count", "22b shoo", "22c spare loaf"]
cfg = dict(
    take="s21", id=21, shots=[21, 22], range=(1633, 1852), g0=1639, g1=1847, cuts=CUTS,
    transition_in={"type": "cut", "frames": 0, "note": "plan: cut from shot 20 (market); 6 in-handle frames g 1633..1638 rendered in 3D (the stranger already walking)"},
    transition_out={"type": "cut", "frames": 0, "note": "plan: cut to shot 23 (market square_eye) at g 1847; 6 out-handle frames g 1847..1852 (kit by the racks)"},
    shot_ranges={"21": [1639, 1739], "22": [1740, 1846]},
    events={"21a_stranger_walks_in": [1633, 1687], "arrives_at_counter": 1688, "21b_hooded_face_low": [1694, 1739], "hand_up_a_dozen": [1712, 1740],
            "22a_henry_counts_12_on_fingers": [1753, 1797], "22b_shoo": [1802, 1829], "kit_off_the_stool": [1810, 1826],
            "22c_kit_glances_at_spare_loaf": 1838},
    set="v3/set3d6/bakery.py: bakery AFTERNOON, steam 0.35 (0 in 21b: no ribbons across the hooded face), oven flicker keyed per frame; 5 custom cameras (street side 24 mm, inside low 22 mm, street low 30 mm on henry, street two-shot 24 mm, inside by the right-wall racks 24 mm); a paler loaf card (cast6.loaf_svg, crust blended to cream) added on the right-wall shelf at (6.2, 3.4, 2.7)",
    light="AFTERNOON",
    cast="v3/cast6: inspector (hooded, hood 1, walk cycle -> inspector_hooded), henry (henry_count with fingers_r 1..5 x2 + 1..2, henry_shoo with mouth closed), kit (stool z 0.98 -> hops off; kit_scared; sad -> determined glance)",
    label_of=lambda g: NAMES[sum(g >= c for c in CUTS)],
    cues=[(1633, 1853, "bakery in the afternoon: low oven crackle, street murmur through the counter opening", "ambience", {}),
          (1633, 1688, "the stranger's slow footsteps on the cobbles + long cloak rustle", "foley", {}),
          (1688, 1690, "he stops at the shutter board (one heavier step)", "foley", {"peak_frame": 1688}),
          (1694, 1694, "cut inside: low ominous cello note under the hooded face", "accent", {}),
          (1712, 1718, "gloved hand comes up (cloth rustle)", "gesture", {"peak_frame": 1714}),
          (1740, 1740, "cut: henry low angle", "cut", {})] +
         [(1753 + int(round(i * 44 / 11.0)), 1755 + int(round(i * 44 / 11.0)), "henry counts finger %d (tiny wooden 'tock')" % (i + 1), "accent", {})
          for i in range(12)] +
         [(1806, 1828, "henry shoos kit: flapping hand whooshes x3, kit's scared squeak-free gulp", "gesture", {"peak_frame": 1808}),
          (1812, 1818, "kit hops off the stool (small thump)", "foley", {"peak_frame": 1816}),
          (1838, 1843, "kit glances at the spare loaf: soft 'idea' twinkle", "accent", {"peak_frame": 1840}),
          (1847, 1847, "plan: cut to shot 23 (market)", "cut", {})],
    compare=[(1720, "a/t0046.jpg"), (1780, "a/t0010.jpg")],
    hue_rows=[("s21 shots 21-22 (g 1639-1846)", (1639, 1846)), ("s21 21a street (g 1633-1693)", (1633, 1693)), ("s21 21b inside low (1694-1739)", (1694, 1739)),
              ("s21 22a-b counter (g 1740-1829)", (1740, 1829)), ("s21 22c racks (g 1830-1852)", (1830, 1852))],
    hue_refs=[("ref a t0001 t0046 t0047", ["a/t0001.jpg", "a/t0046.jpg", "a/t0047.jpg"])],
)
deliver_lib.run(HERE, cfg)
