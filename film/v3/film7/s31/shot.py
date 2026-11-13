#!/usr/bin/env python3
"""shot.py -- film 7 take s31: shot 31 (103.20 s .. the end, g 3096..3218) + a 6-frame in-handle (g 3090..3095), rendered in 3D.
No out-handle: g 3218 is the last frame of the film (N = 3219).
Plan: louvre / wall_eye, final: slow push to the Mona Lisa behind glass; for a moment a faint reflection of a small man in a cap
appears on the glass; hold to the end.  Narration: "...ยิ้มอยู่หลัง กระจก เหมือนวันที่ ไอ้มักกะโรนี ติดกระจกให้ เธอครั้งแรก" (ends 106.70 s).

    one set-up, g 3090..3218: the reopening-day gallery (her back on the wall, rope + queue lanes up), the camera pushing
    slowly from the rope (y 16.3) to 1.9 D from her glass, drifting a
    little up and left; ease-out but never still (an 18 % linear component keeps the last second moving).
    THE REFLECTION: vincenzo (normal clothes, flat cap) as a faint cool ghost on her glass, over the lower right of the canvas: fades in
    on "ไอ้มักกะโรนี" (104.38 s = g 3134 .. g 3146), a small proud smile + blink, gone by g 3192 ("เธอครั้งแรก" 106.01 s = g 3183).
    It is an actor card a hair in front of the glass whose material multiplies the sprite alpha by a keyed opacity (peak 0.34), tints
    it toward the glass's cool sheen and masks it to the glass rectangle (world x/z box), so it never shows on the gilt frame.
Mouths: nobody speaks.  NO depth of field anywhere (C.Take).

Blender frame of g = g - 3000 + 1.
    python3 shot.py probe 1 a:b[:step]
    python3 shot.py stills 1 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7, sprites = C.L, C.actors, C.camrig, C.cast7, C.sprites
lerp, clamp, blink, ez = C.lerp, C.clamp, C.blink, C.ez
TMP = os.path.join(HERE, "work")

G0 = C.g_bound(103.20)                                    # 3096
G_LAST = C.N_FILM - 1                                     # 3218
H = 6
RANGES = {1: (G0 - H, G_LAST)}
G_REFL = (C.g_of(104.38), C.g_of(104.38) + 12, 3176, 3192)  # fade in 3134..3146, hold, fade out 3176..3192
REFL_PEAK = 0.34
LENS = 24.0
CAM0 = ((0.42, 16.3, 3.55), (0.02, 21.8, 3.70))
CAM1 = ((0.06, 19.75, 3.80), (0.00, 21.8, 3.80))


def bf(shot, g):
    return g - 3000 + 1


def cam_of(shot, g):
    a, b = RANGES[1]
    v = (g - a) / float(b - a)
    u = 0.82 * ez(v, "sine") + 0.18 * v
    return Vector(lerp(CAM0[0], CAM1[0], u)), Vector(lerp(CAM0[1], CAM1[1], u))


def refl_k(g):
    a, b, c, d = G_REFL
    if g <= a or g >= d:
        return 0.0
    if g < b:
        return REFL_PEAK * ez((g - a) / float(b - a))
    if g > c:
        return REFL_PEAK * (1.0 - ez((g - c) / float(d - c)))
    return REFL_PEAK


VISITORS_DRAFT = [("v_lady", "lady", (-1.85, 20.05), False, "crowd_stare"), ("v_gent", "gentleman", (1.95, 19.75), True, "crowd_stare_gentleman")]
VISITORS = []      # draft 1 had two visitors at the rope at the frame edges: their heads sat on / below y 880 -> left out


def ghost_material(actor, glass_y, box):
    """card material -> alpha * keyed opacity (node 'refl_k') * world box mask (the glass rectangle); colour tinted cool."""
    m = actor.material; nt = m.node_tree; Lk = nt.links.new
    mix = next(n for n in nt.nodes if n.bl_idname == "ShaderNodeMixShader")
    emi = next(n for n in nt.nodes if n.bl_idname == "ShaderNodeEmission")
    tex = actor.tex
    fac_src = mix.inputs["Fac"].links[0].from_socket
    kv = nt.nodes.new("ShaderNodeValue"); kv.name = "refl_k"; kv.outputs[0].default_value = 0.0
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
    Lk(fac_src, mul.inputs[0]); Lk(kv.outputs[0], mul.inputs[1])
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); Lk(geo.outputs["Position"], sep.inputs[0])
    x0, x1, z0, z1 = box
    cur = mul.outputs[0]
    for comp, lo, hi in (("X", x0, x1), ("Z", z0, z1)):
        for op, val in (("GREATER_THAN", lo), ("LESS_THAN", hi)):
            c = nt.nodes.new("ShaderNodeMath"); c.operation = op; Lk(sep.outputs[comp], c.inputs[0]); c.inputs[1].default_value = val
            mm = nt.nodes.new("ShaderNodeMath"); mm.operation = "MULTIPLY"; Lk(cur, mm.inputs[0]); Lk(c.outputs[0], mm.inputs[1]); cur = mm.outputs[0]
    Lk(cur, mix.inputs["Fac"])
    tint = nt.nodes.new("ShaderNodeMix"); tint.data_type = "RGBA"; tint.blend_type = "MIX"
    tint.inputs["Factor"].default_value = 0.35
    Lk(tex.outputs["Color"], tint.inputs["A"]); tint.inputs["B"].default_value = (0.78, 0.86, 1.0, 1.0)
    Lk(tint.outputs["Result"], emi.inputs["Color"])
    emi.inputs["Strength"].default_value = 1.15
    return kv


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "louvre", "wall_eye", quality=quality, lens=LENS, name="cam_s31")
        sd = os.path.join(TMP, "sprites")
        bpy.context.view_layer.update()
        gl = bpy.data.objects["mona_glass"]
        ws = [gl.matrix_world @ Vector(c) for c in gl.bound_box]
        self.glass_y = min(w.y for w in ws)
        self.glass_box = (min(w.x for w in ws), max(w.x for w in ws), min(w.z for w in ws), max(w.z for w in ws))
        print("s31: glass y %.3f box %s" % (self.glass_y, [round(v, 3) for v in self.glass_box]), flush=True)
        for nm, cast, p, mir, story in VISITORS:
            a = C.make_actor(nm, cast, sd)
            self.actors[nm] = a
        r = actors.Actor("refl", "vincenzo")
        r.build(sprites.DEFAULT_CANVAS["vincenzo"], sd, shadow=None, contact=None)
        r.head_flip = False
        L.no_bounce(r.card)
        r.card.visible_glossy = False
        self.refl = r
        self.actors["refl"] = r
        self.refl_k = ghost_material(r, self.glass_y, self.glass_box)
        # the reflection stands a hair in front of the glass, small (a man ~1.5 D behind the lens seen in the glass), head over
        # the lower right of the canvas
        self.refl_scale = 0.40
        self.refl_feet = Vector((0.26, self.glass_y - 0.012, 3.42 - 2.62 * self.refl_scale))

    def refl_pose(self, g):
        p = dict(cast7.STORY7["vincenzo_stand"][1])
        u = ez((g - G_REFL[0]) / 30.0)
        p.update(mirror=True, yaw=0.18, expr="happy" if g >= 3150 else "neutral", gaze=(lerp(0.3, 0.05, u), -0.15),
                 pitch=-0.08, head_roll=lerp(-2.0, 4.0, u))
        p["blink"] = blink(g, [3160])
        p["t"] = g / 30.0
        return p

    def visitor_pose(self, i, g):
        nm, cast, p, mir, story = VISITORS[i]
        q = dict(cast7.STORY7[story][1])
        q.update(mirror=mir, yaw=0.45, gaze=(0.7, -0.5), pitch=-0.2, head_roll=(-4 if i else 5) + 1.5 * math.sin(g * 0.11 + i),
                 expr="happy" if i == 0 else "stunned")
        q["blink"] = blink(g, [3101 + 9 * i, 3150 + 7 * i])
        q["t"] = g / 30.0
        return q

    def pose(self, shot, gs):
        for g in gs:
            f = bf(1, g)
            loc, look = cam_of(1, g)
            self.key_cam(f, loc, look)
            self.key_set(f, mona=True, queue=True)
            for nm, cast, p, mir, story in VISITORS:
                C.place(self.actors[nm], f, p, 0.0)
            C.place(self.refl, f, (self.refl_feet.x, self.refl_feet.y), self.refl_feet.z, scale=self.refl_scale)
            k = refl_k(g)
            self.refl_k.outputs[0].default_value = k
            self.refl_k.outputs[0].keyframe_insert("default_value", frame=f)
            self.refl.card.hide_render = k <= 0.0
            self.refl.card.keyframe_insert("hide_render", frame=f)
        for g in gs:
            f = bf(1, g)
            self.scene.frame_set(f)
            for i, (nm, cast, p, mir, story) in enumerate(VISITORS):
                self.actors[nm].pose(f, self.visitor_pose(i, g), camera=self.cam)
            self.refl.pose(f, self.refl_pose(g), camera=self.cam)
        fr = [bf(1, g) for g in gs]
        self.sprites_for([(self.actors[v[0]], 224) for v in VISITORS] + [(self.refl, 256)], fr)

    def report(self, shot, g):
        f = bf(1, g)
        loc, look = cam_of(1, g)
        heads = C.head_report(self, f)
        self.scene.frame_set(f)
        # her face (canvas centre + 0.38 D) in screen px
        from bpy_extras.object_utils import world_to_camera_view
        sc = self.scene
        fc = world_to_camera_view(sc, self.cam, Vector((0.0, self.glass_y, 3.55 + 0.38)))
        return dict(shot=31, g=g, cam=[round(c, 3) for c in loc], refl=round(refl_k(g), 3),
                    mona_face=(round(fc.x * 720, 1), round((1 - fc.y) * 1280, 1)), heads=heads)

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(1, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills"):
        Tk = Take("preview", 1)
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[1][0] <= g <= RANGES[1][1]]
        Tk.pose(1, gs)
        for g in gs:
            print(json.dumps(Tk.report(1, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                st = Tk.render(1, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q, 1), [1], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
