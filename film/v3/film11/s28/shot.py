#!/usr/bin/env python3
"""shot.py -- film 11 take s28: shot 28 (60.20-62.50 s = g 1806..1874 + the plan's hard cut on the last word "วัว" ~62.3 s = g 1869),
handles 1800..1874 (the film ends at N = 1875).  barn_wide / light A.  Blossom (chew, ear flick, tail swish) stands in the golden barn; the camera
pushes in slowly; at "วัว" (g ~1869) she looks round at us as if she knows the word is hers.  Nobody else.  No quote, no lip-sync.

    python3 shot.py probe 28 a:b[:step]
    python3 shot.py stills 28 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 28 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast11 = C.D, C.actors, C.camrig, C.cast11
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 28
G0, G1, H = C.g_bound(60.20), 1875, 6
RANGES = {SHOT: (G0 - H, G1 - 1)}          # no frames beyond N: the film's last frame is g 1874 (hard cut)
PRESET, LIGHT = "barn_wide", "A"
BLOSSOM = Vector((-2.2, 5.8, 0.0))
G_WORD = C.g_of(62.20)                     # "วัว" ~ 62.3 s: she looks round around here
CAM0 = ((2.4, -1.6, 1.3), (-3.4, 6.0, 1.6))
CAM1 = ((0.5, -0.4, 1.1), (-6.2, 5.8, 2.05))


def cam_of(g):
    x = (g - (G0 - H)) / float(G1 - 1 - (G0 - H))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


TURN_DEG = 32.0                      # card yaw at the end (sign chosen so the head end swings towards the lens)


def turn_of(g):
    return ez((g - 1846) / 12.0)       # 0 -> 1 over g 1846..1858, still from 1860


def pose_blossom(g):
    """chews and swishes; over g 1846-1858 the head comes up and the card turns ~32 deg (three-quarter, head towards the lens), still from 1860;
    eye wide open on the turn, ear flicks, then the knowing half-lid + ear flick on the word (g 1866-1871)."""
    p = dict(cast11.STORY11["blossom_chew"][1])
    up = ez((g - 1846) / 12.0)
    p.update(head_turn=lerp(0.0, -0.15, up), head_down=lerp(0.1, -0.5, up), chew=g / 12.0 if up < 0.3 else None, chew_amp=1.0,
             tail=0.7 * math.sin(g / 8.0) * (1.0 if g < 1858 else 0.35), mirror=True)
    if p["chew"] is None:
        del p["chew"]
    k = (g - G0 + 20) % 70
    p["ear"] = (1.0 if k < 3 else (-0.3 if k < 6 else 0.0)) if g < 1846 else 0.0
    if 1856 <= g <= 1858 or 1866 <= g <= 1868:
        p["ear"] = 1.0
    elif 1859 <= g <= 1860 or 1869 <= g <= 1871:
        p["ear"] = -0.3
    p["blink"] = 2 if g in (1825, 1826, 1862, 1863) else (1 if g >= 1866 else 0)     # open eye on the turn, half-lid only on the word
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=SHOT):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s28", light=LIGHT)
        self.warm_fill()
        self.blo = self.actors["blo"] = C.make_actor("blo", "blossom", os.path.join(TMP, "sprites"), canvas=cast11.CANVAS11["blossom"])

    def warm_fill(self):
        """director gate note: Blossom in warm golden light (no-shadow warm area fill from the door side, as the milking nook's door spill) and the flat
        yellow lantern rectangles hidden."""
        D.area_fill("s28_warm", (-9.0, 4.5, 2.8), (1.0, 0.25, -0.2), (6.0, 5.0), (1.0, 0.9, 0.5), 1700)
        for h in D.STATE.get("hooks", []):
            if h["kind"] == "lantern":
                bpy_obj = C.bpy.data.objects[h["obj"]]
                bpy_obj.hide_render = True

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.blo, f, BLOSSOM)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.blo.pose(f, pose_blossom(g), camera=self.cam)
        self.sprites_for([(self.blo, 288)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def on_frame(self, f):
        """per-frame card yaw: the camera-parallel yaw plus the turn (set before the stage syncs the cards)."""
        g = f - 1
        r = self.cam.matrix_world.to_3x3() @ Vector((1.0, 0.0, 0.0))
        base = math.degrees(math.atan2(r.y, r.x))
        self.blo.yaw_fixed = base + TURN_DEG * turn_of(g)

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam
        self.no_dof()
        self.scene.cycles.samples = samples
        return C.render.render_frames([bf(shot, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam,
                                      verbose=False, on_frame=self.on_frame)


if __name__ == "__main__":
    C.cli(Take, RANGES, HERE, [SHOT])
