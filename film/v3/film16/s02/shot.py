#!/usr/bin/env python3
"""shot.py -- film 16 take s02 = shot 2 (2.31-3.66 s): LINE line_wide / DAY.  g 69..109 + 9 handle frames each side (g 60..118).
"ชายคนนี้เอา คอขวดเบียร์ ..." -> the row of bottle-necked poles marching to the horizon; Morse at the ladder foot points down the line, proud.
The WHIP arrival (the plan's one whip, hard cut from shot 1): the camera starts panned far off to the side and whips onto the line
in g 66..80 (still part of the in-handle), then crane down + slide + push to the end (still moving on the last frame).
Morse: cast16 morse_proud_point (arm pointing screen-right = along the line), small live sway; mouth is the pose's smile (no speech).
No DOF, no text.

    python3 shot.py camreport | probe a:b[:s] | stills a:b[:s] out_dir [scale] [spp] | final a:b[:s] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

TG, K, LN, actors, cast16 = C.TG, C.K, C.LN, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(2.31), C.g_bound(3.66)          # 69, 110 (exclusive)
H_IN, H_OUT = 9, 9
GA, GB = G0 - H_IN, G1 - 1 + H_OUT                  # 60 .. 118
GS = list(range(GA, GB + 1))
PRESET, LIGHT = "line_wide", "DAY"
WHIP = (G0 - 3, G0 + 11)                            # whip: pan from far off to the line (14 frames, lands at g 80)
WHIP_D = 11.0                                       # look point sideways offset at the start (D)

MORSE_MARK = "morse_ladder_foot"
FOOT = (4.07, -10.82, 0.0)

CAM_LOOK0 = (14.0, -8.3, 3.4)                       # subject: Morse's torso beside the hero pole
CAM_LOC0 = (-3.2, -4.8, 2.7)                        # high, behind-left on the road side (crane down from here)
CAMP = C.CamPath(CAM_LOC0, CAM_LOOK0, GA, GB, push=0.06, slide_px=-100.0, rise_px=-20.0, arc_deg_s=12.0, decay=0.2, snaps=[])


class Cam(object):
    """CamPath + a whip: the look point is swung sideways (a pan, the position stays) and eases back onto the line."""
    def at(self, g):
        loc, look = CAMP.at(g)
        u = 1.0 - C.u_of(g, WHIP[0], WHIP[1], kind="cubic_out") if g < WHIP[1] else 0.0
        if g <= WHIP[0]:
            u = 1.0
        look = Vector(look) + CAMP.right * (WHIP_D * u)
        return loc, look

    def report(self, gs):
        return CAMP.report(gs)


CAM = Cam()


def train_x(g):
    return TG.STATE["train"]["front0"] - 5.0 * (g - GA) / 30.0          # creeps toward the camera (smoke alive)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s02")
        self.key_cam(bf(GA), *CAM.at(GA))
        self.scene.frame_set(bf(GA))
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.mark = (1.9, -6.3, 0.0)                   # on the grass beside the hero pole, nearer the lens (head ~150 px)
        inv = K.frame_mat().inverted()                  # extra foreground (crate of bottles, spool, grass) round the START camera: fills the lower third
        a, b = inv @ Vector(CAM_LOC0), inv @ Vector(CAM_LOOK0)
        old = TG.STATE.get("fg")
        for ob in (old if isinstance(old, (list, tuple)) else [old]):      # the preset's own FG belongs to the preset camera
            if ob is not None:
                ob.hide_render = True
        LN.fg_dress(TG.STATE, TG.STATE["M"], (a.x, a.y), (b.x, b.y), [("bottles", -0.55, 1.2), ("crate", 0.9, 1.5), ("grass", 0, 1.6, 70)], seed=77)

    def pose_of(self, g):
        p = dict(cast16.STORY16["morse_proud_point"][1])
        t = g / 30.0
        p["lean"] = p.get("lean", 0) + 2.0 * math.sin(t * 5.0)
        p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(t * 3.1 + 0.6)
        p["blink"] = blink(g, [g0 for g0 in (66, 97)])
        ar = dict(p["arm_r"])
        hx, hy = ar["hand"]
        ar["hand"] = (hx + 0.06 * math.sin(t * 4.0), hy - 0.10 * u_of(g, 74, 92) + 0.05 * math.sin(t * 6.3))   # the pointing hand sweeps down the line
        p["arm_r"] = ar
        p["t"] = t
        p["gaze"] = (1.0, -0.05)                      # eyes down the pole line he points along
        p["yaw"] = max(p.get("yaw", 0.4), 0.5)
        return p

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.mor, f, self.mark)
            self.key_set(f, train=train_x(g))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mor.pose(f, self.pose_of(g), camera=self.cam)
        self.sprites_for([(self.mor, 192)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        return dict(g=g, heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        for r in rows:
            print(r)
        print("longest run under 0.25 px/frame: %d" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GB]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
