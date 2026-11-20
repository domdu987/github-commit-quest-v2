#!/usr/bin/env python3
"""shot.py -- film 19 take s09 = shot 9 (g 661..772, + 9 handle frames each side: g 652..781).
HALL hall_low / DAY, the mocker's spot by the telescope (mark mocker_telescope), astro19 alone.
"กับดวงดาวเท่านั้น คนหนึ่งหัวเราะลั่น" "นาฬิกาเนี่ยนะ!"
    g 536..602  smug, he turns from profile toward the camera, shoulders starting to shake (fixed smug mouth: no quote yet)
    g 603..636  BELLY LAUGH (laugh_cycle, ~3 Hz bounce, squash + a 0.06 D hop of the feet); fixed laughing mouth until the window opens
    g 622..     lip-sync window opens (mouth_open_at: 20.80 s -0.15): "ฮ่า ฮ่า ฮ่า!" mouth driven (laugh), then "นาฬิกาเนี่ยนะ!" (g 637)
    g 637..669  mock point (astro_mock_point) with talk_mouth(g)
Camera: low, push 9 %/s + slide, snap x1.45 with a pan on "นาฬิกาเนี่ยนะ" (g 637).  No DOF, no text, no caption_shade.
    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")
import puppet                                            # noqa: E402

G0, G1 = C.g_bound(22.02), C.g_bound(25.78)              # 661, 773: shot 9 = g 661..772
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1              # 652 .. 781
GS = list(range(G_FIRST, G_LAST + 1))
G_QUOTE = C.cap_g("จับเวลาเอง")                           # 748
G_KING = C.cap_g("ให้พระราชามา")                          # 722: the deepest bow
SNAP = (G_QUOTE - 5, G_QUOTE + 14)
BLINKS = [690, 735, 770]

LIGHT, PRESET, FINAL_SPP, PPD = "DAY", "hall_low", 8, 400

SUBJ = Vector((-3.24, 3.24, 2.55))
CAM_LOC0 = (-4.9, 0.55, 1.25)
CAM = C.CamPath(CAM_LOC0, tuple(SUBJ), G_FIRST, G_LAST, push=0.07, slide_px=25.0, rise_px=0.0, arc_deg_s=5.0, decay=0.15,
                snaps=[dict(g=SNAP, k=1.5, peak=1.9, shift=(-0.2, 0.0))])

ST = cast19.STORY19
POINT, BOW = ST["astro_mock_point"][1], ST["astro_mock_bow"][1]
LR = lambda a, b, u: puppet.lerp_pose("astro19", a, b, u)


def pose_of(g):
    """mock-royal bow miming the timing of a pocket watch; the mouth is driven for the whole shot (quote window 20.80-25.75)."""
    u = u_of(g, G_FIRST, G0 + 14, "sine")                       # from the pointing end of shot 8 into the bow
    p = LR(dict(POINT, yaw=0.30), BOW, u)
    dip = 0.5 + 0.5 * math.sin(2 * math.pi * (g - G_KING) / 60.0 - 1.2)       # the bow rises and dips (~2 s period... quicker at the king)
    kb = u_of(g, G_KING - 6, G_KING + 10, "sine") - u_of(g, G_QUOTE - 6, G_QUOTE + 8, "sine")
    p["lean"] = 10.0 + 8.0 * dip + 10.0 * kb                    # "ให้พระราชา..." a deep royal bow
    p["head_roll"] = 8.0 * math.sin(g * 0.2)
    p["pitch"] = 0.10 + 0.25 * kb
    arm = dict(p["arm_r"])
    arm["hand"] = (0.78 + 0.05 * math.sin(g * 0.55), 0.96 + 0.07 * math.sin(g * 0.45 + 1.0))    # the hand holding the watch wobbles (timing)
    p["arm_r"] = arm
    p["squash"] = (1.0 + 0.012 * math.sin(g * 0.9), 1.0 - 0.012 * math.sin(g * 0.9))
    p["expr"] = "smug"
    p["mouth"] = cast19.talk_mouth(g, 1.0) if C.mouth_open_at(g) else "smile"
    p["blink"] = blink(g, BLINKS)
    p["t"] = g / 30.0
    return p


def hop_z(g):
    return 0.015 * math.sin(2 * math.pi * g / 24.0) ** 2        # small proud rise on the toes


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s09")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.ast = self.actors["ast"] = C.make_actor("ast", "astro19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)

    def pose(self, gs):
        mark = Vector(self.A["marks"]["mocker_telescope"])
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.ast, f, mark + Vector((0, 0, hop_z(g))))
            self.key_set(f, candles=1.0)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.ast.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.ast, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        v = look - loc
        p = pose_of(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), mouth=str(p.get("mouth")), in_window=C.mouth_open_at(g), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        for r in rows[::6]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
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
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        samples = samples or FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
