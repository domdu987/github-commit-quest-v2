#!/usr/bin/env python3
"""shot.py -- film 16 take s16 = shot 16, TRENCH CUT-AWAY (LINE trench_cut / DUSK): the lead pipe split open, cloth torn, sparks leaking.
Shot g 1007..1074 (33.57-35.82 s), handles 9 frames each side (g 998..1083).  Hard cut in and out.
    g 998..1012  whip-tilt DIVE: the camera starts high above the pit looking steeply down and tilts / drops to the elevation view
    g 1012..     slow slide along the pipe + push 7 %/s; SNAP x1.7 with a sideways pan on "ไฟรั่วหายลงดิน" (35.07 s -> g 1052)
Split framed at ~45 % of the frame height (QA_ART note); the empty pit floor is cut by the push.  Nobody in frame: no mouths.
    python3 shot.py camreport | probe a:b | final a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c16 as C
from mathutils import Vector
TG = C.TG
bf, u_of, lerp = C.bf, C.u_of, C.lerp
G0, G1 = C.g_bound(33.57), C.g_bound(35.82)      # 1007, 1075 (exclusive)
H = 9
GA, GZ = G0 - H, G1 + H - 1                       # 998 .. 1083
GS = list(range(GA, GZ + 1))
G_WORD = C.cap_g("ไฟรั่วหาย")                      # 1052
SNAP = (G_WORD - 2, G_WORD + 11)                  # 1049..1064 (15 f)
DIVE = (GA + 1, GA + 30)                              # dive tilt window (the cut falls at G0 = GA + 9: the dive is already half done)
PRE = C.Vector((22.2, -96.2, 0.0))
CAM0 = Vector((20.905, -95.645, 0.278))           # preset camera
LOOK0 = Vector((24.42, -96.293, -1.85))
# split centre is ~42 % down the preset frame: tilt the look point DOWN a little so the split rises to ~45 % ... then the push drifts it
SUBJ = Vector((24.3, -96.25, -1.50)) + Vector((0.0, 0.7 * 0.995, 0.0)) * 0 
START = 0.55                                       # start 0.55 of the way from subject to preset camera: already close
LOOKC = SUBJ + Vector((-0.03, -0.75, 0.0))      # looks right of the split at g0: it starts left of centre, the slide carries it across
CAM = C.CamPath(LOOKC + (CAM0 - SUBJ), LOOKC, GA, GZ, push=0.09, slide_px=-90.0, rise_px=0.0, arc_deg_s=0.0, decay=0.15,
                snaps=[dict(g=SNAP, k=1.9, peak=1.75, shift=(0.0, 0.0))])
HIGH = Vector((-1.2, 0.5, 2.4))                    # dive start: offset from the drift pose (high above, a little behind)


def cam_pose(g):
    loc, look = CAM.at(g)
    u = u_of(g, DIVE[0], DIVE[1], "cubic") if hasattr(C.ease, "__call__") else 0.0
    k = 1.0 - u
    if k > 0:
        loc = loc + HIGH * (k ** 1.6)
        look = look + Vector((0.0, 0.0, -0.3)) * k
    return loc, look


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "trench_cut", light="DUSK", quality=quality, name="cam_s16")
        self.key_cam(bf(GA), *cam_pose(GA))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_pose(g))
            TG.set_leak("pipe", 1.0, frame=f)

    def report(self, g):
        self.scene.frame_set(bf(g))
        loc, look = cam_pose(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads={}, split_px=TG.project(tuple(SUBJ + Vector((0, 0, 0.0)))))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = C.CamPath.report(CAM, GS[:-1])
        for r in rows[::4]: print(r)
        print("longest run under 0.25 px/frame: %d frames" % worst); sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GZ]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                st = Tk.render([g], out, scale=scale, samples=6)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK if False else HERE + "/work", "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
