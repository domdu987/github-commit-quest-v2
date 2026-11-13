#!/usr/bin/env python3
"""lib5.py -- shared machinery of the film-5 takes s05 / s06 / s07 (render team 1), built on the s01 worked example.

A take's shot.py defines a SPEC module-level object with:
    NAME            "s05"
    RANGES          {sid: (g0, g1)}  rendered film frames of each internal sub-shot (handles included)
    CAST            {actor_name: cast_key}               actors built in the tunnel
    PPD             {sid: {actor_name: px_per_D}}        sprite resolution per sub-shot (actors not listed are hidden)
    cam(sid, g)     -> (loc Vector, look Vector)
    stage(sid, g)   -> {actor_name: dict(pos=Vector floor point, pose=dict, hands=None|dict)}
    lamps(sid, g, T)-> {lamp_name: (pos, strength)}     (T.anch[(name, f)] = sprite anchors of the frame)
    LAMP_NAMES      every lamp name used by the take (others are keyed off)
    gas(sid, g)     -> density (0 = hidden)
    flame(sid, g)   -> set_flame k of the set's insert lamp or None
Blender frame of (sid, g) = 1000 * (sid - 1) + g + 1.  NO depth of field anywhere (client rule).
The set's 3D canary cage is hidden in these takes (alfie carries the cast's 2D held cage, bird drawn inside the bars).
"""
import math, os, sys, time, json, wave

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast5"), os.path.join(V3, "stage"), os.path.join(V3, "set3d5"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast5                                            # noqa: E402  (first: registers alfie, gaffer, miners, canary)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import mine as M                                        # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TP = M.TP


def g_of(t):                     # narration time -> film frame of an event
    return int(round((t + 0.10) * 30))


def bf(sid, g):
    return 1000 * (sid - 1) + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def lerpv(a, b, u):
    return a + (b - a) * u


def camkeys(g, ks):
    """ks = [(g, (loc), (look), ease), ...] -> (loc, look) Vectors"""
    k = keys(g, [(a, tuple(l) + tuple(m), e) for a, l, m, e in ks])
    return Vector(k[:3]), Vector(k[3:])


# ----------------------------------------------------------------------------- lip sync from the narration
_ENV = None


def _envelope():
    global _ENV
    if _ENV is None:
        w = wave.open(os.path.join(PROJ, "film5", "audio", "narration_bankky.wav"))
        sr, n = w.getframerate(), w.getnframes()
        import numpy as np
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
        hop = sr // 30
        env = []
        for i in range(0, len(a) // hop):
            seg = a[i * hop:(i + 1) * hop]
            env.append(float(np.sqrt(np.mean(seg * seg))))
        mx = sorted(env)[int(0.98 * len(env))]
        _ENV = [min(1.0, e / mx) for e in env]
    return _ENV


def loud(g):
    """narration loudness 0..1 heard at film frame g (narration starts at +0.10 s = film frame 3)."""
    env = _envelope(); i = int(g) - 3
    return env[i] if 0 <= i < len(env) else 0.0


def lip(g, g0, g1, silent="flat"):
    """mouth drawing for film frame g inside a quoted line [g0, g1]: a new drawing every 2 frames from the narration loudness
    (silent = flat, low = talk_a, loud = talk_b, every third loud pair round talk_o).  Outside the line: None (no override)."""
    if g < g0 or g > g1:
        return None
    gp = g0 + 2 * ((g - g0) // 2)                       # hold each drawing two frames
    v = max(loud(gp), loud(gp + 1))
    if v < 0.10:
        return silent
    if v < 0.38:
        return "talk_a"
    return "talk_o" if ((gp - g0) // 2) % 3 == 2 else "talk_b"


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, S, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.S = S
        self.scene = scene = bpy.context.scene
        self.A = M.build("tunnel")
        M.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 9000
        self.cam = camrig.make_camera(scene, name="cam_" + S.NAME)
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 600
        M.setup_dof(scene, None, None, cam=self.cam)
        self._hide_set_cage()
        self.actors, self.anch, self.lamps = {}, {}, {}
        sd = os.path.join(HERE, "work", "sprites")
        for n, ck in S.CAST.items():
            a = actors.Actor(n, ck)
            a.build(sprites.DEFAULT_CANVAS[ck], sd, contact=True)
            a.head_flip = False
            M.no_bounce(a.card)
            self.actors[n] = a
        self._gas_drift_nodes()
        if verbose:
            print("%s: built tunnel in %.1f s" % (S.NAME, time.time() - t0), flush=True)

    def _hide_set_cage(self):
        piv = M.STATE["cage_pivot"]
        stack = list(piv.children)
        while stack:
            o = stack.pop()
            o.hide_render = True; o.hide_viewport = True
            stack += list(o.children)

    def _gas_drift_nodes(self):
        m = M.STATE.get("gas_mat")
        nt = m.node_tree
        geo = [n for n in nt.nodes if n.bl_idname == "ShaderNodeNewGeometry"][0]
        sep = [n for n in nt.nodes if n.bl_idname == "ShaderNodeSeparateXYZ"][0]
        add = nt.nodes.new("ShaderNodeVectorMath"); add.operation = "ADD"; add.name = "drift"
        nt.links.new(geo.outputs["Position"], add.inputs[0]); nt.links.new(add.outputs[0], sep.inputs[0])
        self.drift = add

    def gas(self, f, g, density):
        M.set_gas(density, frame=f)
        v = self.drift.inputs[1]
        v.default_value = (0.0, -0.9 * g / 30.0, 0.10 * math.sin(g / 30.0 * 1.3))
        v.keyframe_insert("default_value", frame=f)

    def visible(self, sid):
        for n, a in self.actors.items():
            a.set_hidden(n not in self.S.PPD[sid])

    def probe_anchor(self, n, f, pose, key, loc, look):
        """world point of anchor `key` of actor n posed with `pose` at Blender frame f seen from (loc, look) (no sprite file)."""
        a = self.actors[n]
        camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
        self.scene.frame_set(f)
        a.pose(f, pose, camera=self.cam)
        svg, info = sprites.sprite_svg(a.cast, a.poses[f], 64, canvas=a.canvas, upper_k=a.upper_k[f])
        return actors.local_to_world(a, info["anchors"][key], f)

    def pose(self, sid, gs):
        S = self.S
        if hasattr(S, "prepare") and not getattr(self, "_prepared", False):
            self._prepared = True
            S.prepare(self)
        self.visible(sid)
        st = {}
        for g in gs:
            f = bf(sid, g)
            loc, look = S.cam(sid, g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            M.set_drips(f)
            self.gas(f, g, S.gas(sid, g))
            k = S.flame(sid, g)
            M.set_flame(1.0 if k is None else k, frame=f)
            st[g] = S.stage(sid, g)
            for n, d in st[g].items():
                self.actors[n].place(f, tuple(d["pos"]))
        for g in gs:
            f = bf(sid, g)
            self.scene.frame_set(f)
            for n, d in st[g].items():
                self.actors[n].pose(f, d["pose"], hands=d.get("hands"), camera=self.cam)
        fr = [bf(sid, g) for g in gs]
        for n, ppd in S.PPD[sid].items():
            a = self.actors[n]
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(n, f)] = r["anchors"]
                if r.get("clipped"):
                    print("%s: WARNING sprite of %s clipped on frame %d" % (S.NAME, n, f), flush=True)
        for g in gs:
            f = bf(sid, g)
            self.scene.frame_set(f)
            on = S.lamps(sid, g, self)
            for name in S.LAMP_NAMES:
                pos, s = on.get(name, (Vector((0, -30, 1)), 0.0))
                self.lamps[name] = M.lamp_light(tuple(pos), s, frame=f, name=name)

    def anchor_world(self, n, key, f, toward_cam=0.0):
        a = self.actors[n]
        an = self.anch[(n, f)]
        p = actors.local_to_world(a, an[key], f)
        if toward_cam:
            c = self.cam.matrix_world.to_translation()
            d = c - p; d.z = 0; d.normalize(); p = p + d * toward_cam
        return p

    def report(self, sid, g):
        f = bf(sid, g)
        self.scene.frame_set(f)
        loc, look = self.S.cam(sid, g)
        v = look - loc
        out = dict(shot=sid, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   heads={})
        for n, a in self.actors.items():
            if a.card.hide_render or (n, f) not in self.anch:
                continue
            res = a.feet.get(f)
            an = self.anch[(n, f)]
            hx, hy = an["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][n] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
            pose = a.poses.get(f, {})
            out["heads"][n]["mouth"] = str(pose.get("mouth", pose.get("expr", "")))
        return out

    def render(self, sid, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(sid)
        self.scene.camera = self.cam
        M.setup_dof(self.scene, None, None, cam=self.cam)        # client rule: no depth of field, ever
        self.scene.cycles.samples = samples
        return render.render_frames([bf(sid, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def main(S, argv):
    """python3 shot.py probe|stills|final <sids> <g spec> [out_dir] [scale] [samples]"""
    cmd = argv[1]
    sids = [int(s) for s in argv[2].split(",")]
    T = None
    if cmd in ("probe", "stills"):
        T = Take(S, "preview")
        for sid in sids:
            gs = [g for g in parse(argv[3]) if S.RANGES[sid][0] <= g <= S.RANGES[sid][1]]
            if not gs:
                a, b = S.RANGES[sid]; gs = [a, (a + b) // 2, b]
            T.pose(sid, gs)
            for g in gs:
                print(json.dumps(T.report(sid, g)), flush=True)
                if cmd == "stills":
                    out = argv[4]
                    scale = float(argv[5]) if len(argv) > 5 else 0.5
                    samples = int(argv[6]) if len(argv) > 6 else 6
                    st = T.render(sid, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "%s_%d_g_%04d.png" % (S.NAME, sid, g)))
                    print("sid %d g %d  %.1f s wall %.1f cpu" % (sid, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(argv[4]) if len(argv) > 4 else 1.0
        samples = int(argv[5]) if len(argv) > 5 else 12
        for sid in sids:
            gs = [g for g in parse(argv[3]) if S.RANGES[sid][0] <= g <= S.RANGES[sid][1]]
            out = os.path.join(HERE, "raw", "s%d" % sid)
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: sid %d, %d to render, %d done" % (sid, len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if T is None:
                T = Take(S, "final")
            T.pose(sid, todo)
            for g in todo:
                st = T.render(sid, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = T.report(sid, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("sid %d g %d  %.1f s wall  %.1f s cpu" % (sid, g, st["wall"], st["cpu"]), flush=True)
