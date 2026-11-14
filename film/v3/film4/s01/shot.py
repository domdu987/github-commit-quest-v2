#!/usr/bin/env python3
"""shot.py -- film 4 take s01: shots 1-5 (the opening, g 0..255 + 7 handle frames), pagoda set DAY.

    shot 1  g   0.. 38  medium: kenta on the pagoda platform beside the opened ground storey, both fists on the hanging chain,
                        pulling; slow push (ref a t0001: hero beside the jar)
    shot 2  g  39.. 74  hard cut, ECU raking low inside the ground storey: the pillar foot floating one palm over the stone,
                        warm lamp light through the gap; slow push and rise (ref a t0003)
    shot 3  g  75..110  hard cut, over-the-eave: the ground-storey roof corner big in the foreground, the pagoda rising behind;
                        slow crane up (ref a t0005)
    shot 4  g 111..184  hard cut, medium: kenta in front of the opened base points INTO the pagoda (point lands g 129 on
                        "พอแผ่นดินไหว"), townspeople glance; snap punch-in g 148..156 (middle on "ให้วิ่ง" g 152), jab on
                        "เข้ามาในนี้" g 167 (ref a t0007 / t0009).  Kenta's mouth never moves (the narrator speaks).
    shot 5  g 185..255  10-frame dissolve (g 180..189), high wide establishing from a balcony on the street axis: balustrade
                        and banner in the foreground, street, gate, courtyard, pagoda + tower, mountains; slow eased push and
                        tilt down (ref a t0029-t0033).  Handle out g 256..262.

Blender frame of (shot s, film frame g) = 1000 * (s - 1) + g + 1.
Set: v2 pagoda (G.build("DAY"): open base, warm interior, golden pillar foot, yard / street dressing all in the set now).
This take adds only the shot-5 balcony and per-shot depth of field (G.setup_dof, values of pagoda_work/v2/s01_v2.py).
Event times: narration_bankky.wav / captions_bankky.json (point g 129, punch middle g 152, jab g 167).

    python3 shot.py probe <shot> a:b[:step]
    python3 shot.py stills <shot> a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final <shot> a:b[:step] [scale] [samples]
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast4"), os.path.join(V3, "stage"), os.path.join(V3, "set3d4"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast4                                            # noqa: E402  (first: registers kenta, master, merchant, woman2, farmer)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import pagoda as G                                      # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):                     # narration time -> film frame of an event
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing
G_S2, G_S3, G_S4, G_S5, G_END, H_OUT = 39, 75, 111, 185, 256, 7      # round(t*30) of 1.30, 2.50, 3.70, 6.16, 8.53
DISS = 10                                                           # shot 4 -> 5 dissolve, frames G_S5-5 .. G_S5+4
HANDLE = DISS // 2 + 2                                              # 7
RANGES = {1: (0, G_S2 - 1), 2: (G_S2, G_S3 - 1), 3: (G_S3, G_S4 - 1), 4: (G_S4, G_S5 + HANDLE - 1), 5: (G_S5 - HANDLE, G_END + H_OUT - 1)}
# event times from PROJ/film4/script/captions_bankky.json (narration_bankky.wav at +0.10 s)
G_POINT = g_of(4.20) - 4         # 125: the arm flings out; 85 % of the way by "พอแผ่นดินไหว" (g 129)
G_POINT_IN = g_of(4.20)          # 129
PUNCH = (148, 156)               # snap punch-in, its middle lands on "ให้วิ่ง" (g 152)
G_JAB = g_of(5.48)               # 167 "เข้ามาในนี้": the pointing hand jabs toward the door
G_GLANCE = 136                   # townspeople turn their heads to kenta
G_JAPAN = g_of(6.75)             # 205 "ญี่ปุ่น"
G_QUAKEWORD = g_of(7.55)         # 230 "แผ่นดินไหว"


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


# ----------------------------------------------------------------------------- staging (world D)
PZ = G.PLAT_Z
KENTA_S1 = (-0.95, -3.75, PZ)                     # on the platform, in front of the opened ground storey, left bay
KENTA_S4 = (-2.35, -6.35, 0.0)                    # on the gravel at the platform's south-west corner
TOWN_S4 = {"merchant": (1.35, -1.75, PZ), "woman2": (2.35, -2.55, PZ), "farmer": (3.0, -3.9, PZ)}
EXTRAS_S5 = {"merchant": (-1.6, -36.5, 0.0), "woman2": (2.1, -38.5, 0.0), "farmer": (-2.3, -41.0, 0.0),
             "kenta": (0.6, -27.5, 0.0)}


def sph(look, dist, yaw, pitch):
    yr, pr = math.radians(yaw), math.radians(pitch)
    d = Vector((math.sin(yr) * math.cos(pr), math.cos(yr) * math.cos(pr), math.sin(pr)))
    return look - d * dist


def _mix(g, ks, share):
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), share)
    return Vector(k[:3]), Vector(k[3:])


def _pk(a, b):
    return tuple(a) + tuple(b)


# shot 1: from the south-east, a little below kenta's eyes, slow push (+ a creep to the right)
CAM1_A = (Vector((0.95, -6.55, 2.92)), Vector((-1.08, -1.81, 2.98)))
CAM1_B = (Vector((0.70, -6.18, 2.94)), Vector((-1.36, -1.80, 2.99)))


def cam1(g):
    g0, g1 = RANGES[1]
    return _mix(g, [(g0, _pk(*CAM1_A), "cubic_out"), (g1 + 1, _pk(*CAM1_B), "hold")], 0.35)


# shot 2: inside the ground storey, raking low across the gap
CAM2_A = (Vector((0.66, -1.70, 1.40)), Vector((-0.14, 0.05, 1.47)))
CAM2_B = (Vector((0.55, -1.44, 1.42)), Vector((-0.14, 0.05, 1.52)))


def cam2(g):
    g0, g1 = RANGES[2]
    return _mix(g, [(g0, _pk(*CAM2_A), "cubic_out"), (g1 + 1, _pk(*CAM2_B), "hold")], 0.5)


# shot 3: just outside the ground-storey roof's south-west corner, looking up the pagoda; crane up
CAM3_A = (Vector((-6.55, -6.85, 3.85)), Vector((-2.2, 1.4, 13.0)))
CAM3_B = (Vector((-6.35, -6.75, 4.45)), Vector((-2.0, 1.4, 13.8)))


def cam3(g):
    g0, g1 = RANGES[3]
    return _mix(g, [(g0, _pk(*CAM3_A), "cubic_out"), (g1 + 1, _pk(*CAM3_B), "hold")], 0.4)


# shot 4: eye level from the courtyard, kenta left, the opened base right; punch-in on kenta + the doorway
CAM4_A = (Vector((-3.25, -10.35, 2.30)), Vector((-0.1, -2.2, 2.25)))
CAM4_B = (Vector((-3.14, -10.05, 2.30)), Vector((-0.15, -2.2, 2.26)))
CAM4_C = (Vector((-2.88, -9.05, 2.24)), Vector((-0.6, -3.0, 1.98)))
CAM4_D = (Vector((-2.83, -8.88, 2.24)), Vector((-0.6, -3.0, 2.0)))


def cam4(g):
    g0, g1 = RANGES[4]
    ks = [(g0, _pk(*CAM4_A), "sine"), (PUNCH[0], _pk(*CAM4_B), "quint"), (PUNCH[1], _pk(*CAM4_C), "sine"), (g1 + 1, _pk(*CAM4_D), "hold")]
    return _mix(g, ks, 0.15)


# shot 5: high on a balcony above the street, on the axis toward the gate and the pagoda
CAM5_A = (Vector((1.0, -56.0, 13.6)), Vector((4.6, -4.0, 3.4)))
CAM5_B = (Vector((1.0, -55.4, 13.45)), Vector((4.5, -4.0, 1.8)))


def cam5(g):
    g0, g1 = RANGES[5]
    return _mix(g, [(g0, _pk(*CAM5_A), "sine"), (g1 + 1, _pk(*CAM5_B), "hold")], 0.25)


CAMS = {1: cam1, 2: cam2, 3: cam3, 4: cam4, 5: cam5}


# ----------------------------------------------------------------------------- poses
def kenta_s1(g):
    p = dict(cast4.STORY4["kenta_hang_chain"][1])
    pull = 0.5 - 0.5 * math.cos(2 * math.pi * (g + 4) / 26.0)          # two slow pulls on the chain
    p["lean"] = -8 - 4 * pull
    p["squash"] = (1.0 + 0.015 * pull, 1.0 - 0.02 * pull)
    p["head_roll"] = -6 - 3 * pull
    arm_r = dict(p["arm_r"]); arm_l = dict(p["arm_l"])
    arm_r["hand"] = (0.64, -0.12 + 0.10 * pull); arm_l["hand"] = (0.64, 0.20 + 0.10 * pull)
    p["arm_r"], p["arm_l"] = arm_r, arm_l
    p["blink"] = blink(g, [20])
    return p


def kenta_s4(g):
    p = dict(cast4.STORY4["kenta_point_pagoda"][1])
    p["expr"] = "determined"                     # mouth closed: the narrator speaks
    p["mouth"] = "frown"
    u = ease((g - G_POINT) / 8.0, "back_out") if g >= G_POINT else 0.0
    jab = pulse(g, G_JAB - 3, G_JAB, G_JAB + 7, 1.0)
    rest = (0.42, 0.95)
    point = (0.84 + 0.08 * jab, 0.12)
    hand = (lerp(rest[0], point[0], u), lerp(rest[1], point[1], u))
    p["arm_r"] = dict(hand=hand, shape="point" if u > 0.3 else "fist", bend=lerp(0.6, -0.5, clamp(u)), stretch=1.3)
    p["arm_l"] = "akimbo"
    p["legs"] = "wide"
    look_cam = g >= G_POINT + 10                 # turns from the door to the audience while he points
    turn = ease((g - (G_POINT + 10)) / 6.0, "sine") if look_cam else 0.0
    p["yaw"] = lerp(0.55, 0.15, turn)
    p["gaze"] = (lerp(0.8, 0.05, turn), lerp(-0.2, 0.0, turn))
    p["pitch"] = lerp(-0.2, 0.05, turn)
    p["head_roll"] = -4 + 3 * jab - 2 * math.sin(g * 0.13)
    p["lean"] = 3 + 4 * jab
    p["blink"] = blink(g, [118, 171])
    return p


TOWN_BASE = {"merchant": dict(yaw=0.35, pitch=-0.2, expr="smirk", arm_l="down", arm_r=dict(hand=(0.30, 0.95), bend=0.6), legs="stand"),
             "woman2": dict(yaw=0.45, pitch=-0.25, expr="neutral", arm_l=dict(hand=(-0.12, 0.85), bend=0.7), arm_r=dict(hand=(0.10, 0.88), bend=-0.7), legs="narrow"),
             "farmer": dict(yaw=0.5, pitch=-0.1, expr="neutral", arm_l="down", arm_r=dict(hand=(0.36, 0.9), bend=0.5), legs="stand")}


def town_pose(name, g, shot):
    p = dict(TOWN_BASE[name])
    off = {"merchant": 0, "woman2": 4, "farmer": 9}[name]
    if shot == 4:
        u = ease((g - G_GLANCE - off) / 6.0, "sine") if g >= G_GLANCE + off else 0.0
        p["yaw"] = lerp(-0.45 if name != "farmer" else -0.3, 0.55, u)     # chatting to each other, then a glance at kenta
        p["gaze"] = (lerp(-0.6, 0.8, u), 0.0)
        if name == "merchant":
            p["expr"] = "smirk" if u > 0.5 else "neutral"
    p["head_roll"] = 3 * math.sin(g * 0.11 + off)
    p["blink"] = blink(g, [125 + off * 5, 200 + off * 3])
    return p


def extra_pose(name, g):
    if name == "kenta":
        return dict(yaw=0.2, expr="determined", arm_l="akimbo", arm_r=dict(hand=(0.4, 0.95), bend=0.6), legs="wide")
    p = dict(TOWN_BASE[name]); p["yaw"] = -p["yaw"] if name == "woman2" else p["yaw"]
    p["head_roll"] = 3 * math.sin(g * 0.1)
    return p


# ----------------------------------------------------------------------------- shot-only set pieces (the v2 set carries
# the open base, warm interior and the yard / street dressing itself: pagoda_API.md 1b)
def _ensure_coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c


def build_balcony():
    """Shot 5 foreground (ref a t0029-t0033): a lacquered balustrade across the bottom of the frame, two posts, a red banner at
    the left edge and a potted pine at the right, on the balcony the camera stands on."""
    coll = _ensure_coll("S01_BALC"); C = G.STATE["C"]; M = G.STATE["M"]
    red = C("#b8302a"); red_d = C("#7a2020"); wood = C("#4a2c1c"); gold = M["gold"]; floor = C("#7a5038")
    mb = G.MB()
    y = CAM5_A[0].y + 2.0; z0 = CAM5_A[0].z - 2.83
    mb.box((-3.0, y - 2.6, z0 - 0.2), (6.0, y + 0.2, z0), floor)
    mb.box((-3.0, y - 0.05, z0 + 0.95), (6.0, y + 0.1, z0 + 1.08), red)            # top rail
    mb.box((-3.0, y - 0.05, z0 + 0.15), (6.0, y + 0.1, z0 + 0.25), red_d)          # bottom rail
    x = -2.9
    while x < 6.0:
        mb.frustum((x, y + 0.02, z0 + 0.25), (x, y + 0.02, z0 + 0.95), 0.04, 0.04, wood, seg=6); x += 0.32
    for px in (-1.2, 4.2):
        mb.box((px - 0.15, y - 0.15, z0 - 0.2), (px + 0.15, y + 0.15, z0 + 1.3), red_d)
        mb.box((px - 0.18, y - 0.18, z0 + 1.3), (px + 0.18, y + 0.18, z0 + 1.38), gold)
    ob = mb.obj("s01_balcony", coll, hull=0.012)
    mb3 = G.MB()                                                                       # hanging banner, left edge, near
    bx, by = CAM5_A[0].x - 1.55, CAM5_A[0].y + 2.6
    mb3.oface([(bx, by, z0 + 0.1), (bx + 0.85, by, z0 + 0.1), (bx + 0.85, by, z0 + 2.2), (bx, by, z0 + 2.2)], red, [(0, 0)] * 4, (0, -1, 0))
    mb3.oface([(bx + 0.12, by - 0.01, z0 + 1.2), (bx + 0.73, by - 0.01, z0 + 1.2), (bx + 0.73, by - 0.01, z0 + 1.7), (bx + 0.12, by - 0.01, z0 + 1.7)], gold, [(0, 0)] * 4, (0, -1, 0))
    mb3.oface([(bx + 0.05, by - 0.005, z0 + 0.25), (bx + 0.8, by - 0.005, z0 + 0.25), (bx + 0.8, by - 0.005, z0 + 0.4), (bx + 0.05, by - 0.005, z0 + 0.4)], red_d, [(0, 0)] * 4, (0, -1, 0))
    for o in (ob,):
        T.no_bounce(o)
    return [ob]


# ----------------------------------------------------------------------------- the take
CANVAS_K1 = (-1.9375, -5.8125, 2.0625, 0.25)            # taller than the default: the chain_up runs out of the frame top


class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = G.build("DAY")
        G.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 6000
        self.balc = build_balcony()
        self.cam = camrig.make_camera(scene, name="cam_s01")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.kenta = actors.Actor("kenta", "kenta"); self.kenta.build(CANVAS_K1, sd, contact=True)
        self.town = {}
        for n in ("merchant", "woman2", "farmer"):
            a = actors.Actor(n, n); a.build(sprites.DEFAULT_CANVAS[n], sd, contact=True); self.town[n] = a
        self.all = [self.kenta] + list(self.town.values())
        for a in self.all:
            a.head_flip = False                       # DAY key from the south-west: screen-left in every view of this take
            T.no_bounce(a.card)
        self.info = {}
        self.anch = {}
        if verbose:
            print("s01: built in %.1f s" % (time.time() - t0), flush=True)

    def place(self, shot, f, g):
        if shot == 1:
            self.kenta.place(f, KENTA_S1)
        elif shot == 4:
            self.kenta.place(f, KENTA_S4)
            for n, a in self.town.items():
                a.place(f, TOWN_S4[n])
        elif shot == 5:
            self.kenta.place(f, EXTRAS_S5["kenta"])
            for n, a in self.town.items():
                a.place(f, EXTRAS_S5[n])

    def visible(self, shot):
        self.kenta.set_hidden(shot not in (1, 4, 5))
        for a in self.town.values():
            a.set_hidden(shot not in (4, 5))
        for o in self.balc:
            o.hide_render = shot != 5

    def pose(self, shot, gs):
        self.visible(shot)
        for g in gs:
            f = bf(shot, g)
            loc, look = CAMS[shot](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.place(shot, f, g)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 1:
                self.kenta.pose(f, kenta_s1(g), camera=self.cam)
            elif shot == 4:
                self.kenta.pose(f, kenta_s4(g), camera=self.cam)
                for n, a in self.town.items():
                    a.pose(f, town_pose(n, g, 4), camera=self.cam)
            elif shot == 5:
                self.kenta.pose(f, extra_pose("kenta", g), camera=self.cam)
                for n, a in self.town.items():
                    a.pose(f, extra_pose(n, g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        jobs = []
        if shot == 1:
            jobs = [(self.kenta, 384)]
        elif shot == 4:
            jobs = [(self.kenta, 384)] + [(a, 128) for a in self.town.values()]
        elif shot == 5:
            jobs = [(a, 64) for a in self.all]
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
            if a.card.hide_render or (a.name, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        pts = {"pillar_foot": (0.0, 0.0, G.FOOT_Z), "door": (0.0, -3.0, 2.4), "corner_eave": (-5.25, -5.25, 4.45), "pagoda_top": (0, 0, G.SORIN_TOP),
               "tower_top": (14.0, 0.0, 20.8), "gate": (0.0, -32.0, 4.0)}
        out["pts"] = {k: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for k, p in pts.items()}
        return out

    def dof(self, shot):
        """Depth of field per shot as pagoda_work/v2/s01_v2.py (set's Z-pass blur, G.setup_dof): focus, f-stop."""
        foc, fs = {1: (self.kenta.card, 3.5), 2: ((0.2, -0.62, G.FOOT_Z + 0.5), 6.0), 3: ((-3.6, -3.4, 6.0), 7.0),
                   4: (self.kenta.card, 6.0), 5: (None, None)}[shot]
        self.scene.camera = self.cam
        G.setup_dof(self.scene, foc, fs, cam=self.cam)
        return foc, fs

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(shot)
        self.dof(shot)
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
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take()
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                gs = [RANGES[shot][0], (RANGES[shot][0] + RANGES[shot][1]) // 2, RANGES[shot][1]]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        # resumable: raw/s<shot>/g_%04d.png + .json (json written after the PNG is complete)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        Tk = None
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            out = os.path.join(HERE, "raw", "s%d" % shot)
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if Tk is None:
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
