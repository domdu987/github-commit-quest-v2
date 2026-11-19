#!/usr/bin/env python3
"""shot.py -- film 16 take s13 = shot 13 (g 831..891, plan 27.70-29.72 s) + handles 9 each side (g 822..900).
"แล้วฝังลวด ไว้ในท่อ ตะกั่วใต้ดิน" -- LINE line_trench / DAY: a mule team pulls Cornell's trench plough along the railway, the lead pipe
(with the wire inside) unrolls into the furrow behind it, Morse and the workers follow.  DIS in (13-17 f), CUT out to shot 14.
Camera: low, tracking alongside the team (the plough front moves along the furrow, the camera follows it), push 8 %/s + slide,
one eased SNAP on "ตะกั่ว" (event g 870).  Mouths: nobody speaks.  NO depth of field, NO text.

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] out_dir [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

TG, K, LN, cast16 = C.TG, C.K, C.LN, C.cast16
lerp, clamp, blink, u_of, bf = C.lerp, C.clamp, C.blink, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(27.70), C.g_bound(29.72)            # 831, 892: shot = g 831..891
H_IN, H_OUT = 9, 9
GA, GB = G0 - H_IN, G1 + H_OUT - 1                      # 822 .. 900
GS = list(range(GA, GB + 1))
G_WORD = C.cap_g("ตะกั่วใต้ดิน")                         # 870
SNAP = (G_WORD - 2, G_WORD + 11)

PRESET, LIGHT = "line_trench", "DAY"
K_A, K_B = 0.50, 0.57                                   # plough front (furrow fraction) at GA and GB
def k_of(g):
    return lerp(K_A, K_B, (g - GA) / float(GB - GA))
CAM_L = (9.5, 12.0, 6.0)
CAM_T = (9.5, 0.0, 1.9)
PIPE_LAG = 0.035                                        # the pipe is laid a little behind the plough

CAM_FOCUS = lambda k: Vector(TG.plough_marks(k)["cornell"]) # tracked point: Cornell's mark

class Cam(object):
    """tracking camera: CamPath drift + snap, shifted by the team's travel (the plough mark at k_of(g))."""
    def __init__(self, loc0, look0):
        self.p0 = Vector(TG.plough_marks(k_of(GA))["plough"])
        self.path = C.CamPath(loc0, look0, GA, GB, push=0.06, slide_px=20.0, arc_deg_s=2.0, decay=0.3,
                              snaps=[dict(g=SNAP, k=1.15, peak=1.6, shift=(11.0, 0.0))])
    def at(self, g):
        loc, look = self.path.at(g)
        d = Vector(TG.plough_marks(k_of(g))["plough"]) - self.p0
        d.z = 0.0
        return loc + d * 0.97, look + d * 0.97

STORY = cast16.STORY16
def story(name):
    return dict(STORY[name][1])

CAST_OF = dict(mule_a="mule", mule_b="mule", cornell="cornell", worker_a="worker16_a", worker_b="worker16_b", morse="morse16")
CANVAS = dict(worker_a=(-2.6875, -4.375, 2.6875, 0.375), worker_b=(-2.6875, -4.625, 2.6875, 0.1875), cornell=(-2.6875, -4.1875, 2.6875, 0.1875), morse=(-2.375, -4.375, 2.375, 0.1875))

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s13")
        A = self.A
        p0 = Vector(TG.plough_marks(k_of(GA))["plough"])
        self.cm = Cam(p0 + Vector(CAM_L), p0 + Vector(CAM_T))
        self.dress_fg()
        self.key_cam(bf(GA), *self.cm.at(GA))
        self.scene.frame_set(bf(GA))
        sd = os.path.join(WORK, "sprites")
        self.act = {}
        for nm, cast in CAST_OF.items():
            cv = CANVAS.get(nm)
            ac = self.actors[nm] = self.act[nm] = C.make_actor(nm, cast, sd, canvas=cv, contact=True, cam=self.cam)
        self.hand_err = {}

    def dress_fg(self):
        """foreground dressing (grass, a crate, a shovel) 1-2.5 D from the lens at three points of the camera path (the preset's own
        dressing is placed for its fixed start pose).  sb metres = inverse of the location frame."""
        inv = K.frame_mat().inverted()
        for i, g in enumerate((GA + 6, GA + 40, GA + 74)):
            loc, look = self.cm.at(g)
            cs, ls = inv @ loc, inv @ look
            items = [("blades", 0, 0, [(1.3 + 0.3 * j, 1.2 + 0.2 * j, 0.9 + 0.2 * j) for j in range(4)])]
            LN.fg_dress(TG.STATE, TG.STATE["M"], (cs.x, cs.y), (ls.x, ls.y), items, seed=70 + i)

    def facing(self, g):
        """screen direction the team travels (+1 right, -1 left) from the plough marks projected in this frame's camera"""
        a = Vector(TG.plough_marks(k_of(g))["plough"]); b = Vector(TG.plough_marks(k_of(g) + 0.01)["plough"])
        pa, pb = TG.project(tuple(a)), TG.project(tuple(b))
        return 1 if pb[0] >= pa[0] else -1

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.cm.at(g))
        self.scene.frame_set(bf(gs[0]))
        for g in gs:
            f = bf(g)
            k = k_of(g)
            self.scene.frame_set(f)
            self.key_set(f, trench=(k,), pipe=(k - PIPE_LAG,))
            fc = self.facing(g)
            mk = TG.plough_marks(k)
            ph = g / 44.0
            pl = {}
            pl["mule_a"] = cast16.cycle("mule", ph, "pull", fc, dict(harness=1))
            pl["mule_b"] = cast16.cycle("mule", ph + 0.25, "pull", fc, dict(harness=1, tint=0.15))
            pl["cornell"] = cast16.cycle("cornell", g / 30.0, "walk", fc, story("cornell_plough"), arms="none")
            pl["worker_a"] = cast16.cycle("worker16_a", g / 30.0 + 0.3, "walk", fc, story("worker_a_shovel"), arms="none")
            pl["worker_b"] = cast16.cycle("worker16_b", g / 30.0 + 0.6, "walk", fc, story("worker_b_shovel"), arms="none")
            pl["morse"] = cast16.cycle("morse16", g / 30.0 + 0.1, "walk", fc, dict(yaw=0.6, expr="happy"), arms="both")
            for nm, p in pl.items():
                p["mirror"] = fc < 0
                p["t"] = g / 30.0
                if nm not in ("mule_a", "mule_b"):
                    p["blink"] = blink(g, [17 + 23 * (hash(nm) % 3)])
                m_ = mk["morse_trench" if nm == "morse" else nm]
                if nm == "morse":
                    m_ = (m_[0] + 6.0, m_[1], m_[2])          # Morse follows close behind Cornell (in frame at the end of the snap)
                C.place(self.act[nm], f, m_)
                self.act[nm].pose(f, p, camera=self.cam)
        self.sprites_for([(a, 256) for a in self.act.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.cm.at(g)
        return dict(g=g, k=round(k_of(g), 4), cam=[round(c, 2) for c in loc], heads=C.head_report(self, f), face=self.facing(g))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        Tk = Take("preview")
        rows, worst = C.CamPath.report(Tk.cm, GS[:-1])
        print("longest run under 0.25 px/frame:", worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GB]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("g %d %.1f s" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
