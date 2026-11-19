#!/usr/bin/env python3
"""shot.py -- film 16 take s18 = shot 18 (LINE line_road / DUSK): the mocker in the open buggy (mule in the shafts) taunts Morse.
Shot g 1119..1225 (37.30-40.86 s), handles 9 f each side (g 1110..1234).  Hard cut in (continuity: shot 17 is the key crate at the furrow
end; here a different place, on the road) and hard cut out to the dissolve of shot 19.
LIP-SYNC ONLY in the quote 38.46-40.80 s (event frames 1157..1227): talk_mouth(g); before it the mouth is 'flat' (smug, leaning out),
laughing + tears from the blink at 1154; belly bounce +/-0.06 D at 3 Hz from there.  The mule is a cast16 card (harness 2, walk), the buggy
rolls along +x at 1.4 D/s (wheels turn); the camera tracks it low from the furrow side (pipe + spoil ridge in the foreground).
SNAP x1.7 with a pan on "ใต้ดินแล้ว" (40.12 s -> g 1207).
    python3 shot.py camreport | probe a:b | stills a:b out [scale] | final a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c16 as C
from mathutils import Vector
TG, cast16, actors = C.TG, C.cast16, C.actors
bf, u_of, lerp, blink = C.bf, C.u_of, C.lerp, C.blink
WORK = os.path.join(HERE, "work")
G0, G1 = C.g_bound(37.30), C.g_bound(40.86)      # 1119 .. 1226 (exclusive)
H = 9
GA, GZ = G0 - H, G1 + H - 1
GS = list(range(GA, GZ + 1))
Q0, Q1 = C.g_of(38.46), C.g_of(40.80)            # lip-sync window 1157 .. 1227
G_LAUGH = Q0 - 3                                  # expression change on the closed frame of a blink
G_WORD = C.g_of(40.12)                            # 1207 "ใต้ดินแล้ว"
SNAP = (G_WORD - 3, G_WORD + 11)
V = 1.4 / 30.0                                    # buggy speed, D per frame
X0 = 62.0
bx = lambda g: X0 + V * (g - GA)

SUBJ0 = Vector((X0 + 3.0, -2.3, 3.3))             # mocker's chest / head, road
OFF = Vector((1.3, -8.3, -1.8))                   # camera: furrow side, low (z ~ 1.3), pitch ~ 16 deg
CAM = C.CamPath(SUBJ0 + OFF, SUBJ0, GA, GZ, push=0.05, slide_px=-25.0, arc_deg_s=0.0, decay=0.3,
                snaps=[dict(g=SNAP, k=2.7, peak=1.75, shift=(-2.6, 0.6))])


def cam_pose(g):
    loc, look = CAM.at(g)
    d = Vector((1.0 * V * (g - GA), 0, 0))
    return loc + d, look + d


def mocker_pose(g):
    p = dict(cast16.STORY16["mocker_taunt_buggy"][1])
    if g >= Q0 - 3 and g <= Q1 + 3 and Q0 <= g <= Q1:
        p["mouth"] = cast16.talk_mouth(g, 1.0)
    else:
        p["mouth"] = "flat"
    if g < G_LAUGH:
        p["expr"] = "smug"; p.pop("fx", None)
    p["blink"] = blink(g, [G_LAUGH - 1, 1180, 1214])
    ph = math.sin(2 * math.pi * 3.0 * g / 30.0)
    laugh = u_of(g, G_LAUGH, G_LAUGH + 6)
    p["squash"] = (1.01 + 0.02 * ph * laugh, 0.99 - 0.02 * ph * laugh)
    p["head_roll"] = p.get("head_roll", 0) + 3.0 * math.sin(g * 0.2)
    p["t"] = g / 30.0
    return p, 0.06 * ph * laugh


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "line_road", light="DUSK", quality=quality, name="cam_s18")
        self.key_cam(bf(GA), *cam_pose(GA))
        self.scene.frame_set(bf(GA))
        sd = os.path.join(WORK, "sprites")
        TG.set_buggy(bx(GA), frame=bf(GA))
        self.moc = self.actors["moc"] = C.make_actor("moc", "mocker", sd, canvas=cast16.CANVAS16["mocker"], cam=self.cam)
        self.mul = self.actors["mul"] = C.make_actor("mul", "mule", sd, canvas=cast16.CANVAS16_BUGGY["mule"], cam=self.cam, head_flip=False)
        self.mk = {}

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_pose(g))
            TG.set_buggy(bx(g), frame=f)
            m = TG.STATE["marks"]
            _, bounce = mocker_pose(g)
            mm, ml = m["mocker_buggy"], m["mule_buggy"]
            C.place(self.moc, f, (mm[0], mm[1], mm[2] + bounce))
            C.place(self.mul, f, (ml[0] - 2.4, ml[1], ml[2]))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.moc.pose(f, mocker_pose(g)[0], camera=self.cam)
            mp = cast16.cycle("mule", g / 54.0, "walk", 1, dict(harness=2))
            self.mul.pose(f, mp, camera=self.cam)
        self.sprites_for([(self.moc, 256), (self.mul, 256)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        return dict(g=g, cam=[round(c, 3) for c in cam_pose(g)[0]], heads=C.head_report(self, f), mouth=("sync" if Q0 <= g <= Q1 else "flat"))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = C.CamPath.report(CAM, GS[:-1])
        print(rows[0], rows[-1]); print("longest run under 0.25 px/frame: %d" % worst); sys.exit(0)
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
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
