#!/usr/bin/env python3
"""deliver.py -- s17 deliverables from raw/ (python3 deliver.py)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from deliver_common import deliver
G0, G1, H = 1337, 1447, 7
cues = [dict(frame=1330, duration=124 / 30.0, kind="ambience", label="calm day at the tower top: light wind, a few far birds (diagram moment, quiet)"),
        dict(frame=1359, duration=10 / 30.0, kind="glint", label="tiny bright 'ting' glint on the pointed rod tip (on 'แหลม' g 1362)"),
        dict(frame=1366, duration=28 / 30.0, kind="camera_move", label="eased pull-back down the wire to the full-height view (soft air whoosh)"),
        dict(frame=1405, duration=26 / 30.0, kind="crackle_soft", label="glowing pulse runs down the wire: soft electric hum/fizz travelling top to bottom, falling pitch"),
        dict(frame=1430, duration=0.9, kind="ground", label="pulse sinks into the ground plate: low soft thump, rings spread and fade quietly ('เงียบ ๆ')"),
        dict(frame=1329, duration=10 / 30.0, kind="dissolve", label="10-frame dissolve in from shot 16"),
        dict(frame=1442, duration=10 / 30.0, kind="dissolve", label="10-frame dissolve out to shot 18")]
deliver(HERE, "s17", [17], G0, G1, H, H, "DAY", {"rod": "set_rod(2) throughout (rod + wire); wire bevel 0.028 -> 0.07 D at runtime",
        "events": {"glint": 1362, "pullback": [1366, 1394], "pulse_travel": [1405, 1430], "ground_rings": [1429, 1453]}}, cues)
