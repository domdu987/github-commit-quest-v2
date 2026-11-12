#!/usr/bin/env python3
"""deliver.py -- s16 deliverables from raw/ (python3 deliver.py)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from deliver_common import deliver
G0, G1, H = 1248, 1337, 7
S = [1283, 1286, 1289, 1292, 1295, 1298, 1302, 1304, 1307, 1310, 1313, 1315]
cues = [dict(frame=1241, duration=103 / 30.0, kind="ambience", label="night storm bed: wind round the tower top, distant rain, low rumble"),
        dict(frame=1262, duration=0.6, kind="thunder_far", label="cloud flicker in the storm masses, soft far rumble"),
        dict(frame=1283, duration=34 / 30.0, kind="crackle", label="stepped leader: dry electric crackle building, one sizzle tick per step",
             steps=S),
        dict(frame=1293, duration=0.5, kind="crackle_branch", label="side branches fork off into empty sky and die (thin sizzles)"),
        dict(frame=1299, duration=9 / 30.0, kind="camera_snap", label="snap punch-in on the spire (short whoosh), lands g 1308 after 'จุดที่สูง'", peak_frame=1303),
        dict(frame=1312, duration=5 / 30.0, kind="crackle_up", label="upward streamer hisses off the empty finial"),
        dict(frame=1317, duration=0.4, kind="strike", label="contact on the finial + return stroke: sharp crack, flash (on 'ที่สุดเสมอ')"),
        dict(frame=1317, duration=1.0, kind="thunder", label="thunder clap right on top of the crack, rolling off; flash flicker to g 1328"),
        dict(frame=1240, duration=10 / 30.0, kind="dissolve", label="10-frame dissolve in from shot 15"),
        dict(frame=1332, duration=10 / 30.0, kind="dissolve", label="10-frame dissolve out to shot 17 (day diagram)")]
deliver(HERE, "s16", [16], G0, G1, H, H, "NIGHT_STORM", {"rod": "set_rod(0) throughout (empty spire)",
        "events": {"leader_start": 1283, "punch_in": [1299, 1308], "strike": 1317, "flash_flicker": [1317, 1328]}}, cues)
