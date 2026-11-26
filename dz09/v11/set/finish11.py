"""finish11.py -- the reference-E finish laid over the v9 expressway (spec/refE_look.md).

apply(A) is called by beauty.build(). It keeps the Bangkok expressway, the night and the rain, and changes the light
design to reference E's: a darker, saturated blue surround; rich practicals that each throw a coloured pool
(red / blue beacons, amber hazards, sodium, a lit green exit sign, glowing billboards and city windows, the warm
work lamp); light cones for the post shaft pass; glare guard; dressing for the POV-through-windscreen shot.

Public:
    apply(A)                                   all of the below, once per build
    add_cone(name, loc, aim, length, r0, r1, col)       a post light cone (rain shaft) for any light
    lamp_cone(A)                               (re)attach the work-lamp cone after place_work_lamp
    glare_check(cam, heads, min_frac=0.16)     -> [(emitter name, head index, distance / frame width)]
    place_work_lamp_safe(A, cam, heads, base, aim, ...)  place_work_lamp + slide the lamp off every head
    pov_windscreen(A, on=True)                 bonnet dressing + cabin practicals for the S18 POV
    practical(name, gain)                      per-shot gain on one of the v11 practicals
"""
import os, math, random
import bpy
import numpy as np
from mathutils import Vector

import beauty6 as B6
X = B6.X; kit = B6.kit
HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")

# tunables (reference-E targets: lit pools V 0.75-0.9 against a V 0.2-0.3, S 0.6-0.7 blue surround)
P = dict(
    sky_camera=0.60, lamp_lens=12.0,                   # sky seen by the camera x (v9 1.0); work-lamp lens emission (v9 40)
    moon_key=3.6, moon_glint=1.0, sky_fill=0.42,       # darker surround (v9: 7.0 / 1.3 / 0.65)
    sodium=7500.0, sodium_color=(1.0, 0.56, 0.22),
    flood=20000.0,                                     # the cool flood no longer flattens the scene (v9 36 kW)
    beacon_gain=dict(red=2.2, blue=4.0),               # on the truck's own point lights
    beacon_throw=dict(red=9.0, blue=16.0),             # spot at the light bar aimed at the action: energy = k x beacon
    hazard_gain=5.0,
    tail_gain=1.6,
    windows=2.6,                                       # skyline window emission x
    sign_emit=2.6, sign_pool=16000.0,
    exit_emit=3.2, exit_pool=900.0,
    billboard_emit=(3.0, 2.4, 2.8), dead_billboard_emit=0.9, bb_spot=5200.0,
    shaft=dict(work=0.050, head=0.040, beacon=0.030, sign=0.030),
)
_E0 = {}


# ------------------------------------------------------------------------------------------------------ helpers
def _scale_anim(idb, k, path=None):
    """scale every keyed value of idb's fcurves (and nothing else) by k."""
    for fc in kit.fcurves_of(idb):
        if path and fc.data_path != path: continue
        for kp in fc.keyframe_points:
            kp.co.y *= k; kp.handle_left.y *= k; kp.handle_right.y *= k
        fc.update()


def _follow(light, src_light, k):
    """light.energy = k x src_light.energy (driver), so a throw spot flashes with its beacon."""
    light.energy = src_light.energy * k
    fc = light.driver_add("energy")
    d = fc.driver; d.type = "SCRIPTED"
    v = d.variables.new(); v.name = "e"; v.type = "SINGLE_PROP"
    v.targets[0].id_type = "LIGHT"; v.targets[0].id = src_light; v.targets[0].data_path = "energy"
    d.expression = f"e * {k}"


def add_cone(name, loc, aim, length, r0, r1, col):
    """a light cone for the post shaft pass (v4 shafts.py): an Empty at the lamp whose local -Z runs down the beam.
    col = rgb x strength (sodium cones use 0.066 x colour)."""
    ob = bpy.data.objects.get(name)
    if ob is None:
        ob = bpy.data.objects.new(name, None)
        (bpy.data.collections.get("LIGHTS") or bpy.context.scene.collection).objects.link(ob)
    loc = Vector(loc); aim = Vector(aim)
    ob.location = loc
    ob.rotation_euler = (aim - loc).to_track_quat("-Z", "Y").to_euler()
    ob["fx"] = "cone"; ob["shaft_len"] = float(length); ob["shaft_r0"] = float(r0); ob["shaft_r1"] = float(r1)
    ob["shaft_col"] = tuple(float(c) for c in col)
    ob.hide_render = False
    return ob


def practical(name, gain):
    """per-shot gain on a light (set value x gain); gain 1 restores."""
    ob = bpy.data.objects.get(name)
    if ob is None or ob.type != "LIGHT": return
    if name not in _E0: _E0[name] = ob.data.energy
    ob.data.energy = _E0[name] * gain


# ---------------------------------------------------------------------------------------------------- textures
def _font(size):
    from PIL import ImageFont
    try: return ImageFont.truetype(FONT, size)
    except Exception: return ImageFont.load_default()


def exit_sign_tex():
    """green Thai expressway exit sign, drawn by code: white border, 'ทางออก / EXIT', a big 9, an arrow."""
    p = os.path.join(TEX, "exit_sign_v11.png")
    if os.path.exists(p): return p
    from PIL import Image, ImageDraw
    W, H = 1024, 640
    im = Image.new("RGB", (W, H), (6, 122, 62)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 14, W - 14, H - 14), 46, outline=(244, 248, 244), width=16)
    d.text((70, 60), "ทางออก", fill=(246, 250, 246), font=_font(170))
    d.text((74, 300), "EXIT", fill=(246, 250, 246), font=_font(150))
    d.rounded_rectangle((640, 70, 930, 330), 30, fill=(250, 206, 30))
    d.text((725, 60), "9", fill=(16, 18, 16), font=_font(250))
    d.polygon([(560, 560), (760, 400), (760, 470), (950, 470), (950, 540), (760, 540), (760, 600)][::-1], fill=(246, 250, 246))
    d.polygon([(950, 440), (990, 505), (950, 570)], fill=(246, 250, 246))
    d.text((74, 480), "ดินแดง", fill=(246, 250, 246), font=_font(92))
    os.makedirs(TEX, exist_ok=True); im.save(p)
    return p


def poster_tex(k):
    """wordless glowing billboard art (code-drawn colour fields; no brands, no text): 0 magenta sunset, 1 cyan
    drink-can shapes, 2 amber grid."""
    p = os.path.join(TEX, f"poster_v11_{k}.png")
    if os.path.exists(p): return p
    from PIL import Image, ImageDraw
    W, H = 1040, 360
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    if k == 0:
        t = yy / H
        a = np.stack([255 * (0.95 - 0.25 * t), 60 + 60 * t, 150 + 80 * (1 - t)], -1)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
        d.ellipse((380, 60, 660, 340), fill=(255, 214, 120))
        for i in range(5): d.rectangle((0, 250 + i * 24, W, 258 + i * 24), fill=(120, 30, 110))
        d.polygon([(0, H), (0, 280), (160, 200), (300, 290), (420, H)], fill=(60, 14, 70))
    elif k == 1:
        t = xx / W
        a = np.stack([20 + 30 * t, 170 + 60 * (1 - t), 230 - 20 * t], -1)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
        for i, c in enumerate([(250, 250, 250), (255, 90, 150), (255, 220, 60)]):
            x = 180 + i * 270
            d.rounded_rectangle((x, 50, x + 150, 320), 34, fill=c)
            d.ellipse((x + 30, 130, x + 120, 220), fill=(20, 80, 160))
        d.rectangle((0, 0, W, 16), fill=(250, 250, 250)); d.rectangle((0, H - 16, W, H), fill=(250, 250, 250))
    else:
        im = Image.new("RGB", (W, H), (250, 150, 30)); d = ImageDraw.Draw(im)
        for i in range(9):
            for j in range(3):
                c = (255, 226, 120) if (i + j) % 2 else (210, 70, 20)
                d.rounded_rectangle((30 + i * 112, 28 + j * 106, 122 + i * 112, 112 + j * 106), 14, fill=c)
        d.ellipse((420, 60, 660, 300), fill=(255, 250, 230))
    im.save(p)
    return p


# ------------------------------------------------------------------------------------------------------- lights
def lights11(A):
    lc = bpy.data.collections.get("LIGHTS") or bpy.context.scene.collection
    mk = bpy.data.lights.get("moon_key"); mg = bpy.data.lights.get("moon_glint")
    if mk: mk.energy = P["moon_key"]
    if mg: mg.energy = P["moon_glint"]
    for Lt in bpy.data.lights:
        n = Lt.name
        if n.startswith("sodium_"):
            Lt.energy = P["sodium"]; Lt.color = P["sodium_color"]; Lt.shadow_soft_size = 0.10; Lt.spot_blend = 0.28
        elif n.startswith("flood_key"):
            Lt.energy = P["flood"]
        elif n.startswith("beacon_"):
            colr = "red" if "red" in n else "blue"
            Lt.color = (1.0, 0.04, 0.03) if colr == "red" else (0.06, 0.20, 1.0)
            _scale_anim(Lt, P["beacon_gain"][colr], "energy"); Lt.energy *= P["beacon_gain"][colr]
        elif n.startswith("hazard_"):
            Lt.color = (1.0, 0.50, 0.08)
            _scale_anim(Lt, P["hazard_gain"], "energy"); Lt.energy *= P["hazard_gain"]
    # beacon throws: one red and one blue spot at the light bar, aimed over the rescue zone; they flash with the domes
    tgt = Vector(A["kong_mark"]) + Vector((1.5, -2.0, 0.0))
    for colr in ("red", "blue"):
        src = [o for o in bpy.data.objects if o.type == "LIGHT" and o.name.startswith(f"beacon_{colr}_")]
        if not src: continue
        s0 = src[0]
        Lt = bpy.data.lights.new(f"beacon_throw_{colr}", "SPOT"); Lt.color = s0.data.color
        Lt.spot_size = math.radians(62); Lt.spot_blend = 0.55; Lt.shadow_soft_size = 0.07
        ob = bpy.data.objects.new(f"beacon_throw_{colr}", Lt); lc.objects.link(ob)
        loc = s0.matrix_world.translation + Vector((0, 0, 0.25)); ob.location = loc
        side = Vector((-1.6, 0, 0)) if colr == "red" else Vector((4.2, 2.0, 0))
        aim = tgt + side
        ob.rotation_euler = (aim - loc).to_track_quat("-Z", "Y").to_euler()
        ob["kind"] = f"beacon_{colr}"
        _follow(Lt, s0.data, P["beacon_throw"][colr])
        c = [x * P["shaft"]["beacon"] for x in Lt.color]
        add_cone(f"cone_beacon_{colr}", loc, aim, (aim - loc).length * 0.8, 0.25, 4.5, c)
    # headlight cones (the v4 headlights had no post cone)
    for ob in list(bpy.data.objects):
        if ob.type == "LIGHT" and ob.name.startswith("headlight_"):
            ax = ob.matrix_world.to_3x3() @ Vector((0, 0, -1)); loc = ob.matrix_world.translation.copy()
            add_cone("cone_" + ob.name, loc, loc + ax * 13.0, 13.0, 0.18, 2.6, [x * P["shaft"]["head"] for x in ob.data.color])
    # tail lamps: a little hotter so every car draws a red streak on the wet road
    for nm in ("tail_lamp",):
        m = bpy.data.materials.get(nm)
        if m and m.node_tree:
            for nd in m.node_tree.nodes:
                if nd.type == "EMISSION": nd.inputs["Strength"].default_value *= P["tail_gain"]
    lamp_cone(A)


def lamp_cone(A):
    """the work lamp's cone in the rain (call again after place_work_lamp; beauty.place_work_lamp does)."""
    ob = bpy.data.objects.get("work_lamp")
    old = bpy.data.objects.get("cone_work_lamp")
    if ob is None or ob.hide_render:
        if old: old.hide_render = True
        return
    bpy.context.view_layer.update()
    ax = ob.matrix_world.to_3x3() @ Vector((0, 0, -1)); loc = ob.matrix_world.translation.copy()
    k = min(1.0, ob.data.energy / 6000.0)
    add_cone("cone_work_lamp", loc, loc + ax * 8.0, 8.0, 0.25, 4.0, [x * P["shaft"]["work"] * k for x in ob.data.color])


# ---------------------------------------------------------------------------------------------- glowing practicals
def _boost_emission(m, k=None, to=None):
    if m is None or not m.node_tree: return
    for nd in m.node_tree.nodes:
        if nd.type == "BSDF_PRINCIPLED":
            s = nd.inputs["Emission Strength"]
            s.default_value = to if to is not None else s.default_value * k
        elif nd.type == "EMISSION" and not nd.inputs["Strength"].is_linked:
            s = nd.inputs["Strength"]; s.default_value = to if to is not None else s.default_value * k


def practicals11(A):
    c = kit.coll("DETAIL_V11")
    lc = bpy.data.collections.get("LIGHTS") or bpy.context.scene.collection
    # 1) skyline windows: x P["windows"] (a Math node in front of the emission strength)
    m = bpy.data.materials.get("towers")
    if m:
        nt = m.node_tree
        for nd in nt.nodes:
            if nd.type == "EMISSION" and nd.inputs["Strength"].is_linked:
                src = nd.inputs["Strength"].links[0].from_socket
                mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = P["windows"]
                nt.links.new(src, mul.inputs[0]); nt.links.new(mul.outputs[0], nd.inputs["Strength"])
    # 2) the gantry signs glow green and pour a green pool on the deck below them
    for key in ("sign_dindaeng", "sign_rama9"):
        _boost_emission(bpy.data.materials.get(key), to=P["sign_emit"])
        q = bpy.data.objects.get(key)
        if q is None: continue
        bpy.context.view_layer.update()
        p = q.matrix_world.translation
        Lt = bpy.data.lights.new(f"{key}_pool", "SPOT"); Lt.color = (0.20, 1.0, 0.50); Lt.energy = P["sign_pool"]
        Lt.spot_size = math.radians(95); Lt.spot_blend = 0.6; Lt.shadow_soft_size = 0.4
        ob = bpy.data.objects.new(f"{key}_pool", Lt); lc.objects.link(ob)
        ob.location = (p.x, p.y - 1.5, p.z - 1.0)
        aim = Vector((p.x, p.y - 9.0, 0.0))
        ob.rotation_euler = (aim - ob.location).to_track_quat("-Z", "Y").to_euler()
        add_cone(f"cone_{key}", ob.location, aim, 15.0, 2.5, 7.0, [x * P["shaft"]["sign"] for x in Lt.color])
    # 3) a lit green exit sign on a post at the left barrier, just past the rescue zone: the mid-ground green practical
    s_exit, o_exit = 53.0, -21.2
    base = X.P(s_exit, o_exit, 0.0); th = X.heading(s_exit)
    steel = bpy.data.materials.get("steel_galv") or kit.m_simple("steel_exit", "#70757c", 0.4, 0.6)
    for dx in (-1.9, 1.9):
        kit.cyl(f"exit_post_{dx:+.0f}", 0.13, 7.6, c, 8, steel, loc=tuple(X.P(s_exit, o_exit + dx, 3.8)))
    sm = X.m_textured("sign_exit_v11", exit_sign_tex(), rough=0.45, emit=P["exit_emit"])
    q = kit.quad("exit_sign", 5.6, 3.5, X.P(s_exit - 0.2, o_exit, 6.2), "-Y", c, sm); q.rotation_euler = (0, 0, th)
    bk = kit.box("exit_sign_back", (5.7, 0.12, 3.6), tuple(X.P(s_exit, o_exit, 6.2)), c,
                 bpy.data.materials.get("bb_back_dark") or kit.m_simple("exit_back", "#15171a", 0.6), rot=(0, 0, th))
    Lt = bpy.data.lights.new("exit_pool", "SPOT"); Lt.color = (0.16, 1.0, 0.46); Lt.energy = P["exit_pool"]
    Lt.spot_size = math.radians(120); Lt.spot_blend = 0.7; Lt.shadow_soft_size = 0.5
    ob = bpy.data.objects.new("exit_pool", Lt); lc.objects.link(ob)
    ob.location = X.P(s_exit - 1.2, o_exit, 5.6)
    aim = X.P(s_exit - 6.0, o_exit + 4.0, 0.0)
    ob.rotation_euler = (aim - ob.location).to_track_quat("-Z", "Y").to_euler()
    A["exit_sign"] = tuple(X.P(s_exit, o_exit, 6.2))
    # 4) billboards: three of the four uni-poles are lit posters (wordless), the fourth stays a dark silhouette
    for k in range(3):
        pan = bpy.data.objects.get(f"unipole_panel_{k}")
        if pan is None: continue
        bm = X.m_textured(f"billboard_v11_{k}", poster_tex(k), rough=0.6, emit=P["billboard_emit"][k])
        pan.data.materials.clear(); pan.data.materials.append(bm)
    _boost_emission(bpy.data.materials.get("billboard_poster"), to=P["dead_billboard_emit"])
    bl = bpy.data.lights.get("bb_spot")
    if bl: bl.energy = P["bb_spot"]
    for ob in bpy.data.objects:
        if ob.name.startswith(("exit_", "unipole_panel")) and ob.type == "MESH": ob.pass_index = 4


# --------------------------------------------------------------------------------------------------- glare guard
def _emitters():
    """(name, world point, weight): lamps whose lens is a hot disc when seen by the camera."""
    out = []
    wl = bpy.data.objects.get("worklamp_lens")
    if wl and not wl.hide_render: out.append(("work_lamp", wl.matrix_world.translation.copy(), 1.0))
    for ob in bpy.data.objects:
        if ob.hide_render: continue
        if ob.name.startswith("rescue_truck_floodface"): out.append(("flood", ob.matrix_world.translation.copy(), 1.0))
        elif ob.type == "LIGHT" and ob.name.startswith("headlight_"): out.append((ob.name, ob.matrix_world.translation.copy(), 0.8))
    return out


def glare_check(cam, heads, min_frac=0.16, scene=None):
    """heads: world points (head centres). Returns [(emitter, head index, screen distance / frame width)] for every
    hot lamp that the camera sees closer than min_frac of the frame width to a head (the lamp must be BEHIND the head
    or within 3 D in front of it to count)."""
    from bpy_extras.object_utils import world_to_camera_view as w2c
    scene = scene or bpy.context.scene
    W, H = scene.render.resolution_x, scene.render.resolution_y
    bad = []
    for nm, p, w in _emitters():
        v = w2c(scene, cam, p)
        if v.z <= 0 or not (-0.1 < v.x < 1.1 and -0.1 < v.y < 1.1): continue
        for i, h in enumerate(heads):
            hv = w2c(scene, cam, Vector(h))
            if hv.z <= 0: continue
            d = math.hypot((v.x - hv.x) * W, (v.y - hv.y) * H) / W
            if d < min_frac * w: bad.append((nm, i, round(d, 3)))
    return bad


def place_work_lamp_safe(A, cam, heads, base, aim, energy=None, head_z=None, cable=None, min_frac=0.16, step=0.6, tries=14):
    """place_work_lamp, then slide the lamp sideways (camera right or left, whichever clears first) until its lens is
    at least min_frac of the frame width away from every head on screen. Returns (head position, moved distance)."""
    import beauty as B
    base = Vector((base[0], base[1], 0.0))
    right = cam.matrix_world.to_3x3() @ Vector((1, 0, 0)); right.z = 0; right.normalize()
    best = None
    for k in range(tries + 1):
        for sg in ((1, -1) if k else (1,)):
            b = base + right * (sg * k * step)
            B.place_work_lamp(A, base=(b.x, b.y), aim=aim, energy=energy, head_z=head_z, cable=cable)
            bpy.context.view_layer.update()
            bad = [x for x in glare_check(cam, heads, min_frac) if x[0] == "work_lamp"]
            if not bad:
                return A["work_lamp"], sg * k * step
            if best is None: best = b
    return A["work_lamp"], None


# ------------------------------------------------------------------------------------------- POV through windscreen
_POV = []


def pov_windscreen(A, on=True, seed=5):
    """dressing for the POV from the bonnet through the cracked windscreen (S18): the bonnet stops being one flat
    plane (wet leaves, glass crumbs, a buckled crease with a lifted edge, standing-water streaks that mirror the
    practicals) and the cabin gets two motivated practicals (a warm dome light, a teal dashboard glow) so the driver
    reads. on=False removes it."""
    for nm in list(_POV):
        o = bpy.data.objects.get(nm)
        if o:
            d = o.data; bpy.data.objects.remove(o, do_unlink=True)
            if isinstance(d, bpy.types.Light) and d.users == 0: bpy.data.lights.remove(d)
    _POV.clear()
    if not on: return
    rng = random.Random(seed)
    c = kit.coll("DETAIL_V11")
    th = A["hero_heading"]
    fwd = Vector((-math.sin(th), math.cos(th), 0.0)); right = Vector((math.cos(th), math.sin(th), 0.0))
    ws = Vector(A["windscreen"]); hd = Vector(A["driver_head"])
    dg = bpy.context.evaluated_depsgraph_get()

    def top(p):                                 # the bonnet surface under a point (ray from above)
        ok, hit, nrm, _, ob, _ = bpy.context.scene.ray_cast(dg, Vector((p.x, p.y, 4.0)), Vector((0, 0, -1)), distance=4.0)
        return hit.z if ok else 1.5
    b0 = Vector((ws.x, ws.y, 0.0)) + fwd * 1.0  # scuttle
    bz = top(b0 + fwd * 1.2)
    b0.z = bz

    def on(p, dz=0.0):
        return Vector((p.x, p.y, top(p) + dz))
    leaf = bpy.data.materials.get("leaf_wet") or kit.m_simple("leaf11", "#3a3a16", 0.3)
    shard = bpy.data.materials.get("glass_shard") or kit.m_simple("shard11", "#9fb4c0", 0.05)
    dark = kit.m_simple("bonnet_gap", "#060608", 0.5)
    water = kit.m_simple("bonnet_water", "#0a0c12", 0.03, 0.0, coat=1.0)
    obs = []
    for i in range(26):                         # wet leaves and glass crumbs
        p = on(b0 + fwd * rng.uniform(0.1, 2.4) + right * rng.uniform(-1.2, 1.2), 0.012)
        if i % 3 == 0:
            o = kit.box(f"pov_leaf_{i}", (rng.uniform(0.20, 0.36), rng.uniform(0.10, 0.16), 0.008), tuple(p), c, leaf, rot=(0, 0, rng.uniform(0, 6.3)))
        else:
            s = rng.uniform(0.04, 0.09)
            o = kit.box(f"pov_shard_{i}", (s, s * rng.uniform(0.6, 1.4), s * 0.6), tuple(p), c, shard, rot=(rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 6.3)))
        obs.append(o)
    for i in range(9):                          # standing-water streaks (mirror the beacons and sodium lamps)
        p = on(b0 + fwd * rng.uniform(0.3, 2.2) + right * rng.uniform(-1.1, 1.1), 0.006)
        o = kit.box(f"pov_water_{i}", (rng.uniform(0.25, 0.7), rng.uniform(0.9, 1.9), 0.004), tuple(p), c, water, bevel=0.0, rot=(0, 0, th + rng.uniform(-0.25, 0.25)))
        obs.append(o)
    # the buckled bonnet: a dark gap line across it and a raised fold
    g = on(b0 + fwd * 1.15)
    obs.append(kit.box("pov_crease", (2.5, 0.05, 0.02), tuple(g + Vector((0, 0, 0.012))), c, dark, rot=(0, 0, th + 0.10)))
    fold = kit.box("pov_fold", (2.4, 0.5, 0.05), tuple(g + fwd * 0.26 + Vector((0, 0, 0.05))), c,
                   bpy.data.materials.get("paint_hero_v6") or dark, bevel=0.02, rot=(0.16, 0, th + 0.10))
    obs.append(fold)
    for o in obs: o.pass_index = 3
    lc = bpy.data.collections.get("LIGHTS") or bpy.context.scene.collection
    # cabin practicals: warm dome light over the driver, teal instrument glow from the dash
    for nm, loc, col, e, r in (("pov_dome", hd + Vector((0, 0, 0.42)) + fwd * 0.55, (1.0, 0.80, 0.56), 160.0, 0.10),
                               ("pov_dash", hd + fwd * 0.95 + Vector((0, 0, -0.55)), (0.35, 1.0, 0.85), 45.0, 0.20)):
        Lt = bpy.data.lights.new(nm, "POINT"); Lt.color = col; Lt.energy = e; Lt.shadow_soft_size = r
        ob = bpy.data.objects.new(nm, Lt); lc.objects.link(ob); ob.location = loc
        ob.visible_glossy = False
        obs.append(ob)
    _POV[:] = [o.name for o in obs]


# -------------------------------------------------------------------------------------------------------- apply
def sky11():
    """camera rays see a deeper, more saturated sky (reference E: V 0.29 at the top, 0.51 at the horizon, S 0.75-0.9)."""
    w = bpy.context.scene.world
    if not w or not w.node_tree: return
    for nd in w.node_tree.nodes:
        if nd.type == "BACKGROUND" and abs(nd.inputs["Strength"].default_value - 1.0) < 1e-6:
            nd.inputs["Strength"].default_value = P["sky_camera"]
    m = bpy.data.materials.get("worklamp_glow")
    if m:
        for nd in m.node_tree.nodes:
            if nd.type == "EMISSION": nd.inputs["Strength"].default_value = P["lamp_lens"]


def apply(A):
    sky11()
    lights11(A)
    practicals11(A)
    A["v11"] = True
    return A
