#!/usr/bin/env python3
"""shot.py -- film 16 take s20 = shot 20 (42.27-44.87 s): LINE line_close / RAIN.  Bare poles, rain pours, the wet pole darkens and
small blue sparks crawl down the wood into the puddle.  No cast.  Camera tilts down the hero pole following the sparks.
Frames: shot g 1268..1345, 9-frame handles each side (hard cut in/out): first_g 1259, 96 frames.
    python3 shot.py probe|stills a:b[:step] [out scale samples]   /   python3 shot.py camreport   /   python3 shot.py final a:b[:step] [scale samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c16 as C
from mathutils import Vector
TG, K, LN = C.TG, C.K, C.LN
lerp, clamp, ez, u_of, bf = C.lerp, C.clamp, C.ez, C.u_of, C.bf

G0, G1 = C.g_bound(42.27), C.g_bound(44.87)      # 1268, 1346 (exclusive)
H = 9
GF, GL = G0 - H, G1 + H - 1                       # 1259 .. 1354
GS = list(range(GF, GL + 1))
G_WORD = C.cap_g("ไฟรั่วลงดินหมด")                 # 1319 -> snap
SNAP = (G_WORD - 3, G_WORD + 12)
PRESET, LIGHT = "line_close", "RAIN"
POLE = 1

def pole_pt(z):
    px = LN.px(LN.POLES_Y[POLE]) + 0.03
    return Vector(K.W((px, LN.POLES_Y[POLE], z)))

CAM_LOC0 = Vector((-1.0, -6.0, 4.6))
LOOK_HI, LOOK_LO = None, None

class Cam(object):
    """tilt down the pole: look point descends z 7.4 -> 1.2 (eased) with a slow push, a lateral slide and the snap."""
    def __init__(self):
        self.p = pole_pt(0.0)
    def at(self, g):
        t = (g - GF) / float(GL - GF)
        u = ez(t, "sine")
        z = lerp(7.2, 1.3, u)
        look = self.p + Vector((0, 0, z))
        # lateral slide (camera-right ~ world -y... use view right)
        base = Vector(CAM_LOC0)
        fwd0 = (look - base).normalized()
        right = Vector((fwd0.y, -fwd0.x, 0)).normalized()
        loc = base + right * (0.9 * t) + (look - base).normalized() * (1.4 * t)   # push 8 %/s-ish
        loc.z = lerp(4.6, 2.2, u)
        s = 0.0
        ga, gb = SNAP
        if g > ga:
            s = C.camrig.ease_peak(min(1.0, (g - ga) / float(gb - ga)), 1.7)
        k = 1.9 ** s
        loc = look - (look - loc) / k
        look = look + right * (-0.5 * s)
        return loc, look
CAM = Cam()

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s20")
        self.key_cam(bf(GF), *CAM.at(GF))
        self.scene.frame_set(bf(GF))
        C.rain_look(self)
    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            TG.set_poles("bare", frame=f)
            TG.set_rain(0.55, frame=f)
            TG.set_leak("pole", 1.0, frame=f)
    def report(self, g):
        loc, look = CAM.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads={})
    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        # pole_pt needs the build; approximate with the real run via probe
        Tk = Take("preview"); CAM.p = pole_pt(0.0)
        rows, worst = CAM_report = C.CamPath.report(type("X", (), {"at": CAM.at})(), GS[:-1])
        print(worst); sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GF <= g <= GL]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); CAM.p = pole_pt(0.0); Tk.pose(gs)
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
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK if False else os.path.join(HERE, "work"), "draft")
        def mk():
            t = Take("final" if scale >= 1.0 else "preview"); CAM.p = pole_pt(0.0); return t
        C.final_loop(mk, gs, out, scale=scale, samples=samples)
