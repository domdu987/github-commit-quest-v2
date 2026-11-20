#!/usr/bin/env python3
"""shot.py -- film 19 take s10 = shot 10 (g 773..861 + handles g 764..772 in, 862..871 out).
"นักปราชญ์หัวเราะกันครืน แล้วเรียกเขาว่า ไอ้ช่างไม้" -- the whole Board laughs and calls him 'country carpenter'.
HALL hall_wide / DAY.  The camera stands at the window end of the Board room looking DOWN the hall toward the double doors: the laughing
Board (astro19 the mocker, astro19_b, astro19_c, wigs bouncing at 3 Hz, fingers pointing) lines both walls, near the lens; Harrison
stands small and alone at the far door with his tricorne held to his chest (harrison19 default).  The camera drifts (push + slide + arc
across the room) and SNAPS in on him on "ไอ้ช่างไม้" (caption 28.10 s).  Nobody speaks: laughing / still expression mouths only.

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <dir> [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, cast19 = C.H, C.K, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(25.78), C.g_bound(28.74)     # 773, 862: shot 10 = g 773..861
H_IN, H_OUT = 9, 10                              # CUT in (9), DIS 15 out -> 10 handle frames
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1      # 764..871
GS = list(range(G_FIRST, G_LAST + 1))
G_WORD = C.cap_g("ไอ้ช่างไม้")                   # 846: caption start of the nickname
SNAP = (G_WORD - 10, G_WORD + 4)                 # 836..850 (14 frames): the whip peaks about g 843, the word is at g 846
WHIP = (SNAP[0] - 1, SNAP[1] + 2)                # frames rendered with Cycles motion blur (shutter 0.9): the Board leaves as a smear
LIGHT, PRESET, FINAL_SPP = "DAY", "hall_wide", 8

HAR_XY = (0.0, -5.0)                             # AT the door (harrison_door is (0, -5.55)); the open leaves frame him                             # Harrison just inside the doors, left of the aisle (screen-right of centre)
CAM_LOC0 = (0.0, 9.4, 3.6)
CAM_LOOK0 = (0.0, -5.0, 2.0)
class _Sway(object):
    """CamPath plus a small handheld sway (translation only, level horizon): 0.065 D at 2.6 Hz lateral, 0.05 D at 3.4 Hz vertical"""
    def __init__(self, cp):
        self.cp = cp

    def at(self, g):
        loc, look = self.cp.at(g)
        f = (look - loc).normalized()
        r = Vector((f.y, -f.x, 0.0)).normalized()
        off = r * (0.065 * math.sin(2 * math.pi * g * 2.6 / 30.0 + 0.7)) + Vector((0, 0, 0.05 * math.sin(2 * math.pi * g * 3.4 / 30.0)))
        return loc + off, look + off

    def report(self, gs, depth=None):
        return self.cp.report(gs, depth)


_CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=0.03, slide_px=0.0, rise_px=0.0, arc_deg_s=0.0, decay=0.05,
                snaps=[dict(g=SNAP, k=3.0, peak=3.0, shift=(0.0, 0.7))])
CAM = _Sway(_CAM)

# ---------------------------------------------------------------------------- cast
STAND = dict(mock=(-2.1, 1.0, 0.0), bb=(2.2, 1.5, 0.0), cc=(0.8, 0.5, 0.0))
# name, cast, mark, base STORY19 pose, mirror (faces screen-left), phase offset (frames)
BOARD = [
    ("mock", "astro19", "mocker_table", "astro_belly_laugh", True, 0),
    ("bb", "astro19_b", "astro_a", "astro_b_laugh", True, 7),
    ("cc", "astro19_c", "astro_c", "astro_c_laugh", False, 3),
]


def laugh_pose(name, g):
    cast, mark, base, mir, off = [(b[1], b[2], b[3], b[4], b[5]) for b in BOARD if b[0] == name][0]
    base_p = dict(cast19.STORY19[base][1])
    ph = ((g + off) % 30) / 30.0
    p = cast19.laugh_cycle(ph, base_p)
    p["mirror"] = mir
    p["mouth"] = None
    del p["mouth"]
    if (g // 9 + off) % 2 == 0:                          # a pointing finger at Harrison (screen-centre), alternating hands
        p["arm_r"] = dict(hand=(1.0, 0.12), shape="point", bend=-0.4, stretch=1.25)
    p["blink"] = blink(g + off, [10 + off])
    p["t"] = g / 30.0
    return p


def laugh_z(g, off):
    """~0.06 D bounce at ~3 Hz"""
    return 0.06 * abs(math.sin(math.pi * 3.0 * (g + off) / 30.0))


def harrison_pose(g):
    p = dict(cast19.STORY19["harrison_hopeful_door"][1])       # hands clasped at the chest (no hat: a flat tricorne wedge read badly)
    p["expr"] = "sad"
    p["mirror"] = False
    p["yaw"] = 0.0
    p["lean"] = 1.5 + 1.0 * math.sin(g * 0.12)
    p["head_roll"] = 2.0 * math.sin(g * 0.1)
    p["pitch"] = 0.1
    p["blink"] = blink(g, [800, 830, 870])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s10")
        assert self.final_samples() == FINAL_SPP
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        for b in BOARD:
            self.actors[b[0]] = C.make_actor(b[0], b[1], os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.doors = [o for o in C.bpy.data.objects if o.name.startswith("hdoorleaf")]      # the open door leaves stand behind / around the camera (x +-0.9..1.8, y -6.1..-4.5): hidden, never in view
        self.har = self.actors["har"] = C.make_actor("har", "harrison19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)

    def pose(self, gs):
        marks = self.A["marks"]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            for b in BOARD:
                C.place(self.actors[b[0]], f, Vector(STAND[b[0]]) + Vector((0, 0, laugh_z(g, b[5]))))
            C.place(self.har, f, Vector((HAR_XY[0], HAR_XY[1], 0.0)))
            self.key_set(f, candles=1.0)
            pass
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for b in BOARD:
                self.actors[b[0]].pose(f, laugh_pose(b[0], g), camera=self.cam)
            self.har.pose(f, harrison_pose(g), camera=self.cam)
        self.sprites_for([(self.actors[b[0]], 192) for b in BOARD] + [(self.har, 512)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        out = []
        for g in gs:                                   # whip frames get Cycles camera motion blur, all others none
            blur = WHIP[0] <= g <= WHIP[1]
            self.scene.render.use_motion_blur = blur
            self.scene.render.motion_blur_shutter = 0.9
            try:
                self.scene.cycles.motion_blur_position = "CENTER"
            except Exception:
                pass
            out += C.Take.render(self, [bf(g)], out_dir, scale=scale, samples=samples, threads=threads)
        return out


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
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        samples = samples or FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft" if scale == 0.5 else "q%g" % scale)
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
