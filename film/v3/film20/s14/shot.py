#!/usr/bin/env python3
"""shot.py -- film 20 take s14 = shot 14, SITE site_rise / DAY, stages 0 -> 1 -> 2 -> 3.  g 945..994 + 4-frame handles each side (g 941..998, cuts).
COUNT "ชั้นหนึ่ง / ชั้นสอง / จนถึงยอด" (31.49 / 32.13 / 32.61 s): three eased crane-up SNAPS between the preset cameras site_rise_snap1/2/3; the
tower state jumps on each snap (first platform, second platform, finished spire) at the middle of the snap, the camera ends higher.
    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, cast20 = C.S, C.CO, C.cast20
lerp, clamp, ez, bf = C.lerp, C.clamp, C.ez, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(31.49), C.g_bound(33.21)        # 945, 996
H_IN, H_OUT = 4, 4
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1        # 941 .. 999
GS = list(range(G_FIRST, G_LAST + 1))
W1, W2, W3 = C.cap_g("ชั้นหนึ่ง"), C.cap_g("ชั้นสอง"), C.cap_g("จนถึงยอด")      # 948 / 967 / 981
SN = [(W1 - 5, W1 + 10), (W2 - 5, W2 + 10), (W3 - 4, W3 + 12)]                # snap windows (15 / 15 / 16 frames)
MID = [(a + b) // 2 for a, b in SN]                                            # stage jumps at the snap middles
LIGHT, PRESET = "DAY", "site_rise"


def stage_of(g):
    return 0 + sum(1 for m in MID if g >= m)


def poses(A):
    c = {k: (Vector(A["cams"][k]["loc"]), Vector(A["cams"][k]["look_at"])) for k in ("site_rise_snap1", "site_rise_snap2", "site_rise_snap3")}
    l1, k1 = c["site_rise_snap1"]
    # start pose: lower and closer than snap 1 (the legs only, stage 0)
    l0 = l1 + Vector((6.0, 40.0, -22.0)) * CO.SC * 0.55
    k0 = k1 - Vector((0.0, 0.0, 30.0))
    return [(l0, k0), c["site_rise_snap1"], c["site_rise_snap2"], c["site_rise_snap3"]]


def cam_at(P, g):
    """(loc, look): snaps between consecutive poses + a slow push / slide drift"""
    i, u = 0, 0.0
    loc, look = Vector(P[0][0]), Vector(P[0][1])
    for n, (a, b) in enumerate(SN):
        uu = C.snap_u(g, a, b, 1.7)
        if uu > 0:
            loc = P[n][0].lerp(P[n + 1][0], uu)
            look = P[n][1].lerp(P[n + 1][1], uu)
    t = (g - G_FIRST) / 30.0
    fwd = (look - loc)
    fz = 1.0 + 0.055 * t                                  # 5.5 %/s push toward the aim point
    loc = look - fwd / fz
    right = Vector((fwd.y, -fwd.x, 0.0)).normalized()
    loc = loc + right * (0.9 * CO.SC * t * 4.0)           # slide ~ 3.6 m/s at 100 m: ~40 px/s
    look = look + right * (0.9 * CO.SC * t * 4.0)
    return loc, look


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s14")
        self.P = poses(self.A)
        for ob in C.bpy.data.objects:
            if ob.name.startswith("fg_"):
                ob.hide_render = True
        C.bpy.ops.mesh.primitive_cube_add(size=1.0)       # camera-parented timber post at the left edge (foreground 1.7 D from the lens)
        ob = C.bpy.context.active_object
        ob.name = "fg_post_s14"
        ob.scale = (0.16, 2.6, 0.16)
        ob.parent = self.cam
        ob.location = (-0.8, -0.35, -1.7)
        ob.rotation_euler = (0.0, 0.0, math.radians(4.0))
        ob.data.materials.append(CO.STATE["M"]["timber"])
        self.key_cam(bf(G_FIRST), *cam_at(self.P, G_FIRST))
        self.scene.frame_set(bf(G_FIRST))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(self.P, g))
            S.set_stage(stage_of(g), frame=f)

    def report(self, g):
        return dict(g=g, stage=stage_of(g), heads={})

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
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
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
