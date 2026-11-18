#!/usr/bin/env python3
"""c10.py -- helpers for the film-10 take scripts (copy of film8/common.py switched to cast10 + set3d10/harbour.py).
Import FIRST in a shot script.  C.H = the harbour set module.  NO depth of field.  H.clear_keys() keeps the drivers (bob, gulls).
Key every animated hook on every rendered frame.  One location + light per process (Take does read_factory_settings)."""
import math, os, sys, json, time
HERE0 = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE0))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast10"), os.path.join(V3, "stage"), os.path.join(V3, "set3d10"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast10                                           # noqa: E402  (before sprites)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import harbour as H                                     # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402,F401

N_FILM = 1815


def g_of(t):
    """narration time t (s) -> film frame of an event (narration at +0.10 s)."""
    return int(round((t + 0.10) * 30))


def g_bound(t):
    """plan boundary t -> film frame round(t*30)."""
    return int(round(t * 30))


def bf(shot, g):
    """Blender frame of (shot id, film frame g): each shot id owns a 1000-frame block."""
    return 1000 * (shot - 1) + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def make_actor(name, cast, sprite_dir, canvas=None, contact=True, shadow="proxy"):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = False
    H.no_bounce(a.card)
    return a


def place(actor, f, xy, z=0.0, scale=1.0):
    actor.place(f, (float(xy[0]), float(xy[1]), float(z)), scale=scale)


class Take(object):
    """harbour / sea preset in a fresh scene, custom camera (DOF off), final render settings."""

    def __init__(self, preset, light=None, quality="preview", lens=22.0, name="cam_take", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.preset = preset
        self.A = H.build(None, preset, light=light)
        H.clear_keys()
        H.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 9000
        self.cam = H.make_camera(dict(loc=(0, 0, 5), look_at=(0, 10, 5), lens=lens), name=name)
        self.cam.data.dof.use_dof = False
        scene.camera = self.cam
        self.actors = {}
        self.anch = {}
        if verbose:
            print("take: built %s %s in %.1f s" % (preset, light, time.time() - t0), flush=True)

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
        self.cam.data.dof.use_dof = False
        self.scene.cycles.samples = samples
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False)


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
    """raw/s<id>/g_%04d.png + .json, resumable (skips frames done with the same scale / samples)."""
    Tk = None
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
        if Tk is None:
            Tk = make_take(quality)
        Tk.pose(shot, todo)
        for g in todo:
            st = Tk.render(shot, [g], out, scale=scale, samples=samples, threads=threads)[0]
            png = os.path.join(out, "g_%04d.png" % g)
            os.replace(st["path"], png)
            rep = Tk.report(shot, g)
            rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
            json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
            print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
