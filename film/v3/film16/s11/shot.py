#!/usr/bin/env python3
"""shot.py -- film 16 take s11 = shot 11 (CHAMBER chamber_wide_high-style HIGH angle, DAY): "ทั้งสภาหัวเราะครืน แล้วเรียกเขาว่า ไอ้บ้าลวด".
Shot 11 = g 698..784 (23.26-26.18 s); handles 9 f each side (hard cuts).
    g 689..768  the whole chamber laughs: ~14 congressmen on the tiers (laugh / point poses, hats bounce ~0.06 D at ~3 Hz with squash), the mocker
                at his desk in a belly laugh (tears + blush), Morse at the front table clutching his coil (morse_clutch_coil).  The camera glides
                from the right bank of the tiers across the room (slide), high (~4 D above head height, ~14 deg down).
    g 764..780  SNAP push on "ไอ้บ้าลวด" (event g 769): the camera flies in to a close of Morse (head ~280 px), ease peak 1.8
    g 768       Morse's pose swaps clutch -> snap_up (chin up, jaw set) on the closed frame of a blink (767 half, 768 closed, 769 half)
Mouths: nobody speaks here (the mocker's laugh is the pose's own laughing mouth); only expression mouths.

    python3 shot.py camreport | probe a:b[:s] | stills a:b[:s] out_dir [scale] [spp] | final a:b[:s] [scale] [spp]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

TG, K, actors, cast16 = C.TG, C.K, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

# ------------------------------------------------------------------ timing
G0, G1 = C.g_bound(23.26), C.g_bound(26.18)              # 698, 785 (exclusive)
H_IN, H_OUT = 9, 9
GS = list(range(G0 - H_IN, G1 + H_OUT))                  # 689..793
G_LAST = GS[-1]
G_WORD = C.cap_g("ไอ้บ้าลวด")                            # 769
SNAP = (G_WORD - 5, G_WORD + 11)                         # 764..780 (16 f)
G_SWAP = G_WORD - 1                                      # 768: clutch -> snap_up on the closed frame of the blink 767..769
LIGHT, PRESET = "DAY", "chamber_wide_high"
MORSE_MARK = (-5.6, 8.6, 0.0)                            # beside the left end of the front table (as s08)


class PathCam(C.CamPath):
    """glide A -> B (constant speed, so the shot is moving on its first frame), then a SNAP to the close C, then a slow push on."""

    def __init__(self, A, B, C_, g0, g1, snap, push_after=0.06):
        self.A, self.B, self.Cc = A, B, C_
        self.g0, self.g1, self.snap = g0, g1, snap
        self.push_after = push_after
        self.lens = 22.0

    def base(self, g):
        u = (g - self.g0) / float(self.snap[0] - self.g0)
        u = max(0.0, min(1.0, u))
        u = 0.25 * u + 0.75 * C.camrig.ease_peak(u, 2.0)       # dwell on the banks (where the crowd is), cross the empty dais quickly; still moving at both ends
        return self.A[0].lerp(self.B[0], u), self.A[1].lerp(self.B[1], u)

    def at(self, g):
        loc, look = self.base(g)
        a, b = self.snap
        s = C.camrig.ease_peak((g - a) / float(b - a), 1.8) if g > a else 0.0
        if s > 0.0:
            # fly in along an arc-free line: look point leads (it reaches the target earlier than the camera) so the framing settles on Morse
            sl = min(1.0, s * 1.08)
            loc = loc.lerp(self.Cc[0], s)
            look = look.lerp(self.Cc[1], sl)
        if g > b:
            t = (g - b) / 30.0
            d = (self.Cc[1] - self.Cc[0])
            loc = loc + d * (1.0 - 1.0 / (1.0 + self.push_after * t))
        return loc, look


CASTS = ["congressman_a", "congressman_b", "congressman_c"]


def seat_world(d):
    ti, a, px, py, zt = d
    return tuple(K.W((px + 0.95 * math.cos(a), py + 0.95 * math.sin(a), zt)))


def visible(pt, cam):
    loc, look = cam
    f, r, u = C._cam_basis(loc, look)
    d = Vector(pt) - loc
    z = d.dot(f)
    if z <= 0.5:
        return None
    return (C.W_PX / 2 + C.F_PX * d.dot(r) / z, C.H_PX / 2 - C.F_PX * d.dot(u) / z, z)


def pick_audience(cams, n, tiers=(0, 1, 2), skip=()):
    out = []
    for d in TG.STATE["desks"]:
        if d[0] not in tiers:
            continue
        p = seat_world(d)
        head = Vector(p) + Vector((0, 0, 2.7))
        ok = False
        for cm in cams:
            s = visible(head, cm)
            if s is not None and (25 < s[0] < 695 and 200 < s[1] < 800):
                ok = True
        if ok and not any((Vector(p) - Vector(q)).length < 1.6 for q in skip):
            out.append((p, d[0]))
    out.sort(key=lambda t: (round(t[0][0] / 3.0), t[0][1]))
    step = max(1, len(out) // max(1, n))
    return out[::step][:n]


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s11")
        A = self.A
        mm = Vector(MORSE_MARK)
        self.cam_path = PathCam((Vector((3.0, 11.0, 4.0)), Vector((14.0, 23.0, 2.6))),
                                (Vector((-3.0, 11.0, 4.0)), Vector((-14.0, 23.0, 2.6))),
                                (Vector((mm.x + 1.0, mm.y - 2.6, 3.9)), Vector((mm.x - 0.15, mm.y, 3.0))), GS[0], G_LAST, SNAP)
        self.key_cam(bf(GS[0]), *self.cam_path.at(GS[0]))
        self.scene.frame_set(bf(GS[0]))
        sd = os.path.join(WORK, "sprites")
        self.mor = self.add("mor", "morse16", MORSE_MARK, sd)
        self.mock = self.add("mock", "mocker", A["marks"]["mocker_desk"], sd)
        self.aud = []
        cams = [self.cam_path.at(g) for g in (GS[0], 725, 764)]
        pick = pick_audience(cams, 26, tiers=(0, 1, 2), skip=[A["marks"]["mocker_desk"], MORSE_MARK])
        for i, (p, ti) in enumerate(pick):
            a = self.add("c%d" % i, CASTS[i % 3], p, sd)
            a.kind = "point" if i % 3 == 1 else "laugh"
            a.sideflip = p[0] > MORSE_MARK[0]
            a.phase = (i * 0.37) % 1.0
            self.aud.append(a)

    def add(self, name, cast, mark, sd):
        a = C.make_actor(name, cast, sd, cam=self.cam)
        a.mark = tuple(mark)
        self.actors[name] = a
        a.sideflip = False
        return a

    # ---- bounce: abs(sin) at ~3 Hz (one hop per 1/3 s) + a squash that alternates with it
    @staticmethod
    def hop(g, ph, amp=0.06):
        x = 3.0 * g / 30.0 + ph
        return amp * abs(math.sin(math.pi * x)), math.sin(2 * math.pi * x)

    def morse_pose(self, g):
        clutch = g < G_SWAP
        p = dict(cast16.STORY16["morse_clutch_coil" if clutch else "morse_snap_up"][1])
        p["mirror"] = False
        p["blink"] = blink(g, [G_SWAP - 1, 705, 741])
        p["lean"] = 1.5 * math.sin(g * 0.3)
        if clutch:
            p["fx"] = []                                          # no sweat: only the sting of being laughed at
        return p

    def mock_pose(self, g):
        p = dict(cast16.STORY16["mocker_belly_laugh"][1])
        p["mirror"] = False
        p["fx"] = ["tears", "blush"]
        p["t"] = (g * 0.09) % 1.0
        dz, s = self.hop(g, 0.0)
        p["squash"] = (1.01 + 0.02 * s, 0.99 - 0.02 * s)
        return p

    def aud_pose(self, a, g):
        name = "%s_%s" % (a.cast, a.kind)
        p = dict(cast16.STORY16[name][1])
        p["mirror"] = a.sideflip
        p["fx"] = ["tears"] if a.kind == "laugh" else []
        p["t"] = (g * 0.08 + a.phase) % 1.0
        dz, s = self.hop(g, a.phase)
        p["squash"] = (1.01 + 0.02 * s, 0.99 - 0.02 * s)
        return p

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.cam_path.at(g))
            C.place(self.mor, f, MORSE_MARK)
            dz, _ = self.hop(g, 0.0)
            C.place(self.mock, f, (self.mock.mark[0], self.mock.mark[1], self.mock.mark[2] + dz))
            for a in self.aud:
                dz, _ = self.hop(g, a.phase)
                C.place(a, f, (a.mark[0], a.mark[1], a.mark[2] + dz))
            self.key_set(f, flames=1.0, shafts=True)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mor.pose(f, self.morse_pose(g), camera=self.cam)
            self.mock.pose(f, self.mock_pose(g), camera=self.cam)
            for a in self.aud:
                a.pose(f, self.aud_pose(a, g), camera=self.cam)
        jobs = [(self.mor, 448), (self.mock, 128)] + [(a, 128) for a in self.aud]
        self.sprites_for(jobs, [bf(g) for g in gs])

    def report(self, g):
        return dict(g=g, cam=[round(c, 2) for c in self.cam_path.at(g)[0]], heads=C.head_report(self, bf(g)))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if GS[0] <= g <= G_LAST] if len(sys.argv) > 2 else []
    if cmd == "camreport":
        Tk = Take("preview")
        rows, worst = Tk.cam_path.report(GS[:-1])
        print(rows[0], rows[len(rows) // 2], rows[-1])
        print("longest run under 0.25 px/frame: %d frames (bible max 6); min px %.2f max %.2f" % (worst, min(r["px"] for r in rows), max(r["px"] for r in rows)))
    elif cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["chamber"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
