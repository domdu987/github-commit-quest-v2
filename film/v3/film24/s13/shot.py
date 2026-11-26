#!/usr/bin/env python3
"""shot.py -- film 24 take s13: shot 13 (sea / reveal_top, g 1413..1606 + 6-frame handles g 1407..1412 and 1607..1612).
The one-image reveal, high aerial: the Korean ships (fleeing ahead, k 0) turn into the U round the Japanese fleet (set_korean_turn 0 -> 1
over 2 s, g 1440..1500 = "แล้วเรือเกาหลี ... ก็หันกลับมา" 48.7-50.9 s), then every gun fires (set_cannon_smoke 0 -> 1, g 1500..1570,
"ยิงปืนใหญ่" 51.97 s = g 1563), and the Japanese ships start to be hit one after another (set_damage creeping 0 -> 0.35 from g 1545).
Camera: slow rise and push (custom, from the preset line), DOF off, no characters (people are invisible at this height).
The top third of the frame stays free of key action from g 1560 (the director composites red X marks + "47 : 0" there).
overlay.json: per frame every ship that set_damage has hit: {"g", "ships": [{name, hit_g, x, y}]} (screen px of the deck centre at 720x1280).
    python3 shot.py probe|stills|final a:b[:step] ... ; python3 shot.py overlay
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402

J = C.J
lerp, clamp, ez, bf = C.lerp, C.clamp, C.ez, C.bf
SHOT = 13
G0, G1 = C.g_bound(47.10), C.g_bound(53.57) - 1          # 1413 .. 1606
H = 6
RANGES = {SHOT: (G0 - H, G1 + H)}
PRESET = "reveal_top"
TAKE = "s13"
CAM_G0, CAM_G1 = G0, G1                                  # the camera move spans the take proper
# the U: centre U_C (15, 0), front arc R 78 (+x side), arms 150 long back along both flanks (y = +-78), open toward -x.
# Portrait frame: the camera looks along +x from behind the opening, so the U's long axis is the screen's vertical.
LOC0, LOC1 = (-54.0, 0.0, 150.0), (-40.0, 0.0, 190.0)
LOOK0, LOOK1 = (-12.0, 0.0, 0.0), (-10.0, 0.0, 0.0)
LENS = 18.0
SMOKE_K = 2.6                                            # runtime scale of the cannon smoke puffs and flashes (readable from the air)


# ---- film-wide hook schedules (identical in s14, so that the damage thresholds / hit frames agree)
def turn_k(g):
    return ez((g - 1440) / 60.0, "sine")


def smoke_l(g):
    if g < 1500:
        return 0.0
    if g < 1600:
        return ez((g - 1500) / 70.0)                     # 0 -> 1 by g 1570, held to 1600
    return lerp(1.0, 0.35, ez((g - 1600) / 70.0))        # settles to the aftermath preset's 0.35


def dmg_d(g):
    if g < 1545:
        return 0.0
    if g < 1607:
        return 0.35 * ez((g - 1545) / 62.0, "sine") * 0.4 + 0.35 * 0.6 * ((g - 1545) / 62.0)
    return 0.35 + 0.65 * ((g - 1607) / 159.0) ** 0.9 if g <= 1766 else 1.0


def cam_of(g):
    u = C.calm((g - CAM_G0) / float(CAM_G1 - CAM_G0))
    return Vector(LOC0).lerp(Vector(LOC1), u), Vector(LOOK0).lerp(Vector(LOOK1), u), LENS


class Take(C.Take):
    def __init__(self, shot=SHOT):
        C.Take.__init__(self, PRESET, name="cam_" + TAKE)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, spikes=3, ports=clamp((g - 1492) / 10.0), dragon_smoke=0.0)
            J.set_korean_turn(turn_k(g), frame=f)
            J.set_cannon_smoke(smoke_l(g), frame=f)
            for G_ in J.S["guns"]:                       # bigger puffs + flashes for the aerial (runtime scale, joseon untouched)
                for o in list(G_["puffs"]) + [G_["flash"]]:
                    o.scale = tuple(v * SMOKE_K for v in o.scale)
                    J.key_attr(o, "scale", f, "LINEAR")
            J.set_damage(dmg_d(g), frame=f)

    def hit_g(self, thr):
        lo, hi = 1413, 1766
        for g in range(lo, hi + 1):
            if dmg_d(g) > thr:
                return g
        return None

    def overlay_row(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        self.scene.camera = self.cam
        d = dmg_d(g)
        ships = []
        for D in J.S["dmg"]:
            if d > D["thr"]:
                nm = D["sh"]["name"]
                ride = J.ship_root(nm)
                dz = D["sh"].get("deck_z", 2.4)
                p = ride.matrix_world @ Vector((0.0, 0.0, dz))
                co = world_to_camera_view(self.scene, self.cam, p)
                ships.append(dict(name=nm, hit_g=self.hit_g(D["thr"]), x=round(co.x * 720.0, 1), y=round((1.0 - co.y) * 1280.0, 1)))
        return dict(g=g, ships=ships)

    def report(self, shot, g):
        loc, look, lens = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 2) for c in loc], lens=lens, turn=round(turn_k(g), 3), smoke=round(smoke_l(g), 3), dmg=round(dmg_d(g), 3))

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills"):
        gs = [g for g in C.parse(sys.argv[2]) if RANGES[SHOT][0] <= g <= RANGES[SHOT][1]]
        Tk = Take(); Tk.pose(SHOT, gs)
        for g in gs:
            print(json.dumps(Tk.report(SHOT, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.4
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 10
                st = Tk.render(SHOT, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "%s_g_%04d.png" % (TAKE, g)))
                print("g %d %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "overlay":
        Tk = Take(); gs = list(range(G0 - H, G1 + H + 1)); Tk.pose(SHOT, gs)
        rows = [Tk.overlay_row(SHOT, g) for g in gs]
        json.dump(rows, open(os.path.join(HERE, "overlay.json"), "w"))
        print("overlay.json: %d frames, max %d ships" % (len(rows), max(len(r["ships"]) for r in rows)))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else C.RES_PCT
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else C.preset_samples(PRESET)
        C.final_loop(lambda s_: Take(), [SHOT], sys.argv[2], RANGES, HERE, scale=scale, samples=samples)
