"""beauty.py -- v6 beauty pass over the v4 expressway set (v4 files are imported, never edited).

    import sys; sys.path.insert(0, PROJ + "/v6/set")
    import beauty as B                      # puts v4/set_expressway on sys.path too
    A = B.build()                           # v4 build + world, lights, materials, detail overrides
    B.setup_render("final", threads=4)      # 2 diffuse bounces, sky fill, 8 spp @ 75 %
    cam = B.presets.use("eye", A)           # or any v4 preset via B.X.use_camera(...)
    r = B.render6.render("/abs/out/eye", frame=7)

See API.md for the whole contract.
"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
V4 = os.path.join(PROJ, "v4", "set_expressway")
for p in (V4, HERE):
    if p not in sys.path: sys.path.insert(0, p)

import bpy
import numpy as np
from mathutils import Vector, Matrix

import expressway as X
import kit
import vehicles as V
import tex
from kit import MB, hexlin
import presets
import render6

MOON_DIR = Vector((-0.42, 0.85, 0.32)).normalized()     # the sky's moon disc (v4 build_world); the key comes from it
AMBIENT_STRENGTH = 0.3
SKY_FILL = 1.0


# =========================================================================================================== build
def build(seed=9, detail=True, scene=None):
    A = X.build(seed=seed, haze_cards=False)
    scene = scene or bpy.context.scene
    world6(scene)
    lights6(A)
    materials6(A)
    if detail: detail6(A)
    A["moon_dir"] = tuple(MOON_DIR)
    A["v6"] = True
    return A


SPP = {"preview": 4, "draft": 6, "final": 6, "final8": 8, "final12": 12, "native": 16}


def setup_render(quality="final", threads=4, scene=None):
    """v4 tiers (resolution %, OIDN) with the v6 light transport: 2 diffuse bounces (bounce + contact AO from the
    sky), 1 glossy, light tree off (measured: -11 % CPU here, many small lights are not worth the tree), and 6 spp
    for 'final' (8 spp cost +50 %: 'final8' for holds)."""
    X.setup_render(scene, quality=quality, threads=threads)
    cy = (scene or bpy.context.scene).cycles
    cy.max_bounces = 3; cy.diffuse_bounces = 2; cy.glossy_bounces = 1; cy.transmission_bounces = 1
    cy.samples = SPP.get(quality, cy.samples); cy.use_light_tree = False
    cy.sample_clamp_indirect = 3.0; cy.blur_glossy = 0.7


# =========================================================================================================== world
def world6(scene):
    """dark blue horror sky: navy zenith, deep blue cloud deck with lit edges (hue 235-245, never lavender), a low
    blue horizon glow with a trace of city sodium, the moon disc + a 100 px halo. Lights diffuse rays (sky fill)."""
    w = bpy.data.worlds.get("W_night6") or bpy.data.worlds.new("W_night6")
    scene.world = w
    nt = w.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    N = nt.nodes; L = nt.links.new
    out = N.new("ShaderNodeOutputWorld"); bg = N.new("ShaderNodeBackground")
    tc = N.new("ShaderNodeTexCoord"); sep = N.new("ShaderNodeSeparateXYZ"); L(tc.outputs["Generated"], sep.inputs[0])

    def M(op, a, b=None, clamp=False):
        n = N.new("ShaderNodeMath"); n.operation = op; n.use_clamp = clamp
        for i, x in enumerate((a, b)):
            if x is None: continue
            if isinstance(x, (int, float)): n.inputs[i].default_value = x
            else: L(x, n.inputs[i])
        return n.outputs[0]

    def ramp(fac, stops):
        n = N.new("ShaderNodeValToRGB"); cr = n.color_ramp
        while len(cr.elements) > 1: cr.elements.remove(cr.elements[-1])
        for i, (p, col) in enumerate(stops):
            e = cr.elements[0] if i == 0 else cr.elements.new(p)
            e.position = p; e.color = col
        L(fac, n.inputs[0]); return n.outputs[0]

    def mix(f, a, b, bt="MIX"):
        n = N.new("ShaderNodeMix"); n.data_type = "RGBA"; n.blend_type = bt
        for s, x in ((n.inputs[0], f), (n.inputs[6], a), (n.inputs[7], b)):
            if isinstance(x, (int, float)): s.default_value = x
            elif isinstance(x, tuple): s.default_value = x
            else: L(x, s)
        return n.outputs[2]

    z = M("ADD", M("MULTIPLY", sep.outputs["Z"], 0.5), 0.5)
    grad = ramp(z, [(0.0, hexlin("#040509")), (0.47, hexlin("#0e0e22")), (0.502, hexlin("#2e3474")),
                    (0.53, hexlin("#252a62")), (0.62, hexlin("#191b4c")), (0.80, hexlin("#0f1038")), (1.0, hexlin("#090924"))])
    hz = M("SUBTRACT", 1.0, M("MULTIPLY", M("ABSOLUTE", M("SUBTRACT", z, 0.508)), 30.0), True)
    col = mix(M("MULTIPLY", hz, 0.16), grad, hexlin("#6a5a52"))           # trace of city sodium in the horizon
    # cloud deck: higher contrast (ref edges), lit edges toward the moon, very dark gaps
    vm = N.new("ShaderNodeVectorMath"); vm.operation = "MULTIPLY"; vm.inputs[1].default_value = (1.0, 1.0, 3.2)
    L(tc.outputs["Generated"], vm.inputs[0])
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.4; nz.inputs["Detail"].default_value = 6.0
    nz.inputs["Roughness"].default_value = 0.62; L(vm.outputs[0], nz.inputs["Vector"])
    nz2 = N.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = 14.0; nz2.inputs["Detail"].default_value = 3.0
    L(vm.outputs[0], nz2.inputs["Vector"])
    f = M("ADD", nz.outputs["Fac"], M("MULTIPLY", M("SUBTRACT", nz2.outputs["Fac"], 0.5), 0.18))
    cl = M("MULTIPLY", M("SUBTRACT", f, 0.47), 5.0, True)
    above = M("MULTIPLY", M("SUBTRACT", z, 0.505), 30.0, True)
    dp = N.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"; dp.inputs[1].default_value = MOON_DIR
    L(tc.outputs["Generated"], dp.inputs[0])
    near_moon = M("POWER", M("MAXIMUM", dp.outputs["Value"], 0.0), 18.0)
    edge = M("MULTIPLY", M("MULTIPLY", cl, above), M("ADD", 0.45, M("MULTIPLY", near_moon, 1.6)))
    col = mix(M("MINIMUM", edge, 1.0), col, hexlin("#46447e"))              # lit cloud: hue ~244, S 0.46, not lavender
    dark = M("MULTIPLY", M("MULTIPLY", M("SUBTRACT", 0.47, f), 3.0, True), above)
    col = mix(M("MULTIPLY", dark, 0.75), col, hexlin("#07061a"))
    # moon: disc + core glow + wide halo (exp 300 -> ~100 px at 720 w), halo cooled to blue-white
    moon = M("GREATER_THAN", dp.outputs["Value"], math.cos(math.radians(1.5)))
    halo = M("POWER", M("MAXIMUM", dp.outputs["Value"], 0.0), 300.0)
    halo2 = M("POWER", M("MAXIMUM", dp.outputs["Value"], 0.0), 2500.0)
    col = mix(M("MULTIPLY", halo, 0.55), col, hexlin("#6f80c8"), "ADD")
    col = mix(M("MULTIPLY", halo2, 0.8), col, hexlin("#c9d4f2"), "ADD")
    col = mix(moon, col, (2.4, 2.55, 2.8, 1.0))
    L(col, bg.inputs["Color"])
    # strength: camera/glossy 1.0, diffuse rays SKY_FILL (sky lights the scene: cool fill, contact AO)
    lp = N.new("ShaderNodeLightPath")
    st = M("ADD", M("MULTIPLY", lp.outputs["Is Diffuse Ray"], SKY_FILL - 1.0), 1.0)
    L(st, bg.inputs["Strength"])
    L(bg.outputs[0], out.inputs["Surface"])
    w.cycles.sampling_method = "MANUAL"; w.cycles.sample_map_resolution = 256
    return w


# =========================================================================================================== lights
def lights6(A):
    sc = bpy.context.scene
    lc = bpy.data.collections.get("LIGHTS") or sc.collection
    ld = bpy.data.lights.new("moon_key", "SUN"); ld.energy = 2.2; ld.angle = math.radians(3.0)
    ld.color = (0.62, 0.74, 1.0)
    ob = bpy.data.objects.new("moon_key", ld); lc.objects.link(ob)
    ob.rotation_euler = (-MOON_DIR).to_track_quat("-Z", "Y").to_euler()
    ob.visible_glossy = False          # no streak of the sun on the wet road; the sky disc still reflects
    for L in bpy.data.lights:
        if L.name.startswith("sodium_"):
            L.energy = 10000.0; L.color = (1.0, 0.62, 0.30); L.shadow_soft_size = 0.4
        elif L.name.startswith("flood_key"):
            L.shadow_soft_size = 0.35; L.color = (0.93, 0.96, 1.0)
    for m in bpy.data.materials:          # the fake blue ambient: GI and the sky do the fill now
        if not m.use_nodes or not m.node_tree: continue
        for n in m.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED" and n.inputs["Emission Color"].is_linked and abs(n.inputs["Emission Strength"].default_value - 1.0) < 1e-6:
                n.inputs["Emission Strength"].default_value = AMBIENT_STRENGTH
    # sodium bulb glow a bit less orange
    for m in bpy.data.materials:
        if m.name == "sodium_bulb":
            for n in m.node_tree.nodes:
                if n.type == "EMISSION": n.inputs["Color"].default_value = (1.0, 0.70, 0.38, 1)


# ======================================================================================================== materials
def m_asphalt6():
    """wet asphalt v6: diffuse-rough dry patches (0.5) so the moon draws shadows, damp (0.28), standing water (0.03,
    ~40 %), rain ripples in the water (voronoi rings, re-seeded per frame), tar-sealed crack network, 2-4 cm
    aggregate, tyre-track ruts, chipped lane paint, oil darkening in the lane centres."""
    if "asphalt_v6" in bpy.data.materials: return bpy.data.materials["asphalt_v6"]
    mb = MB("asphalt_v6")
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    sep = mb.n("ShaderNodeSeparateXYZ"); mb.l(uv.outputs[0], sep.inputs[0])
    o, s = sep.outputs["X"], sep.outputs["Y"]; vec = uv.outputs[0]
    ao = mb.math("ABSOLUTE", o)
    ol = mb.wrap(mb.math("SUBTRACT", ao, 0.75), X.LANE)
    r1 = mb.math("ABSOLUTE", mb.math("SUBTRACT", ol, 1.45)); r2 = mb.math("ABSOLUTE", mb.math("SUBTRACT", ol, 4.35))
    rut = mb.math("MAXIMUM", mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", r1, 1.6), True), mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", r2, 1.6), True))
    oil = mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", mb.math("ABSOLUTE", mb.math("SUBTRACT", ol, 2.9)), 1.4), True)
    gut = mb.math("MAXIMUM", mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", mb.math("ABSOLUTE", mb.math("SUBTRACT", ao, 21.4)), 0.8), True),
                  mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", mb.math("ABSOLUTE", mb.math("SUBTRACT", ao, 1.2)), 1.2), True))
    nz = mb.n("ShaderNodeTexNoise", Scale=0.11, Detail=4.0, Roughness=0.62); mb.l(vec, nz.inputs["Vector"])
    nz2 = mb.n("ShaderNodeTexNoise", Scale=0.7, Detail=3.0); mb.l(vec, nz2.inputs["Vector"])
    wet = mb.math("ADD", mb.math("ADD", nz.outputs["Fac"], mb.math("MULTIPLY", rut, 0.10)), mb.math("ADD", mb.math("MULTIPLY", gut, 0.22), mb.math("MULTIPLY", nz2.outputs["Fac"], 0.10)))
    puddle = mb.math("MULTIPLY", mb.math("SUBTRACT", wet, 0.52), 14.0, True)      # 0 dry .. 1 standing water
    damp = mb.math("MULTIPLY", mb.math("SUBTRACT", wet, 0.40), 6.0, True)
    # aggregate + grit + crack network
    ag = mb.n("ShaderNodeTexNoise", Scale=30.0, Detail=4.0, Roughness=0.75); mb.l(vec, ag.inputs["Vector"])
    vo = mb.n("ShaderNodeTexVoronoi", Scale=12.0); mb.l(vec, vo.inputs["Vector"])
    grit = mb.math("LESS_THAN", vo.outputs["Distance"], 0.10)
    ck = mb.n("ShaderNodeTexVoronoi", Scale=0.55); ck.feature = "DISTANCE_TO_EDGE"
    wq = mb.n("ShaderNodeTexNoise", Scale=1.6, Detail=3.0); mb.l(vec, wq.inputs["Vector"])
    wv = mb.n("ShaderNodeVectorMath"); wv.operation = "ADD"; mb.l(vec, wv.inputs[0]); mb.l(wq.outputs["Color"], wv.inputs[1])
    mb.l(wv.outputs[0], ck.inputs["Vector"])
    cmask = mb.n("ShaderNodeTexNoise", Scale=0.3, Detail=2.0); mb.l(vec, cmask.inputs["Vector"])
    crack = mb.math("MULTIPLY", mb.math("LESS_THAN", ck.outputs["Distance"], 0.035), mb.math("GREATER_THAN", cmask.outputs["Fac"], 0.5))
    patch = mb.n("ShaderNodeTexNoise", Scale=0.16, Detail=3.0); mb.l(vec, patch.inputs["Vector"])
    base = mb.ramp(patch.outputs["Fac"], [(0.30, hexlin("#1d1e22")), (0.70, hexlin("#32333a"))])
    base = mb.mix(mb.math("MULTIPLY", grit, 0.55), base, hexlin("#4a4b52"))
    base = mb.mix(mb.math("MULTIPLY", rut, 0.30), base, hexlin("#121317"))
    base = mb.mix(mb.math("MULTIPLY", oil, 0.35), base, hexlin("#0c0c0f"))
    base = mb.mix(crack, base, hexlin("#060607"))

    def stripe(c, w):
        return mb.math("LESS_THAN", mb.math("ABSOLUTE", mb.math("SUBTRACT", ao, c)), w)
    dash = mb.math("LESS_THAN", mb.wrap(s, 15.0), 6.0)
    lw = mb.math("MULTIPLY", mb.math("MAXIMUM", stripe(6.55, 0.14), stripe(12.35, 0.14)), dash)
    wear = mb.n("ShaderNodeTexNoise", Scale=2.2, Detail=6.0, Roughness=0.7); mb.l(vec, wear.inputs["Vector"])
    keep = mb.math("GREATER_THAN", wear.outputs["Fac"], 0.40)
    white = mb.math("MULTIPLY", mb.math("MAXIMUM", lw, stripe(18.15, 0.17)), keep)
    yel = mb.math("MULTIPLY", stripe(1.25, 0.15), keep)
    col = mb.mix(white, base, hexlin("#b2b3ae"))
    col = mb.mix(yel, col, hexlin("#b58e1f"))
    paint = mb.math("MAXIMUM", white, yel)
    col = mb.mix(mb.math("MULTIPLY", damp, 0.35), col, hexlin("#0f1013"))        # damp darkens
    col = mb.mix(mb.math("MULTIPLY", puddle, 0.75), col, hexlin("#050608"))      # water: dark mirror
    rough = mb.math("SUBTRACT", 0.55, mb.math("MULTIPLY", damp, 0.27))
    rough = mb.math("ADD", mb.math("MULTIPLY", rough, mb.math("SUBTRACT", 1.0, puddle)), mb.math("MULTIPLY", puddle, 0.03))
    rough = mb.math("ADD", rough, mb.math("MULTIPLY", paint, 0.10))
    rough = mb.math("SUBTRACT", rough, mb.math("MULTIPLY", crack, 0.15))
    # rain ripples: rings from voronoi feature points, re-seeded each frame (W follows #frame), only in water
    rv = mb.n("ShaderNodeTexVoronoi", Scale=2.4); rv.voronoi_dimensions = "4D"
    mp = mb.n("ShaderNodeMapping", Scale=(1.0, 1.0, 1.0)); mb.l(vec, mp.inputs[0]); mb.l(mp.outputs[0], rv.inputs["Vector"])
    fc = rv.inputs["W"].driver_add("default_value"); fc.driver.expression = "frame * 0.37"
    ring = mb.math("SINE", mb.math("MULTIPLY", rv.outputs["Distance"], 55.0))
    fade = mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", rv.outputs["Distance"], 3.2), True)
    rip = mb.math("MULTIPLY", mb.math("MULTIPLY", ring, fade), puddle)
    bh = mb.math("ADD", mb.math("MULTIPLY", mb.math("ADD", ag.outputs["Fac"], mb.math("MULTIPLY", grit, 0.5)), mb.math("SUBTRACT", 1.0, puddle)),
                 mb.math("ADD", mb.math("MULTIPLY", rip, 0.05), mb.math("MULTIPLY", crack, -0.4)))
    nrm = kit.bump_node(mb, bh, 0.45, 0.012)
    b = mb.principled(col, rough, 0.0, 0.0, normal=nrm, spec=0.55)
    b.inputs["Emission Strength"].default_value = AMBIENT_STRENGTH
    return mb.out(b)


def _base_socket(m):
    """the Principled's Base Color input and whatever currently feeds it (socket or default tuple)."""
    b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if b is None: return None, None
    inp = b.inputs["Base Color"]
    src = inp.links[0].from_socket if inp.is_linked else tuple(inp.default_value)
    return b, src


def grime(m, amount=0.55, foot=0.6, streaks=True, rough_add=0.12, scale=1.0):
    """multiply grime into an existing material: world-space blotches, vertical run-off streaks, darker at the
    foot (z < foot D above the deck: road spray + AO). Also raises roughness."""
    if m is None or not m.use_nodes or m.get("v6_grime"): return
    nt = m.node_tree; N = nt.nodes; L = nt.links.new
    b, src = _base_socket(m)
    if b is None: return
    def node(t, **kw):
        n = N.new(t)
        for k, v in kw.items(): n.inputs[k].default_value = v
        return n
    def math(op, a, bb=None, clamp=False):
        n = N.new("ShaderNodeMath"); n.operation = op; n.use_clamp = clamp
        for i, x in enumerate((a, bb)):
            if x is None: continue
            if isinstance(x, (int, float)): n.inputs[i].default_value = x
            else: L(x, n.inputs[i])
        return n.outputs[0]
    geo = node("ShaderNodeNewGeometry")
    sp = N.new("ShaderNodeSeparateXYZ"); L(geo.outputs["Position"], sp.inputs[0])
    mp = N.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (0.9 * scale, 0.9 * scale, 0.06 * scale)
    L(geo.outputs["Position"], mp.inputs[0])
    st = node("ShaderNodeTexNoise", Scale=4.0, Detail=5.0, Roughness=0.7); L(mp.outputs[0], st.inputs["Vector"])
    bl = node("ShaderNodeTexNoise", Scale=0.35 * scale, Detail=5.0, Roughness=0.65); L(geo.outputs["Position"], bl.inputs["Vector"])
    g = math("MULTIPLY", math("SUBTRACT", bl.outputs["Fac"], 0.45), 2.5, True)
    if streaks:
        g = math("MAXIMUM", g, math("MULTIPLY", math("SUBTRACT", st.outputs["Fac"], 0.5), 3.0, True))
    ft = math("SUBTRACT", 1.0, math("DIVIDE", math("MAXIMUM", sp.outputs["Z"], 0.0), foot), True)
    g = math("MINIMUM", math("ADD", math("MULTIPLY", g, amount), math("MULTIPLY", ft, 0.55)), 0.9)
    mix = N.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"
    L(g, mix.inputs[0])
    if isinstance(src, tuple): mix.inputs[6].default_value = src
    else: L(src, mix.inputs[6])
    mix.inputs[7].default_value = (0.18, 0.17, 0.16, 1)
    L(mix.outputs[2], b.inputs["Base Color"])
    r = b.inputs["Roughness"]
    if r.is_linked:
        rs = r.links[0].from_socket; L(math("ADD", rs, math("MULTIPLY", g, rough_add)), r)
    else:
        r.default_value = min(1.0, r.default_value + rough_add * 0.5)
    m["v6_grime"] = True


def hero_paint():
    """white hero sedan, dirty: mud splash on the lower body, scratches, rain beads (v4 core) with a lighter coat."""
    mb = MB("paint_hero_v6")
    gen = mb.n("ShaderNodeTexCoord")
    sp = mb.n("ShaderNodeSeparateXYZ"); mb.l(gen.outputs["Object"], sp.inputs[0])
    nz = mb.n("ShaderNodeTexNoise", Scale=6.0, Detail=6.0, Roughness=0.7); mb.l(gen.outputs["Object"], nz.inputs["Vector"])
    mud = mb.math("MULTIPLY", mb.math("SUBTRACT", mb.math("ADD", mb.math("MULTIPLY", sp.outputs["Z"], -1.4), nz.outputs["Fac"]), -0.55), 2.5, True)
    sc = mb.n("ShaderNodeTexWave", Scale=9.0, Distortion=9.0, Detail=4.0); sc.wave_type = "BANDS"
    mb.l(gen.outputs["Object"], sc.inputs["Vector"])
    scm = mb.n("ShaderNodeTexNoise", Scale=1.3); mb.l(gen.outputs["Object"], scm.inputs["Vector"])
    scratch = mb.math("MULTIPLY", mb.math("GREATER_THAN", sc.outputs["Fac"], 0.93), mb.math("GREATER_THAN", scm.outputs["Fac"], 0.55))
    base = mb.mix(mb.math("MULTIPLY", mud, 0.85), hexlin("#e4e2dc"), hexlin("#3a3128"))
    base = mb.mix(mb.math("MULTIPLY", scratch, 0.7), base, hexlin("#6d6f73"))
    return mb.out(V._paint_core(mb, base, "sedan", coat=0.5))


def materials6(A):
    road = m_asphalt6()
    for ob in bpy.data.objects:
        if ob.type != "MESH": continue
        for sl in ob.material_slots:
            if sl.material and sl.material.name == "asphalt_wet": sl.material = road
    for m in list(bpy.data.materials):
        n = m.name
        if n.startswith("concrete"):
            grime(m, 0.6, foot=0.9, rough_add=0.15)
        elif n.startswith(("steel_galv", "steel_mast", "steel_gantry", "steel_wbeam", "lamp_housing")):
            grime(m, 0.45, foot=0.5, streaks=True, rough_add=0.2, scale=2.0)
        elif n.startswith(("plastic_", "cone_orange", "case_black", "medic_orange", "bag_", "waterbarrier")):
            grime(m, 0.35, foot=0.35, streaks=False, rough_add=0.1, scale=3.0)
        elif n.startswith("paint_") and "hero" not in n:
            grime(m, 0.25, foot=0.7, streaks=False, rough_add=0.05, scale=1.5)
    # hero sedan: white, muddy, scratched (every object of the hero rig that used the hero paint)
    hero = bpy.data.objects.get(A["hero_car"])
    if hero:
        hp = hero_paint()
        olds = set()
        for ob in [hero] + list(hero.children_recursive):
            for sl in getattr(ob, "material_slots", []):
                if sl.material and sl.material.name.startswith("paint_sedan_#c9ccd0"):
                    olds.add(sl.material.name); sl.material = hp


# =========================================================================================================== detail
def poster_tex():
    """a faded, torn, rain-stained advertising poster (no words, no brands): colour blocks, a circle, peeled strips."""
    from PIL import Image, ImageDraw, ImageFilter
    p = os.path.join(HERE, "tex", "poster_v6.png")
    if os.path.exists(p): return p
    os.makedirs(os.path.dirname(p), exist_ok=True)
    rng = np.random.default_rng(4)
    W, H = 1024, 420
    im = Image.new("RGB", (W, H), (196, 188, 170)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 430, H), fill=(28, 52, 112)); d.ellipse((520, 40, 860, 380), fill=(176, 40, 36))
    d.rectangle((600, 150, 780, 270), fill=(236, 230, 214)); d.rectangle((60, 280, 380, 330), fill=(232, 196, 64))
    for k in range(5): d.rectangle((70, 70 + k * 36, 360 - k * 40, 92 + k * 36), fill=(214, 214, 204))
    a = np.asarray(im).astype(np.float32) / 255
    yy, xx = np.mgrid[0:H, 0:W]
    n = np.asarray(Image.fromarray((rng.random((H // 8, W // 8)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) / 255
    torn = (n > 0.72) | ((xx % 173) < 14) & (n > 0.45)           # peeled strips show grey backing board
    a[torn] = a[torn] * 0.25 + np.array([0.33, 0.33, 0.32]) * 0.75
    runs = np.asarray(Image.fromarray((rng.random((8, W)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) / 255
    a *= (0.55 + 0.45 * runs)[..., None] * (0.75 + 0.25 * (1 - yy / H))[..., None]
    a = 0.6 * a + 0.4 * a.mean(-1, keepdims=True)                  # faded
    Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)).save(p)
    return p


def _curve(name, pts, radius, c, mat):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = radius; cu.bevel_resolution = 1
    sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts): sp.points[i].co = (p[0], p[1], p[2], 1)
    ob = bpy.data.objects.new(name, cu); c.objects.link(ob); ob.data.materials.append(mat); return ob


def _sag(a, b, sag, n=16):
    a, b = Vector(a), Vector(b)
    return [a.lerp(b, t) - Vector((0, 0, sag * 4 * t * (1 - t))) for t in np.linspace(0, 1, n)]


def pylon(name, base, h, c, mat, arms=(0.62, 0.78, 0.92), yaw=0.0):
    """lattice power pylon: 4 tapered legs + bracing + cross arms; returns attachment points of the arm tips."""
    verts, faces = [], []
    def bar(p0, p1, r):
        d = (p1 - p0); q = d.to_track_quat("Z", "Y"); b0 = len(verts)
        for z in (0, 1):
            for a in range(4):
                ang = a * math.pi / 2
                off = q @ Vector((r * math.cos(ang), r * math.sin(ang), 0))
                verts.append(tuple((p0 if z == 0 else p1) + off))
        for a in range(4):
            a2 = (a + 1) % 4; faces.append((b0 + a, b0 + a2, b0 + 4 + a2, b0 + 4 + a))
    R = Matrix.Rotation(yaw, 4, "Z")
    def leg(t, sx, sy):
        w = 7.0 * (1 - t) + 1.2 * t
        return base + R @ Vector((sx * w, sy * w, h * t))
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        bar(leg(0, sx, sy), leg(1, sx, sy), 0.35)
    ts = np.linspace(0, 1, 11)
    for i in range(10):
        for (sx0, sy0, sx1, sy1) in ((-1, -1, 1, -1), (1, -1, 1, 1), (1, 1, -1, 1), (-1, 1, -1, -1)):
            bar(leg(ts[i], sx0, sy0), leg(ts[i + 1], sx1, sy1), 0.15)
            bar(leg(ts[i], sx0, sy0), leg(ts[i], sx1, sy1), 0.15)
    tips = []
    for a in arms:
        span = 16.0 * (1.1 - a * 0.5)
        p0 = base + R @ Vector((-span, 0, h * a)); p1 = base + R @ Vector((span, 0, h * a))
        bar(p0, p1, 0.3)
        tips += [p0 - Vector((0, 0, 2.5)), p1 - Vector((0, 0, 2.5))]
    bar(base + Vector((0, 0, h)), base + Vector((0, 0, h + 6)), 0.25)
    kit.mesh_obj(name, verts, faces, c, mat=mat)
    return tips


def detail6(A, seed=11):
    rng = random.Random(seed)
    c = kit.coll("DETAIL_V6")
    dark = kit.m_simple("silhouette_steel", "#26282c", 0.6, 0.6)
    wire_m = kit.m_simple("wire_black", "#0c0c0e", 0.5)
    # 1) high-voltage line crossing the expressway at two places (top-third detail: wires and lattice silhouettes)
    for (s, h, yaw_off) in ((150.0, 70.0, 0.15), (330.0, 85.0, -0.1)):
        th = X.heading(s) + yaw_off
        right = Vector((math.cos(th), math.sin(th), 0))
        pa = X.P(s, 0, X.CITY_Z) - right * 95; pb = X.P(s, 0, X.CITY_Z) + right * 95
        ta = pylon(f"pylon_{int(s)}_a", pa, h, c, dark, yaw=th + math.pi / 2); tb = pylon(f"pylon_{int(s)}_b", pb, h, c, dark, yaw=th + math.pi / 2)
        # wires run across the deck (pylons stand beside it): connect matching arm tips
        for k in range(len(ta)):
            for j, (p, q) in enumerate(((ta[k], tb[k]),)):
                _curve(f"hv_{int(s)}_{k}", _sag(p, q, 9.0 + k * 0.4), 0.09, c, wire_m)
        _curve(f"hv_{int(s)}_earth", _sag(pa + Vector((0, 0, h + 6)), pb + Vector((0, 0, h + 6)), 7.0), 0.06, c, wire_m)
    # 2) telecom / CCTV poles on the outer barrier with drooping cable spans (near, mid-frame)
    pm = X.m_steel("steel_mast", "#6b6f74", 0.38)
    poles = []
    for s in np.arange(-30, 260, 32.0):
        p = X.P(s, -23.6, 1.6)
        kit.cyl(f"tpole_{int(s)}", 0.16, 11.0, c, 8, pm, loc=tuple(p + Vector((0, 0, 5.5))))
        arm = kit.box(f"tpole_arm_{int(s)}", (2.2, 0.15, 0.15), tuple(p + Vector((1.0, 0, 10.4))), c, pm)
        if int(s) % 64 == 2:
            kit.box(f"cctv_{int(s)}", (0.7, 0.35, 0.35), tuple(p + Vector((2.0, 0, 10.1))), c, kit.m_simple("cctv_white", "#cfd0cc", 0.5), bevel=0.06)
        poles.append(p + Vector((0, 0, 10.6)))
    for i in range(len(poles) - 1):
        for k, (dz, sag) in enumerate(((0.0, 1.4), (-0.4, 2.0), (-0.75, 1.1))):
            _curve(f"tcable_{i}_{k}", _sag(poles[i] + Vector((0, 0, dz)), poles[i + 1] + Vector((0, 0, dz)), sag, 10), 0.035, c, wire_m)
    # 3) second skyline layer, nearer (700-1500 D): dark-blue silhouettes with lit windows, antennas and roof boxes
    tm = X.m_towers()
    sil = kit.m_simple("roof_kit", "#0b0d14", 0.7)
    aviation = bpy.data.materials.get("aviation_red")
    crown = kit.m_emit("crown_led", "#8fb0ff", 3.0)
    for k in range(70):
        sdist = rng.uniform(900, 1700); off = rng.choice([-1, 1]) * rng.uniform(120, 900)
        base = X.P(min(sdist, 1350), 0, 0) + Vector((off, rng.uniform(-80, 80), 0))
        if min(math.hypot(base.x - px, base.y - py) for px, py in X._DECK_PTS) < 70: continue
        h = rng.uniform(35, 150) if rng.random() < 0.8 else rng.uniform(150, 260)
        w, d = rng.uniform(25, 70), rng.uniform(25, 60)
        ob = kit.box(f"tower2_{k}", (w, d, h), (base.x, base.y, X.CITY_Z + h / 2), c, tm, rot=(0, 0, rng.uniform(-0.4, 0.4)))
        ob.visible_shadow = False
        top = X.CITY_Z + h
        if rng.random() < 0.6:
            kit.box(f"roofbox_{k}", (w * 0.4, d * 0.4, 8), (base.x, base.y, top + 4), c, sil).visible_shadow = False
        if rng.random() < 0.55:
            ah = rng.uniform(12, 40)
            a = kit.cyl(f"antenna_{k}", 0.6, ah, c, 6, sil, loc=(base.x + w * 0.2, base.y, top + ah / 2)); a.visible_shadow = False
            if aviation:
                kit.box(f"antenna_av_{k}", (1.6, 1.6, 1.6), (base.x + w * 0.2, base.y, top + ah), c, aviation).visible_shadow = False
        if rng.random() < 0.18:
            kit.box(f"crown_{k}", (w * 1.01, d * 1.01, 2.0), (base.x, base.y, top - 3), c, crown, rot=ob.rotation_euler).visible_shadow = False
    # 4) a dead billboard on scaffolding beside the deck (s 120, left), three small lamps, one still on
    s0 = 150.0; th = X.heading(s0)
    bb_m = X.m_textured("billboard_poster", poster_tex(), rough=0.75, emit=0.12)
    grime(bb_m, 0.8, foot=-1, rough_add=0.1, scale=0.6)
    bp = X.P(s0, -88.0, 0)
    for dx in (-9, -3, 3, 9):
        kit.box(f"bb_leg_{dx}", (0.6, 0.6, 52), tuple(bp + Vector((dx, 0, X.CITY_Z + 26))), c, dark)
    for zz in range(-26, 22, 6):
        kit.box(f"bb_rung_{zz}", (20, 0.3, 0.3), tuple(bp + Vector((0, 0, zz))), c, dark)
    panel = kit.box("bb_panel", (22, 0.6, 9), tuple(bp + Vector((0, 0.6, 18))), c, bb_m)
    panel.rotation_euler = (0, 0, th + 0.35)
    for k, dx in enumerate((-7, 0, 7)):
        lm = kit.m_emit("bb_lamp_on", "#dfe8ff", 25.0) if k == 1 else kit.m_simple("bb_lamp_off", "#202226", 0.5)
        kit.box(f"bb_lamp_{k}", (1.4, 1.0, 0.5), tuple(bp + Vector((dx, -2.2, 13.0))), c, lm)
    L = bpy.data.lights.new("bb_spot", "SPOT"); L.energy = 6000; L.color = (0.85, 0.9, 1.0); L.spot_size = math.radians(70); L.shadow_soft_size = 0.3
    lo = bpy.data.objects.new("bb_spot", L); bpy.data.collections["LIGHTS"].objects.link(lo)
    lo.location = bp + Vector((0, -2.6, 12.6)); lo.rotation_euler = (math.radians(-60), 0, 0)
    # 5) ground scatter near the action: grit, gravel, leaves, cigarette butts, small glass (one mesh)
    verts, faces = [], []
    cols = []
    for _ in range(1400):
        sg = rng.uniform(14, 52); og = rng.uniform(-18, -1.5)
        p = X.P(sg, og, 0)
        e = rng.uniform(0.012, 0.05); rz = rng.uniform(0, 6.3); b = len(verts)
        for (dx, dy) in ((-1, -0.6), (1, -0.8), (0.7, 0.9), (-0.8, 0.7)):
            verts.append((p.x + e * (dx * math.cos(rz) - dy * math.sin(rz)), p.y + e * (dx * math.sin(rz) + dy * math.cos(rz)), 0.006 + rng.uniform(0, 0.01)))
        verts.append((p.x, p.y, 0.006 + e * 0.5))
        faces += [(b, b + 1, b + 4), (b + 1, b + 2, b + 4), (b + 2, b + 3, b + 4), (b + 3, b, b + 4)]
    kit.mesh_obj("scatter_grit", verts, faces, c, mat=kit.m_simple("grit_mix", "#5a5650", 0.7))
    for ob in c.objects:
        if ob.type in ("MESH", "CURVE") and ob.pass_index == 0: ob.pass_index = 4
