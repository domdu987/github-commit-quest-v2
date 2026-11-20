#!/usr/bin/env python3
"""shot.py -- film 21 segment C (plan v3), g 418..541 (CUT in, no handles): "ระหว่างกลาง มีสะพานไม้แคบ ๆ อยู่สะพานเดียว".
World K.build_world(['bridge_high','bridge_end_south']).  ONE travelling camera: high on the east side of the bridge looking down along it (the column of
3D knights marching north), flying south and DESCENDING past the south end and the STIRLING BRIDGE gantry, then riding behind/beside the two cast knights
(knight_a_mtd red near, knight_b_mtd blue far) whose horses fill the 2.6 m deck side by side (walk cycle, riders pinned).  On "เต็มแล้ว" (g 524) the near
knight sucks his belly in (squash + sweat) with a quick push (x1.3, 14 f).  Camera always east of the deck looking west-ish, so the side-view cards never flip.
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out> [draft|final] [samples] | final a:b[:step] [samples] [threads]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C                                              # noqa: E402
import numpy as np                                           # noqa: E402
from mathutils import Vector                                 # noqa: E402
K, bpy, cast21, actors = C.K, C.bpy, C.cast21, C.actors
lerp, clamp, ease, bf, g_of = C.lerp, C.clamp, C.ease, C.bf, C.g_of
G0, G1 = 418, 541
G_FULL = g_of(17.37)                                         # 524
SC = 0.62; V = 1.6                                           # m per head-D of the mounted cards; march speed m/s
TMP = os.path.join(HERE, "work")
def yc(g): return -33.0 + V * (g - G0) / 30.0                # y of the cast pair's centre

KEYS = [(418, (7.5, 8.0, 27.0), (-2.0, -22.0, 3.0), 22.0),
        (448, (6.5, -14.0, 16.0), (-1.5, -29.0, 3.2), 22.0),
        (482, (5.6, -37.5, 6.0), (-1.2, -31.0, 3.6), 22.0),
        (516, (4.9, yc(516) - 6.0, 4.2), (-1.5, yc(516) + 0.4, 4.45), 22.0),
        (560, (4.7, yc(560) - 5.0, 4.15), (-1.5, yc(560) + 0.4, 4.55), 22.0)]
def cam_at(g):
    r = K.cam_path(None, KEYS, g)
    loc, look = Vector(r["loc"]), Vector(r["look"])
    s = clamp((g - G_FULL) / 14.0); k = 1.0 - (1.0 - 1.0 / 1.3) * (1.0 - (1.0 - s) ** 3)      # the quick push on the belly suck
    if s > 0:
        # push toward the look target by the snap, but never closer than 3 m to the near horse
        loc = look - (look - loc) * k
    sway = 0.04 * math.sin(g * 0.31)
    return loc + Vector((0.0, 0.0, sway)), look

HX = {"near": 0.55, "far": -0.62}
def pairpos(g, who):
    ph = 0.0 if who == "near" else 1.9
    y = yc(g) + (0.0 if who == "near" else -0.45) + 0.03 * math.sin(g * 0.37 + ph)
    return (HX[who] + 0.03 * math.sin(g * 0.52 + ph), y)

def pose(g, who):
    base = cast21.STORY21["knight_a_mounted" if who == "near" else "knight_b_mounted"][1]
    p = dict(base); p.update(mode21="walk", gait=((g - G0) / 40.0 + (0.0 if who == "near" else 0.3)) % 1.0)
    ph = 0.0 if who == "near" else 2.1
    p.update(yaw=0.85, lean=2.0 * math.sin(g * 0.21 + ph), head_roll=2.5 * math.sin(g * 0.17 + ph), expr="worried", mouth="flat")
    p["blink"] = C.blink(g, [430, 447, 466, 487, 505, 521, 538] if who == "near" else [437, 455, 478, 499, 514, 532])
    if who == "near":
        if g >= G_FULL - 1:
            u = ease((g - (G_FULL - 1)) / 8.0)
            p.update(fx=["sweat"], pitch=0.1, squash=(lerp(1.0, 0.74, u) + 0.03 * math.sin(g * 0.9) * u, lerp(1.0, 1.05, u)), lean=-9 * u + 1.2 * math.sin(g * 0.8) * u)
        else:
            p["squash"] = (1.0 + 0.012 * math.sin(g * 0.6), 1.0)
    elif g >= G_FULL + 3:
        p["fx"] = ["sweat"]
    return K.with_rim(p)

class Take(object):
    def __init__(self):
        self.A = K.build_world(["bridge_high", "bridge_end_south"])
        for o in [o for o in bpy.data.objects if o.name.startswith("troops_bridge")]: bpy.data.objects.remove(o, do_unlink=True)
        rs = np.random.RandomState(4); B = K.Batch(85)
        for i in range(14):                                   # the marching 3D column ahead of the cast pair (the pair itself is the last rank)
            pair, side = divmod(i, 2); yy = -33.0 + 6.0 + 5.2 * pair; x = (-0.62, 0.62)[side]
            ENG = [m_ for m_ in K.KNIGHT_MATS if m_[0] != 't_blue']; m = ENG[(pair * 2 + side) % len(ENG)]       # English = crimson / gold / cream only (blue = Scots)
            K.horse(B, (x, yy, K.DECK_Z), 90.0, coat=['horse', 'horse_dk', 'horse'][rs.randint(0, 3)], trap=m[0], trim=m[1], tint=0.85 + 0.3 * rs.rand(), rider=(m[0],))
        self.col = B.finalize('troops_bridge')
        self.cam = bpy.context.scene.camera; self.cam.data.dof.use_dof = False
        self.actors = {"near": C.make_actor("ka", "knight_a_mtd", os.path.join(TMP, "sprites")), "far": C.make_actor("kb", "knight_b_mtd", os.path.join(TMP, "sprites"))}

    def key(self, gs):
        for g in gs:
            c, l = cam_at(g); C.key_cam(self.cam, g, c, l)
        for g in gs:
            for who, a in self.actors.items():
                x, y = pairpos(g, who); a.place(bf(g), (x, y, K.DECK_Z + 0.04 * abs(math.sin((g - G0) / 40.0 * 2 * math.pi)) * 0.5), scale=SC)
        for g in gs:
            f = bf(g); bpy.context.scene.frame_set(f)
            for who, a in self.actors.items(): a.pose(f, pose(g, who), camera=self.cam)
        for a in self.actors.values(): a.render_sprites(256, frames=[bf(g) for g in gs])

    def hooks(self, g):
        t = g / 30.0; K.set_flow(t); K.set_flutter(t); K.set_smoke(t)
        for o in self.col: o.location = (0.0, V * (g - G0) / 30.0, 0.02 * math.sin(g * 0.9))

    def render(self, g, out, mode="draft", samples=None, threads=2):
        sc = bpy.context.scene; sc.frame_set(bf(g)); self.hooks(g)
        cam_at(g)                                             # eases STATE['vivid'] for this frame (position keys come from the Blender keys)
        for a in self.actors.values(): a.sync(self.cam, sc)
        sc.camera = self.cam; K.setup_render(sc, mode, samples); sc.render.threads = threads; sc.cycles.denoising_prefilter = "FAST"
        return K.render(out, mode, samples)

if __name__ == "__main__":
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G1]
    Tk = Take(); Tk.key(gs)
    if cmd == "probe":
        for g in gs: print(g, [round(v, 1) for v in cam_at(g)[0]], [round(v, 1) for v in cam_at(g)[1]])
    elif cmd == "stills":
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
