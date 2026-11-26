"""extras7.py -- expression heads, driver poses (seat stand-in), props, wet Kong, action poses (neutral light).
python3 lookdev7.py extras [--parts faces,driver,props,wet,poses]"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lookdev7 as L

OUT, TMP = L.OUT, L.TMP


def run(args):
    parts = args[args.index("--parts") + 1].split(",") if "--parts" in args else ["faces", "driver", "props", "wet", "poses"]
    spp = int(args[args.index("--spp") + 1]) if "--spp" in args else 32
    t = {}
    if "faces" in parts: t.update(faces(spp))
    if "driver" in parts: t.update(driver(spp))
    if "props" in parts: t.update(props(spp))
    if "wet" in parts: t.update(wet(spp))
    if "poses" in parts: t.update(poses(spp))
    L._times(t)


def faces(spp):
    import cast7 as C, faces7 as F
    sc, cam = L.neutral_scene(spp)
    sc.render.resolution_x = sc.render.resolution_y = 360
    chars = {k: C.Character(k) for k in ("kong", "crew", "driver")}
    for ch in chars.values():
        for ob in ch.objects: ob.hide_render = True
    t = {}
    for kk, ch in chars.items():
        for ob in ch.objects: ob.hide_render = False
        ch.place((0, 0, 0), 0); ch.pose(head=(-16, 0, 0))
        hz = ch.head.matrix_world.translation.z
        for e in F.EXPRS[kk]:
            if e == "blink": continue
            ch.set_face(e)
            cam.location = (0, -2.6, hz + 0.1); cam.data.lens = 60; L._aim(cam, (0, 0, hz - 0.08))
            p = os.path.join(TMP, f"face_{kk}_{e}.png"); t[f"face_{kk}_{e}"] = L.render(sc, p)
        for ob in ch.objects: ob.hide_render = True
        ch.sweat.hide_render = True
    return t


def driver(spp):
    import cast7 as C
    sc, cam = L.neutral_scene(spp)
    d = C.Character("driver")
    seatm = C.m_toon("seat", "#5d6068")
    seat = C._obj("seat", None, C.coll("SEAT")); seat.rotation_euler = (0, 0, math.radians(-35))
    for nm, size, loc in (("cush", (1.2, 1.0, 0.30), (0, 0.05, 0.77)), ("back", (1.2, 0.28, 1.9), (0, 0.62, 1.70)),
                          ("base", (1.0, 0.9, 0.62), (0, 0.05, 0.31))):
        me = C._rbox(nm, size, 0.08); me.materials.append(seatm); C._obj(nm, me, C.coll("SEAT"), seat, loc)
    t = {}
    for nm in ("driver_seated", "driver_head_lift", "driver_lunge"):
        d.preset(nm); d.place((0, 0, 0), -35)
        L.frame(sc, cam, 1.9, 7.4, 2.2)
        p = os.path.join(OUT, f"e_{nm}.png"); t["e_" + nm] = L.render(sc, p); L.meta(sc, cam, d, p)
    return t


def props(spp):
    import cast7 as C
    sc, cam = L.neutral_scene(spp)
    sc.render.resolution_x = 1280; sc.render.resolution_y = 720
    for i, b in enumerate((3, 2, 1)):
        cu = C.Cutter(name=f"cut{b}", bars=b, scale=1.0)
        cu.root.location = (-1.25 + i * 0.75, 0, 0.55); cu.root.rotation_euler = (math.radians(-25), 0, math.radians(-70))
    ph = C.Phone(scale=2.2)
    ph.root.location = (0.95, -0.3, 0.45); ph.root.rotation_euler = (math.radians(-12), 0, math.radians(8))
    cam.location = (-0.1, -3.6, 1.55); cam.rotation_euler = (math.radians(72), 0, 0); cam.data.lens = 42
    p = os.path.join(OUT, "e_props.png")
    return {"e_props": L.render(sc, p)}


def wet(spp):
    import cast7 as C
    sc, cam = L.neutral_scene(spp)
    k = C.Character("kong", wet=True, expr="tired")
    cut = C.Cutter(bars=2, wet=True); k.hold(cut, "r", fwd=(0.0, -0.3, -1.0), up=(0, -1, 0.3))
    k.preset("kong_hold_cutter"); k.set_face("tired")
    t = {}
    for vn, f in (("front", 0), ("q", -38)):
        k.place((0, 0, 0), f); L.frame(sc, cam, 2.3, 7.4, 2.2)
        p = os.path.join(OUT, f"e_kong_wet_{vn}.png"); t["e_kong_wet_" + vn] = L.render(sc, p); L.meta(sc, cam, k, p)
    return t


def poses(spp):
    import cast7 as C
    sc, cam = L.neutral_scene(spp)
    k = C.Character("kong"); cr = C.Character("crew")
    ph = C.Phone(scale=1.5); cut = C.Cutter(bars=1)
    t = {}
    jobs = [("kong_phone", k, cr), ("kong_shout", k, cr), ("kong_alarmed", k, cr), ("crew_shout", cr, k), ("crew_scared", cr, k)]
    for nm, ch, other in jobs:
        for ob in other.objects: ob.hide_render = True
        for ob in ch.objects: ob.hide_render = False
        ch.set_face(ch.expr)
        for ob in ph.objects + cut.objects: ob.hide_render = True
        ch.props.clear()
        if nm == "kong_phone":
            k.hold(ph, "r", fwd=(0, -1, -0.6), up=(0, -0.6, 1), offset=(0.0, -0.04, 0.02))
            for ob in ph.objects: ob.hide_render = False
        elif nm == "kong_shout":
            k.hold(cut, "r", fwd=(0, -1, 0.1), up=(0, 0, 1))
            for ob in cut.objects: ob.hide_render = False
        ch.preset(nm); ch.place((0, 0, 0), -20)
        L.frame(sc, cam, 2.3, 7.4, 2.2)
        p = os.path.join(OUT, f"e_{nm}.png"); t["e_" + nm] = L.render(sc, p); L.meta(sc, cam, ch, p)
    return t
