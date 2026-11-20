#!/usr/bin/env python3
"""shot.py -- film 19 take s20 = shot 20 (g 1581..1664, + 9 handle frames each side: g 1572..1673).
HALL hall_low / DAY, the mocker's spot by the telescope (mark mocker_telescope), astro19 alone.

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

G0, G1 = C.g_bound(52.71), C.g_bound(55.49)              # 1581, 1665: shot 20 = g 1581..1664
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1              # 1572 .. 1673
GS = list(range(G_FIRST, G_LAST + 1))
G_SHRUG = C.cap_g("คนเดิมยักไหล่")                        # 1615: the shrug
G_QUOTE = C.cap_g("ฟลุ๊ค")                                # 1633: "ฟลุ๊ค!" -> the snap
SNAP = (G_QUOTE - 5, G_QUOTE + 13)
BLINKS = [1590, 1648]

LIGHT, PRESET, FINAL_SPP, PPD = "DAY", "hall_low", 8, 400

SUBJ = Vector((-3.24, 3.24, 2.60))
CAM_LOC0 = (-4.9, -1.30, 1.25)
CAM = C.CamPath(CAM_LOC0, tuple(SUBJ), G_FIRST, G_LAST, push=0.10, slide_px=45.0, rise_px=0.0, arc_deg_s=13.0, decay=0.15,
                snaps=[dict(g=SNAP, k=1.5, peak=2.0, shift=(-0.3, -0.35))])

ST = cast19.STORY19
IDLE, SHRUG = ST["astro_idle"][1], ST["astro_shrug_fluke"][1]
LR = lambda a, b, u: puppet.lerp_pose("astro19", a, b, u)


def pose_of(g):
    """smug, then the shrug with both palms up on "คนเดิมยักไหล่" (g 1615); the mouth is still until the quote window opens (g 1626),
    then "ฟลุ๊ค! ต้องลองใหม่!" is driven to g 1667; after the window a still smirk."""
    u = u_of(g, G_SHRUG - 6, G_SHRUG + 6, "sine")
    p = LR(dict(IDLE, yaw=0.30), dict(SHRUG, yaw=0.20), u)
    # the shrug pumps: palms up, shoulders (lean / squash) bounce twice on "ฟลุ๊ค" and "ลองใหม่"
    pump = (math.sin(math.pi * u_of(g, G_QUOTE - 3, G_QUOTE + 8)) + 0.7 * math.sin(math.pi * u_of(g, G_QUOTE + 18, G_QUOTE + 30))) * u
    for q, sgn in (("arm_r", 1), ("arm_l", -1)):
        d = dict(p[q])
        d["hand"] = (d["hand"][0] + sgn * 0.16 * pump, d["hand"][1] + 0.30 * pump)
        p[q] = d
    p["lean"] = 7.0 * pump + 4.0 * u * math.sin(g * 0.35)
    p["head_roll"] = -6.0 * u + 5.0 * math.sin(g * 0.2) * u
    p["pitch"] = -0.2 * u - 0.1 * pump
    p["squash"] = (1.0 + 0.02 * pump, 1.0 - 0.02 * pump)
    p["expr"] = "smug"
    p["mouth"] = cast19.talk_mouth(g, 1.0) if C.mouth_open_at(g) else "smirk"
    p["blink"] = blink(g, BLINKS)
    p["t"] = g / 30.0
    return p


def hop_z(g):
    return 0.03 * math.sin(math.pi * u_of(g, G_QUOTE - 3, G_QUOTE + 6)) ** 2      # a hop of smugness on "ฟลุ๊ค"


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s20")
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
                    heads=C.head_report(self, f), wig_bottom=[round(h["y"] + 1.17 * h["w"]) for h in C.head_report(self, f).values()], mouth=str(p.get("mouth")), in_window=C.mouth_open_at(g), dof=self.cam.data.dof.use_dof,
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
