#!/usr/bin/env python3
"""deliver.py -- s25 (shot 25): raw/s1..s3 -> frames/, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv, work/qa.txt."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s21"))
from t5deliver import deliver
S = {1: (2438, 2484, "A floor level: the trunk slides out from under the bed by the candle"),
     2: (2485, 2530, "B attic: vincenzo crouched peeking, trunk out, lid opens"),
     3: (2531, 2578, "C down into the open trunk: the panel, her smile, push in (out-handle 2573-2578)")}
cues = [(2438, 2579, "attic at dusk: candle flame flutter, distant church bell, rooftop pigeons", "ambience"),
        (2444, 2444, "dissolve in from the street", "cut"),
        (2450, 2482, "wooden trunk scraping out over floorboards", "foley"),
        (2485, 2485, "cut to the room", "cut"), (2485, 2494, "last scrape of the trunk", "foley"),
        (2494, 2514, "lid creaks open on old hinges", "foley"), (2512, 2522, "his glance at the window: a tiny tense pluck", "accent"),
        (2531, 2531, "cut into the trunk", "cut"), (2531, 2579, "warm music swell on her smile, 'two whole years' (84.95 s)", "music")]
deliver(dict(here=HERE, take="s25", shots=[25], g0=2444, g1=2573, handle=6, setups=S,
             transition_in={"type": "dissolve", "frames": 10, "note": "plan/task: dissolve in (paris street -> attic); in-handle g 2438-2443 rendered in 3D"},
             transition_out={"type": "dissolve", "frames": 10, "note": "next is shot 26 (dealer's shop, a location change); out-handle g 2573-2578 rendered in 3D"},
             shot_ranges={"25": [2444, 2572]},
             events={"trunk_slides": [2450, 2494], "cut_room": 2485, "lid_opens": [2494, 2514], "glance_window": [2512, 2521], "cut_trunk_insert": 2531},
             cues=cues, compare=[(2470, "a", 80), (2510, "a", 10), (2560, "a", 30)],
             set="v3/set3d7/louvre.py room (under_bed_insert build, ATTIC_DUSK): set_trunk keyed per frame, set_flames keyed; runtime: sun-shaft haze sheet hidden, "
                 "the trunk panel raised 0.13 D once the lid is past 35 deg and turned 180 deg (it sat under the trunk's inner top face and read upside down), "
                 "a small warm no-shadow fill over the trunk; 3 custom cameras 20-24 mm",
             light="ATTIC_DUSK",
             cast="v3/cast7 vincenzo (normal clothes, vincenzo_peek_bed, mirrored to face the trunk)"))
