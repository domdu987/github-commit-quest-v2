#!/usr/bin/env python3
"""shot.py -- film 20 take s25 = shot 25 (g 1814..1911) + handles: 4 in (cut) g 1810..1813, 4 out (cut to shot 26) g 1912..1915.
"กินข้าวบนหอ แทบทุกวัน": RESTO resto_table / DAY 1889, callback of shot 2.  Maupassant eats blissfully (napkin tucked): fork bite, chew,
a sip of wine, chew ...; eye level, wine glass + bread FG from the set; push 8 %/s + slide 40 px/s; SNAP push x1.4 on "แทบทุกวัน"
(event g 1838).  Mouths never move (no quote): fork / glass cycle + a chew bob carry the eating.

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

SHOT = 25
G0, G1 = C.g_bound(60.48), C.g_bound(63.72)    # 1814, 1912: shot = g 1814..1911
H_IN, H_OUT = 4, 4                              # cut in, cut out
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1     # 76..185
GS = list(range(G_FIRST, G_LAST + 1))
G_EVERY = C.g_of(61.15)                          # snap push event
SNAP = (G_EVERY - 2, G_EVERY + 13)

PRESET, LIGHT = "resto_table", "DAY"
MARK = "maupassant_seated"
SEAT_H = 0.865                                  # chair seat 0.46 m in D
HEAD_Z = float(os.environ.get("HEAD_Z", "2.35"))  # head centre above the feet mark (probe-tuned)
PPD = 256
CANVAS = cast20.CANVAS20["maupassant"]
CAM_CLOSER = float(os.environ.get("CAM_CLOSER", "0.6"))   # D closer than the preset along the view
TILT0 = float(os.environ.get("TILT0", "4.0"))

EAT = cast20.STORY20["maupassant_seated_eat"][1]
CHEW = cast20.STORY20["maupassant_seated_eat_chew"][1]
LAT = float(os.environ.get("LAT", "1.05"))
PERIOD = 40.0                                   # frames per fork cycle
BLINKS = [1842, 1880]


def cam_path(A):
    m = Vector(A["marks"][MARK])
    subj = m + Vector((0.0, 0.0, HEAD_Z))
    c = Vector(A["cams"][PRESET]["loc"])
    c = c + (subj - c).normalized() * CAM_CLOSER
    fw = (subj - c).normalized()
    lat = Vector((fw.y, -fw.x, 0.0)).normalized() * LAT        # parallel shift: the head starts left of centre and the slide carries it right
    c, subj = c + lat, subj + lat
    return C.CamPath(c, subj, G_FIRST, G_LAST, push=0.15, slide_px=-70.0, rise_px=0.0, arc_deg_s=-3.0, tilt0=TILT0, tilt_deg_s=0.0,
                     decay=0.3, snaps=[dict(g=SNAP, k=1.6, peak=1.7, shift=(-0.1, 0.0), tilt=-1.0)])


def cam_path_static():
    import int20
    a, b, _ = int20.RESTO_CAMS_M[PRESET] if len(int20.RESTO_CAMS_M[PRESET]) == 3 else (*int20.RESTO_CAMS_M[PRESET], 0)
    loc = CO.W(a)
    A = dict(marks={MARK: CO.W(int20.RESTO_MARKS_M["maupassant_seated"])}, cams={PRESET: dict(loc=loc)})
    return cam_path(A)


TOAST = cast20.STORY20["maupassant_seated_toast"][1]
T_A, T_B, T_C = 0, 44, 84                       # relative frames: fork cycle | wine sip | fork again


def pose_of(g):
    """fork bite (rel 0..44) -> wine sip (44..84) -> fork bite again; arm hands are blended, the prop swaps at the lowest point
    (hand down by the plate); mouth stays a still smile."""
    r = g - G0
    p = dict(EAT)
    p["seated"], p["seat_h"], p["napkin"], p["mouth"] = 1, SEAT_H, 1, "smile"
    ae, ac, at_ = EAT["arm_r"], CHEW["arm_r"], TOAST["arm_r"]
    if T_A <= r < T_B or r >= T_C:
        per = (r - (T_C if r >= T_C else T_A)) / 40.0
        s = 0.5 - 0.5 * math.cos(2 * math.pi * per)
        hand = (lerp(ac["hand"][0], ae["hand"][0], s), lerp(ac["hand"][1], ae["hand"][1], s))
        p["arm_r"] = dict(ae, hand=hand, bend=lerp(ac["bend"], ae["bend"], s))
        p["prop_r"] = dict(EAT["prop_r"], angle=lerp(CHEW["prop_r"]["angle"], EAT["prop_r"]["angle"], s))
        p["bite"] = 1.0 if s > 0.45 else 0.0
    else:
        u = (r - T_B) / float(T_C - T_B)
        s = math.sin(math.pi * u) ** 1.2                    # 0 -> 1 (glass raised) -> 0
        hand = (lerp(ac["hand"][0], at_["hand"][0], s), lerp(ac["hand"][1], at_["hand"][1], s))
        p["arm_r"] = dict(at_, hand=hand, bend=lerp(ac["bend"], at_["bend"], s))
        p["prop_r"] = dict(TOAST["prop_r"])
        p["bite"] = 0.0
    p["yaw"] = 0.32 + 0.07 * math.sin(g * 0.11)
    p["pitch"] = 0.02 + (-0.15 * s if T_B <= r < T_C else 0.06 * (1 - s))
    p["head_roll"] = 2.5 * math.sin(g * 0.157 + 1.0) - (3.0 * s if T_B <= r < T_C else 0)
    p["lean"] = 1.5 * s + 0.8 * math.sin(g * 0.17)
    ch = 0.5 + 0.5 * math.sin(g * 0.52)
    p["squash"] = (1.0 + 0.012 * ch, 1.0 - 0.012 * ch)
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
