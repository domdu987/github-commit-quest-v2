#!/usr/bin/env python3
"""shot.py -- film 24 take s08: shots 8a + 8b (yard).  g 728..924 = 6 in-handle + 8a g 734..860 + 8b g 861..918 + 6 out-handle.
    id 8 (8a) g 728..860  yard macro_spikes: 60 mm f/2.8 on the port roof, yard in bokeh.  set_spikes 0 -> 1 at g 795 (26.4 s), 2 at g 831 (27.6 s),
                          3 at g 852 (28.3 s) (pop-in, a hammer clink on each); slow lateral slide along the roof (2.2 D), focus empty follows the look
                          point (world-fixed, unparented).  No characters (nothing inside the blur).
    id 9 (8b) g 861..924  yard roof_top: high 3/4 over the spiked roof (spikes 3).  set_ports 0 -> 1 over g 882 +- 6 (29.6 s); two kneeling workers on
                          the starboard roof edge (kor_b24 / kor_c24 kneel_hammer, Child-Of the turtle ride, ground anchor on the roof).  Slow push-in.
Blender frame of (id, g) = 1000 * (id - 1) + g + 1.   (ids 8 / 9 here are internal keys: 8 = 8a, 9 = 8b)
    python3 shot.py probe 8,9 a:b[:step] | stills 8,9 a:b[:step] <out> [scale] [samples] | final 8|9 a:b [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
J, actors, cast24 = C.J, C.actors, C.cast24
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
GA, GB, GE = C.g_bound(24.45), C.g_bound(28.70), C.g_bound(30.64)      # 734, 861, 919
H = 6
RANGES = {8: (GA - H, GB - 1), 9: (GB, GE + H - 1)}
PRESET = {8: "macro_spikes", 9: "roof_top"}
G_S1, G_S2, G_S3 = C.g_of(26.4), C.g_of(27.6), C.g_of(28.3)          # 795, 831, 852
G_P = C.g_of(29.6)                                                    # 891 -> ports 0..1 over +-6
SLIDE = 2.2
PUSH9 = 0.16
BEAT = 12
KYAW = None
PPD = dict(k1=64, k2=64)
ROOF = dict(k1="worker_roof_s1", k2="worker_roof_s2")


def spikes_at(g):
    return 0 if g < G_S1 else (1 if g < G_S2 else (2 if g < G_S3 else 3))


def ports_at(g):
    return clamp((g - (G_P - 6)) / 12.0)


def cam_of(shot, g, T):
    pc = T.A["cam"]; loc0, look0 = Vector(pc["loc"]), Vector(pc["look_at"])
    x = (g - RANGES[shot][0]) / float(RANGES[shot][1] - RANGES[shot][0]); u = C.calm(x)
    if shot == 8:
        sh = Vector((0.0, -SLIDE * u, 0.0))                           # along the ship (world y), toward the stern
        return loc0 + sh, look0 + sh, pc["lens"]
    return loc0 + (look0 - loc0) * (PUSH9 * u), look0, pc["lens"]


def _arm(u):
    return dict(hand=(lerp(0.60, 0.78, u), lerp(-0.50, 0.62, u)), bend=lerp(-0.7, -0.2, u), stretch=1.2, layer="front"), lerp(-70.0, 20.0, u)


def hammer_u(g, off):
    p = (g - off) % BEAT
    if p == 0:
        return 1.0
    if p <= 5:
        return 1.0 - ez(p / 5.0)
    if p <= 8:
        return -0.12 * ez((p - 5) / 3.0)
    return lerp(-0.12, 1.0, ((p - 8) / 4.0) ** 1.6)


def pose_k(name, g, off):
    c, p = C.story(name)
    arm, ang = _arm(hammer_u(g, off))
    p["arm_r"] = arm; p["prop_r"] = dict(type="hammer24", angle=ang)
    p["blink"] = blink(g, [off + 20, off + 61]); p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, shot=8):
        C.Take.__init__(self, PRESET[shot], name="cam_s08")
        self.shot = shot
        if shot == 8:
            self.aim_sun(*[self.A["cam"]["loc"], self.A["cam"]["look_at"]])
        else:
            sd = os.path.join(TMP, "sprites")
            self.k = {}
            for key, cast, story_name in (("k1", "kor_b24", "kor_b24_kneel_hammer"), ("k2", "kor_c24", "kor_c24_kneel_hammer")):
                a = self.actors[key] = C.make_actor(key, cast, sd, story=story_name, contact=False)
                C.parent_to_ship(a, "turtle"); a.yaw_fixed = KYAW if KYAW is not None else None
                lp = tuple(self.A["parented"][ROOF[key]]["local"])
                a.lp = lp; a.roofc = C.roof_contact(a, "turtle", lp)
                self.k[key] = a

    def pose(self, shot, gs):
        assert shot == self.shot
        for g in gs:
            f = bf(shot, g); self.scene.frame_set(f)
            loc, look, lens = cam_of(shot, g, self); self.key_cam(f, loc, look, lens=lens)
            if shot == 8:
                self.focus.location = look; self.focus.keyframe_insert("location", frame=f)
                self.key_set(f, spikes=spikes_at(g), ports=0, dragon_smoke=0.0)
            else:
                self.key_set(f, spikes=3, ports=ports_at(g), dragon_smoke=0.0)
                for a in self.k.values():
                    C.place_on_ship(a, f, a.lp)
        if shot == 8:
            return
        for g in gs:
            f = bf(shot, g); self.scene.frame_set(f)
            self.k["k1"].pose(f, pose_k("kor_b24_kneel_hammer", g, 3), camera=self.cam)
            self.k["k2"].pose(f, pose_k("kor_c24_kneel_hammer", g, 8), camera=self.cam)
        self.sprites_for([(a, PPD[n]) for n, a in self.k.items()], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g); self.scene.frame_set(f); loc, look, lens = cam_of(shot, g, self)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f), feet=C.feet_report(self, f),
                    spikes=spikes_at(g), ports=round(ports_at(g), 2))

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]; shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take(shot); Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]; scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.4; samples = int(sys.argv[6]) if len(sys.argv) > 6 else 10
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else C.RES_PCT
        for shot in shots:
            samples = int(sys.argv[5]) if len(sys.argv) > 5 else C.preset_samples(PRESET[shot])
            C.final_loop(lambda s_: Take(s_), [shot], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
