#!/usr/bin/env python3
"""shot.py -- film 23 take s12: shot S12 (LANE day), "bikes (ยกรถถังสี่สิบตัน)": BIGZOOM 2 / reveal: from close on the cyclists' faces PULL BACK and up wide:
four soldiers lift the rubber tank over their heads (the ONLY airborne tank, flagged by set_lift); the cyclists brake.  Cut in (no in-handle).
QA_ART_SET S12: the lane-dirt shade hue 233 / mid 264 -> per-surface ambient on the dirt tinted to hue 248 (tint_dirt).

    python3 shot.py probe a:b[:s] | stills a:b[:s] out [scale] [samples] | final a:b[:s] [scale] [samples] | ground all
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c23 as C                                                          # noqa: E402
from c23 import GH, cast23, lerp, sm, seg                                # noqa: E402
import bpy                                                               # noqa: E402

DIRT_K = (1.0, 1.0, 1.0)          # per-channel factor on the ground / dirt shade colour (QA: hue 233 -> 248)
STOP_I = 24                         # frame (shot-local) the cyclists have come to rest
V0 = 4.0                            # D/s riding speed before the brake
LIFT_I = (6, 44)
CAM_KEYS = [(0.0, dict(loc=(-3.4, -41.8, 3.3), look_at=(-5.2, -47.4, 3.0), lens=24.0)),
            (0.5, dict(loc=(1.4, -54.0, 5.2), look_at=(-6.0, -42.6, 2.5), lens=23.0)),
            (1.0, dict(loc=(5.5, -59.0, 7.4), look_at=(-6.0, -38.0, 2.1), lens=22.0))]                    # the lift (out of frame until the camera has pulled back)


def tint_dirt(k=DIRT_K):
    """QA_ART_SET S12 / S07: per-surface ambient on the lane dirt: multiply the shade colour of the ground and dirt materials by k (channel factors)."""
    n = 0
    for m in bpy.data.materials:
        if not (m.name.startswith("GH_morning_ground") or "_t_dirt" in m.name or "_t_rut" in m.name):
            continue
        nt = m.node_tree
        for nd in nt.nodes:
            if nd.bl_idname == "ShaderNodeMix" and getattr(nd, "blend_type", "") == "MULTIPLY" and not nd.inputs[7].is_linked:
                c = nd.inputs[7].default_value
                nd.inputs[7].default_value = (c[0] * k[0], c[1] * k[1], c[2] * k[2], 1.0); n += 1
            elif nd.bl_idname == "ShaderNodeVectorMath" and nd.operation == "SCALE" and not nd.inputs[0].is_linked and nd.inputs[0].default_value[2] > 0:
                c = nd.inputs[0].default_value
                nd.inputs[0].default_value = (c[0] * k[0], c[1] * k[1], c[2] * k[2]); n += 1
    return n


def lifter_casts(marks, cam0):
    """assign GI faces: the one nearest the S13 start camera is the smiler (the quote speaker)."""
    from mathutils import Vector
    order = sorted(range(4), key=lambda i: (Vector(marks[i][:2]) - Vector(cam0[:2])).length)
    names = {order[0]: "gi_smile", order[1]: "gi_driver", order[2]: "gi_pump", order[3]: "gi_designer"}
    return [names[i] for i in range(4)]


class T(C.Take):
    SID = "S12"
    D_IN = 0
    HERE_DIR = HERE

    def tweak(self):
        # BIGZOOM 2 re-keyed so both cyclists stay framed (x 0.1-0.9, heads above y 845) through the pull-back; same start idea (close on their faces) and the
        # same wide end on the lift
        sh = C.SH.SHOTS["S12"]
        K = CAM_KEYS
        sh["cam"] = K[0][1]
        sh["move"] = dict(path=K)

    def __init__(self, quality="preview"):
        C.Take.__init__(self, quality, work=os.path.join(HERE, "work"))
        m = self.marks
        tint_dirt()
        self.pa, self.pb = m["cyclist_a"][0][:3], m["cyclist_b"][0][:3]
        W = cast23.CANVAS23_WIDE
        self.a = self.add("cya", "fr_beret", W["fr_beret"])
        self.b = self.add("cyb", "fr_cap", W["fr_cap"])
        self.lm = m["lifters"]
        cam13 = C.SH.SHOTS["S13"]["cam"]["loc"]
        self.lc = lifter_casts([(x[0], x[1]) for x in self.lm], (cam13[0] + self.origin.x, cam13[1] + self.origin.y))
        self.L = [self.add("lf%d" % k, self.lc[k]) for k in range(4)]
        self.tank = bpy.data.objects["tank_lift"]
        self.shadow_all()

    # ------------------------------------------------------------ choreography
    def h_lift(self, i):
        return seg(i, *LIFT_I)

    def ride_d(self, i):
        """distance still to ride before the stop point: constant speed V0 then a smooth brake ending at STOP_I (d = 0 for i >= STOP_I)"""
        T0 = STOP_I / 30.0
        s = i / 30.0
        return V0 * (T0 - s) ** 2 / (2 * T0) if s < T0 else 0.0

    def pose_cy(self, k, g):
        i = g - self.clk["g0"]
        cast, col = ("fr_beret", "green") if k == 0 else ("fr_cap", "maroon")
        braking = i >= 8
        p = cast23.ride_frame(cast, i / 14.0 + 0.3 * k, facing=-1, expr="stunned" if braking else "happy", state="brake" if braking else "ride", look=0.8,
                              mouth=("open", 0.12, 0.09) if braking else "smile", basket=(k == 0))
        p["blink"] = cast23.blink_at(i, 80, 13 + 29 * k)
        if braking:
            p["fx"] = ["sweat"]
        p["t"] = i / 30.0
        return p

    def pose_lift(self, k, g):
        i = g - self.clk["g0"]
        h = self.h_lift(i)
        lh = max(1.3, 3.45 * h)
        p = cast23.lift_pose(self.lc[k], i / 30.0 * 1.0 + 0.37 * k, lift_h=lh, expr="determined", strain=h)
        p["blink"] = cast23.blink_at(i, 100 + 7 * k, 11 * k)
        return p

    def staging(self, gs):
        fs = [self.f_of(g) for g in gs]
        for g in gs:
            f = self.f_of(g); i = g - self.clk["g0"]
            GH.set_lift(self.h_lift(i), frame=f)
            for k, (cy, pm) in enumerate(((self.a, self.pa), (self.b, self.pb))):
                d = self.ride_d(i)
                C.place(cy, f, (pm[0] + 0.55 * d, pm[1] - d, C.gz(pm[0] + 0.55 * d, pm[1] - d)))              # they come up the lane (+y) and stop on the mark
            for k, a in enumerate(self.L):
                C.place(a, f, self.lm[k][:3])
        for g in gs:
            f = self.f_of(g)
            self.scene.frame_set(f)
            self.a.pose(f, self.pose_cy(0, g), camera=self.cam, upper_k=1.0)
            self.b.pose(f, self.pose_cy(1, g), camera=self.cam, upper_k=1.0)
            for k, a in enumerate(self.L):
                a.pose(f, self.pose_lift(k, g), camera=self.cam, upper_k=1.0)
        self.sprites_for([(self.a, 256), (self.b, 256)] + [(a, 256) for a in self.L], fs)

    def report(self, g):
        f = self.f_of(g)
        self.scene.frame_set(f)
        return dict(g=g, f=f, cam=[round(v, 3) for v in self.cam.location], lift_z=round(self.tank.location.z, 3), heads=C.head_report(self, f))


if __name__ == "__main__":
    C.run(T)
