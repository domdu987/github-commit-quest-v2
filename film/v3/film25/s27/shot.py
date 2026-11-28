#!/usr/bin/env python3
"""s27 -- row 27 GAG "ไอ้ถังน้ำ" (g 817-838), TRIAL camp_close_tank, Look A.  tommy_b25 holds his tin cup under the tank's tap, waiting, deadpan:
a drip falls into the cup, he blinks, then stares at us.  DEADPAN near-hold 0.4 s then a slow PUSH 6 %.  The tank hull side (plain: stencil off) is the near
backdrop 0.9 D behind him, his shadow falls on it; hatch / tap stay beside his head.
    python3 shot.py probe|draft|final <gspec>      post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D                                          # noqa: E402
C, F, cast25, bpy = D.C, D.F, D.C.cast25, D.bpy
from mathutils import Vector                             # noqa: E402
import tank25 as TK                                      # noqa: E402

PRESET = "camp_close_tank"
G0, G1 = 817, 838
ND = 1.0                                                 # card distance from the hull plate
TAPX = -5.0


class Take(D.Rig):
    def __init__(self, work):
        D.Rig.__init__(self, PRESET, work, fstop=2.0, sun_e=15.0, sky_k=1.3, sun_col=(1.0, 0.95, 0.88), ev=1.0)
        self.H = F.S["tank"]
        TK.set_stencil(self.H, 0); D.flatten_hull(self.H, (0.34, 0.38, 0.17))
        bpy.context.view_layer.update()
        self.mw = self.H.root.matrix_world
        m = F.S["mark"]; ml = self.mw.inverted() @ Vector(m["pos"]); self.sg = -1.0 if ml.y < 0 else 1.0
        # hull half-width from the set's tap mesh (outermost vertices of the plates group): use the spout end
        tap = [o for o in bpy.data.objects if o.name.endswith("_tap")][0]
        inv = self.mw.inverted(); ys = []
        for v in tap.data.vertices:
            w = tap.matrix_world @ v.co; l = inv @ w
            if l.y * self.sg > 0: ys.append(abs(l.y))
        self.spout_y = max(ys)                                        # outer end of the spout (local |y|)
        self.hh = min(ys)                                             # hull plate surface
        n = self.mw.to_3x3() @ Vector((0, self.sg, 0)); self.nrm = math.degrees(math.atan2(n.y, n.x))     # outward normal (deg)
        self.tap_w = self.mw @ Vector((TAPX, self.sg * self.spout_y, 1.25))                              # spout tip, world
        self.actor_b = self.actor("tb", "tommy_b25", contact=dict(width=1.5, depth=0.7, opacity=0.6))
        self.feet = self.mw @ Vector((TAPX - 1.75, self.sg * (self.hh + ND), 0.0))
        self.feet.z = F.gh(self.feet.x, self.feet.y)
        # a drip: small bright water bead
        me = bpy.data.meshes.new("drip"); ob = bpy.data.objects.new("drip", me); bpy.context.scene.collection.objects.link(ob)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07, segments=12, ring_count=8, location=(0, 0, -50)); src = bpy.context.active_object
        ob.data = src.data; bpy.data.objects.remove(src)
        mat = bpy.data.materials.new("water"); mat.use_nodes = True
        bs = mat.node_tree.nodes["Principled BSDF"]; bs.inputs["Base Color"].default_value = (0.75, 0.9, 1.0, 1); bs.inputs["Roughness"].default_value = 0.05
        bs.inputs["Transmission Weight"].default_value = 0.6; bs.inputs["Emission Color"].default_value = (0.6, 0.8, 1.0, 1); bs.inputs["Emission Strength"].default_value = 0.6
        ob.data.materials.append(mat); ob.scale = (1, 1, 1.5); self.drip = ob

    def pose_of(self, g):
        p = D.story("tommy_b25_cup_wait")
        k = g - G0
        p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = [0.86, self.hy.get(g, 1.28) + 0.025 * math.sin(k * 0.5)]
        p["prop_r"] = {"type": "tin_cup25", "angle": 0, "scale": 1.3}
        p["legs"] = {"preset": "stand", "crouch": 0.12}
        if k < 11:
            p["gaze"] = [0.95, 0.25]; p["yaw"] = 0.55
        else:                                                           # the deadpan stare at us
            w = C.smooth((k - 11) / 5.0)
            p["gaze"] = [round(0.95 - 0.95 * w, 2), round(0.25 - 0.25 * w, 2)]; p["yaw"] = round(0.55 - 0.45 * w, 3); p["head_roll"] = round(2 - 4 * w, 2)
        p["pitch"] = round(0.05 + 0.04 * math.sin(k * 0.35), 3)
        p["blink"] = D.blink(g, [822])
        p["light25"] = -1; p["rim25"] = 0.6
        return p

    def cam_of(self, g, P=None):
        k = g - G0
        w = C.calm((k - 9) / 12.0) if k >= 9 else 0.0
        d = 4.6 / (1.0 + 0.06 * w)
        az = self.nrm + 14.0 - 4.0 * w
        P = P or self.feet
        return D.orbit(P, az, d, 1.9, 2.3, side=0.15 * w, lx=self.lx), 40.0

    def cup_screen(self, g, feet):
        from bpy_extras.object_utils import world_to_camera_view
        A = self.anch[("tb", g)]; fx, fy = self.actors["tb"].feet[g]
        az = math.radians(self.nrm + 14.0 - 4.0 * 0 )
        right = Vector((-math.sin(az), math.cos(az), 0.0))
        cx, cy = A["tin_cup_r"]
        w = Vector(feet) + right * (cx - fx) + Vector((0, 0, fy - cy))
        v = world_to_camera_view(self.scene, self.cam, w); t = world_to_camera_view(self.scene, self.cam, self.tap_w)
        return (v.x - t.x) * 720.0, (v.y - t.y) * 1280.0, w.z - self.tap_w.z

    def setup(self, gs):
        self.hy = {}
        self.lx = 0.55
        az = math.radians(self.nrm + 14.0); self.right = Vector((-math.sin(az), math.cos(az), 0.0))
        self.fr = {g: Vector(self.feet) for g in gs}
        for it in range(3):
            for g in gs:
                cam, lens = self.cam_of(g, self.fr[g]); self.key_frame(g, cam, lens, {"tb": dict(feet=self.fr[g], pose=self.pose_of(g))}, focus=self.fr[g] + Vector((0, 0, 2.6)))
            self.pose_frames(gs)
            for g in gs:
                self.scene.frame_set(g)
                dx, dy, dz = self.cup_screen(g, self.fr[g])
                self.hy[g] = self.hy.get(g, 1.28) + (dz + 0.30)                      # cup rim ~0.3 D below the spout tip
                self.fr[g] = self.fr[g] - self.right * (dx / 314.0) * 0.9
        # camera: look at the middle between his head and the tap
        mid = (self.fr[gs[0]] + self.tap_w) * 0.5
        self.feet = Vector(self.fr[gs[0]]); self.lx = 0.55
        for g in gs:
            cam, lens = self.cam_of(g, self.fr[g]); self.key_frame(g, cam, lens, {"tb": dict(feet=self.fr[g], pose=self.pose_of(g))}, focus=self.fr[g] + Vector((0, 0, 2.6)))
        self.pose_frames(gs)
        for g in (gs[0], gs[-1]):
            self.scene.frame_set(g); print("cup-vs-spout residual g%d" % g, [round(v, 2) for v in self.cup_screen(g, self.fr[g])], flush=True)

    def on_frame(self, f):
        D.Rig.on_frame(self, f)
        k = (f - G0) % 15                                               # a bead falls from the spout every 15 frames, lands in the cup
        if k < 9:
            u = k / 8.0
            self.drip.location = self.tap_w + Vector((0, 0, -0.10 - 0.30 * u * u))
        else:
            self.drip.location = (0, 0, -50)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
