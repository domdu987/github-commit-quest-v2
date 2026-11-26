"""lookdev.py -- v6 cast lookdev: neutral ground, soft light, 720x1280, front / 3/4 / side per character,
driver poses, expression strips, props, wet + night checks, numbers measured from the renders.

    python3 lookdev.py renders [--only kong,crew] [--spp 48] [--scale 1.0]
    python3 lookdev.py sheet          # -> lookdev.png (renders next to same-scale ref D crops + the character sheet)
    python3 lookdev.py measure        # -> out/measure.json
"""
import os, sys, math, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out"); TMP = os.path.join(HERE, "tmp")
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)

CAM_DIST = 7.6; CAM_Z = 1.75; LENS = 35.0


def scene(light="soft", spp=48, scale=1.0):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = spp
    sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2
    sc.cycles.transparent_max_bounces = 16; sc.cycles.sample_clamp_indirect = 3.0
    sc.render.threads_mode = "FIXED"; sc.render.threads = 4
    sc.render.resolution_x = 720; sc.render.resolution_y = 1280; sc.render.resolution_percentage = int(scale * 100)
    sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
    sc.render.image_settings.file_format = "PNG"
    import cast6 as C
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    cam_d = bpy.data.cameras.new("cam"); cam_d.lens = LENS; cam_d.sensor_fit = "AUTO"; cam_d.sensor_width = 36
    cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
    cam.location = (0, -CAM_DIST, CAM_Z); cam.rotation_euler = (math.radians(90), 0, 0)
    gm = bpy.data.meshes.new("ground")
    gm.from_pydata([(-900, -900, 0), (900, -900, 0), (900, 900, 0), (-900, 900, 0)], [], [(0, 1, 2, 3)])
    g = bpy.data.objects.new("ground", gm); sc.collection.objects.link(g)
    if light == "soft":
        bg.inputs[0].default_value = C.hexlin("#9fb2cf"); bg.inputs[1].default_value = 0.75
        gm.materials.append(C.m_matte("ground", "#9a9792", rough=0.9, spec=0.2))
        kd = bpy.data.lights.new("key", "AREA"); kd.shape = "DISK"; kd.size = 5.0; kd.energy = 1000
        kd.color = (1.0, 0.95, 0.88)
        k = bpy.data.objects.new("key", kd); sc.collection.objects.link(k)
        k.location = (-5.5, -6.5, 7.0)
        _aim(k, (0, 0, 1.8))
        rd = bpy.data.lights.new("rim", "AREA"); rd.size = 4.0; rd.energy = 500; rd.color = (0.80, 0.86, 1.0)
        r = bpy.data.objects.new("rim", rd); sc.collection.objects.link(r); r.location = (5, 6, 5); _aim(r, (0, 0, 2))
    else:   # night: sodium key, moon back light, blue sky fill (v6 beauty spec numbers, simplified)
        bg.inputs[0].default_value = C.hexlin("#33415e"); bg.inputs[1].default_value = 0.45
        gm.materials.append(C.m_matte("ground", "#2a2c31", rough=0.25, spec=0.5))
        sd = bpy.data.lights.new("sodium", "SPOT"); sd.energy = 2200; sd.color = (1.0, 0.62, 0.30)
        sd.spot_size = math.radians(80); sd.shadow_soft_size = 0.4
        s = bpy.data.objects.new("sodium", sd); sc.collection.objects.link(s); s.location = (-4, -3, 8); _aim(s, (0, 0, 1.5))
        md = bpy.data.lights.new("moon", "SUN"); md.energy = 2.5; md.angle = math.radians(3); md.color = (0.62, 0.74, 1.0)
        m = bpy.data.objects.new("moon", md); sc.collection.objects.link(m); m.location = (2, 10, 10); _aim(m, (0, 0, 0))
    return sc, cam


def _aim(ob, tgt):
    from mathutils import Vector
    d = Vector(tgt) - ob.location
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def frame_cam(cam, center_z=1.75, dist=CAM_DIST, height=CAM_Z, tilt=0.0, lens=LENS, x=0.0):
    cam.location = (x, -dist, height)
    cam.rotation_euler = (math.radians(90 + tilt), 0, 0)
    cam.data.lens = lens


def render(sc, path):
    import bpy
    sc.render.filepath = path
    t = time.time(); bpy.ops.render.render(write_still=True); return time.time() - t


def proj(sc, cam, p):
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    v = world_to_camera_view(sc, cam, Vector(p))
    W = sc.render.resolution_x * sc.render.resolution_percentage / 100
    H = sc.render.resolution_y * sc.render.resolution_percentage / 100
    return (v.x * W, (1 - v.y) * H)


def luma(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def patch(img, xy, r=4):
    x, y = int(round(xy[0])), int(round(xy[1]))
    p = img[max(0, y - r):y + r + 1, max(0, x - r):x + r + 1, :3].reshape(-1, 3)
    return np.median(p, axis=0)


def measure_front(sc, cam, ch, png):
    """numbers from a front render: head px D, ink px, head falloff, body falloff, limb L."""
    from PIL import Image
    from mathutils import Vector
    img = np.asarray(Image.open(png).convert("RGB")).astype(np.float32)
    hw = ch.head.matrix_world
    c = hw @ Vector((0, 0, 0))
    cx, cy = proj(sc, cam, c); ex, _ = proj(sc, cam, c + Vector((0.5, 0, 0)))
    Dpx = 2 * abs(ex - cx)
    def sph(th, ph, r=0.5):
        th, ph = math.radians(th), math.radians(ph)
        return hw @ Vector((r * math.cos(ph) * math.sin(th), -r * 0.97 * math.cos(ph) * math.cos(th), r * 0.98 * math.sin(ph)))
    lit = patch(img, proj(sc, cam, sph(-50, -12))); sh = patch(img, proj(sc, cam, sph(58, -12)))
    Ll, Ls = float(luma(lit)), float(luma(sh))
    # ink: walk left from the head's left silhouette at the centre row
    # ink FWHM (sub-pixel) on the head's left edge, on the row through the chin band (below the hair)
    ry = int(proj(sc, cam, sph(-90, -28))[1])
    row = luma(img[ry]); xs = int(proj(sc, cam, sph(-60, -28))[0])
    xmin = int(np.argmin(row[max(0, xs - 60):xs])) + max(0, xs - 60)
    Lk = row[xmin]; Lin = np.median(row[xmin + 6:xmin + 14]); Lout = np.median(row[xmin - 14:xmin - 6])
    def cross(level, step):
        x = xmin
        while 0 < x < len(row) - 1 and row[x + step] < level: x += step
        a, b = row[x], row[x + step]
        return x + step * ((level - a) / (b - a) if b != a else 0)
    n = round(float(cross((Lk + Lin) / 2, 1) - cross((Lk + Lout) / 2, -1)), 2)
    # body: bean at mid height, lit vs shadow side
    cfg = ch.cfg; zb = cfg["z0"] + 0.40 * cfg["bean_h"]
    import cast6 as C
    rb = C.bean_r(cfg, zb)
    bw = ch.bean.matrix_world
    def bp(a):
        a = math.radians(a); return bw @ Vector((rb * math.sin(a), -rb * cfg["sy"] * math.cos(a), zb))
    bl = patch(img, proj(sc, cam, bp(-55)), 3); bs = patch(img, proj(sc, cam, bp(62)), 3)
    # legs: sample pixels along the right leg curve
    pts = [b.co for b in ch.limbs["leg_r"].data.splines[0].bezier_points]
    rw = ch.root.matrix_world
    Ls_ = []
    for t in np.linspace(0.15, 0.85, 40):
        p = pts[0].lerp(pts[2], t) if t else pts[0]
        q = proj(sc, cam, rw @ p)
        Ls_.append(float(luma(img[int(q[1]), int(q[0])])))
    hd = proj(sc, cam, ch.hands["l"].matrix_world.translation)
    hand = img[int(hd[1]) - 3:int(hd[1]) + 4, int(hd[0]) - 3:int(hd[0]) + 4]
    crown = proj(sc, cam, hw @ Vector((0, 0, 0.49)))[1]
    sole = proj(sc, cam, rw @ Vector((0, 0, 0)))[1]
    return dict(head_D_px=round(Dpx, 1), ink_px=n, ink_pct_D=round(100 * n / Dpx, 2), ink_L=round(float(Lk), 1),
                head_lit_rgb=[int(v) for v in lit], head_shadow_rgb=[int(v) for v in sh],
                head_drop_pct=round(100 * (1 - Ls / Ll), 1),
                body_lit_rgb=[int(v) for v in bl], body_shadow_rgb=[int(v) for v in bs],
                body_drop_pct=round(100 * (1 - float(luma(bs)) / float(luma(bl))), 1),
                leg_L_median=round(float(np.median(Ls_)), 1), leg_L_p95=round(float(np.percentile(Ls_, 95)), 1),
                hand_L_max=round(float(luma(hand).max()), 1),
                figure_px=round(sole - crown, 1), figure_frac_H=round((sole - crown) / img.shape[0], 3))


def renders(only=None, spp=48, scale=1.0):
    import bpy
    sys.path.insert(0, HERE)
    import cast6 as C
    res = {}
    sc, cam = scene("soft", spp, scale)
    chars = {}
    for kind in ("kong", "crew", "driver"):
        chars[kind] = C.Character(kind)
    cut = C.Cutter(bars=3, scale=1.3); chars["kong"].hold(cut, "r", fwd=(0.0, -0.3, -1.0), up=(0, -1, 0.3))
    def show(kind):
        for k, ch in chars.items():
            for ob in ch.objects: ob.hide_render = (k != kind)
            if k == kind: ch.set_face(ch.expr)
        for ob in cut.objects: ob.hide_render = kind != "kong"
    views = [("front", 0), ("q", -40), ("side", -90)]
    for kind, ch in chars.items():
        if only and kind not in only: continue
        show(kind)
        ch.place((0, 0, 0), 0)
        ch.preset({"kong": "kong_hold_cutter", "crew": "crew_idle", "driver": "driver_stand"}[kind])
        for vn, f in views:
            ch.place((0, 0, 0), f)
            frame_cam(cam)
            p = os.path.join(OUT, f"ld_{kind}_{vn}.png")
            t = render(sc, p)
            res[f"{kind}_{vn}_sec"] = round(t, 1)
            if vn == "front":
                res[kind] = measure_front(sc, cam, ch, p)
                res[kind]["proportions"] = ch.proportions()
            print(kind, vn, round(t, 1), flush=True)
    json.dump(res, open(os.path.join(OUT, "measure_%s.json" % ("_".join(only) if only else "all")), "w"), indent=1)
    return res


def extras(spp=32, parts=("driver", "wet", "faces", "props", "night")):
    """driver poses (seated / head-lift / lunge), Kong wet, expression heads, props, a night check."""
    import bpy
    import cast6 as C
    from mathutils import Vector
    res = {}
    if "driver" in parts:
        # ---------------- driver poses, seat stand-in (a grey box seat + wheel) at 3/4
        sc, cam = scene("soft", spp)
        d = C.Character("driver")
        seatm = C.m_matte("seat", "#5d6068", rough=0.8, spec=0.2)
        seat = C._obj("seat", None, C.coll("SEAT")); seat.rotation_euler = (0, 0, math.radians(-35))
        for nm, size, loc in (("cush", (1.3, 1.0, 0.25), (0, 0.10, 0.50)), ("back", (1.3, 0.25, 1.5), (0, 0.65, 1.30))):
            me = C._rbox(nm, size, 0.08); me.materials.append(seatm)
            C._obj(nm, me, C.coll("SEAT"), seat, loc)
        for nm in ("driver_seated", "driver_head_lift", "driver_lunge"):
            d.preset(nm); d.place((0, 0, 0), -35)
            frame_cam(cam, dist=7.6, height=1.6)
            p = os.path.join(OUT, f"ld_{nm}.png"); res[nm + "_sec"] = round(render(sc, p), 1); print(nm, flush=True)
    if "wet" in parts:
        # ---------------- Kong wet (front + 3/4), cutter 2 bars
        sc, cam = scene("soft", spp)
        k = C.Character("kong", wet=True, expr="tired")
        cut = C.Cutter(bars=2, wet=True, scale=1.3); k.hold(cut, "r", fwd=(0.0, -0.3, -1.0), up=(0, -1, 0.3))
        k.preset("kong_hold_cutter"); k.set_face("tired")
        for vn, f in (("front", 0), ("q", -40)):
            k.place((0, 0, 0), f); frame_cam(cam)
            p = os.path.join(OUT, f"ld_kong_wet_{vn}.png"); res["kong_wet_" + vn + "_sec"] = round(render(sc, p), 1)
    if "faces" in parts:
        # ---------------- expression heads (MCU, 320x320, head turned 18 deg so the decal wraps)
        sc, cam = scene("soft", spp)
        sc.render.resolution_x = sc.render.resolution_y = 320
        chars = {kk: C.Character(kk) for kk in ("kong", "crew", "driver")}
        import faces6 as F
        for kk, ch in chars.items():
            for ob in ch.objects: ob.hide_render = True
        for kk, ch in chars.items():
            for ob in ch.objects: ob.hide_render = False
            ch.place((0, 0, 0), 0); ch.pose(head=(-18, 0, 0))
            hz = ch.head.matrix_world.translation.z
            for e in F.EXPRS[kk]:
                if e == "blink": continue
                ch.set_face(e)
                cam.location = (0, -3.2, hz + 0.05); cam.rotation_euler = (math.radians(90), 0, 0); cam.data.lens = 50
                p = os.path.join(TMP, f"face_{kk}_{e}.png"); render(sc, p)
            for ob in ch.objects: ob.hide_render = True
            ch.sweat.hide_render = True
    if "props" in parts:
        # ---------------- props: cutter 3/2/1 + phone
        sc, cam = scene("soft", spp)
        sc.render.resolution_x = 1280; sc.render.resolution_y = 720
        for i, b in enumerate((3, 2, 1)):
            cu = C.Cutter(name=f"cut{b}", bars=b)
            cu.root.location = (-1.25 + i * 0.75, 0, 0.55); cu.root.rotation_euler = (math.radians(-25), 0, math.radians(-70))
        ph = C.Phone()
        ph.root.location = (0.95, -0.3, 0.45); ph.root.rotation_euler = (math.radians(-12), 0, math.radians(8))
        ph.root.scale = (2.2,) * 3
        cam.location = (-0.1, -3.6, 1.55); cam.rotation_euler = (math.radians(72), 0, 0); cam.data.lens = 42
        p = os.path.join(OUT, "ld_props.png"); res["props_sec"] = round(render(sc, p), 1)
    if "night" in parts:
        # ---------------- night check: sodium key + moon back light + blue sky fill, Kong front
        sc, cam = scene("night", spp)
        k = C.Character("kong", wet=True, expr="alarmed", separator=True)
        cut = C.Cutter(bars=1, wet=True, scale=1.3); k.hold(cut, "r", fwd=(0.0, -0.3, -1.0), up=(0, -1, 0.3))
        k.preset("kong_hold_cutter"); k.set_face("alarmed"); k.place((0, 0, 0), -20)
        frame_cam(cam)
        p = os.path.join(OUT, "ld_kong_night.png"); res["night_sec"] = round(render(sc, p), 1)
        k.place((0, 0, 0), 0); p2 = os.path.join(TMP, "night_front.png"); render(sc, p2)
        res["night"] = measure_front(sc, cam, k, p2)
    old = {}
    pm = os.path.join(OUT, "measure_extras.json")
    if os.path.exists(pm): old = json.load(open(pm))
    old.update(res); res = old
    json.dump(res, open(os.path.join(OUT, "measure_extras.json"), "w"), indent=1)
    return res


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "renders"
    args = sys.argv[2:]
    only = None; spp = 48; scale = 1.0
    if "--only" in args: only = args[args.index("--only") + 1].split(",")
    if "--spp" in args: spp = int(args[args.index("--spp") + 1])
    if "--scale" in args: scale = float(args[args.index("--scale") + 1])
    if cmd == "renders":
        print(json.dumps(renders(only, spp, scale), indent=1))
    elif cmd == "extras":
        parts = args[args.index("--parts") + 1].split(",") if "--parts" in args else ("driver", "wet", "faces", "props", "night")
        print(json.dumps(extras(spp, parts), indent=1))
