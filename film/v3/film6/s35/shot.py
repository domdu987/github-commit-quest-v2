#!/usr/bin/env python3
"""shot.py -- film 6 take s35: shot 35 (the ending), market MORNING, g 3069..3193 (6-frame in-handle g 3069..3074, shot g 3075..3193 =
plan 102.50-106.45 s, to the last film frame N-1 = 3193).

    shot 35  Henry's bakery front in the market square on the next morning.  Opens close on the shop: the basket of 13 loaves (the paler
             13th on the very top) on the let-down shutter board, white steam rising off it into the low morning sun, the hanging bread
             sign above; Henry (smiling, hands on his belly) and kit (fists on his hips, beaming) stand in front of their shop.  Kit
             glances up at Henry, Henry ruffles... no -- Henry gives him one more nod; then a long crane pull-back and rise that ends high
             over the square (the whole bakery front, the market waking up), still drifting at the end ("hold to the end").
Mouths: nobody speaks (no quoted line).  Steam cards are local camera-only cards using the set's own steam material (set_steam keys it).
NO depth of field anywhere (client rule): C.Take switches it off at build and before every render.

    python3 shot.py probe 35 a:b[:step]
    python3 shot.py stills 35 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 35 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez = C.lerp, C.clamp, C.blink, C.pulse, C.ez
TMP = os.path.join(HERE, "work")

G0 = C.g_bound(102.50)             # 3075
G_LAST = C.N_FILM - 1              # 3193
H_IN = 6
RANGES = {35: (G0 - H_IN, G_LAST)}


def bf(shot, g):
    return int(g) - 2700           # Blender frame (all takes of this worker map g -> g - 2700)


# ----------------------------------------------------------------------------- staging (market world D; Henry's front faces +x at x -22)
BOARD_Z = 1.25                     # shutter board top
BASKET = Vector((-21.40, 1.75, BOARD_Z))
BASKET_SCALE = 1.7
HENRY = (-20.45, 3.75)
KIT = (-20.45, -0.05)
STEAM = 1.5
# camera: close on the basket + sign -> long crane pull-back and rise
CAM_KEYS = [  # (g, loc, look, lens)
    (G0 - H_IN, (-15.9, -2.3, 2.45), (-21.0, 2.20, 2.38), 28.0),
    (G0 + 34, (-15.6, -2.7, 2.65), (-21.0, 2.20, 2.43), 28.0),
    (G_LAST - 10, (-5.9, 0.9, 4.45), (-20.4, 1.5, 3.25), 24.0),
    (G_LAST, (-5.6, 0.92, 4.5), (-20.4, 1.5, 3.28), 24.0),
]


def cam_at(g):
    ks = CAM_KEYS
    if g <= ks[0][0]:
        k = ks[0]; return Vector(k[1]), Vector(k[2]), k[3]
    for a, b in zip(ks[:-1], ks[1:]):
        if a[0] <= g <= b[0]:
            u = (g - a[0]) / float(b[0] - a[0])
            if a is ks[1]:
                u = ez(u, "sine")            # the big pull-back: ease in and out
            loc = Vector(lerp(a[1], b[1], u)); look = Vector(lerp(a[2], b[2], u)); lens = lerp(a[3], b[3], u)
            return loc, look, lens
    k = ks[-1]; return Vector(k[1]), Vector(k[2]), k[3]


# ----------------------------------------------------------------------------- poses
def henry_pose(g):
    nod = pulse(g, G0 + 8, G0 + 15, G0 + 26, 1.0)
    return dict(yaw=-0.35, pitch=0.15 + 0.40 * nod, expr="happy", head_roll=-5 + 2 * math.sin(g * 0.07), lean=-3,
                gaze=(-0.6, 0.4 * nod), arm_r=dict(hand=(0.36, 1.10), bend=0.9), arm_l=dict(hand=(-0.40, 1.06), bend=0.9),
                legs="wide", blink=blink(g, [3082, 3140, 3180]), t=g / 30.0)


def kit_pose(g):
    up = ez((g - (G0 + 2)) / 8.0) * (1 - ez((g - (G0 + 30)) / 8.0))     # glances up at henry, then back to us
    hop = pulse(g, G0 + 40, G0 + 45, G0 + 52, 1.0)
    return dict(yaw=0.20 + 0.25 * up, pitch=-0.35 - 0.10 * up, expr="grinning", head_roll=-5 + 3 * math.sin(g * 0.11),
                gaze=(0.1 + 0.8 * up, -0.2 - 0.4 * up), arm_l="akimbo", arm_r="akimbo", legs="wide",
                squash=(1 + 0.04 * hop, 1 - 0.04 * hop), blink=blink(g, [3072, 3120, 3165]), t=g / 30.0)


# ----------------------------------------------------------------------------- local steam cards (the set's steam material)
def steam_card(name, base, hw, h, mat, v0):
    me = bpy.data.meshes.new(name)
    me.from_pydata([(-hw, 0, 0), (hw, 0, 0), (hw, 0, h), (-hw, 0, h)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for i, (u, v) in enumerate([(0, v0), (1, v0), (1, v0 + 0.75), (0, v0 + 0.75)]):
        uv.data[i].uv = (u, v)
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(base)
    ob.visible_shadow = False
    ob.visible_diffuse = False
    ob.visible_glossy = False
    return ob


def pale_basket_svg(uid, loaves=13):
    """cast6.basket_svg with the 13th loaf (the first loaf drawn: the single loaf on top) in a paler bake."""
    svg, an = cast6.basket_svg(uid, loaves=loaves)
    if loaves >= 13:
        pale = ('<radialGradient id="%s_pl" cx="0.36" cy="0.30" r="0.80"><stop offset="0" stop-color="#fff3d8"/>'
                '<stop offset="0.45" stop-color="#f3d9a6"/><stop offset="1" stop-color="#cfa46c"/></radialGradient>' % uid)
        svg = svg.replace("</defs>", pale + "</defs>", 1)
        svg = svg.replace('fill="url(#%s_lf)"' % uid, 'fill="url(#%s_pl)"' % uid, 1)
    return svg, an


CANVAS_KIT = (-1.5625, -3.875, 1.5625, 0.1875)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "market", "MORNING", quality=quality, lens=30.0, name="cam_s35")
        sd = os.path.join(TMP, "sprites")
        self.actors["kit"] = C.make_actor("kit", "kit", sd, CANVAS_KIT)
        self.actors["henry"] = C.make_actor("henry", "henry", sd)
        svg, an = pale_basket_svg("b35", 13)
        box = (-0.56, -0.06, 0.56, 0.72)
        pngs = C.svg_pngs([(svg, box, 512)], os.path.join(TMP, "props"))
        self.basket = C.PropCard("basket", pngs, box, scale=BASKET_SCALE, shadow=True)
        loc, look, lens = cam_at(G0)
        self.basket.put(BASKET + Vector((0, 0, 0.66 * BASKET_SCALE)), face=loc)
        M = B.STATE["M"]
        self.steam = []
        top = BASKET + Vector((0, 0, 0.66 * BASKET_SCALE - 0.22))       # just above the pile (basket card origin = handle top)
        for k, (dx, dy, hw, h, v0) in enumerate(((-0.10, 0.0, 0.42, 2.6, 0.1), (0.15, 0.25, 0.36, 2.2, 0.55), (0.05, -0.25, 0.30, 1.9, 0.8))):
            ob = steam_card("s35_steam%d" % k, top + Vector((0.0 + 0.1 * k, dx + dy, -0.15)), hw, h, M["steam" if k % 2 == 0 else "steam2"], v0)
            self.steam.append(ob)
        self.face_steam(loc)

    def face_steam(self, camloc, frame=None):
        for ob in self.steam:
            d = Vector(camloc) - ob.location
            ob.rotation_euler = (0.0, 0.0, math.atan2(d.x, -d.y))
            if frame is not None:
                ob.keyframe_insert("rotation_euler", frame=frame)
        if frame is not None:
            self.basket.put(BASKET + Vector((0, 0, 0.66 * BASKET_SCALE)), face=camloc, frame=frame)

    def pose(self, shot, gs):
        kit, henry = self.actors["kit"], self.actors["henry"]
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(g)
            self.key_cam(f, loc, look, lens=lens)
            C.place(kit, f, KIT, 0.0)
            C.place(henry, f, HENRY, 0.0)
            B.set_steam(STEAM, frame=f)
            B.set_oven(1.0, frame=f)
            self.face_steam(loc, frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            kit.pose(f, kit_pose(g), camera=self.cam)
            henry.pose(f, henry_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(kit, 256), (henry, 256)], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=round(lens, 2), heads=C.head_report(self, f),
                    basket_px=[round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(self.basket.to_world((0, 0.3))), f)[:2]])

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def main():
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
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


if __name__ == "__main__":
    main()
