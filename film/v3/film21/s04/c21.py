#!/usr/bin/env python3
"""c21.py -- helper for film 21 take s04 (adapted from film8/common.py): cast21 cards in the Stirling set (set3d21/stirling.py).
One preset per process. Per frame: key camera + actors, set hooks, sync cards, render, grade (VIVID of the preset)."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE)); PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                            # noqa: E402  (BEFORE sprites)
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402
import stirling as K                                     # noqa: E402
import actors, camrig, render, sprites                   # noqa: E402
from anim import ease, blink, lerp, clamp                # noqa: E402,F401

# world scale of a card: height in the set / puppet height in head-D (cast21 table)
SCALE = {"cressingham": 1.78 / 3.23, "surrey": 1.66 / 3.20, "knight_a": 1.78 / 3.26, "knight_b": 1.78 / 3.38,
         "footman_a": 1.68 / 3.04, "footman_b": 1.68 / 3.24}


def g_of(t):
    return int(round((t + 0.10) * 30))


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def smooth(u):
    return u * u * (3 - 2 * u)


def path(g, wps, mix=0.5):
    """camera waypoints [(g, loc, look)] -> (loc, look) at g; per segment u = mix*sine + (1-mix)*linear (never dead-still)."""
    if g <= wps[0][0]:
        return Vector(wps[0][1]), Vector(wps[0][2])
    for (g0, l0, k0), (g1, l1, k1) in zip(wps, wps[1:]):
        if g <= g1:
            x = (g - g0) / float(g1 - g0)
            u = mix * ez(x, "sine") + (1 - mix) * x
            return (Vector([lerp(a, b, u) for a, b in zip(l0, l1)]), Vector([lerp(a, b, u) for a, b in zip(k0, k1)]))
    return Vector(wps[-1][1]), Vector(wps[-1][2])


class Take21(object):
    def __init__(self, preset, tmp, quality="final", samples=24):
        self.preset = preset
        self.A = K.build_for_cli(preset, placeholders=False)
        K.STATE["preset"] = preset
        self.scene = bpy.context.scene
        self.cam = self.scene.camera
        self.cam.rotation_mode = "XYZ"
        self.cam.data.clip_start = 0.02
        self.cam.data.dof.use_dof = False
        self.lens = K.PRESETS[preset].get("lens", 22.0)
        K.setup_render(self.scene, quality, samples)
        self.scene.cycles.samples = samples
        self.scene.render.threads = int(os.environ.get('THREADS', '4'))
        self.scene.render.use_persistent_data = False
        self.scene.frame_start, self.scene.frame_end = 1, 9000
        self.tmp = tmp
        self.actors, self.anch, self.cfg = {}, {}, {}

    def add(self, name, cast, contact=True):
        a = actors.Actor(name, cast)
        a.build(sprites.DEFAULT_CANVAS[cast], os.path.join(self.tmp, "sprites"), contact=contact)
        a.head_flip = False
        self.actors[name] = a
        return a

    def key_cam(self, g, loc, look):
        camrig.key_camera(g, Vector(loc), Vector(look), cam=self.cam, lens=self.lens, interp="LINEAR", easing="AUTO")

    def place(self, a, g, xyz, scale, flip=False):
        a.place(g, tuple(float(v) for v in xyz), scale=scale, flip=flip, interp="LINEAR")

    def hide(self, a, g, hidden):
        a.card.hide_render = hidden
        a.card.keyframe_insert("hide_render", frame=g)
        for o in (a.proxy, a.contact):
            if o is not None:
                o.hide_render = hidden
                o.keyframe_insert("hide_render", frame=g)

    def poses(self, jobs, gs, ppd=256):
        """jobs [(actor, {g: pose})]: store poses, rasterise sprites."""
        for g in gs:
            self.scene.frame_set(g)
            for a, pf in jobs:
                a.pose(g, pf(g), camera=self.cam)
        for a, _ in jobs:
            for g, r in zip(gs, a.render_sprites(ppd, frames=gs)):
                self.anch[(a.name, g)] = r["anchors"]
                if r.get("clipped"):
                    print("WARNING sprite %s clipped g %d" % (a.name, g), flush=True)

    def render(self, gs, out_dir, on_frame):
        os.makedirs(out_dir, exist_ok=True)
        st = render.render_frames(list(gs), out_dir, scale=1.0, scene=self.scene, camera=self.cam, on_frame=on_frame, verbose=False)
        for s in st:
            K.grade(s["path"])
        return st

    def heads(self, g, radius=0.5):
        out = {}
        self.scene.frame_set(g)
        for a in self.actors.values():
            if a.card.hide_render or (a.name, g) not in self.anch:
                continue
            res = a.feet.get(g)
            hx, hy = self.anch[(a.name, g)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), g, res)
            l = actors.local_to_screen(a, self.cam, (hx - radius, hy), g, res)
            r = actors.local_to_screen(a, self.cam, (hx + radius, hy), g, res)
            sc = 1.0 if self.scene.render.resolution_x == 720 else 2.0
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
