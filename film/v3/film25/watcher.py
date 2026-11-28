#!/usr/bin/env python3
"""watcher.py: finishes + pushes each take as soon as its frames are complete (encode, QA, push to render25/t1)."""
import os, sys, time, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
M = {  # take: (label, g0, g1, first, last, move)
 "s06": ("6", 125, 154, 125, 153, "PULL 10 % (4.0 -> 4.4 D) + slight drift"),
 "s14": ("14", 353, 396, 353, 395, "FOLLOW the model tank (3/4 top-down), then PULL / swoop to the engineer's face"),
 "s29": ("29+30", 882, 918, 882, 917, "FOLLOW the plate in, then PUSH 8 % on the rivets"),
 "s31": ("31+32", 918, 960, 918, 959, "FOLLOW the track drop, then a gentle slide along the loop"),
 "s33": ("33", 960, 982, 960, 981, "PUSH 10 % on the sponson"),
 "s34": ("34", 982, 1016, 982, 1015, "FOLLOW the barrel in, PUNCH 15 % on the clunk (g 1005)"),
 "s58": ("58", 1724, 1746, 1724, 1745, "PUSH 10 % onto the board"),
 "s62": ("62", 1813, 1843, 1813, 1842, "lateral slide from the water tank to the Mark I"),
 "s28": ("28", 838, 882, 838, 881, "PUSH 10 %"),
 "s63": ("63", 1843, 1880, 1843, 1879, "PULL 10 % + ARC"),
 "s05": ("5", 84, 125, 84, 124, "PUSH 12 % + slight ARC"),
 "s15": ("15", 396, 429, 396, 428, "PUSH 12 % + ARC"),
 "s16": ("16", 429, 459, 429, 458, "PULL 10 %"),
 "s17": ("17", 459, 485, 459, 484, "FOLLOW the brush"),
 "s01": ("1+2", 0, 44, 0, 43, "PUSH in through the doors (wide to close), eased"),
 "s37": ("37", 1071, 1095, 1071, 1094, "FOLLOW the crate swing (pan)"),
 "s60": ("60+61", 1778, 1813, 1778, 1812, "PUSH 10 %, PUNCH 15 % on the lid open (g 1801)"),
 "s36": ("36", 1043, 1071, 1043, 1070, "FOLLOW the brush stroke"),
 "s03": ("3+4", 44, 84, 44, 83, "tilt down with the hull, then pan / push onto the dial"),
 "s13": ("13", 316, 353, 316, 352, "PUSH 12 %, WHIP out over the last 5 frames"),
 "s35": ("35", 1016, 1043, 1016, 1042, "FOLLOW the hammer, slide right"),
 "s38": ("38", 1095, 1135, 1095, 1134, "slow ARC 6 deg round the crate"),
}
while True:
    left = 0
    for t, (lab, g0, g1, f, l, mv) in M.items():
        d = os.path.join(HERE, t)
        if os.path.exists(os.path.join(d, "QA.md")) or not os.path.isdir(d):
            continue
        left += 1
        if all(os.path.exists(os.path.join(d, "frames", "g_%04d.json" % g)) for g in range(f, l + 1)):
            subprocess.run(["python3", "shot.py", "autograde", "%d:%d" % (f, l)], cwd=d, stdout=open(os.path.join(HERE, "watcher.log"), "a"), stderr=subprocess.STDOUT)
            subprocess.run(["python3", os.path.join(HERE, "s06", "finish.py"), d, lab, str(g0), str(g1), str(f), str(l), "--move", mv, "--push"],
                           stdout=open(os.path.join(HERE, "watcher.log"), "a"), stderr=subprocess.STDOUT)
    if left == 0:
        break
    time.sleep(60)
