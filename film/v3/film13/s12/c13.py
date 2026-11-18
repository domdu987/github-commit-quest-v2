#!/usr/bin/env python3
"""c13.py -- helper for film-13 takes (copy of film8/common.py switched to cast13 + set3d13/chicago.py).
GOTCHAS: moves must move; key every animated hook on EVERY rendered frame; one location (street | suite | under) per process.
"""
import math, os, sys, json, time, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast13"), os.path.join(V3, "stage"), os.path.join(V3, "set3d13"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast13                                           # noqa: E402  (before sprites / actors: registers the cast)
import puppet                                           # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import chicago as D                                     # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402,F401

T = D.T
SPEC = os.path.join(PROJ, "film13")
N_FILM = 1995


def g_of(t):
    return int(round((t + 0.10) * 30))


def g_bound(t):
    return int(round(t * 30))


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def make_actor(name, cast, sprite_dir, canvas=None, contact=True, shadow="proxy"):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = False
    D.no_bounce(a.card)
    return a


def place(actor, f, xyz, scale=1.0):
    actor.place(f, (float(xyz[0]), float(xyz[1]), float(xyz[2])), scale=scale)


class Take(object):
    def __init__(self, preset, quality="preview", lens=22.0, name="cam_take", light=None, state=None, verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.preset = preset
        self.A = D.build(preset, light=light, state=state)
        D.clear_keys()
        D.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 9000
        self.cam = camrig.make_camera(scene, name=name, lens=lens)
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 6000
        self.no_dof()
        self.actors = {}
        self.anch = {}
        if verbose:
            print("take: built %s in %.1f s" % (preset, time.time() - t0), flush=True)

    def no_dof(self):
        self.cam.data.dof.use_dof = False

    def key_cam(self, f, loc, look, lens=None):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")

    def sprites_for(self, jobs, frames):
        for a, ppd in jobs:
            for f, r in zip(frames, a.render_sprites(ppd, frames=frames)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("take: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def render(self, frames, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam
        self.no_dof()
        self.scene.cycles.samples = samples
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False)


def head_report(take, f, radius=0.5):
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


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def final_loop(make_take, shots, gs_spec, ranges, here, scale=1.0, samples=12, threads=2, quality="final"):
    T_ = None
    for shot in shots:
        gs = [g for g in parse(gs_spec) if ranges[shot][0] <= g <= ranges[shot][1]]
        out = os.path.join(here, "raw", "s%d" % shot)
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
        if T_ is None:
            T_ = make_take(quality)
        T_.pose(shot, todo)
        for g in todo:
            st = T_.render(shot, [g], out, scale=scale, samples=samples, threads=threads)[0]
            png = os.path.join(out, "g_%04d.png" % g)
            os.replace(st["path"], png)
            rep = T_.report(shot, g)
            rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
            json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
            print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
