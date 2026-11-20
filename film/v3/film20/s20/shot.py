#!/usr/bin/env python3
"""shot.py -- film 20 take s20 = shot 20 (g 1382..1429 + 4 handle frames g 1378..1381 before (hard cut in) and g 1430..1433 after
(hard cut out; the plan's last frame is g 1430 = round(47.71*30) - 1 = 1430... see G1)).
"ให้ทหารส่งโทรเลขไร้สาย" -- inside the wooden hut at the wire's foot the SOLDIER-TELEGRAPHIST taps the Morse key; on each tap the
spark gap on the bench flashes blue-white.  TOWER tower_hut / DUSK 1909.
    camera: the preset (0.0, -204.5, 1.45) m looking along +y; push 9 %/s toward the soldier's head + slide 30 px/s + arc + tilt
    taps (dots and dashes) at TAPS: key_press 0 -> 1 (the card's arm goes down onto the set's brass key), spark_gap(True) for the tap frames
    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out> [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

SHOT_G0, SHOT_G1 = C.g_bound(46.08), C.g_bound(47.71)       # 1382, 1431 (shot = 1382..1430)
H_IN, H_OUT = 4, 4
G0, G_LAST = SHOT_G0 - H_IN, SHOT_G1 + H_OUT - 1             # 1378 .. 1434
GS = list(range(G0, G_LAST + 1))
G_WORD = C.cap_g("โทรเลขไร้สาย")                              # 1409

PRESET, LIGHT = "tower_hut", None
TEL_DX, TEL_DY = 0.0, -0.4                    # m: soldier mark offset (desk centre; the desk top hides the card below 0.87 m)
AIM_DX = 0.6                                  # m: the aim point is 0.65 m to his right (screen: soldier left third, spark gap right third)
HEAD_Z = 2.2                                  # soldier's head centre above his feet (D)
PPD = 224
RAISE_M = 0.15                              # soldier raised on a (hidden) box so his torso, hands and the key prop clear the desk top
FLOOR_Z = (0.23 + RAISE_M) * 1.88                       # hut floor plank top: z 0.19 + 0.04 m -> D
SEAT_H = 0.5                                # D above the floor: the bentwood chair seat is at 0.50 m world (0.27 m above the plank = 0.5 D)
# Morse taps (film frames, inclusive first/last frame of each tap): dot dot dash dot dash dot
TAPS = [(1387, 1389), (1393, 1395), (1399, 1404), (1410, 1412), (1416, 1421), (1426, 1428)]
SPARK_FRAMES = set()
for a, b in TAPS:
    SPARK_FRAMES.update(range(a, b + 1))


def tap_amount(g):
    """key_press 0..1: each tap goes down in 1 frame, up in 1 frame."""
    for a, b in TAPS:
        if a - 1 <= g <= b + 1:
            if g <= a:
                return 0.5 if g == a - 1 else 1.0
            if g <= b:
                return 1.0
            return 0.5
    return 0.0


def cam_path(A):
    m = Vector(A["marks"]["telegraphist"])
    subj = m + Vector((AIM_DX * CO.SC, 0.35 * CO.SC, HEAD_Z + 0.45))   # aim between the soldier (left) and the spark gap (right)
    c = Vector(A["cams"][PRESET]["loc"])
    return C.CamPath(c, subj, G0, G_LAST, push=0.09, slide_px=-40.0, rise_px=0.0, arc_deg_s=ARC, tilt0=TILT0, tilt_deg_s=-3.0,
                     decay=0.3, snaps=[])


TILT0 = 2.0
ARC = 20.0


def pose_tel(g):
    p = dict(cast20.STORY20["telegraphist_key"][1])
    p.pop("stool", None)
    p["seated"] = 1
    p["seat_h"] = SEAT_H
    p["yaw"] = 0.25 + 0.05 * math.sin(g * 0.11)
    p["lean"] = 6.0 + 1.5 * math.sin(g * 0.17)
    p["head_roll"] = 3.0 * math.sin(g * 0.13)
    p["key_press"] = tap_amount(g)
    p["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.27))
    p["blink"] = blink(g, [G0 + 14, G0 + 47])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s20")
        m = self.A["marks"]["telegraphist"]
        self.A['marks']['telegraphist'] = (m[0] + TEL_DX * CO.SC, m[1] + TEL_DY * CO.SC, m[2])   # staging: pulled 1.2 m forward to the desk centre so his hands + the key sit ABOVE the desk top
        self.mark = (self.A['marks']['telegraphist'][0], self.A['marks']['telegraphist'][1], FLOOR_Z)                  # the hut floor plank top (0.23 m); a ray cast would hit the chair / the roof
        print("floor z (D):", round(self.mark[2], 3), flush=True)
        for o in C.bpy.data.objects:                                 # TAKE gate: duplicate headphones + the FG post clipping the spark -> no preset FG
            if o.name.startswith("fg_"):
                o.hide_render = True
        old = list(CO.STATE["sg_dyn"])                                # the set's arc + forks + pale halo spheres read as 'a ball with a scribble' (TAKE gate)
        for o in old:
            o.hide_render = True
        CO.STATE["sg_dyn"] = []                                      # S.spark_gap keeps only the blue point light; the arc is ours:
        import random
        rr = random.Random(20)
        sgp = Vector((-0.5 + 1.0, -203.0 + 0.45, 1.1))
        amat = CO.mat_emit("team8_arc", "#dff2ff", 14.0)
        self.arcs = []
        for k in range(3):                                           # three jagged variants between the two brass balls, swapped per frame
            mb = CO.MB("team8_arc%d" % k, CO.root())
            pts = [sgp + Vector((-0.115 + 0.23 * i / 7.0, rr.uniform(-0.02, 0.02), rr.uniform(-0.035, 0.035) if 0 < i < 7 else 0.0)) for i in range(8)]
            for a, b in zip(pts[:-1], pts[1:]):
                mb.rod(amat, a, b, 0.016, 0.016, 5)
            self.arcs += mb.finish(shadow=False)
            for o in self.arcs[-1:]:
                o.hide_render = True
        self.scene.view_settings.exposure = self.scene.view_settings.exposure + 0.35        # hut interior luma 70 -> ~80 (qa_stats floor)
        self.path = cam_path(self.A)
        self.key_cam(bf(G0), *self.path.at(G0))
        self.scene.frame_set(bf(G0))
        self.actors["tel"] = C.make_actor("tel", "telegraphist", os.path.join(WORK, "sprites"), cam=self.cam,
                                          contact=dict(width=1.2, depth=0.5, opacity=0.8))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.actors["tel"], f, self.mark)
            self.key_set(f, spark_gap=(g in SPARK_FRAMES))
            for k, o in enumerate(self.arcs):
                CO.setv(o, (g in SPARK_FRAMES) and (g % 3 == k), f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.actors["tel"].pose(f, pose_tel(g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), spark=bool(g in SPARK_FRAMES), sg_px=CO.project(CO.W((0.5, -202.55, 1.1))))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def cam_path_static():
    import tower20
    A = dict(marks={"telegraphist": CO.W(tower20._m(tower20.HUT[0] - 0.35, tower20.HUT[1] + 1.3)) if False else
                    Vector(tower20._m(tower20.HUT[0] - 0.35, tower20.HUT[1] + 1.3, 0.0))},
             cams={PRESET: dict(loc=Vector(CO.W(tower20.CAMS_M[PRESET]["loc"])))})
    return cam_path(A)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        P = cam_path_static()
        rows, worst = P.report(GS[:-1])
        for r in rows[::6]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
