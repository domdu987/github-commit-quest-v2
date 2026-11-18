#!/usr/bin/env python3
"""shot.py -- film 13 take s04: shots 4, 5, 6 (RAIN, street): pivot (g 162..236), mud_low (237..302), rain_street (303..366);
in-handle g 156..161 (shot 4 continues backwards), out-handle g 367..372 (shot 6 continues).
One build (street, RAIN, lift 0, fill 0), custom cameras per shot (NO DOF), cast13 actors + cast13 crowd cards.
    python3 shot.py stills a:b[:step] out [scale] [samples]   |   python3 shot.py final a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c13 as C
import fx13
from mathutils import Vector
B, STATE, lerp, clamp, ez, bf = C.B, C.B.STATE, C.lerp, C.clamp, C.ez, C.bf
cast13 = C.cast13
LIGHT, PRESET, BSTATE = "RAIN", "street_wide", "lift0,fill0,sink0.1,rain1"
G0, G1 = 156, 372
SH = {4: (162, 236), 5: (237, 302), 6: (303, 366)}
SPRITES = os.path.join(HERE, "work", "sprites")

def shot_of(g):
    for s, (a, b) in SH.items():
        if a <= g <= b: return s
    return 4 if g < 162 else 6

# ---- cameras: (loc, look, lens) start/end per shot; u = (g - a) / (b - a) over the shot's own range (handles extrapolate)
CAMS = {4: (((-14, -40, 46), (0, 4, 43), 22), ((-30, -58, 3.4), (-6, -14, 7), 22)),
        5: (((-29, -46.5, 1.5), (-22.0, -37.5, 2.4), 22), ((-26.5, -45.0, 1.4), (-20.8, -37.5, 2.2), 22)),
        6: (((-9, -27, 2.3), (-10.5, -21, 2.4), 22), ((-6.5, -19.5, 2.0), (-3, -14.2, 2.1), 22))}
def cam_of(g):
    s = shot_of(g); a, b = SH[s]; u = (g - a) / float(b - a)
    u = 0.3 * ez(clamp(u)) + 0.7 * u
    (l0, k0, n0), (l1, k1, n1) = CAMS[s]
    return [lerp(l0[i], l1[i], u) for i in range(3)], [lerp(k0[i], k1[i], u) for i in range(3)], lerp(n0, n1, u)

def gz(x, y, plank=False):
    z = float(STATE["mud_z"](__import__("numpy").array([x]), __import__("numpy").array([y]))[0])
    return z + (0.3 if plank else 0.0) + STATE.get("fill", 0.0) * B.FILL_MAX

# ---- walkers
def walker(cast, pose_name, p0, p1, g0, g1, facing=1, plank=True, speed=0.9):
    """returns f(g) -> (xy, pose, visible)"""
    S = cast13.STORY13[pose_name][1]
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    def f(g):
        u = (g - g0) / float(g1 - g0)
        xy = (lerp(p0[0], p1[0], clamp(u)), lerp(p0[1], p1[1], clamp(u)))
        ph = u * L / 2.0
        base = dict(S); base.pop("legs", None); base.pop("yaw", None)
        pose = cast13.cycle(cast, ph, "walk", facing=facing, base=base, speed=speed)
        pose["blink"] = C.blink(g, [g0 + 17, g0 + 55]); pose["t"] = g / 30.0
        return xy, pose, (g0 - 1 <= g <= g1 + 1)
    return f

class Track(object):
    def __init__(self, name, cast, fn, ppd=192, plank=True, z_extra=None, shots=None):
        self.name, self.cast, self.fn, self.ppd, self.plank, self.z_extra, self.shots = name, cast, fn, ppd, plank, z_extra, shots

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, state=BSTATE, quality=quality, name="cam_s04")
        self.tracks = []
        import bpy
        self.horse = bpy.data.objects["cartA_horse"]
        self.crowd_objs = []
        fx13.tame_puddles(B, rain=True)
        spots = fx13.puddle_spots(B)
        self.ripples = fx13.Ripples(spots, n=16, life=26, seed=3, rmax=0.8)
        self.crowns = [fx13.Crown(B, 10, "fx_c%d" % i) for i in range(4)]
        W = lambda *a, **k: walker(*a, **k)
        # shot 4: far walkers on the plank walk (away from camera it reads small)
        self.add("t4a", "town_a", W("town_a", "town_stand_a", (-12, -22), (0, -11), 150, 250, 1), ppd=128, shots=(4,))
        self.add("t4b", "worker13_a", W("worker13_a", "worker_stand_a", (0, -11), (-12, -22), 150, 250, -1), ppd=128, shots=(4,))
        # shot 5: worker at the stuck cart, townsfolk crossing behind
        S = cast13.STORY13
        self.add("w5", "worker13_b", self._still("worker13_b", "worker_stand_b", (-19.8, -42.0), (-22, -34), 237, 302, 5), ppd=256, plank=True, shots=(5,))
        # shot 6: townsfolk hop along the planks, the gentleman steps off and sinks
        self.add("g6", "gentleman13", self._gent((-12.5, -22.5), (0.5, -11.2), 296, 345), ppd=224, shots=(6,))
        self.add("b6", "town_b", W("town_b", "town_stand_b", (-5.5, -16.0), (1.5, -10.5), 322, 372, 1), ppd=224, shots=(6,))
        self.add("c6", "town_c", W("town_c", "town_stand_c", (0.5, -11.3), (-12.5, -22.8), 296, 372, -1), ppd=224, shots=())

    def add(self, name, cast, fn, ppd=192, plank=True, shots=None):
        a = C.make_actor(name, cast, SPRITES)
        self.actors[name] = a
        self.tracks.append(Track(name, cast, fn, ppd, plank, None, shots))

    def _still(self, cast, pose_name, p0, p1, g0, g1, shot):
        S = dict(cast13.STORY13[pose_name][1])
        def f(g):
            u = clamp((g - g0) / float(g1 - g0))
            xy = (lerp(p0[0], p1[0], 0.0), p0[1])
            p = dict(S); p["yaw"] = 0.5; p["lean"] = 2 * math.sin(g * 0.1); p["head_roll"] = 3 * math.sin(g * 0.07)
            p["blink"] = C.blink(g, [g0 + 20, g0 + 50]); p["t"] = g / 30.0
            return xy, p, True
        return f

    def _gent(self, p0, p1, g0, g1):
        """gentleman hops along the plank; at the end of the walk one boot misses the plank and sinks (comic), pulls up."""
        S = cast13.STORY13["gentleman_stand"][1]
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1]); gs = 335
        def f(g):
            u = clamp((g - g0) / float(g1 - g0))
            if g < gs: xy = (lerp(p0[0], p1[0], clamp((g - g0) / float(gs - g0) * 0.75)), lerp(p0[1], p1[1], clamp((g - g0) / float(gs - g0) * 0.75)))
            else: xy = (lerp(p0[0], p1[0], 0.75), lerp(p0[1], p1[1], 0.75))
            base = dict(S); base.pop("legs", None); base.pop("yaw", None)
            ph = clamp((g - g0) / float(gs - g0)) * L * 0.75 / 2.0
            if g < gs: p = cast13.cycle("gentleman13", ph, "walk", facing=1, base=base, speed=0.9)
            else:
                k = ez((g - gs) / 8.0); p = dict(S); p["yaw"] = 0.5; p["legs"] = dict(stride=0.4, lift_r=0.0, lift_l=0.0, crouch=0.25 * k, knee_r=0.2, knee_l=0.2)
                p["lean"] = -10.0 * k; p["expr"] = "surprised"; p["mud"] = 0.4 * k; p["arm_r"] = dict(hand=(0.9, 0.1), bend=0.3); p["arm_l"] = dict(hand=(-0.9, 0.2), bend=0.3)
            p["blink"] = C.blink(g, [g0 + 15]); p["t"] = g / 30.0
            return xy, p, True
        return f

    def _ground(self, tr, xy, g):
        z = gz(xy[0], xy[1], tr.plank)
        if tr.name == "g6" and g >= 335: z -= 0.55 * ez((g - 335) / 8.0) * (1 - 0.7 * ez((g - 352) / 10.0))
        return z

    def pose(self, gs):
        self.scene.camera = self.cam
        # crowd cards (placed once, camera-aware at three cam positions)
        if not self.crowd_objs:
            self.crowd_shot = {}
            for g_, n, reg, seed in ((170, 7, [(-34, 34, -34, -14)], 6), (225, 7, [(-34, 34, -40, -14)], 16), (262, 4, [(-30, 4, -34, -20)], 13), (330, 3, [(-20, -14, -34, -26), (6, 20, -34, -26)], 26)):
                loc, look, ln = cam_of(g_)
                C.look_at_cam(self.cam, loc, look); self.cam.data.lens = ln
                reg2 = reg
                objs = B.crowd_view(n * 3, reg2, self.cam, seed=seed, ground=B._gnd(), min_dist=3.4)
                keep = []
                for ob in objs:
                    d = (ob.location - Vector(loc)).length
                    if d < (12 if shot_of(g_) != 6 else 14) or len(keep) >= n: ob.hide_render = True; ob.hide_viewport = True
                    else: keep.append(ob)
                for ob in keep: self.crowd_shot[ob.name] = shot_of(g_)
                self.crowd_objs += keep
        for g in gs:
            f = bf(1, g)
            loc, look, ln = cam_of(g)
            self.key_cam(f, loc, look, lens=ln)
            B.set_fill(0.0, frame=f); B.set_lift(0.0, frame=f)
            s = shot_of(g)
            B.set_wheel_sink(0.12 + 0.75 * ez((g - 230) / 70.0), frame=f)
            B.set_rain(1.0, frame=f)
            for ob in self.crowd_objs:
                ob.hide_render = (self.crowd_shot[ob.name] != s); ob.keyframe_insert("hide_render", frame=f)
            hz = STATE["cartA"][0]
            hh = self.horse
            hh.location.z = STATE.get("fill", 0.0) * B.FILL_MAX + (0.10 * math.sin(g * 0.45) + 0.07 * math.sin(g * 0.9)) * (1 if s == 5 else 0.3)
            hh.location.x = 0.06 * math.sin(g * 0.37)
            hh.keyframe_insert("location", index=2, frame=f); hh.keyframe_insert("location", index=0, frame=f)
            # straining: rear up / pitch about the hooves (pivot -15,-34)
            k = 1.0 if s == 5 else 0.35
            pitch = k * (math.radians(4.5) * math.sin(g * 0.33) + math.radians(2.5) * math.sin(g * 0.71)) - k * math.radians(2.0)
            roll = k * math.radians(1.6) * math.sin(g * 0.52)
            hh.rotation_euler = (roll, pitch, 0)
            px, py = -15.0, -34.0
            c, sn = math.cos(pitch), math.sin(pitch)
            hh.location.x += px - (c * px); hh.location.z += (sn * px)
            hh.keyframe_insert("location", frame=f); hh.keyframe_insert("rotation_euler", frame=f)
            self.ripples.key(f)
            wz = 1.4 - 0.9 * STATE.get("sink", 0.0)
            wsink = 0.12 + 0.75 * ez((g - 230) / 70.0)
            plays = ((0, 243, (-24.0, -39.4, 0.0), 1.1), (1, 262, (-15.4, -34.6, 0.0), 0.8), (2, 281, (-24.0, -39.4, 0.0), 1.3))
            for i, cr in enumerate(self.crowns[:3]):
                _, f0, pos, sz = plays[i]; cr.play(f, bf(1, f0), pos, sz, life=20, seed=i + 5)
            gp = (-2.75, -14.03, gz(-2.75, -14.03, True) - 0.15)
            for k2, f0 in enumerate((337, 350)):
                self.crowns[3].play(f, bf(1, f0), gp, 1.1, life=18, seed=11 + k2) if (f >= bf(1, f0) and f <= bf(1, f0) + 18) else None
            if not (bf(1, 337) <= f <= bf(1, 337) + 18 or bf(1, 350) <= f <= bf(1, 350) + 18): self.crowns[3].play(f, bf(1, 9999), gp, 1.0)
            for tr in self.tracks:
                a = self.actors[tr.name]
                xy, p, vis = tr.fn(g)
                show = vis and (tr.shots is None or s in tr.shots)
                C.place(a, f, xy, self._ground(tr, xy, g))
        for g in gs:
            f = bf(1, g); self.scene.frame_set(f)
            for tr in self.tracks:
                xy, p, vis = tr.fn(g)
                self.actors[tr.name].pose(f, p, camera=self.cam)
        for tr in self.tracks:
            fr = [bf(1, g) for g in gs if (tr.shots is None or shot_of(g) in tr.shots)]
            if fr: self.sprites_for([(self.actors[tr.name], tr.ppd)], fr)

    def report(self, g):
        f = bf(1, g); self.scene.frame_set(f)
        loc, look, ln = cam_of(g)
        return dict(g=g, shot=shot_of(g), cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))

    def show(self, tr, g):
        xy, p, vis = tr.fn(g)
        return vis and (tr.shots is None or shot_of(g) in tr.shots)

    def render(self, g, out_dir, scale=1.0, samples=12, threads=2):
        for tr in self.tracks:
            self.actors[tr.name].set_hidden(not self.show(tr, g))
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
