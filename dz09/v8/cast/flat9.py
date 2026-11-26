"""flat9.py -- the three look shots (S06 low hero, S13 phone MCU, S20 head lift) in the v9 set with the cast in FLAT mode.

python3 flat9.py render [--only s06,s13,s20] [--scale 1.0] [--aspect 9:16]     -> out/flat9/<shot>_916.png
python3 flat9.py sheet                                                           -> flat_in_v9.png (ours | closest ref E frame)
python3 flat9.py measure                                                         -> out/flat9/measure.json (face / cloth / surround)
Same marks and camera formulas as look8.py / v9 look9.py.  The work lamp is kept out of the line behind the heads.
"""
import os, sys, json, math, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out", "flat9")
SHOTS = ["s06", "s13", "s20"]          # + "cal": the s13 staging with the work lamp off (moon shade calibration)
REF = {"s06": 26, "s13": 60, "s20": 84}
TITLE = {"s06": "S06 low hero", "s13": "S13 phone MCU", "s20": "S20 head lift"}
GRADE = {"cal": dict(exposure=1.0, toe=0.03), "s06": dict(exposure=0.95, toe=0.03), "s13": dict(exposure=1.215, toe=0.0179), "s20": dict(exposure=0.54, toe=0.0601)}  # v9 look/grade_fit.json
KONG_H, CREW_H, DRV_H_SEATED, DRV_HIP_Z = 2.86, 2.80, 2.03, 1.12


def setup(q="final", threads=4):
    sys.path.insert(0, os.path.join(PROJ, "v9", "set")); sys.path.insert(0, HERE)
    import beauty as B
    A = B.build()
    B.setup_render(q, threads=threads)
    import bpy, stage8 as S, look8
    bpy.context.scene.cycles.transparent_max_bounces = max(bpy.context.scene.cycles.transparent_max_bounces, 32)
    S.set_mode("flat")
    kong = S.Actor8("kong", "kong_wet", height=KONG_H)
    crew = S.Actor8("crew", "crew_wet", height=CREW_H)
    drv = S.Actor8("driver", "driver", height=DRV_H_SEATED)
    drv.pitch_anchor = 0.6
    for a in (kong, crew, drv): a.set_pass_index(2)
    return dict(A=A, B=B, S=S, L=look8, kong=kong, crew=crew, drv=drv, phone=look8.phone_uri())


def shot(G, name, aspect="9:16"):
    import bpy, presets
    from mathutils import Vector
    A, B, S, L = G["A"], G["B"], G["S"], G["L"]
    kong, crew, drv = G["kong"], G["crew"], G["drv"]
    fwd, right = L.frame_dirs(A)
    v = aspect == "9:16"
    for a in (kong, crew, drv): a.hide(False)
    K = Vector(A["kong_mark"]); seat = Vector(A["driver_seat"])
    L.hide_roots(G, []); L.door_glass(G, False)
    L.fill(G, "look_fill_a"); L.fill(G, "look_fill_b")
    post = dict(GRADE[name]); lamp = {}; shadow_from_lamp = name in ("s06", "s13")
    S.tune_flat(**dict(S.FLAT_DEFAULT, EXPO=post["exposure"]))
    hz = L.head_z()
    drv.view_override = None
    drv.place(tuple(Vector((seat.x, seat.y, DRV_HIP_Z - (drv.spec["legs"] + 0.06) * drv.sc)) - fwd * 0.02), L.facing(fwd))
    drv_pose = dict(expr="still", legs=dict(seated=True), arm_r="lap", arm_l="lap", head=(0, 14, 0.0, 0.06), lean=6)
    crew.place(A["crew_mark"], L.facing(-(right * 0.9 + fwd * 0.4)))
    warm = (1.0, 0.72, 0.45)
    if name == "s06":
        to_cam = Vector((4.4, -8.4, 0)).normalized()
        L.hide_roots(G, ["bike_a"])
        kong.place(tuple(K), L.facing(to_cam) - 25)
        side = Vector((-to_cam.y, to_cam.x, 0))
        loc = K + to_cam * 3.4 + side * 0.30 + Vector((0, 0, 0.95)); look = K + Vector((0, 0, 1.65)) + side * 0.2
        cam = L.camera(G, tuple(loc), tuple(look), 28, aspect, K + Vector((0, 0, hz)), 7.0, 22)
        kong.pose(dict(expr="determined", arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3, wet=True), legs="wide", head=(0, -6, 0, 0)), camera=cam)
        crew.pose(dict(expr="neutral"), camera=cam)
        drv.pose(drv_pose, camera=cam)
        presets.foreground(cam, "wheel", side="left", cover=0.38 if v else 0.24, depth=1.6)
        post["sharp_idx"] = [2]
        # lamp behind and well to the side of Kong (not behind his head): rim + long shadow toward the lens
        lamp = dict(base=tuple(K - to_cam * 2.6 + side * 3.4), aim=tuple(K + Vector((0, 0, 1.2))), energy=6500.0)
        for a in (kong, crew): a.set_glow(warm, None)
        focus = K + Vector((0, 0, 1.5)); acts = [kong, crew, drv]
    elif name in ("s13", "cal"):
        P0 = Vector(A["kong_phone_mark"])
        to_cam = Vector((0.12, -1.0, 0)).normalized()
        side = Vector((-to_cam.y, to_cam.x, 0))
        kong.place(tuple(P0), L.facing(to_cam) + 22)
        hcen = P0 + Vector((0, 0, hz))
        loc = hcen + to_cam * 3.0 + Vector((0, 0, 0.25)) - side * 0.15
        look = hcen + Vector((0, 0, -0.40)) - side * 0.10
        cpos = loc - to_cam * 1.25 - side * 0.48; cpos.z = -0.55
        crew.place(tuple(cpos), L.facing(-to_cam) + 15)
        cam = L.camera(G, tuple(loc), tuple(look), 30, aspect, hcen, 12.0, 24)
        kong.pose(dict(expr="guilty", arm_n=dict(hand=(0.26, 0.10), elbow=None, hand_shape="grip"),
                       prop_n=dict(type="phone", screen=G["phone"], angle=0, scale=1.5), head=(0, 10, 0.0, 0.04), lean=4), camera=cam)
        crew.pose(dict(expr="neutral"), camera=cam)
        drv.hide(True)
        post["sharp_idx"] = []
        lamp = dict(base=tuple(P0 - to_cam * 3.2 - side * 3.0), aim=tuple(P0 + Vector((0, 0, 1.4))), energy=8000.0)
        if name == "cal": lamp = dict(hide=True); shadow_from_lamp = False
        kong.set_glow(warm, None); crew.set_glow(None, None)
        focus = P0 + Vector((0, 0, 1.5)); acts = [kong, crew]
    elif name == "s20":
        drv.view_override = "q"
        hc0 = drv.world_of((0, -(drv.spec["legs"] + drv.spec["torso"] + 0.5)), 1.0)
        dm = Vector(A["door_mid"])
        loc = Vector((dm.x, dm.y, 0)) + right * (1.45 if v else 1.8) - fwd * (0.05 if v else 0.45) + Vector((0, 0, 2.05))
        cam0 = L.camera(G, tuple(loc), tuple(hc0), 26, aspect, hc0, 9.0, 22, roll=12.0)
        pose = dict(expr="head_lift", legs=dict(seated=True), arm_r="lap", arm_l="wheel", head=(8, -10, 0, -0.02), lean=4, gaze=(0.6, -0.2))
        drv.pose(pose, camera=cam0)
        hc = drv.head_world()
        look = hc + right * 0.25 + Vector((0, 0, -0.15))
        cam = L.camera(G, tuple(loc), tuple(look), 26 if v else 28, aspect, hc, 9.0, 22, roll=12.0)
        drv.pose(pose, camera=cam)
        L.fill(G, "look_fill_a", tuple(hc + fwd * 0.8 + right * 0.1 + Vector((0, 0, -0.1))), 10.0, size=0.3)
        L.fill(G, "look_fill_b", tuple(hc + right * 1.0 - fwd * 0.2 + Vector((0, 0, 0.5))), 18.0, (0.72, 0.82, 1.0), 0.5)
        kong.hide(True); crew.hide(True)
        L.door_glass(G, True)
        lamp = dict(base=tuple(Vector((dm.x, dm.y, 0)) + right * 2.6 + fwd * 3.8), aim=tuple(dm + right * 0.4 - fwd * 2.0), energy=7000.0, head_z=2.6)
        drv.set_glow((0.75, 0.9, 0.8), None)
        S.tune_flat(AMB=0.40, TINT=(0.72, 0.84, 1.0))        # inside the dark cabin: a brighter, more neutral fill so the pale skin reads
        focus = hc; acts = [drv]
    for a_ in (kong, crew, drv): a_.shadow_light = None     # the lamp object is rebuilt: drop stale references
    B.place_work_lamp(A, **lamp)
    bpy.context.view_layer.update()
    Lk = L.dominant_light(focus)
    if shadow_from_lamp:
        wl = [o for o in bpy.data.objects if o.type == "LIGHT" and o.data.type == "SPOT" and "work" in o.name.lower()]
        if wl: Lk = wl[0]
    if Lk is not None: S.shadow_link(acts, Lk)
    print("SHADOW LIGHT", name, Lk.name if Lk else None, flush=True)
    return post


def render(only, scale, aspect, frame=7):
    G = setup(); G["scale"] = scale
    os.makedirs(OUT, exist_ok=True)
    for n in only:
        t0 = time.time()
        post = shot(G, n, aspect)
        tag = "%s_%s" % (n, "916" if aspect == "9:16" else "169")
        r = G["B"].render6.render(os.path.join(OUT, tag), frame=frame, post_opts=post)
        print("TIME", tag, round(time.time() - t0, 1), r.get("cpu_render"), r.get("cpu_post"), flush=True)


def sheet():
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype(os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), 22)
    w, h, lab = 540, 960, 40
    s = Image.new("RGB", (3 * (2 * w + 12) + 2 * 30, h + lab + 10), (14, 14, 18)); d = ImageDraw.Draw(s)
    for i, n in enumerate(SHOTS):
        x = i * (2 * w + 12 + 30)
        d.text((x + 4, 8), "v8 cast FLAT in v9: " + TITLE[n], fill=(240, 240, 240), font=f)
        d.text((x + w + 16, 8), "ref E f_%03d" % REF[n], fill=(170, 170, 180), font=f)
        p = os.path.join(OUT, n + "_916.png")
        if os.path.exists(p): s.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
        s.paste(Image.open(os.path.join(PROJ, "ref", "e", "frames2", "f_%03d.png" % REF[n])).convert("RGB").resize((w, h), Image.LANCZOS), (x + w + 12, lab))
    s.save(os.path.join(HERE, "flat_in_v9.png")); print("flat_in_v9.png", s.size)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode"); ap.add_argument("--only", default=",".join(SHOTS)); ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    if a.mode == "render": render(a.only.split(","), a.scale, a.aspect)
    elif a.mode == "sheet": sheet()
