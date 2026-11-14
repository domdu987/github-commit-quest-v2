#!/usr/bin/env python3
"""shot.py -- film 5 take s01: shots 1-4 (the opening, g 0..314 + 7 handle frames), mine set (tunnel LAMP + pithead DUSK).

    shot 1  g   0.. 41  tunnel, medium eye level: alfie raises the brass cage (3D set cage carried in his hand, the canary sprite
                        on its perch) beside his face; miners in depth behind him; slow push (ref a t0001)
    shot 2  g  42.. 80  hard cut, ECU of the canary singing, 5 notes floating up, framed between two cage wires, the hanging lamp
                        and the warm lamp-lit wall behind; push + rise with the notes (ref a t0003)
    shot 3  g  81..156  hard cut, low angle looking outbye: alfie (cage held up on screen-left) points at the bird (g 86..93 on
                        "ถ้าเสียงมัน"), snap punch-in g 119..127 (middle g 123 = plan t 4.0), then flings the point at the bright
                        exit (screen-right, lands g 135 on "ให้วิ่ง"); mouth closed throughout (ref a t0007 / t0009)
    shot 4  g 157..314  4a pithead DUSK high establishing, crane down toward the bank (g 157..205);
                        12-frame dissolve (g 200..211) down into 4b the tunnel (eye level, gas haze drifting, push, g 206..250);
                        4c cut to the hanging lamp in the haze (g 251..287); 4d cut, low under the roof lamps, the haze layers
                        drifting past the flame (g 288..314, handle g 315..321)  (ref a t0029-t0033)
NO depth of field anywhere (client note): every render calls M.setup_dof(scene, None, None).

Internal shot ids: 1, 2, 3, 4 (=4a), 5 (=4b), 6 (=4c), 7 (=4d).  Blender frame of (id s, film frame g) = 1000 * (s - 1) + g + 1.

    python3 shot.py probe <ids> a:b[:step]
    python3 shot.py stills <ids> a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final <ids> a:b[:step] [scale] [samples]
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
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

TMP = os.path.join(HERE, "work")


def g_of(t):                     # narration time -> film frame of an event
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing (round(t*30) bounds)
G_S2, G_S3, G_S4, G_END, H_OUT = 42, 81, 157, 315, 7          # 1.40, 2.70, 5.22, 10.50
G_4B, G_4C, G_4D = 206, 251, 288
DISS = 12
HANDLE = DISS // 2 + 2                                          # 8
RANGES = {1: (0, G_S2 - 1), 2: (G_S2, G_S3 - 1), 3: (G_S3, G_S4 - 1), 4: (G_S4, G_4B + HANDLE - 1),
          5: (G_4B - HANDLE, G_4C - 1), 6: (G_4C, G_4D - 1), 7: (G_4D, G_END + H_OUT - 1)}
LOC = {1: "tunnel", 2: "tunnel", 3: "tunnel", 4: "pithead", 5: "tunnel", 6: "tunnel", 7: "tunnel"}
# events (captions.json, narration_bankky.wav at +0.10 s)
G_RAISE = (0, 14)                # shot 1: the cage comes up beside his face
G_PBIRD = g_of(2.75)             # 86 "ถ้าเสียงมัน": point at the bird lands (arm from 83)
PUNCH = (119, 127)               # plan "punch-in at 4.0": middle g 123
G_PEXIT = g_of(4.41)             # 135 "ให้วิ่งทันที": point at the exit lands (arm from 128)
G_LOOK = 141                     # alfie turns from the exit to the audience


GRIP = Vector((0, 0, 0.04))      # the fist closes on top of the ring loop (above the dome, so the cage never hides it)


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


def _ez(u, kind="sine"):
    return ease(clamp(u), kind)


def _lerpv(a, b, u):
    return a + (b - a) * u


# ----------------------------------------------------------------------------- staging (tunnel)
TP = M.TP
ALFIE_1 = TP(6.6, -0.95, 0)
MINERS_1 = {"miner1": TP(10.0, 1.05, 0), "miner2": TP(12.4, 1.45, 0), "miner3": TP(18.5, -0.2, 0)}
ALFIE_3 = TP(10.7, -0.10, 0)

# shot 1: eye level just below alfie's eyes, alfie screen-left, cage beside his face screen-right, miners in depth; slow push
CAM1_A = (TP(3.55, 0.05, 1.82), TP(7.6, -0.58, 2.02))
CAM1_B = (TP(3.90, 0.0, 1.85), TP(7.6, -0.60, 2.04))
# shot 3: low, between the tub train and the left wall, looking outbye; exit (bright pit bottom) right of alfie; punch-in
CAM3_A = (TP(14.4, -1.15, 0.95), TP(9.0, 0.60, 2.05))
CAM3_B = (TP(14.25, -1.12, 0.95), TP(9.0, 0.60, 2.07))
CAM3_C = (TP(13.55, -0.92, 1.05), TP(9.0, 0.78, 2.12))
CAM3_D = (TP(13.45, -0.90, 1.05), TP(9.0, 0.78, 2.13))
# shot 4b: tunnel wide at eye level, slow push inbye
CAM5_A = (TP(1.3, -0.35, 2.45), TP(19.0, 0.25, 2.25))
CAM5_B = (TP(3.3, -0.30, 2.40), TP(19.0, 0.20, 2.25))
# shot 4a: pithead, high establishing, crane down and push toward the bank
CAM4_A = (Vector((13.0, -33.0, 15.0)), Vector((-3.0, 12.0, 12.5)))
CAM4_B = (Vector((10.5, -27.0, 8.5)), Vector((-1.0, 12.0, 6.0)))


def _pk(a, b):
    return tuple(a) + tuple(b)


def _cam(g, ks):
    k = keys(g, ks)
    return Vector(k[:3]), Vector(k[3:])


def cam1(g):
    g0, g1 = RANGES[1]
    return _cam(g, [(g0, _pk(*CAM1_A), "cubic_out"), (g1 + 1, _pk(*CAM1_B), "hold")])


def cam3(g):
    g0, g1 = RANGES[3]
    return _cam(g, [(g0, _pk(*CAM3_A), "sine"), (PUNCH[0], _pk(*CAM3_B), "quint"), (PUNCH[1], _pk(*CAM3_C), "sine"),
                    (g1 + 1, _pk(*CAM3_D), "hold")])


def cam4(g):
    g0, g1 = RANGES[4]
    return _cam(g, [(G_S4, _pk(*CAM4_A), "sine"), (g1 + 1, _pk(*CAM4_B), "hold")])


def cam5(g):
    g0, g1 = RANGES[5]
    return _cam(g, [(g0, _pk(*CAM5_A), "lin"), (g1 + 1, _pk(*CAM5_B), "hold")])


# ----------------------------------------------------------------------------- poses
def alfie_s1(g, ring_screen_ok=True):
    p = dict(cast5.STORY5["alfie_hold_cage"][1])
    p.pop("prop_r", None); p.pop("bird", None)
    p["expr"] = "happy"
    p["arm_r"] = dict(bend=-0.9, stretch=1.3)
    u = _ez((g - G_RAISE[0]) / float(G_RAISE[1] - G_RAISE[0]), "cubic_out")
    p["head_roll"] = -6 + 3 * math.sin(g * 0.12)
    p["gaze"] = (lerp(0.3, 0.8, u), lerp(0.2, -0.2, u))
    p["lean"] = 2 * math.sin(g * 0.09)
    p["blink"] = blink(g, [28])
    return p


CAGE_SCALE = 1.45                # held 2D cage (cast5 prop "cage"): bird head ~0.26 D -> 65-80 px in shots 1 / 3


def held_cage(g, shot):
    """the cast's 2D held cage: prop dict + the canary inside (pose key 'bird'), front bars drawn over the bird."""
    return dict(type="cage", scale=CAGE_SCALE), dict(state="perch_sing", notes=3, beak=0.7 + 0.2 * math.sin(g * 0.9), t=g / 30.0,
                                                    swing=2.5 * math.sin(g * 0.21))


def alfie_s1_held(g):
    """shot 1: the 2D cage in his screen-right hand, raised from the hip to beside his face (g 0..14)."""
    p = alfie_s1(g)
    u = _ez((g - G_RAISE[0]) / float(G_RAISE[1] - G_RAISE[0]), "cubic_out")
    hand = (lerp(0.52, 0.78, u), lerp(0.55, -0.40, u) + 0.015 * math.sin(g * 0.21))
    p["arm_r"] = dict(hand=hand, bend=lerp(0.3, -0.9, u), stretch=1.3)
    p["prop_r"], p["bird"] = held_cage(g, 1)
    return p


def alfie_s3(g):
    p = dict(yaw=-0.25, pitch=-0.25, expr="determined", mouth="frown", legs="wide", head_roll=-3)
    ub = _ez((g - (G_PBIRD - 3)) / 4.0, "back_out") if g >= G_PBIRD - 3 else 0.0       # arm across to the bird
    ue = _ez((g - (G_PEXIT - 7)) / 8.0, "back_out") if g >= G_PEXIT - 7 else 0.0        # arm out to the exit
    rest = (0.40, 0.95)
    bird = (-0.38, 0.62)
    ex = (0.95, 0.22)
    hand = (lerp(lerp(rest[0], bird[0], ub), ex[0], ue), lerp(lerp(rest[1], bird[1], ub), ex[1], ue))
    p["arm_r"] = dict(hand=hand, shape="point" if (ub > 0.3 or ue > 0.3) else "fist", bend=lerp(lerp(0.6, -0.3, clamp(ub)), -0.5, clamp(ue)),
                      stretch=1.3, layer="front")
    turn_e = _ez((g - (G_PEXIT - 7)) / 6.0) if g >= G_PEXIT - 7 else 0.0
    turn_c = _ez((g - G_LOOK) / 6.0) if g >= G_LOOK else 0.0
    yaw = lerp(lerp(-0.35, 0.55, turn_e), 0.2, turn_c)
    p["yaw"] = yaw
    p["gaze"] = (lerp(lerp(-0.8, 0.9, turn_e), 0.05, turn_c), lerp(lerp(-0.4, 0.0, turn_e), 0.0, turn_c))
    p["pitch"] = lerp(-0.3, 0.0, turn_c)
    jab = pulse(g, G_PEXIT - 1, G_PEXIT + 2, G_PEXIT + 9, 1.0)
    p["lean"] = 2 + 4 * jab + 3 * ub * (1 - ue)
    p["head_roll"] = -4 + 3 * jab - 2 * math.sin(g * 0.13)
    p["blink"] = blink(g, [104, 148])
    p["arm_l"] = dict(hand=(-0.74, -0.40 + 0.015 * math.sin(g * 0.21)), bend=-0.8, stretch=1.3)      # 2D cage held up, screen-left
    p["prop_l"], p["bird"] = held_cage(g, 3)
    return p


MINER_POSE = {
    "miner1": dict(yaw=0.35, pitch=-0.1, expr="neutral", arm_l=dict(hand=(-0.42, 0.55), bend=0.5), prop_l=dict(type="flame_lamp"),
                   arm_r="down", legs="stand", flame=1.0),
    "miner2": dict(cast5.STORY5["miners_work_miner2"][1]),
    "miner3": dict(yaw=-0.4, pitch=-0.1, expr="neutral", arm_l="down", arm_r=dict(hand=(0.42, 0.62), bend=-0.5, stretch=1.2),
                   prop_r=dict(type="pickaxe", angle=35), legs="stand"),
}


def miner_pose(n, g):
    p = dict(MINER_POSE[n])
    off = {"miner1": 0, "miner2": 5, "miner3": 11}[n]
    p["t"] = g / 30.0
    p["head_roll"] = p.get("head_roll", 0) + 3 * math.sin(g * 0.11 + off)
    if n == "miner2":                                           # slow digging
        d = 0.5 - 0.5 * math.cos(2 * math.pi * (g + off) / 34.0)
        p["arm_r"] = dict(p["arm_r"], hand=(0.55, 0.72 - 0.12 * d))
        p["lean"] = 14 + 5 * d
    p["blink"] = blink(g, [12 + off, 33 + off])
    return p


def bird_pose(shot, g):
    if shot == 2:
        return dict(state="perch_sing", notes=5, beak=0.75 + 0.2 * math.sin(g * 0.9), t=g / 30.0)
    return dict(state="perch_sing", notes=3 if shot == 1 else 3, beak=0.7 + 0.2 * math.sin(g * 0.9), t=g / 30.0)


# ----------------------------------------------------------------------------- the take
CANVAS_ALFIE = (-1.875, -3.875, 1.875, 0.1875)
CANVAS_BIRD = (-0.75, -1.25, 0.875, 0.125)


class Take(object):
    def __init__(self, loc, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.loc = loc
        self.A = M.build(loc, "DUSK" if loc == "pithead" else None)
        M.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"   # ACCURATE tested (work/pf/crops.png): same detail, +12 CPU s
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 8000
        self.cam = camrig.make_camera(scene, name="cam_s01")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 600
        M.setup_dof(scene, None, None, cam=self.cam)
        self.actors = {}
        self.anch = {}
        self.lamps = {}
        self.ring = {}
        if loc == "tunnel":
            sd = os.path.join(TMP, "sprites")
            a = actors.Actor("alfie", "alfie"); a.build(CANVAS_ALFIE, sd, contact=True); self.actors["alfie"] = a
            for n in ("miner1", "miner2", "miner3"):
                a = actors.Actor(n, n); a.build(sprites.DEFAULT_CANVAS[n], sd, contact=True); self.actors[n] = a
            b = actors.Actor("bird", "canary"); b.build(CANVAS_BIRD, sd, shadow=None); self.actors["bird"] = b
            for a in self.actors.values():
                a.head_flip = False
                M.no_bounce(a.card)
            c = self.A["cage"]
            self.perch_off = Vector(c["perch"]) - Vector(c["hook"])
            self._gas_drift_nodes()
        if verbose:
            print("s01: built %s in %.1f s" % (loc, time.time() - t0), flush=True)

    # -- gas drift: offset the haze pattern's position input (keyed), so the layers slide past the lamps
    def _gas_drift_nodes(self):
        m = M.STATE.get("gas_mat")
        nt = m.node_tree
        geo = [n for n in nt.nodes if n.bl_idname == "ShaderNodeNewGeometry"][0]
        sep = [n for n in nt.nodes if n.bl_idname == "ShaderNodeSeparateXYZ"][0]
        add = nt.nodes.new("ShaderNodeVectorMath"); add.operation = "ADD"; add.name = "s01_drift"
        nt.links.new(geo.outputs["Position"], add.inputs[0]); nt.links.new(add.outputs[0], sep.inputs[0])
        self.drift = add

    def gas(self, f, g, density):
        M.set_gas(density, frame=f)
        v = self.drift.inputs[1]
        v.default_value = (0.0, -0.9 * g / 30.0, 0.10 * math.sin(g / 30.0 * 1.3))
        v.keyframe_insert("default_value", frame=f)

    def cam_of(self, shot, g):
        if shot == 1: return cam1(g)
        if shot == 3: return cam3(g)
        if shot == 4: return cam4(g)
        if shot == 5: return cam5(g)
        if shot == 2: return self.cam2(g)
        if shot == 6: return self.cam6(g)
        if shot == 7: return self.cam7(g)

    # shot 2: ECU of the bird between two wires, the cage held where shot 1 left it
    def cam2(self, g):
        """ECU: camera level with the perch (so the perch dowel lines up under the bird's feet), from the +x side between two
        wires; the bird card stands just in front of the front wires; slow orbit + push, tilt up with the notes."""
        perch = self.ring_high + self.perch_off
        g0, g1 = RANGES[2]
        u = _ez((g - g0) / float(g1 + 1 - g0), "sine")
        az = math.radians(lerp(8.0, 15.0, u))
        d = Vector((math.cos(az), math.sin(az), 0.0)); sr = Vector((-d.y, d.x, 0.0))      # sr = screen right
        loc = perch + d * lerp(1.04, 0.74, u) + Vector((0, 0, 0.02))
        look = perch + sr * lerp(0.17, 0.12, u) + Vector((0, 0, lerp(0.34, 0.24, u)))
        return loc, look

    def cam6(self, g):
        L = Vector(self.A["fixed_lamps"][1])                    # y 13.75, right side
        g0, g1 = RANGES[6]
        u = (g - g0) / float(g1 + 1 - g0)
        loc = TP(12.0 + 0.35 * u, 0.15 - 0.05 * u, 3.05 + 0.08 * u)
        look = L + Vector((0, 0, -0.30 + 0.04 * u))
        return loc, look

    def cam7(self, g):
        L = Vector(self.A["fixed_lamps"][2])                    # y 18.75, left side
        g0, g1 = RANGES[7]
        u = (g - g0) / float(g1 + 1 - g0)
        loc = TP(15.4 + 0.5 * u, -0.45, 1.25 + 0.1 * u)
        look = L + Vector((0.0, 1.2, -0.1))
        return loc, look

    # -- the cage ring: shot 1 rises from his hip to beside his face; shot 3 held up on screen-left
    def ring_points(self):
        cam = self.cam; a = self.actors["alfie"]
        gm = (RANGES[1][0] + RANGES[1][1]) // 2; f = bf(1, gm)
        loc, look = cam1(gm)
        camrig.key_camera(f, loc, look, cam=cam, interp="LINEAR", easing="AUTO"); a.place(f, ALFIE_1)
        self.scene.frame_set(f)
        tc = (loc - ALFIE_1); tc.z = 0; tc.normalize()
        self.ring_high = actors.local_to_world(a, (0.56, -0.10), f) - tc * 0.28
        self.ring_low = actors.local_to_world(a, (0.50, 0.50), f) - tc * 0.28
        g3 = RANGES[3][0]; f3 = bf(3, g3)
        loc, look = cam3(g3)
        camrig.key_camera(f3, loc, look, cam=cam, interp="LINEAR", easing="AUTO"); a.place(f3, ALFIE_3)
        self.scene.frame_set(f3)
        tc = (loc - ALFIE_3); tc.z = 0; tc.normalize()
        self.ring_3 = actors.local_to_world(a, (-0.56, -0.20), f3) - tc * 0.28

    def ring_at(self, shot, g):
        bob = Vector((0, 0, 0.015 * math.sin(g * 0.21)))
        if shot == 1:
            u = _ez((g - G_RAISE[0]) / float(G_RAISE[1] - G_RAISE[0]), "cubic_out")
            return _lerpv(self.ring_low, self.ring_high, u) + bob
        if shot == 2:
            return self.ring_high + bob
        if shot == 3:
            return self.ring_3 + bob
        return None

    def visible(self, shot):
        A = self.actors
        if not A:
            return
        A["alfie"].set_hidden(shot not in (1, 2, 3))
        for n in ("miner1", "miner2", "miner3"):
            A[n].set_hidden(shot != 1)
        A["bird"].set_hidden(shot != 2)
        cg = bpy.data.objects.get("canary_cage")
        if cg is not None:
            cg.hide_render = shot in (1, 3)                       # held 2D cage in shots 1 / 3 (client note); 3D cage only in the ECU

    def pose(self, shot, gs):
        self.visible(shot)
        if self.actors and not hasattr(self, "ring_high"):
            self.ring_points()
        for g in gs:
            f = bf(shot, g)
            loc, look = self.cam_of(shot, g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            if self.loc == "tunnel":
                M.set_drips(f)
                ring = self.ring_at(shot, g)
                M.set_cage(ring, frame=f)
                self.gas(f, g, 0.0 if shot in (1, 2, 3) else {5: 2.0, 6: 2.4, 7: 2.4}[shot])
                if ring is not None:
                    b = self.actors["bird"]
                    perch = ring + self.perch_off
                    if shot == 2:                                      # bird a little in front of the cross dowel
                        loc2, _ = self.cam2(g); d = loc2 - perch; d.z = 0; d.normalize(); perch = perch + d * 0.27
                    b.place(f, tuple(perch))
                if shot == 1:
                    self.actors["alfie"].place(f, ALFIE_1)
                    for n, p in MINERS_1.items():
                        self.actors[n].place(f, p)
                elif shot == 2:
                    self.actors["alfie"].place(f, ALFIE_1)
                elif shot == 3:
                    self.actors["alfie"].place(f, ALFIE_3)
        if self.loc != "tunnel":
            return
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            ring = self.ring_at(shot, g)
            if shot == 1:
                self.actors["alfie"].pose(f, alfie_s1_held(g), camera=self.cam)
                for n in ("miner1", "miner2", "miner3"):
                    self.actors[n].pose(f, miner_pose(n, g), camera=self.cam)
            elif shot == 2:
                self.actors["alfie"].pose(f, alfie_s1(g), hands={"r": {"hand": tuple(ring + GRIP)}}, camera=self.cam)
            elif shot == 3:
                self.actors["alfie"].pose(f, alfie_s3(g), camera=self.cam)
            if shot == 2:
                self.actors["bird"].pose(f, bird_pose(shot, g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        jobs = []
        if shot == 1:
            jobs = [(self.actors["alfie"], 384)] + [(self.actors[n], 160) for n in ("miner1", "miner2", "miner3")]
        elif shot == 2:
            jobs = [(self.actors["bird"], 2048), (self.actors["alfie"], 768)]
        elif shot == 3:
            jobs = [(self.actors["alfie"], 448)]
        for a, ppd in jobs:
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s01: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)
        self.key_lamps(shot, gs)

    def key_lamps(self, shot, gs):
        """actor-carried lamps (keyed lamp_light): alfie's belt lamp, miner1's flame lamp; shot 2 adds a warm rim lamp behind the cage."""
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            loc, _ = self.cam_of(shot, g)
            on = {}
            if shot in (1, 2, 3):
                a = self.actors["alfie"]
                fa = f if shot != 2 else bf(1, RANGES[1][1])
                if shot == 2:
                    p = self.ring_high + Vector((0, 0, -1.05)) + Vector((-0.25, -0.15, 0))
                else:
                    an = self.anch[("alfie", f)]
                    hx, hy = an["hip"]
                    p = actors.local_to_world(a, (hx + 0.30, hy + 0.12), f)
                    tc = loc - p; tc.z = 0; tc.normalize(); p = p + tc * 0.12
                on["lamp_alfie"] = (p, 0.75)
            if shot == 1:
                a = self.actors["miner1"]; an = self.anch[("miner1", f)]
                p = actors.local_to_world(a, an["prop_tip_l"], f)
                tc = loc - p; tc.z = 0; tc.normalize()
                on["lamp_miner1"] = (p + tc * 0.08, 1.0)
            if shot == 2:
                bird = self.ring_high + self.perch_off
                d = loc - bird; d.z = 0; d.normalize()
                on["lamp_rim"] = (bird - d * 0.55 + Vector((0, 0, 0.30)), 0.12)
                on["lamp_key"] = (bird + d * 0.9 + Vector((-0.1, 0.5, 0.45)), 0.15)
            for name in ("lamp_alfie", "lamp_miner1", "lamp_rim", "lamp_key"):
                pos, s = on.get(name, (Vector((0, -30, 1)), 0.0))
                self.lamps[name] = M.lamp_light(tuple(pos), s, frame=f, name=name)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = self.cam_of(shot, g)
        v = look - loc
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={})
        for a in self.actors.values():
            if a.card.hide_render or (a.name, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            hr = 0.5 if a.name != "bird" else 0.09
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - hr, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + hr, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        pts = {}
        if self.loc == "tunnel":
            pts = {"exit": (0.0, -2.0, 1.5), "pit_bottom_far": (0.0, -8.0, 2.0)}
            ring = self.ring_at(shot, g) if self.actors else None
            if ring is not None and shot == 2:
                pts["ring"] = tuple(ring + GRIP); pts["perch"] = tuple(ring + self.perch_off)
            if shot in (1, 3):                                   # held 2D cage: ring = the fist; bird head ~0.18 D x CAGE_SCALE
                a = self.actors["alfie"]; side = "r" if shot == 1 else "l"; res = a.feet.get(f)
                hx, hy = self.anch[("alfie", f)]["hand_" + side]
                hp = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
                hq = actors.local_to_screen(a, self.cam, (hx + 0.18 * CAGE_SCALE, hy), f, res)
                bq = actors.local_to_screen(a, self.cam, (hx, hy + 0.45 * CAGE_SCALE), f, res)
                out["hand_px"] = [round(hp[0], 1), round(hp[1], 1)]
                out["heads"]["bird_in_held_cage"] = dict(x=round(bq[0], 1), y=round(bq[1], 1), w=round(math.hypot(hq[0] - hp[0], hq[1] - hp[1]), 1))
        else:
            pts = {"wheel": (0, 12, 23.6), "gate": (0, 10.1, 1.4), "chimney_top": (-23, 27, 36), "hut": (11.5, -4, 2)}
        out["pts"] = {k: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for k, p in pts.items()}
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(shot)
        self.scene.camera = self.cam
        M.setup_dof(self.scene, None, None, cam=self.cam)        # client note: no depth of field, ever
        self.scene.cycles.samples = samples
        return render.render_frames([bf(shot, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
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


def _take_for(cache, loc, quality):
    if cache.get("loc") != loc:
        actors.clear_registry() if hasattr(actors, "clear_registry") else None
        cache["T"] = Take(loc, quality=quality); cache["loc"] = loc
    return cache["T"]


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    cache = {}
    if cmd in ("probe", "stills"):
        for shot in shots:
            Tk = _take_for(cache, LOC[shot], "preview")
            gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                gs = [RANGES[shot][0], (RANGES[shot][0] + RANGES[shot][1]) // 2, RANGES[shot][1]]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            out = os.path.join(HERE, "raw", "s%d" % shot)
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
            Tk = _take_for(cache, LOC[shot], "final")
            Tk.pose(shot, todo)
            for g in todo:
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(shot, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
