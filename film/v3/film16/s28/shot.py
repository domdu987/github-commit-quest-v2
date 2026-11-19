#!/usr/bin/env python3
"""shot.py -- film 16 take s28 = shot 28 (CHAMBER chamber_low / DAY): "two years later": the mocker, now Postmaster General, poses with sash,
mail bag, key ring, sacks of letters round him.  Shot g 1805..1894 (60.18-63.17 s) + 9 handle frames each side.  Snap + keys pose on 'ไปรษณีย์ใหญ่'.
Mouths still.   python3 shot.py probe a:b | camreport | stills a:b[:s] out [scale] [spp] | final a:b[:s] [scale] [spp]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector, Matrix                             # noqa: E402
import tg_chamber as CH                                  # noqa: E402
TG, K, actors, cast16 = C.TG, C.K, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(60.18), C.g_bound(63.17)             # 1805, 1895 (shot = g 1805..1894)
H = 9
GS = list(range(G0 - H, G1 + H))
G_LAST = GS[-1]
G_WORD = C.cap_g("ไปรษณีย์ใหญ่")                          # snap + pose swap on 'Postmaster General'
SNAP = (G_WORD - 6, G_WORD + 9)
PPD = 256
ANG = 0.0
LIGHT, PRESET = "DAY", "chamber_low"

def P(name):
    return dict(cast16.STORY16[name][1])

def pose_of(g):
    p = P("mocker_pm_keys")
    p["arm_r"] = dict(hand=(0.80, 0.10), bend=0.25, stretch=1.25)        # the key ring held UP beside his head, sash fully visible
    t = g / 30.0
    p["blink"] = blink(g, [G_WORD, 1830, 1850, 1888])
    p["lean"] = p.get("lean", 0) + 2.0 * math.sin(t * 4.2)
    p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(t * 3.1)
    p["squash"] = (1.0 + 0.015 * math.sin(t * 7.0), 1.0 - 0.015 * math.sin(t * 7.0))
    p["t"] = t
    return p

CAM = None

class Take(C.Take):
    def __init__(self, quality="preview"):
        global CAM
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s28")
        self.mark = self.A["marks"]["mocker_post"]
        m = Vector(self.mark)
        look0 = m + Vector((0, 0, 2.7))
        c0 = Vector(self.A["cam"]["loc"]); l0 = Vector(self.A["cam"]["look_at"])
        d = (c0 - l0); d.z = 0; d.normalize()
        d = Matrix.Rotation(math.radians(float(os.environ.get('ANG', ANG))), 3, 'Z') @ d
        loc0 = look0 + d * 4.6 + Vector((0, 0, -0.3))
        CAM = C.CamPath(loc0, look0, G0 - H, G_LAST, push=0.08, slide_px=85.0, arc_deg_s=11.0, decay=0.25,
                        snaps=[dict(g=SNAP, k=1.8, peak=1.7, shift=(-0.9, 0.2))])
        self.build_sacks()
        self.key_cam(bf(GS[0]), *CAM.at(GS[0]))
        self.scene.frame_set(bf(GS[0]))
        self.actors["moc"] = C.make_actor("moc", "mocker", os.path.join(WORK, "sprites"), canvas=cast16.CANVAS16["mocker"], contact=True, cam=self.cam)
    def build_sacks(self):
        """two OPEN sacks of blank white envelopes on the two desks beside his (left and right thirds, low in frame, never across his torso);
        the set's closed burlap sacks stay off"""
        import random, math as _m
        M = TG.STATE["M"]
        D = [d for d in TG.STATE["desks"] if d[0] == 0]
        D.sort(key=lambda d: abs(d[1] - _m.radians(136)))
        (_, a1, x1, y1, z1), (_, a2, x2, y2, z2) = D[0], D[1]
        p2 = Vector((x2, y2)); p1 = Vector((x1, y1))
        spots = [(p1.x, p1.y, 0.0, 1), (p2.x + (p1.x - p2.x) * 0.26, p2.y + (p1.y - p2.y) * 0.26, 0.0, -1)]
        rr = random.Random(5)
        mb = K.MB("s28_sacks")
        top = 0.85
        for (cx, cy, _z, sgn) in spots:
            mb.ell(M["sack"], (cx, cy, top + 0.17), (0.15, 0.14, 0.18), (14, 9))
            mb.cyl(M["sackdk"], (cx, cy, top + 0.345), 0.14, 0.04, "z", 14)
            mb.cyl(M["dark"], (cx, cy, top + 0.368), 0.105, 0.012, "z", 14)
            for i in range(15):
                ang = rr.uniform(0, 6.283)
                if i < 6:                                     # standing up out of the opening
                    r = rr.uniform(0.0, 0.07); z = top + 0.37 + rr.uniform(0.02, 0.10)
                    rx, ry = rr.uniform(-0.7, 0.7), rr.uniform(-0.7, 0.7)
                else:                                         # spilled over the lip onto the desk
                    r = rr.uniform(0.17, 0.46); z = top + 0.012 + 0.004 * i
                    rx, ry = rr.uniform(-0.06, 0.06), rr.uniform(-0.06, 0.06)
                ex, ey = cx + r * _m.cos(ang), cy + r * _m.sin(ang)
                rz = rr.uniform(0, 3.14)
                mb.box(M["paper"], (ex, ey, z), (0.2, 0.135, 0.008), rz=rz, rx=rx, ry=ry)
                for sgn2 in (-1, 1):                          # the V of the flap: two thin lines from the top corners to the middle
                    lx, ly = -sgn2 * 0.06, 0.035
                    ox = lx * _m.cos(rz) - ly * _m.sin(rz); oy = lx * _m.sin(rz) + ly * _m.cos(rz)
                    mb.box(M["sackdk"], (ex + ox, ey + oy, z + 0.006), (0.085, 0.005, 0.004), rz=rz - sgn2 * 0.62, rx=rx, ry=ry)
        self.sacks = mb.finish()

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            x, y, z = self.mark
            C.place(self.actors["moc"], f, (x, y, z + 0.04 * abs(math.sin(g * 0.2))))
            self.key_set(f, mailsacks=(False,), flames=(1.0,))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.actors["moc"].pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.actors["moc"], PPD)], [bf(g) for g in gs])
    def report(self, g):
        f = bf(g)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))
    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        Take("preview")
        rows, worst = CAM.report(GS[:-1])
        print(rows[::5]); print("longest run under 0.25 px/frame: %d" % worst); sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GS[0] <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; spp = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=spp)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["chamber"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
