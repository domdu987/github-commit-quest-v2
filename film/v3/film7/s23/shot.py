#!/usr/bin/env python3
"""shot.py -- film 7 take s23: shots 23-24 (plan 74.53-81.48 s = g 2236..2443) + 6 handle frames each side (g 2230..2449).
Plan: 23 paris / kiosk: newspapers and posters with her face everywhere, gentleman reading;
      24 paris / street_wide: posters on the Morris column, newsboy shouting, people humming.
One location (the paris street area, kiosk build, STREET_GOLDEN), papers at the full count (set_papers 24 keyed every frame: the theft
is known now), four camera set-ups (framing change every 1.6-2.0 s):

    id 1  g 2230..2279  A  the kiosk front: rows of front pages with her face (LE MATIN, EXCELSIOR...), the camera tracks along
                           them.                                                         "หน้าโมนาลิซ่าขึ้นหนังสือพิมพ์"
    id 2  g 2280..2339  B  a gentleman at the kiosk reading the front page, shocked, a lady behind him reading another; slow push.
                                                                                          "ทั่วโลก มีเพลง มีโปสการ์ด"
    id 3  g 2340..2392  C  (shot 24) the rue: the newsboy waves the front page high, shouting (static open mouth, no lip-sync);
                           passers walk toward us; the Morris column with her posters, Notre-Dame far behind.   "มีโฆษณา คนที่ไม่เคย"
    id 4  g 2393..2449  D  push past a lady humming happily (eyes closed, head swaying) into the column poster: her smile
                           ("Elle sourit encore").                                        "เห็นของจริง ก็จำรอยยิ้มนี้ได้หมด"
Mouths: no quoted line -> static mouths only.  NO depth of field (client rule).

    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1,2,.. a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s21"))
import common as C                                       # noqa: E402
import t5lib as T5                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")
T5.variants()

G0, G1, H = C.g_bound(74.53), C.g_bound(81.48), 6           # 2236, 2444
G24 = C.g_bound(78.00)                                       # 2340
SETUPS = {1: (G0 - H, 2279), 2: (2280, G24 - 1), 3: (G24, 2392), 4: (2393, G1 + H - 1)}
RANGES = SETUPS

CAMS = {
    1: (((-1.45, 6.10, 2.65), (-4.8, 10.4, 2.40), 22.0), ((-1.75, 8.05, 2.60), (-4.8, 11.5, 2.40), 22.0)),
    2: (((-0.20, 6.40, 2.75), (-3.4, 10.0, 2.30), 24.0), ((-0.75, 7.15, 2.70), (-3.4, 10.0, 2.30), 24.0)),
    3: (((0.30, 6.60, 2.35), (3.6, 15.5, 2.15), 22.0), ((0.55, 7.30, 2.35), (3.9, 15.5, 2.20), 22.0)),
    4: (((2.85, 11.70, 2.60), (5.1, 15.6, 2.60), 26.0), ((3.75, 13.45, 2.70), (5.2, 15.7, 2.72), 26.0)),
}


def cam_of(sid, g):
    a, b = SETUPS[sid]
    u = ez((g - a) / float(max(1, b - a)), "lin" if sid in (1, 3) else "sine")
    (l0, k0, n0), (l1, k1, n1) = CAMS[sid]
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u)), lerp(n0, n1, u)


# ----------------------------------------------------------------------------- actors: name -> (cast, setups)
ACT = {
    "reader": ("gentleman", (2,)),
    "reader2": ("lady_b", (2,)),
    "boy": ("newsboy", (3,)),
    "walk1": ("lady_c", (3,)),
    "walk2": ("gentleman_b", (3,)),
    "hum": ("lady_d", (4,)),
}
G_HUMWALK = 2404
PPD = {1: 160, 2: 256, 3: 224, 4: 288}


def where(n, g, sid):
    """feet (x, y, z) per frame."""
    if n == "reader":
        return (-2.95, 9.45, 0.0)
    if n == "reader2":
        return (-3.55, 11.75, 0.0)
    if n == "boy":
        return (1.45, 10.4, 0.0)
    if n == "walk1":
        return (3.35 + 0.004 * (g - G24), 19.0 - 0.062 * (g - G24), 0.0)
    if n == "walk2":
        return (0.35 + 0.002 * (g - G24), 23.5 - 0.066 * (g - G24), 0.0)
    if n == "hum":
        d = max(0, g - G_HUMWALK)
        return (3.55 - 0.068 * (d * d / 8.0 if d < 4 else d - 2.0), 14.05 + 0.045 * d, 0.25)


def pose_of(n, g, sid):
    t = g / 30.0
    seed = sum(ord(c) for c in n) * 0.1
    hr, ln, gx, gy = T5.sway(g, seed)
    if n == "reader":
        p = dict(cast7.STORY7["gentleman_read"][1])
        p["head_roll"] = p.get("head_roll", 0.0) + 0.6 * hr
        p["lean"] = p.get("lean", 0.0) + ln
        p["squash"] = (1.0, 1.0 + 0.012 * math.sin(g * 0.9))          # a little shudder of shock
        p["blink"] = blink(g, [2296, 2328])
        p["gaze"] = (0.15 + 0.25 * math.sin(g * 0.25), 0.55)           # eyes run along the lines
    elif n == "reader2":
        p = dict(cast7.STORY7["gentleman_read"][1])
        p.update(expr="surprised", mirror=True, yaw=-0.25, pitch=0.35)
        p["head_roll"] = 4 + hr
        p["blink"] = blink(g, [2310])
    elif n == "boy":
        p = dict(cast7.STORY7["newsboy_shout"][1])
        w = math.sin((g - G24) * 0.42)
        p["arm_r"] = dict(p["arm_r"], hand=(0.52 + 0.06 * w, -0.40 + 0.16 * w))
        p["lean"] = -4 + 3 * w
        p["head_roll"] = -8 + 3 * math.sin((g - G24) * 0.42 + 0.8)
        p["mirror"] = False
        p["blink"] = blink(g, [2372])
    elif n in ("walk1", "walk2"):
        cast = ACT[n][0]
        base = dict(expr="happy", mouth="smile", yaw=0.22, head_roll=4 * math.sin(g * 0.23 + seed), gaze=(-0.5, 0.0) if n == "walk1" else (0.4, 0.0))
        p = cast7.cycle(cast, (g - G24) / 28.0 + seed, "walk", facing=1, base=base, speed=0.8)
        p["blink"] = T5.blinks(g, seed, 60)
    elif n == "hum" and g >= G_HUMWALK:            # strolls off to screen-left, still humming
        d = g - G_HUMWALK
        u = ez(min(1.0, d / 6.0))
        base = dict(expr="happy", mouth="smile", yaw=lerp(0.30, 0.55, u), head_roll=6.0 * math.sin(d * 0.21), gaze=(lerp(0.8, 0.6, u), -0.2))
        p = cast7.cycle("lady_d", d / 28.0, "walk", facing=-1, base=base, speed=lerp(0.3, 0.85, u))
        p["blink"] = 2 if d % 30 in range(12, 22) else 0
        if u < 1.0:                                   # hands leave the waist gradually (no pop at the first step)
            for side, h0 in (("arm_r", (0.10, 0.80)), ("arm_l", (-0.12, 0.80))):
                a = p.get(side)
                if isinstance(a, dict) and "hand" in a:
                    hx, hy = a["hand"]
                    p[side] = dict(a, hand=(lerp(h0[0], hx, u), lerp(h0[1], hy, u)), bend=lerp(0.6, a.get("bend", 0.5), u))
            if isinstance(p.get("legs"), dict):
                p["legs"] = dict(p["legs"], stride=p["legs"].get("stride", 0) * u, lift_r=p["legs"].get("lift_r", 0) * u, lift_l=p["legs"].get("lift_l", 0) * u)
    elif n == "hum":
        p = dict(cast7.STORY7["crowd_stare"][1])
        # mirrored the whole time (faces screen-left, the way she will stroll off), glancing back at the poster: no flip at the walk
        p.update(expr="happy", mouth="smile", yaw=0.30, pitch=-0.25, gaze=(-0.8, -0.3), legs="narrow", mirror=True)
        s = math.sin((g - 2393) * 0.21)
        p["head_roll"] = 9.0 * s                                          # humming, swaying to a tune
        p["lean"] = 2.5 * s
        p["blink"] = 2 if (g - 2393) % 30 in range(12, 22) else blink(g, [2400])   # eyes shut on the long note
        p["arm_r"] = dict(hand=(0.10, 0.80), bend=0.6)
        p["arm_l"] = dict(hand=(-0.12, 0.80), bend=0.6)
    p["t"] = t
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "paris", "kiosk", quality=quality, lens=22.0, name="cam_s23")
        sd = os.path.join(TMP, "sprites")
        for n, (cast, s) in ACT.items():
            self.actors[n] = C.make_actor(n, cast, sd)

    def pose(self, sid, gs):
        for g in gs:
            f = bf(sid, g)
            loc, look, lens = cam_of(sid, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, papers=24)
            for n, a in self.actors.items():
                x, y, z = where(n, g, sid)
                C.place(a, f, (x, y), z)
        jobs = []
        for n, a in self.actors.items():
            if sid not in ACT[n][1]:
                continue
            fr = []
            for g in gs:
                f = bf(sid, g)
                self.scene.frame_set(f)
                a.pose(f, pose_of(n, g, sid), camera=self.cam)
                fr.append(f)
            jobs.append((a, PPD[sid]))
            self.sprites_for([(a, PPD[sid])], fr)

    def _vis(self, sid):
        for n, a in self.actors.items():
            a.set_hidden(sid not in ACT[n][1])

    def report(self, sid, g):
        f = bf(sid, g)
        self._vis(sid)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(sid, g)
        return dict(shot=sid, g=g, cam=[round(c, 3) for c in loc], lens=round(lens, 1), heads=C.head_report(self, f))

    def render(self, sid, gs, out_dir, scale=1.0, samples=12, threads=2):
        self._vis(sid)
        return C.Take.render(self, [bf(sid, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    sids = [int(s) for s in sys.argv[2].split(",")]
    if cmd == "stills":
        Tk = Take("preview")
        for sid in sids:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[sid][0] <= g <= RANGES[sid][1]]
            if not gs:
                continue
            Tk.pose(sid, gs)
            for g in gs:
                print(json.dumps(Tk.report(sid, g)), flush=True)
                out = sys.argv[4]
                scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                st = Tk.render(sid, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (sid, g)))
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), sids, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
