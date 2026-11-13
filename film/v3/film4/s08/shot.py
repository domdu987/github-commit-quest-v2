#!/usr/bin/env python3
"""shot.py -- film 4 take s08: shot 8 (g 480..592, out-handle g 593..599), pagoda set DAY.

Narration (sentence 4, the first quoted line): "ช่างใหญ่หัวเราะ  'เสาที่ไม่ค้ำอะไรเนี่ยนะ ไอ้หนู แผ่นดินไหวทีเดียวก็ล้ม'"
(the master laughed: "a pillar that holds nothing up, kid? one quake and it falls").

    8A  g 480..510  hard cut in from s07.  Eye-level two-shot in the courtyard: the master near (screen-right) points up-left at the
                    pagoda, smug; kenta far (screen-left) by the pagoda's platform.  On "หัวเราะ" (g 495) the master bursts out laughing
                    (eyes shut, static grin: no mouth movement before the quote).  Slow push (ref a t0011).
    8B  g 511..563  snap punch-in (g 508..514) to a low angle on the laughing master (ref a t0013): his mouth moves ONLY here, on the
                    quote "เสาที่ไม่ค้ำอะไรเนี่ยนะ ไอ้หนู แผ่นดินไหวทีเดียวก็ล้ม" (g 511 ->); on "ไอ้หนู" (g 547) he jabs a finger down
                    toward kenta (screen-left); slow drift.
    8C  g 564..599  hard cut (plan 18.7 s) to three townspeople laughing and pointing at the pagoda, the rigid tower behind them
                    (ref a t0015 / t0047); mouths static.  Out-handle g 593..599 rendered in 3D (camera keeps moving).

Blender frame of (part k, film frame g) = 1000 * (k - 1) + g + 1.   python3 shot.py probe|stills|final <parts> a:b ...
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast4"), os.path.join(V3, "stage"), os.path.join(V3, "set3d4"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast4                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import pagoda as G                                      # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


G0, GB, GC, G1, H = 480, 511, 564, 593, 7
RANGES = {1: (G0, GB - 1), 2: (GB, GC - 1), 3: (GC, G1 + H - 1)}
PUNCH = (508, 514)
G_LAUGH = g_of(16.39)            # 495 "หัวเราะ"
QUOTE = [(g_of(16.94), g_of(17.57)), (g_of(17.57), g_of(18.12)), (g_of(18.12), g_of(18.48)), (g_of(18.48), g_of(18.98)),
         (g_of(18.98), g_of(19.76))]        # 511-530 เสาที่ไม่ค้ำ, 530-547 อะไรเนี่ยนะ, 547-557 ไอ้หนู, 557-572 แผ่นดินไหว, 572-596 ทีเดียวก็ล้ม
Q0 = QUOTE[0][0]
G_KID = QUOTE[2][0]              # 547 "ไอ้หนู"


def bf(k, g):
    return 1000 * (k - 1) + int(g) + 1


def _pk(a, b):
    return tuple(a) + tuple(b)


def _mix(g, ks, share):
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), share)
    return Vector(k[:3]), Vector(k[3:])


# ----------------------------------------------------------------------------- staging
MASTER = (8.0, -15.6, 0.0)
KENTA = (-2.35, -6.35, 0.0)
TOWN = {"merchant": (3.05, -16.75, 0.0), "woman2": (4.45, -17.45, 0.0), "farmer": (5.85, -16.65, 0.0)}

CAM_A0 = (Vector((10.3, -20.0, 3.05)), Vector((2.0, -6.5, 2.65)))
CAM_A1 = (Vector((10.05, -19.55, 3.0)), Vector((2.2, -6.5, 2.62)))
CAM_B0 = (Vector((9.35, -18.15, 1.45)), Vector((8.05, -15.15, 3.05)))
CAM_B1 = (Vector((9.15, -17.85, 1.5)), Vector((8.0, -15.15, 3.0)))
CAM_C0 = (Vector((5.3, -22.6, 2.45)), Vector((4.5, -15.6, 2.5)))
CAM_C1 = (Vector((5.25, -22.0, 2.42)), Vector((4.5, -15.6, 2.47)))


def camA(g):
    return _mix(g, [(G0, _pk(*CAM_A0), "sine"), (PUNCH[0], _pk(*CAM_A1), "quint"), (PUNCH[1], _pk(*CAM_B0), "sine"),
                    (GC, _pk(*CAM_B1), "hold")], 0.15)


def camC(g):
    a, b = RANGES[3]
    loc, look = _mix(g, [(a, _pk(*CAM_C0), "cubic_out"), (b + 1, _pk(*CAM_C1), "hold")], 0.4)
    j = 0.018 * math.sin(g * 1.9) + 0.012 * math.sin(g * 3.1 + 1)           # small laugh-bounce handheld feel
    return loc + Vector((0, 0, j)), look + Vector((0, 0, j))


CAMS = {1: camA, 2: camA, 3: camC}


# ----------------------------------------------------------------------------- performances
def _h(g, k=0):
    x = math.sin(g * 12.9898 + k * 78.233) * 43758.5453
    return x - math.floor(x)


def lipsync(g):
    """mouth for frame g inside the quote: a new drawing every 2 frames (talk_a / talk_b / talk_o), 'flat' for one drawing at each
    word boundary; outside the quote None."""
    for (a, b) in QUOTE:
        if a <= g < b:
            if g - a < 2 and a != Q0:
                return "flat"
            s = (g - a) // 2
            r = _h(s + a)
            return "talk_b" if r < 0.45 else ("talk_a" if r < 0.8 else "talk_o")
    return None


def master_pose(g):
    if g < G_LAUGH - 2:
        p = dict(cast4.STORY4["master_point_tower"][1])
        p["mouth"] = "smirk"
        p["head_roll"] = -6 + 1.5 * math.sin(g * 0.2)
        p["blink"] = blink(g, [486])
        return p
    p = dict(cast4.STORY4["master_laugh"][1])
    shake = math.sin(2 * math.pi * (g - G_LAUGH) / 7.0)
    burst = ease((g - (G_LAUGH - 2)) / 5.0, "back_out")
    p["head_roll"] = 14 * burst + 4 * shake
    p["lean"] = -6 * burst - 1.5 * shake
    p["squash"] = (1.0 + 0.03 * burst + 0.012 * shake, 1.0 - 0.03 * burst - 0.012 * shake)
    p["t"] = (g - G_LAUGH) / 30.0
    p["yaw"] = -0.25
    m = lipsync(g)
    p["mouth"] = m if m else "grin"
    p["expr"] = "laughing"
    p["blink"] = 2
    if g >= G_KID - 3:
        u = ease((g - (G_KID - 3)) / 5.0, "back_out")
        jab = pulse(g, G_KID, G_KID + 3, G_KID + 9, 1.0)
        p["arm_l"] = dict(hand=(lerp(-0.26, -0.92, u), lerp(1.18, 0.55 + 0.08 * jab, u)), shape="point" if u > 0.4 else "fist",
                          bend=lerp(0.9, -0.3, u), stretch=1.3)
        p["blink"] = 0 if g >= G_KID + 2 else 2            # opens his eyes to look at the kid
        if g >= G_KID + 2:
            p["expr"] = "grinning"
            p["gaze"] = (-0.7, 0.3)
    return p


def kenta_pose(g):
    p = dict(cast4.STORY4["kenta_worried"][1])
    p["yaw"] = 0.35
    p["gaze"] = (0.7, -0.1)
    p["mouth"] = "wavy"
    p["blink"] = blink(g, [500])
    return p


TOWN_KEYS = {"merchant": "town_laugh_point", "woman2": "town_laugh_point_woman2", "farmer": "town_laugh_point_farmer"}


def town_pose(n, g):
    p = dict(cast4.STORY4[TOWN_KEYS[n]][1])
    off = {"merchant": 0, "woman2": 3, "farmer": 6}[n]
    sh = math.sin(2 * math.pi * (g + off) / 8.0)
    ys = -1.0 if n == "woman2" else 1.0
    p["head_roll"] = (-10 + 4 * sh) * ys
    p["lean"] = (-5 - 2 * sh) * ys
    p["squash"] = (1.0 + 0.015 * sh, 1.0 - 0.015 * sh)
    p["t"] = (g - GC) / 30.0 + off
    if n == "woman2":                                     # she points the same way (at the pagoda, screen-left): unmirrored
        p["mirror"] = False
        p["yaw"] = -0.35; p["head_roll"] = -10 + 4 * sh; p["lean"] = -5 - 2 * sh
    al = dict(p["arm_l"]); al["hand"] = (al["hand"][0], al["hand"][1] + 0.06 * sh); p["arm_l"] = al
    return p


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = G.build("DAY")
        G.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 4000
        self.cam = camrig.make_camera(scene, name="cam_s08")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.master = actors.Actor("master", "master"); self.master.build(sprites.DEFAULT_CANVAS["master"], sd, contact=True)
        self.kenta = actors.Actor("kenta", "kenta"); self.kenta.build(sprites.DEFAULT_CANVAS["kenta"], sd, contact=True)
        self.town = {}
        for n in TOWN:
            a = actors.Actor(n, n); a.build(sprites.DEFAULT_CANVAS[n], sd, contact=True); self.town[n] = a
        self.all = [self.master, self.kenta] + list(self.town.values())
        for a in self.all:
            a.head_flip = False                            # DAY key from the south-west: screen-left in all three cameras
            T.no_bounce(a.card)
        self.anch = {}
        if verbose:
            print("s08: built in %.1f s" % (time.time() - t0), flush=True)

    def visible(self, k):
        self.master.set_hidden(k == 3)
        self.kenta.set_hidden(k == 3)
        for a in self.town.values():
            a.set_hidden(k != 3)

    def pose(self, k, gs):
        self.visible(k)
        for g in gs:
            f = bf(k, g)
            loc, look = CAMS[k](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.master.place(f, MASTER)
            gone = k == 2 and g >= PUNCH[1] + 1                  # kenta has left the frame (bottom-left edge) at the end of the punch
            self.kenta.place(f, (KENTA[0], KENTA[1] - 80.0, -40.0) if gone else KENTA, interp="CONSTANT")
            for n, a in self.town.items():
                a.place(f, TOWN[n])
        for g in gs:
            f = bf(k, g)
            self.scene.frame_set(f)
            if k in (1, 2):
                self.master.pose(f, master_pose(g), camera=self.cam)
                self.kenta.pose(f, kenta_pose(g), camera=self.cam)
            else:
                for n, a in self.town.items():
                    a.pose(f, town_pose(n, g), camera=self.cam)
        fr = [bf(k, g) for g in gs]
        jobs = [(self.master, 384), (self.kenta, 128)] if k in (1, 2) else [(a, 256) for a in self.town.values()]
        for a, ppd in jobs:
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s08: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def report(self, k, g):
        f = bf(k, g)
        self.scene.frame_set(f)
        loc, look = CAMS[k](g)
        v = look - loc
        out = dict(part=k, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={}, mouth=lipsync(g) if k != 3 else None)
        for a in self.all:
            if a.card.hide_render or (a.name, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        pts = {"pagoda_top": (0, 0, G.SORIN_TOP), "tower_top": (14.0, 0.0, 20.8)}
        out["pts"] = {n: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for n, p in pts.items()}
        return out

    def dof(self, k):
        foc, fs = {1: ((MASTER[0], MASTER[1], 2.8), 3.0), 2: ((MASTER[0], MASTER[1], 2.8), 3.5), 3: ((4.45, -17.45, 2.7), 3.0)}[k]
        self.scene.camera = self.cam
        G.setup_dof(self.scene, foc, fs, cam=self.cam)
        return foc, fs

    def render(self, k, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(k)
        self.dof(k)
        self.scene.cycles.samples = samples
        return render.render_frames([bf(k, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
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


def main(Take, RANGES, tag):
    cmd = sys.argv[1]
    parts = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take()
        for k in parts:
            gs = [g for g in parse(sys.argv[3]) if RANGES[k][0] <= g <= RANGES[k][1]]
            if not gs:
                gs = [RANGES[k][0], (RANGES[k][0] + RANGES[k][1]) // 2, RANGES[k][1]]
            Tk.pose(k, gs)
            for g in gs:
                print(json.dumps(Tk.report(k, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(k, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "p%d_g_%04d.png" % (k, g)))
                    print("part %d g %d  %.1f s wall %.1f cpu" % (k, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        Tk = None
        for k in parts:
            gs = [g for g in parse(sys.argv[3]) if RANGES[k][0] <= g <= RANGES[k][1]]
            out = os.path.join(HERE, "raw", "p%d" % k)
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: part %d, %d to render, %d done" % (k, len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if Tk is None:
                Tk = Take(quality="final")
            Tk.pose(k, todo)
            for g in todo:
                st = Tk.render(k, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(k, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("%s part %d g %d  %.1f s wall  %.1f s cpu" % (tag, k, g, st["wall"], st["cpu"]), flush=True)


if __name__ == "__main__":
    main(Take, RANGES, "s08")
