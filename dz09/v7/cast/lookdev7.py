"""lookdev7.py -- v7 cast lookdev at 720x1280.

    python3 lookdev7.py neutral [--only kong,crew,driver] [--spp 32]   front / 3/4 / side, neutral soft light
    python3 lookdev7.py night   [--only ...]                           the same views IN the v6 expressway set (its lights,
                                                                       sky, rain, post6 grade), at Kong's mark
    python3 lookdev7.py extras  [--parts faces,driver,props,wet]       expression heads, driver poses, props, wet Kong
    python3 lookdev7.py sheet                                          -> lookdev.png
Every render writes <png>.json with the projected head centre / head D px / crown and sole px (for the sheet).
"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out"); TMP = os.path.join(HERE, "tmp")
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
sys.path.insert(0, HERE)
VIEWS = [("front", 0), ("q", -38), ("side", -90)]
import os as _o
if _o.environ.get("LD_VIEWS"): VIEWS = [v for v in VIEWS if v[0] in _o.environ["LD_VIEWS"].split(",")]
POSE = {"kong": "kong_hold_cutter", "crew": "crew_idle", "driver": "driver_stand"}
CS = None   # set scale (computed from cast7.HEIGHT)


def _aim(ob, tgt):
    from mathutils import Vector
    d = Vector(tgt) - ob.location
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def neutral_scene(spp=32):
    import bpy, cast7 as C
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = spp
    sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 1
    sc.cycles.transparent_max_bounces = 24; sc.cycles.sample_clamp_indirect = 3.0
    sc.render.threads_mode = "FIXED"; sc.render.threads = 4
    sc.render.resolution_x = 720; sc.render.resolution_y = 1280; sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
    sc.render.image_settings.file_format = "PNG"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = C.hexlin("#b9c3d3"); bg.inputs[1].default_value = 0.55
    cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 35; cam_d.sensor_width = 36
    cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
    gm = bpy.data.meshes.new("ground")
    gm.from_pydata([(-900, -900, 0), (900, -900, 0), (900, 900, 0), (-900, 900, 0)], [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("ground", gm); sc.collection.objects.link(g)
    gm.materials.append(C.m_toon("ground", "#a9a59d", amb=0.3))
    kd = bpy.data.lights.new("key", "AREA"); kd.shape = "DISK"; kd.size = 4.0; kd.energy = 1400; kd.color = (1.0, 0.96, 0.9)
    k = bpy.data.objects.new("key", kd); sc.collection.objects.link(k); k.location = (-5.5, -7.0, 8.0); _aim(k, (0, 0, 2.2))
    rd = bpy.data.lights.new("rim", "AREA"); rd.size = 3.0; rd.energy = 700; rd.color = (0.78, 0.86, 1.0)
    r = bpy.data.objects.new("rim", rd); sc.collection.objects.link(r); r.location = (5, 7, 6); _aim(r, (0, 0, 2.4))
    return sc, cam


def frame(sc, cam, target_z, dist, height, lens=35, yaw=0.0, x=0.0):
    from mathutils import Vector
    import bpy
    cam.location = (x, -dist, height); cam.data.lens = lens
    _aim(cam, (x, 0, target_z))


def meta(sc, cam, ch, png, extra=None):
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    W = sc.render.resolution_x * sc.render.resolution_percentage / 100
    H = sc.render.resolution_y * sc.render.resolution_percentage / 100
    def pr(p):
        v = world_to_camera_view(sc, cam, Vector(p)); return (v.x * W, (1 - v.y) * H)
    hw = ch.head.matrix_world
    c = hw.translation.copy()
    # head D: project the camera-perpendicular radius
    right = cam.matrix_world.to_3x3() @ Vector((1, 0, 0))
    sx = ch.root.matrix_world.to_3x3().to_scale().x
    cx, cy = pr(c); ex, ey = pr(c + right * 0.5 * sx)
    D = 2 * math.hypot(ex - cx, ey - cy)
    crown = pr(c + Vector((0, 0, 0.495 * sx)))[1]; sole = pr(ch.root.matrix_world.translation)[1]
    m = dict(head=(cx, cy), D=D, crown=crown, sole=sole, W=W, H=H)
    if extra: m.update(extra)
    json.dump(m, open(png + ".json", "w"))
    return m


def render(sc, path):
    import bpy
    sc.render.filepath = path
    t = time.time(); bpy.ops.render.render(write_still=True); return round(time.time() - t, 1)


def build_cast(C, kinds, wet=False, sep=False):
    chars = {k: C.Character(k, wet=wet, separator=sep) for k in kinds}
    cut = None
    if "kong" in chars:
        cut = C.Cutter(bars=3, wet=wet)
        chars["kong"].hold(cut, "r", fwd=(0.0, -0.3, -1.0), up=(0, -1, 0.3))
    return chars, cut


def show_only(chars, cut, kind):
    for k, ch in chars.items():
        for ob in ch.objects: ob.hide_render = k != kind
        if k == kind: ch.set_face(ch.expr)
    if cut:
        for ob in cut.objects: ob.hide_render = kind != "kong"


def neutral(only, spp=32):
    import cast7 as C
    sc, cam = neutral_scene(spp)
    kinds = only or ["kong", "crew", "driver"]
    chars, cut = build_cast(C, kinds)
    times = {}
    for kind in kinds:
        ch = chars[kind]; show_only(chars, cut, kind)
        ch.preset(POSE[kind])
        for vn, f in VIEWS:
            ch.place((0, 0, 0), f)
            frame(sc, cam, 2.3, 7.4, 2.2)
            p = os.path.join(OUT, f"n_{kind}_{vn}.png")
            times[f"n_{kind}_{vn}"] = render(sc, p); meta(sc, cam, ch, p)
            print("TIME", kind, vn, times[f"n_{kind}_{vn}"], flush=True)
    _times(times)


def _times(t):
    p = os.path.join(OUT, "times.json"); old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(t); json.dump(old, open(p, "w"), indent=1)


def night(only, q="final"):
    """the same three views inside the v6 beauty set at Kong's mark: its moon key, sodium, flood, sky fill, rain, grade."""
    sys.path.insert(0, os.path.join(PROJ, "v6", "set"))
    import bpy
    from mathutils import Vector
    import beauty as B
    A = B.build(); B.setup_render(q, threads=4)
    import kit, cast7 as C
    X = B.X
    kinds = only or ["kong", "crew", "driver"]
    chars, cut = build_cast(C, kinds, wet=True, sep=True)
    cs = 2.86 / C.HEIGHT
    for ch in chars.values(): ch.root.scale = (cs,) * 3; ch.set_pass_index(2)
    if cut:
        for ob in cut.objects: ob.pass_index = 2
    K = Vector(A["kong_mark"])
    to_cam = Vector((4.4, -8.4, 0)).normalized()
    hide = []
    for r in ("bike_a",):
        ob = bpy.data.objects.get(r)
        if ob:
            for o in [ob] + list(ob.children_recursive): o.hide_render = True
    cam = X.make_camera()
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = 720, 1280
    sc.render.resolution_percentage = X._STATE.get("pct", 100)
    cu = bpy.data.objects.get("cutter3d")
    if cu:
        for ob in [cu] + list(cu.children_recursive): ob.hide_render = True
    import presets; presets.clear_foreground()
    face0 = math.degrees(math.atan2(to_cam[0], -to_cam[1]))
    times = {}
    for kind in kinds:
        ch = chars[kind]; show_only(chars, cut, kind)
        ch.preset(POSE[kind])
        for vn, f in VIEWS:
            ch.place(tuple(K), face0 + f)
            hz = 2.35 * cs
            loc = K + to_cam * 5.2 + Vector((0, 0, 2.1 * cs))
            cam.location = loc; cam.rotation_euler = kit.look_rot(tuple(loc), tuple(K + Vector((0, 0, hz))), 0.0)
            cam.data.lens = 35; cam.data.clip_start = 0.05
            for ob in bpy.data.objects:
                for con in ob.constraints:
                    if con.type == "TRACK_TO": con.target = cam
            cam["preset"] = "look"; cam["aspect"] = "9:16"; cam["focus"] = tuple(K + Vector((0, 0, 3.75 * cs)))
            cam["coc_k"] = 2.0; cam["coc_max"] = 12; cam["dof_k"] = 1.0
            bpy.context.view_layer.update()
            p0 = os.path.join(OUT, f"x_{kind}_{vn}")
            r = B.render6.render(p0, frame=7, post_opts={"exposure": 1.6, "sharp_idx": [2]})
            times[f"x_{kind}_{vn}"] = dict(cpu_render=r.get("cpu_render"), wall=r.get("wall_render"), cpu_post=r.get("cpu_post"))
            png = r["png"]; os.replace(png, p0 + ".png") if png != p0 + ".png" else None
            meta(sc, cam, ch, p0 + ".png")
            print("TIME", kind, vn, times[f"x_{kind}_{vn}"], flush=True)
    _times(times)


if __name__ == "__main__":
    cmd = sys.argv[1]; args = sys.argv[2:]
    only = args[args.index("--only") + 1].split(",") if "--only" in args else None
    spp = int(args[args.index("--spp") + 1]) if "--spp" in args else 32
    if cmd == "neutral": neutral(only, spp)
    elif cmd == "night": night(only)
    elif cmd == "extras":
        import extras7; extras7.run(args)
    elif cmd == "sheet":
        import sheet7; sheet7.main()
