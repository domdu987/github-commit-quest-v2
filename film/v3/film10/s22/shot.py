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
CAM22_B = ((5.0, -18.5, 6.5), (15.5, 7.0, 1.8))
LENS22 = 22.0
CAM23_A = ((-4.7, -8.4, 3.9), (-4.5, 1.2, 4.7))
CAM23_B = ((-2.5, -4.9, 4.0), (-2.3, 1.2, 4.7))
LENS23 = 24.0
STRIPE_END = 0.62


def cam_of(shot, g):
    if shot == 22:
        x = clamp((g - RANGES[22][0]) / float(1658 - RANGES[22][0]))          # arrives close by g 1658 (heads >= 40 px), then drifts on
        a, b = CAM22_A, CAM22_B
        u = ez(x, "sine")
        base = Vector(lerp_v(a[0], b[0], u)), Vector(lerp_v(a[1], b[1], u))
        d = clamp((g - 1658) / float(RANGES[22][1] - 1658))
        return base[0] + Vector((0.9, 0.6, 0.1)) * d, base[1] + Vector((0.5, 0.2, 0.0)) * d
    else:
        x = clamp((g - G23) / float(GEND - G23))
        a, b = CAM23_A, CAM23_B
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector(lerp_v(a[0], b[0], u)), Vector(lerp_v(a[1], b[1], u))


def adm22(g):
    cast, p = pose_of("admiral_arms_akimbo", expr="worried", mouth="flat", fx=["sweat"])
    u = u_of(g, 1650, 1700)
    p["head_roll"] = 4 * u + 1.5 * math.sin(g * 0.1)
    look = u_of(g, 1655, 1690)                             # he looks UP at his own grey ship before the cut
    p["pitch"] = lerp(-0.3, -1.05, look)
    p["gaze"] = (lerp(0.2, 0.35, look), lerp(0.0, -1.0, look))
    p["yaw"] = lerp(p.get("yaw", 0.4), 0.15, look)
    p["blink"] = blink(g, [1640, 1688])
    return p


def pai22(g):
    cast, p = pose_of("painter_calm_smile", expr="neutral", mouth="smile")      # calm closed-mouth smile
    p["lean"] = 1.2 * math.sin(g * 0.09)
    p["blink"] = blink(g, [1655, 1696])
    return p


G_LAST = 1798                                              # his last stroke lands on the cut at "เอง" (59.9 s)
BRUSH_DX = 1.12                                            # brush tip is this far right of his feet (D)
FRONT_OFF = 0.0                                            # calibration of the stripe front vs the brush (D)


def adm_x(g):
    """he shuffles along the stage to the right while he paints (the stripe front follows the brush)."""
    x = clamp((g - G23) / float(G_LAST - G23))
    return lerp(-5.6, -3.4, 0.3 * ez(x, "sine") + 0.7 * x)


def front_x(g):
    """world x of the brush tip (the painted front sits exactly there)."""
    ph = (g - G23) / 22.0 * 2 * math.pi
    sw = 0.5 - 0.5 * math.cos(ph)
    return adm_x(g) + BRUSH_DX + 0.2 * (sw - 0.5)


def stripe_of(g):
    """set_stripes stage whose front sits at the brush tip: lags behind by 3 D at the start, closes to 0 at g_last (about 52 D per stage unit,
    stage 0.45 = front at x -3 at brush height)."""
    x = clamp((g - G23) / float(G_LAST - G23))
    lag = 3.2 * (1.0 - x) ** 1.5
    fx = adm_x(g) + BRUSH_DX - lag + FRONT_OFF
    return clamp(0.4 + (fx + 5.8) / 60.0, 0.0, 0.5)         # measured: at brush height the front runs x -5.8 (stage 0.40) .. +0.3 (0.50), then stops


def blobs(f, pose):
    """wet paint blobs for phone size (puppet-local D, head centre at the origin): WHITE on the moustache and the cap peak, NAVY on the cheek,
    each with a gloss highlight and a drip, dark outlines so they read against the same-coloured ground."""
    ol = 'stroke="#10173a" stroke-width="0.016" stroke-linejoin="round"'
    return (
        # moustache: white blob + shade crescent + gloss + drip
        '<path d="M-0.04,0.16 C0.08,0.10 0.30,0.15 0.31,0.25 C0.29,0.34 0.06,0.35 -0.04,0.27 Z" fill="#fdfdf8" %s/>' % ol +
        '<path d="M0.02,0.31 C0.12,0.34 0.24,0.33 0.29,0.27 C0.22,0.36 0.08,0.36 0.02,0.31 Z" fill="#aab6d6"/>'
        '<ellipse cx="0.10" cy="0.19" rx="0.05" ry="0.018" fill="#ffffff" transform="rotate(-12 0.10 0.19)"/>'
        '<path d="M0.17,0.33 C0.15,0.42 0.15,0.47 0.18,0.47 C0.21,0.47 0.21,0.42 0.20,0.33 Z" fill="#fdfdf8" %s/>' % ol +
        # cap peak: white blob + gloss + drip
        '<path d="M-0.34,-0.40 C-0.24,-0.54 0.00,-0.52 0.03,-0.38 C-0.05,-0.29 -0.27,-0.28 -0.34,-0.40 Z" fill="#fdfdf8" %s/>' % ol +
        '<ellipse cx="-0.14" cy="-0.44" rx="0.06" ry="0.02" fill="#ffffff" transform="rotate(-10 -0.14 -0.44)"/>'
        '<path d="M-0.20,-0.31 C-0.22,-0.22 -0.22,-0.18 -0.19,-0.18 C-0.16,-0.18 -0.16,-0.22 -0.17,-0.31 Z" fill="#fdfdf8" %s/>' % ol +
        # cheek: navy blob + gloss + drip
        '<path d="M-0.42,0.02 C-0.36,-0.06 -0.20,-0.04 -0.19,0.06 C-0.20,0.15 -0.38,0.17 -0.42,0.09 Z" fill="#1f2f5a" %s/>' % ol +
        '<ellipse cx="-0.33" cy="0.00" rx="0.045" ry="0.016" fill="#8aa0e0" transform="rotate(-15 -0.33 0.00)"/>'
        '<path d="M-0.30,0.14 C-0.32,0.24 -0.32,0.29 -0.29,0.29 C-0.26,0.29 -0.26,0.24 -0.27,0.14 Z" fill="#1f2f5a" %s/>' % ol)


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


# ----------------------------------------------------------------------------- the zebra bands he paints (runtime set dressing)
BAND_W, BAND_LEAN, Z0, Z1, ZB = 1.2, 0.7, 3.15, 6.1, 5.1   # band width (D), slant (dx per dz), painted height range, brush height
BAND_X0 = -10.0
NAVY, WHITE = "#1f2f5a", "#f2eee2"


def band_polys(fx):
    """[(colour, [(x,z) ...quad grid cells]) ...] of the finished bands and the growing one, up to the front fx (at brush height)."""
    out = []
    zs = [Z0 + i * (Z1 - Z0) / 6.0 for i in range(7)]
    k = 0
    while BAND_X0 + k * BAND_W < fx:
        a = BAND_X0 + k * BAND_W
        b = min(a + BAND_W, fx)
        quads = []
        for i in range(6):
            za, zb = zs[i], zs[i + 1]
            la, lb = BAND_LEAN * (za - ZB), BAND_LEAN * (zb - ZB)
            quads.append([(a + la, za), (b + la, za), (b + lb, zb), (a + lb, zb)])
        out.append((WHITE if k % 2 == 0 else NAVY, quads))
        k += 1
    return out


class Bands(object):
    """paint bands as thin meshes laid on the hull (raycast to the plating), one object per rendered frame, shown only on its frame."""

    def __init__(self, take):
        import bpy
        self.bpy, self.take = bpy, take
        self.hull = bpy.data.objects["hull_berth"]
        self.mats = {WHITE: D.STATE["C"](WHITE, 1.0, 1.0, True), NAVY: D.STATE["C"](NAVY, 1.0, 1.0, True)}

    def hull_y(self, x, z):
        sc = self.bpy.context.scene
        dg = self.bpy.context.evaluated_depsgraph_get()
        o = Vector((x, -12.0, z))
        for _ in range(6):
            ok, loc, nor, idx, ob, mat = sc.ray_cast(dg, o, Vector((0, 1, 0)))
            if not ok:
                return 1.2
            if ob.name == "hull_berth":
                return loc.y - 0.035
            o = loc + Vector((0, 0.01, 0))
        return 1.2

    def make(self, f, fx):
        bpy = self.bpy
        for col, quads in band_polys(fx):
            verts, faces = [], []
            for q in quads:
                base = len(verts)
                for (x, z) in q:
                    verts.append((x, self.hull_y(x, z), z))
                faces.append((base, base + 1, base + 2, base + 3))
            me = bpy.data.meshes.new("band_%d" % f)
            me.from_pydata(verts, [], faces)
            me.update()
            ob = bpy.data.objects.new("band_%d_%s" % (f, col[1:]), me)
            D.STATE["SET"].objects.link(ob)
            me.materials.append(self.mats[col])
            ob.visible_shadow = False
            ob.visible_glossy = False
            for fr, hid in ((f - 1, True), (f, False), (f + 1, True)):
                ob.hide_render = hid
                ob.keyframe_insert("hide_render", frame=fr)
            fc = C._fcurve(ob, "hide_render")
            if fc is not None:
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"


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
            self.bands = Bands(self)

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
                self.key_set(f, harbour_dazzle=1.0, stripes=0.30 * clamp((g - G23) / float(G_LAST - G23)))
                C.place(self.adm, f, (ax, mk["admiral_plank"][1], mk["admiral_plank"][2]))
                self.scene.frame_set(f)
                self.bands.make(f, front_x(g))
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
