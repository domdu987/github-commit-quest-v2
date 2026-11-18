#!/usr/bin/env python3
"""c11.py -- helpers of the film-11 take scripts (copy of film8/common.py switched to cast11 + set3d11/dairy.py).
Import FIRST in a shot script:  HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import c11 as C
Notes:
  * Blender frame of (shot, g) = 1000 * (shot - 1) + g + 1 (bf).  The dairy hooks are drivers on `frame`: every rendered frame is alive.
  * One location per process (Take does read_factory_settings).
  * Cards: Actor per figure (cast11 canvases), scale = set height / cast height (SCALE), placed on the set's stand points.
"""
import math, os, sys, json, time, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast11"), os.path.join(V3, "stage"), os.path.join(V3, "set3d11"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast11                                           # noqa: E402  (BEFORE sprites)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import dairy as D                                       # noqa: E402
import mine as MN                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, lerp, clamp, blink                      # noqa: E402,F401

NARRATION = os.path.join(PROJ, "film11", "audio", "narration.wav")
CAPTIONS = os.path.join(PROJ, "film11", "script", "captions.json")
N_FILM = 1875

# set height (D) / cast height (head top to soles, no hat) -> card scale
SET_H = dict(jenner=3.3, james=2.3, sarah=3.1, milkmaid2=3.1, towndoc=3.4, mother=3.1, villager_a=3.2, villager_b=3.2, villager_c=3.2,
             villager_d=3.2, villager_e=3.2)
CAST_H = dict(jenner=3.12, james=2.34, sarah=2.92, milkmaid2=2.96, towndoc=3.25, mother=2.92, villager_a=3.00, villager_b=2.94,
              villager_c=2.81, villager_d=3.16, villager_e=2.80)
SCALE = {k: SET_H[k] / CAST_H[k] for k in SET_H}


def g_of(t):
    """narration time t (s) -> film frame of an in-shot event (+0.10 s)."""
    return int(round((t + 0.10) * 30))


def g_bound(t):
    """shot-plan boundary -> film frame round(t * 30)."""
    return int(round(t * 30))


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def captions():
    return json.load(open(CAPTIONS))


def make_actor(name, cast, sprite_dir, canvas=None, contact=True, shadow="proxy"):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = False
    D.no_bounce(a.card)
    return a


def place(actor, f, xy, z=0.0, scale=1.0, flip=False):
    actor.place(f, (float(xy[0]), float(xy[1]), float(z)), scale=scale, flip=flip)


def key_hidden(actor, f, hidden):
    """show / hide a whole Actor (card, shadow proxy, contact decal) at Blender frame f (constant keys, set it on every rendered frame)."""
    for o in actor.objects():
        o.hide_render = bool(hidden)
        o.keyframe_insert("hide_render", frame=f)
        try:
            for fc in o.animation_data.action.fcurves if hasattr(o.animation_data.action, "fcurves") else camrig.fcurves_of(o):
                if fc.data_path == "hide_render":
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"
        except Exception:
            pass


def sore_svg(anchor, kind="blister", r=0.11):
    """the vaccination sore as an SVG fragment (puppet-local D) centred on `anchor`: kind 'dot' (red dot) or 'blister' (pale blister, red ring)."""
    x, y = anchor
    if kind == "dot":
        return ('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#d83a3a" stroke="#8a1c24" stroke-width="0.012"/>' % (x, y, r * 0.45))
    return ('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#e8564f" opacity="0.85"/>'
            '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#f7e9c4" stroke="#b02a30" stroke-width="0.014"/>'
            '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#fffaf0" opacity="0.8"/>' % (x, y, r, x, y, r * 0.66, x - r * 0.2, y - r * 0.22, r * 0.2))


class Take(object):
    """One dairy preset in a fresh scene with one custom camera (no DOF), 12 samples (final) / 6 (preview)."""

    def __init__(self, preset, light=None, quality="preview", lens=22.0, name="cam_take", threads=2, verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.preset = preset
        self.A = D.build(preset, light=light)
        MN.setup_render(scene, quality)
        scene.render.threads_mode = "FIXED"; scene.render.threads = threads
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 20000
        self.cam = camrig.make_camera(scene, name=name, lens=lens)
        self.cam.data.clip_start = 0.05
        self.cam.data.clip_end = 4000
        self.no_dof()
        for h in self.A['hooks']:                       # director note 2026-11-18: no blob-stack smoke -> hide the chimney smoke
            if h['kind'] == 'smoke' and bpy.data.objects.get(h['obj']) is not None:
                bpy.data.objects[h['obj']].hide_render = True
        self.actors = {}
        self.anch = {}
        self.quality = quality
        if verbose:
            print("take: built %s in %.1f s" % (preset, time.time() - t0), flush=True)

    def no_dof(self):
        self.cam.data.dof.use_dof = False

    def key_cam(self, f, loc, look, lens=None):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")

    def hide_set_objects(self, names):
        for n in names:
            o = bpy.data.objects.get(n)
            if o is not None:
                o.hide_render = True

    def sprites_for(self, jobs, frames, overlays=None):
        """jobs = [(actor, px_per_D)]; remember the anchors per (actor name, frame).  overlays {actor name: callable(f, pose, anchors)->svg}:
        a second pass redraws the sprites with the overlay at an anchor found in the first pass."""
        for a, ppd in jobs:
            res = a.render_sprites(ppd, frames=frames)
            for f, r in zip(frames, res):
                self.anch[(a.name, f)] = r["anchors"]
            ov = (overlays or {}).get(a.name)
            if ov is not None:
                res = a.render_sprites(ppd, frames=frames, overlay=lambda f, pose, a=a, ov=ov: ov(f, pose, self.anch[(a.name, f)]))
                for f, r in zip(frames, res):
                    self.anch[(a.name, f)] = r["anchors"]
            for f, r in zip(frames, res):
                if r.get("clipped"):
                    print("take: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def render(self, frames, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam
        self.no_dof()
        self.scene.cycles.samples = samples
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False)


def head_report(take, f, radius=0.5):
    """{actor: dict(x, y, w, chin)} screen px of every visible actor's head at Blender frame f."""
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
        w = math.hypot(r[0] - l[0], r[1] - l[1])
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(w, 1), chin=round(c[1] + w / 2, 1))
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
    """raw/s<id>/g_%04d.png + .json (report, wall, cpu); resumable."""
    cache = {}
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
        if "T" not in cache:
            cache["T"] = make_take(quality)
        Tk = cache["T"]
        Tk.pose(shot, todo)
        for g in todo:
            st = Tk.render(shot, [g], out, scale=scale, samples=samples, threads=threads)[0]
            png = os.path.join(out, "g_%04d.png" % g)
            os.replace(st["path"], png)
            rep = Tk.report(shot, g)
            rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
            json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
            print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
