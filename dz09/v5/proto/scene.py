"""scene.py -- v5 proto: the detailed expressway set (v4/set_expressway, imported) + the real 2.5D Kong (v4/cast_dz09,
imported) + this folder's fixes: darker blue sky, dirty dented wet hero sedan, foreground framing props, per-shot
toon key. Nothing outside v5/proto is written.
"""
import os, sys, math
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler

PROJ = "/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09"
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (PROJ + "/v4/set_expressway", PROJ + "/v4/cast_dz09"):
    if p not in sys.path: sys.path.insert(0, p)
import expressway as X, kit, tex, vehicles as V
import stage25 as st
import draw25d

CAST_SCALE = 0.52 / 0.60
SPR = os.path.join(HERE, "tmp", "sprites")


def hexlin(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple((x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c) + (1.0,)


# ------------------------------------------------------------------------------------------------ sky fix
def fix_sky():
    """darker, bluer night sky: same node graph as the set, new colours (hue ~228-236, no lavender)."""
    w = bpy.context.scene.world
    nt = w.node_tree
    ramps = [n for n in nt.nodes if n.type == "VALTORGB"]
    g = ramps[0].color_ramp
    cols = ["#07080c", "#111829", "#1f2c48", "#1a2744", "#111c38", "#0a1126"]
    for e, c in zip(g.elements, cols):
        e.color = hexlin(c)
    for n in nt.nodes:
        if n.type == "MIX" and n.data_type == "RGBA":
            b = n.inputs[7]
            if b.is_linked: continue
            c = tuple(b.default_value)
            # identify by original colour
            if abs(c[0] - hexlin("#8a7f70")[0]) < 1e-3: b.default_value = hexlin("#3a3431")       # sodium horizon
            elif abs(c[0] - hexlin("#8c98b8")[0]) < 1e-3: b.default_value = hexlin("#24345a")     # lit cloud gaps
            elif abs(c[0] - hexlin("#1f2542")[0]) < 1e-3: b.default_value = hexlin("#060a16")     # dark cloud
            elif abs(c[0] - hexlin("#e9e4cf")[0]) < 1e-3: b.default_value = hexlin("#b9bdc6")     # moon disc
            elif abs(c[0] - hexlin("#b9bbd2")[0]) < 1e-3: b.default_value = hexlin("#4a5a80")     # moon halo
    for n in nt.nodes:
        if n.type == "BACKGROUND": pass


# ------------------------------------------------------------------------------------------------ hero car
def dirty_paint():
    name = "proto_hero_paint"
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = kit.MB(name)
    gen = mb.n("ShaderNodeTexCoord")
    sep = mb.n("ShaderNodeSeparateXYZ"); mb.l(gen.outputs["Object"], sep.inputs[0])
    # vertical dirt streaks / water runs: noise stretched along Z
    mp = mb.n("ShaderNodeMapping", Scale=(7.0, 7.0, 0.55)); mb.l(gen.outputs["Object"], mp.inputs[0])
    streak = mb.n("ShaderNodeTexNoise", Scale=3.0, Detail=6.0, Roughness=0.65); mb.l(mp.outputs[0], streak.inputs["Vector"])
    st_m = mb.math("MULTIPLY", mb.math("SUBTRACT", streak.outputs["Fac"], 0.50), 4.0, True)
    # low grime (road spray) and mud splatter
    nz = mb.n("ShaderNodeTexNoise", Scale=2.2, Detail=5.0); mb.l(gen.outputs["Object"], nz.inputs["Vector"])
    zz = mb.math("ADD", sep.outputs["Z"], mb.math("MULTIPLY", nz.outputs["Fac"], 0.7))
    low = mb.ramp(zz, [(0.0, (1, 1, 1)), (0.75, (1, 1, 1)), (1.45, (0, 0, 0))])
    spl = mb.n("ShaderNodeTexNoise", Scale=26.0, Detail=3.0, Roughness=0.8); mb.l(gen.outputs["Object"], spl.inputs["Vector"])
    spk = mb.math("MULTIPLY", mb.math("GREATER_THAN", spl.outputs["Fac"], 0.60), low)
    # scratches: thin stretched noise lines
    mp2 = mb.n("ShaderNodeMapping", Scale=(1.0, 22.0, 1.0), Rotation=(0.3, 0.0, 0.25)); mb.l(gen.outputs["Object"], mp2.inputs[0])
    scr = mb.n("ShaderNodeTexWave", Scale=3.0, Distortion=9.0, Detail=4.0); mb.l(mp2.outputs[0], scr.inputs["Vector"])
    scr_m = mb.math("MULTIPLY", mb.math("GREATER_THAN", scr.outputs["Fac"], 0.93), 1.0)
    base = hexlin("#a9adb1")
    col = mb.mix(mb.math("MULTIPLY", st_m, 0.45), base, hexlin("#5e5a52"))
    col = mb.mix(mb.math("MULTIPLY", low, 0.75), col, hexlin("#3a342c"))
    col = mb.mix(mb.math("MULTIPLY", spk, 0.8), col, hexlin("#221d18"))
    col = mb.mix(mb.math("MULTIPLY", scr_m, 0.7), col, hexlin("#d8dadc"))
    # dents: large low-frequency noise as bump; droplets (image, box projected) as fine bump
    dn = mb.n("ShaderNodeTexNoise", Scale=1.3, Detail=2.0); mb.l(gen.outputs["Object"], dn.inputs["Vector"])
    nrm = kit.bump_node(mb, dn.outputs["Fac"], 0.35, 0.25)
    nrm = kit.bump_node(mb, scr_m, 0.25, 0.004, nrm)
    drp = mb.n("ShaderNodeTexImage"); drp.image = kit.image(tex.droplets(), True); drp.projection = "BOX"; drp.projection_blend = 0.3
    mpd = mb.n("ShaderNodeMapping", Scale=(3.2, 3.2, 3.2)); mb.l(gen.outputs["Object"], mpd.inputs[0]); mb.l(mpd.outputs[0], drp.inputs[0])
    bead = drp.outputs["Color"]
    nrm2 = kit.bump_node(mb, bead, 0.9, 0.012, nrm)
    rough = mb.math("ADD", 0.16, mb.math("ADD", mb.math("MULTIPLY", low, 0.45), mb.math("MULTIPLY", spk, 0.3)))
    b = mb.principled(col, rough, 0.35, 0.0, 0.04, nrm)
    b.inputs["Coat Weight"].default_value = 0.9
    b.inputs["Coat Roughness"].default_value = 0.03
    mb.l(nrm2, b.inputs["Coat Normal"])
    return mb.out(b)


def fix_hero_car(A, seed=4):
    hero = bpy.data.objects[A["hero_car"]]
    m = dirty_paint()
    rng = np.random.default_rng(seed)
    for o in [hero] + list(hero.children_recursive):
        if o.type != "MESH": continue
        for i, s in enumerate(o.data.materials):
            if s and s.name.startswith("paint_sedan"):
                o.data.materials[i] = m
        if o.name in ("hero_car_body", "hero_car_door_fr"):
            me = o.data
            # dents: push vertices inward around random centres on the sides (local x = side)
            co = np.array([v.co[:] for v in me.vertices])
            if len(co) < 20: continue
            lo, hi = co.min(0), co.max(0)
            cen = []
            for k in range(7 if o.name == "hero_car_body" else 3):
                side = rng.choice([-1, 1]) if o.name == "hero_car_body" else (1 if co[:, 0].mean() > 0 else -1)
                cen.append((side * hi[0] * 0.98 if side > 0 else lo[0] * 0.98, rng.uniform(lo[1] * 0.8, hi[1] * 0.8),
                            rng.uniform(lo[2] + 0.3 * (hi[2] - lo[2]), lo[2] + 0.7 * (hi[2] - lo[2])), rng.uniform(0.35, 0.7), rng.uniform(0.05, 0.12)))
            for (cx, cy, cz, r, d) in cen:
                dd = np.sqrt((co[:, 0] - cx) ** 2 + (co[:, 1] - cy) ** 2 + (co[:, 2] - cz) ** 2)
                w = np.exp(-(dd / r) ** 2) * d
                co[:, 0] -= np.sign(cx) * w
            for v, c in zip(me.vertices, co): v.co = c
            me.update()
    # rain droplets on the hero glass
    for o in [hero] + list(hero.children_recursive):
        if o.type == "MESH":
            for s in o.data.materials:
                if s and "glass" in s.name and not s.get("proto_drops"):
                    _drops_on_glass(s)


def _drops_on_glass(m):
    nt = m.node_tree
    bs = [n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"]
    if not bs: return
    b = bs[0]
    if b.inputs["Normal"].is_linked: return
    gen = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (4.0, 4.0, 4.0)
    nt.links.new(gen.outputs["Object"], mp.inputs[0])
    im = nt.nodes.new("ShaderNodeTexImage"); im.image = kit.image(tex.droplets(), True); im.projection = "BOX"; im.projection_blend = 0.3
    nt.links.new(mp.outputs[0], im.inputs[0])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.8; bp.inputs["Distance"].default_value = 0.01
    nt.links.new(im.outputs["Color"], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
    m["proto_drops"] = 1


# ------------------------------------------------------------------------------------------------ props
_FG = []


def cone(name, loc, yaw=0.0, tilt=0.0, scale=1.0):
    c = kit.coll("PROTO_FG")
    org = kit.m_simple("proto_cone_orange", "#e8561a", 0.45)
    wht = kit.m_simple("proto_cone_white", "#d9dbe0", 0.3)
    blk = kit.m_simple("proto_cone_base", "#141416", 0.6)
    root = bpy.data.objects.new(name, None); c.objects.link(root)
    base = kit.box(name + "_base", (0.62, 0.62, 0.06), (0, 0, 0.03), c, blk, bevel=0.02); base.parent = root
    body = kit.lathe(name + "_body", [(0.26, 0.06), (0.20, 0.45), (0.135, 0.8), (0.04, 1.2), (0.0, 1.22)], c, 24, org); body.parent = root
    band = kit.lathe(name + "_band", [(0.192, 0.50), (0.168, 0.66)], c, 24, wht, cap=False); band.parent = root
    band.scale = (1.04, 1.04, 1.0)
    root.location = loc; root.rotation_euler = (tilt, 0, yaw); root.scale = (scale,) * 3
    for o in (base, body, band): o.pass_index = 4
    _FG.extend([root, base, body, band])
    return root


def shards(name, centre, n=40, radius=0.8, seed=1):
    c = kit.coll("PROTO_FG")
    g = kit.m_simple("proto_shard", "#9fb4c0", 0.05, 0.0, 0.0)
    rng = np.random.default_rng(seed)
    obs = []
    import bmesh
    bm = bmesh.new()
    for i in range(n):
        r = radius * math.sqrt(rng.random()); a = rng.uniform(0, 2 * math.pi)
        s = rng.uniform(0.025, 0.09)
        mat = Matrix.Translation((centre[0] + r * math.cos(a), centre[1] + r * math.sin(a), centre[2] + s * 0.15)) @ \
            Euler((rng.uniform(-0.4, 0.4), rng.uniform(-0.4, 0.4), rng.uniform(0, 6.3))).to_matrix().to_4x4()
        bmesh.ops.create_cube(bm, size=1.0, matrix=mat @ Matrix.Diagonal((s, s * rng.uniform(0.5, 1.4), s * 0.12, 1.0)))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(g)
    ob = bpy.data.objects.new(name, me); c.objects.link(ob); ob.pass_index = 4
    _FG.append(ob)
    return ob


def clear_fg():
    for o in _FG:
        try: bpy.data.objects.remove(o, do_unlink=True)
        except Exception: pass
    _FG.clear()


# ------------------------------------------------------------------------------------------------ the cutter LEDs
def cutter_led_mats():
    """give each of the 3D cutter's 3 LED bars its own emission so they can light one by one."""
    out = []
    for k in range(3):
        ob = bpy.data.objects.get(f"cutter3d_led{k}")
        if ob is None: continue
        m = bpy.data.materials.new(f"proto_led{k}"); m.use_nodes = True; nt = m.node_tree
        for n in list(nt.nodes): nt.nodes.remove(n)
        o = nt.nodes.new("ShaderNodeOutputMaterial"); e = nt.nodes.new("ShaderNodeEmission")
        e.inputs["Color"].default_value = hexlin("#1fd655"); e.inputs["Strength"].default_value = 0.0
        nt.links.new(e.outputs[0], o.inputs["Surface"]); m.cycles.emission_sampling = "NONE"
        ob.data = ob.data.copy(); ob.data.materials.clear(); ob.data.materials.append(m)
        out.append(e.inputs["Strength"])
    return out


def glove_on_cutter():
    """a 3D glove and sleeve on the cutter's rear loop handle (S08/S09: 'the cutter in his glove')."""
    cu = bpy.data.objects["cutter3d"]
    c = kit.coll("PROTO_HAND")
    glove = kit.m_simple("proto_glove", "#151518", 0.75)
    sleeve = kit.m_simple("proto_sleeve", "#d8601c", 0.6)
    band = kit.m_simple("proto_reflect", "#c9ced6", 0.2, 0.6)
    obs = []
    # loop handle at local (0, -0.98?, 0): the rear loop; find it
    lp = bpy.data.objects.get("cutter3d_loop")
    base = lp.location.copy() if lp else Vector((0, -0.95, 0))
    g = kit.lathe("proto_glove", [(0.001, -0.11), (0.08, -0.09), (0.10, 0.0), (0.085, 0.08), (0.001, 0.10)], c, 20, glove)
    g.parent = cu; g.location = base + Vector((0.0, 0.0, 0.11)); g.scale = (1.0, 1.25, 0.85); obs.append(g)
    # knuckles
    for i in range(4):
        k = kit.lathe(f"proto_knuckle{i}", [(0.001, -0.03), (0.035, 0.0), (0.001, 0.03)], c, 12, glove)
        k.parent = cu; k.location = base + Vector((0.06, -0.06 + i * 0.04, 0.05)); obs.append(k)
    s = kit.cyl("proto_sleeve", 0.11, 0.9, c, 20, sleeve, loc=base + Vector((0.05, -0.52, 0.22)), rot=(math.radians(68), 0, 0.12))
    s.parent = cu; obs.append(s)
    cuff = kit.cyl("proto_cuff", 0.10, 0.12, c, 20, glove, loc=base + Vector((0.01, -0.10, 0.14)), rot=(math.radians(68), 0, 0.12))
    cuff.parent = cu; obs.append(cuff)
    for y in (-0.55, -0.40):
        b = kit.cyl("proto_band", 0.113, 0.05, c, 20, band, loc=base + Vector((0.05, y, 0.22 + (y + 0.52) * -0.4)), rot=(math.radians(68), 0, 0.12))
        b.parent = cu; obs.append(b)
    for o in obs: o.pass_index = 4
    return obs


# ------------------------------------------------------------------------------------------------ actors
def make_kong(name, ppd, A):
    a = st.Actor25(name, "kong", gap=0.05, ppd=ppd, mode="25d", follow=0.6, sprite_dir=os.path.join(SPR, name))
    a.root.scale = (CAST_SCALE,) * 3
    for ob in [a.root] + list(a.root.children_recursive):
        if ob.type == "MESH": ob.pass_index = 2
    return a


def hide_actor(a, hide=True):
    for ob in [a.root] + list(a.root.children_recursive):
        if ob.type == "MESH":
            if hide: ob.hide_render = True
    if not hide:
        a.root.hide_render = False


def toon_key(cam_loc, actor_loc, side=-1.0, up=0.55, front=0.75):
    """put the toon key on camera-left (side -1) and above, so the face reads white with a crescent away."""
    t = Vector(cam_loc) - Vector(actor_loc); t.z = 0; t.normalize()
    right = Vector((t.y, -t.x, 0))             # camera right as seen from the camera looking at the actor
    d = (t * front + right * side * 0.7 + Vector((0, 0, up))).normalized()
    ng = st.toon_group()
    for i in range(3): ng.nodes["key_dir"].inputs[i].default_value = d[i]


def build(quality="final", threads=2):
    A = X.build(haze_cards=False)
    X.setup_render(quality=quality, threads=threads)
    fix_sky()
    fix_hero_car(A)
    leds = cutter_led_mats()
    st.sync_lights(key="flood_key", rims=["beacon_red_0", "sodium_1_-1"], shadow="flood_key", rim_gain=0.35)
    st.set_toon(exposure=0.95)
    return A, leds
