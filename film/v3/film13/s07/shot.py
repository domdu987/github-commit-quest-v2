#!/usr/bin/env python3
"""shot.py -- film 13 take s07: shots 7, 8, 9 (DAY, street): setup g 367..446 (filling the street), 447..512 (front stair: fill mound vs door),
513..593 (pullman with plans); in-handle g 361..366 (shot 7 backwards), out-handle g 594..599 (shot 9 continues).
One build (street, DAY, lift 0), custom cameras per shot (NO DOF), cast13 actors + cast13 crowd cards.
    python3 shot.py stills a:b[:step] out [scale] [samples]   |   python3 shot.py final a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c13 as C
import bpy
from mathutils import Vector
import numpy as np
B, STATE, lerp, clamp, ez, bf = C.B, C.B.STATE, C.lerp, C.clamp, C.ez, C.bf
cast13, puppet = C.cast13, C.puppet
LIGHT, PRESET, BSTATE = "DAY", "street_wide", "lift0,fill0.05,mound0"
G0, G1 = 361, 599
SH = {7: (367, 446), 8: (447, 512), 9: (513, 593)}
SPRITES = os.path.join(HERE, "work", "sprites")

def shot_of(g):
    for s, (a, b) in SH.items():
        if a <= g <= b: return s
    return 7 if g < 367 else 9

CAMS = {7: (((-6, -32, 2.8), (-36, -17, 4.5), 22), ((-4, -30, 3.0), (-8, -9, 6.5), 22)),
        8: (((-5, -26, 2.6), (4, -8, 4.5), 22), ((0, -22, 2.8), (7, -8, 4.6), 22)),
        9: (((-12, -31, 2.5), (-8, -12, 8.5), 22), ((-9, -27, 2.5), (-6, -12, 8.0), 22))}
def cam_of(g):
    s = shot_of(g); a, b = SH[s]; u = (g - a) / float(b - a)
    u = 0.3 * ez(clamp(u)) + 0.7 * u
    (l0, k0, n0), (l1, k1, n1) = CAMS[s]
    return [lerp(l0[i], l1[i], u) for i in range(3)], [lerp(k0[i], k1[i], u) for i in range(3)], lerp(n0, n1, u)

def fill_of(g):
    return lerp(0.05, 0.15, clamp((g - 367) / 140.0))
def mound_of(g):
    return lerp(0.25, 0.85, ez((g - 447) / 66.0)) if g >= 447 else (0.25 if g >= 380 else 0.0)

def gz(x, y, plank=False, fill=None):
    z = float(STATE["mud_z"](np.array([x]), np.array([y]))[0])
    return z + (0.3 if plank else 0.0) + (fill if fill is not None else STATE.get("fill", 0.0)) * B.FILL_MAX

class Track(object):
    def __init__(self, name, cast, fn, ppd, plank, shots):
        self.name, self.cast, self.fn, self.ppd, self.plank, self.shots = name, cast, fn, ppd, plank, shots

def digger(cast, pose_name, xy, ph0, facing=1, yaw=0.6):
    S = dict(cast13.STORY13[pose_name][1])
    def f(g):
        s = math.sin((g + ph0) * 0.32)
        p = dict(S); p["yaw"] = yaw; p["expr"] = "determined"; p["mouth"] = "flat"
        p["lean"] = 9 + 8 * s
        p["arm_r"] = dict(hand=(0.5 + 0.15 * s, 1.25 - 0.45 * s), bend=0.3, stretch=1.0)
        p["arm_l"] = dict(hand=(0.2, 1.15 - 0.4 * s), bend=0.3)
        p["prop_r"] = dict(type="jack_bar", angle=-62 + 18 * s)
        p["legs"] = dict(stride=0.25, crouch=0.10 + 0.05 * (1 - s))
        p["blink"] = C.blink(g, [ph0 + 30, ph0 + 90]); p["t"] = g / 30.0
        if facing < 0: p["mirror"] = True
        return xy, p, True
    return f

def walker(cast, pose_name, p0, p1, g0, g1, facing=1, speed=0.9, prop=None):
    S = dict(cast13.STORY13[pose_name][1])
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    def f(g):
        u = clamp((g - g0) / float(g1 - g0))
        xy = (lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u))
        base = dict(S); base.pop("legs", None); base.pop("yaw", None)
        if prop: base["prop_r"] = prop; base["arm_r"] = "down"
        pose = cast13.cycle(cast, u * L / 2.0, "walk", facing=facing, base=base, speed=speed)
        pose["blink"] = C.blink(g, [g0 + 17]); pose["t"] = g / 30.0
        return xy, pose, True
    return f

def pullman_fn():
    walk = dict(cast13.STORY13["pullman_point_plan"][1])
    up = cast13.STORY13["pullman_look_up_confident"][1]
    nod = cast13.STORY13["pullman_nod_smile"][1]
    P0, P1 = (-13.5, -14.0), (-3.5, -14.0)
    GW, GU, GN = 512, 548, 566
    def f(g):
        u = clamp((g - GW) / float(GW + 38 - GW))
        xy = (lerp(P0[0], P1[0], clamp((g - GW) / 38.0)), lerp(P0[1], P1[1], clamp((g - GW) / 38.0)))
        if g < GU:
            base = dict(walk); base.pop("legs", None); base.pop("yaw", None); base["arm_l"] = "akimbo"
            p = cast13.cycle("pullman", (g - GW) * 0.5 / 14.0, "walk", facing=1, base=base, speed=0.85)
        else:
            k = ez((g - GU) / 10.0); p = puppet.lerp_pose("pullman", cast13.STORY13["pullman_point_plan"][1], up, k)
            p["pitch"] = lerp(-0.15, -0.75, k) + 0.04 * math.sin(g * 0.2)
            if g >= GN:
                nn = math.sin((g - GN) * 0.33)                                   # confident nod: down and up twice
                p["pitch"] = lerp(-0.75, 0.2, ez((g - GN) / 6.0)) - 0.35 * max(0.0, math.sin((g - GN - 6) * 0.33)) * -1 if False else -0.35 + 0.45 * max(0.0, nn) - 0.05
                p["expr"] = "smirk"
        p["blink"] = C.blink(g, [530, 575]); p["t"] = g / 30.0
        return xy, p, True
    return f

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, state=BSTATE, quality=quality, name="cam_s07")
        self.tracks, self.crowd_objs = [], []
        # shot 7: diggers at the fill piles, a wheelbarrow walker, townsfolk
        self.add("d7a", "worker13_a", digger("worker13_a", "worker_stand_a", (-17.0, -22.0), 0), 128, False, (7,))
        self.add("d7b", "worker13_b", digger("worker13_b", "worker_stand_b", (-21.5, -23.5), 9), 128, False, (7,))
        self.add("d7c", "worker13_c", digger("worker13_c", "worker_stand_c", (-26.0, -22.0), 4), 128, False, (7,))
        self.add("f7", "foreman13", walker("foreman13", "foreman_stand", (-27, -28), (-33, -28.5), 362, 450, -1, 0.7), 128, False, (7,))
        # shot 8: foreman at the stair foot, two diggers on the mound
        self.add("f8", "foreman13", walker("foreman13", "foreman_stand", (-4.5, -10.5), (-1.5, -10.5), 440, 515, 1, 0.5), 224, False, (8,))
        self.add("w8a", "worker13_a", digger("worker13_a", "worker_stand_a", (8.0, -15.0), 3, -1), 224, False, (8,))
        self.add("w8b", "worker13_b", digger("worker13_b", "worker_stand_b", (13.0, -15.0), 11, -1), 224, False, (8,))
        # shot 9: pullman + two bystanders
        self.add("pul", "pullman", pullman_fn(), 192, False, (9,))
        self.add("w9", "worker13_c", digger("worker13_c", "worker_stand_c", (-16.0, -20.0), 6), 160, False, (9,))
        self.horse = None

    def add(self, name, cast, fn, ppd, plank, shots):
        a = C.make_actor(name, cast, SPRITES)
        self.actors[name] = a
        self.tracks.append(Track(name, cast, fn, ppd, plank, shots))

    def _z(self, tr, xy, g):
        return gz(xy[0], xy[1], tr.plank, fill_of(g))

    def pose(self, gs):
        self.scene.camera = self.cam
        if not self.crowd_objs:
            self.crowd_shot = {}
            for g_, n, reg, seed in ((372, 6, [(-34, 34, -34, -14)], 6), (440, 4, [(-10, 34, -34, -14)], 16), (480, 4, [(-30, 34, -30, -18)], 13), (560, 2, [(-30, 20, -30, -20)], 26)):
                loc, look, ln = cam_of(g_)
                C.look_at_cam(self.cam, loc, look); self.cam.data.lens = ln
                objs = B.crowd_view(n * 3, reg, self.cam, seed=seed, ground=B._gnd(), min_dist=3.4)
                keep = []
                for ob in objs:
                    d = (ob.location - Vector(loc)).length
                    if d < (17 if shot_of(g_) == 9 else 13) or len(keep) >= n: ob.hide_render = True; ob.hide_viewport = True
                    else: keep.append(ob)
                for ob in keep:
                    self.crowd_shot[ob.name] = shot_of(g_); ob["base_z"] = ob.location.z
                self.crowd_objs += keep
        for g in gs:
            f = bf(1, g)
            loc, look, ln = cam_of(g)
            self.key_cam(f, loc, look, lens=ln)
            B.set_fill(fill_of(g), frame=f); B.set_lift(0.0, frame=f); B.set_mound(mound_of(g), frame=f)
            s = shot_of(g)
            for ob in self.crowd_objs:
                ob.hide_render = (self.crowd_shot[ob.name] != s); ob.keyframe_insert("hide_render", frame=f)
                ob.location.z = ob["base_z"] + fill_of(g) * B.FILL_MAX; ob.keyframe_insert("location", index=2, frame=f)
            for tr in self.tracks:
                xy, p, vis = tr.fn(g)
                C.place(self.actors[tr.name], f, xy, self._z(tr, xy, g))
        for g in gs:
            f = bf(1, g); self.scene.frame_set(f)
            for tr in self.tracks:
                if shot_of(g) in tr.shots:
                    xy, p, vis = tr.fn(g)
                    self.actors[tr.name].pose(f, p, camera=self.cam)
        for tr in self.tracks:
            fr = [bf(1, g) for g in gs if shot_of(g) in tr.shots]
            if fr: self.sprites_for([(self.actors[tr.name], tr.ppd)], fr)

    def report(self, g):
        f = bf(1, g); self.scene.frame_set(f)
        loc, look, ln = cam_of(g)
        return dict(g=g, shot=shot_of(g), cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))

    def render(self, g, out_dir, scale=1.0, samples=12, threads=2):
        for tr in self.tracks:
            self.actors[tr.name].set_hidden(shot_of(g) not in tr.shots)
        return C.Take.render(self, [bf(1, g)], out_dir, scale=scale, samples=samples, threads=threads)[0]

if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    if cmd == "stills":
        out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            st = Tk.render(g, out, scale=scale, samples=samples)
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print(json.dumps(Tk.report(g)), "%.1fs" % st["wall"], flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        Tk = Take("final"); C.final_loop(Tk, shot_of, gs, HERE, scale=scale, samples=samples)
