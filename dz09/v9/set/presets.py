"""presets.py -- ref-D camera presets (refD_camera.md templates) and per-shot foreground framing props.

Works on the v4 scene and on the v6 beauty scene (same anchors). All values are in D (1 D = 0.6 m), sensor 36 mm on
the long side (fit AUTO, as v4).

    cam = presets.use("eye", A, aspect="9:16", scale=1.0)       # sets camera, resolution, cam["focus"], cam["coc_k"]
    presets.foreground(cam, "pillar", side="right", cover=0.2, depth=1.1)   # optional, per shot

DOF data stored on the camera for post6: cam["focus"] (world point), cam["coc_k"] (blur radius in px at 1280 long side
for an object at infinity), cam["coc_max"] (clamp, px), cam["dof_k"] (the v4 post's sigma, for 'before' renders).
"""
import math, random
import bpy
from mathutils import Vector, Matrix

import expressway as X
import kit
import vehicles as V

# template, height, lens per refD_camera.md section 4
#   low   = T5/T4 ground-level, looking up at Kong past a crumpled fender (0.6 D, 28 mm)
#   eye   = T3 frontal tableau, eye height 2.7 D, 35 mm, frame-in-a-frame pillar
#   high  = T7 strong establishing, 13 D, ~25 deg down, 45 mm (long lens stacks the rows)
#   macro = T1 prop macro: the cutter's 3-bar LED gauge sharp, door/Kong/beacons as big bokeh, 50 mm


def table(A):
    K = Vector(A["kong_mark"]); KH = K + Vector((0, 0, 2.35))
    door = Vector(A["door_mid"])
    cu = bpy.data.objects.get(A.get("cutter3d", "cutter3d")); bpy.context.view_layer.update()
    cut_m = cu.matrix_world.copy() if cu else Matrix.Translation(Vector(A["cutter_jaw"]))
    led = cut_m @ Vector((0.095, -0.66, -0.19))
    C = {
        "low": dict(loc=(-2.55, 30.4, 0.55), look=tuple(KH + Vector((0.0, 0.0, 0.25))), lens=28, focus=tuple(KH), k=6.0, kmax=24,
                    dof_k=2.0, hide=["bike_a"], fg=[("wheel", dict(side="left", cover=0.42, depth=1.5))],
                    desc="T5 ground level 0.55 D, 28 mm, pitched up a little; a wrecked wheel and wing fill the left 36 %"),
        "eye": dict(loc=(-2.3, 25.2, 2.7), look=(-7.7, 37.5, 2.15), lens=35, focus=tuple(KH), k=4.0, kmax=18,
                    dof_k=1.8, fg=[("pillar", dict(side="right", cover=0.16, depth=1.4))],
                    desc="T3 frontal tableau at eye height 2.7 D, 35 mm, a dark car pillar frames the right edge"),
        "high": dict(loc=(3.8, 7.0, 13.0), look=(-8.6, 42.0, 0.0), lens=45, focus=tuple(K), k=1.6, kmax=10,
                     dof_k=1.2, fg=[("pole", dict(side="left", cover=0.08, depth=6.0))],
                     desc="T7 strong establishing, 13 D up, ~27 deg down, 45 mm; a lamp pole on the left"),
        "macro": dict(loc=tuple(led + Vector((0.55, 0.75, 0.22)).normalized() * 2.6), look=tuple(led + Vector((-0.42, 0.0, 0.10))),
                      lens=50, clip=0.02, focus=tuple(led), k=70.0, kmax=36, dof_k=7.0, props={"cutter": True},
                      fg=[("lip", dict(cover=0.17, depth=0.55))],
                      desc="T1 prop macro, 50 mm: LED gauge sharp, the door seam and the night behind as 30+ px bokeh"),
    }
    W = {"low": dict(loc=(-2.3, 30.0, 0.6)), "eye": dict(loc=(-1.8, 24.0, 2.7), lens=30),
         "high": dict(lens=38), "macro": dict(lens=40)}
    return C, W


PRESETS = ["low", "eye", "high", "macro"]


def use(name, A, aspect="9:16", scale=1.0, scene=None, with_fg=True, pct=None):
    scene = scene or bpy.context.scene
    C, W = table(A)
    p = dict(C[name])
    if aspect == "16:9": p.update(W.get(name, {}))
    cam = X.make_camera()
    cam.location = p["loc"]
    cam.rotation_euler = kit.look_rot(p["loc"], p["look"], p.get("roll", 0.0), p.get("up"))
    cam.data.lens = p["lens"]; cam.data.clip_start = p.get("clip", 0.1)
    rx, ry = (720, 1280) if aspect == "9:16" else (1280, 720)
    scene.render.resolution_x, scene.render.resolution_y = int(rx * scale), int(ry * scale)
    scene.render.resolution_percentage = pct or X._STATE.get("pct", 100)
    for ob in bpy.data.objects:
        for con in ob.constraints:
            if con.type == "TRACK_TO": con.target = cam
    cut = bpy.data.objects.get("cutter3d")
    if cut:
        show = p.get("props", {}).get("cutter", False)
        for ob in [cut] + list(cut.children_recursive): ob.hide_render = not show
    cam["preset"] = name; cam["aspect"] = aspect
    cam["focus"] = p["focus"]; cam["coc_k"] = p["k"]; cam["coc_max"] = p["kmax"]; cam["dof_k"] = p["dof_k"]
    clear_foreground()
    for nm in list(scene.get("v6_hidden", [])):           # restore what the previous preset hid
        ob = bpy.data.objects.get(nm)
        if ob: ob.hide_render = False
    hid = []
    for root in p.get("hide", []):                          # per-preset clutter removal (root name + its children)
        ob = bpy.data.objects.get(root)
        if not ob: continue
        for o in [ob] + list(ob.children_recursive):
            if not o.hide_render: o.hide_render = True; hid.append(o.name)
    scene["v6_hidden"] = hid
    bpy.context.view_layer.update()
    if with_fg:
        for kind, kw in p.get("fg", []):
            foreground(cam, kind, **kw)
    return cam


# ------------------------------------------------------------------------------------------------ foreground framing
FG_COLL = "FG_FRAMING"


def clear_foreground():
    c = bpy.data.collections.get(FG_COLL)
    if c is None: return
    for ob in list(c.objects): bpy.data.objects.remove(ob, do_unlink=True)


def _coll():
    c = bpy.data.collections.get(FG_COLL)
    if c is None:
        c = bpy.data.collections.new(FG_COLL); bpy.context.scene.collection.children.link(c)
    return c


def _frustum(cam, depth):
    sc = bpy.context.scene
    W, H = sc.render.resolution_x, sc.render.resolution_y
    half_long = depth * 18.0 / cam.data.lens
    if W >= H: hw, hh = half_long, half_long * H / W
    else: hh, hw = half_long, half_long * W / H
    return hw, hh


def _grid_mesh(name, nx, ny, fn, c, mat):
    verts, faces = [], []
    for j in range(ny + 1):
        for i in range(nx + 1):
            verts.append(fn(i / nx, j / ny))
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i
            faces.append((a, a + 1, a + nx + 2, a + nx + 1))
    ob = kit.mesh_obj(name, verts, faces, c, mat=mat, smooth=True)
    return ob


def foreground(cam, kind, side="left", cover=0.3, depth=1.2, seed=1):
    """add a framing prop in camera space. kind: 'pillar' (dark car pillar, rain beads), 'fender' (crumpled silver
    panel low in the corner), 'lip' (wet bumper lip across the bottom), 'pole' (galvanised lamp pole), 'post'
    (guard-rail post + W-beam), 'cone' (traffic cone corner). cover = fraction of the frame width (or height for
    'lip') it covers; depth = distance from the lens in D (it is real geometry: lit, shadowed, blurred by DOF)."""
    c = _coll(); rng = random.Random(seed)
    hw, hh = _frustum(cam, depth)
    M = cam.matrix_world.copy()
    sgn = -1 if side == "left" else 1
    def cs(x, y, z): return M @ Vector((x, y, -z))      # camera-space -> world
    edge = sgn * hw                                      # frame edge x at this depth
    inner = edge - sgn * 2 * hw * cover                 # where the prop's inner edge sits
    if kind == "pillar":
        m = V.paint("sedan", "#1b1c20")
        w = abs(edge - inner) + 0.3 * hw
        cx = inner + sgn * w / 2
        def fn(u, v):
            x = cx + (u - 0.5) * w + 0.08 * w * math.sin(v * 2.2)     # slight curve like an A pillar
            y = (v - 0.5) * 2.6 * hh
            z = depth + 0.06 * depth * math.sin(u * math.pi)
            return tuple(cs(x, y, z))
        ob = _grid_mesh("fg_pillar", 6, 12, fn, c, m)
        # rubber door seal along the inner edge
        seal = kit.mesh_obj("fg_seal", [tuple(cs(inner - sgn * 0.01 * hw, (v - 0.5) * 2.6 * hh, depth * 0.98)) for v in (0, 1)] +
                            [tuple(cs(inner + sgn * 0.03 * hw, (v - 0.5) * 2.6 * hh, depth * 0.98)) for v in (0, 1)],
                            [(0, 1, 3, 2)], c, mat=V.mat("rubber"))
        obs = [ob, seal]
    elif kind == "fender":
        m = V.paint("sedan", "#c9ccd0")
        w = abs(edge - inner) + 0.25 * hw
        x0 = inner - w if sgn < 0 else inner
        top = -hh + 2 * hh * 0.62
        def fn(u, v):
            x = x0 + u * w
            # profile: a wheel-arch curve on the inner edge, crumpled
            y = -hh * 1.2 + v * (top + hh * 1.2)
            arch = 0.35 * hh * math.sin(min(1, v) * math.pi) * (1 - abs(u - (0.0 if sgn < 0 else 1.0)))
            z = depth * (1.0 + 0.10 * math.sin(u * 7 + v * 3) * math.sin(v * 5 + 1) + 0.05 * rng.uniform(-1, 1))
            return tuple(cs(x + (arch if sgn < 0 else -arch) * 0.0, y, z))
        ob = _grid_mesh("fg_fender", 16, 16, fn, c, m)
        tyre_c = cs(inner - sgn * 0.05 * hw, -hh * 0.65, depth * 1.35)
        ty = kit.cyl("fg_tyre", 0.75 * hh * 0.45, 0.5 * depth, c, 24, V.mat("tread"), loc=tuple(tyre_c))
        ty.rotation_euler = (M.to_euler()); ty.rotation_euler.rotate_axis("Y", math.pi / 2)
        obs = [ob, ty]
    elif kind == "wheel":
        r = abs(edge - inner) * 0.55
        me = V.wheel_mesh(1.0)
        ob = bpy.data.objects.new("fg_wheel", me); c.objects.link(ob)
        ctr = Vector((inner - sgn * r * 0.95, -hh + r * 0.85, -depth))
        ob.matrix_world = M @ Matrix.Translation(ctr) @ Matrix.Rotation(math.radians(-sgn * 62), 4, "Y") @ Matrix.Scale(r, 4)
        m = V.paint("sedan", "#c9ccd0")
        top = -hh + r * 1.9
        def fn(u, v):
            x = (edge + sgn * 0.3 * hw) + (inner - sgn * 0.1 * hw - (edge + sgn * 0.3 * hw)) * u
            ang = math.pi * v
            y = top + 0.9 * r * math.sin(ang) * 0.35 + v * 1.4 * hh
            z = depth * (1.05 + 0.08 * math.sin(u * 8 + v * 4) * math.sin(v * 6 + 2) + 0.04 * rng.uniform(-1, 1))
            return tuple(cs(x, y, z))
        obs = [ob]
    elif kind == "lip":
        m = V.paint("sedan", "#26324f")
        top = -hh + 2 * hh * cover
        def fn(u, v):
            x = (u - 0.5) * 2.4 * hw
            y = -hh * 1.3 + v * (top + hh * 1.3) + 0.03 * hh * math.sin(u * 9)
            z = depth * (1.0 + 0.25 * v)                   # tilted away like a bonnet
            return tuple(cs(x, y, z))
        ob = _grid_mesh("fg_lip", 18, 8, fn, c, m)
        chrome = kit.mesh_obj("fg_lip_trim", [tuple(cs(-1.2 * hw, top - 0.02 * hh, depth * 1.24)), tuple(cs(1.2 * hw, top - 0.02 * hh, depth * 1.24)),
                                               tuple(cs(1.2 * hw, top + 0.015 * hh, depth * 1.25)), tuple(cs(-1.2 * hw, top + 0.015 * hh, depth * 1.25))],
                              [(0, 1, 2, 3)], c, mat=V.mat("chrome"))
        obs = [ob, chrome]
    elif kind == "pole":
        r = abs(edge - inner) / 2
        cx = inner + sgn * r
        p0 = cs(cx, -hh * 1.4, depth); p1 = cs(cx, hh * 1.4, depth)
        d = p1 - p0
        st = X.m_steel("steel_mast", "#6b6f74", 0.38)
        ob = kit.cyl("fg_pole", r, d.length, c, 20, st, loc=tuple((p0 + p1) / 2))
        ob.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
        band = kit.cyl("fg_pole_band", r * 1.04, d.length * 0.03, c, 20, kit.m_simple("reflect_band", "#d9d6cc", 0.4), loc=tuple(p0 + d * 0.30))
        band.rotation_euler = ob.rotation_euler
        obs = [ob, band]
    elif kind == "post":
        st = X.m_steel("steel_galv", "#7d8288", 0.32)
        w = abs(edge - inner)
        cx = inner + sgn * w / 2
        p = cs(cx, -hh * 0.5, depth)
        post = kit.box("fg_post", (w, w * 0.5, hh * 2.0), tuple(p), c, st)
        post.rotation_euler = M.to_euler()
        beam = kit.box("fg_wbeam", (hw * 3, hh * 0.12, hh * 0.25), tuple(cs(0, -hh * 0.55, depth * 1.02)), c, st)
        beam.rotation_euler = M.to_euler()
        obs = [post, beam]
    elif kind == "cone":
        cm_o = kit.m_simple("cone_orange", "#e2541a", 0.45, coat=0.4)
        h = hh * 1.2
        ob = kit.lathe("fg_cone", [(0.30 * h, 0.0), (0.06 * h, 0.95 * h), (0.001, h)], c, 20, cm_o)
        ob.location = cs(inner + sgn * 0.3 * h, -hh * 1.05, depth)
        obs = [ob]
    elif kind == "beam":                                   # v9: dark gantry / overpass underside across the top
        st = kit.m_simple("fg_beam_dark", "#121417", 0.6, 0.4)
        top = hh * 1.3; bot = hh - 2 * hh * cover
        def fn(u, v):
            x = (u - 0.5) * 2.6 * hw
            y = bot + v * (top - bot) + 0.02 * hh * math.sin(u * 7)
            return tuple(cs(x, y, depth * (1.0 - 0.15 * v)))
        ob = _grid_mesh("fg_beam", 12, 4, fn, c, st)
        lip = kit.mesh_obj("fg_beam_lip", [tuple(cs(-1.3 * hw, bot, depth)), tuple(cs(1.3 * hw, bot, depth)),
                                            tuple(cs(1.3 * hw, bot - 0.025 * hh, depth * 0.97)), tuple(cs(-1.3 * hw, bot - 0.025 * hh, depth * 0.97))],
                           [(0, 1, 2, 3)], c, mat=X.m_steel("steel_gantry", "#8a8f96", 0.35))
        obs = [ob, lip]
    elif kind == "barrier":                                # v9: dark concrete barrier edge across a bottom corner
        cm = kit.m_simple("fg_barrier_dark", "#2a2a2c", 0.85)
        w = 2 * hw * cover
        x0 = edge - sgn * w
        def fn(u, v):
            x = x0 + (edge + sgn * 0.3 * hw - x0) * u
            y = -hh * 1.3 + v * (hh * 0.9) * (0.6 + 0.4 * u)
            return tuple(cs(x, y, depth * (1.0 + 0.05 * math.sin(u * 5 + v * 3))))
        ob = _grid_mesh("fg_barrier", 10, 6, fn, c, cm)
        obs = [ob]
    else:
        raise ValueError(kind)
    for ob in obs:
        ob.pass_index = 5; ob["fg"] = kind
    return obs
