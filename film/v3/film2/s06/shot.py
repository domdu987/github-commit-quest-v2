#!/usr/bin/env python3
"""shot.py -- film 2 take s06: shot 6, vault set LANTERN.

    shot 6  g 359..447  12-frame dissolve in (in-handle g 351..358): low dolly along the left barrel rows (dolly_barrels, 3.2 D
                        toward the door), the soldier on guard in front of the barrels; eased reframe onto the soldier at
                        "ทางการเก็บ" (g 388); snap in (g 405..415) onto the crossed-cannon stencil (barrel_insert), slow push on it,
                        "เกือบ 90 ตัน" lands on the insert (g 424).  Out-handle g 448..454 (10-frame dissolve into shot 7).
Blender frame = g + 1.

    python3 shot.py probe 6 a:b:step | stills 6 a:b:step out_dir [scale] [samples] | final 6 a:b [scale] [samples]
"""
import math, os, sys, time, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast2"), os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast2                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import vault as V                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, lerp, clamp         # noqa: E402

_sp = importlib.util.spec_from_file_location("s04shot", os.path.join(os.path.dirname(HERE), "s04", "shot.py"))
S04 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S04)      # shared CLI (probe / stills / final)

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


G_S6, G_S7 = 359, 448
H_IN, H_OUT = 8, 7
RANGES = {6: (G_S6 - H_IN, G_S7 + H_OUT - 1)}
G_KEP = g_of(12.842)                 # 388 "ทางการเก็บ"
G_DIN = g_of(13.398)                 # 405 "ดินปืนไว้"
G_90 = g_of(14.028)                  # 424 "เกือบ 90 ตัน"
SNAP = (G_DIN, G_DIN + 10)           # 405..415


def bf(shot, g):
    return int(g) + 1


SOLDIER = (-1.05, -9.1, 0.0)


def cam6(g, A):
    d0 = A["cams"]["dolly_barrels"]; d1 = d0["move"]; ins = A["cams"]["barrel_insert"]
    a = (Vector(d0["loc"]) + Vector((0.0, 0.25, 0.0)), Vector(d0["look_at"]) + Vector((0.0, 0.2, 0.25)))
    b = (Vector(d0["loc"]).lerp(Vector(d1["loc"]), 0.55), Vector(d0["look_at"]).lerp(Vector(d1["look_at"]), 0.55) + Vector((0.0, 0.0, 0.55)))
    sold_head = Vector((SOLDIER[0], SOLDIER[1], 2.6))
    c_loc = Vector(d1["loc"]) + Vector((0.15, 0.6, 0.12))
    c = (c_loc, sold_head + Vector((0.55, 0.0, -0.3)))
    hc = Vector(ins["look_at"]); il = Vector(ins["loc"])
    e = (hc + (il - hc) * 1.25 + Vector((0.0, 0.02, 0.04)), hc + Vector((0.0, -0.03, 0.03)))
    f = (hc + (il - hc) * 0.98, hc + Vector((0.0, 0.0, 0.0)))
    ks = [(RANGES[6][0], tuple(a[0]) + tuple(a[1]), "sine"),
          (G_KEP - 4, tuple(b[0]) + tuple(b[1]), "sine"),
          (SNAP[0], tuple(c[0]) + tuple(c[1]), "quint"),
          (SNAP[1], tuple(e[0]) + tuple(e[1]), "sine"),
          (RANGES[6][1], tuple(f[0]) + tuple(f[1]), "hold")]
    k = lerp(keys(g, ks), keys(g, [(fr, v, "lin") for fr, v, ee in ks]), 0.25)
    loc, look = Vector(k[:3]), Vector(k[3:])
    look = look + Vector((0.0, 0.0, 0.006 * math.sin(g * 0.37)))      # hand-held breath
    return loc, look


def soldier_pose(g):
    p = dict(cast2.STORY2["soldier_guard"][1])
    p["head_roll"] = -3 + 2.0 * math.sin(g * 0.09)
    p["yaw"] = 0.25 - 0.12 * ease(clamp((g - G_KEP + 6) / 14.0), "sine")    # turns a little toward us on "the authorities"
    p["squash"] = (1.0 + 0.008 * math.sin(g * 0.2), 1.0 - 0.008 * math.sin(g * 0.2))   # breathing
    p["blink"] = blink(g, [366, 397, 436])
    p["gaze"] = (-0.3 + 0.3 * ease(clamp((g - G_KEP + 6) / 14.0), "sine"), 0.0)
    return p


class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = V.build("LANTERN")
        V.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 2000
        self.cam = camrig.make_camera(scene, name="cam_s06")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 100
        sd = os.path.join(TMP, "sprites")
        self.sol = actors.Actor("soldier", "soldier")
        self.sol.build(sprites.DEFAULT_CANVAS["soldier"], sd, contact=True)
        self.sol.head_flip = False                       # lantern key from screen-left
        V.no_bounce(self.sol.card)
        self.anch = {}
        if verbose:
            print("s06: built in %.1f s" % (time.time() - t0), flush=True)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam6(g, self.A)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.sol.place(f, SOLDIER)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.sol.pose(f, soldier_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        for f, r in zip(fr, self.sol.render_sprites(384, frames=fr)):
            self.anch[f] = r["anchors"]

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam6(g, self.A)
        a = self.sol
        res = a.feet.get(f)
        hx, hy = self.anch[f]["head"]
        c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
        l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
        r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
        st = render.world_to_screen(self.cam, tuple(self.A["stencil_insert"]), f)
        return dict(shot=shot, g=g, cam=[round(v, 3) for v in loc],
                    heads={"soldier": dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))},
                    stencil=[round(st[0], 1), round(st[1], 1)])

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.cycles.samples = samples
        return render.render_frames([bf(shot, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False)


if __name__ == "__main__":
    S04.main(sys.argv, Take=Take, RANGES=RANGES, HERE=HERE)
