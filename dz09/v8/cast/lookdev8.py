"""lookdev8.py -- lookdev renders and the lookdev.png / side_by_side.png sheets.

python3 lookdev8.py neutral      # Cycles, neutral stage: turnarounds, expressions, mouths, props, driver poses, extras
python3 lookdev8.py night        # inside the v6 set at night, camera with the moon behind it (no moon behind heads)
python3 lookdev8.py sheet        # lookdev.png
python3 lookdev8.py sbs          # side_by_side.png (sheet crop | our front render, same total height)
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
LD = os.path.join(HERE, "out", "lookdev")
TIMES = {}

TURN = [("front", 0.0), ("q", -36.0), ("side", -72.0)]
EXPRS = {"kong": ["determined", "tired", "guilty", "alarmed", "shouting", "blink"], "crew": ["neutral", "shouting", "scared", "blink"],
         "driver": ["still", "head_lift", "lunge", "bite"]}
MOUTH_LEVELS = [0.0, 0.25, 0.5, 0.75, 1.0]


def _render(path):
    import bpy
    t0 = time.time()
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    TIMES[os.path.basename(path)] = round(time.time() - t0, 2)


def _ortho(cam, center, scale):
    from mathutils import Vector
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = scale
    cam.location = Vector(center) + Vector((0, -20, 0))
    cam.rotation_euler = (math.radians(90), 0, 0)


def neutral():
    import bpy, neutral8 as N, stage8 as S, draw8
    os.makedirs(LD, exist_ok=True)
    N.reset()
    L = N.build(res=(480, 800), samples=24)
    cam = N.camera((0, -20, 1.4), (0, 0, 1.4), 50, ortho=3.4)
    actors = {}

    def actor(nm, spec, h=2.86):
        if nm not in actors:
            actors[nm] = S.Actor8(nm, spec, height=h, ppd=240)
        for k, a in actors.items():
            a.hide(k != nm)
        return actors[nm]

    S.tune(AMB=0.30)
    # turnarounds (dry and wet Kong, crew, driver)
    for nm, spec in (("kong", "kong"), ("kong_wet", "kong_wet"), ("crew", "crew"), ("driver", "driver")):
        a = actor(nm, spec)
        S.shadow_link([a], L["key"])
        for v, fac in TURN:
            a.place((0, 0, 0), fac)
            pose = {}
            if nm.startswith("kong") and v == "front":
                pose = dict(arm_r="hold_cutter", prop_r=dict(type="cutter", bars=3, wet=nm.endswith("wet")))
            a.pose(pose, camera=cam)
            _ortho(cam, (0, 0, 1.45), 3.3)
            _render(os.path.join(LD, "turn_%s_%s.png" % (nm, v)))
    # expressions (head close-ups), mouth levels, blink
    bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y = (360, 360)
    for nm, spec in (("kong", "kong"), ("crew", "crew"), ("driver", "driver")):
        a = actor(nm, spec)
        a.place((0, 0, 0), 0)
        for e in EXPRS[nm]:
            a.pose(dict(expr=e, blink=2 if e == "blink" else 0), camera=cam)
            _ortho(cam, a.head_world(), 1.15)
            _render(os.path.join(LD, "expr_%s_%s.png" % (nm, e)))
    a = actor("kong", "kong")
    for lv in MOUTH_LEVELS:
        a.pose(dict(expr="neutral", mouth=lv), camera=cam)
        _ortho(cam, a.head_world(), 1.15)
        _render(os.path.join(LD, "mouth_kong_%03d.png" % int(lv * 100)))
    # props: cutter bars 3/2/1 (hand close-ups), phone with the Thai screen
    import phone8
    pp = os.path.join(HERE, "tex", "phone_screen.png")
    if not os.path.exists(pp):
        phone8.screen_png(pp)
    uri = phone8.data_uri(pp)
    bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y = (360, 560)
    for bars in (3, 2, 1):
        a.pose(dict(expr="determined", arm_r="hold_cutter", prop_r=dict(type="cutter", bars=bars)), camera=cam)
        c = a.world_of(a.fig["anchors"]["prop_R"], 2.3)
        _ortho(cam, c + __import__("mathutils").Vector((0, 0, -0.30)), 1.05)
        _render(os.path.join(LD, "prop_cutter_%d.png" % bars))
    a.pose(dict(expr="guilty", arm_r=dict(hand=(-0.12, 0.42), hand_shape="grip"), prop_r=dict(type="phone", screen=uri, scale=1.3)), camera=cam)
    c = a.world_of(a.fig["anchors"]["prop_R"], 2.3)
    _ortho(cam, c + __import__("mathutils").Vector((0, 0, 0.05)), 0.75)
    _render(os.path.join(LD, "prop_phone.png"))
    _ortho(cam, a.world_of((0, -2.9), 0) , 2.2)
    _render(os.path.join(LD, "prop_phone_mcu.png"))
    # driver poses (full figure, q view)
    bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y = (480, 800)
    a = actor("driver", "driver")
    a.place((0, 0, 0), -36)
    dp = {"seated_still": dict(expr="still", legs=dict(seated=True), arm_r="lap", arm_l="lap", head=(0, 16, 0, 0.06), lean=8),
          "head_lift": dict(expr="head_lift", legs=dict(seated=True), arm_r="lap", arm_l="wheel", head=(8, -10, 0, -0.02), lean=2),
          "lunge": dict(expr="lunge", legs="lunge", arm_n="claw", arm_f="claw_up", lean=24, head=(0, -6, 0.06, 0.0)),
          "bite": dict(expr="bite", legs="lunge", arm_n="claw_up", arm_f="claw", lean=30, head=(0, -12, 0.14, 0.04))}
    for k, p in dp.items():
        a.pose(p, camera=cam)
        z0 = 0.9 if "seat" in k or "lift" in k else 1.45
        if "seat" in k or "lift" in k:
            a.root.location.z = 0.0
        _ortho(cam, (0, 0, z0 + (0.4 if "seat" in k or "lift" in k else 0)), 3.3)
        _render(os.path.join(LD, "driver_%s.png" % k))
    # extras lineup (one frame)
    for k, ac in actors.items():
        ac.hide(True)
    X = draw8.extras(10)
    bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y = (1600, 520)
    ex = []
    for i, sp in enumerate(X):
        e = S.Actor8("ex%02d" % i, sp, height=2.6 + (i % 3) * 0.12, ppd=200)
        x = (i - 4.5) * 1.55
        e.place((x, 0, 0), (-30 if i % 3 == 0 else 0) * (1 if i % 2 else -1))
        p = dict(sp["extra_pose"])
        e.pose(p, camera=cam)
        ex.append(e)
    S.shadow_link(ex, L["key"])
    cam.data.type = "ORTHO"; cam.data.ortho_scale = 16.0
    cam.location = (0, -20, 1.45); cam.rotation_euler = (math.radians(90), 0, 0)
    _render(os.path.join(LD, "extras_neutral.png"))
    json.dump(TIMES, open(os.path.join(LD, "times_neutral.json"), "w"), indent=1)


def phone():
    """re-render the two phone tiles only."""
    import bpy, neutral8 as N, stage8 as S, phone8
    from mathutils import Vector
    N.reset()
    L = N.build(res=(360, 560), samples=24)
    cam = N.camera((0, -20, 1.4), (0, 0, 1.4), 50, ortho=3.4)
    S.tune(AMB=0.30)
    a = S.Actor8("kong", "kong", height=2.86, ppd=900)
    a.place((0, 0, 0), 0)
    S.shadow_link([a], L["key"])
    uri = phone8.data_uri(os.path.join(HERE, "tex", "phone_screen.png"))
    a.pose(dict(expr="guilty", arm_r=dict(hand=(-0.20, 0.30), hand_shape="grip"), prop_r=dict(type="phone", screen=uri, scale=1.3)), camera=cam)
    c = a.world_of(a.fig["anchors"]["prop_R"], 2.3)
    _ortho(cam, c + Vector((0, 0, 0.12)), 0.6)
    _render(os.path.join(LD, "prop_phone.png"))
    _ortho(cam, a.world_of((0, -2.9), 0), 2.2)
    _render(os.path.join(LD, "prop_phone_mcu.png"))


def seated():
    """the two seated driver poses on a simple car-seat block (neutral stage)."""
    import bpy, neutral8 as N, stage8 as S
    N.reset()
    L = N.build(res=(480, 800), samples=24)
    cam = N.camera((0, -20, 1.4), (0, 0, 1.4), 50, ortho=3.4)
    S.tune(AMB=0.30)
    a = S.Actor8("driver", "driver", height=2.86, ppd=240)
    a.place((0, 0, 0), -36)
    hip_z = (a.spec["legs"] + 0.06) * a.sc
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    seat = bpy.context.active_object
    seat.scale = (1.0, 1.1, 0.30); seat.location = (0.05, 0.25, hip_z * 0.62 - 0.15)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    back = bpy.context.active_object
    back.scale = (1.0, 0.25, 1.3); back.location = (0.05, 0.85, hip_z * 0.62 + 0.55)
    m = bpy.data.materials.new("seat_m"); m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.08, 0.08, 0.09, 1)
    seat.data.materials.append(m); back.data.materials.append(m)
    dp = {"seated_still": dict(expr="still", legs=dict(seated=True), arm_r="lap", arm_l="lap", head=(0, 16, 0, 0.06), lean=8),
          "head_lift": dict(expr="head_lift", legs=dict(seated=True), arm_r="lap", arm_l="wheel", head=(8, -10, 0, -0.02), lean=2)}
    S.shadow_link([a], L["key"])
    for k, p in dp.items():
        a.root.location.z = hip_z * 0.62 - hip_z
        a.pose(p, camera=cam)
        _ortho(cam, (0, 0, 1.1), 3.3)
        _render(os.path.join(LD, "driver_%s.png" % k))


def find_spot(near, mh, dist=7.5, spread=5.0):
    """an open patch of deck: the camera on the moon side (dist) sees the actor and +/- spread sideways unblocked."""
    import bpy
    from mathutils import Vector
    sc = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    side = Vector((-mh.y, mh.x, 0))
    best = None
    for ix in range(-16, 17):
        for iy in range(-16, 17):
            K = near + Vector((ix * 0.8, iy * 0.8, 0))
            hit, loc, *_ = sc.ray_cast(dg, K + Vector((0, 0, 6)), Vector((0, 0, -1)))
            if not hit or abs(loc.z) > 0.25:
                continue
            K = Vector((K.x, K.y, loc.z))
            cam = K + mh * dist + Vector((0, 0, 1.6))
            ok = True
            for o in (-spread, -spread / 2, 0, spread / 2, spread):
                for h in (0.25, 1.4, 2.6):
                    tgt = K + side * o + Vector((0, 0, h))
                    d = tgt - cam
                    hit, loc, *_ = sc.ray_cast(dg, cam, d.normalized(), distance=d.length - 0.05)
                    if hit:
                        ok = False; break
                if not ok:
                    break
            if ok:
                dd = (K - near).length
                if best is None or dd < best[0]:
                    best = (dd, K)
    return best[1] if best else near


def night():
    """inside the v6 set: camera on the moon side (the moon is behind the camera, never behind a head)."""
    import bpy
    from mathutils import Vector
    sys.path.insert(0, os.path.join(PROJ, "v6", "set"))
    import beauty as B, kit
    A = B.build()
    B.setup_render("final", threads=4)
    import stage8 as S, draw8
    sc = bpy.context.scene
    sc.cycles.transparent_max_bounces = max(sc.cycles.transparent_max_bounces, 32)
    os.makedirs(LD, exist_ok=True)
    md = Vector(A["moon_dir"]); mh = Vector((md.x, md.y, 0)).normalized()
    K = find_spot(Vector(A["kong_phone_mark"]), mh)
    print("night spot", K)
    cam = B.X.make_camera()
    sc.render.resolution_x, sc.render.resolution_y = 360, 640

    def shoot(path, target_z=1.75, dist=6.4, lens=32, focus=None):
        loc = K + mh * dist + Vector((0, 0, 1.5))
        cam.location = loc
        cam.rotation_euler = kit.look_rot(tuple(loc), tuple(K + Vector((0, 0, target_z))), 0.0)
        cam.data.lens = lens
        cam["preset"] = "ld"; cam["aspect"] = "9:16"; cam["focus"] = tuple(focus or (K + Vector((0, 0, 2.2)))); cam["coc_k"] = 2.0; cam["coc_max"] = 8; cam["dof_k"] = 1
        for ob in bpy.data.objects:
            for con in ob.constraints:
                if con.type == "TRACK_TO": con.target = cam
        bpy.context.view_layer.update()
        t0 = time.time()
        r = B.render6.render(path, frame=7, post_opts={"exposure": 1.6, "sharp_idx": [2]})
        TIMES[os.path.basename(path)] = dict(wall=round(time.time() - t0, 2), cpu_render=r.get("cpu_render"))

    acts = {}
    cam_dir = -mh
    face0 = math.degrees(math.atan2(mh.x, -mh.y))        # facing toward the camera
    for nm, spec in (("kong", "kong_wet"), ("crew", "crew_wet"), ("driver", "driver")):
        a = S.Actor8("n_" + nm, spec, height=2.86)
        a.set_pass_index(2)
        acts[nm] = a
    for nm, a in acts.items():
        for o, b in acts.items():
            b.hide(o != nm)
        for v, off in TURN:
            a.place(tuple(K), face0 + off)
            cam.location = K + mh * 6.4 + Vector((0, 0, 1.5))
            bpy.context.view_layer.update()
            pose = dict(arm_r="hold_cutter", prop_r=dict(type="cutter", bars=3, wet=True)) if (nm == "kong" and v == "front") else {}
            if nm == "driver":
                pose = dict(expr="head_lift")
            a.pose(pose, camera=cam)
            L = None
            import look8
            L = look8.dominant_light(K + Vector((0, 0, 1.5)))
            if L:
                S.shadow_link([a], L)
            shoot(os.path.join(LD, "night_%s_%s" % (nm, v)))
    for a in acts.values():
        a.hide(True)
    # extras in the set
    X = draw8.extras(10)
    ex = []
    side = Vector((-mh.y, mh.x, 0))
    for i, sp in enumerate(X):
        e = S.Actor8("nx%02d" % i, sp, height=2.6 + (i % 3) * 0.12)
        e.set_pass_index(2)
        p = K - mh * ((i % 2) * 0.9) + side * ((i - 4.5) * 1.05)
        e.place(tuple(p), face0 + (-25 if i % 3 == 0 else 10) * (1 if i % 2 else -1))
        ex.append((e, sp))
    cam.location = K + mh * 6.0 + Vector((0, 0, 1.6))
    bpy.context.view_layer.update()
    for e, sp in ex:
        e.pose(dict(sp["extra_pose"]), camera=cam)
    S.shadow_link([e for e, _ in ex], look8.dominant_light(K + Vector((0, 0, 1.5))))
    sc.render.resolution_x, sc.render.resolution_y = 960, 540
    shoot(os.path.join(LD, "night_extras"), target_z=1.3, dist=7.5, lens=26, focus=K - mh * 2 + Vector((0, 0, 2)))
    json.dump(TIMES, open(os.path.join(LD, "times_night.json"), "w"), indent=1)


# ---------------------------------------------------------------------------------------------------- sheets
def _font(sz):
    from PIL import ImageFont
    return ImageFont.truetype(os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), sz)


def _tile(path, w, h):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    k = min(w / im.width, h / im.height)
    return im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)


def sheet():
    from PIL import Image, ImageDraw
    bg, fg, dim = (18, 18, 22), (236, 236, 240), (160, 160, 172)
    rows = []

    def row(title, items, w, h):
        rows.append((title, items, w, h))

    row("1  Turnarounds, neutral light (front / 3-4 / side): Kong dry, Kong wet, crew, infected driver", [
        (os.path.join(LD, "turn_%s_%s.png" % (n, v)), "%s %s" % (n, v)) for n in ("kong", "kong_wet", "crew", "driver") for v in ("front", "q", "side")], 300, 500)
    row("2  Inside the v6 set at night, moon behind the camera (front / 3-4 / side)", [
        (os.path.join(LD, "night_%s_%s.png" % (n, v)), "%s %s" % (n, v)) for n in ("kong", "crew", "driver") for v in ("front", "q", "side")], 300, 533)
    row("3  Expressions: Kong (determined = sheet, tired, guilty, alarmed, shouting, blink), crew (neutral, shouting, scared, blink), driver (still, head-lift, lunge, bite)", [
        (os.path.join(LD, "expr_%s_%s.png" % (n, e)), "%s %s" % (n, e)) for n in ("kong", "crew", "driver") for e in EXPRS[n]], 240, 240)
    row("4  Lip-sync mouth driven by a level value (0, 0.25, 0.5, 0.75, 1.0); props: cutter battery 3 / 2 / 1 bars, phone screen (Thai)", [
        (os.path.join(LD, "mouth_kong_%03d.png" % int(l * 100)), "mouth level %.2f" % l) for l in MOUTH_LEVELS] +
        [(os.path.join(LD, "prop_cutter_%d.png" % b), "cutter %d bars" % b) for b in (3, 2, 1)] +
        [(os.path.join(LD, "prop_phone.png"), "phone, Thai screen"), (os.path.join(LD, "prop_phone_mcu.png"), "phone MCU")], 240, 330)
    row("5  Infected driver poses (q view): seated still, head-lift, lunge, bite", [
        (os.path.join(LD, "driver_%s.png" % k), k) for k in ("seated_still", "head_lift", "lunge", "bite")], 330, 550)
    row("6  Background people: 10 distinct (face, hair, clothes colour, pose) - neutral light / in the v6 set", [
        (os.path.join(LD, "extras_neutral.png"), "extras, neutral"), (os.path.join(LD, "night_extras.png"), "extras, v6 set night")], 1500, 520)
    W = 2900
    pad, lab, head = 10, 26, 44
    tiles = []
    y = 70
    layout = []
    for title, items, w, h in rows:
        x = pad
        layout.append(("title", title, (pad, y)))
        y += head
        rowh = 0
        for p, l in items:
            if not os.path.exists(p):
                continue
            t = _tile(p, w, h)
            if x + t.width > W - pad:
                x = pad; y += rowh + lab + pad; rowh = 0
            layout.append(("img", t, (x, y)))
            layout.append(("lab", l, (x, y + t.height + 2)))
            x += t.width + pad
            rowh = max(rowh, t.height)
        y += rowh + lab + 24
    S = Image.new("RGB", (W, y + 10), bg)
    d = ImageDraw.Draw(S)
    d.text((pad, 14), "DEAD ZONE 09 - v8 cast lookdev: sheet-style 2.5D paper puppets, lit by the scene (pseudo-normal cards)", fill=(255, 214, 120), font=_font(30))
    for kind, v, (x, yy) in layout:
        if kind == "title":
            d.text((x, yy + 8), v, fill=fg, font=_font(22))
        elif kind == "img":
            S.paste(v, (x, yy))
        else:
            d.text((x + 2, yy), v, fill=dim, font=_font(16))
    S.save(os.path.join(HERE, "lookdev.png"))
    print("lookdev.png", S.size)


def sbs():
    """sheet crop | our front render, both scaled to the same total height (700 px)."""
    from PIL import Image, ImageDraw
    import numpy as np
    Hh = 700
    pairs = [("kong", "Kong (sheet)", "Kong (v8 front render)"), ("james", "James (sheet)", "crew (v8)"),
             ("tos", "Khun Tos (sheet)", "driver (v8)")]
    ours = {"kong": "kong", "james": "crew", "tos": "driver"}
    tiles = []
    for ref, l1, l2 in pairs:
        a = Image.open(os.path.join(PROJ, "spec", "sheet_measure", "%s_cut.png" % ref)).convert("RGB")
        arr = np.asarray(a).astype(int)
        m = np.abs(arr - np.array([253, 243, 232])).sum(-1) > 28
        ys, xs = np.nonzero(m)
        a = a.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        a = a.resize((int(a.width * Hh / a.height), Hh), Image.LANCZOS)
        b = Image.open(os.path.join(HERE, "out", "measure", "%s_front.png" % ours[ref])).convert("RGB")
        idm = np.asarray(Image.open(os.path.join(HERE, "out", "measure", "%s_id.png" % ours[ref])).convert("RGBA"))[..., 3] > 128
        ys, xs = np.nonzero(idm)
        b = b.crop((xs.min() - 20, ys.min(), xs.max() + 21, ys.max() + 1))
        b = b.resize((int(b.width * Hh / b.height), Hh), Image.LANCZOS)
        tiles.append((a, b, l1, l2))
    W = sum(a.width + b.width + 70 for a, b, _, _ in tiles) + 20
    S = Image.new("RGB", (W, Hh + 110), (253, 243, 232))
    d = ImageDraw.Draw(S)
    d.text((14, 10), "Character sheet (left of each pair) vs v8 Cycles front render (right), same total height %d px (hair top to sole)" % Hh,
           fill=(30, 30, 30), font=_font(22))
    x = 20
    for a, b, l1, l2 in tiles:
        S.paste(a, (x, 60)); d.text((x, 60 + Hh + 8), l1, fill=(40, 40, 40), font=_font(18))
        S.paste(b, (x + a.width + 20, 60)); d.text((x + a.width + 20, 60 + Hh + 8), l2, fill=(40, 40, 40), font=_font(18))
        d.line([(x - 4, 60), (x - 4 + a.width + b.width + 32, 60)], fill=(200, 60, 60), width=2)
        d.line([(x - 4, 60 + Hh - 1), (x - 4 + a.width + b.width + 32, 60 + Hh - 1)], fill=(200, 60, 60), width=2)
        x += a.width + b.width + 70
    S.save(os.path.join(HERE, "side_by_side.png"))
    print("side_by_side.png", S.size)


if __name__ == "__main__":
    {"neutral": neutral, "phone": phone, "seated": seated, "night": night, "sheet": sheet, "sbs": sbs}[sys.argv[1]]()
