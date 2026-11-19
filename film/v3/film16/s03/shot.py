#!/usr/bin/env python3
"""shot.py -- film 16 take s03 = shot 3 (3.66-5.59 s): LINE line_rail / DAY.  g 110..167 + 9 handle frames each side (g 101..176).
"ไอ้บ้าลวด... รถไฟ" -> the 1840s steam train chugs past behind the poles; Morse (on the field side, at pole 3) taps the wire up at the glass
and grins at it.  Camera from the field side looking across the pole line at the track: tracks LEFT with the train (it runs toward -x),
slow push, quick eased snap-in on "รถไฟ" (event g 160).  Morse: cast16 morse_tap_wire_grin.  Nobody speaks.  No DOF, no text.

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

G0, G1 = C.g_bound(3.66), C.g_bound(5.59)          # 110, 168 (exclusive)
H_IN, H_OUT = 9, 9
GA, GB = G0 - H_IN, G1 - 1 + H_OUT                  # 101 .. 176
GS = list(range(GA, GB + 1))
PRESET, LIGHT = "line_rail", "DAY"
G_WORD = C.cap_g("รถไฟ")                            # 160
SNAP = (G_WORD - 3, G_WORD + 10)
POLE = 3


def pole_xy():
    p = K.W((LN.px(LN.POLES_Y[POLE]) + 0.03, LN.POLES_Y[POLE], 0.0))
    return float(p.x), float(p.y)


class _Lazy(object):
    pass


def make_cam(px, py):
    mx, my = px - 1.6, py - 1.7                          # Morse on the field side of the pole
    look0 = (mx + 0.5, my, 2.6)
    loc0 = (mx - 1.2, my - 4.4, 1.7)
    return (mx, my), C.CamPath(loc0, look0, GA, GB, push=0.05, slide_px=-70.0, rise_px=14.0, arc_deg_s=-6.0, decay=0.25,
                               snaps=[dict(g=SNAP, k=1.7, peak=1.6, shift=(0.3, 0.1))])


TRAIN_V = 13.0                                       # D/s toward -x


def train_x(g, front0):
    return front0 + 14.0 - TRAIN_V * (g - GA) / 30.0


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s02")
        px, py = pole_xy()
        (mx, my), self.camp = make_cam(px, py)
        self.mark = (mx, my, 0.0)
        TG.set_ladder(False, 3)
        self.front0 = TG.STATE["train"]["front0"]
        self.key_cam(bf(GA), *self.camp.at(GA))
        self.scene.frame_set(bf(GA))
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)

    def pose_of(self, g):
        p = dict(cast16.STORY16["morse_tap_wire_grin"][1])
        t = g / 30.0
        p["lean"] = p.get("lean", 0) + 2.0 * math.sin(t * 6.0)
        p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(t * 3.3)
        p["blink"] = blink(g, [118, 150])
        ar = dict(p["arm_r"])
        hx, hy = ar["hand"]
        ar["hand"] = (hx + 0.05 * math.sin(t * 9.0), hy + 0.10 * math.sin(t * 9.0 + 1.0))      # the tapping finger
        p["arm_r"] = ar
        p["t"] = t
        p["gaze"] = (1.0, 0.1)                       # eyes on the train (screen right)
        p["yaw"] = max(p.get("yaw", 0.45), 0.55)
        return p

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.camp.at(g))
            C.place(self.mor, f, self.mark)
            TG.set_train(train_x(g, self.front0), frame=f, speed=3.5)
            TG.set_pulse(-1.0, frame=f)
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
        px, py = (0, 0)
        rows, worst = make_cam(1, 1)[1].report(GS[:-1])
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
