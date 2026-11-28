"""look11.py -- the six v9 look stills (copy of v9/set/look9.py) in the v11 set (reference-E finish), re-cast with the
v8 2.5D paper puppets (v8/cast, imported read-only; whatever that folder currently draws).

python3 look11.py render [--only s06,s09] [--aspect 9:16] [--q final] [--scale 1.0]
python3 look11.py repost [--only ...] key=value ...      re-grade from the kept EXRs
python3 look11.py sheet                                  vs_refE.png: v9 | v11 | closest reference-E frame

Framings are look9's, with these v11 changes: the work lamp is placed with B.place_work_lamp_safe (never behind a
head); S18 is re-framed (driver bigger, bonnet <= 25 % of the frame) and dressed with B.pov_windscreen().
"""
import os, sys, json, math, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "look", "out")
V9OUT = os.path.join(PROJ, "v9", "set", "look", "out")
REF = {"s06": 60, "s09": 86, "s13": 84, "s18": 66, "s20": 5, "s24": 78}       # closest reference-E frames (frames2)
TITLE = {"s06": "S06 low hero MS", "s09": "S09 battery macro", "s13": "S13 phone MCU, OTS",
         "s18": "S18 POV windscreen", "s20": "S20 head lift, Dutch", "s24": "S24 high wide"}
SHOTS = ["s06", "s09", "s13", "s18", "s20", "s24"]
SPP_SHOT = {"s09": 4, "s24": 4}
KONG_H = 2.86; CREW_H = 2.80; DRV_H_SEATED = 2.03; DRV_HIP_Z = 1.12


def setup(q="final", threads=4):
    sys.path.insert(0, HERE); sys.path.append(os.path.join(PROJ, "v8", "cast"))
    import beauty as B
    A = B.build()
    B.setup_render(q, threads=threads)
    import bpy, stage8 as S
    bpy.context.scene.cycles.transparent_max_bounces = max(bpy.context.scene.cycles.transparent_max_bounces, 32)
    kong = S.Actor8("kong", "kong_wet", height=KONG_H)
    crew = S.Actor8("crew", "crew_wet", height=CREW_H)
    drv = S.Actor8("driver", "driver", height=DRV_H_SEATED)
    for a in (kong, crew, drv): a.set_pass_index(2)
    try:
        import phone8
        p = os.path.join(PROJ, "v8", "cast", "tex", "phone_screen.png")
        phone = phone8.data_uri(p) if os.path.exists(p) else None
    except Exception:
        phone = None
    return dict(A=A, B=B, S=S, kong=kong, crew=crew, drv=drv, phone=phone)


def facing(front):
    return math.degrees(math.atan2(front[0], -front[1]))


def camera(G, loc, look, lens, aspect, focus, k, kmax, roll=0.0, clip=0.05, keep_cutter=False):
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
        for ob in [cu] + list(cu.children_recursive): ob.hide_render = not keep_cutter
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


def windscreen_soft(G, on):
    import bpy
    m = bpy.data.materials.get("glass_hero")
    if m is None: return
    for n in m.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            if "s0" not in n: n["s0"] = n.inputs["Specular IOR Level"].default_value
            n.inputs["Specular IOR Level"].default_value = 0.05 if on else n["s0"]
        if n.type == "BSDF_GLOSSY":
            if "r0" not in n: n["r0"] = n.inputs["Roughness"].default_value
            n.inputs["Roughness"].default_value = 0.12 if on else n["r0"]
            if "c0" not in n: n["c0"] = list(n.inputs["Color"].default_value)
            n.inputs["Color"].default_value = [c * (0.22 if on else 1.0) for c in n["c0"][:3]] + [1.0]


def frame_dirs(A):
    from mathutils import Vector
    th = A["hero_heading"]
    return Vector((-math.sin(th), math.cos(th), 0.0)), Vector((math.cos(th), math.sin(th), 0.0))


def dominant_light(point, exclude=()):
    import bpy
    from mathutils import Vector
    best, bv = None, 0.0
    for ob in bpy.data.objects:
        if ob.type != "LIGHT" or ob.hide_render or ob.name in exclude or ob.name.startswith(("look_fill", "pov_")): continue
        d = ob.data
        if d.type == "SUN": e = d.energy * 1.0
        else:
            v = Vector(point) - ob.matrix_world.translation
            e = d.energy / (4 * math.pi * max(v.length_squared, 0.25)) * 0.05
            if d.type == "SPOT":
                ax = ob.matrix_world.to_3x3() @ Vector((0, 0, -1))
                if v.normalized().dot(ax) < math.cos(d.spot_size / 2): continue
        if e > bv: best, bv = ob, e
    return best


def stage_shadows(G, actors, point):
    import bpy
    bpy.context.view_layer.update()
    L = dominant_light(point)
    if L is not None:
        try: G["S"].shadow_link(actors, L)
        except Exception as ex: print("shadow_link failed", ex)
    return L


def shot(G, name, aspect):
    import bpy, presets
    from mathutils import Vector
    A = G["A"]; B = G["B"]; kong, crew, drv = G["kong"], G["crew"], G["drv"]
    fwd, right = frame_dirs(A)
    v = aspect == "9:16"
    for a in (kong, crew, drv): a.hide(False)
    drv.view_override = None
    if hasattr(drv, "pitch_override"): drv.pitch_override = 0.0      # seated in the car: the card stays upright in the seat
    K = Vector(A["kong_mark"]); seat = Vector(A["driver_seat"])
    hide_roots(G, []); door_glass(G, False); windscreen_soft(G, False)
    B.pov_windscreen(A, False)
    for nm in ("sodium_2_1", "sodium_2_-1", "moon_key", "flood_key"): B.practical(nm, 1.0)
    post = {"exposure": 1.6}
    fill(G, "look_fill_a"); fill(G, "look_fill_b")
    hz = 2.41
    drv.place(tuple(Vector((seat.x, seat.y, DRV_HIP_Z - (drv.spec["legs"] + 0.06) * drv.sc)) - fwd * 0.02), facing(fwd))
    drv_pose = dict(expr="still", legs=dict(seated=True), arm_r="lap", arm_l="lap", head=(0, 14, 0.0, 0.06), lean=6)
    crew.place(A["crew_mark"], facing(-(right * 0.9 + fwd * 0.4)))
    lamp = None; heads = []; acts = [kong, crew, drv]; key_pt = K + Vector((0, 0, 1.5))

    if name == "s06":
        to_cam = Vector((4.4, -8.4, 0)).normalized(); side = Vector((-to_cam.y, to_cam.x, 0))
        hide_roots(G, ["bike_a"])
        kong.place(tuple(K), facing(to_cam) - 25)
        if v: loc = K + to_cam * 3.4 + side * 0.30 + Vector((0, 0, 0.95)); look = K + Vector((0, 0, 1.65)) + side * 0.2
        else: loc = K + to_cam * 5.6 - side * 0.9 + Vector((0, 0, 0.95)); look = K + Vector((0, 0, 1.6)) - side * 1.55
        cam = camera(G, tuple(loc), tuple(look), 28, aspect, K + Vector((0, 0, hz)), 7.0, 22)
        kong.pose(dict(expr="determined", arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3, wet=True), legs="wide", head=(0, -6, 0, 0)), camera=cam)
        crew.pose(dict(expr="neutral"), camera=cam); drv.pose(drv_pose, camera=cam)
        presets.foreground(cam, "wheel", side="left", cover=0.38 if v else 0.24, depth=1.6)
        lamp = dict(base=tuple(K - to_cam * 5.5 + side * (5.2 if v else 6.5)), aim=tuple(K + Vector((0, 0, 1.0))), energy=9000.0)
        heads = [kong.head_world(), crew.head_world()]
        post["sharp_idx"] = [2]

    elif name == "s09":
        # macro on the 3D cutter's 3-bar gauge (the set prop Kong holds at the door); Kong soft behind
        hide_roots(G, ["bike_a"])
        cam = presets.use("macro", A, aspect=aspect, scale=G["scale"])
        to_cam = (Vector(cam.location) - K); to_cam.z = 0; to_cam.normalize()
        kong.place(tuple(K - to_cam * 0.9), facing(to_cam))
        kong.pose(dict(expr="tired", arm_n="down", legs="stand", head=(0, 8, 0, 0)), camera=cam)
        crew.hide(True); drv.pose(drv_pose, camera=cam)
        post["exposure"] = 1.5; acts = [kong, drv]

    elif name == "s13":
        P0 = Vector(A["kong_phone_mark"]); to_cam = Vector((0.12, -1.0, 0)).normalized(); side = Vector((-to_cam.y, to_cam.x, 0))
        kong.place(tuple(P0), facing(to_cam) + 22)
        hcen = P0 + Vector((0, 0, hz)); d = 3.0 if v else 3.3
        loc = hcen + to_cam * d + Vector((0, 0, 0.25)) - side * (0.15 if v else 0.85)
        look = hcen + Vector((0, 0, -0.40 if v else -0.20)) - side * (0.10 if v else 0.95)
        cpos = loc - to_cam * (1.25 if v else 1.35) - side * (0.48 if v else 0.30); cpos.z = -0.55
        crew.place(tuple(cpos), facing(-to_cam) + 15)
        cam = camera(G, tuple(loc), tuple(look), 30 if v else 32, aspect, hcen, 12.0, 24)
        pp = dict(type="phone", angle=0, scale=1.5)
        if G["phone"]: pp["screen"] = G["phone"]
        kong.pose(dict(expr="guilty", arm_n=dict(hand=(0.26, 0.10), elbow=None, hand_shape="grip"), prop_n=pp, head=(0, 10, 0.0, 0.04), lean=4), camera=cam)
        crew.pose(dict(expr="neutral"), camera=cam); drv.hide(True)
        lamp = dict(base=tuple(P0 - to_cam * 4.5 + side * 4.6), aim=tuple(P0 + Vector((0, 0, 1.2))), energy=9000.0)
        heads = [kong.head_world()]
        post["sharp_idx"] = []; acts = [kong, crew]; key_pt = P0 + Vector((0, 0, 1.5))

    elif name == "s18":
        # POV from the bonnet through the cracked windscreen. v11: closer and a little higher (bonnet <= 25 % of the
        # frame, driver's head ~0.3 W), bonnet dressed, cabin practicals, no work lamp behind the head.
        ws = Vector(A["windscreen"])
        drv.view_override = "front"
        loc = ws + fwd * (2.0 if v else 2.2) - right * 0.25
        hc0 = Vector(A["driver_head"])
        loc.z = hc0.z + 0.30
        cam0 = camera(G, tuple(loc), tuple(hc0), 48, aspect, hc0, 8.0, 18, clip=0.02)
        drv.pose(dict(expr="still", legs=dict(seated=True), arm_r="lap", arm_l="lap", head=(0, 10, 0.0, 0.05), lean=8), camera=cam0)
        hc = drv.head_world()
        look = hc + Vector((0, 0, -0.22 if v else -0.1)) - right * 0.05
        cam = camera(G, tuple(loc), tuple(look), 48 if v else 34, aspect, hc, 8.0, 18, clip=0.02)
        drv.pose(drv.last_pose, camera=cam)
        windscreen_soft(G, True)
        B.practical("sodium_2_1", 0.5); B.practical("sodium_2_-1", 0.5)
        B.pov_windscreen(A, True)
        lamp = dict(base=tuple(ws + fwd * 2.2 + right * 5.5), aim=tuple(ws + fwd * 1.2 + Vector((0, 0, -0.4))), energy=5000.0, head_z=2.3)
        fill(G, "look_fill_a", tuple(hc + fwd * 1.0 + Vector((0, 0, 0.15))), 170.0, (0.86, 0.92, 1.0), 0.3)
        heads = [hc]
        kong.hide(True); crew.hide(True)
        hide_roots(G, ["l2_b", "headlight_l2_b_-1", "headlight_l2_b_1", "cone_headlight_l2_b_-1", "cone_headlight_l2_b_1", "flood_beam"])
        post["exposure"] = 1.45; post["tilt"] = 1.0; post["vignette"] = 0.55; acts = [drv]; key_pt = hc

    elif name == "s20":
        drv.view_override = "q"
        hc0 = drv.world_of((0, -(drv.spec["legs"] + drv.spec["torso"] + 0.5)), 1.0)
        dm = Vector(A["door_mid"])
        loc = Vector((dm.x, dm.y, 0)) + right * (1.45 if v else 1.8) - fwd * (0.05 if v else 0.45) + Vector((0, 0, 2.05))
        cam0 = camera(G, tuple(loc), tuple(hc0), 26, aspect, hc0, 9.0, 22, roll=12.0)
        drv.pose(dict(expr="head_lift", legs=dict(seated=True), arm_r="lap", arm_l="wheel", head=(8, -10, 0, -0.02), lean=4, gaze=(0.6, -0.2)), camera=cam0)
        hc = drv.head_world()
        fill(G, "look_fill_a", tuple(hc + fwd * 0.8 + right * 0.1 + Vector((0, 0, -0.1))), 10.0, size=0.3)
        fill(G, "look_fill_b", tuple(hc + right * 1.0 - fwd * 0.2 + Vector((0, 0, 0.5))), 14.0, (0.72, 0.82, 1.0), 0.5)
        look = hc + right * 0.25 + Vector((0, 0, -0.15))
        cam = camera(G, tuple(loc), tuple(look), 26 if v else 28, aspect, hc, 9.0, 22, roll=12.0)
        drv.pose(drv.last_pose, camera=cam)
        kong.hide(True); crew.hide(True)
        door_glass(G, True)
        lamp = dict(base=tuple(Vector((dm.x, dm.y, 0)) + right * 2.6 + fwd * 3.8), aim=tuple(dm + right * 0.4 - fwd * 2.0), energy=3800.0, head_z=2.6)
        heads = [hc]
        post["exposure"] = 1.4; acts = [drv]; key_pt = hc

    elif name == "s24":
        kong.place(tuple(K), A["kong_to_door_deg"])
        if v: l0, t0, lens = Vector((3.8, 7.0, 13.0)), Vector((-8.6, 42.0, 0.0)), 45
        else: l0, t0, lens = Vector((5.5, 9.0, 12.5)), Vector((-8.8, 40.0, 0.0)), 38
        loc = K + (l0 - K) * 0.62; look = loc + (t0 - l0)
        cam = camera(G, tuple(loc), tuple(look), lens, aspect, K, 1.6, 10)
        kong.pose(dict(expr="determined", arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3, wet=True), legs="wide", lean=8), camera=cam)
        crew.pose(dict(expr="neutral"), camera=cam); drv.pose(drv_pose, camera=cam)
        lamp = dict(base=(-4.2, 37.6), aim=(-7.2, 32.5, 0.6), energy=8000.0)
        heads = [kong.head_world(), crew.head_world()]
        presets.foreground(cam, "pole", side="left", cover=0.08, depth=6.0)
        post["sharp_idx"] = [2]; post["exposure"] = 1.7
    else:
        raise KeyError(name)
    if lamp:
        hp, moved = B.place_work_lamp_safe(A, cam, heads, **lamp)
        post["_lamp_moved"] = moved
    else:
        B.place_work_lamp(A)
    post["_glare"] = B.glare_check(cam, heads)
    bpy.context.view_layer.update()
    stage_shadows(G, [a for a in acts], key_pt)
    return post


def render(only, aspects, q, scale, frame=7):
    G = setup(q); G["scale"] = scale
    times = {}
    os.makedirs(OUT, exist_ok=True)
    import bpy
    for asp in aspects:
        for n in only:
            post = shot(G, n, asp)
            print("STAGE", n, "lamp moved", post.pop("_lamp_moved", None), "glare", post.pop("_glare", None), flush=True)
            bpy.context.scene.cycles.samples = SPP_SHOT.get(n, G["B"].SPP.get(q, 6))
            tag = f"{n}_{'916' if asp == '9:16' else '169'}"
            gf = os.path.join(HERE, "look", "grade11.json")
            if os.path.exists(gf):
                post.update(json.load(open(gf)).get(tag, {}))
            r = G["B"].render6.render(os.path.join(OUT, tag), frame=frame, post_opts=post)
            times[tag] = dict(cpu_render=r.get("cpu_render"), cpu_render_total=r.get("cpu_render_total"), cpu_post=r.get("cpu_post"), wall_render=r.get("wall_render"))
            print("TIME", tag, times[tag], flush=True)
    tp = os.path.join(OUT, "times.json")
    old = json.load(open(tp)) if os.path.exists(tp) else {}
    old.update(times); json.dump(old, open(tp, "w"), indent=1)


def repost(only, kv):
    sys.path.insert(0, HERE)
    import beauty as B
    for n in only:
        tag = f"{n}_916"
        o = dict(kv)
        gf = os.path.join(HERE, "look", "grade11.json")
        if os.path.exists(gf):
            g = json.load(open(gf)).get(tag, {}); g.update(o); o = g
        print(B.render11.repost(os.path.join(OUT, tag), **o), o)


def sheet():
    from PIL import Image, ImageDraw, ImageFont
    try: f = ImageFont.truetype(os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), 20)
    except Exception: f = ImageFont.load_default()
    w, h, lab, gap = 405, 720, 30, 6
    tw = 3 * w + 2 * gap
    s = Image.new("RGB", (3 * tw + 2 * 24, 2 * (h + lab) + 20), (14, 14, 18)); d = ImageDraw.Draw(s)
    for i, n in enumerate(SHOTS):
        x = (i % 3) * (tw + 24); y = (i // 3) * (h + lab + 20)
        for j, (p, t) in enumerate(((os.path.join(V9OUT, f"{n}_916.png"), TITLE[n] + "  v9"), (os.path.join(OUT, f"{n}_916.png"), "v11"),
                                    (os.path.join(PROJ, "ref", "e", "frames2", f"f_{REF[n]:03d}.png"), f"ref E f_{REF[n]:03d}"))):
            d.text((x + j * (w + gap) + 4, y + 4), t, fill=(232, 232, 236) if j < 2 else (170, 170, 180), font=f)
            if os.path.exists(p): s.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (x + j * (w + gap), y + lab))
    s.save(os.path.join(HERE, "vs_refE.png"))
    print(os.path.join(HERE, "vs_refE.png"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode"); ap.add_argument("--only", default=",".join(SHOTS)); ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--q", default="final"); ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--frame", type=int, default=7)
    ap.add_argument("kv", nargs="*")
    a = ap.parse_args()
    if a.mode == "render": render(a.only.split(","), a.aspect.split(","), a.q, a.scale, a.frame)
    elif a.mode == "repost":
        kv = {}
        for x in a.kv:
            k, val = x.split("=")
            kv[k] = json.loads(val)
        repost(a.only.split(","), kv)
    elif a.mode == "sheet": sheet()
