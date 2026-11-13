#!/usr/bin/env python3
"""deliver.py -- take s11 (shot 11): raw/11a, 11b, 11c -> frames/, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv, work/qa.txt.
python3 deliver.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk_deliver

G0, G1, H, G_11B, G_11C = 971, 1093, 8, 1011, 1051
Q_ON, Q_OFF = 1026, 1095
C = dict(
    take="s11", shots=[11], g0=G0, g1=G1, handle_in=H, handle_out=H,
    segs=[("11a", G0 - H), ("11b", G_11B), ("11c", G_11C)],
    seg_ranges={"11a": (G0 - H, G_11B - 1), "11b": (G_11B, G_11C - 1), "11c": (G_11C, G1 + H - 1)},
    transition_in={"type": "cut", "frames": 0, "handle": [G0 - H, G0 - 1],
                   "note": "plan: hard cuts on the alarm; 8-frame in-handle g 963..970 rendered in 3D anyway (gaffer at rest, lamp at his side)"},
    transition_out={"type": "cut_or_dissolve", "frames": 0, "handle": [G1, G1 + H - 1],
                    "note": "8-frame out-handle g 1093..1100 rendered in 3D (11c push continues, the quote's last syllables g 1093..1095)"},
    transitions=[{"at": G0, "type": "in", "handle": [G0 - H, G0 - 1]},
                 {"at": G_11B, "type": "cut", "from_shot": "11a", "to_shot": "11b"},
                 {"at": G_11C, "type": "cut", "from_shot": "11b", "to_shot": "11c"},
                 {"at": G1, "type": "out", "handle": [G1, G1 + H - 1]}],
    shot_ranges={"11": [G0, G1 - 1], "11a": [G0, G_11B - 1], "11b": [G_11B, G_11C - 1], "11c": [G_11C, G1 - 1]},
    set="v3/set3d5/mine.py tunnel LAMP; the set's 3D cage hidden (not in this shot)",
    cast="v3/cast5: gaffer (lift-lamp pose built per frame from gaffer_lift_lamp, flame 1.0 -> 1.7, mouth = lip-sync on the quote g 1026..1095), miner1/2/3 (shrug)",
    cage="not in shot",
    cues=[(G0 - H, G1 + H, "tunnel room tone: drips, timber creak, lamp hiss", "ambience"),
          (978, 992, "the gaffer swings his safety lamp up high: brass handle squeak, flame whoosh as it brightens", "prop", {"peak_frame": 990}),
          (990, G1 + H, "the raised flame burns bright: steady soft roar of the wick", "lamp"),
          (G_11B, G_11B, "cut: closer, low on the gaffer and the lamp", "cut"),
          (Q_ON, Q_OFF, "the gaffer's quoted line (narration voice carries it; his mouth moves g 1026..1095)", "dialogue"),
          (G_11C, G_11C, "cut: the miners in front, the gaffer behind them", "cut"),
          (1054, 1072, "the three miners shrug: cloth rustle, a dismissive snort", "gesture", {"peak_frame": 1061})],
    pairs=[("11a", 995, 83), ("11b", 1035, 85), ("11c", 1064, 87)],
)
if __name__ == "__main__":
    tk_deliver.run(C)
