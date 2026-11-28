"""look8.py -- v6/look/look.py copied and re-cast: three v6 look shots (S06 low hero, S13 phone, S20 head lift) with
the v8 sheet-style 2.5D puppets in place of the v6 bean characters.  Set, lights, cameras, post: unchanged
(same marks, same camera formulas, same post_opts as v6 look.py).

python3 look8.py render [--only s06,s13,s20] [--aspect 9:16] [--scale 1.0] [--q final]
python3 look8.py sheet        -> in_v6.png  (v6 frame | v8 frame, per shot)
"""
import os, sys, json, math, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out", "look")
V6OUT = os.path.join(PROJ, "v6", "look", "out")
TITLE = {"s06": "S06 low hero MS (T4/T5)", "s13": "S13 phone MCU, OTS (T4)", "s20": "S20 head lift, Dutch"}
SHOTS = ["s06", "s13", "s20"]
KONG_H = 2.86          # BU (1.72 m) = the v6 set's Kong height (look.py: 3.49 D x 0.82)
CREW_H = 2.80
DRV_H_SEATED = 2.03    # the seated driver is drawn smaller so his head stays under the sedan's roof (v6: DRV_S 0.58)
DRV_HIP_Z = 1.12       # hip z on the cushion (cushion top 1.29, sunk)


def setup(q="final", threads=4):
    sys.path.insert(0, os.path.join(PROJ, "v6", "set")); sys.path.insert(0, HERE)
    import beauty as B
    A = B.build()
    B.setup_render(q, threads=threads)
    import bpy, stage8 as S
    bpy.context.scene.cycles.transparent_max_bounces = max(bpy.context.scene.cycles.transparent_max_bounces, 32)
    phone = phone_uri()
    kong = S.Actor8("kong", "kong_wet", height=KONG_H)
    crew = S.Actor8("crew", "crew_wet", height=CREW_H)
    drv = S.Actor8("driver", "driver", height=DRV_H_SEATED)
    for a in (kong, crew, drv):
        a.set_pass_index(2)
    G = dict(A=A, B=B, S=S, kong=kong, crew=crew, drv=drv, phone=phone)
    return G


def phone_uri():
    import phone8
    p = os.path.join(HERE, "tex", "phone_screen.png")
    if not os.path.exists(p):
        phone8.screen_png(p)
    return phone8.data_uri(p)


def _vec(*a):
    from mathutils import Vector
    return Vector(a if len(a) > 1 else a[0])


def facing(front):
    return math.degrees(math.atan2(front[0], -front[1]))


def camera(G, loc, look, lens, aspect, focus, k, kmax, roll=0.0, clip=0.05):
    import bpy
    B = G["B"]; X = B.X; import kit, presets
    sc = bpy.context.scene
    cam = X.make_camera()
    cam.location = loc
    cam.rotation_euler = kit.look_rot(loc, look, roll)
    cam.data.lens = lens; cam.data.clip_start = clip
    rx, ry = (720, 1280) if aspect == "9:16" else (1280, 720)
    sc.render.resolution_x, sc.render.resolution_y = int(rx * G["scale"]), int(ry * G["scale"])
    sc.render.resolution_percentage = X._STATE.get("pct", 100)
    for ob in bpy.data.objects:
        for con in ob.constraints:
            if con.type == "TRACK_TO": con.target = cam
    cu = bpy.data.objects.get("cutter3d")
    if cu:
        for ob in [cu] + list(cu.children_recursive): ob.hide_render = True
    cam["preset"] = "look"; cam["aspect"] = aspect
    cam["focus"] = tuple(focus); cam["coc_k"] = k; cam["coc_max"] = kmax; cam["dof_k"] = 1.0
    presets.clear_foreground()
    bpy.context.view_layer.update()
    return cam


def hide_roots(G, roots):
    import bpy
    for ob in G.get("_hid", []): ob.hide_render = False
    hid = []
    for r in roots:
        ob = bpy.data.objects.get(r)
        if not ob: continue
        for o in [ob] + list(ob.children_recursive):
            if not o.hide_render: o.hide_render = True; hid.append(o)
    G["_hid"] = hid


def fill(G, name, loc=None, power=0.0, color=(0.72, 0.82, 1.0), size=0.5):
    import bpy
    ob = bpy.data.objects.get(name)
    if ob is None:
        ld = bpy.data.lights.new(name, "POINT"); ob = bpy.data.objects.new(name, ld); bpy.context.scene.collection.objects.link(ob)
    ob.data.energy = power; ob.data.color = color; ob.data.shadow_soft_size = size
    ob.hide_render = power <= 0
    if loc is not None: ob.location = loc
    ob.visible_glossy = False; ob.visible_transmission = False; ob.visible_camera = False
    return ob


def door_glass(G, clear):
    import bpy
    obs = [bpy.data.objects.get(G["A"]["hero_car"] + n) for n in ("_door_fr", "_body")]
    if "glass_orig" not in G:
        G["glass_orig"] = {o.name: [m.name for m in o.data.materials] for o in obs}
        m = bpy.data.materials.new("look_no_glass"); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        o = nt.nodes.new("ShaderNodeOutputMaterial"); t = nt.nodes.new("ShaderNodeBsdfTransparent")
        nt.links.new(t.outputs[0], o.inputs[0])
        G["no_glass"] = m
    for door in obs:
        for i, nm in enumerate(G["glass_orig"][door.name]):
            if nm.startswith("glass"):
                door.data.materials[i] = G["no_glass"] if clear else bpy.data.materials[nm]


def frame_dirs(A):
    th = A["hero_heading"]
    fwd = _vec(-math.sin(th), math.cos(th), 0.0); right = _vec(math.cos(th), math.sin(th), 0.0)
    return fwd, right


def head_z():
    return 2.41       # v8 Kong head centre above the soles (3.63 D x 0.664); v6 used 2.46


def dominant_light(point, exclude=()):
    """the light that puts the most direct irradiance on `point` (spots inside their cone, the moon sun)."""
    import bpy
    from mathutils import Vector
    best, bv = None, 0.0
    for ob in bpy.data.objects:
        if ob.type != "LIGHT" or ob.hide_render or ob.name in exclude or ob.name.startswith("look_fill"):
            continue
        d = ob.data
        if d.type == "SUN":
            e = d.energy * 1.0
        else:
            v = Vector(point) - ob.matrix_world.translation
            r2 = max(v.length_squared, 0.25)
            e = d.energy / (4 * math.pi * r2) * 0.05
            if d.type == "SPOT":
                ax = ob.matrix_world.to_3x3() @ Vector((0, 0, -1))
                if v.normalized().dot(ax) < math.cos(d.spot_size / 2):
                    continue
        if e > bv:
            best, bv = ob, e
    return best


def stage_shadows(G, actors, point):
    S = G["S"]
    L = dominant_light(point)
    if L is not None:
        S.shadow_link(actors, L)
    return L


# ------------------------------------------------------------------------------------------------------- shots
def shot(G, name, aspect):
    import bpy, presets
    from mathutils import Vector
    A = G["A"]; kong, crew, drv = G["kong"], G["crew"], G["drv"]
    fwd, right = frame_dirs(A)
    v = aspect == "9:16"
    for a in (kong, crew, drv): a.hide(False)
    K = Vector(A["kong_mark"]); seat = Vector(A["driver_seat"])
    hide_roots(G, [])
    door_glass(G, False)
    post = {"exposure": 1.6}
    fill(G, "look_fill_a"); fill(G, "look_fill_b")
    hz = head_z()
    drv.place(tuple(Vector((seat.x, seat.y, DRV_HIP_Z - (drv.spec["legs"] + 0.06) * drv.sc)) - fwd * 0.02), facing(fwd))
    drv_pose = dict(expr="still", legs=dict(seated=True), arm_r="lap", arm_l="lap", head=(0, 14, 0.0, 0.06), lean=6)
    crew.place(A["crew_mark"], facing(-(right * 0.9 + fwd * 0.4)))
    crew_pose = dict(expr="neutral")

    if name == "s06":
        to_cam = (Vector((4.4, -8.4, 0))).normalized()
        hide_roots(G, ["bike_a"])
        kong.place(tuple(K), facing(to_cam) - 25)
        side = Vector((-to_cam.y, to_cam.x, 0))
        loc = K + to_cam * 3.4 + side * 0.30 + Vector((0, 0, 0.95)); look = K + Vector((0, 0, 1.65)) + side * 0.2
        cam = camera(G, tuple(loc), tuple(look), 28, aspect, K + Vector((0, 0, hz)), 7.0, 22)
        kong.pose(dict(expr="determined", arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3, wet=True), legs="wide",
                       head=(0, -6, 0, 0)), camera=cam)
        crew.pose(crew_pose, camera=cam)
        drv.pose(drv_pose, camera=cam)
        presets.foreground(cam, "wheel", side="left", cover=0.38 if v else 0.24, depth=1.6)
        post["sharp_idx"] = [2]
        stage_shadows(G, [kong, crew, drv], K + Vector((0, 0, 1.5)))

    elif name == "s13":
        P0 = Vector(A["kong_phone_mark"])
        to_cam = Vector((0.12, -1.0, 0)).normalized()
        side = Vector((-to_cam.y, to_cam.x, 0))
        kong.place(tuple(P0), facing(to_cam) + 22)
        hcen = P0 + Vector((0, 0, hz))
        d = 3.0
        loc = hcen + to_cam * d + Vector((0, 0, 0.25)) - side * 0.15
        look = hcen + Vector((0, 0, -0.40)) - side * 0.10
        cpos = loc - to_cam * 1.25 - side * 0.48; cpos.z = -0.55
        crew.place(tuple(cpos), facing(-to_cam) + 15)
        cam = camera(G, tuple(loc), tuple(look), 30, aspect, hcen, 12.0, 24)
        kong.pose(dict(expr="guilty", arm_n=dict(hand=(0.26, 0.10), elbow=None, hand_shape="grip"),
                       prop_n=dict(type="phone", screen=G["phone"], angle=0, scale=1.5), head=(0, 10, 0.0, 0.04), lean=4), camera=cam)
        crew.pose(dict(expr="neutral"), camera=cam)
        drv.hide(True)
        post["sharp_idx"] = []
        stage_shadows(G, [kong, crew], P0 + Vector((0, 0, 1.5)))

    elif name == "s20":
        drv.view_override = "q"
        hc0 = drv.world_of((0, -(drv.spec["legs"] + drv.spec["torso"] + 0.5)), 1.0)
        dm = Vector(A["door_mid"])
        loc = Vector((dm.x, dm.y, 0)) + right * (1.45 if v else 1.8) - fwd * (0.05 if v else 0.45) + Vector((0, 0, 2.05))
        cam0 = camera(G, tuple(loc), tuple(hc0), 26, aspect, hc0, 9.0, 22, roll=12.0)
        drv.pose(dict(expr="head_lift", legs=dict(seated=True), arm_r="lap", arm_l="wheel", head=(8, -10, 0, -0.02), lean=4,
                      gaze=(0.6, -0.2)), camera=cam0)
        hc = drv.head_world()
        fill(G, "look_fill_a", tuple(hc + fwd * 0.8 + right * 0.1 + Vector((0, 0, -0.1))), 10.0, size=0.3)
        fill(G, "look_fill_b", tuple(hc + right * 1.0 - fwd * 0.2 + Vector((0, 0, 0.5))), 18.0, (0.72, 0.82, 1.0), 0.5)
        look = hc + right * 0.25 + Vector((0, 0, -0.15))
        cam = camera(G, tuple(loc), tuple(look), 26 if v else 28, aspect, hc, 9.0, 22, roll=12.0)
        drv.pose(drv.last_pose, camera=cam)
        kong.hide(True); crew.hide(True)
        door_glass(G, True)
        stage_shadows(G, [drv], hc)
    else:
        raise KeyError(name)
    bpy.context.view_layer.update()
    return post


def render(only, aspects, q, scale, frame=7):
    G = setup(q); G["scale"] = scale
    times = {}
    os.makedirs(OUT, exist_ok=True)
    for asp in aspects:
        for n in only:
            t0 = time.time()
            post = shot(G, n, asp)
            t1 = time.time()
            tag = f"{n}_{'916' if asp == '9:16' else '169'}"
            r = G["B"].render6.render(os.path.join(OUT, tag), frame=frame, post_opts=post)
            times[tag] = dict(cpu_render=r.get("cpu_render"), cpu_render_total=r.get("cpu_render_total"), cpu_post=r.get("cpu_post"),
                              wall_render=r.get("wall_render"), wall_pose_raster=round(t1 - t0, 2),
                              res=[G["B"].X.bpy.context.scene.render.resolution_x if hasattr(G["B"].X, "bpy") else None])
            print("TIME", tag, times[tag], flush=True)
    tp = os.path.join(OUT, "times.json")
    old = json.load(open(tp)) if os.path.exists(tp) else {}
    old.update(times); json.dump(old, open(tp, "w"), indent=1)


def sheet():
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype(os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), 22)
    w, h, lab = 540, 960, 36
    s = Image.new("RGB", (3 * (2 * w + 12) + 2 * 30, h + lab + 10), (14, 14, 18)); d = ImageDraw.Draw(s)
    for i, n in enumerate(SHOTS):
        x = i * (2 * w + 12 + 30)
        d.text((x + 4, 6), "v6 (approved) " + TITLE[n], fill=(170, 170, 180), font=f)
        d.text((x + w + 16, 6), "v8 sheet puppets", fill=(240, 240, 240), font=f)
        a = Image.open(os.path.join(V6OUT, f"{n}_916.png")).convert("RGB").resize((w, h), Image.LANCZOS)
        s.paste(a, (x, lab))
        p = os.path.join(OUT, f"{n}_916.png")
        if os.path.exists(p):
            s.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (x + w + 12, lab))
    s.save(os.path.join(HERE, "in_v6.png"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode"); ap.add_argument("--only", default=",".join(SHOTS)); ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--q", default="final"); ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--frame", type=int, default=7)
    a = ap.parse_args()
    if a.mode == "render":
        render(a.only.split(","), a.aspect.split(","), a.q, a.scale, a.frame)
    elif a.mode == "sheet":
        sheet()
