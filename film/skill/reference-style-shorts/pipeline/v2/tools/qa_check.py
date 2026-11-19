#!/usr/bin/env python3
"""qa_check.py -- staging and camera checks from out/qa.json (numbers written by build.py; stdlib only).
usage: python3 tools/qa_check.py [out/qa.json] [--md]"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.path.join(HERE, "..", "out", "qa.json")
qa = json.load(open(path))
man = json.load(open(os.path.join(os.path.dirname(path), "manifest.json")))
by = dict(((q["shot"], q["g"]), q) for q in qa)
# the frame that is on screen for each output frame (the incoming shot once the mix passes 50 percent)
vis = []
for g, src in enumerate(man["timeline"]):
    if len(src) == 3:
        vis.append(by[tuple(src[1] if src[2] >= 0.5 else src[0])])
    else:
        vis.append(by[tuple(src[0])])
L = []
P = L.append
P("frames on screen: %d" % len(vis))

# 1. pencil on the line end (s01: uid h1 arm r, s02: h2 arm r while the line grows), eraser on the track (s03: b3 arm l)
#    (these three rows are specific to shots/s01.py; they are skipped when the uids are not there)
e1 = [q["actors"]["h1"]["tip_r_to_pencil_px"] for q in qa if q["shot"] == "s01" and q["g"] >= 9 and "h1" in q["actors"]]
e2 = [q["actors"]["h2"]["tip_r_to_pencil_px"] for q in qa if q["shot"] == "s02" and q["g"] <= 84 and "h2" in q["actors"]]
e3 = [q["actors"]["b3"]["tip_l_to_line_end_px"] for q in qa if q["shot"] == "s03" and 104 <= q["g"] <= 131 and "b3" in q["actors"]]
if e1 and e2:
    P("pencil point to the growing line end: s01 max %.2f px (g 9-55), s02 max %.2f px (g 47-84)" % (max(e1), max(e2)))
if e3:
    P("eraser face centre to the visible line end while rubbing (g 104-131): %.1f to %.1f px (the felt face is 0.35 x 0.18 D = %d x %d px at the far scale)"
      % (min(e3), max(e3), round(0.35 * 166), round(0.18 * 166)))

# 2. heads
rows = []
for q in vis:
    for uid, a in q["actors"].items():
        if uid == "h1":
            continue
        rows.append((q["g"], uid, a["head"][0], a["head"][1], a["D_px"], a["head_bottom"]))
for uid in ("h2", "b3", "h3"):
    r = [x for x in rows if x[1] == uid]
    if not r:
        continue
    ys = [x[3] / 1280.0 for x in r]
    P("%s: head centre y %.2f-%.2f H, head D %.0f-%.0f px, lowest head bottom y = %.0f (must stay under 880)"
      % (uid, min(ys), max(ys), min(x[4] for x in r), max(x[4] for x in r), max(x[5] for x in r)))
two = [q for q in vis if "b3" in q["actors"] and "h3" in q["actors"]]
if two:
    rat = [q["actors"]["h3"]["D_px"] / q["actors"]["b3"]["D_px"] for q in two]
    dy = [q["actors"]["h3"]["head"][1] - q["actors"]["b3"]["head"][1] for q in two]
    q = ([x for x in two if x["g"] == 120] or two)[0]
    P("two-shot depth staging: near/far head ratio %.2f, near head %.0f to %.0f px lower; at g 120 near head x %.0f D %.0f px, far head x %.0f D %.0f px"
      % (rat[0], min(dy), max(dy), q["actors"]["h3"]["head"][0], q["actors"]["h3"]["D_px"], q["actors"]["b3"]["head"][0], q["actors"]["b3"]["D_px"]))

# 3. character travel inside each shot (own D, over the frames on screen)
def travel(uid, g0, g1):
    pts = [(q["actors"][uid]["head_world"], q["actors"][uid]["scale"]) for q in vis if uid in q["actors"] and g0 <= q["g"] <= g1]
    if not pts:
        return None
    xs = [p[0][0] / p[1] for p in pts]; ys = [p[0][1] / p[1] for p in pts]
    return max(xs) - min(xs), max(ys) - min(ys)
tv = [("hero in s02", travel("h2", 51, 101)), ("chief in s03", travel("b3", 102, 149)), ("hero in s03", travel("h3", 102, 149))]
tv = [(n, t) for n, t in tv if t]
if tv:
    P("head travel (own D): " + "; ".join("%s x %.3f y %.3f" % (n, t[0], t[1]) for n, t in tv))

# 4. camera: static frames, speed classes, framing changes
static = [q["g"] for q in vis if abs(q["zoom_rate"]) < 1.5 and q["pan"] < 8]
runs, cur = [], []
for g in static:
    if cur and g == cur[-1] + 1: cur.append(g)
    else:
        if cur: runs.append(cur)
        cur = [g]
if cur: runs.append(cur)
P("camera: %d fully static frame(s) of %d (zoom < 1.5 %%/s and pan < 8 px/s); longest static run %d frame(s)" % (len(static), len(vis), max([len(r) for r in runs] + [0])))
snap = [q["g"] for q in vis if q["corner"] > 450]
runs, cur = [], []
for g in snap:
    if cur and g <= cur[-1] + 2: cur.append(g)
    else:
        if cur: runs.append(cur)
        cur = [g]
if cur: runs.append(cur)
P("snap moves (corner speed > 450 px/s): " + ", ".join("g %d-%d" % (r[0], r[-1]) for r in runs))
for r in runs:
    sp = [by_q["corner"] for by_q in vis if r[0] <= by_q["g"] <= r[-1]]
    z0 = [q for q in vis if q["g"] == max(r[0] - 1, 0)][0]["cam"][2]; z1 = [q for q in vis if q["g"] == r[-1]][0]["cam"][2]
    P("   g %d-%d: %d frames, scale x%.2f, peak %.0f px/s = %.2f x mean" % (r[0], r[-1], len(r), z1 / z0, max(sp), max(sp) / (sum(sp) / len(sp))))
drift = [abs(q["zoom_rate"]) for q in vis if q["corner"] <= 450]
drift.sort()
P("drift frames: median zoom rate %.1f %%/s (quartiles %.1f-%.1f)" % (drift[len(drift) // 2], drift[len(drift) // 4], drift[3 * len(drift) // 4]))
blur = [(q["g"], q["blur"][0], round(q["plate_shift"])) for q in vis if q["blur"]]
P("plate motion blur on g: " + ", ".join("%d (%s, %d px)" % b for b in blur))
last = vis[-6:]
P("last 6 frames: zoom rate %.1f to %.1f %%/s" % (min(q["zoom_rate"] for q in last), max(q["zoom_rate"] for q in last)))
print("\n".join(("- " + l if "--md" in sys.argv else l) for l in L))
