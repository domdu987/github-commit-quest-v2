#!/usr/bin/env python3
"""shot.py -- film 2 take s12: shots 12 and 13, tower set NIGHT_STORM, rod nailed on top (set_rod(1)).

    shot 12  g 883..958  high angle inside the bell chamber: padre, baker, woman and nico all pull ropes hard, the bell swings
                         hard overhead, rain streaks outside the arches, two lightning flashes; snap reframe onto nico (lifted
                         off his feet by his rope) on "ระฆังกันรัว ๆ".  9-frame dissolve in: handle g 877..882.
    shot 13  g 959..1025 10-frame dissolve (mixed here, g 954..963): town_wide, flashes light the clouds again and again, a
                         forked bolt far over the hills, never the tower; eased push up to the tower top with the rod on it,
                         reframe on "แต่ไม่ผ่า".  12-frame dissolve out: handle g 1026..1033.

Blender frame of (shot s, film frame g) = 1000 * (s - 12) + g + 1.

    python3 shot.py probe 12|13 a:b:step
    python3 shot.py stills 12|13 a:b:step <out_dir> [scale] [samples]
    python3 shot.py final 12|13 a:b[:step] [scale] [samples]      (resumable, raw/s<shot>/g_%04d.png + .json)
"""
import math, os, sys, time, json, random

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


# ----------------------------------------------------------------------------- timing
G0, G_S13, G_END = 883, 959, 1026               # round(29.42*30), round(31.98*30), round(34.19*30)
H_IN, DISS, H_OUT = 6, 10, 8                    # 9f dissolve in -> 6 handle; 10f internal; 12f out -> 8 handle
D0 = G_S13 - DISS // 2                          # 954: first mixed frame
RANGES = {12: (G0 - H_IN, D0 + DISS + 1), 13: (D0 - 2, G_END + H_OUT - 1)}     # 877..965, 952..1033
G_RUA = g_of(31.128)                            # 937 "ระฆังกันรัว ๆ"
G_NOT = g_of(33.058)                            # 995 "แต่ไม่ผ่า"
SNAP12 = (G_RUA - 7, G_RUA + 1)                 # snap reframe onto nico
SNAP13 = (G_NOT - 6, G_NOT + 4)
FLASH12 = [(896, [1.0, 0.35, 0.9, 0.2, 0.0]), (944, [0.8, 0.25, 0.0])]
FLASH13 = [(961, [0.9, 0.3, 0.0]), (978, [1.0, 0.4, 1.0, 0.5, 0.15, 0.0]), (1004, [0.7, 0.2, 0.0]), (1019, [1.0, 0.35, 0.8, 0.2, 0.0])]
BOLT13 = [(978, 981, "bolt_far_r"), (1019, 1021, "bolt_far_l")]   # forked bolts far over the hills, well away from the tower
BELL_P = 34.0                                   # bell swing period (frames)
BELL_A = 36.0


def bf(shot, g):
    return 1000 * (shot - 12) + int(g) + 1


def bell_angle(g):
    return BELL_A * math.sin(2 * math.pi * (g - G0) / BELL_P)


def pull(g, phase=0.0):
    """0 = hands up (rope up), 1 = pulled down.  Ropes are pulled as the bell swings back."""
    return 0.5 - 0.5 * math.cos(2 * math.pi * (g - G0) / BELL_P + phase)


# ----------------------------------------------------------------------------- rain
def build_rain(name, center, radius, z0, z1, n, seed, inner=0.0, box=None, length=0.55, width=0.012, k=0.35, avoid=None):
    """Thin emissive streaks (camera rays only, additive) in a cylinder (or box) shell; a 6 D tall periodic column, tiled
    so that moving the object down by (speed * g mod 6) loops without a seam."""
    r = random.Random(seed)
    me = bpy.data.meshes.new(name)
    verts, faces = [], []
    per = 6.0
    base = []
    for i in range(n):
        if box:
            x = r.uniform(box[0], box[1]); y = r.uniform(box[2], box[3])
        else:
            while True:
                a = r.uniform(0, 2 * math.pi); rr = math.sqrt(r.uniform(inner ** 2, radius ** 2))
                x, y = center[0] + rr * math.cos(a), center[1] + rr * math.sin(a)
                if rr >= inner and not (avoid and avoid[0] < x < avoid[1] and avoid[2] < y < avoid[3]):
                    break
        base.append((x, y, r.uniform(0, per), r.uniform(0.7, 1.3)))
    nt = int(math.ceil((z1 - z0) / per)) + 1
    slant = Vector((0.12, 0.05, -1.0)).normalized()
    for t in range(nt):
        for (x, y, z, s) in base:
            zz = z0 + z + t * per
            if zz > z1 + per:
                continue
            c = Vector((x, y, zz)); L = length * s
            side = Vector((1, -0.35, 0)).normalized() * width * 0.5
            a, b = c, c + slant * L
            vi = len(verts)
            verts += [a - side, a + side, b + side, b - side]
            faces.append((vi, vi + 1, vi + 2, vi + 3))
            side2 = Vector((0.35, 1, 0)).normalized() * width * 0.5      # crossed quad: reads from any yaw
            vi = len(verts)
            verts += [a - side2, a + side2, b + side2, b - side2]
            faces.append((vi, vi + 1, vi + 2, vi + 3))
    me.from_pydata([tuple(v) for v in verts], [], faces); me.update()
    m = bpy.data.materials.get("S12_rain") or T.mat_emit("S12_rain", "#b9c8ff", strength=k, camera_only=True, additive=True)
    me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.visible_shadow = False
    T.no_bounce(ob)
    return ob


def key_rain(ob, f, g, speed=0.95):
    ob.location = (-0.12 * speed * g % 0.72, 0.0, -((speed * g) % 6.0))
    ob.keyframe_insert("location", frame=f)
    for fc in T._fcurves(ob):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"


def build_far_bolts():
    """Two forked bolts in front of the painted plate (r about 60 D), 16-19 deg either side of the shot-13 view axis: they
    strike the far hills, never the tower."""
    coll = bpy.context.scene.collection
    bm = T.mat_emit("TWR_bolt", "#f2f2ff", strength=9.0, camera_only=True)
    gm = T.mat_emit("TWR_bolt_glow", "#8c9cff", strength=0.45, camera_only=True, additive=True)
    out = {}
    for nm, top, end, seed in (("bolt_far_r", (57, 44, 62), (50, 36, 6), 21), ("bolt_far_l", (0, 68, 60), (-6, 62, 5), 33)):
        pts = T._bolt_path(top, end, seed, n=22, jag=2.6); n_ = len(pts) - 1
        rad = [1.0 - 0.5 * i / n_ for i in range(n_ + 1)]
        a = T._curve_obj(nm, pts, 0.28, bm, coll, rad); g = T._curve_obj(nm + "_glow", pts, 0.9, gm, coll, rad)
        br = T._bolt_path(pts[6], (pts[6][0] + 10, pts[6][1] - 2, pts[6][2] - 22), seed + 1, n=10, jag=2.0)
        b = T._curve_obj(nm + "_br", br, 0.14, bm, coll, [1.0 - 0.8 * i / (len(br) - 1) for i in range(len(br))])
        for o in (a, g, b):
            o.visible_shadow = False; o.hide_render = True
        out[nm] = [a, g, b]
    return out


# ----------------------------------------------------------------------------- staging
Z = T.Z_CH
MARK = {"padre": (-1.1, -1.05, Z), "nico": (-0.9, 0.45, Z), "baker": (0.8, 1.35, Z), "woman": (0.55, -1.45, Z)}
POSE = {"padre": "padre_ring", "nico": "nico_pull_rope", "baker": "extras_ring", "woman": "extras_ring_woman"}
PHASE = {"padre": 0.0, "nico": 0.5, "baker": 0.9, "woman": 0.3}
ROPE_UP = 3.0                                    # canvas raised by this much so the drawn rope runs out of frame
NICO_LIFT = cast2.STORY2_META["nico_pull_rope"]["lift"]


def lift_of(name, g):
    if name != "nico":
        return 0.0
    u = pull(g, PHASE["nico"])
    return NICO_LIFT + 0.28 * (1.0 - u)          # he rides up with the rope, comes down when he hauls it


# cameras: (loc, look) pairs
C12_A = (Vector((-4.4, -0.35, 19.75)), Vector((0.0, -0.05, 16.5)))         # outside the west arch, rain in front
C12_B = (Vector((-4.1, -0.25, 19.65)), Vector((0.0, 0.0, 16.6)))
C12_C = (Vector((-3.25, 0.25, 19.35)), Vector((-0.9, 0.3, 17.25)))         # onto nico
C12_D = (Vector((-3.15, 0.3, 19.3)), Vector((-0.9, 0.32, 17.3)))


def _k(pair):
    return tuple(pair[0]) + tuple(pair[1])


def cam12(g):
    g0, g1 = RANGES[12]
    ks = [(g0, _k(C12_A), "sine"), (SNAP12[0], _k(C12_B), "quint"), (SNAP12[1], _k(C12_C), "sine"), (g1, _k(C12_D), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.2)
    loc, look = Vector(k[:3]), Vector(k[3:])
    # the ringing shakes the chamber: a small jolt on every haul
    j = 0.018 * math.sin(2 * math.pi * (g - G0) / (BELL_P / 2.0))
    return loc + Vector((0, 0, j)), look + Vector((0.6 * j, 0, j))


C13_A = (Vector((-13.4, -35.0, 8.0)), Vector((0.4, 0.0, 13.6)))
C13_B = (Vector((-12.4, -32.6, 9.2)), Vector((0.3, 0.0, 15.0)))
C13_C = (Vector((-6.2, -16.4, 19.6)), Vector((0.1, 0.0, 25.8)))           # up to the tower top: the rod is there, untouched
C13_D = (Vector((-5.8, -15.6, 20.1)), Vector((0.1, 0.0, 26.1)))


def cam13(g):
    g0, g1 = RANGES[13]
    ks = [(g0, _k(C13_A), "sine"), (SNAP13[0], _k(C13_B), "quint"), (SNAP13[1], _k(C13_C), "sine"), (g1, _k(C13_D), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.2)
    return Vector(k[:3]), Vector(k[3:])


CAMS = {12: cam12, 13: cam13}


def ringer_pose(name, g):
    cast, base = cast2.STORY2[POSE[name]]
    p = dict(base)
    u = pull(g, PHASE[name])
    dy = 0.30 * u - 0.10
    for side in ("arm_l", "arm_r"):
        a = p.get(side)
        if isinstance(a, dict) and "hand" in a:
            a = dict(a); hx, hy = a["hand"]; a["hand"] = (hx, hy + dy); p[side] = a
    p["lean"] = p.get("lean", 0) + 5 * u
    p["squash"] = (1.0 + 0.03 * u, 1.0 - 0.035 * u) if name != "nico" else (0.97 + 0.02 * u, 1.04 - 0.03 * u)
    p["head_roll"] = p.get("head_roll", 0) + 3 * math.sin(2 * math.pi * (g - G0) / BELL_P + PHASE[name])
    bl = {"padre": [890, 925, 950], "nico": [900, 947], "baker": [893, 931], "woman": [907, 940]}[name]
    p["blink"] = blink(g, bl)
    return p


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, shot, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.shot = shot
        self.scene = scene = bpy.context.scene
        self.A = T.build("NIGHT_STORM")
        T.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 16
        scene.frame_start, scene.frame_end = 1, 3000
        T.set_rod(1)
        mk = bpy.data.objects.get("market")
        if mk is not None:
            mk.hide_render = True
        self.cam = camrig.make_camera(scene, name="cam_s12")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        self.actors = {}
        if shot == 12:
            self.rain = [build_rain("rain_near", (0, 0), 6.0, 12.0, 26.0, 700, 3, inner=2.75, k=0.40, avoid=(-5.2, -2.5, -1.1, 1.1)),
                         build_rain("rain_far", (0, 0), 30.0, 0.0, 30.0, 1400, 5, inner=6.0, length=1.2, width=0.03, k=0.16)]
            sd = os.path.join(TMP, "sprites")
            for n in MARK:
                cast = cast2.STORY2[POSE[n]][0]
                c = sprites.DEFAULT_CANVAS[cast]
                a = actors.Actor(n, cast)
                a.build((c[0], c[1] - ROPE_UP, c[2], c[3]), sd, contact=dict(width=0.9, depth=0.42, color="#141428", opacity=0.45))
                a.head_flip = True                    # moon key from screen-right (camera looks +x)
                T.no_bounce(a.card)
                self.actors[n] = a
        else:
            self.rain = [build_rain("rain_town", (-1, -6), 13.0, 0.0, 30.0, 900, 7, length=1.3, width=0.035, k=0.14,
                                    avoid=(-11.0, -2.5, -24.0, -9.0))]
        self.bolts = build_far_bolts() if shot == 13 else {}
        if shot == 13:                                  # the rod must read from the town: a thicker copy (2.2x radius)
            rod = T.STATE["rod_objs"][0]
            m = T.mat_emit("S13_rod_wet", "#a3aee0", strength=0.95)      # wet iron catching the moonlight: reads on the dark sky
            mb = T.MB(); bx, by, bz = T.ROD_BASE; tz = T.ROD_TIP[2]
            mb.frustum((bx, by, bz), (bx, by, tz - 0.2), 0.075, 0.075, m, seg=8); mb.frustum((bx, by, tz - 0.2), (bx, by, tz), 0.1, 0.0, m, seg=8)
            ob = mb.obj("rod_thick", bpy.context.scene.collection, hull=0.02); T.no_bounce(ob)
            rod.hide_render = True
        self.info = {}
        self.anch = {}
        if verbose:
            print("s12: shot %d built in %.1f s" % (shot, time.time() - t0), flush=True)

    def key(self, gs):
        shot = self.shot
        for g in gs:
            f = bf(shot, g)
            loc, look = CAMS[shot](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            T.set_bell(bell_angle(g) if shot == 12 else 0.0, frame=f)
            for ob in self.rain:
                key_rain(ob, f, g, 0.95 if shot == 12 else 1.4)
            fl = 0.0
            for (s, seq) in (FLASH12 if shot == 12 else FLASH13):
                if s <= g < s + len(seq):
                    fl = seq[g - s]
            T.flash(fl, frame=f)
            if shot == 13:
                T.set_bolt(False, frame=f)
                for (a, b, nm) in BOLT13:
                    for o in self.bolts[nm]:
                        o.hide_render = not (a <= g <= b)
                        o.keyframe_insert("hide_render", frame=f)
            for n, a in self.actors.items():
                x, y, z = MARK[n]
                a.place(f, (x, y, z + lift_of(n, g)))

    def pose(self, gs):
        self.key(gs)
        cam = self.cam
        for g in gs:
            f = bf(self.shot, g)
            self.scene.frame_set(f)
            for n, a in self.actors.items():
                a.pose(f, ringer_pose(n, g), camera=cam)
        fr = [bf(self.shot, g) for g in gs]
        for n, a in self.actors.items():
            for f, r in zip(fr, a.render_sprites(320 if n == "nico" else 256, frames=fr)):
                self.anch[(n, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s12: WARNING sprite of %s clipped on frame %d" % (n, f), flush=True)

    def report(self, g):
        f = bf(self.shot, g)
        self.scene.frame_set(f)
        loc, look = CAMS[self.shot](g)
        v = look - loc
        out = dict(shot=self.shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={}, bell=round(bell_angle(g), 1) if self.shot == 12 else 0)
        for n, a in self.actors.items():
            if f not in a.poses:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(n, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][n] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        out["rod_tip"] = [round(x, 1) for x in render.world_to_screen(self.cam, T.ROD_TIP, f)[:2]]
        return out

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.cycles.samples = samples
        return render.render_frames([bf(self.shot, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    shot = int(sys.argv[2])
    gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    if cmd == "probe":
        Tk = Take(shot)
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)))
    elif cmd == "stills":
        out = sys.argv[4]
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        Tk = Take(shot)
        Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]
            dst = os.path.join(out, "s%d_g_%04d.png" % (shot, g))
            os.replace(st["path"], dst)
            print("shot %d g %d  %.1f s wall %.1f cpu  %s" % (shot, g, st["wall"], st["cpu"], json.dumps(Tk.report(g)["heads"])), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw", "s%d" % shot)
        os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            ok = os.path.exists(png) and os.path.exists(js)
            if ok:
                m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
            if not ok:
                todo.append(g)
        print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
        if todo:
            Tk = Take(shot, quality="final")
            Tk.pose(todo)
            for g in todo:
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
