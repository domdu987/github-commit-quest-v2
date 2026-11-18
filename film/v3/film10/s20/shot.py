#!/usr/bin/env python3
"""shot.py -- film 10 take s20: shots 20 + 21 (g 1428..1626, handles g 1422..1427 and g 1627..1632).

    id 20  g 1422..1529  shot 20 (47.59-51.00 s), SEA_DAY bridge_deck: the admiral on the flagship's bridge wing lowers his binoculars,
                         jaw dropped (held open mouth, no lip-sync); the painter next to him grins with folded arms.  The camera and the
                         two cards sail with the flagship (sea time s = 13 + (g - 1428) / 30, after the torpedo run of shots 17-19).
    id 21  g 1530..1632  shot 21 (51.00-54.24 s), harbour_wide DAY, crane move up and back: set_harbour_dazzle k 0 -> 1 (the 6 moored
                         ships, then the 12 in the roads, flip to full dazzle one by one); the berth ship stays at stage 3 (hd1,st3).
Mouths: nobody speaks (no quote in shots 20-21).  NO depth of field.  Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 20,21 a:b[:step]
    python3 shot.py stills 20,21 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 20|21 a:b[:step] [scale] [samples]
"""
import math, os, sys, json, copy, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c10 as C                                          # noqa: E402  (paths, cast10 first, bpy, harbour, stage)
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast10, sprites = C.D, C.actors, C.camrig, C.cast10, C.sprites
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G20, G21, G22 = C.g_bound(47.59), C.g_bound(51.00), C.g_bound(54.24)      # 1428, 1530, 1627
H_IN, H_OUT = 6, 6
RANGES = {20: (G20 - H_IN, G21 - 1), 21: (G21, G22 - 1 + H_OUT)}
LOCS = {20: ("sea", "bridge_deck", "SEA_DAY"), 21: ("harbour", "harbour_wide", "DAY")}
S0 = 13.0                                                # sea time (s) at g = G20: the ships have sailed on after the torpedo run
V = D.SEA_V


def s_of(g):
    return S0 + (g - G20) / 30.0


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def pose_of(name, **kw):
    cast, p = cast10.STORY10[name]
    p = copy.deepcopy(p)
    p.update(kw)
    return cast, p


# ----------------------------------------------------------------------------- shot 20 (sea, bridge wing)
FLAG_PH = random.Random(3).uniform(0, 6.28)              # the flagship's heave driver (harbour._bob(seed 3), CONVOY index 3)


def flag_heave(f):
    return 0.16 * math.sin(f * 0.13 + FLAG_PH)


def _basis20(A):
    """horizontal unit vector f from the preset camera to the admiral, and screen-right r = f x up."""
    c = Vector(A["cams"]["bridge_deck"]["loc"]); m = Vector(A["marks"]["admiral_bridge"])
    f = m - c; f.z = 0; f.normalize()
    return m, f, Vector((f.y, -f.x, 0.0))


CAM_BACK, CAM_UP, CAM_PUSH = 7.4, 1.9, 1.3                # camera distance behind the admiral, height over the deck, push over the shot
PAI_R, PAI_F = 1.75, 0.35                                    # painter: right of the admiral, and behind him (D)
LOOK_F, LOOK_R, LOOK_Z = 4.0, 1.90, 1.55                   # look-at, relative to the admiral's feet (forward, right, up)


def cam20(g, A):
    m, f, r = _basis20(A)
    x = clamp((g - G20) / 102.0)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    sh = Vector((V * s_of(g), 0, 0))
    loc = m + sh - f * (CAM_BACK - CAM_PUSH * u) + Vector((0, 0, CAM_UP)) + r * (0.35 * u)
    look = m + sh + f * LOOK_F + r * (LOOK_R + 0.25 * u) + Vector((0, 0, LOOK_Z))
    return loc, look


ADM_OFF = Vector((0.0, 0.0, 0.0))


def adm20(g):
    """binoculars up (looking at the dazzle ship, the torpedo gone by) -> lowered -> jaw dropped, with a small shake."""
    a = cast10.STORY10["admiral_binoculars_up"][1]
    b = cast10.STORY10["admiral_binoculars_lowered"][1]
    c = cast10.STORY10["admiral_jaw_drop"][1]
    import puppet
    t1, t2 = u_of(g, 1436, 1450), u_of(g, 1448, 1462)
    if t2 > 0:
        p = puppet.lerp_pose("admiral", b, c, t2)
    else:
        p = puppet.lerp_pose("admiral", a, b, t1)
    p = dict(p)
    p["t"] = g / 30.0
    if t2 >= 1:                                          # held jaw drop: a stunned tremble + slow breath
        p["head_dx"] = 0.012 * math.sin(g * 0.9)
        p["squash"] = (1.0 + 0.008 * math.sin(g * 0.21), 1.0 - 0.008 * math.sin(g * 0.21))
        p["lean"] = p.get("lean", 0.0) + 1.5 * math.sin(g * 0.11)
    p["blink"] = blink(g, [1442, 1493])
    p["gaze"] = (0.95, 0.0)                               # eye-line toward the dazzle ship
    return p


def pai20(g):
    cast, p = pose_of("painter_grin")
    p["head_roll"] = 6 + 2.0 * math.sin(g * 0.13)
    p["lean"] = 1.2 * math.sin(g * 0.09)
    p["mouth"] = "grin"                                   # one held grin, never toggled
    p["pitch"] = -0.05
    p["gaze"] = (0.95, 0.05)                              # eye-line out to sea / the dazzle ship (screen-right)
    p["blink"] = blink(g, [1470, 1512])
    return p


# ----------------------------------------------------------------------------- shot 21 (harbour_wide crane move)
HW = None


def cam21(g, A):
    c = A["cams"]["harbour_wide"]
    x = (g - G21) / float(G22 - G21 + H_OUT)
    u = 0.3 * ez(clamp(x), "sine") + 0.7 * clamp(x)
    loc = Vector(lerp_v(CAM21_A[0], CAM21_B[0], u))
    look = Vector(lerp_v(CAM21_A[1], CAM21_B[1], u))
    return loc, look


def lerp_v(a, b, u):
    return tuple(lerp(a[i], b[i], u) for i in range(3))


CAM21_A = ((-40.0, -30.0, 25.0), (10.0, 26.0, 0.0))      # low, close: the quay and the berth ship, a few ships behind
CAM21_B = ((-60.0, -42.0, 42.0), (16.0, 42.0, 0.0))     # crane up and back: the whole basin and the roads
LENS21 = 20.0
HD_G = (G21 + 6, G22 - 10)                               # k 0 -> 1 across the shot (the last ship flips ~10 frames before the cut)

# the quay figures of shot 21 (small, cheering the dazzle ships)
QUAY21 = [("painter", "painter10", "painter_quay"), ("sailor_a", "sailor_a", "sailor_quay_a"), ("sailor_b", "sailor_b", "sailor_quay_b"),
          ("sailor_c", "sailor_c", "sailor_quay_c")]


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=20):
        loc, preset, light = LOCS[shot]
        lens = 24.0 if shot == 20 else LENS21
        C.Take.__init__(self, loc, preset, quality=quality, lens=lens, name="cam_s20", light=light)
        self.shot = shot
        if shot == 21:                                       # QA-tech: no mirrored ships (they read as translucent blue panels on the water)
            self.scene.cycles.glossy_bounces = 0
        for ob in D.STATE.get("cards", []):               # the set's placeholder background cards (old cast): hidden, cast10 sailors replace them
            ob.hide_render = True
        sd = os.path.join(TMP, "sprites")
        if shot == 20:
            self.adm = self.actors["adm"] = C.make_actor("adm", "admiral", sd)
            self.pai = self.actors["pai"] = C.make_actor("pai", "painter10", sd)
        else:
            self.fig = {}
            for nm, cast, mk in QUAY21:
                self.fig[nm] = self.actors[nm] = C.make_actor(nm, cast, sd)

    # -- per shot set-up
    def pose(self, shot, gs):
        A = self.A
        if shot == 20:
            _, ff, rr = _basis20(A)
            mk_a = Vector(A["marks"]["admiral_bridge"]) - ff * 0.9             # a step toward us: the wing rail stays behind their legs
            mk_p = mk_a + rr * PAI_R - ff * PAI_F
            for g in gs:
                f = bf(shot, g)
                loc, look = cam20(g, A)
                self.key_cam(f, loc, look, lens=24.0)
                s = s_of(g)
                self.key_set(f, convoy=s)
                sh = Vector((V * s, 0, flag_heave(f)))
                C.place(self.adm, f, mk_a + sh)
                C.place(self.pai, f, mk_p + sh)
            for g in gs:
                f = bf(shot, g)
                self.scene.frame_set(f)
                self.adm.pose(f, adm20(g), camera=self.cam)
                self.pai.pose(f, pai20(g), camera=self.cam)
            fr = [bf(shot, g) for g in gs]
            self.sprites_for([(self.adm, 288), (self.pai, 256)], fr)
        else:
            for g in gs:
                f = bf(shot, g)
                loc, look = cam21(g, A)
                self.key_cam(f, loc, look, lens=LENS21)
                k = clamp((g - HD_G[0]) / float(HD_G[1] - HD_G[0]))
                self.key_set(f, harbour_dazzle=ez(k, "sine") * 0.35 + 0.65 * k, stripes=3.0)
                for nm, cast, mk in QUAY21:
                    C.place(self.fig[nm], f, A["marks"][mk])
            for g in gs:
                f = bf(shot, g)
                self.scene.frame_set(f)
                for nm, cast, mk in QUAY21:
                    self.fig[nm].pose(f, self.quay_pose(nm, g), camera=self.cam)
            fr = [bf(shot, g) for g in gs]
            self.sprites_for([(a, 160) for a in self.fig.values()], fr)

    def quay_pose(self, nm, g):
        ph = {"painter": 0, "sailor_a": 7, "sailor_b": 13, "sailor_c": 3}[nm]
        if nm == "painter":
            cast, p = pose_of("painter_step_back_proud")
            p["lean"] = p.get("lean", 0.0) + 1.5 * math.sin(g * 0.1)
        else:
            sfx = nm[-2:]                                # _a / _b / _c
            cheer = u_of(g, G21 + 10 + ph, G21 + 30 + ph)
            cast, p = pose_of("sailor_point_laugh" + sfx)
            p["t"] = (g + ph) / 30.0
            p["lean"] = p.get("lean", 0.0) + 2.5 * math.sin(g * 0.3 + ph)
            p["head_roll"] = p.get("head_roll", 0.0) + 3.0 * math.sin(g * 0.37 + ph)
        p["blink"] = blink(g, [G21 + 20 + 7 * ph % 40])
        return p

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam20(g, self.A) if shot == 20 else cam21(g, self.A)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def main():
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take("preview", shot)
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples,
                     take_key=lambda shot: LOCS[shot][0])


if __name__ == "__main__":
    main()
