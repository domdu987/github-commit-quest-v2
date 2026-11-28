"""look.py -- six EP.1 look stills in the v6 beauty set with the v6 cast, framed with ref D camera grammar.

python3 look.py render [--only s06,s09] [--aspect 9:16,16:9] [--q final] [--scale 1.0]
python3 look.py sheet          sheet_916.png, sheet_169.png, vs_ref.png

Shots (refD_camera.md templates):
  s06  T4/T5 low hero MS: Kong with the cutter, camera at chest height looking up, wheel foreground (ref f2_115)
  s09  T1 prop macro: the cutter's 3-bar gauge sharp, Kong's face soft behind (ref f2_001)
  s13  T4 OTS MCU, mild high: Kong on the phone, guilty; the crew's shoulder fills the lower left (ref f2_042)
  s18  T8 POV through the cracked windscreen from the bonnet onto the still driver (ref f2_011)
  s20  POV through the open driver door, Dutch 12 deg: the driver lifts his head (ref f2_008, no Dutch in ref D)
  s24  T7 strong high establishing: the gridlock and the rescue scene small in it (ref f2_072)
"""
import os, sys, json, math, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
REF = {"s06": 115, "s09": 1, "s13": 42, "s18": 11, "s20": 8, "s24": 72}
TITLE = {"s06": "S06 low hero MS (T4/T5)", "s09": "S09 battery macro (T1)", "s13": "S13 phone MCU, OTS (T4)",
         "s18": "S18 POV windscreen (T8)", "s20": "S20 head lift, Dutch", "s24": "S24 high wide (T7)"}
SHOTS = ["s06", "s09", "s13", "s18", "s20", "s24"]
CS = 0.82            # cast scale in the set: Kong 3.49 D x 0.82 = 2.86 D = 1.72 m (the set's Kong height)


def setup(q="final", threads=4):
    sys.path.insert(0, os.path.join(PROJ, "v6", "set")); sys.path.insert(0, os.path.join(PROJ, "v6", "cast"))
    import beauty as B
    A = B.build()
    B.setup_render(q, threads=threads)
    import kit, cast6 as C
    C.AMBIENT[:] = kit.AMBIENT
    kong = C.Character("kong", wet=True, expr="determined", separator=True)
    crew = C.Character("crew", wet=True, expr="neutral", separator=True)
    drv = C.Character("driver", expr="still")
    cut = C.Cutter(bars=3, wet=True, scale=1.3)
    ph = C.Phone(wet=True)
    for ch in (kong, crew, drv):
        ch.root.scale = (CS,) * 3
    G = dict(A=A, B=B, C=C, kong=kong, crew=crew, drv=drv, cut=cut, ph=ph)
    for ch in (kong, crew, drv): ch.set_pass_index(2)
    for ob in cut.objects + ph.objects: ob.pass_index = 2
    return G


def _vec(*a):
    from mathutils import Vector
    return Vector(a if len(a) > 1 else a[0])


def facing(front):
    return math.degrees(math.atan2(front[0], -front[1]))


def hide(G, ch, h=True):
    objs = ch.objects if hasattr(ch, "objects") else ch
    for ob in objs:
        ob.hide_render = h


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


DRV_S = 0.58          # the seated driver is drawn smaller so his head stays under the sedan's roof (roof z 2.3-2.5)
DRV_SEAT = 0.86       # bean bottom z: sunk 0.43 D into the cushion (top 1.29)


def fill(G, name, loc=None, power=0.0, color=(0.72, 0.82, 1.0), size=0.5):
    """per-shot practical fill (point light). power 0 switches it off."""
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
    """S20: the driver door's window is broken out (the crew looks in through the empty frame)."""
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
    """S18: the cracked windscreen's reflection is roughened so the moon glint becomes a soft sheen, not a hot spot
    on the driver's face."""
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


def light_gain(G, name, g):
    """scale one set light for this shot (restored to the set value by the next shot)."""
    import bpy
    ob = bpy.data.objects.get(name)
    if ob is None: return
    if "e0" not in ob: ob["e0"] = ob.data.energy
    ob.data.energy = ob["e0"] * g
    G.setdefault("_lg", set()).add(name)


def frame_dirs(A):
    th = A["hero_heading"]
    fwd = _vec(-math.sin(th), math.cos(th), 0.0); right = _vec(math.cos(th), math.sin(th), 0.0)
    return fwd, right


def head_z(ch_scale=CS):
    return (3.49 - 0.49) * ch_scale      # head centre above the soles


# ------------------------------------------------------------------------------------------------------- shots
def shot(G, name, aspect):
    import bpy, presets
    from mathutils import Vector
    A = G["A"]; kong, crew, drv, cut, ph = G["kong"], G["crew"], G["drv"], G["cut"], G["ph"]
    fwd, right = frame_dirs(A)
    v = aspect == "9:16"
    for ch in (kong, crew, drv, cut, ph): hide(G, ch, False)
    # default staging: Kong at the door with the cutter, crew behind him, the driver seated
    K = Vector(A["kong_mark"]); seat = Vector(A["driver_seat"])
    drv.root.scale = (DRV_S,) * 3
    drv.place(tuple(Vector((seat.x, seat.y, DRV_SEAT - 0.62 * DRV_S)) - fwd * 0.02), facing(fwd))
    hide_roots(G, [])
    door_glass(G, False); windscreen_soft(G, False)
    for nm in list(G.get("_lg", ())): light_gain(G, nm, 1.0)
    drv.preset("driver_seated")
    crew.place(A["crew_mark"], facing(-(right * 0.9 + fwd * 0.4)))
    crew.preset("crew_idle")
    kong.hold(cut, "r", fwd=(0, -0.3, -1), up=(0, -1, 0.3))
    kong.preset("kong_hold_cutter")
    ph.root.parent = None; ph.root.location = (0, 0, -50)
    post = {"exposure": 1.6}
    fill(G, "look_fill_a"); fill(G, "look_fill_b")
    hz = head_z()

    if name == "s06":
        # T4/T5: camera at Kong's chest (1.1 D), 28 mm, looking up; Kong 0.5-0.6 H; a wrecked wheel at the left edge
        to_cam = (Vector((4.4, -8.4, 0))).normalized()
        hide_roots(G, ["bike_a"])
        kong.place(tuple(K), facing(to_cam) - 25)
        kong.pose(arm_r=dict(hand=(0.60, -0.28, 0.10), pole=(1, 0.6, 0.2)), arm_l="down", legs="wide",
                  head=(-12, 4, 0), lean=(-3, 0, 0), expr="determined")
        side = Vector((-to_cam.y, to_cam.x, 0))
        if v:
            loc = K + to_cam * 3.4 + side * 0.30 + Vector((0, 0, 0.95)); look = K + Vector((0, 0, 1.65)) + side * 0.2
            lens = 28
        else:
            loc = K + to_cam * 5.6 - side * 0.9 + Vector((0, 0, 0.95)); look = K + Vector((0, 0, 1.6)) - side * 1.55
            lens = 28
        cam = camera(G, tuple(loc), tuple(look), lens, aspect, K + Vector((0, 0, hz)), 7.0, 22)
        presets.foreground(cam, "wheel", side="left", cover=0.38 if v else 0.24, depth=1.6)
        post["sharp_idx"] = [2]

    elif name == "s09":
        # T1 macro: the gauge sharp in the lower third, Kong's face big and soft behind (50 mm, face coc ~18 px)
        to_cam = (Vector((4.4, -8.4, 0))).normalized()
        hide_roots(G, ["bike_a"])
        kong.place(tuple(K), facing(to_cam))
        kong.pose(arm_r=dict(hand=(0.16, -0.98, 0.86), pole=(1, 0.2, -0.6)), arm_l=dict(hand=(0.30, -0.80, 0.62), pole=(1, 0.2, -0.6)),
                  legs="stand", head=(0, -20, 0), lean=(4, 0, 0), expr="tired")
        kong.hold(cut, "r", fwd=(1, -0.15, 0.0), up=(0, -0.70, 0.70))
        bpy.context.view_layer.update()
        gauge = [o for o in cut.objects if o.name.endswith("_gauge")][0].matrix_world.translation.copy()
        hc = kong.head.matrix_world.translation.copy()
        dirv = to_cam.copy(); sidev = Vector((-dirv.y, dirv.x, 0))
        d = 0.95 if v else 1.0
        loc = gauge + dirv * d + Vector((0, 0, 0.06)) - sidev * (0.22 if v else 0.05)
        look = gauge + (hc - gauge) * (0.40 if v else 0.10) - sidev * (0.04 if v else -0.04)
        cam = camera(G, tuple(loc), tuple(look), 50, aspect, gauge, 85.0, 36, clip=0.02)
        post["exposure"] = 1.5

    elif name == "s13":
        # T4 OTS MCU at eye level: Kong on the phone, guilty, head D ~280 px; the crew's shoulder lower left
        P0 = Vector(A["kong_phone_mark"])
        to_cam = Vector((0.12, -1.0, 0)).normalized()
        side = Vector((-to_cam.y, to_cam.x, 0))           # screen-right for a camera looking along -to_cam
        kong.place(tuple(P0), facing(to_cam) + 22)
        hide(G, cut)
        ph.root.scale = (1.5,) * 3
        kong.hold(ph, "r", fwd=(1, 0.55, 0), up=(0, 0, 1), offset=(0.0, -0.06, -0.10))
        kong.pose(arm_r=dict(hand=(0.60, -0.16, 1.80), pole=(1, 0.5, -1)), arm_l=dict(hand=(0.40, -0.35, 0.50), pole=(1, 0.2, -0.6)), legs="stand",
                  head=(-14, -10, -5), lean=(5, 0, 0), expr="guilty")
        hcen = P0 + Vector((0, 0, hz))
        d = 3.0 if v else 3.3
        loc = hcen + to_cam * d + Vector((0, 0, 0.25)) - side * (0.15 if v else 0.85)
        look = hcen + Vector((0, 0, -0.40 if v else -0.20)) - side * (0.10 if v else 0.95)
        cpos = loc - to_cam * (1.25 if v else 1.35) - side * (0.48 if v else 0.30); cpos.z = -0.55
        crew.place(tuple(cpos), facing(-to_cam) + 15)
        crew.pose(arm_r="down", arm_l="down", legs="stand", head=(0, 0, 0), expr="neutral")
        cam = camera(G, tuple(loc), tuple(look), 30 if v else 32, aspect, hcen, 12.0, 24)
        post["sharp_idx"] = []

    elif name == "s18":
        # T8 POV through the cracked windscreen from the bonnet: bonnet + scuttle fill the lower 40 %, driver centred
        ws = Vector(A["windscreen"])
        drv.pose(arm_r="lap", arm_l="lap", legs="seated", lean=(10, 0, 0), head=(6, -8, 8), expr="still")
        drv.root.location.z = DRV_SEAT - 0.62 * DRV_S
        bpy.context.view_layer.update()
        hc = drv.head.matrix_world.translation.copy()
        loc = ws + fwd * (1.65 if v else 1.85) - right * (0.40 if v else 0.50)
        loc.z = hc.z + 0.18
        look = hc + Vector((0, 0, 0.12 if v else 0.0)) - right * 0.10
        windscreen_soft(G, True)
        light_gain(G, "sodium_2_1", 0.3)
        light_gain(G, "sodium_2_-1", 0.3)   # the lamp right over the car blew the driver's crown out through the glass
        fill(G, "look_fill_a", tuple(hc + fwd * 0.65 + Vector((0, 0, 0.12)) - right * 0.15), 16.0, size=0.35)
        fill(G, "look_fill_b", tuple(hc + right * 1.6 - fwd * 0.3 + Vector((0, 0, 0.3))), 20.0, (1.0, 0.86, 0.72), 0.6)
        cam = camera(G, tuple(loc), tuple(look), 24 if v else 24, aspect, hc, 8.0, 18, clip=0.02)
        hide(G, kong); hide(G, crew); hide(G, cut)
        hide_roots(G, ["l2_b", "headlight_l2_b_-1", "headlight_l2_b_1", "flood_beam"])

    elif name == "s20":
        # the crew's POV through the open driver door, Dutch 12 deg: the driver lifts his head, white eyes
        drv.pose(arm_r="lap", arm_l="wheel", legs=dict(C_LEG_SEATED(G)), lean=(4, -3, 0), head=(-48, 10, -6), expr="head_lift")
        bpy.context.view_layer.update()
        hc = drv.head.matrix_world.translation.copy()
        dm = Vector(A["door_mid"])
        loc = Vector((dm.x, dm.y, 0)) + right * (1.45 if v else 1.8) - fwd * (0.05 if v else 0.45) + Vector((0, 0, 2.05))
        fill(G, "look_fill_a", tuple(hc + fwd * 0.8 + right * 0.1 + Vector((0, 0, -0.1))), 10.0, size=0.3)
        fill(G, "look_fill_b", tuple(hc + right * 1.0 - fwd * 0.2 + Vector((0, 0, 0.5))), 18.0, (0.72, 0.82, 1.0), 0.5)
        look = hc + right * 0.25 + Vector((0, 0, -0.15))
        cam = camera(G, tuple(loc), tuple(look), 26 if v else 28, aspect, hc, 9.0, 22, roll=12.0)
        hide(G, kong); hide(G, cut)
        door_glass(G, True)
        crew.place(tuple(Vector((dm.x, dm.y, 0)) + right * 1.55 - fwd * 1.0), facing(-right))
        crew.pose(arm_r="reach", arm_l="down", legs="stand", lean=(10, 0, 0), expr="neutral")
        hide(G, crew)                      # the crew is the POV holder

    elif name == "s24":
        # T7 strong high: 13 D up, 45 mm (38 mm in 16:9), the rows stack; Kong and the crew small at the door
        kong.place(tuple(K), A["kong_to_door_deg"])
        kong.hold(cut, "r", fwd=(0, -1, 0.1), up=(0, 0, 1))
        kong.pose(arm_r="hold_cutter", arm_l="reach", legs="wide", lean=(10, 0, 0), expr="determined")
        crew.preset("crew_idle")
        if v:
            l0, t0, lens = Vector((3.8, 7.0, 13.0)), Vector((-8.6, 42.0, 0.0)), 45
        else:
            l0, t0, lens = Vector((5.5, 9.0, 12.5)), Vector((-8.8, 40.0, 0.0)), 38
        loc = K + (l0 - K) * 0.62; look = loc + (t0 - l0)          # same angle, 38 % closer: heads read at ~25 px
        loc, look = tuple(loc), tuple(look)
        cam = camera(G, loc, look, lens, aspect, K, 1.6, 10)
        presets.foreground(cam, "pole", side="left", cover=0.08, depth=6.0)
        post["sharp_idx"] = [2]
        post["exposure"] = 1.7
    else:
        raise KeyError(name)
    bpy.context.view_layer.update()
    return post


def C_LEG_SEATED(G):
    d = dict(G["C"].LEG_PRESETS["seated"]); return d


def render(only, aspects, q, scale, frame=7):
    G = setup(q); G["scale"] = scale
    times = {}
    os.makedirs(OUT, exist_ok=True)
    for asp in aspects:
        for n in only:
            post = shot(G, n, asp)
            tag = f"{n}_{'916' if asp == '9:16' else '169'}"
            r = G["B"].render6.render(os.path.join(OUT, tag), frame=frame, post_opts=post)
            times[tag] = dict(cpu_render=r.get("cpu_render"), cpu_render_total=r.get("cpu_render_total"), cpu_post=r.get("cpu_post"),
                              wall_render=r.get("wall_render"))
            print("TIME", tag, times[tag], flush=True)
    tp = os.path.join(OUT, "times.json")
    old = json.load(open(tp)) if os.path.exists(tp) else {}
    old.update(times); json.dump(old, open(tp, "w"), indent=1)


def sheets():
    from PIL import Image, ImageDraw, ImageFont
    try:
        f = ImageFont.truetype(os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), 20)
        fs = ImageFont.truetype(os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), 16)
    except Exception:
        f = fs = ImageFont.load_default()
    bg = (14, 14, 18); fg = (232, 232, 236)
    # 9:16 sheet: 3 x 2 at 360x640
    w, h, lab = 360, 640, 30
    s = Image.new("RGB", (3 * w + 2 * 10, 2 * (h + lab) + 10), bg); d = ImageDraw.Draw(s)
    for i, n in enumerate(SHOTS):
        x = (i % 3) * (w + 10); y = (i // 3) * (h + lab + 10)
        d.text((x + 4, y + 5), TITLE[n], fill=fg, font=f)
        p = os.path.join(OUT, f"{n}_916.png")
        if os.path.exists(p): s.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    s.save(os.path.join(HERE, "sheet_916.png"))
    # 16:9 sheet: 2 x 3 at 640x360
    w, h = 640, 360
    s = Image.new("RGB", (2 * w + 10, 3 * (h + lab) + 20), bg); d = ImageDraw.Draw(s)
    for i, n in enumerate(SHOTS):
        x = (i % 2) * (w + 10); y = (i // 2) * (h + lab + 10)
        d.text((x + 4, y + 5), TITLE[n], fill=fg, font=f)
        p = os.path.join(OUT, f"{n}_169.png")
        if os.path.exists(p): s.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    s.save(os.path.join(HERE, "sheet_169.png"))
    # vs ref: per shot, ref | ours (9:16) side by side; 3 pairs per row
    w, h = 300, 533
    pw = 2 * w + 6
    s = Image.new("RGB", (3 * pw + 2 * 16, 2 * (h + lab) + 16), bg); d = ImageDraw.Draw(s)
    for i, n in enumerate(SHOTS):
        x = (i % 3) * (pw + 16); y = (i // 3) * (h + lab + 16)
        d.text((x + 4, y + 6), f"ref D f2_{REF[n]:03d} (look only)", fill=(170, 170, 180), font=fs)
        d.text((x + w + 10, y + 6), TITLE[n], fill=fg, font=fs)
        r = Image.open(os.path.join(PROJ, "ref", "d", "frames2", f"f_{REF[n]:03d}.png")).convert("RGB").resize((w, h), Image.LANCZOS)
        s.paste(r, (x, y + lab))
        p = os.path.join(OUT, f"{n}_916.png")
        if os.path.exists(p): s.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (x + w + 6, y + lab))
    s.save(os.path.join(HERE, "vs_ref.png"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode"); ap.add_argument("--only", default=",".join(SHOTS)); ap.add_argument("--aspect", default="9:16,16:9")
    ap.add_argument("--q", default="final"); ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--frame", type=int, default=7)
    a = ap.parse_args()
    if a.mode == "render":
        render(a.only.split(","), a.aspect.split(","), a.q, a.scale, a.frame)
    elif a.mode == "sheet":
        sheets()
