#!/usr/bin/env python3
"""shot.py -- film 19 take s05 = shot 5 (g 262..355, 8.74-11.88 s) + 9 in-handle (g 253..261, hard cut in: the whip lands inside the shot)
+ 9 out-handle (g 356..364, dissolve 13 f to shot 6).  SHIP ship_rocks / STORM_DUSK, rain on, set_sea(t) / set_roll(t) keyed on EVERY frame
with the SAME t as shot 4 (t = g / 30) so the sea and the lantern continue across the cut.

"กลางทะเลไม่มีใครรู้ว่าเรืออยู่ตรงไหน เรือจมกันเป็นลำ ๆ" -- the forecastle lurches past the black rocks: the ship's roll / pitch / bob is
SCALED x3 (K_ROLL; the set's own hook is <= 1.9 deg) and keyed on ship_root, so the deck, the cards parented to it (ride_ship) and the
camera riding it (on_ship) heave together while the sea, rocks and fog stay world-fixed.  Three sailors (sailor19_a/b/c) bail with
buckets, each at its own phase (scoop low -> fling to screen-right with the water jet, comic worried faces, a stagger on every lurch);
the captain (hands behind his back) clings at the left.  The FG lantern of the preset swings on its rope in front of the lens.
Camera (c19.CamPath, on_ship): a WHIP arrival (an eased pan-in over g 262..273, from 24 deg off), then a drift push 7 %/s + slide + arc,
and ONE shake (<= 10 f, decaying, translation + tilt) on "เรือจมกัน" (caption 10.91 s = g 330).  Nobody speaks.  NO DOF / text / caption_shade.

    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] <dir> [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402
import h19_ship as SH                                    # noqa: E402

H, K, actors, cast19, bpy = C.H, C.K, C.actors, C.cast19, C.bpy
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0, G1 = C.g_bound(8.74), C.g_bound(11.88)        # 262, 356 -> shot 5 = g 262..355
H_IN, H_OUT = 9, 9
GA, GZ = G0 - H_IN, G1 + H_OUT - 1                # 253 .. 364
GS = list(range(GA, GZ + 1))
G_SINK = C.cap_g("เรือจมกัน")                     # 330: the ONE shake
SHAKE = (G_SINK, G_SINK + 9)                      # <= 10 f
WHIP = (G0, G0 + 7)
BLINKS = {"a": [275, 318], "b": [290, 340], "c": [268, 305]}

PRESET, LIGHT = "ship_rocks", "STORM_DUSK"
FINAL_SPP = 12
PPD = 256
K_ROLL = 2.2                                      # the set's roll / pitch / bob x3 (storm lurch)
HIDE = ("deck_cannon_iron", "deck_carr_w", "deck_hatchw")           # render as black blobs in the FG (QA_TECH): kept out of frame
LANT_OFF = (1.95, 0.80, 0.55)                     # FG lantern centre in the camera frame: forward, right, up (D)

CAM_LOC0 = (2.90, 25.60, 16.60)
CAM_LOOK0 = (2.00, 34.00, 14.20)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, GA, GZ, push=0.07, slide_px=15.0, rise_px=0.0, arc_deg_s=0.0, decay=0.15, snaps=[])

# sailors / captain: ship_root-space D (deck marks of the forecastle)
CPT_AT = (0.8, 38.4)
SAILORS = dict(a=dict(at=(1.5, 32.4), cast="sailor19_a", key="sailor_a_bail", ph=0.00, per=22),
               b=dict(at=(3.8, 34.2), cast="sailor19_b", key="sailor_b_bail", ph=0.37, per=26),
               c=dict(at=(2.4, 36.6), cast="sailor19_c", key="sailor_c_bail", ph=0.71, per=24))
Z_DECK = None


def whip_deg(g):
    return 30.0 * (1.0 - u_of(g, WHIP[0], WHIP[1], kind="sine")) ** 2 if g < WHIP[1] else 0.0


def shake(g):
    """decaying shake over SHAKE: (dx, dy, tilt) in D / D / rad"""
    n = g - SHAKE[0]
    if not (0 <= n < 10):
        return 0.0, 0.0, 0.0
    d = (1.0 - n / 10.0) ** 1.5
    return 0.30 * d * math.sin(n * 2.4), 0.22 * d * math.sin(n * 2.9 + 1.0), 0.05 * d * math.sin(n * 2.1)


def cam_pose(g):
    """camera (loc, look) in the ship's REST frame: drift + whip + shake"""
    loc, look = CAM.at(g)
    v = look - loc
    w = math.radians(whip_deg(g))
    if w:
        v = Matrix.Rotation(w, 3, "Z") @ v                       # looks off to the right of the subject, then swings in
    dx, dy, tl = shake(g)
    f = v.normalized()
    right = Vector((f.y, -f.x, 0.0)).normalized()
    up = right.cross(f).normalized()
    loc = loc + right * dx + up * dy
    look = loc + v + right * dx * 0.5 + up * (dy * 0.5 + tl * v.length)
    return loc, look


def ship_cam(g, f):
    loc, look = cam_pose(g)
    return C.on_ship(Take.SHIP_ROOT, f, loc, look)


def lurch(t):
    """strongly scaled ship motion (pitch, roll in rad; bob in D): the set's own _roll_rel x K_ROLL plus a slow storm roll"""
    p, r, b = SH._roll_rel(t)
    return p * K_ROLL, r * K_ROLL + 0.040 * math.sin(2 * math.pi * t / 2.6), b * 1.2


def swing(g):
    t = g / 30.0
    return 0.20 * math.sin(2 * math.pi * t / 1.7 + 0.4) + 0.03 * math.sin(2 * math.pi * t / 0.6), 0.07 * math.sin(2 * math.pi * t / 2.3)


def bail_pose(sk, g):
    S = SAILORS[sk]
    cast, base = cast19.STORY19[S["key"]]
    p = dict(base)
    u = ((g / float(S["per"])) + S["ph"]) % 1.0
    scoop = 0.5 - 0.5 * math.cos(2 * math.pi * min(1.0, u / 0.6)) if u < 0.6 else 0.0
    fling = u_of(u * 100, 60, 78) * (1 - u_of(u * 100, 84, 100)) if u >= 0.6 else 0.0
    x = lerp(0.35, 0.7, max(fling, 0.0) if u >= 0.6 else 0.0)
    y = lerp(0.05, 0.70, fling) if u >= 0.6 else lerp(0.30, 0.05, scoop)
    p["arm_r"] = dict(base["arm_r"], hand=(x, y))
    p["splash"] = clamp(fling * 1.3)
    stag = math.sin(2 * math.pi * (g / 30.0) / 1.15 + S["ph"] * 6)                # stagger with the deck
    p["lean"] = base.get("lean", 8) + 5.0 * stag + 4.0 * fling
    p["pitch"] = 0.15 + 0.06 * math.sin(2 * math.pi * g / 40.0 + S["ph"])
    p["blink"] = blink(g, BLINKS[sk])
    p["t"] = g / 30.0
    return p


def cpt_pose(g):
    cast, base = cast19.STORY19["captain_idle"]
    p = dict(base)
    t = g / 30.0
    p["expr"] = "worried" if False else base.get("expr", "neutral")
    p["lean"] = 3.0 * math.sin(2 * math.pi * t / 1.15 + 1.2)
    p["head_roll"] = 2.0 * math.sin(2 * math.pi * t / 1.7)
    p["blink"] = blink(g, [280, 332])
    p["t"] = t
    return p


class Take(C.Take):
    SHIP_ROOT = None

    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s05")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        Take.SHIP_ROOT = self.A["ship_root"]
        self.key_cam(bf(GA), *cam_pose(GA))                  # ship level here: ride_ship takes the REST inverse
        self.scene.frame_set(bf(GA))
        sd = os.path.join(WORK, "sprites")
        self.cpt = self.actors["cpt"] = C.make_actor("cpt", "captain19", sd, contact=True, cam=self.cam)
        C.ride_ship(self.cpt, self.A["ship_root"])
        self.sl = {}
        for k, S in SAILORS.items():
            a = self.actors[k] = self.sl[k] = C.make_actor(k, S["cast"], sd, contact=True, cam=self.cam)
            C.ride_ship(a, self.A["ship_root"])
        for n in HIDE:
            ob = bpy.data.objects.get(n)
            if ob is not None:
                ob.hide_render = True
                ob.hide_viewport = True
        self._hang_lantern()

    def _hang_lantern(self):
        bpy.context.view_layer.update()
        names = [o for o in bpy.data.objects if o.name.startswith("fglantern_")]
        light = bpy.data.objects.get("lampfg")
        root = self.A["ship_root"]
        p = Vector(light.location)
        self.lant_top = root.matrix_world @ (p + Vector((-0.04, 0.0, 3.0)) * 0.46 * 1.85)
        piv = bpy.data.objects.new("lant_pivot", None)
        bpy.context.scene.collection.objects.link(piv)
        piv.matrix_world = Matrix.Translation(self.lant_top)
        bpy.context.view_layer.update()
        for o in names + ([light] if light is not None else []):
            mw = o.matrix_world.copy()
            o.parent = piv
            o.matrix_parent_inverse = piv.matrix_world.inverted() @ mw
        self.rope_len = (self.lant_top - p).length 
        piv.rotation_mode = "XYZ"
        piv.scale = (1.0, 1.0, 1.0)
        self.piv = piv

    def key_lantern(self, g, f, loc, look):
        fwd = (look - loc).normalized()
        right = Vector((fwd.y, -fwd.x, 0.0)).normalized()
        up = right.cross(fwd).normalized()
        centre = loc + fwd * LANT_OFF[0] + right * LANT_OFF[1] + up * LANT_OFF[2]
        top = centre + Vector((0, 0, 1)) * self.rope_len
        fh = Vector((fwd.x, fwd.y, 0.0)).normalized()
        a, b = swing(g)
        R = Matrix.Rotation(a, 3, fh) @ Matrix.Rotation(b, 3, right)
        self.piv.location = top
        self.piv.rotation_euler = R.to_euler("XYZ")
        for pr in ("location", "rotation_euler", "scale"):
            self.piv.keyframe_insert(pr, frame=f)

    def key_ship(self, g, f):
        t = g / 30.0
        H.set_sea(t, frame=f)
        pitch, roll, bob = lurch(t)
        root = self.A["ship_root"]
        root.rotation_euler = (pitch, roll, 0.0)
        root.location = (0.0, 0.0, bob * SH.SC)
        K._keyxf(root, f, loc=True, rot=True)

    def pose(self, gs):
        mk = self.A["marks"]
        z = mk["captain_bow"][2]
        for g in gs:
            f = bf(g)
            self.key_ship(g, f)                              # BEFORE the camera (on_ship reads the keyed root)
            H.set_rain(True, frame=f)
            loc, look = ship_cam(g, f)
            self.key_cam(f, loc, look)
            C.place(self.cpt, f, Vector((CPT_AT[0], CPT_AT[1], z)))
            for k, S in SAILORS.items():
                C.place(self.sl[k], f, Vector((S["at"][0], S["at"][1], z)))
            self.key_lantern(g, f, loc, look)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.cpt.pose(f, cpt_pose(g), camera=self.cam)
            for k in SAILORS:
                self.sl[k].pose(f, bail_pose(k, g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = ship_cam(g, f)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof, caption_shade=bool(bpy.data.objects.get("caption_shade")))

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
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GZ]
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
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
