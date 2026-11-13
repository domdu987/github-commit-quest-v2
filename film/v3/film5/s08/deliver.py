#!/usr/bin/env python3
"""deliver.py -- take s08 (shot 8): raw/8a, raw/8b -> frames/, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv, work/qa.txt.
python3 deliver.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk_deliver

G0, G1, H, G_8B = 691, 757, 8, 729
C = dict(
    take="s08", shots=[8], g0=G0, g1=G1, handle_in=H, handle_out=H,
    segs=[("8a", G0 - H), ("8b", G_8B)],
    seg_ranges={"8a": (G0 - H, G_8B - 1), "8b": (G_8B, G1 + H - 1)},
    transition_in={"type": "cut_or_dissolve", "frames": 0, "handle": [G0 - H, G0 - 1],
                   "note": "8-frame in-handle g 683..690 rendered in 3D (8a camera already drifting): enough for a dissolve of up to 12 frames"},
    transition_out={"type": "cut_or_dissolve", "frames": 0, "handle": [G1, G1 + H - 1],
                    "note": "8-frame out-handle g 757..764 rendered in 3D (8b push continues); shot 9 opens on the cage insert"},
    transitions=[{"at": G0, "type": "in", "handle": [G0 - H, G0 - 1]},
                 {"at": G_8B, "type": "cut", "from_shot": "8a", "to_shot": "8b", "note": "cut on 'ไอ้เด็ก' (24.25 s, g 730)"},
                 {"at": G1, "type": "out", "handle": [G1, G1 + H - 1]}],
    shot_ranges={"8": [G0, G1 - 1], "8a": [G0, G_8B - 1], "8b": [G_8B, G1 - 1]},
    set="v3/set3d5/mine.py tunnel LAMP; the set's 3D cage hidden (alfie carries the cast's 2D held cage)",
    cast="v3/cast5: miner1/2/3 (miners_laugh poses, bouncing), alfie with prop 'cage' + pose key 'bird' (canary inside the bars, 3 notes)",
    cage="2D held cage (cast5 prop 'cage', bird drawn inside the bars); set cage hidden",
    cues=[(G0 - H, G1 + H, "tunnel room tone: drips, timber creak, lamp hiss", "ambience"),
          (G0, G1, "the miners roar with laughter: belly laughs, a wheeze, a knee slap (no words)", "laughter"),
          (G0 + 4, G0 + 14, "miner1 jabs his finger at the boy (sleeve swish)", "gesture", {"peak_frame": G0 + 8}),
          (G_8B, G_8B, "cut to alfie, the laughter continues behind him", "cut"),
          (G_8B, G1 + H, "the canary sings 3 small notes, thin and sweet under the laughter", "bird_song", {"notes": 3}),
          (G_8B + 6, G_8B + 20, "alfie hugs the cage closer: soft wire jingle", "prop")],
    pairs=[("8a", 712, 47), ("8b", 748, 47)],
)
if __name__ == "__main__":
    tk_deliver.run(C)
