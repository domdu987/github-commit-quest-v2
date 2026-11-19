#!/usr/bin/env python3
"""shot.py -- film 16 take s24 = shot 24, THE REVEAL MACRO (g 1540..1614 + 9 handle frames each side; hard CUT in at 1540 and out at 1615).
"ไฟเลยวิ่ง อยู่แต่ในลวด ไม่รั่วลงเสา สักหยด" -- the current runs only inside the wire, does not leak down the pole, not one drop.

LINE bottle_macro / AFTER_RAIN: ONE glowing pulse (TG.set_pulse, keyed per frame) runs along the wire from the left, slides over the
bottle neck and PARKS inside the glass (TG.pulse_s_at_pole(1)); the wet pole below stays dark (the pulse's cyan light is linked to the
glass only).  Camera: whip follow -- the look point rides the pulse head from the left edge, then settles on the bottle -- on top of a
drift push + slide + arc, plus one eased SNAP push on "ไม่รั่วลงเสา" (event g 1582).  No cast, no text, no DOF.

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

TG, K, LN = C.TG, C.K, C.LN
lerp, clamp, ez, u_of, bf = C.lerp, C.clamp, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(51.32), C.g_bound(53.83)   # 1540, 1615: shot 24 = g 1540..1614; shot 25 (cut) starts at 1615
H_IN = H_OUT = 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1   # 1531, 1623
GS = list(range(G_FIRST, G_LAST + 1))
G_RUN = (G_FIRST - 4, 1558)
G_PARK = 1558                                  # parked inside the neck from here on ("อยู่แต่ในลวด" 1561 .. "ไม่รั่วลงเสา" 1582)
G_SNAP_WORD = 1582                             # "ไม่รั่วลงเสา": snap push on the glass
SNAP = (G_SNAP_WORD - 3, G_SNAP_WORD + 10)    # 13 frames
S_BACK = 0.05                                  # the pulse starts this far (fraction of the whole wire) before the glass
FOLLOW_END = 1566                              # the look point has left the head and settled on the glass by here

CAM0 = lambda: None                            # (placeholder: the preset camera is read from the Take)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bottle_macro", quality=quality, name="cam_s24")
        self.s_park = TG.pulse_s_at_pole(1)
        self.s0 = self.s_park - S_BACK
        S = TG.STATE
        self.pts, self.cum = S["wire_pts"]["bottle"]
        loc, look = Vector(self.A["cam"]["loc"]), Vector(self.A["cam"]["look_at"])
        self.glass = self.head_world(self.s_park)                       # parked head = inside the glass
        look = self.glass                                               # subject point = the glass (the preset looks a bit past it)
        v = look - loc
        loc = look - v * 1.0
        self.cam_path = C.CamPath(Vector(look) - (look - Vector(self.A["cam"]["loc"])) * 1.0, look, G0, G_LAST, push=0.06, slide_px=115.0,
                                  arc_deg_s=-22.0, decay=0.3, snaps=[dict(g=SNAP, k=2.0, peak=1.9, shift=(-1.3, -0.1))])

    def head_world(self, s):
        d0 = min(1.0, max(0.0, s)) * self.cum[-1]
        p = TG._wire_at(self.pts, self.cum, d0)
        head, _ = TG._pulse_head_target(p)
        return TG.W(head)

    def s_of(self, g):
        u = u_of(g, G_RUN[0], G_RUN[1], kind="sine")
        return lerp(self.s0, self.s_park, u)

    def cam_at(self, g):
        loc, look = self.cam_path.at(g)
        w = 1.0 - u_of(g, G_FIRST, FOLLOW_END, kind="sine")            # 1 = riding the head, 0 = settled on the glass
        off = (self.head_world(self.s_of(g - 7)) - self.glass) * w            # lags the head by 5 frames: it runs ahead of the camera
        return loc + off * 0.25, look + off            # mostly a PAN with the head (the sky sweeps past), a little truck

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.cam_at(g))
            TG.set_pulse(self.s_of(g), frame=f)

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        return dict(g=g, s=round(self.s_of(g), 4), head_px=TG.project(tuple(self.head_world(self.s_of(g)))), glass_px=TG.project(tuple(self.glass)),
                    cam=[round(c, 3) for c in self.cam_at(g)[0]])

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST] if len(sys.argv) > 2 else []
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
