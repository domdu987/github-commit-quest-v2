#!/usr/bin/env python3
"""shot.py -- film 6 take s02: shot 2 only (plan 2.10-3.60 s = g 63..107) + 6 handle frames each side (g 57..113), bakery MORNING.

    shot 2  ECU insert of the customer's basket on the inside counter (same basket card / position as s01): the paler 13th loaf
            drops into frame from above, lands on top of the pile of 12 (g 74, squash + settle), and a white steam puff blooms
            off it (g 74..100) while thin wisps keep rising; slow push-in + slight tilt down the whole shot (never static).
            transition_in: cut (from s01's medium).  Nobody in frame (no mouths, no heads).
NO depth of field anywhere (client rule): C.Take switches it off at build and before every render.

    python3 shot.py stills 2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, ez, bf = C.lerp, C.clamp, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(2.10), C.g_bound(3.60)       # 63, 108
H = 6
RANGES = {2: (G0 - H, G1 + H - 1)}              # 57 .. 113
G_IN = 66                                       # loaf enters the top of frame
G_LAND = 74                                     # lands on the pile ("ที่สิบสามลง" 2.23 s = g 70 .. 88)
G_PUFF = 74

BASKET = Vector((1.30, 1.08, 1.25))
BASKET_SCALE = 1.4
TOP = (0.014, 0.128)                            # where the 13th sits in the basket drawing (s01's top spot)
CAM_A = ((1.20, -1.05, 2.50), (1.30, 1.08, 1.90))
CAM_B = ((1.22, -0.70, 2.42), (1.30, 1.08, 1.92))
LENS = 30.0
STEAM = 0.5

PALE = dict(light="#fdeccb", base="#f0cd92", dark="#cf9a5c", crust="#b07440", score="#fff3d8")


def pale_loaf_svg(uid, r):
    s = cast6.loaf_svg(uid, r=r, seed=4)
    for k, v in cast6.BREAD.items():
        if k in PALE:
            s = s.replace(v, PALE[k])
    return s


def puff_svg(uid, k, seed=0, big=True):
    """cartoon steam: crisp-edged white cloud puffs + curling wisp strokes rising from (0, 0), fading toward their tops;
    k = 0..1 phase (big puff: grows, rises, fades; wisps: one scroll period)."""
    o = []
    env = math.sin(math.pi * clamp(k)) ** 0.6 if big else 1.0
    h = (0.30 + 0.55 * k) if big else 0.75
    nw = 4 if big else 3
    for i in range(nw):
        ph = seed * 1.7 + i * 2.1
        x0 = (i - (nw - 1) / 2.0) * 0.06
        pts = []
        for j in range(13):
            t = j / 12.0
            y = -t * h - (0.0 if big else 0.0)
            x = x0 * (1 + 1.4 * t) + 0.10 * math.sin(t * 7.0 + ph - k * 2 * math.pi) * (0.3 + t)
            pts.append((x, y))
        base_op = (0.70 if big else 0.42) * env
        for a in range(3):                                  # three segments, fading upward
            seg = pts[a * 4:a * 4 + 5]
            d = "M%.4f,%.4f " % seg[0] + " ".join("L%.4f,%.4f" % q for q in seg[1:])
            o.append('<path d="%s" fill="none" stroke="#ffffff" stroke-width="%.3f" stroke-linecap="round" stroke-linejoin="round" opacity="%.3f"/>'
                     % (d, (0.040 if big else 0.030) * (1 - 0.2 * a), base_op * (1.0, 0.65, 0.3)[a]))
    if big:
        for i in range(7):
            a = i * 0.9 + seed
            rr = (0.05 + 0.03 * (i % 3)) * (0.7 + 0.9 * k)
            cx = 0.13 * math.sin(a) * (0.4 + k)
            cy = -0.06 - (0.06 + 0.05 * i) * (0.5 + 1.0 * k)
            o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff" opacity="%.3f"/>' % (cx, cy, rr, 0.55 * env * (1 - 0.6 * k)))
    return '<g id="%s">%s</g>' % (uid, "".join(o))


PUFF_BOX = (-0.7, -1.7, 0.7, 0.05)
PUFF_N = 26                                     # g 74 .. 99
WISP_N = 24                                     # looping thin wisps (period 24 frames)


def cam(g):
    u = ez((g - RANGES[2][0]) / float(RANGES[2][1] - RANGES[2][0]), "sine")
    return Vector(lerp(CAM_A[0], CAM_B[0], u)), Vector(lerp(CAM_A[1], CAM_B[1], u))


def loaf_z(g, top_z):
    """height of the falling loaf centre (world z) above its rest point; squash factor."""
    if g < G_IN:
        return None, 1.0
    if g <= G_LAND:
        u = (g - G_IN) / float(G_LAND - G_IN)
        return top_z + 1.6 * (1 - u * u), 1.0
    sq = {G_LAND + 1: 0.82, G_LAND + 2: 1.08, G_LAND + 3: 0.96, G_LAND + 4: 1.02}.get(g, 1.0)
    return top_z, sq


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=LENS, name="cam_s02")
        pd = os.path.join(TMP, "props")
        svg, an = cast6.basket_svg("bk12", loaves=12)
        bbox = (-0.56, -0.06, 0.56, 0.72)
        self.basket = C.PropCard("basket", C.svg_pngs([(svg, bbox, 640)], pd), bbox, scale=BASKET_SCALE, shadow=True)
        loc0, _ = cam(RANGES[2][0])
        self.basket.put(BASKET + Vector((0, 0, 0.66 * BASKET_SCALE)), face=loc0)
        r = cast6.BASKET_LR * 1.08
        lb = (-r * 1.3, -r * 1.2, r * 1.3, r * 0.9)
        self.loaf = C.PropCard("loaf13", C.svg_pngs([(pale_loaf_svg("lf13", r), lb, 1600)], pd), lb, scale=BASKET_SCALE, shadow=True)
        self.top = self.basket.to_world(TOP)
        items = [(puff_svg("pf%d" % i, i / float(PUFF_N - 1), seed=1), PUFF_BOX, 400) for i in range(PUFF_N)]
        self.puff = C.PropCard("puff", C.svg_pngs(items, pd), PUFF_BOX, scale=1.0, shadow=False)
        items = [(puff_svg("ws%d" % i, i / float(WISP_N), seed=3, big=False), PUFF_BOX, 400) for i in range(WISP_N)]
        self.wisp = C.PropCard("wisp", C.svg_pngs(items, pd), PUFF_BOX, scale=0.8, shadow=False)
        for pc in (self.puff, self.wisp):
            for ob in pc.cards:
                ob.visible_shadow = False

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam(g)
            self.key_cam(f, loc, look)
            self.key_set(f, steam=STEAM, oven=1.0)
            toward = (loc - self.top).normalized()
            z, sq = loaf_z(g, self.top.z)
            if z is None:
                self.loaf.show(None, frame=f)
            else:
                self.loaf.show(0, frame=f)
                self.loaf.root.scale = (BASKET_SCALE * (2 - sq) ** 0.5, BASKET_SCALE, BASKET_SCALE * sq)
                self.loaf.root.keyframe_insert("scale", frame=f)
                self.loaf.put(Vector((self.top.x, self.top.y, z)) + toward * 0.03, face=loc, frame=f)
            k = g - G_PUFF
            base = self.top + Vector((0, 0, 0.08)) + toward * 0.05
            if 0 <= k < PUFF_N:
                self.puff.show(k, frame=f)
            else:
                self.puff.show(None, frame=f)
            self.puff.put(base, face=loc, frame=f)
            if g >= G_LAND + 6:
                self.wisp.show((g - G_LAND) % WISP_N, frame=f)
            else:
                self.wisp.show(None, frame=f)
            self.wisp.put(base + toward * 0.01, face=loc, frame=f)
            self.basket.put(self.basket.root.location, face=loc, frame=f)

    def report(self, shot, g):
        f = bf(shot, g)
        loc, look = cam(g)
        z, sq = loaf_z(g, self.top.z)
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads={}, loaf_z=None if z is None else round(z, 3), squash=sq)
        out["top_px"] = [round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(self.top), f)[:2]]
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd == "stills":
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            Tk.pose(shot, gs)
            out = sys.argv[4]
            scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
            samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
