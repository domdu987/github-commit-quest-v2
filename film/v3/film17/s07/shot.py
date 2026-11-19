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
      (884, (-0.05, 0.75, 1.42), (1.50, 2.30, 1.22)), (899, (0.30, 1.05, 1.40), (1.95, 2.40, 1.20))],
 17: [(900, (0.30, 0.15, 0.50), (1.00, 2.35, 1.50)), (922, (-0.15, 0.30, 0.55), (1.00, 2.35, 1.50)), (930, (-0.25, 0.35, 0.55), (1.00, 2.35, 1.50)),
      (940, (0.95, 1.00, 1.00), (2.05, 3.10, 0.20)), (947, (1.05, 1.30, 1.00), (2.05, 3.10, 0.20))],
 18: [(948, (-2.00, -1.60, 1.50), (-0.70, 2.50, 1.40)), (966, (-1.50, -1.00, 1.48), (-0.60, 2.50, 1.40)), (976, (-0.60, -1.70, 1.50), (0.40, 2.00, 1.30)),
      (984, (-0.10, -2.00, 1.50), (1.00, 1.50, 1.30)), (995, (0.20, -1.90, 1.50), (1.05, 1.40, 1.30))],
 19: [(996, (0.55, -2.20, 3.20), (-0.60, 5.00, 1.8)), (1014, (0.45, -1.30, 2.90), (-0.75, 4.80, 1.7)), (1030, (0.20, -0.30, 2.60), (-0.90, 4.30, 1.6)),
      (1051, (0.10, 0.60, 2.40), (-1.00, 4.00, 1.55))],
}
CAM0 = {s: CAMS[s][0][1] for s in CAMS}
SWAP18 = 976          # sprite swap (measuring -> writing Bertillon) at the peak of the g968-984 snap
Q_FRONT = (-1.00, 2.55, 1.35)   # drawer q4 front when pulled out

def stage(shot, T):
    A = T.A; M = A["marks"]; c0 = CAM0[shot]
    if shot == 16:
        T.add("pris", "prisoner_sitting_a", M["chair"][:3], seated="chair", toward=0.35, cam0=c0)
        T.add("bert", "bertillon_measuring", M["clerk"][:3], mirror=True)
        T.add("gend", "gendarme_standing_a", (2.70, 2.10, 0.0), mirror=True)
    elif shot == 17:
        T.add("pris", "prisoner_sitting_a", M["chair"][:3], seated="chair", toward=0.35, cam0=c0)
        T.add("bert", "bertillon_measuring", (M["clerk"][0], M["clerk"][1], 0.0), mirror=True)
        T.add("foot", "prisoner_standing_c", (2.15, 3.10, 0.0))
        T.add("bert2", "bertillon_measuring", (1.60, 2.95, 0.0))
    elif shot == 18:
        T.add("arm", "prisoner_standing_b", (-1.15, 2.55, 0.0))
        T.add("bertA", "bertillon_measuring", (-0.35, 2.35, 0.0), mirror=True)
        T.add("bertB", "bertillon_writing", (1.05, 1.25, 0.0))
        T.add("pris", "prisoner_sitting_a", M["chair"][:3], seated="chair", toward=0.3, cam0=(0.0, -3.0))
        T.add("gend", "gendarme_standing_b", (2.3, -0.6, 0.0))
    elif shot == 19:
        T.add("bert", "bertillon_holding_card", (-0.30, 2.30, 0.0), mirror=True)
        T.add("gend", "gendarme_standing_a", (0.55, 3.2, 0.0))

def poses(shot, T, g):
    B = lambda k, p: T.pose(k, g, p)
    if shot == 16:
        bp = P("bertillon_measuring", lean=4 + sway(g, 1.2, .21), blink=blink(g, 10), pitch=0.12 + 0.1 * sstep((g - 876) / 8.0))
        tgt = (0.62 + 0.03 * math.sin(g * .4), 2.02, 1.34 + 0.02 * math.sin(g * .5))        # calipers on the prisoner's head
        B("bert", T.reach("bert", g, bp, tgt, "calipers_l"))
        B("pris", P("prisoner_sitting_a", head_roll=sway(g, 2.5, .13), blink=blink(g, 40), lean=sway(g, 1.0, .2)))
        w = S["bertillon_writing"][1]
        gp = P("gendarme_standing_a", pitch=0.45, gaze=(0.3, 0.9), lean=3 + sway(g, 1.2, .2), blink=blink(g, 55), arm_r=dict(w["arm_r"]), prop_r=dict(w["prop_r"]),
               arm_l=dict(w["arm_l"]), prop_l=dict(w["prop_l"]))
        gp["arm_r"]["hand"] = (w["arm_r"]["hand"][0] + 0.04 * math.sin(g * .7), w["arm_r"]["hand"][1] + 0.03 * math.cos(g * .9))   # the pen scribbles
        B("gend", gp)
    elif shot == 17:
        bp = P("bertillon_measuring", lean=4 + sway(g, 1.4, .23), blink=blink(g, 20))
        tgt = (0.98, 2.22 + 0.02 * math.sin(g * .5), 0.86 + 0.03 * math.sin(g * .6))       # the caliper jaws close on the prisoner's hand: the finger gauge
        B("bert", T.reach("bert", g, bp, tgt, "calipers_l"))
        B("pris", P("prisoner_sitting_a", head_roll=sway(g, 2.5, .13), blink=blink(g, 33)))
        B("foot", P("prisoner_standing_c", lean=sway(g, 1.5, .2), head_roll=sway(g, 3, .12), blink=blink(g, 47)))
        bp2 = P("bertillon_measuring", lean=10 + sway(g, 1.4, .25), pitch=0.7, blink=blink(g, 60), legs=dict(preset="step", stride=0.3, crouch=0.35))
        tf = (2.12 + 0.02 * math.sin(g * .6), 3.05, 0.02)                                    # jaws on the foot, at the foot board
        B("bert2", T.reach("bert2", g, bp2, tf, "calipers_r"))
        for k in ("bert", "pris"): T.hide(k, g, g >= 935)            # sprite swap at the peak of the g930-940 snap
        for k in ("bert2", "foot"): T.hide(k, g, g < 935)
    elif shot == 18:
        ap = P("prisoner_standing_b", lean=sway(g, 1.2, .19), head_roll=sway(g, 3, .13), blink=blink(g, 25),
               arm_r=dict(hand=(1.55, 0.55 + 0.03 * math.sin(g * .4)), bend=-0.1, stretch=1.1), arm_l=dict(hand=(-1.55, 0.55 - 0.03 * math.sin(g * .4)), bend=-0.1, stretch=1.1))
        B("arm", ap)
        bp = P("bertillon_measuring", lean=4 + sway(g, 1.3, .23), blink=blink(g, 20))
        ear = (-1.15 + 0.17 + 0.015 * math.sin(g * .5), 2.5, 1.45 + 0.02 * math.sin(g * .45))   # jaws on the arm-span man's ear
        B("bertA", T.reach("bertA", g, bp, ear, "calipers_l"))
        B("bertB", P("bertillon_writing", lean=5 + sway(g, 1.2, .22), pitch=0.55 + 0.05 * math.sin(g * .3), blink=blink(g, 50)))
        T.hide("bertA", g, g >= SWAP18); T.hide("bertB", g, g < SWAP18)
        B("pris", P("prisoner_sitting_a", head_roll=sway(g, 2.5, .13), blink=blink(g, 33)))
        B("gend", P("gendarme_standing_b", lean=sway(g, 1.5, .17), blink=blink(g, 66)))
    elif shot == 19:
        u = sstep((g - 1008) / 20.0)                         # raise the card to the drawer front
        v = sstep((g - 1032) / 10.0)                         # slid in: the card is gone
        bp = P("bertillon_holding_card", blink=blink(g, 18), lean=sway(g, 1.4, .2))
        tgt = (lerp(-0.62, Q_FRONT[0] + 0.02, u), lerp(2.30, Q_FRONT[1], u), lerp(1.62, Q_FRONT[2], u))
        bp = T.reach("bert", g, bp, tgt, "card_l", arm="r")
        if v >= 0.99: bp = dict(bp); bp.pop("prop_r", None)
        B("bert", bp)
        B("gend", P("gendarme_standing_a", lean=sway(g, 1.5, .17), blink=blink(g, 40)))

def hooks(shot, T, g):
    K.set_flicker(1.0, frame=g); K.set_smoke(1.0, frame=g); K.set_dust(0.35, frame=g)
    if shot in (16, 17, 18): K.set_pendulum(frame=g)
    for o in T.hide_objs: o.hide_render = True
    if shot == 19:
        names = ["p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "q0", "q1", "q2", "q3", "q5"]
        base = {"p0": .9, "p1": .5, "p2": .3, "p3": .7, "p4": .2, "p5": .6, "p6": .4, "p7": .8, "q0": .5, "q1": .8, "q2": .3, "q3": .6, "q5": .2}
        for i, nm in enumerate(names):
            K.set_drawer(nm, clamp(base[nm] * (0.6 + 0.4 * sstep((g - 996) / 30.0 - i * 0.05)) + 0.03 * math.sin(g * .2 + i)), frame=g)
        K.set_drawer("q4", 0.8 * sstep((g - 1000) / 14.0) * (1 - sstep((g - 1034) / 14.0)) + 0.0, frame=g)   # the size drawer opens, takes the card, shuts

def run(shot, gs, scale, samples, out, do_render, threads=2):
    T = C.Rig(PRESET[shot])
    import bpy
    T.hide_objs = [o for o in bpy.data.objects if any(m and m.name.startswith('beam_fx') for m in (getattr(o.data, 'materials', None) or []))]
    if shot in (16, 17): T.hide_objs += [bpy.data.objects['measure_cloth']]
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
