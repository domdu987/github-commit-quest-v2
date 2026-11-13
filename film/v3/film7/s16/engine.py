#!/usr/bin/env python3
"""engine.py -- a small spec-driven take runner on top of ../common.py, shared (identical copy) by takes s16, s18, s19 of film 7.

A take script (shot.py) declares SETUPS: {id: Setup(...)}; each set-up is one location + preset, a g range, a camera function and
a list of Cast entries (actor, cast key, feet position (g) -> (x, y, z) or None = off-stage, pose (g) -> dict).  One set-up = one
Take = one process build (the louvre gotcha: one location per process; we also rebuild between set-ups of the same location so each
set-up owns its own actors and dressing).

    python3 shot.py probe <ids> a:b[:step]
    python3 shot.py stills <ids> a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final <ids> a:b[:step] [scale] [samples]

Blender frame of (set-up id, g) = 1000 * (id - 1) + g + 1 (common.bf): g of this film reaches ~2050, every id block holds < 1000 g
so the blocks never overlap.
"""
import math, os, sys, json

FILM7 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if FILM7 not in sys.path:
    sys.path.insert(0, FILM7)
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf


class Cast(object):
    def __init__(self, name, cast, pos, pose, ppd=304, canvas=None, vis=None):
        self.name, self.cast, self.pos, self.pose, self.ppd, self.canvas = name, cast, pos, pose, ppd, canvas
        self.vis = vis or (lambda g: True)


class Setup(object):
    """loc, preset, g (g0, g1 inclusive), cam(g) -> (loc, look[, lens]), cast [Cast], keys(g) -> dict for Take.key_set (flames=, mona=,
    papers=, ...), dress(take) runtime dressing, frame_fx(take, f, g) extra per-frame keys (light ramps), hide (object-name prefixes
    to hide_render), light (LIGHTS key override), lens default."""

    def __init__(self, loc, preset, g, cam, cast=(), keys=None, dress=None, frame_fx=None, hide=(), light=None, lens=22.0, note=""):
        self.loc, self.preset, self.g, self.cam, self.cast = loc, preset, tuple(g), cam, list(cast)
        self.keys = keys or (lambda g: {})
        self.dress, self.frame_fx, self.hide, self.light, self.lens, self.note = dress, frame_fx, tuple(hide), light, lens, note


def ranges(setups):
    return {k: s.g for k, s in setups.items()}


class Take(C.Take):
    def __init__(self, setups, sid, quality="preview", tag="take"):
        S = setups[sid]
        C.Take.__init__(self, S.loc, S.preset, quality=quality, lens=S.lens, name="cam_%s_%d" % (tag, sid), light=S.light)
        self.S, self.sid = S, sid
        sd = os.path.join(os.environ.get("ENGINE_WORK", "work"), "sprites")
        if S.dress:
            S.dress(self)
        if S.hide:
            for ob in self.scene.objects:
                if ob.name.startswith(S.hide):
                    ob.hide_render = True
        for c in S.cast:
            a = C.make_actor(c.name, c.cast, sd, canvas=c.canvas)
            self.actors[c.name] = a

    def cam_at(self, g):
        r = self.S.cam(g)
        return Vector(r[0]), Vector(r[1]), (r[2] if len(r) > 2 else None)

    def pose(self, sid, gs):
        assert sid == self.sid
        S = self.S
        for g in gs:
            f = bf(sid, g)
            loc, look, lens = self.cam_at(g)
            self.key_cam(f, loc, look, lens=lens or S.lens)
            self.key_set(f, **S.keys(g))
            if S.frame_fx:
                S.frame_fx(self, f, g)
            for c in S.cast:
                a = self.actors[c.name]
                p = c.pos(g)
                C.place(a, f, p[:2], p[2] if len(p) > 2 else 0.0)
                vis = bool(c.vis(g))
                for ob in a.root.children:
                    ob.hide_render = not vis
                    ob.keyframe_insert("hide_render", frame=f)
                    fc = C._fcurve(ob, "hide_render")
                    if fc is not None:
                        for kp in fc.keyframe_points:
                            kp.interpolation = "CONSTANT"
        for g in gs:
            f = bf(sid, g)
            self.scene.frame_set(f)
            for c in S.cast:
                self.actors[c.name].pose(f, c.pose(g), camera=self.cam)
        self.sprites_for([(self.actors[c.name], c.ppd) for c in S.cast], sorted(set(bf(sid, g) for g in gs)))

    def report(self, sid, g):
        f = bf(sid, g)
        self.scene.frame_set(f)
        loc, look, lens = self.cam_at(g)
        v = look - loc
        return dict(shot=sid, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, sid, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(sid, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def main(setups, here, tag):
    os.environ.setdefault("ENGINE_WORK", os.path.join(here, "work"))
    cmd = sys.argv[1]
    ids = [int(s) for s in sys.argv[2].split(",")]
    R = ranges(setups)
    if cmd in ("probe", "stills"):
        for sid in ids:
            gs = [g for g in C.parse(sys.argv[3]) if R[sid][0] <= g <= R[sid][1]]
            if not gs:
                continue
            Tk = Take(setups, sid, "preview", tag)
            Tk.pose(sid, gs)
            for g in gs:
                print(json.dumps(Tk.report(sid, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(sid, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (sid, g)))
                    print("set-up %d g %d  %.1f s wall %.1f cpu" % (sid, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, sid: Take(setups, sid, q, tag), ids, sys.argv[3], R, here, scale=scale, samples=samples,
                     take_key=lambda sid: sid)


# ----------------------------------------------------------------------------- helpers for the specs
def walker(cast, p0, vel, g0, facing, base=None, period=28.0, speed=0.85, arms="both", phase0=0.0):
    """(pos(g), pose(g)) of a straight walk from p0 at g0 with vel (D per frame)."""
    p0, vel = Vector(p0), Vector(vel)

    def pos(g):
        return tuple(p0 + vel * (g - g0))

    def pose(g):
        p = cast7.cycle(cast, phase0 + (g - g0) / period, "walk", facing=facing, base=dict(base or {}), arms=arms, speed=speed)
        p["t"] = g / 30.0
        return p
    return pos, pose


def story(name, **over):
    p = dict(cast7.STORY7[name][1])
    p.pop("mouth", None)                      # client rule: no talking mouths outside the quoted lines (static expression mouths only)
    p.update(over)
    return p


def sun_dir(travel, elev):
    return Vector(L.G._kd(travel, elev)).normalized()


def key_sun(take, f, rgb, elev, travel=(0.22, 0.97), fill=1.0, fill_rgb=None):
    """per-frame daylight of the gallery: sun colour / strength (rgb as in LIGHTS key), elevation, the skylight fills scaled by fill."""
    import bpy
    sun = L.STATE["sun"]
    k = max(rgb)
    sun.data.color = tuple(x / k for x in rgb)
    sun.data.energy = math.pi * k
    sun.rotation_euler = (-sun_dir(travel, elev)).to_track_quat("Z", "Y").to_euler()
    sun.data.keyframe_insert("color", frame=f)
    sun.data.keyframe_insert("energy", frame=f)
    sun.keyframe_insert("rotation_euler", frame=f)
    for nm, base in (("sky_fill", 2600.0), ("sky_fill_front", 700.0)):
        ob = bpy.data.objects.get(nm)
        if ob is None:
            continue
        ob.data.energy = base * fill
        if fill_rgb is not None:
            ob.data.color = fill_rgb
            ob.data.keyframe_insert("color", frame=f)
        ob.data.keyframe_insert("energy", frame=f)


def key_grade(take, f, slope=(1.0, 0.985, 0.97), offset=None):
    """key the compositor CDL slope (a global light-colour / exposure ramp; louvre's grade = spec/grade_compositor.py)."""
    ng = take.scene.compositing_node_group
    cb = [n for n in ng.nodes if n.bl_idname == "CompositorNodeColorBalance"][0]
    cb.inputs[14].default_value = (slope[0], slope[1], slope[2], 1.0)
    cb.inputs[14].keyframe_insert("default_value", frame=f)
    if offset is not None:
        cb.inputs[10].default_value = (offset[0], offset[1], offset[2], 1.0)
        cb.inputs[10].keyframe_insert("default_value", frame=f)
