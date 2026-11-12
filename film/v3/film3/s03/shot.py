#!/usr/bin/env python3
"""shot.py -- film 3 take s03: shots 3-5 (g 122..421, + 8 frames in, 7 out), harbor set WINTER.

    shot 3  g 122..203  street_wide establishing (Boston 1919): the street, the elevated trestle, the tank towering at the end,
                        harbour and freighter; slow eased push + rise (speed change on "เมืองบอสตัน", g 164); a three-car El
                        train crosses on the trestle toward the tank; tiny kids and a worker in the street.
    shot 4  g 204..325  10-frame dissolve (g 199..208). Low angle up the riveted wall between the ladder and the filling pipe:
                        a worker climbs the caged ladder; slow tilt up, the rim against the sky at g 258 (t 8.5); reframe right
                        onto the filling pipe going over the rim at g 279 (t 9.2, "กากน้ำตาล").
    shot 5  g 326..421  10-frame dissolve (g 321..330). Low in Commercial Street: two kids play in the snow (a snowball flies at
                        g 372), a worker with a wrench walks past, the stable at the end on the right, the tank looming over it.
                        Out-handle g 422..428 (10-frame dissolve into shot 6).

Blender frame of (shot s, film frame g) = 1000 * (s - 1) + g + 1.
Look fixes at runtime (harbor.py untouched): a train on the trestle; in shot 4 a climbing worker, rivet rows and the pipe in frame
and a shade-only barrel stack at the frame foot; in shot 5 shade-only crates at the frame edge for deep darks.

    python3 shot.py probe 3|4|5 a:b:step
    python3 shot.py stills 3|4|5 a:b:step <out_dir> [scale] [samples]
    python3 shot.py final 3|4|5 a:b [scale] [samples]          (resumable, raw/s<shot>/)
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast3"), os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(V3, "set3d3"),
          os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast3                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import harbor as H                                      # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing
G_S3, G_S4, G_S5, G_S6 = 122, 204, 326, 422
H_IN, D34, D45, H_OUT = 8, 10, 10, 7
RANGES = {3: (G_S3 - H_IN, G_S4 + D34 // 2 + 1), 4: (G_S4 - D34 // 2 - 2, G_S5 + D45 // 2 + 1), 5: (G_S5 - D45 // 2 - 2, G_S6 + H_OUT - 1)}
# 3: 114..210, 4: 197..332, 5: 319..428
G_BOSTON = g_of(5.38)        # 164
G_AMERICA = g_of(6.11)       # 186
G_TOP = g_of(8.5) - 3        # 255: tilt lands on the rim (word at 258)
G_PIPE = g_of(9.2)           # 279
G_SNOW = 372                 # snowball released


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


def kv(loc, look):
    return tuple(loc) + tuple(look)


def mix_lin(g, ks, share):
    return lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, _ in ks]), share)


R = H.TANK_R
TH_B = H.TH_B
TH_L = TH_B + 0.33               # ladder
TH_P = -0.96                     # pipe


def WP(th, out, z, t=0.0):
    return H.wall_pt(th, R + out, z) + H.TAN(th) * t


# ----------------------------------------------------------------------------- shot 3: the train
TRAIN_X = -2.1                   # east track
RAIL_TOP = H.TR_DECK + 0.42
CAR_L, CAR_W, CAR_H, GAP = 11.0, 2.5, 3.1, 0.7
N_CARS = 3
TRAIN_Y0, TRAIN_SPEED = -30.0, 0.40          # front of the train at g 114, D per frame (12 D/s)


def train_front(g):
    return TRAIN_Y0 + TRAIN_SPEED * (g - 114)


def build_train(coll):
    """three El cars (1919: red-brown wooden bodies, cream window band, dark clerestory roof), origin = front of the train"""
    body = T.mat_lit("S03_car", "#8a2e1e", form=(0.0, -0.05, 0.22))
    band = T.mat_lit("S03_band", "#e6cf9a", form=(0.0, -0.05, 0.22))
    win = T.mat_lit("S03_win", "#2a2a46", gain=0.6, shade_mul=0.7)
    roof = T.mat_lit("S03_roof", "#6a5650", form=(0.0, -0.05, 0.22))
    truck = T.mat_lit("S03_truck", "#242026", gain=0.8)
    root = bpy.data.objects.new("s03_train", None); coll.objects.link(root)
    mb = H.MB()
    x0, x1 = -CAR_W / 2, CAR_W / 2; zb = 0.55
    for c in range(N_CARS):
        y1 = -c * (CAR_L + GAP); y0 = y1 - CAR_L
        mb.box((x0, y0, zb), (x1, y1, zb + CAR_H * 0.42), body)                       # lower body
        mb.box((x0 - 0.02, y0, zb + CAR_H * 0.42), (x1 + 0.02, y1, zb + CAR_H * 0.50), band)
        mb.box((x0, y0, zb + CAR_H * 0.50), (x1, y1, zb + CAR_H * 0.86), body)        # window zone
        k = 0
        y = y0 + 0.7
        while y + 0.75 < y1 - 0.5:                                                    # windows both sides
            for xs, xo in ((x0 - 0.03, x0 + 0.01), (x1 - 0.01, x1 + 0.03)):
                mb.box((xs, y, zb + CAR_H * 0.53), (xo, y + 0.75, zb + CAR_H * 0.80), win)
            y += 1.0; k += 1
        for yy in (y0 + 0.05, y1 - 0.15):                                             # end windows + doors
            mb.box((-0.55, yy - 0.03, zb + CAR_H * 0.50), (0.55, yy + 0.13, zb + CAR_H * 0.80), win)
        mb.box((x0 - 0.12, y0 - 0.1, zb + CAR_H * 0.86), (x1 + 0.12, y1 + 0.1, zb + CAR_H * 0.93), roof)   # roof
        mb.box((-0.75, y0 + 0.3, zb + CAR_H * 0.93), (0.75, y1 - 0.3, zb + CAR_H * 1.03), roof)            # clerestory
        for yt in (y0 + 1.8, y1 - 1.8):                                               # trucks
            mb.box((x0 + 0.25, yt - 1.0, 0.0), (x1 - 0.25, yt + 1.0, zb), truck)
    o = mb.obj("s03_train_cars", coll, hull=0.035); o.parent = root; H.no_bounce(o)
    return root


# ----------------------------------------------------------------------------- shade-only foreground
def _mat_shade(name, color):
    return T.mat_lit(name, color, gain=0.0, shade_mul=0.55, form=(0.0, -0.05, 0.22))


def barrel(mb, c, mat, band, r=0.62, h=1.5):
    c = Vector(c)
    mb.frustum(c, c + Vector((0, 0, h * 0.5)), r * 0.9, r, mat, seg=18, cap0=True, cap1=False)
    mb.frustum(c + Vector((0, 0, h * 0.5)), c + Vector((0, 0, h)), r, r * 0.9, mat, seg=18, cap0=False, cap1=True)
    for z in (0.2, h - 0.2):
        rr = r * 0.9 + (r * 0.1) * (1 - abs(z - h / 2) / (h / 2)) + 0.015
        mb.frustum(c + Vector((0, 0, z - 0.05)), c + Vector((0, 0, z + 0.05)), rr, rr, band, seg=18, cap0=False, cap1=False)


def build_foreground():
    coll = bpy.data.collections.new("S03_FG"); bpy.context.scene.collection.children.link(coll)
    wood = _mat_shade("S03_wood", "#7a4a2a"); band = _mat_shade("S03_band_s", "#3c3034"); crate = _mat_shade("S03_crate", "#8a5a34")
    obs = {}
    mb = H.MB()                                       # shot 4: barrels at the foot of the frame, left, near the camera
    for (fw, lf, z, r, h) in ((3.0, 1.55, 0.0, 0.6, 1.45), (3.7, 2.35, 0.0, 0.6, 1.45), (3.35, 1.95, 1.45, 0.56, 1.3)):
        barrel(mb, C4 * Vector((1, 1, 0)) + _fw * fw + _lf * lf + Vector((0, 0, z)), wood, band, r, h)
    o = mb.obj("s4_barrels", coll, hull=0.02); o.visible_shadow = False; obs[4] = [o]
    mb = H.MB()                                       # shot 5: crates and a barrel at the right edge, near the camera
    for (x, y, z, s) in ((-0.9, -16.4, 0.0, 1.2), (-1.3, -15.2, 0.0, 1.0), (-1.0, -15.9, 1.2, 0.9)):
        mb.box((x - s / 2, y - s / 2, z), (x + s / 2, y + s / 2, z + s), crate, tile=(1, 1))
    barrel(mb, (-0.2, -17.3, 0.0), wood, band, 0.5, 1.3)
    o = mb.obj("s5_crates", coll, hull=0.02); o.visible_shadow = False; obs[5] = [o]
    snow = T.mat_lit("S03_snowball", "#f4f6fc", form=(0.0, -0.05, 0.22))
    mb = H.MB(); mb.sphere((0, 0, 0), 0.13, snow, seg=10, rings=6)
    sb = mb.obj("s5_snowball", coll); H.no_bounce(sb); obs["snowball"] = sb
    return obs


# ----------------------------------------------------------------------------- cameras
CAM3_A = kv((1.4, -60.5, 21.0), (8.4, 12.0, 2.6))
CAM3_M = kv((1.9, -56.5, 22.4), (8.7, 12.0, 3.0))
CAM3_B = kv((2.3, -53.0, 23.6), (8.9, 12.0, 3.4))


def cam3(g):
    a, b = RANGES[3]
    k = mix_lin(g, [(a, CAM3_A, "cubic"), (G_BOSTON, CAM3_M, "cubic"), (b, CAM3_B, "hold")], 0.2)
    return Vector(k[:3]), Vector(k[3:])


TH_C4 = math.radians(-100.0)      # shot 4 camera azimuth: west of the stable, the ladder right of centre, the pipe further right
C4 = WP(TH_C4, 8.0, 1.0)
_fw = (WP(TH_C4, 0, 0) - WP(TH_C4, 8, 0)).normalized(); _lf = Vector((-_fw.y, _fw.x, 0))
PIPE_TOP = Vector((21.27, 12.33, 25.2))
CAM4_A = kv(C4, WP(TH_C4 + 0.01, 0.0, 6.0))
CAM4_B = kv(C4 + Vector((0, 0, 0.15)), WP(TH_C4 + 0.015, 0.0, 8.6))
CAM4_TOP = kv(C4 + Vector((0, 0, 0.3)) + _lf * -0.2, WP(TH_C4 + 0.02, 0.0, 12.4))
CAM4_PIPE = kv(Vector((13.6, 3.2, 1.45)), Vector((23.4, 9.9, 15.6)))
CAM4_END = kv(Vector((13.95, 3.45, 1.55)), Vector((23.7, 9.8, 16.2)))


def cam4(g):
    a, b = RANGES[4]
    ks = [(a, CAM4_A, "sine"), (230, CAM4_B, "sine"), (G_TOP, CAM4_TOP, "cubic"), (G_PIPE + 2, CAM4_PIPE, "sine"), (b, CAM4_END, "hold")]
    k = mix_lin(g, ks, 0.2)
    return Vector(k[:3]), Vector(k[3:])


CAM5_A = kv((1.6, -19.2, 1.0), (9.0, 4.0, 4.4))
CAM5_M = kv((1.75, -18.7, 1.08), (9.6, 4.0, 4.8))
CAM5_B = kv((2.0, -18.2, 1.15), (10.3, 4.0, 5.1))


def cam5(g):
    a, b = RANGES[5]
    k = mix_lin(g, [(a, CAM5_A, "sine"), (366, CAM5_M, "sine"), (b, CAM5_B, "hold")], 0.25)
    return Vector(k[:3]), Vector(k[3:])


CAMS = {3: cam3, 4: cam4, 5: cam5}


def head_flip_for(loc, look):
    f = (Vector(look) - Vector(loc)); f.z = 0; f.normalize()
    r = Vector((f.y, -f.x, 0.0))
    return Vector(H.STATE["A"]["key_dir"]).dot(r) < 0.0


# ----------------------------------------------------------------------------- staging and poses
# shot 3: tiny figures in the street (wide, exempt)
S3_FIG = {"kid1": (-1.4, -11.0, 0.0), "kid2": (0.9, -12.6, 0.0), "worker2": (5.9, -16.0, 0.15)}
# shot 4: a worker in the ladder cage
LADDER_BASE = WP(TH_L, 0.42, 0.0)
LT = H.TAN(TH_L)


def climber_feet(g):
    return WP(TH_L, 0.62, 0.0) + Vector((0, 0, 4.4 + 0.018 * (g - 197)))


# shot 5
S5_KID1 = Vector((3.3, -14.6, 0.0))
S5_KID2 = Vector((5.9, -11.2, 0.15))
S5_WALK0, S5_WALK1 = Vector((-2.6, -7.6, 0.0)), Vector((4.4, -7.0, 0.0))     # worker1 crosses the street left -> right


def walker_pos(g):
    a, b = RANGES[5]
    return S5_WALK0.lerp(S5_WALK1, (g - a) / float(b - a))


def walk_legs(g, period=14.0, amp=0.85):
    ph = 2 * math.pi * g / period
    s = math.sin(ph)
    return dict(preset="stand", stride=amp * s, lift_r=max(0.0, -math.cos(ph)) * 0.45, lift_l=max(0.0, math.cos(ph)) * 0.45), ph


def kid1_pose(g, shot):
    c, p0 = cast3.STORY3["kids_play"]
    p = dict(p0)
    if shot == 5:
        # wind-up (arm back) then the throw at G_SNOW, then a hop of joy
        wind = ease(clamp((g - 345) / 20.0), "sine") * (1 - ease(clamp((g - G_SNOW + 2) / 4.0), "cubic_in"))
        thr = ease(clamp((g - G_SNOW + 2) / 5.0), "cubic_out")
        hx = lerp(0.40, 0.62, wind); hy = lerp(-0.42, -0.62, wind)
        hx = lerp(hx, -0.35, thr); hy = lerp(hy, 0.15, thr)
        p["arm_r"] = dict(hand=(hx, hy), bend=-0.8, shape="open", stretch=1.2)
        p["lean"] = -4 + 6 * wind - 10 * thr
        p["yaw"] = 0.45
        p["head_roll"] = -8 + 3 * math.sin(g * 0.3)
        p["blink"] = blink(g, [333, 390, 415])
        p["squash"] = (1 + 0.02 * math.sin(g * 0.5), 1 - 0.02 * math.sin(g * 0.5))
    else:
        p["squash"] = (1, 1 + 0.03 * math.sin(g * 0.6))
    return p


def kid2_pose(g, shot):
    c, p0 = cast3.STORY3["kids_play_girl"]
    p = dict(p0)
    p["yaw"] = -0.4
    hop = max(0.0, math.sin(g * 0.42)) if shot == 5 else max(0.0, math.sin(g * 0.5))
    p["squash"] = (1 + 0.04 * hop, 1 - 0.04 * hop)
    p["head_roll"] = 8 + 4 * math.sin(g * 0.21)
    if shot == 5 and g >= G_SNOW + 8:                 # ducks the snowball
        u = ease(clamp((g - G_SNOW - 8) / 6.0), "cubic_out") * (1 - ease(clamp((g - G_SNOW - 26) / 10.0), "sine"))
        p["expr"] = "excited"; p["lean"] = 10 * u
        p["arm_r"] = dict(hand=(0.30, -0.25), bend=-0.6, shape="open")
    p["blink"] = blink(g, [340, 402])
    return p


def worker2_pose(g):
    c, p0 = cast3.STORY3["worker_wrench"]
    p = dict(p0); p["head_roll"] = -4 + 2 * math.sin(g * 0.13)
    return p


def worker1_walk(g):
    p = dict(yaw=0.55, pitch=-0.1, expr="neutral", head_roll=-3, arm_l=dict(hand=(-0.25, 1.0), bend=0.5),
             arm_r=dict(hand=(0.25, 0.98), bend=0.5), blink=blink(g, [350, 398]))
    legs, ph = walk_legs(g)
    p["legs"] = legs
    p["arm_l"] = dict(hand=(-0.25 - 0.18 * math.sin(ph), 1.0), bend=0.5)
    p["arm_r"] = dict(hand=(0.25 + 0.18 * math.sin(ph), 0.98), bend=0.5)
    b = abs(math.cos(ph))
    p["squash"] = (1 - 0.015 * b, 1 + 0.015 * b)
    return p


def climber_pose(g):
    ph = 2 * math.pi * (g - 197) / 36.0
    s = math.sin(ph)
    p = dict(yaw=0.0, pitch=-0.5, expr="determined", head_roll=2 * s,
             arm_l=dict(hand=(-0.42, -0.55 - 0.25 * max(0, s)), bend=-0.6, stretch=1.15),
             arm_r=dict(hand=(0.42, -0.55 - 0.25 * max(0, -s)), bend=-0.6, stretch=1.15),
             legs=dict(preset="stand", lift_r=0.6 * max(0, -s), lift_l=0.6 * max(0, s), knee_r=0.6, knee_l=-0.6))
    p["blink"] = blink(g, [220, 268, 310])
    return p


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = H.build("WINTER")
        H.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 6000
        H.set_paint(0.0); H.set_seep(0.6)
        H.STATE["drop"].hide_render = True
        coll = bpy.data.collections.new("S03_FX"); scene.collection.children.link(coll)
        self.train = build_train(coll)
        self.fg = build_foreground()
        self.cam = camrig.make_camera(scene, name="cam_s03")
        self.cam.data.clip_start = 0.05
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.act = {}
        spec = {"kid1": [kid1_pose(g, 5) for g in range(319, 429, 3)] + [kid1_pose(0, 3)],
                "kid2": [kid2_pose(g, 5) for g in range(319, 429, 3)],
                "worker1": [worker1_walk(g) for g in range(0, 14)] + [climber_pose(g) for g in range(197, 233, 2)],
                "worker2": [worker2_pose(0)]}
        for n, ps in spec.items():
            a = actors.Actor(n, n)
            a.build(sprites.canvas_for(n, ps, margin=0.12), sd, contact=True)
            T.no_bounce(a.card)
            self.act[n] = a
        # the climber is a second worker1 card (different place and sprites)
        a = actors.Actor("climber", "worker1")
        a.build(sprites.canvas_for("worker1", spec["worker1"], margin=0.12), sd, contact=False)
        T.no_bounce(a.card)
        self.act["climber"] = a
        self.info = {}
        self.anch = {}
        if verbose:
            print("s03: built in %.1f s" % (time.time() - t0), flush=True)

    def who(self, shot):
        return {3: ["kid1", "kid2", "worker2"], 4: ["climber"], 5: ["kid1", "kid2", "worker1"]}[shot]

    def key(self, shot, gs):
        sb = self.fg["snowball"]
        for g in gs:
            f = bf(shot, g)
            loc, look = CAMS[shot](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.train.location = (TRAIN_X, train_front(g), RAIL_TOP)
            self.train.keyframe_insert("location", frame=f)
            if shot == 3:
                for n, p in S3_FIG.items():
                    self.act[n].place(f, p)
            elif shot == 4:
                self.act["climber"].place(f, tuple(climber_feet(g)))
            else:
                self.act["kid1"].place(f, tuple(S5_KID1))
                self.act["kid2"].place(f, tuple(S5_KID2))
                self.act["worker1"].place(f, tuple(walker_pos(g)))
            # snowball: from kid1's raised hand to just past kid2's head
            vis = shot == 5 and G_SNOW <= g < G_SNOW + 14
            u = (g - G_SNOW) / 13.0
            p0 = S5_KID1 + Vector((0.35, 0.0, 2.05)); p1 = S5_KID2 + Vector((0.4, 0.4, 2.4))
            pos = p0.lerp(p1, clamp(u)) + Vector((0, 0, 0.9 * math.sin(math.pi * clamp(u))))
            sb.location = tuple(pos) if vis else (0, 0, -50)
            sb.keyframe_insert("location", frame=f)
        for ob in (self.train, sb):
            for fc in camrig.fcurves_of(ob):
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"

    def visible(self, shot):
        on = self.who(shot)
        for n, a in self.act.items():
            a.set_hidden(n not in on)
        self.train.hide_render = False
        for c in self.train.children:
            c.hide_render = shot != 3
        for nm in ("stable", "snow_patches"):           # shot 4 looks past the stable: hidden from the camera (with the snow
            st = bpy.data.objects.get(nm)               # on its roof), its shadow on the tank stays
            if st is not None:
                st.visible_camera = shot != 4
        for s in (4, 5):
            for o in self.fg[s]:
                o.hide_render = shot != s

    def pose(self, shot, gs):
        self.key(shot, gs)
        self.visible(shot)
        cam = self.cam
        loc, look = CAMS[shot](RANGES[shot][0])
        self.hf = hf = head_flip_for(loc, look)
        for a in self.act.values():
            a.head_flip = hf
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 3:
                self.act["kid1"].pose(f, kid1_pose(g, 3), camera=cam)
                self.act["kid2"].pose(f, kid2_pose(g, 3), camera=cam)
                self.act["worker2"].pose(f, worker2_pose(g), camera=cam)
            elif shot == 4:
                self.act["climber"].pose(f, climber_pose(g), camera=cam)
            else:
                self.act["kid1"].pose(f, kid1_pose(g, 5), camera=cam)
                self.act["kid2"].pose(f, kid2_pose(g, 5), camera=cam)
                self.act["worker1"].pose(f, worker1_walk(g), camera=cam)
        fr = [bf(shot, g) for g in gs]
        ppd = {3: {"kid1": 48, "kid2": 48, "worker2": 48}, 4: {"climber": 96}, 5: {"kid1": 320, "kid2": 192, "worker1": 192}}[shot]
        for n, d in ppd.items():
            a = self.act[n]
            for f, r in zip(fr, a.render_sprites(d, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s03: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = CAMS[shot](g)
        v = look - loc
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), head_flip=self.hf, heads={})
        for n in self.who(shot):
            a = self.act[n]
            if f not in a.poses:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][n] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        if shot == 3:
            out["train_front"] = [round(x, 1) for x in render.world_to_screen(self.cam, (TRAIN_X, train_front(g), RAIL_TOP + 2), f)[:2]]
        if shot == 4:
            out["rim"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(WP(TH_C4, 0, 24.0)), f)[:2]]
            out["pipe_top"] = [round(x, 1) for x in render.world_to_screen(self.cam, (21.27, 12.33, 25.2), f)[:2]]
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
            print("shot %d g %d  %.1f s wall %.1f cpu  %s" % (shot, g, st["wall"], st["cpu"], json.dumps(Tk.report(shot, g))), flush=True)
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
