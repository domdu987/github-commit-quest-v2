#!/usr/bin/env python3
"""shot.py -- film 16 take s12 = shot 12 (CHAMBER chamber_table-style EYE angle, DAY): "เขาได้เงินมา แบบหวุดหวิด" -- "barely got the money".
Shot 12 = g 785..830 (26.18-27.70 s); in-handle 9 f (hard cut), out-handle 9 f (dissolve into shot 13: 13-17 f).
    g 788   the fat money bag drops onto the telegraph table in front of Morse (event "เขาได้เงินมา" g 788): it falls from above the frame, lands
            with a bounce (set_moneybag lift keyed per frame), Morse flinches, then looks at it, a small relieved smile (morse_relieved)
    the mocker stands behind, arms folded, sour (mocker_sour_arms)
Camera: eye level 1.0 D above Morse's head centre... push 8 %/s + slide 40 px/s, no snap (the shot is 1.5 s).  Mouths: nobody speaks.

    python3 shot.py camreport | probe a:b[:s] | stills a:b[:s] out_dir [scale] [spp] | final a:b[:s] [scale] [spp]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

TG, K, actors, cast16 = C.TG, C.K, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

# ------------------------------------------------------------------ timing
G0, G1 = C.g_bound(26.18), C.g_bound(27.70)              # 785, 831 (exclusive)
H_IN, H_OUT = 9, 9
GS = list(range(G0 - H_IN, G1 + H_OUT))                  # 776..839
G_LAST = GS[-1]
G_BAG = C.cap_g("เขาได้เงินมา")                          # 788: the bag lands
LIGHT, PRESET = "DAY", "chamber_table"
MORSE_MARK = (4.0, 9.2, 0.0)                             # just behind the table, right of the instrument; the bag lands in front of him
MOCK_MARK = (6.9, 12.4, 0.0)                            # in the background, left, arms folded
FALL = (G_BAG - 5, G_BAG)                                # 783..788: falls from 7 D above the table to the cloth
# bounces after the landing: (g, lift in D)
BOUNCE = [(G_BAG, 0.0), (G_BAG + 3, 0.55), (G_BAG + 6, 0.0), (G_BAG + 8, 0.18), (G_BAG + 10, 0.0)]


class JoltCam(C.CamPath):
    """the drift camera plus a small thud-shake (the table takes the bag): vertical jolt, 4-frame period, decays in ~8 frames"""

    def at(self, g):
        loc, look = C.CamPath.at(self, g)
        k = g - G_BAG
        if k >= 0:
            j = 0.32 * math.sin(2 * math.pi * k / 4.0) * math.exp(-k / 6.0)
            loc = loc + Vector((0, 0, j)); look = look + Vector((0, 0, j))
        return loc, look


CAM = JoltCam(Vector((2.0, 3.2, 3.5)), Vector((3.6, 9.2, 2.7)), GS[0], G_LAST, push=0.13, slide_px=40.0, rise_px=0.0, arc_deg_s=12.0,
              decay=0.3, snaps=[])


def bag_lift(g):
    if g < FALL[0]:
        return None                                      # not in the world yet (hidden above the frame)
    if g < G_BAG:
        u = (g - FALL[0]) / float(G_BAG - FALL[0])
        return 7.0 * (1.0 - u * u)
    for (g0, l0), (g1, l1) in zip(BOUNCE[:-1], BOUNCE[1:]):
        if g0 <= g <= g1:
            u = (g - g0) / float(g1 - g0)
            up = l1 > l0
            return lerp(l0, l1, u * u if not up else 1 - (1 - u) ** 2) if up else lerp(l0, l1, u * u)
    return 0.0


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s12")
        self.key_cam(bf(GS[0]), *CAM.at(GS[0]))
        self.scene.frame_set(bf(GS[0]))
        sd = os.path.join(WORK, "sprites")
        self.mor = self.add("mor", "morse16", MORSE_MARK, sd)
        self.mock = self.add("mock", "mocker", MOCK_MARK, sd)

    def add(self, name, cast, mark, sd):
        a = C.make_actor(name, cast, sd, cam=self.cam)
        a.mark = tuple(mark)
        self.actors[name] = a
        return a

    def morse_pose(self, g):
        p = dict(cast16.STORY16["morse_relieved"][1])
        p["mirror"] = False
        p["blink"] = blink(g, [G_BAG + 12, 819])
        p["lean"] = 1.5 * math.sin(g * 0.2)
        p["head_roll"] = p["head_roll"] + 1.5 * math.sin(g * 0.13)
        if g < G_BAG + 2:                                  # before / at the thud: braced, looking up at the bag, mouth flat
            p["expr"], p["mouth"], p["gaze"] = "stunned", "flat", (0.2, -0.6)
        # a flinch when it lands, then the relief eases in
        k = max(0.0, 1.0 - abs(g - G_BAG - 1) / 4.0)
        p["squash"] = (1.0 + 0.03 * k, 1.0 - 0.04 * k)
        return p

    def mock_pose(self, g):
        p = dict(cast16.STORY16["mocker_sour_arms"][1])
        p["mirror"] = True                                  # faces Morse and the table: screen-right of him is wrong, he looks across -> mirror
        p["mirror"] = False
        p["blink"] = blink(g, [790, 825])
        p["lean"] = 1.2 * math.sin(g * 0.14)
        p["head_roll"] = p["head_roll"] + 2.0 * math.sin(g * 0.11)
        return p

    def pose(self, gs):
        import tg_chamber as CH
        if not getattr(self, '_bag_moved', False):
            TG.STATE['moneybag_base'] = Vector(TG.STATE['moneybag_base']) + Vector((0.55, 0.45, 0.0))   # onto the table top, off the near-left corner
            self._bag_moved = True
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            for a in self.actors.values():
                C.place(a, f, a.mark)
            lift = bag_lift(g)
            CH.set_moneybag(lift is not None, frame=f, lift=lift or 0.0)
            self.key_set(f, flames=1.0, tape=0.0)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mor.pose(f, self.morse_pose(g), camera=self.cam)
            self.mock.pose(f, self.mock_pose(g), camera=self.cam)
        self.sprites_for([(self.mor, 256), (self.mock, 256)], [bf(g) for g in gs])

    def report(self, g):
        return dict(g=g, cam=[round(c, 2) for c in CAM.at(g)[0]], heads=C.head_report(self, bf(g)), lift=bag_lift(g))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        print(rows[0], rows[len(rows) // 2], rows[-1])
        print("longest run under 0.25 px/frame: %d frames (bible max 6); min px %.2f" % (worst, min(r["px"] for r in rows)))
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GS[0] <= g <= G_LAST]
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
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["chamber"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
