"""c21.py -- helpers for film 21 travel segments (set3d21/stirling.py K + cast21 + v3/stage).  Own copy per take folder."""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                           # noqa: E402  BEFORE sprites / actors
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import numpy as np                                      # noqa: E402
from PIL import Image, ImageDraw                        # noqa: E402
import stirling as K                                    # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402

CARD_H = dict(cressingham=3.23, surrey=3.20, knight_b=3.38, knight_b_great=3.38, footman_a=3.04, footman_b=3.24,
              scot_a=3.18, scot_b=3.36, scot_c=3.07, wallace=3.59)
WORLD_H = dict(cressingham=1.78, surrey=1.66, knight_b=1.78, knight_b_great=1.78, footman_a=1.68, footman_b=1.68,
               scot_a=1.70, scot_b=1.70, scot_c=1.70, wallace=1.92)


def unit_scale(cast):
    return WORLD_H[cast] / CARD_H[cast]


def g_of(t):
    return int(round((t + 0.10) * 30))


def ez(u):
    u = max(0.0, min(1.0, u)); return 0.5 - 0.5 * math.cos(math.pi * u)


def lerp(a, b, u):
    return a + (b - a) * u


def blink(g, starts):
    return any(0 <= g - s < 3 for s in starts)


def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if len(a) > 1 else a
    return out


class Take(object):
    """world presets + cast.  cast = [(name, cast_key)].  cam_fn(g) -> dict(loc, look, lens, vivid); act_fn(g) -> {name: (xyz, pose)}.
    post_fn(g, path) optional image post (whip blur, speed lines).  g0 = frame whose Blender frame is 1."""

    def __init__(self, presets, cast, cam_fn, act_fn, g0, work, post_fn=None, fg=True, hide=()):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.A = K.build_world(presets, fg=fg, hide=hide)
        self.cam = bpy.context.scene.camera
        self.cam.data.dof.use_dof = False
        self.cam.data.clip_start = 0.1
        K.setup_render(bpy.context.scene, "final")
        self.cam_fn, self.act_fn, self.g0, self.work, self.post_fn = cam_fn, act_fn, g0, work, post_fn
        self.acts = {}
        self.cast = dict(cast)
        for nm, cst in cast:
            a = actors.Actor(nm, cst)
            a.build(sprites.DEFAULT_CANVAS[cst], os.path.join(work, "sprites"), contact=True)
            a.head_flip = False
            self.acts[nm] = a
        self.vivid = {}

    def f(self, g):
        return g - self.g0 + 1

    def pose(self, gs):
        for g in gs:
            f = self.f(g); c = self.cam_fn(g); self.vivid[g] = c["vivid"]
            camrig.key_camera(f, c["loc"], c["look"], lens=c["lens"], cam=self.cam, interp="LINEAR", easing="AUTO")
            for nm, (xyz, p) in self.act_fn(g).items():
                self.acts[nm].place(f, tuple(xyz), scale=unit_scale(self.cast[nm]))
        for g in gs:
            f = self.f(g); bpy.context.scene.frame_set(f)
            for nm, (xyz, p) in self.act_fn(g).items():
                self.acts[nm].pose(f, K.with_rim(p), camera=self.cam)
        for nm, a in self.acts.items():
            a.render_sprites(256, frames=[self.f(g) for g in gs])

    def render(self, g, out_dir, scale=1.0, samples=32):
        sc = bpy.context.scene
        K.set_flutter(g / 30.0); K.set_smoke(g / 30.0); K.set_flow(g / 30.0)
        K.setup_render(sc, "final", samples); sc.render.threads_mode = "FIXED"; sc.render.threads = 2
        K.STATE["vivid"] = self.vivid[g]
        st = render.render_frames([self.f(g)], out_dir, scale=scale, scene=sc, camera=self.cam, verbose=False)[0]
        K.grade(st["path"], scale=scale)
        if self.post_fn:
            self.post_fn(g, st["path"])
        return st

    def main(self, argv, rng):
        cmd = argv[1]; gs = [g for g in parse(argv[2]) if rng[0] <= g <= rng[1]]
        if cmd == "stills":
            out = argv[3]; scale = float(argv[4]) if len(argv) > 4 else 0.5; samples = int(argv[5]) if len(argv) > 5 else 8
            os.makedirs(out, exist_ok=True); todo = gs
        else:
            scale = float(argv[3]) if len(argv) > 3 else 1.0; samples = int(argv[4]) if len(argv) > 4 else 32
            out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
            todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        print("%s: %d to render" % (cmd, len(todo)), flush=True)
        if not todo:
            return
        self.pose(todo)
        for g in todo:
            t0 = time.time(); st = self.render(g, os.path.join(self.work, "tmp"), scale=scale, samples=samples)
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("g", g, round(time.time() - t0, 1), "s", flush=True)


def motion_blur_h(path, k):
    import cv2
    if k < 2:
        return
    im = cv2.imread(path); im = cv2.blur(im, (int(k), 1)); cv2.imwrite(path, im)


def speed_lines(path, strength=1.0, seed=0, n=70):
    """white radial speed lines from the frame centre outward (snap punch-in)."""
    im = Image.open(path).convert("RGB"); w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    rs = np.random.RandomState(seed); cx, cy = w / 2, h * 0.5
    for i in range(n):
        a = rs.uniform(0, 2 * math.pi); r0 = rs.uniform(0.35, 0.75) * h * 0.5; r1 = r0 + rs.uniform(0.15, 0.5) * h
        wd = rs.uniform(0.004, 0.012) * w
        p0 = (cx + r0 * math.cos(a), cy + r0 * math.sin(a)); p1 = (cx + r1 * math.cos(a), cy + r1 * math.sin(a))
        nx, ny = -math.sin(a) * wd, math.cos(a) * wd
        d.polygon([p0, (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny)], fill=(255, 255, 255, int(150 * strength)))
    Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB").save(path)
