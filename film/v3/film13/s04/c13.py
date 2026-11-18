#!/usr/bin/env python3
"""c13.py -- helpers for the film-13 take scripts (copied from film8/common.py, switched to cast13 + set3d13/chicago.py).
Import FIRST:  HERE = ...; sys.path.insert(0, HERE); import c13 as C
C.B = the chicago set module; C.Take(preset, light, state) builds ONE location per process (street here), makes one custom camera
(NO depth of field), swaps the placeholder roles of the set for real cast13 cards (C.use_cast13()).
GOTCHAS: key EVERY animated hook on EVERY rendered frame (clear_keys() after build); moves must move (never static > 6 frames)."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast13"), os.path.join(V3, "stage"), os.path.join(V3, "set3d13"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast13                                           # noqa: E402  (before sprites)
import puppet                                           # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import chicago as B                                     # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402,F401

N_FILM = 1995
CAPTIONS = os.path.join(PROJ, "film13", "script", "captions.json")


def g_of(t):
    """narration time t (s) -> film frame of an event (narration at +0.10 s)."""
    return int(round((t + 0.10) * 30))


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def make_actor(name, cast, sprite_dir, canvas=None, contact=True, shadow="proxy"):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = False
    B.no_bounce(a.card)
    return a


def place(actor, f, xy, z=0.0, scale=1.0):
    actor.place(f, (float(xy[0]), float(xy[1]), float(z)), scale=scale)


def use_cast13():
    """crowd / placeholder roles of chicago.py -> real cast13 cards (static poses, true heights incl. hat)."""
    S = cast13.STORY13
    def P(name, h):
        c, p = S[name]; return (c, dict(p), h)
    B.T.PH.update(
        worker=P("worker_stand_a", 3.33), foreman=P("foreman_stand", 3.53), rich=P("rich_look_window_smug", 3.91),
        maid=P("lady_stand", 3.22), clerk=P("gentleman_stand", 3.48), kid=P("town_stand_c", 2.56),
        towns_m=P("town_stand_a", 3.30), towns_f=P("town_stand_b", 3.22), towns_o=P("worker_stand_b", 3.30))


def head_report(take, f, radius=0.5):
    out = {}
    take.scene.frame_set(f)
    for a in take.actors.values():
        if a.card.hide_render or (a.name, f) not in take.anch:
            continue
        res = a.feet.get(f)
        hx, hy = take.anch[(a.name, f)]["head"]
        c = actors.local_to_screen(a, take.cam, (hx, hy), f, res)
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1))
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


def look_at_cam(cam, loc, look):
    """set cam transform directly (used to place crowds before animation)."""
    d = Vector(look) - Vector(loc)
    cam.location = Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()


class Take(object):
    def __init__(self, preset, light=None, state=None, quality="preview", lens=22.0, name="cam_take"):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        use_cast13()
        self.A = B.build(preset, light=light, state=state)
        B.clear_keys()
        B.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 9000
        self.cam = camrig.make_camera(scene, name=name, lens=lens)
        self.cam.data.clip_start = 0.05
        self.cam.data.clip_end = 6000
        self.no_dof()
        self.actors, self.anch = {}, {}
        self.preset = preset
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


def final_loop(take, shot_of, ranges_g, here, scale=1.0, samples=12, threads=2):
    """ranges_g: list of g to render (already filtered). Writes raw/g_%04d.png + .json, resumable."""
    out = os.path.join(here, "raw"); os.makedirs(out, exist_ok=True)
    todo = []
    for g in ranges_g:
        png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
        ok = os.path.exists(png) and os.path.exists(js)
        if ok:
            m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
        if not ok:
            todo.append(g)
    print("final: %d to render, %d done" % (len(todo), len(ranges_g) - len(todo)), flush=True)
    if not todo:
        return
    take.pose(todo)
    for g in todo:
        st = take.render(g, out, scale=scale, samples=samples, threads=threads)
        png = os.path.join(out, "g_%04d.png" % g)
        os.replace(st["path"], png)
        rep = take.report(g)
        rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
        json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
        print("g %d  %.1f s wall  %.1f s cpu" % (g, st["wall"], st["cpu"]), flush=True)
