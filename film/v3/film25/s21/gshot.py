#!/usr/bin/env python3
"""gshot.py -- base class for the general25 waist-up shots (rows 19, 20, 24, 43, 44): a close_cam mark, a near plate wall ND D behind him, mild DOF, orbit camera."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import d25 as D
C, F, cast25 = D.C, D.F, D.C.cast25
from mathutils import Vector


class GeneralClose(D.Rig):
    PRESET = "trial_close_general"
    G0, G1 = 0, 1
    ND, WALL_H, WALL_W = 2.0, 4.1, 14.0
    WALL_AZ = 18.0                                       # wall faces the camera at azimuth f0 + WALL_AZ
    WALL_COL = (0.36, 0.40, 0.33)
    FSTOP = 2.0
    KW = {}
    HIDE = ()

    def __init__(self, work):
        D.Rig.__init__(self, self.PRESET, work, fstop=self.FSTOP, **self.KW)
        import bpy
        for o in bpy.data.objects:
            if o.name in self.HIDE:
                o.hide_render = True; o.hide_viewport = True
        self.gen = self.actor("gen", "general25", contact=dict(width=1.6, depth=0.8, opacity=0.7))
        m = F.S["mark"]; self.P = Vector(m["pos"]); self.f0 = m["face_deg"]; self.P.z = F.gh(self.P.x, self.P.y)
        azc = self.f0 + self.WALL_AZ
        self.wall = D.add_wall("wall", (self.P.x - math.cos(math.radians(azc)) * self.ND, self.P.y - math.sin(math.radians(azc)) * self.ND), azc, self.WALL_W, self.WALL_H + 1.0, D.plate_material("wall_m", self.WALL_COL), z0=self.P.z - 1.0)

    def feet(self, g):
        return self.P

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            self.key_frame(g, cam, lens, dict(gen=dict(feet=self.feet(g), pose=self.pose_of(g))), focus=self.feet(g) + Vector((0, 0, 2.7)))
        self.pose_frames(gs)
