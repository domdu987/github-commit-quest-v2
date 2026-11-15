#!/usr/bin/env python3
"""shot.py -- film 9 take s18: shots 18-19 (plan 51.79 s .. end: g 1554..1766; in-handle g 1548..1553, no out-handle), the ending:
"ส่วนกำแพงของแม่ทัพ นัดแรกร้าว นัดที่สองร้าวทั้งแถว นัดที่สามพังลงมา พร้อมแม่ทัพที่ยังหัวเราะอยู่ข้างบน".
One location (wall_site, two_sections_out build, BATTLE: army, smoke, fires), three set-ups in one process:

    id 1  g 1548..1625  shot 18, from the field (between the cannon row and the wall), oblique onto the general's grey plain-mortar
          section (Lin's creamy section at the left edge): shot 1 hits on "นัดแรกร้าว" (52.96 s = g 1592) -> crater + star crack
          (set_cracks 0.33); shot 2 hits on "นัดที่สอง" (53.68 s = g 1613) -> the cracks race along the courses across the whole row
          (0.33 -> 0.66 by "ร้าวทั้งแถว" g 1632).  The general stands on top, arms akimbo, laughing.  Slow push + drift, a small
          camera kick on each hit.
    id 2  g 1626..1665  shot 19a, on top of his section (wall_top camera, +2 D for 30 courses): the general laughs, head thrown back;
          shot 3 hits below on "นัดที่สาม" (54.99 s = g 1653): flash + dust rise past the parapet, the camera shakes, he wobbles and keeps
          laughing; cracks 0.66 -> 1.
    id 3  g 1666..1766  shot 19b, wide from the field: the section collapses (set_collapse 0 -> 1, g 1660..1715) and the still-laughing
          general drops with the top, slides down the rubble mound toward us in the dust cloud, the helmet flies off over his shoulder
          (helmet_off 0 -> 1, g 1672..1690) and lands in the rubble beside him; he ends sitting in the dust, bare topknot, laughing
          (general_land) on "ที่ยังหัวเราะอยู่ข้างบน".  Lin's rice section stands whole at the left.  Cut on the last frame g 1766.
Mouths: no quote in shots 18-19 -> static mouths (laughing open grin held, no lip-sync).  Comic, no injury.  NO depth of field.

    python3 shot.py stills 1,2,3 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2|3 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

W, actors, camrig, cast9 = C.W, C.actors, C.camrig, C.cast9
lerp, clamp, blink, ez = C.lerp, C.clamp, C.blink, C.ez
TMP = os.path.join(HERE, "work")

G0 = C.g_bound(51.79)                                    # 1554
G_19 = C.g_bound(54.20)                                  # 1626
G_19B = 1666                                             # cut to the wide just before "พังลงมา" (g 1672)
G_LAST = 1766                                            # N - 1
H = 6
RANGES = {1: (G0 - H, G_19 - 1), 2: (G_19, G_19B - 1), 3: (G_19B, G_LAST)}

HIT = [C.g_of(52.96), C.g_of(53.68), C.g_of(54.99)]      # 1592, 1613, 1653
T_IMP = 46.0                                             # frames for set_impact t 0 -> 1; the hit is at t 0.35
G_COL = (1660, 1715)                                     # set_collapse 0 -> 1
TOP = Vector((5.4, 1.0, 16.0))                           # the general on his section's top (30 courses: top z 16)
SLIDE = [Vector(p) for p in [(5.4, 1.0, 16.0), (8.0, -1.5, 4.6), (8.4, -5.6, 1.6), (7.2, -11.4, 0.1)]]
G_DROP = (1666, 1692)                                    # through the air with the breaking top
G_SLIDE = (1692, 1714)                                   # down the rubble mound
G_HELM = (1672, 1690)
HELMET_AT = Vector((9.0, -10.8, 0.25))                   # where the helmet lies in the rubble (shown from g 1691)


def bf(shot, g):
    return 1000 * shot + int(g) - 1500


def imp_t(k, g):
    return clamp((g - (HIT[k] - 0.35 * T_IMP)) / T_IMP)


def cracks(g):
    if g < HIT[0]:
        return 0.0
    if g < HIT[1]:
        return 0.33 * ez((g - HIT[0]) / 8.0)
    if g < HIT[2]:
        return 0.33 + 0.33 * ez((g - HIT[1]) / 19.0)
    return 0.66 + 0.34 * ez((g - HIT[2]) / 7.0)


def collapse(g):
    return clamp((g - G_COL[0]) / float(G_COL[1] - G_COL[0]))


def kick(g, amp):
    """small camera shake after each hit (decaying)."""
    v = Vector((0.0, 0.0, 0.0))
    for h in HIT:
        d = g - h
        if 0 <= d < 14:
            a = amp * math.exp(-d / 4.0)
            v += Vector((a * math.sin(d * 2.3), 0.0, a * math.cos(d * 3.1)))
    return v


# ----------------------------------------------------------------------------- cameras
LENS = 20.0
CAM1 = (((3.0, -13.6, 2.1), (3.6, 0.0, 8.4)), ((5.2, -13.0, 2.3), (7.6, 0.0, 8.4)))
CAM2 = (((18.5, 2.6, 19.0), (1.0, 3.2, 16.6)), ((17.0, 2.9, 18.7), (1.0, 3.0, 16.5)))
CAM3 = (((2.4, -17.4, 2.6), (5.4, 0.0, 8.4)), ((4.8, -17.0, 3.4), (10.4, -3.0, 2.4)))


def cam_of(shot, g):
    a0, a1 = {1: CAM1, 2: CAM2, 3: CAM3}[shot]
    r0, r1 = RANGES[shot]
    x = (g - r0) / float(r1 - r0)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    if shot == 3:                                       # lead the general to his landing spot (pan done ~70 % by g 1712), still moving at the end
        u = 0.7 * (1.0 - (1.0 - x) ** 2.5) + 0.3 * x
    loc, look = Vector(lerp(a0[0], a1[0], u)), Vector(lerp(a0[1], a1[1], u))
    k = kick(g, {1: 0.06, 2: 0.16, 3: 0.0}[shot])
    return loc + k, look + k * 0.6


# ----------------------------------------------------------------------------- the general
def gen_where(shot, g):
    """feet point of the general."""
    if shot == 2:
        return Vector((8.0, 2.4, 16.0))                 # wall_top_battle staging mark general_top (from the field, shot 1 / 3, nearer the outer edge to read)
    if shot < 3 or g < G_DROP[0]:
        return TOP
    if g < G_DROP[1]:
        u = (g - G_DROP[0]) / float(G_DROP[1] - G_DROP[0])
        p = SLIDE[0].lerp(SLIDE[1], u)
        p.z = SLIDE[0].z + (SLIDE[1].z - SLIDE[0].z) * u * u + 1.0 * math.sin(math.pi * u) * (1 - u)   # a little hop, then drops
        return p
    if g < G_SLIDE[1]:
        u = ez((g - G_SLIDE[0]) / float(G_SLIDE[1] - G_SLIDE[0]), "sine") * 0.4 + 0.6 * (g - G_SLIDE[0]) / float(G_SLIDE[1] - G_SLIDE[0])
        s = u * 2.0
        return SLIDE[1].lerp(SLIDE[2], s) if s < 1 else SLIDE[2].lerp(SLIDE[3], s - 1)
    return SLIDE[3]


def gen_pose(shot, g):
    sh = 0.0
    for h in HIT:                                       # wobble on each hit
        d = g - h
        if 0 <= d < 18:
            sh += math.exp(-d / 5.0) * math.sin(d * 1.4)
    if shot < 3 or g < G_DROP[0]:
        p = dict(cast9.STORY9["general_wall_laugh"][1])
        p.update(head_roll=-12 + 4.0 * math.sin(g * 0.35) + 6.0 * sh, lean=-6 + 2.0 * math.sin(g * 0.31) + 5.0 * sh,
                 pitch=-0.9 + 0.08 * math.sin(g * 0.4), squash=(1.02 + 0.02 * math.sin(g * 0.7), 0.98 - 0.02 * math.sin(g * 0.7)))
        p["t"] = g / 30.0
        p["blink"] = 0
        return p
    if g < G_SLIDE[1]:
        p = dict(cast9.STORY9["general_fall"][1])
        p.update(expr="laughing", mouth="talk_b", fx=["tears"])          # still laughing (comic, no injury)
        p["helmet_off"] = clamp((g - G_HELM[0]) / float(G_HELM[1] - G_HELM[0])) if g >= G_HELM[0] else 0.0
        if 0 < p["helmet_off"] < 0.02:
            p["helmet_off"] = 0.02
        p["lie"] = 42 + 10 * math.sin(g * 0.45)
        p["head_roll"] = -14 + 6 * math.sin(g * 0.5)
        p["dust"] = clamp((g - G_DROP[0]) / 20.0) * 0.9
        a = 0.12 * math.sin(g * 0.9)                    # flailing arms
        p["arm_r"] = dict(p["arm_r"], hand=(0.78 + a, -0.55 - a))
        p["arm_l"] = dict(p["arm_l"], hand=(-0.7 - a, -0.6 + a))
        p["t"] = g / 30.0
        return p
    p = dict(cast9.STORY9["general_land"][1])
    q = (g - G_SLIDE[1])
    p.update(head_roll=-8 + 5.0 * math.sin(g * 0.33), pitch=-0.5 + 0.07 * math.sin(g * 0.41), lean=2.0 * math.sin(g * 0.27),
             dust=max(0.08, 0.35 - 0.02 * q), squash=(1.0 + 0.025 * math.sin(g * 0.66), 1.0 - 0.025 * math.sin(g * 0.66)))
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        self.preset = "wall_top_battle" if shot == 2 else "two_sections_out"     # one preset per build (final_loop rebuilds on change)
        C.Take.__init__(self, "wall_site", self.preset, quality=quality, lens=LENS, name="cam_s18", light="BATTLE")
        self.gen = self.actors["gen"] = C.make_actor("gen", "general", os.path.join(TMP, "sprites"), canvas=cast9.CANVAS9_FALL["general"])
        svg, top = cast9.helmet_svg("s18h", rot=104.0, yaw=0.2)
        png = C.svg_png(svg, (-1.1, -1.9, 1.1, 0.7), 220, os.path.join(TMP, "svg"))
        self.helm = C.PropCard("s18_helmet", [png], (-1.1, -1.9, 1.1, 0.7), scale=1.0, shadow=True, scene=self.scene)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS)
            W.set_wall_height("lin", 26, frame=f); W.set_wall_height("general", 30, frame=f)
            imps = [("lin", i, 1.0) for i in range(3)] + [("general", k, imp_t(k, g)) for k in range(3)]
            self.key_set(f, flames=1.0, smoke=1.0, army=True, impact=imps, collapse=collapse(g))
            W.set_cracks("general", cracks(g), frame=f); W.set_cracks("lin", 0.5, frame=f)
            p = gen_where(shot, g); C.place(self.gen, f, p, z=p.z)
            on = shot == 3 and g > G_HELM[1]
            self.helm.put(HELMET_AT + Vector((0, 0, 0.0)), face=loc, frame=f)
            self.helm.root.rotation_euler[1] = math.radians(8.0 * math.sin(g * 0.5) * math.exp(-max(0, g - G_HELM[1]) / 8.0))
            self.helm.root.keyframe_insert("rotation_euler", frame=f)
            self.helm.show(0 if on else None, frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.gen.pose(f, gen_pose(shot, g), camera=self.cam)
        self.sprites_for([(self.gen, {1: 160, 2: 320, 3: 192}[shot])], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), collapse=round(collapse(g), 3),
                    cracks=round(cracks(g), 3))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk, key = None, None
        for shot in shots:
            if key != (shot == 2):
                Tk, key = Take("preview", shot), (shot == 2)
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
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples,
                     take_key=lambda shot: 'top' if shot == 2 else 'out')
