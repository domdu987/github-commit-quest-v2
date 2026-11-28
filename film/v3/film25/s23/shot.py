#!/usr/bin/env python3
"""s23 -- row 23 GAG "ข้าจะเดินตามก้นมัน" (g 676-711), TRIAL, Look A.  IMAGINED gag: the Mark I rolls across the park (tracks scroll, tail wheels turn) with a bum-wiggle
(its yaw sways), the general marches knees-up right behind its backside, waving the little plain flag, mouth open in a cheer (no lip-sync).  FOLLOW pan (camera
travels with the pair, leading); warm, slightly brighter grade (post wb/gamma); a long grey-olive plate wall 6 D behind the path catches both cast shadows.
    python3 shot.py probe|draft|final <gspec>      post: python3 ../s21/post_d.py . <gspec>   (finish.py passes the warm grade for this take)"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D                                          # noqa: E402
C, F, cast25, bpy = D.C, D.F, D.C.cast25, D.bpy
from mathutils import Vector                             # noqa: E402
import tank25 as TK                                      # noqa: E402

PRESET = "trial_close_general"
G0, G1 = 676, 712
V = 0.10                                                 # D / frame (3 D/s: the camera pans about 24 % of the width per second)
YAW = 90.0                                               # tank heading (deg): north, along the free lawn west of the trench
REAR, GAP = -19.8, 1.3
WALL_D = 6.5
PHI = 14.0                                               # view direction: PHI deg left of the travel direction (the pair marches screen-right and away)


class Take(D.Rig):
    def __init__(self, work):
        D.Rig.__init__(self, PRESET, work, fstop=None, sun_e=11.0, sky_k=1.2, sun_left=-32.0, sun_el=28.0)
        self.H = F.S["tank"]
        self.gen = self.actor("gen", "general25", contact=dict(width=1.8, depth=0.8, opacity=0.7))
        a = math.radians(YAW)
        self.ud = Vector((-math.sin(math.radians(PHI)), math.cos(math.radians(PHI)), 0.0))
        self.dirv = Vector((math.cos(a), math.sin(a), 0.0)); self.nrm = Vector((math.sin(a), -math.cos(a), 0.0))      # nrm: toward the camera side (right of travel)
        self.x0 = Vector((-14.0, -8.0, 0.0))
        c = self.x0 - self.nrm * 5.2 + self.dirv * -6.0                          # wall parallel to the path, 5 D left of the tank axis: a plain backdrop that catches the shadows
        self.wall = D.add_wall("wall", (c.x, c.y), math.degrees(math.atan2(self.nrm.y, self.nrm.x)), 64.0, 7.0, D.plate_material("wall_m", (0.36, 0.40, 0.33)))

    def tank_pos(self, g):
        p = self.x0 + self.dirv * (V * (g - G0))
        return p

    def gen_pos(self, g):
        p = self.tank_pos(g) + self.dirv * (REAR - GAP) + self.nrm * 0.0
        p.z = F.gh(p.x, p.y)
        return p

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0)
        w = C.calm(u)
        P = self.gen_pos(g)
        dist = 5.0 - 0.7 * w
        loc = P - self.ud * dist + Vector((0, 0, 0.9))
        right = self.ud.cross(Vector((0, 0, 1))).normalized()
        look = P + Vector((0, 0, 2.7)) + right * 0.2 + self.ud * 1.0
        return (loc, look), 30.0

    def gen_pose(self, g):
        ph = (g - G0) / 24.0
        p = json.loads(json.dumps(cast25.march_flag25(ph, facing=1, t=((g - G0) / 12.0) % 1.0), default=list))
        p["expr"] = "excited"
        p["mouth"] = ["open", 0.24, 0.17] if (g // 3) % 2 == 0 else ["open", 0.17, 0.11]
        p["yaw"] = 0.45 + 0.12 * math.sin((g - G0) * 0.5)
        p["blink"] = D.blink(g, [690, 704])
        p["light25"] = 1; p["rim25"] = 0.6
        return p

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            self.key_frame(g, cam, lens, dict(gen=dict(feet=self.gen_pos(g), pose=self.gen_pose(g))))
        self.pose_frames(gs)

    def on_frame(self, f):
        D.Rig.on_frame(self, f)
        p = self.tank_pos(f)
        wig = 2.2 * math.sin((f - G0) * 2 * math.pi / 12.0)                        # the bum wiggle: the heading sways +-2.2 deg every 12 frames
        TK.pose_on_ground(self.H, p.x, p.y, YAW + wig)
        TK.set_drive(self.H, V * (f - G0) + 3.0)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
