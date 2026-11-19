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
F_FINGER = (2.00, 1.55, 0.84)        # thief's middle finger on the gauge table top
F_TOE = (2.12, 3.17, 0.06)           # jaws at heel/toe on the foot board
SWAP17 = 928                         # thief/Bertillon jump from the table to the foot board at the peak of the g921-935 snap
EAR_P = (-1.15, 2.70)                # thief at the ear insert (18)
SWAP18 = 974                         # measuring -> writing pose at the peak of the g968-980 snap
CAMS = {
 16: [(844, (-0.45, -0.25, 1.50), (1.10, 2.30, 1.28)), (862, (-0.05, 0.10, 1.46), (1.20, 2.30, 1.25)), (874, (0.00, 0.45, 1.44), (1.30, 2.30, 1.24)),
      (884, (-0.05, 0.60, 1.42), (1.35, 2.30, 1.22)), (899, (0.10, 0.70, 1.40), (1.40, 2.30, 1.22))],
 17: [(900, (1.55, 0.80, 1.15), (2.00, 1.60, 0.88)), (912, (1.70, 0.90, 1.12), (2.00, 1.58, 0.86)), (921, (1.80, 0.98, 1.10), (2.00, 1.56, 0.85)),
      (935, (1.35, 2.15, 0.55), (2.15, 3.25, 0.20)), (947, (1.50, 2.30, 0.52), (2.15, 3.22, 0.18))],
 18: [(948, (-0.10, 1.65, 1.50), (-1.00, 2.65, 1.42)), (958, (-0.20, 1.78, 1.50), (-1.00, 2.65, 1.42)), (967, (-0.30, 1.88, 1.50), (-1.02, 2.65, 1.42)),
      (980, (0.25, 1.55, 1.15), (-0.55, 2.45, 1.05)), (995, (0.15, 1.70, 1.15), (-0.55, 2.45, 1.05))],
 19: [(996, (0.05, 1.30, 1.50), (-1.15, 2.90, 1.30)), (1012, (-0.05, 1.55, 1.45), (-1.25, 3.00, 1.30)), (1030, (-0.20, 1.85, 1.42), (-1.25, 3.05, 1.30)),
      (1051, (-0.30, 2.15, 1.40), (-1.25, 3.15, 1.30))],
}
CAM0 = {s: CAMS[s][0][1] for s in CAMS}
DR = {"s": dict(y=2.12, w=0.20, h=0.13), "m": dict(y=3.02, w=0.34, h=0.22), "l": dict(y=3.72, w=0.50, h=0.34)}   # three drawer sizes (19)
DR_X = -1.28
PAPER_G = 1030

def stage(shot, T):
    A = T.A; M = A["marks"]; c0 = CAM0[shot]
    if shot == 16:
        T.add("pris", "prisoner_sitting_a", M["chair"][:3], seated="chair", toward=0.35, cam0=c0)
        T.add("bert", "bertillon_measuring", M["clerk"][:3], mirror=True)
        T.add("gend", "gendarme_standing_a", (2.90, 2.50, 0.0), mirror=True)
    elif shot == 17:
        T.add("thief", "prisoner_standing_c", (2.45, 2.15, 0.0))
        T.add("bert", "bertillon_measuring", (1.45, 2.0, 0.0))
    elif shot == 18:
        T.add("thief", "prisoner_standing_b", (EAR_P[0], EAR_P[1], 0.0))
        T.add("bert", "bertillon_measuring", (-0.50, 2.40, 0.0), mirror=True)
    elif shot == 19:
        T.add("bert", "bertillon_holding_card", (-0.70, 2.70, 0.0))
        import bpy
        for nm, d in DR.items():
            K.drawer_assembly("sz_" + nm, (DR_X, d["y"], 1.28), -90, w=d["w"], h=d["h"], depth=0.5, travel=0.42, cards=10, seed=5, front_mat="honey")
        B = K.Batch(17); B.box("walnut", (-1.30, 2.95, 1.25), (0.04, 2.2, 0.95)); B.finalize("sz_panel", ink_t=K.STATE["ink_t"] * 0.6)

def poses(shot, T, g):
    B = lambda k, p, pos=None: T.pose(k, g, p, pos)
    if shot == 16:
        bp = P("bertillon_measuring", lean=4 + sway(g, 1.2, .21), blink=blink(g, 10), pitch=0.12 + 0.1 * sstep((g - 876) / 8.0))
        tgt = (0.62 + 0.03 * math.sin(g * .4), 2.02, 1.34 + 0.02 * math.sin(g * .5))        # calipers on the prisoner's head
        B("bert", T.reach("bert", g, bp, tgt, "calipers_l"))
        B("pris", P("prisoner_sitting_a", head_roll=sway(g, 2.5, .13), blink=blink(g, 40), lean=sway(g, 1.0, .2)))
        w = S["bertillon_writing"][1]
        gp = P("gendarme_standing_a", pitch=0.45, gaze=(0.3, 0.9), lean=3 + sway(g, 1.2, .2), blink=blink(g, 55), arm_r=dict(w["arm_r"]), prop_r=dict(w["prop_r"]),
               arm_l=dict(w["arm_l"]), prop_l=dict(w["prop_l"]))
        gp = T.nib_on_card("gend", gp)                                                     # nib on the card
        d = dict(gp["arm_r"]); d["hand"] = (d["hand"][0] + 0.04 * math.sin(g * .9), d["hand"][1] + 0.025 * math.cos(g * 1.3)); gp["arm_r"] = d   # the pen scribbles on the card
        B("gend", gp)
    elif shot == 17:
        at_table = g < SWAP17
        if at_table:
            tp = P("prisoner_standing_c", lean=sway(g, 1.0, .2), blink=blink(g, 47), head_roll=sway(g, 2.5, .12), arm_r=dict(hand=(0.2, 1.5), bend=0.2, shape="point"))
            tp = T.hand_to("thief", g, tp, (F_FINGER[0] - 0.01, F_FINGER[1], F_FINGER[2] + 0.01 * math.sin(g * .5)), "r", shape="point")
            B("thief", tp, (2.45, 2.15, 0.0))
            bp = P("bertillon_measuring", lean=4 + sway(g, 1.2, .23), blink=blink(g, 20), pitch=0.35)
            tf = (F_FINGER[0] + 0.02, F_FINGER[1], F_FINGER[2] + 0.015 * math.sin(g * .6))   # jaws closing on the middle finger
            B("bert", T.reach("bert", g, bp, tf, "calipers_r", pos=(1.35, 2.0, 0.0)), (1.35, 2.0, 0.0))
        else:
            tp = P("prisoner_standing_c", lean=sway(g, 1.0, .2), blink=blink(g, 47), head_roll=sway(g, 2.5, .12))
            B("thief", tp, (2.2, 3.2, 0.06))
            T.cast["bert"]["mirror"] = True
            bp = P("bertillon_measuring", lean=12 + sway(g, 1.0, .25), blink=blink(g, 60), pitch=0.7, legs=dict(preset="step", stride=0.3, crouch=0.35))
            tt = (F_TOE[0] + 0.02 * math.sin(g * .6), F_TOE[1], F_TOE[2])
            B("bert", T.reach("bert", g, bp, tt, "calipers_l", pos=(2.95, 3.0, 0.0)), (2.95, 3.0, 0.0))
    elif shot == 18:
        T.cast["bert"]["mirror"] = True
        tp = P("prisoner_standing_b", lean=sway(g, 1.0, .19), head_roll=sway(g, 2.5, .13), blink=blink(g, 25))
        B("thief", tp)
        if g < SWAP18:
            bp = P("bertillon_measuring", lean=4 + sway(g, 1.3, .23), blink=blink(g, 20))
            ear = (EAR_P[0] + 0.21 + 0.01 * math.sin(g * .5), EAR_P[1] + 0.10, 1.40 + 0.015 * math.sin(g * .45))   # jaws around the thief's ear
            B("bert", T.reach("bert", g, bp, ear, "calipers_l"))
        else:
            bp = P("bertillon_writing", lean=5 + sway(g, 1.0, .22), pitch=0.55 + 0.05 * math.sin(g * .3), blink=blink(g, 50))
            bp = T.nib_on_card("bert", bp)
            d = dict(bp["arm_r"]); d["hand"] = (d["hand"][0] + 0.035 * math.sin(g * .9), d["hand"][1] + 0.02 * math.cos(g * 1.2)); bp["arm_r"] = d      # writing numbers
            B("bert", bp)
    elif shot == 19:
        open_m = sstep((g - 1002) / 10.0) * (1 - sstep((g - 1032) / 10.0))
        xf = DR_X + 0.42 * open_m
        u = sstep((g - 1000) / 10.0)
        w = sstep((g - 1012) / 14.0)                                              # card slides into the pulled-out medium drawer
        bp = P("bertillon_holding_card", blink=blink(g, 18), lean=sway(g, 1.0, .2))
        tgt = (lerp(-0.80, xf + 0.08, u) - 0.28 * w, lerp(2.75, DR["m"]["y"], u), lerp(1.55, 1.28, u))
        bp = T.reach("bert", g, bp, tgt, "card_r", arm="r")
        if g >= 1026: bp = dict(bp); bp.pop("prop_r", None)                       # card is inside
        B("bert", bp)

def hooks(shot, T, g):
    K.set_flicker(1.0, frame=g); K.set_smoke(1.0, frame=g); K.set_dust(0.35, frame=g)
    if shot in (16, 17, 18): K.set_pendulum(frame=g)
    for o in T.hide_objs: o.hide_render = True
    if shot == 19:
        K.set_drawer("sz_m", sstep((g - 1002) / 10.0) * (1 - sstep((g - 1032) / 10.0)), frame=g)
        K.set_drawer("sz_l", 0.8 * sstep((g - 1036) / 8.0), frame=g)           # a second pass: the large drawer slides out
        K.set_drawer("sz_s", 0.35 * sstep((g - 1040) / 8.0), frame=g)

def run(shot, gs, scale, samples, out, do_render, threads=2):
    T = C.Rig(PRESET[shot])
    import bpy
    T.hide_objs = [o for o in bpy.data.objects if any(m and m.name.startswith('beam_fx') for m in (getattr(o.data, 'materials', None) or []))]
    if shot in (16, 17): T.hide_objs += [bpy.data.objects['measure_cloth']]
    if shot == 17: T.hide_objs += [o for o in bpy.data.objects if o.name.startswith('fg')]
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
