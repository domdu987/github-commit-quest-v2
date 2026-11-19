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

G0, G1 = C.g_bound(40.86), C.g_bound(42.27)       # 1226 .. 1268 (exclusive)
H = 9
GF, GL = G0 - H, G1 + H - 1
G_POP = C.cap_g("ลวดบนเสาไม้") + 8                 # the pole stands: set pole 3 on, hand-held pole props off
PRESET, LIGHT = "line_wide", "DAY"
PPD = 192
BASE = (40.7, -8.3, 0.0)                           # foot of the pole being raised (pole 3)
MIRROR = {"mor": False, "wa": False, "wb": False}

def pose_of(key, name, g):
    p = dict(cast16.STORY16[name][1]); p["mirror"] = MIRROR[key]
    if g >= G_POP:
        p.pop("prop_r", None); p.pop("prop_l", None)
    p["lean"] = p.get("lean", 0) + 2.0 * math.sin(g * 0.3 + hash(key) % 5)
    p["blink"] = blink(g, [1236 + hash(key) % 7, 1256])
    return p

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s19")
        TG.set_ladder(False, 3); TG.set_train(None)
        self.mk = dict(mor=(40.0, -7.2, 0.0), wa=(38.9, -9.4, 0.0), wb=(41.9, -5.5, 0.0))
        d = os.path.join(WORK, "sprites")
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", d, canvas=cast16.CANVAS16_POLE["morse16"] if isinstance(cast16.CANVAS16_POLE, dict) else cast16.CANVAS16_POLE, cam=self.cam)
        self.wa = self.actors["wa"] = C.make_actor("wa", "worker16_a", d, canvas=cast16.CANVAS16_POLE["worker16_a"] if isinstance(cast16.CANVAS16_POLE, dict) else cast16.CANVAS16_POLE, cam=self.cam)
        self.wb = self.actors["wb"] = C.make_actor("wb", "worker16_b", d, canvas=cast16.CANVAS16_POLE["worker16_b"] if isinstance(cast16.CANVAS16_POLE, dict) else cast16.CANVAS16_POLE, cam=self.cam)
        look0 = Vector((40.7, -7.2, 2.7))
        self.cam_path = C.CamPath(look0 + Vector(CAM_OFF), look0, GF, GL, push=0.11, slide_px=-45.0, arc_deg_s=0.0, decay=0.3, snaps=[dict(g=(G_POP - 11, G_POP + 2), k=1.5, peak=1.8, shift=(0.3, 0.1))])
        self.key_cam(bf(GF), *self.cam_path.at(GF))
        self.scene.frame_set(bf(GF))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.cam_path.at(g))
            TG.set_poles("bare", 4 if g >= G_POP else 3, frame=f)
            for k, a in (("mor", self.mor), ("wa", self.wa), ("wb", self.wb)):
                C.place(a, f, self.mk[k])
        for g in gs:
            f = bf(g); self.scene.frame_set(f)
            self.mor.pose(f, pose_of("mor", "morse_raise_pole", g), camera=self.cam)
            self.wa.pose(f, pose_of("wa", "worker_a_raise_pole", g), camera=self.cam)
            self.wb.pose(f, pose_of("wb", "worker_b_raise_pole", g), camera=self.cam)
        self.sprites_for([(self.mor, PPD), (self.wa, PPD), (self.wb, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g); self.scene.frame_set(f)
        loc, look = self.cam_path.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

CAM_OFF = (-5.3, 5.8, -0.1)

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
