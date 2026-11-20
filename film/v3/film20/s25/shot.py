#!/usr/bin/env python3
"""shot.py -- film 20 take s25 = shot 25 (g 1853..1911) + handles: 4 in (cut) g 1849..1852, 4 out (cut to shot 26) g 1912..1915.
"กินข้าวบนหอ แทบทุกวัน": RESTO resto_table / DAY 1889, callback of shot 2.  Maupassant eats blissfully (napkin tucked): fork bite, chew,
a sip of wine, chew ...; eye level, wine glass + bread FG from the set; push 8 %/s + slide 40 px/s; SNAP push x1.4 on "ที่เดียว"
(event g 1879).  Mouths never move (no quote): fork / glass cycle + a chew bob carry the eating.

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
G0, G1 = C.g_bound(61.77), C.g_bound(63.72)    # 1853, 1912 (plan 61.77-63.72 s): shot = g 1853..1911
H_IN, H_OUT = 6, 4                              # 9-frame MATCH-DISSOLVE in from s24 (6 handle frames), cut out
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1     # 76..185
GS = list(range(G_FIRST, G_LAST + 1))
G_EVERY = C.g_of(62.52)                          # snap push event: "ที่เดียว" (62.52 s)
SNAP = (G_EVERY - 2, G_EVERY + 13)

PRESET, LIGHT = "resto_table", "DAY"
MARK = "maupassant_seated"
SEAT_H = 0.865                                  # chair seat 0.46 m in D
HEAD_Z = float(os.environ.get("HEAD_Z", "2.35"))  # head centre above the feet mark (probe-tuned)
PPD = 256
CANVAS = cast20.CANVAS20["maupassant"]
CAM_CLOSER = float(os.environ.get("CAM_CLOSER", "1.45"))   # D closer than the preset along the view
TILT0 = float(os.environ.get("TILT0", "6.0"))

EAT = cast20.STORY20["maupassant_seated_eat"][1]
CHEW = cast20.STORY20["maupassant_seated_eat_chew"][1]
DZ = float(os.environ.get('DZ', '-0.5'))
LAT = float(os.environ.get("LAT", "0.25"))
PERIOD = 40.0                                   # frames per fork cycle
BLINKS = [1842, 1880]


def cam_path(A):
    m = Vector(A["marks"][MARK])
    subj = m + Vector((0.0, 0.0, HEAD_Z))
    c = Vector(A["cams"][PRESET]["loc"])
    c = c + (subj - c).normalized() * CAM_CLOSER + Vector((0.0, 0.0, DZ))        # DZ < 0: lower camera = the railing bar behind him falls below his head, less cloth
    fw = (subj - c).normalized()
    lat = Vector((fw.y, -fw.x, 0.0)).normalized() * LAT        # parallel shift: the head starts left of centre and the slide carries it right
    c, subj = c + lat, subj + lat
    return C.CamPath(c, subj, G_FIRST, G_LAST, push=0.15, slide_px=-55.0, rise_px=0.0, arc_deg_s=-3.0, tilt0=TILT0, tilt_deg_s=0.0,
                     decay=0.3, snaps=[dict(g=SNAP, k=1.6, peak=1.7, shift=(-0.1, 0.0), tilt=-1.0)])


def cam_path_static():
    import int20
    a, b, _ = int20.RESTO_CAMS_M[PRESET] if len(int20.RESTO_CAMS_M[PRESET]) == 3 else (*int20.RESTO_CAMS_M[PRESET], 0)
    loc = CO.W(a)
    A = dict(marks={MARK: CO.W(int20.RESTO_MARKS_M["maupassant_seated"])}, cams={PRESET: dict(loc=loc)})
    return cam_path(A)


TOAST = cast20.STORY20["maupassant_seated_toast"][1]
G_BITE = 1817                                   # s24's first bite: the fork cycle is the SAME function of g in s24 and here (match-dissolve)
G_SIP0, G_SIP1 = 1873, 1913                     # wine sip (glass raised ~1893, lowered at the end of the shot)


def pose_of(g):
    """continues s24's fork cycle (bite at 1817, 1857, ...) so the match-dissolve is seamless, then a sip of wine g 1873..1913."""
    p = dict(EAT)
    p["seated"], p["seat_h"], p["napkin"], p["mouth"] = 1, SEAT_H, 1, "smile"
    ae, ac, at_ = EAT["arm_r"], CHEW["arm_r"], TOAST["arm_r"]
    sip = G_SIP0 <= g < G_SIP1
    if not sip:
        s = 0.5 - 0.5 * math.cos(2 * math.pi * ((g - G_BITE) / PERIOD) + math.pi)
        hand = (lerp(ac["hand"][0], ae["hand"][0], s), lerp(ac["hand"][1], ae["hand"][1], s))
        p["arm_r"] = dict(ae, hand=hand, bend=lerp(ac["bend"], ae["bend"], s))
        p["prop_r"] = dict(EAT["prop_r"], angle=lerp(CHEW["prop_r"]["angle"], EAT["prop_r"]["angle"], s))
        p["bite"] = 1.0 if s > 0.5 else 0.0
        p["pitch"] = 0.02 + 0.06 * (1 - s)
        p["head_roll"] = 2.5 * math.sin(2 * math.pi * (g - G_BITE) / PERIOD + 1.0)
        p["lean"] = 2.0 * s + 0.8 * math.sin(g * 0.17)
    else:
        u = (g - G_SIP0) / float(G_SIP1 - G_SIP0)
        s = math.sin(math.pi * u) ** 1.2
        hand = (lerp(ac["hand"][0], at_["hand"][0], s), lerp(ac["hand"][1], at_["hand"][1], s))
        p["arm_r"] = dict(at_, hand=hand, bend=lerp(ac["bend"], at_["bend"], s))
        p["prop_r"] = dict(TOAST["prop_r"])
        p["bite"] = 0.0
        p["pitch"] = 0.02 - 0.15 * s
        p["head_roll"] = 2.5 * math.sin(g * 0.157 + 1.0) - 3.0 * s
        p["lean"] = 1.5 * s + 0.8 * math.sin(g * 0.17)
    p["yaw"] = 0.30 + 0.07 * math.sin(g * 0.11)                 # same as s24
    ch = 0.5 + 0.5 * math.sin(g * 0.52)
    p["squash"] = (1.0 + 0.012 * (1 - s) if not sip else 1.0, 1.0 - 0.012 * (1 - s) if not sip else 1.0)
    p["blink"] = blink(g, [1838, 1880])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s%02d" % SHOT)
        C.grade(self.scene, float(os.environ.get('EXPO','-0.9')), float(os.environ.get('SAT','1.45')))
        self.path = cam_path(self.A)
        for ob in C.bpy.data.objects:                           # the preset FG bentwood chair (fg_i_woodlt) swings across the lens at g ~1870: hide it
            if ob.name.startswith("fg_i_woodlt"):
                ob.hide_render = True
        clear_camera_tube(self.path, radius_m=1.5, only=("furn_bent",))
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


def clear_camera_tube(path, radius_m=0.65, step=4, only=None):
    """delete the faces of the set's merged furniture (objects furn_*, fg_*) that lie within radius_m of the camera path: the FG chair back
    the lens would pass through (a pillar across the frame at g ~1870)."""
    import bmesh
    C.bpy.context.view_layer.update()
    pts = [path.at(g)[0] for g in range(G_FIRST, G_LAST + 1, step)]
    r = radius_m * CO.SC
    n = 0
    for o in C.bpy.data.objects:
        if o.type != "MESH" or not o.name.startswith(only or ("furn_", "fg_")):
            continue
        bm = bmesh.new(); bm.from_mesh(o.data)
        mw = o.matrix_world
        dead = [f for f in bm.faces if any(any((mw @ v.co - p).length < r for p in pts) for v in f.verts)]
        if dead:
            bmesh.ops.delete(bm, geom=dead, context="FACES"); n += len(dead)
            bm.to_mesh(o.data); o.data.update()
        bm.free()
    print("clear_camera_tube: %d faces deleted" % n, flush=True)


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
