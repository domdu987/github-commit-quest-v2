#!/usr/bin/env python3
"""shot.py -- film 20 take s02 = shot 2 (g 80..177) + handles: 4 in (cut) g 76..79, 8 out (dissolve 13 into shot 3) g 178..185.
"แต่กลับขึ้นไปนั่งกินข้าว ... เดียวกันนั้น": RESTO resto_table / DAY.  Maupassant (seated, napkin tucked, blissful) eats at the white-cloth
window table; the camera starts tight on him (the window hidden behind his head), pushes; on "เดียวกันนั้น" (event g 139) a SNAP
PULL-OUT x0.6 reveals the riveted iron lattice girders across the big window and Paris far below = he is IN the tower.
Mouths never move (no quote): the fork cycle + a chew bob carry the eating.

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
    python3 deliver.py
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

SHOT = 2
G0, G1 = C.g_bound(2.67), C.g_bound(5.93)      # 80, 178: shot = g 80..177
H_IN, H_OUT = 4, 8                              # cut in, dissolve 13 out (13/2 + 2 = 8)
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1     # 76..185
GS = list(range(G_FIRST, G_LAST + 1))
G_SAME = C.cap_g("เดียวกันนั้น")                 # snap pull-out event
SNAP = (G_SAME - 2, G_SAME + 13)

PRESET, LIGHT = "resto_table", "DAY"
MARK = "maupassant_seated"
SEAT_H = 0.865                                  # chair seat 0.46 m in D
HEAD_Z = float(os.environ.get("HEAD_Z", "2.35"))  # head centre above the feet mark (probe-tuned)
PPD = 256
CANVAS = cast20.CANVAS20["maupassant"]
CAM_CLOSER = float(os.environ.get("CAM_CLOSER", "2.0"))   # D closer than the preset along the view
LAT = float(os.environ.get("LAT", "-0.75"))
TILT0 = float(os.environ.get("TILT0", "4.0"))

EAT = cast20.STORY20["maupassant_seated_eat"][1]
CHEW = cast20.STORY20["maupassant_seated_eat_chew"][1]
PERIOD = 40.0                                   # frames per fork cycle
BLINKS = [92, 150]


def cam_path(A):
    m = Vector(A["marks"][MARK])
    subj = m + Vector((0.0, 0.0, HEAD_Z))
    c = Vector(A["cams"][PRESET]["loc"])
    c = c + (subj - c).normalized() * CAM_CLOSER
    fw = (subj - c).normalized()
    lat = Vector((fw.y, -fw.x, 0.0)).normalized() * LAT        # parallel shift: head starts right of centre, the slide carries it left
    c, subj = c + lat, subj + lat
    return C.CamPath(c, subj, G_FIRST, G_LAST, push=0.15, slide_px=100.0, rise_px=0.0, arc_deg_s=5.0, tilt0=TILT0, tilt_deg_s=0.0,
                     decay=0.3, snaps=[dict(g=SNAP, k=0.5, peak=1.7, shift=(0.25, 0.0), tilt=0.0)])


def cam_path_static():
    import int20
    a, b, _ = int20.RESTO_CAMS_M[PRESET] if len(int20.RESTO_CAMS_M[PRESET]) == 3 else (*int20.RESTO_CAMS_M[PRESET], 0)
    loc = CO.W(a)
    A = dict(marks={MARK: CO.W(int20.RESTO_MARKS_M["maupassant_seated"])}, cams={PRESET: dict(loc=loc)})
    return cam_path(A)


def pose_of(g):
    """fork cycle between maupassant_seated_eat (fork + bite at the mouth) and _eat_chew (fork down); mouth stays a still smile."""
    s = 0.5 - 0.5 * math.cos(2 * math.pi * ((g - G_FIRST) / PERIOD))      # 0 chew .. 1 bite at the mouth
    p = dict(EAT)
    p["seated"], p["seat_h"], p["napkin"] = 1, SEAT_H, 1
    p["mouth"] = "smile"
    ae, ac = EAT["arm_r"]["hand"], CHEW["arm_r"]["hand"]
    p["arm_r"] = dict(EAT["arm_r"], hand=(lerp(ac[0], ae[0], s), lerp(ac[1], ae[1], s)), bend=lerp(CHEW["arm_r"]["bend"], EAT["arm_r"]["bend"], s))
    pr = dict(EAT["prop_r"]); pr["angle"] = lerp(CHEW["prop_r"]["angle"], EAT["prop_r"]["angle"], s)
    p["prop_r"] = pr
    p["bite"] = 1.0 if s > 0.45 else 0.0
    p["yaw"] = 0.30 + 0.07 * math.sin(g * 0.11)
    p["pitch"] = 0.02 + 0.06 * (1 - s)
    p["head_roll"] = 2.5 * math.sin(2 * math.pi * (g - G_FIRST) / PERIOD + 1.0)       # head bobs with the chewing
    p["lean"] = 2.0 * s + 0.8 * math.sin(g * 0.17)
    p["squash"] = (1.0 + 0.012 * (1 - s), 1.0 - 0.012 * (1 - s))
    p["blink"] = blink(g, BLINKS)
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s%02d" % SHOT)
        self.path = cam_path(self.A)
        self.key_cam(bf(G_FIRST), *self.path.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        for ob in list(bpy_objs("actor_")):                  # the build's stand-in card(s) (resto_table stages one) are replaced by ours
            ob.hide_render = True
            ob.hide_viewport = True
        self.mau = self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), canvas=CANVAS,
                                                     contact=dict(width=1.1, depth=0.5, opacity=0.5), cam=self.cam)

    def pose(self, gs):
        mark = self.A["marks"][MARK]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.mau, f, mark)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mau.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.mau, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    dist=round((self.path.subj0 - loc).length, 2), heads=C.head_report(self, f), upper_k=round(self.mau.upper_k.get(f, 1.0), 3))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def bpy_objs(prefix):
    return [o for o in C.bpy.data.objects if o.name.startswith(prefix)]


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
