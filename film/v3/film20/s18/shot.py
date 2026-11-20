#!/usr/bin/env python3
"""shot.py -- film 20 take s18 = shot 18 (g 1221..1301, DISSOLVED IN from shot 17: 17 f -> 11 handle frames g 1210..1220 before,
4 handle frames g 1302..1305 after the hard cut to shot 19).
"ยี่สิบปีผ่านไป ใกล้วันรื้อ เข้ามาทุกที" -- TOWER tower_dusk (camera tower_dusk_chars, T14) / DUSK 1909.
OLD EIFFEL (white beard, stoop) stands small and worried in front of the foot of the tower; the officer and three demolition men
stand at their marks beside the demolition wagon (crowbars / ropes / scrap cart are set art).  Nobody's mouth moves.
    g 1210..1253  push 20 %/s easing toward 0 (decay), slight sway (arc), slide, tilt; Eiffel gazes up at the tower (expr calm, hand at chin)
    g 1252..1267  SNAP push x1.3 on "ใกล้วันรื้อ" (event g 1254); the face swaps calm -> worried (sweat) on the closed frame of a blink
    g 1267..1305  the push keeps easing out; idle sway of all five, officer stern, demolition men shift their weight

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out> [scale] [spp] | final a:b[:step] [scale] [spp]
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

SHOT_G0, SHOT_G1 = C.g_bound(40.70), C.g_bound(43.39)       # 1221, 1302 (shot = 1221..1301)
H_IN, H_OUT = 11, 4                                          # DIS 17 -> 17/2 + 2 = 10.5 -> 11; cut out: 4
G0, G_LAST = SHOT_G0 - H_IN, SHOT_G1 + H_OUT - 1             # 1210 .. 1305
GS = list(range(G0, G_LAST + 1))
G_SOON = C.cap_g("ใกล้วันรื้อ")                               # 1254
SNAP = (G_SOON - 2, G_SOON + 13)
G_SWAP = G_SOON                                             # closed frame of the blink G_SWAP-1 .. G_SWAP+1

PRESET, CAM, LIGHT = "tower_dusk", "tower_dusk_chars", None
CAST = [  # (key, cast, mark, canvas-key, extra pose, yaw)
    ("eif", "eiffel_old", "eiffel_old"),
    ("off", "officer", "officer"),
    ("da", "riveter_hammer", "demo_a"),
    ("db", "riveter_tongs", "demo_b"),
    ("dc", "riveter_forge", "demo_c"),
]
HEAD_Z = 2.75                                  # old Eiffel's head centre above his feet (D)
PPD = 160
DEMO_XY = dict(eiffel_old=(-5.6, -219.0), officer=(-6.7, -216.6), demo_a=(-8.4, -215.2), demo_b=(-7.2, -213.6), demo_c=(-9.6, -214.0))


def cam_path(A):
    m = Vector(A["marks"]["eiffel_old"])
    subj = m + Vector((AIM_DX * CO.SC, AIM_DY * CO.SC, HEAD_Z))
    c = CO.W(CAM_M)
    return C.CamPath(c, subj, G0, G_LAST, push=0.20, slide_px=-30.0, rise_px=0.0, arc_deg_s=-4.0, tilt0=TILT0, tilt_deg_s=-4.5,
                     decay=0.95, snaps=[dict(g=SNAP, k=1.55, peak=1.9, shift=(0.75, 0.0), tilt=-3.0), dict(g=(1280, 1296), k=1.15, peak=1.7, shift=(0.0, 0.0), tilt=-2.0)])


CAM_M = (-5.4, -227.0, 0.7)                     # start camera (m): T14 lens + shift, moved so all five stand in frame
TILT0 = -3.0
AIM_DY = 0.0                                   # aim 4 m behind Eiffel (toward the wagon group)
AIM_DX = -0.9                                  # aim point 2.2 m left of old Eiffel (between him and the wagon)


def cam_path_static():
    import tower20
    A = dict(marks={"eiffel_old": CO.W((-6.8, -212.6, 0.0))}, cams={})
    return cam_path(A)


# ----------------------------------------------------------------------------- poses
C.add_expression("calm20", eyes="half", tilt=0.0, brows=("both", 0.10, 8.0, 0.05, 0.18, 0.012), mouth="flat")


def pose_eif(g):
    p = dict(cast20.STORY20["eiffel_old_worried"][1])
    p["yaw"] = 0.25 + 0.05 * math.sin(g * 0.11)
    p["lean"] = 5.0 + 1.2 * math.sin(g * 0.17)
    p["head_roll"] = 4.0 + 2.0 * math.sin(g * 0.13 + 1.0)
    p["pitch"] = -0.28 + 0.04 * math.sin(g * 0.09)            # chin up: he looks at the tower first
    p["gaze"] = (0.4, -0.8) if g < G_SWAP else (0.1, 0.5)     # up at the tower, then down at the wagon
    p["expr"] = "calm" if g < G_SWAP else "worried"
    p["blink"] = blink(g, [G_SWAP - 1, G0 + 12])
    p["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.27))
    p["t"] = g / 30.0
    return p


def pose_off(g):
    p = dict(cast20.STORY20["officer_stern"][1])
    p["yaw"] = -0.3 + 0.04 * math.sin(g * 0.1 + 2)
    p["lean"] = 1.5 * math.sin(g * 0.13 + 0.5)
    p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.24 + 1))
    p["blink"] = blink(g, [G0 + 30, G0 + 71])
    p["t"] = g / 30.0
    return p


def pose_demo(k, g):
    ph = {"da": 0.0, "db": 2.1, "dc": 4.0}[k]
    base = {"da": "riveter_hammer_work", "db": "riveter_tongs_work", "dc": "riveter_forge_work"}[k]
    p = dict(cast20.STORY20[base][1])
    p["expr"] = "neutral"
    p["yaw"] = {"da": 0.5, "db": -0.5, "dc": 0.4}[k] + 0.06 * math.sin(g * 0.12 + ph)
    p["lean"] = 2.0 + 2.5 * math.sin(g * 0.15 + ph)
    p["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.25 + ph))
    p["prop_r"] = {"da": dict(type="rivet_hammer", angle=-95 + 6 * math.sin(g * 0.15 + ph)),
                   "db": dict(type="cane20", angle=-80, scale=0.7),
                   "dc": dict(type="hammer20", angle=-100)}[k]
    p["blink"] = blink(g, [G0 + 20 + int(ph * 7), G0 + 66 + int(ph * 5)])
    p["t"] = g / 30.0
    return p


POSES = dict(eif=lambda g: pose_eif(g), off=lambda g: pose_off(g), da=lambda g: pose_demo("da", g), db=lambda g: pose_demo("db", g),
             dc=lambda g: pose_demo("dc", g))


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s18", cam_name=CAM)
        C.fix_antenna_wires()
        for m, xy in DEMO_XY.items():                                # staging: the whole group moved 2-4 m toward the wagon (-13) so five heads + the wagon fit one 8 m frame
            self.A["marks"][m] = CO.W((xy[0], xy[1], 0.0))
        self.path = cam_path(self.A)
        self.key_cam(bf(G0), *self.path.at(G0))
        self.scene.frame_set(bf(G0))
        for o in C.bpy.data.objects:                                 # warm dusk ground: the invisible shade casters make the near ground a flat blue slab; the torn FG planks are broken geometry
            if o.name.startswith(("shade_casters", "fg_")):
                o.hide_render = True
        self.fg = []
        C.warm_ground_sun(strength=2.2, color=(1.0, 0.56, 0.30))
        self.dress_ground()
        self.fg0 = {o.name: o.location.copy() for o in self.fg}
        self.marks = {m: C.on_ground(self.A["marks"][m]) for _k, _c, m in CAST}
        for m in self.marks:                                             # kegs / carts under a mark would lift the card: the avenue is z 0.113 D everywhere here
            self.marks[m] = (self.marks[m][0], self.marks[m][1], 0.113)
        print("ground z (D):", {m: round(v[2], 3) for m, v in self.marks.items()}, flush=True)
        for k, cast, mark in CAST:
            self.actors[k] = C.make_actor(k, cast, os.path.join(WORK, "sprites"), cam=self.cam,
                                          contact=dict(width=1.2, depth=0.5, opacity=0.8))

    def dress_ground(self):
        """FG dressing at the sides of the lens path (the camera passes beside them: parallax whoosh): barrels, crates, a rope coil and
        stones on the avenue; metres, parented to the scaled root like the set's own props."""
        M = CO.STATE["M"]
        mb = CO.MB("team8_fg", CO.root())
        for (x, y) in ((-8.6, -223.6), (-9.2, -221.4), (-3.0, -222.6)):
            mb.cyl(M["timber"], (x, y, 0.45), 0.34, 0.9, "z", 14)
            mb.cyl(M["metal"], (x, y, 0.2), 0.355, 0.05, "z", 14)
            mb.cyl(M["metal"], (x, y, 0.7), 0.355, 0.05, "z", 14)
        for (x, y, r) in ((-2.4, -220.2, 0.3), (-8.0, -219.8, -0.4)):
            mb.box(M["timberdk"], (x, y, 0.3), (0.8, 0.6, 0.6), rz=r)
            mb.box(M["plank"], (x, y, 0.62), (0.84, 0.64, 0.05), rz=r)
        mb.cyl(M["rope"], (-7.4, -222.2, 0.08), 0.35, 0.16, "z", 12)
        mb.finish()

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            loc, _ = self.path.at(g)
            d = (self.path.loc0 - Vector(self.A['cams'][PRESET]['loc'])) + 0.75 * (loc - self.path.loc0)
            d.z = 0.0
            for o in self.fg:                                        # FG follows the start camera, then rides 75 % of its ground travel
                o.location = self.fg0[o.name] + d / CO.SC
                o.keyframe_insert("location", frame=f)
            for k, cast, mark in CAST:
                C.place(self.actors[k], f, self.marks[mark])
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for k, cast, mark in CAST:
                self.actors[k].pose(f, POSES[k](g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        tower = {k: CO.project(CO.W(p)) for k, p in (("base", (0, 0, 0.0)), ("platform2", (0, 0, 115.0)), ("summit", (0, 0, 300.0)))}
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), tower_px=tower)

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        P = cam_path_static()
        rows, worst = P.report(GS[:-1])
        for r in rows[::6]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G_LAST]
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
