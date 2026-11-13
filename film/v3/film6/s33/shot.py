#!/usr/bin/env python3
"""shot.py -- film 6 take s33: shot 33 ("aha"), market AFTERNOON, g 2830..2970 (6-frame handles: shot g 2836..2964 = plan 94.54-98.83 s).

    shot 33  The earlier bakers, still locked in the pillory, three in a row on the platform (the neighbour baker2 and two more bakers),
             sad and drooping; a basket of their own bread stands in front of each on the platform boards, white steam drifting off it
             into the low afternoon sun -- they never cheated, the weight just floated away.  Three framings (a framing change every
             ~1.5 s):
               A  g 2830..2878  low, frontal: the three heads in a row behind the steaming baskets, slow push    "ร้านพวกนั้น ไม่ได้โกงเลย"
               B  g 2879..2922  punch-in: the middle baker over his steaming basket; slow tilt up with the steam  "ขนมปังของพวกเขา"
               C  g 2923..2970  from the right, low: the steam rises past the bakers' sad faces into the sky,    "แค่ลอยหายไปในอากาศ ทีละนิด"
                                tilt up (dissolve out to shot 34)
Mouths: nobody speaks (no quoted line): the static mouth of each expression.
The set's 3D pillory board + post (one neck hole) is cut out of the 'pillory' mesh at runtime (platform, rails, lanterns and splats stay);
each baker is a cast6 'pillory' pose card (the drawn board + post of each one).  baker3 / baker4 are recoloured copies of cast6 baker2
registered at runtime (cast6 is not edited).  Steam: local camera-only cards with the set's steam material (B.set_steam keys it).
NO depth of field anywhere (client rule).

    python3 shot.py probe 33 a:b[:step] | stills 33 a:b[:step] <out_dir> [scale] [samples] | final 33 a:b[:step] [scale] [samples]
"""
import math, os, sys, json, copy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import bpy, bmesh                                        # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6, sprites = C.B, C.actors, C.camrig, C.cast6, C.sprites
lerp, clamp, blink, pulse, ez = C.lerp, C.clamp, C.blink, C.pulse, C.ez
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(94.54), C.g_bound(98.83)        # 2836, 2965
H = 6
RANGES = {33: (G0 - H, G1 + H - 1)}                 # 2830..2970
CUT_B, CUT_C = 2879, 2923


def bf(shot, g):
    return int(g) - 2700


# ----------------------------------------------------------------------------- extra bakers (recoloured baker2)
def register_bakers():
    P, CE = cast6.P, cast6.CE
    base = P.CAST["baker2"]
    v3 = copy.deepcopy(base)
    v3.update(seed=82.5, pencil_moustache=False, moustache=True, hair=dict(color="#a8582a", front=0.07, grow=0.20))
    v3["hat_colors"] = dict(light="#d8b890", base="#b08a5e", dark="#7a5a3a", shine="#f0dcc0", cuff="#c49c6c", stitch="#7a5a3a")
    v3["sleeve"] = dict(base["sleeve"], color="#5e6f8a", dark="#3e4a62", cuff="#6e80a0")
    v3["colors"] = dict(base["colors"], base="#5e6f8a", dark="#3e4a62")
    v4 = copy.deepcopy(base)
    v4.update(seed=83.5, torso_w=0.66, hair=dict(color="#9a948c", front=0.07, grow=0.20))
    v4["hat"] = "none"
    v4["sleeve"] = dict(base["sleeve"], color="#8a6a4a", dark="#5e4630", cuff="#9a7a58")
    v4["colors"] = dict(base["colors"], base="#8a6a4a", dark="#5e4630")
    for n, c in (("baker3", v3), ("baker4", v4)):
        P.CAST[n] = c
        CE.CANVAS[n] = CE.CANVAS["baker2"]
        sprites.DEFAULT_CANVAS[n] = sprites.DEFAULT_CANVAS["baker2"]


# ----------------------------------------------------------------------------- staging (market world D; pillory platform top z 1.0 at (-4, 9.5))
PZ = 1.0
BAKERS = [  # name, cast, feet (x, y), basket (x, y)
    ("bk_l", "baker3", (-5.55, 9.55), (-5.35, 8.55)),
    ("bk_m", "baker2", (-4.00, 9.80), (-3.95, 8.70)),
    ("bk_r", "baker4", (-2.45, 9.55), (-2.65, 8.55)),
]
BASKET_SCALE = 1.25
STEAM = 1.5
CANVAS_B = (-1.6875, -4.5625, 1.6875, 0.1250)

CAMS = {  # framing: [(g, loc, look, lens), ...] linear between keys (sine-eased)
    "A": [(RANGES[33][0], (-4.05, 4.70, 1.85), (-4.0, 9.6, 3.05), 24.0), (CUT_B - 1, (-4.05, 5.35, 1.95), (-4.0, 9.6, 3.10), 24.0)],
    "B": [(CUT_B, (-3.75, 6.75, 1.75), (-3.98, 9.4, 3.15), 30.0), (CUT_C - 1, (-3.75, 6.95, 1.80), (-3.98, 9.4, 3.60), 30.0)],
    "C": [(CUT_C, (0.40, 7.40, 1.60), (-4.0, 9.4, 3.85), 26.0), (RANGES[33][1], (0.30, 7.55, 1.60), (-4.0, 9.4, 4.12), 26.0)],
}


def framing(g):
    return "A" if g < CUT_B else ("B" if g < CUT_C else "C")


def cam_at(g):
    ks = CAMS[framing(g)]
    a, b = ks[0], ks[-1]
    u = ez((g - a[0]) / float(b[0] - a[0]), "sine")
    return Vector(lerp(a[1], b[1], u)), Vector(lerp(a[2], b[2], u)), lerp(a[3], b[3], u)


# ----------------------------------------------------------------------------- poses
WRIST = cast6.PILLORY_WRIST_Y


def baker_pose(i, g):
    """sad, drooping in the pillory; slow 'no' shakes (we weighed exactly), sighs; in C they look up after the steam."""
    ph = [0.0, 1.7, 3.3][i]
    shake = math.sin(g * 0.16 + ph) * (0.18 if (g // 40 + i) % 2 == 0 else 0.05)
    up = ez((g - (CUT_C + 6 + 4 * i)) / 14.0) if g >= CUT_C else 0.0
    sigh = pulse(g, 2850 + 17 * i, 2858 + 17 * i, 2872 + 17 * i, 1.0)
    p = dict(yaw=[0.10, 0.0, -0.10][i] + shake, pitch=0.35 + 0.15 * sigh - 0.55 * up, expr=["sad", "sad", "worried"][i],
             head_roll=[-7, 5, 8][i] + 3 * math.sin(g * 0.05 + ph), gaze=(0.0, 0.6 - 1.2 * up),
             arm_r=dict(hand=(0.56, WRIST), bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.56, WRIST), bend=-0.6, stretch=1.3),
             legs="narrow", pillory=True, squash=(1 + 0.02 * sigh, 1 - 0.02 * sigh),
             blink=blink(g, [[2838, 2890, 2935], [2846, 2905, 2950], [2832, 2868, 2925]][i]), t=g / 30.0)
    if i == 1:
        p["fx"] = ["tears"] if g >= CUT_B else []
    return p


# ----------------------------------------------------------------------------- helpers
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


def cut_pillory_board():
    """delete the 3D board, post, hole rims, padlock and sign of the set's pillory (the bakers carry their own drawn boards)."""
    ob = bpy.data.objects.get("pillory")
    cx, cy = -4.0, 9.5
    bm = bmesh.new(); bm.from_mesh(ob.data)
    mw = ob.matrix_world
    kill = [v for v in bm.verts if (lambda p: p.z > PZ + 0.06 and abs(p.x - cx) < 1.85 and cy - 0.3 < p.y < cy + 0.55)(mw @ v.co)]
    bmesh.ops.delete(bm, geom=kill, context="VERTS")
    bm.to_mesh(ob.data); bm.free(); ob.data.update()
    return len(kill)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "market", "AFTERNOON", quality=quality, lens=26.0, name="cam_s33")
        register_bakers()
        n = cut_pillory_board()
        print("s33: cut %d pillory verts" % n, flush=True)
        sd = os.path.join(TMP, "sprites")
        for (nm, cast, feet, bx) in BAKERS:
            self.actors[nm] = C.make_actor(nm, cast, sd, CANVAS_B)
        box = (-0.56, -0.06, 0.56, 0.72)
        items = [(cast6.basket_svg("b33_%d" % k, loaves=[10, 12, 11][k])[0], box, 384) for k in range(3)]
        pngs = C.svg_pngs(items, os.path.join(TMP, "props"))
        M = B.STATE["M"]
        self.baskets, self.steam = [], []
        for k, (nm, cast, feet, bx) in enumerate(BAKERS):
            pc = C.PropCard("basket%d" % k, [pngs[k]], box, scale=BASKET_SCALE, shadow=True)
            self.baskets.append(pc)
            top = Vector((bx[0], bx[1], PZ + 0.66 * BASKET_SCALE - 0.30))
            for j, (dx, hw, h, v0) in enumerate(((-0.08, 0.38, 2.9, 0.15 + 0.3 * k), (0.12, 0.30, 2.4, 0.6 + 0.2 * k), (0.02, 0.45, 3.4, 0.4 + 0.25 * k))):
                self.steam.append(steam_card("s33_steam%d%d" % (k, j), top + Vector((dx, -0.05 * j, 0)), hw, h,
                                             M["steam" if (j + k) % 2 == 0 else "steam2"], v0))

    def face(self, camloc, f):
        for ob in self.steam:
            d = Vector(camloc) - ob.location
            ob.rotation_euler = (0.0, 0.0, math.atan2(d.x, -d.y))
            ob.keyframe_insert("rotation_euler", frame=f)
        for k, pc in enumerate(self.baskets):
            bx = BAKERS[k][3]
            pc.put(Vector((bx[0], bx[1], PZ + 0.66 * BASKET_SCALE)), face=camloc, frame=f)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(g)
            self.key_cam(f, loc, look, lens=lens)
            for (nm, cast, feet, bx) in BAKERS:
                C.place(self.actors[nm], f, feet, PZ)
            B.set_steam(STEAM, frame=f)
            B.set_oven(1.0, frame=f)
            self.face(loc, f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for i, (nm, cast, feet, bx) in enumerate(BAKERS):
                self.actors[nm].pose(f, baker_pose(i, g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(self.actors[nm], 320) for (nm, c, ft, bx) in BAKERS], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(g)
        return dict(shot=shot, g=g, framing=framing(g), cam=[round(c, 3) for c in loc], lens=round(lens, 2), heads=C.head_report(self, f))

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
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)


if __name__ == "__main__":
    main()
