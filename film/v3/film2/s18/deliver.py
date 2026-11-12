#!/usr/bin/env python3
"""deliver.py -- s18 deliverables from raw/ (python3 deliver.py)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from deliver_common import deliver
G0, G1, H = 1447, 1585, 7
cues = [dict(frame=1440, duration=152 / 30.0, kind="ambience", label="rain outside the open arches, drips off the wet rope onto the planks, wind"),
        dict(frame=1462, duration=0.8, kind="thunder", label="flash outside the arches, thunder"),
        dict(frame=1470, duration=1.0, kind="crackle_faint", label="faint intermittent crackle in the top corner of the chamber"),
        dict(frame=1501, duration=0.6, kind="crackle", label="beat 1 'ผ่านหิน': crackle crawls over the stone (gritty), lands g 1505"),
        dict(frame=1521, duration=0.6, kind="crackle", label="beat 2 'ผ่านไม้': crackle runs along the wooden beam and headstock (woody snap), lands g 1523"),
        dict(frame=1542, duration=0.65, kind="crackle", label="beat 3 'ผ่านเชือก': hiss down the wet rope (sizzle on water), lands g 1543"),
        dict(frame=1550, duration=1.2, kind="drips", label="glowing drops fall off the rope: sizzling drips on the planks ('ระฆังที่เปียกฝน')"),
        dict(frame=1500, duration=6 / 30.0, kind="camera_snap", label="snap onto the stone"),
        dict(frame=1517, duration=6 / 30.0, kind="camera_snap", label="snap onto the wood"),
        dict(frame=1537, duration=6 / 30.0, kind="camera_snap", label="snap onto the rope"),
        dict(frame=1439, duration=10 / 30.0, kind="dissolve", label="10-frame dissolve in from shot 17"),
        dict(frame=1580, duration=10 / 30.0, kind="dissolve", label="10-frame dissolve out to shot 19")]
deliver(HERE, "s18", [18], G0, G1, H, H, "NIGHT_STORM", {"rod": "set_rod(0) throughout",
        "events": {"stone": [1501, 1516], "wood": [1521, 1537], "rope": [1542, 1560], "flash_outside": [1462, 1465]}}, cues)
