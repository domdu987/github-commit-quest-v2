#!/usr/bin/env python3
"""shot.py -- film 17 take s07: shots 16-19 (the measuring montage), narration 28.25-34.74.
g0 850, g1 1045, handles 6 each side -> first_g 844 .. last_g 1051.  Blender frame = g.
  16  g 844..899   measure_chair   calipers on a head, push + slide, snap to the writing hand
  17  g 900..947   measure_low     finger on the gauge -> snap (14 f) -> foot on the foot board
  18  g 948..995   measure_wide    arm-span + ear, Bertillon writes the card, slide past the gauge
  19  g 996..1051  records_aisle   the card into a size drawer, drawers fill; push + slide
python3 shot.py probe|stills|final <shot> <a:b[:step]> [scale] [samples] [out]"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import cast17, K, lerp, lerpv, sstep, clamp
S = cast17.STORY17
RANGES = {16: (844, 899), 17: (900, 947), 18: (948, 995), 19: (996, 1051)}
PRESET = {16: "measure_chair", 17: "measure_low", 18: "measure_wide", 19: "records_aisle"}

def blink(g, off): return cast17.blink_at(g, 84, off)
def sway(g, a, f, ph=0.0): return a * math.sin(g * f + ph)
def P(story, **kw):
    p = dict(S[story][1]); p.update(kw); return p
def with_arm(p, key, **kw):
    d = dict(p[key]); d.update(kw); p = dict(p); p[key] = d; return p

# ------------------------------------------------------------------ camera paths (world m)
CAMS = {
 16: [(844, (-0.45, -0.25, 1.50), (1.00, 2.30, 1.28)), (862, (-0.10, 0.10, 1.46), (1.10, 2.30, 1.25)), (874, (0.15, 0.50, 1.44), (1.15, 2.30, 1.24)),
      (882, (-0.35, 0.65, 1.42), (1.40, 2.20, 1.22)), (899, (0.30, 1.05, 1.40), (1.20, 2.25, 1.20))],
 17: [(900, (0.30, 0.15, 0.50), (1.00, 2.35, 1.50)), (922, (-0.15, 0.30, 0.55), (1.00, 2.35, 1.50)), (930, (-0.25, 0.35, 0.55), (1.00, 2.35, 1.50)),
      (940, (0.40, 1.30, 0.65), (2.15, 3.30, 0.50)), (947, (0.70, 1.55, 0.65), (2.15, 3.30, 0.50))],
 18: [(948, (-2.90, -3.90, 1.50), (0.10, 2.40, 1.35)), (966, (-1.60, -3.95, 1.50), (0.50, 2.40, 1.35)), (981, (-0.20, -3.90, 1.45), (0.90, 2.40, 1.35)),
      (995, (0.60, -3.80, 1.45), (1.00, 2.40, 1.32))],
 19: [(996, (0.95, -3.40, 3.95), (-0.10, 6.40, 2.0)), (1014, (0.80, -2.30, 3.60), (-0.35, 6.30, 1.95)), (1030, (0.30, -0.90, 3.30), (-0.60, 5.90, 1.9)),
      (1051, (0.10, 0.60, 3.00), (-0.75, 5.60, 1.85))],
}

def stage(shot, T):
    A = T.A; M = A["marks"]
    if shot == 16:
        T.add("pris", "prisoner_sitting_a", M["chair"][:3], seated="chair")
        T.add("bert", "bertillon_measuring", M["clerk"][:3], mirror=True)
        T.add("gend", "gendarme_standing_a", (2.55, 3.05, 0.0))
    elif shot == 17:
        T.add("pris", "prisoner_sitting_a", M["chair"][:3], seated="chair")
        T.add("bert", "bertillon_measuring", (M["clerk"][0], M["clerk"][1], 0.0), mirror=True)
        T.add("foot", "prisoner_standing_c", (2.15, 3.10, 0.0))
        T.add("bert2", "bertillon_measuring", (1.45, 3.05, 0.0))
    elif shot == 18:
        T.add("arm", "prisoner_standing_b", M["armspan"][:3])
        T.add("bert", "bertillon_writing", (1.05, 1.25, 0.0))
        T.add("pris", "prisoner_sitting_a", M["chair"][:3], seated="chair")
        T.add("gend", "gendarme_standing_b", M["queue0"][:3])
    elif shot == 19:
        T.add("bert", "bertillon_holding_card", M["desk_clerk"][:3])
        T.add("gend", "gendarme_standing_a", M["desk_stand"][:3])

def poses(shot, T, g):
    B = lambda k, p, **kw: T.pose(k, g, p)
    if shot == 16:
        u = (g - 844) / 55.0
        bp = P("bertillon_measuring", lean=4 + sway(g, 1.2, .21), pitch=0.12 + 0.1 * sstep((g - 876) / 8.0), blink=blink(g, 10))
        # calipers: open around the head (g 844..872), then lowered and read (g 872..), nodding
        bp = with_arm(bp, "arm_r", hand=(0.88 + 0.05 * math.sin(g * .5), 0.34 - 0.06 * math.sin(g * .5)))
        B("bert", bp)
        B("pris", P("prisoner_sitting_a", head_roll=sway(g, 2.5, .13), blink=blink(g, 40), lean=sway(g, 1.0, .2)))
        B("gend", P("gendarme_standing_a", lean=sway(g, 1.5, .17), head_roll=sway(g, 3, .11), blink=blink(g, 55)))
    elif shot == 17:
        bp = P("bertillon_measuring", lean=4 + sway(g, 1.4, .23), blink=blink(g, 20)); bp = with_arm(bp, "arm_r", hand=(0.88, 0.34 + 0.07 * math.sin(g * .55)))
        B("bert", bp)
        B("pris", P("prisoner_sitting_a", head_roll=sway(g, 2.5, .13), blink=blink(g, 33)))
        B("foot", P("prisoner_standing_c", lean=sway(g, 1.5, .2), head_roll=sway(g, 3, .12), blink=blink(g, 47)))
        bp2 = P("bertillon_measuring", lean=6 + sway(g, 1.4, .25), pitch=0.6, blink=blink(g, 60)); bp2 = with_arm(bp2, "arm_r", hand=(0.95, 2.7 + 0.07 * math.sin(g * .6)))
        B("bert2", bp2)
    elif shot == 18:
        # the prisoner holds both arms out for the arm-span, Bertillon writes
        ap = P("prisoner_standing_b", lean=sway(g, 1.2, .19), head_roll=sway(g, 3, .13), blink=blink(g, 25),
               arm_r=dict(hand=(1.55, 0.55 + 0.03 * math.sin(g * .4)), bend=-0.1, stretch=1.1), arm_l=dict(hand=(-1.55, 0.55 - 0.03 * math.sin(g * .4)), bend=-0.1, stretch=1.1))
        B("arm", ap)
        B("bert", P("bertillon_writing", lean=5 + sway(g, 1.2, .22), pitch=0.55 + 0.05 * math.sin(g * .3), blink=blink(g, 50)))
        B("pris", P("prisoner_sitting_a", head_roll=sway(g, 2.5, .13), blink=blink(g, 33)))
        B("gend", P("gendarme_standing_b", lean=sway(g, 1.5, .17), blink=blink(g, 66)))
    elif shot == 19:
        # card raised, then slid into the drawer (hand moves to the cabinet wall), drawer closes
        u = clamp((g - 1008) / 22.0)
        bp = P("bertillon_holding_card", blink=blink(g, 18), lean=sway(g, 1.4, .2))
        B("bert", bp)
        B("gend", P("gendarme_standing_a", lean=sway(g, 1.5, .17), blink=blink(g, 40)))

def hooks(shot, T, g):
    K.set_flicker(1.0, frame=g); K.set_smoke(1.0, frame=g); K.set_dust(1.0, frame=g)
    if shot in (16, 17, 18): K.set_pendulum(frame=g)
    if shot == 19:
        # drawers: p-series open one after another, the card drawer slides shut (size drawers fill up)
        for i, nm in enumerate(["p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "q0", "q1", "q2", "q3", "q4", "q5"]):
            base = {"p0": .9, "p1": .5, "p2": .3, "p3": .7, "p4": .2, "p5": .6, "p6": .4, "p7": .8, "q0": .5, "q1": .8, "q2": .3, "q3": .6, "q4": .9, "q5": .2}[nm]
            wob = base * (0.55 + 0.45 * sstep((g - 996) / 20.0 - i * 0.06)) if i % 2 else base
            K.set_drawer(nm, clamp(wob + 0.04 * math.sin(g * .2 + i)), frame=g)

def run(shot, gs, scale, samples, out, do_render, threads=2):
    T = C.Rig(PRESET[shot])
    stage(shot, T)
    path = C.Path(CAMS[shot])
    K.clear_keys() if hasattr(K, "clear_keys") else None
    gs = list(gs)
    for g in gs:
        loc, look = path.at(g); T.key_cam(g, loc, look); hooks(shot, T, g)
    for g in gs: T.scene.frame_set(g); poses(shot, T, g)
    ppd = 256 if scale <= 0.5 else 320
    T.sprites(ppd, gs)
    json.dump({g: [round(c, 3) for c in path.at(g)[0]] for g in gs}, open(os.path.join(out, "cam_%d.json" % shot), "w")) if os.path.isdir(out) else None
    if do_render: return T.render(gs, out, scale, samples, threads)

def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if ":" in part else [a[0]]
    return out

if __name__ == "__main__":
    cmd, shot, spec = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    out = sys.argv[6] if len(sys.argv) > 6 else os.path.join(HERE, "work", "stills"); os.makedirs(out, exist_ok=True)
    lo, hi = RANGES[shot]; gs = [g for g in parse(spec) if lo <= g <= hi]
    if cmd == "final":
        pending = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        gs = pending
    if gs: run(shot, gs, scale, samples, out, cmd in ("stills", "final"), threads=int(os.environ.get("THREADS", 2)))
