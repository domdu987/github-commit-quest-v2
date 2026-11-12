#!/usr/bin/env python3
"""shot.py -- film 2 take s15: shot 15, tower set DUSK -> NIGHT_STORM, town_wide family, no actors, no rod (set_rod(0)).

    g 1151..1247  golden dusk over Brescia; dark storm clouds roll in over the town from behind the tower (north) and the
                  light goes from DUSK to NIGHT_STORM under them; the first warm windows light up one group after another
                  (g 1196 / 1209 / 1222 / 1234); one far sheet-lightning flicker at g 1238 (thunder rumble).
                  Camera: slow eased push and tilt up toward the sky, speed change at "เมฆดำ" (g 1197), small reframe up
                  at "เหนือเมือง" (g 1214..1224).
    12-frame dissolve in (handle g 1143..1150), 10-frame dissolve out (handle g 1248..1254).

The picture is two true-3D passes of the same camera move, DUSK and NIGHT_STORM (raw/dusk, raw/storm), mixed by deliver.py
with a moving cloud-front mask (a soft fbm edge drifting down the frame).  The storm pass also animates its sky dome
(slow turn: the storm masses drift) and its window groups; the dusk pass turns its sky the same way.

Blender frame = g + 1.
    python3 shot.py stills DUSK|NIGHT_STORM a:b:step <dir> [scale] [samples]
    python3 shot.py final DUSK|NIGHT_STORM a:b [scale] [samples]
"""
import math, os, sys, time, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import tower as T                                       # noqa: E402
import camrig, render                                   # noqa: E402
from anim import ease, keys, lerp, clamp                # noqa: E402


def g_of(t):
    return int(round((t + 0.10) * 30))


G0, G_END, H_IN, H_OUT = 1151, 1248, 8, 7
RANGE = (G0 - H_IN, G_END + H_OUT - 1)          # 1143..1254
G_CLOUD = g_of(39.786)                          # 1197 "เมฆดำก็ตั้งเค้า"
G_OVER = g_of(40.678)                           # 1223 "เหนือเมือง"
REFRAME = (1214, 1224)
WIN_ON = [1196, 1209, 1222, 1234]               # window groups light up
FLICKER = (1238, [0.25, 0.08, 0.32, 0.0])       # far sheet lightning (storm pass only)
SKY_TURN = 0.055                                # deg per frame of the sky dome (clouds drift)


def _k(pair):
    return tuple(pair[0]) + tuple(pair[1])


CA = (Vector((-13.6, -35.4, 8.0)), Vector((0.5, 0.0, 12.6)))
CB = (Vector((-13.0, -34.0, 8.4)), Vector((0.45, 0.0, 13.6)))
CC = (Vector((-12.3, -32.6, 8.9)), Vector((0.4, 0.0, 14.8)))
CD = (Vector((-11.8, -31.4, 9.3)), Vector((0.35, 0.0, 16.6)))
CE = (Vector((-11.4, -30.6, 9.6)), Vector((0.3, 0.0, 17.2)))


def cam(g):
    ks = [(RANGE[0], _k(CA), "sine"), (G_CLOUD, _k(CB), "cubic"), (REFRAME[0], _k(CC), "quint"), (REFRAME[1], _k(CD), "sine"),
          (RANGE[1], _k(CE), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.2)
    return Vector(k[:3]), Vector(k[3:])


def win_level(g, i):
    s = WIN_ON[i]
    return ease(clamp((g - s) / 5.0), "sine")


class Take(object):
    def __init__(self, preset, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.preset = preset
        self.scene = scene = bpy.context.scene
        self.A = T.build(preset)
        T.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 3000
        T.set_rod(0)                                    # that night there is no rod
        mk = bpy.data.objects.get("market")
        if mk is not None:
            mk.hide_render = True
        self.cam = camrig.make_camera(scene, name="cam_s15")
        self.cam.data.clip_start = 0.05
        self.cam.data.clip_end = 400
        self.sky = bpy.data.objects.get("sky")
        self.wmats = []
        if preset == "NIGHT_STORM":
            ob = bpy.data.objects.get("night_windows")
            base = ob.data.materials[0]
            r = random.Random(15)
            for i in range(len(WIN_ON)):
                m = base.copy(); m.name = "S15_win_%d" % i
                ob.data.materials.append(m); self.wmats.append(m)
            n0 = len(ob.data.materials) - len(WIN_ON)
            for poly in ob.data.polygons:
                if poly.material_index == 0:
                    poly.material_index = n0 + r.randrange(len(WIN_ON))
            self.win_k = T.STATE["P"]["win_k"]
        if verbose:
            print("s15: %s built in %.1f s" % (preset, time.time() - t0), flush=True)

    def key(self, gs):
        for g in gs:
            f = g + 1
            loc, look = cam(g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            if self.sky is not None:
                self.sky.rotation_euler = (0.0, 0.0, math.radians(SKY_TURN * (g - RANGE[0])))
                self.sky.keyframe_insert("rotation_euler", frame=f)
            if self.preset == "NIGHT_STORM":
                fl = 0.0
                s, seq = FLICKER
                if s <= g < s + len(seq):
                    fl = seq[g - s]
                T.flash(fl, frame=f)
                for i, m in enumerate(self.wmats):
                    sock = m.node_tree.nodes["strength"].inputs["Strength"]
                    sock.default_value = self.win_k * win_level(g, i)
                    sock.keyframe_insert("default_value", frame=f)

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.cycles.samples = samples
        return render.render_frames([g + 1 for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False, check=False)

    def report(self, g):
        f = g + 1
        self.scene.frame_set(f)
        loc, look = cam(g)
        v = look - loc
        return dict(g=g, preset=self.preset, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    spire=[round(x, 1) for x in render.world_to_screen(self.cam, T.FINIAL_TOP, f)[:2]])


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


if __name__ == "__main__":
    cmd, preset = sys.argv[1], sys.argv[2]
    gs = [g for g in parse(sys.argv[3]) if RANGE[0] <= g <= RANGE[1]]
    if cmd == "stills":
        out = sys.argv[4]
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        Tk = Take(preset); Tk.key(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "%s_g_%04d.png" % (preset[:5].lower(), g)))
            print("%s g %d  %.1f s" % (preset, g, st["wall"]), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw", "dusk" if preset == "DUSK" else "storm")
        os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            ok = os.path.exists(png) and os.path.exists(js)
            if ok:
                m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
            if not ok:
                todo.append(g)
        print("final %s: %d to render, %d done" % (preset, len(todo), len(gs) - len(todo)), flush=True)
        if todo:
            Tk = Take(preset, quality="final"); Tk.key(todo)
            for g in todo:
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("%s g %d  %.1f s wall  %.1f s cpu" % (preset, g, st["wall"], st["cpu"]), flush=True)
