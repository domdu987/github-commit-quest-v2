#!/usr/bin/env python3
"""shot.py -- film 2 take s11: shot 11 (g 799..882, handles 7 in / 6 out = g 792..888), tower set DAY, square_low.

    Low camera in the square (s01 shot 2's position, stone pier in shade at the left edge): baker, woman and the old man point
    up at the tower and laugh; the tower with the rod on its spire stands above them.
      g 792..827   low wide on the laughing crowd, slow creep in and rise ("จนคนทั้งเมือง")
      g 826..834   snap reframe closer on the three ("เรียกแท่งเหล็กนั้นว่า", g 828 / 836)
      g 846..856   punch-in on the rod far above: tilt up + snap zoom 22 -> 150 mm, lands on "ไม้จิ้มฟ้า" (g 856)
      g 856..888   the rod against the sky, small drift (out-handle g 883..888 for the 9-frame dissolve into shot 12)
Blender frame = g + 1.   python3 shot.py probe|stills|final ...  (as s09)
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast2"), os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast2                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


G0, G1, H_IN, H_OUT = 799, 883, 7, 6
RANGE = (G0 - H_IN, G1 + H_OUT - 1)
REFRAME = (826, 834)
PUNCH = (846, g_of(28.428))                       # 846 .. 856
CAM0 = Vector((0.25, -20.3, 0.55))
EXTRAS = {"woman": (-0.40, -16.0, 0.0), "old": (0.55, -14.9, 0.0), "baker": (1.45, -16.2, 0.0)}
POSES = {"woman": "extras_point_laugh_woman", "old": "extras_point_laugh_old", "baker": "extras_point_laugh"}
ROD_MID = Vector(T.ROD_TIP).lerp(Vector(T.ROD_BASE), 0.55)


def cam(g):
    """(loc, look_at, lens)"""
    a = (CAM0, Vector((0.10, -5.0, 9.2)), 22.0)
    b = (CAM0 + Vector((0.10, 0.45, 0.08)), Vector((0.12, -5.0, 9.45)), 22.0)
    c = (CAM0 + Vector((0.20, 0.85, 0.02)), Vector((0.20, -5.0, 8.6)), 22.0)
    d = (CAM0 + Vector((0.25, 1.05, 0.04)), Vector((0.24, -5.0, 8.8)), 22.0)
    e = (CAM0 + Vector((0.27, 1.10, 0.05)), ROD_MID + Vector((0.0, 0.0, -0.12)), 420.0)
    f_ = (CAM0 + Vector((0.31, 1.16, 0.06)), ROD_MID + Vector((0.03, 0.0, -0.04)), 440.0)
    T_ = lambda p: tuple(p[0]) + tuple(p[1]) + (p[2],)
    ks = [(RANGE[0], T_(a), "sine"), (REFRAME[0], T_(b), "quint"), (REFRAME[1], T_(c), "sine"),
          (PUNCH[0], T_(d), "quint"), (PUNCH[1], T_(e), "sine"), (RANGE[1] + 1, T_(f_), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.12)
    # zoom: interpolate the lens geometrically inside the punch
    if PUNCH[0] < g < PUNCH[1]:
        u = ease((g - PUNCH[0]) / float(PUNCH[1] - PUNCH[0]), "quint")
        lens = 22.0 * (420.0 / 22.0) ** u
    else:
        lens = k[6]
    return Vector(k[:3]), Vector(k[3:6]), lens


def extra_pose(n, g):
    _, base = cast2.STORY2[POSES[n]]
    p = dict(base)
    ph = {"woman": 0.0, "old": 1.3, "baker": 2.4}[n]
    lau = 0.5 + 0.5 * math.sin(g * 1.05 + ph)
    p["squash"] = (1.0 + 0.025 * lau, 1.0 - 0.03 * lau)
    p["head_roll"] = base.get("head_roll", 0) + 4 * math.sin(g * 0.52 + ph)
    p["lean"] = base.get("lean", 0) - 3 * lau
    p["t"] = (g - RANGE[0]) / 30.0 * 0.5 + base.get("t", 0.0)
    for side in ("arm_l", "arm_r"):
        arm = p.get(side)
        if isinstance(arm, dict) and arm.get("shape") == "point":           # jabbing finger
            arm = dict(arm); hx, hy = arm["hand"]; arm["hand"] = (hx + 0.02 * math.sin(g * 0.9 + ph), hy - 0.04 * lau); p[side] = arm
    return p


def _box(name, lo, hi, mat, coll):
    me = bpy.data.meshes.new(name)
    x0, y0, z0 = lo; x1, y1, z1 = hi
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me.from_pydata(v, [], f); me.update()
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        n = poly.normal
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (co.x / 2.0, co.y / 2.0) if abs(n.z) > 0.5 else ((co.y / 2.0, co.z / 2.0) if abs(n.x) > 0.5 else (co.x / 2.0, co.z / 2.0))
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); T.no_bounce(ob)
    return ob


class Take(object):
    def __init__(self, quality="preview"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = sc = bpy.context.scene
        self.A = T.build("DAY")
        T.setup_render(sc, quality)
        sc.render.use_persistent_data = False
        sc.cycles.transparent_max_bounces = 12
        sc.frame_start, sc.frame_end = 1, 3000
        T.set_rod(1)
        mk = bpy.data.objects.get("market")
        if mk is not None:
            mk.hide_render = True
        coll = bpy.data.collections.new("S11_FG"); sc.collection.children.link(coll)
        tex = os.path.join(V3, "set3d2", "tex_tower")
        stone = T.mat_lit("S11_stone", image=os.path.join(tex, "stone.png"), gain=0.9, shade_mul=0.42, form=(0.0, -0.05, 0.22))
        hide = T.mat_lit("S11_block", color="#6a4a3a")
        _box("s11_pier", (-1.15, -18.9, 0.0), (-0.3, -18.1, 7.0), stone, coll)
        _box("s11_pier_cap", (-1.35, -19.1, 7.0), (-0.1, -17.9, 7.5), stone, coll)
        _box("s11_block", (-9.0, -40.0, 0.0), (4.0, -21.6, 16.0), hide, coll)
        self.cam = camrig.make_camera(sc, name="cam_s11")
        self.cam.data.clip_start = 0.02; self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.extras = {}
        for n in EXTRAS:
            a = actors.Actor(n, n); a.build(sprites.DEFAULT_CANVAS[n], sd, contact=True); a.head_flip = False; T.no_bounce(a.card)
            self.extras[n] = a
        self.anch = {}

    def pose(self, gs):
        for g in gs:
            f = g + 1
            loc, look, lens = cam(g)
            camrig.key_camera(f, loc, look, lens=lens, cam=self.cam, interp="LINEAR", easing="AUTO")
            for n, a in self.extras.items():
                a.place(f, EXTRAS[n])
        for g in gs:
            f = g + 1
            self.scene.frame_set(f)
            for n, a in self.extras.items():
                a.pose(f, extra_pose(n, g), camera=self.cam)
        fr = [g + 1 for g in gs]
        for a in self.extras.values():
            for f, r in zip(fr, a.render_sprites(320, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s11: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def report(self, g):
        f = g + 1
        self.scene.frame_set(f)
        out = dict(g=g, lens=round(self.cam.data.lens, 1), heads={})
        for a in self.extras.values():
            res = a.feet.get(f); hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        out["rod_tip"] = [round(x, 1) for x in render.world_to_screen(self.cam, T.ROD_TIP, f)[:2]]
        out["rod_base"] = [round(x, 1) for x in render.world_to_screen(self.cam, T.ROD_BASE, f)[:2]]
        return out

    def render(self, gs, out, scale=1.0, samples=12):
        self.scene.cycles.samples = samples
        return render.render_frames([g + 1 for g in gs], out, scale=scale, threads=2, scene=self.scene, camera=self.cam, verbose=False)


def parse(spec):
    a = [int(v) for v in spec.split(":")]
    return list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]
    if cmd == "probe":
        Tk = Take(); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)))
    elif cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take(); Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
            print("g %d %.1f s" % (g, st["wall"]), json.dumps(Tk.report(g)), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.json" % g))]
        print("final s11: %d to render" % len(todo), flush=True)
        if todo:
            Tk = Take(quality="final"); Tk.pose(todo)
            for g in todo:
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g); os.replace(st["path"], png)
                rep = Tk.report(g); rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
                json.dump(rep, open(png[:-4] + ".json", "w"))
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
