#!/usr/bin/env python3
"""shot.py -- film 11 take s02 = shot 2 (garden_hut / A), g 78..160 (+6 handles each side).
James on the stool, sleeve rolled; Jenner (scratch_arm) touches the lancet to his upper arm; a tiny red dot card appears;
James winces then is brave.  Slow push-in + small orbit.
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]    |    python3 shot.py final a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C
from mathutils import Vector
D, actors, camrig, cast11, puppet, sprites = C.D, C.actors, C.camrig, C.cast11, C.puppet, C.sprites
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
G0, G1 = C.g_bound(2.60), C.g_bound(5.37) - 1        # 78..160
H = 6
RANGE = (G0 - H, G1 + H)
PRESET, LIGHT = "garden_hut", "A"
R = Vector((0.48, 0.88, 0.0))                          # screen-right on the ground for the preset camera
JAMES = Vector((-7.66, -4.00, 0.0))                    # feet point: hip over the 3D stool (-8.0, -3.4), card 0.6 D in front of it
JEN = Vector((-8.3, -5.0, 0.0))
G_TOUCH, G_DOT = 106, 109

CAM0 = ((-1.8, -6.4, 1.55), (-8.2, -3.8, 1.65))
CAM1 = ((-3.9, -6.0, 1.6), (-8.4, -4.0, 1.7))


def cam_of(g):
    x = clamp((g - RANGE[0]) / float(RANGE[1] - RANGE[0]))
    u = 0.3 * ez(x) + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def stage_of(f):
    g = f - 1
    return 1.0 if g >= G_DOT else 0.0


def pose_james(g):
    p = dict(cast11.STORY11["james_sit_sleeve"][1])
    p["legs"] = cast11._sit("james", fx=0.32)
    wince = ez((g - G_TOUCH + 2) / 4.0) * (1.0 - ez((g - G_TOUCH - 14) / 8.0))
    p["expr"] = "worried" if wince > 0.5 else ("determined" if g > G_TOUCH else "determined")
    if wince > 0.5:
        p["sweat"] = 0.5
    brave = g > G_TOUCH + 18
    if brave:
        p["expr"] = "determined"; p["mouth"] = "smile"; p["pitch"] = -0.2
    p["head_roll"] = -4 * wince - 3 * (1 if brave else 0) + 1.0 * math.sin(g * 0.13)
    p["lean"] = 2.0 * wince + 1.0 * math.sin(g * 0.11)
    p["blink"] = blink(g, [90, 138])
    p["t"] = g / 30.0
    return p


def pose_jen(g):
    p = dict(cast11.STORY11["jenner_scratch_arm"][1])
    a = ez((g - G0 + 6) / 34.0)                                # approach / bend in
    back = ez((g - G_TOUCH - 10) / 16.0)                        # draws the lancet back
    p["lean"] = lerp(3, 11, a) - 6 * back + 0.8 * math.sin(g * 0.15)
    p["yaw"] = lerp(0.45, 0.72, a)
    p["blink"] = blink(g, [86, 128])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s02", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        self.jam = self.actors["jam"] = C.make_actor("jam", "james", sd)
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd)
        self.ov = C.sore_overlay("james", stage_of, frac=0.4, k=1.5, cuff=True)
        self.hide("vhen42")
        S_ = D.STATE
        mb, hm = D.MB(), D.MB()
        D.fg_props(mb, hm, S_["M"], S_["protos"], S_["SET"], D.R(5), dict(loc=CAM0[0], look_at=CAM0[1]),
                   [("basket", 1.9, 5.4, 0.3, 0.7), ("hay", 0.9, 4.7, 0, 0.35), ("pot", 2.8, 6.4, 0, 0.5), ("pail", 3.4, 5.0, 0.4, 0.45), ("hay", -2.2, 4.4, 0, 0.3)], hooks=False)
        for nm, m_ in (("s02_dress", mb), ("s02_dress_flora", hm)):
            o = m_.obj(nm, S_["SET"]); D.no_bounce(o)

    def pose(self, gs):
        fr = [bf(1, g) for g in gs]
        for g in gs:
            f = bf(1, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            self.jam.place(f, tuple(JAMES))
            self.jen.place(f, tuple(JEN))
        for g in gs:
            f = bf(1, g); self.scene.frame_set(f)
            self.jam.pose(f, pose_james(g), camera=self.cam)
        self.sprites_for([(self.jam, 320)], fr)
        for g in gs:
            f = bf(1, g); self.scene.frame_set(f)
            pt = actors.local_to_world(self.jam, C.sore_point("james", pose_james(g), 0.4), f, camera=self.cam)
            tt = ez((g - G0 + 6) / (G_TOUCH - G0 + 6))
            tip = Vector(pt) + Vector((0.0, 0.0, 0.0))
            ang = lerp(45, 60, ez((g - G0) / 40.0))
            back = ez((g - G_TOUCH - 10) / 16.0)
            tip = Vector(pt).lerp(Vector(pt) + Vector((-0.55, -0.25, 0.45)), back) if g > G_TOUCH else Vector(pt).lerp(Vector(pt) + Vector((-0.9, -0.3, 0.5)), 1 - tt)
            p = pose_jen(g)
            for k in ("arm_r", "prop_r"):
                p.pop(k, None)
            p["prop_r"] = dict(type="lancet", angle=ang)
            self.jen.pose(f, p, hands={"r": {"tip": tuple(tip), "prop": "lancet", "angle": ang}}, camera=self.cam)
        self.sprites_for([(self.jen, 320)], fr)

    def render_sprites_final(self, gs):
        pass

    def report(self, g):
        f = bf(1, g); self.scene.frame_set(f)
        return dict(g=g, heads=C.head_report(self, f))

    def render1(self, gs, out_dir, scale=1.0, samples=12):
        return C.Take.render(self, [bf(1, g) for g in gs], out_dir, scale=scale, samples=samples)


def sprites_with_overlay(Tk, fr):
    """re-rasterise James with the sore overlay"""
    Tk.jam.render_sprites(320, frames=fr, overlay=Tk.ov)


if __name__ == "__main__":
    cmd = sys.argv[1]
    spec = sys.argv[2]
    if cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take("preview")
        gs = [g for g in C.parse(spec) if RANGE[0] <= g <= RANGE[1]]
        Tk.pose(gs)
        sprites_with_overlay(Tk, [bf(1, g) for g in gs])
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            st = Tk.render1([g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
            print("g %d %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        def mk(q):
            T = Take(q)
            orig = T.pose
            def pose(gs):
                orig(gs); sprites_with_overlay(T, [bf(1, g) for g in gs])
            T.pose = pose
            return T
        C.final_loop(mk, [1], spec, {1: RANGE}, HERE, scale=scale, samples=samples)
