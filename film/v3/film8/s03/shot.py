#!/usr/bin/env python3
"""shot.py -- film 8 take s03: shots 3-7 (g 178..607, plan 5.92-20.28 s) + handles (in g 172..177, out g 608..613), the bazaar at
NOON.  One location (bazaar, NOON light), five set-ups in one build (internal id = plan shot number):

    id 3  g 172..257  shot 3, bazaar_wide CRANE DOWN: high over the south end of the street, descending to the preset height while
                      pushing in: both brick arcades, awnings and goods, lantern strings, the merchant's stall (right), the square,
                      the iwan with its turquoise dome in blazing sun.  Townsfolk cross the street (woman with a jar, the boy runs,
                      the old man with his stick).  Dissolve in from the desert night (g 172..177 = in-handle, the crane continues).
    id 4  g 258..357  shot 4, well_eye: the woman and the old man fan themselves sweating by the tiled well, the boy hops from
                      foot to foot on the burning ground ("ทรายลวกเท้า" 10.79-11.93 s).  Slow push + orbit.
    id 5  g 358..431  shot 5, merchant_stall: the rich water merchant on his takht among the giant jars, laughing big ("หัวเราะลั่น"
                      13.33-14.37 s), farid stands calm in front of the stall.  Slow push in.
    id 6  g 432..540  shot 6, LOW MEDIUM TWO-SHOT from the west side of the street: the merchant (left, up on his takht) points down
                      and mocks farid; LIP-SYNC 14.4-17.9 s (g 435..540) driven by the narration envelope; farid (right) calm, arms
                      folded, a small smile and a slow blink.  Slow orbit.
    id 7  g 541..613  shot 7, bazaar wide from street level: farid walks calmly through the street while the townsfolk on both sides
                      point and laugh "ไอ้บ้าน้ำแข็ง" (19.36-20.25 s); the merchant laughs on his takht.  Slow push.  Out-handle 608..613.
Mouths move only in the merchant quote (shot 6).  Everyone else: static expression mouths (laughing grins are static).
NO depth of field anywhere (client rule).

Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 3,4 a:b[:step]
    python3 shot.py stills 3,4 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 3|4|.. a:b[:step] [scale] [samples]
"""
import math, os, sys, json, wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402  (paths, cast8 first, bpy, desert, stage)
from mathutils import Vector                             # noqa: E402
import numpy as np                                       # noqa: E402

D, actors, camrig, cast8 = C.D, C.actors, C.camrig, C.cast8
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
ST = cast8.STORY8

# ----------------------------------------------------------------------------- timing
G0, G1 = C.g_bound(5.92), C.g_bound(20.28)             # 178, 608
H_IN, H_OUT = 6, 6
B4, B5, B6, B7 = C.g_bound(8.60), C.g_bound(11.94), C.g_bound(14.40), C.g_bound(18.04)   # 258, 358, 432, 541
RANGES = {3: (G0 - H_IN, B4 - 1), 4: (B4, B5 - 1), 5: (B5, B6 - 1), 6: (B6, B7 - 1), 7: (B7, G1 + H_OUT - 1)}
LOC = ("bazaar", "bazaar_wide")
LIGHT = "NOON"
TALK = (C.g_of(14.4), C.g_of(17.9))                    # 435..540 merchant quote (lip-sync)
G_HOT = (C.g_of(10.79), C.g_of(11.93))                 # 327..361 "ทรายลวกเท้า"
G_NICK = C.g_of(19.36)                                 # 584 "ไอ้บ้าน้ำแข็ง"
PPD = {3: 128, 4: 192, 5: 192, 6: 256, 7: 160}


def aim(loc, az, el, d=30.0):
    a, e = math.radians(az), math.radians(el)
    return tuple(loc[i] + d * v for i, v in enumerate((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))))


def V(*a):
    return Vector(a)


# ----------------------------------------------------------------------------- cameras (loc0, look0) -> (loc1, look1), lens
CAMS = {
    3: ((V(0.2, -14.5, 13.0), V(0.0, 30.0, 6.8)), (V(0.4, -12.0, 6.6), V(0.0, 30.0, 4.6)), 20.0),
    4: ((V(-3.7, 24.6, 2.3), V(0.9, 40.0, 4.3)), (V(-2.3, 27.5, 2.45), V(1.5, 40.0, 4.2)), 22.0),
    5: ((V(-1.3, 3.6, 3.3), V(3.6, 9.4, 3.0)), (V(-0.6, 4.7, 3.15), V(3.5, 9.2, 3.05)), 22.0),
    6: ((V(-2.0, 11.6, 1.95), V(3.5, 5.0, 3.3)), (V(-1.6, 10.9, 1.9), V(3.7, 5.3, 3.3)), 19.0),
    7: ((V(0.3, -4.2, 4.1), V(0.0, 24.0, 3.4)), (V(0.3, -2.9, 3.9), V(0.0, 24.0, 3.4)), 20.0),
}


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    if shot == 3:                                            # crane: the descent eases out into the preset height
        u = 0.5 * ez(x, "sine") + 0.5 * (1 - (1 - x) ** 2)
    else:
        u = 0.35 * ez(x, "sine") + 0.65 * x
    (l0, k0), (l1, k1), lens = CAMS[shot]
    return l0.lerp(l1, u), k0.lerp(k1, u), lens


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


# ----------------------------------------------------------------------------- lip-sync from the narration envelope
_ENV = {}


def env(g):
    """narration loudness 0..1 at film frame g (narration at +0.10 s), a 1/30 s window."""
    if not _ENV:
        w = wave.open(C.NARRATION)
        sr = w.getframerate(); n = w.getnchannels()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
        if n > 1:
            a = a.reshape(-1, n).mean(1)
        _ENV["a"], _ENV["sr"] = a, sr
    a, sr = _ENV["a"], _ENV["sr"]
    i = int((g / 30.0 - 0.10) * sr)
    s = a[max(0, i - sr // 60): max(1, i + sr // 60)]
    r = float(np.sqrt((s ** 2).mean())) if len(s) else 0.0
    return clamp(r / 6000.0)


def lip(g):
    lv = env(g)
    if lv < 0.06:
        return "flat"
    return ("open", 0.15 + 0.13 * lv, 0.035 + 0.15 * lv)


# ----------------------------------------------------------------------------- cast in each shot: name -> (cast, feet xyz)
# street walkable |x| < 2; merchant's takht x 1.9..4.3 y 4.4..12.6 at z 0.9; jars x 0.6..1.8 y 4.5..12.7
MER_TAKHT = (3.3, 8.1, 0.9)
FAR6 = (0.2, 6.3, 0.0)


def walk_path(g, ga, gb, p0, p1):
    x = clamp((g - ga) / float(gb - ga))
    return tuple(lerp(p0[i], p1[i], x) for i in range(3))


def stage(shot, g):
    """{actor name: (feet xyz, pose dict)} of the visible cast at (shot, g)."""
    t = g / 30.0
    S = {}
    if shot == 3:
        # the woman with a jar on her shoulder walks across (screen-left), the boy runs across (screen-right), the old man stands
        p = walk_path(g, 172, 257, (1.6, 11.0, 0), (-0.6, 10.2, 0))
        S["wom"] = (p, dict(cast8.cycle("woman", g / 28.0, "walk", facing=-1, base=dict(expr="neutral", prop_r="water_jar", jar_hold="shoulder"), arms="l"),
                            arm_r=dict(hand=(0.64, 0.10), bend=-0.6, stretch=1.25, layer="back"), jar_hold="shoulder", sweat=0.5, t=t))
        p = walk_path(g, 172, 257, (-1.7, 19.0, 0), (1.6, 20.5, 0))
        S["boy"] = (p, cast8.cycle("boy", g / 16.0, "run", facing=1, base=dict(expr="excited", mouth="grin")))
        S["old"] = ((-1.5, 15.5, 0), dict(ST["oldman_stick"][1], head_roll=4 + 2 * math.sin(g * 0.12), lean=6 + 1.5 * math.sin(g * 0.09),
                                          blink=blink(g, [200, 240]), mirror=False))
        p = walk_path(g, 172, 257, (-1.2, 26.0, 0), (0.4, 25.2, 0))
        S["wom2"] = (p, cast8.cycle("woman", g / 28.0 + 0.4, "walk", facing=1, base=dict(expr="neutral")))
    elif shot == 4:
        fan = 25.0 * math.sin(2 * math.pi * g / 8.0)
        S["wom"] = ((3.2, 34.9, 0), dict(ST["town_fan"][1], mirror=True, prop_r=dict(type="fan", angle=-75 + fan), t=t,
                                         head_roll=-6 + 2 * math.sin(g * 0.13), lean=1.5 * math.sin(g * 0.1), blink=blink(g, [285, 335])))
        fan2 = 22.0 * math.sin(2 * math.pi * (g + 3) / 9.0)
        S["old"] = ((-2.4, 38.3, 0), dict(ST["town_fan_oldman"][1], prop_r=dict(type="fan", angle=-75 + fan2), t=t + 0.5,
                                          head_roll=-6 + 2 * math.sin(g * 0.11 + 1), lean=3 + 1.5 * math.sin(g * 0.08), blink=blink(g, [300])))
        # the boy hops foot to foot on the burning ground: a slow run cycle in place + little hops
        ph = (g - 258) / 12.0
        hop = 0.28 * abs(math.sin(math.pi * ph))
        bp = cast8.cycle("boy", ph * 0.5, "run", facing=1, base=dict(expr="shocked", sweat=1.0, heat=0.6, t=t), speed=0.45)
        bp.update(head_roll=8 * math.sin(math.pi * ph), arm_r=dict(hand=(0.55, -0.05 + 0.2 * abs(math.sin(math.pi * ph))), bend=-0.8, shape="open", stretch=1.2),
                  arm_l=dict(hand=(-0.55, 0.05 + 0.2 * abs(math.cos(math.pi * ph))), bend=-0.8, shape="open", stretch=1.2))
        S["boy"] = ((-1.0 + 0.12 * math.sin(math.pi * ph / 2), 35.0, hop), bp)
    elif shot == 5:
        k = math.sin(2 * math.pi * g / 9.0)
        S["mer"] = (MER_TAKHT, dict(ST["merchant_laugh"][1], squash=(1.0 + 0.02 * k, 1.0 - 0.02 * k), lean=-8 - 3 * k,
                                    head_roll=-10 + 3 * math.sin(2 * math.pi * g / 18.0), pitch=-0.8 + 0.08 * k, t=t))
    elif shot == 6:
        talk = TALK[0] <= g <= TALK[1]
        pt = u_of(g, 434, 446)                                 # the point comes up on "น้ำแข็งกลางทะเลทราย"
        jab = 0.05 * pt * math.sin(2 * math.pi * g / 14.0)
        mk = dict(ST["merchant_mock"][1])
        mk.update(mirror=False, mouth=lip(g) if talk else "flat", head_roll=8 + 4 * math.sin(g * 0.15), t=t,
                  arm_r=dict(hand=(lerp(0.40, 1.00, pt), lerp(0.90, 0.18, pt) + jab), shape="point" if pt > 0.4 else "open", bend=lerp(0.9, -0.5, pt), stretch=1.3),
                  lean=lerp(0, 6, pt) + 2 * math.sin(g * 0.2), pitch=-0.1 + 0.08 * math.sin(g * 0.23), gaze=(0.5, 0.35),
                  blink=blink(g, [470, 515]))
        if 476 <= g <= 488:                                   # "ไอ้บ้า!": a sharper jab, eyes wide
            mk.update(expr="grinning")
        S["mer"] = (MER_TAKHT, mk)
        fp = dict(ST["farid_smile"][1])
        fp.update(mirror=True, yaw=0.30, pitch=-0.15 + 0.04 * math.sin(g * 0.07), head_roll=4 + 1.5 * math.sin(g * 0.09),
                  gaze=(0.45, -0.35), lean=1.0 * math.sin(g * 0.06), blink=blink(g, [455, 500, 532]),
                  expr="smug" if g < 500 else "happy", mouth="smile")
        S["far"] = (FAR6, fp)
    elif shot == 7:
        p = walk_path(g, 541, 613, (1.3, 8.4, 0), (-0.5, 6.0, 0))
        S["far"] = (p, cast8.cycle("farid", g / 30.0, "walk", facing=-1, base=dict(expr="smug", mouth="smile"), speed=0.8))
        k = math.sin(2 * math.pi * g / 8.0)
        S["wom"] = ((-1.6, 2.8, 0), dict(ST["town_laugh"][1], squash=(1 + 0.02 * k, 1 - 0.02 * k), head_roll=10 + 3 * k, t=t))
        S["old"] = ((1.75, 3.6, 0), dict(ST["town_point_oldman"][1], mirror=True, head_roll=6 + 2 * math.sin(g * 0.3),
                                         arm_r=dict(hand=(0.90, -0.02 + 0.05 * math.sin(g * 0.5)), shape="point", bend=-0.5, stretch=1.3)))
        S["boy"] = ((-1.4, 13.0, 0), dict(ST["town_laugh_boy"][1], squash=(1 + 0.03 * k, 1 - 0.03 * k), t=t))
        S["wom2"] = ((1.1, 17.0, 0), dict(ST["town_point"][1], mirror=True, head_roll=6 + 2 * math.sin(g * 0.25)))
        k2 = math.sin(2 * math.pi * g / 10.0)
        S["mer"] = (MER_TAKHT, dict(ST["merchant_laugh"][1], mirror=True, squash=(1 + 0.02 * k2, 1 - 0.02 * k2), lean=-8 - 3 * k2, t=t))
    return S


CASTS = dict(far="farid", mer="merchant", wom="woman", old="oldman", boy="boy", wom2="woman")


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=3):
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=20.0, name="cam_s03", light=LIGHT)
        for n, c in CASTS.items():
            self.actors[n] = C.make_actor(n, c, os.path.join(TMP, "sprites"))

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f)
            S = stage(shot, g)
            for n, a in self.actors.items():
                if n in S:
                    C.place(a, f, S[n][0][:2], z=S[n][0][2])
                for o in a.objects():
                    o.hide_render = n not in S
                    o.keyframe_insert("hide_render", frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            S = stage(shot, g)
            for n, (xyz, p) in S.items():
                self.actors[n].pose(f, p, camera=self.cam)
        for n, a in self.actors.items():
            fr = [bf(shot, g) for g in gs if n in stage(shot, g)]
            if fr:
                self.sprites_for([(a, PPD[shot])], fr)
            for g in gs:                              # hidden on this frame: a blank sprite so Cycles finds a file
                p = a.sprite_path(bf(shot, g))
                if n not in stage(shot, g) and not os.path.exists(p):
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    from PIL import Image
                    Image.new("RGBA", (16, 16), (0, 0, 0, 0)).save(p)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens,
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f),
                    mouth=str(stage(shot, g).get("mer", (0, {}))[1].get("mouth")) if shot == 6 else None)

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
