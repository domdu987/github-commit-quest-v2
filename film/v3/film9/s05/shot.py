#!/usr/bin/env python3
"""shot.py -- film 9 take s05: shots 5, 6, 7 (g 270..506 + 6 handle frames each side: g 264..512).
One location (wall_site, DAY light), one build, three set-ups joined by the plan's cuts:

    id 5  g 264..338  shot 5, cauldron: the giant wok steams, lin stirs on his platform (screen-right).  The armoured general strides
                      in from screen-left, stops at the stove, looks at the rice soup and bursts out laughing ("หัวเราะลั่น").
    id 6  g 339..432  shot 6, low medium two-shot from the site side: the general big in the foreground left, pointing up at lin and
                      mocking (lip-sync on the quote "ข้าวเหนียวเนี่ยนะ เอ็งจะทำขนมให้กำแพงกินเหรอ!"), lin on his platform behind the
                      steaming wok stays calm (calm smile, keeps stirring).
    id 7  g 433..512  shot 7, site medium: three workers in the foreground point and laugh at lin ("ไอ้ช่างขนม"), lin small at the
                      cauldron, scaffolds, the wall and the gate tower behind.  Out-handle g 507..512.
Mouths: only the general's quote moves a mouth (g 333..432, driven by the narration envelope); all other mouths are static.
NO depth of field (client rule).  Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 5,6,7 a:b[:step]
    python3 shot.py stills 5,6,7 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 5|6|7 a:b[:step] [scale] [samples]
"""
import math, os, sys, json, wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402  (paths, cast9 first, bpy, wall, stage)
from mathutils import Vector                             # noqa: E402
import numpy as np                                       # noqa: E402

W, actors, camrig, cast9 = C.W, C.actors, C.camrig, C.cast9
lerp, clamp, ez, bf = C.lerp, C.clamp, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0 = C.g_bound(9.01)               # 270 shot 5
G6 = C.g_bound(11.30)              # 339 shot 6
G7 = C.g_bound(14.44)              # 433 shot 7
G1 = C.g_bound(16.90)              # 507 shot 8 (next take)
H = 6
RANGES = {5: (G0 - H, G6 - 1), 6: (G6, G7 - 1), 7: (G7, G1 + H - 1)}
G_STOP = C.g_of(9.89) - 4          # 296: the general stops at the stove ("หัวเราะ" = g 300)
G_LAUGH = C.g_of(9.89)             # 300: bursts out laughing
G_TALK = (C.g_of(10.98) + 1, G7 - 1)      # 333..432: the quote (mouth moves only here)
G_KHANOM = C.g_of(16.17)           # 488: "ไอ้ช่างขนม" -- the workers' laugh peaks

# ----------------------------------------------------------------------------- narration envelope (lip-sync level)
_ENV = {}


def env(g):
    if not _ENV:
        w = wave.open(C.NARRATION); sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
        for gg in range(0, 1800):
            t = gg / 30.0 - 0.10
            s = a[max(0, int(t * sr)):max(0, int((t + 1 / 30.0) * sr))]
            _ENV[gg] = float(np.sqrt((s ** 2).mean())) / 3000.0 if len(s) else 0.0
    return _ENV.get(g, 0.0)


def mouth_of(g):
    lv = env(g)
    if lv < 0.25:
        return "smile"
    return cast9.talk_mouth(g, clamp(lv / 2.0), seed=3.0, hold=2)


# ----------------------------------------------------------------------------- staging (world D; wall inner face y 5, site +y)
LIN = Vector((-15.15, 13.3, 1.5))           # W mark lin_stir: platform beside the wok
GEN_A0 = Vector((-5.7, 17.8, 0.0))          # shot 5: enters from screen-left (+x) ...
GEN_A1 = Vector((-9.5, 17.4, 0.0))          # ... stops at the stove (wok rim r 3.0 round (-11, 13.5))
GEN_B = Vector((-9.9, 18.4, 0.0))           # shot 6: site side of the stove, foreground left
WORKERS = [("worker_a", "workers_laugh", Vector((-20.1, 21.0, 0.0))),
           ("worker_b", "workers_laugh_b", Vector((-20.6, 20.1, 0.0))),
           ("worker_c", "workers_point_c", Vector((-22.4, 17.4, 0.0)))]


def aim(loc, look):
    return (tuple(loc), tuple(look))


# all three cameras look from the site side (+y) and west of the wok, so lin on his platform (-x side of the wok) is clear of the
# rim and on screen-RIGHT of the wok: lin is drawn mirrored (stirs screen-left).
CAM = {5: (aim((-9.6, 24.6, 5.6), (-11.8, 12.0, 2.2)), aim((-10.3, 23.6, 5.4), (-12.0, 12.0, 2.2))),
       6: (aim((-10.2, 23.4, 2.8), (-11.3, 13.0, 3.6)), aim((-10.6, 22.85, 2.76), (-11.6, 13.0, 3.6))),
       7: (aim((-28.3, 23.9, 5.2), (-12.5, 13.0, 1.4)), aim((-28.0, 22.6, 5.0), (-12.5, 13.2, 1.4)))}
LENS = {5: 22.0, 6: 22.0, 7: 24.0}
PPD = {5: 256, 6: 320, 7: 256}


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    (l0, k0), (l1, k1) = CAM[shot]
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


# ----------------------------------------------------------------------------- poses
STIR = cast9.STORY9["lin_stir"][1]


def pose_stir(g, calm=0.0):
    """lin stirring: both hands on a small ellipse every 24 frames, paddle angle 58 +- 8 (STORY9 note); calm > 0 = smile."""
    p = json.loads(json.dumps(STIR))
    ph = 2 * math.pi * g / 24.0
    dx, dy = 0.12 * math.cos(ph), 0.05 * math.sin(ph)
    p["arm_l"]["hand"] = (p["arm_l"]["hand"][0] + dx, p["arm_l"]["hand"][1] + dy)
    p["arm_r"]["hand"] = (p["arm_r"]["hand"][0] + dx, p["arm_r"]["hand"][1] + dy)
    p["prop_l"]["angle"] = 58 + 8 * math.sin(ph)
    p["lean"] = 8 + 2.5 * math.sin(ph)
    p["t"] = g / 30.0
    if calm > 0:
        p["expr"] = "smug" if calm > 0.5 else "determined"
        p["mouth"] = "smile"
        p["gaze"] = (lerp(0.7, 0.5, calm), lerp(0.6, 0.0, calm))
        p["yaw"] = lerp(0.55, 0.25, calm)
        p["pitch"] = lerp(0.45, 0.1, calm)
    p["mirror"] = True
    p["blink"] = C.blink(g, [281, 352, 395, 450, 497])
    return p


def pose_gen_a(g):
    """shot 5: walk in (cycle, facing screen-right), stop, look at the soup, then the belly laugh (static open mouth until g 333)."""
    if g < G_STOP:
        ph = (g - RANGES[5][0]) / 18.0
        base = dict(expr="smug", pitch=-0.2, yaw=0.6)
        p = cast9.cycle("general", ph, "walk", facing=1, base=base, speed=1.25)
        return p
    s = u_of(g, G_STOP, G_LAUGH)
    if g < G_LAUGH:
        p = dict(yaw=0.6, pitch=lerp(-0.2, 0.3, s), expr="surprised", gaze=(0.8, 0.6), arm_r="akimbo", arm_l="akimbo", legs="wide")
        return p
    p = json.loads(json.dumps(cast9.STORY9["general_laugh"][1]))
    k = g - G_LAUGH
    p["squash"] = (1.02, 0.98) if (k // 3) % 2 == 0 else (0.99, 1.01)
    p["head_roll"] = -10 + 3 * math.sin(k * 0.7)
    p["lean"] = -8 + 2 * math.sin(k * 0.9)
    p["mouth"] = mouth_of(g) if g >= G_TALK[0] else "talk_b"
    p["yaw"] = 0.45
    p["t"] = g / 30.0
    return p


def pose_gen_b(g):
    """shot 6: laughs, then points at lin and mocks (lip-sync), a second laugh on 'กินเหรอ!'."""
    k = g - G6
    mock = json.loads(json.dumps(cast9.STORY9["general_mock"][1]))
    laugh = json.loads(json.dumps(cast9.STORY9["general_laugh"][1]))
    if g < G6 + 12 or g >= C.g_of(13.98) - 4:          # laugh beats at both ends
        p = laugh
        p["squash"] = (1.02, 0.98) if (k // 3) % 2 == 0 else (0.99, 1.01)
        p["head_roll"] = -10 + 3 * math.sin(k * 0.7)
        p["lean"] = -8 + 2 * math.sin(k * 0.9)
        p["yaw"] = 0.45
    else:
        p = mock
        f = u_of(g, G6 + 12, G6 + 20)
        p["arm_r"]["hand"] = (lerp(0.45, 1.05, f), lerp(0.95, 0.1 + 0.05 * math.sin(k * 0.5), f))
        p["arm_r"]["shape"] = "point" if f > 0.5 else "open"
        p["head_roll"] = 8 + 3 * math.sin(k * 0.21)
        p["lean"] = 2 * math.sin(k * 0.17) + 3 * f
        p["pitch"] = -0.3 + 0.08 * math.sin(k * 0.3)
        p["gaze"] = (0.9, -0.5)
    p["mouth"] = mouth_of(g)
    p["blink"] = C.blink(g, [366, 404])
    p["t"] = g / 30.0
    return p


def pose_worker(name, key, g):
    p = json.loads(json.dumps(cast9.STORY9[key][1]))
    k = g + 7 * len(name)
    pk = math.exp(-((g - G_KHANOM) / 10.0) ** 2)
    p["lean"] = p.get("lean", 0) - 4 * pk + 2.2 * math.sin(k * 0.6)
    p["head_roll"] = p.get("head_roll", 0) + 3 * math.sin(k * 0.45)
    p["squash"] = (1.0 + 0.015 * math.sin(k * 1.9), 1.0 - 0.015 * math.sin(k * 1.9))
    if "arm_r" in p and isinstance(p["arm_r"], dict):
        h = p["arm_r"]["hand"]; p["arm_r"]["hand"] = (h[0], h[1] + 0.05 * math.sin(k * 0.8))
    if name == "worker_c":
        p["mirror"] = True                       # right of lin on screen: points back at him (screen-left)
    p["blink"] = C.blink(g, [450 + len(name), 495])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "wall_site", "cauldron", quality=quality, lens=22.0, name="cam_s05", light="DAY")
        sd = os.path.join(TMP, "sprites")
        self.lin = self.actors["lin"] = C.make_actor("lin", "lin", sd, canvas=(-2.625, -4.875, 2.625, 0.125))
        self.gen = self.actors["gen"] = C.make_actor("gen", "general", sd, canvas=(-2.25, -5.375, 2.25, 0.125))
        self.wk = []
        for nm, key, xy in WORKERS:
            a = self.actors[nm] = C.make_actor(nm, cast9.STORY9[key][0], sd)
            self.wk.append((a, key, xy))

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS[shot])
            self.key_set(f, steam=1.1, heights=(16, 16))
            C.place(self.lin, f, LIN, z=LIN.z)
            if shot == 5:
                gp = GEN_A0.lerp(GEN_A1, clamp((g - RANGES[5][0]) / float(G_STOP - RANGES[5][0])))
            else:
                gp = GEN_B
            C.place(self.gen, f, gp)
            self.gen.card.hide_render = shot == 7; self.gen.card.keyframe_insert("hide_render", frame=f)
            for a, key, xy in self.wk:
                C.place(a, f, xy)
                a.card.hide_render = shot != 7; a.card.keyframe_insert("hide_render", frame=f)
        jobs = [(self.lin, PPD[shot])]
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.lin.pose(f, pose_stir(g, calm=0.0 if shot == 5 else 1.0), camera=self.cam)
            if shot != 7:
                self.gen.pose(f, pose_gen_a(g) if shot == 5 else pose_gen_b(g), camera=self.cam)
            else:
                for a, key, xy in self.wk:
                    a.pose(f, pose_worker(a.name, key, g), camera=self.cam)
        if shot != 7:
            jobs.append((self.gen, PPD[shot]))
        else:
            jobs += [(a, PPD[shot]) for a, k, xy in self.wk]
        self.sprites_for(jobs, [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
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
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
