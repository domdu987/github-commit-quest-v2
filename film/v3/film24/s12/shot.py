#!/usr/bin/env python3
"""shot.py -- film 24 take s12: shot 12 (sea board), g 1257..1412 + 6 handle frames each side (1251..1418).
The turtle ship and the Japanese ship j_board lie alongside (special 'board').  Camera over the turtle roof looks at j_board's rail:
soldiers peer worried at the spiked roof (sweat), two of them take real steps back (walk cycle in reverse, feet stepping) from "มีแต่เหล็กแหลม"
(g 1389); the ladder pair (ashi_d24_ladder_front + ashi_b24_ladder_back) stands planted.  One slow push from cams['board'] to cams['board_end'] (down onto
the spikes).  Fleet chase keyed every frame; the camera follows it (x += CHASE_V*s).  No quote -> no lip-sync, mouths fixed.
Blender frame = 11000 + g + 1.
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
J, actors, cast24 = C.J, C.actors, C.cast24
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

SHOT = 12
G0, G1 = C.g_bound(41.91), C.g_bound(47.10) - 1          # 1257..1412
H = 6
RANGE = {SHOT: (G0 - H, G1 + H)}
PRESET = {SHOT: "board"}
G_BACK = C.g_of(46.19)                                   # 1389 "มีแต่เหล็กแหลม": the two peerers step back
G_BACK_END = G_BACK + 24
STEP = 0.8                                               # D walked back
PPD = dict(c=256, d=224, b=224)
PUSH_LOC, PUSH_LOOK = 0.30, 0.14                         # fraction of the way to cams['board_end'] (the push ends looking down onto the spikes)


def chase_s(g):
    return (g - RANGE[SHOT][0]) / 30.0


def cam_of(A, g):
    c0, c1 = A["cams"]["board"], A["cams"]["board_end"]
    x = (g - RANGE[SHOT][0]) / float(RANGE[SHOT][1] - RANGE[SHOT][0])
    u = C.calm(x)
    off = Vector((J.CHASE_V * chase_s(g), 0, 0))
    loc = Vector(c0["loc"]).lerp(Vector(c1["loc"]), PUSH_LOC * u) + off
    look = Vector(c0["look_at"]).lerp(Vector(c1["look_at"]), PUSH_LOOK * u) + off
    return loc, look, lerp(c0["lens"], c1["lens"], PUSH_LOC * u)


def back_u(g):
    return ez((g - G_BACK) / float(G_BACK_END - G_BACK))


def pose_peer(member, g, k, mirror=False):
    c, p = C.story(member + "_peer_worried")
    u = back_u(g)
    p["mirror"] = mirror
    p["pitch"] = p.get("pitch", 0.75) - 0.25 * ez((g - 1250) / 150.0)
    p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.1 + k)
    p["head_roll"] = p.get("head_roll", 0) + 1.2 * math.sin(g * 0.08 + k)
    p["blink"] = blink(g, [1275 + 9 * k, 1340 + 7 * k])
    p["t"] = g / 30.0
    if g >= G_BACK and u < 1.0:
        c2, q = C.story(member + "_step_back")
        ph = 1.0 - (g - G_BACK) / 28.0                         # reverse phase: the feet step backwards
        w = cast24.cycle(member, ph, "walk", facing=1, base=dict(q), arms="none", speed=0.55)
        w["mirror"] = mirror
        w["lean"] = q.get("lean", -9) * 0.5
        w["blink"] = blink(g, [G_BACK + 8])
        w["t"] = g / 30.0
        return w
    if g >= G_BACK_END:
        c2, q = C.story(member + "_step_back")
        q["mirror"] = mirror
        q["t"] = g / 30.0
        return q
    return p


def pose_ladder(member, g, k):
    c, p = C.story(member)
    p["lean"] = p.get("lean", 0) + 1.0 * math.sin(g * 0.09 + k)
    p["head_roll"] = p.get("head_roll", 0) + 1.5 * math.sin(g * 0.07 + k)
    p["blink"] = blink(g, [1300 + 11 * k, 1385])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, shot=SHOT):
        C.Take.__init__(self, PRESET[shot], name="cam_s12")
        sd = os.path.join(TMP, "sprites")
        P = self.A["parented"]
        jb = P["soldier_board_a"]["ship"]
        x0, y0, z0 = P["soldier_board_c"]["local"]
        ya = P["soldier_board_a"]["local"][1]
        self.ship = jb
        # (name, member, story, local x, local y)
        yb = P["soldier_board_b"]["local"][1]
        spec = [("c", "ashi_c24", None, x0 - 0.5, y0),
                ("b", "ashi_b24", "ashi_b24_ladder_back", x0 + 2.4, yb),
                ("d", "ashi_d24", "ashi_d24_ladder_front", x0 + 4.6, yb)]
        self.lp = {}
        for nm, mem, st, lx, ly in spec:
            a = self.actors[nm] = C.make_actor(nm, mem, sd, story=st, contact=False)
            C.parent_to_ship(a, jb)
            self.lp[nm] = (lx, ly, z0)
            C.roof_contact(a, jb, self.lp[nm], width=1.5, depth=0.7, normal=(0, 0, 1))
        self.dir = Vector((1.0, 0.0, 0.0))                       # step-back direction (ship-local), checked in the draft

    def lp_at(self, nm, g):
        lx, ly, lz = self.lp[nm]
        if nm == "c":
            lx += self.dir.x * STEP * back_u(g)
        return (lx, ly, lz)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(self.A, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, spikes=3, ports=0, dragon_smoke=0.0, fleet_chase=chase_s(g), korean_turn=0.0, damage=0.0,
                         cannon_smoke=0.0, special="board")
            for nm in self.lp:
                C.place_on_ship(self.actors[nm], f, self.lp_at(nm, g))
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.actors["c"].pose(f, pose_peer("ashi_c24", g, 0), camera=self.cam)
            self.actors["b"].pose(f, pose_ladder("ashi_b24_ladder_back", g, 2), camera=self.cam)
            self.actors["d"].pose(f, pose_ladder("ashi_d24_ladder_front", g, 3), camera=self.cam)
        self.sprites_for([(self.actors[n], PPD[n]) for n in self.actors], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(self.A, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=round(lens, 2), heads=C.head_report(self, f),
                    feet=C.feet_report(self, f))

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
