#!/usr/bin/env python3
"""shot.py -- film 16 take s10 = shot 10 (CHAMBER, DAY, low angle, CLOSER on the MOCKER): "ถ้าลวดของเอ็งส่งข่าวได้จริง ข้าจะมานั่งเฝ้ามันเอง!"
Shot 10 = g 597..697 (19.91-23.26 s); handles 9 f each side.  LIP-SYNC (talk_mouth) the whole shot (quote 2 inside 18.32-23.20 s + 0.10 s clock).
    g 588..661  mocker_boast_finger: index finger up, other hand on the chest, chin up
    g 662       pose swap on the closed frame of a blink (661 half, 662 closed, 663 half) -> mocker_boast_chest (thumps his own chest)
    g 672..686  THE PUNCH-IN (the film's one): snap x1.8 + a short truck on "เฝ้ามันเอง" (event g 677) with FOCUS LINES drawn behind him
                (puppet fx focus_lines, seed = g, redrawn every frame) from g 672 to the end of the take
Camera: low (1.25 D above the floor), head ~290 px, bearing on the other side of the axis from shot 9, push 8 %/s + slide + arc.
FG: desk-corner inkwell + quill 2.7 D from the lens, lower right.

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
G0, G1 = C.g_bound(19.91), C.g_bound(23.26)              # 597, 698 (exclusive)
H_IN, H_OUT = 9, 9
GS = list(range(G0 - H_IN, G1 + H_OUT))                  # 588..706
G_LAST = GS[-1]
G_SWAP = 662                                             # boast_finger -> boast_chest on the closed frame of the blink 661..663
G_PUNCH = (672, 686)                                     # 14 f punch-in, peak at "เฝ้ามันเอง" (event g 677)
G_FOCUS = 672                                            # focus lines on from here
LIGHT, PRESET = "DAY", "chamber_low"
BEARING = -62.0                                          # deg: camera bearing rotated off the globe on the room axis
CANVAS = (-2.875, -6.0, 2.875, 0.125)                         # wide + tall card: the focus lines reach 2.7 D from the head centre (no clipped streaks)
FOCAL_Z = 2.75                                           # D above the floor the camera looks at (chest / chin of the mocker)


def bpy_objs(*prefixes):
    return [o for o in C.bpy.data.objects if any(o.name.startswith(p) for p in prefixes)]


def mocker_mark():
    """the mocker steps out in front of his desk: world mark + 3.2 D toward the room centre, and the unit vector toward the centre"""
    m = Vector(TG.STATE["A"]["marks"]["mocker_desk"] if "A" in TG.STATE else (0, 0, 0))
    return m


class Rig(object):
    """camera path of the take; the geometry is known only after the set is built (marks), so it is created in Take.__init__"""
    pass


def cap_phrases():
    return [(c["t"], c["end"]) for c in C.captions() if 18.32 <= c["t"] < 23.2]


def lip_mouth(g):
    """'flat' outside the quote window 18.32-23.20 s (+0.10 s clock); inside: talk_mouth, closed for the last 2 frames of each phrase"""
    if g < C.g_of(18.32) or g > C.g_of(23.20):
        return "flat"
    for a, b in cap_phrases():
        if C.g_of(a) <= g < C.g_of(b):
            if g >= C.g_of(b) - 2:
                return "flat"
            break
    return cast16.talk_mouth(g, 1.0, 0.0, 2)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s10")
        A = self.A
        M = Vector(A["marks"]["mocker_desk"])
        u0 = (Vector((0.0, 12.95, 0.0)) - Vector((M.x, M.y, 0.0))).normalized()         # toward the room centre
        a = math.radians(BEARING)
        u = Vector((u0.x * math.cos(a) - u0.y * math.sin(a), u0.x * math.sin(a) + u0.y * math.cos(a), 0.0))   # the camera's bearing from the mocker
        self.u = u
        self.mp = Vector((M.x, M.y, 0.0)) + u0 * 3.2                                      # mocker's floor point
        loc0 = self.mp + u * 1.75 + Vector((0, 0, 1.85))
        look0 = self.mp + Vector((0, 0, FOCAL_Z))
        self.cam_path = C.CamPath(loc0, look0, GS[0], G_LAST, push=0.08, slide_px=40.0, rise_px=0.0, arc_deg_s=7.0, decay=0.3,
                                  snaps=[dict(g=G_PUNCH, k=1.3, peak=1.8, shift=(-0.1, 0.0))])
        self.key_cam(bf(GS[0]), *self.cam_path.at(GS[0]))
        self.scene.frame_set(bf(GS[0]))
        self.mock = C.make_actor("mock", "mocker", os.path.join(WORK, "sprites"), canvas=CANVAS, cam=self.cam)
        self.actors["mock"] = self.mock
        for ob in bpy_objs("fgdesk_"):
            ob.hide_render = True                                 # the preset's own FG desk is replaced by ours
        self.build_fg(self.cam_path.at(GS[0]))

    def build_fg(self, cam):
        """desk corner with the big inkwell + quill, 1.6 D from the lens at the lower left (world-fixed; the camera pushes past it)"""
        loc, look = cam
        f, r, up = C._cam_basis(loc, look)
        base = Vector(loc) + f * 2.7 + r * 1.35 + Vector((0, 0, 0))
        base.z = 1.2
        M = TG.STATE["M"]
        yaw = math.atan2(f.y, f.x) - math.pi / 2
        from mathutils import Matrix, Euler
        mb = K.MB("fg10")
        mb.push(Matrix.Translation(base / 1.85) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
        s = 0.62
        mb.box(M["walnut"], (0.12 * s, 0.0, 0.0), (0.62 * s, 0.5 * s, 0.05 * s)); mb.box(M["baize"], (0.12 * s, 0.0, 0.03 * s), (0.52 * s, 0.4 * s, 0.012 * s))
        mb.cyl(M["glassjar"], (0.0, 0.0, 0.09 * s), 0.07 * s, 0.12 * s, "z", 14, True); mb.cyl(M["ink"], (0.0, 0.0, 0.08 * s), 0.06 * s, 0.09 * s, "z", 14)
        mb.cyl(M["brass"], (0.0, 0.0, 0.16 * s), 0.075 * s, 0.025 * s, "z", 14)
        mb.rod(M["paper"], (0.0, 0.0, 0.14 * s), (0.16 * s, 0.12 * s, 0.62 * s), 0.008 * s, 0.003 * s, 5)
        mb.ell(M["paper"], (0.12 * s, 0.09 * s, 0.5 * s), (0.03 * s, 0.012 * s, 0.14 * s), (8, 6), (0, 0.2, 0.7))
        mb.pop()
        self.fg = mb.finish()

    def mock_pose(self, g):
        finger = g < G_SWAP
        p = dict(cast16.STORY16["mocker_boast_finger" if finger else "mocker_boast_chest"][1])
        p["mirror"] = True
        p["fx"] = ["blush"]
        if g >= G_FOCUS:
            p["fx"] = ["blush", {"type": "focus_lines", "seed": g, "n": 80}]
        p["blink"] = blink(g, [G_SWAP - 1, 612, 640, 690])
        s = math.sin(2 * math.pi * 2.0 * g / 30.0)
        p["squash"] = (1.005 + 0.012 * s, 0.995 - 0.012 * s)
        p["mouth"] = lip_mouth(g)                                # LIP-SYNC (only the quote)
        p["head_roll"] = p["head_roll"] + 2.0 * math.sin(g * 0.27)
        if not finger:                                           # the thump on his chest
            h = p["arm_r"]["hand"]
            th = max(0.0, math.sin(g * 0.62)) * 0.07
            p["arm_r"] = dict(p["arm_r"], hand=(h[0], h[1] + th))
        return p

    def bounce(self, g):
        return 0.03 * abs(math.sin(math.pi * 2.0 * g / 30.0))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.cam_path.at(g))
            C.place(self.mock, f, (self.mp.x, self.mp.y, self.bounce(g)))
            self.key_set(f, flames=1.0)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mock.pose(f, self.mock_pose(g), camera=self.cam)
        self.sprites_for([(self.mock, 512)], [bf(g) for g in gs])

    def report(self, g):
        return dict(g=g, cam=[round(c, 2) for c in self.cam_path.at(g)[0]], heads=C.head_report(self, bf(g)), mouth=lip_mouth(g))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if GS[0] <= g <= G_LAST] if len(sys.argv) > 2 else []
    if cmd == "camreport":
        Tk = Take("preview")
        rows, worst = Tk.cam_path.report(GS[:-1])
        print(rows[0], rows[len(rows) // 2], rows[-1])
        print("longest run under 0.25 px/frame: %d frames (bible max 6); min px %.2f" % (worst, min(r["px"] for r in rows)))
    elif cmd in ("probe", "stills"):
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
