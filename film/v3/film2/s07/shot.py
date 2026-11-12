#!/usr/bin/env python3
"""shot.py -- film 2 take s07: shot 7, tower set DAY, bell chamber at eye level (chamber_eye side).

    shot 7  g 448..534  10-frame dissolve in (in-handle g 441..447): nico, the smallest ringer, between the baker (left) and the
                        woman (right); all three haul their ropes.  On "เด็กดึงเชือก" (g 465) nico hauls hard; the rope springs
                        back up and lifts him off his feet (g 470..484, peak 0.95 D), legs dangling, he hangs there kicking,
                        drops back on "น้อยที่สุด" (g 506..512, squash on landing), and is lifted again for the out-handle.
                        Snap tilt/push onto nico as he rises (g 472..482).  Out-handle g 535..541 (10-frame dissolve into shot 8).

Ropes as in s04: 3D ropes 0.1 D behind each card, keyed with the pull; hands pinned on them.  Nico rides his rope: when it rises
above its rest height his feet leave the floor by the same amount.  Blender frame = g + 1.

    python3 shot.py probe 7 a:b:step | stills 7 a:b:step out_dir [scale] [samples] | final 7 a:b [scale] [samples]
"""
import math, os, sys, time, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("s04shot", os.path.join(os.path.dirname(HERE), "s04", "shot.py"))
S04 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S04)      # ropes, CLI, path setup
import cast2                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")
g_of = S04.g_of

G_S7, G_S8 = 448, 535
H_IN, H_OUT = 7, 7
RANGES = {7: (G_S7 - H_IN, G_S8 + H_OUT - 1)}
G_DEK = g_of(15.412)            # 465 "เด็กดึงเชือก"
G_RAKANG = g_of(15.968)         # 482 "ระฆัง"
G_NOI = g_of(16.751)            # 506 "น้อยที่สุด"
SNAP = (472, 482)
CH = T.Z_CH


def bf(shot, g):
    return int(g) + 1


RINGERS = {   # name: (cast, story pose, feet, upper hand side, phase)
    "baker": ("baker", "extras_ring", (-0.95, -0.3, CH), "r", 0.0),
    "woman": ("woman", "extras_ring_woman", (1.35, -0.3, CH), "l", 0.5),
    "nico": ("nico", "nico_pull_rope", (0.2, -0.15, CH), "r", 0.25),
}
HAUL = 0.34


def adult_u(g, ph):
    return S04.pull_u(g, ph)


def nico_rope(g):
    """rope offset (D, + = up) of nico's rope: small hauls, a big haul, the spring up that lifts him, the drop, the second lift."""
    if g < G_DEK - 6:
        return -0.22 * S04.pull_u(g, 0.25)
    ks = [(G_DEK - 6, -0.22 * S04.pull_u(G_DEK - 6, 0.25), "cubic_in"),
          (G_DEK + 1, -0.42, "sine"),                 # big haul down
          (G_DEK + 4, -0.42, "back_out"),             # the bell swings back: the rope shoots up
          (G_RAKANG, 0.62, "sine"),
          (G_RAKANG + 10, 0.50, "sine"),
          (G_NOI, 0.58, "cubic_in"),
          (G_NOI + 5, 0.0, "sine"),                   # drops back on the floor
          (G_NOI + 14, -0.30, "cubic_in"),            # hauls again ...
          (G_NOI + 18, -0.30, "back_out"),
          (G_S8 + 2, 0.45, "sine"),                   # ... and up he goes again
          (RANGES[7][1], 0.42, "hold")]
    v = keys(g, ks)
    if G_RAKANG - 2 <= g <= G_NOI:                  # bobbing on the rope
        v += 0.05 * math.sin((g - G_RAKANG) * 0.55)
    return v


def lift(g):
    return max(0.0, nico_rope(g))


DANGLE = 0.32                                    # STORY2_META["nico_pull_rope"]["lift"]: dangling feet hang this much higher


def dangling(g):
    return lift(g) >= 0.06


def dangle_z(g):
    return lift(g) + DANGLE if dangling(g) else 0.0


def bell_angle(g):
    # one slow swing; the kick that sends nico up is the bell coming back
    return 14.0 * math.sin(2 * math.pi * (g - 441) / 48.0) + 10.0 * pulse(g, G_DEK + 2, G_RAKANG - 4, G_NOI, 1.0)


# ----------------------------------------------------------------------------- camera
HEAD_N = Vector((0.2, -0.15, CH + 2.0))


def cam7(g):
    a = (Vector((0.62, -4.3, CH + 2.05)), Vector((0.05, 1.9, CH + 2.6)))
    b = (Vector((0.42, -4.0, CH + 2.1)), Vector((0.12, 1.9, CH + 2.65)))
    up = HEAD_N + Vector((0, 0, 0.6))
    c = (up + (Vector((0.42, -4.0, CH + 2.1)) - HEAD_N).normalized() * 3.3 + Vector((0.0, 0.0, -0.35)), up + Vector((0.0, 0.0, -0.45)))
    d = (c[0] + Vector((-0.08, 0.05, -0.05)), c[1] + Vector((0.0, 0.0, -0.22)))
    e = (c[0] + Vector((-0.18, 0.12, -0.2)), c[1] + Vector((0.05, 0.0, -0.50)))
    f = (e[0] + Vector((-0.05, 0.05, 0.25)), e[1] + Vector((0.0, 0.0, -0.05)))
    ks = [(RANGES[7][0], tuple(a[0]) + tuple(a[1]), "sine"),
          (SNAP[0], tuple(b[0]) + tuple(b[1]), "quint"),
          (SNAP[1], tuple(c[0]) + tuple(c[1]), "sine"),
          (G_NOI, tuple(d[0]) + tuple(d[1]), "cubic"),          # follows him down
          (G_NOI + 14, tuple(e[0]) + tuple(e[1]), "sine"),
          (RANGES[7][1], tuple(f[0]) + tuple(f[1]), "hold")]
    k = lerp(keys(g, ks), keys(g, [(fr, v, "lin") for fr, v, ee in ks]), 0.25)
    loc, look = Vector(k[:3]), Vector(k[3:])
    look = look + Vector((0.0, 0.0, 0.008 * math.sin(g * 0.41) + tilt_k(g) * tilt_lift(g)))   # tilt up with him while he hangs
    return loc, look


def tilt_k(g):
    return keys(g, [(G_RAKANG - 4, 0.7, "sine"), (G_RAKANG + 10, 1.1, "sine"), (G_NOI + 14, 1.1, "sine"), (G_S8 - 12, 1.5, "hold")])


def tilt_lift(g):
    """lift smoothed over +-4 frames (the camera operator follows, a little late)."""
    w = [math.cos(math.pi * i / 10.0) for i in range(-4, 5)]
    return sum(wi * lift(g - 2 + i) for wi, i in zip(w, range(-4, 5))) / sum(w)


# ----------------------------------------------------------------------------- poses
def ringer_pose(name, g):
    cast, story, feet, up, ph = RINGERS[name]
    p = dict(cast2.STORY2[story][1])
    p.pop("prop_l", None); p.pop("prop_r", None)
    s = 1 if up == "r" else -1
    if name == "nico":
        L = lift(g)
        haul = clamp(-nico_rope(g) / 0.42)
        if not dangling(g):
            p["legs"] = "wide" if haul > 0.3 else "stand"
            p["expr"] = "determined"; p["mouth"] = "clench"
        else:
            p["expr"] = "shocked" if g < G_NOI else "worried"
            p.pop("mouth", None)
            if g >= G_NOI:
                p["mouth"] = "clench"
            kick = math.sin((g - G_RAKANG) * 0.6)
            lg = dict(p["legs"]); lg["knee_l"] = -0.6 + 0.5 * kick; lg["knee_r"] = 1.0 - 0.5 * kick
            p["legs"] = lg
        land = pulse(g, G_NOI + 4, G_NOI + 5, G_NOI + 11, 1.0)
        p["squash"] = (0.97 + 0.08 * land + 0.03 * haul, 1.04 - 0.10 * land - 0.04 * haul)
        p["lean"] = -4 + 6 * haul
        p["head_roll"] = 8 + 3 * math.sin(g * 0.3)
        p["blink"] = blink(g, [452, 494, 527])
        return p
    u = adult_u(g, ph)
    p["lean"] = p.get("lean", 0) + s * 7.0 * u
    p["squash"] = (1.0 + 0.04 * u, 1.0 - 0.05 * u)
    p["head_roll"] = p.get("head_roll", 0) + s * 4.0 * u
    p["head_dy"] = 0.04 * u
    # they turn and stare at the boy going up
    look = ease(clamp((g - G_RAKANG + 6) / 8.0), "sine") * (1.0 - ease(clamp((g - G_NOI - 8) / 10.0), "sine"))
    if look > 0.3:
        p["expr"] = "stunned"; p.pop("mouth", None)
        p["gaze"] = (s * 0.6, -0.6)
        p["pitch"] = -0.6
    p["blink"] = blink(g, [446 + int(ph * 20), 503 + int(ph * 12)])
    return p


def rest_hands(name):
    cast, story, feet, up, ph = RINGERS[name]
    p = cast2.STORY2[story][1]
    lo = "l" if up == "r" else "r"
    return p["arm_" + up]["hand"], p["arm_" + lo]["hand"], up, lo


def rope_off(name, g):
    if name == "nico":
        return nico_rope(g)
    return -HAUL * adult_u(g, RINGERS[name][4])


class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = T.build("DAY")
        T.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 2000
        T.set_rod(1)
        mk = bpy.data.objects.get("market")
        if mk is not None:
            mk.hide_render = True
        self.cam = camrig.make_camera(scene, name="cam_s07")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.act = {}
        for n, (cast, story, feet, up, ph) in RINGERS.items():
            a = actors.Actor(n, cast)
            a.build(sprites.canvas_for(cast, [cast2.STORY2[story][1]]) if n == "nico" else sprites.DEFAULT_CANVAS[cast], sd, contact=True)
            a.head_flip = False
            T.no_bounce(a.card)
            self.act[n] = a
        self.coll = bpy.data.collections.new("S07_ROPES"); scene.collection.children.link(self.coll)
        self.mats = S04.rope_mats()
        self.ropes, self.rope_xy, self.hand_z = {}, {}, {}
        self.info, self.anch = {}, {}
        if verbose:
            print("s07: built in %.1f s" % (time.time() - t0), flush=True)

    def place_ropes(self):
        if self.ropes:
            return
        g = G_S7
        f = bf(7, g)
        loc, look = cam7(g)
        camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
        for n, a in self.act.items():
            a.place(f, RINGERS[n][2])
        self.scene.frame_set(f)
        for n, a in self.act.items():
            cast, story, feet, up, ph = RINGERS[n]
            p = dict(cast2.STORY2[story][1]); p.pop("prop_l", None); p.pop("prop_r", None)
            if n == "nico":
                p["legs"] = "stand"                # rest = standing on the floor (the dangling legs are 0.32 D higher)
            a.pose(f, p, camera=self.cam)
            fp = sprites.feet_of(cast, p)
            hu, hl, _, _ = rest_hands(n)
            wu = actors.local_to_world(a, hu, f, feet=fp, camera=self.cam)
            wl = actors.local_to_world(a, hl, f, feet=fp, camera=self.cam)
            c = self.cam.matrix_world.to_translation()
            back = (Vector((wu.x, wu.y, 0)) - Vector((c.x, c.y, 0))).normalized() * S04.ROPE_BACK
            x, y = wu.x + back.x, wu.y + back.y
            self.rope_xy[n] = (x, y)
            self.hand_z[n] = (wu.z, wl.z)
            self.ropes[n] = S04.make_rope("rope_" + n, x, y, wl.z - 0.7, self.coll, self.mats, sally=(wl.z - 0.25, wu.z + 0.25))

    def pose(self, shot, gs):
        self.place_ropes()
        for g in gs:
            f = bf(shot, g)
            loc, look = cam7(g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            T.set_bell(bell_angle(g), frame=f, interp="LINEAR")
            for n, a in self.act.items():
                x, y, z = RINGERS[n][2]
                a.place(f, (x, y, z + (dangle_z(g) if n == "nico" else 0.0)))
                r = self.ropes[n]
                r.location = (self.rope_xy[n][0], self.rope_xy[n][1], rope_off(n, g))
                r.keyframe_insert("location", frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for n, a in self.act.items():
                p = ringer_pose(n, g)
                hu, hl, up, lo = rest_hands(n)
                x, y = self.rope_xy[n]
                zu, zl = self.hand_z[n]
                dz = rope_off(n, g)
                hands = {up: {"hand": (x, y, zu + dz), "stretch": 1.3, "bend": -0.6},
                         lo: {"hand": (x, y, zl + dz), "stretch": 1.3, "bend": -0.5}}
                _, inf = a.pose(f, p, hands=hands, camera=self.cam)
                self.info.setdefault(g, {})[n] = [round(inf[s]["error"], 3) for s in (up, lo)]
        fr = [bf(shot, g) for g in gs]
        for n, a in self.act.items():
            ppd = {"nico": 448, "baker": 320, "woman": 320}[n]
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s07: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam7(g)
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads={}, lift=round(lift(g), 3))
        for a in self.act.values():
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        out["pin_err"] = self.info.get(g, {})
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.cycles.samples = samples
        return render.render_frames([bf(shot, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False)


if __name__ == "__main__":
    S04.main(sys.argv, Take=Take, RANGES=RANGES, HERE=HERE)
