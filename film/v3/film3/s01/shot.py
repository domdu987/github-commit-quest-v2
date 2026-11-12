#!/usr/bin/env python3
"""shot.py -- film 3 take s01: shots 1-2 (the hook, g 0..121 + 8 handle frames), harbor set WINTER.

    shot 1  g   0.. 51  close and low at the foot of the tank: tommy crouches and slides the tin bucket under the dripping
                        bucket seam (g 0..20, his hand pinned to the rim); a glossy elongated drop swells at the end of the seep
                        strip, lets go (g 17) and lands in the bucket on g 30 (t 0.9); snap pull-up g 33..51: the camera backs
                        away and tilts up, the riveted wall towers over the tiny boy
    shot 2  g  52..121  hard cut, base_eye: the foreman (near, right) jabs his paintbrush up at the tank, then shoves the brush
                        and the paint pot at tommy (far, by the bucket); snap punch-in on the brush g 83..89 (lands on
                        "สีมาทาทับแทน", g 87). Mouth closed. Out-handle g 122..129 (12-frame dissolve into s03).

Blender frame of (shot s, film frame g) = 1000 * (s - 1) + g + 1.
Look fixes at runtime (harbor.py untouched): the set's dot drop is hidden and replaced by an animated glossy elongated drop with a
painted highlight; shade-only foreground masses (barrels / crate, key gain 0) at the frame edges for deep darks.

    python3 shot.py probe 1|2 a:b:step
    python3 shot.py stills 1|2 a:b:step <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b [scale] [samples]          (resumable, raw/s<shot>/)
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast3"), os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(V3, "set3d3"),
          os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast3                                            # noqa: E402  (first: registers tommy, foreman, workers, kids)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import harbor as H                                      # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):                     # narration time -> film frame of an event
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing
G_S2, G_S3, H_OUT = 52, 122, 8                  # boundaries round(t*30): 1.75, 4.05 s; 12-frame dissolve out -> 6 + 2 handle
RANGES = {1: (0, G_S2 - 1), 2: (G_S2, G_S3 + H_OUT - 1)}
SLIDE = (0, 19)                                  # bucket slides in under the seam
RELEASE = 22                                     # his hand lets go of the rim
DROP_LAND = g_of(0.9)                            # 30: lands in the bucket
DROP2_GO, DROP2_LAND = 47, 60                    # the next drop (falls in the pull-up, lands after the cut)
PULL = (33, 51)                                  # snap pull-up
JAB = (60, 78)                                   # foreman jabs the brush up at the tank (two jabs)
SHOVE = (78, 86)                                 # shoves brush and pot at tommy
PUNCH = (83, 89)                                 # snap punch-in on the brush, lands on g 87 ("สีมาทาทับแทน" t 2.78)
G_PAINT = g_of(2.78)                             # 86


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


# ----------------------------------------------------------------------------- the wall frame (bucket seam)
R = H.TANK_R
TH = H.TH_B


def W(t, out, z):
    """world point t D along the wall (+ = screen-right seen from outside), `out` D out from the wall surface, height z."""
    return H.wall_pt(TH + t / R, R + out, z)


BUCKET_END = Vector(H.BUCKET_MARK)              # bucket base centre under the seam (0.47 D out)
BUCKET_START = W(-0.62, 0.62, 0.0)               # where he sets it down first, nearer him
TOMMY_S1 = W(-1.30, 0.80, 0.0)
TOMMY_S2 = W(0.30, 1.45, 0.0)                    # beside the bucket, in line with the shove
FOREMAN_S2 = Vector(H.BOSS_MARK) + (W(0, 1, 0) - W(0, 0, 0)) * 0.9 + (W(1, 0, 0) - W(0, 0, 0)) * -0.35


def bucket_pos(g):
    u = ease(clamp((g - SLIDE[0]) / float(SLIDE[1] - SLIDE[0])), "cubic_out") if g < SLIDE[1] else 1.0
    return BUCKET_START.lerp(BUCKET_END, u)


def fill_z(fill):
    return 0.035 + (H.BUCKET_H - 0.05) * fill


FILL0, FILL1 = 0.02, 0.05


def bucket_fill(g):
    return FILL0 if g < DROP_LAND else (FILL1 if g < DROP2_LAND else FILL1 + 0.02)


# ----------------------------------------------------------------------------- the drop (replaces the set's dark dot)
# The bucket-seam seep strip runs from the seam (z 2.88) down to z 0.78, just above the bucket rim. A glossy bead runs down the
# strip (accelerating), hangs and swells at the tip, lets go and falls into the bucket.
STRIP_TOP_Z = H.HT.COURSE - 0.12
STRIP_TIP_Z = STRIP_TOP_Z - (STRIP_TOP_Z - 0.78)


def drop_state(g, born, tip, go, land):
    """(visible, z_centre, out, sx, sz) of one drop."""
    if g < born or g >= land:
        return False, 0.0, 0.0, 0.0, 0.0
    if g < tip:                                   # sliding down the strip
        u = ease(clamp((g - born) / float(tip - born)), "quad_in")
        r = 0.062; sz = 1.5 + 0.9 * u
        z = lerp(STRIP_TOP_Z - 0.35, STRIP_TIP_Z + r * 1.4, u)
        return True, z, 0.07, r, r * sz
    if g < go:                                    # hanging at the tip, swelling
        u = ease(clamp((g - tip) / float(go - tip)), "quad_in")
        r = 0.064 + 0.020 * u; sz = 1.5 + 0.7 * u
        return True, STRIP_TIP_Z - r * sz * 0.7, 0.07 + 0.03 * u, r, r * sz
    u = (g - go) / float(land - go)               # free fall into the bucket
    z0 = STRIP_TIP_Z - 0.084 * 2.2 * 0.7
    z1 = fill_z(FILL0) + 0.04
    return True, z0 - (z0 - z1) * u * u, 0.10 + 0.06 * u, 0.07, 0.07 * (2.2 + 0.6 * u)


DROPS = [(0, 15, 22, DROP_LAND), (31, 44, 52, DROP2_LAND)]
DROP_GO = 22


def build_drop_objects(coll):
    M = H.STATE["M"]
    gl = H._add_gloss(H.mat_lit("S01_drop", "#9a4510", gain=0.9, form=(0.0, -0.05, 0.22)), 0.6, 0.12, (1.0, 0.9, 0.75))
    hi = T.mat_emit("S01_drop_hi", color="#fff1d6", strength=1.6) if "color" in T.mat_emit.__code__.co_varnames else None
    obs = []
    for i in range(2):
        mb = H.MB(); mb.sphere((0, 0, 0), 1.0, gl, seg=14, rings=9)
        d = mb.obj("s01_drop%d" % i, coll); H.no_bounce(d); d.visible_shadow = False
        # painted highlight: a tiny bright ellipse on the upper-left of the drop, facing the camera side
        if hi is not None:
            mb = H.MB(); mb.sphere((0, 0, 0), 1.0, hi, seg=8, rings=5)
            h = mb.obj("s01_drop%d_hi" % i, coll); h.parent = d
            o = H.OUT(TH); h.location = (o.x * 0.78 - o.y * 0.18, o.y * 0.78 + o.x * 0.18, 0.32); h.scale = (0.34, 0.30, 0.26)
            H.no_bounce(h); h.visible_shadow = False
        obs.append(d)
    # splash: a small crown ring at the fill surface
    mb = H.MB(); mb.frustum((0, 0, 0), (0, 0, 1.0), 1.0, 1.35, gl, seg=16, cap0=False, cap1=False)
    sp = mb.obj("s01_splash", coll); H.no_bounce(sp); sp.visible_shadow = False
    return obs, sp


# ----------------------------------------------------------------------------- shade-only foreground masses
def _mat_shade(name, color=None, image=None):
    return T.mat_lit(name, color, image=image, gain=0.0, shade_mul=0.55, form=(0.0, -0.05, 0.22)) if image is None else \
        T.mat_lit(name, image=image, gain=0.0, shade_mul=0.55, form=(0.0, -0.05, 0.22))


def barrel(mb, c, mat, band, r=0.62, h=1.5):
    c = Vector(c)
    mb.frustum(c, c + Vector((0, 0, h * 0.5)), r * 0.9, r, mat, seg=18, cap0=True, cap1=False)
    mb.frustum(c + Vector((0, 0, h * 0.5)), c + Vector((0, 0, h)), r, r * 0.9, mat, seg=18, cap0=False, cap1=True)
    for z in (0.2, h - 0.2):
        rr = r * 0.9 + (r * 0.1) * (1 - abs(z - h / 2) / (h / 2)) + 0.015
        mb.frustum(c + Vector((0, 0, z - 0.05)), c + Vector((0, 0, z + 0.05)), rr, rr, band, seg=18, cap0=False, cap1=False)


def build_foreground():
    coll = bpy.data.collections.new("S01_FG"); bpy.context.scene.collection.children.link(coll)
    wood = _mat_shade("S01_wood", "#7a4a2a"); band = _mat_shade("S01_band", "#3c3034"); crate = _mat_shade("S01_crate", "#8a5a34")
    obs = {}
    # shot 1 end of the pull-up: two barrels at the screen-left edge, near the camera's end position
    mb = H.MB()
    barrel(mb, W(-3.55, 12.2, 0.0), wood, band, 0.62, 1.5)
    barrel(mb, W(-4.6, 11.4, 0.0), wood, band, 0.62, 1.5)
    o = mb.obj("s1_barrels", coll, hull=0.02); o.visible_shadow = False; obs["s1"] = [o]
    # shot 2: a crate stack and a barrel at the screen-left edge, 2..3 D in front of the camera
    mb = H.MB()
    p = W(-2.6, 7.0, 0.0)
    mb.box(tuple(p + Vector((-0.7, -0.7, 0))), tuple(p + Vector((0.7, 0.7, 1.4))), crate, tile=(1, 1))
    mb.box(tuple(p + Vector((-0.55, -0.6, 1.4))), tuple(p + Vector((0.6, 0.55, 2.5))), crate, tile=(1, 1))
    barrel(mb, W(-1.6, 6.5, 0.0) + Vector((0, 0, 0)), wood, band, 0.6, 1.45)
    o = mb.obj("s2_crates", coll, hull=0.02); o.visible_shadow = False; obs["s2"] = [o]
    return obs


# ----------------------------------------------------------------------------- cameras
def sph(look, dist, yaw, pitch):
    yr, pr = math.radians(yaw), math.radians(pitch)
    d = Vector((math.sin(yr) * math.cos(pr), math.cos(yr) * math.cos(pr), math.sin(pr)))
    return look - d * dist


def kv(loc, look):
    return tuple(loc) + tuple(look)


def cam1(g):
    a = kv(W(-0.78, 4.05, 1.30), W(-0.72, 0.35, 1.02))
    b = kv(W(-0.62, 3.85, 1.24), W(-0.60, 0.35, 1.00))            # drifts with the bucket, leans in
    c = kv(W(-0.66, 3.95, 1.18), W(-0.62, 0.35, 1.06))            # the drop lands, eye follows it down then up
    d = kv(W(-1.10, 14.2, 0.24), W(-0.95, 0.0, 5.05))             # pulled up: the wall towers over him
    e = kv(W(-1.16, 14.6, 0.22), W(-0.98, 0.0, 5.25))
    ks = [(0, a, "sine"), (18, b, "sine"), (PULL[0], c, "quint"), (PULL[1], d, "cubic_out"), (G_S2 + 6, e, "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, _ in ks]), 0.14)
    return Vector(k[:3]), Vector(k[3:])


def cam2(g):
    head = FOREMAN_S2 + Vector((0, 0, 2.85))
    a = kv(W(0.75, 9.7, 2.55), W(1.55, 0.6, 2.70))
    b = kv(W(0.85, 9.3, 2.62), W(1.62, 0.6, 2.80))
    # punch-in: close on the foreman's shoving hand and the brush, his face at the top of the frame
    look = head + (W(-1, 0, 0) - W(0, 0, 0)) * 0.70 + Vector((0, 0, -0.70))
    pc = look + (W(0.85, 9.6, 2.4) - look).normalized() * 2.75
    c = kv(pc, look)
    sd = W(1, 0, 0) - W(0, 0, 0)
    d = kv(pc + sd * 0.42 + (W(0, 1, 0) - W(0, 0, 0)) * -0.05 + Vector((0, 0, 0.08)), look + sd * 0.22 + Vector((0, 0, 0.06)))
    ks = [(G_S2, a, "cubic_out"), (PUNCH[0], b, "quint"), (PUNCH[1], c, "sine"), (G_S3 + H_OUT, d, "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, _ in ks]), 0.3)
    return Vector(k[:3]), Vector(k[3:])


CAMS = {1: cam1, 2: cam2}


def head_flip_for(loc, look):
    """True when the key comes from screen-right for this camera (as film-2 s01: False = key from screen-left)."""
    f = (Vector(look) - Vector(loc)); f.z = 0; f.normalize()
    r = Vector((f.y, -f.x, 0.0))
    kd = Vector(H.STATE["A"]["key_dir"])
    return kd.dot(r) < 0.0


# ----------------------------------------------------------------------------- poses
TB_CAST, TB_POSE = cast3.STORY3["tommy_bucket_place"]


def tommy_pose1(g):
    p = dict(TB_POSE)
    p.pop("prop_r", None)                         # the bucket is the set's own 3D bucket; his hand grips its rim
    p["arm_l"] = dict(p["arm_l"])
    # head: watches the swelling drop, follows its fall, then looks up the wall during the pull-up
    look_up = keys(g, [(0, 0.45, "sine"), (15, 0.15, "sine"), (DROP_GO, 0.05, "cubic_in"), (DROP_LAND, -0.3, "sine"),
                       (DROP_LAND + 6, -0.1, "sine"), (PULL[0] + 2, 0.8, "hold")])
    p["pitch"] = 0.6 - 1.1 * look_up
    p["gaze"] = (0.6, -0.9 * look_up)
    p["head_roll"] = 6 - 6 * look_up
    p["lean"] = 16 - 8 * clamp((g - RELEASE) / 10.0)
    p["blink"] = blink(g, [8, DROP_LAND + 2, 45])
    if g >= RELEASE:
        u = ease(clamp((g - RELEASE) / 7.0), "sine")
        p["arm_r"] = dict(hand=(0.62 - 0.35 * u, 0.93 - 0.05 * u), bend=-0.3 + 0.9 * u, stretch=1.3 - 0.3 * u)
    p["fx"] = ["sweat"] if g >= DROP_LAND + 4 else []
    return p


def tommy_pose2(g):
    c, p0 = cast3.STORY3["tommy_worried"]
    p = dict(p0)
    p["yaw"] = 0.35
    p["head_roll"] = 6 + 2 * math.sin(g * 0.21)
    p["pitch"] = 0.1
    p["gaze"] = (0.8, 0.0)
    p["blink"] = blink(g, [70, 104])
    return p


FM_CAST = "foreman"
BRUSH_UP = dict(hand=(-0.55, -0.85), bend=-0.8, stretch=1.25)
BRUSH_FWD = dict(hand=(-1.0, 0.66), bend=-0.2, stretch=1.3)


def foreman_pose(g):
    p = dict(yaw=-0.38, pitch=-0.35, expr="angry", mouth="clench", head_roll=-6, lean=3, legs="wide")
    # screen-left arm: the brush. Two jabs up at the tank, then a shove toward tommy (screen-left, far)
    if g < SHOVE[0]:
        j = 0.0
        for s in (JAB[0] + 4, JAB[0] + 12):
            j += pulse(g, s - 3, s, s + 5, 1.0)
        hx, hy = BRUSH_UP["hand"]
        arm_l = dict(BRUSH_UP); arm_l["hand"] = (hx - 0.06 * j, hy - 0.10 * j + 0.04 * math.sin(g * 0.5))
        ang = -125.0 - 8 * j
    else:
        u = ease(clamp((g - SHOVE[0]) / float(SHOVE[1] - SHOVE[0])), "back_out")
        hx = lerp(BRUSH_UP["hand"][0], BRUSH_FWD["hand"][0], u); hy = lerp(BRUSH_UP["hand"][1], BRUSH_FWD["hand"][1], u)
        arm_l = dict(hand=(hx + 0.02 * math.sin(g * 0.6) * (g > SHOVE[1]), hy), bend=lerp(-0.8, -0.6, u), stretch=lerp(1.25, 1.3, u))
        ang = lerp(-125.0, -178.0, u)
    p["arm_l"] = arm_l
    p["prop_l"] = dict(type="paintbrush", angle=ang)
    # screen-right arm: the paint pot, hanging at his side, then swung forward with the shove
    u2 = ease(clamp((g - SHOVE[0] - 1) / 8.0), "cubic_out") if g >= SHOVE[0] else 0.0
    p["arm_r"] = dict(hand=(lerp(0.62, 0.05, u2), lerp(1.05, 0.62, u2)), bend=lerp(0.4, -0.2, u2), stretch=1.1)
    p["prop_r"] = dict(type="paintpot")
    p["lean"] = lerp(3, -7, u2) + 1.2 * math.sin(g * 0.37)
    p["head_roll"] = -6 + 2.0 * math.sin(g * 0.9) * (g < SHOVE[0]) + lerp(0, -4, u2)
    p["blink"] = blink(g, [57, 99, 118])
    p["squash"] = (1.0 + 0.012 * math.sin(g * 0.75), 1.0 - 0.012 * math.sin(g * 0.75))
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
        scene.frame_start, scene.frame_end = 1, 3000
        H.set_paint(0.0); H.set_seep(1.0)
        H.STATE["drop"].hide_render = True                  # the set's dark dot: replaced by our animated drop
        coll = bpy.data.collections.new("S01_FX"); scene.collection.children.link(coll)
        self.drops, self.splash = build_drop_objects(coll)
        self.fg = build_foreground()
        self.cam = camrig.make_camera(scene, name="cam_s01")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        poses_t = [tommy_pose1(g) for g in range(0, 52, 3)] + [tommy_pose2(g) for g in range(52, 130, 6)]
        poses_f = [foreman_pose(g) for g in range(52, 130, 2)]
        self.tommy = actors.Actor("tommy", "tommy")
        self.tommy.build(sprites.canvas_for("tommy", poses_t, margin=0.12), sd, contact=True)
        self.foreman = actors.Actor("foreman", "foreman")
        self.foreman.build(sprites.canvas_for("foreman", poses_f, margin=0.12), sd, contact=True)
        self.all = [self.tommy, self.foreman]
        for a in self.all:
            T.no_bounce(a.card)
        self.keyed = set()
        self.info = {}
        self.anch = {}
        if verbose:
            print("s01: built in %.1f s" % (time.time() - t0), flush=True)

    def key(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = CAMS[shot](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            H.set_bucket(pos=tuple(bucket_pos(g)), fill=bucket_fill(g), visible=True, frame=f, interp="LINEAR")
            for i in range(len(DROPS)):
                d = self.drops[i]
                vis, z, out, sx, sz = drop_state(g, *DROPS[i])
                p = W(0.0, out, z if vis else 0.5)
                d.location = tuple(p); d.scale = (max(sx, 1e-3), max(sx, 1e-3), max(sz, 1e-3))
                d.hide_render = not vis
                d.keyframe_insert("location", frame=f); d.keyframe_insert("scale", frame=f); d.keyframe_insert("hide_render", frame=f)
            # splash crown for 5 frames after each landing
            sp = self.splash; vis = False
            for born, tip, go, land in DROPS:
                if land <= g < land + 5:
                    u = (g - land) / 4.0; vis = True
                    sp.location = tuple(W(0.0, 0.16, fill_z(bucket_fill(g))))
                    sp.scale = (0.03 + 0.07 * u, 0.03 + 0.07 * u, 0.06 * math.sin(math.pi * min(1, u + 0.15)))
            sp.hide_render = not vis
            sp.keyframe_insert("location", frame=f); sp.keyframe_insert("scale", frame=f); sp.keyframe_insert("hide_render", frame=f)
            if shot == 1:
                self.tommy.place(f, tuple(TOMMY_S1))
            else:
                self.tommy.place(f, tuple(TOMMY_S2))
                self.foreman.place(f, tuple(FOREMAN_S2))
            self.keyed.add((shot, g))
        for ob in [self.splash] + self.drops:
            if ob.animation_data and ob.animation_data.action:
                for fc in camrig.fcurves_of(ob):
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT" if fc.data_path == "hide_render" else "LINEAR"

    def visible(self, shot):
        self.foreman.set_hidden(shot == 1)
        for o in self.fg["s1"]:
            o.hide_render = shot != 1
        for o in self.fg["s2"]:
            o.hide_render = shot != 2

    def pose(self, shot, gs):
        self.key(shot, gs)
        self.visible(shot)
        cam = self.cam
        tm = self.tommy
        loc, look = CAMS[shot](RANGES[shot][0])
        hf = head_flip_for(loc, look)
        for a in self.all:
            a.head_flip = hf
        self.hf = hf
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 1:
                p = tommy_pose1(g)
                hands = None
                if g < RELEASE:
                    bp = bucket_pos(g)
                    side = (W(-1, 0, 0) - W(0, 0, 0)).normalized()
                    rim = bp + side * (H.BUCKET_R1 - 0.02) + Vector((0, 0, H.BUCKET_H + 0.01))
                    hands = {"r": {"hand": tuple(rim), "stretch": 1.3, "bend": -0.3}}
                _, inf = tm.pose(f, p, hands=hands, camera=cam)
                self.info[(shot, g)] = dict(tommy_r=round(inf["r"]["error"], 3) if hands else None)
            else:
                tm.pose(f, tommy_pose2(g), camera=cam)
                self.foreman.pose(f, foreman_pose(g), camera=cam)
        fr = [bf(shot, g) for g in gs]
        jobs = [(tm, 320 if shot == 1 else 96)]
        if shot == 2:
            jobs.append((self.foreman, 320))
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
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), head_flip=self.hf, heads={})
        for a in self.all:
            if a.card.hide_render or f not in a.poses:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        if shot == 1:
            out["bucket"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(bucket_pos(g) + Vector((0, 0, 0.36))), f)[:2]]
            out["strip_end"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(W(0, 0.05, STRIP_TIP_Z)), f)[:2]]
        out.update({k: v for k, v in self.info.get((shot, g), {}).items() if v is not None})
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
