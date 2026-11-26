#!/usr/bin/env python3
"""shot.py -- film 24 take s05: shots 5 + 6 on the flagship `jflag` (sea).  g 425..649 = 6 in-handle + shot 5 (g 431..512) +
shot 6 (g 513..643) + 6 out-handle.  Two presets (flag_deck, flag_deck_b), two builds (sun follows the preset camera).
    id 5  g 425..512  flag_deck:   jp_cmd24_laugh_big (head back, held open mouth), ashi_a24 + ashi_b24 laugh_point behind.  Slow push-in.
    id 6  g 513..649  flag_deck_b: jp_cmd24_point_mock (g 513..~575) then finger_up_promise (~585..), lip-sync (talk_mouth) over the quote
                                   (narration 16.1-21.4 s = film g 486..645; shot 6 lies completely inside it).  Slow slide left.
Mouths: only jp_cmd24, only inside g_of(16.1)..g_of(21.4); shot 5's laugh_big keeps its held laugh mouth (not a lip-sync pose).
Blender frame of (id, g) = 1000 * (id - 1) + g + 1.
    python3 shot.py probe 5,6 a:b[:step] | stills 5,6 a:b[:step] <out> [scale 0.4] [samples 10] | final 5|6|5,6 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

J, actors, cast24 = C.J, C.actors, C.cast24
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G5, G6, GEND = C.g_bound(14.37), C.g_bound(17.10), C.g_bound(21.47)     # 431, 513, 644
H = 6
RANGES = {5: (G5 - H, G6 - 1), 6: (G6, GEND + H - 1)}
PRESET = {5: "flag_deck", 6: "flag_deck_b"}
Q0, Q1 = C.g_of(16.1), C.g_of(21.4)                       # lip-sync window in film frames (486 .. 645)
G_FINGER = C.g_of(18.11)                                  # point_mock ("เต่ามันคลานช้า") -> finger_up_promise ("ถ้าเต่าตัวนั้น...")
PUSH5, SLIDE6 = 0.10, 2.6
PPD = dict(cmd=160, a=96, b=96)


def ship_pt(lp):
    return J.ship_root("jflag").matrix_world @ Vector(lp)


def cam_of(shot, g, T):
    pc = T.A["cam"]
    loc0, look0 = Vector(pc["loc"]), Vector(pc["look_at"])
    x = (g - RANGES[shot][0]) / float(RANGES[shot][1] - RANGES[shot][0])
    u = C.calm(x)
    if shot == 5:                                          # push-in along the view line
        return loc0 + (look0 - loc0) * (PUSH5 * u), look0, pc["lens"]
    d = look0 - loc0
    side = Vector((-d.y, d.x, 0.0)).normalized()          # screen-left of the view (right-hand normal flipped below)
    s = -SLIDE6 * u
    return loc0 + side * s, look0 + side * s * 0.6, pc["lens"]


# ----------------------------------------------------------------------------- poses
def mouth_cmd(g):
    return cast24.talk_mouth(g, 1.0) if Q0 <= g <= Q1 else "flat"


def pose_cmd5(g):
    c, p = C.story("jp_cmd24_laugh_big")
    p["lean"] = p.get("lean", 0) + 1.2 * math.sin(g * 0.55)          # laughing shake (feet planted)
    p["head_roll"] = 2.0 * math.sin(g * 0.45 + 0.6)
    p["pitch"] = -0.32 + 0.08 * math.sin(g * 0.5)             # head thrown back
    p["blink"] = blink(g, [])
    p["t"] = g / 30.0
    return p


def pose_cmd6(g):
    if g < G_FINGER:
        c, p = C.story("jp_cmd24_point_mock")
    else:
        c, p = C.story("jp_cmd24_finger_up_promise")
    p["mouth"] = mouth_cmd(g)
    p["lean"] = p.get("lean", 0) + 0.8 * math.sin(g * 0.13)
    p["blink"] = blink(g, [530, 598])
    p["t"] = g / 30.0
    return p


def pose_sol(name, g, ph, mirror=False):
    c, p = C.story(name)
    p["mirror"] = mirror
    p["lean"] = p.get("lean", 0) + 1.0 * math.sin(g * 0.5 + ph)
    p["blink"] = blink(g, [])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, shot=5):
        C.Take.__init__(self, PRESET[shot], name="cam_s05")
        self.shot = shot
        sd = os.path.join(TMP, "sprites")
        self.cmd = self.actors["cmd"] = C.make_actor("cmd", "jp_cmd24", sd)
        self.lp = {k: tuple(self.A["parented"][v]["local"]) for k, v in dict(cmd="commander_deck", a="soldier_deck_a", b="soldier_deck_b").items()}
        C.parent_to_ship(self.cmd, "jflag")
        if shot == 5:
            self.a = self.actors["a"] = C.make_actor("a", "ashi_a24", sd)
            self.b = self.actors["b"] = C.make_actor("b", "ashi_b24", sd)
            C.parent_to_ship(self.a, "jflag"); C.parent_to_ship(self.b, "jflag")
        for n, a in self.actors.items():
            if not hasattr(a, "ship"):
                a.ship = "jflag"

    def pose(self, shot, gs):
        assert shot == self.shot
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            loc, look, lens = cam_of(shot, g, self)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f)
            C.place_on_ship(self.cmd, f, self.lp["cmd"])
            if shot == 5:
                C.place_on_ship(self.a, f, self.lp["a"])
                C.place_on_ship(self.b, f, self.lp["b"])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.cmd.pose(f, pose_cmd5(g) if shot == 5 else pose_cmd6(g), camera=self.cam)
            if shot == 5:
                self.a.pose(f, pose_sol("ashi_a24_laugh_point", g, 0.0), camera=self.cam)
                self.b.pose(f, pose_sol("ashi_b24_laugh_point", g, 1.7, mirror=True), camera=self.cam)
        fs = [bf(shot, g) for g in gs]
        jobs = [(self.cmd, PPD["cmd"])]
        if shot == 5:
            jobs += [(self.a, PPD["a"]), (self.b, PPD["b"])]
        self.sprites_for(jobs, fs)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g, self)
        r = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f), feet=C.feet_report(self, f),
                 mouth=mouth_cmd(g) if shot == 6 else "laugh")
        return r

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take(shot)
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.4
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 10
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else C.RES_PCT
        for shot in shots:
            samples = int(sys.argv[5]) if len(sys.argv) > 5 else C.preset_samples(PRESET[shot])
            C.final_loop(lambda s_: Take(s_), [shot], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
