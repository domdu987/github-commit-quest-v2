#!/usr/bin/env python3
"""shot.py -- film 19 take s07 = shot 7 (HALL hall_window DAY), g 466..544 + 9 in-handle (457..465) + 9 out-handle (545..553).
"นักดาราศาสตร์ในคณะกรรมการบอกว่า ต้องวัดดวงจันทร์" (15.54-18.17 s): astro19 at the telescope points up at the painted Moon picture, lecturing;
astro19_b and astro19_c nod along.  Camera: slide + push + arc from the other side of the room than shot 3; SNAP on "คณะกรรมการ"
(16.58 -> g 500).  Mouths flat (no quote).  No DOF, no text, no caption_shade.  Hook keyed every frame: candles.
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(15.54), C.g_bound(18.17)    # 466, 545 (exclusive)
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1
GS = list(range(G_FIRST, G_LAST + 1))
G_SNAP_WORD = C.g_of(16.58)                    # "คณะกรรมการ" -> g 500
SNAP = (G_SNAP_WORD - 8, G_SNAP_WORD + 8)
LIGHT, PRESET = "DAY", "hall_window"
FINAL_SPP = 8
CONTACT = dict(width=1.6, depth=0.75, color="#1a1626", opacity=0.9)

CAM_LOC0 = (-1.6, -3.7, 2.5)
CAM_LOOK0 = (-1.95, 2.6, 2.55)
class SwayCam(C.CamPath):
    """CamPath + a slow lateral sway of the camera body (loc only): parallax of the dense hall that keeps all three astronomers framed."""
    SWAY_D, SWAY_T = 2.2, 2.4

    def at(self, g):
        loc, look = C.CamPath.at(self, g)
        f = (look - loc).normalized()
        r = Vector((f.y, -f.x, 0.0)).normalized()
        ph = 2.0 * math.pi * (g - G_FIRST) / (30.0 * self.SWAY_T)
        taper = 1.0 - u_of(g, SNAP[0] + 6, SNAP[1] + 14, "sine")      # sway settles: the end framing keeps all three inside
        return loc + r * (self.SWAY_D * taper * math.sin(ph)), look


CAM = SwayCam(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=0.015, slide_px=0.0, rise_px=0.0, arc_deg_s=0.0, decay=0.15,
              snaps=[dict(g=SNAP, k=1.15, peak=2.0, shift=(0.0, -0.10))])

MARK_A = (-2.8, 2.5, 0.0)                      # astro19 lecturing (faces screen-left, points at the Moon)
MARK_B = (-0.85, 3.4, 0.0)                      # astro19_b nodding (faces screen-left)
MARK_C = (-1.60, 1.45, 0.0)                      # astro19_c nodding (faces screen-right)


def nod(g, ph, amp=0.25, hz=1.8):
    return amp * (0.5 + 0.5 * math.sin(2 * math.pi * hz * g / 30.0 + ph))


def pose_a(g):
    p = dict(cast19.STORY19["astro_mock_point"][1])
    p["mirror"] = True
    p["mouth"] = "flat"
    p["expr"] = "smug"
    p["yaw"] = 0.3
    p["pitch"] = -0.35 + 0.05 * math.sin(g * 0.3)                   # chin up at the Moon
    p["lean"] = -3.0 + 2.0 * math.sin(g * 0.2)
    p["head_roll"] = 4.0 * math.sin(g * 0.25)
    p["arm_r"] = dict(hand=(0.95, -0.60 + 0.10 * math.sin(g * 0.5)), shape="point", bend=-0.2, stretch=1.45, layer="top")   # jabs up at the Moon
    p["arm_l"] = "akimbo"
    p["blink"] = blink(g, [480, 521])
    u_look = 1.0 - u_of(g, SNAP[0] - 2, SNAP[0] + 6, "sine")                 # eyes follow the point up-left at the Moon, back to the lens on the snap
    p["gaze"] = (1.0 * u_look, -1.0 * u_look)
    p["yaw"] = 0.3 + 0.35 * u_look
    return p


def pose_b(g):
    p = dict(cast19.STORY19["astro_b_idle"][1])
    p["mirror"] = True
    p["yaw"] = 0.35
    p["expr"] = "unimpressed"
    p["mouth"] = "flat"
    p["pitch"] = -0.05 + nod(g, 0.0)
    p["lean"] = 1.0 + 3.0 * nod(g, 0.0)
    p["arm_r"] = dict(hand=(0.35, 0.55), bend=0.8, shape="open", layer="top")                  # a hand at the chin
    p["arm_l"] = dict(hand=(-0.35, 1.0), bend=0.5)
    p["gaze"] = (0.8, 0.3)
    p["blink"] = blink(g, [470, 512, 540])
    p["legs"] = "stand"
    return p


def pose_c(g):
    p = dict(cast19.STORY19["astro_c_idle"][1])
    p["mirror"] = True
    p["yaw"] = 0.35
    p["expr"] = "smirk"
    p["mouth"] = "flat"
    p["pitch"] = -0.05 + nod(g, 1.9, 0.3)
    p["lean"] = 1.0 + 3.0 * nod(g, 1.9)
    p["arm_r"] = dict(hand=(0.3, 0.9), bend=0.8, shape="open", layer="top")
    p["arm_l"] = dict(hand=(-0.4, 1.0), bend=0.5)
    p["gaze"] = (0.8, 0.5)
    p["blink"] = blink(g, [490, 530])
    return p


def bob(g, ph=0.0):
    return 0.012 * math.sin(2 * math.pi * g / 20.0 + ph)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s07")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.ab = self.actors["ab"] = C.make_actor("ab", "astro19_b", os.path.join(WORK, "sprites"), contact=CONTACT, cam=self.cam)
        self.aa = self.actors["aa"] = C.make_actor("aa", "astro19", os.path.join(WORK, "sprites"), contact=CONTACT, cam=self.cam)
        self.ac = self.actors["ac"] = C.make_actor("ac", "astro19_c", os.path.join(WORK, "sprites"), contact=CONTACT, cam=self.cam)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.ab, f, Vector(MARK_B) + Vector((0, 0, bob(g))))
            C.place(self.aa, f, Vector(MARK_A) + Vector((0, 0, bob(g, 1.7))))
            C.place(self.ac, f, Vector(MARK_C) + Vector((0, 0, bob(g, 3.1))))
            self.key_set(f, candles=1.0)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.ab.pose(f, pose_b(g), camera=self.cam)
            self.aa.pose(f, pose_a(g), camera=self.cam)
            self.ac.pose(f, pose_c(g), camera=self.cam)
        self.sprites_for([(self.ab, 256), (self.aa, 256), (self.ac, 256)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        for r in rows:
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
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
