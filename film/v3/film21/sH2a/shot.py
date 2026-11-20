#!/usr/bin/env python3
"""shot.py -- film 21 segment H2a (plan v3), g 1345..1392 (D6 in) + 3 handle frames before (1342-1344: H1's move continued into P_NECK) and 3 after (1393-1395: the
drift continued).  World K.build_world(['bridge_end_north','valley_loop']).  Starts EXACTLY at K.POSES['P_NECK'] (g 1345), CRANES up fast (~1 s) while backing south
to K.POSES['P_TOP'] (g 1392) and hold-drifts: the bottle-and-cork image (English in crimson boxed in the loop, the Scots spear wall with blue saltire banners at the
bridge mouth, the other half waiting on the south bank).
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out> [draft|final] [samples] | final a:b[:step] [samples] [threads]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C                                              # noqa: E402
import numpy as np                                           # noqa: E402
from mathutils import Vector                                 # noqa: E402
K, bpy, cast21, actors, sprites = C.K, C.bpy, C.cast21, C.actors, C.sprites
TMP = os.path.join(HERE, 'work')
G_A, G_B = 1345, 1392                                        # P_NECK / P_TOP
G0, G1 = 1342, 1395
WALL_Y = 31.5                                                # the spear wall stands at the end of the (shortened) deck
NECK, TOP = K.POSES["P_NECK"], K.POSES["P_TOP"]          # P_TOP = (-10,-115,115) -> (0,70,0): looks NORTH from above the south bank (API 13)
# the heading turns smoothly over the WHOLE crane: south (P_NECK) -> east-south-east -> north-east -> north (P_TOP), arcing up on the WEST side; never overhead
KEYS = [(1342, (-2.3, 53.0, 5.6), (0.0, 22.0, 1.9), 22.0),
        (G_A,) + NECK,
        (1356, (-34.0, 36.0, 30.0), (4.0, 20.0, 2.0), 22.0),
        (1368, (-58.0, -25.0, 78.0), (6.0, 25.0, 0.0), 22.0),
        (G_B,) + TOP,
        (1400, (TOP[0][0] + 1.0, TOP[0][1] - 1.8, TOP[0][2] + 0.5), (TOP[1][0], TOP[1][1] + 0.2, 0.0), 22.0)]
def _viv3(v): return (v[0], v[1], v[2] if len(v) > 2 else 1.0)
def cam_at(g):
    r = K.cam_path(None, KEYS, g)
    v0, v1 = _viv3(K.VIVID["bridge_end_north"]), _viv3(K.VIVID["P_TOP"])
    t = C.smooth((g - G_A) / float(G_B - G_A)); lg = lambda a, b: math.exp((1 - t) * math.log(a) + t * math.log(b))
    K.STATE["vivid"] = (lg(v0[0], v1[0]), v0[1] + (v1[1] - v0[1]) * t, lg(v0[2], v1[2]) * (1.0 + 0.30 * 4 * t * (1 - t)))     # my own ease: the handle frames keep exactly the P_TOP grade
    r["vivid"] = K.STATE["vivid"]; return r

CRIM, BLUE = "#b3202a", "#2b50b8"
def add_variant(base, new, colour):
    d = cast21._recolour(base, colour); cast21.P.CAST[new] = d
    for tab in (cast21.CE.CANVAS, sprites.DEFAULT_CANVAS):
        if base in tab: tab[new] = tab[base]
def _hm(cast, pose_name, hm):
    """metres per head-D for a cast card: standing height hm / (feet - head_top) of the drawing."""
    p = cast21.STORY21[pose_name][1]; a = sprites.sprite_svg(cast, p, 64)[1]["anchors"]
    return hm / (a["feet"][1] - a["head_top"][1])

class Take(object):
    def __init__(self):
        K.BRIDGE_Y1 = WALL_Y - 0.4                           # the deck ENDS at the wall (set code reads the global at build time)
        self.A = K.build_world(["bridge_end_north", "valley_loop"], over=dict(foam_k=1.25))
        for o in [o for o in bpy.data.objects if o.name.startswith(("crowd_", "spear_wall", "wall_banners", "troops_causeway"))]: bpy.data.objects.remove(o, do_unlink=True)
        self.cam = bpy.context.scene.camera; self.cam.data.dof.use_dof = False; self.cam.data.clip_end = 9000
        rs = np.random.RandomState(11)
        # --- the English in the loop: one solid CRIMSON mass (rows only from y 58: nobody at the lens at P_NECK), tightly packed, no shadow stubble
        B = K.Batch(71)
        for r in range(20):
            for c in range(26):
                x = -19.5 + c * 1.5 + (0.7 if r % 2 else 0) + rs.uniform(-0.15, 0.15); y = 58.0 + r * 1.7 + rs.uniform(-0.15, 0.15)
                if math.hypot(x - K.LOOP_C[0], y - K.LOOP_C[1]) < K.LOOP_R - 14 and float(K.sd_at(x, y)) > 3:
                    z = float(K.ground(x, y)); B.box("cloth_red", (x, y, z + 0.8), (0.7, 0.45, 1.6)); B.sphere("cloth_red", (x, y, z + 1.78), 0.24, seg=6, rings=4)
        B.finalize("en_loop", ink=False, shadow=False)
        # --- the other half waits on the south bank (crimson block on the clear lawn by the bridge's south mouth)
        B = K.Batch(72)
        for r in range(13):
            for c in range(17):
                x = -12.0 + c * 1.5 + (0.7 if r % 2 else 0) + rs.uniform(-0.15, 0.15); y = -40.0 - r * 1.8
                z = float(K.ground(x, y)); B.box("cloth_red", (x, y, z + 0.8), (0.7, 0.45, 1.6)); B.sphere("cloth_red", (x, y, z + 1.78), 0.24, seg=6, rings=4)
        B.finalize("en_south", ink=False, shadow=False)
        # --- the cork: 5 ranks of Scots (front two = cast cards tinted blue, back three = blue 3D bodies), spears level, 4 LARGE saltire banners (on the flanks)
        B = K.Batch(73)
        for rank in range(2, 5):
            for k in range(14):
                x = -9.0 + 18.0 * k / 13.0 + (0.5 if rank % 2 else 0.0); y = WALL_Y + 1.1 * rank; z = float(K.ground(x, y))
                B.box("t_blue", (x, y, z + 0.85), (0.8, 0.6, 1.6)); B.sphere("steel", (x, y, z + 1.78), 0.21, seg=6, rings=4)
                K.spear(B, (x, y - 0.4, z), tilt=(0.0, -0.9), h=2.4)
        B.finalize("wall_back", ink=False)
        Bp = K.Batch(87)
        for k, sx in enumerate((-14.0, -10.5, 10.5, 14.0)):
            K.banner(Bp, (sx, WALL_Y + 2.0, float(K.ground(sx, WALL_Y))), 9.0, 215, "t_saltire", "t_white", "saltire", rs, size=(6.6, 4.3))
        Bp.finalize("wall_banners")
        # --- cast: 12 English on the causeway (crimson variants) + the front two Scots ranks (blue variants)
        add_variant("footman_a", "footman_a_crim", CRIM); add_variant("footman_b", "footman_b_crim", CRIM)
        for b_ in ("scot_a", "scot_b", "scot_c"): add_variant(b_, b_ + "_blue", BLUE)
        cz = K.place_troops(self.A, "causeway", 12, seed=3, cb=lambda it: None)
        self.eng = []
        for i, (x, y, z, kind, sc) in enumerate(cz):
            base = ("footman_a", "footman_b")[i % 2]; cast = base + "_crim"
            self.eng.append((C.make_actor("en%d" % i, cast, os.path.join(TMP, "sprites")), cast, (x, y, z), _hm(base, base + "_worried", 1.68), base))
        self.scots = []
        n = 0
        for rank in range(2):
            for k in range(14):
                x = -9.0 + 18.0 * k / 13.0 + (0.5 if rank else 0.0); y = WALL_Y + 1.1 * rank; base = ("scot_a", "scot_b", "scot_c")[(k + rank) % 3]; cast = base + "_blue"
                self.scots.append((C.make_actor("sc%d" % n, cast, os.path.join(TMP, "sprites")), cast, (x, y, float(K.ground(x, y))), _hm(base, base + "_spear_wall", 1.70), n, base)); n += 1
    def pose_en(self, i, base, g):
        p = dict(cast21.STORY21[base + ("_bump" if (g + 7 * i) % 40 < 7 else "_worried")][1])
        p["head_roll"] = p.get("head_roll", 0) + 5.0 * math.sin(g * 0.45 + i); p["lean"] = 2.0 * math.sin(g * 0.3 + 1.7 * i)
        p["blink"] = C.blink(g, [1350 + 9 * i % 40, 1380 + 5 * i % 30]); return K.with_rim(p)
    def pose_sc(self, n, base, g):
        p = dict(cast21.STORY21[base + "_spear_wall"][1]); p["lean"] = 1.5 * math.sin(g * 0.2 + n); p["head_roll"] = 2.0 * math.sin(g * 0.13 + n)
        p["blink"] = C.blink(g, [1350 + 11 * n % 37, 1382 + 3 * n % 20]); return K.with_rim(p)
    def key(self, gs):
        for g in gs:
            r = cam_at(g); C.key_cam(self.cam, g, r["loc"], r["look"])
        allc = [(a, c, xyz, hm, 128, "en") for (a, c, xyz, hm, bs) in self.eng] + [(a, c, xyz, hm, 128, n) for (a, c, xyz, hm, n, bs) in self.scots]
        for (a, c, xyz, hm, ppd, n) in allc:
            for g in gs: a.place(C.bf(g), xyz, scale=hm)
        for g in gs:
            f = C.bf(g); bpy.context.scene.frame_set(f)
            for i, (a, c, xyz, hm, bs) in enumerate(self.eng): a.pose(f, self.pose_en(i, bs, g), camera=self.cam)
            for (a, c, xyz, hm, n, bs) in self.scots: a.pose(f, self.pose_sc(n, bs, g), camera=self.cam)
        for (a, c, xyz, hm, ppd, n) in allc: a.render_sprites(ppd, frames=[C.bf(g) for g in gs])
    def hooks(self, g):
        t = g / 30.0; K.set_flow(t); K.set_smoke(t); K.set_flutter(t)
    def render(self, g, out, mode="draft", samples=None, threads=2):
        sc = bpy.context.scene; sc.frame_set(C.bf(g)); self.hooks(g); r = cam_at(g)
        for a in actors.REGISTRY: a.sync(self.cam, sc)
        sc.camera = self.cam; K.setup_render(sc, mode, samples); sc.render.threads = threads; sc.cycles.denoising_prefilter = "FAST"
        return K.render(out, mode, samples)
if __name__ == "__main__":
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G1]
    if cmd == "probe":
        Tk = Take()
        for g in gs: r = cam_at(g); print(g, [round(v, 1) for v in r["loc"]], [round(v, 1) for v in r["look"]], [round(v, 2) for v in r["vivid"]])
    else:
        Tk = Take(); Tk.key(gs)
        if cmd == "stills":
            out = sys.argv[3]; mode = sys.argv[4] if len(sys.argv) > 4 else "draft"; smp = int(sys.argv[5]) if len(sys.argv) > 5 else None
            os.makedirs(out, exist_ok=True)
            for g in gs: print("g", g, "%.1fs" % Tk.render(g, os.path.join(out, "g_%04d.png" % g), mode, smp), flush=True)
        elif cmd == "final":
            smp = int(sys.argv[3]) if len(sys.argv) > 3 else 32; th = int(sys.argv[4]) if len(sys.argv) > 4 else 2
            out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
            for g in gs:
                png = os.path.join(out, "g_%04d.png" % g)
                if os.path.exists(png + ".ok"): continue
                dt = Tk.render(g, png, "final", smp, th); open(png + ".ok", "w").write("%d %.1f" % (smp, dt)); print("g", g, "%.1fs" % dt, flush=True)
