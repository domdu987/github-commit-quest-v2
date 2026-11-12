#!/usr/bin/env python3
"""deliver.py -- s12: raw/s12 -> frames/ (g 1008..1138), take.mkv, meta.json, cues.json, contact.jpg; then QA numbers.
python3 deliver.py [qa]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib3

G0, G1, HOUT = 1008, 1131, 8
KICK, Q0, Q1 = 1035, 1062, 1122
meta = {"shots": [12], "g0": G0, "g1": G1, "handle_in": 0, "handle_out": HOUT,
        "transition_in": {"type": "cut", "frames": 0},
        "transition_out": {"type": "dissolve", "frames": 12, "note": "out-handle g 1131..1138 rendered in 3D (shot 12 camera continues)"},
        "shot_ranges": {"12": [G0, G1 - 1]}, "set": "v3/set3d3/harbor.py", "light": "WINTER",
        "mouth": {"foreman": [Q0, Q1], "note": "lip-sync cycle only inside the quote; closed (cigar) elsewhere; tommy never talks"},
        "events": {"kick": KICK, "bucket_lands": KICK + 12, "bucket_bounce_lands": KICK + 18, "punch_in": [1050, 1058], "reframe_to_tommy": [1092, 1104]}}
drips = [1013, 1035]                      # drip impacts (period 22, phase 3): before the kick into the bucket, after onto the ground
drips = [g for g in range(G0, G1 + HOUT) if (g - 3) % 22 == 21]
cues = [(G0, G1 + HOUT, "harbour winter ambience at the tank foot (gulls far, wind, low tank hum)", "ambience"),
        (G0, G0, "hard cut from shot 11", "cut")]
for g in drips:
    cues.append((g, g, ("drip: molasses drop plinks into the tin bucket" if g < KICK else "drip: molasses drop pats onto the frozen yard (soft)"), "drip", {"impact_frame": g}))
cues += [(KICK - 8, KICK - 2, "foreman winds up (cloth rustle, boot scrape)", "foley"),
         (KICK, KICK, "KICK: boot hits the tin bucket (hollow metal clang), molasses sloshes out; small camera jolt", "kick", {"impact_frame": KICK}),
         (KICK + 1, KICK + 7, "molasses splash on the ground where the bucket stood", "splash"),
         (KICK + 12, KICK + 12, "bucket lands on its side (tin clatter)", "clatter", {"impact_frame": KICK + 12}),
         (KICK + 18, KICK + 26, "small bounce and roll of the bucket (tin rattle dying away)", "clatter", {"impact_frame": KICK + 18}),
         (KICK + 8, 1050, "foreman's smug closed-mouth chuckle ('hmph', mouth closed, cigar)", "laugh"),
         (1050, 1058, "snap punch-in on the foreman (short whoosh in), peak about g 1054", "camera_snap", {"peak_frame": 1054}),
         (Q0, Q1, "the foreman's quoted line (in the narration track): mouth moves", "dialogue"),
         (1092, 1104, "reframe left onto tommy (soft whoosh)", "camera_move"),
         (G1 - 6, G1 + 6, "dissolve out to shot 13", "dissolve")]
lib3.deliver("s12", [("raw", 12, G0, G1 + HOUT - 1)], meta, cues)
if len(sys.argv) > 1:
    lib3.qa({12: (G0, G1 - 1)}, main={12: "foreman"})
