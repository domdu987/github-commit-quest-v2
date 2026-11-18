#!/usr/bin/env python3
"""shot.py -- film 10 take s22: shots 22 + 23 (g 1627..1814, handles g 1621..1626 and g 1815..1820).

    id 22  g 1621..1709  shot 22 (54.24-57.00 s), harbour_wide DAY toward the berth ship (hd1, st0): every ship is dazzle except the
                         admiral's grey one; the admiral and the painter stand on the quay looking at it.  Slow crane-in.
    id 23  g 1710..1820  shot 23 (57.00-60.40 s), hull_plank DAY: the admiral on the hanging stage, brush in hand, paint spots on face,
                         moustache and cap, sheepish, paints a stripe on his own ship (set_stripes 0 -> 0.47, keyed linear).
                         The hard cut on "เอง" (about g 1797-1800) is the director's; frames render past it.
Mouths: nobody speaks.  NO depth of field.  Blender frame of (id, g) = 1000 * (id - 1) + g + 1.
"""
import math, os, sys, json, copy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c10 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast10, sprites = C.D, C.actors, C.camrig, C.cast10, C.sprites
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G22, G23, GEND = C.g_bound(54.24), C.g_bound(57.00), 1815          # 1627, 1710, N
H_IN, H_OUT = 6, 6
RANGES = {22: (G22 - H_IN, G23 - 1), 23: (G23, GEND - 1 + H_OUT)}
LOCS = {22: ("harbour", "harbour_wide", "DAY"), 23: ("harbour", "hull_plank", "DAY")}


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def pose_of(name, **kw):
    cast, p = cast10.STORY10[name]
    p = copy.deepcopy(p)
    p.update(kw)
    return cast, p


def lerp_v(a, b, u):
    return tuple(lerp(a[i], b[i], u) for i in range(3))


CAM22_A = ((-24.0, -28.0, 19.0), (20.0, 18.0, 3.0))
CAM22_B = ((5.0, -18.5, 6.5), (15.5, 7.0, 4.6))
LENS22 = 22.0
CAM23_A = ((-4.0, -8.4, 3.9), (-3.8, 1.2, 4.7))
CAM23_B = ((-2.2, -4.9, 4.0), (-1.9, 1.2, 4.7))
LENS23 = 24.0
STRIPE_END = 0.62


def cam_of(shot, g):
    if shot == 22:
        x = clamp((g - RANGES[22][0]) / float(RANGES[22][1] - RANGES[22][0]))
        a, b = CAM22_A, CAM22_B
    else:
        x = clamp((g - G23) / float(GEND - G23))
        a, b = CAM23_A, CAM23_B
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector(lerp_v(a[0], b[0], u)), Vector(lerp_v(a[1], b[1], u))


def adm22(g):
    cast, p = pose_of("admiral_arms_akimbo", expr="worried", mouth="flat", fx=["sweat"])
    u = u_of(g, 1650, 1700)
    p["head_roll"] = 4 * u + 1.5 * math.sin(g * 0.1)
    look = u_of(g, 1650, 1685)                             # he looks UP at his own grey ship before the cut
    p["pitch"] = lerp(-0.3, -0.95, look)
    p["gaze"] = (lerp(0.2, 0.35, look), lerp(0.0, -1.0, look))
    p["yaw"] = lerp(p.get("yaw", 0.4), 0.15, look)
    p["blink"] = blink(g, [1640, 1688])
    return p


def pai22(g):
    cast, p = pose_of("painter_calm_smile")
    p["lean"] = 1.2 * math.sin(g * 0.09)
    p["blink"] = blink(g, [1655, 1696])
    return p


G_LAST = 1798                                              # his last stroke lands on the cut at "เอง" (59.9 s)
BRUSH_DX = 1.25                                            # brush tip is this far right of his feet (D)
FRONT_OFF = 0.0                                            # calibration of the stripe front vs the brush (D)


def adm_x(g):
    """he shuffles along the stage to the right while he paints (the stripe front follows the brush)."""
    x = clamp((g - G23) / float(G_LAST - G23))
    return lerp(-5.0, -2.5, 0.3 * ez(x, "sine") + 0.7 * x)


def stripe_of(g):
    """set_stripes stage whose front sits at the brush tip: lags behind by 3 D at the start, closes to 0 at g_last (about 52 D per stage unit,
    stage 0.45 = front at x -3 at brush height)."""
    x = clamp((g - G23) / float(G_LAST - G23))
    lag = 3.2 * (1.0 - x) ** 1.5
    fx = adm_x(g) + BRUSH_DX - lag + FRONT_OFF
    return clamp(0.4 + (fx + 5.8) / 60.0, 0.0, 0.5)         # measured: at brush height the front runs x -5.8 (stage 0.40) .. +0.3 (0.50), then stops


def blobs(f, pose):
    """big paint blobs for phone size (puppet-local D, head centre at the origin): navy on the moustache and the cheek, white on the cap."""
    return ('<g stroke="#10173a" stroke-width="0.012">'
            '<path d="M-0.02,0.15 C0.10,0.10 0.30,0.14 0.30,0.25 C0.28,0.36 0.08,0.36 -0.02,0.28 Z" fill="#1f2f5a"/>'
            '<ellipse cx="0.20" cy="0.34" rx="0.035" ry="0.07" fill="#1f2f5a"/>'
            '<path d="M-0.30,-0.40 C-0.20,-0.52 0.00,-0.50 0.02,-0.38 C-0.05,-0.30 -0.25,-0.30 -0.30,-0.40 Z" fill="#f4f1e6"/>'
            '<circle cx="-0.33" cy="0.10" r="0.085" fill="#1f2f5a"/><circle cx="-0.38" cy="0.20" r="0.035" fill="#f4f1e6"/>'
            '</g>')


def adm23(g):
    """on the stage, brush sweeping the hull (screen-right), a sheepish glance back at us; the brush goes up and down."""
    cast, p = pose_of("admiral_plank_sheepish", plank=0, expr="sheepish")
    ph = (g - G23) / 22.0 * 2 * math.pi
    sw = 0.5 - 0.5 * math.cos(ph)                         # 0..1 sweep
    ar = dict(p["arm_r"])
    ar["hand"] = (lerp(0.78, 0.98, sw), lerp(0.50, 0.20, sw))
    p["arm_r"] = ar
    pr = dict(p["prop_r"])
    pr["angle"] = lerp(-12, -44, sw)
    p["prop_r"] = pr
    p["t"] = g / 30.0
    p["paint_spots"] = 1.0
    al = dict(p["arm_l"])
    al["hand"] = (al["hand"][0], al["hand"][1] + 0.05 * math.sin(g * 0.3))     # the scratching hand fidgets
    p["arm_l"] = al
    p["head_roll"] = p.get("head_roll", 0.0) + 2.5 * math.sin(g * 0.11)
    p["blink"] = blink(g, [1735, 1778])
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=22):
        loc, preset, light = LOCS[shot]
        C.Take.__init__(self, loc, preset, quality=quality, lens=LENS22 if shot == 22 else LENS23, name="cam_s22", light=light)
        self.shot = shot
        if shot == 22:                                       # QA-tech: no mirrored ships (they read as translucent blue panels on the water)
            self.scene.cycles.glossy_bounces = 0
        for ob in D.STATE.get("cards", []):               # old placeholder cards hidden
            ob.hide_render = True
        sd = os.path.join(TMP, "sprites")
        if shot == 22:
            self.adm = self.actors["adm"] = C.make_actor("adm", "admiral", sd)
            self.pai = self.actors["pai"] = C.make_actor("pai", "painter10", sd)
        else:
            self.adm = self.actors["adm"] = C.make_actor("adm", "admiral", sd)

    def pose(self, shot, gs):
        A = self.A
        mk = A["marks"]
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS22 if shot == 22 else LENS23)
            if shot == 22:
                self.key_set(f, harbour_dazzle=1.0, stripes=0.0)
                C.place(self.adm, f, (14.0, -8.0, 0.0))
                C.place(self.pai, f, (10.4, -9.4, 0.0))
            else:
                ax = adm_x(g)
                self.key_set(f, harbour_dazzle=1.0, stripes=stripe_of(g))
                C.place(self.adm, f, (ax, mk["admiral_plank"][1], mk["admiral_plank"][2]))
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 22:
                self.adm.pose(f, adm22(g), camera=self.cam)
                self.pai.pose(f, pai22(g), camera=self.cam)
            else:
                self.adm.pose(f, adm23(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        if shot == 22:
            self.sprites_for([(self.adm, 200), (self.pai, 200)], fr)
        else:
            self.sprites_for([(self.adm, 320, blobs)], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

def main():
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take("preview", shot)
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
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples,
                     take_key=lambda shot: LOCS[shot][1])


if __name__ == "__main__":
    main()
