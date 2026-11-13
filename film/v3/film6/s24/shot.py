#!/usr/bin/env python3
"""shot.py -- film 6 take s24: shots 24, 25, 26 (plan 64.50-73.87 s = g 1935..2215) + 6-frame handles (g 1929..1934, 2216..2221),
market AFTERNOON.

    shot 24  g 1935..2052  (in-handle g 1929..1934)  "...ผู้ตรวจขนมปังของพระราชา แล้วเทขนมปังทั้งตะกร้าลงบนตาชั่ง"
             A g 1929..1974  medium, low: inspector_royal (hood down, tabard + chain) at the big balance, the basket of 12 in his
                             hands, stern, turns to the bread pan (slow push)
             B g 1975..2018  side two-shot: he tips the basket, the loaves tumble onto the bread pan (set_loaves 0 -> 12 while the
                             basket's own drawing empties 12 -> 0)
             C g 2019..2052  wide frontal of the whole balance: 12 loaves on the bread pan, the beam stays down on the weights side
                             (set_big_scale(-7) the whole take); he looks up at the beam
    shot 25  g 2053..2129   "ตาชั่งไม่ขยับ ขาดไปนิดเดียว"
             D g 2053..2092  ECU the pivot and the brass pointer: tilted off the centre mark of a little dial (runtime prop), push
             E g 2093..2129  low close-up of the inspector under the tilted beam, eyes narrowing ("a hair short")
    shot 26  g 2130..2215  (out-handle g 2216..2221)  "ทหารลากลุงเฮนรี่ไปที่ขื่อ ทั้งตลาดหยิบผักเน่าขึ้นมารอ"
             F g 2130..2176  pillory side, low: guard1 (ahead, leaning back) and guard2 drag pale henry (heels in) toward the
                             pillory steps; townsfolk behind
             G g 2177..2221  over the crowd: woman1 (tomato) and man1 (cabbage) in the foreground raise rotten veg overhead
                             (g 2180..2190, on "ผักเน่าขึ้น"), henry hauled to the platform steps beyond
Mouths: nobody speaks (no quoted line in 24-26): static expression mouths only.  NO depth of field (common.Take).
Internal shot ids 24, 25, 26: Blender frame of g = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 24 a:b[:step]
    python3 shot.py stills 24,25 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 24,25,26 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6, render = C.B, C.actors, C.camrig, C.cast6, C.render
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(64.50), C.g_bound(73.87)            # 1935, 2216
H = 6
RANGES = {24: (G0 - H, C.g_bound(68.43) - 1), 25: (C.g_bound(68.43), C.g_bound(71.00) - 1), 26: (C.g_bound(71.00), G1 + H - 1)}
# framings (g ranges, inclusive)
FR = dict(A=(1929, 1974), B=(1975, 2018), C=(2019, 2052), D=(2053, 2092), E=(2093, 2129), F=(2130, 2176), G=(2177, 2221))
BEAM = -7.0                                              # the short dozen: weights pan down, the whole take
G_POUR = (1984, 2016)                                    # tilt in 1984..1990, loaves fall 1990..2014 ("แล้วเทขนมปัง" 66.06 = g 1985)
G_RAISE = (2180, 2190)                                   # "ผักเน่าขึ้น" 72.76 s = g 2186

# ----------------------------------------------------------------------------- staging (market world D)
INSP = (1.75, 4.75)                                      # left of the bread pan (pan centre (3, 6), R 1.05)
HEN_PATH = ((0.85, 6.55), (-0.25, 6.45))                 # shot 26 F: henry dragged toward the pillory steps (-4, 6.2)
HEN_PATH_G = ((-0.60, 6.40), (-2.60, 6.25))              # shot 26 G: on to the foot of the steps

BYSTANDERS = dict(C={"tw1": (3.93, 1.49), "tm1": (7.01, 3.64), "tb1": (8.26, 4.36)},
                  F={"tw1": (-6.6, 4.6), "tm1": (-5.9, 12.6), "tb1": (-0.4, 11.4)},
                  G={"tw1": (-6.4, 4.2), "tm1": (-1.2, 10.6)})
CAMS = {
    "A": (((0.10, 1.55, 2.05), (2.25, 5.90, 2.75)), ((0.32, 2.05, 2.12), (2.25, 5.90, 2.80)), 24.0),
    "B": (((1.95, 1.10, 2.85), (2.45, 6.00, 2.50)), ((2.05, 1.45, 2.85), (2.45, 6.00, 2.50)), 24.0),
    "C": (((4.90, -5.30, 3.10), (4.60, 6.00, 3.90)), ((4.75, -4.80, 3.10), (4.60, 6.00, 3.95)), 22.0),
    "D": (((6.15, 3.25, 6.00), (6.00, 5.20, 6.15)), ((6.10, 3.60, 6.05), (6.00, 5.20, 6.18)), 30.0),
    "E": (((3.00, 2.20, 1.80), (1.75, 4.90, 3.00)), ((2.85, 2.40, 1.80), (1.75, 4.90, 3.00)), 24.0),
    "F": (((-0.45, 1.90, 2.25), (-1.20, 8.40, 2.60)), ((-0.70, 2.10, 2.25), (-1.40, 8.40, 2.60)), 22.0),
    "G": (((3.10, 0.60, 2.05), (-3.30, 8.20, 3.00)), ((2.95, 0.80, 2.05), (-3.40, 8.20, 3.05)), 22.0),
}

def framing(g):
    for k, (a, b) in FR.items():
        if a <= g <= b:
            return k
    raise ValueError(g)


def cam_at(g):
    k = framing(g)
    a, b = FR[k]
    (l0, t0), (l1, t1), lens = CAMS[k]
    u = ez((g - a) / float(max(1, b - a)), "sine")
    return Vector(lerp(l0, l1, u)), Vector(lerp(t0, t1, u)), lens


# ----------------------------------------------------------------------------- poses
def insp_pose(g):
    k = framing(g)
    bl = blink(g, [1950, 2004, 2046, 2098, 2124])
    if k == "A":
        u = ez((g - 1950) / 16.0)                       # turns from us to the pan
        return dict(yaw=lerp(0.10, 0.50, u), pitch=lerp(-0.30, 0.20, u), expr="determined", head_roll=lerp(0, -4, u),
                    gaze=(lerp(0.0, 0.7, u), lerp(-0.2, 0.5, u)), lean=lerp(0, 4, u),
                    arm_r=dict(hand=(0.70, 0.55), bend=-0.5, stretch=1.3), prop_r="basket", basket=dict(loaves=12, tilt=lerp(0, 10, u)),
                    arm_l=dict(hand=(0.30, 0.70), bend=-0.5, stretch=1.3, shape="open"), legs="wide", blink=bl, t=g / 30.0)
    if k == "B":
        ut = ez((g - G_POUR[0]) / 6.0)
        n = basket_left(g)
        ph = ((g - G_POUR[0]) / 9.0) % 1.0 if G_POUR[0] + 4 <= g <= G_POUR[1] - 2 else 0.0
        p = dict(yaw=0.55, pitch=0.35, expr="determined", head_roll=-4, lean=6 + 3 * ut, gaze=(0.8, 0.6),
                 arm_r=dict(hand=(lerp(0.80, 1.00, ut), lerp(0.45, 0.22, ut)), bend=-0.4, stretch=1.3), prop_r="basket",
                 basket=dict(loaves=n, tilt=lerp(10, 66, ut), pour=ph if n > 0 else 0.0), legs="wide", blink=bl, t=g / 30.0)
        an = cast6.figure("inspector_royal", dict(p, arm_l="down"), "q")["anchors"]      # the other hand lifts the basket's bottom
        hx, hy = an["basket_base"]
        p["arm_l"] = dict(hand=(hx + 0.02, hy + 0.03), bend=0.5, stretch=1.3, shape="open")
        return p
    if k == "C":
        u = ez((g - 2024) / 10.0)                       # lowers the empty basket, looks up at the beam
        return dict(yaw=lerp(0.55, 0.35, u), pitch=lerp(0.35, -0.55, u), expr="determined", head_roll=lerp(-4, 3, u),
                    gaze=(lerp(0.8, 0.5, u), lerp(0.6, -0.8, u)), lean=lerp(8, -2, u),
                    arm_r=dict(hand=(lerp(1.00, 0.62, u), lerp(0.22, 1.00, u)), bend=-0.3, stretch=1.2), prop_r="basket",
                    basket=dict(loaves=0, tilt=lerp(66, 20, u)), arm_l="akimbo", legs="wide", blink=bl, t=g / 30.0)
    # E: close, low: eyes narrow, glances up at the beam and back down at the pan
    u = ez((g - 2096) / 10.0); v = ez((g - 2114) / 8.0)
    return dict(yaw=0.40, pitch=lerp(-0.45, 0.10, v), expr="angry" if g >= 2102 else "determined", head_roll=lerp(3, -3, u),
                gaze=(lerp(0.4, 0.75, u), lerp(-0.8, 0.5, v)), lean=0,
                arm_r=dict(hand=(0.62, 1.00), bend=-0.3, stretch=1.2), prop_r="basket", basket=dict(loaves=0, tilt=20),
                arm_l="akimbo", legs="wide", blink=bl, t=g / 30.0)


def basket_left(g):
    """loaves still in the basket (the pan shows 12 - this)."""
    a, b = G_POUR[0] + 6, G_POUR[1] - 2                  # 1990 .. 2014: 12 loaves in 24 frames
    if g < a:
        return 12
    return max(0, 12 - int(12 * (g - a) / float(b - a)))


def pan_loaves(g):
    return 0 if g < FR["B"][0] else (12 - basket_left(g))


def path_pt(path, u):
    (x0, y0), (x1, y1) = path
    return (lerp(x0, x1, u), lerp(y0, y1, u))


def drag_u(g):
    k = framing(g)
    a, b = FR[k]
    return (g - a) / float(b - a)


def henry_xy(g):
    return path_pt(HEN_PATH if framing(g) == "F" else HEN_PATH_G, drag_u(g))


def henry_pose(g):
    ph = (g / 20.0) % 1.0
    jerk = 0.5 + 0.5 * math.sin(2 * math.pi * ph)
    return dict(yaw=0.10, pitch=-0.30 + 0.06 * jerk, expr="shocked", pale=1.0, fx=["sweat"], head_roll=6 + 4 * math.sin(g * 0.45),
                lean=-8 - 3 * jerk, squash=(0.98, 1.02),
                arm_r=dict(hand=(0.82, 0.10), bend=-0.5, shape="open", stretch=1.3),
                arm_l=dict(hand=(-0.82, 0.12 - 0.04 * jerk), bend=-0.5, shape="open", stretch=1.3),
                legs=dict(preset="wide", crouch=0.12 + 0.03 * jerk, toe_r=0.6, toe_l=-0.6), blink=blink(g, [2150, 2196]), t=g / 30.0)


def guard_pose(cast, g, lead):
    """lead: guard1 ahead (screen-left), facing henry (screen-right), leaning back hauling; guard2 behind, mirrored, pushing."""
    cyc = cast6.cycle(cast, (g / 24.0 + (0.0 if lead else 0.5)) % 1.0, "walk")
    p = dict(yaw=0.55, pitch=-0.10, expr="angry", lean=-12 if lead else 6, head_roll=-4,
             arm_r=dict(hand=(0.80, 0.30), bend=-0.5, stretch=1.3, shape="open"),
             arm_l=dict(hand=(-0.30, 0.55), bend=0.4), prop_l=dict(type="spear", angle=-70),
             legs=cyc["legs"], head_dy=cyc.get("head_dy", 0.0), blink=blink(g, [2140 + (9 if lead else 0), 2190]), t=g / 30.0)
    if not lead:
        p["mirror"] = True
    return p


def town_pose(cast, g, veg, seed=0):
    u = ez((g - G_RAISE[0] - seed) / float(G_RAISE[1] - G_RAISE[0]), "sine")
    shake = 0.03 * math.sin(g * 0.9 + seed) * u
    hand = (lerp(0.45, 0.66, u), lerp(0.55, -0.74, u) + shake)
    return dict(yaw=0.40, pitch=lerp(0.0, -0.45, u), expr="angry", head_roll=lerp(0, -6, u), lean=lerp(0, -6, u),
                arm_r=dict(hand=hand, bend=-1.0 if u > 0.5 else -0.5, stretch=1.3, layer="top"), prop_r=veg,
                arm_l=dict(hand=(-0.50, 0.40), bend=-0.4, shape="open", stretch=1.2), legs="wide",
                blink=blink(g, [2178 + seed, 2210 - seed]), t=g / 30.0)


# ----------------------------------------------------------------------------- the take
def key_vis(actor, f, visible):
    for ob in actor.objects():
        if ob is None:
            continue
        ob.hide_render = not visible
        ob.keyframe_insert("hide_render", frame=f)
        fc = C._fcurve(ob, "hide_render")
        if fc is not None:
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


class Take(C.Take):
    # who is in which framing; ppd per actor
    CASTING = dict(A=["insp"], B=["insp"], C=["insp", "tm1", "tb1"], D=[], E=["insp"],
                   F=["henry", "guard1", "guard2", "tw1", "tm1", "tb1"], G=["henry", "guard1", "guard2", "woman", "man", "tw1", "tm1"])

    def __init__(self, quality="preview"):
        C.Take.__init__(self, "market", "AFTERNOON", quality=quality, lens=24.0, name="cam_s24")
        sd = os.path.join(TMP, "sprites" + os.environ.get("SPR_TAG", ""))
        mk = lambda n, c: C.make_actor(n, c, sd)
        self.actors["insp"] = mk("insp", "inspector_royal")
        self.actors["henry"] = mk("henry", "henry")
        self.actors["guard1"] = C.make_actor("guard1", "guard1", sd, canvas=(-2.25, -5.5, 2.25, 0.125))
        self.actors["guard2"] = C.make_actor("guard2", "guard2", sd, canvas=(-2.25, -5.0625, 2.25, 0.125))
        self.actors["woman"] = mk("woman", "woman1")
        self.actors["man"] = mk("man", "man1")
        self.actors["tw1"] = mk("tw1", "woman1")
        self.actors["tm1"] = mk("tm1", "man1")
        self.actors["tb1"] = mk("tb1", "baker2")
        self.dial = self.make_dial()

    def make_dial(self):
        """runtime prop (the set module is untouched): a little brass dial plate hung in front of the pivot on an iron bracket from
        the front A-post, with a red centre mark and ticks every 4 deg, and a brass needle hanging from the pivot that turns with the
        beam (parented to big_beam_pivot): -7 reads as 'off the mark, short'.  Small: only the ECU (D) and the inspector close-up
        (E) see it."""
        import bmesh
        cx, cy = B.BIG_SCALE; zp = B.BIG_PIV_Z
        scn = bpy.context.scene

        def mat(name, rgb, rough=0.5, metal=0.0):
            m = bpy.data.materials.new(name); m.use_nodes = True
            b = m.node_tree.nodes.get("Principled BSDF")
            b.inputs["Base Color"].default_value = rgb + (1,); b.inputs["Roughness"].default_value = rough
            b.inputs["Metallic"].default_value = metal
            return m
        brass, ink, red, iron = mat("dial_brass", (0.95, 0.86, 0.62), 0.5), mat("dial_ink", (0.05, 0.03, 0.04)), \
            mat("dial_red", (0.60, 0.04, 0.03)), mat("dial_iron", (0.10, 0.09, 0.11), 0.6)

        def obj(name, faces_fn, m, parent=None):
            me = bpy.data.meshes.new(name + "_me"); bm = bmesh.new(); faces_fn(bm); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new(name, me); ob.data.materials.append(m); scn.collection.objects.link(ob)
            if parent is not None:
                ob.parent = parent; ob.matrix_parent_inverse = parent.matrix_world.inverted()
            return ob

        def P(r, a, y):                                   # angle a from straight down, in the plane y
            return (cx + r * math.sin(a), y, zp - r * math.cos(a))
        R0, R1, Y = 0.26, 0.70, cy - 0.80
        A0, A1 = math.radians(-34), math.radians(34)

        def plate(bm):
            vs = []
            for i in range(25):
                a = lerp(A0, A1, i / 24.0)
                vs.append((bm.verts.new(P(R0, a, Y)), bm.verts.new(P(R1, a, Y))))
            for i in range(24):
                bm.faces.new((vs[i][0], vs[i][1], vs[i + 1][1], vs[i + 1][0]))
        obj("dial_plate", plate, brass)
        for d in range(-32, 33, 4):
            a = math.radians(d); L = 0.26 if d == 0 else 0.12; w = 0.026 if d == 0 else 0.012
            ux, uz = math.sin(a), -math.cos(a); px, pz = math.cos(a), math.sin(a)

            def tick(bm, a=a, L=L, w=w, ux=ux, uz=uz, px=px, pz=pz):
                pts = [(R1 - 0.02 - L, -w), (R1 - 0.02, -w), (R1 - 0.02, w), (R1 - 0.02 - L, w)]
                vv = [bm.verts.new((cx + r * ux + s * px, Y - 0.006, zp + r * uz + s * pz)) for r, s in pts]
                bm.faces.new(vv)
            obj("dial_tick%+d" % d, tick, red if d == 0 else ink)

        def bracket(bm):                                  # iron strap from the dial up to the A-post (y ~ cy-0.38 there)
            for x in (cx - 0.24, cx + 0.24):
                bmesh.ops.create_cube(bm, size=1.0, matrix=__import__("mathutils").Matrix.LocRotScale(
                    Vector((x, cy - 0.60, zp - 0.50)), None, Vector((0.04, 0.44, 0.04))))
        obj("dial_bracket", bracket, iron)
        piv = bpy.data.objects.get("big_beam_pivot")
        bpy.context.view_layer.update()                   # the pivot's matrix_world must be current before parenting

        def needle(bm):
            pts = [(cx - 0.025, zp), (cx + 0.025, zp), (cx + 0.008, zp - 0.66), (cx - 0.008, zp - 0.66)]
            bm.faces.new([bm.verts.new((x, Y - 0.03, z)) for x, z in pts])
        nd = obj("dial_needle", needle, iron, parent=piv)

        def hub(bm):
            bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.07, radius2=0.07, depth=0.06,
                                  matrix=__import__("mathutils").Matrix.LocRotScale(Vector((cx, Y - 0.05, zp)),
                                                                                    __import__("mathutils").Euler((math.pi / 2, 0, 0)), None))
        obj("dial_hub", hub, iron, parent=piv)
        return nd

    def pose(self, shot, gs):
        A = self.actors
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(g)
            self.key_cam(f, loc, look, lens)
            B.set_big_scale(BEAM, frame=f)
            B.set_loaves(pan_loaves(g), frame=f)
            self.key_set(f)
            k = framing(g)
            for n, a in A.items():
                key_vis(a, f, n in self.CASTING[k])
            C.place(A["insp"], f, INSP if k != "E" else INSP)
            hx, hy = henry_xy(g) if k in ("F", "G") else (30.0, 30.0)
            C.place(A["henry"], f, (hx, hy))
            C.place(A["guard1"], f, (hx - 1.25, hy + 0.15))
            C.place(A["guard2"], f, (hx + 1.15, hy - 0.10))
            for n, xy in BYSTANDERS.get(k, {}).items():
                C.place(A[n], f, xy)
            C.place(A["woman"], f, (0.51, 2.21)); C.place(A["man"], f, (1.80, 4.08))
        hen_frames, other = [], []
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            k = framing(g)
            cast = self.CASTING[k]
            if "insp" in cast:
                A["insp"].pose(f, insp_pose(g), camera=self.cam)
            if "henry" in cast:
                A["henry"].pose(f, henry_pose(g), camera=self.cam); hen_frames.append(f)
            if "woman" in cast:
                A["woman"].pose(f, town_pose("woman1", g, "tomato", 0), camera=self.cam)
                A["man"].pose(f, dict(town_pose("man1", g, "cabbage", 3), mirror=True), camera=self.cam)
            if "tw1" in cast:
                gg = g if k == "G" else (2100 if k == "F" else 1900)
                A["tw1"].pose(f, dict(town_pose("woman1", gg, "tomato", 5), yaw=-0.3, mirror=k != "C"), camera=self.cam)
            if "tm1" in cast:
                gg = g if k == "G" else (2195 if k == "F" else 1900)
                A["tm1"].pose(f, dict(town_pose("man1", gg, "cabbage", 2), mirror=True), camera=self.cam)
            if "tb1" in cast:
                A["tb1"].pose(f, dict(yaw=-0.4, pitch=-0.2, expr="worried", arm_r="down", arm_l="down", legs="narrow",
                                      blink=blink(g, [2040, 2160]), t=g / 30.0), camera=self.cam)
        if hen_frames:
            self.sprites_for([(A["henry"], 320)], hen_frames)
            for f in hen_frames:
                self.scene.frame_set(f)
                g = f - 1000 * (shot - 1) - 1
                an = self.anch[("henry", f)]
                wl = actors.local_to_world(A["henry"], an["hand_l"], f, camera=self.cam)
                wr = actors.local_to_world(A["henry"], an["hand_r"], f, camera=self.cam)
                A["guard1"].pose(f, guard_pose("guard1", g, True), hands={"r": {"hand": tuple(wl), "bend": -0.5, "stretch": 1.35, "shape": "open"}}, camera=self.cam)
                A["guard2"].pose(f, guard_pose("guard2", g, False), hands={"r": {"hand": tuple(wr), "bend": -0.5, "stretch": 1.35, "shape": "open"}}, camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        jobs = []
        for n, ppd in (("insp", 448), ("guard1", 320), ("guard2", 320), ("woman", 512), ("man", 512), ("tw1", 192), ("tm1", 192), ("tb1", 192)):
            ff = [f for f in fr if f in A[n].poses]
            if ff:
                for f2, r in zip(ff, A[n].render_sprites(ppd, frames=ff)):
                    self.anch[(n, f2)] = r["anchors"]

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(g)
        v = look - loc
        return dict(shot=shot, g=g, framing=framing(g), cam=[round(c, 3) for c in loc], lens=lens,
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), pan_loaves=pan_loaves(g), beam=BEAM)

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
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
