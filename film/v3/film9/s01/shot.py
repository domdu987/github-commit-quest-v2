#!/usr/bin/env python3
"""shot.py -- film 9 take s01: shots 1 + 2 (plan 0.00-3.62 s = g 0..108) + 6 out-handle frames g 109..114.  The hook:
"this mason boils sticky rice in a giant pot, then pours it into the mortar of the city wall".
One location (wall_site, DAY, lin 18 / general 21 courses, cauldron steam), three set-ups in one process:

    id 1  g 0..53     shot 1, `cauldron` (preset camera, slow push + orbit): Lin on his platform stirs the giant steaming wok of
                      milky rice soup with the big paddle (hands on a small ellipse, paddle angle sweeping).
    id 2  g 54..81    shot 2a, `pour_close` (preset camera, the client-approved shot-2 set-up, slow push): Lin at his rice-mortar
                      trough tips a bucket of milky rice soup into the lime mortar ("แล้วเทลงไปใน" 1.84 s).
    id 3  g 82..114   shot 2b (cut on "ปูนก่อ" 2.64 s = g 82): medium from the site side along Lin's rice-mortar section: Lin at the
                      foot of the wall trowels the creamy mortar into the joints between the bricks ("กำแพงเมือง" 2.99 s).  g 109..114
                      = out-handle (the trowelling and the move continue).
No quote in shots 1-2: no lip-sync, static expression mouths.  NO depth of field (client rule; c9.Take switches it off).

    python3 shot.py probe 1,2,3 a:b[:step]
    python3 shot.py stills 1,2,3 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2|3 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402  (paths, cast9 first, bpy, wall, stage)
from mathutils import Vector                             # noqa: E402

W, actors, camrig, cast9 = C.B, C.actors, C.camrig, C.cast9
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G_S2 = C.g_bound(1.80)             # 54: shot 2 starts
G_CUT = C.g_of(2.64)               # 82: "ปูนก่อ" -> cut to the trowelling
G_END = C.g_bound(3.62)            # 109: shot 3 (other take) starts
H_OUT = 6
RANGES = {1: (0, G_S2 - 1), 2: (G_S2, G_CUT - 1), 3: (G_CUT, G_END + H_OUT - 1)}
LOC = ("wall_site", "cauldron")
LIGHT = "DAY"

# ----------------------------------------------------------------------------- staging
LIN_STIR = None                    # from A['marks'] (platform, z 1.5)
LIN_TROUGH = Vector((-5.2, 11.2, 0.0))
LIN_WALL = Vector((-6.0, 6.3, 0.0))     # at the foot of Lin's section (inner face y 5), trowelling the low courses

CAM = {
    1: (((-9.0, 20.8, 6.1), (-13.3, 12.7, 3.1)), ((-9.9, 19.6, 5.7), (-13.5, 12.8, 3.0)), 24.0),
    2: (((-0.4, 12.9, 3.6), (-5.4, 10.6, 1.6)), ((-1.0, 12.7, 3.35), (-5.4, 10.55, 1.55)), 24.0),
    3: (((-10.2, 9.0, 2.5), (-5.6, 5.3, 2.0)), ((-9.5, 8.6, 2.45), (-5.5, 5.3, 2.0)), 24.0),
}
PPD = {1: 256, 2: 320, 3: 320}


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    (l0, k0), (l1, k1), lens = CAM[shot]
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u)), lens


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


# ----------------------------------------------------------------------------- poses
STIR = cast9.STORY9["lin_stir"][1]
POUR = cast9.STORY9["lin_pour"][1]
TROW = cast9.STORY9["lin_trowel"][1]


def pose_stir(g):
    p = json.loads(json.dumps(STIR))
    ph = 2 * math.pi * g / 24.0
    dx, dy = 0.12 * math.cos(ph), 0.05 * math.sin(ph)
    p["arm_l"]["hand"] = (0.36 + dx, 0.10 + dy)
    p["prop_l"]["angle"] = 58 + 8 * math.sin(ph)
    p["lean"] = 8 + 4 * math.cos(ph)
    p["head_roll"] = -4 + 2 * math.sin(ph + 0.6)
    p["blink"] = blink(g, [22, 47])
    p["t"] = g / 30.0
    p["paddle_soup"] = 1.0
    return p


def pose_pour(g):
    """mirrored (the trough is screen-left of him from the pour_close camera)."""
    p = json.loads(json.dumps(POUR))
    a, b = RANGES[2]
    tip = u_of(g, a, a + 9)
    p["pour"] = lerp(0.35, 0.95, tip) + 0.04 * math.sin(g * 0.4)
    p["bucket_water"] = 1.0 - 0.8 * u_of(g, a + 6, b)
    p["pour_len"] = 1.4
    p["lean"] = 14 + 3 * tip + 1.2 * math.sin(g * 0.23)
    p["head_roll"] = -4 + 1.5 * math.sin(g * 0.17)
    p["blink"] = blink(g, [70])
    p["t"] = g / 30.0
    return p


def pose_trowel(g):
    p = json.loads(json.dumps(TROW))
    a = RANGES[3][0]
    ph = 2 * math.pi * (g - a) / 16.0
    s = 0.5 + 0.5 * math.sin(ph)
    p["arm_r"]["hand"] = (lerp(0.62, 0.95, s), 0.50 + 0.05 * math.cos(ph))
    p["prop_r"]["angle"] = 10 - 10 * math.cos(ph)
    p["prop_r"]["scale"] = 1.8
    p["lean"] = 14 + 2.5 * math.sin(ph)
    p["head_roll"] = -4 + 1.5 * math.sin(ph * 0.5)
    p["gaze"] = (0.6 + 0.15 * s, 0.75)
    p["trowel_mortar"] = 1.0 - 0.6 * s
    p["blink"] = blink(g, [100])
    p["t"] = g / 30.0
    return p


POSE = {1: pose_stir, 2: pose_pour, 3: pose_trowel}


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=22.0, name="cam_s01", light=LIGHT)
        global LIN_STIR
        LIN_STIR = Vector(self.A["marks"]["lin_stir"])
        self.lin = self.actors["lin"] = C.make_actor("lin", "lin", os.path.join(TMP, "sprites"))

    def feet(self, shot):
        return {1: LIN_STIR, 2: LIN_TROUGH, 3: LIN_WALL}[shot]

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            ft = self.feet(shot)
            C.place(self.lin, f, (ft.x, ft.y), z=ft.z, flip=shot in (1, 2))   # wok / trough are screen-left of him
            self.key_set(f, steam=0.75 if shot == 1 else 1.0, heights=(18, 21))
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.lin.pose(f, POSE[shot](g), camera=self.cam)
        self.sprites_for([(self.lin, PPD[shot])], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
