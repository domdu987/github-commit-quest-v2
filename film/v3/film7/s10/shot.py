#!/usr/bin/env python3
"""shot.py -- film 7 take s10: shots 10-11 (plan 30.66-37.12 s = g 920..1113) + 6-frame handles (g 914..1119).

  shot 10 "paris street_wide DUSK -> louvre closet: night falls; vincenzo_hide_closet among brooms with a lantern"
    id 1  g 914..949   the rue at dusk (STREET_DUSK, papers 0): the gas lamps come on one after another (set_flames 0.15 -> 1.2),
                       a slow crane down the street toward the quai.                     ("คืนวันอาทิตย์")
    id 2  g 950..990   CUT into the storage closet (CLOSET_NIGHT): vincenzo crouched among brooms, mops, buckets and the smocks on
                       their pegs, a hand on the storm lantern, listening; slow push.     ("เขาแอบซ่อนตัวในตู้เก็บของ")
    id 3  g 991..1025  punch-in on his worried face in the lantern light; he glances at the door and holds his breath.
                       ("เพราะวันจันทร์") -- rendered past the shot end (to g 1025) for the dissolve.
  shot 11 "louvre gallery_wide: Monday: the empty museum, only workers in white smocks walking"
    id 4  g 1014..1062 DISSOLVE IN (10 frames, g 1015..1024, centred on the shot boundary g 1020): the empty salon from high in the
                       service-door corner, three workers in white smocks crossing the parquet, nobody else.  ("พิพิธภัณฑ์ปิด")
    id 5  g 1063..1119 lower and closer: two smocked workers walk past the lens toward her wall.  ("ใส่เสื้อคลุมขาวเดินกัน
                       ทั้งตึก"); g 1114..1119 = out-handle.
Nobody speaks: no lip-sync (static mouths).  NO depth of field (common.Take).  One location per process (Take per id group).
Blender frame = 1000*(id-1)+g+1.

    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2,3|4,5 a:b [scale] [samples]
"""
import math, os, sys, json, copy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7, sprites = C.L, C.actors, C.camrig, C.cast7, C.sprites
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
P = cast7.P if hasattr(cast7, "P") else __import__("puppet")
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(30.66), C.g_bound(37.12)          # 920, 1114
G11 = C.g_bound(34.00)                               # 1020
H = 6
DIS = (1015, 1024)                                   # dissolve closet -> gallery (10 frames centred on g 1020)
RANGES = {1: (G0 - H, 949), 2: (950, 990), 3: (991, DIS[1] + 1), 4: (DIS[0] - 1, 1062), 5: (1063, G1 + H - 1)}
LOC = {1: ("paris", "notre_dame_view"), 2: ("louvre", "closet"), 3: ("louvre", "closet"), 4: ("louvre", "gallery_wide"),
       5: ("louvre", "gallery_wide")}
KEY = {1: "street", 2: "closet", 3: "closet", 4: "gallery", 5: "gallery"}
G_LOOK = C.g_of(32.88)                               # 989 "เพราะวันจันทร์": glances at the door


# ----------------------------------------------------------------------------- white-smock workers (runtime cast copies)
def _smock_of(base, seed, cap=None):
    c = copy.deepcopy(P.CAST[base])
    vs = P.CAST["vincenzo_smock"]
    c.update(costume="smock7", smock_len=0.42 if base != "coworker2" else 0.34, smock_flare=0.10, pencil=False, seed=seed)
    c["sleeve"] = dict(vs["sleeve"])
    col = dict(c.get("colors", {}))
    col.update(base="#f4f2ec", smock="#f4f2ec", dark="#b8bccb", collar="#ffffff", button="#ffffff")
    c["colors"] = col
    if cap:
        c["hat_colors"] = dict(c.get("hat_colors", {}), **cap)
    return c


def register_workers():
    if "worker7_a" in P.CAST:
        return
    P.CAST["worker7_a"] = _smock_of("coworker1", 133.1)
    P.CAST["worker7_b"] = _smock_of("coworker2", 137.7)
    c = _smock_of("guard", 141.3)
    c.update(hat="newsboy", hat_style="flatcap", hat_tilt=2.0)
    c["hat_colors"] = dict(light="#8a7a6a", base="#5e5246", dark="#3a3028", shine="#aa9a88", visor="#4a4036", band="#3a3028")
    P.CAST["worker7_c"] = c
    for n, b in (("worker7_a", "coworker1"), ("worker7_b", "coworker2"), ("worker7_c", "guard")):
        sprites.DEFAULT_CANVAS[n] = sprites.DEFAULT_CANVAS[b]


# ----------------------------------------------------------------------------- cameras / staging
def cam_of(sid, g):
    if sid == 1:
        u = ez((g - RANGES[1][0]) / float(RANGES[1][1] - RANGES[1][0]))
        return (Vector(lerp((-1.3, 18.0, 6.4), (-1.1, 21.0, 5.0), u)), Vector(lerp((1.2, 60.0, 4.6), (1.4, 60.0, 3.6), u)), 22.0)
    if sid == 2:
        u = ez((g - RANGES[2][0]) / float(RANGES[2][1] - RANGES[2][0]))
        return (Vector(lerp((2.35, 0.22, 3.05), (2.15, 0.45, 2.95), u)), Vector(lerp((-1.0, 3.0, 1.55), (-0.9, 3.0, 1.55), u)), 20.0)
    if sid == 3:
        u = ez((g - RANGES[3][0]) / float(RANGES[3][1] - RANGES[3][0]))
        return (Vector(lerp((1.58, 0.24, 2.36), (1.52, 0.33, 2.36), u)), Vector(lerp((-0.05, 2.4, 1.72), (-0.05, 2.4, 1.72), u)), 22.0)
    if sid == 4:
        u = ez((g - RANGES[4][0]) / float(RANGES[4][1] - RANGES[4][0]))
        return (Vector(lerp((9.6, 1.6, 5.4), (9.3, 2.3, 5.0), u)), Vector(lerp((-3.0, 19.0, 3.2), (-3.2, 19.0, 3.3), u)), 20.0)
    u = ez((g - RANGES[5][0]) / float(RANGES[5][1] - RANGES[5][0]))
    return (Vector(lerp((3.3, 10.9, 2.55), (2.9, 12.0, 2.55), u)), Vector(lerp((-0.6, 18.0, 2.35), (-0.6, 19.0, 2.45), u)), 22.0)


VIN_HIDE = Vector((0.28, 1.42, 0.0))                 # crouched between the crates and the zinc bucket
LANTERN = Vector((0.75, 2.6, 1.28))

# gallery walkers: (cast, start xy, velocity per frame, phase offset)
WALK4 = {"w1": ("worker7_a", (-3.6, 9.0), (0.052, 0.006), 0.0),
         "w2": ("worker7_b", (5.4, 12.6), (-0.046, 0.004), 0.4),
         "w3": ("worker7_c", (4.0, 7.3), (-0.034, 0.036), 0.7)}
WALK5 = {"w1": ("worker7_a", (1.9, 13.4), (-0.016, 0.050), 0.1),
         "w2": ("worker7_b", (-1.3, 14.6), (0.006, 0.046), 0.55)}


def walker_xy(spec, g, g_start):
    cast, p0, v, ph = spec
    d = g - g_start
    return Vector((p0[0] + v[0] * d, p0[1] + v[1] * d, 0.0))


def walker_pose(spec, g, g_start, seed):
    cast, p0, v, ph = spec
    facing = 1 if v[0] >= 0 else -1
    away = v[1] > abs(v[0])                        # walking into the room (away from the lens)
    base = dict(expr="neutral" if seed % 2 else "smirk", yaw=0.55 if not away else 0.75, gaze=(0.6 * facing, 0.0), head_roll=2 * facing)
    p = cast7.cycle(cast, (g - g_start) / 28.0 + ph, "walk", facing=facing, base=base, arms="both", speed=0.8)
    p["blink"] = blink(g, [g_start + 9 + 7 * seed, g_start + 38 + 5 * seed])
    p["t"] = g / 30.0
    return p


def vin_pose_hide(g, sid):
    p = dict(cast7.STORY7["vincenzo_hide_closet"][1])
    p.pop("prop_r", None)
    p["sweat"] = 0.6
    if sid == 3 and g >= G_LOOK - 2:
        u = ez((g - (G_LOOK - 2)) / 5.0)
        p["gaze"] = (lerp(0.8, -0.85, u), lerp(0.0, -0.2, u))
        p["yaw"] = lerp(0.20, -0.05, u)
        p["expr"] = "worried" if g < G_LOOK + 2 else "stunned"
        p["pitch"] = lerp(0.20, 0.05, u)
    p["head_roll"] = p.get("head_roll", 0) + 1.0 * math.sin(g * 0.31)
    p["lean"] = p.get("lean", 0) + 1.0 * math.sin(g * 0.17)
    p["blink"] = blink(g, [962, 984, G_LOOK + 1, 1012])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        loc, preset = LOC[shot]
        C.Take.__init__(self, loc, preset, quality=quality, lens=22.0, name="cam_s10_%s" % KEY[shot])
        self.key = KEY[shot]
        sd = os.path.join(TMP, "sprites")
        if self.key == "closet":
            self.actors["vin"] = C.make_actor("vin", "vincenzo", sd)
        elif self.key == "gallery":
            register_workers()
            for n in ("w1", "w2", "w3"):
                self.actors[n] = C.make_actor(n, WALK4[n][0], sd)

    def pose(self, shot, gs):
        assert KEY[shot] == self.key
        S = self.scene
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            if self.key == "street":
                k = 0.15 + 1.05 * ez((g - RANGES[1][0]) / float(RANGES[1][1] - RANGES[1][0] - 6))
                self.key_set(f, flames=k, papers=0)
            elif self.key == "closet":
                self.key_set(f)
                C.place(self.actors["vin"], f, VIN_HIDE)
            else:
                self.key_set(f, mona=True)
                spec = WALK4 if shot == 4 else WALK5
                for n, a in self.actors.items():
                    if n in spec:
                        C.place(a, f, walker_xy(spec[n], g, RANGES[shot][0]))
                    else:
                        C.place(a, f, (30.0, 40.0, 0.0))
                    a.card.hide_render = n not in spec
                    a.card.keyframe_insert("hide_render", frame=f)
        self.info = {}
        for g in gs:
            f = bf(shot, g)
            S.frame_set(f)
            if self.key == "closet":
                hands = {"r": dict(hand=tuple(LANTERN + Vector((0.0, 0.0, 0.42))), layer="front", shape="fist")}
                _, info = self.actors["vin"].pose(f, vin_pose_hide(g, shot), hands=hands, camera=self.cam)
                self.info[g] = {k: round(v["error"], 3) for k, v in info.items()}
            elif self.key == "gallery":
                spec = WALK4 if shot == 4 else WALK5
                for i, (n, a) in enumerate(self.actors.items()):
                    if n in spec:
                        a.pose(f, walker_pose(spec[n], g, RANGES[shot][0], i), camera=self.cam)
                    else:
                        a.pose(f, walker_pose(WALK4[n], g, RANGES[shot][0], i), camera=self.cam)     # hidden
        fr = [bf(shot, g) for g in gs]
        if self.actors:
            ppd = {2: 320, 3: 448, 4: 192, 5: 288}[shot]
            self.sprites_for([(a, ppd) for a in self.actors.values()], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens,
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), hand_err=getattr(self, "info", {}).get(g))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        cache = {}
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            if cache.get("k") != KEY[shot]:
                cache["T"] = Take("preview", shot); cache["k"] = KEY[shot]
            Tk = cache["T"]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples,
                     take_key=lambda shot: KEY[shot])
