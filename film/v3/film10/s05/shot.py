#!/usr/bin/env python3
"""shot.py -- film 10 take s05: shots 5, 6, 7 (g 293..537, + 6 handle frames each side: g 287..543), harbour quay_low, DAY.
  shot 5  g 287..365  the admiral strides up the quay (screen-left), sees the half-striped hull, bursts out laughing (g 320..342, narration
                      'หัวเราะลั่น'); the painter, painting a stroke, turns to him and calms.  At g 343 (quote start 11.33 s) he turns to the
                      grey ships and starts mocking (lip-sync).
  shot 6  g 366..449  low two-shot: admiral points at the grey ships (screen-right) mocking, lip-sync; painter calm, brush upright.
  shot 7  g 450..543  push-in on the admiral: finger up, chest out, the promise; lip-sync until g 540 (17.90 s + 0.1).
Mouths move only on the boss quote (captions 11.33..17.90 s + 0.10 s offset = g 343..540).
Blender frame of (shot, g) = 1000*(shot-1) + g + 1.
    python3 shot.py probe 5,6,7 a:b[:step]
    python3 shot.py stills 5,6,7 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 5|6|7 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c10 as C                                           # noqa: E402
from mathutils import Vector                              # noqa: E402

actors, camrig, cast10, puppet = C.actors, C.camrig, C.cast10, C.cast10.puppet if hasattr(C.cast10, "puppet") else None
import puppet                                             # noqa: E402
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
S10 = cast10.STORY10

G_S5, G_S6, G_S7, G_END = C.g_bound(9.76), C.g_bound(12.20), C.g_bound(15.0), C.g_bound(17.92)   # 293 366 450 538
H = 6
RANGES = {5: (G_S5 - H, G_S6 - 1), 6: (G_S6, G_S7 - 1), 7: (G_S7, G_END + H - 1)}
LOC = ("harbour", "quay_low")
LIGHT = "DAY"
STRIPES = 0.6
G_SEE = 318                                  # the admiral stops and sees the hull
G_LAUGH = (320, 342)
G_QUOTE = (C.g_of(11.33), C.g_of(17.90))     # 343 .. 540: lip-sync window
G_PAINT_TURN = (322, 332)                    # painter turns to the admiral and calms
ADM_END = Vector((20.4, -7.0, 0.0))
PNT = Vector((17.3, -4.6, 0.0))
PPD = 320
BRUSH = cast10.BRUSH


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def adm_pos(g):
    if g >= G_SEE:
        return ADM_END
    x = ADM_END.x + (G_SEE - g) * 0.157
    return Vector((x, ADM_END.y - (x - ADM_END.x) * 0.45, 0.0))


# ----------------------------------------------------------------------------- cameras
# (loc, look) keys per shot: [start, end]
CAMS = {
    5: ((18.8, -15.6, 1.6), (20.6, -5.6, 3.0), (19.2, -14.6, 1.6), (19.3, -5.4, 3.05)),
    6: ((19.4, -14.2, 1.6), (18.4, -5.4, 3.0), (19.6, -12.8, 1.6), (18.4, -5.6, 3.1)),
    7: ((24.0, -13.2, 1.65), (20.4, -7.0, 2.7), (22.6, -10.9, 1.7), (20.4, -7.0, 2.8)),
}
LENS = 24.0


def cam_of(shot, g):
    a0, a1, b0, b1 = CAMS[shot]
    r0, r1 = RANGES[shot][0], RANGES[shot][1]
    if shot == 5:
        r0 = G_S5
    if shot == 7:
        r1 = G_END
    x = clamp((g - r0) / float(r1 - r0))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return (Vector([lerp(a0[i], b0[i], u) for i in range(3)]), Vector([lerp(a1[i], b1[i], u) for i in range(3)]))


# ----------------------------------------------------------------------------- poses
def talk(g):
    return cast10.talk_mouth(g, 1.0, 0.3) if G_QUOTE[0] <= g <= G_QUOTE[1] else "flat"


def laugh_pose(g):
    p = dict(S10["admiral_laugh_big"][1])
    ph = math.sin((g - G_LAUGH[0]) * 0.95)
    p["squash"] = (1.02 + 0.025 * ph, 0.98 - 0.025 * ph)
    p["head_roll"] = -10 + 3.0 * math.sin((g - G_LAUGH[0]) * 0.55)
    p["lean"] = -8 + 2.0 * ph
    p["t"] = g / 30.0
    return p


def adm_pose(g, shot):
    if g < G_SEE - 2:                                       # striding up the quay, toward screen-left
        p = cast10.cycle("admiral", (g - G_S5) / 27.0, "walk", facing=-1, base=dict(expr="smug", pitch=-0.3, mouth="flat"))
        p["blink"] = cast10.blink_at(g, 90, 20)
        return p
    walk = cast10.cycle("admiral", (G_SEE - 2 - G_S5) / 27.0, "walk", facing=-1, base=dict(expr="smug", pitch=-0.3, mouth="flat"))
    if g < G_LAUGH[0]:                                      # stops, sees the hull (short beat), 4 frames of take
        t = u_of(g, G_SEE - 2, G_LAUGH[0])
        p = puppet.lerp_pose("admiral", walk, laugh_pose(G_LAUGH[0]), t)
        p["mirror"] = True
        p["squash"] = (1.02, 0.98)
        return p
    if g < 339:
        p = laugh_pose(g); p["mirror"] = True
        return p
    point = dict(S10["admiral_point_mock"][1])
    if shot < 7:
        if g < 347:                                         # turns to the grey ships; mirror flips at the middle of the blend
            t = u_of(g, 339, 347)
            p = puppet.lerp_pose("admiral", laugh_pose(g), point, t)
            p["mirror"] = t < 0.5
            p["mouth"] = talk(g)
            return p
        p = dict(point)
        p["head_roll"] = point.get("head_roll", 8) + 2.0 * math.sin(g * 0.21)
        p["lean"] = 1.5 * math.sin(g * 0.13)
        p["arm_r"] = dict(point["arm_r"], hand=(point["arm_r"]["hand"][0] + 0.05 * math.sin(g * 0.27), point["arm_r"]["hand"][1] - 0.04 * math.sin(g * 0.37)))
        p["mouth"] = talk(g)
        p["blink"] = cast10.blink_at(g, 80, 11)
        p["squash"] = (1.0 + 0.012 * math.sin(g * 0.5), 1.0 - 0.012 * math.sin(g * 0.5))
        return p
    p = dict(S10["admiral_finger_up_promise"][1])
    p["head_roll"] = -4 + 2.0 * math.sin(g * 0.19)
    p["lean"] = -6 + 1.5 * math.sin(g * 0.11)
    a = dict(p["arm_r"]); a["hand"] = (a["hand"][0] + 0.03 * math.sin(g * 0.3), a["hand"][1] + 0.06 * math.sin(g * 0.43)); p["arm_r"] = a
    p["mouth"] = talk(g)
    p["blink"] = cast10.blink_at(g, 84, 37)
    p["squash"] = (1.01 + 0.012 * math.sin(g * 0.5), 0.99 - 0.012 * math.sin(g * 0.5))
    return p


def stroke_pose(g):
    p = dict(S10["painter_paint_stroke"][1])
    s = 0.5 - 0.5 * math.cos((g - G_S5) * 2 * math.pi / 26.0)
    a = dict(p["arm_r"]); a["hand"] = (lerp(0.70, 0.66, s), lerp(0.55, -0.30, s)); p["arm_r"] = a
    pr = dict(p["prop_r"]); pr["angle"] = lerp(-20, -62, s); p["prop_r"] = pr
    p["t"] = g / 30.0
    return p


def calm_pose(g):
    p = dict(S10["painter_calm_smile"][1])
    p["head_roll"] = -4 + 1.5 * math.sin(g * 0.11)
    p["lean"] = 1.0 * math.sin(g * 0.08)
    a = dict(p["arm_r"]); a["hand"] = (a["hand"][0], a["hand"][1] + 0.025 * math.sin(g * 0.17)); p["arm_r"] = a
    p["blink"] = cast10.blink_at(g, 100, 47)
    p["t"] = g / 30.0
    return p


def pnt_pose(g):
    if g < G_PAINT_TURN[0]:
        p = stroke_pose(g); p["mirror"] = True
        return p
    if g < G_PAINT_TURN[1]:
        t = u_of(g, *G_PAINT_TURN)
        p = puppet.lerp_pose("painter10", stroke_pose(g), calm_pose(g), t)
        p["mirror"] = t < 0.5
        p["brush_paint"] = 0.8; p["t"] = g / 30.0
        return p
    return calm_pose(g)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=LENS, name="cam_s05", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        self.adm = self.actors["adm"] = C.make_actor("adm", "admiral", sd)
        self.pnt = self.actors["pnt"] = C.make_actor("pnt", "painter10", sd)
        self.hp = {}

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS)
            C.place(self.adm, f, adm_pos(g))
            C.place(self.pnt, f, PNT)
            self.key_set(f, stripes=STRIPES)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.adm.pose(f, adm_pose(g, shot), camera=self.cam)
            self.pnt.pose(f, pnt_pose(g), camera=self.cam)
        self.sprites_for([(self.adm, PPD), (self.pnt, PPD)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], mouth=adm_pose(g, shot).get("mouth"), heads=C.head_report(self, f))

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
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
