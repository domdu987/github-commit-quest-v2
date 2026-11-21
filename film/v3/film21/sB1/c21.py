#!/usr/bin/env python3
"""c21.py -- helper module of film-21 take s02 (shots 4-7).  Copy of the film8/common.py idea for cast21 + set3d21/stirling.py.

    import c21 as C          # sets sys.path, imports cast21 BEFORE the stage sprites, bpy, stirling (K), the stage modules

What is here
  clock        g_of(t) (narration t -> film frame), bf(g) (blender frame = g + 1)
  Take         one stirling preset in a fresh scene + one stage camera (22 mm, no DoF) + cast cards (stage Actors)
  cards        add_actor(), place_card(): the cast cards stand in the set; 1 head D = SC metres (0.535 -> a scot is 1.70 m)
  gamma        K.grade() applies gamma 1.28 to the whole frame; the card emission is pre-compensated (power 1/1.28) so the cast keeps its drawn colours
  render       Take.render_frame(): frame_set, actors.sync_all, bpy render, K.grade()
"""
import math, os, sys, json, time

FILM = os.path.dirname(os.path.abspath(__file__))          # film/v3/film21/s02
V3 = os.path.dirname(os.path.dirname(FILM))                # film/v3
PROJ = os.path.dirname(V3)                                 # film
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                              # noqa: E402  (before sprites: canvases reach sprites.DEFAULT_CANVAS)
import numpy as np                                         # noqa: E402
import bpy                                                 # noqa: E402
from mathutils import Vector                               # noqa: E402
import stirling as K                                       # noqa: E402
import actors, camrig, sprites                             # noqa: E402

SC = 1.7 / 3.18            # metres per head-D: a scot (3.18 D head-top to soles) is 1.70 m
CAPTIONS = os.path.join(PROJ, "film21", "script", "captions.json")


def g_of(t):
    return int(round((t + 0.10) * 30))


def bf(g):
    return int(g) + 1


def lerp(a, b, u):
    return a + (b - a) * u


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def sine(u):
    u = clamp(u)
    return 0.5 - 0.5 * math.cos(math.pi * u)


def mixu(u, k=0.35):
    """mostly linear ease (no dead ends): k sine + (1 - k) linear."""
    u = clamp(u)
    return k * sine(u) + (1 - k) * u


def snap_u(u, peak=1.0):
    """smootherstep for snaps."""
    u = clamp(u)
    return u * u * u * (u * (u * 6 - 15) + 10)


def blink_at(g, period=96, offset=0):
    return cast21.blink_at(g, period, offset)


def vl(a, b, u):
    return tuple(lerp(a[i], b[i], u) for i in range(3))


def aim(loc, az, el, d=30.0):
    a, e = math.radians(az), math.radians(el)
    return tuple(loc[i] + d * v for i, v in enumerate((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))))


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, preset, quality="final", samples=24, threads=2, fg=True, verbose=True):
        t0 = time.time()
        self.preset = preset
        self.pr = K.PRESETS[preset]
        self.A = K.build_for_cli(preset, placeholders=False)
        sc = self.scene = bpy.context.scene
        self.quality, self.samples = quality, samples
        K.setup_render(sc, quality, samples)
        sc.render.threads_mode = "FIXED"
        sc.render.threads = threads
        sc.render.use_persistent_data = False
        sc.cycles.denoising_prefilter = "FAST"
        sc.frame_start, sc.frame_end = 1, 9000
        for o in list(bpy.data.objects):                    # the set's own camera is replaced by the stage camera
            if o.type == "CAMERA":
                bpy.data.objects.remove(o)
        self.cam = camrig.make_camera(sc, name="cam_s02", lens=self.pr.get("lens", 22.0))
        self.cam.data.clip_start = 0.05
        self.cam.data.clip_end = 9000.0
        self.cam.data.dof.use_dof = False
        K.setup_render(sc, quality, samples)                # make_camera resets 720x1280
        sc.render.threads_mode = "FIXED"; sc.render.threads = threads
        self.actors = {}
        self.sprite_dir = os.path.join(FILM, "work", "sprites_%s" % preset)
        self.res = {}
        if verbose:
            print("take: built %s in %.1f s" % (preset, time.time() - t0), flush=True)

    # -- scene dressing helpers
    def hide(self, prefixes):
        n = 0
        for o in bpy.data.objects:
            if any(o.name.startswith(p) for p in prefixes):
                o.hide_render = True; o.hide_viewport = True; n += 1
        return n

    def ground(self, x, y):
        return float(K.ground(x, y))

    # -- actors
    def add_actor(self, name, cast, shadow="proxy", contact=True):
        a = actors.Actor(name, cast)
        a.build(sprites.DEFAULT_CANVAS[cast], self.sprite_dir, contact=contact, shadow=shadow)
        a.head_flip = False
        _compensate(a)
        self.actors[name] = a
        return a

    def key_cam(self, f, loc, look, lens=None, roll=0.0):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, roll=roll, interp="LINEAR", easing="AUTO")

    def render_sprites(self, frames, ppd=256):
        """rasterise the stored poses of every actor for the given blender frames."""
        for a in self.actors.values():
            fr = [f for f in frames if f in a.poses]
            if not fr:
                continue
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.res[(a.name, f)] = r
                if r.get("clipped"):
                    print("take: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def head_px(self, name, f):
        a = self.actors[name]
        self.scene.frame_set(f)
        bpy.context.view_layer.update()
        r = self.res.get((name, f))
        if not r:
            return None
        hx, hy = r["anchors"]["head"]
        feet = a.feet.get(f) if hasattr(a, "feet") else None
        c = actors.local_to_screen(a, self.cam, (hx, hy), f, feet)
        k = 720.0 / self.scene.render.resolution_x
        return round(c[0] * k, 1), round(c[1] * k, 1), round(c[2], 1)

    def render_frame(self, g, out_png):
        f = bf(g)
        sc = self.scene
        sc.frame_set(f)
        for name in self.cam.keys() if False else []:
            pass
        actors.sync_all(sc, self.cam)
        sc.camera = self.cam
        sc.render.filepath = out_png
        pct = int(os.environ.get('PCT', '100'))
        sc.render.resolution_percentage = pct
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        dt = time.time() - t0
        if pct == 100:
            K.grade(out_png)
        return dt


def _compensate(a, gamma=1.28):
    """K.grade() raises the whole frame to ^1.28: pre-compensate the card emission (power 1/1.28 on the linear colour, about the same in display space)
    so the drawn cast keeps its colours (head #fef7f6, ink #3a2832)."""
    for m in (a.card.active_material, ) if a.card and a.card.active_material else []:
        nt = m.node_tree
        emi = [n for n in nt.nodes if n.bl_idname == "ShaderNodeEmission"]
        for e in emi:
            lk = [l for l in nt.links if l.to_socket == e.inputs["Color"]]
            if not lk:
                continue
            src = lk[0].from_socket
            gm = nt.nodes.new("ShaderNodeGamma")
            gm.inputs["Gamma"].default_value = 1.0 / gamma
            nt.links.new(src, gm.inputs["Color"])
            nt.links.new(gm.outputs["Color"], e.inputs["Color"])


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out
