#!/usr/bin/env python3
"""shot.py -- film 24 take s07: shot 7 (sea flag_deck_crew), g 644..733 + 6 handle frames each side (638..739).
Four different ashigaru on the open flagship deck (anchors soldier_deck_a..d, parented to jflag's ride) laugh and point at the turtle ship
(laugh_point), hips bouncing (legs crouch oscillation) with the feet planted.  Camera: the preset flag_deck_crew camera, one slow lateral
slide (SLIDE D along the deck) travelling with the fleet (set_fleet_chase keyed every frame).  No quote: mouths fixed (laughing).
Blender frame = 6000 + g + 1.
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
J, actors, cast24 = C.J, C.actors, C.cast24
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

SHOT = 7
G0, G1 = C.g_bound(21.47), C.g_bound(24.45) - 1          # 644..733
H = 6
RANGE = {SHOT: (G0 - H, G1 + H)}
PRESET = {SHOT: "flag_deck_crew"}
SLIDE = 0.9
SPOT = dict(a="soldier_deck_a", b="soldier_deck_b", c="soldier_deck_c", d="soldier_deck_d")
MEM = dict(a="ashi_a24", b="ashi_c24", c="ashi_d24", d="ashi_b24")
MIRROR = dict(a=False, b=True, c=False, d=True)
PPD = dict(a=224, b=224, c=224, d=224)
PH = dict(a=0.0, b=1.3, c=2.6, d=4.1)


def chase_s(g):
    return (g - RANGE[SHOT][0]) / 30.0


def cam_of(A, g):
    pc = A["cam"]
    x = (g - RANGE[SHOT][0]) / float(RANGE[SHOT][1] - RANGE[SHOT][0])
    u = C.calm(x)
    loc0, look0 = Vector(pc["loc"]), Vector(pc["look_at"])
    fwd = look0 - loc0; fwd.z = 0; fwd.normalize()
    right = fwd.cross(Vector((0, 0, 1)))
    off = Vector((J.CHASE_V * chase_s(g), 0, 0)) + right * (SLIDE * u)
    return loc0 + off, look0 + off, pc["lens"]


def pose_s(k, g):
    c, p = C.story(MEM[k] + "_laugh_point")
    p["mirror"] = MIRROR[k]
    ph = PH[k]
    b = abs(math.sin(g * 0.42 + ph))                               # laugh beat ~ every 7.5 frames
    p["legs"] = dict(preset="wide", crouch=0.03 + 0.09 * b)        # hips bounce, soles stay on the deck
    p["head_dy"] = 0.04 * b
    p["lean"] = p.get("lean", 0) + 2.0 * math.sin(g * 0.42 + ph + 0.8)
    p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(g * 0.21 + ph)
    p["blink"] = blink(g, [660 + 7 * ord(k) % 13, 710 + ord(k) % 9])
    p["t"] = g / 30.0 + ph
    return p


class Take(C.Take):
    def __init__(self, shot=SHOT):
        C.Take.__init__(self, PRESET[shot], name="cam_s07")
        sd = os.path.join(TMP, "sprites")
        P = self.A["parented"]
        self.lp = {}
        la, lb = P["soldier_deck_a"]["local"], P["soldier_deck_b"]["local"]
        pos = dict(a=tuple(la), b=tuple(lb),                                   # the two on-screen anchors of the preset camera
                   c=((la[0] + lb[0]) / 2 - 2.6, (la[1] + lb[1]) / 2 + 0.2, la[2]),   # back row, between them
                   d=(la[0] - 1.8, la[1] + 2.0, la[2]))                       # back row, right
        for k in "abcd":
            a = self.actors[k] = C.make_actor(k, MEM[k], sd, contact=False)
            self.ship = P["soldier_deck_a"]["ship"]
            C.parent_to_ship(a, self.ship)
            self.lp[k] = pos[k]
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
