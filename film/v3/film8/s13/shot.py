#!/usr/bin/env python3
"""shot.py -- film 8 take s13: shots 13 + 14 (g 964..1173, in-handle g 958..963, out-handle g 1174..1179), the false ending:
"until one day he overslept; the ice in the channels melted into mud by noon; the merchant laughed to tears:
'See? There's no ice in the desert!'".  One location (desert_ice plain, NOON, channels keyed 'mud' every frame), two set-ups
joined by the plan's cut at 35.50 s:

    id 1  g 958..1064  shot 13: farid asleep on his back in the wall's shade at its foot (smiling, zzz), a bucket, a jar and his
                       saw beside him, the muddy channels in front.  On "เขาตื่นสาย" (32.75 s = g 985) he jolts up (lie 90 -> 0 in
                       5 frames), shocked + pale + sweat, hands flying to his head, then stares at the mud.  The camera starts
                       low and close and cranes up + back + pans left the whole set-up, ending high over the five channels of mud
                       running to the yakhchal (the plan's channels_wide view at noon).
    id 2  g 1065..1179 shot 14: medium on the merchant standing on the bank between channels 3 and 4, the mud in front, the
                       dome behind; farid small in the background on the next bank, head hanging.  He laughs big (head back),
                       bends over laughing to tears (cry, tears, slaps his knee); straightens a little and points at the mud for
                       the quote "เห็นมั้ย ทะเลทรายไม่มีน้ำแข็งหรอก!" (37.0-38.9 s = g 1113..1170: lip-sync from the narration
                       envelope), back into the laugh on "หรอก!".  Slow push in + slight orbit.  Handle g 1174..1179 rendered in 3D.
Mouths move only inside the quote (g 1113..1170, merchant).  NO depth of field anywhere (client rule).

Blender frame of (id, g) = 1000 * (id - 1) + g + 1.
    python3 shot.py probe 1,2 a:b[:step]
    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json, wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
import numpy as np                                       # noqa: E402

D, actors, camrig, cast8 = C.D, C.actors, C.camrig, C.cast8
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0 = C.g_bound(32.12)              # 964 shot 13
G_CUT = C.g_bound(35.50)           # 1065 shot 14
G_END = C.g_bound(39.14)           # 1174 shot 15 starts
H = 6
RANGES = {1: (G0 - H, G_CUT - 1), 2: (G_CUT, G_END + H - 1)}
LOC = ("desert_ice", "channels_wide")
LIGHT = "NOON"
G_WAKE = C.g_of(32.75)             # 985 "เขาตื่นสาย": up by here
G_JOLT = (G_WAKE - 5, G_WAKE)      # 980..985 lie 90 -> 0
G_MELT = C.g_of(33.38)             # 1004 "น้ำแข็งในร่องละลาย": hands to the head, stares at the mud
G_TEARS = C.g_of(35.96)            # 1082 "หัวเราะจนน้ำตาไหล": bends over laughing to tears
G_Q0, G_Q1 = C.g_of(37.0), C.g_of(38.9)   # 1113..1170 the quote (lip-sync)
G_HOR = C.g_of(38.74)              # 1165 "หรอก!"

# ----------------------------------------------------------------------------- staging (world D; +x east, +y north; wall north face y -0.8)
FARID_A = Vector((3.0, 0.15, 0.0))       # asleep at the wall foot, in its shade
MERCH = Vector((-1.0, 11.6, 0.0))        # bank lane between channel 4 (y 10.2) and 5 (y 13.0): no lantern post near
FARID_B = Vector((11.0, 14.6, 0.0))       # shot 14 background: the north bank beyond channel 5, small, screen-left of the merchant
SUN_ELEV = 70.0                          # runtime: noon sun raised 44 -> 70 deg so the wall's shadow ends at y ~4.7: farid sleeps in the
                                         # shade, the mud in channels 3-5 and the merchant are in the blazing sun
LENS = 22.0


def aim(loc, az, el, d=30.0):
    a, e = math.radians(az), math.radians(el)
    return tuple(loc[i] + d * v for i, v in enumerate((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))))


# set-up 1: low and close north-west of him looking south-east at the sleeper (wall behind), crane up + back + pan left to the
# channels running east to the dome.
CAM_A0 = ((-3.5, 5.0, 1.6), aim((-3.5, 5.0, 1.6), 116.0, -8.0))
CAM_A1 = ((-12.0, 6.2, 6.2), aim((-12.0, 6.2, 6.2), 101.0, -12.5))
# set-up 2: medium on the merchant from the west-north-west over channel 4, looking east-south-east: dome behind, wall right.
CAM_B0 = ((-6.5, 13.6, 2.75), aim((-6.5, 13.6, 2.75), 105.0, -2.0))
CAM_B1 = ((-5.4, 13.75, 2.7), aim((-5.4, 13.75, 2.7), 107.5, -2.5))
PPD = {1: 256, 2: 320}
CANVAS_FAR = (-2.25, -4.5, 2.25, 0.25)    # farid standing + lying (CANVAS8_LIE) in one card


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    a0, a1 = (CAM_A0, CAM_A1) if shot == 1 else (CAM_B0, CAM_B1)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector(lerp(a0[0], a1[0], u)), Vector(lerp(a0[1], a1[1], u))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


# ----------------------------------------------------------------------------- lip-sync level from the narration
def _envelope():
    w = wave.open(C.NARRATION)
    n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
    a = np.frombuffer(w.readframes(n), dtype={2: np.int16, 4: np.int32}[sw]).astype(np.float32)
    a = a.reshape(-1, ch).mean(axis=1) / float(2 ** (8 * sw - 1))
    hop = sr // 30
    rms = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2)) for i in range(len(a) // hop)])
    return rms / max(1e-6, np.percentile(rms[rms > 0], 95))


ENV = None


def talk_level(g):
    """loudness of the narration at film frame g (narration plays at +0.10 s: sample index = g - 3)."""
    global ENV
    if ENV is None:
        ENV = _envelope()
    i = g - 3
    return float(clamp(ENV[i] * 1.3)) if 0 <= i < len(ENV) else 0.0


# ----------------------------------------------------------------------------- poses
SLEEP = cast8.STORY8["farid_sleep"][1]
SHOCK = cast8.STORY8["farid_wake_shocked"][1]
LAUGH = cast8.STORY8["merchant_laugh"][1]
TEARS = cast8.STORY8["merchant_tears"][1]


def pose_farid_a(g):
    if g < G_JOLT[0]:
        p = dict(SLEEP)
        br = math.sin(g * 0.21)                                   # slow breathing
        p.update(squash=(1.0 + 0.012 * br, 1.0 - 0.012 * br), t=g / 30.0, pitch=-0.2 + 0.04 * br)
        return p
    j = u_of(g, *G_JOLT)
    p = dict(SHOCK)
    look = u_of(g, G_MELT - 8, G_MELT + 4)                         # turns to stare at the mud (screen-left, the channels)
    p["lie"] = 90.0 * (1.0 - j)
    p["yaw"] = lerp(0.2, -0.45, look) + 0.05 * math.sin(g * 0.37)
    p["gaze"] = (lerp(0.0, -0.7, look), lerp(-0.2, 0.25, look))
    p["pitch"] = lerp(-0.4, 0.15, look)
    trem = 0.02 * math.sin(g * 1.9)
    hands = u_of(g, G_MELT - 4, G_MELT + 6)
    p["arm_r"] = dict(SHOCK["arm_r"], hand=(lerp(0.40, 0.30, hands) + trem, lerp(-0.18, -0.42, hands)))
    p["arm_l"] = dict(SHOCK["arm_l"], hand=(lerp(-0.40, -0.30, hands) - trem, lerp(-0.16, -0.42, hands)))
    p["head_roll"] = 6 - 10 * look + 2.0 * math.sin(g * 0.29)
    p["lean"] = -4 + 3 * look
    s = 1.0 + 0.06 * math.sin(math.pi * clamp((g - G_JOLT[0]) / 9.0))          # a pop of stretch on the jolt
    p["squash"] = (2.0 - s, s)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [1030, 1052])
    return p


def pose_merchant(g):
    """laugh (head back) -> bent over laughing to tears -> straighter, pointing at the mud for the quote -> laugh on 'หรอก!'."""
    tears = u_of(g, G_TEARS - 6, G_TEARS + 6)
    point = u_of(g, G_Q0 - 6, G_Q0 + 4) * (1.0 - u_of(g, G_HOR - 3, G_HOR + 5))
    shake = math.sin(g * 1.15)
    p = dict(LAUGH) if tears < 0.5 else dict(TEARS)
    p["pitch"] = lerp(-0.8, -0.2, tears) + 0.25 * point + 0.05 * shake
    p["head_roll"] = lerp(-10, 14, tears) - 10 * point + 3 * shake
    p["lean"] = lerp(-8, 12, tears) - 7 * point + 1.5 * shake
    p["yaw"] = lerp(0.2, 0.3, tears) + 0.08 * point
    p["squash"] = (1.0 + 0.015 * shake, 1.0 - 0.015 * shake)
    p["t"] = g / 30.0
    if tears > 0.0:
        p["cry"] = tears
        p["fx"] = ["tears"]
    else:
        p.pop("cry", None); p.pop("fx", None)
    p["expr"] = "laughing"
    p["blink"] = 2 if tears >= 0.5 and point < 0.5 else 0
    slap = 0.10 * max(0.0, math.sin(g * 0.62))                    # the right hand slaps the knee / belly with the laugh
    if point > 0.0:
        p["arm_r"] = dict(hand=(lerp(0.62, 1.05, point), lerp(1.42, 0.55, point) - slap * (1 - point)), bend=lerp(0.5, -0.4, point),
                          shape="point" if point > 0.5 else "open", stretch=1.3)
    elif tears >= 0.5:
        p["arm_r"] = dict(TEARS["arm_r"], hand=(0.62, 1.42 - slap))
    else:
        p["arm_r"] = dict(LAUGH["arm_r"], hand=(0.36, 0.95 - 0.5 * slap))
    if G_Q0 <= g <= G_Q1:
        p["mouth"] = cast8.talk_mouth(g, talk_level(g), seed=3.0, hold=2)
        p["blink"] = 0 if point > 0.5 else p["blink"]
        if point > 0.5:
            p["expr"] = "grinning"                                 # eyes open while he points ('laughing' closes them)
    else:
        p["mouth"] = "talk_b"                                      # the laughing mouth, static (no lip motion outside the quote)
    return p


def pose_farid_b(g):
    return dict(yaw=0.3, pitch=0.35, expr="sad", gaze=(0.4, 0.4), head_roll=-4 + 1.5 * math.sin(g * 0.11), lean=4,
                arm_r=dict(hand=(0.30, 1.05), bend=0.2), arm_l=dict(hand=(-0.30, 1.05), bend=0.2), legs="stand",
                blink=blink(g, [1092, 1140]), pale=0.4, sweat=0.6, t=g / 30.0)


# ----------------------------------------------------------------------------- runtime set dressing
def dress():
    """props round the sleeper and along the banks (desert is sparse): his bucket, a jar, a straw mat under him, rocks at the wall
    foot, tools, a pile of mud bricks, palms and shrubs beyond the channels."""
    S = D.STATE; M = S['M']; mb = D.MB()
    mb.box((FARID_A.x - 2.0, FARID_A.y - 0.45, 0.0), (FARID_A.x + 2.0, FARID_A.y + 0.55, 0.03), M['mat'])
    D._bucket(mb, (FARID_A.x + 2.6, 0.35, 0.0), M, s=0.62)
    D._jar(mb, (FARID_A.x - 2.7, -0.2, 0.0), M, h=1.2, r=0.4, seed=3)
    D._jar(mb, (FARID_A.x + 3.4, -0.25, 0.0), M, h=0.9, r=0.32, mat=M['terra_l'], seed=4)
    D.beam(mb, (FARID_A.x + 1.2, 0.55, 0.05), (FARID_A.x + 2.0, 0.62, 0.05), 0.18, 0.03, M['iron'])             # the saw blade
    D.beam(mb, (FARID_A.x + 0.95, 0.53, 0.06), (FARID_A.x + 1.2, 0.55, 0.06), 0.07, 0.07, M['wood'])
    D.rod(mb, (0.2, 0.55, 0.05), (1.2, 0.35, 0.12), 0.04, M['wood'])                                             # the pick, dropped
    for k in range(9):                                                                                            # mud bricks
        x = 8.0 + 0.48 * (k % 3); z = 0.17 * (k // 3)
        mb.box((x, -0.55, z), (x + 0.44, -0.1, z + 0.16), M['mudbrick'])
    for k, (x, y, r) in enumerate(((-4.5, 0.0, 0.35), (0.6, -0.2, 0.25), (6.6, 0.1, 0.3), (12.0, -0.1, 0.4), (-8.0, 0.2, 0.3))):
        D.lumpy(mb, (x, y, 0.1), r, M['rock'], 900 + k, seg=8, rings=4, rough=0.3, squash=0.6)
    ob = D._obj(mb, 's13_dress', S['SET'], hull=0.012); D.no_bounce(ob)
    pb = D.MB()
    for k, (x, y, h) in enumerate(((-6.0, 17.5, 7.5), (-2.5, 19.0, 6.5), (3.5, 17.2, 8.0), (9.0, 18.5, 7.0), (16.0, 17.0, 7.5), (-12.0, 16.5, 7.0))):
        D._palm(pb, (x, y, 0.0), M, h=h, seed=50 + k)
    for k, (x, y) in enumerate(((-4.0, 15.6), (1.0, 16.0), (7.5, 15.4), (13.0, 16.2), (20.0, 15.8))):
        D._shrub(pb, (x, y, 0.0), M, 60 + k, s=1.1)
    ob2 = D._obj(pb, 's13_palms', S['SET'], hull=0.012); D.no_bounce(ob2)
    return ob


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=LENS, name="cam_s13", light=LIGHT)
        self.far = self.actors["far"] = C.make_actor("far", "farid", os.path.join(TMP, "sprites_far"), canvas=CANVAS_FAR)
        self.mer = self.actors["mer"] = C.make_actor("mer", "merchant", os.path.join(TMP, "sprites_mer"))
        dress()
        D.STATE['sun'].rotation_euler = (-Vector(D.G._kd((0.18, 0.98), SUN_ELEV))).to_track_quat('Z', 'Y').to_euler()

    def pose(self, shot, gs):
        far, mer = self.far, self.mer
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS)
            C.place(far, f, FARID_A if shot == 1 else FARID_B)
            C.place(mer, f, MERCH)
            mer.card.hide_render = shot == 1; mer.card.keyframe_insert("hide_render", frame=f)
            self.key_set(f, ice="mud")
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            far.pose(f, pose_farid_a(g) if shot == 1 else pose_farid_b(g), camera=self.cam)
            if shot == 2:
                mer.pose(f, pose_merchant(g), camera=self.cam)
        fs = [bf(shot, g) for g in gs]
        jobs = [(far, PPD[shot] if shot == 1 else 256)] + ([(mer, PPD[shot])] if shot == 2 else [])
        self.sprites_for(jobs, fs)

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
