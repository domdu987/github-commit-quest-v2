#!/usr/bin/env python3
"""s64 -- rows 64+65 "วันนั้น นักบินอังกฤษ รายงานว่า" (g 1880-1931), SKY sky_close_cockpit, Look A.  W -> C in one move: the RFC biplane (big in frame) flies over the Somme fields (prop spinning, the plane
drifts along +x), the camera FOLLOWS it and then eases in PUSH 25 % to pilot25 leaning out of the cockpit (lean_look: goggles up, eyes wide), saturated blue sky, wing edge and struts in the near frame.
   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D
C, F, cast25, bpy = D.C, D.F, D.C.cast25, D.bpy
from mathutils import Vector
G0, G1 = 1880, 1932
V = 0.10


class Take(D.Rig):
    def __init__(self, work):
        D.Rig.__init__(self, "sky_close_cockpit", work, fstop=2.8, sun_e=9.0, sky_k=1.3, sun_left=30.0, sun_el=38.0)
        self.root = [o for o in bpy.data.objects if o.parent is None and o.type == "EMPTY" and "plane" in o.name.lower()]
        self.pl = F.S.get("plane") or None
        # the plane's root = the empty carrying scale 2.2 at z = 60 (set by sky.build close)
        cands = [o for o in bpy.data.objects if abs(o.scale.x - 2.2) < 1e-3 and o.location.z > 50]
        self.root = cands[0]
        self.prop = [o for o in bpy.data.objects if o.name.endswith("prop") or "prop" in o.name.lower()]
        self.x0 = self.root.location.x
        self.pil = self.actor("p", "pilot25", canvas=cast25.CANVAS25_POSES["pilot25_lean_look"], contact=None)

    def seat(self, g):
        self.root.location.x = self.x0 + V * (g - G0)
        bpy.context.view_layer.update()
        return self.root.matrix_world @ Vector((-0.8, 0.0, 1.9))

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0)
        w = C.calm(u); w2 = C.smooth(max(0.0, (u - 0.25) / 0.75))
        cp = self.seat(g)
        P = Vector((cp.x, cp.y, cp.z - 1.5))
        d = 19.0 - 15.6 * w2
        az = -90.0 + 18.0 * (1 - w2)
        return D.orbit(P, az, d, 3.0 - 1.1 * w2, 1.5 + 0.4 * w2 + 1.5 * (1 - w2), side=0.0, lx=0.9 * w2), 28.0

    def pose_of(self, g):
        k = g - G0
        p = D.story("pilot25_lean_look")
        w = C.smooth((g - 1900) / 14.0)
        p["lean"] = round(24 + 16 * w, 1); p["yaw"] = round(0.6 + 0.2 * w, 3); p["pitch"] = 0.6
        p["gaze"] = [0.8, 0.9]; p["head_roll"] = round(8 + 6 * math.sin(k * 0.3), 2)
        p["t"] = (k / 10.0) % 1.0
        p["mouth"] = "open" if False else p.get("mouth", "talk_a")
        p["blink"] = D.blink(g, [1913])
        p["light25"] = -1; p["rim25"] = 0.6
        return p

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            cp = self.seat(g)
            feet = Vector((cp.x, cp.y, cp.z - 1.5))
            self.key_frame(g, cam, lens, dict(p=dict(feet=feet, pose=self.pose_of(g))), focus=feet + Vector((0, 0, 1.8)))
        self.pose_frames(gs)

    def on_frame(self, f):
        D.Rig.on_frame(self, f)
        self.seat(f)
        for o in self.prop:
            o.rotation_euler[0] = 0.9 * (f - G0)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
