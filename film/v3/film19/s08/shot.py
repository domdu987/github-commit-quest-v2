#!/usr/bin/env python3
"""shot.py -- film 19 take s08 = shot 8 (g 545..660, + 9 handle frames each side: g 536..669).
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

G0, G1 = C.g_bound(18.17), C.g_bound(22.02)              # 545, 661: shot 8 = g 545..660
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1              # 536 .. 669
GS = list(range(G_FIRST, G_LAST + 1))
G_QUOTE = C.cap_g("นาฬิกาเนี่ยนะ")                        # 637
G_MOUTH0 = 623                                           # the grin / open mouth starts no earlier than g 619 (window 20.80 s = g 622 +-4)
G_LAUGH0 = C.cap_g("หัวเราะลั่น") - 9                      # laugh starts building before the caption
SNAP = (G_QUOTE - 4, G_QUOTE + 14)
BLINKS = [560, 584]

YAW0 = float(os.environ.get("YAW0", "1.35"))
LIGHT, PRESET, FINAL_SPP, PPD = "DAY", "hall_low", 8, 320

SUBJ = Vector((-3.24, 3.24, 2.62))                        # chest/neck of the mocker at his mark
CAM_LOC0 = (-3.30, -1.85, 1.15)
CAM = C.CamPath(CAM_LOC0, tuple(SUBJ), G_FIRST, G_LAST, push=0.07, slide_px=-45.0, rise_px=0.0, arc_deg_s=11.5, decay=0.15,
                snaps=[dict(g=SNAP, k=1.3, peak=2.5, shift=(0.80, -0.25))])

ST = cast19.STORY19
IDLE, LAUGH, POINT = ST["astro_idle"][1], ST["astro_belly_laugh"][1], ST["astro_mock_point"][1]
LR = lambda a, b, u: puppet.lerp_pose("astro19", a, b, u)


def pose_of(g):
    turn = u_of(g, G_FIRST + 12, G0 + 52, "sine")
    smug = dict(IDLE)
    smug.update(yaw=lerp(YAW0, 0.12, turn), pitch=-0.05, head_roll=2.0 * math.sin(g * 0.15), expr="smug", mouth="flat")
    if g < G_LAUGH0:
        shake = u_of(g, G_LAUGH0 - 30, G_LAUGH0)               # shoulders begin to shake
        p = dict(smug)
        p["squash"] = (1.0 + 0.012 * shake * math.sin(g * 1.7), 1.0 - 0.012 * shake * math.sin(g * 1.7))
    else:
        u = u_of(g, G_LAUGH0, G_LAUGH0 + 8)
        base = LR(smug, LAUGH, u) if u < 1 else dict(LAUGH)
        base["yaw"] = lerp(smug["yaw"], 0.12, u)
        p = cast19.laugh_cycle(((g - G_LAUGH0) % 30) / 30.0, base)
        sq = p["squash"]
        p["squash"] = (1.0 + 2.0 * (sq[0] - 1.0), 1.0 + 2.0 * (sq[1] - 1.0))     # stronger belly bounce
        p["expr"] = "laughing" if (u >= 0.5 and g >= G_MOUTH0) else "smug"
        if g < G_MOUTH0:
            p["mouth"] = "flat"
        if g >= G_QUOTE + 3:                                    # the quote: he straightens up and points
            v = u_of(g, G_QUOTE + 3, G_QUOTE + 13, "sine")
            tgt = dict(POINT, yaw=0.30)
            q = LR(p, tgt, v)
            q["squash"] = (1.02 + 0.015 * math.sin(g * 0.9), 0.98 - 0.015 * math.sin(g * 0.9))
            q["expr"] = "smug"
            p = q
    # mouth: still outside the quote window; inside, driven
    if C.mouth_open_at(g) and g >= G_MOUTH0:
        if G_QUOTE - 2 > g:                                     # "ฮ่า ฮ่า ฮ่า!" belly laugh: mouth driven, wide
            p["mouth"] = cast19.talk_mouth(g, 1.0, seed=3, hold=3) if g % 10 < 5 else "talk_b"
        else:
            p["mouth"] = cast19.talk_mouth(g, 1.0)
    else:
        p.pop("mouth", None) if p.get("expr") == "laughing" else p.__setitem__("mouth", "flat")
    p["gaze"] = (lerp(0.9, 0.0, u_of(g, G0 + 20, G0 + 55, "sine")), 0.0)
    p["blink"] = blink(g, BLINKS)
    p["t"] = g / 30.0
    return p


def hop_z(g):
    if g < G_LAUGH0 + 6 or g > G_QUOTE + 3:
        return 0.0
    ph = (g - G_LAUGH0) / 30.0 * 3.0
    return 0.08 * (1.0 + math.sin(2 * math.pi * ph - math.pi / 2))      # 0..0.06 D at 3 Hz


# director option (3): the chair(s) of the Board table's left row stand between the orbiting camera and the mocker during the snap.
# They are merged into per-material meshes, so delete the FACES whose centre lies in this box (set dressing from the shot, never the set module).
CHAIR_BOX = ((-2.95, -1.35), (0.7, 3.8), (0.04, 2.45))          # x, y, z in world D


def hide_chairs(box=CHAIR_BOX):
    import bmesh
    n = 0
    for ob in list(C.bpy.data.objects):
        if ob.type != "MESH" or not ob.name.startswith("hall_"):
            continue
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        M = ob.matrix_world
        dead = [f for f in bm.faces if all(lo <= c <= hi for c, (lo, hi) in zip(M @ f.calc_center_median(), box))]
        if dead:
            bmesh.ops.delete(bm, geom=dead, context="FACES")
            bm.to_mesh(ob.data)
            n += len(dead)
        bm.free()
    return n


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s08")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        C.bpy.context.view_layer.update()
        print("take: hid %d chair faces" % hide_chairs(), flush=True)
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
