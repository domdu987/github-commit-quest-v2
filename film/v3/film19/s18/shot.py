#!/usr/bin/env python3
"""shot.py -- film 19 take s18 = shot 18: "ลูกชายเขาพกมันข้ามทะเลไปจาไมกา" -- the ship under full sail with bow wave and wake, swell crest in the foreground;
snap on "จาไมกา" (caption "ไปจาไมกา" 47.68 s -> g 1433, the word heard ~g 1438).
SHIP ship_hero / NOON, no actors.  g 1384..1467 (46.12-48.92 s) + 9 handle frames each side (dissolve 11 in from shot 17, dissolve 13 out to shot 19): g 1375..1476.
The ship sits at the origin (it 'sails' by the sea moving: set_sea(g/30) and set_roll(g/30) keyed on EVERY frame; the wake is part of the set).
Camera (c19.CamPath): push 8 %/s + slide + small arc from the hero preset pose; moving on the first frame, decay 0.1; SNAP push on "จาไมกา".  NO depth of field, NO text, NO caption_shade.

    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
    python3 deliver.py [draft]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K = C.H, C.K
WORK = os.path.join(HERE, "work")
TAKE = "s18"
PRESET, LIGHT = "ship_hero", "NOON"
SHOT_T0, SHOT_T1 = 46.12, 48.92
H_IN, H_OUT = 9, 9
G0, G1 = C.g_bound(SHOT_T0), C.g_bound(SHOT_T1)          # shot = g G0..G1-1
FIRST_G, G_LAST = G0 - H_IN, G1 + H_OUT - 1
GS = list(range(FIRST_G, G_LAST + 1))
FINAL_SPP = 12                                           # H.STATE['samples'] of ship_hero (cost_report): Take() checks it

SEAK = float(os.environ.get("SEAK", "1"))                    # sea clock rate (1 = real time)
S = 1.85                                                 # metres -> world D
# hero preset pose, pulled back (DS x the preset distance) so the WHOLE ship fits the frame with a margin; the ship then travels across the frame
# (slide + orbit) and a snap pushes in x1.33 with a pan on the word.  Values from a random search (scratchpad plan18.py) under the constraint:
# every key point of the ship's bbox (bow, stern, mast tops, flanks) inside the frame with >= 30 px margin on EVERY frame.
_loc, _look = Vector((-30.200786086416148, 60.27572081495611, 4.2)) * S, Vector((24.26311741508658, -23.591335979586283, 9.440777928304122)) * S
DS = float(os.environ.get("DS", "1.51"))
_loc = _look - (_look - _loc) * DS
_L = (_look - _loc).length
_f = (_look - _loc).normalized(); _r = Vector((_f.y, -_f.x, 0.0)).normalized(); _u = _r.cross(_f).normalized()
_o = _r * (float(os.environ.get("OX", "-47.8")) * _L / C.F_PX) + _u * (float(os.environ.get("OY", "22.95")) * _L / C.F_PX)
CAM_LOC0, CAM_LOOK0 = _loc + _o, _look + _o
G_WORD = C.cap_g("ไปจาไมกา") + 5                         # ~1438: the word จาไมกา (the caption phrase starts at ไป, 1433)
SNAP = (1428, 1445)                                     # 17 f, x1.33 with a pan, landing on the word
_P = [float(v) for v in os.environ.get("CAMP", "0.02,94.55,7.59,-13.76").split(",")]      # push, slide px/s, rise px/s, arc deg/s
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, FIRST_G, G_LAST, push=_P[0], slide_px=_P[1], rise_px=_P[2], arc_deg_s=_P[3], decay=0.1,
                snaps=[dict(g=SNAP, k=1.33, peak=2.0, shift=(-1.06, -0.91))])


def widen_sea(preset, k, nu, nv):
    """the sea is ONE grid fitted to the preset camera's footprint; a pull-back would show its edge.  Runtime patch (set modules stay
    untouched): fit the grid to a virtual camera k times farther from the look point on the same axis (a k times wider footprint)."""
    import h19_ship as SH
    P = SH.PRESETS[preset]
    loc, look = Vector(P["cam"]["loc"]), Vector(P["cam"]["look"])
    P["cam"] = dict(P["cam"], loc=tuple(look + (loc - look) * k))
    P["sea_nu"], P["sea_nv"] = nu, nv


class Take(C.Take):
    def __init__(self, quality="preview"):
        widen_sea(PRESET, float(os.environ.get('WIDEN', '3.2')), int(os.environ.get('NU', '900')), int(os.environ.get('NV', '1300')))
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_" + TAKE)
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(C.bf(FIRST_G), *CAM.at(FIRST_G))
        g_ = C.bpy.data.objects.get("glint")                    # tone the blown sun glint down (QA-tech): 40 -> GLINT x the set's energy
        if g_ is not None:
            g_.data.energy *= float(os.environ.get("GLINT", "0.45"))

    def pose(self, gs):
        for g in gs:
            f = C.bf(g)
            self.key_set(f, sea=g / 30.0 * SEAK, roll=g / 30.0 * SEAK)           # same t, every frame
            self.key_cam(f, *CAM.at(g))
            C.key_vis([o for o in (C.bpy.data.objects.get('gulls_gullt'), C.bpy.data.objects.get('gulls_gullw')) if o], False, f)   # no gulls (one was clipped by the edge)

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
