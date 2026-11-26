"""shots.py -- 3D Kong look test in the v4 expressway set (set imported read-only as a library).

python3 shots.py [--scale 0.5] [--quality final] [--threads 4] [--only low,mcu,ots,macro,mcu25] [--tag x]
  low    1. low close: Kong ~0.6 H, crashed sedan behind, foreground debris soft
  mcu    2. eye-level medium close, shallow DOF, city bokeh
  ots    3. over Kong's shoulder toward the hero car and the 3D driver
  macro  4. macro insert: the cutter's battery bars sharp, Kong's face soft behind
  mcu25  shot 2 again with the current 2.5D card Kong (v4/cast_dz09) for the comparison
Writes out/<shot>.png (+ _raw, EXR passes) and out/timing.json.
"""
import os, sys, math, json, time, argparse, random
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
SET = os.path.join(PROJ, "v4", "set_expressway")
for p in (HERE, SET): sys.path.insert(0, p) if p not in sys.path else None
import bpy
from mathutils import Vector, Matrix
import expressway as X
import kit
import kong3d as K
from bpy_extras.object_utils import world_to_camera_view

OUT = os.path.join(HERE, "out")
X.QUALITY.setdefault("k3", (6, 75, 3))        # runtime tier for this look test: 6 spp at 75 % + OIDN (set file untouched)
OTS_R, OTS_Z, OTS_L = -1.6, 3.0, 0.55


def frame_vectors():
    A = X._STATE["A"]; th = A["hero_heading"]
    right = Vector((math.cos(th), math.sin(th), 0)); fwd = Vector((-math.sin(th), math.cos(th), 0))
    return A, right, fwd


def set_cam(loc, look, lens, focus, k, name, roll=0.0, clip=0.02, scale=1.0):
    sc = bpy.context.scene
    cam = X.make_camera()
    cam.location = loc; cam.rotation_euler = kit.look_rot(tuple(loc), tuple(look), roll)
    cam.data.lens = lens; cam.data.clip_start = clip
    sc.render.resolution_x, sc.render.resolution_y = int(720 * scale), int(1280 * scale)
    sc.render.resolution_percentage = X._STATE.get("pct", 100)
    for ob in bpy.data.objects:
        for con in ob.constraints:
            if con.type == "TRACK_TO": con.target = cam
    cut = bpy.data.objects.get("cutter3d")          # the set's own staged cutter: ours is in Kong's hands
    if cut:
        for ob in [cut] + list(cut.children_recursive): ob.hide_render = True
    cam["preset"] = name; cam["aspect"] = "9:16"; cam["focus"] = tuple(focus); cam["dof_k"] = k
    bpy.context.view_layer.update()
    return cam


def screen_h(cam, pts):
    sc = bpy.context.scene
    ys = [world_to_camera_view(sc, cam, Vector(p)).y for p in pts]
    return max(ys) - min(ys), min(ys), max(ys)


# --------------------------------------------------------------------------------------------- foreground debris
def fg_debris(coll, centre, toward, seed=4):
    """a few close foreground pieces (glass shards, a reflector chunk, a cone) near a low camera."""
    rng = random.Random(seed)
    glass = K.m_plain("dz3_fg_glass", "#9fb4bf", 0.05, 0.0, wet=False, spec=0.9)
    red = K.m_plain("dz3_fg_red", "#b3121a", 0.2, wet=True)
    orange = K.m_plain("dz3_fg_cone", "#f26a16", 0.45, wet=True)
    white = K.m_plain("dz3_fg_white", "#e8e8e2", 0.3, wet=True)
    obs = []
    c = Vector(centre)
    side = Vector((-toward.y, toward.x, 0))
    for i in range(34):
        p = c + side * rng.uniform(-1.0, 1.0) + toward * rng.uniform(-0.3, 0.9)
        s = rng.uniform(0.03, 0.09)
        ob = K._rbox(f"fg_shard{i}", (s, s * rng.uniform(0.6, 1.4), 0.012), coll, glass, 0.004, 0)
        ob.location = (p.x, p.y, 0.008); ob.rotation_euler = (rng.uniform(-0.2, 0.2), rng.uniform(-0.2, 0.2), rng.uniform(0, 6.3))
        obs.append(ob)
    for i in range(3):
        p = c + side * rng.uniform(-0.6, 0.6) + toward * rng.uniform(0.0, 0.6)
        ob = K._rbox(f"fg_lamp{i}", (rng.uniform(0.10, 0.2), 0.07, 0.035), coll, red, 0.01, 0)
        ob.location = (p.x, p.y, 0.02); ob.rotation_euler = (0, 0, rng.uniform(0, 6.3)); obs.append(ob)
    # a knocked-over cone lying on its side
    cone = K._lathe("fg_cone", [(0.0, 0.0), (0.26, 0.0), (0.24, 0.05), (0.19, 0.12), (0.06, 0.75), (0.0, 0.78)], coll, orange, 24)
    band = K._lathe("fg_coneband", [(0.155, 0.30), (0.145, 0.33), (0.115, 0.45), (0.105, 0.48)], coll, white, 24)
    band.parent = cone
    p = c + side * 0.75 + toward * 0.25
    cone.location = (p.x, p.y, 0.22); cone.rotation_euler = (math.radians(90), 0, math.atan2(side.y, side.x) + 0.6)
    obs += [cone, band]
    for ob in obs: ob.pass_index = 4
    return obs


# ------------------------------------------------------------------------------------------------- kicker / fill
def kong_light(name, loc, target, energy, col, size, receivers):
    """a soft area light that lights only the cast (light linking), as a DP would add a bounce card on set."""
    ld = bpy.data.lights.new(name, "AREA"); ld.energy = energy; ld.color = col; ld.size = size
    lo = bpy.data.objects.new(name, ld); bpy.context.scene.collection.objects.link(lo)
    lo.location = loc; lo.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    lo.visible_camera = False; lo.visible_glossy = True
    rc = kit.coll(name + "_recv")
    if rc.name in bpy.context.scene.collection.children: bpy.context.scene.collection.children.unlink(rc)
    for ob in receivers:
        if ob.name not in rc.objects: rc.objects.link(ob)
    lo.light_linking.receiver_collection = rc
    lo.light_linking.blocker_collection = rc         # only the cast shadows this light (it reaches into the car)
    return lo


def cast_objects(fig):
    return [o for o in [fig.root] + list(fig.root.children_recursive) if o.type in ("MESH", "CURVE")]


# ----------------------------------------------------------------------------------------------------- the shots
def stage(A, right, fwd, wet=True):
    K._MAT.clear()
    kong = K.Figure3D("kong", "kong", wet=wet, cutter=True)
    drv = K.Figure3D("driver", "driver", wet=False, cutter=False)
    seat = Vector(A["driver_seat"])
    drv.place((seat.x, seat.y, seat.z - 0.08), math.degrees(math.atan2(fwd.x, -fwd.y)))
    # seated, hands on the wheel, head slumped (still)
    drv.pose(expr="still", seated=True, head=(-34, 12, -8), lean=(6, 0, 0),
             arm_r=dict(hand=(-0.22, -0.78, 0.62), pole=(-0.6, 0.0, 0.3)), arm_l=dict(hand=(0.22, -0.78, 0.62), pole=(0.6, 0.0, 0.3)))
    drv.set_pass_index(4)
    return kong, drv


def shot_setup(name, A, right, fwd, kong, drv, scale):
    K0 = Vector(A["kong_mark"])
    door = Vector(A["door_mid"]); pillar = Vector(A["door_pillar"])
    up = Vector((0, 0, 1))
    extra = []
    if name in ("low",):
        cam_loc = K0 + right * 2.75 - fwd * 0.55 + Vector((0, 0, 0.40))
        kong.place(K0, K.facing_toward(K0, cam_loc) + 14)
        kong.pose(expr="determined", head=(-12, -8, 4), lean=(-3, 0, -6), legs="wide",
                  cutter=dict(at=(-0.36, -0.40, 1.02), fwd=(0.58, -0.22, 0.78), up=(0.15, -0.95, 0.05),
                              pole_r=(-1.0, 0.3, 0.5), pole_l=(1.0, -0.4, 0.2)))
        kong.set_pass_index(2)
        bpy.context.view_layer.update()
        look = K0 + Vector((0, 0, 1.62)) + (cam_loc - K0).normalized() * 0.0
        cam = set_cam(cam_loc, look, 22, kong.head_world(), 3.2, "k3_low", roll=-2.0, scale=scale)
        toward = (K0 - cam_loc); toward.z = 0; toward.normalize()
        extra += fg_debris(kit.coll("FG3D"), cam_loc + toward * 0.75, toward)
        extra.append(kong_light("k3_fill_low", cam_loc + Vector((0.6, -0.4, 1.4)) - toward * 1.0, kong.head_world(), 60, (0.68, 0.66, 1.0), 2.5,
                                cast_objects(kong)))
    elif name in ("mcu", "mcu25"):
        cam_loc = K0 - fwd * 4.3 + right * 1.55 + Vector((0, 0, 2.30))
        kong.place(K0, K.facing_toward(K0, cam_loc) + 22)
        kong.pose(expr="tired", head=(-10, 4, -3), lean=(2, 0, -4),
                  cutter=dict(at=(-0.42, -0.30, 0.86), fwd=(0.30, -0.35, -0.88), up=(0.0, -0.9, 0.3), two_hands=False,
                              pole_r=(-1.0, 0.6, 0.6)),
                  arm_l=dict(hand=(0.36, -0.40, 1.30), pole=(1.0, 0.2, 0.6)))
        kong.set_pass_index(2)
        bpy.context.view_layer.update()
        look = K0 + Vector((0, 0, 1.95)) + fwd * 0.6
        cam = set_cam(cam_loc, look, 50, kong.head_world(), 6.0, "k3_mcu", scale=scale)
        extra.append(kong_light("k3_fill_mcu", cam_loc + Vector((-0.8, 0, 0.6)), kong.head_world(), 45, (0.68, 0.66, 1.0), 2.0,
                                cast_objects(kong)))
    elif name == "ots":
        tgt = Vector(A["driver_head"])
        kong.place(K0, K.facing_toward(K0, pillar) - 8)
        kong.pose(expr="shouting", head=(8, 4, 0), lean=(8, 0, 6), legs="wide",
                  cutter=dict(at=(0.02, -0.55, 1.18), fwd=(0.0, -1.0, 0.18), up=(0, 0, 1), pole_r=(-1.0, 0.4, 0.2), pole_l=(1.0, 0.3, 0.0)))
        kong.set_pass_index(4)
        bpy.context.view_layer.update()
        kf = (pillar - K0); kf.z = 0; kf.normalize()
        kr = kf.cross(up)                    # Kong's right
        cam_loc = K0 - kf * 2.2 + kr * OTS_R + Vector((0, 0, OTS_Z))
        look = tgt.lerp(kong.head_world(), OTS_L) + Vector((0, 0, -0.25))
        cam = set_cam(cam_loc, look, 30, tgt, 3.2, "k3_ots", scale=scale)
        extra.append(kong_light("k3_drv_ots", tgt + fwd * 0.9 + right * 0.5 + Vector((0, 0, 0.15)), tgt, 40,
                                (0.75, 0.95, 1.0), 0.5, cast_objects(drv)))     # dash / phone glow on the driver
        extra.append(kong_light("k3_rim_ots", K0 + kf * 0.8 - kr * 1.5 + Vector((0, 0, 3.0)), kong.head_world(), 50, (1.0, 0.55, 0.25), 1.0,
                                cast_objects(kong)))
    elif name == "macro":
        cam_dir = (-fwd * 0.80 + right * 0.60).normalized()     # Kong turns from the door toward the gridlock tail
        kong.place(K0, K.facing_toward(K0, K0 + cam_dir))
        cam_local = Vector((0.10, -1.95, 1.40))
        at = Vector((-0.44, -0.62, 1.44)); fw = Vector((1.0, 0.0, 0.08))
        g_local = at + fw * 0.5
        upv = (cam_local - g_local).normalized()
        kong.pose(expr="determined", head=(0, -8, 3), lean=(-3, 0, 0),
                  cutter=dict(at=tuple(at), fwd=tuple(fw), up=tuple(upv), pole_r=(-1.0, 0.2, -0.6), pole_l=(1.0, 0.0, -0.6)))
        kong.set_pass_index(4)
        bpy.context.view_layer.update()
        cut = kong.cutter
        g = cut.matrix_world @ Vector(cut["gauge"])
        hw = kong.head_world()
        cam_loc = kong.root.matrix_world @ cam_local
        look = g + (hw - g) * 0.45
        cam = set_cam(cam_loc, look, 40, g, 20.0, "k3_macro", scale=scale)
        extra.append(kong_light("k3_fill_macro", cam_loc + Vector((0.5, 0, 0.7)), hw, 25, (0.68, 0.66, 1.0), 1.5, cast_objects(kong)))
    return cam, extra


def measure(kong, cam):
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in (kong.head, kong.hair) for c in o.bound_box]
    pts += [kong.foot[s].matrix_world.translation for s in "rl"]
    h, y0, y1 = screen_h(cam, pts)
    return dict(kong_frac_h=round(h, 3), y_bottom=round(y0, 3), y_top=round(y1, 3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--quality", default="final")
    ap.add_argument("--threads", type=int, default=4); ap.add_argument("--only", default="low,mcu,ots,macro,mcu25")
    ap.add_argument("--tag", default=""); ap.add_argument("--adaptive", type=float, default=0.0); ap.add_argument("--dry", action="store_true")
    a = ap.parse_args(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    timing = {}
    tp = os.path.join(OUT, "timing.json")
    if os.path.exists(tp): timing = json.load(open(tp))
    for name in a.only.split(","):
        t0 = time.time()
        A = X.build()
        A, right, fwd = frame_vectors()
        X.setup_render(quality=a.quality, threads=a.threads)
        if a.adaptive: bpy.context.scene.cycles.adaptive_threshold = a.adaptive
        build_s = time.time() - t0
        if name == "mcu25":
            kong, drv = stage(A, right, fwd)
            for ob in [kong.root] + list(kong.root.children_recursive): ob.hide_render = True
            cam, extra = shot_setup("mcu", A, right, fwd, kong, drv, a.scale)
            cam["preset"] = "k25_mcu"
            sys.path.insert(0, os.path.join(PROJ, "v4", "cast_dz09"))
            import standins as SI, stage25 as st
            K0 = Vector(A["kong_mark"])
            k25 = st.Actor25("k25", "kong_wet", gap=0.05, ppd=150, mode="25d", sprite_dir=os.path.join(HERE, "tmp", "sprites"))
            k25.place(tuple(K0), K.facing_toward(K0, cam.location) + 22)
            k25.root.scale = (SI.CAST_SCALE,) * 3
            for ob in [k25.root] + list(k25.root.children_recursive):
                if ob.type == "MESH": ob.pass_index = 2
            try: st.sync_lights(key="flood_key", rims=["beacon_red_0", "sodium_1_-1", "beacon_blue_1"], shadow="flood_key")
            except Exception as ex: print("sync_lights:", ex)
            bpy.context.view_layer.update()              # root.matrix_world must be current for the camera-relative yaw
            k25.pose({"expr": "tired", "arm_r": "hold", "prop_r": {"type": "cutter", "bars": 3}}, camera=cam)
            # same framing rule as the 3D shot: the head at the same height on screen
        else:
            kong, drv = stage(A, right, fwd)
            cam, extra = shot_setup(name, A, right, fwd, kong, drv, a.scale)
        m = measure(kong, cam) if name != "mcu25" else {}
        print(name, m, flush=True)
        if a.dry: continue
        out = os.path.join(OUT, ("draft_" if a.scale < 1 else "") + name + a.tag)
        r = X.render_still(out, frame=7)
        r.update(m); r["build_s"] = round(build_s, 1); r["scale"] = a.scale; r["quality"] = a.quality; r["threads"] = a.threads
        r["cpu_total"] = round(r["cpu_render"] + r.get("cpu_post", 0), 1)
        timing[os.path.basename(out)] = {k: v for k, v in r.items() if not isinstance(v, str)}
        print(name, json.dumps(timing[os.path.basename(out)]), flush=True)
        json.dump(timing, open(tp, "w"), indent=1)


if __name__ == "__main__":
    main()
