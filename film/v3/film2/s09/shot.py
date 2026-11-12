#!/usr/bin/env python3
"""shot.py -- film 2 take s09: shot 9 (g 605..718 + 6 handle frames out), tower set DAY, bell chamber, chamber_eye.

    Two-shot in depth: padre near (priest_mark, padre_laugh: closed laughing eyes, tears, hands on the belly, body bouncing),
    nico far under the bell (hero_mark, nico_hold_rod: the rod upright beside him, determined).
      g 605        hard cut in; two-shot, camera settling (cubic out) and creeping in
      g 609..646   "บาทหลวงหัวเราะ": padre laughs (mouth wide open, held: laughing is not speech), shoulders bounce
      g 632..642   snap reframe onto padre (lands g 639 = t 21.2)
      g 647..718   the quoted line "เหล็กแท่งเดียว จะไปสู้ฟ้าได้ยังไง ไอ้หนู": padre's mouth moves (lip-sync from the narration
                   envelope: flat / talk_a / talk_b / talk_o, a new drawing at most every 2 frames)
      g 670..678   small push-in step on "จะไปสู้ฟ้า" (g 676)
      g 696..704   snap reframe past padre's shoulder onto nico on "ไอ้หนู" (g 703); nico's look hardens (no mouth)
      g 719..724   out-handle (9-frame dissolve into shot 10), the camera keeps drifting
Blender frame = g + 1.
    python3 shot.py probe a:b:step
    python3 shot.py stills a:b:step out_dir [scale] [samples]
    python3 shot.py final a:b [scale] [samples]
"""
import math, os, sys, time, json, wave

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast2"), os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast2                                            # noqa: E402
import bpy                                              # noqa: E402
import numpy as np                                      # noqa: E402
from mathutils import Vector                            # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


G0, G1, H_OUT = 605, 719, 6
RANGE = (G0, G1 + H_OUT - 1)
G_QUOTE0, G_QUOTE1 = g_of(21.464), g_of(23.956)          # 647 .. 722 (padre speaks)
SNAP_P = (632, 642)                                      # onto padre, lands 639
STEP = (670, 678)
SNAP_N = (696, 705)                                      # onto nico, "ไอ้หนู" g 703

PADRE = (-0.62, -0.75, 15.0)
NICO = (0.62, 0.75, 15.0)


# ----------------------------------------------------------------------------- lip-sync from the narration envelope
def _envelope():
    w = wave.open(os.path.join(PROJ, "audio", "narration.wav"))
    sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    env = {}
    for g in range(G_QUOTE0 - 2, G_QUOTE1 + 3):
        t = g / 30.0 - 0.10
        i0, i1 = int(max(0, (t - 1 / 60.0) * sr)), int((t + 1 / 60.0) * sr)
        env[g] = float(np.sqrt(np.mean(a[i0:i1] ** 2))) if i1 > i0 else 0.0
    m = max(env.values()) or 1.0
    return {g: v / m for g, v in env.items()}


ENV = _envelope()


def mouth(g):
    """speech mouth for frame g inside the quote, held for 2 frames (even frames choose)."""
    if not (G_QUOTE0 <= g < G_QUOTE1):
        return None
    g2 = g - ((g - G_QUOTE0) % 2)
    v = ENV.get(g2, 0.0)
    if v < 0.12:
        return "flat"
    if v < 0.40:
        return "talk_a"
    return "talk_o" if (g2 // 2) % 5 == 3 else "talk_b"


# ----------------------------------------------------------------------------- camera
def V(*a):
    return Vector(a)


PH = V(PADRE[0], PADRE[1], 15.0 + 2.82)          # padre head (approx)
NH = V(NICO[0], NICO[1], 15.0 + 1.98)


def cam(g):
    two_a = (V(0.30, -4.25, 17.25), V(0.02, 1.9, 17.55))
    two_b = (V(0.22, -4.00, 17.30), V(0.0, 1.9, 17.58))
    pad_a = (V(-0.60, -3.05, 17.55), PH + V(0.16, 0.0, -0.30))
    pad_b = (V(-0.68, -2.85, 17.58), PH + V(0.13, 0.0, -0.30))
    pad_c = (V(-0.80, -2.62, 17.62), PH + V(0.10, 0.0, -0.32))
    pad_d = (V(-0.86, -2.52, 17.62), PH + V(0.08, 0.0, -0.32))
    nic_a = (V(0.05, -2.55, 17.05), NH + V(-0.32, 0.0, -0.22))
    nic_b = (V(0.12, -2.35, 17.02), NH + V(-0.30, 0.0, -0.24))
    T_ = lambda p: tuple(p[0]) + tuple(p[1])
    ks = [(G0, T_(two_a), "cubic_out"), (SNAP_P[0], T_(two_b), "quint"), (SNAP_P[1], T_(pad_a), "sine"),
          (STEP[0], T_(pad_b), "quint"), (STEP[1], T_(pad_c), "sine"), (SNAP_N[0], T_(pad_d), "quint"),
          (SNAP_N[1], T_(nic_a), "sine"), (RANGE[1] + 1, T_(nic_b), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.12)
    return Vector(k[:3]), Vector(k[3:])


# ----------------------------------------------------------------------------- poses
def padre_pose(g):
    _, base = cast2.STORY2["padre_laugh"]
    p = dict(base)
    lau = 0.5 + 0.5 * math.sin(g * 1.15)                 # laugh bounce
    k = 1.0 if g < G_QUOTE0 else 0.45                     # calmer while speaking
    p["squash"] = (1.0 + 0.03 * lau * k, 1.0 - 0.035 * lau * k)
    p["head_roll"] = 14 - 6 * k * lau + (4 * math.sin(g * 0.2) if g >= G_QUOTE0 else 0)
    p["lean"] = -6 - 3 * k * lau
    p["t"] = (g - G0) / 30.0 * 0.6
    m = mouth(g)
    if m is not None:
        p["mouth"] = m
    for a, dy in (("arm_r", 0.03), ("arm_l", 0.03)):
        arm = dict(p[a]); hx, hy = arm["hand"]; arm["hand"] = (hx, hy - dy * lau * k); p[a] = arm
    return p


def nico_pose(g):
    _, base = cast2.STORY2["nico_hold_rod"]
    p = dict(base)
    p["expr"] = "determined"
    p["blink"] = blink(g, [620, 661, 690])
    p["head_roll"] = -3 + 2 * math.sin(g * 0.09) + (-3 * ease((g - 700) / 6.0) if g > 700 else 0)
    p["gaze"] = (-0.6, -0.1)
    p["squash"] = (1.0 + 0.008 * math.sin(g * 0.18), 1.0 - 0.008 * math.sin(g * 0.18))
    return p


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, quality="preview"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = sc = bpy.context.scene
        self.A = T.build("DAY")
        T.setup_render(sc, quality)
        sc.render.use_persistent_data = False
        sc.cycles.transparent_max_bounces = 12
        sc.frame_start, sc.frame_end = 1, 3000
        T.set_rod(0)
        T.set_bell(0)
        mk = bpy.data.objects.get("market")
        if mk is not None:
            mk.hide_render = True
        self.cam = camrig.make_camera(sc, name="cam_s09")
        self.cam.data.clip_start = 0.02; self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.padre = actors.Actor("padre", "padre"); self.padre.build(sprites.DEFAULT_CANVAS["padre"], sd, contact=True)
        self.nico = actors.Actor("nico", "nico"); self.nico.build(sprites.DEFAULT_CANVAS["nico"], sd, contact=True)
        self.all = [self.padre, self.nico]
        for a in self.all:
            a.head_flip = False
            T.no_bounce(a.card)
        self.anch = {}

    def pose(self, gs):
        for g in gs:
            f = g + 1
            loc, look = cam(g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.padre.place(f, PADRE); self.nico.place(f, NICO)
        for g in gs:
            f = g + 1
            self.scene.frame_set(f)
            self.padre.pose(f, padre_pose(g), camera=self.cam)
            self.nico.pose(f, nico_pose(g), camera=self.cam)
        fr = [g + 1 for g in gs]
        for a, ppd in ((self.padre, 512), (self.nico, 384)):
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s09: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def report(self, g):
        f = g + 1
        self.scene.frame_set(f)
        out = dict(g=g, heads={}, mouth=mouth(g))
        for a in self.all:
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
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
        print("final s09: %d to render" % len(todo), flush=True)
        if todo:
            Tk = Take(quality="final"); Tk.pose(todo)
            for g in todo:
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g); os.replace(st["path"], png)
                rep = Tk.report(g); rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
                json.dump(rep, open(png[:-4] + ".json", "w"))
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
