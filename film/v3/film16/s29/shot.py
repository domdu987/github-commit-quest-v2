#!/usr/bin/env python3
"""shot.py -- film 16 take s29 = shot 29 (CHAMBER chamber_table / DAY): the clerk slides the telegraph instrument across the table to the postmaster
mocker (g 1930-1950); his proud smile drops into horror with a sweat drop (g 1952); snap push-in on his face at 'ความดูแลของเขา' (g 1956).
Shot g 1895..1979 (63.17-66.01 s) + 9 handle frames each side.  Mouths still (horror = held expression mouth).
    python3 shot.py probe a:b | camreport | stills a:b[:s] out [scale] [spp] | final a:b[:s] [scale] [spp]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
import tg_chamber as CH                                  # noqa: E402
TG, K, actors, cast16 = C.TG, C.K, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(63.17), C.g_bound(66.01)             # 1895, 1980 (shot = g 1895..1979)
H = 9
GS = list(range(G0 - H, G1 + H))
G_LAST = GS[-1]
G_WORD = C.cap_g("ความดูแลของเขา")                        # 1956: snap push-in on the mocker's face
SLIDE = (1930, 1950)                                      # the clerk slides the instrument to the mocker
G_HORROR = 1952                                           # pose swap on the closed frame of the blink 1951..1953
SNAP = (G_WORD - 4, G_WORD + 9)
PPD = 256
LIGHT, PRESET = "DAY", "chamber_table"
SLIDE_D = -1.0                                            # world D: the instrument travels left toward the mocker
CAST = dict(moc=dict(cast="mocker", at=(-4.7, 8.7), mirror=False), clk=dict(cast="clerk16", at=(2.6, 8.7), mirror=True))

def P(name):
    return dict(cast16.STORY16[name][1])

def pose_of(k, g):
    t = g / 30.0
    if k == "moc":
        p = P("mocker_pm_proud" if g < G_HORROR else "mocker_horror")
        p["blink"] = blink(g, [1905, 1930, G_HORROR - 1, 1970])
        p["lean"] = p.get("lean", 0) + 2.0 * math.sin(t * 4.2)
        if g >= G_HORROR:
            p["squash"] = (0.98 + 0.02 * math.sin(t * 22.0), 1.02 - 0.02 * math.sin(t * 22.0))     # trembling
        else:
            p["squash"] = (1.0 + 0.015 * math.sin(t * 7.0), 1.0 - 0.015 * math.sin(t * 7.0))
    else:
        p = P("clerk_idle" if g < SLIDE[0] - 3 else "clerk_slide_instrument")
        p["blink"] = blink(g, [1912, 1944, 1975])
        p["lean"] = p.get("lean", 0) + 1.5 * math.sin(t * 3.3)
    p["mirror"] = CAST[k]["mirror"]
    p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(t * 3.1 + len(k))
    p["t"] = t
    return p

class Cam2(C.CamPath):
    """CamPath drift for the two-shot, then the SNAP swings the camera to an explicit close pose (look point + eye point) in 14 f (eased, peak 1.7)."""
    def __init__(self, *a, end_loc, end_look, **k):
        C.CamPath.__init__(self, *a, **k)
        self.el, self.ek = Vector(end_loc), Vector(end_look)
    def at(self, g):
        loc, look = C.CamPath.at(self, g)
        ga, gb = SNAP
        u = 0.0 if g <= ga else min(1.0, C.camrig.ease_peak((g - ga) / float(gb - ga), 1.7))
        t = max(0, g - gb) / 30.0
        d = self.ek - self.el
        el = self.ek - d * (1.0 - 0.05 * t)                       # slow push after the snap
        return loc.lerp(el, u), look.lerp(self.ek, u)

CAM = None

class Take(C.Take):
    def __init__(self, quality="preview"):
        global CAM
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s29")
        look0 = Vector((-1.1, 8.7, 2.7)); loc0 = Vector((0.7, -2.6, 4.4))
        CAM = Cam2(loc0, look0, G0 - H, G_LAST, push=0.05, slide_px=-45.0, arc_deg_s=-7.0, decay=0.25, snaps=[], end_loc=(-5.8, 5.8, 3.4), end_look=(-4.7, 8.7, 2.85))
        self.key_cam(bf(GS[0]), *CAM.at(GS[0]))
        self.scene.frame_set(bf(GS[0]))
        for k, v in CAST.items():
            self.actors[k] = C.make_actor(k, v["cast"], os.path.join(WORK, "sprites"), canvas=cast16.CANVAS16[v["cast"]], contact=True, cam=self.cam)
        self.make_instrument()
    def make_instrument(self):
        """the instrument slides: cut it out of the set's table objects, rebuild the same mesh as its own objects (offset keyed), the lever follows"""
        import bmesh
        M = TG.STATE["M"]
        lo = Vector(K.W((CH.TG_C[0] - 1.8, CH.TG_C[1] - 0.72, 0.9625))); hi = Vector(K.W((CH.TG_C[0] + 1.45, CH.TG_C[1] + 1.1, 3.0)))
        for ob in TG.STATE["table_objs"]:
            if ob.name.endswith("wiremat"):
                continue
            bm = bmesh.new(); bm.from_mesh(ob.data)
            dead = [v for v in bm.verts if lo.x <= v.co.x <= hi.x and lo.y <= v.co.y <= hi.y and v.co.z > lo.z]
            bmesh.ops.delete(bm, geom=dead, context="VERTS")
            bm.to_mesh(ob.data); bm.free()
        mb = K.MB("s29_instr")
        CH.tg_arm_parts(mb, M, CH.TG_C, CH.TG_S)
        self.instr = mb.finish()
        self.lever = TG.STATE["lever"]
        self.lever0 = Vector(self.lever.location)
    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            for k, a in self.actors.items():
                x, y = CAST[k]["at"]
                C.place(a, f, (x, y, 0.03 * math.sin(g * 0.5 + len(k))))
            u = u_of(g, *SLIDE, kind="sine")
            off = Vector((SLIDE_D * u, 0.0, 0.0))
            for ob in self.instr:
                ob.location = off
                ob.keyframe_insert("location", frame=f)
            self.lever.location = self.lever0 + off
            self.lever.keyframe_insert("location", frame=f)
            self.key_set(f, tape=(0.0, 0), flames=(1.0,))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for k, a in self.actors.items():
                a.pose(f, pose_of(k, g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])
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
