"""shot.py -- film 20 take s24 = shot 24 (g 1732..1813) + handles: 8 in (dissolve 13 from shot 23) g 1724..1731, 4 out (cut to shot 25) g 1814..1817.
"ส่วนโมปัสซังต์ เล่ากันว่า หลังหอเปิด": RESTO resto_wide / DAY 1889.  The WAITER leads MAUPASSANT in across the first-floor restaurant (they
walk diagonally away from the camera toward the window end, three-quarter view: faces visible, no back cards).  Camera: the preset
wide pose moved closer, push 7 %/s + slide 40 px/s, a SNAP push x1.3 on "หลังหอเปิด" (event g 1779); FG chair back from the set.
Mouths never move (no quote): waiter smiles, Maupassant smug.

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

SHOT = 24
G0, G1 = C.g_bound(57.75), C.g_bound(60.48)    # 1732, 1814: shot = g 1732..1813
H_IN, H_OUT = 8, 4                              # dissolve 13 in (13/2 + 2), cut out
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1     # 1724..1817
GS = list(range(G_FIRST, G_LAST + 1))
G_OPEN = C.g_of(59.2)                           # "หลังหอเปิด": snap push
SNAP = (G_OPEN - 2, G_OPEN + 13)

PRESET, LIGHT = "resto_wide", "DAY"
PPD = 256
CAM_START = tuple(float(v) for v in os.environ.get("CAM_START", "-0.9,4.2,0.9").split(","))     # metres
CAM_AIM = tuple(float(v) for v in os.environ.get("CAM_AIM", "0.2,12.0,1.4").split(","))          # metres (subject point for pushes)
TILT0 = float(os.environ.get("TILT0", "0.0"))
PATH_M = [(-0.5, 8.0), (0.0, 11.0), (0.1, 14.0)]                  # waiter floor path along the runner to the window table (metres)
SPEED = float(os.environ.get("SPEED", "1.7"))                               # m/s
GAP = float(os.environ.get("GAP", "1.0"))                                   # Maupassant follows this far behind (m)
ARC0 = float(os.environ.get("ARC0", "1.05"))                                  # waiter's arc length (m) at G0


def path_pos(sm):
    """point at arc length sm (m) along PATH_M (extrapolated past the ends)"""
    pts = [Vector((x, y, 0.0)) for x, y in PATH_M]
    segs = [(pts[i], pts[i + 1], (pts[i + 1] - pts[i]).length) for i in range(len(pts) - 1)]
    if sm <= 0:
        a, b, L = segs[0]
        return a + (b - a).normalized() * sm
    for a, b, L in segs:
        if sm <= L:
            return a + (b - a) * (sm / L)
        sm -= L
    a, b, L = segs[-1]
    return b + (b - a).normalized() * sm


def walker_s(g, who):
    return ARC0 + SPEED * (g - G0) / 30.0 - (GAP if who == "mau" else 0.0)


LAT_M = float(os.environ.get("LAT_M", "0.55"))                                # waiter walks this far to the right of Maupassant's line (m)


def mark_of(g, who):
    p = path_pos(walker_s(g, who)) + Vector((LAT_M / 2 if who == "wai" else -LAT_M / 2, 0.0, 0.0))
    return (CO.W((p.x, p.y, 0.0))[0], CO.W((p.x, p.y, 0.0))[1], 0.0)


def cam_path(A):
    loc = Vector(CO.W(CAM_START))
    subj = Vector(CO.W(CAM_AIM))
    return C.CamPath(loc, subj, G_FIRST, G_LAST, push=float(os.environ.get('PUSH', '0.09')), slide_px=float(os.environ.get('SLIDE', '25')), rise_px=0.0, arc_deg_s=3.0, tilt0=TILT0, tilt_deg_s=0.0,
                     decay=0.3, snaps=[dict(g=SNAP, k=1.45, peak=1.7, shift=(0.1, 0.0), tilt=1.5)])


def cam_path_static():
    return cam_path(None)


MAU_BASE = dict(yaw=0.55, expr="smug", mouth="flat", arm_r="down", arm_l="down")
WAI_BASE = dict(yaw=0.55, expr="happy", arm_r=dict(hand=(0.78, 0.62), bend=-0.3, stretch=1.15, shape="open"), arm_l=dict(hand=(-0.35, 0.92), bend=0.5),
                prop_l="towel20")


def pose_of(g, who):
    ph = (walker_s(g, who) / 1.5) % 1.0                      # one cycle (two steps) per 1.15 m
    if who == "mau":
        p = cast20.cycle("maupassant", ph, "walk", 1, dict(MAU_BASE), "both", 1.1)
        p["pitch"] = -0.10
        p["head_roll"] = 2.0 * math.sin(g * 0.2)
    else:
        p = cast20.cycle("waiter", ph, "walk", 1, dict(WAI_BASE), "l", 1.15)
        p["arm_r"] = dict(WAI_BASE["arm_r"], hand=(0.78, 0.62 + 0.04 * math.sin(g * 0.23)))
        p["pitch"] = 0.04
    p["yaw"] = 0.55 + 0.04 * math.sin(g * 0.13 + (0 if who == "mau" else 1.5))
    p["blink"] = blink(g, [1760, 1801] if who == "mau" else [1748, 1790])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s%02d" % SHOT)
        for ob in [o for o in C.bpy.data.objects if o.name.startswith("actor_")]:      # the build's stand-in cards at the marks
            ob.hide_render = True
            ob.hide_viewport = True
        C.grade(self.scene, float(os.environ.get('EXPO','1.0')), float(os.environ.get('SAT','1.25')))
        self.path = cam_path(self.A)
        self.key_cam(bf(G_FIRST), *self.path.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.mau = self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), canvas=cast20.CANVAS20["maupassant"],
                                                     contact=dict(width=1.1, depth=0.5, opacity=0.6), cam=self.cam)
        self.wai = self.actors["wai"] = C.make_actor("wai", "waiter", os.path.join(WORK, "sprites"), canvas=cast20.CANVAS20["waiter"],
                                                     contact=dict(width=1.1, depth=0.5, opacity=0.6), cam=self.cam)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.mau, f, mark_of(g, "mau"))
            C.place(self.wai, f, mark_of(g, "wai"))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mau.pose(f, pose_of(g, "mau"), camera=self.cam)
            self.wai.pose(f, pose_of(g, "wai"), camera=self.cam)
        self.sprites_for([(self.mau, PPD), (self.wai, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), upper_k=round(self.mau.upper_k.get(f, 1.0), 3))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = cam_path_static().report(GS[:-1])
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
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
