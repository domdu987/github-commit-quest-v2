#!/usr/bin/env python3
"""shot.py -- film 7 take s04: shots 4-6 (plan 7.80-19.96 s = g 234..598) + 6-frame handles (g 228..233 in, g 599..604 out).
transition_in = dissolve (from shot 3's kiosk; the in-handle g 228..233 is rendered in 3D), out: cut to shot 7.
All in the louvre Salon Carré (GALLERY_DAY), Mona present.  Eight set-ups (internal ids), a framing change every 1.0-2.0 s:

  shot 4  "คืออย่างนี้ ปารีส ปีหนึ่งเก้าหนึ่งหนึ่ง โมนาลิซ่าเป็นแค่ภาพเล็ก ๆ"
    id 1  g 228..285  establishing wide from the service-door corner (gallery_wide area): the salon hang on three walls, skylight,
                      divan; a crowd of visitors (ladies in big hats, gentlemen in bowlers, a boy) strolls across without stopping,
                      the guard at ease; slow crane drift left.
    id 2  g 286..335  mid-room toward the back wall: she is a small picture in the middle of the hang; visitors cross in front of
                      her without a look; slow push.
  shot 5  "ภาพหนึ่ง แขวนปนกับภาพอีกเป็นร้อย คนเดินผ่าน แทบไม่หยุดดู"
    id 3  g 336..389  close on the small Mona Lisa, pulling back (lens 46 -> 24) until the big pictures crowd round her.
    id 4  g 390..440  eye level at the rope (wall_eye): a lady strolls in, slows, glances up at her for a beat, and walks on
                      (g 404..420 the glance); the guard by the wall.
  shot 6  "ผู้อำนวยการลูฟวร์ประกาศว่า ใครจะขโมยภาพนี้ได้ ก็ขโมยหอคอยนอเทรอดามได้เหมือนกัน"
    id 5  g 441..499  low angle: the director (top hat, monocle) stands proudly beside her, hand on hip; slow rising push.
                      Mouth closed (the narrator introduces him).
    id 6  g 500..539  lower and closer, huge from below: the boast, finger to the sky -- LIP-SYNC on the quote (from 16.57 s).
    id 7  g 540..569  ECU cut-in on the painting (her face, the smile, behind glass), slow push; his voice goes on off screen.
    id 8  g 570..604  extreme low angle on him again, finger up, lip-sync to the end of the quote (19.95 s = g 602), then a
                      smug closed mouth (handle).
Mouths: ONLY the director's, only inside the quote (16.57-19.95 s, narration envelope -> cast7.talk_mouth).
NO depth of field (C.Take).

    python3 shot.py probe|stills <ids> a:b[:step] [out scale samples] ;  python3 shot.py final <id> a:b
"""
import math, os, sys, json, wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import numpy as np                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1, H = C.g_bound(7.80), C.g_bound(19.96), 6        # 234, 599
RANGES = {1: (G0 - H, 285), 2: (286, 335), 3: (336, 389), 4: (390, 440), 5: (441, 499), 6: (500, 539), 7: (540, 569),
          8: (570, G1 + H - 1)}
SHOT_OF = {1: 4, 2: 4, 3: 5, 4: 5, 5: 6, 6: 6, 7: 6, 8: 6}
PRESET = {1: "gallery_wide", 2: "gallery_wide", 3: "wall_eye", 4: "wall_eye", 5: "wall_eye", 6: "wall_eye", 7: "wall_eye", 8: "wall_eye"}
Q0, Q1 = C.g_of(16.57), C.g_of(19.95)                    # the quote: 500 .. 602


# ----------------------------------------------------------------------------- lip-sync level from the narration
_ENV = {}


def level(g):
    if not (Q0 <= g <= Q1):
        return 0.0
    if not _ENV:
        w = wave.open(C.NARRATION)
        sr, n = w.getframerate(), w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
        for gg in range(Q0 - 2, Q1 + 3):
            t = gg / 30.0 - 0.10
            s0, s1 = int((t - 0.02) * sr), int((t + 0.045) * sr)
            _ENV[gg] = float(np.sqrt(np.mean(a[max(0, s0):s1] ** 2)))
        ref = np.percentile(list(_ENV.values()), 90) or 1.0
        for k in _ENV:
            _ENV[k] = min(1.0, _ENV[k] / ref)
    return _ENV.get(g, 0.0)


def director_mouth(g):
    lev = level(g)
    return cast7.talk_mouth(g, lev, seed=7.0, hold=2) if lev > 0.12 else None


# ----------------------------------------------------------------------------- cameras  (loc, look, lens) per set-up
def _cam(a, b, g, rg, kind="sine"):
    u = ez((g - rg[0]) / float(rg[1] - rg[0]), kind)
    return Vector(lerp(a[0], b[0], u)), Vector(lerp(a[1], b[1], u)), lerp(a[2], b[2], u)


CAMS = {
    1: (((7.9, 1.9, 3.9), (-2.6, 21.0, 4.5), 22.0), ((6.4, 2.7, 3.7), (-3.4, 21.0, 4.4), 22.0)),
    2: (((2.3, 7.4, 3.05), (0.0, 22.0, 3.6), 24.0), ((1.9, 8.6, 3.0), (0.0, 22.0, 3.6), 24.0)),
    3: (((0.05, 18.9, 3.62), (0.0, 21.9, 3.62), 46.0), ((0.35, 16.2, 3.45), (0.05, 21.9, 3.5), 24.0)),
    4: (((0.75, 14.3, 2.85), (-0.15, 22.0, 3.02), 24.0), ((0.60, 14.9, 2.82), (-0.10, 22.0, 2.98), 24.0)),
    5: (((3.55, 15.4, 1.35), (1.05, 22.0, 3.75), 22.0), ((3.30, 16.1, 1.55), (1.10, 22.0, 3.85), 22.0)),
    6: (((2.95, 17.15, 0.95), (1.55, 20.2, 3.45), 24.0), ((2.85, 17.40, 0.95), (1.55, 20.2, 3.50), 24.0)),
    7: (((0.02, 20.05, 3.86), (0.0, 21.92, 3.80), 50.0), ((0.02, 20.25, 3.86), (0.0, 21.92, 3.80), 52.0)),
    8: (((2.60, 18.05, 0.65), (1.95, 19.8, 3.55), 22.0), ((2.55, 18.20, 0.68), (1.95, 19.8, 3.60), 22.0)),
}


def cam_of(sid, g):
    a, b = CAMS[sid]
    return _cam(a, b, g, RANGES[sid])


# ----------------------------------------------------------------------------- the crowd
# walker: cast, feet at g0, velocity per frame, facing (+1 screen-right), cycle phase offset, speed, base pose extras
WALKERS = {
    1: [("w_lady1", "lady", (-3.4, 11.8), (0.040, -0.010), 1, 0.0, 0.8, {}),
        ("w_gent1", "gentleman", (4.6, 11.6), (-0.048, 0.010), -1, 0.4, 0.9, {}),
        ("w_lady2", "lady", (2.3, 17.0), (-0.036, 0.0), -1, 0.7, 0.75, {"hat_side": -1}),
        ("w_gent2", "gentleman", (2.95, 17.3), (-0.036, 0.0), -1, 0.2, 0.75, {}),
        ("w_boy", "newsboy", (-1.8, 9.2), (0.030, 0.030), 1, 0.5, 1.0, {})],
    2: [("w_lady1", "lady", (-1.9, 13.6), (0.040, 0.0), 1, 0.1, 0.8, {}),
        ("w_gent1", "gentleman", (3.4, 15.4), (-0.042, 0.0), -1, 0.5, 0.85, {}),
        ("w_gent2", "gentleman", (-1.2, 17.8), (0.030, 0.0), 1, 0.3, 0.7, {})],
}
STANDERS = {1: [("guard", "guard", (3.6, 13.4), "guard_at_ease", True)],
            4: [("guard", "guard", (2.35, 21.1), "guard_at_ease", True)]}


def walker_pose(spec, g, sid):
    name, cast, p0, v, facing, ph0, speed, extra = spec
    base = dict(expr="neutral", yaw=0.7, pitch=-0.05, gaze=(0.0, 0.0))
    base.update(extra)
    p = cast7.cycle(cast, ph0 + (g - RANGES[sid][0]) / 28.0, "walk", facing=facing, base=base, arms="both", speed=speed)
    p["blink"] = blink(g, [RANGES[sid][0] + 9 + int(ph0 * 30)])
    p["t"] = g / 30.0
    return p


def walker_xy(spec, g, sid):
    name, cast, p0, v = spec[:4]
    d = g - RANGES[sid][0]
    return Vector((p0[0] + v[0] * d, p0[1] + v[1] * d, 0.0))


# ----------------------------------------------------------------------------- the lady who glances (id 4)
LADY_Y = 19.55
GL = (402, 408, 418, 424)                                # slow .. stopped glance .. walk on


def lady_speed(g):
    a, b, c, d = GL
    if g < a or g > d:
        return 1.0
    if g < b:
        return lerp(1.0, 0.12, ez((g - a) / float(b - a)))
    if g <= c:
        return 0.12
    return lerp(0.12, 1.0, ez((g - c) / float(d - c)))


def lady_track(g):
    """x and cycle phase at g (integrated so the stop is smooth)."""
    x, ph = -1.05, 0.0
    for k in range(RANGES[4][0], g):
        s = lady_speed(k)
        x += 0.052 * s
        ph += s / 28.0
    return x, ph


def lady_pose(g):
    x, ph = lady_track(g)
    s = lady_speed(g)
    a, b, c, d = GL
    look = clamp((g - a) / 6.0) * (1.0 - clamp((g - c) / 6.0))
    base = dict(expr="neutral", yaw=lerp(0.7, 0.35, look), pitch=lerp(-0.05, -0.35, look), gaze=(lerp(0.0, -0.55, look), lerp(0.0, -0.7, look)),
                head_roll=lerp(0.0, 5.0, look))
    if g > c:
        base["expr"] = "bored"
    p = cast7.cycle("lady", ph, "walk", facing=1, base=base, arms="both", speed=lerp(0.35, 0.8, s))
    p["blink"] = blink(g, [396, 421])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the director (ids 5, 6, 8)
DIRECTOR = Vector((2.0, 19.75, 0.0))
DIR_CANVAS = (-1.6875, -6.0, 2.25, 0.125)                # wider / taller than cast7's: the finger to the sky clipped
PROUD = cast7.STORY7["director_proud"][1]
BOAST = cast7.STORY7["director_boast"][1]


def director_pose(g, sid):
    if sid == 5:
        p = dict(PROUD)
        p["pitch"] = PROUD["pitch"] + 0.05 * math.sin(g * 0.12)
        p["head_roll"] = PROUD["head_roll"] + 2.0 * math.sin(g * 0.09)
        u = ez((g - 480) / 19.0) if g > 480 else 0.0       # draws breath before the boast: chin up, chest out
        p["pitch"] -= 0.12 * u
        p["lean"] = -3.0 * u
        p["blink"] = blink(g, [455, 486])
    else:
        p = dict(BOAST)
        p.pop("mouth", None)
        rx, ry = 0.80, -1.05
        jab = 0.04 * math.sin(g * 0.45)
        p["arm_r"] = dict(BOAST["arm_r"], hand=(rx + 0.02 * math.sin(g * 0.2), ry - abs(jab)), stretch=1.45, bend=-0.6)
        if sid == 6 and g < 506:                           # the finger goes up at the start of the boast
            u = ez((g - 500) / 6.0)
            p["arm_r"] = dict(BOAST["arm_r"], hand=(lerp(0.40, rx, u), lerp(0.55, ry, u)), bend=lerp(0.6, -1.0, u))
            p["arm_r"]["shape"] = "point" if u > 0.4 else "ball"
        p["head_roll"] = BOAST["head_roll"] + 3.0 * math.sin(g * 0.21)
        p["pitch"] = BOAST["pitch"] + 0.06 * math.sin(g * 0.33)
        p["lean"] = BOAST["lean"] + 1.5 * math.sin(g * 0.17)
        m = director_mouth(g)
        if m:
            p["mouth"] = m
        p["blink"] = blink(g, [520, 588])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", sid=1):
        C.Take.__init__(self, "louvre", PRESET[sid], quality=quality, lens=24.0, name="cam_s04_%d" % sid)
        self.sid = sid
        sd = os.path.join(TMP, "sprites")
        for spec in WALKERS.get(sid, []):
            self.actors[spec[0]] = C.make_actor(spec[0], spec[1], sd)
        for name, cast, xy, pose, _ in STANDERS.get(sid, []):
            self.actors[name] = C.make_actor(name, cast, sd)
        if sid == 4:
            self.actors["lady"] = C.make_actor("lady", "lady", sd)
        if sid in (5, 6, 8):
            self.actors["director"] = C.make_actor("director", "director", sd, canvas=DIR_CANVAS)

    def pose(self, sid, gs):
        assert sid == self.sid
        for g in gs:
            f = bf(sid, g)
            loc, look, lens = cam_of(sid, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, mona=True)
            for spec in WALKERS.get(sid, []):
                C.place(self.actors[spec[0]], f, walker_xy(spec, g, sid), 0.0)
            for name, cast, xy, pose, _ in STANDERS.get(sid, []):
                C.place(self.actors[name], f, Vector((xy[0], xy[1], 0.0)), 0.0)
            if sid == 4:
                C.place(self.actors["lady"], f, Vector((lady_track(g)[0], LADY_Y, 0.0)), 0.0)
            if "director" in self.actors:
                C.place(self.actors["director"], f, DIRECTOR, 0.0)
        for g in gs:
            f = bf(sid, g)
            self.scene.frame_set(f)
            for spec in WALKERS.get(sid, []):
                self.actors[spec[0]].pose(f, walker_pose(spec, g, sid), camera=self.cam)
            for name, cast, xy, pose, mir in STANDERS.get(sid, []):
                p = dict(cast7.STORY7[pose][1]); p["mirror"] = mir
                p["pitch"] = p.get("pitch", 0.0) + 0.04 * math.sin(g * 0.1); p["blink"] = blink(g, [250, 300, 410]); p["t"] = g / 30.0
                self.actors[name].pose(f, p, camera=self.cam)
            if sid == 4:
                self.actors["lady"].pose(f, lady_pose(g), camera=self.cam)
            if "director" in self.actors:
                self.actors["director"].pose(f, director_pose(g, sid), camera=self.cam)
        fr = [bf(sid, g) for g in gs]
        jobs = []
        for n, a in self.actors.items():
            ppd = {1: 176, 2: 224}.get(sid, 304)
            if n == "director":
                ppd = 400 if sid in (6, 8) else 320
            jobs.append((a, ppd))
        self.sprites_for(jobs, fr)

    def report(self, sid, g):
        f = bf(sid, g)
        loc, look, lens = cam_of(sid, g)
        out = dict(shot=sid, plan_shot=SHOT_OF[sid], g=g, cam=[round(c, 3) for c in loc], lens=round(lens, 1), heads=C.head_report(self, f))
        if "director" in self.actors:
            out["mouth"] = director_mouth(g) if sid != 5 else None
            out["level"] = round(level(g), 2)
        return out

    def render(self, sid, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(sid, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    sids = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for sid in sids:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[sid][0] <= g <= RANGES[sid][1]]
            if not gs:
                continue
            Tk = Take("preview", sid)
            Tk.pose(sid, gs)
            for g in gs:
                print(json.dumps(Tk.report(sid, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(sid, [g], out, scale=scale, samples=samples, threads=int(os.environ.get("THREADS", "2")))[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (sid, g)))
                    print("id %d g %d  %.1f s wall %.1f cpu" % (sid, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, sid: Take(q, sid), sids, sys.argv[3], RANGES, HERE, scale=scale, samples=samples, take_key=lambda s: s)
