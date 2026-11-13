#!/usr/bin/env python3
"""deliver.py -- take s09 (shots 9 + 10): raw/9a..10c -> frames/ (two 10-frame dissolves mixed), meta.json, cues.json, contact.jpg,
compare.jpg, take.mkv, work/qa.txt.   python3 deliver.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk_deliver

G0, G1, H = 757, 971, 8
D1, D2, DISS = 812, 871, 10
G_9B, G_9D, G_10B, G_10C, G_SIL = 787, 842, 906, 936, 913
C = dict(
    take="s09", shots=[9, 10], g0=G0, g1=G1, handle_in=H, handle_out=H,
    segs=[("9a", G0 - H), ("9b", G_9B), ("9c", D1), ("9d", G_9D), ("10a", D2), ("10b", G_10B), ("10c", G_10C)],
    seg_ranges={"9a": (G0 - H, G_9B - 1), "9b": (G_9B, D1 + 6), "9c": (D1 - 7, G_9D - 1), "9d": (G_9D, D2 + 6),
                "10a": (D2 - 7, G_10B - 1), "10b": (G_10B, G_10C - 1), "10c": (G_10C, G1 + H - 1)},
    dissolves=[{"at": D1, "frames": DISS, "from": "9b", "to": "9c"}, {"at": D2, "frames": DISS, "from": "9d", "to": "10a"}],
    transition_in={"type": "cut_or_dissolve", "frames": 0, "handle": [G0 - H, G0 - 1],
                   "note": "8-frame in-handle g 749..756 rendered in 3D (9a push already moving)"},
    transition_out={"type": "cut", "frames": 0, "handle": [G1, G1 + H - 1],
                    "note": "plan: hard cut into shot 11; 8-frame out-handle g 971..978 rendered in 3D (10c push continues) in case of a dissolve"},
    transitions=[{"at": G0, "type": "in", "handle": [G0 - H, G0 - 1]},
                 {"at": G_9B, "type": "cut", "from_shot": "9a", "to_shot": "9b"},
                 {"at": D1, "type": "dissolve", "frames": DISS, "mixed": [D1 - 5, D1 + 4], "from_shot": "9b", "to_shot": "9c",
                  "mix": "smoothstep P*P*(3-2P), P = i/(n+1); day 1 -> day 5"},
                 {"at": G_9D, "type": "cut", "from_shot": "9c", "to_shot": "9d"},
                 {"at": D2, "type": "dissolve", "frames": DISS, "mixed": [D2 - 5, D2 + 4], "from_shot": "9d", "to_shot": "10a",
                  "mix": "smoothstep; day 5 -> day 10 (= the shot 9 / shot 10 boundary)"},
                 {"at": G_10B, "type": "cut", "from_shot": "10a", "to_shot": "10b"},
                 {"at": G_10C, "type": "hard_cut", "from_shot": "10b", "to_shot": "10c", "note": "the alarm: on 'เขาตะโกน' (31.11 s)"},
                 {"at": G1, "type": "out", "handle": [G1, G1 + H - 1]}],
    shot_ranges={"9": [G0, D2 - 1], "10": [D2, G1 - 1], "9a": [G0, G_9B - 1], "9b": [G_9B, D1 - 1], "9c": [D1, G_9D - 1],
                 "9d": [G_9D, D2 - 1], "10a": [D2, G_10B - 1], "10b": [G_10B, G_10C - 1], "10c": [G_10C, G1 - 1]},
    set="v3/set3d5/mine.py tunnel LAMP; inserts: the set's 3D cage on its nail with the canary sprite INSIDE on the perch (second cross "
        "dowel removed at runtime so no bar cuts the bird); chalk tally (1 / 5 / 10) shrink-wrapped on the pit prop above the nail",
    cast="v3/cast5: canary sprite (inserts); 10c alfie with prop 'cage' + pose key 'bird' (perch_quiet, inside the bars), gaffer/miner1/miner2 far",
    cage="9a-10b: set 3D cage on the nail, canary card at the perch (behind the front wires); 10c: 2D held cage, set cage hidden",
    cues=[(G0 - H, G1, "tunnel room tone, close and quiet around the cage", "ambience"),
          (G0, D1, "day 1: the canary sings a long bright song, 5 notes (one per floating note)", "bird_song", {"notes": 5}),
          (G_9B, G_9B, "cut: ECU of the singing bird", "cut"),
          (D1 - 5, D1 + 5, "dissolve: days pass (soft whoosh)", "dissolve"),
          (D1, D2, "day 5: a shorter song, 3 notes", "bird_song", {"notes": 3}),
          (D1 + 2, D1 + 6, "chalk scratch: the tally reads 5", "prop"),
          (D2 - 5, D2 + 5, "dissolve: days pass", "dissolve"),
          (D2, G_SIL, "day 10: only 3 thin notes, weaker", "bird_song", {"notes": 3}),
          (G_SIL, G_10C, "silence: the beak closes, the room tone drops away, one drip", "silence"),
          (G_10C, G_10C, "HARD CUT: alfie", "cut"),
          (G_10C, G1 + H, "alfie shouts 'run!' (narration carries the line; his mouth is a held shout, not lip-synced); cage wires rattle", "shout"),
          (G_10C + 8, G_10C + 18, "the men in the depth turn round", "gesture")],
    pairs=[("9a", 775, 39), ("9b", 800, 41), ("9c", 830, 43), ("10b", 925, 69), ("10c", 955, 71)],
)
if __name__ == "__main__":
    tk_deliver.run(C)
