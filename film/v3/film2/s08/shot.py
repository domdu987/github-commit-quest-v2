#!/usr/bin/env python3
"""shot.py -- film 2 take s08: shot 8 (g 535..604 + 7 handle frames in), room set NIGHT, book_insert.

    Top-down on the open book on the stool, candle beside it (NIGHT preset: moonlight + candle pool).  Nico's hands (the
    puppet's ink-ball hands on rubber-hose ink arms, coming in from the bottom of frame) hold the book; his right index finger
    goes to the diagram and traces the bolt -> rod -> wire -> ground on "ฟ้าผ่าชอบ / วิ่งลงเหล็ก".
      g 528..534  in-handle (10-frame dissolve from shot 7)
      g 535..555  slow top-down drift + roll over the whole open book, left hand holds the page, right hand on the right page
      g 556..566  snap push-in on the diagram (lands on "ฟ้าผ่าชอบ" g 562); the finger arrives at the bolt / rod tip
      g 566..604  the finger runs down the rod and along the wire to the ground stake (g 578..598, "วิ่งลงเหล็ก" g 590),
                  the camera follows it down (eased, never parks).  Hard cut out to shot 9.
Blender frame = g + 1.
    python3 shot.py stills a:b:step out_dir [scale] [samples]
    python3 shot.py final a:b [scale] [samples]          (resumable, raw/g_%04d.png + .json)
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import bpy                                              # noqa: E402
from mathutils import Vector, Euler                     # noqa: E402
import room as R                                        # noqa: E402
import render                                           # noqa: E402
from anim import ease, keys, lerp, clamp                # noqa: E402


def g_of(t):
    return int(round((t + 0.10) * 30))


G0, G1, H_IN = 535, 605, 7                       # shot 8 = [535, 605); 10f dissolve in -> 7 handle frames
RANGE = (G0 - H_IN, G1 - 1)
G_LIKES = g_of(18.647)                            # 562 "ฟ้าผ่าชอบ"
G_RUNS = g_of(19.562)                             # 590 "วิ่งลงเหล็ก"
PUSH = (556, 566)
POOL_RGB = (1.15, 1.05, 0.22)                      # set default (1.3, 0.95, 0.12)
INK = "#3a2832"                                    # puppet ink (hands, arms)
HAND_R = 0.052                                     # nico's hand ball radius (limb_w 0.05)
ARM_R = 0.026

BOOK = None                                        # filled after build: centre, size, page z


def page(sx, sy, lift=0.0):
    """book-page SVG coordinates (1.2 x 0.84, y down) -> world point on the page (plus lift in z)."""
    (cx, cy, cz), (bw, bh) = BOOK["centre"], BOOK["size"]
    x = cx - bw / 2 + sx / 1.2 * bw
    y = cy - bh / 2 + (0.84 - sy) / 0.84 * bh
    tilt = 0.035 * abs(sx - 0.6) / 0.6                      # the pages rise toward the outer edges
    return Vector((x, y, BOOK["page_z"] + tilt + lift))


# ----------------------------------------------------------------------------- the finger path on the diagram
PATH = [(0.20, 0.13), (0.262, 0.105), (0.27, 0.20), (0.27, 0.30), (0.33, 0.30), (0.44, 0.40), (0.44, 0.58), (0.44, 0.76), (0.50, 0.80)]
PATH_KEYS = [(G0, None), (552, (1.10, 0.78)), (PUSH[1], (0.20, 0.13)), (572, (0.262, 0.105)), (G_RUNS + 9, (0.50, 0.80))]


def _poly_at(u):
    seg = [math.dist(PATH[i], PATH[i + 1]) for i in range(len(PATH) - 1)]
    L = sum(seg) * clamp(u)
    for i, s in enumerate(seg):
        if L <= s or i == len(seg) - 1:
            k = clamp(L / s) if s > 0 else 0
            return (PATH[i][0] + (PATH[i + 1][0] - PATH[i][0]) * k, PATH[i][1] + (PATH[i + 1][1] - PATH[i][1]) * k)
        L -= s


def finger(g):
    """fingertip in page coords and its lift above the page."""
    rest = (1.10, 0.78)
    if g <= 552:
        wob = 0.006 * math.sin(g * 0.31)
        return (rest[0] + wob, rest[1] - 0.004 * math.sin(g * 0.23)), 0.03
    if g <= PUSH[1]:                                         # hand travels over the gutter to the bolt (arcs up)
        u = ease((g - 552) / float(PUSH[1] - 552), "cubic")
        p = (rest[0] + (0.20 - rest[0]) * u, rest[1] + (0.13 - rest[1]) * u)
        return p, 0.03 + 0.10 * math.sin(math.pi * u)
    if g <= 576:                                             # taps the bolt, slides to the rod point
        u = ease((g - PUSH[1]) / 10.0, "sine")
        return (0.20 + 0.062 * u, 0.13 - 0.025 * u), 0.012 + 0.02 * math.sin(math.pi * u)
    u = ease((g - 576) / float(G_RUNS + 9 - 576), "sine")    # down the rod, along the wire, into the ground
    return _poly_at(0.11 + 0.89 * u), 0.012


# ----------------------------------------------------------------------------- camera (top-down, up = +y, gentle roll)
def cam_at(g):
    #   page sx, sy of the frame centre, height above the page, roll deg, small tilt (deg about x)
    ks = [(RANGE[0], (0.62, 0.50, 0.90, -4.0, 2.0), "sine"),
          (PUSH[0], (0.58, 0.47, 0.82, 1.5, 1.0), "quint"),
          (PUSH[1], (0.26, 0.30, 0.47, 5.0, 0.0), "sine"),
          (578, (0.28, 0.33, 0.44, 6.0, -0.5), "sine"),
          (G_RUNS + 9, (0.42, 0.62, 0.43, 3.5, -1.0), "sine"),
          (G1 + 2, (0.44, 0.66, 0.42, 3.0, -1.2), "hold")]
    lin = keys(g, [(f, v, "lin") for f, v, e in ks])
    sx, sy, h, roll, tilt = lerp(keys(g, ks), lin, 0.15)
    c = page(sx, sy)
    # the frame centre sits a little below the subject: push the subject up to ~0.45 H (captions below)
    fov_h = h * 1280.0 / 782.2
    loc = Vector((c.x, c.y - 0.05 * fov_h, c.z + h))
    rot = Euler((math.radians(tilt), 0.0, math.radians(roll)), "XYZ")
    return loc, rot


# ----------------------------------------------------------------------------- hands
def _sphere(name, r, mat, coll):
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    import bmesh
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=r); bm.to_mesh(me); bm.free()
    for poly in me.polygons:
        poly.use_smooth = True
    me.materials.append(mat)
    return ob


def _tube(name, r, mat, coll):
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r, radius2=r, depth=1.0); bm.to_mesh(me); bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    return ob


def place_tube(ob, a, b):
    a, b = Vector(a), Vector(b)
    d = b - a
    ob.location = (a + b) / 2
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    ob.scale = (1.0, 1.0, d.length)


class Take(object):
    def __init__(self, quality="preview"):
        global BOOK
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = sc = bpy.context.scene
        pr = R.PRESETS["NIGHT"]                          # runtime tweak (set module untouched): yellower candle pool, so where
        pr["pools"] = [(pr["pools"][0][0], POOL_RGB, pr["pools"][0][2])]   # it meets the blue moon key the page goes cream, not pink
        self.A = R.build("NIGHT")
        BOOK = dict(self.A["book"])
        R.setup_render(sc, quality)
        sc.render.use_persistent_data = False
        sc.frame_start, sc.frame_end = 1, 2000
        cd = bpy.data.cameras.new("cam_s08"); cd.lens = 22.0; cd.sensor_width = 36.0; cd.sensor_fit = "AUTO"
        cd.clip_start = 0.01; cd.clip_end = 60
        self.cam = bpy.data.objects.new("cam_s08", cd); sc.collection.objects.link(self.cam); sc.camera = self.cam
        coll = bpy.data.collections.new("S08_HANDS"); sc.collection.children.link(coll)
        ink = R.K.mat_emit("S08_ink", INK, strength=1.0)
        self.hand_l = _sphere("hand_l", HAND_R, ink, coll)
        self.hand_r = _sphere("hand_r", HAND_R, ink, coll)
        self.arm_l = _tube("arm_l", ARM_R, ink, coll)
        self.arm_r = _tube("arm_r", ARM_R, ink, coll)
        self.thumb_l = _tube("thumb_l", ARM_R * 0.8, ink, coll)
        self.index_r = _tube("index_r", ARM_R * 0.62, ink, coll)
        for o in coll.objects:
            o.visible_diffuse = False; o.visible_glossy = False
            o.visible_shadow = False              # an unlit puppet hand: its moon shadow uncovered a pale warm blob on the page
        self.flame_mats = [m for m in bpy.data.materials if m.name.startswith("ROOM_NIGHT_e_ffcf6a")]
        self.info = {}

    def key(self, gs):
        for g in gs:
            f = g + 1
            loc, rot = cam_at(g)
            self.cam.location = loc; self.cam.rotation_euler = rot
            self.cam.keyframe_insert("location", frame=f); self.cam.keyframe_insert("rotation_euler", frame=f)
            # left hand: pinches the lower outer corner of the left page (thumb on the page), small breathing
            br = 0.004 * math.sin(g * 0.21)
            hl = page(0.07 + br, 0.79 + br, 0.045)
            self.hand_l.location = hl
            shoulder_l = hl + Vector((-0.22, -0.95, -0.25))
            place_tube(self.arm_l, shoulder_l, hl)
            place_tube(self.thumb_l, hl, page(0.11 + br, 0.74 + br, 0.03))
            # right hand: ball behind the fingertip, index stroke pointing up the page
            (fx, fy), lift = finger(g)
            tip = page(fx, fy, lift)
            fdir = Vector((-0.55, 1.0, 0.0)).normalized()
            hr = tip - fdir * 0.10 + Vector((0, 0, 0.02))
            self.hand_r.location = hr
            place_tube(self.index_r, hr, tip)
            shoulder_r = hr + Vector((0.30, -0.95, -0.25))
            place_tube(self.arm_r, shoulder_r, hr)
            for o in (self.hand_l, self.hand_r, self.arm_l, self.arm_r, self.thumb_l, self.index_r):
                o.keyframe_insert("location", frame=f)
                if o.rotation_mode == "QUATERNION":
                    o.keyframe_insert("rotation_quaternion", frame=f); o.keyframe_insert("scale", frame=f)
            # candle flicker
            fl = 5.0 * (1.0 + 0.10 * math.sin(g * 1.7) + 0.06 * math.sin(g * 4.3 + 1.0))
            for m in self.flame_mats:
                for n in m.node_tree.nodes:
                    if n.type == "EMISSION":
                        n.inputs["Strength"].default_value = fl
                        n.inputs["Strength"].keyframe_insert("default_value", frame=f)
            self.info[g] = dict(fingertip=[round(fx, 3), round(fy, 3)], lift=round(lift, 3),
                                tip_px=[round(v, 1) for v in render.world_to_screen(self.cam, tuple(tip), f)[:2]] if False else None)
        for ob in [self.cam] + [self.hand_l, self.hand_r, self.arm_l, self.arm_r, self.thumb_l, self.index_r]:
            ad = ob.animation_data
            if ad and ad.action:
                for fc in _fcurves(ad.action):
                    for kp in fc.keyframe_points:
                        kp.interpolation = "LINEAR"

    def report(self, g):
        f = g + 1
        self.scene.frame_set(f)
        (fx, fy), lift = finger(g)
        tip = page(fx, fy, lift)
        sx, sy = render.world_to_screen(self.cam, tuple(tip), f)[:2]
        return dict(g=g, fingertip_page=[round(fx, 3), round(fy, 3)], fingertip_px=[round(sx, 1), round(sy, 1)],
                    cam=[round(c, 3) for c in self.cam.location])

    def render(self, gs, out, scale=1.0, samples=12):
        self.scene.cycles.samples = samples
        return render.render_frames([g + 1 for g in gs], out, scale=scale, threads=2, scene=self.scene, camera=self.cam, verbose=False)


def _fcurves(action):
    try:
        return list(action.fcurves)
    except AttributeError:                                   # layered actions (Blender 4.4+/5)
        out = []
        for layer in action.layers:
            for strip in layer.strips:
                for cb in strip.channelbags:
                    out += list(cb.fcurves)
        return out


def parse(spec):
    a = [int(v) for v in spec.split(":")]
    return list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]
    if cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take(); Tk.key(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
            print("g %d %.1f s" % (g, st["wall"]), json.dumps(Tk.report(g)), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        todo = [g for g in gs if not (os.path.exists(os.path.join(out, "g_%04d.json" % g)))]
        print("final s08: %d to render" % len(todo), flush=True)
        if todo:
            Tk = Take(quality="final"); Tk.key(todo)
            for g in todo:
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g); os.replace(st["path"], png)
                rep = Tk.report(g); rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
                json.dump(rep, open(png[:-4] + ".json", "w"))
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
