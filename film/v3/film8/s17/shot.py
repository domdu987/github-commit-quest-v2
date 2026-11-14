#!/usr/bin/env python3
"""shot.py -- film 8 take s17: shots 17-19, THE REVEAL (plan 44.89-55.57 s), with 6 handle frames each side.
"because the clear night sky is colder than ice, the water's heat floats away up to the sky; and the wall shades it all day:
so water freezes although the air around is not even at zero degrees."  One location (desert_ice plain), three set-ups:

    id 17  g 1341..1484  shot 17 (g 1347..1478), NIGHT: low in channel 1, the camera tilts up from the dark starlit water (soft heat
                         wisps lifting off every channel) to the brilliant sky -- the Milky Way overhead, the dome and its glowing door
                         at the right, lanterns into depth.  The wisps are this shot's own (the set's 26 D cards read as hard streaks):
                         ~44 short soft translucent ribbons born on the water, rising, widening and fading out on the way up.
    id 18  g 1474..1566  shot 18 (g 1479..1560), NOON: from the north bank, the 15 D wall stands against the blazing sun; its
                         long blue shadow lies over all five channels (ice kept, thick), the sunlit sand beyond.  Slow crane down + push.
    id 19  g 1556..1672  shot 19 (g 1561..1666), NIGHT: channel close-up, ice crystals spread across the open water from the banks
                         inward (a runtime frost-front mask on the set's ice material), the thin sheet with frost needles grows.
In-take transitions: 10-frame dissolves centred on the plan cuts (g 1474..1483 and g 1556..1565), both set-ups rendered there.

NO depth of field (client rule): C.Take switches it off at build and before every render.  Nobody on screen (no mouths).
Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py stills 17,19 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 17,19|18 a:b[:step] [scale] [samples]
"""
import math, os, sys, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import bpy                                               # noqa: E402
import numpy as np                                       # noqa: E402
from PIL import Image, ImageFilter                       # noqa: E402
from mathutils import Vector                             # noqa: E402

D, camrig = C.D, C.camrig
lerp, clamp, ez, bf = C.lerp, C.clamp, C.ez, C.bf
TMP = os.path.join(HERE, "work")
os.makedirs(TMP, exist_ok=True)

# ----------------------------------------------------------------------------- timing
G0 = C.g_bound(44.89)              # 1347
G_18 = C.g_bound(49.30)            # 1479
G_19 = C.g_bound(52.03)            # 1561
G1 = C.g_bound(55.57)              # 1667
H = 6                              # handles
XD = 10                            # in-take dissolve length (frames), centred on the plan cut
RANGES = {17: (G0 - H, G_18 + XD // 2 - 1), 18: (G_18 - XD // 2, G_19 + XD // 2 - 1), 19: (G_19 - XD // 2, G1 + H - 1)}
LIGHT = {17: "NIGHT", 18: "NOON", 19: "NIGHT"}


def aim(loc, az, el, d=30.0):
    a, e = math.radians(az), math.radians(el)
    return tuple(loc[i] + d * v for i, v in enumerate((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))))


def mix_u(x):
    x = clamp(x)
    return 0.4 * ez(x, "sine") + 0.6 * x


# ----------------------------------------------------------------------------- cameras
# 17: low over channel 1 (y 1.8) near its west part, looking ENE along the channels; tilt up from the water to the Milky Way.
CAM17 = dict(p0=(-6.0, 1.55, 0.55), p1=(-4.6, 1.75, 0.95), az0=67.0, az1=67.5, el0=4.0, el1=30.0, lens=18.0)
# 18: from the north (beyond channel 5), looking south-south-west at the wall, the sun above its crest; crane down + push.
CAM18 = dict(p0=(9.0, 28.5, 9.4), p1=(8.0, 26.8, 8.4), az0=-160.0, az1=-158.0, el0=4.5, el1=6.5, lens=16.0)
# 19: close over channel 2 (y 4.6) looking east along it, as the preset channel_ecu, slow glide + slight tilt down.
CAM19 = dict(p0=(-5.0, 4.25, 1.15), p1=(-3.9, 4.45, 1.0), az0=79.0, az1=80.5, el0=-10.0, el1=-12.0, lens=22.0)
CAMS = {17: CAM17, 18: CAM18, 19: CAM19}


def cam_of(shot, g):
    c = CAMS[shot]; a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    if shot == 17:                  # hold the tilt slower at the start (wisps lifting off the water), ease into the sky
        u = clamp(0.25 * x + 0.75 * ez(x, "sine"))
    else:
        u = mix_u(x)
    p = Vector(lerp(c["p0"], c["p1"], u))
    return p, Vector(aim(p, lerp(c["az0"], c["az1"], u), lerp(c["el0"], c["el1"], u))), c["lens"]


# ----------------------------------------------------------------------------- soft heat wisps (runtime, replaces the set's cards)
def wisp_texture(path):
    """128 x 512 RGBA: three soft sinuous ribbons + a faint veil, heavily blurred, periodic-free (each card fades at both ends)."""
    if os.path.exists(path):
        return path
    W, Hh = 128, 512
    yy, xx = np.mgrid[0:Hh, 0:W].astype(np.float32)
    v = yy / Hh
    a = np.zeros((Hh, W), np.float32)
    r = random.Random(5)
    for k in range(3):
        x0 = W * (0.3 + 0.2 * k) + r.uniform(-6, 6); ph = r.uniform(0, 6.28); amp = r.uniform(10, 18)
        xc = x0 + amp * np.sin(ph + 2 * math.pi * 1.3 * v) + 5 * np.sin(2 * ph + 2 * math.pi * 3.1 * v)
        sig = 5.0 + 9.0 * (1 - v)                       # wider toward the top (v 0 = top of the image)
        a += (0.55 - 0.1 * k) * np.exp(-0.5 * ((xx - xc) / sig) ** 2)
    a += 0.18 * np.exp(-0.5 * ((xx - W / 2) / 26.0) ** 2)
    a = np.clip(a, 0, 1)
    im = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    rgba = Image.merge("RGBA", (Image.new("L", (W, Hh), 255),) * 3 + (im,))
    rgba.save(path)
    return path


def wisp_material(img_path, rgb=(0.72, 0.86, 1.0)):
    """camera-only additive: emission rgb x K x tex alpha (UV shimmer-distorted by a 4D noise, W keyed per frame) x sin(pi v)^1.4 x
    object alpha (ob.color[3], keyed per card per frame)."""
    m = bpy.data.materials.new("s17_wisp"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    N, L = nt.nodes.new, nt.links.new
    out = N("ShaderNodeOutputMaterial")
    uv = N("ShaderNodeUVMap")
    nz = N("ShaderNodeTexNoise"); nz.name = "shimmer"; nz.noise_dimensions = "4D"; nz.inputs["Scale"].default_value = 3.0
    nz.inputs["Detail"].default_value = 1.5
    L(uv.outputs["UV"], nz.inputs["Vector"])
    sub = N("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = (0.5, 0.5, 0.5)
    L(nz.outputs["Color"], sub.inputs[0])
    sc = N("ShaderNodeVectorMath"); sc.operation = "MULTIPLY"; sc.inputs[1].default_value = (0.16, 0.05, 0.0)
    L(sub.outputs[0], sc.inputs[0])
    ad = N("ShaderNodeVectorMath"); ad.operation = "ADD"; L(uv.outputs["UV"], ad.inputs[0]); L(sc.outputs[0], ad.inputs[1])
    tx = N("ShaderNodeTexImage"); tx.image = bpy.data.images.load(img_path, check_existing=True); tx.extension = "CLIP"
    L(ad.outputs[0], tx.inputs["Vector"])
    sp = N("ShaderNodeSeparateXYZ"); L(uv.outputs["UV"], sp.inputs[0])
    mu = N("ShaderNodeMath"); mu.operation = "MULTIPLY"; mu.inputs[1].default_value = math.pi; L(sp.outputs["Y"], mu.inputs[0])
    sn = N("ShaderNodeMath"); sn.operation = "SINE"; L(mu.outputs[0], sn.inputs[0])
    sn2 = N("ShaderNodeMath"); sn2.operation = "MAXIMUM"; sn2.inputs[1].default_value = 0.0; L(sn.outputs[0], sn2.inputs[0])
    pw = N("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 1.4; L(sn2.outputs[0], pw.inputs[0])
    sx = N("ShaderNodeMath"); sx.operation = "MULTIPLY"; sx.inputs[1].default_value = math.pi; L(sp.outputs["X"], sx.inputs[0])
    snx = N("ShaderNodeMath"); snx.operation = "SINE"; L(sx.outputs[0], snx.inputs[0])
    snx2 = N("ShaderNodeMath"); snx2.operation = "MAXIMUM"; snx2.inputs[1].default_value = 0.0; L(snx.outputs[0], snx2.inputs[0])
    oi = N("ShaderNodeObjectInfo")
    m1 = N("ShaderNodeMath"); m1.operation = "MULTIPLY"; L(tx.outputs["Alpha"], m1.inputs[0]); L(pw.outputs[0], m1.inputs[1])
    m2 = N("ShaderNodeMath"); m2.operation = "MULTIPLY"; L(m1.outputs[0], m2.inputs[0]); L(oi.outputs["Alpha"], m2.inputs[1])
    m2b = N("ShaderNodeMath"); m2b.operation = "MULTIPLY"; L(m2.outputs[0], m2b.inputs[0]); L(snx2.outputs[0], m2b.inputs[1])
    kv = N("ShaderNodeValue"); kv.name = "wisp_K"; kv.outputs[0].default_value = 0.0
    m3 = N("ShaderNodeMath"); m3.operation = "MULTIPLY"; L(m2b.outputs[0], m3.inputs[0]); L(kv.outputs[0], m3.inputs[1])
    em = N("ShaderNodeEmission"); em.inputs["Color"].default_value = (*rgb, 1.0); L(m3.outputs[0], em.inputs["Strength"])
    tr = N("ShaderNodeBsdfTransparent"); add = N("ShaderNodeAddShader"); L(tr.outputs[0], add.inputs[0]); L(em.outputs[0], add.inputs[1])
    lp = N("ShaderNodeLightPath"); tr2 = N("ShaderNodeBsdfTransparent"); mx = N("ShaderNodeMixShader")
    L(lp.outputs["Is Camera Ray"], mx.inputs["Fac"]); L(tr2.outputs[0], mx.inputs[1]); L(add.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m


class Wisps(object):
    """n soft cards; card i: channel c, x, birth phase, life (frames), rise height, width; each frame: z rises with age (eased),
    the card widens and grows, alpha = fade-in (15 %) x fade-out (from 40 % of life), turned to face the camera about Z."""

    def __init__(self, n=44, seed=11):
        S = D.STATE
        self.mat = wisp_material(wisp_texture(os.path.join(TMP, "wisp_soft.png")))
        me = bpy.data.meshes.new("s17_wisp_quad")
        me.from_pydata([(-0.5, 0, 0), (0.5, 0, 0), (0.5, 0, 1), (-0.5, 0, 1)], [], [(0, 1, 2, 3)])
        uvl = me.uv_layers.new(name="UVMap")
        for i, co in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
            uvl.data[i].uv = co
        me.materials.append(self.mat)
        r = random.Random(seed)
        self.cards = []
        for i in range(n):
            ob = bpy.data.objects.new("s17_wisp_%02d" % i, me)
            S["SET"].objects.link(ob)
            ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
            ob.visible_transmission = False; ob.visible_volume_scatter = False
            c = D.CH_Y[i % 5]
            p = dict(x=r.uniform(-12.0, 24.0), y=c + r.uniform(-0.45, 0.45), life=r.uniform(90, 140), ph=r.random(),
                     rise=r.uniform(6.0, 11.0), w=r.uniform(0.7, 1.15), h=r.uniform(2.6, 4.0), sway=r.uniform(0.2, 0.5),
                     sp=r.uniform(0.03, 0.06), a=r.uniform(0.6, 1.0))
            self.cards.append((ob, p))
        for i in range(12):                              # foreground: small wisps lifting off channels 1-2 in front of the lens
            ob = bpy.data.objects.new("s17_wisp_n%02d" % i, me)
            S["SET"].objects.link(ob)
            ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
            ob.visible_transmission = False; ob.visible_volume_scatter = False
            c = D.CH_Y[i % 2]
            p = dict(x=r.uniform(-2.0, 9.0), y=c + r.uniform(-0.5, 0.5), life=r.uniform(70, 100), ph=r.random(),
                     rise=r.uniform(2.8, 4.5), w=r.uniform(0.45, 0.7), h=r.uniform(1.3, 2.0), sway=r.uniform(0.1, 0.25),
                     sp=r.uniform(0.04, 0.07), a=r.uniform(0.7, 1.0))
            self.cards.append((ob, p))
        self.nt = self.mat.node_tree

    def key(self, f, g, cam_loc, level):
        self.nt.nodes["wisp_K"].outputs[0].default_value = 0.24 * level
        self.nt.nodes["wisp_K"].outputs[0].keyframe_insert("default_value", frame=f)
        w = self.nt.nodes["shimmer"].inputs["W"]; w.default_value = 0.035 * g; w.keyframe_insert("default_value", frame=f)
        for ob, p in self.cards:
            age = ((g / p["life"]) + p["ph"]) % 1.0
            z = -0.12 + p["rise"] * (age ** 0.85)
            x = p["x"] + p["sway"] * math.sin(g * p["sp"] + p["ph"] * 6.28) + 0.8 * age
            env = clamp(age / 0.12) * (1.0 - ez(clamp((age - 0.25) / 0.6), "sine"))
            ob.location = (x, p["y"], z)
            d = Vector(cam_loc) - Vector((x, p["y"], z))
            ob.rotation_euler = (0.0, 0.0, math.atan2(d.x, -d.y) + math.pi)
            ob.scale = (p["w"] * (1.0 + 0.9 * age), 1.0, p["h"] * (1.0 + 0.5 * age))
            ob.color = (1.0, 1.0, 1.0, env * p["a"])
            for path in ("location", "rotation_euler", "scale", "color"):
                ob.keyframe_insert(path, frame=f)
            ob.hide_render = level <= 0.001 or env <= 0.001
            ob.keyframe_insert("hide_render", frame=f)


# ----------------------------------------------------------------------------- frost front (shot 19): crystals spread from the banks
def add_frost_front():
    """alpha of the set's ice x a front mask: d = distance of the point from its channel's nearest bank lip (0 at the lip, 1 at the
    centre line) + noise fingers; mask = smoothstep(spread - d) -- value node 's17_spread' -0.4 (no ice) .. 1.6 (whole channel).
    A soft white rim glows along the advancing front."""
    m = D.STATE["M"]["ice"]; nt = m.node_tree; N, L = nt.nodes.new, nt.links.new
    iv = nt.nodes["ice_vis"]
    tgt = iv.outputs[0].links[0].to_node                  # av (alpha x ice_vis)
    geo = N("ShaderNodeNewGeometry"); sp = N("ShaderNodeSeparateXYZ"); L(geo.outputs["Position"], sp.inputs[0])
    # local offset from the channel centre: ((y - 1.8 + 1.4) mod 2.8) - 1.4
    a1 = N("ShaderNodeMath"); a1.operation = "ADD"; a1.inputs[1].default_value = -1.8 + 1.4; L(sp.outputs["Y"], a1.inputs[0])
    md = N("ShaderNodeMath"); md.operation = "FLOORED_MODULO"; md.inputs[1].default_value = 2.8; L(a1.outputs[0], md.inputs[0])
    a2 = N("ShaderNodeMath"); a2.operation = "ADD"; a2.inputs[1].default_value = -1.4; L(md.outputs[0], a2.inputs[0])
    ab = N("ShaderNodeMath"); ab.operation = "ABSOLUTE"; L(a2.outputs[0], ab.inputs[0])
    dd = N("ShaderNodeMath"); dd.operation = "SUBTRACT"; dd.inputs[0].default_value = 1.0; L(ab.outputs[0], dd.inputs[1])   # 0 lip .. 1 centre
    nz = N("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.2; nz.inputs["Detail"].default_value = 6.0
    nz.inputs["Roughness"].default_value = 0.65; L(geo.outputs["Position"], nz.inputs["Vector"])
    nz2 = N("ShaderNodeMath"); nz2.operation = "MULTIPLY_ADD"; nz2.inputs[1].default_value = 0.9; nz2.inputs[2].default_value = -0.45
    L(nz.outputs["Fac"], nz2.inputs[0])
    d2 = N("ShaderNodeMath"); d2.operation = "ADD"; L(dd.outputs[0], d2.inputs[0]); L(nz2.outputs[0], d2.inputs[1])
    spv = N("ShaderNodeValue"); spv.name = "s17_spread"; spv.outputs[0].default_value = 5.0
    fr = N("ShaderNodeMath"); fr.operation = "SUBTRACT"; L(spv.outputs[0], fr.inputs[0]); L(d2.outputs[0], fr.inputs[1])
    mk = N("ShaderNodeMapRange"); mk.interpolation_type = "SMOOTHSTEP"; mk.inputs["From Min"].default_value = 0.0
    mk.inputs["From Max"].default_value = 0.12; L(fr.outputs[0], mk.inputs["Value"])
    mm = N("ShaderNodeMath"); mm.operation = "MULTIPLY"
    L(iv.outputs[0], mm.inputs[0]); L(mk.outputs["Result"], mm.inputs[1])
    for l in list(iv.outputs[0].links):
        if l.to_node != mm:
            to = l.to_socket; nt.links.remove(l); L(mm.outputs[0], to)
    # rim: 4 m (1 - m) on the colour, toward frost white
    om = N("ShaderNodeMath"); om.operation = "SUBTRACT"; om.inputs[0].default_value = 1.0; L(mk.outputs["Result"], om.inputs[1])
    rm = N("ShaderNodeMath"); rm.operation = "MULTIPLY"; L(mk.outputs["Result"], rm.inputs[0]); L(om.outputs[0], rm.inputs[1])
    rk = N("ShaderNodeMath"); rk.operation = "MULTIPLY"; rk.inputs[1].default_value = 3.2; L(rm.outputs[0], rk.inputs[0])
    rc = N("ShaderNodeMath"); rc.operation = "MINIMUM"; rc.inputs[1].default_value = 1.0; L(rk.outputs[0], rc.inputs[0])
    cm = [n for n in nt.nodes if n.bl_idname == "ShaderNodeMix" and n.data_type == "RGBA" and n.inputs[6].is_linked
          and n.inputs[6].links[0].from_node.bl_idname == "ShaderNodeTexImage" and n.inputs[7].is_linked][0]
    outs = list(cm.outputs[2].links)
    wm = N("ShaderNodeMix"); wm.data_type = "RGBA"; L(rc.outputs[0], wm.inputs[0]); L(cm.outputs[2], wm.inputs[6])
    wm.inputs[7].default_value = (0.92, 0.97, 1.0, 1.0)
    for l in outs:
        to = l.to_socket; nt.links.remove(l); L(wm.outputs[2], to)
    # make the rim also more opaque: alpha = max(alpha, rim * 0.8 * mask_vis)
    return spv


def key_spread(spv, v, f):
    spv.outputs[0].default_value = v
    spv.outputs[0].keyframe_insert("default_value", frame=f)


# ----------------------------------------------------------------------------- runtime dressing
def dress(shot):
    S = D.STATE; M = S["M"]; mb = D.MB()
    if shot in (17, 19):
        # the bank between channels 1 and 2 (y 3.2) and between 2 and 3 (y 6.0): jars, buckets, a stack of reed mats, rocks
        D._jar(mb, (3.4, 6.0, 0.0), M, h=1.05, r=0.36, seed=3)
        D._jar(mb, (4.15, 6.1, 0.0), M, h=0.8, r=0.3, seed=4)
        D._bucket(mb, (-1.0, 3.15, 0.0), M, s=0.55)
        D._bucket(mb, (6.5, 6.0, 0.0), M, s=0.55)
        D._jar(mb, (-7.5, 6.0, 0.0), M, h=0.95, r=0.34, seed=5)
        D._bucket(mb, (-8.6, 3.25, 0.0), M, s=0.5)
        for k, (x, y) in enumerate(((9.0, 3.2), (14.0, 3.15), (-3.6, 6.05), (4.4, 8.8), (16.5, 6.0))):
            D.lumpy(mb, (x, y, 0.05), 0.22 + 0.04 * k % 0.12, M["rock"], 900 + k, seg=8, rings=4, rough=0.3, squash=0.6)
        for k, (x, y) in enumerate(((-12.0, -4.5), (-4.0, 19.0), (6.0, 20.5), (18.0, 19.0))):
            D._shrub(mb, (x, y, 0.0), M, 40 + k, s=1.0)
    if shot == 18:
        # the sunlit north side: jars, buckets and a sledge with cut ice blocks waiting in the shade line, shrubs, palms far
        D._jar(mb, (4.6, 15.6, 0.0), M, h=1.3, r=0.45, seed=7)
        D._jar(mb, (5.5, 15.9, 0.0), M, h=1.0, r=0.36, seed=8)
        D._bucket(mb, (3.6, 15.4, 0.0), M, s=0.6)
        D._bucket(mb, (-2.0, 11.6, 0.0), M, s=0.55)
        D._jar(mb, (1.4, 8.8, 0.0), M, h=0.9, r=0.32, seed=9)
        for k, (x, y) in enumerate(((11.5, 17.5), (-3.0, 18.5), (14.0, 21.0))):
            D._shrub(mb, (x, y, 0.0), M, 60 + k, s=1.1)
        for k, (x, y) in enumerate(((7.5, 16.4), (2.0, 17.2), (12.0, 15.6))):
            D.lumpy(mb, (x, y, 0.05), 0.25, M["rock"], 950 + k, seg=8, rings=4, rough=0.3, squash=0.6)
    ob = D._obj(mb, "s17_dress", S["SET"], hull=0.012)
    D.no_bounce(ob)
    return ob


# ----------------------------------------------------------------------------- the take
STATE_ICE = {17: "water", 18: "thick"}


class Take(C.Take):
    def __init__(self, quality="preview", shot=17):
        preset = "wall_low" if LIGHT[shot] == "NOON" else "channel_ecu"
        C.Take.__init__(self, "desert_ice", preset, quality=quality, lens=CAMS[shot]["lens"], name="cam_s17", light=LIGHT[shot])
        self.light = LIGHT[shot]
        D.set_heat_wisps(0.0)
        self.dress = dress(18 if self.light == "NOON" else 17)
        self.wisps = Wisps() if self.light == "NIGHT" else None
        self.spread = add_frost_front() if self.light == "NIGHT" else None

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            if shot == 17:
                a, b = RANGES[17]
                lvl = 0.6 + 0.4 * clamp((g - a) / 30.0)
                self.key_set(f, stars=1.5, twinkle=0.45, ice="water")
                key_spread(self.spread, 5.0, f)
                self.wisps.key(f, g, loc, lvl)
            elif shot == 18:
                self.key_set(f, ice="thick")
                hole = D.STATE["ice"]["hole"]
                hole.hide_render = True; hole.keyframe_insert("hide_render", frame=f)
            else:
                a, b = G_19 - 2, G1 - 8                  # the front crosses the channel over the shot
                u = clamp((g - a) / float(b - a))
                spread = lerp(-0.35, 1.55, 0.3 * u + 0.7 * ez(u, "sine"))
                lvl = lerp(0.18, 0.42, u)
                self.key_set(f, stars=1.3, ice=(lvl, 0.0))
                key_spread(self.spread, spread, f)
                self.wisps.key(f, g, loc, 0.0)
                hole = D.STATE["ice"]["hole"]              # no sawn hole on the first freezing night
                hole.hide_render = True; hole.keyframe_insert("hide_render", frame=f)

    def report(self, shot, g):
        loc, look, lens = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    az=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={})

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd == "stills":
        out = sys.argv[4]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        Tk = None
        for shot in shots:
            if Tk is None or Tk.light != LIGHT[shot]:
                Tk = Take("preview", shot)
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, s: Take(q, s), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples,
                     take_key=lambda s: LIGHT[s])
