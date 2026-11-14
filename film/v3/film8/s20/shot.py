#!/usr/bin/env python3
"""shot.py -- film 8 take s20: shots 20 + 21, the ending (g 1661..1838: 6 in-handle frames g 1661..1666, then shot 20 g 1667..1751,
shot 21 g 1752..1838 = the last film frame; no out-handle).  "ส่วนพ่อค้าน้ำ ต้องควักเงิน ซื้อน้ำแข็งทั้งโดม ตามที่ลั่นวาจาไว้ว่า
'ข้าจะซื้อหมดเลย'".  One location (desert_ice plain, SUMMER, the channels baked to mud), two set-ups joined by the plan's cut at 58.40 s:

    id 20  g 1661..1751  shot 20, wide at the dome: the sweating merchant (heat shimmer, sweat) walks along the bank lane (y 8.8)
                         between the mud channels toward the yakhchal door, the heavy coin purse in his hand; behind him a queue of
                         townsfolk (woman with her water jar, the old man, the boy, a second woman fanning) follows in single file.
                         Farid waits at the porch door, arms folded, calm smile.  The camera trucks along with the queue (slow).
    id 21  g 1752..1838  shot 21, medium two-shot from the south (over the mud channel) looking north: merchant left, farid right in
                         front of the porch, the dome's stepped cone at the right edge.  The merchant holds out the purse, scratching
                         his turban, sheepish (blush, sweat); lip-sync "ข้าจะซื้อหมดเลย" g 1797..1827 only; farid calmly holds out
                         one ice block; they swap at g 1817 (block -> merchant, purse -> farid); the merchant looks at his single
                         block; hold to the end with a slow push.
Mouths: only the merchant, only g 1797..1827 (talk_mouth); elsewhere static expression mouths.
NO depth of field anywhere (client rule): C.Take switches it off at build and before every render.

    python3 shot.py probe 20,21 a:b[:step]
    python3 shot.py stills 20,21 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 20|21 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast8 = C.D, C.actors, C.camrig, C.cast8
lerp, clamp, blink, ez = C.lerp, C.clamp, C.blink, C.ez
TMP = os.path.join(HERE, "work")


def bf(shot, g):
    return 1000 * (shot - 19) + int(g) - 1600          # own frame blocks: id 20 -> 1061.., id 21 -> 2152..


# ----------------------------------------------------------------------------- timing
H_IN = 6
G0 = C.g_bound(55.57)              # 1667: shot 20 starts
G_CUT = C.g_bound(58.40)           # 1752: shot 21
G_LAST = 1838                      # last film frame (N = 1839)
RANGES = {20: (G0 - H_IN, G_CUT - 1), 21: (G_CUT, G_LAST)}
LOC = ("desert_ice", "dome_wide")
LIGHT = "SUMMER"
G_SAY = (C.g_of(59.79), C.g_of(60.8))          # 1797..1827 lip-sync "ข้าจะซื้อหมดเลย"
G_OUT = (G_SAY[0] + 1, G_SAY[0] + 15)          # farid holds the block out 1798..1812
G_SWAP = 1817                                  # props change hands
G_BACK = (G_SWAP + 1, G_SWAP + 13)             # hands come back 1818..1830

# ----------------------------------------------------------------------------- staging (world D; +x east, +y north)
LANE = 8.8                         # bank lane between channel 3 (y 7.4) and channel 4 (y 10.2): leads straight to the porch door
FARID_A = Vector((21.4, LANE, 0.0))
V_WALK = 0.052                     # D per frame along +x (merchant speed 0.75, 28-frame cycle)
MER_X0 = 12.9                      # merchant x at g 1661
QUEUE = [("woman", 2.05, 0.37), ("oldman", 3.95, 0.71), ("boy", 5.6, 0.12), ("woman2", 7.35, 0.55)]   # (who, gap behind merchant, phase)
MER_B = Vector((19.75, LANE, 0.0))
FARID_B = Vector((21.45, LANE, 0.0))
LENS = 22.0


def aim(loc, az, el, d=30.0):
    a, e = math.radians(az), math.radians(el)
    return tuple(loc[i] + d * v for i, v in enumerate((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))))


# set-up 20: south-west of the queue over the mud channels looking north-east: queue on the lane crossing the frame toward the porch,
# the dome cone filling the right half, palms + camel on the sand beyond.  Trucks east with the queue (slower than they walk).
CAM_A0 = (6.0, 1.6, 2.75); AZ_A0, EL_A0 = 52.0, 5.0
CAM_A1 = (7.8, 2.0, 2.7); AZ_A1, EL_A1 = 55.0, 5.5
# set-up 21: south of them over channel 3 looking north (a little east): merchant left, farid right, porch + cone right.
CAM_B0 = (19.9, 2.9, 2.45); AZ_B0, EL_B0 = 6.0, 3.5
CAM_B1 = (20.2, 3.6, 2.40); AZ_B1, EL_B1 = 9.0, 4.0
PPD = {20: 256, 21: 320}


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    if shot == 20:
        c0, c1, z0, z1, e0, e1 = CAM_A0, CAM_A1, AZ_A0, AZ_A1, EL_A0, EL_A1
    else:
        c0, c1, z0, z1, e0, e1 = CAM_B0, CAM_B1, AZ_B0, AZ_B1, EL_B0, EL_B1
    loc = Vector(lerp(c0, c1, u))
    return loc, Vector(aim(loc, lerp(z0, z1, u), lerp(e0, e1, u)))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


# ----------------------------------------------------------------------------- poses
def _walk(cast, g, ph0, base, speed=0.75, arms="both"):
    return cast8.cycle(cast, ph0 + (g - RANGES[20][0]) / 28.0, "walk", facing=1, base=base, arms=arms, speed=speed)


def pose_merchant_a(g):
    base = dict(expr="worried", sweat=1.0, heat=1.0, t=g / 30.0, prop_r="coin_purse", yaw=0.62, pitch=0.15, head_roll=-4,
                blink=blink(g, [1690, 1735]))
    p = _walk("merchant", g, 0.0, base, arms="l")
    p["arm_r"] = dict(hand=(0.62, 0.78 + 0.03 * math.sin(g * 0.45)), bend=0.4, stretch=1.05, layer="front")
    for k in ("sweat", "heat", "t", "prop_r"):
        p[k] = base[k]
    return p


def pose_town_a(who, g, ph):
    cast = "woman" if who.startswith("woman") else who
    if who == "woman":
        base = dict(expr="worried", prop_r="water_jar", jar_hold="shoulder", sweat=0.8, heat=0.5, t=g / 30.0, yaw=0.6)
        p = _walk(cast, g, ph, base, speed=0.72, arms="l")
        p["arm_r"] = dict(hand=(0.64, 0.10), bend=-0.6, stretch=1.25, layer="back")
    elif who == "woman2":
        base = dict(expr="worried", prop_r=dict(type="fan", angle=-75 + 25 * math.sin(g * 1.5)), sweat=1.0, heat=0.8, t=g / 30.0, yaw=0.6)
        p = _walk(cast, g, ph, base, speed=0.72, arms="l")
        p["arm_r"] = dict(hand=(0.46, 0.00), bend=-0.7, stretch=1.2)
    elif who == "oldman":
        base = dict(expr="unimpressed", prop_r=dict(type="stick", angle=95), sweat=1.0, heat=0.6, t=g / 30.0, yaw=0.6, lean=5)
        p = _walk(cast, g, ph, base, speed=0.7, arms="l")
        p["arm_r"] = dict(hand=(0.48, 0.70 + 0.04 * math.sin(g * 0.45)), bend=0.4)
    else:
        base = dict(expr="excited", sweat=0.6, heat=0.5, t=g / 30.0, yaw=0.6)
        p = _walk(cast, g, ph, base, speed=0.8)
    for k in ("sweat", "heat", "t", "jar_hold", "prop_r"):
        if k in base:
            p[k] = base[k]
    p["blink"] = blink(g, [1680 + int(ph * 40), 1725 + int(ph * 30)])
    return p


def pose_farid_a(g):
    p = dict(cast8.STORY8["farid_smile"][1])
    p.update(mirror=True, yaw=0.35, head_roll=-5 + 2.0 * math.sin(g * 0.11), lean=1.0 * math.sin(g * 0.08),
             gaze=(0.3 + 0.1 * math.sin(g * 0.07), 0.0), blink=blink(g, [1700, 1742]))
    return p


ICE_HOLD = (0.62, 0.62)            # farid's block hand (unmirrored figure: +x = toward the merchant after mirror)
ICE_OUT = (0.92, 0.50)
PURSE_HOLD = (0.78, 0.40)          # merchant's purse hand (merchant_pay)
PURSE_OUT = (0.96, 0.48)


def pose_merchant_b(g):
    p = dict(cast8.STORY8["merchant_pay"][1])
    out = u_of(g, G_SAY[0] - 6, G_SWAP - 2) * (1.0 - u_of(g, *G_BACK))
    back = u_of(g, *G_BACK)
    hx, hy = lerp(PURSE_HOLD, PURSE_OUT, out) if g < G_SWAP else lerp(PURSE_OUT, (0.62, 0.70), back)
    p["arm_r"] = dict(hand=(hx, hy + 0.025 * math.sin(g * 0.3)), bend=-0.4 if g < G_SWAP else lerp(-0.4, 0.3, back), stretch=1.3)
    p["prop_r"] = "coin_purse" if g < G_SWAP else "ice_block"
    scratch = 0.06 * math.sin(g * 0.9) * (1.0 - out)          # scratching the back of the turban
    p["arm_l"] = dict(hand=(-0.48 + scratch, -0.30 + 0.5 * scratch), bend=-0.9, stretch=1.2, layer="top")
    p["t"] = g / 30.0
    p["head_roll"] = 10 + 2.5 * math.sin(g * 0.13) - 6 * back
    p["lean"] = 4 + 1.2 * math.sin(g * 0.1)
    if g >= G_SWAP + 4:
        p["gaze"] = (0.5, 0.9)                             # looks down at his one block
        p["pitch"] = 0.45
        p["expr"] = "grinning" if g < 1828 else "worried"
    if G_SAY[0] <= g <= G_SAY[1]:
        p["mouth"] = cast8.talk_mouth(g, 1.0, seed=3.0)
    p["blink"] = blink(g, [1770, 1793, 1830])
    return p


def pose_farid_b(g):
    out = u_of(g, *G_OUT) * (1.0 - u_of(g, *G_BACK))
    back = u_of(g, *G_BACK)
    if g < G_SWAP:
        hx, hy = lerp(ICE_HOLD, ICE_OUT, out)
    else:
        hx, hy = lerp(ICE_OUT, (0.56, 0.78), back)
    p = dict(yaw=0.40, pitch=-0.15 + 0.05 * math.sin(g * 0.09), expr="smug" if g < G_SWAP + 3 else "happy", mouth="smile", mirror=True,
             head_roll=-5 + 2.0 * math.sin(g * 0.12), lean=1.0 * math.sin(g * 0.07), gaze=(0.7, 0.1),
             arm_r=dict(hand=(hx, hy + 0.02 * math.sin(g * 0.27)), bend=-0.3, stretch=1.25, layer="front"),
             arm_l=dict(hand=(-0.40, 0.98), bend=0.3), legs="stand")
    p["prop_r"] = "ice_block" if g < G_SWAP else "coin_purse"
    p["blink"] = blink(g, [1765, 1819])
    return p


# ----------------------------------------------------------------------------- runtime set dressing (never edits desert.py)
def dress():
    """SUMMER plain near the porch: a camel couched on the sand beyond the channels (the merchant's), date palms, water jars + a straw
    mat with ice blocks by the porch, rocks and shrubs, a donkey far away."""
    S = D.STATE; M = S['M']; mb = D.MB()
    camel = D.MB()

    def beast(c, s=1.0, rot=0.0, couched=True, seed=0):
        ca, sa = math.cos(rot), math.sin(rot)
        P = lambda x, y, z: Vector((c[0] + s * (x * ca - y * sa), c[1] + s * (x * sa + y * ca), s * z))
        z0 = 0.0 if couched else 1.4
        D.lumpy(camel, P(0, 0, z0 + 0.75), 1.05, M['terra_l'], 900 + seed, seg=12, rings=6, rough=0.05, squash=0.55)
        D.lumpy(camel, P(0.05, 0, z0 + 1.3), 0.55, M['terra_l'], 910 + seed, seg=10, rings=5, rough=0.05, squash=0.9)
        D.chain_rod(camel, [P(0.9, 0, z0 + 0.9), P(1.35, 0, z0 + 1.5), P(1.55, 0, z0 + 2.2)], 0.17 * s, M['terra_l'])
        D.lumpy(camel, P(1.75, 0, z0 + 2.25), 0.26, M['terra_l'], 920 + seed, seg=8, rings=4, rough=0.05, squash=0.7)
        if couched:
            for dx in (-0.7, 0.7):
                for dy in (-0.45, 0.45):
                    D.lumpy(camel, P(dx, dy, 0.18), 0.3, M['terra_l'], 930 + seed, seg=8, rings=4, rough=0.05, squash=0.5)
        else:
            for dx in (-0.6, 0.6):
                for dy in (-0.3, 0.3):
                    D.rod(camel, P(dx, dy, 0), P(dx, dy, z0 + 0.4), 0.09 * s, M['terra_l'])
        # saddle cloth + bags
        D.lumpy(camel, P(0.0, 0, z0 + 1.55), 0.55, M['red'], 940 + seed, seg=8, rings=4, rough=0.0, squash=0.35)
        for dy in (-0.75, 0.75):
            D.lumpy(camel, P(-0.2, dy, z0 + 0.95), 0.38, M['kilim'][0], 950 + seed, seg=8, rings=4, rough=0.1, squash=1.1)

    beast((14.8, 16.6), 1.0, rot=math.radians(-15), couched=True, seed=1)
    beast((-2.0, 34.0), 0.9, rot=math.radians(170), couched=False, seed=2)
    beast((2.0, 37.0), 0.85, rot=math.radians(170), couched=False, seed=3)
    for k, (x, y, h) in enumerate(((19.0, 19.5, 7.0), (28.0, 18.5, 8.0), (9.5, 21.0, 6.5), (31.5, 22.0, 7.5))):
        D._palm(mb, (x, y, 0), M, h=h, seed=40 + k)
    # by the porch, on the sand north of channel 5 and on the porch's north side
    for k, (x, y, h) in enumerate(((22.6, 15.0, 1.5), (23.5, 15.4, 1.2), (21.6, 15.6, 1.3))):
        D._jar(mb, (x, y, 0), M, h=h, r=0.45, seed=k)
    mb.box((24.2, 14.6, 0), (26.6, 16.0, 0.04), M['mat'], tile=(2, 2))
    for (x, y, z) in ((24.4, 14.75, 0.04), (25.4, 14.75, 0.04), (24.9, 14.75, 0.64)):
        mb.box((x, y, z), (x + 0.9, y + 0.8, z + 0.6), M['ice_block'])
    for k, (x, y) in enumerate(((17.5, 15.0), (11.0, 15.5), (27.5, 15.4), (6.0, 16.0), (20.5, 22.0))):
        D._shrub(mb, (x, y, 0), M, 60 + k, s=0.9)
    r = D._rnd(77)
    for k in range(14):
        x, y = r.uniform(0, 30), r.uniform(15.0, 26.0)
        D.lumpy(mb, (x, y, 0.05), r.uniform(0.15, 0.4), M['rock'], 960 + k, seg=8, rings=4, rough=0.3, squash=0.6)
    ob = D._obj(mb, 's20_dress', S['SET'], hull=0.015)
    ob2 = D._obj(camel, 's20_camels', S['SET'], hull=0.015)
    return ob, ob2


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=20):
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=LENS, name="cam_s20", light=LIGHT)
        dress()
        sd = os.path.join(TMP, "sprites")
        self.mer = self.actors["mer"] = C.make_actor("mer", "merchant", sd)
        self.far = self.actors["far"] = C.make_actor("far", "farid", sd)
        self.town = {}
        for who, gap, ph in QUEUE:
            cast = "woman" if who.startswith("woman") else who
            self.town[who] = self.actors[who] = C.make_actor(who, cast, sd)

    def mer_x(self, g):
        return MER_X0 + V_WALK * (g - RANGES[20][0])

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS)
            self.key_set(f, ice="mud")
            if shot == 20:
                mx = self.mer_x(g)
                C.place(self.mer, f, (mx, LANE, 0.0))
                C.place(self.far, f, FARID_A)
                for who, gap, ph in QUEUE:
                    a = self.town[who]
                    C.place(a, f, (mx - gap, LANE, 0.0))
                    a.card.hide_render = False; a.card.keyframe_insert("hide_render", frame=f)
            else:
                C.place(self.mer, f, MER_B)
                C.place(self.far, f, FARID_B)
                for who, gap, ph in QUEUE:      # the queue waits further back along the lane (off frame left / behind)
                    a = self.town[who]
                    C.place(a, f, (MER_B.x - 1.6 - gap, LANE, 0.0))
                    a.card.hide_render = True; a.card.keyframe_insert("hide_render", frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 20:
                self.mer.pose(f, pose_merchant_a(g), camera=self.cam)
                self.far.pose(f, pose_farid_a(g), camera=self.cam)
                for who, gap, ph in QUEUE:
                    self.town[who].pose(f, pose_town_a(who, g, ph), camera=self.cam)
            else:
                self.mer.pose(f, pose_merchant_b(g), camera=self.cam)
                self.far.pose(f, pose_farid_b(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        jobs = [(self.mer, PPD[shot]), (self.far, PPD[shot])]
        if shot == 20:
            jobs += [(self.town[w], PPD[shot]) for w, _, _ in QUEUE]
        self.sprites_for(jobs, fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

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
                    out = sys.argv[4]
                    os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
