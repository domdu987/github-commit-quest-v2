#!/usr/bin/env python3
"""shot.py -- film 7 take s14: shots 14-15 (plan 44.53-51.19 s = g 1336..1535) + 6-frame handles (g 1330..1541).
louvre exit_door (CORRIDOR_MORNING), one location, five set-ups:

Shot 14 (g 1336..1433)  "แต่ประตูทางออกล็อกอยู่ / เขายืนเหงื่อแตก"
    C1 g 1330..1380  medium wide, slow push: vincenzo (smock, bulge) tugs the locked door: right hand pinned on the lock (the knob
                     is missing), three hard tugs (1340 / 1352 / 1364), the door rattles 0..0.9 deg in its frame.
    C2 g 1381..1433  CUT close, 3/4 from the right: sweat pours (sweat 0.6 -> 1, pale), one more weak tug, a gulp, then he hears
                     steps and his eyes flick toward screen-right (1422).
Shot 15 (g 1434..1535)  "จนช่างประปาคนหนึ่งเดินผ่านมา / ช่วยไขประตูให้ / แถมยิ้มทักอีกต่างหาก"
    C3 g 1434..1464  CUT wide: the plumber walks in from screen-right to the door, vincenzo backs off to the left, stiff grin.
    C4 g 1465..1494  CUT insert (ECU): the plumber's key in the lock turns (1463..1475, "ช่วยไขประตูให้" 48.81 s = g 1467), clunk,
                     he pulls: the door starts to swing (1479..), daylight cracks in.
    C5 g 1495..1541  CUT medium two-shot: the door swings wide (-> 92 deg) on the bright courtyard, the plumber turns and greets
                     him with a big smile and a wave ("แถมยิ้มทัก" 49.69 s = g 1494); vincenzo's frozen nervous grin.  Handle 1536..1541.
Mouths: nobody speaks on a quoted line: static expression mouths only (no lip-sync).  NO depth of field (C.Take).
Theft headlines: the corridor's own two framed notices (louvre news[2] / news[3], "LE VOL DU LOUVRE" / "MYSTERE AU LOUVRE") are
re-textured at runtime with the neutral posters (choc / opera): the theft is not known yet.
Blender frame of g = g + 1.

    python3 shot.py probe 1 a:b[:step]
    python3 shot.py stills 1 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1 a:b[:step] [scale] [samples]
"""
import math, os, sys, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez = C.lerp, C.clamp, C.blink, C.pulse, C.ez
TMP = os.path.join(HERE, "work")

_spec = importlib.util.spec_from_file_location("s01shot", os.path.join(os.path.dirname(HERE), "s01", "shot.py"))
S01 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(S01)     # reuse s01's dress_corridor() (read-only)

G0, G1 = C.g_bound(44.53), C.g_bound(51.19)        # 1336, 1536
G15 = C.g_bound(47.80)                              # 1434
H = 6
RANGES = {1: (G0 - H, G1 + H - 1)}                  # 1330..1541
SHOT_RANGES = {14: (G0, G15 - 1), 15: (G15, G1 - 1)}
SPAN = {"C1": (1330, 1380), "C2": (1381, 1433), "C3": (1434, 1464), "C4": (1465, 1494), "C5": (1495, 1541)}
FP = lambda g: g + 1


def setup_of(g):
    for k, (a, b) in SPAN.items():
        if a <= g <= b:
            return k
    raise ValueError(g)


# ----------------------------------------------------------------------------- the door and its lock
HINGE = Vector((-1.1, 9.88, 0.0))
LOCK0 = Vector((0.70, 9.70, 2.49))                 # the lock box / keyhole on the shut door (knob missing)
TUGS = [1340, 1352, 1364, 1398]
G_KEY_IN, G_TURN = 1458, (1463, 1475)
G_OPEN = (1479, 1515)                              # door 0 -> 92
G_LET_GO = 1487


def door_at(g):
    if g < G_OPEN[0]:
        r = 0.0
        for t in TUGS:
            r = max(r, (0.9 if t != 1398 else 0.45) * pulse(g, t, t + 1, t + 6, 1.0))
        return r
    u = (g - G_OPEN[0]) / float(G_OPEN[1] - G_OPEN[0])
    return 92.0 * (ez(u, "sine") if u < 1 else 1.0)


def lock_at(g):
    a = math.radians(door_at(g))
    rel = LOCK0 - HINGE
    x = rel.x * math.cos(a) + rel.y * math.sin(a)
    y = -rel.x * math.sin(a) + rel.y * math.cos(a)
    return Vector((HINGE.x + x, HINGE.y + y, LOCK0.z))


def tug(g):
    r = 0.0
    for t in TUGS:
        r = max(r, (1.0 if t != 1398 else 0.5) * pulse(g, t - 2, t, t + 5, 1.0))
    return r


# ----------------------------------------------------------------------------- blocking
VIN_DOOR = Vector((0.22, 8.92, 0.0))
VIN_BACK = Vector((-0.30, 6.75, 0.0))
G_BACK = (1440, 1456)
PL_START, PL_LOCK = Vector((2.70, 3.30, 0.0)), Vector((1.38, 8.98, 0.0))
G_PL_WALK = (1410, 1457)


def vin_at(g):
    u = ez((g - G_BACK[0]) / float(G_BACK[1] - G_BACK[0]))
    p = VIN_DOOR.lerp(VIN_BACK, u)
    return p + Vector((-0.03 * tug(g), 0.0, 0.0))


def pl_at(g):
    u = clamp((g - G_PL_WALK[0]) / float(G_PL_WALK[1] - G_PL_WALK[0]))
    u = u if u < 0.8 else 0.8 + 0.2 * ez((u - 0.8) / 0.2, "sine")
    return PL_START.lerp(PL_LOCK, u)


CAMS = {
    "C1": (((1.75, 4.00, 2.45), (0.05, 10.0, 2.85), 22.0), ((1.55, 4.70, 2.45), (0.05, 10.0, 2.85), 22.0)),
    "C2": (((2.15, 6.55, 2.40), (0.15, 9.6, 2.30), 26.0), ((2.05, 6.80, 2.40), (0.15, 9.6, 2.30), 27.0)),
    "C3": (((1.05, 2.60, 2.55), (0.35, 10.0, 2.85), 20.0), ((1.00, 2.95, 2.55), (0.35, 10.0, 2.85), 20.0)),
    "C4": (((0.50, 7.25, 2.70), (1.05, 9.6, 2.30), 28.0), ((0.42, 7.10, 2.70), (0.95, 9.6, 2.30), 27.0)),
    "C5": (((-0.45, 3.00, 2.50), (0.70, 10.0, 2.85), 22.0), ((-0.40, 3.55, 2.50), (0.65, 10.0, 2.85), 22.0)),
}


def cam_lin(g):
    s = setup_of(g)
    a, b = SPAN[s]
    u = ez((g - a) / float(b - a), "sine")
    (l0, k0, f0), (l1, k1, f1) = CAMS[s]
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u)), lerp(f0, f1, u)


# ----------------------------------------------------------------------------- poses
def vin_pose(g):
    t = tug(g)
    if g < G_BACK[0]:
        sw = 0.55 if g < 1381 else lerp(0.6, 1.0, clamp((g - 1381) / 30.0))
        p = dict(expr="worried", bulge=1.0, sweat=sw, pale=lerp(0.3, 0.55, clamp((g - 1381) / 30.0)), yaw=0.40,
                 pitch=-0.10 + 0.08 * t, head_roll=6 - 5 * t, gaze=(0.9, -0.2), lean=-3 - 6 * t, legs="narrow",
                 arm_l=dict(hand=(-0.18, 1.00), bend=0.7, shape="open", layer="front"))
        if 1381 <= g:
            p["yaw"] = lerp(0.40, 0.18, ez((g - 1381) / 10.0))                 # half toward us: the sweaty face
            p["gaze"] = (0.2, 0.1)
            p["expr"] = "worried"
            gl = pulse(g, 1410, 1412, 1417, 1.0)                               # gulp
            p["pitch"] = -0.05 + 0.16 * gl
            if g >= 1422:                                                      # steps behind him: eyes flick right
                p["gaze"] = (0.95, 0.0); p["yaw"] = 0.32
        p["blink"] = blink(g, [1372, 1393, 1419])
        return p, True
    # backing off / the nervous grin at the plumber
    u = ez((g - G_BACK[0]) / float(G_BACK[1] - G_BACK[0]))
    p = dict(cast7.STORY7["vincenzo_nervous_smile"][1])
    p.update(bulge=1.0, sweat=lerp(1.0, 0.8, u), pale=0.4, yaw=0.45, gaze=(0.9, 0.0), legs="narrow",
             expr="worried" if g < 1446 else "grinning")
    if g < G_BACK[1]:
        p["legs"] = dict(preset="step", stride=0.25 * math.sin(math.pi * u))
    if g >= 1495:
        p["head_roll"] = -6 + 2 * math.sin((g - 1495) * 0.4)                 # a stiff little nod back
        p["pitch"] = -0.05 + 0.08 * pulse(g, 1503, 1506, 1512, 1.0)
    p["blink"] = blink(g, [1445, 1490, 1525])
    return p, False


def pl_pose(g):
    if g < G_PL_WALK[1] - 3:
        u = clamp((G_PL_WALK[1] - 3 - g) / 6.0)
        base = dict(expr="happy", yaw=0.45, gaze=(0.0, 0.0), head_roll=-3)
        p = cast7.cycle("plumber", (g - G_PL_WALK[0]) / 24.0, "walk", facing=-1, base=base, speed=lerp(0.3, 0.8, u))
        if u < 1 and isinstance(p.get("legs"), dict):
            p["legs"] = dict(p["legs"], stride=p["legs"]["stride"] * u, lift_r=p["legs"]["lift_r"] * u, lift_l=p["legs"]["lift_l"] * u)
        p["blink"] = blink(g, [1447])
        return p, None
    if g < G_LET_GO:
        p = dict(cast7.STORY7["plumber_open_door"][1])
        p["expr"] = "happy"; p.pop("mouth", None)
        p["mirror"] = True
        p["blink"] = blink(g, [1470])
        return p, "key"
    # greets vincenzo: big smile + wave (plumber_greet waves screen-left = toward vincenzo)
    p = dict(cast7.STORY7["plumber_greet"][1])
    p["expr"] = "happy"; p.pop("mouth", None)            # a closed warm smile: no mouth movement outside the quoted lines
    w = ez((g - G_LET_GO) / 6.0)
    if "arm_r" in p and isinstance(p["arm_r"], dict) and "hand" in p["arm_r"]:
        hx, hy = p["arm_r"]["hand"]
        p["arm_r"] = dict(p["arm_r"], hand=(hx + 0.08 * math.sin((g - G_LET_GO) * 0.7) * w, hy))
    p["blink"] = blink(g, [1520])
    return p, None


def key_angle(g):
    """screen angle of the key (mirrored plumber, key pointing left into the lock): turns 180 -> 90 deg."""
    u = ez((g - G_TURN[0]) / float(G_TURN[1] - G_TURN[0]))
    return 180.0 - 90.0 * u


# ----------------------------------------------------------------------------- runtime dressing
def neutral_notices():
    """the corridor's own framed notices carry theft headlines (news[2], news[3]): swap in the neutral posters (choc, opera)."""
    M = L.STATE['M']
    for name, mat in (("corridor_notice_0", M['posters'][2]), ("corridor_notice_1", M['posters'][5])):
        ob = bpy.data.objects.get(name)
        if ob is not None:
            ob.data.materials.clear(); ob.data.materials.append(mat)
            for poly in ob.data.polygons:
                poly.material_index = 0


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "louvre", "exit_door", quality=quality, lens=22.0, name="cam_s14")
        self.shot = shot
        S01.dress_corridor()
        neutral_notices()
        for ob in self.scene.objects:
            if ob.name.startswith('sun_shafts'):
                ob.hide_render = True                    # s01: the shaft sheet washed the left half
        sd = os.path.join(TMP, "sprites")
        self.actors["vin"] = C.make_actor("vin", "vincenzo_smock", sd)
        self.actors["pl"] = C.make_actor("pl", "plumber", sd)

    def pose(self, shot, gs):
        vin, pl = self.actors["vin"], self.actors["pl"]
        for g in gs:
            f = FP(g)
            loc, look, lens = cam_lin(g)
            self.key_cam(f, loc, look, lens)
            C.place(vin, f, vin_at(g), 0.0)
            C.place(pl, f, pl_at(g), 0.0)
            self.key_set(f, door=door_at(g))            # (before his walk the plumber waits at PL_START, out of C1 / C2's view)
        for g in gs:
            f = FP(g)
            self.scene.frame_set(f)
            p, pin = vin_pose(g)
            hands = None
            if pin:
                lk = lock_at(g) + Vector((0.0, 0.0, -0.04 * tug(g)))
                hands = {"r": dict(hand=tuple(lk), bend=-0.5, stretch=1.3, shape="fist")}
            vin.pose(f, p, hands=hands, camera=self.cam)
            self.scene.frame_set(f)
            q, mode = pl_pose(g)
            hands = None
            if mode == "key":
                k_in = ez((g - (G_KEY_IN - 3)) / 4.0)
                tgt = lock_at(g)
                if k_in < 1.0:
                    tgt = tgt + Vector((0.25 * (1 - k_in), -0.15 * (1 - k_in), -0.1 * (1 - k_in)))
                hands = {"r": dict(tip=tuple(tgt), prop="key", angle=key_angle(g), stretch=1.35)}
            _, info = pl.pose(f, q, hands=hands, camera=self.cam)
            if hands and os.environ.get("DBG"):
                print("key", g, round(info["r"].get("error", 0), 3), flush=True)
        big = [FP(g) for g in gs if setup_of(g) in ("C2", "C4")]
        small = [FP(g) for g in gs if setup_of(g) not in ("C2", "C4")]
        for fr, ppd in ((small, 320), (big, 512)):
            if fr:
                self.sprites_for([(vin, ppd), (pl, ppd)], fr)

    def report(self, shot, g):
        f = FP(g)
        self.scene.frame_set(f)
        loc, look, lens = cam_lin(g)
        v = look - loc
        return dict(shot=shot, g=g, setup=setup_of(g), cam=[round(c, 3) for c in loc], lens=round(lens, 1),
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), door=round(door_at(g), 2),
                    heads=C.head_report(self, f), lock=[round(v, 1) for v in C.render.world_to_screen(self.cam, lock_at(g), f)[:2]])

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [FP(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[1][0] <= g <= RANGES[1][1]]
        Tk = Take("preview", 1)
        Tk.pose(1, gs)
        for g in gs:
            print(json.dumps(Tk.report(1, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[4]
                os.makedirs(out, exist_ok=True)
                scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                st = Tk.render(1, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q, 1), [1], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
