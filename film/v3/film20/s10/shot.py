#!/usr/bin/env python3
"""shot.py -- film 20 CAFE Maupassant takes (team7): s09 / s10 / s16 / s17.  ONE file, identical in the four take folders; the shot
is chosen by the folder name (sNN).  CAFE cafe_low / cafe_low_close, DAY; view 'stub' (1887, shots 9-10) or 'full' (1889, shots 16-17).

  s09 (g 604..675)  cafe_low: he rises from the banquette (crouch 0.6 -> 0 on the legs, lean forward then upright), tugs his cravat
                    twice, chin up; crane up + push + slide; snap on 'ประกาศลั่น' (g 659).  NO mouth movement (quote starts g 682).
  s10 (g 676..752)  cafe_low_close: QUOTE 1 22.62-25.11 s, lip-sync from the narration loudness (cast20 MOUTH_SET); he turns his back
                    to the window (yaw +0.3 -> -0.6), eyes shut, arms crossed; snap push on 'มันสักครั้ง!' (g 732).
  s16 (g 1093..1142) cafe_low, view FULL: belly laugh (3 Hz bounce), crash pull-out from the grin to the gloat framing; he starts
                    lip-sync on the laugh at 37.12 s (g 1117).
  s17 (g 1143..1220) cafe_low_close, FULL: QUOTE 2 lip-sync (loudness), laughing, thumb jerked over the shoulder at the tower, mimes
                    crumpling on 'เป็นเศษเหล็ก!' (g 1195); snap push there.

    python3 shot.py probe a:b[:step]          camera / head numbers, no render
    python3 shot.py camreport                 never-parked check
    python3 shot.py stills a:b[:step] out [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]   -> raw/ (resumable; run 2 processes) ; scale<1 -> work/draft
    python3 shot.py mouth                     print the lip-sync table (no bpy work)
"""
import math, os, sys, json, wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")
SHOT = int(os.path.basename(HERE)[1:])
H = 4                                                    # handle frames on each cut side

CFG = {
    9:  dict(g=(604, 675), preset="cafe_low", view="stub"),
    10: dict(g=(676, 752), preset="cafe_low_close", view="stub"),
    16: dict(g=(1093, 1142), preset="cafe_low", view="full"),
    17: dict(g=(1143, 1220), preset="cafe_low_close", view="full"),
}[SHOT]
G0, G1 = CFG["g"]                                        # in-shot frames G0..G1 inclusive
GA, GZ = G0 - H, G1 + H                                  # rendered range
PRESET, VIEW = CFG["preset"], CFG["view"]
GS = list(range(GA, GZ + 1))

# ----------------------------------------------------------------------------- lip-sync from the narration loudness
QUOTE1 = (C.g_of(22.62), C.g_of(25.11) - 1)              # 682..755
QUOTE2 = (C.g_of(37.12), C.g_of(40.67))                  # 1117..1223
WIN = QUOTE1 if SHOT in (9, 10) else QUOTE2
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
HEAD_Z = 2.6
PPD = 256
CANVAS = (-1.75, -4.0, 1.75, 0.25)
FOLD_R, FOLD_L = dict(hand=(-0.40, 0.92), bend=0.9, layer="top"), dict(hand=(0.40, 0.96), bend=0.9, layer="top")


def arm(x, y, **kw):
    return dict(hand=(x, y), **kw)


C.add_expression("grin20", eyes="happy", tilt=0.0, brows=("both", 0.105, -10.0, 0.050, 0.18, 0.012), mouth="smile")

# per-shot camera ---------------------------------------------------------------------------------
CAMP = {
    9:  dict(push=0.07, slide_px=25.0, rise_px=38.0, arc_deg_s=22.0, arc0=-26.0, tilt0=0.0, tilt_deg_s=-1.0, decay=0.25,
             snaps=[dict(g=(657, 670), k=1.30, peak=2.0, shift=(0.0, 0.0), tilt=0.0, arc=22.0)]),
    10: dict(push=0.05, slide_px=10.0, rise_px=0.0, arc_deg_s=26.0, arc0=-30.0, tilt0=0.0, tilt_deg_s=0.0, decay=0.25,
             snaps=[dict(g=(729, 742), k=1.25, peak=2.2, shift=(0.0, 0.0), tilt=-3.0, arc=48.0)]),
    16: dict(push=-0.16, slide_px=10.0, rise_px=0.0, arc_deg_s=-14.0, arc0=6.0, tilt0=5.5, tilt_deg_s=0.0, decay=0.3,
             snaps=[dict(g=(1090, 1108), k=0.65, peak=2.0, shift=(0.0, 0.0), tilt=0.0, arc=-6.0)]),
    17: dict(push=0.05, slide_px=10.0, rise_px=0.0, arc_deg_s=26.0, arc0=-30.0, tilt0=0.0, tilt_deg_s=0.0, decay=0.25,
             snaps=[dict(g=(1192, 1205), k=1.25, peak=2.2, shift=(0.0, 0.0), tilt=-3.0, arc=48.0)]),
}[SHOT]
if os.environ.get('CAMP'):
    CAMP.update(json.loads(os.environ['CAMP']))          # tuning only
CAM_SHIFT = {9: (0.0, 0.0), 10: (0.0, 0.0), 16: (0.0, 0.0), 17: (0.0, 0.0)}[SHOT]
START_CLOSE = {16: 1.5}.get(SHOT, 1.0)                   # s16 starts this much closer than the preset (the grin), then pulls out


def cam_path(A):
    m = Vector(A["marks"]["maupassant"])
    subj = m + Vector((0.0, 0.0, HEAD_Z))
    c = Vector(A["cams"][PRESET]["loc"])
    if START_CLOSE != 1.0:
        c = subj + (c - subj) / START_CLOSE
    return C.CamPath(c, subj, GA, GZ, **CAMP)


# ----------------------------------------------------------------------------- poses
def rise_crouch():
    """leg crouch that puts the seat top on the banquette (0.865 D)."""
    p = cast20._seated("maupassant", dict(cast20.STORY20["maupassant_idle"][1], seated=1, seat_h=0.80))
    return p["legs"]["crouch"]


def bounce(g, hz=3.0, a=0.03):
    s = math.sin(2 * math.pi * hz * g / 30.0)
    return (1.0 + a * s, 1.0 - a * s)


def pose_s09(g):
    c0 = _CROUCH
    r0, r1 = 612, 634                                    # the rise
    ur = u_of(g, r0, r1)
    p = dict(yaw=lerp(0.45, 0.25, ur), expr="sneer", legs=dict(crouch=lerp(c0, 0.0, ur), spread=0.05), t=g / 30.0)
    # arms: hands on the table edge while seated -> push off -> cravat tug
    p["arm_l"] = arm(lerp(-0.40, -0.55, ur), lerp(1.04, 0.95, ur), bend=0.6)
    tug = max(0.0, math.sin(math.pi * clamp((g - 640) / 8.0))) + max(0.0, math.sin(math.pi * clamp((g - 650) / 8.0)))
    if g < 636:
        p["arm_r"] = arm(lerp(0.40, 0.55, ur), lerp(1.04, 0.95, ur), bend=0.6)
    else:
        p["arm_r"] = arm(0.22 + 0.04 * tug, 0.78 - 0.05 * tug, bend=0.8, shape="open", layer="top")
    p["lean"] = lerp(0.0, 0.0, ur) + 7.0 * math.sin(math.pi * clamp((g - 608) / 30.0)) * (1 if g < 640 else 0)
    up = u_of(g, 654, 668)
    p["pitch"] = lerp(0.05, -0.45, up) - 0.1 * math.sin(math.pi * ur)
    p["head_roll"] = lerp(4.0, -4.0, up) + 1.5 * math.sin(g * 0.15)
    p["expr"] = "sneer" if g < 654 else "smug"
    p["gaze"] = (0.5, 0.0)
    p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.27))
    p["blink"] = blink(g, [616, 649])
    p["mouth"] = "flat"
    return p


def pose_s10(g):
    u = u_of(g, 676, 712)                                # turns his back on the window (face yaw +0.3 -> -0.6)
    p = dict(yaw=lerp(0.30, -0.60, u), expr="smug_shut", arm_r=FOLD_R, arm_l=FOLD_L, legs="wide", t=g / 30.0)
    hm = math.sin(math.pi * clamp((g - 729) / 8.0))      # chin jerk on the last words
    p["pitch"] = lerp(-0.30, -0.50, u) - 0.15 * hm
    p["head_roll"] = lerp(5.0, -5.0, u) + 2.0 * math.sin(g * 0.2) + 3 * hm
    p["lean"] = lerp(0.0, -4.0, u) + 1.2 * math.sin(g * 0.19)
    p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.26))
    # eyes: open sneer for the first beat, then shut behind a blink at g 686
    p["expr"] = "sneer" if g < 686 else "smug_shut"
    p["blink"] = blink(g, [685])
    m = mouth_of(g)
    p["mouth"] = m if m is not None else "flat"
    return p


def pose_s16(g):
    p = dict(yaw=0.30, pitch=-0.55, expr="laughing20", fx=["tears"], head_roll=-9 + 2.0 * math.sin(g * 0.3), lean=-8, t=g / 30.0,
             arm_r=arm(0.50, 1.0, bend=0.9, shape="open"), arm_l=arm(-0.56, 0.98, bend=0.9, shape="open"), legs="wide")
    p["squash"] = bounce(g)
    m = mouth_of(g)
    if m is not None:
        p["mouth"] = m
    return p


def pose_s17(g):
    p = dict(yaw=0.30, pitch=-0.5, expr="laughing20", fx=["tears"], head_roll=-8 + 2.0 * math.sin(g * 0.3), lean=-6, t=g / 30.0, legs="wide")
    p["squash"] = bounce(g, a=0.025)
    cr = u_of(g, 1190, 1196) - u_of(g, 1202, 1210)       # crumple mime on 'เป็นเศษเหล็ก!' 1195
    p["arm_l"] = arm(-0.85, 0.30, shape="point", bend=0.6, stretch=1.2)     # thumb over the shoulder at the tower
    wob = 0.04 * math.sin(g * 0.9) if cr > 0.05 else 0.0
    p["arm_r"] = arm(lerp(0.52, 0.36, cr) + wob, lerp(1.0, 0.70, cr), bend=0.9, shape="open" if cr < 0.5 else "ball")
    m = mouth_of(g)
    if m is not None:
        p["mouth"] = m
    return p


POSE = {9: pose_s09, 10: pose_s10, 16: pose_s16, 17: pose_s17}[SHOT]
_CROUCH = None


def stand_mark(A, g):
    """feet position: s09 steps from the banquette to the standing mark while rising."""
    m = Vector(A["marks"]["maupassant"])
    if SHOT == 9:
        s = Vector(A["marks"]["maupassant_seat"])
        u = u_of(g, 612, 640)
        return (lerp(s.x, m.x, u), lerp(s.y - 0.30, m.y, u))
    return (m.x, m.y)


class Take(C.Take):
    def __init__(self, quality="preview"):
        global _CROUCH
        C.Take.__init__(self, PRESET, light="DAY", quality=quality, name="cam_s%02d" % SHOT)
        mk = self.A["marks"]["maupassant"]
        self.A["marks"]["maupassant"] = (mk[0], mk[1], C.ground_z(mk[0], mk[1], top=0.6))   # the CAFE ceiling is below top=40: ray from 0.6 D
        _CROUCH = rise_crouch()
        self.path = cam_path(self.A)
        self.key_cam(bf(GA), *self.path.at(GA))
        self.scene.frame_set(bf(GA))
        self.mau = self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), canvas=CANVAS,
                                                     contact=dict(width=1.3, depth=0.55, opacity=0.7), cam=self.cam)

    def pose(self, gs):
        z = self.A["marks"]["maupassant"][2]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            x, y = stand_mark(self.A, g)
            bob = 0.06 * abs(math.sin(2 * math.pi * 1.5 * g / 30.0)) if SHOT in (16, 17) else 0.0     # laugh bounce ~0.06 D at 3 Hz
            C.place(self.mau, f, (x, y, z + bob))
            self.key_set(f, set_window_view=(VIEW,), smoke=(0.0,)) if False else self.key_set(f, set_window_view=VIEW)
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
        loc, look = self.path.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), mouth=str(mouth_of(g)))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def cam_path_static():
    """CamPath without building the set: numbers from the probe of cafe_low / cafe_low_close (world D)."""
    loc = {"cafe_low": (1.692, 8.648, 0.94), "cafe_low_close": (1.786, 9.964, 1.598)}[PRESET]
    return cam_path(dict(marks={"maupassant": (1.692, 13.16, 0.0)}, cams={PRESET: dict(loc=loc)}))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "mouth":
        for g in GS:
            print(g, round(envelope()[g], 2), mouth_of(g))
        sys.exit(0)
    if cmd == "camreport":
        P = cam_path_static()
        rows, worst = P.report(GS[:-1])
        for r in rows[::4]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (max 6)" % worst)
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
