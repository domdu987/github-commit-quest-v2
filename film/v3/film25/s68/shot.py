#!/usr/bin/env python3
"""s68 -- rows 68-70 FINAL CALLBACK (g 2009-2092, ends exactly on g 2092, no out-handle), STREET street_close_tail, Look A.
"และคนที่ เดินตามก้นมัน ใกล้ที่สุด ก็คือท่านนายพล": the tank rolls up the brick high street of Flers (tracks scroll, tail wheels roll); four Tommies march behind it,
cheering (varied); a slow eased PUSH (about 1.5x in scale) past them ends waist-up on the general25, marching knees-up right behind the tank's backside,
waving his little flag, cheering, sheepish.  Camera: behind-right, low; the group moves +y at V D/frame.
    python3 shot.py probe|draft|final <gspec>      post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D                                          # noqa: E402
C, F, cast25, bpy = D.C, D.F, D.C.cast25, D.bpy
from mathutils import Vector                             # noqa: E402
import tank25 as TK                                      # noqa: E402

PRESET = "street_close_tail"
G0, G1 = 2009, 2093
V = 0.06                                                 # D per frame (1.8 D/s)
PHI = 28.0                                               # view direction is rotated PHI deg left of the travel direction (+y): the group marches screen-right
TY0 = 44.0                                               # tank front y at G0
REAR = -19.8                                             # tail wheels' outer edge, tank-local x
GAP = 2.4                                                # general behind the tail wheels
GEN_X = -0.2
# Tommies: (member, x, depth behind the general, mode, phase offset)
TOM = [("tommy_c25", -1.5, 3.4, "cheer_march", 0.15), ("tommy_a25", 1.6, 4.8, "march", 0.55), ("tommy_d25", -2.0, 6.2, "wave_march", 0.8), ("tommy_b25", 2.1, 7.6, "cheer_march", 0.35)]


class Take(D.Rig):
    def __init__(self, work):
        D.Rig.__init__(self, PRESET, work, fstop=None, sun_e=12.0, sky_k=1.5, sun_left=28.0, sun_el=42.0)
        self.H = F.S["tank"]
        self.gen = self.actor("gen", "general25", contact=dict(width=1.8, depth=0.8, opacity=0.7))
        self.tm = {m: self.actor(m, m, contact=dict(width=1.4, depth=0.7, opacity=0.6)) for m, *_ in TOM}
        self.ud = Vector((-math.sin(math.radians(PHI)), math.cos(math.radians(PHI)), 0.0))       # view direction (unit, horizontal)

    def ty(self, g):
        return TY0 + V * (g - G0)

    def gen_pos(self, g):
        y = self.ty(g) + REAR - GAP
        return Vector((GEN_X, y, F.gh(GEN_X, y)))

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0)
        w = C.calm(u)
        dist = 10.4 - 5.8 * w                                  # 10.4 -> 4.6 D
        P = self.gen_pos(g)
        loc = P - self.ud * dist + Vector((0, 0, 1.45 + 0.1 * w))
        right = self.ud.cross(Vector((0, 0, 1))).normalized()
        look = P + Vector((0, 0, 2.1 + 0.2 * (1 - w))) + right * (0.15 + 0.6 * (1 - w)) + self.ud * (0.4 * (1 - w))
        return (loc, look), 34.0 + 6.0 * w

    # ------------------------------------------------------------------ acting
    def gen_pose(self, g):
        ph = (g - G0) / 24.0
        p = cast25.march_flag25(ph, facing=1, t=((g - G0) / 14.0) % 1.0)
        p = json.loads(json.dumps(p, default=list))
        u = (g - G0) / float(G1 - 1 - G0)
        p["expr"] = "excited" if u < 0.55 else "happy"
        p["mouth"] = ["open", 0.24, 0.17] if (g // 4) % 2 == 0 else ["open", 0.16, 0.10]          # cheering "huzzah"
        if u > 0.6:                                                                                # sheepish: a glance at us, a sweat drop, a blush
            p["fx"] = ["blush", "sweat"]
            w = C.smooth((u - 0.6) / 0.15)
            p["gaze"] = [round(-0.8 * w, 2), 0.0]; p["yaw"] = round(0.6 - 0.35 * w, 3)
        p["blink"] = D.blink(g, [2031, 2058, 2079])
        p["light25"] = -1; p["rim25"] = 0.6
        return p

    def tom_pose(self, m, mode, off, g):
        ph = ((g - G0) / 24.0 + off)
        p = json.loads(json.dumps(cast25.cycle(m, ph, "march"), default=list))
        a = cast25.STORY25[m + "_cheer"][1] if (m + "_cheer") in cast25.STORY25 else {}
        if mode in ("cheer_march", "wave_march"):
            for k in ("arm_r", "arm_l"):
                if k in a: p[k] = json.loads(json.dumps(a[k], default=list))
            s = math.sin(ph * 2 * math.pi * 2)
            if mode == "cheer_march":                                     # arms pump up and down
                for k in ("arm_r", "arm_l"):
                    if isinstance(p.get(k), dict) and "hand" in p[k]:
                        h = list(p[k]["hand"]); h[1] = round(h[1] + 0.18 * s * (1 if k == "arm_r" else -1), 3); p[k]["hand"] = h
        p["expr"] = "excited" if mode != "march" else "happy"
        p["mouth"] = ["open", 0.22, 0.15] if (g // 5 + int(off * 10)) % 2 == 0 else ["open", 0.14, 0.09]
        p["blink"] = D.blink(g, [2020 + int(off * 40), 2055 + int(off * 30)])
        p["light25"] = -1; p["rim25"] = 0.6
        return p

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            G = self.gen_pos(g)
            per = dict(gen=dict(feet=G, pose=self.gen_pose(g)))
            for m, x, dep, mode, off in TOM:
                rt = self.ud.cross(Vector((0, 0, 1))).normalized()
                q = G - self.ud * dep + rt * x
                per[m] = dict(feet=Vector((q.x, q.y, F.gh(q.x, q.y))), pose=self.tom_pose(m, mode, off, g), hide=((q - cam[0]).dot(self.ud) < 0.7))
            self.key_frame(g, cam, lens, per)
        self.pose_frames(gs)

    def on_frame(self, f):
        D.Rig.on_frame(self, f)
        for n, st in self._st[f].items():
            self.actors[n].card.hide_render = bool(st.get("hide"))
            if self.actors[n].proxy is not None: self.actors[n].proxy.hide_render = bool(st.get("hide"))
            if self.actors[n].contact is not None: self.actors[n].contact.hide_render = bool(st.get("hide"))
        TK.pose_on_ground(self.H, 0.0, self.ty(f), 90.0)
        TK.set_drive(self.H, V * (f - G0) + 5.0)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
