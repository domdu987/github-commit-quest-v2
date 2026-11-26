#!/usr/bin/env python3
"""shot.py -- film 24 take s10: shot 10 (sea flag_bow), g 1002..1112 + 6 handle frames each side (996..1118).
The Japanese commander (jp_cmd24_shout_forward, gunbai) shouts from the bow of his flagship `jflag`; the fleet behind.
LIP-SYNC only in 34.8-37.0 s ("เห็นไหม เต่ากลัวแล้ว! ตามไปให้หมด!"): g_of(34.81)=1047 .. g_of(37.0)=1111; flat outside.
Camera: the preset flag_bow camera (ahead of the bow, looking aft) slowly pushed in 9 %, travelling WITH the fleet (set_fleet_chase keyed
every frame, camera x follows CHASE_V*s) so the water slides past.   One id (10): Blender frame = 9000 + g + 1.

    python3 shot.py probe a:b[:step] | stills a:b[:step] <out> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
J, actors, cast24 = C.J, C.actors, C.cast24
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

SHOT = 10
G0, G1 = C.g_bound(33.40), C.g_bound(37.09) - 1          # 1002..1112
H = 6
RANGE = {SHOT: (G0 - H, G1 + H)}
RANGES = RANGE
PRESET = {SHOT: "flag_bow"}
LIP0, LIP1 = C.g_of(34.81), C.g_of(37.00)                # 1047 .. 1111
PUSH = 0.09
PPD = 224


def chase_s(g):
    return (g - RANGE[SHOT][0]) / 30.0


def cam_of(A, g):
    pc = A["cam"]
    x = (g - RANGE[SHOT][0]) / float(RANGE[SHOT][1] - RANGE[SHOT][0])
    u = C.calm(x)
    off = Vector((J.CHASE_V * chase_s(g), 0, 0))
    loc0, look = Vector(pc["loc"]) + off, Vector(pc["look_at"]) + off
    loc = loc0 + (look - loc0) * (PUSH * u)
    return loc, look, pc["lens"]


def pose_cmd(g):
    c, p = C.story("jp_cmd24_shout_forward")
    p["mouth"] = cast24.talk_mouth(g, 1.0) if LIP0 <= g <= LIP1 else "flat"
    p["lean"] = p.get("lean", 0) + 1.2 * math.sin(g * 0.13)
    p["head_roll"] = p.get("head_roll", 0) + 1.5 * math.sin(g * 0.09)
    a = p.get("arm_r")
    if isinstance(a, dict) and "hand" in a:                       # the arm pumps forward a little on each shouted phrase
        hx, hy = a["hand"]
        k = 0.05 * math.sin(g * 0.35) if LIP0 <= g <= LIP1 else 0.0
        a = dict(a); a["hand"] = (hx + k, hy - k); p["arm_r"] = a
    p["blink"] = blink(g, [1040, 1090])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, shot=SHOT):
        C.Take.__init__(self, PRESET[shot], name="cam_s10")
        sd = os.path.join(TMP, "sprites")
        self.cmd = self.actors["cmd"] = C.make_actor("cmd", "jp_cmd24", sd, contact=False)
        pa = self.A["parented"]["commander_bow"]; ship, self.lp = pa["ship"], tuple(pa["local"])
        C.parent_to_ship(self.cmd, ship)
        self.deckc = C.roof_contact(self.cmd, ship, self.lp, width=1.8, depth=0.8, normal=(0, 0, 1))

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(self.A, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, spikes=3, ports=0, dragon_smoke=0.0, fleet_chase=chase_s(g), korean_turn=0.0, damage=0.0, cannon_smoke=0.0)
            C.place_on_ship(self.cmd, f, self.lp)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.cmd.pose(f, pose_cmd(g), camera=self.cam)
        self.sprites_for([(self.cmd, PPD)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(self.A, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f),
                    feet=C.feet_report(self, f), mouth=pose_cmd(g)["mouth"])

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
