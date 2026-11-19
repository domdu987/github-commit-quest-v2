#!/usr/bin/env python3
"""shot.py -- film 16 take s14 = shot 14 (g 892..957, plan 29.72-31.93 s) + handles 9 each side (g 883..966).
"ขุดไปหนึ่ง กิโล / ห้ากิโล / สิบห้ากิโล" -- LINE line_trench_high / DAY -> DUSK: the count.  Three eased SNAP crane-ups inside one take
(13 f each, x ~1.5-2.5): each snap the camera is higher, the furrow + pipe behind the team longer (set_trench 0.18 -> 0.3 -> 0.6 -> 0.9,
the team travels with it), the sun lower (set_light_mix DAY->DUSK).  Between the snaps: drift (push 7 %/s + slide + a little arc).
Hard cut in from shot 13, DIS out to shot 15 (DUSK).  Mouths: nobody speaks.  NO depth of field, NO text.

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

G0, G1 = C.g_bound(29.72), C.g_bound(31.93)            # 892, 958: shot = g 892..957
H_IN, H_OUT = 9, 9
GA, GB = G0 - H_IN, G1 + H_OUT - 1                      # 883 .. 966
GS = list(range(GA, GB + 1))
W1, W2, W3 = C.cap_g("ขุดไปหนึ่ง"), C.cap_g("ห้ากิโล"), C.cap_g("สิบห้ากิโล")      # 895 / 924 / 940
SN = [(W1 - 2, W1 + 11), (W2 - 2, W2 + 11), (W3 - 2, W3 + 11)]                    # 893..906, 922..935, 938..951 (13 f each)

G_TREES = 941                                           # the near trees leave with snap 3 (the crane-up flies through their crowns)

def bpy_obj(n):
    return C.bpy.data.objects.get(n)

PRESET, LIGHT = "line_trench_high", "DAY"
KS = [0.20, 0.30, 0.60, 0.90]                           # furrow state before snap 1 / after snap 1, 2, 3
MIX = [0.0, 0.10, 0.55, 1.0]                            # DAY -> DUSK after each snap
WALK = 0.010                                            # extra furrow fraction per second the team walks between the snaps
PIPE_LAG = 0.025
PUSH, SLIDE_PX, ARC, DECAY = 0.09, 55.0, 8.0, 0.25
PEAK = 1.6

def ease_peak(u):
    return C.camrig.ease_peak(u, PEAK) if u > 0 else 0.0

def us(g):
    """eased progress 0..1 of each of the three snaps at frame g"""
    return [ease_peak(clamp((g - a) / float(b - a), 0.0, 1.0)) if g > a else 0.0 for a, b in SN]

def k_base(g):
    u = us(g)
    return KS[0] + sum((KS[i + 1] - KS[i]) * u[i] for i in range(3))

def mix_of(g):
    u = us(g)
    return MIX[0] + sum((MIX[i + 1] - MIX[i]) * u[i] for i in range(3))

def k_of(g):
    return k_base(g) + WALK * (g - GA) / 30.0

class Cam(object):
    """P0 (low, close, = snap-1 pose pulled in) -> snap 1 -> snap 2 -> snap 3 (the preset's own three crane-up cameras), each move a
    13 f eased snap; drift on top (push, slide, arc, still moving at both ends); the camera is carried along with the team walking."""
    def __init__(self, cams):
        c1, c2, c3 = [(Vector(cams[n]["loc"]), Vector(cams[n]["look_at"])) for n in ("line_trench_snap1", "line_trench_snap2", "line_trench_snap3")]
        l0 = c1[1] + (c1[0] - c1[1]) * 0.55
        l0.z = max(0.9, l0.z - 1.0)
        r3 = Vector(((c3[1] - c3[0]).y, -(c3[1] - c3[0]).x, 0)).normalized() * 0.0
        self.P = [(l0, c1[1] + Vector((0, 0, -0.2))), c1, c2, (c3[0] + r3, c3[1] + r3)]
        self.d0 = (self.P[0][1] - self.P[0][0]).length

    def base(self, g):
        u = us(g)
        loc, look = Vector(self.P[0][0]), Vector(self.P[0][1])
        for i in range(3):
            loc = loc + (self.P[i + 1][0] - self.P[i][0]) * u[i]
            look = look + (self.P[i + 1][1] - self.P[i][1]) * u[i]
        return loc, look

    def at(self, g):
        loc, look = self.base(g)
        T = (GB - GA) / 30.0
        t = (g - GA) / 30.0
        p = t - DECAY * t * t / (2 * T)
        fwd = (look - loc)
        d = fwd.length
        fwd.normalize()
        right = Vector((fwd.y, -fwd.x, 0)).normalized()
        look = look + right * (SLIDE_PX * d / C.F_PX * p)
        zoom = max(0.3, 1.0 + PUSH * p)
        fwd = C.Matrix.Rotation(math.radians(ARC * p), 3, "Z") @ fwd
        loc = look - fwd * (d / zoom)
        # carried along with the team's extra walk
        tr = Vector(TG.plough_marks(k_of(g))["plough"]) - Vector(TG.plough_marks(k_base(g))["plough"])
        tr.z = 0
        return loc + tr, look + tr

STORY = cast16.STORY16
def story(name):
    return dict(STORY[name][1])

CAST_OF = dict(mule_a="mule", mule_b="mule", cornell="cornell", worker_a="worker16_a", worker_b="worker16_b")
CANVAS = dict(worker_a=(-2.6875, -4.375, 2.6875, 0.375), worker_b=(-2.6875, -4.625, 2.6875, 0.1875), cornell=(-2.6875, -4.1875, 2.6875, 0.1875), morse=(-2.375, -4.375, 2.375, 0.1875))

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s14")
        self.cm = Cam(self.A["cams"])
        self.trees = [o for o in (bpy_obj(n) for n in ('trees_leafA', 'trees_leafB', 'trees_trunk')) if o is not None]
        self.key_cam(bf(GA), *self.cm.at(GA))
        self.scene.frame_set(bf(GA))
        sd = os.path.join(WORK, "sprites")
        self.act = {}
        for nm, cast in CAST_OF.items():
            self.actors[nm] = self.act[nm] = C.make_actor(nm, cast, sd, canvas=CANVAS.get(nm), contact=True, cam=self.cam)

    def clear_trees(self, radius=15.0):
        """the snap-3 crane-up flies through the tree crowns beside the field: cut the tree geometry within `radius` D of the camera path
        (trees are merged into trees_leafA / leafB / trunk; only this take's camera sees the hole)."""
        import bmesh, bpy
        pts = [self.cm.at(g)[0] for g in range(920, GB + 1, 3)]
        for name in ("trees_leafA", "trees_leafB", "trees_trunk"):
            ob = bpy.data.objects.get(name)
            if ob is None:
                continue
            bm = bmesh.new(); bm.from_mesh(ob.data)
            mw = ob.matrix_world
            bad = [v for v in bm.verts if any((mw @ v.co - p).length < radius for p in pts)]
            bmesh.ops.delete(bm, geom=bad, context="VERTS")
            bm.to_mesh(ob.data); bm.free()

    def facing(self, g):
        a = Vector(TG.plough_marks(k_of(g))["plough"]); b = Vector(TG.plough_marks(k_of(g) + 0.01)["plough"])
        pa, pb = TG.project(tuple(a)), TG.project(tuple(b))
        return 1 if pb[0] >= pa[0] else -1

    def pose(self, gs):
        for g in gs:
            self.key_cam(bf(g), *self.cm.at(g))
        for g in gs:
            f = bf(g)
            k = k_of(g)
            self.scene.frame_set(f)
            C.key_vis(self.trees, g < G_TREES, f)
            self.key_set(f, trench=(k,), pipe=(k - PIPE_LAG,), light_mix=("DAY", "DUSK", mix_of(g)))
            fc = self.facing(g)
            mk = TG.plough_marks(k)
            ph = g / 44.0
            pl = {}
            pl["mule_a"] = cast16.cycle("mule", ph, "pull", fc, dict(harness=1))
            pl["mule_b"] = cast16.cycle("mule", ph + 0.25, "pull", fc, dict(harness=1, tint=0.15))
            pl["cornell"] = cast16.cycle("cornell", g / 30.0, "walk", fc, story("cornell_plough"), arms="none")
            pl["worker_a"] = cast16.cycle("worker16_a", g / 30.0 + 0.3, "walk", fc, story("worker_a_shovel"), arms="none")
            pl["worker_b"] = cast16.cycle("worker16_b", g / 30.0 + 0.6, "walk", fc, story("worker_b_shovel"), arms="none")
            for nm, p in pl.items():
                p["mirror"] = fc < 0
                p["t"] = g / 30.0
                if nm not in ("mule_a", "mule_b"):
                    p["blink"] = blink(g, [17 + 23 * (len(nm) % 3)])
                C.place(self.act[nm], f, mk[nm])
                self.act[nm].pose(f, p, camera=self.cam)
        self.sprites_for([(a, 256) for a in self.act.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.cm.at(g)
        return dict(g=g, k=round(k_of(g), 4), mix=round(mix_of(g), 3), cam=[round(c, 2) for c in loc], heads=C.head_report(self, f), face=self.facing(g))

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
