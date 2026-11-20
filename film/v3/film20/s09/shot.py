#!/usr/bin/env python3
"""shot.py -- film 20 CAFE Maupassant CAMERA-TRAVEL takes (team7, QA_TEAM §I re-plan): s09 = T09 (shots 9+10) and s16 = T16 (shots 16+17).
ONE file, identical in both take folders; the take is chosen by the folder name.  CAFE cafe_low, DAY; window view 'stub' (T09, 1887)
or 'full' (T16, 1889).  No cuts inside a take: the camera TRAVELS (crane / push / orbit, Catmull-Rom keys, never parked).

  s09 = T09  g 604..752 (20.15-25.09 s), out handle 8 (DIS 11 into T11), 4 frames in (match join to T06): wide on the banquette,
             crane up as he rises (g 612-640), cravat tugs, push in for the vow (lip-sync 22.62-25.11 s, g 682..755), orbit while he
             turns his back on the window, then a quick ~1 s push-in to the close-up on "สักครั้ง" (g 728-750).
  s16 = T16  g 1093..1220 (36.44-40.70 s), 4 frames in (hard cut onto the grin), out handle 11 (DIS 17 into T18): close on the grin,
             crash pull-out (g 1093-1110) to a medium-wide with the full tower in the window, laugh bounce, lip-sync from 37.12 s
             (g 1117), slow push-in for the jeer, thumb over the shoulder, crumple mime + ~1 s push-in on "เป็นเศษเหล็ก!" (g 1195).

    python3 shot.py probe a:b[:step]          camera / head numbers, no render
    python3 shot.py stills a:b[:step] out [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]   -> raw/ (resumable); scale<1 -> work/draft
    python3 shot.py mouth                     lip-sync table
"""
import math, os, sys, json, wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")
SHOT = int(os.path.basename(HERE)[1:])                   # 9 = T09, 16 = T16

CFG = {9:  dict(g=(604, 752), h_in=4, h_out=8, view="stub"),
       16: dict(g=(1093, 1220), h_in=4, h_out=11, view="full")}[SHOT]
G0, G1 = CFG["g"]                                        # in-take frames G0..G1 inclusive
GA, GZ = G0 - CFG["h_in"], G1 + CFG["h_out"]
PRESET, VIEW = "cafe_low", CFG["view"]
GS = list(range(GA, GZ + 1))

# ----------------------------------------------------------------------------- lip-sync from the narration loudness
QUOTE1 = (C.g_of(22.62), C.g_of(25.11) - 1)              # 682..755
QUOTE2 = (C.g_of(37.12), C.g_of(40.67))                  # 1117..1223
WIN = QUOTE1 if SHOT == 9 else QUOTE2
_ENV = None


def envelope():
    """per film frame: narration RMS in a 1-frame window centred on the frame time (narration t = g/30 - 0.10), 0..1 normalised to
    the loudest frame of the quote windows."""
    global _ENV
    if _ENV is not None:
        return _ENV
    import numpy as np
    w = wave.open(os.path.join(C.PROJ, "film20", "audio", "narration.wav"))
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0
    env = {}
    for g in range(600, 1230):
        t = g / 30.0 - 0.10
        a, b = int((t - 1 / 60.0) * sr), int((t + 1 / 60.0) * sr)
        env[g] = float(np.sqrt(np.mean(x[a:b] ** 2)))
    ref = max(env[g] for g in list(range(QUOTE1[0], QUOTE1[1] + 1)) + list(range(QUOTE2[0], QUOTE2[1] + 1)))
    _ENV = {g: min(1.0, v / ref) for g, v in env.items()}
    return _ENV


def mouth_of(g):
    """the mouth drawing of frame g: None outside the quote window (the pose's own fixed mouth), else loudness -> MOUTH_SET.
    A new drawing every 2 frames (hold) from the 3-frame-smoothed loudness; silence (pause between words) = flat."""
    if not (WIN[0] <= g <= WIN[1]):
        return None
    env = envelope()
    lev = (env[g - 1] + 2 * env[g] + env[g + 1]) / 4.0
    gh = g - (g - WIN[0]) % 2                            # hold 2 frames
    lev = (env[gh - 1] + 2 * env[gh] + env[gh + 1]) / 4.0
    if lev < 0.10:
        return "flat"
    m = cast20.talk_mouth(gh, min(1.0, lev * 1.4), seed=1.0)
    if lev > 0.80 and m != "flat":
        return ("open", 0.30, 0.19)
    if lev > 0.55 and m in ("talk_a", "talk_o"):
        return ("open", 0.20, 0.10)
    if lev < 0.25 and m == "talk_b":
        return ("open", 0.12, 0.05)
    return m


# ----------------------------------------------------------------------------- staging
PPD = 256
CANVAS = (-1.75, -4.0, 1.75, 0.25)
FOLD_R, FOLD_L = dict(hand=(-0.40, 0.92), bend=0.9, layer="top"), dict(hand=(0.40, 0.96), bend=0.9, layer="top")
C.add_expression("grin20", eyes="happy", tilt=0.0, brows=("both", 0.105, -10.0, 0.050, 0.18, 0.012), mouth="smile")


def arm(x, y, **kw):
    return dict(hand=(x, y), **kw)


# ----------------------------------------------------------------------------- the travelling camera (Catmull-Rom through keys)
# key = (g, dist D from the look point, azimuth deg round him (0 = the preset's side, + = toward screen-right of the window),
#        camera height z D, look-at height z D, look-at truck x D).  Head width px ~ 782 / dist.
KEYS = {
    9: [(600, 7.0, 16, 0.95, 2.95, 0.0), (622, 6.3, 12, 1.2, 2.9, 0.0), (645, 5.6, 6, 1.6, 2.75, 0.0),
        (682, 4.6, 8, 2.2, 2.6, 0.0), (712, 4.0, 14, 2.20, 2.55, 0.0), (728, 3.6, 18, 2.15, 2.55, 0.0),
        (740, 2.6, 24, 2.15, 2.60, 0.0), (752, 2.05, 28, 2.15, 2.62, 0.0), (762, 1.85, 30, 2.15, 2.62, 0.0)],
    16: [(1089, 2.1, -4, 2.20, 2.65, 0.0), (1096, 2.5, -2, 2.10, 2.60, 0.0), (1110, 5.4, 6, 1.0, 2.6, 0.0),
         (1135, 5.8, 10, 1.05, 2.7, 0.0), (1165, 5.0, 4, 1.3, 2.65, 0.0), (1185, 4.0, 0, 1.85, 2.55, 0.0),
         (1195, 3.3, -3, 2.15, 2.60, 0.0), (1210, 2.1, -6, 2.20, 2.65, 0.0), (1222, 1.9, -7, 2.20, 2.65, 0.0),
         (1232, 1.8, -8, 2.20, 2.65, 0.0)],
}[SHOT]
if os.environ.get("KEYS"):
    KEYS = [tuple(k) for k in json.loads(os.environ["KEYS"])]       # tuning only


def _cr(p0, p1, p2, p3, t0, t1, t2, t3, t):
    """non-uniform Catmull-Rom (tangents by finite differences) between p1 and p2."""
    m1 = (p2 - p0) / (t2 - t0) if t2 != t0 else 0.0
    m2 = (p3 - p1) / (t3 - t1) if t3 != t1 else 0.0
    h = t2 - t1
    u = (t - t1) / h
    return ((2 * u ** 3 - 3 * u ** 2 + 1) * p1 + (u ** 3 - 2 * u ** 2 + u) * h * m1 + (-2 * u ** 3 + 3 * u ** 2) * p2 + (u ** 3 - u ** 2) * h * m2)


def cam_vals(g):
    K = KEYS
    g = clamp(g, K[0][0], K[-1][0])
    i = 0
    while i < len(K) - 2 and g > K[i + 1][0]:
        i += 1
    a, b = K[i], K[i + 1]
    p0 = K[i - 1] if i > 0 else (2 * a[0] - b[0],) + tuple(2 * a[j] - b[j] for j in range(1, 6))
    p3 = K[i + 2] if i + 2 < len(K) else (2 * b[0] - a[0],) + tuple(2 * b[j] - a[j] for j in range(1, 6))
    return [_cr(p0[j], a[j], b[j], p3[j], p0[0], a[0], b[0], p3[0], g) for j in range(1, 6)]


def cam_at(g, mark):
    d, az, zc, zl, tx = cam_vals(g)
    r = math.radians(az)
    look = Vector((mark[0] + tx, mark[1], zl))
    loc = Vector((mark[0] + tx + d * math.sin(r), mark[1] - d * math.cos(r), zc))
    return loc, look


# ----------------------------------------------------------------------------- poses
def rise_crouch():
    p = cast20._seated("maupassant", dict(cast20.STORY20["maupassant_idle"][1], seated=1, seat_h=0.80))
    return p["legs"]["crouch"]


_CROUCH = None


def bounce(g, hz=3.0, a=0.03):
    s = math.sin(2 * math.pi * hz * g / 30.0)
    return (1.0 + a * s, 1.0 - a * s)


def pose_t09(g):
    """g 604..752 (+ handles): rise, cravat, chin up (to 668), fold arms + turn his back on the window (676-712), chin jerk on 'สักครั้ง'."""
    ur = u_of(g, 612, 634)
    uf = u_of(g, 664, 680)                               # arms: cravat hand -> folded
    p = dict(legs=dict(crouch=lerp(_CROUCH, 0.0, ur), spread=0.05), t=g / 30.0)
    p["yaw"] = lerp(lerp(0.45, 0.25, ur), lerp(0.30, -0.60, u_of(g, 676, 712)), uf)
    tug = max(0.0, math.sin(math.pi * clamp((g - 640) / 8.0))) + max(0.0, math.sin(math.pi * clamp((g - 650) / 8.0)))
    if g < 636:
        a_r = arm(lerp(0.40, 0.55, ur), lerp(1.04, 0.95, ur), bend=0.6)
        a_l = arm(lerp(-0.40, -0.55, ur), lerp(1.04, 0.95, ur), bend=0.6)
    else:
        a_r = arm(0.22 + 0.04 * tug, 0.78 - 0.05 * tug, bend=0.8, shape="open", layer="top")
        a_l = arm(-0.55, 0.95, bend=0.6)
    if g >= 664:                                          # fold the arms
        a_r = dict(hand=(lerp(a_r["hand"][0], FOLD_R["hand"][0], uf), lerp(a_r["hand"][1], FOLD_R["hand"][1], uf)), bend=lerp(0.8, 0.9, uf), layer="top")
        a_l = dict(hand=(lerp(a_l["hand"][0], FOLD_L["hand"][0], uf), lerp(a_l["hand"][1], FOLD_L["hand"][1], uf)), bend=lerp(0.6, 0.9, uf), layer="top")
    p["arm_r"], p["arm_l"] = a_r, a_l
    hm = math.sin(math.pi * clamp((g - 729) / 9.0))       # chin jerk on 'สักครั้ง' (g 732)
    up = u_of(g, 654, 668)
    p["pitch"] = lerp(lerp(0.05, -0.45, up) - 0.1 * math.sin(math.pi * ur), lerp(-0.30, -0.50, u_of(g, 676, 712)) - 0.15 * hm, uf)
    p["head_roll"] = lerp(lerp(4.0, -4.0, up), lerp(5.0, -5.0, u_of(g, 676, 712)) + 3 * hm, uf) + 1.8 * math.sin(g * 0.17)
    p["lean"] = (7.0 * math.sin(math.pi * clamp((g - 608) / 30.0)) if g < 640 else 0.0) + lerp(0.0, -4.0, u_of(g, 676, 712)) + 1.2 * math.sin(g * 0.19)
    p["gaze"] = (0.5, 0.0)
    p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.27))
    if g < 654:
        p["expr"] = "sneer"
    elif g < 686:
        p["expr"] = "smug"
    else:
        p["expr"] = "smug_shut"                           # eyes shut behind the blink at 685
    p["blink"] = blink(g, [616, 649, 685])
    m = mouth_of(g)
    p["mouth"] = m if m is not None else "flat"
    return p


def pose_t16(g):
    """g 1089..1231: belly laugh (3 Hz bounce); from 1143 the thumb over the shoulder at the tower, crumple mime on 1195."""
    p = dict(yaw=0.30, pitch=-0.55, expr="laughing20", fx=["tears"], head_roll=-9 + 2.5 * math.sin(g * 0.3), lean=-8, t=g / 30.0, legs="wide")
    p["squash"] = bounce(g, a=0.03)
    ut = u_of(g, 1136, 1146)                              # belly-hold arms -> thumb over the shoulder
    p["arm_l"] = dict(hand=(lerp(-0.56, -0.85, ut), lerp(0.98, 0.30, ut)), bend=lerp(0.9, 0.6, ut), shape="open" if ut < 0.5 else "point",
                      stretch=lerp(1.0, 1.2, ut))
    cr = u_of(g, 1190, 1196) - u_of(g, 1202, 1210)        # crumple mime on 'เป็นเศษเหล็ก!' 1195
    wob = 0.04 * math.sin(g * 0.9) if cr > 0.05 else 0.0
    p["arm_r"] = arm(lerp(0.50, 0.36, cr) + wob, lerp(1.0, 0.70, cr), bend=0.9, shape="open" if cr < 0.5 else "ball")
    p["pitch"] = -0.55 - 0.1 * ut
    m = mouth_of(g)
    if m is not None:
        p["mouth"] = m
    return p


POSE = {9: pose_t09, 16: pose_t16}[SHOT]


def feet_at(A, g):
    m = Vector(A["marks"]["maupassant"])
    if SHOT == 9:                                         # steps forward off the banquette edge while rising
        s = Vector(A["marks"]["maupassant_seat"])
        u = u_of(g, 612, 640)
        return (lerp(s.x, m.x, u), lerp(s.y - 0.30, m.y, u))
    return (m.x, m.y)


class Take(C.Take):
    def __init__(self, quality="preview"):
        global _CROUCH
        C.Take.__init__(self, PRESET, light="DAY", quality=quality, name="cam_s%02d" % SHOT)
        mk = self.A["marks"]["maupassant"]
        self.A["marks"]["maupassant"] = (mk[0], mk[1], C.ground_z(mk[0], mk[1], top=0.6))   # ray from 0.6 D: the CAFE ceiling is below 40
        _CROUCH = rise_crouch()
        self.mark = self.A["marks"]["maupassant"]
        self.key_cam(bf(GA), *cam_at(GA, self.mark))
        self.scene.frame_set(bf(GA))
        self.mau = self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), canvas=CANVAS,
                                                     contact=dict(width=1.3, depth=0.55, opacity=0.7), cam=self.cam)

    def pose(self, gs):
        z = self.mark[2]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(g, self.mark))
            x, y = feet_at(self.A, g)
            bob = 0.06 * abs(math.sin(2 * math.pi * 1.5 * g / 30.0)) if SHOT == 16 and g < 1230 else 0.0     # laugh bounce 0.06 D at 3 Hz
            C.place(self.mau, f, (x, y, z + bob))
            self.key_set(f, set_window_view=VIEW)
            if SHOT == 9:
                self.A["hooks"]["smoke"](0.0, frame=f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mau.pose(f, POSE(g), camera=self.cam)
        self.sprites_for([(self.mau, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_at(g, self.mark)
        return dict(g=g, cam=[round(c, 3) for c in loc], dist=round(cam_vals(g)[0], 2), heads=C.head_report(self, f), mouth=str(mouth_of(g)))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "mouth":
        for g in GS:
            print(g, round(envelope()[g], 2), mouth_of(g))
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GZ]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
