#!/usr/bin/env python3
"""shot.py -- film 2 take s01: shots 1-3 (the opening, g 0..210 + 7 handle frames), tower set DAY.

    shot 1  g   0.. 66  close on nico kneeling on the spire tip, hammering the iron strap round the rod (hits g 12, 27, 42,
                        a small shake on each), snap pull-out g 44..60 up and away: he is on the very top, the town far below
    shot 2  g  67..121  hard cut: padre in the square (padre_order, angry, pointing up), the tower with tiny nico behind;
                        snap punch-in on padre g 100..108 (lands on "ทิ้งเฉยเลย" g 105); mouth closed
    shot 3  g 122..210  12-frame dissolve (g 116..127): town_wide establishing, slow eased push and rise, baker / woman / old
                        and padre in the square, tiny nico still hammering on top.  Handle out g 211..217.

Blender frame of (shot s, film frame g) = 1000 * (s - 1) + g + 1 (the shots overlap in the dissolve).
Foreground masses in shade (the look note "DAY exteriors too few darks"): shot 2 a stone pier at the left edge, shot 3 the
brick pier and low wall at the left edge (shade-only material: an off-screen roof's shadow would also darken the whole near square).

    python3 shot.py probe 1|2|3 a:b:step
    python3 shot.py render <shot> <a:b[:step]> <out_dir> [--scale 0.5] [--samples 6]
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast2"), os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast2                                            # noqa: E402  (first: registers nico, padre, extras)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):                     # narration time -> film frame of an event
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing
G_S2, G_S3, G_END, H_OUT = 67, 122, 211, 7      # shot boundaries round(t*30): 2.24, 4.06, 7.04 s
DISS = 12                                        # shot 2 -> 3 dissolve, frames G_S3-6 .. G_S3+5
HANDLE = DISS // 2 + 2
RANGES = {1: (0, G_S2 - 1), 2: (G_S2, G_S3 + HANDLE - 1), 3: (G_S3 - HANDLE, G_END + H_OUT - 1)}
HITS = [g_of(0.3), g_of(0.8), g_of(1.3)]         # 12, 27, 42
HITS_ALL = HITS + list(range(HITS[-1] + 16, G_END + H_OUT + 8, 16))    # he keeps hammering (tiny) in shots 2 and 3
PULL = (44, 60)                                  # snap pull-out (16 frames), centre on "บนยอดหอระฆัง" g 46..
PUNCH = (100, 108)                               # snap punch-in on padre, lands on "ทิ้งเฉยเลย" (g 105)
G_1769 = g_of(4.51)                              # 138
G_BRESCIA = g_of(5.40)                           # 165


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


# ----------------------------------------------------------------------------- staging
ROD = Vector(T.ROD_BASE)
HAND_L_W = Vector((0.10, -0.035, 28.05))         # left hand guides the rod just above the finial (the rod slides down through it)
STRIKE_W = Vector((0.06, -0.06, 28.68))          # hammer head lands on the rod's side, above his head (against the sky)
YAW_S1 = -48.0                                   # shot 1 view: from the south-east, looking north-west
_f = Vector((math.sin(math.radians(YAW_S1)), math.cos(math.radians(YAW_S1)), 0.0))
_r = Vector((_f.y, -_f.x, 0.0))
NICO_FEET = Vector((0.05, 0.0, 26.95)) - _r * 0.52 - _f * 0.45
PADRE_S2 = (1.25, -16.4, 0.0)
CAM_S2 = Vector((0.25, -20.3, 1.05))
SQ = T.SQ_MARKS
PADRE_S3 = (1.3, -8.2, 0.0)
EXTRAS_S3 = {"baker": (-3.2, -7.8, 0.0), "woman": (3.4, -9.4, 0.0), "old": (-0.9, -8.8, 0.0)}


ROD_STEP = 0.15                                  # the rod sits 3 steps high at the start and drops one step on every hit of shot 1


def rod_off(g):
    n = sum(1 for s in HITS if g >= s)
    return ROD_STEP * (3 - n)


def hammer_u(g):
    """0 = hammer raised, 1 = head on the strap; small extra lift (negative) as anticipation."""
    u = 0.0
    for s in HITS_ALL:
        if s - 8 <= g <= s + 8:
            if g <= s - 5:
                u = -0.18 * ease((g - (s - 8)) / 3.0, "sine")
            elif g <= s:
                u = -0.18 + 1.18 * ease((g - (s - 5)) / 5.0, "cubic_in")
            else:
                u = 1.0 - ease((g - s - 1) / 7.0, "sine") if g > s + 1 else 1.0
    return u


def shake(g, amp):
    """decaying jolt after every hit of shot 1: (dx, dz) offsets of the look point in D."""
    dx = dz = 0.0
    for i, s in enumerate(HITS):
        d = g - s
        if 0 <= d <= 6:
            a = amp * math.exp(-0.55 * d)
            dz += a * math.cos(d * 2.2) * (1 if i % 2 == 0 else -1)
            dx += 0.6 * a * math.sin(d * 2.9 + i)
    return dx, dz


def sph(look, dist, yaw, pitch):
    yr, pr = math.radians(yaw), math.radians(pitch)
    d = Vector((math.sin(yr) * math.cos(pr), math.cos(yr) * math.cos(pr), math.sin(pr)))
    return look - d * dist


def cam1(g):
    #           dist  yaw    pitch  look x, y, z
    ks = [(0, (3.95, YAW_S1 - 3.0, -15.0, -0.12, -0.17, 28.32), "sine"),
          (PULL[0], (3.45, YAW_S1 + 2.0, -13.0, -0.12, -0.17, 28.28), "quint"),
          (PULL[1], (16.5, YAW_S1 + 9.0, -31.0, -0.6, -0.6, 24.6), "sine"),
          (G_S2 + 4, (17.4, YAW_S1 + 10.5, -32.0, -0.6, -0.6, 24.4), "hold")]
    lin = keys(g, [(f, v, "lin") for f, v, e in ks])
    k = lerp(keys(g, ks), lin, 0.12)                # a constant-speed share: the camera never parks
    dist, yaw, pitch, lx, ly, lz = k
    look = Vector((lx, ly, lz))
    dx, dz = shake(g, 0.035 * dist / 3.0)
    look = look + _r * dx + Vector((0, 0, dz))
    return sph(look, dist, yaw, pitch), look


def cam2(g):
    a = (CAM_S2, Vector((0.05, -5.0, 9.6)))
    b = (CAM_S2 + Vector((0.22, 0.55, 0.10)), Vector((0.22, -5.0, 9.85)))
    head = Vector((PADRE_S2[0], PADRE_S2[1], 2.95))
    pc = head + (CAM_S2 - head).normalized() * 3.0 + Vector((-0.35, 0.0, -0.25))
    c = (pc, head + Vector((-0.42, 0.0, 0.22)))
    d = (pc + Vector((-0.06, 0.18, 0.02)), head + Vector((-0.40, 0.0, 0.26)))
    ks = [(G_S2, tuple(a[0]) + tuple(a[1]), "cubic_out"),
          (PUNCH[0], tuple(b[0]) + tuple(b[1]), "quint"),
          (PUNCH[1], tuple(c[0]) + tuple(c[1]), "sine"),
          (G_S3 + HANDLE, tuple(d[0]) + tuple(d[1]), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.3)
    return Vector(k[:3]), Vector(k[3:])


CAM3_A = (Vector((-13.4, -35.2, 8.2)), Vector((0.2, 0.0, 7.0)))
CAM3_B = (Vector((-11.2, -30.6, 11.0)), Vector((0.5, 0.0, 7.0)))


def cam3(g):
    g0, g1 = RANGES[3]
    mid = (CAM3_A[0].lerp(CAM3_B[0], 0.52) + Vector((0.25, 0, 0)), CAM3_A[1].lerp(CAM3_B[1], 0.5) + Vector((0.25, 0, 0.1)))
    ks = [(g0, tuple(CAM3_A[0]) + tuple(CAM3_A[1]), "cubic"),
          (G_BRESCIA, tuple(mid[0]) + tuple(mid[1]), "cubic"),
          (g1, tuple(CAM3_B[0]) + tuple(CAM3_B[1]), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.18)
    return Vector(k[:3]), Vector(k[3:])


CAMS = {1: cam1, 2: cam2, 3: cam3}


# ----------------------------------------------------------------------------- poses
NH_CAST, NH_POSE = cast2.STORY2["nico_hammer"]
RAISE_HAND = (0.64, -0.08)                       # hand up beside the head, hammer head high above it in the sky (big arc down to the rod)
RAISE_ANG = -78.0
STRIKE_ANG = -8.0
RAISE_TIP = (RAISE_HAND[0] + 0.36 * math.cos(math.radians(RAISE_ANG)), RAISE_HAND[1] + 0.36 * math.sin(math.radians(RAISE_ANG)))


def nico_pose(g):
    p = dict(NH_POSE)
    p.pop("prop_l", None)                         # the rod is the set's own (set_rod(1)); his left hand grips it
    u = hammer_u(g)
    sq = 0.0
    for s in HITS_ALL:
        sq += pulse(g, s - 1, s + 1, s + 6, 1.0)
    p["squash"] = (1.0 + 0.03 * sq, 1.0 - 0.035 * sq)
    p["head_roll"] = -6 + 4 * u
    p["lean"] = 8 - 6 * clamp(u)
    p["blink"] = blink(g, [3, 33, 88, 150, 196])
    p["gaze"] = (0.8, -0.2)
    p["prop_r"] = dict(type="hammer", angle=-105.0)
    return p, u


def padre_pose(g, shot):
    cast, pose = cast2.STORY2["padre_order"]
    p = dict(pose)
    shakeh = math.sin(g * 0.9) * 2.5                  # furious jabbing of the pointing finger
    arm = dict(p["arm_l"]); hx, hy = arm["hand"]
    jab = 0.06 * math.sin(g * 0.75) + (0.05 * pulse(g, PUNCH[0] - 2, PUNCH[0] + 3, PUNCH[1] + 4, 1.0) if shot == 2 else 0)
    arm["hand"] = (hx - 0.02 * math.cos(g * 0.75), hy - jab)
    p["arm_l"] = arm
    p["head_roll"] = -7 + shakeh
    p["lean"] = -3 + 1.5 * math.sin(g * 0.37)
    p["blink"] = blink(g, [81, 118, 160, 199])
    p["squash"] = (1.0 + 0.012 * math.sin(g * 0.75), 1.0 - 0.012 * math.sin(g * 0.75))
    return p


def extra_pose(name, g):
    if name == "old":
        cast, pose = cast2.STORY2["old_stick"]
        p = dict(pose); p["head_roll"] = -3 + 2 * math.sin(g * 0.11); p["blink"] = blink(g, [140, 190])
        return p
    if name == "baker":
        return dict(yaw=0.35, pitch=-0.3, expr="neutral", head_roll=4 + 2 * math.sin(g * 0.13), arm_l="hip",
                    arm_r=dict(hand=(0.3, 1.0), bend=0.6), legs="stand", blink=blink(g, [131, 178]))
    return dict(yaw=-0.3, pitch=-0.25, expr="neutral", head_roll=-5 + 2 * math.sin(g * 0.1 + 1), arm_l="down",
                arm_r=dict(hand=(0.35, 0.95), bend=0.5), legs="stand", blink=blink(g, [150, 203]))


# ----------------------------------------------------------------------------- foreground masses in shade
def _box(name, lo, hi, mat, coll):
    me = bpy.data.meshes.new(name)
    x0, y0, z0 = lo; x1, y1, z1 = hi
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me.from_pydata(v, [], f); me.update()
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:                      # world-scaled box UVs (texture tile = 2 D)
        n = poly.normal
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            if abs(n.z) > 0.5:
                uv.data[li].uv = (co.x / 2.0, co.y / 2.0)
            elif abs(n.x) > 0.5:
                uv.data[li].uv = (co.y / 2.0, co.z / 2.0)
            else:
                uv.data[li].uv = (co.x / 2.0, co.z / 2.0)
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); T.no_bounce(ob)
    return ob


def build_foreground():
    coll = bpy.data.collections.new("S01_FG"); bpy.context.scene.collection.children.link(coll)
    tex = os.path.join(V3, "set3d2", "tex_tower")
    stone = T.mat_lit("S01_stone", image=os.path.join(tex, "stone.png"), gain=0.9, shade_mul=0.42, form=(0.0, -0.05, 0.22))
    brick = T.mat_lit("S01_brick", image=os.path.join(tex, "brick.png"), gain=0.0, shade_mul=0.40, form=(0.0, -0.05, 0.22))
    hide = T.mat_lit("S01_block", color="#6a4a3a")
    obs = {}
    # shot 2: a stone pier at the left edge, 2 D in front of the camera, shadowed by a block behind the camera
    obs["pier2"] = [_box("s2_pier", (-1.15, -18.9, 0.0), (-0.3, -18.1, 7.0), stone, coll),
                    _box("s2_pier_cap", (-1.35, -19.1, 7.0), (-0.1, -17.9, 7.5), stone, coll),
                    _box("s2_block", (-9.0, -40.0, 0.0), (4.0, -21.6, 16.0), hide, coll)]
    # shot 3: a brick pier and low wall at the left edge, painted in shade (key gain 0), no cast shadow
    obs["loggia3"] = [_box("s3_pier", (-12.6, -25.6, 0.0), (-11.6, -24.8, 16.0), brick, coll),
                      _box("s3_wall", (-17.0, -25.5, 0.0), (-12.6, -24.9, 5.2), brick, coll),
                      ]
    for o in obs["loggia3"]:
        o.visible_shadow = False                  # gain 0: the pier stands in the shade of an off-screen roof (no square-wide shadow)
    return obs


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = T.build("DAY")
        T.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 3000
        T.set_rod(1)
        mk = bpy.data.objects.get("market")             # director: the striped stall awning reads as a US flag -> hidden
        if mk is not None:
            mk.hide_render = True
        self.fg = build_foreground()
        self.cam = camrig.make_camera(scene, name="cam_s01")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.nico = actors.Actor("nico", "nico")
        self.nico.build(sprites.DEFAULT_CANVAS["nico"], sd)
        self.padre = actors.Actor("padre", "padre")
        self.padre.build(sprites.DEFAULT_CANVAS["padre"], sd, contact=True)
        self.extras = {}
        for n in EXTRAS_S3:
            a = actors.Actor(n, n); a.build(sprites.DEFAULT_CANVAS[n], sd, contact=True); self.extras[n] = a
        self.all = [self.nico, self.padre] + list(self.extras.values())
        for a in self.all:
            a.head_flip = False                       # key from screen-left in all three views
            T.no_bounce(a.card)
        self.keyed = set()
        self.info = {}
        self.anch = {}
        if verbose:
            print("s01: built in %.1f s" % (time.time() - t0), flush=True)

    def key(self, shot, gs):
        rod = T.STATE["rod_objs"][0]
        for g in gs:
            f = bf(shot, g)
            rod.location = (0.0, 0.0, rod_off(g) if shot == 1 else 0.0)
            rod.keyframe_insert("location", frame=f)
            loc, look = CAMS[shot](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.nico.place(f, tuple(NICO_FEET))
            if shot == 2:
                self.padre.place(f, PADRE_S2)
            elif shot == 3:
                self.padre.place(f, PADRE_S3)
                for n, a in self.extras.items():
                    a.place(f, EXTRAS_S3[n])
            self.keyed.add((shot, g))

    def visible(self, shot):
        self.padre.set_hidden(shot == 1)
        for a in self.extras.values():
            a.set_hidden(shot != 3)
        for o in self.fg["pier2"]:
            o.hide_render = shot != 2
        for o in self.fg["loggia3"]:
            o.hide_render = shot != 3

    def pose(self, shot, gs):
        self.key(shot, gs)
        self.visible(shot)
        cam = self.cam
        n = self.nico
        feet = sprites.feet_of("nico", nico_pose(0)[0])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            p, u = nico_pose(g)
            k = actors.upper_stretch(n, cam, f, p)
            ro = Vector((0, 0, rod_off(g)))
            hl = actors.world_to_local(n, cam, tuple(HAND_L_W), f, feet=feet)
            st = actors.world_to_local(n, cam, tuple(STRIKE_W + ro), f, feet=feet)
            if u >= 0:
                b = math.sin(math.pi * clamp(u))                       # arc: the head travels up and out, not on a chord
                tip = (RAISE_TIP[0] + (st[0] - RAISE_TIP[0]) * u + 0.22 * b, RAISE_TIP[1] + (st[1] - RAISE_TIP[1]) * u - 0.10 * b)
                ang = RAISE_ANG + (STRIKE_ANG - RAISE_ANG) * u
            else:                                                       # anticipation: cock back a bit further
                tip = (RAISE_TIP[0] + 0.25 * u, RAISE_TIP[1] + 0.12 * u)
                ang = RAISE_ANG + 45.0 * u
            hands = {"l": {"hand": hl, "stretch": 1.3, "bend": -0.5},
                     "r": {"tip": tip, "prop": "hammer", "angle": ang, "stretch": 1.3, "bend": -0.7, "layer": "front"}}
            _, inf = n.pose(f, p, hands=hands, camera=cam, upper_k=k)
            self.info[(shot, g)] = dict(nico_l=inf["l"]["error"], nico_r=inf["r"]["error"], u=round(u, 3))
            if shot >= 2:
                self.padre.pose(f, padre_pose(g, shot), camera=cam)
            if shot == 3:
                for nm, a in self.extras.items():
                    a.pose(f, extra_pose(nm, g), camera=cam)
        fr = [bf(shot, g) for g in gs]
        jobs = [(n, {1: 512, 2: 64, 3: 64}[shot])]
        if shot >= 2:
            jobs.append((self.padre, 384 if shot == 2 else 96))
        if shot == 3:
            jobs += [(a, 96) for a in self.extras.values()]
        for a, ppd in jobs:
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s01: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = CAMS[shot](g)
        v = look - loc
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={})
        for a in self.all:
            if a.card.hide_render or f not in a.poses:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        out["rod_tip"] = [round(x, 1) for x in render.world_to_screen(self.cam, T.ROD_TIP, f)[:2]]
        out["strike"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(STRIKE_W), f)[:2]]
        out.update(self.info.get((shot, g), {}))
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(shot)
        self.scene.cycles.samples = samples
        return render.render_frames([bf(shot, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
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
        Tk = Take()
        Tk.pose(shot, gs)
        for g in gs:
            print(json.dumps(Tk.report(shot, g)))
    elif cmd == "stills":
        out = sys.argv[4]
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        Tk = Take()
        Tk.pose(shot, gs)
        for g in gs:
            st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
            dst = os.path.join(out, "s%d_g_%04d.png" % (shot, g))
            os.replace(st["path"], dst)
            print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        # resumable: raw/s<shot>/g_%04d.png + raw/s<shot>/g_%04d.json (json written after the PNG is complete)
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
            Tk = Take(quality="final")
            Tk.pose(shot, todo)
            for g in todo:
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(shot, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
