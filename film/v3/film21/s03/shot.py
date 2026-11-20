#!/usr/bin/env python3
"""shot.py -- film 21 take s03: shots 8-9, g 418..541 (+ 7 in-handle g 411..417 for the D11 dissolve in, + 6 out-handle g 542..547).

  shot 8  g 411..498  bridge_high (3D set only): from 24 m above the south bank the long narrow trestle bridge, the only crossing; a column of
                      mounted knights (3D horses of the set, rigid, marching north 2 m/s with a hoof bob) crosses two by two.
                      Push in along the bridge 8 %/s (24 m -> 19 m) + lateral truck 25 px/s.  No fg prop (preset has none; the pavilions are the fg).
  shot 9  g 499..547  bridge_end_south, camera moved to the east side of the deck's south mouth (side-view horse cards need a side view):
                      two horses abreast, wedged on the 2.6 m deck (x +-0.55, rail posts at +-1.3), riders knight_a_mtd (near, red) and
                      knight_b_mtd (far, blue); a leaning English gate spear is the fg.  Drift push 8 %/s + slide 40 px/s, then the SNAP
                      (16 f, x1.4) on "เต็มแล้ว" (17.37 s narration = g 524) while the near knight sucks his belly in.
Nobody speaks.  One location (bridge) per process: run shot 8 and shot 9 as separate processes.

    python3 shot.py probe 8|9 a:b[:step]
    python3 shot.py stills 8|9 a:b[:step] <out_dir> [draft|final] [samples]
    python3 shot.py final 8|9 a:b[:step] [samples] [threads]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C                                              # noqa: E402
import numpy as np                                           # noqa: E402
from mathutils import Vector                                 # noqa: E402
K, bpy, cast21, actors = C.K, C.bpy, C.cast21, C.actors
lerp, clamp, ease, smooth, bf, g_of = C.lerp, C.clamp, C.ease, C.smooth, C.bf, C.g_of

G_IN, G_CUT, G_END = 411, 499, 542                           # first rendered g (7 handle frames), plan cut, take end
G_LAST = 547                                                 # + 6 out-handle frames
RANGES = {8: (G_IN, G_CUT - 1), 9: (G_CUT, G_LAST)}
G_FULL = g_of(17.37)                                         # 524 "เต็มแล้ว"
TMP = os.path.join(HERE, "work")
SC = 0.62                                                    # metres per head-D for the mounted cards (knight 1.78 m = 3.26 head D)

def _unit(v): v = Vector(v); return v / v.length

# ============================================================================= shot 8 (3D only)
CAM8 = (-5.0, -62.0, 24.0); LOOK8 = (0.0, 6.0, 1.0)
def cam8(g):
    t = (g - G_IN) / 30.0                                    # seconds since the first rendered frame (nearly constant speed, eased only at the very start)
    u = 0.12 * ease(t / 3.0) + 0.88 * t / 3.0
    c0, l0 = Vector(CAM8), Vector(LOOK8)
    d = (l0 - c0); dist = d.length
    sn = clamp((g - 466) / 14.0); push = 0.10 * 3.0 * u + 0.12 * (1.0 - (1.0 - sn) ** 3)   # + snap push x1.3 (14 f) at g466
    c = c0 + d * push
    c.z -= 2.5 * u
    right = _unit(d.cross(Vector((0, 0, 1))))
    slide = 36.0 / 782.0 * dist * 3.0 * u                    # 25 px/s at the target distance, as a truck (position AND target move)
    return c + right * slide, l0 + right * (slide * 0.45)

KNIGHT_X = 0.62
def build8():
    A = K.build(preset="bridge_high")
    K.PRESETS["bridge_high"].get("fg") and K.PRESETS["bridge_high"]["fg"](A, K.PRESETS["bridge_high"])
    # own column of 3D riders (place_troops puts them on fixed points; here ONE object so the whole column can march)
    for o in [o for o in bpy.data.objects if o.name.startswith("troops_bridge")]: bpy.data.objects.remove(o, do_unlink=True)
    rs = np.random.RandomState(4); B = K.Batch(85)
    for i in range(16):
        pair, side = divmod(i, 2); yy = -29.0 + 5.2 * pair; x = (-0.62, 0.62)[side]
        m = K.KNIGHT_MATS[(pair * 2 + side) % 5]
        K.horse(B, (x, yy, K.DECK_Z), 90.0, coat=['horse', 'horse_dk', 'horse'][rs.randint(0, 3)], trap=m[0], trim=m[1], tint=0.85 + 0.3 * rs.rand(), rider=(m[0],))
    obs = B.finalize('troops_bridge')
    return A, obs

# ============================================================================= shot 9
CAM9_0 = Vector((4.9, -33.2, 3.15)); LOOK9_0 = Vector((0.0, -31.3, 3.95))
G9_0 = G_CUT
def cam9(g):
    t = (g - G9_0) / 30.0
    d0 = (LOOK9_0 - CAM9_0)
    u = 0.15 * ease(t / 1.2) * 0 + t                         # linear drift: never a dead hold
    zoom = 1.0 - 0.08 * u                                    # 8 %/s pull of the distance (drift push)
    s = clamp((g - G_FULL) / 16.0)                           # the snap: 16 f, x1.4, fast start / soft end
    snap = 1.0 - (1.0 - 1.0 / 1.4) * (1.0 - (1.0 - s) ** 3)
    right = _unit(d0.cross(Vector((0, 0, 1))))
    slide = right * (-0.30 * t)                               # ~40 px/s at ~6 m (0.3 m/s)
    look = LOOK9_0 + slide
    c = look - d0 * (zoom * snap)
    return Vector(c), Vector(look)

HX = {"near": (KNIGHT_X - 0.07, -32.7), "far": (-KNIGHT_X, -29.95)}      # horse centres (x, y); the near one is east (camera side)
def jostle(g, who):
    ph = 0.0 if who == "near" else 1.9
    return (0.035 * math.sin(g * 0.52 + ph), 0.05 * math.sin(g * 0.37 + ph * 1.3))

def pose9(g, who):
    base = cast21.STORY21["knight_a_mounted" if who == "near" else "knight_b_mounted"][1]
    p = dict(base); p.update(mode21="idle", t=((g + (0 if who == "near" else 23)) / 70.0) % 1.0)
    ph = 0.0 if who == "near" else 2.1
    p["yaw"] = 0.85
    p["lean"] = 2.0 * math.sin(g * 0.21 + ph)
    p["head_roll"] = 2.5 * math.sin(g * 0.17 + ph)
    p["blink"] = C.blink(g, [507, 518, 531, 543] if who == "near" else [512, 526, 539])
    p["expr"] = "worried"; p["mouth"] = "flat"
    if who == "near":
        u = ease((g - (G_FULL - 1)) / 8.0)                  # "เต็มแล้ว": he sucks his belly in (swap behind the blink at 523-525)
        if g >= G_FULL - 1:
            sb = cast21.STORY21["knight_a_mounted_suck_belly"][1]
            p.update(pitch=0.1, fx=["sweat"], squash=(lerp(1.0, 0.84, u), lerp(1.0, 1.03, u)), lean=-6 * u + 1.0 * math.sin(g * 0.8) * u, mode21="idle")
            p["expr"] = "worried"
        else:
            p["squash"] = (1.0 + 0.012 * math.sin(g * 0.6), 1.0)
    else:
        if g >= G_FULL + 3:
            p["fx"] = ["sweat"]
    p["blink"] = bool(p["blink"])
    return p

def build9():
    A = K.build(preset="bridge_end_south")
    A["cam_obj"] = bpy.context.scene.camera
    for o in bpy.data.objects:
        if o.name.startswith("ph_"): o.hide_render = True        # stand-in cast of the preset's marks
    # foreground: a gate spear leaning in near the lens (replaces the preset's spear, tuned to the preset camera)
    C.hide_prefix(["fg_generic"])
    return A

# ============================================================================= the take
class Take(object):
    def __init__(self, shot, quality="draft"):
        self.shot = shot
        bpy.ops.wm.read_factory_settings(use_empty=True) if False else None
        if shot == 8:
            self.A, self.col = build8()
        else:
            self.A = build9()
        self.cam = bpy.context.scene.camera
        self.cam.data.dof.use_dof = False; self.cam.data.clip_start = 0.1
        self.actors = {}
        if shot == 9:
            self.actors["near"] = C.make_actor("ka", "knight_a_mtd", os.path.join(TMP, "sprites"))
            self.actors["far"] = C.make_actor("kb", "knight_b_mtd", os.path.join(TMP, "sprites"))
            self.make_fg()
        self.pose_ok = set()

    def make_fg(self):
        # gate spear 2.4 m from the lens, entering from the lower left, leaning in; its base on the sand
        c, l = cam9(G9_0)
        fwd = _unit(l - c); right = _unit(fwd.cross(Vector((0, 0, 1))))
        d, xp = 3.2, 120
        p = c + fwd * d + right * ((xp - 360) * d / 782.2)
        B = K.Batch(96); z = float(K.ground(p.x, p.y))
        K.spear(B, (p.x, p.y, z), tilt=(0.1, -0.95), h=3.6); B.finalize("fg_team", shadow=False)

    def key(self, gs):
        for g in gs:
            c, l = cam9(g) if self.shot == 9 else cam8(g)
            C.key_cam(self.cam, g, c, l)
        if self.shot == 9:
            for g in gs:
                for who, a in self.actors.items():
                    jx, jy = jostle(g, who); x, y = HX[who]
                    bob = 0.0
                    a.place(bf(g), (x + jx, y + jy, K.DECK_Z + bob), scale=SC)
            for g in gs:
                f = bf(g); bpy.context.scene.frame_set(f)
                for who, a in self.actors.items():
                    a.pose(f, pose9(g, who), camera=self.cam)
            for who, a in self.actors.items():
                a.render_sprites(256, frames=[bf(g) for g in gs])

    def hooks(self, g):
        t = g / 30.0
        K.set_flow(t); K.set_flutter(t); K.set_smoke(t)
        if self.shot == 8:
            for o in self.col:
                o.location = (0.0, 2.0 * (g - G_IN) / 30.0, 0.025 * math.sin(g * 0.9))

    def render(self, g, out, mode="draft", samples=None, threads=2):
        sc = bpy.context.scene; sc.frame_set(bf(g)); self.hooks(g)
        for a in self.actors.values(): a.sync(self.cam, sc)
        sc.camera = self.cam
        K.setup_render(sc, mode, samples); sc.render.threads = threads; sc.cycles.denoising_prefilter = "FAST"
        return K.render(out, mode, samples)

    def report(self, g):
        sc = bpy.context.scene; sc.frame_set(bf(g)); bpy.context.view_layer.update()
        res = {"g": g, "cam": [round(v, 2) for v in self.cam.location]}
        if self.shot == 9:
            K.setup_render(sc, "final"); bpy.context.view_layer.update()
            for who, a in self.actors.items():
                an = None
                r = a.poses.get(bf(g))
                x, y = HX[who]
                head = K.project(self.cam, (x, y, K.DECK_Z + 3.81 * SC))
                res[who + "_head"] = [round(head[0]), round(head[1]), round(head[2], 1)]
        return res

if __name__ == "__main__":
    cmd, shot = sys.argv[1], int(sys.argv[2])
    gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    Tk = Take(shot); Tk.key(gs)
    if cmd == "probe":
        for g in gs: print(json.dumps(Tk.report(g)), flush=True)
    elif cmd == "stills":
        out = sys.argv[4]; mode = sys.argv[5] if len(sys.argv) > 5 else "draft"; samples = int(sys.argv[6]) if len(sys.argv) > 6 else None
        os.makedirs(out, exist_ok=True)
        for g in gs:
            dt = Tk.render(g, os.path.join(out, "g_%04d.png" % g), mode, samples); print("g", g, "%.1fs" % dt, json.dumps(Tk.report(g)), flush=True)
    elif cmd == "final":
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 24; threads = int(sys.argv[5]) if len(sys.argv) > 5 else 2
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        for g in gs:
            png = os.path.join(out, "g_%04d.png" % g)
            if os.path.exists(png) and os.path.exists(png + ".ok"): continue
            dt = Tk.render(g, png, "final", samples, threads); open(png + ".ok", "w").write("%d %.1f" % (samples, dt))
            print("g", g, "%.1fs" % dt, flush=True)
