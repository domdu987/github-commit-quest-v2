#!/usr/bin/env python3
"""shot.py -- film 6b take s22: shots 22-25 (plan 41.27-48.60 s = g 1238..1457) + 6 handle frames each side (g 1232..1463).

    shot 22  g 1232..1310  bakery AFTERNOON.  (A) g ..1286: CU kit alone in the empty shop, hand on the chin, thinking (worried ->
                           determined on "ว่าลุงไม่ได้โกง" g 1259), the street and blue sky behind through the counter opening, slow push.
                           (B) g 1287..1310 punch-in on "ขนมปังก้อนเดิม": kit holds up the morning loaf right in front of the lens
                           and squints at it, push.
    shot 23  g 1311..1343  bakery MORNING (dawn, cool).  ECU of the hand balance: the loaf settles on the pan, the beam wobbles to
                           dead level; parchment tag "500 ก." on the pan; a little white steam off the warm loaf.  Push in.
    shot 24  g 1344..1387  bakery AFTERNOON (gold), the same framing (match cut): no steam; on "ตกบ่ายเหลือ" the loaf pan RISES
                           (beam -8, g 1348..1364, overshoot) and the tag flips to a red "480 ก." on "สี่ร้อย" (g 1361..1367).
    shot 25  g 1388..1463  bakery MORNING.  ECU of the fresh loaves on the cooling table with BIG white steam billowing up
                           ("ควันขาว ๆ"); (A) low push g ..1427, (B) g 1428.. crane up into the white cloud.
Mouths: nobody speaks (no quote in 22-25).  NO depth of field (C.Take switches it off at build and before every render).
Internal shot ids 22..25; Blender frame of film frame g = g + 1 (each shot builds its own scene).

    python3 shot.py stills <shot> a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final <shot> a:b[:step] [scale] [samples]
"""
import math, os, sys, json, base64

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
sys.path.insert(0, os.path.join(V3, "film6"))
import common as C                                       # noqa: E402  (paths, cast6 first, bpy, bakery, stage)
import bpy                                               # noqa: E402
import numpy as np                                       # noqa: E402
from PIL import Image                                    # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez = C.lerp, C.clamp, C.blink, C.pulse, C.ez
TMP = os.path.join(HERE, "work")
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")


def g_of(t):
    return int(round((t + 0.10) * 30))


def g_bound(t):
    return int(round(t * 30))


# ----------------------------------------------------------------------------- timing (film 6b clock)
H = 6
G0, G1 = g_bound(41.27), g_bound(48.60)            # 1238, 1458
S23, S24, S25 = g_bound(43.70), g_bound(44.80), g_bound(46.27)    # 1311, 1344, 1388
RANGES = {22: (G0 - H, S23 - 1), 23: (S23, S24 - 1), 24: (S24, S25 - 1), 25: (S25, G1 + H - 1)}
PRESET = {22: "AFTERNOON", 23: "MORNING", 24: "AFTERNOON", 25: "MORNING"}
G_NOTCHEAT = g_of(41.85)       # 1259 "ว่าลุงไม่ได้โกง"
G_LOAF = g_of(42.80)           # 1287 "ขนมปังก้อนเดิม" -> punch-in on the loaf
G_FALL = g_of(44.75)           # 1346 "ตกบ่ายเหลือ"
G_480 = g_of(45.39)            # 1365 "สี่ร้อย"
G_EVERY = g_of(47.49)          # 1428 "ขนมปังทุก" -> crane up


def bf(g):
    return int(g) + 1


# ----------------------------------------------------------------------------- set geometry (bakery world D)
SS = Vector((2.4, 0.75, 1.25))            # small balance foot; pivot z 2.2, arm 0.5, loaf pan at x 1.9, pan top ~z 1.63
PAN = Vector((1.9, 0.75, 1.63))
KIT = (0.55, 2.55)

# ----------------------------------------------------------------------------- 2D pieces: tags, puffs
def tag_svg(text, ink, fill="#f4e4bc"):
    f = base64.b64encode(open(FONT, "rb").read()).decode()
    return ('<style>@font-face{font-family:Kn;src:url(data:font/ttf;base64,%s)}</style>'
            '<path d="M-0.30,-0.15 L0.30,-0.15 L0.34,-0.11 L0.34,0.11 L0.30,0.15 L-0.30,0.15 L-0.34,0.11 L-0.34,-0.11 Z" '
            'fill="%s" stroke="#3a2832" stroke-width="0.022" stroke-linejoin="round"/>'
            '<circle cx="-0.27" cy="0" r="0.028" fill="#3a2832"/>'
            '<path d="M-0.30,0.13 L0.30,0.13" stroke="#d9c393" stroke-width="0.02"/>'
            '<text x="0.035" y="0.072" font-family="Kn" font-size="0.205" text-anchor="middle" fill="%s" '
            'stroke="#3a2832" stroke-width="0.008" paint-order="stroke">%s</text>' % (f, fill, ink, text))


TAG_BOX = (-0.37, -0.18, 0.37, 0.18)


def puff_png(path, seed, n=256):
    """a soft white cloud puff (RGBA), lumpy, cached."""
    if os.path.exists(path):
        return path
    rng = np.random.RandomState(seed)
    y, x = np.mgrid[0:n, 0:n] / float(n) - 0.5
    a = np.zeros((n, n))
    for k in range(7):
        cx, cy = rng.uniform(-0.17, 0.17), rng.uniform(-0.12, 0.17)
        r = rng.uniform(0.10, 0.19)
        a = np.maximum(a, np.clip(1.25 - ((x - cx) ** 2 + (y - cy) ** 2) / r ** 2, 0, 1))
    # soft noise breakup
    nz = np.zeros((n, n))
    for s, w in ((8, 0.5), (16, 0.3), (32, 0.2)):
        g = rng.rand(s, s)
        nz += w * np.array(Image.fromarray((g * 255).astype(np.uint8)).resize((n, n), Image.BICUBIC)) / 255.0
    a = np.clip(a * (0.75 + 0.5 * nz) - 0.1, 0, 1)
    a = np.array(Image.fromarray((a * 255).astype(np.uint8)).resize((n, n), Image.BICUBIC)) / 255.0
    a = a ** 1.2 * 0.92
    shade = 0.94 + 0.06 * np.clip(0.5 - y * 1.6, 0, 1)        # slightly darker underside
    rgb = np.stack([shade * 0.97, shade * 0.98, shade], -1)
    img = np.concatenate([rgb, a[..., None]], -1)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray((img * 255).astype(np.uint8), "RGBA").save(path)
    return path


class Puffs(object):
    """billboard white steam puffs (emission cards facing the camera) rising from source points; per-frame keys of location, scale and
    object colour alpha (opacity).  sources: [(world point, radius D)], life frames, rise D over the life, grow factor."""

    def __init__(self, name, cam, sources, n_per, life, rise, size, grow=2.4, drift=0.25, strength=1.0, seed=1, alpha=0.8):
        self.obs, self.par = [], []
        rng = np.random.RandomState(seed)
        mats = []
        for k in range(4):
            img = bpy.data.images.load(puff_png(os.path.join(TMP, "props", "puff_%d.png" % k), 100 + k), check_existing=True)
            img.alpha_mode = "STRAIGHT"
            m = bpy.data.materials.new("%s_m%d" % (name, k))
            m.use_nodes = True
            nt = m.node_tree; nt.nodes.clear()
            out = nt.nodes.new("ShaderNodeOutputMaterial")
            tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = img; tx.interpolation = "Cubic"
            oi = nt.nodes.new("ShaderNodeObjectInfo")
            em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = strength
            tr = nt.nodes.new("ShaderNodeBsdfTransparent")
            mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.use_clamp = True
            mc = nt.nodes.new("ShaderNodeMixRGB"); mc.blend_type = "MULTIPLY"; mc.inputs[0].default_value = 1.0
            mix = nt.nodes.new("ShaderNodeMixShader")
            nt.links.new(tx.outputs["Color"], mc.inputs[1]); nt.links.new(oi.outputs["Color"], mc.inputs[2])
            nt.links.new(mc.outputs[0], em.inputs["Color"])
            nt.links.new(tx.outputs["Alpha"], mul.inputs[0]); nt.links.new(oi.outputs["Alpha"], mul.inputs[1])
            nt.links.new(mul.outputs[0], mix.inputs[0]); nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
            nt.links.new(mix.outputs[0], out.inputs["Surface"])
            try:
                m.surface_render_method = "BLENDED"
            except Exception:
                pass
            mats.append(m)
        me = actors._quad(name + "_quad", -0.5, -0.5, 0.5, 0.5)
        i = 0
        for (pt, rad) in sources:
            for j in range(n_per):
                ob = bpy.data.objects.new("%s_%d" % (name, i), me.copy())
                ob.data.materials.append(mats[i % 4])
                bpy.context.scene.collection.objects.link(ob)
                ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
                c = ob.constraints.new("TRACK_TO"); c.target = cam; c.track_axis = "TRACK_NEGATIVE_Y"; c.up_axis = "UP_Z"
                ang = rng.uniform(0, 2 * math.pi); rr = rad * math.sqrt(rng.uniform(0, 1))
                self.obs.append(ob)
                self.par.append(dict(p=Vector(pt) + Vector((rr * math.cos(ang), rr * math.sin(ang), 0)),
                                     ph=(j + rng.uniform(-0.3, 0.3)) / float(n_per), life=life * rng.uniform(0.85, 1.15),
                                     rise=rise * rng.uniform(0.8, 1.2), size=size * rng.uniform(0.75, 1.25),
                                     dx=rng.uniform(-drift, drift), dy=rng.uniform(-drift, drift) * 0.5, sw=rng.uniform(0, 6.28),
                                     spin=rng.uniform(-0.6, 0.6)))
                i += 1
        self.grow, self.alpha = grow, alpha

    def key(self, f, g, level=1.0):
        for ob, P in zip(self.obs, self.par):
            u = ((g / P["life"]) + P["ph"]) % 1.0
            s = P["size"] * (0.45 + self.grow * u)
            ob.location = P["p"] + Vector((P["dx"] * u + 0.05 * math.sin(g * 0.12 + P["sw"]), P["dy"] * u, P["rise"] * (u ** 0.8)))
            ob.scale = (s, s, s)
            a = level * self.alpha * (min(1.0, u / 0.18) * (1 - u) ** 1.3)
            ob.color = (1.0, 1.0, 1.0, a)
            ob.keyframe_insert("location", frame=f); ob.keyframe_insert("scale", frame=f); ob.keyframe_insert("color", frame=f)


# ----------------------------------------------------------------------------- cameras
def cam22(g):
    if g < G_LOAF:                                                   # A: CU kit, push in + drift
        u = ez((g - RANGES[22][0]) / float(G_LOAF - RANGES[22][0]), "sine")
        loc = Vector(lerp((1.05, 4.30, 2.15), (0.85, 3.90, 2.08), u))
        look = Vector(lerp((0.56, 2.55, 2.02), (0.55, 2.55, 2.00), u))
        return loc, look, 24.0
    u = ez((g - G_LOAF) / float(S23 - G_LOAF), "sine")               # B: punch-in on the loaf + face
    loc = Vector(lerp((0.20, 4.85, 2.08), (0.15, 4.55, 2.05), u))
    look = Vector(lerp((0.20, 2.55, 1.95), (0.22, 2.55, 1.95), u))
    return loc, look, 24.0


SCALE_A = ((1.42, 1.62, 1.95), (1.88, 0.74, 1.70))      # ECU of the loaf pan (23 / 24 share it: match cut)
SCALE_B = ((1.52, 1.48, 1.90), (1.88, 0.74, 1.72))


def cam23(g):
    u = ez((g - S23) / float(S24 - S23), "sine")
    return Vector(lerp(SCALE_A[0], SCALE_B[0], u)), Vector(lerp(SCALE_A[1], SCALE_B[1], u)), 26.0


def cam24(g):
    u = ez((g - S24) / float(S25 - S24), "sine")
    a = SCALE_B
    b = ((1.60, 1.40, 1.86), (1.88, 0.74, 1.82))         # keeps pushing, tilts up with the rising pan
    return Vector(lerp(a[0], b[0], u)), Vector(lerp(a[1], b[1], u)), 26.0


def cam25(g):
    if g < G_EVERY:
        u = ez((g - S25) / float(G_EVERY - S25), "sine")
        loc = Vector(lerp((3.35, 2.55, 2.05), (3.55, 2.95, 1.95), u))
        look = Vector(lerp((4.55, 4.40, 1.62), (4.55, 4.40, 1.75), u))
        return loc, look, 24.0
    u = ez((g - G_EVERY) / float(RANGES[25][1] + 1 - G_EVERY), "sine")
    loc = Vector(lerp((3.45, 2.75, 2.25), (3.40, 2.65, 2.95), u))
    look = Vector(lerp((4.55, 4.40, 2.60), (4.55, 4.40, 3.40), u))
    return loc, look, 22.0


CAMS = {22: cam22, 23: cam23, 24: cam24, 25: cam25}


# ----------------------------------------------------------------------------- kit (shot 22)
def kit_pose(g):
    if g < G_LOAF:
        u = ez((g - G_NOTCHEAT + 3) / 6.0)                           # worried -> determined
        p = dict(yaw=lerp(0.22, 0.12, u), pitch=lerp(-0.18, 0.02, u), expr="worried" if u < 0.5 else "determined",
                 head_roll=lerp(-6, -2, u) + 1.5 * math.sin(g * 0.09), gaze=(lerp(0.75, 0.25, u), lerp(-0.7, 0.05, u)),
                 arm_r="chin", arm_l=dict(hand=(-0.10, 0.78), bend=0.7), legs="narrow", t=g / 30.0)
        p["pitch"] += 0.10 * pulse(g, G_NOTCHEAT + 2, G_NOTCHEAT + 4, G_NOTCHEAT + 9, 1.0)    # one small nod
        p["blink"] = blink(g, [1244, G_NOTCHEAT - 1, 1281])
        return p
    u = ez((g - G_LOAF) / 5.0)
    p = dict(yaw=0.30, pitch=-0.05, expr="stunned" if g < 1300 else "determined", head_roll=-5 + 2 * math.sin(g * 0.11),
             gaze=(0.95, -0.25), arm_r=dict(hand=(lerp(0.60, 0.74, u), lerp(0.30, -0.02, u)), bend=-0.6, stretch=1.3, layer="top"),
             prop_r=dict(type="loaf", scale=1.6), arm_l=dict(hand=(-0.10, 0.78), bend=0.7), legs="narrow", t=g / 30.0)
    p["blink"] = blink(g, [G_LOAF, 1299])
    return p


# ----------------------------------------------------------------------------- the take
CANVAS_KIT = (-1.5625, -3.875, 1.5625, 0.1875)


class Take(C.Take):
    def __init__(self, shot, quality="preview"):
        self.shot = shot
        C.Take.__init__(self, "bakery", PRESET[shot], quality=quality, lens=24.0, name="cam_s%d" % shot)
        self.puffs = None
        sd = os.path.join(TMP, "sprites%d" % shot)
        if shot == 22:
            self.actors["kit"] = C.make_actor("kit", "kit", sd, CANVAS_KIT)
        if shot in (23, 24):
            items = [(tag_svg("500 ก.", "#3a2832"), TAG_BOX, 900), (tag_svg("480 ก.", "#c8281e", "#f7dcc0"), TAG_BOX, 900)]
            pngs = C.svg_pngs(items, os.path.join(TMP, "props"))
            self.tag = C.PropCard("tag", pngs, TAG_BOX, scale=0.42, shadow=True)
            pan = B.STATE["small"]["pans"][0]
            self.tag.root.parent = pan
            bpy.context.view_layer.update()
            self.tag_rest = pan.matrix_world.inverted() @ (PAN + Vector((-0.20, 0.16, 0.06)))
            self.tag.root.location = self.tag_rest
            loc, _, _ = CAMS[shot](S23)
            d = Vector(loc) - (PAN + Vector((-0.20, 0.16, 0.06)))
            self.tag.root.rotation_euler = (math.radians(-8), math.radians(-6), math.atan2(d.x, -d.y))
        if shot == 23:
            self.puffs = Puffs("puffs", self.cam, [(PAN + Vector((0, 0, 0.18)), 0.06)], 5, 34, 0.75, 0.30, grow=1.6,
                               drift=0.10, strength=2.4, seed=3, alpha=0.75)
        if shot == 25:
            srcs = [(Vector((4.30, 4.15, 1.55)), 0.35), (Vector((4.75, 4.75, 1.55)), 0.35), (Vector((4.25, 5.30, 1.55)), 0.3)]
            self.puffs = Puffs("puffs", self.cam, srcs, 6, 48, 2.2, 0.75, grow=2.2, drift=0.35, strength=2.4, seed=7, alpha=0.95)

    def cam_of(self, g):
        return CAMS[self.shot](g)

    def pose(self, gs):
        shot = self.shot
        for g in gs:
            f = bf(g)
            loc, look, lens = self.cam_of(g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, steam=dict(AFTERNOON=0.0, MORNING=0.35)[PRESET[shot]] if shot != 25 else 1.5, oven=1.0)
            if shot == 22:
                C.place(self.actors["kit"], f, KIT, 0.0)
            if shot == 23:
                k = g - S23
                B.set_scale(2.8 * math.exp(-k / 6.0) * math.cos(k * 0.55), frame=f)
                self.tag.show(0, frame=f)
            if shot == 24:
                u = clamp((g - (G_FALL + 2)) / 16.0)
                ang = -8.0 * ez(u, "sine") - 1.6 * math.sin(math.pi * clamp((g - (G_FALL + 14)) / 10.0))
                B.set_scale(ang, frame=f)
                # tag flip: squash x to 0 (g 1361..1364), swap, open (1364..1367)
                gf = G_480 - 1
                sx = 1.0
                if gf - 3 <= g < gf:
                    sx = 1.0 - (g - (gf - 3)) / 3.0
                elif gf <= g < gf + 3:
                    sx = (g - gf) / 3.0
                sx = max(0.04, sx)
                self.tag.root.scale = (0.42 * sx, 0.42, 0.42 * (1.0 + 0.12 * (1 - sx)))
                self.tag.root.keyframe_insert("scale", frame=f)
                self.tag.show(0 if g < gf else 1, frame=f)
                lo = B.STATE["small"]["loaf"]
                lo.scale = (1.0, 1.0, 1.0)
                lo.keyframe_insert("scale", frame=f)
            if self.puffs is not None:
                self.puffs.key(f, g, level=1.0)
        if shot == 22:
            kit = self.actors["kit"]
            for g in gs:
                f = bf(g)
                self.scene.frame_set(f)
                kit.pose(f, kit_pose(g), camera=self.cam)
            self.sprites_for([(kit, 640)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look, lens = self.cam_of(g)
        out = dict(shot=self.shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f))
        an = self.anch.get(("kit", f))
        if an and "prop_tip_r" in an:
            k = self.actors["kit"]
            out["loaf_px"] = [round(v, 1) for v in actors.local_to_screen(k, self.cam, an["prop_tip_r"], f, k.feet.get(f))[:2]]
        return out

    def render_g(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def final(shot, spec, scale=1.0, samples=12):
    gs = [g for g in C.parse(spec) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    out = os.path.join(HERE, "raw")
    os.makedirs(out, exist_ok=True)
    todo = []
    for g in gs:
        png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
        ok = os.path.exists(png) and os.path.exists(js)
        if ok:
            m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
        if not ok:
            todo.append(g)
    print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
    if not todo:
        return
    Tk = Take(shot, "final")
    Tk.pose(todo)
    for g in todo:
        st = Tk.render_g([g], out, scale=scale, samples=samples)[0]
        png = os.path.join(out, "g_%04d.png" % g)
        os.replace(st["path"], png)
        rep = Tk.report(g)
        rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
        json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
        print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)


if __name__ == "__main__":
    cmd, shot = sys.argv[1], int(sys.argv[2])
    if cmd == "stills":
        Tk = Take(shot, "preview")
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
        out = sys.argv[4]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            st = Tk.render_g([g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
            print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        final(shot, sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 1.0, int(sys.argv[5]) if len(sys.argv) > 5 else 12)
