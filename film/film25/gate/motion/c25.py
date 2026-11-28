#!/usr/bin/env python3
"""c25.py -- film-25 shot helpers (adapted from v3/film24/common.py for set3d25 / set25 + cast25).  Import it FIRST:

    import c25 as C        # sets sys.path, imports cast25 (before sprites), bpy, set25, stage modules

GOTCHAS (film24 list, re-checked for set25):
  * RENDER = the set's own final: F.setup_render(scene, 'final') (64 adaptive samples, thr 0.012, OIDN accurate albedo+normal,
    Standard view -0.25 EV, 720x1280 native) then F.post(raw, out) (unsharp + clarity + grade()).  Never deliver raw frames.
    Drafts: Take.render(..., scale=0.4, samples=12): post() still upscales to 720x1280.
  * SUN IS AIMED PER CAMERA (front.finish: from the camera's left, 28 deg).  Several shots in one build: key the sun on every
    frame (Take.key_sun, CONSTANT) for that shot's camera.  Puppets: light25 = -1 (key from screen-left) matches it.
  * KEYS: key every animated thing on EVERY rendered frame (camera, sun, actor place/pose).  Keys are CONSTANT: the smooth
    spline is evaluated in Python per frame, so Blender never interpolates anything.
  * Actor roots carry no rotation (actors.Actor.sync writes the card basis).  Contact decal = Actor(contact=...) on the
    heightfield height F.gh(x, y) (the stage decal; keep it even when the feet are off frame).
  * CARD SIZE: px_per_D * canvas must be whole pixels (multiples of 16).
  * One location per process (build() resets the scene).  Never edit set or cast modules: dress at runtime.
"""
import math, os, sys, json, time

GATE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # film25/gate
PROJ = os.path.dirname(os.path.dirname(GATE))                         # film/
V3 = os.path.join(PROJ, "v3")
for p in (os.path.join(V3, "cast25"), os.path.join(V3, "stage"), os.path.join(V3, "set3d25")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast25                                            # noqa: E402  (FIRST: registers the film-25 cast before sprites)
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402
import set25 as W                                        # noqa: E402
import front as F                                        # noqa: E402
import actors, camrig, render, sprites                   # noqa: E402

NARRATION = os.path.join(PROJ, "film25", "audio", "narration.wav")
CAPTIONS = os.path.join(PROJ, "film25", "script", "captions.json")
FPS = 30


def g_bound(t):
    return int(round(t * FPS))


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def smooth(u):                       # smootherstep (C2 ends)
    u = clamp(u)
    return u * u * u * (u * (6.0 * u - 15.0) + 10.0)


def calm(u):                         # calm move: never freezes at the ends (film-8 rule)
    u = clamp(u)
    return 0.35 * (0.5 - 0.5 * math.cos(math.pi * u)) + 0.65 * u


def out_cubic(u):
    u = clamp(u)
    return 1.0 - (1.0 - u) ** 3


def audio_level():
    """per-frame narration loudness 0..1 (RMS of the 1/30 s window, normalised to the 95th percentile) -> talk_mouth level"""
    import wave
    import numpy as np
    w = wave.open(NARRATION)
    sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
    a = np.frombuffer(w.readframes(n), dtype={2: np.int16, 4: np.int32}[sw]).astype(np.float32)
    a = a.reshape(-1, ch).mean(1)
    hop = sr // FPS
    rms = np.array([float(np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9)) for i in range(len(a) // hop)])
    ref = np.percentile(rms, 95)
    return [float(clamp(r / ref * 1.2)) for r in rms]


class Take(object):
    """one set25 preset in a fresh scene, its own camera keyed per frame, the set's final render + post()."""

    def __init__(self, preset, verbose=True):
        t0 = time.time()
        self.A = W.build(preset)
        self.scene = bpy.context.scene
        self.cam = self.scene.camera
        self.scene.frame_start, self.scene.frame_end = 1, 9000
        self.actors = {}
        self.anch = {}
        if verbose:
            print("take: built %s in %.1f s" % (preset, time.time() - t0), flush=True)

    def key_cam(self, f, loc, look, lens, roll=0.0):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, roll=roll, interp="CONSTANT")

    def aim_sun(self, loc, look):
        """aim the key sun from the left of this camera (front.finish rule).  Called per frame from on_frame (not keyed)."""
        az, el = F.sun_for_camera(dict(loc=tuple(loc), look_at=tuple(look)), F.S.get("sun_elev", 28.0))
        F.set_sun(az, el)

    def on_frame(self, f):
        """per-frame hook before each render (override): aim the sun etc."""
        pass

    def make_actor(self, name, cast, sprite_dir, canvas=None, contact=True):
        a = actors.Actor(name, cast)
        a.build(canvas or cast25.CANVAS25[cast], sprite_dir, contact=contact, shadow="proxy")
        a.head_flip = False
        F.T.no_bounce(a.card)
        self.actors[name] = a
        return a

    def sprites_for(self, jobs, frames):
        for a, ppd in jobs:
            fs = [f for f in frames if f in a.poses]
            for f, r in zip(fs, a.render_sprites(ppd, frames=fs)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("take: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def render(self, frames, out_dir, scale=1.0, samples=None, threads=2, keep_raw=True):
        """the set's final: Cycles at `scale` (1.0 = native 720x1280), then F.post (sharpen, clarity, grade) -> out_dir/g_%04d.png"""
        F.setup_render(self.scene, "final")
        if samples:
            self.scene.cycles.samples = int(samples)
        raw_dir = os.path.join(out_dir, "raw")
        stats = render.render_frames(list(frames), raw_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam,
                                     on_frame=self.on_frame, verbose=False)
        for st in stats:
            t0 = time.time()
            dst = os.path.join(out_dir, "g_%04d.png" % st["frame"])
            F.post(st["path"], dst)
            if not keep_raw:
                os.remove(st["path"])
            st["path"] = dst
            st["wall"] += time.time() - t0
        return stats


def head_report(take, f, radius=0.5):
    """{actor: dict(x, y, w)} head centre / width in px (720x1280) at Blender frame f"""
    out = {}
    take.scene.frame_set(f)
    for a in take.actors.values():
        if a.card.hide_render or (a.name, f) not in take.anch:
            continue
        res = a.feet.get(f)
        hx, hy = take.anch[(a.name, f)]["head"]
        c = actors.local_to_screen(a, take.cam, (hx, hy), f, res)
        l = actors.local_to_screen(a, take.cam, (hx - radius, hy), f, res)
        r = actors.local_to_screen(a, take.cam, (hx + radius, hy), f, res)
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
    return out


def feet_report(take, f):
    out = {}
    for a in take.actors.values():
        if a.card.hide_render:
            continue
        p = actors.local_to_screen(a, take.cam, a.feet_at(f), f)
        out[a.name] = (round(p[0], 1), round(p[1], 1))
    return out


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out
