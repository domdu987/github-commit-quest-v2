"""beauty.py (v9) -- ref-D NIGHT finish over the v4 expressway: a clear blue moonlit night in rain.

Same API shape as v6/set/beauty.py:
    import sys; sys.path.insert(0, PROJ + "/v9/set")
    import beauty as B                      # puts v4/set_expressway on sys.path too
    A = B.build()                           # v4 build + v6 grime/detail + v9 world, lights, road, props
    B.setup_render("final", threads=4)
    cam = B.presets.use("eye", A)
    r = B.render6.render("/abs/out/eye", frame=7)        # B.render9 is the same module (post9)
New in v9: B.set_moon(azimuth_deg=None, elevation_deg=None, direction=None) turns the moon disc, its halo, the
cloud lighting and the moon key together (per-shot moon placement). See API.md.
"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
import beauty6 as B6                       # v6 beauty (copied, render6 -> render9); puts v4 on sys.path
import bpy
import numpy as np
from mathutils import Vector, Matrix

X = B6.X; kit = B6.kit; V = B6.V; tex = B6.tex
from kit import MB, hexlin
import presets
import render9
import render11
import finish11
render6 = render11          # v11: B.render6 / B.render9-style calls go through post11 (render9 stays importable)
render6 = render11                         # v6 name kept for shot scripts (v11: post11)
grime = B6.grime; hero_paint = B6.hero_paint; poster_tex = B6.poster_tex

MOON_DIR = Vector((-0.42, 0.85, 0.30)).normalized()
AMBIENT_STRENGTH = 0.10
SKY_FILL = finish11.P["sky_fill"]       # v11: darker surround (v9 0.65)
WET = dict(puddle_at=0.50, puddle_gain=10.0, damp_at=0.34, damp_rough=0.34, base_rough=0.50)   # v11: wetter deck (v9: 0.56 / 12 / 0.40 / 0.24 / 0.52)
SPP = dict(B6.SPP); SPP["final"] = 5      # v11: 5 spp (alpha-card cast + more lights; OIDN holds it)
ADAPTIVE = 0.07

# ---- tuning (linear, pre-exposure; post9 exposure ~1.5) ------------------------------------------------------
SKY = dict(
    zenith=(0.030, 0.058, 0.170),          # clear deep cornflower at the top
    mid=(0.052, 0.088, 0.215),
    horizon=(0.100, 0.145, 0.285),         # luminous horizon band (ref: sky brightest toward the horizon / moon)
    below=(0.010, 0.014, 0.030),
    cloud_dark=(0.022, 0.034, 0.085),      # rain-cloud bodies away from the moon
    cloud_lit=(0.11, 0.15, 0.30),          # silver edges toward the moon
    halo=(0.16, 0.22, 0.42), halo_core=(0.55, 0.62, 0.85), disc=(3.2, 3.35, 3.6))
MOON_GLOSSY = True
MOON_KEY = dict(energy=7.0, angle_deg=1.4, glint=1.3, glint_angle_deg=12.0, color=(0.66, 0.78, 1.0))


# ============================================================================================================ build
def build(seed=9, detail=True, scene=None):
    A = B6.X.build(seed=seed, haze_cards=False)
    scene = scene or bpy.context.scene
    world9(scene)
    lights9(A)
    materials9(A)
    if detail:
        B6.detail6(A)
        detail9(A)
    A["moon_dir"] = tuple(MOON_DIR)
    A["v9"] = True
    finish11.apply(A)                      # v11: reference-E finish (practicals, pools, cones)
    return A


def setup_render(quality="final", threads=4, scene=None):
    B6.setup_render(quality, threads=threads, scene=scene)
    cy = (scene or bpy.context.scene).cycles
    cy.sample_clamp_indirect = 2.5
    cy.blur_glossy = 0.5                   # crisper wet reflections (v6 0.7)
    cy.adaptive_threshold = ADAPTIVE       # 0.05 -> 0.07: -8 % CPU, no visible noise after OIDN
    cy.transparent_max_bounces = 8         # 14 -> 8 (smoke cards, rain beads, ink hulls): -5 % CPU


# ============================================================================================================ world
def world9(scene):
    """clear moonlit sky: deep cornflower zenith -> luminous blue horizon (hue 222-232, never lavender), broken rain
    clouds dark away from the moon with silver edges near it, a big soft moon (disc 1.8 deg, halo ~6 deg, faint
    15 deg bloom). Diffuse rays see the same sky (strong cool fill, as ref D night: key:fill ~2.5:1)."""
    w = bpy.data.worlds.get("W_night9") or bpy.data.worlds.new("W_night9")
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
        n = N.new("ShaderNodeValToRGB"); cr = n.color_ramp; cr.interpolation = "EASE"
        while len(cr.elements) > 1: cr.elements.remove(cr.elements[-1])
        for i, (p, col) in enumerate(stops):
            e = cr.elements[0] if i == 0 else cr.elements.new(p)
            e.position = p; e.color = tuple(col) + (1.0,) if len(col) == 3 else col
        L(fac, n.inputs[0]); return n.outputs[0]

    def mix(f, a, b, bt="MIX"):
        n = N.new("ShaderNodeMix"); n.data_type = "RGBA"; n.blend_type = bt
        for s, x in ((n.inputs[0], f), (n.inputs[6], a), (n.inputs[7], b)):
            if isinstance(x, (int, float)): s.default_value = x
            elif isinstance(x, tuple): s.default_value = x if len(x) == 4 else tuple(x) + (1.0,)
            else: L(x, s)
        return n.outputs[2]

    def dot_moon():
        dp = N.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"; dp.inputs[1].default_value = MOON_DIR
        dp.name = dp.label = "moon_dot"; L(tc.outputs["Generated"], dp.inputs[0]); return dp.outputs["Value"]

    z = M("ADD", M("MULTIPLY", sep.outputs["Z"], 0.5), 0.5)                       # 0.5 = horizon
    S = SKY
    grad = ramp(z, [(0.0, S["below"]), (0.46, S["below"]), (0.500, S["horizon"]), (0.56, S["mid"]),
                    (0.75, S["zenith"]), (1.0, S["zenith"])])
    dmo = dot_moon()
    # moon-side sky is lighter (ref T13: 0.52 at the top, 0.72 near the moon)
    side = M("POWER", M("MAXIMUM", dmo, 0.0), 6.0)
    col = mix(M("MULTIPLY", side, 0.55), grad, S["horizon"])
    # broken rain clouds: stretched noise, soft edges
    vm = N.new("ShaderNodeVectorMath"); vm.operation = "MULTIPLY"; vm.inputs[1].default_value = (1.0, 1.0, 3.6)
    L(tc.outputs["Generated"], vm.inputs[0])
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.6; nz.inputs["Detail"].default_value = 7.0
    nz.inputs["Roughness"].default_value = 0.58; L(vm.outputs[0], nz.inputs["Vector"])
    nz2 = N.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = 11.0; nz2.inputs["Detail"].default_value = 4.0
    L(vm.outputs[0], nz2.inputs["Vector"])
    f = M("ADD", nz.outputs["Fac"], M("MULTIPLY", M("SUBTRACT", nz2.outputs["Fac"], 0.5), 0.22))
    cl = M("MULTIPLY", M("SUBTRACT", f, 0.53), 5.0, True)                            # 0 clear .. 1 cloud
    above = M("MULTIPLY", M("SUBTRACT", z, 0.503), 25.0, True)
    cl = M("MULTIPLY", cl, above)
    near = M("POWER", M("MAXIMUM", dmo, 0.0), 10.0)
    body = mix(M("MULTIPLY", near, 0.6), S["cloud_dark"], S["mid"])                                      # bodies lighter near the moon
    col = mix(M("MULTIPLY", cl, 0.85), col, body)
    edge = M("MULTIPLY", M("MULTIPLY", cl, M("SUBTRACT", 1.0, cl)), 4.0)             # rims of the clouds
    rim = M("MULTIPLY", edge, M("ADD", 0.05, M("MULTIPLY", near, 1.2)))
    col = mix(M("MINIMUM", rim, 1.0), col, S["cloud_lit"])
    # moon: halo wide + core + disc (clouds veil the halo a little)
    veil = M("SUBTRACT", 1.0, M("MULTIPLY", cl, 0.45))
    h1 = M("POWER", M("MAXIMUM", dmo, 0.0), 40.0)
    h2 = M("POWER", M("MAXIMUM", dmo, 0.0), 260.0)
    h3 = M("POWER", M("MAXIMUM", dmo, 0.0), 1800.0)
    col = mix(M("MULTIPLY", M("MULTIPLY", h1, 0.35), veil), col, S["halo"], "ADD")
    col = mix(M("MULTIPLY", M("MULTIPLY", h2, 0.9), veil), col, S["halo"], "ADD")
    col = mix(M("MULTIPLY", h3, 1.0), col, S["halo_core"], "ADD")
    dsc = M("MULTIPLY", M("SUBTRACT", dmo, math.cos(math.radians(1.9))), 1.0 / (math.cos(math.radians(1.6)) - math.cos(math.radians(1.9))), True)
    # faint maria on the disc
    mn = N.new("ShaderNodeTexNoise"); mn.inputs["Scale"].default_value = 160.0; mn.inputs["Detail"].default_value = 2.0
    L(tc.outputs["Generated"], mn.inputs["Vector"])
    dcol = mix(M("MULTIPLY", M("SUBTRACT", mn.outputs["Fac"], 0.45), 1.2, True), S["disc"], tuple(c * 0.82 for c in S["disc"]))
    col = mix(dsc, col, dcol)
    L(col, bg.inputs["Color"])
    # diffuse rays see a cheap version (gradient + moon-side glow + halo): same light, no cloud noise evaluation
    # (Cycles skips the unused branch of a Mix Shader; measured -3 CPU s per frame)
    cheap = mix(M("MULTIPLY", side, 0.55), grad, S["horizon"])
    cheap = mix(M("MULTIPLY", h1, 0.35), cheap, S["halo"], "ADD")
    cheap = mix(M("MULTIPLY", h2, 0.9), cheap, S["halo"], "ADD")
    bg2 = N.new("ShaderNodeBackground"); L(cheap, bg2.inputs["Color"]); bg2.inputs["Strength"].default_value = SKY_FILL
    lp = N.new("ShaderNodeLightPath")
    ms = N.new("ShaderNodeMixShader"); L(lp.outputs["Is Diffuse Ray"], ms.inputs[0])
    L(bg.outputs[0], ms.inputs[1]); L(bg2.outputs[0], ms.inputs[2])
    L(ms.outputs[0], out.inputs["Surface"])
    w.cycles.sampling_method = "MANUAL"; w.cycles.sample_map_resolution = 512
    return w


def set_moon(azimuth_deg=None, elevation_deg=None, direction=None):
    """turn the moon (sky disc, halo, cloud lighting) and the moon key together. azimuth 0 = +Y (down the road),
    90 = -X (our left looking +Y). Returns the unit direction toward the moon."""
    global MOON_DIR
    if direction is None:
        az = math.radians(azimuth_deg if azimuth_deg is not None else math.degrees(math.atan2(-MOON_DIR.x, MOON_DIR.y)))
        el = math.radians(elevation_deg if elevation_deg is not None else math.degrees(math.asin(MOON_DIR.z)))
        direction = (-math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el))
    d = Vector(direction).normalized(); MOON_DIR = d
    w = bpy.context.scene.world
    for n in w.node_tree.nodes:
        if n.name.startswith("moon_dot"): n.inputs[1].default_value = d
    for nm in ("moon_key", "moon_glint"):
        k = bpy.data.objects.get(nm)
        if k: k.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    return tuple(d)


# =========================================================================================================== lights
def lights9(A):
    """moon key (crisp, 1.2 deg), sodium pools tighter and crisper, flood/headlights/beacons with small radii so
    they draw long, sharp cast shadows on the wet road; a warm halogen work lamp on a tripod behind the rescue
    (the ref campfire: a low warm practical whose shadows run toward the lens)."""
    sc = bpy.context.scene
    lc = bpy.data.collections.get("LIGHTS") or sc.collection
    ld = bpy.data.lights.new("moon_key", "SUN"); ld.energy = MOON_KEY["energy"]; ld.angle = math.radians(MOON_KEY["angle_deg"])
    ld.color = MOON_KEY["color"]
    ob = bpy.data.objects.new("moon_key", ld); lc.objects.link(ob)
    ob.rotation_euler = (-MOON_DIR).to_track_quat("-Z", "Y").to_euler()
    ob.visible_glossy = False
    if MOON_GLOSSY:                        # the moon glint path on the wet road (cars and people cut it with shadows):
        lg = bpy.data.lights.new("moon_glint", "SUN")       # a separate, weaker, wider glossy-only sun, so car glass
        lg.energy = MOON_KEY["glint"]; lg.angle = math.radians(MOON_KEY["glint_angle_deg"])  # does not blow out
        lg.color = MOON_KEY["color"]
        og = bpy.data.objects.new("moon_glint", lg); lc.objects.link(og)
        og.rotation_euler = ob.rotation_euler.copy()
        og.visible_diffuse = False; og.visible_transmission = False; og.visible_volume_scatter = False
        rc = bpy.data.collections.get("MOON_GLINT_RECEIVERS") or bpy.data.collections.new("MOON_GLINT_RECEIVERS")
        for nm in ("road_L", "road_R"):          # light linking: only the wet road takes the glint (not car glass)
            r = bpy.data.objects.get(nm)
            if r and r.name not in rc.objects: rc.objects.link(r)
        og.light_linking.receiver_collection = rc
    for Lt in bpy.data.lights:
        n = Lt.name
        if n.startswith("sodium_"):
            Lt.energy = 6500.0; Lt.color = (1.0, 0.60, 0.28); Lt.shadow_soft_size = 0.15; Lt.spot_size = math.radians(80); Lt.spot_blend = 0.35
        elif n.startswith("flood_key"):
            Lt.energy = 36000.0; Lt.shadow_soft_size = 0.08; Lt.color = (0.92, 0.96, 1.0)
        elif n.startswith("headlight_"):
            Lt.energy = 4200.0; Lt.shadow_soft_size = 0.04; Lt.color = (1.0, 0.94, 0.84)
        elif n.startswith("beacon_"):
            Lt.shadow_soft_size = 0.05
        elif n.startswith("hazard_"):
            Lt.shadow_soft_size = 0.05
    for m in bpy.data.materials:          # the v4 fake blue ambient: GI and the sky do the fill
        if not m.use_nodes or not m.node_tree: continue
        for nd in m.node_tree.nodes:
            if nd.type == "BSDF_PRINCIPLED" and nd.inputs["Emission Color"].is_linked and abs(nd.inputs["Emission Strength"].default_value - 1.0) < 1e-6:
                nd.inputs["Emission Strength"].default_value = AMBIENT_STRENGTH
        if m.name == "sodium_bulb":
            for nd in m.node_tree.nodes:
                if nd.type == "EMISSION": nd.inputs["Color"].default_value = (1.0, 0.68, 0.36, 1)
    work_lamp(A, lc)


WORK_LAMP = dict(base=(-3.5, 40.6, 0.0), head_z=2.25, aim=(-6.6, 31.5, 0.4), energy=6000.0, color=(1.0, 0.64, 0.34))


_WL = []          # objects of the current work lamp (rebuilt by place_work_lamp)


def work_lamp(A, lc, base=None, aim=None, energy=None, head_z=None, cable=True):
    """portable halogen work light on a tripod (rescue kit), default in lane 1 behind the action, aimed back at the
    hero car / Kong: warm pool, long crisp radial shadows of Kong, the crew, cones and debris toward the lens.
    place_work_lamp() moves it per shot (rebuilds the parts)."""
    c = kit.coll("DETAIL_V9")
    W = WORK_LAMP
    b = Vector(base or W["base"]); b.z = 0.0; head = b + Vector((0, 0, head_z or W["head_z"]))
    leg_m = kit.m_simple("tripod_black", "#1a1b1e", 0.45, 0.6)
    obs = []
    for k in range(3):
        a = k * 2 * math.pi / 3 + 0.3
        foot = b + Vector((math.cos(a) * 0.75, math.sin(a) * 0.75, 0.0))
        d = head - Vector((0, 0, 0.25)) - foot
        leg = kit.cyl(f"tripod_leg_{k}", 0.035, d.length, c, 6, leg_m, loc=tuple(foot + d / 2))
        leg.rotation_euler = d.to_track_quat("Z", "Y").to_euler(); obs.append(leg)
    obs.append(kit.cyl("tripod_mast", 0.045, 0.6, c, 8, leg_m, loc=tuple(head - Vector((0, 0, 0.3)))))
    aim = Vector(aim or W["aim"]); dv = (aim - head).normalized()
    hous = kit.box("worklamp_housing", (0.62, 0.30, 0.48), tuple(head), c, kit.m_simple("worklamp_yellow", "#c99a1c", 0.45, coat=0.3), bevel=0.04)
    hous.rotation_euler = dv.to_track_quat("Y", "Z").to_euler()
    lens = kit.box("worklamp_lens", (0.50, 0.03, 0.36), tuple(head + dv * 0.16), c, kit.m_emit("worklamp_glow", "#ffd9a8", 40.0))
    lens.rotation_euler = hous.rotation_euler
    lens.visible_shadow = False
    obs += [hous, lens]
    Lt = bpy.data.lights.new("work_lamp", "SPOT"); Lt.energy = energy or W["energy"]; Lt.color = W["color"]
    Lt.spot_size = math.radians(110); Lt.spot_blend = 0.6; Lt.shadow_soft_size = 0.06
    ob = bpy.data.objects.new("work_lamp", Lt); lc.objects.link(ob)
    ob.location = head + dv * 0.22
    ob.rotation_euler = dv.to_track_quat("-Z", "Y").to_euler()
    ob["kind"] = "practical"
    L2 = bpy.data.lights.new("work_lamp_spill", "POINT"); L2.energy = 60.0; L2.color = W["color"]; L2.shadow_soft_size = 0.2
    o2 = bpy.data.objects.new("work_lamp_spill", L2); lc.objects.link(o2); o2.location = head + Vector((0, 0, 0.35))
    obs += [ob, o2]
    if cable:
        cm = bpy.data.materials.get("cable") or kit.m_simple("cable", "#111112", 0.5)
        tg = Vector(A["tailgate"])
        pts = [b.lerp(tg, t) + Vector((math.sin(t * 9) * 0.6, 0, 0.03)) for t in np.linspace(0, 1, 14)]
        obs.append(B6._curve("worklamp_cable", pts, 0.03, c, cm))
    for o in obs:
        if o.type in ("MESH", "CURVE"): o.pass_index = 4
    _WL[:] = [o.name for o in obs]
    A["work_lamp"] = tuple(head)
    return head


def place_work_lamp(A, base=None, aim=None, energy=None, head_z=None, cable=None, hide=False):
    """move the work lamp for a shot: base (x, y) on the deck, aim a world point, energy W. base None = default spot
    (with its cable to the truck). hide=True switches it off and hides it."""
    for nm in list(_WL):
        o = bpy.data.objects.get(nm)
        if o is None: continue
        d = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if d is not None and d.users == 0:
            if isinstance(d, bpy.types.Light): bpy.data.lights.remove(d)
            elif isinstance(d, bpy.types.Mesh): bpy.data.meshes.remove(d)
            elif isinstance(d, bpy.types.Curve): bpy.data.curves.remove(d)
    lc = bpy.data.collections.get("LIGHTS") or bpy.context.scene.collection
    if base is not None and len(base) == 2: base = (base[0], base[1], 0.0)
    head = work_lamp(A, lc, base, aim, energy, head_z, cable if cable is not None else base is None)
    if hide:
        for nm in _WL: bpy.data.objects[nm].hide_render = True
    finish11.lamp_cone(A)                  # v11: the lamp's cone in the rain follows it
    return head


# ======================================================================================================== materials
def m_asphalt9():
    """wet asphalt v9: lighter dry aggregate (diffuse albedo ~0.05-0.07 so pools of light and cast shadows read),
    damp sheen (0.22), standing water mirror (0.02) ~45 %, rain ripples in water AND fine drop pits on damp asphalt
    (sparkle), crack network, patch repairs, skid marks, worn lane paint."""
    if "asphalt_v9" in bpy.data.materials: return bpy.data.materials["asphalt_v9"]
    mb = MB("asphalt_v9")
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
    wet = mb.math("ADD", mb.math("ADD", nz.outputs["Fac"], mb.math("MULTIPLY", rut, 0.12)), mb.math("ADD", mb.math("MULTIPLY", gut, 0.22), mb.math("MULTIPLY", nz2.outputs["Fac"], 0.12)))
    puddle = mb.math("MULTIPLY", mb.math("SUBTRACT", wet, WET["puddle_at"]), WET["puddle_gain"], True)
    damp = mb.math("MULTIPLY", mb.math("SUBTRACT", wet, WET["damp_at"]), 5.0, True)
    ag = mb.n("ShaderNodeTexNoise", Scale=34.0, Detail=3.0, Roughness=0.8); mb.l(vec, ag.inputs["Vector"])
    vo = mb.n("ShaderNodeTexVoronoi", Scale=14.0); mb.l(vec, vo.inputs["Vector"])
    grit = mb.math("LESS_THAN", vo.outputs["Distance"], 0.12)
    ck = mb.n("ShaderNodeTexVoronoi", Scale=0.65); ck.feature = "DISTANCE_TO_EDGE"
    wq = mb.n("ShaderNodeTexNoise", Scale=1.6, Detail=3.0); mb.l(vec, wq.inputs["Vector"])
    wv = mb.n("ShaderNodeVectorMath"); wv.operation = "ADD"; mb.l(vec, wv.inputs[0]); mb.l(wq.outputs["Color"], wv.inputs[1])
    mb.l(wv.outputs[0], ck.inputs["Vector"])
    cmask = mb.n("ShaderNodeTexNoise", Scale=0.3, Detail=2.0); mb.l(vec, cmask.inputs["Vector"])
    crack = mb.math("MULTIPLY", mb.math("LESS_THAN", ck.outputs["Distance"], 0.014), mb.math("GREATER_THAN", cmask.outputs["Fac"], 0.52))
    # fine hairline cracks (smaller cells)
    # patch repairs: rectangular-ish darker cells (manhattan voronoi)
    patchrep = mb.math("GREATER_THAN", nz2.outputs["Fac"], 0.66)                # darker resurfaced patches
    patch = mb.n("ShaderNodeTexNoise", Scale=0.16, Detail=3.0); mb.l(vec, patch.inputs["Vector"])
    base = mb.ramp(patch.outputs["Fac"], [(0.30, hexlin("#40414a")), (0.70, hexlin("#5a5b63"))])
    base = mb.mix(mb.math("MULTIPLY", ag.outputs["Fac"], 0.5), base, hexlin("#2a2b30"))
    base = mb.mix(mb.math("MULTIPLY", grit, 0.6), base, hexlin("#6a6b70"))
    base = mb.mix(mb.math("MULTIPLY", patchrep, 0.65), base, hexlin("#1e1f23"))
    base = mb.mix(mb.math("MULTIPLY", rut, 0.30), base, hexlin("#1c1d21"))
    base = mb.mix(mb.math("MULTIPLY", oil, 0.30), base, hexlin("#141418"))
    base = mb.mix(mb.math("MULTIPLY", crack, 0.85), base, hexlin("#0b0b0d"))

    def stripe(c, w):
        return mb.math("LESS_THAN", mb.math("ABSOLUTE", mb.math("SUBTRACT", ao, c)), w)
    dash = mb.math("LESS_THAN", mb.wrap(s, 15.0), 6.0)
    lw = mb.math("MULTIPLY", mb.math("MAXIMUM", stripe(6.55, 0.14), stripe(12.35, 0.14)), dash)
    wear = mb.n("ShaderNodeTexNoise", Scale=2.6, Detail=4.0, Roughness=0.72); mb.l(vec, wear.inputs["Vector"])
    keep = mb.math("GREATER_THAN", wear.outputs["Fac"], 0.42)
    white = mb.math("MULTIPLY", mb.math("MAXIMUM", lw, stripe(18.15, 0.17)), keep)
    yel = mb.math("MULTIPLY", stripe(1.25, 0.15), keep)
    col = mb.mix(white, base, hexlin("#c4c5c0"))
    col = mb.mix(yel, col, hexlin("#c49a22"))
    paint = mb.math("MAXIMUM", white, yel)
    col = mb.mix(mb.math("MULTIPLY", damp, 0.30), col, hexlin("#202126"))
    col = mb.mix(mb.math("MULTIPLY", puddle, 0.85), col, hexlin("#060709"))
    rough = mb.math("SUBTRACT", WET["base_rough"], mb.math("MULTIPLY", damp, WET["damp_rough"]))
    rough = mb.math("ADD", mb.math("MULTIPLY", rough, mb.math("SUBTRACT", 1.0, puddle)), mb.math("MULTIPLY", puddle, 0.02))
    rough = mb.math("ADD", rough, mb.math("MULTIPLY", paint, 0.12))
    rough = mb.math("SUBTRACT", rough, mb.math("MULTIPLY", crack, 0.15))
    # rain ripples in water (re-seeded per frame) + fine drop pits on damp asphalt (sparkle of point lights)
    rv = mb.n("ShaderNodeTexVoronoi", Scale=2.8); rv.voronoi_dimensions = "4D"
    mb.l(vec, rv.inputs["Vector"])
    fc = rv.inputs["W"].driver_add("default_value"); fc.driver.expression = "frame * 0.37"
    # one ring per drop cell at a random radius (random age): reads as rain rings, not a regular scale pattern
    rc = mb.n("ShaderNodeSeparateColor"); mb.l(rv.outputs["Color"], rc.inputs[0])
    age = rc.outputs[0]
    d0 = mb.math("ABSOLUTE", mb.math("SUBTRACT", rv.outputs["Distance"], mb.math("MULTIPLY", age, 0.32)))
    ring = mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", d0, 22.0), True)
    rip = mb.math("MULTIPLY", mb.math("MULTIPLY", ring, mb.math("SUBTRACT", 1.0, age)), puddle)
    bh = mb.math("ADD", mb.math("MULTIPLY", mb.math("ADD", ag.outputs["Fac"], mb.math("MULTIPLY", grit, 0.6)), mb.math("SUBTRACT", 1.0, puddle)),
                 mb.math("ADD", mb.math("MULTIPLY", rip, 0.10), mb.math("MULTIPLY", crack, -0.5)))
    nrm = kit.bump_node(mb, bh, 0.5, 0.012)
    b = mb.principled(col, rough, 0.0, 0.0, normal=nrm, spec=0.6)
    b.inputs["Emission Strength"].default_value = AMBIENT_STRENGTH * 0.5
    return mb.out(b)


def materials9(A):
    B6.materials6(A)
    road = m_asphalt9()
    for ob in bpy.data.objects:
        if ob.type != "MESH": continue
        for sl in ob.material_slots:
            if sl.material and sl.material.name in ("asphalt_v6", "asphalt_wet"): sl.material = road
    # glass shards: sparkle (sharper, brighter speculars)
    m = bpy.data.materials.get("glass_shard")
    if m:
        for nd in m.node_tree.nodes:
            if nd.type == "BSDF_PRINCIPLED":
                nd.inputs["Roughness"].default_value = 0.02; nd.inputs["Base Color"].default_value = (0.10, 0.13, 0.15, 1)


# =========================================================================================================== detail
def _blob_tree(name, base, h, crown_r, c, trunk_m, leaf_m, rng, kind="rain"):
    """low-poly Bangkok roadside tree: a rain tree (umbrella crown of 5-9 lumpy blobs) or a palm (fronds)."""
    obs = []
    tr = kit.cyl(name + "_trunk", 0.9 if kind == "rain" else 0.55, h, c, 7, trunk_m, loc=(base.x, base.y, base.z + h / 2))
    tr.rotation_euler = (rng.uniform(-0.06, 0.06), rng.uniform(-0.06, 0.06), 0); obs.append(tr)
    top = base + Vector((0, 0, h))
    if kind == "rain":
        import bmesh
        bm = bmesh.new()
        for k in range(rng.randint(14, 20)):
            a = rng.uniform(0, 2 * math.pi); rr = crown_r * math.sqrt(rng.random()) * 0.85
            p = top + Vector((math.cos(a) * rr, math.sin(a) * rr, rng.uniform(-1.0, 2.0) + (1 - rr / crown_r) * 2.0))
            rad = crown_r * rng.uniform(0.25, 0.42); sz = rng.uniform(0.6, 0.8)
            g = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
            for v in g["verts"]:
                v.co = Vector((v.co.x * rad, v.co.y * rad, v.co.z * rad * sz)) * (1.0 + rng.uniform(-0.22, 0.22)) + p
        me = bpy.data.meshes.new(name + "_crown"); bm.to_mesh(me); bm.free()
        for poly in me.polygons: poly.use_smooth = True
        ob = bpy.data.objects.new(name + "_crown", me); c.objects.link(ob); me.materials.append(leaf_m); obs.append(ob)
    else:
        for k in range(9):
            a = k * 2 * math.pi / 9 + rng.uniform(-0.2, 0.2)
            d = Vector((math.cos(a), math.sin(a), 0))
            pts = [top + d * (crown_r * t) + Vector((0, 0, 1.2 * math.sin(t * 2.2) * crown_r * 0.35 - t * t * crown_r * 0.35)) for t in np.linspace(0, 1, 6)]
            cu = B6._curve(f"{name}_f{k}", pts, 0.5, c, leaf_m); cu.data.bevel_resolution = 0
            obs.append(cu)
    return obs


def detail9(A, seed=21):
    """background and midground layers (ref D's tree lines / poles / wires), and foreground micro-props:
    1) roadside trees (rain trees + palms) whose crowns rise just above the deck on both sides -> dark silhouettes
       against the lighter sky, separated in depth;  2) uni-pole billboards (wordless, dim);  3) glass-shard and
       plastic-fragment scatter (sparkle) around the crash;  4) leaves/litter and tyre skid marks."""
    rng = random.Random(seed)
    c = kit.coll("DETAIL_V9")
    bl = bpy.data.lights.get("bb_spot")
    if bl: bl.energy = 1800.0                  # the v6 dead billboard: a dim silhouette, not a lit poster
    bp = bpy.data.objects.get("bb_panel")
    if bp: bp.data.materials[0] = kit.m_simple("bb_back_dark", "#15171c", 0.7)   # seen from its back: a dark slab
    trunk_m = kit.m_simple("tree_trunk", "#1d1a18", 0.8)
    leaf_m = kit.m_simple("tree_leaf_night", "#0f1813", 0.8)
    n = 0
    for side in (-1, 1):
        s = -80.0 + rng.uniform(0, 10)
        while s < 520:
            o = side * rng.uniform(32, 75)
            p = X.P(s, o, X.CITY_Z)
            if min(math.hypot(p.x - px, p.y - py) for px, py in X._DECK_PTS) > 28:
                kind = "palm" if rng.random() < 0.3 else "rain"
                h = rng.uniform(26, 40) if kind == "rain" else rng.uniform(34, 46)
                _blob_tree(f"tree_{n}", p, h, rng.uniform(7, 12) if kind == "rain" else rng.uniform(5, 7), c, trunk_m, leaf_m, rng, kind)
                n += 1
            s += rng.uniform(9, 22)
    # uni-pole billboards: a few lit, most dark
    bbm = X.m_textured("billboard_poster9", poster_tex(), rough=0.7, emit=0.25)
    dark = kit.m_simple("silhouette_steel", "#26282c", 0.6, 0.6)
    for k, (s, o, rot) in enumerate(((70, -48, 0.5), (210, 52, -0.6), (330, -60, 0.35), (460, 70, -0.4))):
        p = X.P(s, o, X.CITY_Z)
        kit.cyl(f"unipole_{k}", 1.4, 55, c, 10, dark, loc=(p.x, p.y, X.CITY_Z + 27.5))
        pan = kit.box(f"unipole_panel_{k}", (26, 0.8, 9), (p.x, p.y, X.CITY_Z + 58), c, bbm if k == 3 else dark)   # dark silhouettes
        pan.rotation_euler = (0, 0, X.heading(s) + rot)
        kit.box(f"unipole_frame_{k}", (26.6, 1.2, 0.5), (p.x, p.y, X.CITY_Z + 53.2), c, dark, rot=(0, 0, X.heading(s) + rot))
    # skyline behind the start of the deck (-s): dark towers with lit windows, for reverse angles (S18, S20)
    tm = X.m_towers(); sil = kit.m_simple("roof_kit", "#0b0d14", 0.7)
    for k in range(44):
        base = Vector((rng.choice([-1, 1]) * rng.uniform(80, 1100), rng.uniform(-2600, -1100), 0))   # the path is straight (x = o, y = s) here
        h = rng.uniform(40, 170) if rng.random() < 0.8 else rng.uniform(170, 300)
        w, d = rng.uniform(25, 70), rng.uniform(25, 60)
        ob = kit.box(f"tower_back_{k}", (w, d, h), (base.x, base.y, X.CITY_Z + h / 2), c, tm, rot=(0, 0, rng.uniform(-0.4, 0.4)))
        ob.visible_shadow = False
        if rng.random() < 0.5:
            ah = rng.uniform(10, 35)
            kit.cyl(f"tower_back_ant_{k}", 0.6, ah, c, 6, sil, loc=(base.x, base.y, X.CITY_Z + h + ah / 2)).visible_shadow = False
    # glass shards + plastic fragments around the crash (s 20-50), denser near the car
    verts, faces = [], []; pv, pf = [], []
    cx, cy = A["door_mid"][0], A["door_mid"][1]
    for _ in range(1300):
        if rng.random() < 0.55:
            r = abs(rng.gauss(0, 3.0)); a = rng.uniform(0, 2 * math.pi); x, y = cx + r * math.cos(a), cy + r * math.sin(a) - 1.0
        else:
            x, y = rng.uniform(-17, -1.5), rng.uniform(18, 52)
        e = rng.uniform(0.012, 0.04); rz = rng.uniform(0, 6.3)
        tgt = (verts, faces) if rng.random() < 0.94 else (pv, pf)
        vv, ff = tgt; b = len(vv)
        for (dx, dy) in ((-1, -0.5), (1, -0.7), (rng.uniform(-0.4, 0.6), 1.0)):
            vv.append((x + e * (dx * math.cos(rz) - dy * math.sin(rz)), y + e * (dx * math.sin(rz) + dy * math.cos(rz)), 0.004 + rng.uniform(0, 0.012)))
        ff.append((b, b + 1, b + 2))
    gm = bpy.data.materials.get("glass_shard")
    kit.mesh_obj("scatter_glass9", verts, faces, c, mat=gm)
    kit.mesh_obj("scatter_plastic9", pv, pf, c, mat=kit.m_simple("plastic_frag", "#7a4a3a", 0.4, coat=0.3))
    # leaves and litter: flat dark quads along the gutters and in the lanes
    lv, lf = [], []
    for _ in range(180):
        o = rng.choice([rng.uniform(-22.0, -19.5), rng.uniform(-2.2, -0.9), rng.uniform(-19, -2)])
        p = X.P(rng.uniform(5, 70), o, 0.006)
        e = rng.uniform(0.04, 0.10); rz = rng.uniform(0, 6.3); b = len(lv)
        for (dx, dy) in ((-1, -0.45), (1, -0.45), (1, 0.45), (-1, 0.45)):
            lv.append((p.x + e * (dx * math.cos(rz) - dy * math.sin(rz)), p.y + e * (dx * math.sin(rz) + dy * math.cos(rz)), 0.006 + rng.uniform(0, 0.004)))
        lf.append((b, b + 1, b + 2, b + 3))
    kit.mesh_obj("scatter_leaves9", lv, lf, c, mat=kit.m_simple("leaf_wet", "#141309", 0.6))
    # skid marks behind the hero car: two dark rubber arcs (decal strips just above the road)
    sk = MB("skid_rubber"); a_ = sk.n("ShaderNodeTexNoise", Scale=8.0, Detail=4.0)
    sk.out(sk.principled((0.012, 0.012, 0.013, 1), 0.45, ambient=None, alpha=sk.math("MULTIPLY", a_.outputs["Fac"], 1.2, True)))
    hx, hy = -9.6, 34.0
    for side in (-0.9, 0.9):
        pts = []
        for t in np.linspace(0, 1, 30):
            y = hy - 3.0 - t * 16.0; x = hx + side + math.sin(t * 2.0) * 1.6 * t
            pts.append((x, y))
        sv, sf = [], []
        for i, (x, y) in enumerate(pts):
            sv += [(x - 0.16, y, 0.009), (x + 0.16, y, 0.009)]
            if i: sf.append((2 * i - 2, 2 * i - 1, 2 * i + 1, 2 * i))
        kit.mesh_obj(f"skid_{side}", sv, sf, c, mat=sk.m).visible_shadow = False
    for ob in c.objects:
        if ob.type in ("MESH", "CURVE") and ob.pass_index == 0: ob.pass_index = 4
        if ob.name.startswith(("tree_", "unipole_")): ob.pass_index = 4
    bevel_pass(A)


def bevel_pass(A, radius=30.0):
    """clean bevels on the small hard-edged set props near the action (cases, boxes, debris, barriers, crates):
    a 2-segment Bevel modifier, angle-limited, width ~3 % of the prop's size (max 0.035 D)."""
    act = Vector(A["kong_mark"]); n = 0
    skip = ("road", "barrier_", "median", "slab", "scatter", "tree_", "tower", "pier", "block", "city", "glass_piles",
            "decal", "skid", "pool", "joint", "drains", "rail", "wbeam", "sign_", "led_", "fg_", "worklamp_lens")
    for ob in list(bpy.data.objects):
        if ob.type != "MESH" or ob.name.startswith(skip) or ob.data.users > 1: continue
        if len(ob.data.vertices) > 400 or any(m.type == "BEVEL" for m in ob.modifiers): continue
        dim = max(ob.dimensions)
        if dim > 4.0 or dim < 0.08: continue
        if (ob.matrix_world.translation - act).length > radius: continue
        md = ob.modifiers.new("v9_bevel", "BEVEL"); md.width = min(0.035, 0.03 * dim); md.segments = 2
        md.limit_method = "ANGLE"; md.angle_limit = math.radians(35); md.use_clamp_overlap = True
        n += 1
    A["bevelled"] = n
    return n


# ============================================================================================================ v11
glare_check = finish11.glare_check
place_work_lamp_safe = finish11.place_work_lamp_safe
pov_windscreen = finish11.pov_windscreen
add_cone = finish11.add_cone
practical = finish11.practical
