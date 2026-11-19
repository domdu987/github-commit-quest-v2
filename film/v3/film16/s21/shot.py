#!/usr/bin/env python3
"""shot.py -- film 16 take s21 = shot 21 (44.87-46.02 s): LINE line_trench_end / RAIN.  Morse crouched at the test key on the crate
presses: nothing (the lever goes down twice, no spark, no click); Cornell holds his slouch hat over him; a worker waits, arms folded.
Rain streaks (thin), dark puddle.  Shot g 1346..1380; handles 9 each side (hard cut in, dissolve out into shot 22): first_g 1337, 53 frames.
    python3 shot.py probe|stills a:b[:step] [out scale samples]  /  python3 shot.py camreport  /  python3 shot.py final a:b[:step] [scale samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c16 as C
from mathutils import Vector, Matrix, Euler
TG, K, LN, actors, cast16 = C.TG, C.K, C.LN, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(44.87), C.g_bound(46.02)       # 1346 .. 1381 (exclusive)
H = 9
GF, GL = G0 - H, G1 + H - 1
G_WORD = C.cap_g("ข่าวไปไม่ถึงไหน")                  # 1350: first press lands on the word
PRESS = [(G_WORD + 2, G_WORD + 8), (G_WORD + 17, G_WORD + 23)]      # two presses, nothing happens
PRESET, LIGHT = "line_trench_end", "RAIN"
PPD = 256

def key_knob():
    kx, ky = LN.KEYCRATE
    loc = Matrix.Rotation(0.5, 3, "Z") @ (Vector((0.31, -0.2, 0.76)) * 1.6)     # key_station(sc=1.6, yaw 0.5) on the 1.8 D crate: knob z 2.25
    return Vector(K.W((kx + loc.x, ky + loc.y, loc.z)))

def press_u(g):
    v = 0.0
    for a, b in PRESS:
        if a <= g <= b:
            u = (g - a) / float(b - a)
            v = max(v, math.sin(math.pi * u))
    return v

MIRROR = {"mor": False, "cor": False, "wa": False}

def morse_pose(g):
    p = dict(cast16.STORY16["morse_key_wait"][1]); p.pop("prop_r", None)
    p["key_press"] = 0.0
    p["lean"] = p.get("lean", 0) + 4 * press_u(g) + 1.2 * math.sin(g * 0.2)
    p["expr"] = "worried" if g < G_WORD + 10 else "sad"
    p["gaze"] = (0.9, 0.4) if g < G_WORD + 16 else (0.3, -0.5)
    p["yaw"] = 0.7
    p["blink"] = blink(g, [G_WORD + 12])
    p["mirror"] = MIRROR["mor"]
    return p

def cornell_pose(g):
    p = dict(cast16.STORY16["cornell_hat_over"][1]); p["mirror"] = MIRROR["cor"]
    p["head_roll"] = -5 + 1.5 * math.sin(g * 0.17)
    p["gaze"] = (0.9, 0.7)
    return p

def worker_pose(g):
    p = dict(cast16.STORY16["worker_a_wait_arms"][1]); p["mirror"] = MIRROR["wa"]
    p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.13 + 1)
    p["blink"] = blink(g, [G_WORD + 20])
    p["gaze"] = (0.9, 0.3)
    return p

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s21")
        C.rain_look(self, bead_k=None)
        for ob in C.bpy.data.objects:
            if ob.name.startswith(('fg_wheat', 'fg_verge')):
                ob.hide_render = True            # dark foreground grass over the lower third
        M = self.A["marks"]
        self.mk = dict(mor=(120.3, -8.9, 0.0), cor=(121.4, -9.2, 0.0), wa=(122.4, -9.9, 0.0))
        d = os.path.join(WORK, "sprites")
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", d, contact=True, cam=self.cam)
        self.cor = self.actors["cor"] = C.make_actor("cor", "cornell", d, contact=True, cam=self.cam)
        self.wa = self.actors["wa"] = C.make_actor("wa", "worker16_a", d, contact=True, cam=self.cam)
        m = Vector(self.mk["mor"])
        look0 = Vector((120.8, -9.0, 2.5))
        self.cam_path = C.CamPath(look0 + Vector((0.3, 5.4, 1.3)), look0, GF, GL, push=0.08, slide_px=-10.0, decay=0.3, snaps=[dict(g=(G_WORD - 2, G_WORD + 11), k=1.6, peak=2.0, shift=(0.0, 0.0))])
        self.key_cam(bf(GF), *self.cam_path.at(GF))
        self.scene.frame_set(bf(GF))
        if os.environ.get('NOACT'):
            for a in self.actors.values():
                a.card.hide_render = True

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.cam_path.at(g))
            TG.set_rain(0.55, frame=f)
            for k, a in (("mor", self.mor), ("cor", self.cor), ("wa", self.wa)):
                C.place(a, f, self.mk[k])
        for g in gs:
            f = bf(g); self.scene.frame_set(f)
            kn = key_knob(); kn.z -= 0.14 * press_u(g)
            _, inf = self.mor.pose(f, morse_pose(g), hands={"r": {"hand": tuple(kn)}}, camera=self.cam); self.herr = inf
            self.cor.pose(f, cornell_pose(g), camera=self.cam)
            self.wa.pose(f, worker_pose(g), camera=self.cam)
        self.sprites_for([(self.mor, PPD), (self.cor, PPD), (self.wa, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g); self.scene.frame_set(f)
        loc, look = self.cam_path.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), press=round(press_u(g), 2), herr={k: v.get("error") for k, v in getattr(self, "herr", {}).items()})

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if GF <= g <= GL]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
