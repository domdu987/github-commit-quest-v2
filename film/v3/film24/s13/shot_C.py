#!/usr/bin/env python3
"""shot_C.py -- film 24 version C take s13: shot 13 split in three with hard cuts at (old) g 1527 and 1560.  Render g = OLD numbering; meta_C.json adds +208.
  13a  g 1407..1526  reveal_top   the accepted aerial U (same move / hooks as s13/shot.py), relit golden hour (JOSEON_LOOK=C).  Handle-in 6 f.
  13b  g 1527..1559  cannon_close set_broadside: 4 starboard ports fire in sequence (stern -> bow), slow world-fixed slide.
  13c  g 1560..1612  hit_close    set_hit_explosion peaks at g 1567; two ashigaru leap off the far rail (jump_arc + set_jump_splash); slow push.  Handle-out 6 f.
Internal shot ids (bf blocks): 13 = 13a, 113 = 13b, 213 = 13c.  Output: work_C/raw/s<id>/g_%04d.png (720x1280, post applied).
overlay_C.json: 13c only, per frame the hit ship's deck point from g 1567 on (hit_g 1567), old numbering.
    JOSEON_LOOK=C python3 shot_C.py probe|stills|final|overlay ...
"""
import math, os, sys, json
os.environ.setdefault("JOSEON_LOOK", "C")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402

J = C.J
lerp, clamp, ez, bf = C.lerp, C.clamp, C.ez, C.bf
SH_A, SH_B, SH_C = 13, 113, 213
RANGES = {SH_A: (1407, 1526), SH_B: (1527, 1559), SH_C: (1560, 1612)}
PRESETS = {SH_A: "reveal_top", SH_B: "cannon_close", SH_C: "hit_close"}
G_B0, G_C0 = 1527, 1560
G_HIT = 1567                                             # the explosion peaks here (set_hit_explosion t = 0.4 s)
G_HIT0 = 1555                                            # first hit (t = 0)
JUMP_G = (1569, 1581)                                    # jump starts of ashigaru 0 / 1
OUT = os.path.join(HERE, "work_C")
TMP = os.path.join(HERE, "work")

# ---- 13a (identical schedule to s13/shot.py; the camera span is the old take proper 1413..1606, 13a only uses its first part)
LOC0, LOC1 = (-54.0, 0.0, 150.0), (-40.0, 0.0, 190.0)
LOOK0, LOOK1 = (-12.0, 0.0, 0.0), (-10.0, 0.0, 0.0)
SMOKE_K = 2.6


def turn_k(g):
    return ez((g - 1440) / 60.0, "sine")


def smoke_l(g):
    if g < 1500:
        return 0.0
    if g < 1600:
        return ez((g - 1500) / 70.0)
    return lerp(1.0, 0.35, ez((g - 1600) / 70.0))


def cam_a(g):
    u = C.calm((g - 1413) / float(1606 - 1413))
    return Vector(LOC0).lerp(Vector(LOC1), u), Vector(LOOK0).lerp(Vector(LOOK1), u), 18.0


class Take(C.Take):
    def __init__(self, shot):
        self.shot = shot
        C.Take.__init__(self, PRESETS[shot], name="cam_s13_%d" % shot)
        self.base = dict(self.A["cam"])
        if shot == SH_C:
            self._actors()

    # ------------------------------------------------------------------ 13c cast
    def _actors(self):
        orig = C.story
        sd = os.path.join(TMP, "sprites")
        self.cast = []
        for i, (cast, st_, st_air) in enumerate((("ashi_a24", "ashi_a24_peer_worried", "ashi_a24_step_back"),
                                                 ("ashi_b24", "ashi_b24_peer_worried", "ashi_b24_step_back"))):
            a = self.actors["ashi%d" % i] = C.make_actor("ashi%d" % i, cast, sd, contact=False)
            self.cast.append((a, st_, st_air))

    def cam_b(self, g):
        b = self.base
        u = C.calm((g - G_B0) / 32.0)
        slide = Vector((-3.0, 0.0, 0.0)) * u            # world-fixed slide along the ship
        return Vector(b["loc"]) + slide, Vector(b["look_at"]) + slide, b["lens"]

    def cam_c(self, g):
        b = self.base
        u = C.calm((g - G_C0) / 52.0)
        loc, look = Vector(b["loc"]), Vector(b["look_at"])
        return loc.lerp(look, 0.10 * u) + Vector((0, 0, -0.1 * u)), look + Vector((0.8 * u, 0, 0)), b["lens"]

    def cam_of(self, g):
        return {SH_A: cam_a, SH_B: self.cam_b, SH_C: self.cam_c}[self.shot](g)

    # ------------------------------------------------------------------ poses
    def pose(self, shot, gs):
        sh = self.shot
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = self.cam_of(g)
            self.key_cam(f, loc, look, lens=lens)
            if sh == SH_A:
                self.key_set(f, spikes=3, ports=clamp((g - 1492) / 10.0), dragon_smoke=0.0)
                J.set_korean_turn(turn_k(g), frame=f)
                J.set_cannon_smoke(smoke_l(g), frame=f)
                for G_ in J.S["guns"]:
                    for o in list(G_["puffs"]) + [G_["flash"]]:
                        o.scale = tuple(v * SMOKE_K for v in o.scale)
                        J.key_attr(o, "scale", f, "LINEAR")
                J.set_damage(0.0, frame=f)
            elif sh == SH_B:
                self.key_set(f, spikes=3, ports=1.0, dragon_smoke=0.0)
                J.set_broadside((g - 1529) / 30.0, f)
            else:
                self.key_set(f, spikes=3, ports=1.0, dragon_smoke=0.0)
                J.set_hit_explosion((g - G_HIT0) / 30.0, f)
                for i, (a, st_ground, st_air) in enumerate(self.cast):
                    tj = (g - JUMP_G[i]) / 30.0
                    J.set_jump_splash(i, max(tj, -1.0), f)
                    C.place(a, f, tuple(J.jump_arc(i, max(tj, 0.0))))
        if sh == SH_C:
            self.scene.frame_set(bf(shot, gs[0]))
            for g in gs:
                f = bf(shot, g)
                self.scene.frame_set(f)
                for i, (a, st_ground, st_air) in enumerate(self.cast):
                    air = g >= JUMP_G[i]
                    c_, p = C.story(st_air if air else st_ground)
                    p = J.card_rim(p)
                    p["mirror"] = bool(i)
                    p["t"] = g / 30.0
                    if air:                              # comic tumble: lean and flail with the arc
                        p["lean"] = p.get("lean", 0) + 14.0 * math.sin((g - JUMP_G[i]) * 0.5)
                    a.pose(f, p, camera=self.cam)
            self.sprites_for([(a, 128) for a, _, _ in self.cast], [bf(shot, g) for g in gs])

    # ------------------------------------------------------------------ overlay (13c)
    def overlay_row(self, g):
        f = bf(SH_C, g)
        self.scene.frame_set(f)
        self.scene.camera = self.cam
        ships = []
        if g >= G_HIT:
            jb = J.S["ships"]["j_board"]
            p = jb["ride"].matrix_world @ Vector((0.0, 0.0, jb.get("deck_z", 2.4)))
            co = world_to_camera_view(self.scene, self.cam, p)
            ships.append(dict(name="j_board", hit_g=G_HIT, x=round(co.x * 720.0, 1), y=round((1.0 - co.y) * 1280.0, 1)))
        return dict(g=g, ships=ships)

    def report(self, shot, g):
        loc, look, lens = self.cam_of(g)
        r = dict(shot=shot, g=g, cam=[round(c, 2) for c in loc], lens=lens)
        if self.shot == SH_C:
            f = bf(shot, g)
            self.scene.frame_set(f)
            r["heads"] = C.head_report(self, f)
            r["feet"] = C.feet_report(self, f)
        return r

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def which(g):
    return SH_A if g < G_B0 else (SH_B if g < G_C0 else SH_C)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills", "overlay", "final"):
        pass
    if cmd in ("probe", "stills"):
        gs = [g for g in C.parse(sys.argv[2]) if RANGES[SH_A][0] <= g <= RANGES[SH_C][1]]
        sh = which(gs[0])
        assert all(which(g) == sh for g in gs), "one shot per process"
        Tk = Take(sh); Tk.pose(sh, gs)
        for g in gs:
            print(json.dumps(Tk.report(sh, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.4
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 10
                os.makedirs(out, exist_ok=True)
                st = Tk.render(sh, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s13C_g_%04d.png" % g))
                print("g %d %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "overlay":
        Tk = Take(SH_C); gs = list(range(RANGES[SH_C][0], RANGES[SH_C][1] + 1)); Tk.pose(SH_C, gs)
        rows = [Tk.overlay_row(g) for g in gs]
        json.dump(rows, open(os.path.join(HERE, "overlay_C.json"), "w"))
        print("overlay_C.json: %d frames" % len(rows))
    elif cmd == "final":
        # usage: final <13a|13b|13c|all> [a:b] ; one shot per process (one location build, fresh sun)
        which_s = sys.argv[2]
        spec = sys.argv[3] if len(sys.argv) > 3 else "1407:1612"
        shots = {"13a": [SH_A], "13b": [SH_B], "13c": [SH_C]}[which_s]
        os.makedirs(OUT, exist_ok=True)
        C.final_loop(lambda s_: Take(s_), shots, spec, RANGES, OUT, samples=C.preset_samples(PRESETS[shots[0]]))
