#!/usr/bin/env python3
"""shot.py -- film 20 take s19 = shot 19 (g 1302..1381, hard CUT in from shot 18 (4 handle frames g 1298..1301) and hard cut out to
shot 20 (4 handle frames g 1382..1385)).  REVEAL 1: "ไอเฟลเลยขึง สายอากาศ จากยอดหอ ลงมาถึงพื้น".
TOWER tower_dusk_summit / DUSK 1909: camera (-2.8, -218, 0.5) m on the avenue, looking UP at the summit; OLD EIFFEL (mark eiffel_old)
stands 5 m ahead at screen left and points up at the summit (pose eiffel_old_point_up).  The four antenna wires run from the summit
down to the anchor post at the hut.  On "จากยอดหอ" (44.67 -> event g 1343) a WHIP-TILT swings the camera down along the wire to the
post / hut / ground (aim lerp summit -> post, eased, 9 frames), then the camera pushes in on the hut until the hard cut.
    g 1298..1342 slow tilt-up + push + slide (never parked); Eiffel points up, idle sway, blink
    g 1343..1352 WHIP-TILT down along the wire (the snap of this shot, x ~ 10 px/frame peak 90+)
    g 1352..1385 push on the post / hut, sinking tilt
    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out> [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

SHOT_G0, SHOT_G1 = C.g_bound(43.39), C.g_bound(46.08)       # 1302, 1382 (shot = 1302..1381)
H_IN, H_OUT = 4, 4
G0, G_LAST = SHOT_G0 - H_IN, SHOT_G1 + H_OUT - 1             # 1298 .. 1385
GS = list(range(G0, G_LAST + 1))
G_WIRE = C.cap_g("จากยอดหอ")                                 # 1343: whip start
WHIP = (G_WIRE, G_WIRE + 9)

PRESET, LIGHT = "tower_dusk_summit", None
CAM_M = (-2.75, -215.4, 0.4)                    # camera (m)
PITCH_A0, PITCH_A1 = 28.0, 30.0
SHIFT_A, SHIFT_B = 0.0, 0.15                                  # lens shift: the picture moves up, so a high pitch still keeps Eiffel's head above y 880                # aim pitch above the horizon before the whip (deg), tilts up slowly
SUMMIT = (0.0, 0.0, 300.0)
POST_AIM = (4.0, -201.4, 5.5)                  # end of the whip: the wire's foot (anchor post top) - slightly under, hut below
PITCH_B0 = 0.0                                 # aim pitch at the end of the whip
EIF_HEAD_Z = 2.7
WIRE_GLOW = 0.7


def bearing(a, b):
    return math.degrees(math.atan2(b[0] - a[0], b[1] - a[1]))


def elev(a, b):
    return math.degrees(math.atan2(b[2] - a[2], math.hypot(b[0] - a[0], b[1] - a[1])))


def cam_at(g):
    """(loc, look) in world D.  loc: push toward Eiffel 7 %/s early, then toward the hut 9 %/s; slide to the right."""
    t = (g - G0) / 30.0
    base = Vector(CAM_M)
    eif = Vector((-3.2, -213.0, 0.5))
    hut = Vector(POST_AIM)
    u = u_of(g, WHIP[0], WHIP[1] + 6)                      # camera eases from the Eiffel push to the hut push
    toward = (eif - base).normalized() * (1 - u) + (hut - base).normalized() * u
    toward.z = 0.0
    toward.normalize()
    dist = 0.2 * t if g < WHIP[0] else 0.2 * (WHIP[0] - G0) / 30.0 + 1.6 * (g - WHIP[0]) / 30.0                     # m travelled
    right = Vector((toward.y, -toward.x, 0.0))
    loc_m = base + toward * dist * 1.0 + right * (-0.65 * t if g < WHIP[0] else -0.65 * (WHIP[0] - G0) / 30.0)
    # aim
    ya = bearing(loc_m, SUMMIT) + 2.0            # a little left of the summit so the wires cross the frame
    pa = PITCH_A0 + (PITCH_A1 - PITCH_A0) * min(1.0, t / 1.5)
    yb = bearing(loc_m, POST_AIM)
    pb = PITCH_B0
    w = C.snap_u(g, WHIP[0], WHIP[1], 1.9)                 # eased whip, peak speed 1.9 x mean
    yaw = lerp(ya, yb, w)
    pitch = lerp(pa, pb, w)
    d = Vector((math.sin(math.radians(yaw)) * math.cos(math.radians(pitch)), math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
                math.sin(math.radians(pitch))))
    loc = CO.W(tuple(loc_m))
    return Vector(loc), Vector(loc) + d * 40.0


# ----------------------------------------------------------------------------- poses
def pose_eif(g):
    p = dict(cast20.STORY20["eiffel_old_point_up"][1])
    p["arm_r"] = dict(p["arm_r"], hand=(1.15, -1.25), stretch=1.3, bend=-0.3)      # the arm clearly extended UP at the summit (TAKE gate: reads as a salute)
    ph = 0.4
    p["yaw"] = 0.55 + 0.05 * math.sin(g * 0.11)
    p["lean"] = 3.0 + 1.0 * math.sin(g * 0.17)
    p["pitch"] = -0.35 + 0.03 * math.sin(g * 0.09)
    p["head_roll"] = 2.0 * math.sin(g * 0.13 + ph)
    p["gaze"] = (0.3, -0.9)
    p["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.27))
    p["blink"] = blink(g, [G0 + 21, G0 + 66])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s19")
        C.fix_antenna_wires()
        self.key_cam(bf(G0), *cam_at(G0))
        self.scene.frame_set(bf(G0))
        for o in C.bpy.data.objects:                                 # warm dusk ground (TAKE gate): no shade casters, no preset FG
            if o.name.startswith(("shade_casters", "fg_")):
                o.hide_render = True
        self.fg = []
        self.fg0 = {}
        C.warm_ground_sun(strength=2.2, color=(1.0, 0.56, 0.30))
        self.board = Vector(self.A["cams"][PRESET]["loc"])
        self.mark = C.on_ground(self.A["marks"]["eiffel_old"])
        self.actors["eif"] = C.make_actor("eif", "eiffel_old", os.path.join(WORK, "sprites"), cam=self.cam,
                                          contact=dict(width=1.2, depth=0.5, opacity=0.8))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(g))
            self.cam.data.shift_y = lerp(SHIFT_A, SHIFT_B, C.snap_u(g, WHIP[0], WHIP[1], 1.9))
            self.cam.data.keyframe_insert('shift_y', frame=f)
            C.place(self.actors["eif"], f, self.mark if g < WHIP[0] + 6 else (self.mark[0], self.mark[1], self.mark[2] - 200.0))   # fully out of frame by g 1349: parked below the ground
            loc, _ = cam_at(g)
            d = (Vector(CO.W(CAM_M)) - self.board) + 0.75 * (loc - Vector(CO.W(CAM_M)))   # FG: start offset, then 75 % of the camera's travel
            d.z = 0.0
            for o in self.fg:
                o.location = self.fg0[o.name] + d / CO.SC
                o.keyframe_insert("location", frame=f)
            self.key_set(f, wire_glow=WIRE_GLOW)                 # the wires read pale against the dusk sky (set default 0.2 is dark below the summit)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.actors["eif"].pose(f, pose_eif(g), camera=self.cam)
        self.sprites_for([(a, 200) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_at(g)
        v = look - loc
        pts = dict(summit=SUMMIT, post=POST_AIM, base=(0, 0, 0))
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), px={k: CO.project(CO.W(p)) for k, p in pts.items()})

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def camreport():
    """px/frame of the frame corners (never parked) -- uses C.CamPath-like numbers from cam_at"""
    from c20 import _corner_shift
    rows, run, worst = [], 0, 0
    for g in GS[:-1]:
        a, b = cam_at(g), cam_at(g + 1)
        sp = max(_corner_shift(a, b, 20 * CO.SC, cx, cy) for cx in (0, 720) for cy in (0, 1280))
        rows.append((g, round(sp, 1)))
        run = run + 1 if sp < 0.25 else 0
        worst = max(worst, run)
    return rows, worst


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = camreport()
        print(rows[::3])
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
