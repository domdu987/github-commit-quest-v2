#!/usr/bin/env python3
"""shot.py -- film 20 take s15 = shot 15, THE PERMIT (g 996..1091 + handles: 8 in-dissolve g 988..995, 4 out-cut g 1092..1095).
"แต่ใบอนุญาต ให้หอตั้งอยู่ ได้แค่ 20 ปี ครบแล้วต้องรื้อ" -- the permit lets the tower stand only 20 years, then it must come down.

TOWER tower_fair / DAY 1889 (set_year 1889, crowd level 3).  Eye-level two-shot in depth on the fair ground: Eiffel (proud) in front,
the official in the tricolour sash behind-right offering the sealed document; Eiffel takes it; on "ครบแล้วต้องรื้อ" (event g 1067) his smile
drops (proud -> worried + sweat, swapped on the closed frame of a 3-frame blink) and the camera SNAPS in on him.
Camera (c20.CamPath): push 8 %/s toward Eiffel's head + slide 30 px/s + arc, decay, one snap x1.55 on the drop.  Preset FG (lamp-post,
bench) moved with the camera so they stay 1-2 D from the lens.  Mouths never move (no quote here).
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

G0, G1 = C.g_bound(33.21), C.g_bound(36.44)      # 996, 1093 -> shot = g 996..1092 (plan says 996-1092)
H_IN, H_OUT = 8, 4                              # DIS 13 in: 13/2 + 2 = 8 ; hard cut out: 4
GF = G0 - H_IN                                  # first rendered frame
G_LAST = G1 + H_OUT - 1
GS = list(range(GF, G_LAST + 1))
G_PERMIT = C.cap_g("แต่ใบอนุญาต")                # ~1000
G_TWENTY = C.cap_g("ได้แค่ 20 ปี")               # ~1041
G_DROP = C.cap_g("ครบแล้วต้องรื้อ")              # 1067: smile drops + snap
SNAP = (G_DROP - 3, G_DROP + 13)
HAND = (G0 + 12, G0 + 34)                       # document handed over (official arm out, Eiffel reaches)
G_SWAP_DOC = G0 + 24                            # doc prop moves official -> Eiffel (hands meet)
BLINKS = [G0 + 10, G_DROP - 1]
LIGHT, PRESET = "DAY", "tower_fair"
YEAR = 1889
PPD = 256

# staging (world D): Eiffel at the preset mark, the official a step behind and to the right
CAM_BACK = 6.6                                  # D from the camera to Eiffel at the start
CAM_Z = 1.7
TILT0 = -8.5
FG_SHIFT = (2.7, -0.3, 0.0)
EIF_Z = 2.55                                    # head centre above the feet


def marks(A):
    e = Vector(A["marks"]["eiffel_fair"])
    return dict(eiffel=e, official=e + Vector((2.7, 1.3, 0.0)))


def cam_path(A):
    m = marks(A)
    subj = m["eiffel"] + Vector((0.9, 0.0, EIF_Z))
    c = Vector((subj.x - 1.2, subj.y - CAM_BACK, CAM_Z))
    return C.CamPath(c, subj, GF, G_LAST, push=0.10, slide_px=-40.0, rise_px=0.0, arc_deg_s=8.0, tilt0=TILT0, tilt_deg_s=2.5,
                     decay=0.25, snaps=[dict(g=SNAP, k=2.3, peak=1.9, shift=(0.0, 0.0), tilt=-4.0)])


def move_fg(A, cam_loc):
    d = Vector(cam_loc) - Vector(A["cams"][PRESET]["loc"])
    d.z = 0.0
    d = d + Vector(FG_SHIFT)                       # (right, forward) D: slide the bench out of the official's way
    for ob in C.bpy.data.objects:
        if ob.name.startswith(("fg_", "shade_casters")):
            ob.location = ob.location + d / CO.SC


def cam_path_static():
    import tower20
    cam = tower20.CAMS_M[PRESET]
    A = dict(marks=dict(eiffel_fair=CO.W((-4.4, -143.8, 0.0))), cams={PRESET: dict(loc=CO.W(cam["loc"]))})
    return cam_path(A)


# ----------------------------------------------------------------------------- poses
C.add_expression("proud_smile", eyes="happy", tilt=0.0, brows=("both", 0.10, 8.0, 0.045, 0.16, 0.012), mouth="smile")


def idle(g, ph=0.0):
    return dict(lean=3.0 * math.sin(g * 0.23 + ph), squash=(1.0, 1.0 + 0.015 * math.sin(g * 0.31 + ph)))


def official_pose(g):
    u = u_of(g, HAND[0], HAND[1])                                       # 0 doc held up, 1 arm stretched toward Eiffel
    held = g < G_SWAP_DOC
    p = dict(yaw=0.35, arm_r="hip", legs="wide")
    if held:
        p["arm_l"] = dict(hand=(lerp(-0.55, -1.15, u), lerp(0.85, 0.68, u)), bend=0.2, stretch=lerp(1.0, 1.25, u))
        p["prop_l"] = "doc_seal"
    else:
        u2 = u_of(g, G_SWAP_DOC, G_SWAP_DOC + 10)
        p["arm_l"] = dict(hand=(lerp(-1.15, -0.4, u2), lerp(0.68, 0.30, u2)), bend=0.2, stretch=lerp(1.25, 1.0, u2))
    p["expr"] = "happy" if g > G_SWAP_DOC else "stern"
    p["pitch"] = -0.05
    p.update(idle(g, 1.3))
    p["blink"] = blink(g, [G0 + 30])
    p["t"] = g / 30.0
    return p


def eiffel_pose(g):
    u = u_of(g, HAND[0], HAND[1])
    p = dict(yaw=0.40, legs=None)
    p.pop("legs")
    got = g >= G_SWAP_DOC
    if g < G_DROP:
        bl, _ = C.blink_swap(g, G_DROP, 0, 0)
    bl, ex = C.blink_swap(g, G_DROP, "proud", "worried")
    p["expr"] = ex
    if got:
        u2 = u_of(g, G_SWAP_DOC, G_SWAP_DOC + 12)
        p["arm_r"] = dict(hand=(lerp(1.0, 0.45, u2), lerp(0.62, 0.75, u2)), bend=-0.2, stretch=lerp(1.2, 1.0, u2))
        p["prop_r"] = "doc_seal"
    else:
        p["arm_r"] = dict(hand=(lerp(0.3, 1.0, u), lerp(0.2, 0.62, u)), bend=-0.2, stretch=lerp(1.0, 1.2, u))
    p["arm_l"] = "hip" if g < G_DROP else dict(hand=(-0.3, 0.98), bend=0.7)
    if g >= G_DROP:
        p["fx"] = ["sweat"]
        p["pitch"] = 0.2
        p["head_roll"] = 4.0
    p.update(idle(g, 0.4))
    p["blink"] = bl if g < G_DROP + 2 else blink(g, [G_DROP + 40])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s15")
        self.path = cam_path(self.A)
        move_fg(self.A, self.path.loc0)
        self.key_cam(bf(GF), *self.path.at(GF))
        self.scene.frame_set(bf(GF))
        self.M = {k: C.on_ground(v) for k, v in marks(self.A).items()}
        self.eif = self.actors["eif"] = C.make_actor("eif", "eiffel", os.path.join(WORK, "sprites"),
                                                     contact=dict(width=1.3, depth=0.55, opacity=0.8), cam=self.cam)
        self.off = self.actors["off"] = C.make_actor("off", "official", os.path.join(WORK, "sprites"),
                                                     contact=dict(width=1.3, depth=0.55, opacity=0.8), cam=self.cam)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.eif, f, self.M["eiffel"])
            C.place(self.off, f, self.M["official"])
            self.key_set(f, set_year=YEAR, set_crowd=3)
        self.bob_crowd(gs)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.eif.pose(f, eiffel_pose(g), camera=self.cam)
            self.off.pose(f, official_pose(g), camera=self.cam)
        self.sprites_for([(self.eif, PPD), (self.off, PPD)], [bf(g) for g in gs])

    def bob_crowd(self, gs):
        """the fair crowd cards are static placeholders: give each a small idle bob + sway (nobody frozen), keyed every frame."""
        cards = [ob for grp in CO.STATE.get("cards", []) for ob in grp]
        if not hasattr(self, "_card0"):
            self._card0 = [(ob, ob.location.copy(), ob.rotation_euler.copy()) for ob in cards]
        for g in gs:
            f = bf(g)
            for i, (ob, loc0, rot0) in enumerate(self._card0):
                ph = i * 1.9
                ob.location = (loc0.x, loc0.y, loc0.z + 0.10 * abs(math.sin(g * 0.28 + ph)))
                ob.rotation_euler = (rot0.x, rot0.y, rot0.z + 0.05 * math.sin(g * 0.13 + ph))
                ob.keyframe_insert("location", frame=f)
                ob.keyframe_insert("rotation_euler", frame=f)
                for fc in (ob.animation_data.action.fcurves if hasattr(ob.animation_data.action, "fcurves") else []):
                    for kp in fc.keyframe_points:
                        kp.interpolation = "LINEAR"

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        P = cam_path_static()
        rows, worst = P.report(GS[:-1])
        for r in rows[::4]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GF <= g <= G_LAST]
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
