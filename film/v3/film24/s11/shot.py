#!/usr/bin/env python3
"""shot.py -- film 24 take s11: shot 11 (sea chase), g 1113..1256 + 6 handle frames each side (1107..1262).
On the bow deck of the nearest Japanese ship j_near three varied ashigaru (ashi_a24 / ashi_c24 / ashi_d24, sword_raise, planted, one mirrored)
raise their katanas; the fleet charges (set_fleet_chase keyed every frame).  Camera: the preset chase camera travelling with the ship
plus one slow lateral slide along the deck (0 -> 3.2 D to the camera's right side).  No quote: mouths fixed ("clench").  Blender frame = 10000 + g + 1.
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
J, actors, cast24 = C.J, C.actors, C.cast24
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

SHOT = 11
G0, G1 = C.g_bound(37.09), C.g_bound(41.91) - 1          # 1113..1256
H = 6
RANGE = {SHOT: (G0 - H, G1 + H)}
PRESET = {SHOT: "chase"}
SLIDE = -1.6
CAMX, CAMY, CAMZ = 6.0, 5.2, 10.0
PPD = dict(a=224, b=224, c=224)
MEM = dict(a="ashi_a24", b="ashi_c24", c="ashi_d24")
MIRROR = dict(a=False, b=True, c=False)
SPOT = dict(a="soldier_chase_a", b="soldier_chase_b", c="soldier_chase_c")


def chase_s(g):
    return (g - RANGE[SHOT][0]) / 30.0


def cam_of(A, g):
    pc = A["cam"]
    if "loc2" in A:
        pc = dict(pc, loc=A["loc2"], look_at=A["look2"])
    x = (g - RANGE[SHOT][0]) / float(RANGE[SHOT][1] - RANGE[SHOT][0])
    u = C.calm(x)
    loc0, look0 = Vector(pc["loc"]), Vector(pc["look_at"])
    fwd = (look0 - loc0); fwd.z = 0; fwd.normalize()
    right = fwd.cross(Vector((0, 0, 1)))
    off = Vector((J.CHASE_V * chase_s(g), 0, 0)) + right * (SLIDE * u)
    return loc0 + off, look0 + off, pc["lens"]


def pose_s(k, g):
    c, p = C.story(MEM[k] + "_sword_raise")
    p["mirror"] = MIRROR[k]
    ph = {"a": 0.0, "b": 1.9, "c": 3.7}[k]
    p["lean"] = p.get("lean", 0) + 1.8 * math.sin(g * 0.16 + ph)               # eager sway, feet planted
    p["head_roll"] = p.get("head_roll", 0) + 1.5 * math.sin(g * 0.11 + ph)
    pr = dict(p["prop_r"]); pr["angle"] = pr["angle"] + 5.0 * math.sin(g * 0.2 + ph); p["prop_r"] = pr   # the blade waves
    p["blink"] = blink(g, [1130 + 13 * len(k) + ord(k), 1200 + ord(k)])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, shot=SHOT):
        C.Take.__init__(self, PRESET[shot], name="cam_s11")
        sd = os.path.join(TMP, "sprites")
        P = self.A["parented"]
        xn = J._fl("j_near")["deck_x"][1]
        self.A["loc2"] = tuple(J.L2W("j_near", (xn + CAMX, -CAMY, CAMZ)))
        self.A["look2"] = tuple(J.L2W("j_near", (xn - 1.8, 0.4, J._fl("j_near")["deck_z"] + 1.6)))
        self.lp = {}
        for k in "abc":
            a = self.actors[k] = C.make_actor(k, MEM[k], sd, contact=False)
            self.ship = P[SPOT[k]]["ship"]
            C.parent_to_ship(a, self.ship)
            self.lp[k] = tuple(P[SPOT[k]]["local"])
            C.roof_contact(a, self.ship, self.lp[k], width=1.5, depth=0.7, normal=(0, 0, 1))

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(self.A, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, spikes=3, ports=0, dragon_smoke=0.0, fleet_chase=chase_s(g), korean_turn=0.0, damage=0.0, cannon_smoke=0.0)
            for k in self.lp:
                C.place_on_ship(self.actors[k], f, self.lp[k])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for k in self.lp:
                self.actors[k].pose(f, pose_s(k, g), camera=self.cam)
        self.sprites_for([(self.actors[k], PPD[k]) for k in self.lp], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(self.A, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f), feet=C.feet_report(self, f))

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills"):
        gs = [g for g in C.parse(sys.argv[2]) if RANGE[SHOT][0] <= g <= RANGE[SHOT][1]]
        Tk = Take(SHOT)
        Tk.pose(SHOT, gs)
        for g in gs:
            print(json.dumps(Tk.report(SHOT, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.4
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 10
                st = Tk.render(SHOT, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (SHOT, g)))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else C.RES_PCT
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else C.preset_samples(PRESET[SHOT])
        C.final_loop(lambda s_: Take(s_), [SHOT], sys.argv[2], RANGE, HERE, scale=scale, samples=samples)
