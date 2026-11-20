#!/usr/bin/env python3
"""shot.py -- film 20 take s12 = shot 12, SITE site_girders / DAY stage 1.  g 822..906 + in-handle 4 (g 818..821, cut) + out-handle 4
(g 907..910, cut).  "แต่เขาก็สร้างต่อ เหล็ก 18,000 ชิ้น": the camera slides along a huge stack of red-lead girders at 1 m height; two workers
carry a girder on their shoulders past it, a derrick swings a girder up behind; snap push on "เหล็ก 18,000 ชิ้น".
    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(27.39), C.g_bound(30.23)       # 822, 907
H_IN, H_OUT = 4, 4
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1        # 818 .. 910
GS = list(range(G_FIRST, G_LAST + 1))
G_STEEL = C.cap_g("เหล็ก 18,000")                   # the strongest word: snap push
LIGHT, PRESET = "DAY", "site_girders"
PPD = 256

CAM0 = (-73.0, -39.8, 1.0)                         # metres: south of the stack (stack face y ~ -31.8), 1 m high
SUBJ = (-73.0, -31.8, 1.45)                         # a point on the pile face the camera pushes toward
WALK_Y = -34.2                                     # the carriers walk along the stack, 2 m from the pile face, 3 m from the lens
CARRY_X0, CARRY_X1 = -71.4, -66.7                  # metres, walking +x (screen-right) ... over the whole range


def cam_path():
    return C.CamPath(CO.W(CAM0), CO.W(SUBJ), G_FIRST, G_LAST, push=0.02, slide_px=160.0, rise_px=-12.0, arc_deg_s=6.0,
                     tilt0=-3.0, tilt_deg_s=0.0, decay=0.2,
                     snaps=[dict(g=(G_STEEL - 2, G_STEEL + 14), k=1.12, peak=2.0, shift=(0.0, 0.0), tilt=0.0)])


def walk_x(g):
    """carriers' front-man x (metres): constant walking speed across the range"""
    return lerp(CARRY_X0, CARRY_X1, (g - G_FIRST) / float(G_LAST - G_FIRST))


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s12")
        self.path = cam_path()
        self.key_cam(C.bf(G_FIRST), *self.path.at(G_FIRST))
        self.scene.frame_set(C.bf(G_FIRST))
        for ob in C.bpy.data.objects:
            if ob.name.startswith("fg_"):
                ob.hide_render = True
        self.actors["a"] = C.make_actor("a", "riveter_tongs", os.path.join(WORK, "sprites"), cam=self.cam,
                                        contact=dict(width=1.3, depth=0.55, opacity=0.8))
        self.actors["b"] = C.make_actor("b", "riveter_hammer", os.path.join(WORK, "sprites"), cam=self.cam,
                                        contact=dict(width=1.3, depth=0.55, opacity=0.8))
        self.make_carried_girder()

    def make_carried_girder(self):
        """the girder on the two men's shoulders: a red-lead I-girder (web + two flanges) 4.6 m long, repositioned every frame"""
        M = CO.STATE["M"]
        parts = []
        for (sz, dz) in (((4.6, 0.16, 0.025), 0.0), ((4.6, 0.16, 0.025), 0.28), ((4.6, 0.025, 0.28), 0.14)):
            C.bpy.ops.mesh.primitive_cube_add(size=1.0)
            ob = C.bpy.context.active_object
            ob.scale = (sz[0] * CO.SC, sz[1] * CO.SC, sz[2] * CO.SC)
            ob.data.materials.append(M.get("ironlt") or M["redlead"])
            parts.append((ob, dz))
        self.girder = parts

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            loc_, look_ = self.path.at(g)
            jv = Vector((0.08 * math.sin(g * 1.9), 0.08 * math.cos(g * 1.3), 0.05 * math.sin(g * 2.3 + 1.0)))   # hand-held energy
            self.key_cam(f, loc_ + jv, look_ + jv * 0.4)
            xa = walk_x(g)
            for who, dx in (("a", 0.0), ("b", -2.6)):
                m = CO.W((xa + dx, WALK_Y, 0.0))
                z = C.ground_z(m[0], m[1]) if False else 0.0
                C.place(self.actors[who], f, (m[0], m[1], z))
            # carried girder: ride on the shoulders (z ~ 1.45 m), centred between the two men, long axis +x
            cx = CO.W((xa - 1.3, WALK_Y + 0.12, 1.42))
            for ob, dz in self.girder:
                ob.location = (cx[0], cx[1], cx[2] + dz * CO.SC * 0 + (dz - 0.14) * CO.SC)
                ob.keyframe_insert("location", frame=f)
                ob.hide_render = False
                ob.keyframe_insert("hide_render", frame=f)
            self.key_set(f, set_stage=1, crane_swing=ez((g - G_FIRST) / float(G_LAST - G_FIRST)))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for who, cast, ph in (("a", "riveter_tongs", 0.0), ("b", "riveter_hammer", 0.5)):
                p = cast20.cycle(cast, (g / 30.0) * 1.6 + ph, "walk", 1, None, "both", 1.0)
                p["arm_r"] = dict(hand=(0.35, -0.35), bend=0.7, stretch=1.0, layer="front")
                p["arm_l"] = dict(hand=(0.2, -0.3), bend=0.7, stretch=1.0, layer="back")
                p["expr"] = "working"
                p["head_roll"] = 3 * math.sin(g * 0.3 + ph)
                p["blink"] = blink(g, [830 if who == "a" else 861, 890])
                p["t"] = g / 30.0
                self.actors[who].pose(f, p, camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        return dict(g=g, heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        P = cam_path()
        rows, worst = P.report(range(G_FIRST, G_LAST))
        print(min(r["px"] for r in rows), max(r["px"] for r in rows), "longest parked", worst)
        sys.exit(0)
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
