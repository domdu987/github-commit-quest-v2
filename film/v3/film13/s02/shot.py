#!/usr/bin/env python3
"""shot.py -- film 13 take s02: shots 2 + 3 (g 57..164: 6 in-handle frames g 57..62, shot 2 g 63..107, shot 3 g 108..158, out-handle 159..164).
One location: the suite (SUITE light).  The hotel is rising, so the street below drifts DOWN in the window: every object outside the room
(street, shops, opposite row, church, town, crowd cards) is lowered by drift(g) (the set cannot lift the suite itself); sky/backdrop/room stay.
    id 2  g 57..107  suite_two: lady in the teal armchair and the gentleman beside her sip tea calmly at the window; slow push.
    id 3  g 108..164 tea_close: cup and saucer, tea surface a perfect mirror (ripple 0) in the sunbeam, the window and the sliding rooftops
                     behind; slow push.
    python3 shot.py probe ID a:b[:step] | stills ID a:b[:step] <out> [scale] [samples] | final ID a:b[:step] [scale] [samples]
Blender frame of (id, g) = 1000 * (id - 1) + g + 1."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import c13 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
D, actors, camrig, cast13 = C.D, C.actors, C.camrig, C.cast13
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
G2, G3, G4 = C.g_bound(2.10), C.g_bound(3.60), C.g_bound(5.30)       # 63, 108, 159
H_IN, H_OUT = 6, 6
RANGES = {2: (G2 - H_IN, G3 - 1), 3: (G3, G4 + H_OUT - 1)}
SUITE_PRESET, LIGHT = "suite_two", "SUITE"
DRIFT_K = 2.0                         # visual gain of the street drift (true: 3.6 D per unit lift) so the slide reads through the window


def lift_of(g):                       # continues shot 1 (0.55 -> 0.65 at g 63) at the same rate
    return 0.65 + 0.15 * (g - G2) / float(G4 - G2)


DRIFT_RATE = 6.0 / 30.0               # D per frame (QA-art: the street must visibly slide >= 60-100 px; true lift would be ~0.55 D / 3 s)


def drift(g):
    return DRIFT_RATE * (g - G2)


CAMS = {2: (((0.45, 8.4, 31.45), (1.05, 0.0, 32.9)), ((0.85, 7.2, 31.45), (1.05, 0.0, 33.0)), 22.0),
        3: (((-2.4, 7.4, 34.6), (-3.3, 1.2, 32.4)), ((-2.7, 6.7, 34.3), (-3.3, 1.2, 32.5)), 34.0)}


def cam_of(shot, g):
    a, b, lens = CAMS[shot]
    lo, hi = RANGES[shot]
    x = clamp((g - lo) / float(hi - lo))
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector([lerp(a[0][i], b[0][i], u) for i in range(3)]), Vector([lerp(a[1][i], b[1][i], u) for i in range(3)]), lens


# ----------------------------------------------------------------------------- guests
LADY_XY = (-0.2, 1.5)
GENT_XY = (2.2, 1.0)
PPD = 192
ZF = 30.0


def sip(g, t0, up=10, hold=16, down=10):
    """0..1 trapezoid: cup rises (up frames), is held at the lips (hold), lowers (down)."""
    u = g - t0
    if u < 0 or u > up + hold + down:
        return 0.0
    if u < up:
        return math.sin(0.5 * math.pi * u / up) ** 2
    if u < up + hold:
        return 1.0
    return math.cos(0.5 * math.pi * (u - up - hold) / down) ** 2


def p_lady(g):
    """lady in the teal armchair holds cup AND saucer together (teacup_saucer) in her right hand and lifts them to her lips; the other hand rests in her lap."""
    p = dict(cast13.STORY13["lady_sip_tea"][1])
    s = min(1.0, sip(g, 72) + sip(g, 150))
    p["arm_r"] = dict(hand=(lerp(0.34, 0.26, s), lerp(0.62, 0.34, s)), bend=lerp(-0.5, -0.9, s), stretch=1.2, layer="front")
    p["prop_r"] = dict(type="teacup_saucer", scale=1.5)
    p["arm_l"] = dict(hand=(0.05, 0.95), bend=0.4, stretch=1.2, layer="front")
    p.pop("prop_l", None)
    p["pitch"] = lerp(-0.05, 0.10, s) + 0.03 * math.sin(g * 0.09)
    p["head_roll"] = 3 + 1.2 * math.sin(g * 0.06)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [70, 131])
    return p


def p_gent(g):
    p = dict(cast13.STORY13["gentleman_stand"][1])
    s = 0.22 * sip(g, 92, 12, 10, 12)          # a small lift of the cup + saucer toward the chest, the cup stays visible to the cut
    p.update(yaw=0.5, expr="neutral", mouth="smile", arm_r="behind",
             arm_l=dict(hand=(lerp(0.12, 0.10, s), lerp(0.95, 0.80, s)), bend=lerp(0.5, 0.3, s), stretch=1.2, layer="front"),
             prop_l=dict(type="teacup_saucer", scale=1.5), tea=1.0)
    p["pitch"] = -0.08 + 0.12 * s + 0.03 * math.sin(g * 0.08)
    p["lean"] = 1.0 * math.sin(g * 0.07)
    p["head_roll"] = -2 + 1.0 * math.sin(g * 0.05)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [88, 140])
    return p


ROOM = ("floor_room", "rug", "curtains", "room", "paintings", "furniture", "tea", "chandelier", "candles")
STATIC = ("sky", "backdrop")


def make_tower():
    """a clock tower with a spire on the opposite row (runtime dressing): a clear landmark outside the window that drifts down with the street."""
    S = D.STATE; M = S["M"]; mb = D.MB()
    x, y = 4.5, -76.0
    D.sbox(mb, (x - 2.6, y - 2.6, 14.0), (x + 2.6, y + 2.6, 30.0), M["brick_d"], 0.15)
    D.sbox(mb, (x - 2.9, y - 2.9, 29.6), (x + 2.9, y + 2.9, 30.6), M["cream"], 0.3)
    D.sbox(mb, (x - 1.7, y - 2.7, 24.0), (x + 1.7, y - 2.5, 28.4), M["cream"], 0.3)
    D.sbox(mb, (x - 1.1, y - 2.8, 25.0), (x + 1.1, y - 2.6, 27.4), M["dark"], 0.3)
    mb.frustum((x, y, 30.6), (x, y, 42.0), 2.7, 0.15, M["slate"], seg=4)
    D.rod(mb, (x, y, 42.0), (x, y, 45.0), 0.1, M["brass"], seg=4)
    ob = D._obj(mb, "s02_tower", S["SET"])
    return ob


class Take(C.Take):
    def __init__(self, quality="preview", shot=2):
        C.Take.__init__(self, "suite", SUITE_PRESET, quality=quality, lens=22.0, name="cam_s02", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        self.tower = make_tower()
        try:                                        # soften the rug texture (fine diagonal stripes alias into scan-line shimmer at grazing angles)
            for n in D.STATE["M"]["rug"].node_tree.nodes:
                if n.bl_idname == "ShaderNodeTexImage":
                    n.image.scale(336, 240)
        except Exception as e:
            print("rug soften failed", e)
        pre_names = set(ob.name for ob in D.STATE["SET"].objects)
        self.lady = self.actors["lady"] = C.make_actor("lady", "lady13_seat", sd, canvas=cast13.CANVAS13_POSE["lady_sip_tea"])
        self.gent = self.actors["gent"] = C.make_actor("gent", "gentleman13", sd)
        # the street crowd of the preset (suite_two PRESET_CROWD), placed for the shot-2 camera
        loc, look, lens = cam_of(2, G2)
        self.key_cam(bf(2, G2), loc, look, lens=lens)
        self.scene.camera = self.cam
        self.scene.frame_set(bf(2, G2))
        C.bpy.context.view_layer.update()
        D.PRESET_CROWD["suite_two"](self.cam)
        self.movers = [(ob, ob.location.z) for ob in D.STATE["SET"].objects
                       if ob.type == "MESH" and ob.name not in ROOM and ob.name not in STATIC and not ob.name.startswith("bgproto")
                       and (ob.name in pre_names or ob.name.startswith("bgcard_"))]

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, tea_ripple=0.0)
            d = drift(g)
            for ob, z0 in self.movers:
                ob.location.z = z0 - d
                ob.keyframe_insert("location", index=2, frame=f)
            C.place(self.lady, f, LADY_XY, z=ZF)
            C.place(self.gent, f, GENT_XY, z=ZF)
        if shot == 2:
            for nm in ("chandelier", "candles", "tea"):          # shot 2 only: chandelier fragment + the shot-3 teacup that floats at the window edge
                ob = C.bpy.data.objects.get(nm)
                if ob is not None:
                    for g in gs:
                        ob.hide_render = True
                        ob.keyframe_insert("hide_render", frame=bf(shot, g))
            for g in gs:
                f = bf(shot, g)
                self.scene.frame_set(f)
                self.lady.pose(f, p_lady(g), camera=self.cam)
                self.gent.pose(f, p_gent(g), camera=self.cam)
            fr = [bf(shot, g) for g in gs]
            self.sprites_for([(self.lady, PPD), (self.gent, PPD)], fr)
        else:
            for a in (self.lady, self.gent):
                for g in gs:
                    a.card.hide_render = True
                    a.card.keyframe_insert("hide_render", frame=bf(shot, g))

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    drift=round(drift(g), 3), heads=C.head_report(self, f) if shot == 2 else {})

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
                    print("shot %d g %d  %.1f s wall" % (shot, g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
