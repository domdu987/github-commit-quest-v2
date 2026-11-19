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
ANG = -38.0
LIGHT, PRESET = "DAY", "chamber_low"

def P(name):
    return dict(cast16.STORY16[name][1])

def pose_of(g):
    p = P("mocker_pm_proud" if g < G_WORD + 1 else "mocker_pm_keys")
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
        loc0 = look0 + d * 4.9 + Vector((0, 0, -1.0))
        CAM = C.CamPath(loc0, look0, G0 - H, G_LAST, push=0.08, slide_px=85.0, arc_deg_s=11.0, decay=0.25,
                        snaps=[dict(g=SNAP, k=1.8, peak=1.7, shift=(-0.9, 0.2))])
        self.key_cam(bf(GS[0]), *CAM.at(GS[0]))
        self.scene.frame_set(bf(GS[0]))
        self.actors["moc"] = C.make_actor("moc", "mocker", os.path.join(WORK, "sprites"), canvas=cast16.CANVAS16["mocker"], contact=True, cam=self.cam)
    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            x, y, z = self.mark
            C.place(self.actors["moc"], f, (x, y, z + 0.04 * abs(math.sin(g * 0.2))))
            self.key_set(f, mailsacks=(True,), flames=(1.0,))
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
