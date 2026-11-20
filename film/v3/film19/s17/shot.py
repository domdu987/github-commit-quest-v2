#!/usr/bin/env python3
"""shot.py -- film 19 take s17 = shot 17: "ทุกหนึ่งชั่วโมงที่ต่างกัน เรือก็ห่างบ้านสิบห้าองศา ยิ่งเวลาต่าง ยิ่งไกล" -- the ship sails on, the V-wake lengthens behind it,
the camera pulls back and up as the ship grows smaller (distance grows); SNAP BACK on "ยิ่งไกล" (caption 45.56 s = g 1370).
SHIP ship_aerial / NOON, no actors.  g 1280..1383 (42.65-46.12 s) + 9 handle frames each side (hard cut in; dissolve 11 out to shot 18): g 1271..1392.
The ship sits at the origin (it 'sails' by the sea moving: set_sea(g/30) and set_roll(g/30) keyed on EVERY frame; the wake is part of the set).
Camera (c19.CamPath): high drift PULL 7 %/s + slow orbit about the ship + lateral slide; moving on the first frame, decay 0.1 (still moving on
the last).  No snap (shot < 2 s).  NO depth of field, NO text, NO caption_shade.

    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
    python3 deliver.py [draft]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector, Matrix                             # noqa: E402

H, K = C.H, C.K
WORK = os.path.join(HERE, "work")
TAKE = "s17"
PRESET, LIGHT = "ship_aerial", "NOON"
SHOT_T0, SHOT_T1 = 42.65, 46.12
H_IN, H_OUT = 9, 9
G0, G1 = C.g_bound(SHOT_T0), C.g_bound(SHOT_T1)          # shot = g G0..G1-1
FIRST_G, G_LAST = G0 - H_IN, G1 + H_OUT - 1
GS = list(range(FIRST_G, G_LAST + 1))
FINAL_SPP = 10                                           # H.STATE['samples'] of ship_aerial (cost_report): Take() checks it

SEAK = float(os.environ.get("SEAK", "1"))                    # sea clock rate (1 = real time)
S = 1.85                                                 # metres -> world D
AZ = float(os.environ.get("AZ", "183.59"))              # camera azimuth about the ship vs the aerial preset (deg): ~150 = from BEHIND the ship, so the long V wake
                                                         # trails toward the camera and the ship sails away from it as the camera pulls back
DIST0 = float(os.environ.get("DIST0", "0.9"))          # start distance as a fraction of the preset aerial distance
_loc, _look = Vector((-70.0, 95.0, 85.0)) * S, Vector((2.0, 6.0, 14.0)) * S
_d = Matrix.Rotation(math.radians(AZ), 3, "Z") @ ((_loc - _look) * DIST0)
CAM_LOOK0, CAM_LOC0 = _look, _look + _d
_f = (CAM_LOOK0 - CAM_LOC0).normalized(); _u = Vector((_f.y, -_f.x, 0.0)).normalized().cross(_f).normalized()
_o = _u * (float(os.environ.get("OFF", "-160")) * (CAM_LOOK0 - CAM_LOC0).length / C.F_PX)          # start framing offset (px)
CAM_LOOK0, CAM_LOC0 = CAM_LOOK0 + _o, CAM_LOC0 + _o
G_WORD = C.cap_g("ยิ่งไกล")                              # 1370: the strongest word
_S = [float(v) for v in os.environ.get('SNP', '1377,15,0.70,2.3,-120,60').split(',')]   # snap: start g, frames, k, peak, shift right/up (D)
SNAP = (int(_S[0]), int(_S[0] + _S[1]))                                       # 13 f, x1/0.58 = 1.7 pull-back with a pan (shift), landing ~10 f after the word starts
# values found by a random search (scratchpad plan17.py) with the constraint: the whole ship inside the frame (30 px margin) on EVERY frame
_P = [float(v) for v in os.environ.get("CAMP", "-0.035,60,106.84,-26").split(",")]      # push (pull), slide px/s, rise px/s, arc deg/s
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, FIRST_G, G_LAST, push=_P[0], slide_px=_P[1], rise_px=_P[2], arc_deg_s=_P[3], decay=0.1,
                snaps=[dict(g=SNAP, k=_S[2], peak=_S[3], shift=(_S[4], _S[5]))])


def widen_sea(preset, k, nu, nv):
    """the sea is ONE grid fitted to the preset camera's footprint; a pull-back would show its edge.  Runtime patch (set modules stay
    untouched): fit the grid to a virtual camera k times farther from the look point on the same axis (a k times wider footprint)."""
    import h19_ship as SH
    P = SH.PRESETS[preset]
    loc, look = Vector(P["cam"]["loc"]), Vector(P["cam"]["look"])
    P["cam"] = dict(P["cam"], loc=tuple(look + Matrix.Rotation(math.radians(AZ), 3, "Z") @ ((loc - look) * k)))   # same azimuth as our camera
    P["sea_nu"], P["sea_nv"] = nu, nv
    # a LONG white V wake trailing far behind the ship (the set's wake fades by ~150 m): the set's own 'streaks' hook (broken foam lines,
    # ship frame, metres): two Kelvin arms (half-angle ~19 deg) + the turbulent centre line, each 300 m long
    L = 300.0
    P["streaks"] = list(P.get("streaks", [])) \
        + [((sx * 3.5, -21.0), (sx * (3.5 + sl * L), -21.0 - L), wd, am) for sx in (-1, 1)
           for (sl, wd, am) in ((0.34, 4.0, 1.0), (0.27, 3.4, 1.0), (0.21, 3.0, 1.0), (0.15, 2.6, 1.0), (0.09, 2.2, 1.0))] \
        + [((0.0, -21.0), (0.0, -21.0 - L), 3.0, 0.7)]


class Take(C.Take):
    def __init__(self, quality="preview"):
        widen_sea(PRESET, float(os.environ.get("WIDEN", "11")), int(os.environ.get("NU", "1300")), int(os.environ.get("NV", "1800")))
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_" + TAKE)
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(C.bf(FIRST_G), *CAM.at(FIRST_G))
        g_ = C.bpy.data.objects.get('glint')                      # tone down the glare patches (sun glint)
        if g_ is not None:
            g_.data.energy *= float(os.environ.get('GLINT', '0.45'))

    def pose(self, gs):
        for g in gs:
            f = C.bf(g)
            self.key_set(f, sea=g / 30.0 * SEAK, roll=g / 30.0 * SEAK)           # same t, every frame
            self.key_cam(f, *CAM.at(g))
            C.key_vis([o for o in (C.bpy.data.objects.get('gulls_gullt'), C.bpy.data.objects.get('gulls_gullw')) if o], False, f)   # no gulls (clipped at the edge)

    def report(self, g):
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 2) for c in loc], heads={}, dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [C.bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        for r in rows[::6]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if FIRST_G <= g <= G_LAST]
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
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else FINAL_SPP
        quality = "final" if scale >= 1.0 else "preview"
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
