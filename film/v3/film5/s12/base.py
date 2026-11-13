#!/usr/bin/env python3
"""base.py -- shared engine of film 5 takes s12 / s13 / s14 (render team 3), built on the s01 structure.

A take = a dict of sub-shots {id: Sub}.  Each Sub gives, per film frame g: the camera, the visible actors (feet point, pose, pinned
hands, sprite px per D), set controls (cage / gas / flame / blast / extra lights).  Blender frame of (sub s, g) = 1000 * (s - 1) + g + 1.
NO depth of field anywhere (client note): M.setup_dof(scene, None, None, cam=...) at build and before every render.

    python3 shot.py probe <ids> a:b[:step]
    python3 shot.py stills <ids> a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final <ids> a:b[:step] [scale] [samples]
"""
import math, os, sys, time, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(BASE_DIR))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast5"), os.path.join(V3, "stage"), os.path.join(V3, "set3d5"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast5                                            # noqa: E402  (first: registers alfie, miners, canary)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import mine as M                                        # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TP = M.TP
SETUP = None                     # optional callable(Take) run after the build (runtime set changes of a take)


def g_of(t):                     # narration time -> film frame of an event
    return int(round((t + 0.10) * 30))


def bf(sub, g):
    return 1000 * (sub - 1) + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def lerpv(a, b, u):
    return Vector(a) + (Vector(b) - Vector(a)) * u


def cam_keys(g, ks):
    """ks = [(g, loc, look, ease)] -> (loc, look) Vectors."""
    k = keys(g, [(a, tuple(l) + tuple(o), e) for a, l, o, e in ks])
    return Vector(k[:3]), Vector(k[3:])


def run_legs(g, period=10.0, stride=1.2, phase=0.0, lift=0.8):
    """a run cycle for the puppet's step legs: stride swings + / -, the moving foot lifts."""
    a = 2 * math.pi * (g / period + phase)
    s = math.sin(a)
    up = max(0.0, math.cos(a))
    dn = max(0.0, -math.cos(a))
    return dict(preset="step", stride=stride * s, lift_l=lift * up, lift_r=lift * dn, knee_l=1.0, knee_r=1.0, toe_r=0.6, toe_l=0.6)


def walk_legs(g, period=16.0, stride=0.7, phase=0.0):
    return run_legs(g, period, stride, phase, lift=0.35)


def talk(g, g0, g1, seed=0):
    """lip-sync mouth for a quoted line (new drawing every 2 frames), closed outside [g0, g1]."""
    if g < g0 or g > g1:
        return None
    seq = ["talk_a", "talk_b", "talk_b", "talk_a", "talk_o", "talk_b", "flat", "talk_a", "talk_b", "talk_o", "talk_a", "flat"]
    return seq[((g - g0) // 2 + seed) % len(seq)]


class Sub(object):
    """one framing.  rng = (g_first, g_last) incl. handles; name = label in meta; actors = {name: (cast, canvas or None)}"""
    def __init__(self, name, rng, cam, stage, ctl=None, lamps=None, actors=(), gas=0.0, ppd=None, extra=None):
        self.name, self.rng, self.cam, self.stage, self.ctl, self.lamps = name, rng, cam, stage, ctl, lamps
        self.actors = list(actors); self.gas = gas; self.ppd = ppd or {}; self.extra = extra


CAST = {"alfie": ("alfie", (-1.875, -3.875, 1.875, 0.1875)),
        "gaffer": ("gaffer", None), "miner1": ("miner1", None), "miner2": ("miner2", None), "miner3": ("miner3", None),
        "bird": ("canary", (-0.75, -1.25, 0.875, 0.125))}


class Take(object):
    def __init__(self, take, subs, quality="preview", verbose=True, workdir=None):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.take, self.subs = take, subs
        self.scene = scene = bpy.context.scene
        self.A = M.build("tunnel")
        M.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 12000
        self.cam = camrig.make_camera(scene, name="cam_" + take)
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 600
        M.setup_dof(scene, None, None, cam=self.cam)
        self.actors, self.anch, self.lamps = {}, {}, {}
        sd = os.path.join(workdir, "sprites")
        names = sorted({n for s in subs.values() for n in s.actors})
        for n in names:
            cast, cv = CAST[n]
            a = actors.Actor(n, cast)
            a.build(cv or sprites.DEFAULT_CANVAS[cast], sd, contact=(n != "bird"), shadow=None if n == "bird" else "proxy")
            a.head_flip = False
            M.no_bounce(a.card)
            self.actors[n] = a
        self.cage_objs = [o for o in bpy.data.objects if o.name.startswith("canary_cage")]
        c = self.A["cage"]
        self.perch = Vector(c["perch"]); self.floor = Vector(c["floor"]); self.hook = Vector(c["hook"])
        self._gas_drift_nodes()
        self._flame_nodes()
        if SETUP is not None:
            SETUP(self)
        if verbose:
            print("%s: built tunnel in %.1f s (%s)" % (take, time.time() - t0, ", ".join(names)), flush=True)

    # -- gas drift (as s01): keyed offset of the haze pattern so the layers slide past the lamps
    def _gas_drift_nodes(self):
        m = M.STATE.get("gas_mat")
        nt = m.node_tree
        geo = [n for n in nt.nodes if n.bl_idname == "ShaderNodeNewGeometry"][0]
        sep = [n for n in nt.nodes if n.bl_idname == "ShaderNodeSeparateXYZ"][0]
        add = nt.nodes.new("ShaderNodeVectorMath"); add.operation = "ADD"; add.name = "t3_drift"
        nt.links.new(geo.outputs["Position"], add.inputs[0]); nt.links.new(add.outputs[0], sep.inputs[0])
        self.drift = add

    def gas(self, f, g, density):
        M.set_gas(density, frame=f)
        v = self.drift.inputs[1]
        v.default_value = (0.0, -0.9 * g / 30.0, 0.10 * math.sin(g / 30.0 * 1.3))
        v.keyframe_insert("default_value", frame=f)

    # -- the foreman's insert-lamp flame: colour keyed warm -> pale blue (firedamp), done at runtime on the set's own materials
    def _flame_nodes(self):
        pre = M.STATE["pre"]
        self.flame_emis = []
        for nm in ("e_flame_ins", "e_flamec_ins"):
            m = bpy.data.materials[pre + nm]
            e = [n for n in m.node_tree.nodes if n.bl_idname == "ShaderNodeEmission"][0]
            self.flame_emis.append((e, tuple(e.inputs["Color"].default_value)))

    def flame(self, f, k, blue):
        M.set_flame(k, frame=f)
        BLUE = [(0.35, 0.62, 1.0, 1.0), (0.75, 0.9, 1.0, 1.0)]
        for (e, c0), cb in zip(self.flame_emis, BLUE):
            col = tuple(c0[i] * (1 - blue) + cb[i] * blue for i in range(4))
            e.inputs["Color"].default_value = col
            e.inputs["Color"].keyframe_insert("default_value", frame=f)
        L = M.STATE["insert_light"]
        L.data.color = (1.0 - 0.55 * blue, 0.8 - 0.05 * blue, 0.5 + 0.5 * blue)
        L.data.keyframe_insert("color", frame=f)

    def cage3d(self, visible):
        for o in self.cage_objs:
            o.hide_render = not visible

    def visible(self, sid):
        S = self.subs[sid]
        for n, a in self.actors.items():
            a.set_hidden(n not in S.actors)

    def per_frame(self, sid, g):
        """per-frame visibility (render one frame at a time): S.extra = {"cage3d": g -> bool, "hide": g -> set of actor names}"""
        S = self.subs[sid]; ex = S.extra or {}
        self.cage3d(ex["cage3d"](g) if "cage3d" in ex else True)
        hid = ex["hide"](g) if "hide" in ex else set()
        for n, a in self.actors.items():
            a.set_hidden(n not in S.actors or n in hid)

    def pose(self, sid, gs):
        S = self.subs[sid]
        self.cur = sid
        self.visible(sid)
        st = {}
        for g in gs:
            f = bf(sid, g)
            loc, look = S.cam(g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            M.set_drips(f)
            M.set_cage(getattr(self, "cage_at", None), frame=f)
            self.gas(f, g, S.gas(g) if callable(S.gas) else S.gas)
            if S.ctl:
                S.ctl(self, f, g)
            st[g] = S.stage(self, g)
            for n, d in st[g].items():
                self.actors[n].place(f, tuple(d["pos"]), flip=d.get("flip", False))
        for g in gs:
            f = bf(sid, g)
            self.scene.frame_set(f)
            for n, d in st[g].items():
                hands = d.get("hands")
                if callable(hands):
                    hands = hands(self, f)
                self.actors[n].pose(f, d["pose"], hands=hands, camera=self.cam)
        fr = [bf(sid, g) for g in gs]
        for n in S.actors:
            a = self.actors[n]
            for f, r in zip(fr, a.render_sprites(S.ppd.get(n, 256), frames=fr)):
                self.anch[(n, f)] = r["anchors"]
                if r.get("clipped"):
                    print("%s: WARNING sprite of %s clipped on frame %d" % (self.take, n, f), flush=True)
        self.key_lamps(sid, gs, st)

    def anchor_world(self, n, key, f):
        a = self.actors[n]
        return actors.local_to_world(a, self.anch[(n, f)][key], f)

    def key_lamps(self, sid, gs, st):
        S = self.subs[sid]
        names = set()
        for s in self.subs.values():
            names |= set(getattr(s, "lamp_names", ()))
        for g in gs:
            f = bf(sid, g)
            self.scene.frame_set(f)
            on = S.lamps(self, g, f) if S.lamps else {}
            for name in sorted(names | set(on)):
                pos, s_, col = (tuple(on[name]) + (M.WARM,))[:3] if name in on else (Vector((0, -30, 1)), 0.0, M.WARM)
                self.lamps[name] = M.lamp_light(tuple(pos), s_, frame=f, name=name, color=col)

    def report(self, sid, g):
        S = self.subs[sid]
        f = bf(sid, g)
        self.scene.frame_set(f)
        loc, look = S.cam(g)
        v = look - loc
        out = dict(shot=S.name, sub=sid, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   heads={})
        for n in S.actors:
            a = self.actors[n]
            if (n, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(n, f)]["head"]
            hr = 0.5 if n != "bird" else 0.09
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - hr, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + hr, hy), f, res)
            out["heads"][n] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        pts = {"perch": tuple(self.perch), "cage_floor": tuple(self.floor), "hook": tuple(self.hook), "flame": tuple(M.STATE["insert_flame_pos"]),
               "front": tuple(TP(max(0.5, M.blast_front(M.STATE.get("blast_u", 0.0))), 0, 2.3))}
        out["pts"] = {k: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for k, p in pts.items()}
        return out

    def render(self, sid, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(sid)
        self.scene.camera = self.cam
        M.setup_dof(self.scene, None, None, cam=self.cam)        # client note: no depth of field, ever
        self.scene.cycles.samples = samples
        if len(gs) == 1:
            self.per_frame(sid, gs[0])
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


def main(take, subs, here, argv):
    cmd = argv[1]
    ids = [int(s) for s in argv[2].split(",")]
    work = os.path.join(here, "work")
    T = None
    if cmd in ("probe", "stills"):
        quality = "preview"
        for sid in ids:
            S = subs[sid]
            gs = [g for g in parse(argv[3]) if S.rng[0] <= g <= S.rng[1]] if len(argv) > 3 else []
            if not gs:
                gs = [S.rng[0], (S.rng[0] + S.rng[1]) // 2, S.rng[1]]
            if T is None:
                T = Take(take, subs, quality, workdir=work)
            T.pose(sid, gs)
            for g in gs:
                print(json.dumps(T.report(sid, g)), flush=True)
                if cmd == "stills":
                    out = argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(argv[5]) if len(argv) > 5 else 0.5
                    samples = int(argv[6]) if len(argv) > 6 else 6
                    st = T.render(sid, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "%s_g_%04d.png" % (S.name, g)))
                    print("sub %s g %d  %.1f s wall %.1f cpu" % (S.name, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(argv[4]) if len(argv) > 4 else 1.0
        samples = int(argv[5]) if len(argv) > 5 else 12
        for sid in ids:
            S = subs[sid]
            gs = [g for g in parse(argv[3]) if S.rng[0] <= g <= S.rng[1]]
            out = os.path.join(here, "raw", "s%d" % sid)
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: sub %s, %d to render, %d done" % (S.name, len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if T is None:
                T = Take(take, subs, "final", workdir=work)
            T.pose(sid, todo)
            for g in todo:
                st = T.render(sid, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = T.report(sid, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("sub %s g %d  %.1f s wall  %.1f s cpu" % (S.name, g, st["wall"], st["cpu"]), flush=True)
